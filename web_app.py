"""
Simple Web Interface - Minimal Flask app for RAG
Run: python web_app.py then visit http://localhost:5000
"""

try:
    from flask import Flask, request, jsonify, render_template_string
    FLASK_AVAILABLE = True
except ImportError:
    print("❌ Flask not installed. Run: pip install flask")
    FLASK_AVAILABLE = False
    exit(1)

from rag_simple import SimpleRAG
import os

app = Flask(__name__)
rag = None

def init_rag():
    """Initialize RAG system once"""
    global rag
    if rag is None:
        rag = SimpleRAG()
        if os.path.exists('docs'):
            if rag.load_folder('docs'):
                rag.build_index()
                print("✅ RAG system ready")
            else:
                print("⚠️  No documents loaded")
        else:
            print("📁 Create 'docs/' folder and add PDFs")
    return rag

@app.route('/')
def home():
    """Simple, clean web interface"""
    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Simple RAG System</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; background: #f5f5f5; }
            .container { background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            h1 { color: #333; text-align: center; margin-bottom: 30px; }
            .input-group { margin-bottom: 20px; }
            input[type="text"] { width: 100%; padding: 15px; font-size: 16px; border: 2px solid #ddd; border-radius: 5px; box-sizing: border-box; }
            button { width: 100%; padding: 15px; font-size: 16px; background: #007bff; color: white; border: none; border-radius: 5px; cursor: pointer; }
            button:hover { background: #0056b3; }
            button:disabled { background: #ccc; cursor: not-allowed; }
            .answer { background: #f8f9fa; padding: 20px; margin: 20px 0; border-left: 4px solid #007bff; border-radius: 5px; }
            .status { text-align: center; padding: 10px; font-weight: bold; }
            .examples { margin: 20px 0; }
            .examples button { width: auto; margin: 5px; padding: 8px 15px; font-size: 14px; background: #6c757d; }
            .examples button:hover { background: #545b62; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🤖 Simple RAG System</h1>
            
            <div class="input-group">
                <input type="text" id="question" placeholder="Ask a question about your documents..." />
            </div>
            
            <div class="input-group">
                <button onclick="askQuestion()" id="askBtn">Ask Question</button>
            </div>
            
            <div class="examples">
                <strong>Example questions:</strong><br>
                <button onclick="setQuestion('What are the main topics?')">Main topics</button>
                <button onclick="setQuestion('What are the key benefits?')">Benefits</button>
                <button onclick="setQuestion('Summarize the content')">Summary</button>
            </div>
            
            <div id="status" class="status"></div>
            <div id="answer" class="answer" style="display:none;"></div>
        </div>

        <script>
            function setQuestion(text) {
                document.getElementById('question').value = text;
            }
            
            async function askQuestion() {
                const question = document.getElementById('question').value.trim();
                if (!question) return;
                
                const btn = document.getElementById('askBtn');
                const status = document.getElementById('status');
                const answerDiv = document.getElementById('answer');
                
                btn.disabled = true;
                btn.textContent = 'Thinking...';
                status.textContent = '🤔 Processing your question...';
                answerDiv.style.display = 'none';
                
                try {
                    const response = await fetch('/ask', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({question: question})
                    });
                    
                    const data = await response.json();
                    
                    if (data.error) {
                        status.textContent = '❌ ' + data.error;
                    } else {
                        status.textContent = '';
                        answerDiv.innerHTML = '<strong>Q:</strong> ' + question + '<br><br><strong>A:</strong> ' + data.answer.replace(/\\n/g, '<br>');
                        answerDiv.style.display = 'block';
                    }
                } catch (error) {
                    status.textContent = '❌ Error: ' + error.message;
                }
                
                btn.disabled = false;
                btn.textContent = 'Ask Question';
            }
            
            document.getElementById('question').addEventListener('keypress', function(e) {
                if (e.key === 'Enter') askQuestion();
            });
        </script>
    </body>
    </html>
    '''
    return render_template_string(html)

@app.route('/ask', methods=['POST'])
def ask_question():
    """Handle question requests"""
    try:
        data = request.get_json()
        question = data.get('question', '').strip()
        
        if not question:
            return jsonify({'error': 'No question provided'}), 400
        
        rag_system = init_rag()
        answer = rag_system.ask(question)
        
        return jsonify({'answer': answer})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/status')
def status():
    """System status"""
    rag_system = init_rag()
    return jsonify({
        'documents': len(set(rag_system.sources)) if rag_system.sources else 0,
        'chunks': len(rag_system.chunks),
        'ready': rag_system.index is not None
    })

if __name__ == '__main__':
    print("🌐 Starting Simple RAG Web Interface...")
    print("📁 Make sure you have PDFs in the 'docs/' folder")
    print("🚀 Open: http://localhost:5000")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
