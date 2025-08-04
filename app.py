"""
Production Web App for Render.com
Enhanced RAG Nutrition Database with Multi-PDF Support
"""

from flask import Flask, request, jsonify, render_template_string
import sys
import os
import logging
from datetime import datetime

# Configure logging for production
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from rag import EnhancedRAG
    HAS_RAG = True
    logger.info("✅ RAG modules loaded successfully")
except ImportError as e:
    logger.error(f"❌ RAG modules not available: {e}")
    HAS_RAG = False

app = Flask(__name__)

# Global RAG system
rag_system = None
initialization_time = None

def initialize_rag():
    """Initialize RAG system for production"""
    global rag_system, initialization_time
    if not HAS_RAG:
        logger.warning("RAG not available - running in demo mode")
        return None
    
    if rag_system is not None:
        return rag_system
    
    try:
        logger.info("🤖 Initializing Enhanced RAG System...")
        start_time = datetime.now()
        
        rag_system = EnhancedRAG()
        
        # Check if docs folder exists
        if os.path.exists('docs') and os.listdir('docs'):
            logger.info("📁 Loading documents from docs/ folder...")
            if rag_system.load_folder('docs'):
                rag_system.build_index()
                initialization_time = datetime.now() - start_time
                logger.info(f"✅ RAG initialized in {initialization_time.total_seconds():.2f} seconds")
                logger.info(f"📊 Loaded {len(rag_system.structured_data)} structured items")
            else:
                logger.warning("⚠️ Failed to load documents")
        else:
            logger.warning("⚠️ No docs/ folder found or empty")
            
    except Exception as e:
        logger.error(f"❌ Failed to initialize RAG: {e}")
        rag_system = None
    
    return rag_system

# HTML Template with enhanced styling
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🥗 Enhanced RAG Nutrition Database</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh; padding: 20px;
        }
        .container { 
            max-width: 1000px; margin: 0 auto; 
            background: rgba(255,255,255,0.95); 
            border-radius: 20px; padding: 30px; 
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        }
        .header { text-align: center; margin-bottom: 30px; }
        .header h1 { color: #2c3e50; margin-bottom: 10px; font-size: 2.5em; }
        .header p { color: #7f8c8d; font-size: 1.2em; }
        .status { 
            background: #e8f5e8; border: 2px solid #4caf50; 
            border-radius: 10px; padding: 15px; margin-bottom: 20px; 
            text-align: center; color: #2e7d32; font-weight: bold;
        }
        .query-section { margin-bottom: 30px; }
        .input-group { display: flex; gap: 10px; margin-bottom: 20px; }
        #query { 
            flex: 1; padding: 15px; border: 2px solid #ddd; 
            border-radius: 10px; font-size: 16px;
            transition: border-color 0.3s;
        }
        #query:focus { outline: none; border-color: #667eea; }
        button { 
            background: linear-gradient(135deg, #667eea, #764ba2); 
            color: white; border: none; padding: 15px 25px; 
            border-radius: 10px; cursor: pointer; font-size: 16px; font-weight: bold;
            transition: transform 0.2s;
        }
        button:hover { transform: translateY(-2px); }
        .examples { margin-bottom: 20px; }
        .example-btn { 
            background: #f8f9fa; color: #495057; border: 1px solid #dee2e6; 
            margin: 5px; padding: 8px 12px; border-radius: 20px; 
            font-size: 14px; cursor: pointer;
        }
        .example-btn:hover { background: #e9ecef; }
        .result { 
            background: #f8f9fa; border-left: 4px solid #667eea; 
            padding: 20px; border-radius: 10px; margin-top: 20px;
            min-height: 100px;
        }
        .loading { color: #667eea; font-style: italic; }
        .error { color: #e74c3c; background: #ffeaea; border-color: #e74c3c; }
        table { width: 100%; border-collapse: collapse; margin: 10px 0; }
        th, td { padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }
        th { background: #f8f9fa; font-weight: bold; }
        .footer { text-align: center; margin-top: 30px; color: #7f8c8d; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🥗 Enhanced RAG Nutrition Database</h1>
            <p>Multilingual nutrition data with semantic search across 13 PDFs</p>
        </div>
        
        <div class="status" id="status">
            🔄 Checking system status...
        </div>
        
        <div class="query-section">
            <div class="input-group">
                <input type="text" id="query" placeholder="Ask about nutrition data... (e.g., 'weight of rice', '5 lowest weight vegetables')" />
                <button onclick="askQuestion()">🔍 Search</button>
            </div>
            
            <div class="examples">
                <strong>💡 Try these examples:</strong><br>
                <button class="example-btn" onclick="setQuery('weight of rice')">Weight of rice</button>
                <button class="example-btn" onclick="setQuery('give me 5 vegetables which have lowest weight')">5 lowest weight vegetables</button>
                <button class="example-btn" onclick="setQuery('list all oats items')">List oats items</button>
                <button class="example-btn" onclick="setQuery('highest weight cereals')">Highest weight cereals</button>
                <button class="example-btn" onclick="setQuery('beans weight')">Beans weight</button>
            </div>
            
            <div class="result" id="result">
                <p>👆 Enter your question above or click an example to get started!</p>
            </div>
        </div>
        
        <div class="footer">
            <p>🚀 Powered by Enhanced RAG • 📊 534 nutrition items from 13 PDFs • 🌍 Multilingual support</p>
        </div>
    </div>

    <script>
        // Check system status on load
        window.onload = function() {
            fetch('/status')
                .then(response => response.json())
                .then(data => {
                    const statusDiv = document.getElementById('status');
                    if (data.status === 'ready') {
                        statusDiv.innerHTML = `✅ System Ready! ${data.items} nutrition items loaded from ${data.pdfs} PDFs`;
                        statusDiv.style.background = '#e8f5e8';
                        statusDiv.style.borderColor = '#4caf50';
                    } else {
                        statusDiv.innerHTML = `⚠️ ${data.message}`;
                        statusDiv.style.background = '#fff3cd';
                        statusDiv.style.borderColor = '#ffc107';
                    }
                })
                .catch(error => {
                    document.getElementById('status').innerHTML = '❌ System Error';
                });
        };

        function setQuery(text) {
            document.getElementById('query').value = text;
        }

        function askQuestion() {
            const query = document.getElementById('query').value.trim();
            if (!query) {
                alert('Please enter a question!');
                return;
            }

            const resultDiv = document.getElementById('result');
            resultDiv.innerHTML = '<p class="loading">🤔 Searching nutrition database...</p>';

            fetch('/ask', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ question: query, web_format: true })
            })
            .then(response => response.json())
            .then(data => {
                if (data.answer) {
                    resultDiv.innerHTML = data.answer;
                } else {
                    resultDiv.innerHTML = '<p class="error">❌ ' + (data.error || 'No answer found') + '</p>';
                }
            })
            .catch(error => {
                resultDiv.innerHTML = '<p class="error">❌ Error: ' + error.message + '</p>';
            });
        }

        // Allow Enter key to submit
        document.getElementById('query').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                askQuestion();
            }
        });
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    """Main page"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/status')
def status():
    """System status check"""
    try:
        rag = initialize_rag()
        if rag and hasattr(rag, 'structured_data') and rag.structured_data:
            return jsonify({
                'status': 'ready',
                'items': len(rag.structured_data),
                'pdfs': len([f for f in os.listdir('docs') if f.endswith('.pdf')]) if os.path.exists('docs') else 0,
                'initialization_time': initialization_time.total_seconds() if initialization_time else 0
            })
        else:
            return jsonify({
                'status': 'warning',
                'message': 'System available but no documents loaded'
            })
    except Exception as e:
        logger.error(f"Status check error: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        })

@app.route('/ask', methods=['POST'])
def ask_question():
    """Handle questions"""
    try:
        data = request.get_json()
        question = data.get('question', '').strip()
        web_format = data.get('web_format', False)
        
        if not question:
            return jsonify({'error': 'No question provided'})
        
        rag = initialize_rag()
        if not rag:
            return jsonify({'error': 'RAG system not available'})
        
        if not hasattr(rag, 'structured_data') or not rag.structured_data:
            return jsonify({'error': 'No documents loaded'})
        
        logger.info(f"Processing question: {question}")
        answer = rag.ask(question, web_format=web_format)
        
        return jsonify({'answer': answer})
        
    except Exception as e:
        logger.error(f"Question processing error: {e}")
        return jsonify({'error': str(e)})

@app.route('/health')
def health_check():
    """Health check for Render.com"""
    return jsonify({
        'status': 'healthy',
        'mode': 'production',
        'timestamp': datetime.now().isoformat()
    })

# Initialize RAG on startup
initialize_rag()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
