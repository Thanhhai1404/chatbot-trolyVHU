@echo off
REM ===================================================================
REM QUICK START - CHỈ CHẠY ACTION SERVER + SHELL
REM ===================================================================

echo ========================================
echo GEMINI CHATBOT - QUICK START
echo ========================================
echo.

REM Check model
if not exist "models\vhu-chatbot-gemini-v1.tar.gz" (
    echo ❌ Model not found!
    pause
    exit /b 1
)

echo ✅ Model: vhu-chatbot-gemini-v1.tar.gz
echo.

echo Starting action server...
echo (Cửa sổ mới sẽ mở)
echo.

REM Start action server in background
start "Action Server" /MIN cmd /c "cd /d %CD% && call rasa_env_new\Scripts\activate && rasa run actions"

echo Waiting for action server (10 seconds)...
timeout /t 10 /nobreak >nul

echo.
echo ========================================
echo STARTING RASA SHELL
echo ========================================
echo.
echo Test với các câu hỏi:
echo   • "thời tiết hôm nay thế nào?"
echo   • "cho mua gì ngon?"
echo   • "học phí là bao nhiêu?"
echo.
echo ========================================
echo.

REM Activate và run shell
call rasa_env_new\Scripts\activate
rasa shell --model models/vhu-chatbot-gemini-v1.tar.gz
