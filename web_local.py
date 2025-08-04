"""
Local Web Interface - Test the UI locally
Run this to test the web interface on your machine
"""

from flask import Flask, request, jsonify, render_template_string
import sys
import os

# Add current directory to path to import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from rag import EnhancedRAG
    HAS_RAG = True
except ImportError as e:
    print(f"⚠️  RAG modules not available: {e}")
    print("💡 This will show the UI only (no actual processing)")
    HAS_RAG = False

app = Flask(__name__)

# Global RAG system
rag_system = None

def initialize_rag():
    """Initialize RAG system for local testing"""
    global rag_system
    if not HAS_RAG:
        return None
        
    if rag_system is None:
        print("🚀 Initializing local RAG system...")
        try:
            rag_system = EnhancedRAG()
            
            # Try to load documents
            if os.path.exists('docs'):
                success = rag_system.load_multiple_pdfs('docs')
                if success:
                    docs = rag_system.get_loaded_documents()
                    print(f"✅ Loaded {len(docs)} documents: {docs}")
                    
                    # Build the index for semantic search
                    rag_system.build_index()
                    print("✅ Built search index")
                else:
                    print("⚠️  No documents loaded from docs/ folder")
            else:
                print("📁 No docs/ folder found - create it and add PDF files")
                
        except Exception as e:
            print(f"❌ Failed to initialize RAG: {e}")
            return None
            
    return rag_system

@app.route('/')
def home():
    """Serve the enhanced UI"""
    # Import the HTML from app_render.py or define it here
    with open('app_render.py', 'r') as f:
        content = f.read()
        
    # Extract the HTML template (between the triple quotes)
    start = content.find('html = """') + 10
    end = content.find('"""', start)
    html_template = content[start:end]
    
    return render_template_string(html_template)

@app.route('/ask', methods=['POST'])
def ask_question():
    """Handle questions (with fallback for demo)"""
    try:
        data = request.get_json()
        question = data.get('question', '')
        
        if not question:
            return jsonify({'error': 'No question provided'}), 400
        
        if not HAS_RAG:
            # Demo mode - return sample responses
            demo_responses = {
                'main topics': 'This is a demo response. The main topics would be extracted from your documents.',
                'benefits': 'Demo: Key benefits would be listed here based on document analysis.',
                'summary': 'Demo: A comprehensive summary would be generated from your PDF documents.',
                'recommendations': 'Demo: Recommendations would be extracted and presented here.'
            }
            
            # Find matching demo response
            question_lower = question.lower()
            for key, response in demo_responses.items():
                if key in question_lower:
                    return jsonify({'answer': f"🎭 {response}\\n\\n💡 To get real answers, install the required packages and add PDF files to the docs/ folder."})
            
            return jsonify({'answer': f"🎭 Demo mode: You asked '{question}'. Install the full system to get real answers from your documents!"})
        
        # Real RAG processing
        rag = initialize_rag()
        if not rag:
            return jsonify({'error': 'RAG system not initialized'}), 500
            
        answer = rag.ask(question, web_format=True)
        return jsonify({'answer': answer})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/status')
def get_status():
    """Get system status"""
    try:
        if not HAS_RAG:
            return jsonify({
                'status': 'demo_mode',
                'message': 'UI demo only - install requirements for full functionality',
                'environment': 'local_demo',
                'loaded_documents': ['demo.pdf (sample)'],
                'document_count': 1
            })
        
        rag = initialize_rag()
        if rag:
            docs = rag.get_loaded_documents()
            return jsonify({
                'status': 'ready',
                'environment': 'local',
                'loaded_documents': docs,
                'document_count': len(docs)
            })
        else:
            return jsonify({
                'status': 'not_ready',
                'message': 'RAG system failed to initialize'
            })
        
    except Exception as e:
        return jsonify({'status': 'error', 'error': str(e)}), 500

@app.route('/health')
def health_check():
    """Health check"""
    return jsonify({'status': 'healthy', 'mode': 'local_test'})

if __name__ == '__main__':
    print("🌐 Starting local web interface...")
    print("📁 Make sure to:")
    print("   1. Create a 'docs/' folder")
    print("   2. Add PDF files to it")
    print("   3. Install requirements if you want real processing")
    print("\\n🚀 Open: http://localhost:5000")
    print("⏹️  Press Ctrl+C to stop")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
