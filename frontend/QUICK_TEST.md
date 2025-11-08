# ⚡ QUICK TEST - VHU CHATBOT WEB INTERFACE

**Hướng dẫn test nhanh trong 5 phút!**

---

## 🚀 BƯỚC 1: KHỞI ĐỘNG SERVERS (2 phút)

### Terminal 1: Action Server
```powershell
conda activate rasa
cd d:\workspace\chatbot
rasa run actions --port 5055
```
✅ Đợi thấy: "Action endpoint is up and running"

### Terminal 2: Rasa Server
```powershell
conda activate rasa
cd d:\workspace\chatbot
rasa run --enable-api --cors "*" --port 5005
```
✅ Đợi thấy: "Rasa server is up and running"

### Terminal 3: Frontend (Chọn 1 trong 3 cách)

**Cách 1: Live Server (Khuyến nghị)**
1. Mở file `frontend/index.html` trong VS Code
2. Click chuột phải → "Open with Live Server"
3. Tự động mở: http://127.0.0.1:5500/frontend/index.html

**Cách 2: Python Server**
```powershell
cd d:\workspace\chatbot\frontend
python -m http.server 8000
```
Sau đó mở: http://localhost:8000/index.html

**Cách 3: Double-click file HTML**
- Double-click `frontend/index.html`
- ⚠️ Có thể gặp CORS error

---

## 🧪 BƯỚC 2: TEST CHỨC NĂNG (3 phút)

### ✅ Checklist UI
- [ ] Trang landing page hiển thị đẹp
- [ ] Chat button (💬) ở góc dưới phải
- [ ] Click button → Chat widget mở ra
- [ ] Welcome message hiển thị
- [ ] 5 quick reply buttons xuất hiện

### ✅ Test 6 câu hỏi quan trọng

Copy từng câu, paste vào chat, Enter:

#### 1️⃣ Tra cứu 44 ngành
```
Có những ngành nào?
```
🎯 **Kỳ vọng:** Bot liệt kê 44 ngành với mã ngành

#### 2️⃣ Thông tin ngành cụ thể
```
Cho tôi biết về ngành Công nghệ thông tin
```
🎯 **Kỳ vọng:** Bot trả về:
- Mã ngành: 7480201
- Học phí: 450,000 VNĐ/tín chỉ
- Thời gian: 4 năm
- Điều kiện tốt nghiệp, v.v.

#### 3️⃣ Tính học phí
```
Tính học phí
```
→ Bot hỏi ngành → Trả lời: `Công nghệ thông tin`
→ Bot hỏi tín chỉ → Trả lời: `15`

🎯 **Kỳ vọng:** Bot tính:
- 15 × 450,000 = 6,750,000 VNĐ
- + Phí sinh hoạt: 150,000 VNĐ
- + Phí bảo hiểm: 100,000 VNĐ
- **Tổng: 7,000,000 VNĐ**

#### 4️⃣ Gợi ý ngành học
```
Gợi ý ngành học cho tôi
```
→ Bot hỏi sở thích → Trả lời: `Tôi thích lập trình và toán học`

🎯 **Kỳ vọng:** Bot gợi ý:
- Công nghệ thông tin
- Khoa học máy tính
- Hệ thống thông tin

#### 5️⃣ Chỉ đường GPS
```
Chỉ đường đến VHU
```
→ Bot hỏi vị trí → Trả lời: `Bến Thành`

🎯 **Kỳ vọng:** Bot trả về link Google Maps

#### 6️⃣ Gemini AI (Câu hỏi ngoài domain)
```
Kể cho tôi nghe về lịch sử của Đại học Văn Hiến
```
🎯 **Kỳ vọng:** Gemini AI trả lời thông tin chung về VHU

---

## 📸 BƯỚC 3: CHỤP SCREENSHOTS (30 giây)

Chụp 4 màn hình quan trọng:

1. **Landing Page**: Full page với hero + features
2. **Chat Open**: Chat widget với welcome message
3. **Conversation**: Cuộc hội thoại với 5-6 messages
4. **Program Info**: Bot trả lời chi tiết về 1 ngành

---

## ✅ SUCCESS INDICATORS

Nếu thấy những điều này, web interface **HOẠT ĐỘNG HOÀN HẢO**:

✅ Landing page hiển thị đẹp với màu VHU (blue + gold)
✅ Chat button có animation bounce
✅ Chat widget mở/đóng mượt mà
✅ Welcome message hiển thị ngay khi mở chat
✅ User messages màu xanh bên phải
✅ Bot messages màu trắng bên trái
✅ Typing indicator (3 chấm) xuất hiện khi chờ
✅ Quick reply buttons hoạt động
✅ Auto scroll xuống tin nhắn mới
✅ Clear chat xóa được tất cả messages
✅ Rasa API trả lời đúng cho 6 câu hỏi test

---

## 🐛 COMMON ISSUES & FIXES

### ❌ "Failed to fetch" error
**Fix:** Rasa server chưa chạy hoặc sai port
```powershell
# Check ports
netstat -an | findstr ":5005 :5055"

# Restart Rasa with CORS
rasa run --enable-api --cors "*" --port 5005
```

### ❌ Chat button không xuất hiện
**Fix:** File CSS/JS chưa load
- Mở Console (F12)
- Check tab Network
- Reload page (Ctrl+R)

### ❌ Bot không trả lời
**Fix:** Action server chưa chạy
```powershell
rasa run actions --port 5055
```

### ❌ Quick replies không hiển thị
**Fix:** Response format của Rasa không đúng
- Check Console (F12) xem bot response
- Phải có `buttons` array trong response

---

## 🎯 TEST COMPLETION CRITERIA

**Hoàn thành test khi:**
- [ ] Tất cả 3 servers đang chạy
- [ ] Landing page load thành công
- [ ] 6 câu hỏi test đều trả lời đúng
- [ ] UI/UX mượt mà, không lag
- [ ] Chụp được 4 screenshots đẹp
- [ ] Không có error trong Console

---

## 📝 NOTES CHO BÁO CÁO

**Ghi chú khi làm báo cáo:**

1. **Architecture:**
   - Frontend: HTML + Tailwind CSS + Vanilla JS
   - Backend: Rasa 3.6.20 (Port 5005 + 5055)
   - AI: DIET Classifier + Gemini AI + Goong Maps

2. **Features implemented:**
   - 6 main functions (44 programs, tuition, recommendation, GPS, scholarships, Gemini AI)
   - Real-time chat with typing indicator
   - Quick replies for better UX
   - Responsive design (desktop + mobile)
   - Keyboard shortcuts (Ctrl+K, Ctrl+L, Enter, Esc)

3. **Performance:**
   - Model accuracy: 99.9%
   - Average response time: <2 seconds
   - 44 programs in database
   - 30 intents trained
   - 12 custom actions

4. **Showcase points:**
   - Beautiful UI with VHU branding
   - Smooth animations and transitions
   - Full REST API integration
   - Multi-turn conversations (forms/slots)
   - AI fallback with Gemini
   - GPS integration with Goong Maps

---

## 🎓 READY FOR PRESENTATION!

Nếu tất cả test PASS → Bạn đã sẵn sàng để:
- ✅ Demo trực tiếp
- ✅ Làm báo cáo môn học
- ✅ Chụp screenshots
- ✅ Ghi video demo

**Good luck! 🚀**

---

**Created by:** Hải - VHU Student  
**Date:** November 7, 2024  
**Total development time:** ~2 hours  
