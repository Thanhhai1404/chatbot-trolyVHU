from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from typing import Any, Text, Dict, List
import logging
import json
import os

logger = logging.getLogger(__name__)

# Hàm đọc dữ liệu từ JSON files
def load_json_data(filename):
    """Load data from JSON file in knowledge_base folder"""
    try:
        # Đường dẫn đến file JSON
        base_path = os.path.dirname(os.path.dirname(__file__))  # Root của project
        file_path = os.path.join(base_path, "data", "knowledge_base", filename)
        
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error loading {filename}: {str(e)}")
        return {}

# Load dữ liệu từ JSON files
PROGRAMS_DATA = load_json_data("programs.json")
TUITION_DATA = load_json_data("tuition.json")
SCHOLARSHIPS_DATA = load_json_data("scholarships.json")
CAMPUSES_DATA = load_json_data("campuses.json")
CONTACTS_DATA = load_json_data("contacts.json")

# Helper functions
def find_program_by_alias(program_name):
    """Tìm program bằng name hoặc alias"""
    if not program_name or "programs" not in PROGRAMS_DATA:
        return None
    
    program_lower = program_name.lower().strip()
    
    for prog in PROGRAMS_DATA["programs"]:
        # Check aliases
        if any(alias.lower() == program_lower for alias in prog.get("aliases", [])):
            return prog
        # Check name
        if prog["name"].lower() == program_lower:
            return prog
    
    return None

def find_tuition_by_program_id(program_id):
    """Tìm học phí theo program_id"""
    if not program_id or "tuition_fees" not in TUITION_DATA:
        return None
    
    for tuition in TUITION_DATA["tuition_fees"]:
        if tuition["program_id"] == program_id:
            return tuition
    
    return None

def find_scholarship_by_id(scholarship_id):
    """Tìm học bổng theo ID"""
    if not scholarship_id or "scholarships" not in SCHOLARSHIPS_DATA:
        return None
    
    scholarship_lower = scholarship_id.lower()
    
    for scholar in SCHOLARSHIPS_DATA["scholarships"]:
        if scholarship_lower in scholar["name"].lower():
            return scholar
    
    return None


#  ===================  CUSTOM ACTIONS  ===================

class ActionTuitionSpecific(Action):
    def name(self) -> str:
        return "action_tuition_specific"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Lấy entity program
        program = tracker.get_slot("program")
        if not program:
            program = next(tracker.get_latest_entity_values("program"), None)
        
        if program:            # Tìm program từ JSON
            prog_info = find_program_by_alias(program)
            
            if prog_info:
                # Tìm học phí
                tuition_info = find_tuition_by_program_id(prog_info["id"])
                
                if tuition_info:
                    # Tính toán tự động học phí
                    credit_fee = tuition_info['fee_per_credit']
                    total_credits = tuition_info['total_credits']
                    total_fee = credit_fee * total_credits
                    
                    # Tính học phí theo năm (giả sử 4 năm = 8 học kỳ)
                    fee_per_semester = total_fee / 8
                    fee_per_year = total_fee / 4
                    
                    # Tạo message thân thiện
                    message = f"Bạn ơi, mình tra giúp bạn học phí nè! 💰\n\n"
                    message += f"📚 **Ngành: {prog_info['name']}**\n\n"
                    
                    message += "💡 **Chi tiết học phí:**\n"
                    message += f"├─ Học phí/tín chỉ: **{credit_fee:,} VNĐ**\n"
                    message += f"├─ Tổng số tín chỉ: **{total_credits} tín chỉ**\n"
                    message += f"└─ Tổng cả khóa (4 năm): **~{total_fee:,} VNĐ**\n\n"
                    
                    message += "📊 **Học phí ước tính theo thời gian:**\n"
                    message += f"• Mỗi học kỳ: **~{fee_per_semester:,.0f} VNĐ** (~{fee_per_semester/1000000:.1f} triệu)\n"
                    message += f"• Mỗi năm: **~{fee_per_year:,.0f} VNĐ** (~{fee_per_year/1000000:.1f} triệu)\n"
                    message += f"• Cả 4 năm: **~{total_fee:,} VNĐ** (~{total_fee/1000000:.1f} triệu)\n\n"
                    
                    # Thông tin bổ sung
                    if "general_info" in TUITION_DATA:
                        gen_info = TUITION_DATA["general_info"]
                        message += "💳 **Hỗ trợ thanh toán:**\n"
                        if gen_info.get("payment_deadline"):
                            message += f"⏰ Hạn đóng: {gen_info.get('payment_deadline')}\n"
                        if gen_info.get("discount_policy") and isinstance(gen_info['discount_policy'], list):
                            message += f"🎁 Ưu đãi: {gen_info['discount_policy'][0]}\n"
                        message += "\n"
                    
                    message += f"ℹ️ *Lưu ý: {tuition_info.get('note', 'Học phí có thể thay đổi theo từng năm học')}*\n\n"
                    message += "📞 Liên hệ **028 6295 1517** để được tư vấn chi tiết nha!"
                    
                    dispatcher.utter_message(text=message)
                    return [SlotSet("program", program)]
            
            # Nếu không tìm thấy
            dispatcher.utter_message(
                text=f"Ôi bạn ơi, mình chưa có thông tin chi tiết về học phí ngành **{program}** nè.\n\n"
                     "📚 **Các ngành có sẵn:** CNTT, QTKD, Marketing, Kế toán, Ngôn ngữ Anh, "
                     "Du lịch, Tâm lý học, Logistics, Thiết kế đồ họa, Luật.\n\n"
                     "📞 **Hoặc gọi:** 028 6295 1517 để được tư vấn nha!"
            )
        else:
            # Gợi ý nếu không có program
            dispatcher.utter_message(
                text="Bạn ơi, bạn muốn biết học phí của ngành nào nè? 💰\n\n"
                     "📚 **Ví dụ nè:** Học phí ngành Công nghệ thông tin, Học phí CNTT, Học phí Marketing...\n\n"
                     "📋 **Các ngành có sẵn:** CNTT, QTKD, Marketing, Kế toán, Ngôn ngữ Anh, "
                     "Du lịch, Tâm lý học, Logistics, Thiết kế đồ họa, Luật."
            )
        
        return []


class ActionScholarshipCondition(Action):
    def name(self) -> str:
        return "action_scholarship_condition"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        scholarship_type = tracker.get_slot("scholarship_type")
        if not scholarship_type:
            scholarship_type = next(tracker.get_latest_entity_values("scholarship_type"), None)
        
        if scholarship_type:
            scholar_info = find_scholarship_by_id(scholarship_type)
            
            if scholar_info:
                message = f"🎓 **{scholar_info['name']}:**\n\n"
                message += f"💰 **Giá trị:** {scholar_info['value']}\n"
                message += f"⏱️ **Thời gian:** {scholar_info['duration']}\n\n"
                message += f"📋 **Điều kiện:\n**"
                for i, cond in enumerate(scholar_info['conditions'], 1):
                    message += f"  {i}. {cond}\n"
                
                message += f"\n📝 **Cách thức nộp:** {scholar_info['application_process']}\n"
                message += f"📅 **Hạn nộp:** {scholar_info['deadline']}\n\n"
                
                if "required_documents" in scholar_info:
                    message += "📄 **Hồ sơ cần có:**\n"
                    for doc in scholar_info["required_documents"]:
                        message += f"  • {doc}\n"
                    message += "\n"
                
                if "general_info" in SCHOLARSHIPS_DATA:
                    contact = SCHOLARSHIPS_DATA["general_info"].get("contact", {})
                    message += f"📞 **Liên hệ:** {contact.get('phone', '028 7301 5555')}"
                
                dispatcher.utter_message(text=message)
                return []
        
        # Thông tin chung nếu không có loại học bổng cụ thể
        message = "🎓 **Các loại học bổng tại VHU:**\n\n"
        
        if "scholarships" in SCHOLARSHIPS_DATA:
            for scholar in SCHOLARSHIPS_DATA["scholarships"][:4]:  # Hiển thị 4 loại chính
                message += f"✅ **{scholar['name']}:**\n"
                message += f"   💰 {scholar['value']}\n"
                message += f"   📋 {scholar['conditions'][0] if scholar['conditions'] else 'Xem chi tiết'}\n\n"
        
        if "general_info" in SCHOLARSHIPS_DATA:
            gen_info = SCHOLARSHIPS_DATA["general_info"]
            message += f"📊 **Tỷ lệ sinh viên nhận học bổng:** {gen_info.get('percentage_students_receive', 'Cao')}\n"
            contact = gen_info.get("contact", {})
            message += f"📞 **Liên hệ:** {contact.get('phone', '028 7301 5555')}"
        
        dispatcher.utter_message(text=message)
        return []


class ActionProgramInfo(Action):
    def name(self) -> str:
        return "action_program_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        program = tracker.get_slot("program")
        if not program:
            program = next(tracker.get_latest_entity_values("program"), None)
        
        if program:
            prog_info = find_program_by_alias(program)
            
            if prog_info:
                message = f"📚 **Thông tin ngành {prog_info['name']}:**\n\n"
                message += f"📝 **Mô tả:** {prog_info['description']}\n"
                message += f"⏱️ **Thời gian:** {prog_info['duration']}\n"
                message += f"🎓 **Bằng cấp:** {prog_info['degree']}\n\n"
                
                if "subjects" in prog_info:
                    message += "📖 **Các môn học chính:**\n"
                    for subject in prog_info["subjects"][:5]:
                        message += f"  • {subject}\n"
                    message += "\n"
                
                if "career_opportunities" in prog_info:
                    message += "💼 **Cơ hội nghề nghiệp:**\n"
                    for career in prog_info["career_opportunities"][:5]:
                        message += f"  • {career}\n"
                    message += "\n"
                
                message += "📞 **Tư vấn thêm:** 028 7301 5555\n"
                message += "🌐 **Website:** www.vhu.edu.vn"
                
                dispatcher.utter_message(text=message)
                return [SlotSet("program", program)]
            else:
                dispatcher.utter_message(
                    text=f"Mình chưa có thông tin chi tiết về ngành {program}. "
                         "Bạn có thể liên hệ phòng tuyển sinh để được tư vấn cụ thể nhé!"
                )
        else:
            dispatcher.utter_message(
                text="Bạn muốn biết thông tin về ngành nào ạ? "
                     "Ví dụ: Công nghệ thông tin, Marketing, Du lịch..."
            )
        
        return []


class ActionCampusesInfo(Action):
    def name(self) -> str:
        return "action_campuses_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        campus = tracker.get_slot("campus")
        if not campus:
            campus = next(tracker.get_latest_entity_values("campus"), None)
        
        if "campuses" not in CAMPUSES_DATA:
            dispatcher.utter_message("Xin lỗi, hiện chưa có thông tin về cơ sở.")
            return []
        
        campuses = CAMPUSES_DATA["campuses"]
        
        if campus:
            # Tìm cơ sở cụ thể
            campus_lower = campus.lower()
            found_campus = None
            
            for camp in campuses:
                if campus_lower in camp["name"].lower() or campus_lower in camp["id"]:
                    found_campus = camp
                    break
            
            if found_campus:
                message = f"🏫 **{found_campus['name']}:**\n\n"
                message += f"📍 **Địa chỉ:** {found_campus['address']}\n"
                message += f"📞 **Điện thoại:** {found_campus.get('phone', 'N/A')}\n"
                message += f"📧 **Email:** {found_campus.get('email', 'N/A')}\n\n"
                
                if "facilities" in found_campus:
                    message += "🏢 **Cơ sở vật chất:**\n"
                    for facility in found_campus["facilities"]:
                        message += f"  • {facility}\n"
                    message += "\n"
                
                if "programs" in found_campus:
                    message += "📚 **Các ngành đào tạo:**\n"
                    for program in found_campus["programs"]:
                        message += f"  • {program}\n"
                    message += "\n"
                
                if "transport" in found_campus:
                    message += "🚌 **Phương tiện:**\n"
                    for trans in found_campus["transport"]:
                        message += f"  • {trans}\n"
                
                dispatcher.utter_message(text=message)
                return []
        
        # Hiển thị tất cả cơ sở
        message = f"🏫 **Hệ thống {CAMPUSES_DATA.get('general_info', {}).get('total_campuses', len(campuses))} cơ sở của VHU:**\n\n"
        
        for i, camp in enumerate(campuses, 1):
            message += f"**{i}. {camp['name']}:**\n"
            message += f"📍 {camp['address']}\n"
            message += f"📞 {camp.get('phone', 'N/A')}\n\n"
        
        if "general_info" in CAMPUSES_DATA:
            gen_info = CAMPUSES_DATA["general_info"]
            if gen_info.get("shuttle_bus"):
                message += f"🚌 {gen_info['shuttle_bus']}\n\n"
        
        message += "📞 **Liên hệ:** 028 7301 5555"
        
        dispatcher.utter_message(text=message)
        return []


class ActionSupportProblem(Action):
    def name(self) -> str:
        return "action_support_problem"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        support_type = tracker.get_slot("support_type")
        if not support_type:
            support_type = next(tracker.get_latest_entity_values("support_type"), None)
        
        message = "🆘 **Hỗ trợ sinh viên VHU:**\n\n"
        
        # Thông tin từ contacts.json
        if "contact" in CONTACTS_DATA and "departments" in CONTACTS_DATA["contact"]:
            depts = CONTACTS_DATA["contact"]["departments"]
            
            if support_type:
                if "đăng ký" in support_type.lower():
                    dept = depts.get("academic_affairs", {})
                    message += f"📝 **{dept.get('name', 'Phòng Đào tạo')}:**\n"
                    message += f"📞 {dept.get('phone', 'N/A')}\n"
                    message += f"📧 {dept.get('email', 'N/A')}\n"
                elif "học phí" in support_type.lower() or "tài chính" in support_type.lower():
                    dept = depts.get("finance", {})
                    message += f"💰 **{dept.get('name', 'Phòng Tài chính')}:**\n"
                    message += f"📞 {dept.get('phone', 'N/A')}\n"
                    message += f"📧 {dept.get('email', 'N/A')}\n"
                elif "sinh viên" in support_type.lower() or "học bổng" in support_type.lower():
                    dept = depts.get("student_affairs", {})
                    message += f"🎓 **{dept.get('name', 'Phòng CTSV')}:**\n"
                    message += f"📞 {dept.get('phone', 'N/A')}\n"
                    message += f"📧 {dept.get('email', 'N/A')}\n"
                else:
                    message += "📞 **Các phòng ban hỗ trợ:**\n\n"
                    for key, dept in depts.items():
                        message += f"• **{dept.get('name')}:** {dept.get('phone', 'N/A')}\n"
            else:
                message += "📞 **Các phòng ban hỗ trợ:**\n\n"
                for key, dept in depts.items():
                    message += f"• **{dept.get('name')}:** {dept.get('phone', 'N/A')}\n"
        
        if "contact" in CONTACTS_DATA:
            main_contact = CONTACTS_DATA["contact"].get("main_campus", {})
            message += f"\n📞 **Tổng đài:** {main_contact.get('hotline', '028 7301 5555')}"
        
        dispatcher.utter_message(text=message)
        return []


class ActionExamSchedule(Action):
    def name(self) -> str:
        return "action_exam_schedule"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        semester = tracker.get_slot("semester")
        exam_type = tracker.get_slot("exam_type")
        
        message = "📅 **Lịch thi Đại học Văn Hiến:**\n\n"
        
        if "contact" in CONTACTS_DATA:
            website = CONTACTS_DATA["contact"].get("main_campus", {}).get("website", "www.vhu.edu.vn")
            message += f"🖥️ **Xem lịch thi tại:** {website}\n"
            message += "• **VHU Portal:** student.vhu.edu.vn\n"
            message += "• **Bảng thông báo** tại các khoa/phòng\n\n"
        
        if exam_type:
            if "cuối kỳ" in exam_type.lower():
                message += "📝 **Thi cuối kỳ:**\n"
                message += "• Thời gian: Tuần 16-17 của học kỳ\n"
                message += "• Hình thức: Thi trên giấy/online\n"
            elif "giữa kỳ" in exam_type.lower():
                message += "📝 **Thi giữa kỳ:**\n"
                message += "• Thời gian: Tuần 8-9 của học kỳ\n"
                message += "• Hình thức: Theo từng môn\n"
            elif "online" in exam_type.lower():
                message += "💻 **Thi online:**\n"
                message += "• Nền tảng: Google Classroom/LMS\n"
                message += "• Yêu cầu: Camera, micro\n"
        
        message += "\n⚠️ **Lưu ý quan trọng:**\n"
        message += "• Kiểm tra lịch thi thường xuyên\n"
        message += "• Mang thẻ sinh viên khi thi\n"
        message += "• Có mặt trước 15 phút\n\n"
        
        if "contact" in CONTACTS_DATA:
            phone = CONTACTS_DATA["contact"].get("main_campus", {}).get("phone", "028 7301 5555")
            message += f"📞 **Hỗ trợ:** {phone}"
        
        dispatcher.utter_message(text=message)
        return []


class ActionDefaultFallback(Action):
    """Custom fallback action với gợi ý thông minh"""
    
    def name(self) -> str:
        return "action_default_fallback"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        intent = tracker.latest_message.get('intent', {}).get('name')
        confidence = tracker.latest_message.get('intent', {}).get('confidence', 0)
        
        logger.info(f"Fallback triggered - Intent: {intent}, Confidence: {confidence}")
        
        if confidence < 0.5:
            message = "Xin lỗi, mình chưa hiểu rõ câu hỏi của bạn. 😅\n\n"
            message += "Bạn có thể hỏi mình về:\n"
            message += "• 📚 **Học phí các ngành** (VD: học phí CNTT)\n"
            message += "• 🎓 **Học bổng** (VD: điều kiện học bổng)\n"
            message += "• 📝 **Phương thức tuyển sinh**\n"
            message += "• 🏫 **Thông tin cơ sở, địa chỉ**\n"
            message += "• 📞 **Thông tin liên hệ**\n"
            message += "• 📅 **Lịch thi, lịch học**\n\n"
            message += "Hoặc liên hệ: **028 7301 5555** để được tư vấn trực tiếp!"
        else:
            message = "Xin lỗi, mình chưa có thông tin này. 😔\n\n"
            message += "Bạn có thể liên hệ:\n"
            message += "📞 **Hotline:** 028 7301 5555\n"
            message += "📧 **Email:** info@vhu.edu.vn\n"
            message += "🌐 **Website:** www.vhu.edu.vn"
        
        dispatcher.utter_message(text=message)
        return []
