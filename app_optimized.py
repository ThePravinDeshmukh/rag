"""
Memory-Optimized Production App for Render.com Free Tier
Enhanced RAG Nutrition Database with Ultra-Low Memory Usage
"""

from flask import Flask, request, jsonify, render_template_string
import sys
import os
import logging
from datetime import datetime
import gc

# Configure logging for production
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__)

# Global RAG system (lazy loaded)
rag_system = None
initialization_time = None

def initialize_rag():
    """Initialize RAG system with memory optimization for free tier"""
    global rag_system, initialization_time
    if rag_system is not None:
        return rag_system
    
    try:
        logger.info("🤖 Initializing Memory-Optimized RAG System...")
        start_time = datetime.now()
        
        # Import and initialize RAG with minimal memory footprint
        from rag import EnhancedRAG
        rag_system = EnhancedRAG()
        
        # Check if docs folder exists
        if os.path.exists('docs') and os.listdir('docs'):
            logger.info("📁 Loading documents with memory optimization...")
            if rag_system.load_folder('docs'):
                rag_system.build_index()
                initialization_time = datetime.now() - start_time
                logger.info(f"✅ RAG initialized in {initialization_time.total_seconds():.2f} seconds")
                logger.info(f"📊 Loaded {len(rag_system.structured_data)} structured items")
                
                # Force garbage collection to free memory
                gc.collect()
            else:
                logger.warning("⚠️ Failed to load documents")
        else:
            logger.warning("⚠️ No docs/ folder found or empty")
            
    except Exception as e:
        logger.error(f"❌ Failed to initialize RAG: {e}")
        rag_system = None
    
    return rag_system

# Compact HTML Template (reduced memory footprint)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🥗 RAG Nutrition Database</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Segoe UI', sans-serif; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh; padding: 20px;
        }
        .container { 
            max-width: 900px; margin: 0 auto; 
            background: rgba(255,255,255,0.95); 
            border-radius: 15px; padding: 25px; 
            box-shadow: 0 15px 35px rgba(0,0,0,0.1);
        }
        .header { text-align: center; margin-bottom: 25px; }
        .header h1 { color: #2c3e50; margin-bottom: 8px; font-size: 2.2em; }
        .header p { color: #7f8c8d; font-size: 1.1em; }
        .status { 
            background: #e8f5e8; border: 2px solid #4caf50; 
            border-radius: 8px; padding: 12px; margin-bottom: 15px; 
            text-align: center; color: #2e7d32; font-weight: bold;
        }
        .input-group { display: flex; gap: 8px; margin-bottom: 15px; }
        #query { 
            flex: 1; padding: 12px; border: 2px solid #ddd; 
            border-radius: 8px; font-size: 15px;
        }
        #query:focus { outline: none; border-color: #667eea; }
        button { 
            background: linear-gradient(135deg, #667eea, #764ba2); 
            color: white; border: none; padding: 12px 20px; 
            border-radius: 8px; cursor: pointer; font-size: 15px; font-weight: bold;
        }
        button:hover { opacity: 0.9; }
        .examples { margin-bottom: 15px; }
        .example-btn { 
            background: #f8f9fa; color: #495057; border: 1px solid #dee2e6; 
            margin: 3px; padding: 6px 10px; border-radius: 15px; 
            font-size: 13px; cursor: pointer;
        }
        .example-btn:hover { background: #e9ecef; }
        .result { 
            background: #f8f9fa; border-left: 4px solid #667eea; 
            padding: 15px; border-radius: 8px; margin-top: 15px;
            min-height: 80px;
        }
        .loading { color: #667eea; font-style: italic; }
        .error { color: #e74c3c; background: #ffeaea; border-color: #e74c3c; }
        table { width: 100%; border-collapse: collapse; margin: 8px 0; }
        th, td { padding: 10px; text-align: left; border-bottom: 1px solid #ddd; }
        th { background: #f8f9fa; font-weight: bold; }
        .footer { text-align: center; margin-top: 25px; color: #7f8c8d; font-size: 14px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🥗 RAG Nutrition Database</h1>
            <p>Multilingual nutrition search • Free Tier Optimized</p>
        </div>
        
        <div class="status" id="status">🔄 Checking system status...</div>
        
        <div class="input-group">
            <input type="text" id="query" placeholder="Ask about nutrition... (e.g., 'weight of rice', '5 lowest weight vegetables')" />
            <button onclick="askQuestion()">🔍 Search</button>
        </div>
        
        <div class="examples">
            <strong>💡 Examples:</strong><br>
            <button class="example-btn" onclick="setQuery('weight of rice')">Weight of rice</button>
            <button class="example-btn" onclick="setQuery('5 lowest weight vegetables')">5 lowest vegetables</button>
            <button class="example-btn" onclick="setQuery('oats weight')">Oats weight</button>
            <button class="example-btn" onclick="setQuery('beans')">Beans</button>
        </div>
        
        <div class="result" id="result">
            <p>👆 Enter your question above to get started!</p>
        </div>
        
        <div class="footer">
            <p>🚀 Memory-Optimized for Render.com Free Tier • 📊 534 nutrition items</p>
        </div>
    </div>

    <script>
        window.onload = function() {
            fetch('/status')
                .then(response => response.json())
                .then(data => {
                    const statusDiv = document.getElementById('status');
                    if (data.status === 'ready') {
                        statusDiv.innerHTML = `✅ Ready! ${data.items} items from ${data.pdfs} PDFs`;
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
            resultDiv.innerHTML = '<p class="loading">🤔 Searching...</p>';

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
                'memory_optimized': True
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
    """Handle questions with memory optimization"""
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
        
        logger.info(f"Processing: {question[:50]}...")
        answer = rag.ask(question, web_format=web_format)
        
        # Force garbage collection after processing
        gc.collect()
        
        return jsonify({'answer': answer})
        
    except Exception as e:
        logger.error(f"Question error: {e}")
        return jsonify({'error': str(e)})

@app.route('/health')
def health_check():
    """Health check for Render.com"""
    return jsonify({
        'status': 'healthy',
        'mode': 'memory_optimized',
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
