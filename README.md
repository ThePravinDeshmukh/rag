# 🤖 Simple RAG System

**Clean, minimal PDF Q&A system - no bloat, just functionality!**

## 🎯 **WHICH APP TO LAUNCH & WHEN?**

| **Use Case** | **Launch Command** | **When to Use** |
|--------------|-------------------|-----------------|
| **🎯 Interactive Q&A** | `python rag_simple.py` | **MOST COMMON** - Ask questions in terminal |
| **🌐 Web Interface** | `python web_app.py` | Want a clean browser UI at localhost:5000 |
| **🧪 Quick Test** | `python demo_simple.py` | Test if system works with sample questions |
| **🔧 System Check** | `python test_simple.py` | Validate setup & check dependencies |
| **🔄 Legacy Code** | `python rag.py` | Only if you have old code to maintain |

## 📁 What's Here (5 Python Files)

```
rag/
├── rag_simple.py      # 🎯 MAIN APP - Interactive terminal Q&A (241 lines)
├── web_app.py         # 🌐 Web browser interface (167 lines)  
├── demo_simple.py     # 🧪 Quick demo with sample questions (52 lines)
├── test_simple.py     # 🔧 System validation & dependency check (94 lines)
├── rag.py            # 🔄 Legacy compatibility wrapper (77 lines)
└── docs/             # 📄 Your PDF files go here
```

## 🚀 Quick Start

### 1. **Setup Dependencies**
```powershell
pip install -r requirements_minimal.txt
```

### 2. **Add Your Documents**
```powershell
# Create docs folder and add your PDFs
mkdir docs
# Copy your PDF files into docs/
```

### 3. **Choose Your Interface**

#### **🎯 Command Line (RECOMMENDED)**
```powershell
python rag_simple.py
# Interactive terminal - ask questions directly
```

#### **🌐 Web Interface**
```powershell
python web_app.py
# Visit: http://localhost:5000 - clean browser UI
```

#### **🧪 Quick Test**
```powershell
python demo_simple.py
# Runs 3 sample questions to test your setup
```

## 🎯 **DETAILED FILE BREAKDOWN**

### 📄 `rag_simple.py` - **THE MAIN APP** (241 lines)
**Purpose**: Complete RAG system in one file - your primary interface
**When to use**: Interactive Q&A sessions, main development work

**Key Functions:**
- `SimpleRAG.__init__()` - Initialize models (SentenceTransformers + DistilGPT2)
- `load_pdf(pdf_path)` - Load single PDF file into chunks
- `load_folder(folder_path)` - Load all PDFs from directory
- `build_index()` - Create FAISS vector search index
- `search(question, top_k=3)` - Find relevant document chunks
- `generate_answer(question, context)` - Generate AI response
- `ask(question)` - Complete Q&A pipeline (search + generate)
- `main()` - Interactive command-line interface

**Core Features:**
- ✅ PDF text extraction with chunking (300 words + 50 overlap)
- ✅ Semantic search using sentence embeddings
- ✅ Source attribution (shows which PDF answered)
- ✅ GPU support (RTX 2050) with CPU fallback
- ✅ Error handling and user-friendly output

---

### 🌐 `web_app.py` - **WEB INTERFACE** (167 lines)
**Purpose**: Clean Flask web UI for browser-based interaction
**When to use**: Want visual interface, sharing with others, easier UI

**Key Functions:**
- `init_rag()` - Initialize RAG system once (global instance)
- `home()` - Serve main HTML page with embedded CSS/JS
- `ask_question()` - Handle POST requests from web form
- `status()` - Return system status (docs loaded, chunks, ready state)

**Features:**
- ✅ Single-page application with embedded HTML/CSS/JS
- ✅ Real-time question answering via AJAX
- ✅ Example question buttons for easy testing
- ✅ Clean, responsive design
- ✅ Error handling with user feedback
- ✅ Runs on localhost:5000

---

### 🧪 `demo_simple.py` - **QUICK DEMO** (52 lines)
**Purpose**: Automated testing with predefined questions
**When to use**: Validate system works, quick functionality check

**Key Functions:**
- `main()` - Run demo sequence automatically

**Demo Flow:**
1. Check if `docs/` folder exists (create if missing)
2. Initialize RAG system
3. Load all PDFs from docs folder
4. Ask 3 predefined questions:
   - "What is this document about?"
   - "What are the main points?"
   - "Can you summarize the content?"
5. Display answers and next steps

---

### 🔧 `test_simple.py` - **SYSTEM VALIDATOR** (94 lines)
**Purpose**: Comprehensive dependency and system testing
**When to use**: First setup, troubleshooting, before deployment

**Key Functions:**
- `test_imports()` - Check all required packages (torch, transformers, etc.)
- `test_rag_system()` - Validate RAG initialization works
- `main()` - Run complete test suite

**Validates:**
- ✅ PyTorch installation
- ✅ Transformers library
- ✅ SentenceTransformers
- ✅ FAISS vector search
- ✅ PyPDF2 for PDF processing
- ✅ NumPy for computations
- ✅ RAG system initialization
- ✅ Provides clear error messages with install commands

---

### 🔄 `rag.py` - **LEGACY WRAPPER** (77 lines)
**Purpose**: Backward compatibility for old code
**When to use**: Only if you have existing code using old interface

**Key Functions:**
- `PDFRAGSystem.__init__()` - Legacy constructor interface
- `load_pdf_and_build_index()` - Old-style single PDF loading
- `load_multiple_pdfs_and_build_index()` - Old-style multi-PDF loading
- `ask_question()` - Legacy question interface
- `get_loaded_documents()` - Return loaded document list

**Note**: This wraps the modern `rag_simple.py` functionality but uses outdated method names. Use `rag_simple.py` for new projects.

## 🔧 Key Features

- 🧠 **AI Models**: DistilGPT2 + SentenceTransformers (all-MiniLM-L6-v2) - lightweight & fast
- 📄 **PDF Support**: PyPDF2 extraction with intelligent chunking (300 words + 50 overlap)
- 🔍 **Smart Search**: FAISS vector similarity with L2 distance
- 📚 **Source Attribution**: Shows which document(s) answered your question
- 💻 **GPU Ready**: Automatically detects and uses your RTX 2050 (falls back to CPU)
- 🌐 **Dual Interface**: Both command-line and web browser options
- 🔄 **Legacy Compatible**: Works with old code via compatibility wrapper

## 🎯 Usage Examples

### **Basic RAG Operations:**
```python
from rag_simple import SimpleRAG

# Initialize system
rag = SimpleRAG()

# Load documents
rag.load_folder('docs')  # Load all PDFs from folder
# OR
rag.load_pdf('path/to/document.pdf')  # Load single PDF

# Build search index
rag.build_index()

# Ask questions
answer = rag.ask("What are the main topics?")
print(answer)  # Includes source attribution
```

### **Web Interface Usage:**
```python
# Start web server
python web_app.py

# Visit http://localhost:5000
# - Clean UI with input field
# - Example question buttons
# - Real-time answers with sources
```

### Example Questions:
- "What are the main topics covered?"
- "What are the key benefits mentioned?"
- "Can you summarize the important points?"
- "What recommendations are given?"

## 🐛 Troubleshooting

**No documents loaded?**
- Create `docs/` folder
- Add PDF files
- Run again

**Import errors?**
- Install: `pip install torch transformers sentence-transformers faiss-cpu PyPDF2 numpy`
- For web: `pip install flask`

**Slow performance?**
- First run downloads AI models (~5 minutes)
- Subsequent runs much faster
- GPU automatically detected and used

## ✅ That's It!

**No more confusion. No more bloat. Just a simple, working RAG system!**

🎯 **Start with**: `python rag_simple.py`
