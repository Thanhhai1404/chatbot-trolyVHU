# 📚 HƯỚNG DẪN BỔ SUNG 43 NGÀNH ĐÀO TẠO

## ✅ **10 ngành đã có sẵn:**
1. Công nghệ thông tin
2. Quản trị kinh doanh
3. Kế toán
4. Marketing
5. Ngôn ngữ Anh
6. Tâm lý học
7. Luật kinh tế
8. Du lịch
9. Logistics
10. Thiết kế đồ họa

---

## 📝 **33 NGÀNH CẦN BỔ SUNG VÀO `programs.json`:**

### **KHỐI KINH TẾ - QUẢN TRỊ (13 ngành)**
11. **Tài chính - Ngân hàng**
12. **Quản trị nhà hàng - Khách sạn**
13. **Kinh doanh quốc tế**
14. **Kinh tế**
15. **Quản trị văn phòng**
16. **Thương mại điện tử**
17. **Kinh doanh nông nghiệp**
18. **Bất động sản**
19. **Quản trị dịch vụ du lịch và lữ hành**
20. **Kinh doanh thời trang**
21. **Quản trị logistics và chuỗi cung ứng**
22. **Kinh doanh thương mại**
23. **Quản trị khách sạn**

### **KHỐI NGOẠI NGỮ (6 ngành)**
24. **Ngôn ngữ Nhật**
25. **Ngôn ngữ Hàn**
26. **Ngôn ngữ Trung Quốc**
27. **Sư phạm tiếng Anh**
28. **Ngôn ngữ Pháp**
29. **Biên - Phiên dịch tiếng Anh**

### **KHỐI CÔNG NGHỆ - KỸ THUẬT (8 ngành)**
30. **Công nghệ kỹ thuật điện tử - Truyền thông**
31. **Công nghệ thông tin (An toàn thông tin)**
32. **Kỹ thuật xây dựng**
33. **Kiến trúc**
34. **Công nghệ kỹ thuật cơ khí**
35. **Công nghệ kỹ thuật ô tô**
36. **Kỹ thuật điện**
37. **Thiết kế công nghiệp**

### **KHỐI XÃ HỘI - NHÂN VĂN (6 ngành)**
38. **Báo chí**
39. **Quan hệ công chúng (PR)**
40. **Truyền thông đa phương tiện**
41. **Công tác xã hội**
42. **Luật**
43. **Khoa học chính trị**

---

## 📄 **TEMPLATE BỔ SUNG (Copy vào `programs.json`):**

```json
{
  "id": "tai-chinh-ngan-hang",
  "name": "Tài chính - Ngân hàng",
  "aliases": ["Tài chính ngân hàng", "Banking", "Finance", "TCNH"],
  "description": "Ngành Tài chính - Ngân hàng đào tạo về quản lý tài chính, đầu tư, ngân hàng, chứng khoán",
  "duration": "4 năm",
  "degree": "Cử nhân",
  "faculty": "Khoa Kinh tế",
  "training_system": "Chính quy, Vừa làm vừa học",
  "career_opportunities": [
    "Chuyên viên tài chính ngân hàng",
    "Phân tích đầu tư",
    "Quản lý quỹ",
    "Chuyên viên tín dụng",
    "Chuyên viên môi giới chứng khoán"
  ],
  "subjects": [
    "Quản trị tài chính",
    "Ngân hàng thương mại",
    "Thị trường tài chính",
    "Phân tích đầu tư",
    "Quản trị rủi ro tài chính"
  ],
  "admission_requirements": {
    "combination": ["A00", "A01", "D01"],
    "min_score": 18.0
  }
}
```

---

## 🎯 **CÁCH BỔ SUNG:**

### **Bước 1:** Mở file `programs.json`

### **Bước 2:** Thêm ngành mới sau ngành "Thiết kế đồ họa" (dòng ~210)

### **Bước 3:** Copy template trên và thay đổi thông tin:
- `id`: tên không dấu, viết thường, dấu gạch ngang
- `name`: Tên chính thức của ngành
- `aliases`: Các tên gọi khác, viết tắt
- `description`: Mô tả ngắn gọn
- `faculty`: Khoa đào tạo (Kinh tế, Ngoại ngữ, Công nghệ...)
- `career_opportunities`: 5-7 nghề nghiệp
- `subjects`: 5-7 môn học chính
- `admission_requirements`: Tổ hợp xét tuyển

### **Bước 4:** Nhớ thêm dấu phẩy `,` giữa các ngành

---

## 💡 **LƯU Ý:**

1. **Kiểm tra syntax JSON** sau khi chỉnh sửa:
   ```bash
   python -m json.tool data/knowledge_base/programs.json
   ```

2. **Cập nhật tổng số ngành:**
   ```json
   "general_info": {
     "total_programs": 43
   }
   ```

3. **Thêm ngành vào Lookup Table:**
   - Mở `data/lookups/programs.txt`
   - Thêm tên ngành và aliases

4. **Train lại model sau khi cập nhật:**
   ```bash
   rasa train
   ```

---

## 📞 **Lấy thông tin chính xác:**

Truy cập: **https://vhu.edu.vn/tuyen-sinh/cac-nganh-dao-tao**

Hoặc liên hệ:
- **Phòng Đào tạo:** 028 7301 5555
- **Email:** daotao@vhu.edu.vn

---

## 📊 **SAU KHI BỔ SUNG:**

Chatbot sẽ trả lời được:
- "Thông tin ngành Tài chính ngân hàng"
- "Học phí ngành Kiến trúc"
- "Ngành Báo chí ra trường làm gì"
- "Điều kiện tuyển sinh ngành Luật"
- ... và 33 ngành khác!

🎉 **HOÀN THÀNH!**
