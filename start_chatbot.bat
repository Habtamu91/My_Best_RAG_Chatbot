@echo off
echo ========================================
echo Starting RAG Chatbot (Backend + Frontend)
echo ========================================
echo.

echo This will open two windows:
echo 1. Backend server (port 8000)
echo 2. Frontend server (port 8080)
echo.

pause

echo Starting backend...
start "RAG Chatbot Backend" cmd /k "cd /d %~dp0backend && C:\ProgramData\anaconda3\python.exe run.py"

timeout /t 3 /nobreak >nul

echo Starting frontend...
start "RAG Chatbot Frontend" cmd /k "cd /d %~dp0frontend && C:\ProgramData\anaconda3\python.exe -m http.server 8080"

timeout /t 2 /nobreak >nul

echo.
echo ========================================
echo Both servers are starting!
echo ========================================
echo.
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:8080
echo.
echo The browser will open automatically...
echo.

timeout /t 3 /nobreak >nul
start http://localhost:8080

echo.
echo Close this window when done (servers will keep running)
pause

