@echo off
REM ====================================================================
REM  🚀 QUICK START - TEST GEMINI AI IN RASA SHELL
REM ====================================================================

echo.
echo ============================================================
echo       🤖 GEMINI AI - RASA SHELL TEST
echo ============================================================
echo.

echo [1/3] Checking model...
if exist "models\vhu-chatbot-gemini-v1.tar.gz" (
    echo ✓ Model found: vhu-chatbot-gemini-v1.tar.gz
) else (
    echo ✗ Model not found!
    echo Please train first: rasa train
    pause
    exit /b 1
)

echo.
echo [2/3] Starting Action Server...
echo Please wait for "Action endpoint is up and running"
echo.
start "Action Server" cmd /k "call rasa_env_new\Scripts\activate.bat && rasa run actions"

echo Waiting 10 seconds for action server to start...
timeout /t 10 /nobreak > nul

echo.
echo [3/3] Starting Rasa Shell...
echo.
echo ============================================================
echo     📝 TEST COMMANDS:
echo ============================================================
echo.
echo   OUT-OF-SCOPE (Gemini will answer):
echo   - "thời tiết hôm nay thế nào?"
echo   - "python là gì?"
echo   - "cho tôi món ăn ngon"
echo.
echo   VHU QUESTIONS (Existing actions):
echo   - "học phí là bao nhiêu?"
echo   - "trường có những ngành nào?"
echo   - "VHU ở đâu?"
echo.
echo ============================================================
echo.

call rasa_env_new\Scripts\activate.bat
rasa shell --model models/vhu-chatbot-gemini-v1.tar.gz

pause
