@echo off
echo ========================================
echo HUONG DAN SU DUNG CHUC NANG CHI DUONG
echo ========================================
echo.
echo BUOC 1: DANG KY GOONG MAPS API
echo -------------------------------
echo 1. Truy cap: https://account.map4d.vn/auth/register
echo 2. Dang ky tai khoan (Email + SDT)
echo 3. Dang nhap va tao API Key
echo 4. Copy API Key
echo.
echo BUOC 2: THEM API KEY VAO FILE .env
echo -----------------------------------
echo Mo file .env va them:
echo GOONG_API_KEY=your_api_key_here
echo.
echo BUOC 3: TEST API
echo ----------------
echo python test_goong_maps.py
echo.
echo BUOC 4: TRAIN MODEL
echo -------------------
echo rasa train
echo.
echo BUOC 5: CHAY ACTION SERVER (Terminal 1)
echo ----------------------------------------
echo rasa run actions
echo.
echo BUOC 6: CHAY RASA SHELL (Terminal 2)
echo -------------------------------------
echo rasa shell
echo.
echo TEST CASES:
echo -----------
echo User: "Toi muon den truong"
echo Bot: "Ban dang o dau vay?"
echo User: "Toi o Tan Huong, Tan Phu"
echo Bot: "Ban muon den co so nao?" (7 co so)
echo User: "2" (chon Harmony Campus)
echo Bot: [Chi duong chi tiet + hoi ve xe buyt]
echo.
echo ========================================
echo CHI TIET XEM FILE: DIRECTIONS_FEATURE_GUIDE.md
echo ========================================
pause
