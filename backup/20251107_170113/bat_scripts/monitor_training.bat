@echo off
echo ====================================
echo THEO DOI TRAINING PROGRESS
echo ====================================
echo.
echo Training dang chay... Vui long doi!
echo.
echo Thoi gian du kien: 10-15 phut
echo.
echo [TIP] Ban co the:
echo   - Kiem tra CPU/RAM usage trong Task Manager
echo   - Doc tai lieu LITE_VS_FULL_POWER.md trong luc doi
echo   - Uong cafe ☕
echo.
echo Nhan Ctrl+C de huy (KHONG KHUYEN KHICH!)
echo.

timeout /t 60 /nobreak >nul

:check_loop
echo [%time%] Dang training...
dir models /o-d 2>nul | find ".tar.gz" >nul
if %errorlevel% equ 0 (
    echo.
    echo ====================================
    echo TRAINING HOAN TAT!
    echo ====================================
    echo.
    dir models /o-d | find ".tar.gz"
    echo.
    echo Kiem tra model moi trong thu muc models/
    echo.
    pause
    exit /b 0
)

timeout /t 30 /nobreak >nul
goto check_loop
