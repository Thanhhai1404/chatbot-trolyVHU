# 🗺️ HƯỚNG DẪN ĐĂNG KÝ GOONG MAPS API

## Bước 1: Đăng ký tài khoản

1. Truy cập: https://account.map4d.vn/auth/register
2. Điền thông tin:
   - Email
   - Số điện thoại
   - Mật khẩu
3. Xác nhận email

## Bước 2: Tạo API Key

1. Đăng nhập: https://account.map4d.vn/
2. Vào mục **"API Keys"**
3. Click **"Create new key"**
4. Chọn APIs cần dùng:
   - ✅ **Geocoding API** (chuyển địa chỉ → tọa độ)
   - ✅ **Directions API** (tính đường đi)
5. Copy API Key

## Bước 3: Thêm vào file .env

```env
# Goong Maps API
GOONG_API_KEY=your_api_key_here
```

## Free Tier

- ✅ **50,000 requests/tháng** miễn phí
- ✅ Không cần thẻ tín dụng
- ✅ Đủ cho chatbot sinh viên

## Tài liệu API

- Geocoding: https://docs.map4d.vn/map4d-service/api/v1.0/#/api_geocode
- Directions: https://docs.map4d.vn/map4d-service/api/v1.0/#/api_route
