# How to Set Up OpenAI API Key

## Step 1: Get Your OpenAI API Key

1. Go to: **https://platform.openai.com/api-keys**
2. Sign up or log in to your OpenAI account
3. Click **"Create new secret key"**
4. Copy your API key (it looks like: `sk-...`)
   - ⚠️ **Important**: Copy it immediately - you won't be able to see it again!

## Step 2: Add API Key to .env File

### Option A: Edit the .env File Directly

1. Navigate to: `C:\Users\dell\Desktop\BizPredict\RAG_Chatbot\`
2. Open the `.env` file in any text editor (Notepad, VS Code, etc.)
3. Find this line:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```
4. Replace `your_openai_api_key_here` with your actual API key:
   ```
   OPENAI_API_KEY=sk-your-actual-api-key-here
   ```
5. Save the file

### Option B: Edit from PowerShell

Run this command (replace `YOUR_API_KEY` with your actual key):

```powershell
cd C:\Users\dell\Desktop\BizPredict\RAG_Chatbot
(Get-Content .env) -replace 'your_openai_api_key_here', 'YOUR_API_KEY' | Set-Content .env
```

Or manually edit:
```powershell
notepad .env
```

## Step 3: Restart the Backend Server

After adding the API key:

1. Stop the current server (Ctrl+C in the terminal running it)
2. Restart the server:
   ```powershell
   cd C:\Users\dell\Desktop\BizPredict\RAG_Chatbot\backend
   C:\ProgramData\anaconda3\python.exe run.py
   ```

## Step 4: Verify It's Working

1. The server should start without errors
2. Try uploading a PDF in the frontend
3. Ask a question - you should get intelligent AI responses!

## Example .env File Content

Your `.env` file should look like this (with your actual key):

```
OPENAI_API_KEY=sk-proj-abc123xyz789...
USE_OPENAI=true
LLM_MODEL=gpt-3.5-turbo
```

## Troubleshooting

### "Invalid API Key" Error
- Make sure you copied the entire key (starts with `sk-`)
- Check there are no extra spaces before or after the key
- Verify the key is active at https://platform.openai.com/api-keys

### API Key Not Being Read
- Make sure the `.env` file is in the `RAG_Chatbot` folder (not in `backend`)
- Restart the server after editing `.env`
- Check that `USE_OPENAI=true` is set

### Don't Have an OpenAI Account?
1. Go to https://platform.openai.com/signup
2. Create a free account
3. You get $5 in free credits to try it out!

---

**Note**: Keep your API key secret! Never commit the `.env` file to Git or share it publicly.

