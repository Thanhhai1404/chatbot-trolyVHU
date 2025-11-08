# 🔧 FIXING GEMINI AI - TROUBLESHOOTING LOG

## ❌ VẤN ĐỀ BAN ĐẦU
Gemini không được kích hoạt khi user hỏi câu ngoài phạm vi như "thời tiết hôm nay thế nào?". Bot trả lời "Xin lỗi, mình chưa có thông tin này" thay vì dùng Gemini AI.

---

## 🔍 QUÁ TRÌNH DEBUG

### Issue #1: RulePolicy Override
**Vấn đề:** `RulePolicy` có config `core_fallback_action_name: "utter_fallback"` 
→ Override rule Gemini

**Giải pháp:** ✅ Đã fix trong `config.yml`
```yaml
- name: RulePolicy
  # Removed core_fallback to let Gemini handle fallback via rules
```

### Issue #2: Intent Classification Threshold
**Vấn đề:** `FallbackClassifier` có threshold = 0.65 quá cao
→ Model không phân loại câu "thời tiết" vào `out_of_scope` hoặc `nlu_fallback`

**Giải pháp:** ✅ Đã fix trong `config.yml`
```yaml
- name: FallbackClassifier
  threshold: 0.5  # Giảm từ 0.65 → 0.5
  ambiguity_threshold: 0.1  # Tăng từ 0.05 → 0.1
```

### Issue #3: Rules Configuration
**Status:** ✅ ĐÃ ĐÚNG - Không cần sửa

Rules đã được cấu hình trong `data/rules.yml`:
```yaml
- rule: Gemini AI fallback for out-of-scope questions
  steps:
    - intent: out_of_scope
    - action: action_gemini_fallback

- rule: Gemini AI fallback for nlu_fallback
  steps:
    - intent: nlu_fallback
    - action: action_gemini_fallback
```

### Issue #4: NLU Training Data
**Status:** ✅ ĐÃ ĐÚNG - Không cần sửa

Intent `out_of_scope` đã có examples trong `data/nlu.yml`:
```yaml
- intent: out_of_scope
  examples: |
    - thời tiết hôm nay thế nào  # ← Đã có!
    - công thức nấu phở
    - bạn bao nhiêu tuổi
    # ... 30+ examples khác
```

### Issue #5: Action Implementation
**Status:** ✅ ĐÃ ĐÚNG - Không cần sửa

`ActionGeminiFallback` trong `actions/actions.py`:
```python
should_use_gemini = (
    intent in ['out_of_scope', 'nlu_fallback'] and
    not is_vhu_question
)
```

---

## 🔧 GIẢI PHÁP CUỐI CÙNG

### 1. Config Changes

**File:** `config.yml`

#### Before:
```yaml
- name: FallbackClassifier
  threshold: 0.65  # Quá cao
  ambiguity_threshold: 0.05

- name: RulePolicy
  core_fallback_threshold: 0.3
  core_fallback_action_name: "utter_fallback"  # Override Gemini
```

#### After:
```yaml
- name: FallbackClassifier
  threshold: 0.5  # Giảm để dễ trigger fallback
  ambiguity_threshold: 0.1  # Tăng để phát hiện ambiguous

- name: RulePolicy
  # Removed core_fallback configs
```

### 2. Re-train Model
```bash
rasa train
# New model: models/20251023-XXXXXX-YYYY.tar.gz
```

---

## 📊 CÁCH HOẠT ĐỘNG (LÝ THUYẾT)

### Flow khi user hỏi "thời tiết hôm nay thế nào?":

```
1. NLU Pipeline
   ├─ Input: "thời tiết hôm nay thế nào?"
   ├─ DIETClassifier: Phân loại intent
   └─ FallbackClassifier: Kiểm tra confidence
       └─ If confidence < 0.5:
           └─ Intent = out_of_scope hoặc nlu_fallback

2. Core (Dialogue Management)
   ├─ RulePolicy: Tìm matching rule
   └─ Rule found: "Gemini AI fallback for out-of-scope"
       └─ Action = action_gemini_fallback

3. Action Execution
   ├─ Check: is_vhu_related_question("thời tiết...")
   │   └─ False (không liên quan VHU)
   └─ should_use_gemini = True
       └─ Call Gemini API
           └─ Response: "Chào bạn! Hôm nay ở Sài Gòn..."
```

### Flow khi user hỏi "học phí CNTT":

```
1. NLU Pipeline
   ├─ Input: "học phí CNTT"
   ├─ DIETClassifier: Phân loại intent
   └─ Intent = ask_tuition_specific (confidence > 0.9)

2. Core (Dialogue Management)
   ├─ TEDPolicy: Predict action
   └─ Action = action_tuition_specific

3. Action Execution
   └─ Bot VHU trả lời về học phí CNTT
```

---

## ✅ KẾT QUẢ MONG ĐỢI

### Test Cases:

| Câu hỏi | Intent Predicted | Confidence | Action Called | Response From |
|---------|------------------|------------|---------------|---------------|
| "thời tiết hôm nay thế nào?" | `out_of_scope` | < 0.5 | `action_gemini_fallback` | ✅ Gemini AI |
| "công thức nấu phở ngon" | `out_of_scope` | < 0.5 | `action_gemini_fallback` | ✅ Gemini AI |
| "bạn bao nhiêu tuổi" | `out_of_scope` | < 0.5 | `action_gemini_fallback` | ✅ Gemini AI |
| "học phí CNTT" | `ask_tuition_specific` | > 0.9 | `action_tuition_specific` | ✅ Bot VHU |
| "địa chỉ trường" | `ask_location` | > 0.9 | `action_campuses_info` | ✅ Bot VHU |

---

## 🧪 CÁCH TEST

### Test 1: Unit Test (Python)
```bash
python test_gemini_integration.py
# Expected: 4/4 tests PASS
```

### Test 2: Rasa Shell
```bash
# Terminal 1: Start action server
rasa run actions

# Terminal 2: Start shell
rasa shell

# Test inputs:
Your input -> thời tiết hôm nay thế nào?
# Expected: Gemini response với thời tiết

Your input -> học phí CNTT
# Expected: Bot VHU response với học phí chi tiết
```

---

## 🚨 TROUBLESHOOTING

### Nếu vẫn không hoạt động:

#### 1. Kiểm tra model đã train với config mới chưa
```bash
# Check file models/
dir models
# Should see newest .tar.gz file
```

#### 2. Kiểm tra action server có load action_gemini_fallback không
```bash
rasa run actions
# Should see log: "Registered function for 'action_gemini_fallback'"
```

#### 3. Test Gemini API key
```bash
python test_gemini_integration.py
# Should see SUCCESS responses
```

#### 4. Check logs khi test trong shell
- Action server terminal sẽ show:
  ```
  INFO - Gemini Fallback - Intent: out_of_scope, Confidence: 0.45
  INFO - Gemini response sent successfully
  ```

#### 5. Nếu model vẫn phân loại sai
→ Thêm nhiều examples hơn cho `out_of_scope` intent
→ Giảm threshold xuống 0.4 hoặc 0.3

---

## 📝 NOTES

- Threshold 0.5 là balance tốt giữa accuracy và coverage
- Nếu quá nhiều câu VHU bị nhầm thành out_of_scope → Tăng threshold lên 0.55-0.6
- Nếu quá ít câu out_of_scope được detect → Giảm threshold xuống 0.4-0.45
- Gemini API có rate limit: 60 requests/minute (free tier)
- Mỗi Gemini call tốn ~500-1000 tokens

---

## 🎯 NEXT STEPS

- [ ] Wait for training to complete
- [ ] Test in rasa shell
- [ ] Fine-tune threshold nếu cần
- [ ] Add more out_of_scope examples nếu cần
- [ ] Monitor Gemini API usage
- [ ] Consider caching common responses
