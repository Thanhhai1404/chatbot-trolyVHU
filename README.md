# Chatbot Trợ lý ảo Đại học Văn Hiến (VHU)

Chatbot trợ lý ảo tư vấn tuyển sinh và hỗ trợ sinh viên của Đại học Văn Hiến, được xây dựng bằng Rasa Framework.

## 📋 Tính năng

### ✅ Hoàn thành
- **30 intents** xử lý các câu hỏi phổ biến về:
  - Tuyển sinh và ngành học
  - Học phí và học bổng
  - Cơ sở vật chất và ký túc xá
  - Thông tin liên hệ và hỗ trợ
  
- **44 ngành đào tạo** với thông tin chi tiết:
  - Thông tin ngành học, tổ hợp môn
  - Học phí theo từng ngành
  - Cơ hội nghề nghiệp
  - Điều kiện tuyển sinh

- **7 Custom Actions** thông minh:
  - `action_program_info`: Tra cứu thông tin ngành học
  - `action_tuition_specific`: Tra cứu học phí chi tiết
  - `action_scholarship_condition`: Điều kiện học bổng
  - `action_campuses_info`: Thông tin cơ sở
  - `action_exam_schedule`: Lịch thi
  - `action_support_problem`: Hỗ trợ kỹ thuật
  - `action_default_fallback`: Xử lý câu hỏi ngoài phạm vi

- **Knowledge Base JSON**:
  - `programs.json`: 44 ngành đào tạo
  - `tuition.json`: Học phí chi tiết
  - `scholarships.json`: 4 loại học bổng
  - `campuses.json`: 2 cơ sở
  - `contacts.json`: Thông tin liên hệ

## 🏗️ Cấu trúc dự án

```
Chatbot/
├── data/
│   ├── nlu.yml                 # Training data (870+ dòng)
│   ├── rules.yml               # 32 rules
│   ├── stories.yml             # 34 stories
│   └── knowledge_base/         # Cơ sở dữ liệu JSON
│       ├── programs.json       # 44 ngành
│       ├── tuition.json        # Học phí
│       ├── scholarships.json   # Học bổng
│       ├── campuses.json       # Cơ sở
│       └── contacts.json       # Liên hệ
├── actions/
│   └── actions.py              # Custom actions (450+ dòng)
├── models/                     # Trained models
├── config.yml                  # Rasa configuration
├── domain.yml                  # Domain (340+ dòng)
├── credentials.yml             # API credentials
└── endpoints.yml               # Action server config
```

## 🚀 Cài đặt

### Yêu cầu
- Python 3.8+
- pip
- Git

### Các bước cài đặt

1. **Clone repository**
```bash
git clone https://github.com/Thanhhai1404/chatbot-trolyVHU.git
cd chatbot-trolyVHU
```

2. **Tạo virtual environment**
```bash
python -m venv rasa_env
# Windows
rasa_env\Scripts\activate
# Linux/Mac
source rasa_env/bin/activate
```

3. **Cài đặt dependencies**
```bash
pip install rasa
pip install rasa[full]
```

4. **Train model**
```bash
rasa train
```

## 🎯 Sử dụng

### Chạy chatbot trong terminal
```bash
rasa shell
```

### Chạy với Action Server (để sử dụng custom actions)
**Terminal 1 - Action Server:**
```bash
rasa run actions
```

**Terminal 2 - Rasa Shell:**
```bash
rasa shell
```

### Chạy test scripts
```bash
# Test intent classification
python test_intents.py

# Test full chatbot
python test_chatbot.py
```

## 📊 Thống kê dữ liệu

### Training Data (NLU)
- **Intents**: 30 (29 chính + 1 out_of_scope)
- **Training Examples**: 200+ câu
- **Entities**: 27 entities
- **Synonyms**: 15+ từ đồng nghĩa
- **Regex Patterns**: 4 patterns
- **Lookup Tables**: 5 files

### Ngành đào tạo (44 ngành)
- **Khối Kinh tế - Quản trị**: 7 ngành
- **Khối Tài chính - Kế toán**: 4 ngành
- **Khối Luật**: 2 ngành
- **Khối Công nghệ thông tin**: 3 ngành
- **Khối Công nghệ**: 5 ngành
- **Khối Y - Dược**: 2 ngành
- **Khối Ngôn ngữ - Văn hóa**: 8 ngành
- **Khối Quan hệ quốc tế**: 1 ngành
- **Khối Xã hội - Nhân văn**: 2 ngành
- **Khối Truyền thông**: 2 ngành
- **Khối Du lịch - Khách sạn**: 4 ngành
- **Khối Điện ảnh - Nghệ thuật**: 2 ngành
- **Khối Âm nhạc**: 2 ngành

### Học phí
- **Thấp nhất**: 7.0 - 7.2 triệu VNĐ/học kỳ (Văn học, Ngôn ngữ)
- **Trung bình**: 7.5 - 7.8 triệu VNĐ/học kỳ (Kinh tế, Quản trị, Luật)
- **Cao**: 8.0 - 8.5 triệu VNĐ/học kỳ (CNTT, Kỹ thuật, Y-Dược)
- **Cao nhất**: 9.0 triệu VNĐ/học kỳ (Âm nhạc)

## 📝 Ví dụ câu hỏi

```
User: Xin chào
Bot: Xin chào! Mình là trợ lý ảo của Đại học Văn Hiến...

User: Trường có những ngành nào?
Bot: Đại học Văn Hiến có 44 ngành đào tạo...

User: Học phí ngành CNTT là bao nhiêu?
Bot: Học phí ngành Công nghệ thông tin:
     - Học phí/học kỳ: 8,500,000 VNĐ
     - Học phí/năm: 17,000,000 VNĐ

User: Điều kiện học bổng khuyến khích học tập?
Bot: Học bổng Khuyến khích học tập:
     - Điểm GPA: Từ 3.0 trở lên...
```

## 🔧 Cấu hình

### Config.yml
- **Pipeline**: CountVectorsFeaturizer + DIETClassifier
- **Policies**: TEDPolicy + RulePolicy + FallbackPolicy
- **Language**: Vietnamese (vi)

### Tối ưu hóa
- DIETClassifier: 300 epochs, 3 transformer layers
- TEDPolicy: 150 epochs
- FallbackClassifier: threshold 0.6

## 📚 Tài liệu bổ sung

- `HUONG_DAN_BO_SUNG_NGANH.md`: Hướng dẫn bổ sung ngành mới
- `TONG_KET_TOI_UU_JSON.md`: Tổng kết tối ưu hóa JSON
- `TONG_KET_HOAN_THANH_44_NGANH.md`: Báo cáo hoàn thành

## 🤝 Đóng góp

Mọi đóng góp đều được chào đón! Hãy:
1. Fork repository
2. Tạo branch mới (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Tạo Pull Request

## 📞 Liên hệ

- **Tác giả**: Thanh Hai
- **GitHub**: [@Thanhhai1404](https://github.com/Thanhhai1404)
- **Trường**: Đại học Văn Hiến
- **Email**: tuyensinh@vhu.edu.vn
- **Hotline**: 1800 1568

## 📄 License

Dự án này được phát hành dưới MIT License.

## 🎓 Về Đại học Văn Hiến

**Đại học Văn Hiến** là một trong những trường đại học tư thục hàng đầu tại TP.HCM, với:
- 44 ngành đào tạo đa dạng
- 2 cơ sở hiện đại (Harmony Campus & MyU Campus)
- Đội ngũ giảng viên giàu kinh nghiệm
- Cơ sở vật chất đầy đủ

**Website**: http://vhu.edu.vn  
**Tuyển sinh**: http://ts.vhu.edu.vn

---

**⭐ Nếu dự án hữu ích, hãy cho một star nhé! ⭐**
