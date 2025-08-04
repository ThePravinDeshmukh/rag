"""
Simple RAG System - Everything in one file
Clean, minimal implementation for PDF Q&A
"""

import os
import numpy as np
import faiss
import torch
from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer
from transformers import AutoModelForCausalLM, AutoTokenizer


class SimpleRAG:
    """Minimal RAG system - everything you need in one class"""
    
    def __init__(self):
        """Initialize with lightweight models"""
        print("🤖 Initializing Simple RAG...")
        
        # Device detection
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Device: {self.device}")
        
        # Load models
        print("Loading models...")
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
        
        try:
            self.tokenizer = AutoTokenizer.from_pretrained("distilgpt2")
            self.model = AutoModelForCausalLM.from_pretrained("distilgpt2")
            self.tokenizer.pad_token = self.tokenizer.eos_token
        except Exception as e:
            print(f"Model loading failed: {e}")
            self.model = None
            self.tokenizer = None
        
        # Storage
        self.chunks = []
        self.embeddings = None
        self.index = None
        self.sources = []  # Track which document each chunk came from
        
        print("✅ Simple RAG ready!")
    
    def load_pdf(self, pdf_path):
        """Load a single PDF file"""
        try:
            print(f"📄 Loading: {os.path.basename(pdf_path)}")
            reader = PdfReader(pdf_path)
            text = ""
            
            for page in reader.pages:
                text += page.extract_text() + "\\n"
            
            # Split into chunks
            words = text.split()
            chunk_size = 300
            overlap = 50
            
            for i in range(0, len(words), chunk_size - overlap):
                chunk = " ".join(words[i:i + chunk_size])
                if len(chunk.strip()) > 50:  # Only meaningful chunks
                    self.chunks.append(chunk.strip())
                    self.sources.append(os.path.basename(pdf_path))
            
            print(f"✅ Created {len(self.chunks)} chunks")
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
        """Build search index from chunks"""
        if not self.chunks:
            print("❌ No chunks to index")
            return False
        
        print("🔍 Building search index...")
        
        # Create embeddings
        self.embeddings = self.embedder.encode(self.chunks, show_progress_bar=True)
        
        # Build FAISS index
        dimension = self.embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(np.array(self.embeddings).astype('float32'))
        
        print("✅ Index built successfully")
        return True
    
    def search(self, question, top_k=3):
        """Search for relevant chunks"""
        if self.index is None:
            return []
        
        # Get question embedding
        query_embedding = self.embedder.encode([question])
        
        # Search
        distances, indices = self.index.search(
            np.array(query_embedding).astype('float32'), top_k
        )
        
        # Return results with sources
        results = []
        for idx in indices[0]:
            if idx < len(self.chunks):
                results.append({
                    'text': self.chunks[idx],
                    'source': self.sources[idx]
                })
        
        return results
    
    def generate_answer(self, question, context):
        """Generate answer from context"""
        if not self.model:
            # Fallback: extract from context
            sentences = context.split('.')[:3]
            return ". ".join(sentences) + "."
        
        try:
            prompt = f"Context: {context[:500]}\\n\\nQuestion: {question}\\nAnswer:"
            
            inputs = self.tokenizer.encode(prompt, return_tensors="pt", max_length=300, truncation=True)
            
            with torch.no_grad():
                outputs = self.model.generate(
                    inputs,
                    max_new_tokens=80,
                    temperature=0.7,
                    do_sample=True,
                    pad_token_id=self.tokenizer.eos_token_id
                )
            
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            if "Answer:" in response:
                answer = response.split("Answer:")[-1].strip()
                if len(answer) > 10:
                    return answer
            
            # Fallback
            sentences = context.split('.')[:2]
            return ". ".join(sentences) + "."
            
        except Exception as e:
            print(f"Generation error: {e}")
            sentences = context.split('.')[:2]
            return ". ".join(sentences) + "."
    
    def ask(self, question):
        """Main method: ask a question and get an answer"""
        if not self.chunks:
            return "❌ No documents loaded. Use load_pdf() or load_folder() first."
        
        if self.index is None:
            return "❌ No index built. Use build_index() first."
        
        # Search for relevant chunks
        results = self.search(question)
        if not results:
            return "❌ No relevant information found."
        
        # Combine context
        context = "\\n\\n".join([r['text'] for r in results])
        sources = list(set([r['source'] for r in results]))
        
        # Generate answer
        answer = self.generate_answer(question, context)
        
        # Add sources
        if sources:
            answer += f"\\n\\n📚 Sources: {', '.join(sources)}"
        
        return answer


def main():
    """Simple command-line interface"""
    print("🤖 Simple RAG System")
    print("="*30)
    
    rag = SimpleRAG()
    
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
    
    print("\\n💬 Ask questions (type 'quit' to exit):")
    
    while True:
        try:
            question = input("\\n❓ Question: ").strip()
            
            if question.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
            
            if not question:
                continue
            
            print("🤔 Thinking...")
            answer = rag.ask(question)
            print(f"💡 {answer}")
            
        except KeyboardInterrupt:
            print("\\n👋 Goodbye!")
            break


if __name__ == "__main__":
    main()
