@echo off
echo ========================================
echo START GEMINI CHATBOT - FULL SYSTEM
echo ========================================
echo.
echo Chuẩn bị khởi động hệ thống...
echo.

REM Check model exists
if not exist "models\vhu-chatbot-gemini-v1.tar.gz" (
    echo ❌ ERROR: Model vhu-chatbot-gemini-v1.tar.gz không tồn tại!
    echo.
    echo Chạy lệnh này để train model:
    echo     rasa train --fixed-model-name vhu-chatbot-gemini-v1
    echo.
    pause
    exit /b 1
)

echo ✅ Model found: vhu-chatbot-gemini-v1.tar.gz
echo.

REM Check .env file
if not exist ".env" (
    echo ❌ WARNING: File .env không tồn tại!
    echo Gemini AI sẽ không hoạt động mà không có API key.
    echo.
    echo Tạo file .env và thêm:
    echo     GEMINI_API_KEY=your_api_key_here
    echo.
    pause
)

echo ========================================
echo STEP 1: Starting ACTION SERVER
echo ========================================
echo.
echo Đang khởi động action server...
echo Port: 5055
echo.

REM Start action server in new window
start "VHU Action Server" cmd /k "cd /d %CD% && call rasa_env_new\Scripts\activate && rasa run actions --port 5055"

echo Đợi action server khởi động...
timeout /t 5 /nobreak >nul

echo ✅ Action server đã start!
echo.

echo ========================================
echo STEP 2: Starting RASA SERVER  
echo ========================================
echo.
echo Đang khởi động Rasa server...
echo Model: vhu-chatbot-gemini-v1.tar.gz
echo Port: 5005
echo.

REM Wait a bit more
timeout /t 2 /nobreak >nul

REM Start Rasa server in new window
start "VHU Rasa Server" cmd /k "cd /d %CD% && call rasa_env_new\Scripts\activate && rasa run --model models/vhu-chatbot-gemini-v1.tar.gz --port 5005 --enable-api"

echo Đợi Rasa server khởi động...
timeout /t 10 /nobreak >nul

echo ✅ Rasa server đã start!
echo.

echo ========================================
echo STEP 3: Testing SYSTEM
echo ========================================
echo.

REM Test if servers are up
python debug_gemini_fallback.py

echo.
echo ========================================
echo STEP 4: Starting RASA SHELL
echo ========================================
echo.
echo Bạn có thể test bot ngay bây giờ!
echo.
echo Test questions:
echo   1. "thời tiết hôm nay thế nào?"  (Gemini)
echo   2. "cho mua gì ngon?"             (Gemini)
echo   3. "học phí là bao nhiêu?"        (VHU action)
echo.
echo Press any key to open Rasa Shell...
pause >nul

REM Start Rasa shell
start "VHU Chatbot Shell" cmd /k "cd /d %CD% && call rasa_env_new\Scripts\activate && rasa shell --model models/vhu-chatbot-gemini-v1.tar.gz"

echo.
echo ========================================
echo ✅ HỆ THỐNG ĐÃ KHỞI ĐỘNG HOÀN TẤT!
echo ========================================
echo.
echo 🖥️  3 cửa sổ đã mở:
echo     1. Action Server (port 5055)
echo     2. Rasa Server (port 5005)
echo     3. Rasa Shell (chat interface)
echo.
echo 📝 Để tắt hệ thống:
echo     - Đóng tất cả cửa sổ terminal
echo     - Hoặc Ctrl+C trong mỗi cửa sổ
echo.
echo 🎯 Enjoy testing Gemini AI!
echo.
pause
