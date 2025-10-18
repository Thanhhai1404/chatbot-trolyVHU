# 🧪 CÂU HỎI KIỂM TRA CHATBOT VHU - TÍNH HỌC PHÍ TỰ ĐỘNG

## 📋 HƯỚNG DẪN KIỂM TRA

### Bước 1: Mở 2 Terminal

**Terminal 1 - Action Server:**
```bash
cd d:\workspace\Chatbot
rasa_env_new\Scripts\activate
rasa run actions
```

**Terminal 2 - Rasa Shell:**
```bash
cd d:\workspace\Chatbot
rasa_env_new\Scripts\activate
rasa shell
```

---

## 💰 KIỂM TRA TÍNH HỌC PHÍ TỰ ĐỘNG

### Test 1: Hỏi học phí ngành CNTT
```
Your input -> học phí ngành công nghệ thông tin
```

**Kỳ vọng:**
- ✅ Bot trả lời với tone thân thiện: "Bạn ơi, mình tra giúp bạn học phí nè!"
- ✅ Hiển thị đầy đủ:
  - Học phí/tín chỉ: 450,000 VNĐ
  - Tổng số tín chỉ: 140
  - **Tổng cả khóa (4 năm): ~63,000,000 VNĐ** (tự động tính)
  - Học phí/học kỳ: 7-9 triệu đồng
  - Học phí/năm: 15-18 triệu đồng

---

### Test 2: Hỏi học phí bằng alias
```
Your input -> học phí CNTT
```

**Kỳ vọng:**
- ✅ Bot nhận diện alias "CNTT" = "Công nghệ thông tin"
- ✅ Trả về thông tin học phí tương tự Test 1

---

### Test 3: Hỏi học phí ngành Marketing
```
Your input -> học phí ngành marketing là bao nhiêu
```

**Kỳ vọng:**
- ✅ Hiển thị học phí Marketing
- ✅ Học phí/tín chỉ: 380,000 VNĐ
- ✅ Tổng 140 tín chỉ
- ✅ **Tổng cả khóa: ~51,300,000 VNĐ**

---

### Test 4: Hỏi học phí ngành Kế toán
```
Your input -> cho mình biết học phí kế toán
```

**Kỳ vọng:**
- ✅ Tone thân thiện
- ✅ Tính toán chính xác: 380,000 × 135 = 51,300,000 VNĐ

---

### Test 5: Hỏi học phí ngành không có trong DB
```
Your input -> học phí ngành vật lý
```

**Kỳ vọng:**
- ✅ Bot trả lời: "Ôi bạn ơi, mình chưa có thông tin chi tiết về học phí ngành vật lý nè."
- ✅ Gợi ý các ngành có sẵn
- ✅ Tone thân thiện

---

### Test 6: Hỏi chung chung về học phí
```
Your input -> học phí trường bao nhiêu
```

**Kỳ vọng:**
- ✅ Bot trả lời chung: "Bạn ơi, học phí trung bình khoảng 20-25 triệu đồng/năm..."
- ✅ Hỏi lại bạn muốn biết ngành nào

---

### Test 7: Hỏi học phí với typo
```
Your input -> hoc phi cong nghe thong tin
```

**Kỳ vọng:**
- ✅ Bot vẫn nhận diện được (nhờ lookup tables)
- ✅ Trả về thông tin chính xác

---

## 🎓 KIỂM TRA TONE THÂN THIỆN (PEER-TO-PEER)

### Test 8: Chào hỏi
```
Your input -> xin chào
```

**Kỳ vọng:**
- ✅ "Chào bạn 👋! Mình là trợ lý ảo của Đại học Văn Hiến. Bạn muốn tìm hiểu thông tin gì nè?"
- ✅ Hoặc: "Hiii! Mình là trợ lý VHU đây, có gì cần giúp không nè? 😊"

---

### Test 9: Hỏi về học bổng
```
Your input -> điều kiện học bổng
```

**Kỳ vọng:**
- ✅ "Để mình kể cho bạn nghe về học bổng nè:"
- ✅ Tone thân thiện, gần gũi

---

### Test 10: Hỏi về tuyển sinh
```
Your input -> phương thức tuyển sinh
```

**Kỳ vọng:**
- ✅ "Mình tra giúp bạn nè, trường có 4 phương thức tuyển sinh đó:"
- ✅ Kết thúc bằng: "Bạn định xét theo phương thức nào nè? 😊"

---

### Test 11: Hỏi địa chỉ
```
Your input -> trường ở đâu
```

**Kỳ vọng:**
- ✅ "Mình cho bạn địa chỉ 2 cơ sở nha:"
- ✅ "Bạn muốn đến thăm cơ sở nào không nè? 😊"

---

### Test 12: Cảm ơn
```
Your input -> cảm ơn
```

**Kỳ vọng:**
- ✅ "Không có gì đâu nè, vui là được rồi 😊"
- ✅ Hoặc: "Hehe, được giúp bạn mình cũng vui lắm! 💖"

---

### Test 13: Tạm biệt
```
Your input -> tạm biệt
```

**Kỳ vọng:**
- ✅ "Bye bye! Chúc bạn một ngày vui vẻ nha 💪✨"
- ✅ Hoặc: "Hẹn gặp lại bạn nha 👋 Chúc học tốt!"

---

## 🔍 KIỂM TRA FALLBACK & OUT-OF-SCOPE

### Test 14: Câu hỏi ngoài phạm vi
```
Your input -> thời tiết hôm nay thế nào
```

**Kỳ vọng:**
- ✅ "Ôi, câu hỏi này nằm ngoài chuyên môn của mình rồi bạn ơi! 😅"
- ✅ Gợi ý các chủ đề có thể hỗ trợ

---

### Test 15: Câu hỏi không rõ ràng
```
Your input -> bao nhiêu
```

**Kỳ vọng:**
- ✅ "Mình chưa hiểu ý bạn lắm 😅, bạn có thể nói lại rõ hơn được không nè?"
- ✅ Gợi ý ví dụ câu hỏi

---

## 📊 CHECK LIST TỔNG HỢP

### ✅ Tính năng tự động tính học phí
- [ ] Tính đúng: `total_fee = credit_fee × total_credits`
- [ ] Hiển thị "Tổng cả khóa (4 năm)"
- [ ] Hiển thị học phí/học kỳ và học phí/năm
- [ ] Format số tiền rõ ràng (dấu phẩy)

### ✅ Tone thân thiện (peer-to-peer)
- [ ] Sử dụng "Bạn ơi", "nè", "nha"
- [ ] Emoji phù hợp 😊 💰 🎓 ✨
- [ ] Không dùng "Quý khách", "Vui lòng"
- [ ] Kết thúc câu thân thiện

### ✅ Entity Recognition
- [ ] Nhận diện tên ngành chính xác
- [ ] Nhận diện alias (CNTT, QTKD, MKT...)
- [ ] Xử lý typo/sai chính tả

### ✅ Custom Actions
- [ ] `action_tuition_specific` hoạt động
- [ ] `action_program_info` hoạt động
- [ ] `action_scholarship_condition` hoạt động
- [ ] Action server chạy ổn định

---

## 🚀 LỆNH KIỂM TRA NHANH

### Chạy test tự động:
```bash
cd d:\workspace\Chatbot
rasa_env_new\Scripts\activate
python test_tuition_calculation_v2.py
```

### Test trong Rasa Shell:
```bash
# Terminal 1
rasa run actions

# Terminal 2
rasa shell
```

### Test với script:
```bash
python test_chatbot.py
```

---

## 📝 GHI CHÚ

### Các ngành có sẵn trong tuition.json:
1. ✅ Công nghệ thông tin (CNTT, IT)
2. ✅ Quản trị kinh doanh (QTKD)
3. ✅ Kế toán
4. ✅ Marketing (MKT)
5. ✅ Ngôn ngữ Anh (Tiếng Anh)
6. ✅ Tâm lý học
7. ✅ Luật kinh tế (Luật)
8. ✅ Quản trị du lịch (Du lịch)
9. ✅ Logistics
10. ✅ Thiết kế đồ họa (TKĐH)

### Công thức tính học phí:
```python
total_fee = fee_per_credit × total_credits
fee_per_semester = total_fee / 8  # 4 năm = 8 học kỳ
fee_per_year = total_fee / 4      # 4 năm
```

### Ví dụ: CNTT
- Học phí/tín chỉ: 450,000 VNĐ
- Tổng tín chỉ: 140
- **Tổng cả khóa: 450,000 × 140 = 63,000,000 VNĐ**
- Học phí/học kỳ: 63,000,000 / 8 = 7,875,000 VNĐ (~7.9 triệu)
- Học phí/năm: 63,000,000 / 4 = 15,750,000 VNĐ (~15.8 triệu)

---

**🎉 Chúc bạn test thành công! 🎉**
