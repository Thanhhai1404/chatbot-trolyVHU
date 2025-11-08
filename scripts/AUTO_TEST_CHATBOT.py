"""
AUTO TEST CHATBOT - Tự động hỏi tất cả câu hỏi và ghi kết quả
Version: 2.1.0
Date: 19/10/2025

Script này sẽ:
1. Tự động gửi tất cả câu hỏi test đến chatbot
2. Ghi lại responses của bot
3. Tạo báo cáo chi tiết
4. So sánh với expected results
"""

import requests
import json
import time
from datetime import datetime
from pathlib import Path

class ChatbotAutoTester:
    def __init__(self, base_url="http://localhost:5005"):
        self.base_url = base_url
        self.webhook_url = f"{base_url}/webhooks/rest/webhook"
        self.sender_id = f"test_user_{int(time.time())}"
        self.test_results = []
        self.total_tests = 0
        self.passed_tests = 0
        self.failed_tests = 0
        
    def send_message(self, message, wait_time=1):
        """Gửi message đến chatbot"""
        try:
            payload = {
                "sender": self.sender_id,
                "message": message
            }
            
            response = requests.post(
                self.webhook_url,
                json=payload,
                timeout=10
            )
            
            if response.status_code == 200:
                bot_responses = response.json()
                time.sleep(wait_time)  # Đợi bot xử lý
                return bot_responses
            else:
                return [{"text": f"ERROR: Status {response.status_code}"}]
                
        except Exception as e:
            return [{"text": f"ERROR: {str(e)}"}]
    
    def format_response(self, responses):
        """Format bot responses"""
        if not responses:
            return "No response"
        
        formatted = []
        for resp in responses:
            if "text" in resp:
                formatted.append(resp["text"])
            elif "custom" in resp:
                formatted.append(f"[Custom: {resp['custom']}]")
        
        return "\n".join(formatted)
    
    def test_conversation(self, test_name, questions, expected_keywords=None):
        """Test một cuộc hội thoại"""
        print(f"\n{'='*80}")
        print(f"🧪 TEST: {test_name}")
        print(f"{'='*80}\n")
        
        conversation_log = []
        test_passed = True
        
        for i, question in enumerate(questions, 1):
            print(f"\n👤 User [{i}/{len(questions)}]: {question}")
            
            responses = self.send_message(question)
            bot_reply = self.format_response(responses)
            
            print(f"🤖 Bot: {bot_reply[:500]}...")  # Limit output
            
            # Log conversation
            conversation_log.append({
                "question": question,
                "response": bot_reply,
                "timestamp": datetime.now().isoformat()
            })
            
            # Check expected keywords
            if expected_keywords and i <= len(expected_keywords):
                keywords = expected_keywords[i-1]
                if keywords:
                    found = all(kw.lower() in bot_reply.lower() for kw in keywords)
                    if found:
                        print(f"   ✅ Contains expected keywords: {keywords}")
                    else:
                        print(f"   ❌ Missing keywords: {keywords}")
                        test_passed = False
        
        self.total_tests += 1
        if test_passed:
            self.passed_tests += 1
            status = "✅ PASSED"
        else:
            self.failed_tests += 1
            status = "❌ FAILED"
        
        # Save result
        self.test_results.append({
            "test_name": test_name,
            "status": status,
            "conversation": conversation_log,
            "timestamp": datetime.now().isoformat()
        })
        
        print(f"\n{status}: {test_name}")
        return test_passed
    
    def run_all_tests(self):
        """Chạy tất cả các test cases"""
        
        print("="*80)
        print("🚀 CHATBOT VHU - AUTOMATED TESTING SUITE v2.1.0")
        print("="*80)
        print(f"🕐 Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🌐 Server: {self.base_url}")
        print(f"👤 Sender ID: {self.sender_id}\n")
        
        # ============= TEST 1: BASIC INTENTS =============
        self.test_conversation(
            "Test 1: Basic Greetings & Help",
            [
                "Xin chào",
                "Bot có thể làm gì?",
                "Cảm ơn",
                "Tạm biệt"
            ],
            [
                ["chào", "giúp"],
                ["tư vấn", "tuyển sinh"],
                ["vui"],
                ["hẹn gặp", "chúc"]
            ]
        )
        
        # ============= TEST 2: TUITION QUERIES =============
        self.test_conversation(
            "Test 2.1: Direct Tuition Query - CNTT",
            [
                "Học phí ngành CNTT bao nhiêu?"
            ],
            [
                ["công nghệ thông tin", "16,416,000", "1,368,000"]
            ]
        )
        
        self.test_conversation(
            "Test 2.2: Direct Tuition Query - Marketing",
            [
                "Học phí Marketing là bao nhiêu?"
            ],
            [
                ["marketing", "15,792,000"]
            ]
        )
        
        self.test_conversation(
            "Test 2.3: Tuition with Form",
            [
                "Cho mình hỏi học phí",
                "Kế toán"
            ],
            [
                ["ngành nào"],
                ["kế toán", "15,792,000"]
            ]
        )
        
        # ============= TEST 3: SCHOLARSHIP QUERIES =============
        self.test_conversation(
            "Test 3.1: General Scholarship",
            [
                "Có học bổng gì không?"
            ],
            [
                ["học bổng", "thủ khoa", "100%"]
            ]
        )
        
        self.test_conversation(
            "Test 3.2: Specific Scholarship",
            [
                "Học bổng tài năng là gì?"
            ],
            [
                ["tài năng", "thủ khoa"]
            ]
        )
        
        # ============= TEST 4: PROGRAM INFORMATION =============
        self.test_conversation(
            "Test 4.1: Single Program Info",
            [
                "Ngành CNTT học gì?"
            ],
            [
                ["công nghệ thông tin", "lập trình"]
            ]
        )
        
        self.test_conversation(
            "Test 4.2: List All Programs",
            [
                "Trường có những ngành gì?"
            ],
            [
                ["44 ngành", "khoa"]
            ]
        )
        
        # ============= TEST 5: ADMISSION INFO =============
        self.test_conversation(
            "Test 5.1: General Admission",
            [
                "Điều kiện tuyển sinh?"
            ],
            [
                ["tuyển sinh", "điểm"]
            ]
        )
        
        self.test_conversation(
            "Test 5.2: Program-specific Admission",
            [
                "Điều kiện vào ngành CNTT?"
            ],
            [
                ["công nghệ thông tin", "tuyển sinh"]
            ]
        )
        
        # ============= TEST 6: CAMPUS INFO =============
        self.test_conversation(
            "Test 6.1: Campus List",
            [
                "Trường có mấy cơ sở?"
            ],
            [
                ["cơ sở", "quận"]
            ]
        )
        
        self.test_conversation(
            "Test 6.2: Specific Campus",
            [
                "Cơ sở Quận 12 ở đâu?"
            ],
            [
                ["quận 12", "địa chỉ"]
            ]
        )
        
        # ============= TEST 7: MULTI-TURN CONVERSATIONS =============
        self.test_conversation(
            "Test 7.1: Context-aware Conversation",
            [
                "Tôi quan tâm ngành CNTT",
                "Học phí bao nhiêu?",
                "Có học bổng gì không?",
                "Điều kiện tuyển sinh?"
            ],
            [
                ["công nghệ thông tin"],
                ["16,416,000"],
                ["học bổng"],
                ["tuyển sinh"]
            ]
        )
        
        self.test_conversation(
            "Test 7.2: Program Comparison",
            [
                "So sánh CNTT và Marketing",
                "Học phí thằng nào rẻ hơn?"
            ],
            [
                ["công nghệ thông tin", "marketing"],
                ["rẻ", "marketing"]
            ]
        )
        
        # ============= TEST 8: FORM-BASED INTERACTIONS =============
        self.test_conversation(
            "Test 8.1: Tuition Form Complete",
            [
                "Học phí",
                "CNTT"
            ],
            [
                ["ngành nào"],
                ["công nghệ thông tin", "16,416,000"]
            ]
        )
        
        self.test_conversation(
            "Test 8.2: Scholarship Form",
            [
                "Học bổng",
                "Học bổng tài năng"
            ],
            [
                ["loại học bổng"],
                ["tài năng", "thủ khoa"]
            ]
        )
        
        # ============= TEST 9: VARIATIONS & SYNONYMS =============
        self.test_conversation(
            "Test 9.1: Synonym Recognition - CNTT",
            [
                "IT là gì?",
                "Học phí Information Technology?"
            ],
            [
                ["công nghệ thông tin"],
                ["công nghệ thông tin", "16,416,000"]
            ]
        )
        
        self.test_conversation(
            "Test 9.2: Synonym Recognition - QTKD",
            [
                "Quản trị KD học gì?",
                "Học phí Business Administration?"
            ],
            [
                ["quản trị kinh doanh"],
                ["quản trị kinh doanh", "15,792,000"]
            ]
        )
        
        # ============= TEST 10: FOLLOW-UP ACTIONS =============
        self.test_conversation(
            "Test 10.1: Scholarship Suggestion after Tuition",
            [
                "Học phí CNTT bao nhiêu?",
                "Có"  # Response to scholarship suggestion
            ],
            [
                ["16,416,000", "học bổng"],
                ["học bổng"]
            ]
        )
        
        # ============= TEST 11: ERROR HANDLING =============
        self.test_conversation(
            "Test 11.1: Out of Scope",
            [
                "Thời tiết hôm nay thế nào?"
            ],
            [
                ["xin lỗi", "tuyển sinh"]
            ]
        )
        
        self.test_conversation(
            "Test 11.2: Non-existent Program",
            [
                "Học phí ngành Vật lý?"
            ],
            [
                ["không tìm thấy", "ngành"]
            ]
        )
        
        # ============= TEST 12: COMPLEX QUERIES =============
        self.test_conversation(
            "Test 12.1: Multiple Questions in One",
            [
                "Học phí và học bổng ngành CNTT?"
            ],
            [
                ["công nghệ thông tin"]
            ]
        )
        
        self.test_conversation(
            "Test 12.2: Full Exploration Journey",
            [
                "Xin chào",
                "Tôi muốn biết về ngành CNTT",
                "Học phí bao nhiêu?",
                "Có học bổng gì không?",
                "Điều kiện tuyển sinh?",
                "Trường ở đâu?",
                "Cảm ơn bot"
            ],
            [
                ["chào"],
                ["công nghệ thông tin"],
                ["16,416,000"],
                ["học bổng"],
                ["tuyển sinh"],
                ["cơ sở"],
                ["vui"]
            ]
        )
        
        # ============= TEST 13: PDF DATA ACCURACY =============
        self.test_conversation(
            "Test 13.1: Verify Highest Tuition",
            [
                "Học phí ngành Kiểm toán?"
            ],
            [
                ["kiểm toán", "22,056,000"]
            ]
        )
        
        self.test_conversation(
            "Test 13.2: Verify Lowest Tuition",
            [
                "Học phí ngành Ngôn ngữ Pháp?"
            ],
            [
                ["pháp", "8,736,000"]
            ]
        )
        
        self.test_conversation(
            "Test 13.3: Verify Scholarship Count",
            [
                "Có bao nhiêu loại học bổng?"
            ],
            [
                ["13", "học bổng"]
            ]
        )
        
        # ============= TEST 14: ALL MAJOR PROGRAMS =============
        programs_to_test = [
            ("CNTT", "16,416,000"),
            ("Marketing", "15,792,000"),
            ("Kế toán", "15,792,000"),
            ("QTKD", "15,792,000"),
            ("Luật", "17,472,000"),
            ("Du lịch", "15,792,000"),
            ("Logistics", "17,028,000"),
            ("Ngôn ngữ Anh", "15,084,000"),
        ]
        
        for program, expected_fee in programs_to_test:
            self.test_conversation(
                f"Test 14.x: Tuition for {program}",
                [f"Học phí {program}?"],
                [[expected_fee]]
            )
        
        # ============= TEST 15: RESPONSE VARIATIONS =============
        print(f"\n{'='*80}")
        print("🧪 TEST 15: Response Variations")
        print(f"{'='*80}\n")
        
        responses_list = []
        for i in range(5):
            print(f"\nTry {i+1}/5: Xin chào")
            resp = self.send_message("Xin chào")
            reply = self.format_response(resp)
            responses_list.append(reply)
            print(f"Bot: {reply[:100]}...")
        
        unique_responses = len(set(responses_list))
        print(f"\n✅ Unique responses: {unique_responses}/5")
        
        if unique_responses >= 3:
            self.passed_tests += 1
            print("✅ PASSED: Good variation (≥3 different responses)")
        else:
            self.failed_tests += 1
            print("❌ FAILED: Low variation (<3 different responses)")
        
        self.total_tests += 1
    
    def generate_report(self):
        """Tạo báo cáo chi tiết"""
        
        print("\n\n")
        print("="*80)
        print("📊 FINAL TEST REPORT")
        print("="*80)
        
        # Summary
        print(f"\n📈 SUMMARY:")
        print(f"   Total Tests: {self.total_tests}")
        print(f"   ✅ Passed: {self.passed_tests}")
        print(f"   ❌ Failed: {self.failed_tests}")
        
        if self.total_tests > 0:
            pass_rate = (self.passed_tests / self.total_tests) * 100
            print(f"   📊 Pass Rate: {pass_rate:.1f}%")
            
            if pass_rate >= 95:
                status = "✅ EXCELLENT"
            elif pass_rate >= 80:
                status = "⚠️ GOOD"
            else:
                status = "❌ NEEDS IMPROVEMENT"
            
            print(f"   🎯 Status: {status}")
        
        # Save to JSON
        output_file = Path("test_results_auto.json")
        report_data = {
            "test_date": datetime.now().isoformat(),
            "sender_id": self.sender_id,
            "summary": {
                "total": self.total_tests,
                "passed": self.passed_tests,
                "failed": self.failed_tests,
                "pass_rate": pass_rate if self.total_tests > 0 else 0
            },
            "results": self.test_results
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 Full report saved to: {output_file}")
        
        # Save to readable text
        text_file = Path("test_results_auto.txt")
        with open(text_file, 'w', encoding='utf-8') as f:
            f.write("="*80 + "\n")
            f.write("CHATBOT VHU - AUTOMATED TEST RESULTS\n")
            f.write("="*80 + "\n\n")
            f.write(f"Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total Tests: {self.total_tests}\n")
            f.write(f"Passed: {self.passed_tests}\n")
            f.write(f"Failed: {self.failed_tests}\n")
            f.write(f"Pass Rate: {pass_rate:.1f}%\n\n")
            
            for i, result in enumerate(self.test_results, 1):
                f.write(f"\n{'='*80}\n")
                f.write(f"TEST {i}: {result['test_name']}\n")
                f.write(f"Status: {result['status']}\n")
                f.write(f"{'='*80}\n\n")
                
                for conv in result['conversation']:
                    f.write(f"👤 User: {conv['question']}\n")
                    f.write(f"🤖 Bot: {conv['response']}\n\n")
        
        print(f"📄 Readable report saved to: {text_file}")
        
        print("\n" + "="*80)
        print("✅ TESTING COMPLETE!")
        print("="*80 + "\n")


def check_server():
    """Kiểm tra server có chạy không"""
    try:
        response = requests.get("http://localhost:5005", timeout=5)
        return True
    except:
        return False


def main():
    """Main function"""
    
    print("\n" + "="*80)
    print("🤖 CHATBOT VHU - AUTOMATED TESTING SUITE")
    print("Version: 2.1.0")
    print("Date: October 19, 2025")
    print("="*80 + "\n")
    
    # Check if server is running
    print("🔍 Checking if Rasa server is running...")
    
    if not check_server():
        print("\n❌ ERROR: Rasa server is not running!")
        print("\n📝 To start the server, run these commands:")
        print("\n   Terminal 1 - Actions Server:")
        print("   cd d:\\workspace\\Chatbot")
        print("   rasa run actions")
        print("\n   Terminal 2 - Rasa Server:")
        print("   cd d:\\workspace\\Chatbot")
        print("   rasa run --enable-api --cors \"*\"")
        print("\n⏰ Wait for both servers to start, then run this script again.\n")
        return
    
    print("✅ Server is running!\n")
    
    # Run tests
    tester = ChatbotAutoTester()
    
    try:
        tester.run_all_tests()
        tester.generate_report()
    except KeyboardInterrupt:
        print("\n\n⚠️ Testing interrupted by user")
        tester.generate_report()
    except Exception as e:
        print(f"\n\n❌ Error during testing: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
