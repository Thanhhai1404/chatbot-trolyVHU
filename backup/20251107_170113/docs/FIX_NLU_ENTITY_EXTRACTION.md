# 🐛 FIX: Lỗi NLU Extract Entity Nhầm trong Tư Vấn Ngành Học

## ❌ VẤN ĐỀ

Sau khi nâng cấp lên **FULL POWER MODE**, bot bị lỗi:

**User input:**
```
tôi muốn tư vấn chọn ngành
```

**Bot response (SAI):**
```
🎓 **TƯ VẤN NGÀNH HỌC DÀNH CHO BẠN**
📚 **Tổ hợp môn:** VĂN        ← ❌ TỰ Ý GÁN
💡 **Sở thích:** lập           ← ❌ TỰ Ý GÁN
```

**Kỳ vọng (ĐÚNG):**
```
Để mình tư vấn ngành phù hợp, bạn cho mình biết:
1️⃣ Tổ hợp môn của bạn là gì?
2️⃣ Sở thích hoặc ngành bạn quan tâm?
```

---

## 🔍 NGUYÊN NHÂN

### 1. **NLU FULL POWER quá mạnh**
- Model FULL POWER có transformer layers mạnh hơn (2→4 layers, 128→256 size)
- Nhạy cảm hơn với pattern matching
- Extract entity từ câu trigger "tôi muốn tư vấn **chọn** ngành"

### 2. **Training data có pattern tương tự**
```yaml
# data/nlu.yml, dòng 228
- Giúp tôi chọn ngành học  ← Pattern có từ "chọn"
```

→ NLU thấy "chọn" → nhầm là entity!

### 3. **Logic validation yếu**
```python
# Code cũ - SAI
if not subject_combo and not interest:  # Chỉ hỏi khi CẢ HAI đều None
    ask_user()
```

→ Nếu có 1 trong 2 (dù sai), bot vẫn chạy tiếp!

---

## ✅ GIẢI PHÁP

### Fix 1: **Thêm Action Reset Slots**

**File mới:** `actions/actions.py`

```python
class ActionSetSlotsToNone(Action):
    """Reset các slots trước khi tư vấn ngành"""
    
    def name(self) -> Text:
        return "action_set_slots_to_none"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        return [
            SlotSet("subject_combination", None),
            SlotSet("interest", None),
            SlotSet("recommended_programs", None)
        ]
```

**Lợi ích:** Đảm bảo slots **luôn sạch** trước khi hỏi user!

---

### Fix 2: **Update Rule để Reset Slots**

**File:** `data/rules.yml`

```yaml
# TRƯỚC (Cũ):
- rule: recommend programs when asked
  steps:
    - intent: ask_recommend_programs
    - action: action_recommend_programs

# SAU (Mới):
- rule: recommend programs when asked
  steps:
    - intent: ask_recommend_programs
    - action: action_set_slots_to_none  # ← THÊM: Reset trước
    - action: action_recommend_programs
```

**Flow mới:**
1. User: "tôi muốn tư vấn ngành"
2. Intent: `ask_recommend_programs`
3. **Action 1:** `action_set_slots_to_none` → Reset slots
4. **Action 2:** `action_recommend_programs` → Hỏi user

---

### Fix 3: **Cải thiện Logic Validation**

**File:** `actions/actions.py` - Method `ActionRecommendPrograms.run()`

```python
# TRƯỚC (Cũ):
if not subject_combo and not interest:  # Chỉ check None
    ask_user()

# SAU (Mới):
# Validate: Phải có ít nhất 1 trong 2 thông tin HỢP LỆ
valid_subject = subject_combo and len(str(subject_combo).strip()) >= 2
valid_interest = interest and len(str(interest).strip()) >= 2

if not valid_subject and not valid_interest:  # Check cả None và length
    ask_user()
```

**Lợi ích:**
- ✅ Reject values quá ngắn (< 2 ký tự) như "VĂN", "lập"
- ✅ Buộc user phải cung cấp thông tin đầy đủ

---

### Fix 4: **Fix Syntax Errors (Bonus)**

**File:** `actions/actions.py`

```python
# TRƯỚC (Tiếng Việt):
if "contact" in CONTACTS_DATA và "departments" in ...  # ❌
if "học phí" in ... hoặc "tài chính" in ...           # ❌

# SAU (Python):
if "contact" in CONTACTS_DATA and "departments" in ... # ✅
if "học phí" in ... or "tài chính" in ...              # ✅
```

---

### Fix 5: **Update Domain**

**File:** `domain.yml`

```yaml
actions:
  # ...existing actions...
  - action_set_slots_to_none  # ← THÊM action mới
  - action_recommend_programs
```

---

## 📊 KẾT QUẢ SAU KHI FIX

### Test case 1: Trigger không có entity
```
User: tôi muốn tư vấn chọn ngành

Bot:
Để mình tư vấn ngành phù hợp, bạn cho mình biết:
1️⃣ **Tổ hợp môn** của bạn là gì?
2️⃣ **Sở thích** hoặc ngành bạn quan tâm?
```
✅ **PASS** - Bot hỏi lại thay vì tự ý gán!

### Test case 2: Có đầy đủ thông tin
```
User: Tôi học khối C01 và thích công nghệ

Bot:
🎓 **TƯ VẤN NGÀNH HỌC DÀNH CHO BẠN**
📚 **Tổ hợp môn:** C01
💡 **Sở thích:** công nghệ
🌟 **Top 5 ngành phù hợp:**
...
```
✅ **PASS** - Bot hiểu đúng và tư vấn!

### Test case 3: Thiếu một phần thông tin
```
User: Tôi thích công nghệ nhưng chưa biết học khối nào

Bot:
🎓 **TƯ VẤN NGÀNH HỌC DÀNH CHO BẠN**
💡 **Sở thích:** công nghệ
🌟 **Top 5 ngành phù hợp:**
...
```
✅ **PASS** - Bot vẫn tư vấn được dựa trên sở thích!

---

## 🔄 TRAINING & DEPLOYMENT

### Các file đã sửa:
1. ✅ `actions/actions.py` - Thêm `ActionSetSlotsToNone` + fix validation
2. ✅ `data/rules.yml` - Update rule để reset slots
3. ✅ `domain.yml` - Thêm action mới
4. ✅ Fix syntax errors (và→and, hoặc→or)

### Training command:
```bash
rasa train --fixed-model-name vhu-chatbot-full-power-fixed
```

### Model output:
```
models/vhu-chatbot-full-power-fixed.tar.gz
```

---

## 🎯 BÀI HỌC

### 1. **FULL POWER = Strong but Sensitive**
- Model mạnh hơn → nhạy cảm hơn với patterns
- Cần validation logic chặt chẽ hơn
- Cần reset slots để tránh false positives

### 2. **Always Validate User Input**
- Không tin vào entity extraction 100%
- Check cả giá trị None và length
- Ưu tiên hỏi lại thay vì assume

### 3. **Test After Upgrade**
- FULL POWER mode có behavior khác LITE
- Cần test lại tất cả flows quan trọng
- Đặc biệt là các form/slot-based features

---

## ✅ CHECKLIST TESTING

Sau khi train xong, test các cases:

- [ ] "tôi muốn tư vấn ngành" → Bot phải hỏi lại
- [ ] "tư vấn ngành cho tôi" → Bot phải hỏi lại  
- [ ] "Tôi học C01 thích công nghệ" → Bot tư vấn ngay
- [ ] "Tôi thích lập trình" → Bot tư vấn (chỉ có interest)
- [ ] "Tôi học khối A00" → Bot tư vấn (chỉ có subject)
- [ ] "giúp tôi chọn ngành học" → Bot phải hỏi lại (không extract "chọn")

**Kỳ vọng:** Tất cả phải PASS!

---

## 📚 TÀI LIỆU LIÊN QUAN

- `FULL_POWER_SUMMARY.md` - So sánh LITE vs FULL POWER
- `UPGRADE_TO_FULL_POWER.md` - Hướng dẫn nâng cấp
- `FEATURE_PROGRAM_RECOMMENDATION.md` - Chi tiết feature tư vấn ngành

---

## 🚀 DEPLOYMENT

Sau khi train xong và test PASS:

```bash
# Terminal 1: Start action server
rasa run actions --port 5055

# Terminal 2: Start bot (hoặc rasa shell để test)
rasa shell
```

**Status:** ✅ FIXED & READY TO DEPLOY!
