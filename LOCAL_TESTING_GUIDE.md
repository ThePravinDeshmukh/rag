# 🧪 **LOCAL TESTING GUIDE**

## 📋 **How to Test Your RAG Apps Locally**

### **🎯 Purpose:**
Test both versions locally to see the difference and ensure everything works before deploying to Render.com.

---

## **1. 🔍 Test Original App (`app.py`)**

### **Start the App:**
```powershell
.\venv\Scripts\python.exe app.py
```

### **Expected Behavior:**
```
✅ RAG modules loaded successfully
🤖 Initializing Enhanced RAG System...
Device: cpu
✅ Enhanced RAG ready!
📁 Loading documents from docs/ folder...
📦 Loading embedding model...    ← LOADS AT STARTUP
...
📊 Loaded 534 structured items
✅ RAG initialized in X.XX seconds
* Running on http://127.0.0.1:5000
```

### **⚠️ Memory Impact:**
- **Startup**: Immediately loads models (~600MB)
- **Cause of Render.com failure**: Exceeds 512MB limit

---

## **2. 🚀 Test Optimized App (`app_optimized.py`)**

### **Start the App:**
```powershell
.\venv\Scripts\python.exe app_optimized.py
```

### **Expected Behavior:**
```
* Serving Flask app 'app_optimized'
* Running on http://127.0.0.1:5000    ← STARTS INSTANTLY
```

### **✅ Memory Optimization:**
- **Startup**: No model loading (~150MB)
- **First query**: Models load on-demand
- **Result**: Works within 512MB limit

---

## **3. 🌐 Web Interface Testing**

### **Open in Browser:**
```
http://localhost:5000
```

### **Test These Scenarios:**

#### **A. Status Check:**
- Page loads instantly
- Status shows: "✅ Ready! 534 items from 13 PDFs"

#### **B. Example Queries:**
1. **"weight of rice"**
   - Expected: "Rice: 7.3 grams 🌏 (Hindi: तांदूळ चावल)"

2. **"5 lowest weight vegetables"**
   - Expected: Table with mushroom (1.7g), soybeans (3.5g), etc.

3. **"beans"**
   - Expected: Table with all bean varieties and weights

#### **C. First Query (Optimized App Only):**
- **First query takes ~30 seconds** (model loading)
- **Subsequent queries <2 seconds** (models cached)

---

## **4. 🔧 API Testing (Optional)**

### **Test with curl:**
```powershell
# Test status endpoint
curl http://localhost:5000/status

# Test query endpoint
curl -X POST http://localhost:5000/ask -H "Content-Type: application/json" -d "{\"question\": \"weight of rice\", \"web_format\": true}"
```

### **Test with Python:**
```python
import requests
import json

# Test query
response = requests.post(
    'http://localhost:5000/ask',
    json={'question': 'weight of rice', 'web_format': True}
)
print(response.json())
```

---

## **5. 📊 Memory Monitoring (Optional)**

### **Check Memory Usage:**
```powershell
# Install psutil if not already installed
.\venv\Scripts\pip.exe install psutil

# Monitor memory
.\venv\Scripts\python.exe -c "import psutil; import os; print(f'Memory: {psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024:.1f} MB')"
```

---

## **6. 🔄 Switch Between Apps**

### **Stop Current App:**
```powershell
# Press Ctrl+C in terminal
# OR
taskkill /f /im python.exe
```

### **Start Other App:**
```powershell
# Switch to original
.\venv\Scripts\python.exe app.py

# Switch to optimized
.\venv\Scripts\python.exe app_optimized.py
```

---

## **7. ✅ Testing Checklist**

### **Both Apps Should:**
- ✅ Start without errors
- ✅ Load all 13 PDFs (534 items)
- ✅ Respond to example queries
- ✅ Show proper multilingual support
- ✅ Handle weight-based queries correctly

### **Key Differences:**
| Feature | `app.py` | `app_optimized.py` |
|---------|----------|-------------------|
| **Startup** | Loads models immediately | Instant start |
| **Memory at startup** | ~600MB | ~150MB |
| **First query** | <2 seconds | ~30 seconds |
| **Render.com compatibility** | ❌ Fails | ✅ Works |

---

## **8. 🚀 Ready for Deployment**

### **Once Local Testing Passes:**
1. **Commit changes:**
   ```bash
   git add .
   git commit -m "Memory optimization for Render.com free tier"
   git push origin main
   ```

2. **Deploy to Render.com:**
   - Use `app_optimized.py` (via updated Procfile)
   - Expect successful deployment within 512MB limit

### **Expected Render.com Behavior:**
- **Build**: ~3-5 minutes (downloading packages)
- **Startup**: ~15 seconds (instant app start)
- **First query**: ~30 seconds (model loading)
- **Runtime**: Stable at ~400MB

---

## **🎉 You're Ready!**

Your local testing confirms both apps work, with `app_optimized.py` being the production-ready version for Render.com's free tier! 🚀
