# Scripts Utility

Thư mục này chứa các scripts hỗ trợ phát triển và testing.

---

## 📚 MỤC LỤC

1. [Trích xuất dữ liệu PDF](#trích-xuất-dữ-liệu-pdf)
2. [Tạo và cập nhật dữ liệu](#tạo-và-cập-nhật-dữ-liệu)
3. [Testing Scripts](#testing-scripts)
4. [Tạo training data](#tạo-training-data)

---

## 📄 TRÍCH XUẤT DỮ LIỆU PDF

### ⭐ `extract_tuition_from_pdf_v2.py` (MỚI)
**Mục đích**: Trích xuất học phí từ PDF chính thức

**Cách dùng**:
```powershell
python scripts/extract_tuition_from_pdf_v2.py
```

**Tính năng**:
- Đọc PDF bằng `pdfplumber`
- Parse 44 ngành với học phí chính xác
- Parse 13 loại học bổng
- Tự động cập nhật `tuition.json`
- Lưu text gốc để verify

---

## 🔧 TẠO VÀ CẬP NHẬT DỮ LIỆU

- `create_full_programs_data.py`: Tạo dữ liệu programs.json
- `create_full_tuition_data.py`: Tạo dữ liệu tuition.json
- `fix_program_aliases.py`: Fix aliases
- `fix_tuition_program_ids.py`: Fix program IDs
- `update_actions_tone.py`: Cập nhật tone

---

## 🧪 TESTING SCRIPTS

### ⭐ `test_tuition_data.py` (MỚI)
Verify dữ liệu học phí
```powershell
python scripts/test_tuition_data.py
```

### ⭐ `test_tuition_chatbot.py` (MỚI)
Hướng dẫn test chatbot
```powershell
python scripts/test_tuition_chatbot.py
```

### Khác
- `test_chatbot.py`: Test chatbot chung
- `test_intents.py`: Test intent recognition
- `test_buoc2_conversation.py`: Test BƯỚC 2 features

---

## 📝 TẠO TRAINING DATA

### `generate_training_examples.py`
Auto-generate 110+ training examples
```powershell
python scripts/generate_training_examples.py
```

---

## 🔄 WORKFLOW KHUYẾN NGHỊ

### Cập nhật học phí hàng năm
```powershell
# 1. Đặt PDF mới vào thư mục gốc
# 2. Sửa path trong extract_tuition_from_pdf_v2.py
# 3. Chạy:
python scripts/extract_tuition_from_pdf_v2.py
python scripts/test_tuition_data.py
rasa train
rasa shell
```

---

**Cập nhật**: 19/10/2025  
**Version**: 2.1.0
