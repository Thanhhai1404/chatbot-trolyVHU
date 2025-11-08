@echo off
echo ========================================
echo    VHU CHATBOT - QUICK START
echo    Created by: Hai - VHU Student
echo ========================================
echo.

echo Starting servers...
echo.

REM Start Action Server
echo [1/3] Starting Action Server (Port 5055)...
start "Action Server" cmd /k "conda activate rasa && cd /d %~dp0 && rasa run actions --port 5055"
timeout /t 3 /nobreak >nul

REM Start Rasa Server
echo [2/3] Starting Rasa Server (Port 5005)...
start "Rasa Server" cmd /k "conda activate rasa && cd /d %~dp0 && rasa run --enable-api --cors * --port 5005"
timeout /t 5 /nobreak >nul

REM Start Frontend Server
echo [3/3] Starting Frontend Server (Port 8000)...
start "Frontend Server" cmd /k "cd /d %~dp0frontend && python -m http.server 8000"
timeout /t 2 /nobreak >nul

echo.
echo ========================================
echo    ALL SERVERS STARTED!
echo ========================================
echo.
echo Action Server: http://localhost:5055
echo Rasa Server:   http://localhost:5005
echo Frontend:      http://localhost:8000
echo.
echo Opening browser...
start http://localhost:8000
echo.
echo Press any key to stop all servers...
pause >nul

REM Stop all servers
taskkill /FI "WindowTitle eq Action Server*" /T /F >nul 2>&1
taskkill /FI "WindowTitle eq Rasa Server*" /T /F >nul 2>&1
taskkill /FI "WindowTitle eq Frontend Server*" /T /F >nul 2>&1

echo All servers stopped.
