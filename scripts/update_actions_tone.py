"""
Script để cập nhật tone responses trong actions.py
Chuyển từ tone formal sang tone thân thiện (peer-to-peer)
"""

# Mapping old phrases -> new friendly phrases
TONE_MAPPINGS = {
    # Greeting patterns
    "Xin lỗi,": "Ôi bạn ơi,",
    "Rất tiếc,": "Híc,",
    "Rất vui được": "Mình vui lắm khi được",
    
    # Information providing
    "Thông tin chi tiết": "Thông tin mình tìm được",
    "Dưới đây là": "Đây nè,",
    "Đây là thông tin": "Bạn ơi, đây là thông tin",
    "Mình xin cung cấp": "Mình cho bạn biết",
    
    # Questions/Suggestions
    "Bạn muốn biết": "Bạn muốn biết",
    "Vui lòng": "Bạn",
    "Hãy": "Bạn nên",
    "Quý khách": "Bạn",
    
    # Endings
    "để biết thêm chi tiết!": "để biết thêm chi tiết nha!",
    "để được tư vấn chi tiết!": "để được tư vấn nha!",
    "nhé!": "nha!",
    
    # Professional terms -> casual
    "liên hệ:": "liên hệ nha:",
    "Các ngành hiện có:": "Các ngành có sẵn nè:",
    "Ví dụ:": "Ví dụ nè:",
    "Lưu ý:": "Lưu ý nha:",
}

# Patterns to add "nè", "nha", "luôn" for friendliness
FRIENDLY_ENDINGS = {
    "!": " nha!",
    ".": " nè.",
    "đó.": " đó nha.",
    "rồi.": " rồi nha.",
}

print("Mapping tone changes:")
for old, new in TONE_MAPPINGS.items():
    print(f"  '{old}' → '{new}'")
