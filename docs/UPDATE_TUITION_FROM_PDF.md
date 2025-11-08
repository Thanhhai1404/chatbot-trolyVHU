# CẬP NHẬT DỮ LIỆU HỌC PHÍ TỪ PDF CHÍNH THỨC

## 📄 Nguồn dữ liệu
- **File PDF**: `VHU. TB chinh sach hoc phi-hoc bong NH 2025-2026_FInal.pdf`
- **Ngày cập nhật**: 15/01/2025
- **Năm học**: 2025-2026

## ✅ Đã hoàn thành

### 1. Trích xuất dữ liệu từ PDF
- ✅ Tạo script: `scripts/extract_tuition_from_pdf_v2.py`
- ✅ Trích xuất text và bảng từ 3 trang PDF
- ✅ Parse 44 ngành học với mức học phí chính xác
- ✅ Parse 13 loại học bổng
- ✅ Lưu text gốc vào: `scripts/pdf_extracted_text.txt`

### 2. Cập nhật Knowledge Base
**File**: `data/knowledge_base/tuition.json`

**Cấu trúc dữ liệu mới**:
```json
{
  "academic_year": "2025-2026",
  "last_updated": "2025-01-15",
  "source": "VHU. TB chinh sach hoc phi-hoc bong NH 2025-2026_FInal.pdf",
  "programs": {
    "information_technology": {
      "name": "Công nghệ thông tin",
      "tuition_per_credit": 1368000,
      "tuition_semester_1": 16416000,
      "credits_semester_1": 12,
      "estimated_total_4_years": 131328000
    },
    ...44 ngành khác
  },
  "scholarships": [
    {
      "type": "Học bổng tài năng",
      "description": "Thủ khoa đầu vào cấp trường: Miễn 100% học phí toàn khóa"
    },
    ...12 loại khác
  ],
  "notes": [
    "Nhà trường cam kết không tăng học phí trong suốt khóa học",
    ...
  ]
}
```

### 3. Cập nhật Actions
**File**: `actions/actions.py`

**Thay đổi**:
- ✅ Cập nhật `find_tuition_by_program_id()` để hỗ trợ cấu trúc JSON mới
- ✅ Cập nhật `ActionTuitionSpecific` để hiển thị:
  - Học phí/tín chỉ
  - Học phí học kỳ 1 (12 tín chỉ)
  - Ước tính học phí 4 năm (8 học kỳ)
  - Top 3 học bổng
  - Ghi chú quan trọng
  - Thông tin liên hệ mới (1800 1568)

## 📊 Dữ liệu chi tiết

### Học phí theo nhóm ngành

#### Nhóm 1 - 8.736.000 VNĐ/học kỳ 1
- Ngôn ngữ Pháp
- Việt Nam học (dành cho người Việt Nam)

#### Nhóm 2 - 10.848.000 VNĐ/học kỳ 1
- Xã hội học

#### Nhóm 3 - 12.264.000 VNĐ/học kỳ 1
- Kỹ thuật môi trường

#### Nhóm 4 - 14.028.000 VNĐ/học kỳ 1
- Văn học
- Công nghệ sinh học

#### Nhóm 5 - 15.084.000 VNĐ/học kỳ 1
- Đạo diễn điện ảnh, truyền hình
- Ngôn ngữ Nhật
- Ngôn ngữ Anh
- Công nghệ tài chính
- Công nghệ thực phẩm
- Quản trị khách sạn
- Kinh tế

#### Nhóm 6 - Đa dạng (14.316.000 - 15.792.000 VNĐ)
- Kỹ thuật xây dựng: 14.316.000 VNĐ
- Du lịch, QTKD, Marketing, Kế toán, KHMT...: 15.792.000 VNĐ

#### Nhóm 7 - Đa dạng (14.880.000 - 16.416.000 VNĐ)
- Kỹ thuật Điện tử - Viễn thông: 14.880.000 VNĐ
- **Công nghệ thông tin**: 16.416.000 VNĐ ⭐
- Luật kinh tế: 16.416.000 VNĐ
- Kinh doanh thương mại: 16.416.000 VNĐ

#### Nhóm 8 - Đa dạng (15.444.000 - 17.028.000 VNĐ)
- Điều dưỡng: 15.444.000 VNĐ
- Ngôn ngữ Trung Quốc: 17.028.000 VNĐ
- Thương mại điện tử: 17.028.000 VNĐ
- Logistics: 17.028.000 VNĐ

#### Nhóm 9 - 17.472.000 VNĐ/học kỳ 1
- Luật
- Việt Nam học (dành cho người nước ngoài)

#### Nhóm 10 - 22.056.000 VNĐ/học kỳ 1
- Kiểm toán (cao nhất)

### Học bổng

#### 1. Học bổng tài năng
- **Thủ khoa cấp trường**: Miễn 100% học phí toàn khóa (1 suất)
- **Á khoa cấp trường**: Giảm 50% học phí toàn khóa (2 suất)
- **Thủ khoa từng ngành**: Giảm 30% học phí

#### 2. Đóng trước
- Đóng hết 1 năm: Giảm 10%
- Đóng hết 2 năm: Giảm 15%
- Đóng hết 3 năm: Giảm 20%
- **Đóng toàn khóa**: Giảm 25% ⭐

#### 3. Học tập suốt đời
- 26-30 tuổi: Giảm 35%
- 31-40 tuổi: Giảm 50%
- 41-50 tuổi: Giảm 70%
- 51-60 tuổi: Giảm 85%
- **>60 tuổi**: Miễn 100% ⭐

#### 4. Anh chị em ruột
- Giảm 20% học phí toàn khóa (áp dụng cho 1 người)

#### 5. Dịch vụ all-in-one
- Tặng phí giữ xe
- Dịch vụ hành chính
- Balo
- Đồng phục thể dục

## 🔧 Cách sử dụng script

### Chạy script trích xuất
```powershell
cd d:\workspace\Chatbot
python scripts/extract_tuition_from_pdf_v2.py
```

### Output
- ✅ `data/knowledge_base/tuition.json` - Dữ liệu JSON đã cập nhật
- ✅ `scripts/pdf_extracted_text.txt` - Text gốc từ PDF (để kiểm tra)

### Kiểm tra kết quả
```powershell
# Xem file JSON
cat data/knowledge_base/tuition.json | head -n 50

# Validate Rasa
rasa data validate

# Train model
rasa train
```

## 📝 Test Chatbot

### Câu hỏi mẫu
```
User: Học phí ngành CNTT bao nhiêu?
Bot: → Hiển thị 16.416.000 VNĐ/học kỳ 1 (1.368.000 VNĐ/tín chỉ)
     → Ước tính 4 năm: ~131 triệu VNĐ
     → Top 3 học bổng
     → Liên hệ 1800 1568

User: Có học bổng gì không?
Bot: → Liệt kê 13 loại học bổng với mô tả chi tiết
```

## 🎯 Lợi ích

### 1. Dữ liệu chính xác
- ✅ Trích xuất trực tiếp từ thông báo chính thức của trường
- ✅ Đầy đủ 44 ngành (không còn thiếu sót)
- ✅ Đúng năm học 2025-2026

### 2. Thông tin đầy đủ
- ✅ Học phí/tín chỉ
- ✅ Học phí/học kỳ
- ✅ Ước tính 4 năm
- ✅ 13 loại học bổng
- ✅ Chính sách ưu đãi

### 3. Dễ cập nhật
- ✅ Script có thể tái sử dụng cho năm sau
- ✅ Chỉ cần thay file PDF mới
- ✅ Tự động parse và cập nhật JSON

## 📞 Thông tin liên hệ (mới)
- **Tổng đài**: 1800 1568 (miễn phí)
- **Email**: tuyensinh@vhu.edu.vn
- **Website**: https://tuyensinh.vhu.edu.vn/

## 🔄 Quy trình cập nhật cho năm sau

1. **Nhận file PDF mới** (VD: năm 2026-2027)
2. **Đặt file vào thư mục gốc** `d:\workspace\Chatbot\`
3. **Sửa đường dẫn trong script**:
   ```python
   PDF_PATH = Path("d:/workspace/Chatbot/VHU_2026-2027.pdf")
   ```
4. **Chạy script**: `python scripts/extract_tuition_from_pdf_v2.py`
5. **Kiểm tra**: `cat data/knowledge_base/tuition.json`
6. **Train lại**: `rasa train`
7. **Test**: `rasa shell`

## ⚠️ Lưu ý

1. **Cam kết của trường**: Không tăng học phí trong suốt khóa học
2. **Xét duyệt hàng năm**: Các chương trình học bổng có thể thay đổi
3. **Dữ liệu chính xác nhất**: Luôn gọi 1800 1568 để được tư vấn chi tiết

---
**Cập nhật**: 19/10/2025
**Người thực hiện**: GitHub Copilot
**Trạng thái**: ✅ Hoàn thành
