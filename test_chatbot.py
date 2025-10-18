"""
Script test tự động cho VHU Chatbot
Kiểm tra tất cả các chức năng chính
"""

import asyncio
from rasa.core.agent import Agent
from colorama import init, Fore, Style

init(autoreset=True)

# Test cases được nhóm theo chức năng
TEST_CASES = {
    "🔴 1. Test các lỗi đã sửa (QUAN TRỌNG)": [
        "học phí chung",
        "phương thức tuyển sinh", 
        "cho mình xin thông tin liên hệ",
        "thông tin liên hệ",
        "liên hệ",
        "lịch học",
        "cho tôi lịch học",
        "cách đóng học phí",
        "đóng học phí"
    ],
    
    "🟢 2. Chào hỏi & Cơ bản": [
        "xin chào",
        "hello",
        "tạm biệt",
        "cảm ơn bạn",
        "bạn là ai"
    ],
    
    "🟢 3. Thông tin trường & Ngành học": [
        "giới thiệu về đại học văn hiến",
        "trường có bao nhiêu ngành",
        "trường có những ngành nào",
        "thông tin ngành công nghệ thông tin",
        "ngành quản trị kinh doanh học gì"
    ],
    
    "🟡 4. Học phí (Test Entity Extraction)": [
        "học phí chung",
        "học phí ngành công nghệ thông tin",
        "học phí CNTT",
        "học phí IT",
        "học phí ngành kế toán",
        "học phí marketing"
    ],
    
    "🟡 5. Học bổng": [
        "có học bổng không",
        "điều kiện để nhận học bổng",
        "GPA bao nhiêu thì được học bổng",
        "học bổng toàn phần yêu cầu gì"
    ],
    
    "🟡 6. Tuyển sinh": [
        "phương thức tuyển sinh",
        "các cách tuyển sinh của trường",
        "điều kiện tuyển sinh",
        "khi nào bắt đầu tuyển sinh",
        "cần giấy tờ gì để nhập học"
    ],
    
    "🟡 7. Liên hệ & Địa điểm": [
        "liên hệ",
        "thông tin liên hệ",
        "số điện thoại của trường",
        "email tuyển sinh",
        "trường ở đâu",
        "địa chỉ đại học văn hiến"
    ],
    
    "🟡 8. Lịch học & Lịch thi": [
        "lịch học",
        "cho tôi lịch học",
        "khi nào khai giảng",
        "cho em hỏi lịch thi cuối kỳ",
        "lịch thi môn toán cao cấp"
    ],
    
    "🟡 9. Cơ sở & Cơ sở vật chất": [
        "trường mình có mấy cơ sở",
        "địa chỉ các cơ sở của trường",
        "cơ sở vật chất của trường thế nào",
        "có thư viện không",
        "trường có ký túc xá không"
    ],
    
    "🟡 10. Thanh toán học phí": [
        "đóng học phí",
        "cách đóng học phí",
        "cách thức thanh toán học phí",
        "có thể trả góp không"
    ],
    
    "🟡 11. Hỗ trợ & Câu lạc bộ": [
        "trường có hỗ trợ sinh viên không",
        "em bị mất thẻ sinh viên",
        "cần hỗ trợ đăng ký học phần",
        "trường có những câu lạc bộ nào"
    ],
    
    "🔵 12. Out of Scope (Ngoài phạm vi)": [
        "đặt pizza",
        "thời tiết hôm nay",
        "bóng đá",
        "giá vàng hôm nay"
    ],
    
    "🔵 13. Fallback (Câu không rõ nghĩa)": [
        "asdfghjkl",
        "học phí rẻ nhất là ngành gì",
        "so với UIT thì sao"
    ]
}


async def test_chatbot():
    """Test chatbot với tất cả test cases"""
    print(f"\n{Fore.CYAN}{'='*80}")
    print(f"{Fore.CYAN}🤖 BẮT ĐẦU TEST CHATBOT VHU")
    print(f"{Fore.CYAN}{'='*80}\n")
    
    # Load agent (không dùng await vì Agent.load không phải async)
    try:
        print(f"{Fore.YELLOW}⏳ Đang load model...")
        agent = Agent.load("models")
        print(f"{Fore.GREEN}✅ Load model thành công!\n")
    except Exception as e:
        print(f"{Fore.RED}❌ Lỗi load model: {str(e)}")
        return
    
    total_tests = 0
    passed_tests = 0
    failed_tests = 0
    results = []
    
    # Chạy từng nhóm test
    for group_name, test_messages in TEST_CASES.items():
        print(f"\n{Fore.MAGENTA}{group_name}")
        print(f"{Fore.MAGENTA}{'-'*80}")
        
        for i, message in enumerate(test_messages, 1):
            total_tests += 1
            
            try:
                # Gửi message và nhận response
                responses = await agent.handle_text(message)
                
                if responses:
                    intent = responses[0].get("recipient_id") if responses else "unknown"
                    response_text = responses[0].get("text", "") if responses else ""
                    
                    # Kiểm tra response có hợp lý không
                    is_valid = len(response_text) > 0
                    
                    if is_valid:
                        passed_tests += 1
                        status = f"{Fore.GREEN}✅ PASS"
                        results.append({
                            "message": message,
                            "status": "PASS",
                            "group": group_name
                        })
                    else:
                        failed_tests += 1
                        status = f"{Fore.RED}❌ FAIL"
                        results.append({
                            "message": message,
                            "status": "FAIL",
                            "group": group_name,
                            "error": "No response"
                        })
                    
                    # Hiển thị kết quả
                    print(f"{status} | {i}. \"{message}\"")
                    print(f"   {Fore.CYAN}└─> {response_text[:100]}..." if len(response_text) > 100 else f"   {Fore.CYAN}└─> {response_text}")
                    
                else:
                    failed_tests += 1
                    print(f"{Fore.RED}❌ FAIL | {i}. \"{message}\"")
                    print(f"   {Fore.RED}└─> No response from bot")
                    results.append({
                        "message": message,
                        "status": "FAIL",
                        "group": group_name,
                        "error": "No response"
                    })
                
            except Exception as e:
                failed_tests += 1
                print(f"{Fore.RED}❌ ERROR | {i}. \"{message}\"")
                print(f"   {Fore.RED}└─> {str(e)}")
                results.append({
                    "message": message,
                    "status": "ERROR",
                    "group": group_name,
                    "error": str(e)
                })
            
            # Delay nhỏ giữa các request
            await asyncio.sleep(0.1)
    
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
                print(f"  Group: {result['group']}")
                if "error" in result:
                    print(f"  Error: {result['error']}")
                print()
    
    # Đánh giá tổng thể
    print(f"\n{Fore.CYAN}{'='*80}")
    if passed_tests / total_tests >= 0.9:
        print(f"{Fore.GREEN}🎉 XUẤT SẮC! Chatbot hoạt động rất tốt!")
    elif passed_tests / total_tests >= 0.7:
        print(f"{Fore.YELLOW}⚠️ TỐT! Chatbot cần cải thiện một số chức năng.")
    else:
        print(f"{Fore.RED}❌ CẦN KHẮC PHỤC! Chatbot có nhiều vấn đề cần sửa.")
    print(f"{Fore.CYAN}{'='*80}\n")


if __name__ == "__main__":
    asyncio.run(test_chatbot())
