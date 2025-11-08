@echo off
echo ====================================
echo FIX ACTION_RECOMMEND_PROGRAMS
echo ====================================
echo.

cd /d "%~dp0"

echo [1/4] Kich hoat virtual environment...
call rasa_env_new\Scripts\activate.bat

echo.
echo [2/4] Kiem tra syntax errors trong actions.py...
python -m py_compile actions\actions.py
if %errorlevel% neq 0 (
    echo [X] CO LOI SYNTAX! Dang fix...
    goto :fix_indent
) else (
    echo [OK] Khong co loi syntax!
)

echo.
echo [3/4] Test action_recommend_programs...
python test_recommend_action.py
if %errorlevel% neq 0 (
    echo [!] Action co loi runtime
    goto :end
)

echo.
echo [4/4] Khoi dong lai action server...
echo Nhan Ctrl+C de dung action server khi can
rasa run actions --port 5055

goto :end

:fix_indent
echo.
echo Dang fix indentation errors...
python -c "import re; content = open('actions/actions.py', encoding='utf-8').read(); content = re.sub(r'^      message', '    message', content, flags=re.MULTILINE); open('actions/actions.py', 'w', encoding='utf-8').write(content)"
echo [OK] Da fix xong! Chay lai script nay de test.

:end
pause
