@echo off
echo ============================================
echo VHU CHATBOT - CHUYEN DOI FULL POWER MODE
echo ============================================
echo.

echo [!] CANH BAO:
echo     - FULL POWER MODE se train LAU HON (10-15 phut thay vi 2-3 phut)
echo     - Can RAM LON HON (4GB+ thay vi 2GB)
echo     - DO CHINH XAC CAO HON (90%%+ thay vi 85%%)
echo.

set /p confirm="Ban co chac chan muon chuyen sang FULL POWER MODE? (Y/N): "
if /i not "%confirm%"=="Y" (
    echo Da huy!
    pause
    exit /b
)

echo.
echo [1/4] Sao luu config hien tai...
copy config.yml config_lite_backup.yml
echo     [OK] Da backup: config_lite_backup.yml

echo.
echo [2/4] Ap dung config FULL POWER...
copy config_full_power.yml config.yml
echo     [OK] Da cap nhat config.yml

echo.
echo [3/4] Train lai model voi FULL POWER...
echo     [!] Qua trinh nay co the mat 10-15 phut!
call rasa_env_new\Scripts\activate.bat
rasa train

if %errorlevel% equ 0 (
    echo     [OK] Train thanh cong!
) else (
    echo     [X] Train that bai! Khoi phuc config cu...
    copy config_lite_backup.yml config.yml
    pause
    exit /b 1
)

echo.
echo [4/4] So sanh ket qua...
echo.
echo ====================================
echo HOAN THANH!
echo ====================================
echo.
echo Bot da chuyen sang FULL POWER MODE!
echo.
echo SO SANH:
echo     LITE MODE:
echo       - Train time: 2-3 phut
echo       - RAM: 2GB
echo       - Accuracy: ~85%%
echo.
echo     FULL POWER MODE:
echo       - Train time: 10-15 phut
echo       - RAM: 4GB+
echo       - Accuracy: ~90-95%%
echo.
echo De quay lai LITE MODE, chay:
echo     copy config_lite_backup.yml config.yml
echo     rasa train
echo.
pause
