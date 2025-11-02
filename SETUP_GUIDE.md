# RAG Chatbot Setup Guide

## 📋 Required vs Optional Configuration

### ✅ REQUIRED (Choose ONE):

**Option 1: Gemini API (Recommended - FREE!)**
```
GEMINI_API_KEY=your_gemini_api_key_here
```
👉 Get it from: https://makersuite.google.com/app/apikey

**Option 2: OpenAI API**
```
OPENAI_API_KEY=your_openai_api_key_here
```
👉 Get it from: https://platform.openai.com/api-keys

**Option 3: Use Local Models (FREE, but slower)**
```
# Just leave both keys empty - uses sentence-transformers (local)
```

### ⚙️ OPTIONAL Settings:

All these have default values - you can leave them as-is:

```
# Which provider to use (if you have multiple keys)
LLM_PROVIDER=gemini

# Model selection
GEMINI_MODEL=gemini-pro
LLM_MODEL=gpt-3.5-turbo

# Chunking (how text is split)
CHUNK_SIZE=1000
CHUNK_OVERLAP=200

# How many results to retrieve
TOP_K_RESULTS=3

# Vector database type
VECTOR_STORE_TYPE=chroma
```

---

## 🚀 Quick Setup Steps

### 1. Get Gemini API Key (Recommended)
1. Go to: https://makersuite.google.com/app/apikey
2. Sign in with Google account
3. Click "Get API key"
4. Copy your key (starts with `AIzaSy...`)

### 2. Create .env File

Create `.env` file in `RAG_Chatbot` folder:

```powershell
cd C:\Users\dell\Desktop\BizPredict\RAG_Chatbot
notepad .env
```

Add this (replace with your actual key):

```
GEMINI_API_KEY=AIzaSy-your-actual-key-here
LLM_PROVIDER=gemini
```

### 3. Install Google Generative AI Package

```powershell
cd C:\Users\dell\Desktop\BizPredict\RAG_Chatbot\backend
C:\ProgramData\anaconda3\python.exe -m pip install google-generativeai
```

### 4. Restart Backend Server

```powershell
cd C:\Users\dell\Desktop\BizPredict\RAG_Chatbot\backend
C:\ProgramData\anaconda3\python.exe run.py
```

### 5. Test It!

1. Open frontend: `RAG_Chatbot\frontend\index.html`
2. Upload a PDF
3. Ask questions!

---

## 📝 Minimal .env File

If you just want to get started quickly, create `.env` with ONLY this:

```
GEMINI_API_KEY=your_key_here
```

Everything else will use defaults!

---

## ❓ Which Fields Do I Need to Update?

### For Gemini (Recommended):
**REQUIRED:**
- `GEMINI_API_KEY` ← **Update this!**

**Optional:**
- `LLM_PROVIDER=gemini` (already default)
- `GEMINI_MODEL=gemini-pro` (already default)

### For OpenAI:
**REQUIRED:**
- `OPENAI_API_KEY` ← **Update this!**
- `USE_OPENAI=true`

**Optional:**
- `LLM_MODEL=gpt-3.5-turbo` (already default)

### For Local (Free, No API Key):
**REQUIRED:**
- Nothing! Just leave API keys empty

---

## 🔧 Installation Required

When you add Gemini support, install:

```powershell
C:\ProgramData\anaconda3\python.exe -m pip install google-generativeai
```

---

## ✅ Verification

After setup, test if it works:

1. Check backend is running: http://localhost:8000/health
2. Upload a PDF in frontend
3. Ask: "What is this document about?"
4. Should get intelligent AI response!

---

**That's it!** You're ready to use the chatbot! 🎉

