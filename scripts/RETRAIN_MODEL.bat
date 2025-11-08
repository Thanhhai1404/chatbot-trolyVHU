@echo off
REM ============================================================================
REM RETRAIN RASA MODEL WITH 100% TRAINING DATA (44 PROGRAMS)
REM ============================================================================
echo.
echo ============================================================================
echo        RETRAIN VHU CHATBOT - 100%% Coverage for 44 Programs
echo ============================================================================
echo.

REM Check if rasa_env exists
if not exist "rasa_env" (
    echo [ERROR] rasa_env not found!
    echo Please activate your Rasa environment first.
    echo.
    echo Try: conda activate rasa_env
    pause
    exit /b 1
)

echo [INFO] Activating Rasa environment...
call rasa_env\Scripts\activate.bat

echo.
echo ============================================================================
echo Verification: Training Data Completeness
echo ============================================================================
echo.
python scripts\verify_training_data.py

if errorlevel 1 (
    echo.
    echo [WARNING] Verification found some issues.
    echo Do you want to continue anyway? (Press Ctrl+C to cancel)
    pause
)

echo.
echo ============================================================================
echo Starting Rasa Training...
echo ============================================================================
echo.
echo [INFO] This will take 3-5 minutes...
echo [INFO] Training with:
echo        - 44 programs
echo        - 44 synonyms
echo        - 145+ NLU examples
echo.

rasa train

if errorlevel 1 (
    echo.
    echo [ERROR] Training failed!
    echo Please check the error messages above.
    pause
    exit /b 1
)

echo.
echo ============================================================================
echo Training COMPLETED Successfully!
echo ============================================================================
echo.
echo [SUCCESS] New model trained and saved to models/
echo.
echo Next steps:
echo   1. Test with: rasa shell
echo   2. Or run: START_ALL.bat
echo.
echo Test commands:
echo   - hoc phi Piano bao nhieu?
echo   - cho toi biet ve nganh Thanh nhac
echo   - Duoc hoc ra truong lam gi?
echo   - Dieu duong hoc nhung gi?
echo.
pause
