@echo off
echo ========================================
echo TEST GEMINI AI INTEGRATION
echo ========================================
echo.

echo [*] Activating virtual environment...
call rasa_env_new\Scripts\activate.bat
echo.

echo [1] Test Gemini API Key...
python test_gemini_integration.py
echo.

echo ========================================
echo TEST HOAN THANH!
echo ========================================
echo.
echo Neu thanh cong, ban co the:
echo 1. Chay action server: rasa run actions
echo 2. Chay chatbot: rasa shell
echo.
pause
