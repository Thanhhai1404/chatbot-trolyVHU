# ============================================================================
# HƯỚNG DẪN TEST GEMINI AI - POWERSHELL VERSION
# ============================================================================

Write-Host "`n============================================================================" -ForegroundColor Cyan
Write-Host "             TEST CHỨC NĂNG GEMINI AI - VHU CHATBOT" -ForegroundColor Yellow
Write-Host "============================================================================`n" -ForegroundColor Cyan
Write-Host "Hướng dẫn test đầy đủ chức năng Gemini AI Integration`n" -ForegroundColor White

# ============================================================================
# STEP 1: PRE-TEST CHECKS
# ============================================================================

Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host "STEP 1: KIỂM TRA TRƯỚC KHI TEST" -ForegroundColor Yellow
Write-Host "============================================================================`n" -ForegroundColor Cyan

Write-Host "[1/4] Kiểm tra Model..." -ForegroundColor White
if (-Not (Test-Path "models\vhu-chatbot-gemini-v1.tar.gz")) {
    Write-Host "❌ ERROR: Model không tồn tại!`n" -ForegroundColor Red
    Write-Host "Chạy lệnh này để train model:" -ForegroundColor Yellow
    Write-Host "    rasa train --fixed-model-name vhu-chatbot-gemini-v1`n" -ForegroundColor White
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host "✅ Model: vhu-chatbot-gemini-v1.tar.gz`n" -ForegroundColor Green

Write-Host "[2/4] Kiểm tra .env file..." -ForegroundColor White
if (-Not (Test-Path ".env")) {
    Write-Host "❌ WARNING: File .env không tồn tại!`n" -ForegroundColor Red
    Write-Host "Tạo file .env với nội dung:" -ForegroundColor Yellow
    Write-Host "    GEMINI_API_KEY=your_api_key_here`n" -ForegroundColor White
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host "✅ File .env tồn tại`n" -ForegroundColor Green

Write-Host "[3/4] Kiểm tra Python packages..." -ForegroundColor White
& rasa_env_new\Scripts\activate.ps1
$packageCheck = python -c "import google.generativeai; import dotenv; print('OK')" 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ ERROR: Missing packages`n" -ForegroundColor Red
    Write-Host "Chạy: pip install google-generativeai python-dotenv`n" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host "✅ Packages OK`n" -ForegroundColor Green

Write-Host "[4/4] Kiểm tra Gemini API Key..." -ForegroundColor White
python -c "from dotenv import load_dotenv; import os; load_dotenv(); key = os.getenv('GEMINI_API_KEY'); print('✅ API Key:', key[:20] + '...' if key else '❌ No API Key')"
Write-Host ""

Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host "✅ PRE-CHECKS COMPLETED" -ForegroundColor Green
Write-Host "============================================================================`n" -ForegroundColor Cyan
Read-Host "Press Enter to continue"

# ============================================================================
# STEP 2: TEST GEMINI API (UNIT TEST)
# ============================================================================

Write-Host "`n============================================================================" -ForegroundColor Cyan
Write-Host "STEP 2: TEST GEMINI API (UNIT TEST)" -ForegroundColor Yellow
Write-Host "============================================================================`n" -ForegroundColor Cyan
Write-Host "Test Gemini API hoạt động KHÔNG CẦN action server...`n" -ForegroundColor White

python test_gemini_integration.py

Write-Host "`nKết quả mong đợi:" -ForegroundColor Yellow
Write-Host "  ✅ Test 1: Classification PASS" -ForegroundColor Green
Write-Host "  ✅ Test 2: Gemini response có text" -ForegroundColor Green
Write-Host "  ✅ Test 3: VHU question fallback OK" -ForegroundColor Green
Write-Host "  ✅ Test 4: Integration test PASS`n" -ForegroundColor Green
Write-Host "Nếu có lỗi, kiểm tra:" -ForegroundColor Yellow
Write-Host "  - API key trong .env" -ForegroundColor White
Write-Host "  - Internet connection" -ForegroundColor White
Write-Host "  - Gemini API quota`n" -ForegroundColor White
Read-Host "Press Enter to continue"

# ============================================================================
# STEP 3: TEST ACTION SERVER
# ============================================================================

Write-Host "`n============================================================================" -ForegroundColor Cyan
Write-Host "STEP 3: TEST ACTION SERVER" -ForegroundColor Yellow
Write-Host "============================================================================`n" -ForegroundColor Cyan
Write-Host "Bước này sẽ:" -ForegroundColor White
Write-Host "  1. Start action server (cửa sổ mới)" -ForegroundColor White
Write-Host "  2. Chờ 10 giây" -ForegroundColor White
Write-Host "  3. Test action_gemini_fallback`n" -ForegroundColor White
Read-Host "Press Enter to start"

Write-Host "Starting Action Server..." -ForegroundColor Yellow
$actionServerCmd = "cd '$PWD'; rasa_env_new\Scripts\activate.ps1; rasa run actions"
Start-Process powershell -ArgumentList "-NoExit", "-Command", $actionServerCmd -WindowStyle Minimized

Write-Host "`nĐợi action server khởi động (10 giây)..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

Write-Host "`nTesting action server..." -ForegroundColor Yellow
python debug_gemini_fallback.py

Write-Host "`nKết quả mong đợi:" -ForegroundColor Yellow
Write-Host "  ✅ Action server is running" -ForegroundColor Green
Write-Host "  ✅ action_gemini_fallback is registered" -ForegroundColor Green
Write-Host "  ✅ Gemini responded successfully`n" -ForegroundColor Green
Write-Host "Nếu FAIL, check:" -ForegroundColor Yellow
Write-Host "  - Cửa sổ Action Server có error không" -ForegroundColor White
Write-Host "  - Port 5055 có bị chiếm không`n" -ForegroundColor White
Read-Host "Press Enter to continue"

# ============================================================================
# STEP 4: TEST RASA SHELL (INTEGRATION TEST)
# ============================================================================

Write-Host "`n============================================================================" -ForegroundColor Cyan
Write-Host "STEP 4: TEST TRONG RASA SHELL" -ForegroundColor Yellow
Write-Host "============================================================================`n" -ForegroundColor Cyan
Write-Host "Bây giờ sẽ mở Rasa Shell để test thực tế...`n" -ForegroundColor White
Write-Host "TEST CASES:`n" -ForegroundColor Yellow

Write-Host "1. Câu hỏi NGOÀI PHẠM VI (should use Gemini):" -ForegroundColor Cyan
Write-Host "   - `"thời tiết hôm nay thế nào?`"" -ForegroundColor White
Write-Host "   - `"cho mua gì ngon?`"" -ForegroundColor White
Write-Host "   - `"python là gì?`"`n" -ForegroundColor White

Write-Host "2. Câu hỏi VHU (should use existing actions):" -ForegroundColor Cyan
Write-Host "   - `"học phí là bao nhiêu?`"" -ForegroundColor White
Write-Host "   - `"trường có những ngành nào?`"" -ForegroundColor White
Write-Host "   - `"VHU ở đâu?`"`n" -ForegroundColor White

Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host "KẾT QUẢ ĐÚNG:" -ForegroundColor Yellow
Write-Host "============================================================================`n" -ForegroundColor Cyan

Write-Host "✅ Câu ngoài phạm vi:" -ForegroundColor Green
Write-Host "   → Gemini response (dài, có thông tin chi tiết)" -ForegroundColor White
Write-Host "   → Có dòng `"💙 Bạn có muốn hỏi gì về VHU?`"`n" -ForegroundColor White

Write-Host "✅ Câu VHU:" -ForegroundColor Green
Write-Host "   → Response từ existing action" -ForegroundColor White
Write-Host "   → Format đẹp với emoji và markdown`n" -ForegroundColor White

Write-Host "❌ Câu ngoài phạm vi:" -ForegroundColor Red
Write-Host "   → `"Xin lỗi, mình chưa có thông tin này`"" -ForegroundColor White
Write-Host "   → Nghĩa là Gemini CHƯA hoạt động`n" -ForegroundColor White

Write-Host "============================================================================`n" -ForegroundColor Cyan
Read-Host "Press Enter to start Rasa Shell"

rasa shell --model models/vhu-chatbot-gemini-v1.tar.gz

# ============================================================================
# CLEANUP
# ============================================================================

Write-Host "`n============================================================================" -ForegroundColor Cyan
Write-Host "TEST COMPLETED" -ForegroundColor Green
Write-Host "============================================================================`n" -ForegroundColor Cyan
Write-Host "Để tắt action server:" -ForegroundColor Yellow
Write-Host "  - Đóng cửa sổ PowerShell action server" -ForegroundColor White
Write-Host "  - Hoặc tìm process và kill`n" -ForegroundColor White
Write-Host "Để test lại, chạy: .\test_gemini_full.ps1`n" -ForegroundColor White
Read-Host "Press Enter to exit"
