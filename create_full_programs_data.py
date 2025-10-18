"""
Script tạo dữ liệu đầy đủ cho 43+ ngành đào tạo từ PDF đã trích xuất
Bổ sung thông tin chi tiết hơn cho từng ngành
"""
import json
import os

def create_comprehensive_programs_data():
    """Tạo dữ liệu đầy đủ cho tất cả các ngành"""
    
    programs = [
        # === KHỐI KINH TẾ - QUẢN TRỊ ===
        {
            "id": "7340101",
            "name": "Quản trị kinh doanh",
            "aliases": ["QTKD", "Business Administration", "Quản trị kinh doanh tổng hợp", "Quản trị dự án"],
            "full_name": "Cử nhân Quản trị kinh doanh",
            "degree": "Cử nhân",
            "duration": "4 năm",
            "faculty": "Khoa Kinh tế - Quản trị",
            "subject_combinations": ["A00", "A01", "C04", "D01"],
            "description": "Đào tạo các nhà quản trị có kiến thức toàn diện về kinh doanh, quản trị doanh nghiệp và quản trị dự án.",
            "career_opportunities": [
                "Chuyên viên quản trị doanh nghiệp",
                "Quản lý dự án",
                "Giám đốc điều hành",
                "Chuyên viên phát triển kinh doanh"
            ],
            "tuition_per_term": "7,500,000"
        },
        {
            "id": "7340115",
            "name": "Marketing",
            "aliases": ["MKT", "Marketing truyền thông", "Quản trị Marketing", "Digital Marketing"],
            "full_name": "Cử nhân Marketing",
            "degree": "Cử nhân",
            "duration": "4 năm",
            "faculty": "Khoa Kinh tế - Quản trị",
            "subject_combinations": ["A00", "A01", "C04", "D01"],
            "description": "Đào tạo chuyên gia Marketing đa năng với các chuyên ngành: Marketing truyền thông, Quản trị Marketing, Digital Marketing.",
            "career_opportunities": [
                "Chuyên viên Marketing",
                "Digital Marketing Manager",
                "Brand Manager",
                "Content Marketing Specialist"
            ],
            "tuition_per_term": "7,500,000"
        },
        {
            "id": "7340121",
            "name": "Kinh doanh thương mại",
            "aliases": ["KDTM", "Trade", "Thương mại"],
            "full_name": "Cử nhân Kinh doanh thương mại",
            "degree": "Cử nhân",
            "duration": "4 năm",
            "faculty": "Khoa Kinh tế - Quản trị",
            "subject_combinations": ["A00", "A01", "C04", "D01"],
            "description": "Đào tạo chuyên gia kinh doanh thương mại trong nước và quốc tế.",
            "career_opportunities": [
                "Chuyên viên kinh doanh",
                "Quản lý chuỗi cung ứng",
                "Chuyên viên xuất nhập khẩu",
                "Giám đốc kinh doanh"
            ],
            "tuition_per_term": "7,500,000"
        },
        {
            "id": "7340122",
            "name": "Thương mại điện tử",
            "aliases": ["TMĐT", "E-commerce", "E-Commerce"],
            "full_name": "Cử nhân Thương mại điện tử",
            "degree": "Cử nhân",
            "duration": "4 năm",
            "faculty": "Khoa Kinh tế - Quản trị",
            "subject_combinations": ["A00", "A01", "C04", "D01"],
            "description": "Đào tạo chuyên gia về kinh doanh trên nền tảng số, quản lý website thương mại điện tử.",
            "career_opportunities": [
                "E-commerce Manager",
                "Online Business Developer",
                "Digital Sales Specialist",
                "Marketplace Manager"
            ],
            "tuition_per_term": "7,500,000"
        },
        {
            "id": "7340404",
            "name": "Quản trị nhân lực",
            "aliases": ["QTNL", "HR", "Human Resources", "HRM"],
            "full_name": "Cử nhân Quản trị nhân lực",
            "degree": "Cử nhân",
            "duration": "4 năm",
            "faculty": "Khoa Kinh tế - Quản trị",
            "subject_combinations": ["A00", "A01", "C04", "D01"],
            "description": "Đào tạo chuyên gia quản trị nguồn nhân lực, phát triển tổ chức.",
            "career_opportunities": [
                "HR Manager",
                "Recruitment Specialist",
                "Training & Development Manager",
                "Compensation & Benefits Manager"
            ],
            "tuition_per_term": "7,500,000"
        },
        {
            "id": "7510605",
            "name": "Logistics và Quản lý chuỗi cung ứng",
            "aliases": ["Logistics", "SCM", "Supply Chain", "QLCCUƯ"],
            "full_name": "Cử nhân Logistics và Quản lý chuỗi cung ứng",
            "degree": "Cử nhân",
            "duration": "4 năm",
            "faculty": "Khoa Kinh tế - Quản trị",
            "subject_combinations": ["A00", "A01", "C04", "D01"],
            "description": "Đào tạo chuyên gia logistics và quản lý chuỗi cung ứng cho các doanh nghiệp.",
            "career_opportunities": [
                "Logistics Manager",
                "Supply Chain Coordinator",
                "Warehouse Manager",
                "Import-Export Specialist"
            ],
            "tuition_per_term": "7,500,000"
        },
        {
            "id": "7310101",
            "name": "Kinh doanh quốc tế",
            "aliases": ["KDQT", "International Business", "Kinh tế", "Kinh tế số"],
            "full_name": "Cử nhân Kinh doanh quốc tế",
            "degree": "Cử nhân",
            "duration": "4 năm",
            "faculty": "Khoa Kinh tế - Quản trị",
            "subject_combinations": ["A00", "A01", "C04", "D01"],
            "description": "Đào tạo chuyên gia kinh doanh quốc tế và kinh tế số trong môi trường toàn cầu hóa.",
            "career_opportunities": [
                "Chuyên viên kinh doanh quốc tế",
                "Chuyên viên xuất nhập khẩu",
                "Chuyên viên phát triển thị trường quốc tế",
                "Quản lý dự án quốc tế"
            ],
            "tuition_per_term": "7,500,000"
        },
        
        # === KHỐI TÀI CHÍNH - KẾ TOÁN ===
        {
            "id": "7340201",
            "name": "Tài chính doanh nghiệp",
            "aliases": ["TCDN", "Corporate Finance", "Tài chính ngân hàng", "Tài chính - Ngân hàng"],
            "full_name": "Cử nhân Tài chính doanh nghiệp",
            "degree": "Cử nhân",
            "duration": "4 năm",
            "faculty": "Khoa Tài chính - Kế toán",
            "subject_combinations": ["A00", "A01", "C04", "D01"],
            "description": "Đào tạo chuyên gia tài chính doanh nghiệp và ngân hàng với kiến thức chuyên sâu.",
            "career_opportunities": [
                "Chuyên viên tài chính",
                "Phân tích tài chính",
                "Quản lý quỹ đầu tư",
                "Chuyên viên ngân hàng"
            ],
            "tuition_per_term": "7,500,000"
        },
        {
            "id": "7340205",
            "name": "Công nghệ tài chính",
            "aliases": ["Fintech", "FinTech", "Ngân hàng số", "Digital Banking"],
            "full_name": "Cử nhân Công nghệ tài chính",
            "degree": "Cử nhân",
            "duration": "4 năm",
            "faculty": "Khoa Tài chính - Kế toán",
            "subject_combinations": ["A00", "A01", "C04", "D01"],
            "description": "Đào tạo chuyên gia về công nghệ tài chính, ngân hàng số và các giải pháp thanh toán điện tử.",
            "career_opportunities": [
                "Fintech Developer",
                "Digital Banking Specialist",
                "Payment Solutions Manager",
                "Blockchain Analyst"
            ],
            "tuition_per_term": "7,800,000"
        },
        {
            "id": "7340301",
            "name": "Kế toán",
            "aliases": ["KT", "Accounting", "Kế toán doanh nghiệp"],
            "full_name": "Cử nhân Kế toán",
            "degree": "Cử nhân",
            "duration": "4 năm",
            "faculty": "Khoa Tài chính - Kế toán",
            "subject_combinations": ["A00", "A01", "C04", "D01"],
            "description": "Đào tạo kế toán viên chuyên nghiệp phục vụ các doanh nghiệp và tổ chức.",
            "career_opportunities": [
                "Kế toán trưởng",
                "Kế toán tổng hợp",
                "Kế toán quản trị",
                "Chuyên viên kiểm soát chi phí"
            ],
            "tuition_per_term": "7,500,000"
        },
        {
            "id": "7340302",
            "name": "Kiểm toán",
            "aliases": ["Auditing", "Audit", "Kiểm toán nội bộ"],
            "full_name": "Cử nhân Kiểm toán",
            "degree": "Cử nhân",
            "duration": "4 năm",
            "faculty": "Khoa Tài chính - Kế toán",
            "subject_combinations": ["A00", "A01", "C02", "D01"],
            "description": "Đào tạo kiểm toán viên chuyên nghiệp cho các công ty kiểm toán và doanh nghiệp.",
            "career_opportunities": [
                "Kiểm toán viên",
                "Kiểm toán nội bộ",
                "Tư vấn kiểm toán",
                "Giám đốc kiểm soát nội bộ"
            ],
            "tuition_per_term": "7,500,000"
        },
        
        # === KHỐI LUẬT ===
        {
            "id": "7380101",
            "name": "Luật",
            "aliases": ["Law", "Luật dân sự", "Luật thương mại quốc tế", "Luật tài chính ngân hàng"],
            "full_name": "Cử nhân Luật",
            "degree": "Cử nhân",
            "duration": "4 năm",
            "faculty": "Khoa Luật",
            "subject_combinations": ["A00", "A01", "C04", "D01"],
            "description": "Đào tạo luật sư với các chuyên ngành: Luật dân sự, Luật thương mại quốc tế, Luật tài chính ngân hàng.",
            "career_opportunities": [
                "Luật sư",
                "Chuyên viên pháp lý",
                "Trợ lý pháp lý doanh nghiệp",
                "Tư vấn luật"
            ],
            "tuition_per_term": "7,500,000"
        },
        {
            "id": "7380107",
            "name": "Luật kinh tế",
            "aliases": ["Economic Law", "Luật KT"],
            "full_name": "Cử nhân Luật kinh tế",
            "degree": "Cử nhân",
            "duration": "4 năm",
            "faculty": "Khoa Luật",
            "subject_combinations": ["A00", "A01", "C04", "D01"],
            "description": "Đào tạo chuyên gia luật kinh tế phục vụ các doanh nghiệp và tổ chức.",
            "career_opportunities": [
                "Chuyên viên luật kinh tế",
                "Tư vấn pháp lý doanh nghiệp",
                "Chuyên viên hợp đồng thương mại",
                "Luật sư doanh nghiệp"
            ],
            "tuition_per_term": "7,500,000"
        },
        
        # === KHỐI CÔNG NGHỆ - KỸ THUẬT ===
        {
            "id": "7480101",
            "name": "Khoa học dữ liệu",
            "aliases": ["Data Science", "KHĐL", "Hệ thống thông tin", "Khoa học máy tính"],
            "full_name": "Cử nhân Khoa học dữ liệu",
            "degree": "Cử nhân",
            "duration": "4 năm",
            "faculty": "Khoa Công nghệ thông tin",
            "subject_combinations": ["A00", "A01", "K01", "D01"],
            "description": "Đào tạo chuyên gia khoa học dữ liệu, hệ thống thông tin và phân tích dữ liệu lớn.",
            "career_opportunities": [
                "Data Scientist",
                "Data Analyst",
                "Business Intelligence Analyst",
                "Machine Learning Engineer"
            ],
            "tuition_per_term": "8,500,000"
        },
        {
            "id": "7480201",
            "name": "Công nghệ thông tin",
            "aliases": ["CNTT", "IT", "Information Technology", "Thiết kế đồ họa", "Công nghệ phần mềm"],
            "full_name": "Cử nhân Công nghệ thông tin",
            "degree": "Cử nhân",
            "duration": "4 năm",
            "faculty": "Khoa Công nghệ thông tin",
            "subject_combinations": ["A00", "A01", "K01", "D01"],
            "description": "Đào tạo kỹ sư CNTT với các chuyên ngành: Thiết kế đồ họa/game/Multimedia, Công nghệ phần mềm.",
            "career_opportunities": [
                "Lập trình viên",
                "Graphic Designer",
                "Game Developer",
                "Software Engineer"
            ],
            "tuition_per_term": "8,500,000"
        },
        {
            "id": "7480102",
            "name": "Mạng máy tính và Truyền thông",
            "aliases": ["Network", "MMTT", "An toàn thông tin", "Information Security"],
            "full_name": "Cử nhân Mạng máy tính và Truyền thông",
            "degree": "Cử nhân",
            "duration": "4 năm",
            "faculty": "Khoa Công nghệ thông tin",
            "subject_combinations": ["A00", "A01", "K01", "D01"],
            "description": "Đào tạo chuyên gia về mạng máy tính và an toàn thông tin.",
            "career_opportunities": [
                "Network Administrator",
                "Security Engineer",
                "System Administrator",
                "Network Security Specialist"
            ],
            "tuition_per_term": "8,500,000"
        },
        {
            "id": "7420201",
            "name": "Công nghệ sinh học",
            "aliases": ["Biotechnology", "CNSH", "Công nghệ sinh học y sinh", "Công nghệ sinh học nông nghiệp"],
            "full_name": "Cử nhân Công nghệ sinh học",
            "degree": "Cử nhân",
            "duration": "4 năm",
            "faculty": "Khoa Công nghệ",
            "subject_combinations": ["A00", "A02", "B00", "D07"],
            "description": "Đào tạo chuyên gia công nghệ sinh học y sinh và nông nghiệp.",
            "career_opportunities": [
                "Chuyên viên công nghệ sinh học",
                "Nghiên cứu viên sinh học",
                "Chuyên viên kiểm nghiệm",
                "Quản lý phòng thí nghiệm"
            ],
            "tuition_per_term": "8,000,000"
        },
        {
            "id": "7520207",
            "name": "Kỹ thuật Điện tử - Viễn thông",
            "aliases": ["Electronics", "KTĐT-VT", "Hệ thống nhúng và IoT", "Thiết kế vi mạch"],
            "full_name": "Cử nhân Kỹ thuật Điện tử - Viễn thông",
            "degree": "Cử nhân",
            "duration": "4 năm",
            "faculty": "Khoa Công nghệ",
            "subject_combinations": ["A00", "A01", "C01", "D01"],
            "description": "Đào tạo kỹ sư điện tử viễn thông, hệ thống nhúng và IoT.",
            "career_opportunities": [
                "Kỹ sư điện tử",
                "Kỹ sư viễn thông",
                "IoT Developer",
                "Embedded Systems Engineer"
            ],
            "tuition_per_term": "8,000,000"
        },
        {
            "id": "7520320",
            "name": "Kỹ thuật môi trường",
            "aliases": ["KTMT", "Environmental Engineering", "Môi trường"],
            "full_name": "Cử nhân Kỹ thuật môi trường",
            "degree": "Cử nhân",
            "duration": "4 năm",
            "faculty": "Khoa Công nghệ",
            "subject_combinations": ["A00", "A02", "B00", "D07"],
            "description": "Đào tạo kỹ sư môi trường phục vụ công tác bảo vệ môi trường.",
            "career_opportunities": [
                "Kỹ sư môi trường",
                "Chuyên viên xử lý nước thải",
                "Chuyên viên đánh giá tác động môi trường",
                "Quản lý môi trường doanh nghiệp"
            ],
            "tuition_per_term": "8,000,000"
        },
        {
            "id": "7540101",
            "name": "Công nghệ thực phẩm",
            "aliases": ["CNTP", "Food Technology", "Công nghệ chế biến thực phẩm"],
            "full_name": "Cử nhân Công nghệ thực phẩm",
            "degree": "Cử nhân",
            "duration": "4 năm",
            "faculty": "Khoa Công nghệ",
            "subject_combinations": ["A00", "A02", "B00", "D07"],
            "description": "Đào tạo kỹ sư công nghệ thực phẩm và chế biến thực phẩm.",
            "career_opportunities": [
                "Kỹ sư công nghệ thực phẩm",
                "Chuyên viên kiểm nghiệm thực phẩm",
                "Quản lý sản xuất thực phẩm",
                "Nghiên cứu và phát triển sản phẩm"
            ],
            "tuition_per_term": "8,000,000"
        },
        {
            "id": "7580201",
            "name": "Kỹ thuật xây dựng",
            "aliases": ["KTXD", "Civil Engineering", "Xây dựng"],
            "full_name": "Cử nhân Kỹ thuật xây dựng",
            "degree": "Cử nhân",
            "duration": "4 năm",
            "faculty": "Khoa Công nghệ",
            "subject_combinations": ["A00", "A01", "C01", "D07"],
            "description": "Đào tạo kỹ sư xây dựng dân dụng và công nghiệp.",
            "career_opportunities": [
                "Kỹ sư xây dựng",
                "Giám sát thi công",
                "Thiết kế kết cấu công trình",
                "Quản lý dự án xây dựng"
            ],
            "tuition_per_term": "8,000,000"
        },
        
        # === KHỐI Y - DƯỢC ===
        {
            "id": "7720301",
            "name": "Điều dưỡng",
            "aliases": ["Nursing", "Điều dưỡng đa khoa"],
            "full_name": "Cử nhân Điều dưỡng",
            "degree": "Cử nhân",
            "duration": "4 năm",
            "faculty": "Khoa Y - Dược",
            "subject_combinations": ["B03", "C02", "D01", "D07"],
            "description": "Đào tạo điều dưỡng viên chuyên nghiệp phục vụ ngành y tế.",
            "career_opportunities": [
                "Điều dưỡng viên",
                "Điều dưỡng trưởng",
                "Chuyên viên chăm sóc sức khỏe",
                "Quản lý điều dưỡng"
            ],
            "tuition_per_term": "8,200,000"
        },
        {
            "id": "7720201",
            "name": "Dược học",
            "aliases": ["Pharmacy", "Dược sĩ"],
            "full_name": "Cử nhân Dược học",
            "degree": "Cử nhân",
            "duration": "4 năm",
            "faculty": "Khoa Y - Dược",
            "subject_combinations": ["B03", "C02", "D01", "D07"],
            "description": "Đào tạo dược sĩ chuyên nghiệp cho các nhà thuốc và bệnh viện.",
            "career_opportunities": [
                "Dược sĩ",
                "Chuyên viên quản lý dược",
                "Dược sĩ lâm sàng",
                "Trưởng phòng dược"
            ],
            "tuition_per_term": "8,500,000"
        },
        
        # === KHỐI NGÔN NGỮ - SƯ PHẠM ===
        {
            "id": "7220201",
            "name": "Ngôn ngữ Anh",
            "aliases": ["English", "Tiếng Anh", "Tiếng Anh thương mại", "TESOL", "Tiếng Anh biên - phiên dịch", "Tiếng Anh quan hệ quốc tế"],
            "full_name": "Cử nhân Ngôn ngữ Anh",
            "degree": "Cử nhân",
            "duration": "4 năm",
            "faculty": "Khoa Ngôn ngữ - Văn hóa",
            "subject_combinations": ["A01", "D01", "D10", "D15"],
            "description": "Đào tạo chuyên gia tiếng Anh với các chuyên ngành: Thương mại, Phương pháp dạy học, Biên phiên dịch, Quan hệ quốc tế.",
            "career_opportunities": [
                "Giảng viên tiếng Anh",
                "Phiên dịch viên",
                "Chuyên viên giao tiếp doanh nghiệp",
                "Biên dịch viên"
            ],
            "tuition_per_term": "7,200,000"
        },
        {
            "id": "7220203",
            "name": "Ngôn ngữ Pháp",
            "aliases": ["French", "Tiếng Pháp", "Tiếng Pháp thương mại"],
            "full_name": "Cử nhân Ngôn ngữ Pháp",
            "degree": "Cử nhân",
            "duration": "4 năm",
            "faculty": "Khoa Ngôn ngữ - Văn hóa",
            "subject_combinations": ["A01", "D01", "D10", "D15"],
            "description": "Đào tạo chuyên gia tiếng Pháp thương mại.",
            "career_opportunities": [
                "Giảng viên tiếng Pháp",
                "Phiên dịch viên tiếng Pháp",
                "Chuyên viên giao tiếp quốc tế",
                "Hướng dẫn viên du lịch tiếng Pháp"
            ],
            "tuition_per_term": "7,200,000"
        },
        {
            "id": "7220204",
            "name": "Ngôn ngữ Trung Quốc",
            "aliases": ["Chinese", "Tiếng Trung", "Tiếng Trung thương mại", "Tiếng Trung biên - phiên dịch"],
            "full_name": "Cử nhân Ngôn ngữ Trung Quốc",
            "degree": "Cử nhân",
            "duration": "4 năm",
            "faculty": "Khoa Ngôn ngữ - Văn hóa",
            "subject_combinations": ["A01", "D01", "D10", "D15"],
            "description": "Đào tạo chuyên gia tiếng Trung với chuyên ngành thương mại và biên phiên dịch. Liên kết quốc tế với Trung Quốc.",
            "career_opportunities": [
                "Phiên dịch viên tiếng Trung",
                "Chuyên viên xuất nhập khẩu Trung Quốc",
                "Giảng viên tiếng Trung",
                "Chuyên viên quan hệ thương mại"
            ],
            "tuition_per_term": "7,200,000"
        },
        {
            "id": "7220209",
            "name": "Ngôn ngữ Nhật",
            "aliases": ["Japanese", "Tiếng Nhật", "Tiếng Nhật thương mại", "Tiếng Nhật giảng dạy", "Tiếng Nhật biên – phiên dịch"],
            "full_name": "Cử nhân Ngôn ngữ Nhật",
            "degree": "Cử nhân",
            "duration": "4 năm",
            "faculty": "Khoa Ngôn ngữ - Văn hóa",
            "subject_combinations": ["A01", "D01", "D10", "D15"],
            "description": "Đào tạo chuyên gia tiếng Nhật với các chuyên ngành: Thương mại, Giảng dạy, Biên phiên dịch.",
            "career_opportunities": [
                "Phiên dịch viên tiếng Nhật",
                "Giảng viên tiếng Nhật",
                "Chuyên viên doanh nghiệp Nhật",
                "Biên dịch viên"
            ],
            "tuition_per_term": "7,200,000"
        },
        
        # === KHỐI QUAN HỆ QUỐC TẾ - NGHIÊN CỨU VĂN HÓA ===
        {
            "id": "7310206",
            "name": "Quan hệ quốc tế",
            "aliases": ["International Relations", "HTQT", "Đối ngoại – Hợp tác quốc tế", "Truyền thông quốc tế"],
            "full_name": "Cử nhân Quan hệ quốc tế",
            "degree": "Cử nhân",
            "duration": "4 năm",
            "faculty": "Khoa Quan hệ quốc tế",
            "subject_combinations": ["A01", "D01", "D14", "D15"],
            "description": "Đào tạo chuyên gia quan hệ quốc tế và hợp tác quốc tế.",
            "career_opportunities": [
                "Chuyên viên quan hệ quốc tế",
                "Chuyên viên đối ngoại",
                "Chuyên viên tổ chức quốc tế",
                "Chuyên viên hợp tác quốc tế"
            ],
            "tuition_per_term": "7,500,000"
        },
        {
            "id": "7310608",
            "name": "Đông phương học",
            "aliases": ["Oriental Studies", "Nhật Bản học", "Hàn Quốc học"],
            "full_name": "Cử nhân Đông phương học",
            "degree": "Cử nhân",
            "duration": "4 năm",
            "faculty": "Khoa Ngôn ngữ - Văn hóa",
            "subject_combinations": ["A01", "D01", "C00", "D15"],
            "description": "Đào tạo chuyên gia về văn hóa, lịch sử và xã hội Đông Á (Nhật Bản, Hàn Quốc).",
            "career_opportunities": [
                "Nghiên cứu viên văn hóa Đông Á",
                "Chuyên viên quan hệ văn hóa quốc tế",
                "Hướng dẫn viên du lịch",
                "Chuyên viên tổ chức sự kiện văn hóa"
            ],
            "tuition_per_term": "7,200,000"
        },
        {
            "id": "7310612",
            "name": "Trung Quốc học",
            "aliases": ["Chinese Studies", "Trung Hoa học"],
            "full_name": "Cử nhân Trung Quốc học",
            "degree": "Cử nhân",
            "duration": "4 năm",
            "faculty": "Khoa Ngôn ngữ - Văn hóa",
            "subject_combinations": ["A01", "D01", "D10", "D15"],
            "description": "Đào tạo chuyên gia về văn hóa, lịch sử và xã hội Trung Quốc.",
            "career_opportunities": [
                "Nghiên cứu viên văn hóa Trung Quốc",
                "Chuyên viên quan hệ văn hóa",
                "Chuyên viên thương mại Trung Quốc",
                "Hướng dẫn viên du lịch"
            ],
            "tuition_per_term": "7,200,000"
        },
        {
            "id": "7229030",
            "name": "Văn học",
            "aliases": ["Literature", "Văn – Quản trị văn phòng", "Giảng dạy văn học", "Văn – Truyền thông"],
            "full_name": "Cử nhân Văn học",
            "degree": "Cử nhân",
            "duration": "4 năm",
            "faculty": "Khoa Ngôn ngữ - Văn hóa",
            "subject_combinations": ["C00", "D01", "D14", "D15"],
            "description": "Đào tạo chuyên gia văn học với các chuyên ngành: Quản trị văn phòng, Giảng dạy, Truyền thông.",
            "career_opportunities": [
                "Giảng viên văn học",
                "Biên tập viên",
                "Chuyên viên quản trị văn phòng",
                "Nhà báo văn hóa"
            ],
            "tuition_per_term": "7,000,000"
        },
        {
            "id": "7310630",
            "name": "Việt Nam học",
            "aliases": ["Vietnamese Studies"],
            "full_name": "Cử nhân Việt Nam học",
            "degree": "Cử nhân",
            "duration": "4 năm",
            "faculty": "Khoa Ngôn ngữ - Văn hóa",
            "subject_combinations": ["C00", "D01", "D14", "D15"],
            "description": "Đào tạo chuyên gia về văn hóa, lịch sử và xã hội Việt Nam.",
            "career_opportunities": [
                "Nghiên cứu viên Việt Nam học",
                "Giảng viên văn hóa Việt Nam",
                "Chuyên viên bảo tồn di sản",
                "Hướng dẫn viên du lịch văn hóa"
            ],
            "tuition_per_term": "7,000,000"
        },
        
        # === KHỐI XÃ HỘI HỌC - TÂM LÝ ===
        {
            "id": "7310301",
            "name": "Xã hội học",
            "aliases": ["Sociology", "XHTT", "Xã hội học truyền thông đại chúng", "Xã hội học quản trị nhân sự và tổ chức xã hội"],
            "full_name": "Cử nhân Xã hội học",
            "degree": "Cử nhân",
            "duration": "4 năm",
            "faculty": "Khoa Xã hội - Nhân văn",
            "subject_combinations": ["A00", "C00", "C04", "D01"],
            "description": "Đào tạo chuyên gia xã hội học với chuyên ngành truyền thông đại chúng và quản trị nhân sự.",
            "career_opportunities": [
                "Chuyên viên nghiên cứu xã hội",
                "Chuyên viên truyền thông xã hội",
                "Chuyên viên phát triển cộng đồng",
                "Chuyên viên quản trị nhân sự"
            ],
            "tuition_per_term": "7,200,000"
        },
        {
            "id": "7310401",
            "name": "Tâm lý học",
            "aliases": ["Psychology", "Tham vấn và trị liệu tâm lý", "Tham vấn tâm lý và quản trị nhân sự"],
            "full_name": "Cử nhân Tâm lý học",
            "degree": "Cử nhân",
            "duration": "4 năm",
            "faculty": "Khoa Xã hội - Nhân văn",
            "subject_combinations": ["A00", "D08", "D13", "B03"],
            "description": "Đào tạo chuyên gia tâm lý với chuyên ngành tham vấn, trị liệu và quản trị nhân sự.",
            "career_opportunities": [
                "Tâm lý trị liệu",
                "Tư vấn tâm lý",
                "Chuyên viên phát triển nhân sự",
                "Tâm lý giáo dục"
            ],
            "tuition_per_term": "7,500,000"
        },
        
        # === KHỐI TRUYỀN THÔNG ===
        {
            "id": "7320108",
            "name": "Quan hệ công chúng",
            "aliases": ["PR", "Public Relations", "Truyền thông và sáng tạo nội dung", "Tổ chức sự kiện"],
            "full_name": "Cử nhân Quan hệ công chúng",
            "degree": "Cử nhân",
            "duration": "4 năm",
            "faculty": "Khoa Truyền thông",
            "subject_combinations": ["C00", "D01", "D14", "D15"],
            "description": "Đào tạo chuyên gia PR, truyền thông và sáng tạo nội dung, tổ chức sự kiện.",
            "career_opportunities": [
                "PR Manager",
                "Event Manager",
                "Content Creator",
                "Communications Specialist"
            ],
            "tuition_per_term": "7,500,000"
        },
        {
            "id": "7320104",
            "name": "Truyền thông đa phương tiện",
            "aliases": ["Multimedia", "Sản xuất phim và quảng cáo", "Công nghệ truyền thông"],
            "full_name": "Cử nhân Truyền thông đa phương tiện",
            "degree": "Cử nhân",
            "duration": "4 năm",
            "faculty": "Khoa Truyền thông",
            "subject_combinations": ["A00", "A01", "C01", "D01"],
            "description": "Đào tạo chuyên gia sản xuất phim, quảng cáo và công nghệ truyền thông.",
            "career_opportunities": [
                "Film Producer",
                "Video Editor",
                "Creative Director",
                "Advertising Specialist"
            ],
            "tuition_per_term": "8,000,000"
        },
        
        # === KHỐI DU LỊCH - KHÁCH SẠN ===
        {
            "id": "7810101",
            "name": "Quản trị du lịch",
            "aliases": ["Tourism Management", "QTDL", "Quản trị sự kiện", "Du lịch"],
            "full_name": "Cử nhân Quản trị du lịch",
            "degree": "Cử nhân",
            "duration": "4 năm",
            "faculty": "Khoa Du lịch - Khách sạn",
            "subject_combinations": ["A00", "C00", "C04", "D01"],
            "description": "Đào tạo chuyên gia quản trị du lịch và tổ chức sự kiện du lịch.",
            "career_opportunities": [
                "Quản lý điểm đến du lịch",
                "Quản lý công ty lữ hành",
                "Event Planner",
                "Chuyên viên phát triển du lịch"
            ],
            "tuition_per_term": "7,500,000"
        },
        {
            "id": "7810103",
            "name": "Quản trị lữ hành",
            "aliases": ["Travel Management", "Hướng dẫn du lịch", "Tour Guide"],
            "full_name": "Cử nhân Quản trị lữ hành",
            "degree": "Cử nhân",
            "duration": "4 năm",
            "faculty": "Khoa Du lịch - Khách sạn",
            "subject_combinations": ["A00", "C00", "C04", "D01"],
            "description": "Đào tạo chuyên gia quản trị lữ hành và hướng dẫn viên du lịch chuyên nghiệp.",
            "career_opportunities": [
                "Tour Manager",
                "Hướng dẫn viên du lịch",
                "Tour Operator",
                "Travel Consultant"
            ],
            "tuition_per_term": "7,500,000"
        },
        {
            "id": "7810201",
            "name": "Quản trị khách sạn",
            "aliases": ["Hotel Management", "QTKS", "Quản trị khách sạn - Khu du lịch"],
            "full_name": "Cử nhân Quản trị khách sạn",
            "degree": "Cử nhân",
            "duration": "4 năm",
            "faculty": "Khoa Du lịch - Khách sạn",
            "subject_combinations": ["A00", "C00", "D01", "C04"],
            "description": "Đào tạo chuyên gia quản trị khách sạn và khu du lịch.",
            "career_opportunities": [
                "Hotel Manager",
                "Resort Manager",
                "Front Office Manager",
                "F&B Manager"
            ],
            "tuition_per_term": "7,500,000"
        },
        {
            "id": "7810202",
            "name": "Quản trị nhà hàng và dịch vụ ăn uống",
            "aliases": ["Restaurant Management", "F&B Management"],
            "full_name": "Cử nhân Quản trị nhà hàng và dịch vụ ăn uống",
            "degree": "Cử nhân",
            "duration": "4 năm",
            "faculty": "Khoa Du lịch - Khách sạn",
            "subject_combinations": ["A00", "C00", "D01", "C04"],
            "description": "Đào tạo chuyên gia quản trị nhà hàng và dịch vụ ăn uống.",
            "career_opportunities": [
                "Restaurant Manager",
                "F&B Director",
                "Catering Manager",
                "Service Manager"
            ],
            "tuition_per_term": "7,500,000"
        },
        
        # === KHỐI ĐIỆN ẢNH - NGHỆ THUẬT ===
        {
            "id": "7210235",
            "name": "Đạo diễn điện ảnh, truyền hình",
            "aliases": ["Film Director", "TV Director", "Quay phim"],
            "full_name": "Cử nhân Đạo diễn điện ảnh, truyền hình",
            "degree": "Cử nhân",
            "duration": "4 năm",
            "faculty": "Khoa Điện ảnh - Nghệ thuật",
            "subject_combinations": ["A00", "D01", "M20", "M21"],
            "description": "Đào tạo đạo diễn điện ảnh và truyền hình, kỹ thuật viên quay phim chuyên nghiệp.",
            "career_opportunities": [
                "Đạo diễn phim",
                "Đạo diễn truyền hình",
                "Cameraman",
                "Film Producer"
            ],
            "tuition_per_term": "8,500,000"
        },
        {
            "id": "7210302",
            "name": "Công nghệ điện ảnh, truyền hình",
            "aliases": ["Film Technology", "Dựng phim", "Film Editing", "Thiết kế mỹ thuật điện ảnh", "Công nghệ hoạt hình"],
            "full_name": "Cử nhân Công nghệ điện ảnh, truyền hình",
            "degree": "Cử nhân",
            "duration": "4 năm",
            "faculty": "Khoa Điện ảnh - Nghệ thuật",
            "subject_combinations": ["A00", "D01", "V00", "H01"],
            "description": "Đào tạo chuyên gia dựng phim, thiết kế mỹ thuật điện ảnh, công nghệ hoạt hình.",
            "career_opportunities": [
                "Film Editor",
                "Visual Effects Artist",
                "Animation Designer",
                "Art Director"
            ],
            "tuition_per_term": "8,500,000"
        },
        {
            "id": "7210205",
            "name": "Thanh nhạc",
            "aliases": ["Vocal Music", "Thanh nhạc thính phòng", "Thanh nhạc nhạc nhẹ"],
            "full_name": "Cử nhân Thanh nhạc",
            "degree": "Cử nhân",
            "duration": "4 năm",
            "faculty": "Khoa Âm nhạc",
            "subject_combinations": ["N00"],
            "description": "Đào tạo ca sĩ chuyên nghiệp với chuyên ngành thanh nhạc thính phòng và nhạc nhẹ. Xét tuyển kết hợp thi năng khiếu.",
            "career_opportunities": [
                "Ca sĩ chuyên nghiệp",
                "Giảng viên thanh nhạc",
                "Nghệ sĩ biểu diễn",
                "Chuyên viên đào tạo giọng hát"
            ],
            "tuition_per_term": "9,000,000"
        },
        {
            "id": "7210208",
            "name": "Piano",
            "aliases": ["Piano cổ điển", "Piano ứng dụng", "Sản xuất âm nhạc", "Giảng dạy âm nhạc"],
            "full_name": "Cử nhân Piano",
            "degree": "Cử nhân",
            "duration": "4 năm",
            "faculty": "Khoa Âm nhạc",
            "subject_combinations": ["N00"],
            "description": "Đào tạo nghệ sĩ Piano chuyên nghiệp với chuyên ngành cổ điển, ứng dụng, sản xuất và giảng dạy. Xét tuyển kết hợp thi năng khiếu.",
            "career_opportunities": [
                "Nghệ sĩ Piano",
                "Giảng viên Piano",
                "Music Producer",
                "Chuyên viên sáng tác âm nhạc"
            ],
            "tuition_per_term": "9,000,000"
        }
    ]
    
    return {
        "academic_year": "2024-2025",
        "total_programs": len(programs),
        "general_info": {
            "university": "Đại học Văn Hiến",
            "university_code": "VHU",
            "admission_year": 2025,
            "admission_methods": [
                "Phương thức 1: Xét tuyển bằng điểm thi tốt nghiệp THPT 2025",
                "Phương thức 2: Xét tuyển theo kết quả học tập THPT",
                "Phương thức 3: Xét tuyển theo điểm thi đánh giá năng lực ĐHQG Tp. HCM, ĐHQG Hà Nội",
                "Phương thức 4: Xét tuyển thẳng theo quy định của Bộ Giáo dục & Đào tạo",
                "Phương thức 5: Xét tuyển kết hợp thi tuyển các ngành Thanh nhạc, Piano, Đạo diễn điện ảnh, Công nghệ điện ảnh"
            ],
            "target_students": "Thí sinh đang học lớp 12 hoặc đã tốt nghiệp THPT",
            "scope": "Thí sinh trong cả nước"
        },
        "programs": programs
    }

def main():
    print("=" * 70)
    print("TẠO DỮ LIỆU ĐẦY ĐỦ CHO 43 NGÀNH ĐÀO TẠO")
    print("=" * 70)
    
    # Tạo dữ liệu
    data = create_comprehensive_programs_data()
    
    # Lưu vào file programs.json
    output_path = "d:\\workspace\\Chatbot\\data\\knowledge_base\\programs.json"
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"\n✓ Đã tạo file: {output_path}")
    print(f"✓ Tổng số ngành: {data['total_programs']}")
    
    # Thống kê theo khối
    faculties = {}
    for prog in data['programs']:
        faculty = prog['faculty']
        if faculty not in faculties:
            faculties[faculty] = []
        faculties[faculty].append(prog['name'])
    
    print("\n" + "=" * 70)
    print("THỐNG KÊ THEO KHOA")
    print("=" * 70)
    for faculty, programs in faculties.items():
        print(f"\n{faculty}: {len(programs)} ngành")
        for i, prog in enumerate(programs, 1):
            print(f"  {i}. {prog}")
    
    print("\n" + "=" * 70)
    print("HOÀN THÀNH!")
    print("=" * 70)
    
    # Cập nhật file lookups/programs.txt
    programs_txt_path = "d:\\workspace\\Chatbot\\data\\lookups\\programs.txt"
    with open(programs_txt_path, 'w', encoding='utf-8') as f:
        for prog in data['programs']:
            f.write(prog['name'] + '\n')
            for alias in prog['aliases']:
                if alias != prog['name']:
                    f.write(alias + '\n')
    
    print(f"\n✓ Đã cập nhật: {programs_txt_path}")

if __name__ == "__main__":
    main()
