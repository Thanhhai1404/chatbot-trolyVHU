# 🚨 BÁO CÁO LỖI HỆ THỐNG - ERROR REPORT

**Ngày kiểm tra:** October 23, 2025  
**Công cụ:** `rasa data validate`  
**Trạng thái:** ❌ **CÓ LỖI CẦN SỬA**

---

## 🔴 LỖI NGHIÊM TRỌNG (CRITICAL ERRORS)

### **ERROR 1: `utter_fallback` không tồn tại** 🔴

```
The action 'utter_fallback' is used in the stories, 
but is not a valid utterance action.
```

**Nguyên nhân:**
- ✅ Đã xóa `utter_fallback` khỏi domain.yml (đúng)
- ❌ Nhưng stories.yml VẪN CÒN gọi `utter_fallback`

**Vị trí lỗi:** `data/stories.yml`

**Impact:** 🔴 **CRITICAL** - Bot sẽ lỗi khi chạy story có utter_fallback

**Cách sửa:**
```bash
# Tìm và thay thế utter_fallback trong stories.yml
# Option 1: Thay bằng action_gemini_fallback
# Option 2: Xóa story có utter_fallback
```

---

## ⚠️ CẢNH BÁO (WARNINGS)

### **GROUP 1: Unused Utterances (24 utterances)** ⚠️

Các `utter_*` được định nghĩa nhưng KHÔNG được sử dụng trong rules/stories:

```yaml
1.  utter_compliment_response            ⚠️
2.  utter_cant_help                      ⚠️
3.  utter_ask_campus_friendly            ⚠️
4.  utter_anything_else                  ⚠️
5.  utter_encourage                      ⚠️
6.  utter_offer_help                     ⚠️
7.  utter_ask_scholarship_type_friendly  ⚠️
8.  utter_checking                       ⚠️
9.  utter_default_fallback_friendly      ⚠️
10. utter_clarify_program                ⚠️
11. utter_compare_programs               ⚠️
12. utter_multiple_programs_discussed    ⚠️
13. utter_suggest_campus                 ⚠️
14. utter_suggest_admission              ⚠️
15. utter_ask_program_friendly           ⚠️
16. utter_remember_program               ⚠️
17. utter_got_it                         ⚠️
18. utter_did_that_help                  ⚠️
19. utter_list_programs                  ⚠️ (ĐÃ PHÁT HIỆN TRƯỚC)
20. utter_how_are_you                    ⚠️
21. utter_default_fallback               ⚠️
22. utter_suggest_scholarship            ⚠️
23. utter_suggest_career                 ⚠️
24. utter_wrap_up                        ⚠️ (có thể)
```

**Impact:** 🟡 **MEDIUM** - Không gây lỗi nhưng làm domain.yml dài và phức tạp

**Phân loại:**

#### **A. Friendly Prompts (Form-related)** - 3 cái
```yaml
- utter_ask_campus_friendly            # Cho campus form
- utter_ask_scholarship_type_friendly  # Cho scholarship form
- utter_ask_program_friendly           # Cho program form
```
**Gợi ý:** 
- 🟢 **GIỮ LẠI** nếu muốn friendly prompts cho forms
- 🔴 **XÓA** nếu không dùng custom ask actions

#### **B. Conversational Responses** - 8 cái
```yaml
- utter_compliment_response      # Trả lời khen ngợi
- utter_anything_else            # Hỏi có cần gì nữa
- utter_encourage                # Khuyến khích
- utter_offer_help               # Đề nghị giúp đỡ
- utter_checking                 # Đang kiểm tra
- utter_got_it                   # Hiểu rồi
- utter_did_that_help            # Có giúp được không
- utter_how_are_you              # Hỏi thăm
```
**Gợi ý:**
- 🟡 **TÙY CHỌN** - Có thể dùng trong stories để bot thân thiện hơn
- 🔴 **XÓA** nếu không có kế hoạch sử dụng

#### **C. Fallback-related** - 3 cái
```yaml
- utter_default_fallback_friendly  # Friendly fallback
- utter_default_fallback           # Default fallback
- utter_cant_help                  # Không giúp được
```
**Gợi ý:**
- 🔴 **XÓA TẤT CẢ** - Đã có action_gemini_fallback thay thế

#### **D. Suggestion Utterances** - 3 cái
```yaml
- utter_suggest_campus       # Gợi ý cơ sở
- utter_suggest_admission    # Gợi ý tuyển sinh
- utter_suggest_scholarship  # Gợi ý học bổng
- utter_suggest_career       # Gợi ý nghề nghiệp
```
**Gợi ý:**
- ✅ **Đã có actions thay thế:**
  - `action_suggest_campus_location`
  - `action_suggest_admission`
  - `action_suggest_scholarship`
  - `action_suggest_career`
- 🔴 **XÓA** - Không cần utterances, dùng actions

#### **E. Context-aware Utterances** - 5 cái
```yaml
- utter_clarify_program               # Làm rõ ngành
- utter_compare_programs              # So sánh ngành
- utter_multiple_programs_discussed   # Nhiều ngành đã bàn
- utter_remember_program              # Nhớ ngành
- utter_wrap_up                       # Kết thúc
```
**Gợi ý:**
- ✅ **Đã có actions thay thế:**
  - `action_compare_programs`
  - `action_remember_context`
- 🔴 **XÓA** - Dùng actions thay vì utterances

#### **F. Duplicates** - 1 cái
```yaml
- utter_list_programs  # Đã phát hiện trước
```
**Gợi ý:** 🔴 **XÓA** - Dùng `action_list_all_programs`

---

## 📊 TỔNG KẾT LỖI

| Loại lỗi | Số lượng | Mức độ |
|-----------|----------|--------|
| **Critical Errors** | 1 | 🔴 |
| **Unused Utterances** | 24 | ⚠️ |
| **Unused Actions** | 10 | ⚠️ |
| **Total Issues** | 35 | ⚠️ |

---

## 🎯 KẾ HOẠCH SỬA LỖI

### **PHASE 1: Sửa lỗi Critical** 🔴 (BẮT BUỘC)

#### Bước 1: Tìm utter_fallback trong stories
```bash
grep -n "utter_fallback" data/stories.yml
```

#### Bước 2: Thay thế hoặc xóa
```yaml
# Option 1: Thay bằng Gemini
- action: utter_fallback
↓
- action: action_gemini_fallback

# Option 2: Xóa story có utter_fallback
```

---

### **PHASE 2: Dọn dẹp Unused Utterances** ⚠️ (KHUYẾN NGHỊ)

#### **Option A: Xóa an toàn (Recommended)** 🟢

Xóa các utterances **CHẮC CHẮN** không dùng:

```yaml
# domain.yml - XÓA những cái này:

# 1. Fallback-related (3 cái)
- utter_default_fallback_friendly  ❌
- utter_default_fallback           ❌
- utter_cant_help                  ❌

# 2. Suggestion utterances (4 cái) - Đã có actions
- utter_suggest_campus             ❌
- utter_suggest_admission          ❌
- utter_suggest_scholarship        ❌
- utter_suggest_career             ❌

# 3. Context-aware (5 cái) - Đã có actions
- utter_clarify_program            ❌
- utter_compare_programs           ❌
- utter_multiple_programs_discussed ❌
- utter_remember_program           ❌
- utter_wrap_up                    ❌

# 4. Duplicate
- utter_list_programs              ❌

# TOTAL: 13 utterances
```

**Impact:** Thấp - Chỉ xóa những gì đã có thay thế

---

#### **Option B: Xóa tất cả unused** 🔴 (Aggressive)

Xóa toàn bộ 24 unused utterances

**Impact:** Cao - Cần test kỹ

---

#### **Option C: Giữ nguyên** 🟡

Không xóa gì, để dành cho tương lai

**Impact:** Không có - Nhưng domain.yml sẽ dài và rối

---

### **PHASE 3: Xóa Unused Actions** ⚠️ (TÙY CHỌN)

```yaml
# domain.yml - XÓA nếu đồng ý:
- action_hello                      ❌ (không có implement)
- utter_list_programs               ❌ (duplicate)

# Form-related - XÓA NẾU forms không hoạt động:
- action_ask_program                ⚠️
- action_ask_scholarship_type       ⚠️
- action_ask_campus                 ⚠️
- validate_tuition_form             ⚠️
- validate_scholarship_form         ⚠️
- validate_admission_form           ⚠️
- validate_campus_form              ⚠️
```

---

## 🚀 HÀNH ĐỘNG ĐỀ XUẤT

### **Cấp 1: PHẢI SỬA NGAY** 🔴

```bash
1. Sửa utter_fallback trong stories.yml
   → Thay bằng action_gemini_fallback
```

### **Cấp 2: NÊN SỬA** 🟡

```bash
2. Xóa 13 unused utterances (Option A)
   → Giảm complexity của domain.yml

3. Xóa action_hello và utter_list_programs
   → Cleanup duplicates
```

### **Cấp 3: CÓ THỂ SỬA** ⚠️

```bash
4. Test forms → Quyết định giữ hay xóa form actions
5. Xóa thêm 11 conversational utterances nếu không cần
```

---

## ❓ CÂU HỎI CHO BẠN

**Bạn muốn tôi:**

### Option 1: **Sửa lỗi Critical only** (An toàn) ✅
```
✅ Sửa utter_fallback trong stories.yml
❌ Không xóa gì khác
```
**Time:** 2 phút  
**Risk:** Thấp

---

### Option 2: **Sửa Critical + Cleanup cơ bản** (Khuyến nghị) 🟡
```
✅ Sửa utter_fallback trong stories.yml
✅ Xóa 13 unused utterances (chắc chắn không dùng)
✅ Xóa action_hello, utter_list_programs
```
**Time:** 5 phút  
**Risk:** Thấp

---

### Option 3: **Cleanup hoàn toàn** (Aggressive) 🔴
```
✅ Sửa utter_fallback
✅ Xóa tất cả 24 unused utterances
✅ Test và xóa form actions nếu không dùng
```
**Time:** 10-15 phút  
**Risk:** Trung bình

---

**BẠN CHỌN OPTION NÀO? Trả lời số (1/2/3) để tôi thực hiện!** 🎯
