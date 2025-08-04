"""
Quick Demo - Test the simple RAG system
Run: python demo_simple.py
"""

from rag_simple import SimpleRAG
import os

def main():
    print("🧪 Simple RAG Demo")
    print("="*20)
    
    # Create a sample document if none exists
    docs_folder = "docs"
    if not os.path.exists(docs_folder):
        os.makedirs(docs_folder)
        print(f"📁 Created {docs_folder}/ folder")
        print("📄 Add PDF files to this folder and run again")
        return
    
    # Initialize RAG
    rag = SimpleRAG()
    
    # Load documents
    if rag.load_folder(docs_folder):
        rag.build_index()
    else:
        print("❌ No PDFs found. Add PDF files to docs/ folder")
        return
    
    # Demo questions
    questions = [
        "What is this document about?",
        "What are the main points?",
        "Can you summarize the content?"
    ]
    
    print("\\n🎯 Demo Questions:")
    print("-"*30)
    
    for i, question in enumerate(questions, 1):
        print(f"\\n{i}. {question}")
        answer = rag.ask(question)
        print(f"💡 {answer}")
    
    print("\\n✅ Demo completed!")
    print("💡 For interactive mode, run: python rag_simple.py")
    print("🌐 For web interface, run: python web_app.py")

if __name__ == "__main__":
    main()
