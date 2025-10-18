import json

# Tạo dữ liệu học phí
tuition_data = {
    "academic_year": "2024-2025",
    "currency": "VNĐ",
    "note": "Học phí theo học kỳ, 1 năm học có 2 học kỳ",
    "general_info": {
        "payment_deadline": "Trong vòng 2 tuần đầu của học kỳ",
        "late_payment_fee": "50,000 VNĐ/ngày trễ hạn",
        "bank_info": {
            "bank_name": "Ngân hàng TMCP Đầu tư và Phát triển Việt Nam (BIDV)",
            "branch": "Chi nhánh Tân Bình",
            "account_number": "12345678901",
            "account_name": "Trường Đại học Văn Hiến",
            "swift_code": "BIDVVNVX"
        },
        "discount_policy": [
            "Giảm 10% cho sinh viên đóng học phí cả năm học",
            "Giảm 5% cho anh chị em cùng học tại trường",
            "Miễn học phí cho sinh viên đạt học bổng toàn phần"
        ],
        "contact": {
            "department": "Phòng Tài chính",
            "phone": "028.3969.5555",
            "email": "taichinh@vhu.edu.vn",
            "office_hours": "Thứ 2 - Thứ 6: 7h30 - 16h30",
            "location": "Phòng A102 - Cơ sở 1 (Harmony Campus)"
        }
    },
    "programs": [
        {"id": "7340101", "name": "Quản trị kinh doanh", "tuition_per_term": "7,500,000", "annual_tuition": "15,000,000"},
        {"id": "7340115", "name": "Marketing", "tuition_per_term": "7,500,000", "annual_tuition": "15,000,000"},
        {"id": "7340121", "name": "Kinh doanh thương mại", "tuition_per_term": "7,500,000", "annual_tuition": "15,000,000"},
        {"id": "7340122", "name": "Thương mại điện tử", "tuition_per_term": "7,500,000", "annual_tuition": "15,000,000"},
        {"id": "7340404", "name": "Quản trị nhân lực", "tuition_per_term": "7,500,000", "annual_tuition": "15,000,000"},
        {"id": "7510605", "name": "Logistics và Quản lý chuỗi cung ứng", "tuition_per_term": "7,500,000", "annual_tuition": "15,000,000"},
        {"id": "7310101", "name": "Kinh doanh quốc tế", "tuition_per_term": "7,500,000", "annual_tuition": "15,000,000"},
        {"id": "7340201", "name": "Tài chính doanh nghiệp", "tuition_per_term": "7,500,000", "annual_tuition": "15,000,000"},
        {"id": "7340205", "name": "Công nghệ tài chính", "tuition_per_term": "7,800,000", "annual_tuition": "15,600,000"},
        {"id": "7340301", "name": "Kế toán", "tuition_per_term": "7,500,000", "annual_tuition": "15,000,000"},
        {"id": "7340302", "name": "Kiểm toán", "tuition_per_term": "7,500,000", "annual_tuition": "15,000,000"},
        {"id": "7380101", "name": "Luật", "tuition_per_term": "7,500,000", "annual_tuition": "15,000,000"},
        {"id": "7380107", "name": "Luật kinh tế", "tuition_per_term": "7,500,000", "annual_tuition": "15,000,000"},
        {"id": "7480101", "name": "Khoa học dữ liệu", "tuition_per_term": "8,500,000", "annual_tuition": "17,000,000"},
        {"id": "7480201", "name": "Công nghệ thông tin", "tuition_per_term": "8,500,000", "annual_tuition": "17,000,000"},
        {"id": "7480102", "name": "Mạng máy tính và Truyền thông", "tuition_per_term": "8,500,000", "annual_tuition": "17,000,000"},
        {"id": "7420201", "name": "Công nghệ sinh học", "tuition_per_term": "8,000,000", "annual_tuition": "16,000,000"},
        {"id": "7520207", "name": "Kỹ thuật Điện tử - Viễn thông", "tuition_per_term": "8,000,000", "annual_tuition": "16,000,000"},
        {"id": "7520320", "name": "Kỹ thuật môi trường", "tuition_per_term": "8,000,000", "annual_tuition": "16,000,000"},
        {"id": "7540101", "name": "Công nghệ thực phẩm", "tuition_per_term": "8,000,000", "annual_tuition": "16,000,000"},
        {"id": "7580201", "name": "Kỹ thuật xây dựng", "tuition_per_term": "8,000,000", "annual_tuition": "16,000,000"},
        {"id": "7720301", "name": "Điều dưỡng", "tuition_per_term": "8,200,000", "annual_tuition": "16,400,000"},
        {"id": "7720201", "name": "Dược học", "tuition_per_term": "8,500,000", "annual_tuition": "17,000,000"},
        {"id": "7220201", "name": "Ngôn ngữ Anh", "tuition_per_term": "7,200,000", "annual_tuition": "14,400,000"},
        {"id": "7220203", "name": "Ngôn ngữ Pháp", "tuition_per_term": "7,200,000", "annual_tuition": "14,400,000"},
        {"id": "7220204", "name": "Ngôn ngữ Trung Quốc", "tuition_per_term": "7,200,000", "annual_tuition": "14,400,000"},
        {"id": "7220209", "name": "Ngôn ngữ Nhật", "tuition_per_term": "7,200,000", "annual_tuition": "14,400,000"},
        {"id": "7310608", "name": "Đông phương học", "tuition_per_term": "7,200,000", "annual_tuition": "14,400,000"},
        {"id": "7310612", "name": "Trung Quốc học", "tuition_per_term": "7,200,000", "annual_tuition": "14,400,000"},
        {"id": "7229030", "name": "Văn học", "tuition_per_term": "7,000,000", "annual_tuition": "14,000,000"},
        {"id": "7310630", "name": "Việt Nam học", "tuition_per_term": "7,000,000", "annual_tuition": "14,000,000"},
        {"id": "7310206", "name": "Quan hệ quốc tế", "tuition_per_term": "7,500,000", "annual_tuition": "15,000,000"},
        {"id": "7310301", "name": "Xã hội học", "tuition_per_term": "7,200,000", "annual_tuition": "14,400,000"},
        {"id": "7310401", "name": "Tâm lý học", "tuition_per_term": "7,500,000", "annual_tuition": "15,000,000"},
        {"id": "7320108", "name": "Quan hệ công chúng", "tuition_per_term": "7,500,000", "annual_tuition": "15,000,000"},
        {"id": "7320104", "name": "Truyền thông đa phương tiện", "tuition_per_term": "8,000,000", "annual_tuition": "16,000,000"},
        {"id": "7810101", "name": "Quản trị du lịch", "tuition_per_term": "7,500,000", "annual_tuition": "15,000,000"},
        {"id": "7810103", "name": "Quản trị lữ hành", "tuition_per_term": "7,500,000", "annual_tuition": "15,000,000"},
        {"id": "7810201", "name": "Quản trị khách sạn", "tuition_per_term": "7,500,000", "annual_tuition": "15,000,000"},
        {"id": "7810202", "name": "Quản trị nhà hàng và dịch vụ ăn uống", "tuition_per_term": "7,500,000", "annual_tuition": "15,000,000"},
        {"id": "7210235", "name": "Đạo diễn điện ảnh, truyền hình", "tuition_per_term": "8,500,000", "annual_tuition": "17,000,000"},
        {"id": "7210302", "name": "Công nghệ điện ảnh, truyền hình", "tuition_per_term": "8,500,000", "annual_tuition": "17,000,000"},
        {"id": "7210205", "name": "Thanh nhạc", "tuition_per_term": "9,000,000", "annual_tuition": "18,000,000"},
        {"id": "7210208", "name": "Piano", "tuition_per_term": "9,000,000", "annual_tuition": "18,000,000"}
    ],
    "tuition_ranges": {
        "lowest": {"range": "7,000,000 - 7,200,000 VNĐ/học kỳ", "programs": ["Văn học", "Việt Nam học", "Ngôn ngữ"]},
        "medium": {"range": "7,500,000 - 7,800,000 VNĐ/học kỳ", "programs": ["Kinh tế", "Quản trị", "Tài chính", "Kế toán", "Luật", "Du lịch"]},
        "high": {"range": "8,000,000 - 8,500,000 VNĐ/học kỳ", "programs": ["CNTT", "Kỹ thuật", "Y-Dược", "Truyền thông", "Điện ảnh"]},
        "highest": {"range": "9,000,000 VNĐ/học kỳ", "programs": ["Âm nhạc (Thanh nhạc, Piano)"]}
    }
}

# Lưu file
with open("d:\\workspace\\Chatbot\\data\\knowledge_base\\tuition.json", 'w', encoding='utf-8') as f:
    json.dump(tuition_data, f, ensure_ascii=False, indent=2)

print("✓ Đã cập nhật tuition.json với 44 ngành!")
print(f"✓ Tổng số ngành: {len(tuition_data['programs'])}")
