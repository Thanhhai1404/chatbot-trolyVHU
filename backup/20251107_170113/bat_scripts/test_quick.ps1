# ============================================================================
# QUICK TEST - GEMINI AI (PowerShell)
# ============================================================================

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "     QUICK TEST - GEMINI AI" -ForegroundColor Yellow
Write-Host "========================================`n" -ForegroundColor Cyan

# Check model
if (-Not (Test-Path "models\vhu-chatbot-gemini-v1.tar.gz")) {
    Write-Host "❌ Model not found! Run: rasa train --fixed-model-name vhu-chatbot-gemini-v1" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "✅ Model: vhu-chatbot-gemini-v1.tar.gz`n" -ForegroundColor Green

# Test 1: Unit test
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "TEST 1: GEMINI API (Unit Test)" -ForegroundColor Yellow
Write-Host "========================================`n" -ForegroundColor Cyan
& rasa_env_new\Scripts\activate.ps1
python test_gemini_integration.py
Write-Host "`n⏸️  Pause để xem kết quả Test 1..." -ForegroundColor Yellow
Read-Host "Press Enter"
Clear-Host

# Test 2: Start action server và test
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "TEST 2: ACTION SERVER" -ForegroundColor Yellow
Write-Host "========================================`n" -ForegroundColor Cyan
Write-Host "Starting action server (new window)..." -ForegroundColor Yellow
$actionCmd = "cd '$PWD'; rasa_env_new\Scripts\activate.ps1; rasa run actions"
Start-Process powershell -ArgumentList "-NoExit", "-Command", $actionCmd -WindowStyle Minimized

Write-Host "Waiting 10 seconds..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

Write-Host "`nTesting action server..." -ForegroundColor Yellow
python debug_gemini_fallback.py
Write-Host "`n⏸️  Pause để xem kết quả Test 2..." -ForegroundColor Yellow
Read-Host "Press Enter"
Clear-Host

# Test 3: Rasa Shell
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "TEST 3: RASA SHELL (Integration)" -ForegroundColor Yellow
Write-Host "========================================`n" -ForegroundColor Cyan
Write-Host "CÂU HỎI TEST:`n" -ForegroundColor Yellow
Write-Host "1. NGOÀI PHẠM VI (Gemini):" -ForegroundColor Cyan
Write-Host "   thời tiết hôm nay thế nào?" -ForegroundColor White
Write-Host "   cho mua gì ngon?`n" -ForegroundColor White
Write-Host "2. VHU DOMAIN (Existing):" -ForegroundColor Cyan
Write-Host "   học phí là bao nhiêu?" -ForegroundColor White
Write-Host "   trường có những ngành nào?`n" -ForegroundColor White
Write-Host "========================================`n" -ForegroundColor Cyan
Read-Host "Press Enter to start"

rasa shell --model models/vhu-chatbot-gemini-v1.tar.gz

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "TEST COMPLETED!" -ForegroundColor Green
Write-Host "========================================`n" -ForegroundColor Cyan
Read-Host "Press Enter to exit"
