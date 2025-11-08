"""
Cấu hình Gemini AI cho VHU Chatbot
Chỉ xử lý câu hỏi ngoài phạm vi - không thay đổi chức năng cũ
"""
import os
import logging
import requests
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

# Cấu hình Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "YOUR_API_KEY_HERE")

# Models ưu tiên (từ nhanh đến chậm)
PREFERRED_MODELS = [
    "models/gemini-2.0-flash-lite",
    "models/gemini-2.5-flash-lite", 
    "models/gemini-2.0-flash",
    "models/gemini-2.5-flash",
    "models/gemini-flash-lite-latest"
]

def configure_gemini():
    """Cấu hình Gemini AI - kiểm tra API key"""
    if not GEMINI_API_KEY or GEMINI_API_KEY == "YOUR_API_KEY_HERE":
        logger.error("Chưa có GEMINI_API_KEY")
        return False
    return True

def get_gemini_response(question: str, context: str = "") -> str:
    """
    Gọi Gemini API để trả lời câu hỏi ngoài phạm vi VHU
    
    Args:
        question: Câu hỏi của user
        context: Context về VHU nếu có
    
    Returns:
        str: Câu trả lời từ Gemini
    """
    if not configure_gemini():
        return "Híc, mình chưa được cấu hình để trả lời câu này. 😅\n\n💡 Bạn hỏi mình về VHU đi nha: học phí, ngành học, tuyển sinh..."
    
    # Lấy thời gian thực để Gemini biết ngày giờ chính xác
    from datetime import datetime
    import pytz
    
    # Timezone Việt Nam
    vietnam_tz = pytz.timezone('Asia/Ho_Chi_Minh')
    current_time = datetime.now(vietnam_tz)
    
    current_datetime = current_time.strftime("%d/%m/%Y %H:%M")
    current_day_name = current_time.strftime("%A")
    
    # Dịch tên ngày sang tiếng Việt
    day_names_vi = {
        "Monday": "Thứ Hai",
        "Tuesday": "Thứ Ba", 
        "Wednesday": "Thứ Tư",
        "Thursday": "Thứ Năm",
        "Friday": "Thứ Sáu",
        "Saturday": "Thứ Bảy",
        "Sunday": "Chủ Nhật"
    }
    current_day_vi = day_names_vi.get(current_day_name, current_day_name)
    
    # Prompt hướng dẫn Gemini
    system_prompt = f"""
Bạn là trợ lý AI của Đại học Văn Hiến (VHU), một trường đại học tư thục uy tín tại TP.HCM.

⏰ THỜI GIAN HIỆN TẠI (QUAN TRỌNG):
- Ngày giờ: {current_datetime} ({current_day_vi})
- Nếu được hỏi về thời gian, hãy dùng thông tin này!

NHIỆM VỤ: Trả lời câu hỏi ngoài phạm vi thông tin trường học với tone thân thiện, gận gũi như một sinh viên VHU.

QUY TẮC:
1. Luôn giữ vai trò là trợ lý VHU
2. Trả lời ngắn gọn, dễ hiểu (tối đa 150 từ)
3. Sử dụng emoji phù hợp
4. Nếu không biết, thành thật nói không biết
5. KHÔNG kết thúc với "💙 Bạn có muốn hỏi gì về VHU" (sẽ được thêm tự động)

CONTEXT VỀ VHU:
- Trường đại học tư thục từ 1997
- 44 ngành đào tạo
- 2 cơ sở tại TP.HCM
- Mạnh về CNTT, Kinh doanh, Du lịch
- Hotline: 1800 1568

Câu hỏi: {question}
"""
    
    # Thử từng model cho đến khi có response
    for model_name in PREFERRED_MODELS:
        try:
            response_text = _call_gemini_http(model_name, system_prompt)
            if response_text:
                response_text += "\n\n💙 Bạn có muốn hỏi gì về VHU không nè? Mình sẵn sàng tư vấn! 😊"
                return response_text
        except Exception as e:
            logger.warning(f"Model {model_name} failed: {e}")
            continue
    
    # Nếu tất cả models đều fail
    return "Xin lỗi, mình không thể trả lời câu này lúc này. 😅\n\n📞 Bạn có thể hỏi mình về VHU nhé: học phí, tuyển sinh, ngành học..."

def _call_gemini_http(model_name: str, prompt: str) -> str:
    """Gọi Gemini API qua HTTP"""
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/{model_name}:generateContent?key={GEMINI_API_KEY}"
        
        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": prompt
                        }
                    ]
                }
            ],
            "generationConfig": {
                "temperature": 0.7,
                "maxOutputTokens": 200,
                "topP": 0.8,
                "topK": 10
            }
        }
        
        headers = {"Content-Type": "application/json"}
        
        response = requests.post(url, json=payload, headers=headers, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            
            if "candidates" in data and data["candidates"]:
                candidate = data["candidates"][0]
                if "content" in candidate and "parts" in candidate["content"]:
                    return candidate["content"]["parts"][0]["text"].strip()
        elif response.status_code == 429:
            # Rate limit - thử model khác
            raise Exception("Rate limit exceeded")
        else:
            logger.error(f"HTTP {response.status_code}: {response.text}")
            raise Exception(f"HTTP {response.status_code}")
        
        return None
        
    except Exception as e:
        logger.error(f"HTTP API call failed: {e}")
        raise e

def is_vhu_related_question(question: str) -> bool:
    """
    Kiểm tra câu hỏi có liên quan đến VHU không
    
    Args:
        question: Câu hỏi cần kiểm tra
        
    Returns:
        bool: True nếu liên quan VHU, False nếu ngoài phạm vi
    """
    vhu_keywords = [
        # Từ khóa về trường
        "văn hiến", "vhu", "đại học", "trường", "học phí", "tuyển sinh",
        "ngành", "chương trình", "học bổng", "cơ sở", "ký túc xá",
        
        # Từ khóa học tập
        "cntt", "marketing", "du lịch", "kinh doanh", "tâm lý",
        "tài chính", "kế toán", "ngoại ngữ", "luật",
        
        # Từ khóa tuyển sinh
        "điểm", "thi", "xét tuyển", "hồ sơ", "đăng ký",
        
        # Từ khóa dịch vụ
        "liên hệ", "địa chỉ", "hotline", "hỗ trợ", "tư vấn"
    ]
    
    question_lower = question.lower()
    return any(keyword in question_lower for keyword in vhu_keywords)
