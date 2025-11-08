@echo off
echo ========================================
echo TESTING GEMINI AI IN RASA SHELL - V2
echo ========================================
echo.
echo Model: vhu-chatbot-gemini-v1
echo.
echo Test questions (type these in shell):
echo 1. "thoi tiet hom nay the nao?"     (Weather - out of scope)
echo 2. "cho mua gi ngon?"               (Food - out of scope)
echo 3. "hoc phi cua truong la bao nhieu?" (VHU question - should use existing action)
echo.
echo Starting Rasa Shell in 3 seconds...
timeout /t 3 >nul
echo.

cd /d D:\workspace\Chatbot
call rasa_env_new\Scripts\activate && rasa shell --model models/vhu-chatbot-gemini-v1.tar.gz
