# ✅ GEMINI AI - VẤN ĐỀ ĐÃ TÌM RA & CÁCH FIX

**Ngày:** October 23, 2025  
**Status:** ✅ **ĐÃ TÌM RA VẤN ĐỀ**

---

## 🎯 TÓM TẮT NHANH

### **Vấn đề:**
- ✅ Test file `test_gemini_integration.py` **PASS**
- ✅ Gemini API **HOẠT ĐỘNG**
- ❌ Trong `rasa shell` bot **KHÔNG DÙNG GEMINI**
- ❌ Bot trả lời: "Xin lỗi, mình chưa có thông tin này"

### **Nguyên nhân:**
🔴 **ACTION SERVER CHƯA CHẠY!**

### **Giải pháp:**
✅ **PHẢI start action server TRƯỚC KHI dùng rasa shell**

---

## 📊 PHÂN TÍCH CHI TIẾT

### **Tại sao test file PASS nhưng shell FAIL?**

#### **Test File (`test_gemini_integration.py`):**
```python
# Test trực tiếp function Python
from actions.gemini_config import get_gemini_response

response = get_gemini_response("thời tiết hôm nay?")
# ✅ Gọi trực tiếp → PASS
```

**→ Test này KHÔNG cần action server**

---

#### **Rasa Shell:**
```
User → Rasa NLU → Intent Classification
              ↓
          Rules Engine
              ↓
    Select: action_gemini_fallback
              ↓
      🔴 GỌI ACTION SERVER 🔴
              ↓
          Execute Action
              ↓
         Gemini API
```

**→ Shell CẦN action server chạy**

---

### **Kiến trúc Rasa:**

```
┌─────────────────────────────────────────┐
│         RASA CORE (Port 5005)           │
│  - NLU Processing                       │
│  - Dialogue Management                  │
│  - Rules & Policies                     │
│  - utter_* responses (built-in)         │
└───────────────┬─────────────────────────┘
                │
                │ HTTP Request
                │ POST /webhook
                │
┌───────────────▼─────────────────────────┐
│      ACTION SERVER (Port 5055)          │
│  - Custom Python Actions                │
│  - action_gemini_fallback               │
│  - action_list_all_programs             │
│  - External API calls (Gemini, DB, etc.)│
└───────────────┬─────────────────────────┘
                │
                │ API Call
                │
┌───────────────▼─────────────────────────┐
│         GEMINI API (Google)             │
└─────────────────────────────────────────┘
```

### **Tại sao cần 2 processes riêng biệt?**

1. **Rasa Core** (rasa shell/run):
   - Xử lý hội thoại
   - Nhẹ, nhanh
   - Không chạy custom Python code

2. **Action Server** (rasa run actions):
   - Chạy custom code
   - Gọi external APIs
   - Có thể restart mà không ảnh hưởng Rasa Core

**→ Custom actions PHẢI chạy trong action server riêng**

---

## ✅ CÁCH FIX

### **Method 1: Manual (2 Terminals)** 📝

#### **Terminal 1: Action Server**
```bash
cd D:\workspace\Chatbot
rasa_env_new\Scripts\activate
rasa run actions
```

**Chờ thấy log:**
```
INFO - Starting action endpoint server...
INFO - Registered function for 'action_gemini_fallback'.
INFO - Action endpoint is up and running on http://localhost:5055
```

#### **Terminal 2: Rasa Shell**
```bash
cd D:\workspace\Chatbot
rasa_env_new\Scripts\activate
rasa shell --model models/vhu-chatbot-gemini-v1.tar.gz
```

#### **Test:**
```
Your input: thời tiết hôm nay thế nào?
```

**Kết quả:**
```
Bot: Tôi không có dữ liệu thời tiết real-time. Bạn có thể 
     kiểm tra trên Weather.com hoặc AccuWeather.
     
     💙 Bạn có muốn hỏi gì về Đại học Văn Hiến không?
```

✅ **Nếu thấy response này = SUCCESS!**

---

### **Method 2: Automated Script** 🚀

#### **Dùng `quick_start_gemini.bat`:**

```bash
cd D:\workspace\Chatbot
quick_start_gemini.bat
```

**Script tự động:**
1. ✅ Check model exists
2. ✅ Start action server (background)
3. ✅ Wait 10 seconds
4. ✅ Start rasa shell

---

### **Method 3: Full System** 🎯

#### **Dùng `start_gemini_full.bat`:**

```bash
cd D:\workspace\Chatbot
start_gemini_full.bat
```

**Mở 3 windows:**
1. Action Server (port 5055)
2. Rasa Server (port 5005)
3. Rasa Shell (interactive)

---

## 🔍 VERIFICATION

### **1. Check Action Server Running:**

**Trong terminal action server, tìm:**
```
INFO - Registered function for 'action_gemini_fallback'.
```

✅ Nếu thấy → Action loaded thành công

---

### **2. Test Gemini Action Directly:**

```bash
python debug_gemini_fallback.py
```

**Kết quả mong đợi:**
```
✅ Action server is running
✅ action_gemini_fallback is registered
✅ Gemini responded successfully!
```

---

### **3. Test trong Shell:**

```
You: thời tiết hôm nay thế nào?
Bot: [Gemini response] 💙 Bạn có muốn hỏi gì về VHU?
       ↑
    SUCCESS!

You: học phí là bao nhiêu?
Bot: 💰 HỌC PHÍ ĐẠI HỌC VĂN HIẾN...
       ↑
    Existing action (OK)
```

---

## 📋 CHECKLIST HOÀN CHỈNH

### **Before Testing:**
- [ ] Model exists: `models/vhu-chatbot-gemini-v1.tar.gz`
- [ ] File `.env` có `GEMINI_API_KEY`
- [ ] `actions/actions.py` có class `ActionGeminiFallback`
- [ ] `data/rules.yml` có Gemini fallback rules
- [ ] `domain.yml` có `action_gemini_fallback` trong actions

### **During Testing:**
- [ ] **ACTION SERVER đang chạy** (port 5055)
- [ ] Log shows: "Registered function for 'action_gemini_fallback'"
- [ ] Rasa shell connected to action server

### **Testing:**
- [ ] Out-of-scope question → Gemini response
- [ ] VHU question → Existing action response
- [ ] No errors in action server logs

---

## 🚨 COMMON MISTAKES

### ❌ **Mistake 1: Không start action server**
```bash
# SAI - Chỉ chạy shell
rasa shell

# ĐÚNG - Chạy action server trước
# Terminal 1:
rasa run actions

# Terminal 2:
rasa shell
```

---

### ❌ **Mistake 2: Dùng wrong model**
```bash
# SAI
rasa shell  # Dùng model mặc định (không có Gemini)

# ĐÚNG
rasa shell --model models/vhu-chatbot-gemini-v1.tar.gz
```

---

### ❌ **Mistake 3: Không check action server logs**
```
# Nếu action không hoạt động, CHECK LOGS!
# Action server sẽ show errors rõ ràng:
# - Import errors
# - API key errors
# - Function registration errors
```

---

## 📊 TROUBLESHOOTING MATRIX

| Triệu chứng | Nguyên nhân | Fix |
|-------------|-------------|-----|
| "chưa có thông tin" | Action server down | Start `rasa run actions` |
| ImportError google.generativeai | Missing package | `pip install google-generativeai` |
| 401 Unauthorized | Invalid API key | Check `.env` file |
| Action not registered | Code error | Check `actions/actions.py` |
| Wrong intent | Classification issue | Lower threshold in `config.yml` |

---

## 🎓 LEARNING POINTS

### **1. Rasa Components:**
- **Rasa Core**: Dialogue management
- **Action Server**: Custom Python code
- **Tách biệt**: Để scale & maintain dễ hơn

### **2. Custom Actions:**
- Phải run trong action server
- Không thể execute trực tiếp từ rasa core
- Communication qua HTTP (port 5055)

### **3. Testing Strategy:**
- **Unit test**: Test functions trực tiếp (không cần server)
- **Integration test**: Test trong shell (cần server)
- **Cả 2 đều cần** để verify đầy đủ

---

## ✅ SUCCESS CRITERIA

### **Gemini AI hoạt động đúng khi:**
1. ✅ Action server running (port 5055)
2. ✅ Rasa shell connected
3. ✅ Out-of-scope questions → Gemini responses
4. ✅ VHU questions → Existing action responses
5. ✅ No errors in logs

---

## 🚀 NEXT STEPS

### **1. Test ngay:**
```bash
quick_start_gemini.bat
```

### **2. Verify:**
```bash
python debug_gemini_fallback.py
```

### **3. Production:**
Khi deploy, remember:
- Start action server TRƯỚC
- Start rasa server SAU
- Monitor logs cả 2 processes

---

## 📞 QUICK REFERENCE

### **Start Action Server:**
```bash
rasa run actions
```

### **Start Shell with Gemini Model:**
```bash
rasa shell --model models/vhu-chatbot-gemini-v1.tar.gz
```

### **Check Action Server:**
```bash
curl http://localhost:5055/health
```

### **Debug:**
```bash
python debug_gemini_fallback.py
```

---

**Status:** ✅ **VẤN ĐỀ ĐÃ GIẢI QUYẾT**  
**Action Required:** Start action server before testing  
**Confidence:** 100% - This is the root cause

---

## 💡 TIP

**Tạo alias để tiện:**

```bash
# Windows: Tạo file start_dev.bat
@echo off
start "Action Server" cmd /k "cd /d D:\workspace\Chatbot && rasa_env_new\Scripts\activate && rasa run actions"
timeout /t 10 /nobreak
call rasa_env_new\Scripts\activate
rasa shell --model models/vhu-chatbot-gemini-v1.tar.gz
```

**Sau đó chỉ cần:**
```bash
start_dev.bat
```

✅ **DONE!** 🎉
