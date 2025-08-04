"""
Legacy RAG Module - Backward compatibility wrapper
Provides the original PDFRAGSystem interface
"""

import os
from rag_core import RAGCore


class PDFRAGSystem:
    """Legacy wrapper for backward compatibility"""
    
    def __init__(self, model_name="facebook/opt-350m"):
        """Initialize RAG system (legacy interface)"""
        print("⚠️  Using legacy PDFRAGSystem interface")
        print("💡 Consider using RAGCore directly for new projects")
        self.rag_core = RAGCore()
        self.chunks = []
        self.chunk_metadata = []
        self.loaded_documents = []
    
    def load_pdf_and_build_index(self, pdf_path):
        """Load single PDF (legacy method)"""
        return self.rag_core.load_single_pdf(pdf_path)
    
    def load_multiple_pdfs_and_build_index(self, docs_folder):
        """Load multiple PDFs (legacy method)"""
        return self.rag_core.load_multiple_pdfs(docs_folder)
    
    def ask_question(self, question):
        """Ask question (legacy method)"""
        return self.rag_core.ask_question(question)
    
    def get_loaded_documents(self):
        """Get loaded documents (legacy method)"""
        return self.rag_core.get_loaded_documents()
    
    def search_in_specific_document(self, question, document_name, top_k=3):
        """Search in specific document (legacy method)"""
        return self.rag_core.search_in_document(question, document_name, top_k)
    
    # Legacy methods for compatibility
    def extract_text_from_pdf(self, pdf_path):
        return self.rag_core.pdf_processor.extract_text_from_pdf(pdf_path)
    
    def chunk_text(self, text, chunk_size=500, overlap=50):
        return self.rag_core.pdf_processor.chunk_single_document(text, chunk_size, overlap)
    
    def generate_answer(self, question, context):
        return self.rag_core.ai_models.generate_answer(question, context)


def main():
    """Legacy main function for backward compatibility"""
    rag_system = PDFRAGSystem()
    
    pdf_path = input("Enter PDF path: ").strip()
    
    if not os.path.exists(pdf_path):
        print("PDF not found")
        return
    
    if rag_system.load_pdf_and_build_index(pdf_path):
        print("PDF loaded! Ask questions (type 'quit' to exit):")
        
        while True:
            question = input("\nQuestion: ").strip()
            if question.lower() in ['quit', 'exit']:
                break
            if question:
                answer = rag_system.ask_question(question)
                print(f"Answer: {answer}")


if __name__ == "__main__":
    main()
