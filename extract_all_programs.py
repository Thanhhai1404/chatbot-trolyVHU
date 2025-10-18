"""
Script để trích xuất toàn bộ thông tin 43 ngành đào tạo từ PDF
"""
import pdfplumber
import json
import re

def extract_programs_from_pdf(pdf_path):
    """Trích xuất thông tin các ngành từ PDF"""
    programs = []
    
    with pdfplumber.open(pdf_path) as pdf:
        # Đọc tất cả các trang
        full_text = ""
        for page in pdf.pages:
            full_text += page.extract_text() + "\n"
        
        # Tìm các ngành theo pattern: STT. Tên ngành Mã ngành
        lines = full_text.split('\n')
        
        current_program = None
        program_number = 0
        
        for i, line in enumerate(lines):
            line = line.strip()
            
            # Tìm mã ngành (7 chữ số)
            code_match = re.search(r'\b(7\d{6})\b', line)
            
            if code_match:
                program_code = code_match.group(1)
                
                # Lấy tên ngành (phần trước mã ngành)
                text_before_code = line[:code_match.start()].strip()
                
                # Loại bỏ số thứ tự đầu dòng
                text_before_code = re.sub(r'^\d+\.\s*', '', text_before_code)
                # Loại bỏ dấu "-" đầu dòng
                text_before_code = re.sub(r'^-\s*', '', text_before_code)
                
                program_name = text_before_code.strip()
                
                if program_name:
                    program_number += 1
                    
                    # Tìm tổ hợp môn (A00, A01, C04, D01, etc.)
                    subject_combos = []
                    # Tìm trong dòng hiện tại và 5 dòng tiếp theo
                    for j in range(i, min(i+6, len(lines))):
                        combo_matches = re.findall(r'([A-D]\d{2}): ([^\n]+?)(?=[A-D]\d{2}:|$)', lines[j])
                        for combo_code, subjects in combo_matches:
                            subject_combos.append({
                                "code": combo_code,
                                "subjects": subjects.strip()
                            })
                    
                    program_data = {
                        "number": program_number,
                        "code": program_code,
                        "name": program_name,
                        "subject_combinations": subject_combos[:4] if subject_combos else []  # Lấy tối đa 4 tổ hợp
                    }
                    
                    programs.append(program_data)
                    print(f"✓ Extracted: {program_number}. {program_name} - {program_code}")
    
    return programs

def map_to_json_format(programs):
    """Chuyển đổi sang format JSON cho programs.json"""
    
    # Mapping tên ngành sang alias
    name_to_alias_map = {
        "Quản trị kinh doanh tổng hợp": ["QTKD", "Quản trị kinh doanh", "Business Administration"],
        "Quản trị dự án": ["QTDA", "Project Management"],
        "Marketing truyền thông": ["Marketing", "MKT"],
        "Quản trị Marketing": ["Marketing Management"],
        "Digital Marketing": ["Marketing Online", "Marketing số"],
        "Kinh doanh thương mại": ["KDTM", "Trade"],
        "Thương mại điện tử": ["TMĐT", "E-commerce"],
        "Quản trị nhân lực": ["QTNL", "HR", "Human Resources"],
        "Logistics và Quản lý chuỗi cung ứng": ["Logistics", "SCM"],
        "Kinh doanh quốc tế": ["KDQT", "International Business"],
        "Tài chính doanh nghiệp": ["TCDN", "Corporate Finance"],
        "Ngân hàng số": ["Digital Banking", "Fintech"],
        "Kế toán": ["Accounting", "KT"],
        "Kiểm toán": ["Auditing"],
        "Công nghệ thông tin": ["CNTT", "IT", "Information Technology"],
        "An toàn thông tin": ["Information Security", "ATTT"],
        "Kỹ thuật môi trường": ["KTMT", "Environmental Engineering"],
        "Công nghệ thực phẩm": ["CNTP", "Food Technology"],
        "Kỹ thuật xây dựng": ["KTXD", "Civil Engineering"],
        "Khoa học dữ liệu": ["Data Science", "KHĐL"],
        "Thiết kế đồ họa": ["Graphic Design", "TKĐH"],
        "Mạng máy tính và Truyền thông": ["Network", "MMTT"],
        "Luật kinh tế": ["Law", "Luật"],
        "Luật thương mại quốc tế": ["International Trade Law"],
        "Phương pháp dạy học bộ môn tiếng Anh": ["TESOL", "Teaching English"],
        "Ngôn ngữ Anh": ["English", "Tiếng Anh"],
        "Ngôn ngữ Trung Quốc": ["Chinese", "Tiếng Trung"],
        "Ngôn ngữ Hàn Quốc": ["Korean", "Tiếng Hàn"],
        "Đối ngoại – Hợp tác quốc tế": ["International Relations", "HTQT"],
        "Đông phương học": ["Oriental Studies"],
        "Quan hệ công chúng": ["PR", "Public Relations"],
        "Sư phạm mầm non": ["Preschool Education"],
        "Xã hội học truyền thông đại chúng": ["Mass Communication", "XHTT"],
        "Tham vấn và trị liệu tâm lý": ["Psychology", "Tâm lý học"],
        "Công tác xã hội": ["Social Work"],
        "Truyền thông và sáng tạo nội dung": ["Content Creation", "TTSTNĐ"],
        "Sản xuất phim và quảng cáo": ["Film Production"],
        "Quản trị du lịch": ["Tourism Management", "QTDL"],
        "Quản trị lữ hành": ["Travel Management"],
        "Quản trị khách sạn - Khu du lịch": ["Hotel Management", "QTKS"],
        "Hướng dẫn du lịch": ["Tour Guide"],
        "Đạo diễn điện ảnh, truyền hình": ["Film Director"],
        "Dựng phim": ["Film Editing"],
        "Thanh nhạc thính phòng": ["Vocal Music"],
        "Piano ứng dụng": ["Applied Piano"]
    }
    
    json_programs = []
    
    for prog in programs:
        program_name = prog["name"]
        aliases = name_to_alias_map.get(program_name, [program_name])
        
        json_prog = {
            "id": prog["code"],
            "name": program_name,
            "aliases": aliases,
            "full_name": f"Ngành {program_name}",
            "degree": "Cử nhân",
            "duration": "4 năm",
            "subject_combinations": [combo["code"] for combo in prog["subject_combinations"]],
            "subject_details": prog["subject_combinations"],
            "description": f"Chương trình đào tạo {program_name} tại Đại học Văn Hiến",
            "career_opportunities": [
                f"Làm việc tại các doanh nghiệp trong lĩnh vực {program_name.lower()}",
                "Cơ hội thăng tiến cao",
                "Mức lương cạnh tranh"
            ],
            "admission_criteria": {
                "min_score": "Theo điểm sàn của Bộ GD&ĐT",
                "priority_subjects": [combo["subjects"] for combo in prog["subject_combinations"][:2]]
            }
        }
        
        json_programs.append(json_prog)
    
    return json_programs

def main():
    pdf_path = "d:\\workspace\\Chatbot\\Thong tin tuyen sinh VHU 1.pdf"
    output_path = "d:\\workspace\\Chatbot\\extracted_programs_full.json"
    
    print("=" * 60)
    print("TRÍCH XUẤT THÔNG TIN CÁC NGÀNH ĐÀO TẠO TỪ PDF")
    print("=" * 60)
    
    # Trích xuất dữ liệu
    programs = extract_programs_from_pdf(pdf_path)
    
    print(f"\n✓ Đã trích xuất {len(programs)} ngành đào tạo")
    
    # Chuyển đổi sang JSON format
    json_programs = map_to_json_format(programs)
    
    # Lưu file JSON
    output_data = {
        "academic_year": "2024-2025",
        "total_programs": len(json_programs),
        "programs": json_programs
    }
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n✓ Đã lưu file: {output_path}")
    print("\nCác ngành đã trích xuất:")
    for i, prog in enumerate(programs, 1):
        print(f"{i:2d}. {prog['name']} ({prog['code']})")
    
    print("\n" + "=" * 60)
    print("HOÀN THÀNH!")
    print("=" * 60)

if __name__ == "__main__":
    main()
