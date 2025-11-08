# 🌐 VHU CHATBOT - WEB INTERFACE

**Trang web tích hợp Rasa Chatbot với giao diện đẹp mắt và tính năng đầy đủ**

Created by: Hải - VHU Student  
Date: November 2024  
Version: 1.0

---

## 📁 CẤU TRÚC

```
frontend/
├── index.html          # Landing page + Chat widget
├── css/
│   └── style.css      # Custom styles & animations
├── js/
│   ├── config.js      # API configuration & constants
│   ├── chat.js        # Rasa API integration
│   └── ui.js          # UI controls & helpers
├── assets/            # Images, icons (nếu có)
├── GUIDE.md          # Hướng dẫn chi tiết
└── README.md         # File này
```

---

## ✨ TÍNH NĂNG

### 🎨 Landing Page
- **Hero Section**: Banner giới thiệu chatbot
- **6 Feature Cards**: Hiển thị các tính năng chính
  - 📚 44 ngành đào tạo
  - 💰 Tính học phí
  - 🎯 Gợi ý ngành học
  - 🗺️ Chỉ đường GPS
  - 🏅 Thông tin học bổng
  - 🧠 Gemini AI fallback
- **Statistics**: 99.9% accuracy, 44 programs, 30 intents, 7 campuses
- **Responsive Design**: Hoạt động tốt trên mọi thiết bị

### 💬 Chat Widget
- **Floating Button**: Button chat ở góc dưới phải
- **Expandable Window**: Chat window 400x600px
- **Welcome Message**: Tự động chào khi mở chat
- **Quick Replies**: Các nút trả lời nhanh
- **Message Bubbles**: User (xanh) vs Bot (trắng)
- **Typing Indicator**: Hiển thị khi bot đang suy nghĩ
- **Auto Scroll**: Tự động scroll xuống tin nhắn mới
- **Clear Chat**: Xóa toàn bộ cuộc trò chuyện
- **Keyboard Shortcuts**: Ctrl+K, Ctrl+L, Enter, Escape

### 🎨 UI/UX
- **VHU Branding**: Colors (Blue #0066CC, Gold #FFB800)
- **Smooth Animations**: Fade in, slide up, bounce effects
- **Custom Scrollbar**: Thanh cuộn đẹp mắt
- **Hover Effects**: Transform, shadow effects
- **Notifications**: Success/Error messages
- **Loading States**: Typing indicator, loading spinner

---

## 🚀 CÁCH CHẠY

### Phương pháp 1: Live Server (Khuyến nghị)

1. Install extension "Live Server" trong VS Code
2. Mở file `index.html`
3. Click chuột phải → "Open with Live Server"
4. Browser tự mở: `http://127.0.0.1:5500/frontend/index.html`

### Phương pháp 2: Python HTTP Server

```bash
cd frontend
python -m http.server 8000
```

Sau đó mở: `http://localhost:8000/index.html`

### Phương pháp 3: Mở trực tiếp

- Double click vào `index.html`
- ⚠️ Có thể gặp CORS error

---

## 🔧 CẤU HÌNH

### API Endpoint (config.js)

```javascript
const CONFIG = {
    RASA_API_URL: 'http://localhost:5005/webhooks/rest/webhook',
    API_TIMEOUT: 10000,
    ACTION_SERVER_URL: 'http://localhost:5055'
};
```

### UI Settings (config.js)

```javascript
const CHATBOT_SETTINGS = {
    chatWindowWidth: '400px',
    chatWindowHeight: '600px',
    maxMessagesDisplay: 100,
    autoGreeting: true,
    greetingDelay: 500
};
```

---

## 🧪 TEST

### Checklist cơ bản

- [ ] Landing page hiển thị đúng
- [ ] Chat button xuất hiện
- [ ] Click chat button → Widget mở
- [ ] Welcome message hiển thị
- [ ] Send message → Bot trả lời
- [ ] Quick replies hoạt động
- [ ] Clear chat hoạt động
- [ ] Keyboard shortcuts hoạt động

### Test các chức năng chính

1. **Tra cứu ngành**: "Có những ngành nào?"
2. **Tính học phí**: "Tính học phí CNTT 15 tín chỉ"
3. **Gợi ý ngành**: "Gợi ý ngành cho tôi"
4. **Chỉ đường**: "Chỉ đường từ Bến Thành đến VHU"
5. **Học bổng**: "Có học bổng nào?"
6. **Gemini AI**: "Giới thiệu về VHU"

---

## 📱 RESPONSIVE

- **Desktop**: 400x600px chat window
- **Tablet**: Scaled down appropriately
- **Mobile**: Full screen chat

---

## 🎨 DESIGN SYSTEM

### Colors

```css
--vhu-blue: #0066CC;
--vhu-gold: #FFB800;
--text-primary: #1F2937;
--text-secondary: #6B7280;
--bg-light: #F9FAFB;
```

### Typography

- **Font**: Inter, SF Pro, Segoe UI
- **Sizes**: 12px - 48px
- **Weights**: 400 (Regular), 500 (Medium), 700 (Bold)

### Shadows

- **Small**: 0 2px 8px rgba(0,0,0,0.1)
- **Medium**: 0 4px 20px rgba(0,102,204,0.3)
- **Large**: 0 8px 30px rgba(0,102,204,0.6)

---

## 🔌 API INTEGRATION

### Request Format

```javascript
POST http://localhost:5005/webhooks/rest/webhook
Content-Type: application/json

{
    "sender": "user_1234567890_5678",
    "message": "Xin chào"
}
```

### Response Format

```javascript
[
    {
        "text": "Xin chào! Tôi có thể giúp gì cho bạn?",
        "buttons": [
            {
                "title": "44 ngành đào tạo",
                "payload": "Có những ngành nào?"
            }
        ]
    }
]
```

---

## 🐛 TROUBLESHOOTING

### Lỗi: "Failed to fetch"

**Nguyên nhân**: Rasa server chưa chạy hoặc CORS chưa enable

**Giải pháp**:
```bash
rasa run --enable-api --cors "*" --port 5005
```

### Lỗi: Messages không hiển thị

**Nguyên nhân**: Lỗi JavaScript

**Giải pháp**: Mở Console (F12) và check error

### Lỗi: Live Server không hoạt động

**Giải pháp**: Dùng Python HTTP server hoặc mở trực tiếp file

---

## 📚 TÀI LIỆU THAM KHẢO

- [Rasa REST API Documentation](https://rasa.com/docs/rasa/pages/http-api)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [Font Awesome Icons](https://fontawesome.com/icons)
- [MDN Web Docs](https://developer.mozilla.org/)

---

## 🎯 FEATURES NÂNG CAO (FUTURE)

- [ ] Dark mode toggle
- [ ] Multi-language support (EN/VI)
- [ ] Voice input/output
- [ ] Chat history export
- [ ] Emoji picker
- [ ] File upload
- [ ] Rich media (cards, carousels)
- [ ] User authentication
- [ ] Chat analytics dashboard

---

## 📄 LICENSE

MIT License - Tự do sử dụng cho mục đích học tập

---

## 👨‍💻 DEVELOPER

**Hải - VHU Student**
- Project: VHU Chatbot Web Interface
- Course: AI/NLP
- Year: 2024

---

**For detailed guide, see [GUIDE.md](GUIDE.md)**
