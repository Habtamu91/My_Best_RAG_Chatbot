@echo off
echo ========================================
echo Starting RAG Chatbot Backend Server
echo ========================================
echo.

cd /d "%~dp0backend"
echo Current directory: %CD%
echo.

echo Installing/Updating dependencies...
C:\ProgramData\anaconda3\python.exe -m pip install -q fastapi uvicorn python-multipart PyPDF2 python-dotenv pydantic chromadb openai
echo.

echo Starting backend server...
echo Backend will be available at: http://localhost:8000
echo API docs at: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo.

C:\ProgramData\anaconda3\python.exe run.py

pause

