# Fix OpenAI API Key Error

## 🔴 Error You're Seeing

```
Error code: 401 - Incorrect API key provided
```

This means your OpenAI API key is either:
- ❌ Invalid or expired
- ❌ Has extra spaces/newlines
- ❌ From wrong OpenAI account/project

## ✅ Solution Steps

### Step 1: Get a Fresh API Key

1. **Go to**: https://platform.openai.com/api-keys
2. **Sign in** to your OpenAI account
3. **Delete the old key** (if you want) or create a **new one**
4. Click **"Create new secret key"**
5. **Copy the key immediately** (you can't see it again!)

### Step 2: Update .env File

1. **Open** `.env` file:
   ```powershell
   cd C:\Users\dell\Desktop\BizPredict\RAG_Chatbot
   notepad .env
   ```

2. **Find this line**:
   ```
   OPENAI_API_KEY=sk-proj-...
   ```

3. **Replace with your NEW key**:
   ```
   OPENAI_API_KEY=sk-proj-YOUR_NEW_KEY_HERE
   ```

4. **Important**: Make sure:
   - ✅ No spaces before or after the key
   - ✅ No quotes around the key
   - ✅ Key is on one line only
   - ✅ Key starts with `sk-`

5. **Save** the file

### Step 3: Restart Backend Server

**Important**: You must restart the backend for changes to take effect!

1. **Stop** the current backend (Ctrl+C in the terminal)
2. **Restart** it:
   ```powershell
   cd C:\Users\dell\Desktop\BizPredict\RAG_Chatbot\backend
   C:\ProgramData\anaconda3\python.exe run.py
   ```

### Step 4: Test Again

1. Go back to your browser
2. **Upload PDF again**
3. Should work now! ✅

---

## 🔄 Alternative: Use Gemini Instead (FREE!)

If you're having trouble with OpenAI, you can switch to **Gemini** (free tier available):

### Quick Switch to Gemini

1. **Get Gemini API key**: https://makersuite.google.com/app/apikey
2. **Update .env**:
   ```
   GEMINI_API_KEY=your_gemini_key_here
   LLM_PROVIDER=gemini
   ```
3. **Install Gemini package**:
   ```powershell
   C:\ProgramData\anaconda3\python.exe -m pip install google-generativeai
   ```
4. **Restart backend**

---

## 📝 Example of Correct .env Format

```env
OPENAI_API_KEY=sk-proj-abc123xyz789...fullkeyhere
USE_OPENAI=true
```

**NOT:**
```env
OPENAI_API_KEY="sk-proj-abc123xyz789"  ❌ No quotes
OPENAI_API_KEY= sk-proj-abc123xyz789   ❌ No leading space
OPENAI_API_KEY=sk-proj-abc123xyz789     ❌ No trailing space
```

---

## 🔍 Verify Your Key Format

After updating, check:
```powershell
cd C:\Users\dell\Desktop\BizPredict\RAG_Chatbot
Get-Content .env | Select-String "OPENAI_API_KEY"
```

Should show:
```
OPENAI_API_KEY=sk-proj-...yourkey...
```

---

## 💡 Pro Tips

1. **Never commit .env to Git** - it's already in .gitignore ✅
2. **Keep keys secure** - don't share them
3. **Rotate keys regularly** for security
4. **Use Gemini for testing** - it's free!

---

**After updating, restart the backend and try uploading again!** 🚀

