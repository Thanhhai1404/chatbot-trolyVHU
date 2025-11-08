@echo off
REM ============================================================================
REM HƯỚNG DẪN TEST GEMINI AI - STEP BY STEP
REM ============================================================================

echo.
echo ============================================================================
echo             TEST CHỨC NĂNG GEMINI AI - VHU CHATBOT
echo ============================================================================
echo.
echo Hướng dẫn test đầy đủ chức năng Gemini AI Integration
echo.

REM ============================================================================
REM STEP 1: PRE-TEST CHECKS
REM ============================================================================

echo ============================================================================
echo STEP 1: KIỂM TRA TRƯỚC KHI TEST
echo ============================================================================
echo.

echo [1/4] Kiểm tra Model...
if not exist "models\vhu-chatbot-gemini-v1.tar.gz" (
    echo ❌ ERROR: Model không tồn tại!
    echo.
    echo Chạy lệnh này để train model:
    echo     rasa train --fixed-model-name vhu-chatbot-gemini-v1
    echo.
    pause
    exit /b 1
)
echo ✅ Model: vhu-chatbot-gemini-v1.tar.gz
echo.

echo [2/4] Kiểm tra .env file...
if not exist ".env" (
    echo ❌ WARNING: File .env không tồn tại!
    echo.
    echo Tạo file .env với nội dung:
    echo     GEMINI_API_KEY=your_api_key_here
    echo.
    pause
    exit /b 1
)
echo ✅ File .env tồn tại
echo.

echo [3/4] Kiểm tra Python packages...
call rasa_env_new\Scripts\activate
python -c "import google.generativeai; import dotenv; print('✅ Packages OK')" 2>nul
if errorlevel 1 (
    echo ❌ ERROR: Missing packages
    echo.
    echo Chạy: pip install google-generativeai python-dotenv
    pause
    exit /b 1
)
echo.

echo [4/4] Kiểm tra Gemini API Key...
python -c "from dotenv import load_dotenv; import os; load_dotenv(); key = os.getenv('GEMINI_API_KEY'); print('✅ API Key:', key[:20] + '...' if key else '❌ No API Key')" 2>nul
echo.

echo ============================================================================
echo ✅ PRE-CHECKS COMPLETED
echo ============================================================================
echo.
pause

REM ============================================================================
REM STEP 2: TEST GEMINI API (UNIT TEST)
REM ============================================================================

echo ============================================================================
echo STEP 2: TEST GEMINI API (UNIT TEST)
echo ============================================================================
echo.
echo Test Gemini API hoạt động KHÔNG CẦN action server...
echo.

python test_gemini_integration.py

echo.
echo Kết quả mong đợi:
echo   ✅ Test 1: Classification PASS
echo   ✅ Test 2: Gemini response có text
echo   ✅ Test 3: VHU question fallback OK
echo   ✅ Test 4: Integration test PASS
echo.
echo Nếu có lỗi, kiểm tra:
echo   - API key trong .env
echo   - Internet connection
echo   - Gemini API quota
echo.
pause

REM ============================================================================
REM STEP 3: TEST ACTION SERVER
REM ============================================================================

echo ============================================================================
echo STEP 3: TEST ACTION SERVER
echo ============================================================================
echo.
echo Bước này sẽ:
echo   1. Start action server (cửa sổ mới)
echo   2. Chờ 10 giây
echo   3. Test action_gemini_fallback
echo.
pause

echo Starting Action Server...
start "VHU Action Server" /MIN cmd /c "cd /d %CD% && call rasa_env_new\Scripts\activate && rasa run actions"

echo.
echo Đợi action server khởi động (10 giây)...
timeout /t 10 /nobreak >nul

echo.
echo Testing action server...
python debug_gemini_fallback.py

echo.
echo Kết quả mong đợi:
echo   ✅ Action server is running
echo   ✅ action_gemini_fallback is registered
echo   ✅ Gemini responded successfully
echo.
echo Nếu FAIL, check:
echo   - Cửa sổ Action Server có error không
echo   - Port 5055 có bị chiếm không
echo.
pause

REM ============================================================================
REM STEP 4: TEST RASA SHELL (INTEGRATION TEST)
REM ============================================================================

echo ============================================================================
echo STEP 4: TEST TRONG RASA SHELL
echo ============================================================================
echo.
echo Bây giờ sẽ mở Rasa Shell để test thực tế...
echo.
echo TEST CASES:
echo.
echo 1. Câu hỏi NGOÀI PHẠM VI (should use Gemini):
echo    - "thời tiết hôm nay thế nào?"
echo    - "cho mua gì ngon?"
echo    - "python là gì?"
echo.
echo 2. Câu hỏi VHU (should use existing actions):
echo    - "học phí là bao nhiêu?"
echo    - "trường có những ngành nào?"
echo    - "VHU ở đâu?"
echo.
echo ============================================================================
echo.
echo KẾT QUẢ ĐÚNG:
echo.
echo ✅ Câu ngoài phạm vi:
echo    → Gemini response (dài, có thông tin chi tiết)
echo    → Có dòng "💙 Bạn có muốn hỏi gì về VHU?"
echo.
echo ✅ Câu VHU:
echo    → Response từ existing action
echo    → Format đẹp với emoji và markdown
echo.
echo ❌ Câu ngoài phạm vi:
echo    → "Xin lỗi, mình chưa có thông tin này"
echo    → Nghĩa là Gemini CHƯA hoạt động
echo.
echo ============================================================================
echo.
echo Press any key to start Rasa Shell...
pause >nul

rasa shell --model models/vhu-chatbot-gemini-v1.tar.gz

REM ============================================================================
REM CLEANUP
REM ============================================================================

echo.
echo ============================================================================
echo TEST COMPLETED
echo ============================================================================
echo.
echo Để tắt action server:
echo   - Đóng cửa sổ "VHU Action Server"
echo   - Hoặc tìm process và kill
echo.
echo Để test lại, chạy: test_gemini_full.bat
echo.
pause
