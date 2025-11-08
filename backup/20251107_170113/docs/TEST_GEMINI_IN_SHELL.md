# HƯỚNG DẪN TEST GEMINI AI TRONG RASA SHELL

## ✅ HOÀN THÀNH
- ✅ Gemini API đã được tích hợp
- ✅ Model đã được train: `20251023-170613-acyclic-cream.tar.gz`
- ✅ Intent `out_of_scope` đã được cấu hình
- ✅ Rules đã được thêm cho Gemini fallback
- ✅ Test script đã pass 100%

## 🚀 CÁCH TEST

### Bước 1: Start Action Server
Mở terminal 1 và chạy:
```bash
cd d:\workspace\chatbot
rasa_env_new\Scripts\rasa.exe run actions
```

**Kiểm tra output có dòng:**
```
✅ Registered function for 'action_gemini_fallback'
✅ Action endpoint is up and running on http://0.0.0.0:5055
```

### Bước 2: Start Rasa Shell
Mở terminal 2 và chạy:
```bash
cd d:\workspace\chatbot
rasa_env_new\Scripts\rasa.exe shell
```

### Bước 3: Test các câu hỏi

#### ✅ TEST 1: Câu hỏi ngoài phạm vi (Gemini xử lý)
```
Your input -> thời tiết hôm nay thế nào
```
**Kết quả mong đợi:**
- ✅ Gemini trả lời về thời tiết
- ✅ Có câu "💙 Bạn có muốn hỏi gì về VHU không?" ở cuối

```
Your input -> công thức nấu phở ngon
```
**Kết quả mong đợi:**
- ✅ Gemini trả lời về cách nấu phở
- ✅ Có nhắc đến VHU trong response

```
Your input -> bạn bao nhiêu tuổi
```
**Kết quả mong đợi:**
- ✅ Gemini trả lời thân thiện
- ✅ Có context về VHU

#### ✅ TEST 2: Câu hỏi về VHU (Bot cũ xử lý)
```
Your input -> học phí công nghệ thông tin
```
**Kết quả mong đợi:**
- ✅ Bot trả lời chi tiết về học phí CNTT
- ✅ KHÔNG dùng Gemini

```
Your input -> địa chỉ trường ở đâu
```
**Kết quả mong đợi:**
- ✅ Bot trả lời về địa chỉ cơ sở
- ✅ KHÔNG dùng Gemini

```
Your input -> học bổng có những loại nào
```
**Kết quả mong đợi:**
- ✅ Bot trả lời về các loại học bổng
- ✅ KHÔNG dùng Gemini

## 🔍 DEBUG

### Kiểm tra logs của Action Server
Trong terminal action server, bạn sẽ thấy:
```
INFO - Gemini Fallback - Intent: out_of_scope, Confidence: 0.95, Message: thời tiết hôm nay
INFO - Gemini response sent successfully
```

### Nếu Gemini không hoạt động:
1. Kiểm tra file `.env` có đúng API key không
2. Check Action Server có log lỗi không
3. Chạy test script: `python test_gemini_integration.py`

## 📊 KẾT QUẢ MONG ĐỢI

### ✅ Success Cases:
| Câu hỏi | Intent | Xử lý bởi |
|---------|--------|-----------|
| "thời tiết hôm nay" | `out_of_scope` | Gemini AI |
| "nấu phở thế nào" | `out_of_scope` | Gemini AI |
| "bạn bao nhiêu tuổi" | `out_of_scope` | Gemini AI |
| "học phí CNTT" | `ask_tuition_specific` | Bot VHU |
| "địa chỉ trường" | `ask_location` | Bot VHU |

### ❌ Failure Cases (và cách fix):
| Vấn đề | Nguyên nhân | Giải pháp |
|--------|-------------|-----------|
| Gemini không trả lời | API key sai | Kiểm tra `.env` |
| Bot trả lời "chưa hiểu" | Model chưa train | Chạy `rasa train --force` |
| Lỗi connection | Action server chưa chạy | Start action server |

## 🎯 NEXT STEPS

Sau khi test thành công:
1. ✅ Test thêm nhiều câu hỏi edge cases
2. ✅ Fine-tune Gemini prompts (nếu cần)
3. ✅ Monitor API usage (free tier có limit)
4. ✅ Thêm logging cho analytics

## 📝 NOTES
- Gemini chỉ được kích hoạt cho intent `out_of_scope` và `nlu_fallback`
- Tất cả câu hỏi về VHU được ưu tiên xử lý bởi bot cũ
- API key được lưu an toàn trong `.env` (không commit lên Git)
