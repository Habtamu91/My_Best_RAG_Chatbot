# Testing Guide - How to Check if RAG Chatbot Works

## 🧪 Step-by-Step Testing Process

### Step 1: Verify Backend Installation

First, check if all dependencies are installed:

```bash
cd RAG_Chatbot/backend
pip list | findstr "fastapi uvicorn PyPDF2"
```

You should see the packages listed. If not, install them:
```bash
pip install -r requirements.txt
```

### Step 2: Start the Backend Server

Open a terminal and run:

```bash
cd RAG_Chatbot/backend
python run.py
```

**Expected Output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

**✅ Success Indicators:**
- Server starts without errors
- No import errors
- Server is listening on port 8000

### Step 3: Test Backend Health Endpoint

Open a new terminal or use your browser:

**Option A: Browser**
```
http://localhost:8000/health
```

**Option B: Command Line (PowerShell)**
```powershell
Invoke-RestMethod -Uri http://localhost:8000/health
```

**Option C: Command Line (curl)**
```bash
curl http://localhost:8000/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "message": "RAG Chatbot API is running"
}
```

**✅ If you see this, the backend is working!**

### Step 4: Test API Documentation

Open in browser:
```
http://localhost:8000/docs
```

This should show the FastAPI interactive documentation (Swagger UI) where you can test endpoints directly.

### Step 5: Test Frontend Connection

**Option A: Direct File Opening**
1. Navigate to `RAG_Chatbot/frontend/`
2. Double-click `index.html`
3. Open browser console (F12)
4. Check for any errors

**Option B: Local Server (Recommended)**
```bash
cd RAG_Chatbot/frontend
python -m http.server 8080
```
Then open: `http://localhost:8080`

**✅ Check Frontend Console:**
- Open Developer Tools (F12)
- Look for: "Server is not responding" or connection errors
- If no errors appear, the connection is working

### Step 6: Test PDF Upload

1. **Prepare a test PDF** (any PDF document)
2. In the frontend:
   - Click "Choose PDF file"
   - Select your PDF
   - Click "Upload PDF"
   - Wait for processing

**✅ Success Indicators:**
- Status shows: "✓ PDF uploaded successfully! Processed X chunks"
- Chat input becomes enabled
- No error messages

**❌ Common Issues:**
- "Cannot connect to server" → Backend not running
- "Only PDF files are supported" → Wrong file type
- "Error processing PDF" → Check backend terminal for details

### Step 7: Test Chat Functionality

1. Type a question in the chat input (e.g., "What is this document about?")
2. Press Enter or click Send
3. Wait for response

**✅ Success Indicators:**
- Your question appears as a user message (blue bubble on right)
- AI response appears as assistant message (white bubble on left)
- Response is relevant to your question

**❌ Common Issues:**
- "No documents uploaded" → Upload failed, try again
- "Connection error" → Backend may have stopped
- Empty response → Check backend logs

### Step 8: Check Backend Logs

While testing, watch the backend terminal for:
- Upload requests: `POST /api/upload`
- Chat requests: `POST /api/chat`
- Any error messages

**Example successful log:**
```
INFO:     127.0.0.1:xxxxx - "POST /api/upload HTTP/1.1" 200 OK
INFO:     127.0.0.1:xxxxx - "POST /api/chat HTTP/1.1" 200 OK
```

## 🔍 Manual API Testing (Alternative)

If frontend doesn't work, test the API directly:

### Test Upload (PowerShell)
```powershell
$file = "C:\path\to\your\document.pdf"
$uri = "http://localhost:8000/api/upload"
$form = @{
    file = Get-Item -Path $file
}
Invoke-RestMethod -Uri $uri -Method Post -Form $form
```

### Test Chat (PowerShell)
```powershell
$body = @{
    question = "What is this document about?"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/chat" `
    -Method Post `
    -Body $body `
    -ContentType "application/json"
```

## ✅ Verification Checklist

- [ ] Backend starts without errors
- [ ] Health endpoint returns `{"status": "healthy"}`
- [ ] API docs accessible at `/docs`
- [ ] Frontend loads without console errors
- [ ] Frontend can connect to backend (no CORS errors)
- [ ] PDF upload succeeds
- [ ] Chat input becomes enabled after upload
- [ ] Questions return responses
- [ ] Responses are relevant to the PDF content

## 🐛 Troubleshooting Quick Tests

### Test 1: Check if Python can import modules
```bash
cd RAG_Chatbot/backend
python -c "from app.main import app; print('✓ Imports OK')"
```

### Test 2: Check if embedding service works
```bash
cd RAG_Chatbot/backend
python -c "from app.services.embedding import get_embedding_service; es = get_embedding_service(); print('✓ Embedding service OK')"
```

### Test 3: Check if vector store initializes
```bash
cd RAG_Chatbot/backend
python -c "from app.services.vectorstore import get_vector_store; vs = get_vector_store(); print('✓ Vector store OK')"
```

### Test 4: Check if PDF loader works
```bash
cd RAG_Chatbot/backend
python -c "import PyPDF2; print('✓ PyPDF2 installed')"
```

## 📊 Expected Behavior Summary

| Action | Expected Result |
|--------|----------------|
| Start backend | Server runs on port 8000 |
| Open `/health` | Returns `{"status": "healthy"}` |
| Open frontend | UI loads, shows upload section |
| Upload PDF | Status: "Uploaded successfully", chat enabled |
| Ask question | AI response appears in chat |
| Ask follow-up | Gets relevant response |

## 🎯 Quick Test Script

Create and run this quick test:

```python
# quick_test.py
import requests
import json

BASE_URL = "http://localhost:8000"

# Test 1: Health check
print("Test 1: Health Check")
try:
    r = requests.get(f"{BASE_URL}/health")
    print(f"✓ Status: {r.status_code}")
    print(f"✓ Response: {r.json()}")
except Exception as e:
    print(f"✗ Failed: {e}")

# Test 2: Check if upload endpoint exists
print("\nTest 2: Upload Endpoint")
try:
    r = requests.options(f"{BASE_URL}/api/upload")
    print(f"✓ Endpoint accessible: {r.status_code}")
except Exception as e:
    print(f"✗ Failed: {e}")

# Test 3: Check if chat endpoint exists
print("\nTest 3: Chat Endpoint")
try:
    r = requests.options(f"{BASE_URL}/api/chat")
    print(f"✓ Endpoint accessible: {r.status_code}")
except Exception as e:
    print(f"✗ Failed: {e}")

print("\n✓ All tests completed!")
```

Run with:
```bash
cd RAG_Chatbot/backend
pip install requests
python quick_test.py
```

