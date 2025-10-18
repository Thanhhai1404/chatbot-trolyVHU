"""
Script test tự động tính học phí
Kiểm tra logic tính toán trong action_tuition_specific
Cập nhật: 18/10/2025
"""
import json
import os

def load_json_data(filename):
    """Load dữ liệu từ JSON file"""
    file_path = os.path.join("data", "knowledge_base", filename)
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def calculate_tuition_auto(tuition_info):
    """
    Logic tính toán học phí TỰ ĐỘNG (giống trong actions.py)
    Input: tuition_info với fee_per_credit và total_credits
    Output: dict với các giá trị tính toán
    """
    credit_fee = tuition_info['fee_per_credit']
    total_credits = tuition_info['total_credits']
    
    # Tính toán TỰ ĐỘNG
    total_fee = credit_fee * total_credits  # Tổng học phí cả khóa
    fee_per_semester = total_fee / 8        # Chia cho 8 học kỳ (4 năm)
    fee_per_year = total_fee / 4            # Chia cho 4 năm
    
    return {
        "credit_fee": credit_fee,
        "total_credits": total_credits,
        "total_fee": total_fee,
        "fee_per_semester": fee_per_semester,
        "fee_per_year": fee_per_year
    }

def format_vnd(amount):
    """Format số thành VNĐ với dấu phẩy"""
    return f"{int(amount):,} VNĐ"

def format_million(amount):
    """Format số thành triệu"""
    millions = amount / 1_000_000
    return f"~{millions:.1f} triệu"

def test_tuition_calculation():
    """Test tính toán học phí cho tất cả các ngành"""
    print("=" * 80)
    print("KIỂM TRA TỰ ĐỘNG TÍNH HỌC PHÍ")
    print("=" * 80)
    
    # Load data
    tuition_data = load_json_data("tuition.json")
    
    # Kiểm tra cấu trúc
    if "tuition_fees" not in tuition_data:
        print("❌ Lỗi: Không tìm thấy 'tuition_fees' trong tuition.json")
        print(f"Keys có sẵn: {list(tuition_data.keys())}")
        return
    
    tuition_fees = tuition_data["tuition_fees"]
    print(f"\n✅ Tìm thấy {len(tuition_fees)} ngành trong tuition.json\n")
    
    # Test với 5 ngành đầu tiên
    test_programs = tuition_fees[:5]
    
    print("📊 KẾT QUẢ TÍNH TOÁN TỰ ĐỘNG:\n")
    print("=" * 80)
    
    for i, prog in enumerate(test_programs, 1):
        program_name = prog["program_name"]
        
        # Tính toán TỰ ĐỘNG
        calc = calculate_tuition_auto(prog)
        
        print(f"\n{i}. **{program_name}**")
        print(f"   📊 Dữ liệu gốc:")
        print(f"      • Học phí/tín chỉ: {format_vnd(calc['credit_fee'])}")
        print(f"      • Tổng tín chỉ: {calc['total_credits']} tín chỉ")
        print(f"\n   🔢 Tính toán TỰ ĐỘNG:")
        print(f"      • Học phí/học kỳ: {format_vnd(calc['fee_per_semester'])} {format_million(calc['fee_per_semester'])}")
        print(f"      • Học phí/năm: {format_vnd(calc['fee_per_year'])} {format_million(calc['fee_per_year'])}")
        print(f"      • Tổng 4 năm: {format_vnd(calc['total_fee'])} {format_million(calc['total_fee'])}")
        print("   " + "-" * 76)
    
    print("\n" + "=" * 80)
    print("✅ HOÀN TẤT KIỂM TRA!")
    print("=" * 80)
    
    # Hiển thị công thức
    print("\n📐 CÔNG THỨC TÍNH TỰ ĐỘNG:")
    print("   1. total_fee = fee_per_credit × total_credits")
    print("   2. fee_per_semester = total_fee ÷ 8 (4 năm × 2 học kỳ)")
    print("   3. fee_per_year = total_fee ÷ 4")
    print("\n💡 Ưu điểm: Tính toán chính xác dựa trên tín chỉ thực tế của từng ngành!")

def test_specific_program(program_name):
    """Test tính toán cho một ngành cụ thể"""
    print("\n" + "=" * 80)
    print(f"KIỂM TRA CHI TIẾT: {program_name.upper()}")
    print("=" * 80)
    
    tuition_data = load_json_data("tuition.json")
    tuition_fees = tuition_data.get("tuition_fees", [])
    
    # Tìm ngành
    found = None
    for prog in tuition_fees:
        if program_name.lower() in prog["program_name"].lower():
            found = prog
            break
    
    if not found:
        print(f"❌ Không tìm thấy ngành: {program_name}")
        print(f"Các ngành có sẵn: {[p['program_name'] for p in tuition_fees[:5]]}")
        return
    
    # Tính toán
    calc = calculate_tuition_auto(found)
    
    print(f"\n📚 **Ngành:** {found['program_name']}")
    print(f"🆔 **Mã:** {found['program_id']}")
    print(f"\n📊 **TÍNH TOÁN CHI TIẾT:**")
    print(f"\n   🔸 Dữ liệu cơ bản:")
    print(f"      • Học phí/tín chỉ: {format_vnd(calc['credit_fee'])}")
    print(f"      • Tổng số tín chỉ: {calc['total_credits']} tín chỉ")
    
    print(f"\n   🔸 Tính toán TỰ ĐỘNG:")
    print(f"      • Tổng học phí (= {calc['credit_fee']:,} × {calc['total_credits']}):")
    print(f"        → {format_vnd(calc['total_fee'])}")
    
    print(f"\n      • Học phí/học kỳ (= {calc['total_fee']:,} ÷ 8):")
    print(f"        → {format_vnd(calc['fee_per_semester'])} {format_million(calc['fee_per_semester'])}")
    
    print(f"\n      • Học phí/năm (= {calc['total_fee']:,} ÷ 4):")
    print(f"        → {format_vnd(calc['fee_per_year'])} {format_million(calc['fee_per_year'])}")
    
    # Hiển thị như chatbot sẽ trả lời
    print(f"\n{'='*80}")
    print("💬 **CHATBOT SẼ TRẢ LỜI:**")
    print(f"{'='*80}")
    print(f"""
Bạn ơi, mình tra giúp bạn học phí nè! 💰

📚 **Học phí ngành {found['program_name']}:**

💡 **Chi tiết học phí:**
├─ Học phí/tín chỉ: {format_vnd(calc['credit_fee'])}
├─ Tổng số tín chỉ: {calc['total_credits']} tín chỉ
└─ Tổng cả khóa (4 năm): {format_vnd(calc['total_fee'])}

📊 **Học phí ước tính theo thời gian:**
• Mỗi học kỳ: {format_vnd(calc['fee_per_semester'])} ({format_million(calc['fee_per_semester'])})
• Mỗi năm (2 HK): {format_vnd(calc['fee_per_year'])} ({format_million(calc['fee_per_year'])})
• Cả 4 năm (8 HK): {format_vnd(calc['total_fee'])} ({format_million(calc['total_fee'])})

📞 **Liên hệ:** 028 6295 1517 để được tư vấn chi tiết nha!
    """)
    print("=" * 80)

def compare_calculation_methods():
    """So sánh 2 phương pháp: Manual vs Auto"""
    print("\n" + "=" * 80)
    print("SO SÁNH: MANUAL vs TỰ ĐỘNG")
    print("=" * 80)
    
    tuition_data = load_json_data("tuition.json")
    prog = tuition_data["tuition_fees"][0]  # Ngành đầu tiên
    
    calc = calculate_tuition_auto(prog)
    
    print(f"\n📚 Ngành: {prog['program_name']}")
    print(f"\n📊 Dữ liệu input:")
    print(f"   • fee_per_credit: {calc['credit_fee']:,} VNĐ")
    print(f"   • total_credits: {calc['total_credits']}")
    
    print(f"\n🔢 TÍNH TOÁN TỰ ĐỘNG:")
    print(f"   1. total_fee = {calc['credit_fee']:,} × {calc['total_credits']}")
    print(f"      → {calc['total_fee']:,} VNĐ")
    print(f"\n   2. fee_per_semester = {calc['total_fee']:,} ÷ 8")
    print(f"      → {calc['fee_per_semester']:,.0f} VNĐ")
    print(f"\n   3. fee_per_year = {calc['total_fee']:,} ÷ 4")
    print(f"      → {calc['fee_per_year']:,.0f} VNĐ")
    
    print(f"\n✅ Ưu điểm tính toán tự động:")
    print(f"   • Chính xác dựa trên số tín chỉ thực tế")
    print(f"   • Không cần hardcode")
    print(f"   • Dễ maintain và update")
    print(f"   • Nhất quán với dữ liệu gốc")

if __name__ == "__main__":
    # 1. Test tổng quan
    test_tuition_calculation()
    
    # 2. Test chi tiết một số ngành
    print("\n\n🔍 KIỂM TRA CHI TIẾT CÁC NGÀNH\n")
    test_specific_program("Công nghệ thông tin")
    test_specific_program("Marketing")
    test_specific_program("Kế toán")
    
    # 3. So sánh phương pháp
    compare_calculation_methods()
    
    print("\n\n" + "=" * 80)
    print("🎉 HOÀN TẤT TẤT CẢ KIỂM TRA!")
    print("=" * 80)
