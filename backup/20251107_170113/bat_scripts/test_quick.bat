@echo off
REM ============================================================================
REM QUICK TEST - Test nhanh Gemini AI
REM ============================================================================

echo.
echo ========================================
echo     QUICK TEST - GEMINI AI
echo ========================================
echo.

REM Check model
if not exist "models\vhu-chatbot-gemini-v1.tar.gz" (
    echo ❌ Model not found! Run: rasa train --fixed-model-name vhu-chatbot-gemini-v1
    pause
    exit /b 1
)

echo ✅ Model: vhu-chatbot-gemini-v1.tar.gz
echo.

REM Test 1: Unit test
echo ========================================
echo TEST 1: GEMINI API (Unit Test)
echo ========================================
echo.
call rasa_env_new\Scripts\activate
python test_gemini_integration.py
echo.
echo ⏸️  Pause để xem kết quả Test 1...
pause
cls

REM Test 2: Start action server và test
echo ========================================
echo TEST 2: ACTION SERVER
echo ========================================
echo.
echo Starting action server (new window)...
start "Action Server" /MIN cmd /c "cd /d %CD% && call rasa_env_new\Scripts\activate && rasa run actions"

echo Waiting 10 seconds...
timeout /t 10 /nobreak >nul

echo.
echo Testing action server...
python debug_gemini_fallback.py
echo.
echo ⏸️  Pause để xem kết quả Test 2...
pause
cls

REM Test 3: Rasa Shell
echo ========================================
echo TEST 3: RASA SHELL (Integration)
echo ========================================
echo.
echo CÂU HỎI TEST:
echo.
echo 1. NGOÀI PHẠM VI (Gemini):
echo    thời tiết hôm nay thế nào?
echo    cho mua gì ngon?
echo.
echo 2. VHU DOMAIN (Existing):
echo    học phí là bao nhiêu?
echo    trường có những ngành nào?
echo.
echo ========================================
echo.
pause

rasa shell --model models/vhu-chatbot-gemini-v1.tar.gz

echo.
echo ========================================
echo TEST COMPLETED!
echo ========================================
echo.
pause
