# 🤖 Enhanced RAG System

**Clean, minimal PDF Q&A system optimized for structured data - no bloat, just functionality!**

## 🎯 **WHICH APP TO LAUNCH & WHEN?**

| **Use Case** | **Launch Command** | **When to Use** |
|--------------|-------------------|-----------------|
| **🎯 Interactive Q&A** | `python rag.py` | **MAIN APP** - Enhanced terminal interface |
| **🌐 Web Interface** | `python web_app.py` | Clean browser UI at localhost:5000 |
| **🧪 Quick Demo** | `python demo.py` | Test with sample questions |
| **🔧 System Check** | `python test.py` | Validate setup & dependencies |

## 📁 What's Here (4 Clean Files)

```
rag/
├── rag.py            # 🎯 MAIN APP - Enhanced Q&A with structured data (285 lines)
├── web_app.py        # 🌐 Web browser interface (167 lines)  
├── demo.py           # 🧪 Quick demo with sample questions (45 lines)
├── test.py           # 🔧 System validation & dependency check (85 lines)
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

#### **🎯 Main App (RECOMMENDED)**
```powershell
python rag.py
# Enhanced system with structured data extraction
# Perfect for your cereal exchange data
```

#### **🌐 Web Interface**
```powershell
python web_app.py
# Visit: http://localhost:5000 - clean browser UI
```

#### **🧪 Quick Demo**
```powershell
python demo.py
# Test with sample cereal exchange questions
```

## 🔧 Key Features

- 🧠 **AI Models**: DistilGPT2 + SentenceTransformers (all-MiniLM-L6-v2) - lightweight & fast
- 📄 **Enhanced PDF Processing**: Smart extraction of structured data from tables
- 🔍 **Smart Search**: FAISS vector similarity + structured data priority
- 📚 **Source Attribution**: Shows which document(s) answered your question
- 💻 **GPU Ready**: Automatically detects and uses your RTX 2050 (falls back to CPU)
- 🌐 **Dual Interface**: Both command-line and web browser options
- 📊 **Structured Data**: Perfect for cereal exchange lists, tables, weights

## 🎯 Perfect for Your Cereal Data

### **Exact Weight Queries:**
- **Input**: "weight of rice"
- **Output**: "**Rice**: 7.3 grams" ✅

### **List All Items:**
```python
from rag import EnhancedRAG

rag = EnhancedRAG()
rag.load_folder('docs')  # Load your cereal PDF
rag.build_index()

# Ask specific questions
answer = rag.ask("list all rice items")
# Shows: Rice (7.3g), Rice flakes (8.7g), Rice flour (10.1g), etc.

answer = rag.ask("bread weight") 
# Shows all bread types with weights
```

### **Example Questions for Your Cereal Exchange:**
- "weight of rice" → "Rice: 7.3 grams"
- "list all bread items" → Shows all 6 bread types
- "quinoa weight" → "Quinoa: 5.9 grams"  
- "how much oats" → Shows oats variations

## 📊 **What Makes This Enhanced?**

✅ **Extracts 53+ structured items** from your cereal PDF  
✅ **Handles multilingual text** (English + Hindi + Marathi)  
✅ **Smart pattern recognition** for item-weight pairs  
✅ **Exact match priority** - finds precise answers first  
✅ **No more confusion** - only 4 clean files  

## 🐛 Troubleshooting

**Missing dependencies?**
```powershell
pip install -r requirements_minimal.txt
```

**No documents loaded?**
- Create `docs/` folder
- Add PDF files  
- Run again

**Slow first run?**
- AI models downloading (~5 minutes)
- Subsequent runs much faster
- GPU automatically detected

## ✅ That's It!

**No more bloat. No more confusion. Just a working enhanced RAG system!**

🎯 **Start with**: `python rag.py`
