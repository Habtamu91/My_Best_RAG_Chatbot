# Quick Start Guide - RAG Chatbot

## 🎯 Two Ways to Run

### Method 1: Use Batch Files (Easiest) ⭐

I've created **3 batch files** for you:

1. **`start_chatbot.bat`** - Starts both backend AND frontend automatically
   - Just double-click this file!
   - Opens 2 terminal windows (backend + frontend)
   - Opens browser automatically

2. **`start_backend.bat`** - Starts only the backend
   - Use this if you want to control when to start backend

3. **`start_frontend.bat`** - Starts only the frontend
   - Use this if backend is already running

### Method 2: Manual Setup (Step-by-Step)

## Step-by-Step Manual Setup

### **Step 1: Install Dependencies**

Open PowerShell and run:

```powershell
cd C:\Users\dell\Desktop\BizPredict\RAG_Chatbot\backend
C:\ProgramData\anaconda3\python.exe -m pip install fastapi uvicorn python-multipart PyPDF2 python-dotenv pydantic chromadb openai
```

**Wait for installation to complete** ✓

---

### **Step 2: Start Backend Server**

Open **Terminal Window 1** (PowerShell):

```powershell
cd C:\Users\dell\Desktop\BizPredict\RAG_Chatbot\backend
C:\ProgramData\anaconda3\python.exe run.py
```

**You should see:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

**✅ Keep this window open!** The backend must keep running.

---

### **Step 3: Verify Backend is Working**

Open a **NEW PowerShell window** and test:

```powershell
Invoke-RestMethod -Uri http://localhost:8000/health
```

**Expected result:**
```json
status: healthy
message: RAG Chatbot API is running
```

**✅ If you see this, backend is working!**

---

### **Step 4: Start Frontend**

You have **3 options**:

#### **Option A: Double-Click (Easiest)**
1. Go to: `C:\Users\dell\Desktop\BizPredict\RAG_Chatbot\frontend\`
2. **Double-click** `index.html`
3. Opens in your browser automatically! ✓

#### **Option B: Local Server (Recommended)**
Open **Terminal Window 2**:

```powershell
cd C:\Users\dell\Desktop\BizPredict\RAG_Chatbot\frontend
C:\ProgramData\anaconda3\python.exe -m http.server 8080
```

Then open browser and go to: `http://localhost:8080`

#### **Option C: Use the batch file**
Double-click `start_frontend.bat` in the RAG_Chatbot folder

---

### **Step 5: Test Your Chatbot!**

1. **Upload a PDF**:
   - Click "Choose PDF file"
   - Select any PDF document
   - Click "Upload PDF"
   - Wait for: "✓ PDF uploaded successfully!"

2. **Ask Questions**:
   - Type: "What is this document about?"
   - Press Enter or click "Send"
   - **You should see AI responses!** 🎉

---

## 📊 Visual Guide

```
┌─────────────────────────────────────┐
│  TERMINAL 1: Backend Server          │
│  (Keep Running)                      │
│                                       │
│  cd backend                           │
│  python run.py                        │
│  → http://localhost:8000             │
└─────────────────────────────────────┘
              ↕ API Calls
┌─────────────────────────────────────┐
│  BROWSER: Frontend                  │
│                                     │
│  Option A: Double-click index.html │
│  Option B: http://localhost:8080   │
│                                     │
│  [Upload PDF] → [Ask Questions]    │
└─────────────────────────────────────┘
```

---

## ✅ Quick Checklist

- [ ] Dependencies installed
- [ ] Backend running on port 8000
- [ ] Health check returns "healthy"
- [ ] Frontend opened in browser
- [ ] Can upload PDFs
- [ ] Can ask questions and get responses

---

## 🎯 Recommended: Use Batch Files!

**Easiest way:** Just double-click `start_chatbot.bat`

It will:
- ✅ Start backend automatically
- ✅ Start frontend automatically
- ✅ Open browser automatically
- ✅ Everything ready to use!

---

## 🐛 Common Issues

| Issue | Solution |
|-------|----------|
| "Port 8000 already in use" | Kill process using port 8000 or change port in `.env` |
| "Cannot connect to server" | Make sure backend is running in Terminal 1 |
| "Module not found" | Run: `pip install -r backend/requirements.txt` |
| Frontend shows errors | Check browser console (F12) for details |

---

**That's it!** Your chatbot is ready! 🚀

