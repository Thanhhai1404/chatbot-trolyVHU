# 🗺️ HƯỚNG DẪN SỬ DỤNG CHỨC NĂNG CHỈ ĐƯỜNG

## 📋 TỔNG QUAN

Chức năng mới cho phép bot chỉ đường từ vị trí user đến 7 cơ sở VHU bằng **Goong Maps API**.

## 🚀 CÀI ĐẶT

### Bước 1: Đăng ký Goong Maps API

1. Truy cập: https://account.map4d.vn/auth/register
2. Đăng ký tài khoản (Email + SĐT)
3. Đăng nhập và tạo API Key
4. Copy API Key

### Bước 2: Thêm API Key vào .env

```env
GOONG_API_KEY=your_api_key_here
```

### Bước 3: Test API

```bash
python test_goong_maps.py
```

**Kết quả mong đợi:**
- ✅ Geocoding: Chuyển địa chỉ → tọa độ
- ✅ Directions: Tính đường đi
- ✅ Format: Message đẹp với emoji

### Bước 4: Train Model

```bash
rasa train
```

### Bước 5: Chạy Action Server

```bash
rasa run actions
```

### Bước 6: Test trong Shell

```bash
rasa shell
```

## 💬 CÁC TEST CASES

### Test 1: Hỏi đường cơ bản

```
User: Tôi muốn đến trường
Bot: Bạn đang ở đâu vậy? 📍
User: Tôi ở Tân Hương, Tân Phú
Bot: Bạn muốn đến cơ sở nào? (Hiển thị 7 cơ sở)
User: 2
Bot: [Chỉ đường chi tiết với khoảng cách, thời gian, các bước rẽ]
     🚌 Bạn có muốn biết thông tin xe buýt không?
```

### Test 2: Hỏi thêm về xe buýt

```
User: Có
Bot: [Thông tin xe buýt: tuyến, giá vé, thời gian, lưu ý]
```

### Test 3: Các cách hỏi khác

```
- "chỉ đường đến trường"
- "làm sao đến VHU"
- "hướng dẫn đường đi"
- "từ Quận 9 đến trường"
- "tôi muốn đến cơ sở"
```

## 📍 7 CƠ SỞ VHU

1. **Trụ sở chính** - 613 Âu Cơ, Tân Phú
2. **Harmony Campus** - 624 Âu Cơ, Tân Bình
3. **MyU Campus** - 665-667-669 Điện Biên Phủ, Q3
4. **Cơ sở Bình Triệu** - Khu phố 6, Bình Triệu, Thủ Đức
5. **Cơ sở Bình Tân** - Quốc lộ 1A, Bình Tân
6. **Cơ sở Thủ Đức** - Phước Thiện, Long Thạnh Mỹ, Thủ Đức
7. **Cơ sở Tân Bình** - Hoàng Văn Thụ, Tân Bình

## 🔧 CẤU TRÚC CODE

### Files đã tạo mới:

1. **`actions/goong_maps_api.py`** (262 lines)
   - `geocode_address()`: Địa chỉ → tọa độ
   - `get_directions()`: Tính đường đi
   - `format_directions_message()`: Format output
   - `get_transit_info()`: Thông tin xe buýt

2. **`test_goong_maps.py`** (103 lines)
   - Test script để kiểm tra API

3. **`GOONG_API_SETUP.md`**
   - Hướng dẫn đăng ký API

### Files đã sửa:

1. **`data/nlu.yml`**
   - Thêm intent: `ask_directions`, `confirm_transit_info`
   - Thêm examples cho intent mới

2. **`domain.yml`**
   - Thêm 2 intents mới
   - Thêm 3 slots: `user_location`, `target_campus`, `want_transit_info`
   - Thêm form: `directions_form`
   - Thêm 5 actions: `action_ask_user_location`, `action_ask_target_campus`, `action_get_directions`, `action_show_transit_info`, `validate_directions_form`
   - Thêm 3 responses mới

3. **`actions/actions.py`**
   - Thêm class `ActionGetDirections` (150 lines)
   - Thêm class `ActionShowTransitInfo` (60 lines)

4. **`actions/forms.py`**
   - Thêm class `ValidateDirectionsForm` (70 lines)

5. **`data/rules.yml`**
   - Thêm 3 rules cho chức năng chỉ đường

6. **`.env`**
   - Thêm `GOONG_API_KEY`

## 📊 OUTPUT EXAMPLE

```
🗺️ Chỉ đường từ Tân Hương, Tân Phú đến Harmony Campus

📍 Điểm đến: 624 Âu Cơ, Tân Bình, TP.HCM
📏 Khoảng cách: 3.8 km
⏱️ Thời gian: ~12 phút (xe máy)

🛣️ Hướng dẫn chi tiết:
1️⃣ ⬆️ Đi thẳng trên đường Tân Hương (500m)
2️⃣ ↪️ Rẽ phải vào đường Âu Cơ (2.5km)
3️⃣ ▶️ Tiếp tục thẳng (800m)
4️⃣ ▶️ Đến nơi bên phải tay

💡 Lưu ý: Tránh giờ cao điểm 7-9h sáng và 17-19h chiều

🚌 Bạn có muốn biết thêm thông tin xe buýt không nè?
```

**Nếu user trả lời "Có":**

```
🚌 Thông tin xe buýt đến Harmony Campus:

🚍 Xe buýt: 03, 18, 65, 93
📍 Cách bến xe Tân Sơn Nhất 2km
📍 Gần sân bay Tân Sơn Nhất

💰 Giá vé xe buýt: Khoảng 7,000đ/lượt
⏱️ Thời gian: Thường lâu hơn xe máy 10-15 phút

💡 Lưu ý: Xe buýt đông giờ cao điểm, bạn nên dự phòng thời gian nha!

🚐 VHU còn có xe đưa đón miễn phí giữa các cơ sở đó! 🎉
```

## ⚠️ XỬ LÝ LỖI

### Lỗi 1: Không tìm thấy địa chỉ

```
⚠️ Mình không tìm thấy địa chỉ 'abc xyz'.

💡 Bạn thử nhập cụ thể hơn nhé (VD: '123 Lê Văn Việt, Quận 9')
```

### Lỗi 2: API key chưa có

```
⚠️ Xin lỗi, mình không thể tìm đường lúc này.

💡 Bạn có thể liên hệ hotline 1800 1568 để được hỗ trợ nha! 😊
```

### Lỗi 3: Chọn cơ sở không hợp lệ

```
⚠️ Mình không hiểu bạn chọn cơ sở nào.

Bạn có thể chọn bằng số (1-7) hoặc tên cơ sở nha! 😊
```

## 📈 TÍNH NĂNG NỔI BẬT

✅ **Thông minh:**
- Tự động thêm "TP.HCM" vào địa chỉ
- Hiểu được nhiều cách nhập (số, tên cơ sở)
- Parse và format đẹp

✅ **Thân thiện:**
- Emoji phù hợp
- Tone gần gũi
- Lưu ý hữu ích

✅ **Đầy đủ:**
- Khoảng cách + thời gian
- Chi tiết từng bước rẽ
- Thông tin xe buýt (optional)

✅ **An toàn:**
- Validate input
- Handle lỗi gracefully
- Fallback messages

## 🔗 KHÔNG ẢNH HƯỞNG ĐẾN CHỨC NĂNG CŨ

- ✅ 44 ngành học: KHÔNG THAY ĐỔI
- ✅ 30 intents: KHÔNG THAY ĐỔI
- ✅ 7 custom actions cũ: KHÔNG THAY ĐỔI
- ✅ 4 forms cũ: KHÔNG THAY ĐỔI
- ✅ Gemini AI: KHÔNG THAY ĐỔI

**CHỈ THÊM MỚI**, không xóa, không sửa chức năng cũ!

## 📞 HỖ TRỢ

Nếu gặp vấn đề:
1. Kiểm tra GOONG_API_KEY trong .env
2. Chạy `python test_goong_maps.py`
3. Xem logs trong terminal

---

**Tác giả:** GitHub Copilot  
**Ngày tạo:** 30/10/2025  
**Version:** 1.0
