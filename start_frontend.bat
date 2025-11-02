@echo off
echo ========================================
echo Starting RAG Chatbot Frontend
echo ========================================
echo.

cd /d "%~dp0frontend"
echo Current directory: %CD%
echo.

echo Starting frontend server...
echo Frontend will be available at: http://localhost:8080
echo.
echo Press Ctrl+C to stop the server
echo.

C:\ProgramData\anaconda3\python.exe -m http.server 8080

pause

