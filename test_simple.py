"""
System Test - Check if everything works
Run this to validate your setup
"""

def test_imports():
    """Test if required packages are available"""
    print("🧪 Testing imports...")
    
    try:
        import torch
        print("✅ PyTorch")
    except ImportError:
        print("❌ PyTorch - install with: pip install torch")
        return False
    
    try:
        import transformers
        print("✅ Transformers")
    except ImportError:
        print("❌ Transformers - install with: pip install transformers")
        return False
    
    try:
        import sentence_transformers
        print("✅ SentenceTransformers") 
    except ImportError:
        print("❌ SentenceTransformers - install with: pip install sentence-transformers")
        return False
    
    try:
        import faiss
        print("✅ FAISS")
    except ImportError:
        print("❌ FAISS - install with: pip install faiss-cpu")
        return False
    
    try:
        import PyPDF2
        print("✅ PyPDF2")
    except ImportError:
        print("❌ PyPDF2 - install with: pip install PyPDF2")
        return False
    
    try:
        import numpy
        print("✅ NumPy")
    except ImportError:
        print("❌ NumPy - install with: pip install numpy")
        return False
    
    return True

def test_rag_system():
    """Test if RAG system can be imported"""
    try:
        from rag_simple import SimpleRAG
        print("✅ SimpleRAG system import successful")
        
        # Try to initialize
        print("🤖 Testing RAG initialization...")
        rag = SimpleRAG()
        print("✅ RAG system initialized successfully")
        return True
        
    except Exception as e:
        print(f"❌ RAG system test failed: {e}")
        return False

def main():
    print("🧪 Simple RAG System Test")
    print("="*30)
    
    # Test imports
    if not test_imports():
        print("\\n❌ Missing dependencies. Install with:")
        print("pip install -r requirements_minimal.txt")
        return
    
    # Test RAG system
    if not test_rag_system():
        print("\\n❌ RAG system failed to initialize")
        return
    
    print("\\n🎉 All tests passed!")
    print("\\n🚀 Ready to use:")
    print("• 📄 Add PDFs to 'docs/' folder")  
    print("• 🎯 Run: python rag_simple.py")
    print("• 🌐 Web: python web_app.py")
    print("• 🧪 Demo: python demo_simple.py")

if __name__ == "__main__":
    main()
