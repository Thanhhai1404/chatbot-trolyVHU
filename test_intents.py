"""
Script test Intent Classification (không cần Action Server)
Kiểm tra xem bot có nhận diện đúng intent không
"""

from rasa.nlu.model import Interpreter
from colorama import init, Fore
import os

init(autoreset=True)

# Test cases
TEST_CASES = {
    "🔴 1. Test các lỗi đã sửa": {
        "học phí chung": "ask_tuition",
        "phương thức tuyển sinh": "ask_admission_methods",
        "cho mình xin thông tin liên hệ": "ask_contact",
        "thông tin liên hệ": "ask_contact",
        "liên hệ": "ask_contact",
        "lịch học": "ask_schedule",
        "cho tôi lịch học": "ask_schedule",
        "cách đóng học phí": "ask_fee_payment",
        "đóng học phí": "ask_fee_payment"
    },
    
    "🟢 2. Chào hỏi & Cơ bản": {
        "xin chào": "greet",
        "hello": "greet",
        "tạm biệt": "goodbye",
        "cảm ơn bạn": "thank",
        "bạn là ai": "bot_challenge"
    },
    
    "🟢 3. Thông tin trường & Ngành học": {
        "giới thiệu về đại học văn hiến": "ask_about_school",
        "trường có bao nhiêu ngành": "ask_major_count",
        "trường có những ngành nào": "ask_list_programs",
        "thông tin ngành công nghệ thông tin": "ask_program_info",
        "ngành quản trị kinh doanh học gì": "ask_program_info"
    },
    
    "🟡 4. Học phí (Test Entity)": {
        "học phí chung": "ask_tuition",
        "học phí ngành công nghệ thông tin": "ask_tuition_specific",
        "học phí CNTT": "ask_tuition_specific",
        "học phí IT": "ask_tuition_specific",
        "học phí ngành kế toán": "ask_tuition_specific",
        "học phí marketing": "ask_tuition_specific"
    },
    
    "🟡 5. Học bổng": {
        "có học bổng không": "ask_scholarship",
        "điều kiện để nhận học bổng": "ask_scholarship_condition",
        "GPA bao nhiêu thì được học bổng": "ask_scholarship_condition",
        "học bổng toàn phần yêu cầu gì": "ask_scholarship_condition"
    },
    
    "🟡 6. Tuyển sinh": {
        "phương thức tuyển sinh": "ask_admission_methods",
        "các cách tuyển sinh của trường": "ask_admission_methods",
        "điều kiện tuyển sinh": "ask_admission_methods",
        "khi nào bắt đầu tuyển sinh": "ask_admission_time",
        "cần giấy tờ gì để nhập học": "ask_admission_documents"
    },
    
    "🟡 7. Liên hệ & Địa điểm": {
        "liên hệ": "ask_contact",
        "thông tin liên hệ": "ask_contact",
        "số điện thoại của trường": "ask_contact",
        "email tuyển sinh": "ask_contact",
        "trường ở đâu": "ask_location",
        "địa chỉ đại học văn hiến": "ask_location"
    },
    
    "🟡 8. Lịch học & Lịch thi": {
        "lịch học": "ask_schedule",
        "cho tôi lịch học": "ask_schedule",
        "khi nào khai giảng": "ask_schedule",
        "cho em hỏi lịch thi cuối kỳ": "ask_exam_schedule",
        "lịch thi môn toán cao cấp": "ask_exam_schedule"
    },
    
    "🟡 9. Cơ sở & Cơ sở vật chất": {
        "trường mình có mấy cơ sở": "ask_campuses",
        "địa chỉ các cơ sở của trường": "ask_campuses",
        "cơ sở vật chất của trường thế nào": "ask_facility",
        "có thư viện không": "ask_facility",
        "trường có ký túc xá không": "ask_dorm"
    },
    
    "🟡 10. Thanh toán học phí": {
        "đóng học phí": "ask_fee_payment",
        "cách đóng học phí": "ask_fee_payment",
        "cách thức thanh toán học phí": "ask_fee_payment",
        "có thể trả góp không": "ask_fee_payment"
    },
    
    "🟡 11. Hỗ trợ & Câu lạc bộ": {
        "trường có hỗ trợ sinh viên không": "ask_support",
        "em bị mất thẻ sinh viên": "ask_support_problem",
        "cần hỗ trợ đăng ký học phần": "ask_support_problem",
        "trường có những câu lạc bộ nào": "ask_club"
    },
    
    "🔵 12. Out of Scope": {
        "đặt pizza": "out_of_scope",
        "thời tiết hôm nay": "out_of_scope",
        "bóng đá": "out_of_scope",
        "giá vàng hôm nay": "out_of_scope"
    }
}


def test_intent_classification():
    """Test Intent Classification"""
    print(f"\n{Fore.CYAN}{'='*80}")
    print(f"{Fore.CYAN}🎯 TEST INTENT CLASSIFICATION - VHU CHATBOT")
    print(f"{Fore.CYAN}{'='*80}\n")
    
    # Tìm model mới nhất
    try:
        print(f"{Fore.YELLOW}⏳ Đang load NLU model...")
        models_dir = "models"
        model_files = [f for f in os.listdir(models_dir) if f.endswith('.tar.gz')]
        
        if not model_files:
            print(f"{Fore.RED}❌ Không tìm thấy model!")
            return
        
        latest_model = max(model_files, key=lambda x: os.path.getctime(os.path.join(models_dir, x)))
        model_path = os.path.join(models_dir, latest_model)
        
        print(f"{Fore.CYAN}📦 Model: {latest_model}")
        
        interpreter = Interpreter.load(model_path)
        print(f"{Fore.GREEN}✅ Load model thành công!\n")
    except Exception as e:
        print(f"{Fore.RED}❌ Lỗi load model: {str(e)}")
        return
    
    total_tests = 0
    passed_tests = 0
    failed_tests = 0
    results = []
    
    # Chạy từng nhóm test
    for group_name, test_cases in TEST_CASES.items():
        print(f"\n{Fore.MAGENTA}{group_name}")
        print(f"{Fore.MAGENTA}{'-'*80}")
        
        for i, (message, expected_intent) in enumerate(test_cases.items(), 1):
            total_tests += 1
            
            try:
                # Parse message
                result = interpreter.parse(message)
                predicted_intent = result['intent']['name']
                confidence = result['intent']['confidence']
                entities = result.get('entities', [])
                
                # Kiểm tra kết quả
                is_correct = predicted_intent == expected_intent
                
                if is_correct and confidence >= 0.5:
                    passed_tests += 1
                    status = f"{Fore.GREEN}✅ PASS"
                    results.append({
                        "message": message,
                        "expected": expected_intent,
                        "predicted": predicted_intent,
                        "confidence": confidence,
                        "status": "PASS"
                    })
                else:
                    failed_tests += 1
                    status = f"{Fore.RED}❌ FAIL"
                    results.append({
                        "message": message,
                        "expected": expected_intent,
                        "predicted": predicted_intent,
                        "confidence": confidence,
                        "status": "FAIL"
                    })
                
                # Hiển thị kết quả
                entity_str = ""
                if entities:
                    entity_str = f" | Entities: {', '.join([f'{e['entity']}={e['value']}' for e in entities[:2]])}"
                
                print(f"{status} | {i}. \"{message}\"")
                print(f"   {Fore.CYAN}└─> Intent: {predicted_intent} (confidence: {confidence:.2f}){entity_str}")
                
                if not is_correct:
                    print(f"   {Fore.RED}    Expected: {expected_intent}")
                
            except Exception as e:
                failed_tests += 1
                print(f"{Fore.RED}❌ ERROR | {i}. \"{message}\"")
                print(f"   {Fore.RED}└─> {str(e)}")
                results.append({
                    "message": message,
                    "expected": expected_intent,
                    "status": "ERROR",
                    "error": str(e)
                })
    
    # Summary
    print(f"\n{Fore.CYAN}{'='*80}")
    print(f"{Fore.CYAN}📊 KẾT QUẢ TỔNG HỢP")
    print(f"{Fore.CYAN}{'='*80}")
    print(f"{Fore.WHITE}Tổng số test: {total_tests}")
    print(f"{Fore.GREEN}✅ Passed: {passed_tests} ({passed_tests/total_tests*100:.1f}%)")
    print(f"{Fore.RED}❌ Failed: {failed_tests} ({failed_tests/total_tests*100:.1f}%)")
    
    # Chi tiết các test fail
    if failed_tests > 0:
        print(f"\n{Fore.RED}{'='*80}")
        print(f"{Fore.RED}❌ CHI TIẾT CÁC TEST THẤT BẠI:")
        print(f"{Fore.RED}{'='*80}")
        
        for result in results:
            if result["status"] in ["FAIL", "ERROR"]:
                print(f"{Fore.YELLOW}• {result['message']}")
                print(f"  Expected: {result['expected']}")
                if "predicted" in result:
                    print(f"  Got: {result['predicted']} (confidence: {result.get('confidence', 0):.2f})")
                if "error" in result:
                    print(f"  Error: {result['error']}")
                print()
    
    # Đánh giá tổng thể
    print(f"\n{Fore.CYAN}{'='*80}")
    if passed_tests / total_tests >= 0.95:
        print(f"{Fore.GREEN}🎉 XUẤT SẮC! Intent classification hoạt động rất tốt!")
        print(f"{Fore.GREEN}✅ Bạn có thể chạy 'rasa shell' để test full chatbot với Actions.")
    elif passed_tests / total_tests >= 0.85:
        print(f"{Fore.YELLOW}⚠️ TỐT! Intent classification cần cải thiện một chút.")
        print(f"{Fore.YELLOW}💡 Gợi ý: Bổ sung thêm training examples cho các intent bị nhầm.")
    else:
        print(f"{Fore.RED}❌ CẦN KHẮC PHỤC! Intent classification có nhiều vấn đề.")
        print(f"{Fore.RED}🔧 Cần train lại model hoặc cải thiện NLU data.")
    
    print(f"\n{Fore.CYAN}📝 HƯỚNG DẪN TEST ĐẦY ĐỦ:")
    print(f"{Fore.WHITE}   1. Mở terminal 1: rasa run actions")
    print(f"{Fore.WHITE}   2. Mở terminal 2: rasa shell")
    print(f"{Fore.WHITE}   3. Test các câu hỏi để xem Custom Actions hoạt động")
    print(f"{Fore.CYAN}{'='*80}\n")


if __name__ == "__main__":
    test_intent_classification()
