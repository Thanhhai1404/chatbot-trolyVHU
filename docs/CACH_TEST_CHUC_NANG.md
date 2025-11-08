# 📖 HƯỚNG DẪN TEST CHỨC NĂNG GEMINI AI

**Mục đích:** Kiểm tra Gemini AI Integration hoạt động đúng trong VHU Chatbot

---

## 🎯 CÁC LOẠI TEST

### **1. Unit Test** ✅

- Test Gemini API trực tiếp
- KHÔNG cần action server
- KHÔNG cần rasa server
- **Thời gian:** 1 phút

### **2. Action Server Test** ⚙️

- Test action_gemini_fallback
- CẦN action server
- KHÔNG cần rasa server
- **Thời gian:** 2 phút

### **3. Integration Test** 🔗

- Test trong rasa shell
- CẦN action server
- CẦN rasa shell
- **Thời gian:** 5 phút

---

## 📋 PRE-REQUISITES

### **Checklist trước khi test:**

```bash
✅ Model: models/vhu-chatbot-gemini-v1.tar.gz
✅ File .env có GEMINI_API_KEY
✅ Packages: google-generativeai, python-dotenv
✅ Internet connection
✅ Port 5055 available (cho action server)
```

### **Kiểm tra nhanh:**

```bash
# Check model
dir models\vhu-chatbot-gemini-v1.tar.gz

# Check .env
type .env

# Check packages
python -c "import google.generativeai; print('OK')"

# Check API key
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print(os.getenv('GEMINI_API_KEY')[:20])"
```

---

## 🧪 METHOD 1: AUTOMATED TEST (Khuyến nghị)

### **Option A: Full Test**

```bash
cd D:\workspace\Chatbot
test_gemini_full.bat
```

**Script sẽ:**

1. ✅ Check prerequisites
2. ✅ Run unit test
3. ✅ Start action server
4. ✅ Test action server
5. ✅ Open rasa shell
6. ✅ Hướng dẫn test cases

**Ưu điểm:** Đầy đủ, có hướng dẫn từng bước

---

### **Option B: Quick Test**

```bash
cd D:\workspace\Chatbot
test_quick.bat
```

**Script sẽ:**

1. ✅ Unit test
2. ✅ Action server test
3. ✅ Rasa shell

**Ưu điểm:** Nhanh, ít pause

---

## 🔬 METHOD 2: MANUAL TEST (Hiểu rõ hơn)

### **STEP 1: Unit Test**

#### **Test Gemini API trực tiếp:**

```bash
cd D:\workspace\Chatbot
rasa_env_new\Scripts\activate
python test_gemini_integration.py
```

#### **Kết quả mong đợi:**

```
🧪 TEST GEMINI INTEGRATION
==================================================
[1] 🔍 Test: Câu hỏi ngoài phạm vi - Gemini xử lý
❓ Question: Thời tiết hôm nay thế nào?
📊 VHU-related: False
✅ Classification: CORRECT
🤖 Calling Gemini...
✅ Response received: Tôi không có thông tin...
✅ TEST 1 PASSED!

[2] 🔍 Test: Câu hỏi VHU - Fallback message
...
✅ TEST 2 PASSED!

==================================================
✅ 4/4 TESTS PASSED!
```

#### **Nếu FAIL:**

| Error                                   | Nguyên nhân       | Fix                                         |
| --------------------------------------- | ----------------- | ------------------------------------------- |
| `No module named 'google.generativeai'` | Package chưa cài  | `pip install google-generativeai`           |
| `API key not found`                     | Không có .env     | Tạo file .env với API key                   |
| `401 Unauthorized`                      | API key sai       | Check key tại https://makersuite.google.com |
| `Connection timeout`                    | Không có internet | Check mạng                                  |

---

### **STEP 2: Action Server Test**

#### **2.1. Start Action Server:**

**Terminal 1:**

```bash
cd D:\workspace\Chatbot
rasa_env_new\Scripts\activate
rasa run actions
```

#### **Chờ thấy logs:**

```
INFO     rasa_sdk.endpoint  - Starting action endpoint server...
INFO     rasa_sdk.executor  - Registered function for 'action_gemini_fallback'.
INFO     rasa_sdk.endpoint  - Action endpoint is up and running on http://localhost:5055
```

✅ **Nếu thấy "Registered function for 'action_gemini_fallback'" = SUCCESS!**

#### **Nếu có ERROR:**

```python
# ImportError
pip install google-generativeai python-dotenv

# Port already in use
# Tìm và kill process đang dùng port 5055
netstat -ano | findstr :5055
taskkill /PID <PID> /F
```

---

#### **2.2. Test Action Server:**

**Terminal 2:**

```bash
cd D:\workspace\Chatbot
python debug_gemini_fallback.py
```

#### **Kết quả mong đợi:**

```
🎯 GEMINI FALLBACK DEBUGGER
============================================================
🔍 KIỂM TRA ACTION SERVER
============================================================

✅ Action server is running

============================================================
🔍 KIỂM TRA ACTION_GEMINI_FALLBACK
============================================================

✅ action_gemini_fallback is registered
✅ Gemini responded successfully!
   Response preview: Tôi không có thông tin thời tiết...

============================================================
✅ ALL CHECKS PASSED!
```

#### **Nếu FAIL:**

| Triệu chứng                 | Nguyên nhân | Fix                      |
| --------------------------- | ----------- | ------------------------ |
| "Action server NOT running" | Chưa start  | Start terminal 1         |
| "Cannot connect"            | Port sai    | Check port 5055          |
| "Action not registered"     | Code lỗi    | Check actions/actions.py |
| "No Gemini response"        | API key sai | Check .env               |

---

### **STEP 3: Integration Test (Rasa Shell)**

#### **3.1. Giữ Action Server chạy (Terminal 1)**

Không được tắt terminal 1!

---

#### **3.2. Start Rasa Shell:**

**Terminal 2:**

```bash
cd D:\workspace\Chatbot
rasa_env_new\Scripts\activate
rasa shell --model models/vhu-chatbot-gemini-v1.tar.gz
```

#### **Chờ thấy:**

```
INFO     root  - Starting Rasa server on http://localhost:5005
Your input ->
```

---

#### **3.3. Test Cases:**

### **Test Case 1: Câu hỏi NGOÀI PHẠM VI** 🌟

#### **Input:**

```
Your input: thời tiết hôm nay thế nào?
```

#### **Kết quả ĐÚNG:** ✅

```
Bot: Tôi không có dữ liệu thời tiết real-time. Để biết thời tiết
     hôm nay, bạn có thể:

     1. Kiểm tra trên Weather.com
     2. Sử dụng ứng dụng AccuWeather
     3. Tìm trên Google: "thời tiết hôm nay"

     💙 Bạn có muốn hỏi gì về Đại học Văn Hiến không?
```

**Dấu hiệu SUCCESS:**

- ✅ Response dài, có thông tin chi tiết
- ✅ Có dòng "💙 Bạn có muốn hỏi gì về VHU?"
- ✅ Nội dung hợp lý với câu hỏi

#### **Kết quả SAI:** ❌

```
Bot: Xin lỗi, mình chưa có thông tin này. 😔
     Bạn có thể hỏi mình về:
     • 📚 Học phí các ngành
     ...
```

**Dấu hiệu FAIL:**

- ❌ Response là fallback message cũ
- ❌ Không có Gemini response
- ❌ Không có dòng "💙 Bạn có muốn hỏi..."

**→ Check action server logs có lỗi không**

---

### **Test Case 2: Câu hỏi NGOÀI PHẠM VI khác**

#### **Input:**

```
Your input: cho mua gì ngon?
```

#### **Kết quả ĐÚNG:** ✅

```
Bot: Tôi là trợ lý ảo của Đại học Văn Hiến, tôi không có
     thông tin về ẩm thực. Tuy nhiên, bạn có thể:

     1. Tìm trên Google Maps
     2. Xem các app giao đồ ăn: Grab, Shopee Food
     3. Hỏi bạn bè địa phương

     💙 Bạn có muốn hỏi gì về Đại học Văn Hiến không?
```

---

### **Test Case 3: Câu VHU** 🎓

#### **Input:**

```
Your input: học phí là bao nhiêu?
```

#### **Kết quả ĐÚNG:** ✅

```
Bot: 💰 HỌC PHÍ ĐẠI HỌC VĂN HIẾN

     Học phí phụ thuộc vào ngành học:

     📚 Nhóm KHXH & Nhân văn: 15.000.000đ/năm
     💻 Nhóm Kỹ thuật: 18.000.000đ/năm
     ...
```

**Dấu hiệu:**

- ✅ Response từ action_tuition_specific
- ✅ Format đẹp với emoji
- ✅ KHÔNG phải Gemini response

---

### **Test Case 4: Câu VHU khác**

#### **Input:**

```
Your input: trường có những ngành nào?
```

#### **Kết quả ĐÚNG:** ✅

```
Bot: Đại học Văn Hiến có 44 ngành đào tạo bậc đại học...
     [Danh sách ngành]
```

---

### **Test Case 5: Câu ngoài phạm vi - Technical**

#### **Input:**

```
Your input: python là gì?
```

#### **Kết quả ĐÚNG:** ✅

```
Bot: Python là một ngôn ngữ lập trình bậc cao, phổ biến...
     [Giải thích chi tiết về Python]

     💙 Bạn có muốn hỏi gì về Đại học Văn Hiến không?
```

---

## 📊 TEST RESULT MATRIX

| Test Case          | Input                 | Expected Result          | Indicator         |
| ------------------ | --------------------- | ------------------------ | ----------------- |
| **Out-of-scope 1** | "thời tiết hôm nay?"  | Gemini response + 💙     | Gemini working ✅ |
| **Out-of-scope 2** | "cho mua gì ngon?"    | Gemini response + 💙     | Gemini working ✅ |
| **Out-of-scope 3** | "python là gì?"       | Gemini response + 💙     | Gemini working ✅ |
| **VHU domain 1**   | "học phí bao nhiêu?"  | Existing action response | No Gemini (OK) ✅ |
| **VHU domain 2**   | "trường có ngành gì?" | Existing action response | No Gemini (OK) ✅ |
| **VHU domain 3**   | "VHU ở đâu?"          | Existing action response | No Gemini (OK) ✅ |

---

## 🚨 TROUBLESHOOTING

### **Problem 1: "chưa có thông tin" xuất hiện**

#### **Triệu chứng:**

```
Your input: thời tiết hôm nay?
Bot: Xin lỗi, mình chưa có thông tin này. 😔
```

#### **Nguyên nhân & Fix:**

1. **Action server không chạy:**

   ```bash
   # Check
   curl http://localhost:5055/health

   # Fix
   rasa run actions
   ```

2. **Intent classification sai:**

   ```bash
   # Check intent
   rasa shell nlu
   # Nhập: "thời tiết hôm nay?"
   # Xem intent là gì

   # Fix: Lower threshold
   # config.yml:
   - name: FallbackClassifier
     threshold: 0.4  # Giảm từ 0.5
   ```

3. **Rule không match:**
   ```bash
   # Check rules.yml có:
   - rule: Gemini AI fallback for out-of-scope questions
     steps:
       - intent: out_of_scope
       - action: action_gemini_fallback
   ```

---

### **Problem 2: Action server crash**

#### **Error log:**

```
ModuleNotFoundError: No module named 'google.generativeai'
```

#### **Fix:**

```bash
pip install google-generativeai python-dotenv
# Restart action server
```

---

### **Problem 3: Gemini API error**

#### **Error log:**

```
ERROR - Gemini API error: 401 Unauthorized
```

#### **Fix:**

1. Check API key trong .env
2. Test key: https://makersuite.google.com/app/apikey
3. Regenerate key nếu cần
4. Restart action server

---

### **Problem 4: Slow response**

#### **Triệu chứng:**

- Bot mất 5-10 giây mới trả lời

#### **Nguyên nhân:**

- Gemini API call mất thời gian

#### **OK hoặc NOT:**

- ✅ **OK** nếu 3-5 giây (bình thường)
- ⚠️ **Slow** nếu >10 giây (check internet)

---

## 📈 SUCCESS METRICS

### **Test PASS khi:**

```
✅ Unit test: 4/4 tests passed
✅ Action server: Registered action_gemini_fallback
✅ Direct test: Gemini responded successfully
✅ Shell test: Out-of-scope → Gemini response
✅ Shell test: VHU questions → Existing actions
✅ Shell test: No errors in logs
```

### **Test FAIL khi:**

```
❌ Unit test: <4/4 tests passed
❌ Action server: Action not registered
❌ Direct test: No Gemini response
❌ Shell test: Out-of-scope → Fallback message
❌ Shell test: Errors in action server logs
```

---

## 🎯 QUICK REFERENCE

### **Scripts:**

```bash
# Full automated test
test_gemini_full.bat

# Quick test
test_quick.bat

# Start action server + shell
quick_start_gemini.bat

# Debug only
python debug_gemini_fallback.py
```

### **Manual commands:**

```bash
# Terminal 1: Action Server
rasa run actions

# Terminal 2: Rasa Shell
rasa shell --model models/vhu-chatbot-gemini-v1.tar.gz

# Test Gemini API
python test_gemini_integration.py

# Check action server
curl http://localhost:5055/health
```

---

## 📝 TEST CHECKLIST

### **Before Testing:**

- [ ] Model trained: vhu-chatbot-gemini-v1.tar.gz
- [ ] .env file exists with valid API key
- [ ] Packages installed: google-generativeai, python-dotenv
- [ ] Internet connection working
- [ ] Port 5055 available

### **During Testing:**

- [ ] Action server started successfully
- [ ] Log shows "Registered function for 'action_gemini_fallback'"
- [ ] Debug script passes all checks
- [ ] Rasa shell connects to action server

### **Test Cases:**

- [ ] Out-of-scope question 1: Weather → Gemini response ✅
- [ ] Out-of-scope question 2: Food → Gemini response ✅
- [ ] Out-of-scope question 3: Tech → Gemini response ✅
- [ ] VHU question 1: Tuition → Existing action ✅
- [ ] VHU question 2: Programs → Existing action ✅
- [ ] VHU question 3: Location → Existing action ✅

### **After Testing:**

- [ ] No errors in action server logs
- [ ] No errors in rasa shell
- [ ] Responses are relevant and helpful
- [ ] Response time acceptable (<5 seconds)

---

## 🎉 CONCLUSION

**Nếu tất cả tests PASS:**

- ✅ Gemini AI Integration hoạt động hoàn hảo
- ✅ Ready for production
- ✅ Có thể deploy

**Nếu có tests FAIL:**

- ⚠️ Xem Troubleshooting section
- ⚠️ Check logs chi tiết
- ⚠️ Run debug script

---

**Happy Testing!** 🚀
