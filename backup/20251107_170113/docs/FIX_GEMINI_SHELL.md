# 🔧 FIX GEMINI KHÔNG HOẠT ĐỘNG TRONG SHELL

## 🎯 VẤN ĐỀ PHÁT HIỆN

**Triệu chứng:**
- ✅ Test file `test_gemini_integration.py` PASS
- ✅ Gemini API hoạt động
- ❌ Trong `rasa shell` bot vẫn báo "chưa có thông tin"

**Nguyên nhân:**
🔴 **ACTION SERVER CHƯA CHẠY!**

---

## 💡 GIẢI THÍCH

### **Rasa Architecture:**
```
User Input → Rasa NLU → Intent Classification
                          ↓
                    Rules/Policies
                          ↓
                    Action Selection
                          ↓
            ┌─────────────┴─────────────┐
            ↓                           ↓
    Utter Response              Custom Action
    (rasa core)                 (action server)
                                        ↓
                                action_gemini_fallback
                                        ↓
                                    Gemini API
```

### **Tại sao cần Action Server?**

**Custom actions** (như `action_gemini_fallback`) phải chạy trong **action server riêng biệt**:

1. **Rasa Core** (rasa shell):
   - Xử lý NLU, dialoguemanagement
   - Chỉ có thể gọi `utter_*` responses
   - Port: 5005

2. **Action Server**:
   - Chạy custom Python code
   - Gọi external APIs (Gemini, database, etc.)
   - Port: 5055

3. **Communication:**
   ```
   Rasa Core ←→ HTTP ←→ Action Server ←→ Gemini API
   ```

**Nếu không có action server:**
- Rasa không thể execute `action_gemini_fallback`
- Fallback về default response: "chưa có thông tin"

---

## ✅ GIẢI PHÁP

### **Option 1: Quick Start (Recommended)** 🟢

#### Bước 1: Mở **2 terminals**

**Terminal 1: Action Server**
```bash
cd D:\workspace\Chatbot
rasa_env_new\Scripts\activate
rasa run actions
```
**Chờ đến khi thấy:**
```
INFO     - Starting action endpoint server...
INFO     - Action endpoint is up and running on http://localhost:5055
```

**Terminal 2: Rasa Shell**
```bash
cd D:\workspace\Chatbot
rasa_env_new\Scripts\activate
rasa shell --model models/vhu-chatbot-gemini-v1.tar.gz
```

#### Bước 2: Test
```
Your input: thời tiết hôm nay thế nào?
```

**Kết quả mong đợi:**
```
Tôi không có dữ liệu thời tiết real-time...
💙 Bạn có muốn hỏi gì về Đại học Văn Hiến không?
```

---

### **Option 2: Automated Script** 🔵

#### Sử dụng `quick_start_gemini.bat`:

```bash
cd D:\workspace\Chatbot
quick_start_gemini.bat
```

**Script sẽ tự động:**
1. ✅ Check model exists
2. ✅ Start action server (cửa sổ riêng)
3. ✅ Wait 10 seconds
4. ✅ Start rasa shell

---

### **Option 3: Full System** 🔴 (Advanced)

#### Sử dụng `start_gemini_full.bat`:

```bash
cd D:\workspace\Chatbot
start_gemini_full.bat
```

**Script sẽ start:**
1. ✅ Action Server (port 5055)
2. ✅ Rasa Server (port 5005)
3. ✅ Rasa Shell
4. ✅ Run debug tests

---

## 🔍 DEBUG CHECKLIST

### **1. Kiểm tra Action Server đang chạy:**

**Trong terminal action server, tìm dòng:**
```
INFO     - Registered function for 'action_gemini_fallback'.
```

**Nếu không thấy:**
- ❌ Class `ActionGeminiFallback` chưa được load
- 🔧 Fix: Check `actions/actions.py` có class đó không

---

### **2. Kiểm tra Gemini API Key:**

```bash
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('API Key:', os.getenv('GEMINI_API_KEY')[:20] + '...')"
```

**Kết quả mong đợi:**
```
API Key: AIzaSyA0al8DNKVdNoJ...
```

**Nếu `None`:**
- ❌ File `.env` không tồn tại hoặc sai format
- 🔧 Fix: Tạo `.env` với `GEMINI_API_KEY=your_key`

---

### **3. Kiểm tra Intent Classification:**

**Run debug script:**
```bash
python debug_gemini_fallback.py
```

**Kiểm tra output:**
```
🔍 KIỂM TRA ACTION SERVER
✅ Action server is running

🔍 KIỂM TRA ACTION_GEMINI_FALLBACK
✅ action_gemini_fallback is registered
✅ Gemini responded successfully!
```

**Nếu fail:**
- Xem phần troubleshooting bên dưới

---

### **4. Test Intent trong Shell:**

Sau khi start cả 2 servers, test:

```bash
# VHU question - should use existing action
You: học phí là bao nhiêu?
Expected: "💰 HỌC PHÍ ĐẠI HỌC VĂN HIẾN..." (existing action)

# Out-of-scope - should use Gemini
You: thời tiết hôm nay?
Expected: Gemini response + "💙 Bạn có muốn hỏi..."

# Another out-of-scope
You: cho mua gì ngon?
Expected: Gemini response + "💙 Bạn có muốn hỏi..."
```

---

## 🚨 TROUBLESHOOTING

### **Problem 1: "chưa có thông tin" vẫn xuất hiện** ❌

**Nguyên nhân:**
- Intent không được classify vào `out_of_scope` hoặc `nlu_fallback`
- Model confidence quá cao

**Fix:**
```yaml
# config.yml - Giảm threshold
- name: FallbackClassifier
  threshold: 0.4  # Giảm từ 0.5 → 0.4
  ambiguity_threshold: 0.15  # Tăng từ 0.1 → 0.15
```

**Sau đó train lại:**
```bash
rasa train --fixed-model-name vhu-chatbot-gemini-v2
```

---

### **Problem 2: Action server crash** ❌

**Lỗi:**
```
ImportError: No module named 'google.generativeai'
```

**Fix:**
```bash
pip install google-generativeai python-dotenv
```

---

### **Problem 3: Gemini API error** ❌

**Lỗi trong action server:**
```
ERROR - Gemini API error: 401 Unauthorized
```

**Fix:**
1. Check API key trong `.env`
2. Verify key còn hoạt động: https://makersuite.google.com/app/apikey
3. Thử key mới

---

### **Problem 4: Action không được gọi** ❌

**Check logs action server:**
```
INFO - Action 'action_gemini_fallback' was called
```

**Nếu không thấy log này:**
- ❌ Rule không match
- ❌ Intent classification sai

**Fix:**
```bash
# Test intent classification
rasa shell nlu --model models/vhu-chatbot-gemini-v1.tar.gz

# Nhập: "thời tiết hôm nay?"
# Check intent là gì
```

---

## 📝 WORKFLOW ĐÚNGgit

### **Development:**
```bash
# Terminal 1: Action Server (luôn chạy khi dev)
rasa run actions --debug

# Terminal 2: Train và test
rasa train --fixed-model-name vhu-chatbot-gemini-v1
rasa shell --model models/vhu-chatbot-gemini-v1.tar.gz
```

### **Production:**
```bash
# Terminal 1: Action Server
rasa run actions

# Terminal 2: Rasa Server
rasa run --model models/vhu-chatbot-gemini-v1.tar.gz --enable-api

# Terminal 3: (Optional) Monitor logs
tail -f rasa.log
```

---

## ✅ VERIFICATION SCRIPT

Tạo file `verify_gemini.py`:

```python
import requests

def verify():
    # 1. Check action server
    try:
        r = requests.get("http://localhost:5055/health")
        print("✅ Action server: UP")
    except:
        print("❌ Action server: DOWN")
        return False
    
    # 2. Check Gemini action
    try:
        r = requests.post(
            "http://localhost:5055/webhook",
            json={
                "next_action": "action_gemini_fallback",
                "tracker": {
                    "sender_id": "test",
                    "latest_message": {
                        "text": "test",
                        "intent": {"name": "out_of_scope"}
                    },
                    "events": []
                }
            }
        )
        if r.status_code == 200:
            print("✅ Gemini action: OK")
        else:
            print(f"❌ Gemini action: ERROR {r.status_code}")
            return False
    except Exception as e:
        print(f"❌ Gemini action: ERROR {e}")
        return False
    
    print("\n✅ ALL CHECKS PASSED!")
    print("You can now use 'rasa shell'")
    return True

if __name__ == "__main__":
    verify()
```

**Run:**
```bash
python verify_gemini.py
```

---

## 🎯 TÓM TẮT

### **VẤN ĐỀ:**
- Gemini API hoạt động nhưng không trigger trong shell

### **NGUYÊN NHÂN:**
- Action server chưa chạy

### **GIẢI PHÁP:**
1. ✅ **LUÔN start action server trước khi dùng rasa shell**
2. ✅ Use `quick_start_gemini.bat` để tự động
3. ✅ Verify bằng `debug_gemini_fallback.py`

### **TEST:**
```bash
# Terminal 1
rasa run actions

# Terminal 2
rasa shell --model models/vhu-chatbot-gemini-v1.tar.gz

# Test input
You: thời tiết hôm nay thế nào?
```

**Kết quả mong đợi:**
```
Bot: [Gemini response về thời tiết]
     💙 Bạn có muốn hỏi gì về Đại học Văn Hiến không?
```

---

**Status:** ✅ **FIXED - CHỈ CẦN START ACTION SERVER**  
**Next:** Test với `quick_start_gemini.bat` 🚀
