@echo off
echo ========================================
echo    VHU CHATBOT - STARTUP SCRIPT
echo    Created by: Hai - VHU Student
echo ========================================
echo.

REM Check if conda is available
where conda >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Conda not found! Please install Anaconda/Miniconda first.
    pause
    exit /b 1
)

echo [1/4] Activating conda environment 'rasa'...
call conda activate rasa
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Failed to activate conda environment 'rasa'
    echo Please run: conda create -n rasa python=3.10 -y
    pause
    exit /b 1
)

echo [2/4] Starting Rasa Action Server (Port 5055)...
start "VHU Chatbot - Action Server" cmd /k "conda activate rasa && cd /d %~dp0 && rasa run actions --port 5055"
timeout /t 3 /nobreak >nul

echo [3/4] Starting Rasa Core Server (Port 5005)...
start "VHU Chatbot - Core Server" cmd /k "conda activate rasa && cd /d %~dp0 && rasa run --enable-api --cors * --port 5005"
timeout /t 5 /nobreak >nul

echo [4/4] Opening Web Interface...
start "VHU Chatbot - Frontend" "http://127.0.0.1:5500/frontend/index.html"

echo.
echo ========================================
echo    SERVERS STARTED SUCCESSFULLY!
echo ========================================
echo.
echo Action Server: http://localhost:5055
echo Core Server:   http://localhost:5005
echo Web Interface: http://127.0.0.1:5500/frontend/index.html
echo.
echo [IMPORTANT] You need to:
echo 1. Open frontend/index.html in VS Code
echo 2. Right-click and select "Open with Live Server"
echo.
echo Press Ctrl+C in each window to stop servers
echo ========================================
pause
