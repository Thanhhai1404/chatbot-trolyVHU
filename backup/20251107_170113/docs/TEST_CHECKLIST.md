# ✅ TEST CHECKLIST - GEMINI AI

## 🎯 CÁCH TEST NHANH NHẤT

### **OPTION 1: Automated (Khuyến nghị)** ⭐
```bash
test_gemini_full.bat
```
→ Tự động test tất cả, có hướng dẫn chi tiết

---

### **OPTION 2: Quick Test**
```bash
test_quick.bat
```
→ Nhanh hơn, ít pause

---

### **OPTION 3: Manual (2 Terminals)**

**Terminal 1:**
```bash
rasa run actions
```
Chờ thấy: `Registered function for 'action_gemini_fallback'`

**Terminal 2:**
```bash
rasa shell --model models/vhu-chatbot-gemini-v1.tar.gz
```

---

## 🧪 TEST CASES

### **1. Ngoài phạm vi (Gemini):**
```
thời tiết hôm nay thế nào?
cho mua gì ngon?
python là gì?
```

**Kết quả ĐÚNG:**
- ✅ Response dài, có nội dung
- ✅ Có dòng "💙 Bạn có muốn hỏi gì về VHU?"

**Kết quả SAI:**
- ❌ "Xin lỗi, mình chưa có thông tin này"
- ❌ Không có Gemini response

---

### **2. VHU domain (Existing actions):**
```
học phí là bao nhiêu?
trường có những ngành nào?
VHU ở đâu?
```

**Kết quả ĐÚNG:**
- ✅ Response từ existing action
- ✅ Format đẹp với emoji
- ✅ KHÔNG phải Gemini response

---

## 🔍 QUICK DEBUG

```bash
# Check action server
python debug_gemini_fallback.py
```

**Kết quả mong đợi:**
```
✅ Action server is running
✅ action_gemini_fallback is registered
✅ Gemini responded successfully!
```

---

## ⚠️ TROUBLESHOOTING

### **Problem: "chưa có thông tin"**

**Check:**
1. Action server có chạy không?
   ```bash
   # Xem có process này không:
   rasa run actions
   ```

2. Port 5055 có available không?
   ```bash
   netstat -ano | findstr :5055
   ```

3. API key có đúng không?
   ```bash
   type .env
   # Phải có: GEMINI_API_KEY=...
   ```

**Fix:**
```bash
# Restart action server
# Terminal 1:
rasa run actions

# Terminal 2:
rasa shell --model models/vhu-chatbot-gemini-v1.tar.gz
```

---

## ✅ SUCCESS CRITERIA

- [ ] Action server started (có log "Registered function")
- [ ] Debug script passed (3/3 checks)
- [ ] Out-of-scope questions → Gemini response
- [ ] VHU questions → Existing action response
- [ ] No errors in logs
- [ ] Response time < 5 seconds

---

## 📞 QUICK COMMANDS

```bash
# Test all
test_gemini_full.bat

# Quick test
test_quick.bat

# Start action + shell
quick_start_gemini.bat

# Debug only
python debug_gemini_fallback.py

# Unit test only
python test_gemini_integration.py
```

---

**🎯 RUN NGAY:** `test_gemini_full.bat` hoặc `test_quick.bat`
