# 🤖 HƯỚNG DẪN SETUP GEMINI AI - GIAI ĐOẠN 3

## ✅ **ĐÃ HOÀN THÀNH**

### 1. **Files đã được tạo/cập nhật:**
- ✅ `actions/gemini_config.py` - Cấu hình Gemini API
- ✅ `actions/actions.py` - Thêm ActionGeminiFallback  
- ✅ `domain.yml` - Thêm action_gemini_fallback
- ✅ `data/rules.yml` - Thêm rule cho Gemini fallback
- ✅ `.env.example` - Template environment variables
- ✅ `requirements.txt` - Thêm google-generativeai
- ✅ `test_gemini_ai.py` - Script test tính năng

### 2. **Packages đã cài đặt:**
- ✅ `google-generativeai` - SDK Gemini API
- ✅ `python-dotenv` - Đọc environment variables

---

## 🚀 **CÁCH SỬ DỤNG**

### **Bước 1: Lấy Gemini API Key**
1. Truy cập: https://makersuite.google.com/app/apikey
2. Đăng nhập Google account
3. Tạo API key mới
4. Copy API key

### **Bước 2: Cấu hình Environment**
```bash
# Tạo file .env từ template
cp .env.example .env

# Chỉnh sửa .env và thêm API key thật:
GEMINI_API_KEY=your_actual_api_key_here
```

### **Bước 3: Train lại model**
```bash
rasa train
```

### **Bước 4: Test Gemini AI**
```bash
# Terminal 1 - Action Server
rasa run actions

# Terminal 2 - Test
python test_gemini_ai.py
```

---

## 🎯 **CÁCH HOẠT ĐỘNG**

### **Trước khi có Gemini:**
```
User: "Thời tiết hôm nay thế nào?"
Bot: "Xin lỗi, mình chưa hiểu rõ câu hỏi..." (fallback cứng)
```

### **Sau khi có Gemini:**
```
User: "Thời tiết hôm nay thế nào?"
Bot: "Mình không thể dự báo thời tiết chính xác, nhưng bạn có thể check trên các app thời tiết như VnExpress, AccuWeather... 🌤️

💙 Bạn có muốn hỏi gì về VHU không nè? Mình sẵn sàng tư vấn! 😊"
```

---

## ⚙️ **CƠ CHẾ HOẠT ĐỘNG**

### **1. Workflow:**
```
User Input → Intent Classification → Confidence Check
                                          ↓
If confidence < 0.3 OR nlu_fallback → Check VHU-related?
                                          ↓
If NOT VHU-related → Call Gemini API → Response + VHU suggestion
If VHU-related → Normal fallback → Gợi ý câu hỏi VHU
```

### **2. Điều kiện kích hoạt Gemini:**
- ✅ Intent confidence < 0.3 HOẶC intent = nlu_fallback
- ✅ Câu hỏi KHÔNG liên quan VHU (không chứa keywords VHU)
- ✅ Có GEMINI_API_KEY hợp lệ

### **3. Fallback an toàn:**
- ❌ Nếu Gemini API lỗi → Fallback về cách cũ
- ❌ Nếu không có API key → Fallback về cách cũ
- ❌ Nếu là câu hỏi VHU → Xử lý bình thường

---

## 🔍 **TEST SCENARIOS**

### **A. Câu hỏi ngoài phạm vi (Gemini xử lý):**
- "Thời tiết hôm nay thế nao?"
- "Cách nấu phở ngon"
- "Bitcoin giá bao nhiêu?"
- "Học tiếng Anh hiệu quả"

### **B. Câu hỏi VHU (Bot cũ xử lý):**
- "học phí công nghệ thông tin"
- "tuyển sinh năm 2025"
- "địa chỉ trường"

### **C. Câu mơ hồ (Gemini có thể xử lý):**
- "tôi buồn quá"
- "không biết chọn gì"
- "asdfghjkl"

---

## ⚠️ **LƯU Ý QUAN TRỌNG**

### **1. Bảo mật:**
- 🔒 Không commit file `.env` vào Git
- 🔒 API key phải được bảo mật
- 🔒 Có rate limiting cho API calls

### **2. Chi phí:**
- 💰 Gemini Pro có giới hạn free tier
- 💰 Monitor usage để tránh vượt quota

### **3. Không ảnh hưởng chức năng cũ:**
- ✅ Tất cả 30 intents cũ vẫn hoạt động
- ✅ 7 custom actions cũ không thay đổi
- ✅ 44 ngành học vẫn được xử lý bình thường
- ✅ Forms và conversation flows không đổi

---

## 📊 **EXPECTED RESULTS**

### **Trước Gemini:**
- ❌ Bot không trả lời được câu ngoài phạm vi
- ❌ User experience kém với fallback cứng
- ❌ Chỉ xử lý được câu hỏi VHU

### **Sau Gemini:**
- ✅ Bot trả lời được câu hỏi chung
- ✅ Vẫn ưu tiên trả lời câu hỏi VHU
- ✅ User experience tốt hơn
- ✅ Luôn hướng user về chủ đề VHU

---

## 🎉 **KÍCH HOẠT TÍNH NĂNG**

```bash
# 1. Tạo file .env với API key
echo "GEMINI_API_KEY=your_key_here" > .env

# 2. Train model
rasa train

# 3. Start action server
rasa run actions

# 4. Test
rasa shell
# Hoặc
python test_gemini_ai.py
```

**🚀 Gemini AI đã sẵn sàng tăng cường trí tuệ cho VHU Chatbot!** 🤖💙
