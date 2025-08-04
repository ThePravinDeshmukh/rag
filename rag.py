"""
Enhanced RAG System - Optimized for structured data extraction
Better handling of numerical data, tables, and precise information retrieval
"""

import os
import numpy as np
import faiss
import torch
import re
from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer
from transformers import AutoModelForCausalLM, AutoTokenizer


class EnhancedRAG:
    """Enhanced RAG system with better structured data handling"""
    
    def __init__(self):
        """Initialize with lightweight models and lazy loading for memory optimization"""
        print("🤖 Initializing Enhanced RAG...")
        
        # Device detection (CPU only for free tier)
        self.device = "cpu"  # Force CPU for Render.com free tier
        print(f"Device: {self.device}")
        
        # Initialize containers
        self.chunks = []
        self.structured_data = []  # Store structured entries separately
        self.embeddings = None
        self.index = None
        self.sources = []
        
        # Lazy load models (don't load until needed to save memory)
        self.embedder = None
        
        print("✅ Enhanced RAG ready!")
    
    def _ensure_models_loaded(self):
        """Lazy load models only when needed"""
        if self.embedder is None:
            print("📦 Loading embedding model...")
            self.embedder = SentenceTransformer('all-MiniLM-L6-v2', device=self.device)
    
    def extract_structured_data(self, text, source_file):
        """Extract structured data (item-weight pairs) from text with item-weight on separate lines"""
        structured_entries = []
        lines = text.split('\n')
        
        for i in range(len(lines) - 1):
            current_line = lines[i].strip()
            next_line = lines[i + 1].strip()
            
            # Skip empty lines or very short lines
            if not current_line or len(current_line) < 5:
                continue
            
            # Skip header lines
            if any(skip in current_line.lower() for skip in ['cereal exchange', 'marathi names', 'hindi names', 'pictures', 'grams for']):
                continue
            
            # Check if current line has item name and next line is just a weight number
            if (any(c.isalpha() for c in current_line) and  # Has letters (item name)
                next_line and  # Next line exists
                re.match(r'^\s*\d+\.?\d*\s*$', next_line)):  # Next line is just a number
                
                # Extract multilingual names from current line
                multilingual_names = self.extract_multilingual_names(current_line)
                english_name = multilingual_names['english']
                
                if english_name and len(english_name.strip()) > 2:
                    try:
                        weight_val = float(next_line.strip())
                        structured_entries.append({
                            'item': english_name.strip(),
                            'full_item': current_line,
                            'multilingual': multilingual_names,
                            'weight': weight_val,
                            'weight_str': f"{weight_val} grams",
                            'source': source_file,
                            'original_line': f"{current_line} | {next_line}"
                        })
                    except ValueError:
                        continue
            
            # Handle complex multi-line entries (like Oats entries)
            # Look ahead for weight on lines i+2, i+3, i+4
            elif any(c.isalpha() for c in current_line):
                
                # Check up to 4 lines ahead for a weight
                for look_ahead in range(2, 5):
                    if i + look_ahead < len(lines):
                        future_line = lines[i + look_ahead].strip()
                        if re.match(r'^\s*\d+\.?\d*\s*$', future_line):
                            
                            # For multi-line items, combine lines to get full context
                            if look_ahead == 2:
                                # Weight 2 lines ahead - combine current + next
                                combined_item = current_line + " " + next_line
                            elif look_ahead == 3:
                                # Weight 3 lines ahead - combine current + next + line after
                                line_plus_2 = lines[i + 2].strip() if i + 2 < len(lines) else ""
                                combined_item = current_line + " " + next_line + " " + line_plus_2
                            else:
                                # Weight 4 lines ahead
                                line_plus_2 = lines[i + 2].strip() if i + 2 < len(lines) else ""
                                line_plus_3 = lines[i + 3].strip() if i + 3 < len(lines) else ""
                                combined_item = current_line + " " + next_line + " " + line_plus_2 + " " + line_plus_3
                            
                            multilingual_names = self.extract_multilingual_names(combined_item)
                            english_name = multilingual_names['english']
                            
                            if english_name and len(english_name.strip()) > 2:
                                # Avoid duplicates by checking if we already have this item
                                existing_items = [entry['item'].lower() for entry in structured_entries]
                                if english_name.strip().lower() not in existing_items:
                                    try:
                                        weight_val = float(future_line.strip())
                                        structured_entries.append({
                                            'item': english_name.strip(),
                                            'full_item': combined_item,
                                            'multilingual': multilingual_names,
                                            'weight': weight_val,
                                            'weight_str': f"{weight_val} grams",
                                            'source': source_file,
                                            'original_line': f"{combined_item} | {future_line}"
                                        })
                                        break  # Found weight, stop looking ahead
                                    except ValueError:
                                        continue
        
        return structured_entries
    
    def extract_english_name(self, text):
        """Extract English item name from multilingual text"""
        # Clean up the text and extract the English portion
        
        # First approach: take everything before first non-Latin character
        english_chars = []
        for char in text:
            if char.isalpha() and ord(char) < 128:  # Latin letters only
                english_chars.append(char)
            elif char in [' ', '-', '.']:  # Allow spaces, hyphens, dots
                english_chars.append(char)
            else:
                break  # Stop at first non-English character
        
        english_part = ''.join(english_chars).strip()
        
        # Clean up multiple spaces and trailing punctuation
        english_part = re.sub(r'\s+', ' ', english_part)
        english_part = english_part.strip('. -')
        
        return english_part

    def extract_multilingual_names(self, text):
        """Extract and preserve all language versions (English, Hindi, Marathi)"""
        # Split the text into parts and identify different language sections
        parts = text.split()
        
        english_words = []
        hindi_words = []
        marathi_words = []
        
        for word in parts:
            if word.strip():
                # Check character composition
                has_latin = any(ord(char) < 128 and char.isalpha() for char in word)
                has_devanagari = any(0x0900 <= ord(char) <= 0x097F for char in word)  # Hindi/Marathi Unicode range
                
                if has_latin and not has_devanagari:
                    english_words.append(word)
                elif has_devanagari:
                    # Could be Hindi or Marathi - for now group together
                    if any(char in word for char in ['ा', 'ी', 'ू', 'े', 'ो']):  # Common Devanagari vowels
                        hindi_words.append(word)
                    else:
                        marathi_words.append(word)
        
        return {
            'english': ' '.join(english_words).strip(),
            'hindi': ' '.join(hindi_words).strip(),
            'marathi': ' '.join(marathi_words).strip(),
            'full_text': text.strip()
        }
    
    def load_pdf(self, pdf_path):
        """Load a single PDF file with enhanced data extraction"""
        try:
            print(f"📄 Loading: {os.path.basename(pdf_path)}")
            reader = PdfReader(pdf_path)
            text = ""
            
            for page in reader.pages:
                text += page.extract_text() + "\n"
            
            source_name = os.path.basename(pdf_path)
            
            # Extract structured data first
            structured = self.extract_structured_data(text, source_name)
            self.structured_data.extend(structured)
            print(f"📊 Extracted {len(structured)} structured items")
            
            # Create enhanced chunks
            words = text.split()
            chunk_size = 200  # Smaller chunks for better precision
            overlap = 50
            
            for i in range(0, len(words), chunk_size - overlap):
                chunk = " ".join(words[i:i + chunk_size])
                if len(chunk.strip()) > 50:
                    self.chunks.append(chunk.strip())
                    self.sources.append(source_name)
            
            print(f"✅ Created {len(self.chunks)} text chunks")
            return True
            
        except Exception as e:
            print(f"❌ Error loading PDF: {e}")
            return False
    
    def load_folder(self, folder_path):
        """Load all PDFs from a folder"""
        if not os.path.exists(folder_path):
            print(f"❌ Folder not found: {folder_path}")
            return False
        
        pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]
        if not pdf_files:
            print(f"❌ No PDFs found in {folder_path}")
            return False
        
        print(f"📁 Found {len(pdf_files)} PDFs")
        for pdf_file in pdf_files:
            self.load_pdf(os.path.join(folder_path, pdf_file))
        
        return len(self.chunks) > 0
    
    def build_index(self):
        """Build search index from chunks with lazy model loading"""
        if not self.chunks:
            print("❌ No chunks to index")
            return False
        
        print("🔍 Building search index...")
        
        # Ensure models are loaded
        self._ensure_models_loaded()
        
        # Create embeddings for text chunks
        self.embeddings = self.embedder.encode(self.chunks, show_progress_bar=True)
        
        # Build FAISS index
        dimension = self.embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(np.array(self.embeddings).astype('float32'))
        
        print("✅ Index built successfully")
        return True
    
    def search_structured_data(self, query):
        """Search structured data for specific items and weights"""
        query_lower = query.lower()
        results = []
        
        # Handle special weight-based queries
        if any(phrase in query_lower for phrase in ['lowest weight', 'lightest', 'minimum weight', 'smallest weight']):
            return self.search_by_weight_order(query, ascending=True)
        elif any(phrase in query_lower for phrase in ['highest weight', 'heaviest', 'maximum weight', 'largest weight']):
            return self.search_by_weight_order(query, ascending=False)
        
        # Extract key search terms, removing common words
        search_terms = []
        query_words = query_lower.split()
        
        # Remove common words that shouldn't affect search
        stop_words = {'list', 'all', 'show', 'me', 'the', 'what', 'is', 'are', 'with', 'items', 'weight', 'grams', 'of', 'give', 'which', 'have'}
        for word in query_words:
            if word not in stop_words and len(word) > 2:
                search_terms.append(word)
        
        # If no meaningful terms, return empty
        if not search_terms:
            return []
        
        # Direct item name matching with improved logic
        exact_matches = []
        partial_matches = []
        
        for entry in self.structured_data:
            item_lower = entry['item'].lower()
            full_item_lower = entry.get('full_item', '').lower()
            
            # Check for exact word matches
            item_words = item_lower.split()
            full_words = full_item_lower.split()
            
            exact_match = False
            partial_match = False
            
            for search_term in search_terms:
                # Handle special cases for common food terms
                if search_term == 'bajra' and ('millet' in item_lower or 'bajra' in full_item_lower):
                    exact_match = True
                    break
                elif search_term == 'rice' and 'rice' in item_words:
                    exact_match = True
                    break
                elif search_term == 'wheat' and 'wheat' in item_words:
                    exact_match = True
                    break
                elif search_term in item_words:
                    exact_match = True
                    break
                elif search_term in item_lower:
                    partial_match = True
            
            if exact_match:
                exact_matches.append(entry)
            elif partial_match:
                partial_matches.append(entry)
        
        # Return exact matches first, then partial matches
        results = exact_matches + partial_matches
        
        return results
    
    def search_by_weight_order(self, query, ascending=True):
        """Search for items by weight order (lowest/highest)"""
        query_lower = query.lower()
        
        # Determine what type of items to filter for
        category_filters = {
            'vegetable': ['vegetable', 'leafy', 'root'],
            'fruit': ['fruit'],
            'cereal': ['cereal', 'grain', 'rice', 'wheat', 'oats'],
            'legume': ['legume', 'bean', 'dal', 'lentil', 'pea'],
        }
        
        # Find which category is mentioned in query
        target_category = None
        target_items = []
        
        for category, keywords in category_filters.items():
            if any(keyword in query_lower for keyword in keywords):
                target_category = category
                break
        
        # Filter items based on category and source
        filtered_items = []
        
        for entry in self.structured_data:
            item_lower = entry['item'].lower()
            source = entry.get('source', '').lower()
            
            # If specific category mentioned, filter by it
            if target_category == 'vegetable':
                if any(source_pattern in source for source_pattern in ['vegetable exchange', 'leafy vegetable', 'root vegetable']):
                    filtered_items.append(entry)
            elif target_category == 'fruit':
                if 'fruit' in source:
                    filtered_items.append(entry)
            elif target_category == 'cereal':
                if 'cereal' in source:
                    filtered_items.append(entry)
            elif target_category == 'legume':
                if 'legume' in source:
                    filtered_items.append(entry)
            else:
                # If no specific category, include all but prefer common vegetables
                if any(veg_word in item_lower for veg_word in [
                    'carrot', 'potato', 'onion', 'tomato', 'cabbage', 'spinach', 
                    'beetroot', 'radish', 'cucumber', 'brinjal', 'cauliflower', 
                    'broccoli', 'lettuce', 'capsicum', 'green', 'leafy'
                ]) or any(source_pattern in source for source_pattern in ['vegetable exchange', 'leafy vegetable', 'root vegetable']):
                    filtered_items.append(entry)
        
        # Sort by weight
        filtered_items.sort(key=lambda x: x.get('weight', float('inf')), reverse=not ascending)
        
        # Extract number from query (default to 5)
        import re
        number_match = re.search(r'(\d+)', query)
        limit = int(number_match.group(1)) if number_match else 5
        
        # Return top N items
        return filtered_items[:limit]
    
    def search_weight_query(self, query):
        """Handle specific weight queries like 'weight of rice'"""
        query_lower = query.lower()
        
        # Extract item name from weight queries
        weight_patterns = [
            r'weight of (\w+)',
            r'(\w+) weight',
            r'how much (\w+)',
            r'grams of (\w+)',
            r'(\w+) grams'
        ]
        
        item_name = None
        for pattern in weight_patterns:
            match = re.search(pattern, query_lower)
            if match:
                item_name = match.group(1)
                break
        
        if item_name:
            # Search for items containing this name, prioritize exact matches
            exact_matches = []
            partial_matches = []
            
            for entry in self.structured_data:
                entry_lower = entry['item'].lower()
                if entry_lower == item_name:
                    exact_matches.append(entry)
                elif item_name in entry_lower:
                    partial_matches.append(entry)
            
            # Return exact matches first, then partial matches
            results = exact_matches + partial_matches
            return results, item_name
        
        return [], None

    def search_multilingual(self, query, language=None):
        """Search for items in specific languages or show multilingual information"""
        if not self.structured_data:
            return []
        
        query_lower = query.lower()
        matching_entries = []
        
        for entry in self.structured_data:
            if 'multilingual' not in entry:
                continue
                
            ml = entry['multilingual']
            
            # If specific language requested
            if language:
                if language.lower() == 'hindi' and ml.get('hindi'):
                    if any(word in ml['hindi'].lower() for word in query_lower.split()):
                        matching_entries.append(entry)
                elif language.lower() == 'marathi' and ml.get('marathi'):
                    if any(word in ml['marathi'].lower() for word in query_lower.split()):
                        matching_entries.append(entry)
            else:
                # Search in all available languages
                if (any(word in entry['item'].lower() for word in query_lower.split()) or
                    (ml.get('hindi') and any(word in ml['hindi'].lower() for word in query_lower.split())) or
                    (ml.get('marathi') and any(word in ml['marathi'].lower() for word in query_lower.split()))):
                    matching_entries.append(entry)
        
        return matching_entries
    
    def format_structured_results(self, results, query_type="general", include_multilingual=True, output_format="markdown"):
        """Format structured data results with optional multilingual support"""
        if not results:
            return None
        
        if query_type == "weight" and len(results) == 1:
            # Single exact weight answer
            entry = results[0]
            formatted = f"**{entry['item']}**: {entry['weight_str']}"
            
            # Add multilingual names if available and requested
            if include_multilingual and 'multilingual' in entry:
                ml = entry['multilingual']
                if ml.get('hindi') or ml.get('marathi'):
                    formatted += "\n\n🌏 **Other names:**"
                    if ml.get('hindi'):
                        formatted += f"\n• Hindi: {ml['hindi']}"
                    if ml.get('marathi'):
                        formatted += f"\n• Marathi: {ml['marathi']}"
            
            return formatted
        
        elif query_type == "weight" and len(results) > 1:
            # Multiple results for weight query - show the most relevant first
            entry = results[0]
            formatted = f"**{entry['item']}**: {entry['weight_str']}"
            
            # Add multilingual for main result
            if include_multilingual and 'multilingual' in entry:
                ml = entry['multilingual']
                if ml.get('hindi') or ml.get('marathi'):
                    formatted += " 🌏"
                    if ml.get('hindi'):
                        formatted += f" (Hindi: {ml['hindi']})"
                    if ml.get('marathi'):
                        formatted += f" (Marathi: {ml['marathi']})"
            
            if len(results) > 1:
                formatted += f"\n\n📋 **Other {results[0]['item'].split()[0]} items:**\n"
                for entry in results[1:5]:  # Show up to 4 more
                    item_line = f"• **{entry['item']}**: {entry['weight_str']}"
                    if include_multilingual and 'multilingual' in entry:
                        ml = entry['multilingual']
                        if ml.get('hindi'):
                            item_line += f" (Hindi: {ml['hindi']})"
                    formatted += item_line + "\n"
                if len(results) > 5:
                    formatted += f"... and {len(results) - 5} more"
            return formatted
        
        elif output_format == "html":
            # HTML table format for web interface
            formatted = "<div class='table-container'>"
            formatted += "<h3>📊 Items found:</h3>"
            formatted += "<table class='results-table'>"
            if include_multilingual:
                formatted += "<tr><th>Item</th><th>Weight</th><th>Other Names</th></tr>"
                for entry in results[:20]:  # Limit to 20 for web display
                    other_names = ""
                    if 'multilingual' in entry:
                        ml = entry['multilingual']
                        names = []
                        if ml.get('hindi'):
                            names.append(f"Hindi: {ml['hindi']}")
                        if ml.get('marathi'):
                            names.append(f"Marathi: {ml['marathi']}")
                        other_names = " | ".join(names)
                    formatted += f"<tr><td><strong>{entry['item']}</strong></td><td>{entry['weight_str']}</td><td>{other_names}</td></tr>"
            else:
                formatted += "<tr><th>Item</th><th>Weight</th></tr>"
                for entry in results[:20]:
                    formatted += f"<tr><td><strong>{entry['item']}</strong></td><td>{entry['weight_str']}</td></tr>"
            formatted += "</table>"
            if len(results) > 20:
                formatted += f"<p>... and {len(results) - 20} more items.</p>"
            formatted += "</div>"
            return formatted
            
        elif len(results) <= 8:
            # Table format for moderate results - enhanced with multilingual
            formatted = "📊 **Items found:**\n\n"
            if include_multilingual:
                formatted += "| Item | Weight | Other Names |\n"
                formatted += "|------|--------|-------------|\n"
                for entry in results:
                    other_names = ""
                    if 'multilingual' in entry:
                        ml = entry['multilingual']
                        names = []
                        if ml.get('hindi'):
                            names.append(f"Hindi: {ml['hindi']}")
                        if ml.get('marathi'):
                            names.append(f"Marathi: {ml['marathi']}")
                        other_names = " | ".join(names)
                    formatted += f"| **{entry['item']}** | {entry['weight_str']} | {other_names} |\n"
            else:
                formatted += "| Item | Weight |\n"
                formatted += "|------|--------|\n"
                for entry in results:
                    formatted += f"| **{entry['item']}** | {entry['weight_str']} |\n"
            return formatted
        
        else:
            # Summarized format for many results
            total = len(results)
            formatted = f"📊 **Found {total} items:**\n\n"
            formatted += "| Item | Weight | Hindi/Marathi |\n"
            formatted += "|------|--------|---------------|\n"
            for i, entry in enumerate(results[:8]):
                other_names = ""
                if include_multilingual and 'multilingual' in entry:
                    ml = entry['multilingual']
                    if ml.get('hindi') or ml.get('marathi'):
                        other_names = ml.get('hindi', '') or ml.get('marathi', '')
                formatted += f"| **{entry['item']}** | {entry['weight_str']} | {other_names} |\n"
            if total > 8:
                formatted += f"\n... and {total - 8} more items."
            return formatted
    
    def ask(self, question, web_format=False):
        """Enhanced question answering with structured data priority"""
        if not self.chunks and not self.structured_data:
            return "❌ No documents loaded. Use load_pdf() or load_folder() first."
        
        question_lower = question.lower()
        output_format = "html" if web_format else "markdown"
        
        # 1. Check for multilingual queries
        if any(word in question_lower for word in ['hindi', 'marathi', 'multilingual', 'names', 'translations']):
            if 'hindi' in question_lower:
                multilingual_results = self.search_multilingual(question, 'hindi')
            elif 'marathi' in question_lower:
                multilingual_results = self.search_multilingual(question, 'marathi')
            else:
                multilingual_results = self.search_multilingual(question)
            
            if multilingual_results:
                answer = self.format_structured_results(multilingual_results, "list", include_multilingual=True, output_format=output_format)
                if answer:
                    sources = list(set([r['source'] for r in multilingual_results]))
                    source_text = f"📚 Source: {', '.join(sources)}" if not web_format else f"<p><em>Source: {', '.join(sources)}</em></p>"
                    return f"{answer}\n\n{source_text}"
        
        # 2. Check for weight-specific queries
        weight_results, item_name = self.search_weight_query(question)
        if weight_results:
            answer = self.format_structured_results(weight_results, "weight", output_format=output_format)
            if answer:
                sources = list(set([r['source'] for r in weight_results]))
                source_text = f"📚 Source: {', '.join(sources)}" if not web_format else f"<p><em>Source: {', '.join(sources)}</em></p>"
                return f"{answer}\n\n{source_text}"
        
        # 3. Check for general structured data queries
        if any(word in question_lower for word in ['list', 'all', 'items', 'cereals', 'weight']):
            structured_results = self.search_structured_data(question)
            if structured_results:
                answer = self.format_structured_results(structured_results, "list", output_format=output_format)
                if answer:
                    sources = list(set([r['source'] for r in structured_results]))
                    source_text = f"📚 Source: {', '.join(sources)}" if not web_format else f"<p><em>Source: {', '.join(sources)}</em></p>"
                    return f"{answer}\n\n{source_text}"
        
        # 4. Try structured data search for any food item queries
        structured_results = self.search_structured_data(question)
        if structured_results:
            answer = self.format_structured_results(structured_results, "list", output_format=output_format)
            if answer:
                sources = list(set([r['source'] for r in structured_results]))
                source_text = f"📚 Source: {', '.join(sources)}" if not web_format else f"<p><em>Source: {', '.join(sources)}</em></p>"
                return f"{answer}\n\n{source_text}"
        
        # 5. Fall back to regular semantic search
        if self.index is None:
            return "❌ No index built. Use build_index() first."
        
        # Regular semantic search
        query_embedding = self.embedder.encode([question])
        distances, indices = self.index.search(
            np.array(query_embedding).astype('float32'), 3
        )
        
        results = []
        for idx in indices[0]:
            if idx < len(self.chunks):
                results.append({
                    'text': self.chunks[idx],
                    'source': self.sources[idx]
                })
        
        if not results:
            return "❌ No relevant information found."
        
        # Generate answer from context
        context = "\n\n".join([r['text'] for r in results])
        sources = list(set([r['source'] for r in results]))
        
        # Simple extractive answer
        sentences = context.split('.')[:3]
        answer = ". ".join(sentences) + "."
        
        return f"{answer}\n\n📚 Sources: {', '.join(sources)}"


def main():
    """Enhanced command-line interface"""
    print("🤖 Enhanced RAG System - Better Structured Data Handling")
    print("="*60)
    
    rag = EnhancedRAG()
    
    # Try to load documents
    if os.path.exists('docs'):
        if rag.load_folder('docs'):
            rag.build_index()
        else:
            print("❌ No documents loaded from docs/ folder")
            return
    else:
        print("📁 Create a 'docs/' folder and add PDF files")
        return
    
    print(f"\n📊 Loaded {len(rag.structured_data)} structured items")
    print("💬 Ask questions (type 'quit' to exit):")
    print("💡 Try: 'weight of rice', 'list all rice items', 'oats weight'")
    
    while True:
        try:
            question = input("\n❓ Question: ").strip()
            
            if question.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
            
            if not question:
                continue
            
            print("🤔 Searching...")
            answer = rag.ask(question)
            print(f"💡 {answer}")
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break


if __name__ == "__main__":
    main()
