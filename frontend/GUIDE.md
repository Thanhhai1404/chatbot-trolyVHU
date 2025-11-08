# 🎓 VHU CHATBOT - WEB INTERFACE GUIDE

## 📋 MỤC LỤC

1. [Chuẩn bị](#chuẩn-bị)
2. [Khởi động Backend](#khởi-động-backend)
3. [Khởi động Frontend](#khởi-động-frontend)
4. [Test chức năng](#test-chức-năng)
5. [Troubleshooting](#troubleshooting)
6. [Screenshots cho báo cáo](#screenshots-cho-báo-cáo)

---

## 🔧 CHUẨN BỊ

### 1. Kiểm tra cấu trúc folder

```
chatbot/
├── frontend/              ✅ Web interface
│   ├── index.html        ✅ Landing page + Chat widget
│   ├── css/
│   │   └── style.css     ✅ Custom animations & styles
│   ├── js/
│   │   ├── config.js     ✅ API configuration
│   │   ├── chat.js       ✅ Rasa integration
│   │   └── ui.js         ✅ UI controls
│   └── assets/
├── actions/              ✅ Backend actions
├── data/                 ✅ Training data
└── models/               ✅ Trained model
```

### 2. Cài đặt VS Code extension (nếu chưa có)

- Mở VS Code
- Vào Extensions (Ctrl+Shift+X)
- Tìm "Live Server" của Ritwick Dey
- Click Install

---

## 🚀 KHỞI ĐỘNG BACKEND

### Bước 1: Activate conda environment

```bash
conda activate rasa
```

### Bước 2: Start Action Server (Terminal 1)

```bash
cd d:\workspace\chatbot
rasa run actions --port 5055
```

✅ **Kiểm tra:** Thấy message "Action endpoint is up and running on http://0.0.0.0:5055"

### Bước 3: Start Rasa Server với CORS (Terminal 2)

```bash
cd d:\workspace\chatbot
rasa run --enable-api --cors "*" --port 5005 --debug
```

✅ **Kiểm tra:** Thấy message "Rasa server is up and running"

### Bước 4: Test API endpoint

Mở browser và truy cập: `http://localhost:5005/`

✅ **Kiểm tra:** Thấy `{"version":"X.X.X","minimum_compatible_version":"X.X.X"}`

---

## 🌐 KHỞI ĐỘNG FRONTEND

### Cách 1: Dùng Live Server (Khuyến nghị)

1. Mở VS Code
2. Mở file `frontend/index.html`
3. Click chuột phải → "Open with Live Server"
4. Browser tự động mở: `http://127.0.0.1:5500/frontend/index.html`

✅ **Kiểm tra:** Thấy trang VHU Chatbot với chat button ở góc dưới phải

### Cách 2: Dùng Python HTTP Server

```bash
cd d:\workspace\chatbot\frontend
python -m http.server 8000
```

Sau đó mở browser: `http://localhost:8000/index.html`

### Cách 3: Mở trực tiếp file HTML

- Double click vào `frontend/index.html`
- Browser sẽ mở file với đường dẫn `file:///...`

⚠️ **Lưu ý:** Cách này có thể gặp CORS error khi call API

---

## 🧪 TEST CHỨC NĂNG

### Test 1: Kiểm tra UI

✅ **Checklist:**
- [ ] Landing page hiển thị đúng (hero section, 6 feature cards, statistics)
- [ ] Chat button floating ở góc dưới phải
- [ ] Click chat button → Chat widget mở ra
- [ ] Chat widget có header, message area, input box
- [ ] Design đẹp với màu VHU (blue #0066CC, gold #FFB800)

### Test 2: Chức năng Chat cơ bản

**2.1. Test Welcome Message**
- Click chat button
- ✅ Thấy welcome message từ bot
- ✅ Thấy 5 quick reply buttons (44 ngành, học phí, gợi ý, chỉ đường, học bổng)

**2.2. Test Send Message**
- Nhập "xin chào" → Enter
- ✅ Message của user hiển thị bên phải (màu xanh)
- ✅ Typing indicator xuất hiện
- ✅ Response của bot hiển thị bên trái (màu trắng)
- ✅ Auto scroll xuống cuối

**2.3. Test Quick Replies**
- Click button "44 ngành đào tạo"
- ✅ Button biến mất sau khi click
- ✅ Message được gửi tự động
- ✅ Bot trả lời danh sách 44 ngành

### Test 3: Các chức năng chính

**3.1. Test tra cứu ngành đào tạo**

```
User: "Có những ngành nào?"
Bot: [Danh sách 44 ngành với mã ngành]

User: "Ngành Công nghệ thông tin"
Bot: [Thông tin chi tiết: mã ngành, học phí, thời gian, v.v.]
```

**3.2. Test tính học phí**

```
User: "Tính học phí"
Bot: "Bạn muốn tính học phí cho ngành nào?"
User: "Công nghệ thông tin"
Bot: "Bạn đăng ký bao nhiêu tín chỉ?"
User: "15"
Bot: [Kết quả: 15 x 450,000 = 6,750,000 VNĐ + phí khác]
```

**3.3. Test gợi ý ngành học**

```
User: "Gợi ý ngành học"
Bot: "Bạn thích môn học nào?"
User: "Toán và Lý"
Bot: [Gợi ý: CNTT, Kỹ thuật, Điện tử viễn thông]
```

**3.4. Test chỉ đường (GPS)**

```
User: "Chỉ đường đến VHU"
Bot: "Bạn đang ở đâu?"
User: "Bến Thành"
Bot: [Link Google Maps với chỉ đường]
```

**3.5. Test học bổng**

```
User: "Có học bổng nào?"
Bot: [Danh sách 7 loại học bổng với điều kiện]
```

**3.6. Test Gemini AI fallback**

```
User: "Kể tôi nghe về lịch sử VHU"
Bot: [Gemini AI trả lời thông tin chung về VHU]
```

### Test 4: Các tính năng UI

**4.1. Test Clear Chat**
- Click nút "Xóa chat" (trash icon)
- ✅ Confirm dialog xuất hiện
- Click OK
- ✅ Tất cả messages bị xóa
- ✅ Welcome message hiện lại

**4.2. Test Close/Open Chat**
- Click X ở header → Chat đóng
- ✅ Chat widget biến mất
- ✅ Chat button xuất hiện lại
- Click chat button → Chat mở lại
- ✅ Messages vẫn còn (không bị mất)

**4.3. Test responsive**
- Resize browser window xuống nhỏ (<768px)
- ✅ Chat widget full screen trên mobile
- ✅ UI vẫn hoạt động tốt

**4.4. Test keyboard shortcuts**
- `Enter` trong input box → Send message ✅
- `Ctrl+K` → Toggle chat ✅
- `Ctrl+L` → Clear chat ✅
- `Escape` → Close chat ✅

---

## 🐛 TROUBLESHOOTING

### Lỗi 1: "Failed to fetch" / CORS Error

**Nguyên nhân:** Rasa server chưa chạy hoặc CORS chưa enable

**Giải pháp:**
```bash
# Stop Rasa server (Ctrl+C)
# Start lại với CORS:
rasa run --enable-api --cors "*" --port 5005
```

### Lỗi 2: Chat button không xuất hiện

**Nguyên nhân:** File CSS hoặc JS chưa load

**Giải pháp:**
- Mở Developer Tools (F12)
- Check tab Console xem có lỗi không
- Check tab Network xem file nào fail

### Lỗi 3: Bot không trả lời

**Nguyên nhân:** Action server chưa chạy

**Giải pháp:**
```bash
# Terminal riêng:
rasa run actions --port 5055
```

### Lỗi 4: Messages không hiển thị đúng

**Nguyên nhân:** Lỗi JavaScript

**Giải pháp:**
- Mở Console (F12)
- Xem error message
- Check file `chat.js` dòng báo lỗi

### Lỗi 5: Live Server không hoạt động

**Giải pháp:**
- Restart VS Code
- Hoặc dùng Python HTTP server thay thế
- Hoặc mở trực tiếp file HTML

---

## 📸 SCREENSHOTS CHO BÁO CÁO

### Screenshot 1: Landing Page
- Full page với hero section + features + statistics
- File name: `01_landing_page.png`

### Screenshot 2: Chat Widget Closed
- Page với chat button ở góc dưới phải
- File name: `02_chat_button.png`

### Screenshot 3: Chat Widget Open
- Chat widget đang mở với welcome message
- File name: `03_chat_open.png`

### Screenshot 4: Chat Conversation
- Cuộc hội thoại thực tế với bot
- Ít nhất 5-6 messages
- File name: `04_conversation.png`

### Screenshot 5: Quick Replies
- Bot hiển thị quick reply buttons
- File name: `05_quick_replies.png`

### Screenshot 6: Program Information
- Bot trả lời thông tin ngành học
- File name: `06_program_info.png`

### Screenshot 7: Tuition Calculation
- Bot tính học phí với form
- File name: `07_tuition.png`

### Screenshot 8: GPS Directions
- Bot cung cấp link Google Maps
- File name: `08_gps.png`

### Screenshot 9: Mobile View
- Chat trên mobile (responsive)
- File name: `09_mobile.png`

### Screenshot 10: Developer Console
- Terminal với Rasa server running
- File name: `10_backend.png`

---

## 📊 THÔNG SỐ HỆ THỐNG (CHO BÁO CÁO)

### Backend
- **Rasa Version:** 3.6.20
- **Model:** 20251105-094248-savory-envelope.tar.gz
- **Accuracy:** 99.9%
- **Intents:** 30
- **Entities:** 7
- **Actions:** 12 custom actions
- **Database:** 44 programs

### AI Integration
- **Rasa NLU:** DIET Classifier
- **Gemini AI:** google/gemini-1.5-flash-002
- **Goong Maps API:** GPS navigation
- **Slot Filling:** FormAction pattern

### Frontend
- **Framework:** Vanilla JavaScript
- **UI Library:** Tailwind CSS (CDN)
- **Icons:** Font Awesome 6.4.0
- **Browser Support:** Chrome, Firefox, Edge, Safari
- **Mobile Support:** Responsive design

### API
- **Endpoint:** http://localhost:5005/webhooks/rest/webhook
- **Method:** POST
- **Format:** JSON
- **CORS:** Enabled
- **Timeout:** 10 seconds

---

## 🎯 CHECKLIST HOÀN THÀNH

### Trước khi demo/báo cáo:

- [ ] Backend servers đang chạy (ports 5005 & 5055)
- [ ] Frontend đang chạy (Live Server hoặc HTTP server)
- [ ] Test tất cả 5 chức năng chính
- [ ] Chụp 10 screenshots
- [ ] Chuẩn bị câu hỏi demo mẫu
- [ ] Check logs không có error
- [ ] Đọc lại PROJECT_SUMMARY.md
- [ ] Backup code (đã có ở backup folder)

---

## 🚀 DEMO FLOW KHUYẾN NGHỊ

### 1. Giới thiệu (30 giây)
- Mở landing page
- Giải thích về VHU Chatbot
- Chỉ các features trên trang

### 2. Demo Chat Widget (1 phút)
- Click chat button
- Giải thích UI/UX
- Hiển thị welcome message

### 3. Demo các chức năng (3 phút)

**3.1. Tra cứu ngành (30s)**
```
"Có những ngành nào?"
"Cho tôi biết về ngành Công nghệ thông tin"
```

**3.2. Tính học phí (30s)**
```
"Tính học phí"
→ "Công nghệ thông tin"
→ "15 tín chỉ"
```

**3.3. Gợi ý ngành (30s)**
```
"Gợi ý ngành học cho tôi"
→ "Tôi thích toán và lập trình"
```

**3.4. Chỉ đường GPS (30s)**
```
"Chỉ đường đến VHU"
→ "Bến Thành"
```

**3.5. Gemini AI (30s)**
```
"Kể cho tôi nghe về VHU"
```

### 4. Giải thích kỹ thuật (1 phút)
- Backend: Rasa + Actions + APIs
- Frontend: HTML + CSS + JS
- AI: DIET + Gemini + Goong Maps
- Accuracy: 99.9%

---

## 📞 HỖ TRỢ

Nếu gặp vấn đề khi chạy:

1. Check terminal xem có error không
2. Check Console trong browser (F12)
3. Restart tất cả servers
4. Kiểm tra lại đường dẫn files
5. Xem lại phần Troubleshooting

---

**Good luck với báo cáo! 🎓🚀**

Created by: Hải - VHU Student
Date: November 2024
Version: 1.0
