@echo off
REM Test Gemini in Rasa Shell - Automated

echo ====================================================
echo TEST GEMINI AI TRONG RASA SHELL
echo ====================================================
echo.
echo Dang kiem tra action server...

REM Check if action server is running
curl -s http://localhost:5055/health > nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Action server chua chay!
    echo Vui long chay lenh sau trong terminal khac:
    echo    rasa run actions
    echo.
    pause
    exit /b 1
)

echo [OK] Action server dang chay
echo.
echo ====================================================
echo BAT DAU TEST
echo ====================================================
echo.

REM Test với input tự động
(
echo thoi tiet hom nay the nao
echo cong thuc nau pho ngon  
echo ban bao nhieu tuoi
echo hoc phi cong nghe thong tin
echo /stop
) | rasa_env_new\Scripts\rasa.exe shell

echo.
echo ====================================================
echo TEST HOAN THANH
echo ====================================================
pause
