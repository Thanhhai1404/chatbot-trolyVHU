# =================================================================
# 🎓 HƯỚNG DẪN BỔ SUNG TRAINING DATA CHO 44 NGÀNH
# =================================================================

## VẤN ĐỀ HIỆN TẠI

Bạn phát hiện đúng! Bot hiện tại **CHƯA CÓ ĐỦ TRAINING DATA** cho tất cả 44 ngành.

### Kiểm tra:
- ✅ Database có **44 ngành** đầy đủ trong `programs.json`
- ❌ NLU training chỉ có **~30-50 examples** (không đủ)
- ❌ Cần **ít nhất 5-10 examples/ngành** = ~220-440 examples

---

## GIẢI PHÁP: BỔ SUNG TRAINING DATA

### Option 1: Sử dụng Synonyms (NHANH - Khuyến nghị)

File `data/synonyms.yml` đã có **đầy đủ 44 ngành**! 
Bot có thể hiểu được tất cả các biến thể tên ngành.

**Kiểm tra:**
```powershell
cd d:\workspace\chatbot
Get-Content data\synonyms.yml | Select-String "synonym:" | Measure-Object
```

**Kết quả:** Đã có 44+ synonyms covering tất cả ngành!

### Option 2: Generate Training Examples (TỐT NHẤT)

Tạo file mới: `data/nlu_44_programs.yml`

```yaml
version: "3.1"

nlu:
- intent: ask_programs
  examples: |
    - [Quản trị kinh doanh](program)
    - [Marketing](program)
    - [Kinh doanh thương mại](program)
    - [Thương mại điện tử](program)
    - [Quản trị nhân lực](program)
    - [Logistics và Quản lý chuỗi cung ứng](program)
    - [Kinh doanh quốc tế](program)
    - [Tài chính doanh nghiệp](program)
    - [Công nghệ tài chính](program)
    - [Kế toán](program)
    - [Kiểm toán](program)
    - [Luật](program)
    - [Luật kinh tế](program)
    - [Khoa học dữ liệu](program)
    - [Công nghệ thông tin](program)
    - [Mạng máy tính và Truyền thông](program)
    - [Công nghệ sinh học](program)
    - [Kỹ thuật Điện tử - Viễn thông](program)
    - [Kỹ thuật môi trường](program)
    - [Công nghệ thực phẩm](program)
    - [Kỹ thuật xây dựng](program)
    - [Điều dưỡng](program)
    - [Dược học](program)
    - [Ngôn ngữ Anh](program)
    - [Ngôn ngữ Pháp](program)
    - [Ngôn ngữ Trung Quốc](program)
    - [Ngôn ngữ Nhật](program)
    - [Quan hệ quốc tế](program)
    - [Đông phương học](program)
    - [Trung Quốc học](program)
    - [Văn học](program)
    - [Việt Nam học](program)
    - [Xã hội học](program)
    - [Tâm lý học](program)
    - [Quan hệ công chúng](program)
    - [Truyền thông đa phương tiện](program)
    - [Quản trị du lịch](program)
    - [Quản trị lữ hành](program)
    - [Quản trị khách sạn](program)
    - [Quản trị nhà hàng và dịch vụ ăn uống](program)
    - [Đạo diễn điện ảnh, truyền hình](program)
    - [Công nghệ điện ảnh, truyền hình](program)
    - [Thanh nhạc](program)
    - [Piano](program)

- intent: ask_program_info
  examples: |
    - chi tiết ngành [Quản trị kinh doanh](program)
    - thông tin ngành [Marketing](program)
    - [Công nghệ thông tin](program) ra trường làm gì
    - học phí ngành [Kế toán](program)
    - [Luật](program) học những gì
    - [Dược học](program) như thế nào
    - cho tôi biết về [Tâm lý học](program)
    - ngành [Du lịch](program) có tốt không
    - [Công nghệ tài chính](program) ra trường làm gì
    - [Khoa học dữ liệu](program) học mấy năm
```

**Sau đó thêm vào `config.yml`:**
```yaml
importers:
- name: "MultiProjectImporter"
- name: "RasaFileImporter"
  paths:
    - data/nlu.yml
    - data/nlu_44_programs.yml  # <-- THÊM DÒNG NÀY
    - data/stories.yml
    - data/rules.yml
```

---

## CÁCH TEST SAU KHI BỔ SUNG

### 1. Retrain model
```powershell
cd d:\workspace\chatbot
rasa train
```

### 2. Test trong shell
```powershell
rasa shell
```

**Test commands:**
```
User: Có những ngành nào?
Bot: [Hiện 44 ngành]

User: Cho tôi biết về ngành Dược học
Bot: [Thông tin chi tiết về Dược học]

User: Ngành Thanh nhạc học phí bao nhiêu?
Bot: [Thông tin học phí Thanh nhạc]

User: Piano ra trường làm gì?
Bot: [Cơ hội việc làm ngành Piano]
```

---

## TẠI SAO SYNONYMS QUAN TRỌNG?

File `synonyms.yml` giúp bot hiểu **NHIỀU CÁCH GỌI TÊN** của cùng 1 ngành:

```yaml
- synonym: "Công nghệ thông tin"
  examples: |
    - CNTT
    - IT
    - Information Technology
    - công nghệ thông tin
    - cong nghe thong tin
```

Khi user hỏi "CNTT như thế nào?", bot sẽ:
1. Nhận diện entity: `CNTT`
2. Convert qua synonym → "Công nghệ thông tin"
3. Tìm trong `programs.json` theo key "Công nghệ thông tin"
4. Trả về thông tin đúng!

---

## KIỂM TRA COVERAGE HIỆN TẠI

```powershell
# Check synonyms
cd d:\workspace\chatbot
$syn = Get-Content data\synonyms.yml -Raw
$matches = ([regex]::Matches($syn, "- synonym:")).Count
Write-Host "Synonyms defined: $matches"

# Check programs
$json = Get-Content data\knowledge_base\programs.json -Raw | ConvertFrom-Json
Write-Host "Programs in database: $($json.programs.Count)"

# Tỉ lệ
Write-Host "Coverage: $($matches / $json.programs.Count * 100)%"
```

---

## KẾT LUẬN

### Hiện tại:
- ✅ **Database**: 44 ngành ĐẦY ĐỦ
- ✅ **Synonyms**: 44 ngành ĐẦY ĐỦ
- ⚠️  **NLU Training**: CHƯA ĐỦ (chỉ ~30 ngành)

### Giải pháp:
1. **Nhanh**: Dùng synonyms (đã có) → Bot vẫn hiểu được!
2. **Tốt**: Thêm training data như option 2
3. **Tốt nhất**: Retrain model với data mới

### Test ngay:
```powershell
rasa shell

# Thử ngành ít người biết:
User: Ngành Piano như thế nào?
User: Thanh nhạc học phí bao nhiêu?
User: Đạo diễn điện ảnh ra trường làm gì?
```

Nếu bot **không trả lời được** → Cần retrain với more data!

---

**Created:** November 7, 2024  
**Issue:** Missing NLU training for some of 44 programs  
**Solution:** Add more training examples + Use synonyms
