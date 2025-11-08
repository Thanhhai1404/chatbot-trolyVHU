"""
Goong Maps API Integration cho VHU Chatbot
Chức năng chỉ đường từ vị trí user đến cơ sở VHU
"""
import os
import logging
import requests
from typing import Dict, Optional, List
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

# Cấu hình API
GOONG_API_KEY = os.getenv("GOONG_API_KEY", "")
GEOCODING_URL = "https://rsapi.goong.io/geocode"
DIRECTIONS_URL = "https://rsapi.goong.io/Direction"

def configure_goong_api() -> bool:
    """Kiểm tra Goong API key có hợp lệ không"""
    if not GOONG_API_KEY or GOONG_API_KEY == "":
        logger.error("Chưa có GOONG_API_KEY trong file .env")
        return False
    return True

def geocode_address(address: str) -> Optional[Dict[str, float]]:
    """
    Chuyển địa chỉ text thành tọa độ (lat, lng)
    
    Args:
        address: Địa chỉ dạng text (VD: "Tân Hương, Tân Phú, TP.HCM")
    
    Returns:
        {"lat": 10.xxx, "lng": 106.xxx} hoặc None nếu lỗi
    """
    if not configure_goong_api():
        return None
    
    try:
        # Thêm "TP.HCM" nếu chưa có để tăng độ chính xác
        if "tp.hcm" not in address.lower() and "hồ chí minh" not in address.lower():
            address = f"{address}, TP. Hồ Chí Minh"
        
        params = {
            "address": address,
            "api_key": GOONG_API_KEY
        }
        
        response = requests.get(GEOCODING_URL, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get("results") and len(data["results"]) > 0:
                location = data["results"][0]["geometry"]["location"]
                return {
                    "lat": location["lat"],
                    "lng": location["lng"]
                }
        
        logger.error(f"Geocoding failed: {response.status_code} - {response.text}")
        return None
        
    except Exception as e:
        logger.error(f"Geocoding error: {e}")
        return None

def get_directions(origin_lat: float, origin_lng: float, 
                   dest_lat: float, dest_lng: float,
                   vehicle: str = "bike") -> Optional[Dict]:
    """
    Lấy hướng dẫn đường đi từ điểm A đến điểm B
    
    Args:
        origin_lat, origin_lng: Tọa độ điểm xuất phát
        dest_lat, dest_lng: Tọa độ điểm đến
        vehicle: "bike" (xe máy), "car" (ô tô), "taxi"
    
    Returns:
        {
            "distance": "8.2 km",
            "duration": "25 phút",
            "steps": [
                {"instruction": "Đi thẳng", "distance": "500m"},
                ...
            ]
        }
    """
    if not configure_goong_api():
        return None
    
    try:
        params = {
            "origin": f"{origin_lat},{origin_lng}",
            "destination": f"{dest_lat},{dest_lng}",
            "vehicle": vehicle,
            "api_key": GOONG_API_KEY
        }
        
        response = requests.get(DIRECTIONS_URL, params=params, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get("routes") and len(data["routes"]) > 0:
                route = data["routes"][0]
                legs = route["legs"][0]
                
                # Parse steps
                steps = []
                for step in legs.get("steps", []):
                    instruction = step.get("html_instructions", "")
                    # Loại bỏ HTML tags
                    instruction = instruction.replace("<b>", "").replace("</b>", "")
                    instruction = instruction.replace("<div>", "").replace("</div>", "")
                    
                    steps.append({
                        "instruction": instruction,
                        "distance": step.get("distance", {}).get("text", ""),
                        "duration": step.get("duration", {}).get("text", "")
                    })
                
                return {
                    "distance": legs.get("distance", {}).get("text", "N/A"),
                    "duration": legs.get("duration", {}).get("text", "N/A"),
                    "steps": steps,
                    "start_address": legs.get("start_address", ""),
                    "end_address": legs.get("end_address", "")
                }
        
        logger.error(f"Directions API failed: {response.status_code} - {response.text}")
        return None
        
    except Exception as e:
        logger.error(f"Directions API error: {e}")
        return None

def format_directions_message(directions: Dict, campus_name: str, 
                               user_location: str, campus_address: str = None) -> str:
    """
    Format dữ liệu đường đi thành message thân thiện
    
    Args:
        directions: Kết quả từ get_directions()
        campus_name: Tên cơ sở VHU
        user_location: Địa chỉ user nhập
        campus_address: Địa chỉ chính xác từ campuses.json (optional)
      Returns:
        str: Message đẹp với emoji
    """
    if not directions:
        return (
            f"⚠️ Xin lỗi bạn, mình không thể tìm đường từ **{user_location}** "
            f"đến **{campus_name}** lúc này.\n\n"
            "💡 Bạn thử:\n"
            "• Nhập địa chỉ cụ thể hơn (VD: '123 Lê Văn Việt, Quận 9')\n"
            "• Hoặc liên hệ hotline **1800 1568** để được hỗ trợ nha! 😊"
        )
    
    message = f"🗺️ **Chỉ đường từ {user_location} đến {campus_name}**\n\n"
    # Ưu tiên địa chỉ từ campuses.json thay vì từ Goong API
    destination = campus_address if campus_address else directions.get('end_address', 'N/A')
    message += f"📍 **Điểm đến:** {destination}\n"
    message += f"📏 **Khoảng cách:** {directions['distance']}\n"
    message += f"⏱️ **Thời gian:** ~{directions['duration']} (xe máy)\n\n"
    message += "🛣️ **Hướng dẫn chi tiết:**\n"
    
    steps = directions.get("steps", [])
    # Hiển thị TẤT CẢ các bước, không giới hạn
    for i, step in enumerate(steps, 1):
        instruction = step["instruction"]
        distance = step["distance"]
        
        # Thêm emoji cho từng bước
        if "rẽ phải" in instruction.lower() or "turn right" in instruction.lower():
            emoji = "↪️"
        elif "rẽ trái" in instruction.lower() or "turn left" in instruction.lower():
            emoji = "↩️"
        elif "thẳng" in instruction.lower() or "straight" in instruction.lower():
            emoji = "⬆️"
        else:
            emoji = "▶️"
        
        message += f"{i}️⃣ {emoji} {instruction}"
        if distance:
            message += f" ({distance})"
        message += "\n"
    
    message += "\n💡 **Lưu ý:** Tránh giờ cao điểm 7-9h sáng và 17-19h chiều\n"
    message += "\n🚌 Bạn có muốn biết thêm **thông tin xe buýt** không nè?"
    
    return message

def get_transit_info(user_location: str, campus_name: str, 
                     campus_transport: List[str]) -> str:
    """
    Lấy thông tin xe buýt từ data có sẵn
    
    Args:
        user_location: Địa chỉ user
        campus_name: Tên cơ sở
        campus_transport: Danh sách xe buýt từ campuses.json
    
    Returns:
        str: Thông tin xe buýt
    """
    if not campus_transport:
        return (
            "⚠️ Hiện chưa có thông tin xe buýt chi tiết đến cơ sở này.\n\n"
            "💡 Bạn có thể:\n"
            "• Dùng Google Maps để tìm xe buýt\n"
            "• Hoặc liên hệ hotline **1800 1568** để được tư vấn! 😊"
        )
    
    message = f"🚌 **Thông tin xe buýt đến {campus_name}:**\n\n"
    
    for transport in campus_transport:
        # Parse transport info (VD: "Xe buýt: 03, 18, 65, 93")
        if "xe buýt" in transport.lower() or "bus" in transport.lower():
            message += f"🚍 {transport}\n"
        else:
            message += f"📍 {transport}\n"
    
    message += "\n💰 **Giá vé xe buýt:** Khoảng 7,000đ/lượt\n"
    message += "⏱️ **Thời gian:** Thường lâu hơn xe máy 10-15 phút\n\n"
    message += "💡 **Lưu ý:** Xe buýt đông giờ cao điểm, bạn nên dự phòng thời gian nha!\n\n"
    message += "🚐 VHU còn có **xe đưa đón miễn phí** giữa các cơ sở đó! 🎉"
    
    return message
