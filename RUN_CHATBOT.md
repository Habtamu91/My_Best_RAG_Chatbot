# How to Run RAG Chatbot (Backend + Frontend)

## 🚀 Complete Setup Guide

### Step 1: Install Dependencies

First, make sure all backend dependencies are installed:

```powershell
cd C:\Users\dell\Desktop\BizPredict\RAG_Chatbot\backend
C:\ProgramData\anaconda3\python.exe -m pip install fastapi uvicorn python-multipart PyPDF2 python-dotenv pydantic chromadb
```

If you're using OpenAI (which you are):
```powershell
C:\ProgramData\anaconda3\python.exe -m pip install openai
```

If you want to use Gemini instead:
```powershell
C:\ProgramData\anaconda3\python.exe -m pip install google-generativeai
```

### Step 2: Verify .env File

Make sure your `.env` file exists and is configured:

```powershell
cd C:\Users\dell\Desktop\BizPredict\RAG_Chatbot
Get-Content .env
```

You should see your `OPENAI_API_KEY` configured (which you already have! ✓)

### Step 3: Start the Backend Server

Open **Terminal/PowerShell Window 1**:

```powershell
cd C:\Users\dell\Desktop\BizPredict\RAG_Chatbot\backend
C:\ProgramData\anaconda3\python.exe run.py
```

**Expected Output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000
```

**✅ Keep this terminal window open!** The backend must stay running.

### Step 4: Verify Backend is Running

Open a **NEW Terminal/PowerShell Window** and test:

```powershell
Invoke-RestMethod -Uri http://localhost:8000/health
```

**Expected Output:**
```json
{
  "status": "healthy",
  "message": "RAG Chatbot API is running"
}
```

If you see this, the backend is working! ✅

### Step 5: Open the Frontend

You have **3 options**:

#### **Option A: Direct File Open (Easiest)**
1. Navigate to: `C:\Users\dell\Desktop\BizPredict\RAG_Chatbot\frontend\`
2. Double-click `index.html`
3. It will open in your default browser

#### **Option B: Local Server (Recommended)**
Open **Terminal/PowerShell Window 2**:

```powershell
cd C:\Users\dell\Desktop\BizPredict\RAG_Chatbot\frontend
C:\ProgramData\anaconda3\python.exe -m http.server 8080
```

Then open your browser and go to:
```
http://localhost:8080
```

#### **Option C: VS Code Live Server**
If you have VS Code:
1. Right-click on `index.html`
2. Select "Open with Live Server"

### Step 6: Test the Chatbot

1. **Upload a PDF**: 
   - Click "Choose PDF file"
   - Select any PDF document
   - Click "Upload PDF"
   - Wait for: "✓ PDF uploaded successfully!"

2. **Ask a Question**:
   - Type a question (e.g., "What is this document about?")
   - Press Enter or click "Send"
   - You should see an AI response!

---

## 📋 Quick Reference

### Run Backend:
```powershell
cd C:\Users\dell\Desktop\BizPredict\RAG_Chatbot\backend
C:\ProgramData\anaconda3\python.exe run.py
```

### Run Frontend (Option B):
```powershell
cd C:\Users\dell\Desktop\BizPredict\RAG_Chatbot\frontend
C:\ProgramData\anaconda3\python.exe -m http.server 8080
```

### Test Backend Health:
```powershell
Invoke-RestMethod -Uri http://localhost:8000/health
```

---

## 🐛 Troubleshooting

### Backend won't start?
- Check if port 8000 is already in use
- Verify all dependencies are installed
- Check `.env` file exists and has API key
- Look for error messages in the terminal

### Frontend can't connect?
- Make sure backend is running on port 8000
- Check browser console (F12) for errors
- Verify CORS is enabled (it is by default)

### API errors?
- Check your OpenAI API key is valid
- Verify you have API credits
- Check backend terminal for error messages

### PDF upload fails?
- Make sure PDF file is not corrupted
- Check file size (large files may timeout)
- Verify backend is running

---

## 🎯 What You Should See

### Terminal 1 (Backend):
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     127.0.0.1:xxxxx - "POST /api/upload HTTP/1.1" 200 OK
INFO:     127.0.0.1:xxxxx - "POST /api/chat HTTP/1.1" 200 OK
```

### Browser (Frontend):
- Clean interface with upload section on left
- Chat section on right
- Upload PDF → Ask questions → Get AI responses!

---

## ✅ Checklist

- [ ] Backend dependencies installed
- [ ] `.env` file configured with API key
- [ ] Backend server running on port 8000
- [ ] Health endpoint returns "healthy"
- [ ] Frontend opened in browser
- [ ] Can upload PDFs
- [ ] Can ask questions and get responses

---

**You're all set!** 🎉 Now you can upload PDFs and chat with your documents!

