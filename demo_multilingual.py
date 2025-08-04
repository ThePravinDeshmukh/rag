#!/usr/bin/env python3
"""
Multilingual RAG Demo
Showcase Hindi/Marathi text extraction and search capabilities
"""

from rag import EnhancedRAG
import sys

def demo_multilingual():
    """Demo the multilingual capabilities"""
    print("🌏 Multilingual RAG System Demo")
    print("=" * 50)
    print("This system can extract and search cereal data in multiple languages!")
    print()
    
    # Initialize
    rag = EnhancedRAG()
    
    # Load document
    print("📄 Loading cereal exchange data...")
    success = rag.load_pdf('docs/cereal.pdf')
    if not success:
        print("❌ Could not load cereal.pdf")
        return
    
    rag.build_index()
    print(f"✅ Loaded {len(rag.structured_data)} cereal items with multilingual support")
    print()
    
    # Demo queries
    demo_queries = [
        {
            'query': 'weight of rice',
            'description': 'Basic weight query with Hindi/Marathi names'
        },
        {
            'query': 'rice multilingual',
            'description': 'Show all rice items with their local names'
        },
        {
            'query': 'list wheat items with hindi names',
            'description': 'Wheat items with Hindi translations'
        },
        {
            'query': 'show bajra',
            'description': 'Pearl millet information'
        },
        {
            'query': 'list all items with marathi names',
            'description': 'All items showing Marathi names'
        }
    ]
    
    for i, demo in enumerate(demo_queries, 1):
        print(f"🔍 Demo {i}: {demo['description']}")
        print(f"❓ Query: '{demo['query']}'")
        print()
        
        answer = rag.ask(demo['query'])
        print(f"💬 Answer:")
        print(answer)
        print()
        print("-" * 60)
        print()
    
    print("🎉 Demo complete!")
    print()
    print("📝 Key Features Demonstrated:")
    print("• Automatic extraction of Hindi/Marathi text from PDFs")
    print("• Weight queries return local language names")
    print("• Search works across English, Hindi, and Marathi")
    print("• Clean table format with multilingual columns")
    print("• Structured data with 80+ cereal items")

if __name__ == "__main__":
    demo_multilingual()
