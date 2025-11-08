from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, EventType
from typing import Any, Text, Dict, List, Optional
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

# MAPPING tên ngành -> key trong tuition.json
PROGRAM_NAME_TO_TUITION_KEY = {
    # IT & Computer
    "công nghệ thông tin": "information_technology",
    "cntt": "information_technology",
    "it": "information_technology",
    "information technology": "information_technology",
    
    "mạng máy tính và truyền thông": "networking_communications",
    "network": "networking_communications",
    
    # Business & Management
    "quản trị kinh doanh": "business_administration",
    "qtkd": "business_administration",
    "business administration": "business_administration",
    
    "marketing": "marketing",
    "mkt": "marketing",
    
    "kinh doanh thương mại": "commercial_business",
    "thương mại": "commercial_business",
    
    # Accounting & Finance
    "kế toán": "accounting",
    "accounting": "accounting",
    
    "kiểm toán": "auditing",
    "auditing": "auditing",
    
    "tài chính - ngân hàng": "finance_banking",
    "finance banking": "finance_banking",
    
    # Languages
    "ngôn ngữ anh": "english",
    "tiếng anh": "english",
    "english": "english",
    
    "ngôn ngữ trung quốc": "chinese",
    "tiếng trung": "chinese",
    "chinese": "chinese",
    
    "ngôn ngữ nhật": "japanese",
    "tiếng nhật": "japanese",
    "japanese": "japanese",
    
    "ngôn ngữ hàn quốc": "korean",
    "tiếng hàn": "korean",
    "korean": "korean",
    
    "ngôn ngữ pháp": "french",
    "tiếng pháp": "french",
    "french": "french",
    
    # Tourism & Hospitality
    "du lịch": "tourism",
    "tourism": "tourism",
    
    "quản trị khách sạn": "hotel_management",
    "hotel management": "hotel_management",
    
    # Law
    "luật": "law",
    "luật kinh tế": "law",
    "law": "law",
    
    # Logistics
    "logistics và quản lý chuỗi cung ứng": "logistics_supply_chain",
    "logistics": "logistics_supply_chain",
    
    # Nursing & Healthcare
    "điều dưỡng": "nursing",
    "nursing": "nursing",
    
    "y tế công cộng": "public_health",
    "public health": "public_health",
    
    # Media & Arts
    "đạo diễn điện ảnh, truyền hình": "film_directing",
    "film directing": "film_directing",
    "đạo diễn": "film_directing",
    
    "công nghệ điện ảnh": "film_technology",
    "film technology": "film_technology",
    
    "thanh nhạc": "vocal_music",
    "vocal music": "vocal_music",
    
    "piano": "piano",
    
    # Psychology & Social
    "tâm lý học": "psychology",
    "psychology": "psychology",
    
    "xã hội học": "sociology",
    "sociology": "sociology",
    
    # Language & Literature
    "văn học": "literature",
    "literature": "literature",
    
    "việt nam học": "vietnam_studies_vn",
    "vietnam studies": "vietnam_studies_vn",
    
    # Engineering
    "kỹ thuật môi trường": "environmental_engineering",
    "environmental engineering": "environmental_engineering",
    
    "công nghệ sinh học": "biotechnology",
    "biotechnology": "biotechnology",
}


def get_tuition_key_from_program_name(program_name):
    """Chuyển đổi tên ngành sang key trong tuition.json"""
    if not program_name:
        return None
    
    program_lower = program_name.lower().strip()
    return PROGRAM_NAME_TO_TUITION_KEY.get(program_lower, None)


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
    """Tìm học phí theo program_id - Cập nhật cho cấu trúc JSON mới"""
    if not program_id:
        return None
    
    # Cấu trúc mới: {"programs": {"cntt": {...}, "qtkd": {...}}}
    if "programs" in TUITION_DATA:
        program_id_lower = program_id.lower().replace(" ", "_")
        
        # Tìm trực tiếp theo key
        if program_id_lower in TUITION_DATA["programs"]:
            return TUITION_DATA["programs"][program_id_lower]
        
        # Tìm theo tất cả các key (case-insensitive)
        for key, value in TUITION_DATA["programs"].items():
            if key.lower() == program_id_lower:
                return value
    
    # Fallback: cấu trúc cũ
    if "tuition_fees" in TUITION_DATA:
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

class ActionListAllPrograms(Action):
    """Hiển thị danh sách TẤT CẢ các ngành từ programs.json"""
    
    def name(self) -> str:
        return "action_list_all_programs"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        if "programs" not in PROGRAMS_DATA:
            dispatcher.utter_message(text="Xin lỗi, hiện chưa có thông tin về các ngành đào tạo.")
            return []
        
        programs = PROGRAMS_DATA["programs"]
        total = PROGRAMS_DATA.get("total_programs", len(programs))
        
        message = f"📚 **DANH SÁCH TẤT CẢ {total} NGÀNH ĐÀO TẠO TẠI VHU**\n\n"
        
        # Nhóm theo khoa
        faculties = {}
        for prog in programs:
            faculty = prog.get("faculty", "Khác")
            if faculty not in faculties:
                faculties[faculty] = []
            faculties[faculty].append(prog["name"])
        
        # Hiển thị theo từng khoa
        for idx, (faculty, prog_list) in enumerate(faculties.items(), 1):
            message += f"**{idx}. {faculty}** ({len(prog_list)} ngành):\n"
            for i, prog_name in enumerate(prog_list, 1):
                message += f"   {i}. {prog_name}\n"
            message += "\n"
        
        message += "💡 **Bạn muốn biết chi tiết ngành nào không nè?**\n"
        message += "📞 **Liên hệ:** 028 7301 5555 để được tư vấn nha!"
        
        dispatcher.utter_message(text=message)
        return []


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
        
        if program:
            # Tìm program từ JSON
            prog_info = find_program_by_alias(program)
            
            if prog_info:
                # Tìm key trong tuition.json từ tên ngành
                tuition_key = get_tuition_key_from_program_name(prog_info['name'])
                
                # Fallback: thử dùng alias
                if not tuition_key:
                    for alias in prog_info.get('aliases', []):
                        tuition_key = get_tuition_key_from_program_name(alias)
                        if tuition_key:
                            break
                
                # Tìm học phí
                tuition_info = None
                if tuition_key and "programs" in TUITION_DATA:
                    tuition_info = TUITION_DATA["programs"].get(tuition_key)
                
                if tuition_info:
                    # Xử lý cấu trúc JSON mới (từ PDF)
                    if "tuition_semester_1" in tuition_info:
                        credit_fee = tuition_info['tuition_per_credit']
                        semester_1_fee = tuition_info['tuition_semester_1']
                        total_4_years = tuition_info['estimated_total_4_years']
                        
                        # Tạo message thân thiện
                        message = f"Bạn ơi, mình tra giúp bạn học phí nè! 💰\n\n"
                        message += f"📚 **Ngành: {prog_info['name']}**\n"
                        message += f"📅 **Năm học: {TUITION_DATA.get('academic_year', '2025-2026')}**\n\n"
                        
                        message += "💡 **Chi tiết học phí:**\n"
                        message += f"├─ Học phí/tín chỉ: **{credit_fee:,} VNĐ**\n"
                        message += f"├─ Học kỳ 1 (12 tín chỉ): **{semester_1_fee:,} VNĐ** (~{semester_1_fee/1000000:.1f} triệu)\n"
                        message += f"└─ Ước tính 4 năm (8 học kỳ): **~{total_4_years:,} VNĐ** (~{total_4_years/1000000:.1f} triệu)\n\n"
                        
                        # Thông tin học bổng
                        if "scholarships" in TUITION_DATA and TUITION_DATA["scholarships"]:
                            message += "🎓 **Học bổng có sẵn:**\n"
                            scholarships = TUITION_DATA["scholarships"][:3]  # Hiển thị 3 loại đầu
                            for idx, sch in enumerate(scholarships, 1):
                                message += f"{idx}. {sch['description']}\n"
                            message += "\n"
                        
                        # Ghi chú từ PDF
                        if "notes" in TUITION_DATA and TUITION_DATA["notes"]:
                            note = TUITION_DATA["notes"][0]  # Lấy ghi chú đầu tiên
                            message += f"ℹ️ *{note}*\n\n"
                        
                        message += "📞 **Liên hệ:** 1800 1568 (miễn phí) | Email: tuyensinh@vhu.edu.vn"
                        
                    else:
                        # Xử lý cấu trúc cũ
                        credit_fee = tuition_info.get('fee_per_credit', 0)
                        total_credits = tuition_info.get('total_credits', 120)
                        total_fee = credit_fee * total_credits
                        fee_per_semester = total_fee / 8
                        
                        message = f"Bạn ơi, mình tra giúp bạn học phí nè! 💰\n\n"
                        message += f"📚 **Ngành: {prog_info['name']}**\n\n"
                        message += "💡 **Chi tiết học phí:**\n"
                        message += f"├─ Học phí/tín chỉ: **{credit_fee:,} VNĐ**\n"
                        message += f"├─ Tổng số tín chỉ: **{total_credits} tín chỉ**\n"
                        message += f"└─ Ước tính mỗi học kỳ: **~{fee_per_semester:,.0f} VNĐ**\n\n"
                        message += "📞 Liên hệ **028 6295 1517** để được tư vấn chi tiết nha!"
                    
                    dispatcher.utter_message(text=message)
                    return [SlotSet("program", program)]
            
            # Nếu không tìm thấy
            dispatcher.utter_message(
                text=f"Ôi bạn ơi, mình chưa có thông tin chi tiết về học phí ngành **{program}** nè.\n\n"
                     "📚 **Có 43 ngành đào tạo tại VHU:** CNTT, QTKD, Marketing, Kế toán, "
                     "Ngôn ngữ Anh, Luật, Du lịch, Tâm lý học, và nhiều ngành khác.\n\n"
                     "📞 **Gọi ngay:** 1800 1568 (miễn phí) để được tư vấn nha!"
            )
        else:
            # Gợi ý nếu không có program
            dispatcher.utter_message(
                text="Bạn ơi, bạn muốn biết học phí của ngành nào nè? 💰\n\n"
                     "📚 **Ví dụ nè:** Học phí ngành Công nghệ thông tin, Học phí CNTT, Học phí Marketing...\n\n"
                     "📋 **VHU có 43 ngành đào tạo.** Bạn hỏi ngành nào cũng được nha!"
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
        
        # Lấy location nếu có (để tìm theo quận/địa chỉ)
        location = next(tracker.get_latest_entity_values("location"), None)
        
        # Lấy danh sách cơ sở (cấu trúc mới hoặc cũ)
        all_locations = []
        if "headquarters" in CAMPUSES_DATA:
            all_locations.append(CAMPUSES_DATA["headquarters"])
        if "training_campuses" in CAMPUSES_DATA:
            all_locations.extend(CAMPUSES_DATA["training_campuses"])
        elif "campuses" in CAMPUSES_DATA:
            all_locations = CAMPUSES_DATA["campuses"]
          # Kiểm tra nếu không có dữ liệu
        if not all_locations:
            dispatcher.utter_message("Xin lỗi, hiện chưa có thông tin về cơ sở.")
            return []
        
        # Ưu tiên tìm theo campus name, sau đó mới đến location
        search_term = campus or location
        
        if search_term:
            # Tìm cơ sở cụ thể
            search_lower = search_term.lower()
            found_campus = None
            
            for camp in all_locations:
                camp_name = camp.get("name", "")
                camp_id = camp.get("id", "")
                camp_address = camp.get("address", "")
                  # Search trong name, id, hoặc address
                if (search_lower in camp_name.lower() or 
                    search_lower in camp_id.lower() or 
                    search_lower in camp_address.lower()):
                    found_campus = camp
                    break
            
            if found_campus:
                message = f"🏫 **{found_campus['name']}:**\n\n"
                message += f"📍 **Địa chỉ:** {found_campus['address']}\n"
                
                if "phone" in found_campus:
                    message += f"📞 **Điện thoại:** {found_campus['phone']}\n"
                if "hotline" in found_campus:
                    message += f"📞 **Hotline:** {found_campus['hotline']}\n"
                if "email" in found_campus:
                    message += f"📧 **Email:** {found_campus['email']}\n"
                
                message += "\n"
                
                if "description" in found_campus:
                    message += f"📝 **Mô tả:** {found_campus['description']}\n\n"
                
                if "facilities" in found_campus:
                    message += "🏢 **Cơ sở vật chất:**\n"
                    for facility in found_campus["facilities"][:5]:
                        message += f"  • {facility}\n"
                    message += "\n"
                
                if "programs_available" in found_campus:
                    message += "📚 **Các ngành đào tạo:**\n"
                    for program in found_campus["programs_available"][:5]:
                        message += f"  • {program}\n"
                    message += "\n"
                
                if "transport" in found_campus:
                    message += "🚌 **Phương tiện:**\n"
                    for trans in found_campus["transport"]:
                        message += f"  • {trans}\n"
                    message += "\n"
                
                message += "📞 **Liên hệ thêm:** 1800 1568 (miễn phí)"
                dispatcher.utter_message(text=message)
                return []
        
        # Hiển thị tất cả cơ sở
        general_info = CAMPUSES_DATA.get('general_info', {})
        total_locations = general_info.get('total_locations', len(all_locations))
        main_campus = general_info.get('main_campus', 1)
        training_campuses = general_info.get('training_campuses', len(all_locations) - 1)
        
        message = f"🏫 **VHU có tổng cộng {total_locations} cơ sở:**\n"
        message += f"   • {main_campus} cơ sở chính (trụ sở)\n"
        message += f"   • {training_campuses} cơ sở đào tạo\n\n"
        
        # Hiển thị trụ sở chính
        if "headquarters" in CAMPUSES_DATA:
            hq = CAMPUSES_DATA["headquarters"]
            message += f"**🏢 TRỤ SỞ CHÍNH:**\n"
            message += f"• **{hq['name']}**\n"
            message += f"  📍 {hq['address']}\n"
            message += f"  ☎️ {hq.get('hotline', hq.get('phone', 'N/A'))}\n\n"
        
        # Hiển thị TẤT CẢ các cơ sở đào tạo
        if "training_campuses" in CAMPUSES_DATA:
            message += f"**📚 CÁC CƠ SỞ ĐÀO TẠO:**\n\n"
            for i, camp in enumerate(CAMPUSES_DATA["training_campuses"], 1):
                message += f"**{i}. {camp['name']}**\n"
                message += f"   📍 {camp['address']}\n"
                message += f"   ☎️ {camp.get('phone', '028 6295 1517')}\n"
                message += "\n"
        
        # Thông tin chung
        message += "─" * 50 + "\n\n"
        
        if "shuttle_bus" in CAMPUSES_DATA:
            shuttle = CAMPUSES_DATA["shuttle_bus"]
            if shuttle.get("available"):
                message += f"🚌 **Xe đưa đón:** {shuttle.get('note', 'Có')}"
                if shuttle.get('free_for_students'):
                    message += " (Miễn phí cho sinh viên)\n"
                else:
                    message += "\n"
        
        if "contact" in CAMPUSES_DATA:
            contact = CAMPUSES_DATA["contact"]
            message += f"📞 **Tổng đài:** {contact.get('main_hotline', '1800 1568')} (miễn phí)\n"
            message += f"📧 **Email:** {contact.get('email', 'tuyensinh@vhu.edu.vn')}\n"
            message += f"🌐 **Website:** {contact.get('website', 'www.vhu.edu.vn')}"
        
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


# =============================================================================
# CHỨC NĂNG MỚI - CHỈ ĐƯỜNG (GOONG MAPS API)
# =============================================================================

class ActionGetDirections(Action):
    """Lấy hướng dẫn đường đi từ vị trí user đến cơ sở VHU"""
    
    def name(self) -> Text:
        return "action_get_directions"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        from actions.goong_maps_api import (
            geocode_address,
            get_directions,
            format_directions_message
        )
        
        user_location = tracker.get_slot("user_location")
        target_campus_input = tracker.get_slot("target_campus")
        
        if not user_location or not target_campus_input:
            dispatcher.utter_message(text="⚠️ Mình cần biết vị trí của bạn và cơ sở bạn muốn đến nha!")
            return []
          # Parse campus selection (số hoặc tên)
        campus_mapping = {
            "1": "tru-so-chinh",
            "trụ sở": "tru-so-chinh",
            "trụ sở chính": "tru-so-chinh",
            "hunghau house": "tru-so-chinh",
            "2": "harmony-campus",
            "harmony": "harmony-campus",
            "3": "hunghau-campus",
            "hunghau": "hunghau-campus",
            "hunghau campus": "hunghau-campus",
            "4": "myu-campus",
            "myu": "myu-campus",
            "5": "nguyen-ba-tuyen-campus",
            "nguyễn bá tuyển": "nguyen-ba-tuyen-campus",
            "nguyen ba tuyen": "nguyen-ba-tuyen-campus",
            "6": "quoc-lo-1a-campus",
            "quốc lộ 1a": "quoc-lo-1a-campus",
            "quoc lo 1a": "quoc-lo-1a-campus",
            "7": "615-au-co-campus",
            "615 âu cơ": "615-au-co-campus",
            "615 au co": "615-au-co-campus"
        }
        
        target_campus_id = campus_mapping.get(target_campus_input.lower().strip())
        
        if not target_campus_id:
            # Thử tìm trong input
            for key, value in campus_mapping.items():
                if key in target_campus_input.lower():
                    target_campus_id = value
                    break
        
        if not target_campus_id:
            dispatcher.utter_message(text="⚠️ Mình không tìm thấy cơ sở này. Bạn thử chọn lại bằng số (1-7) nha!")
            return []
        
        # Lấy thông tin cơ sở từ CAMPUSES_DATA
        campus_info = None
        campus_name = ""
        campus_address = ""
        campus_transport = []
        
        # Tìm trong headquarters
        if target_campus_id == CAMPUSES_DATA.get("headquarters", {}).get("id"):
            campus_info = CAMPUSES_DATA["headquarters"]
            campus_name = campus_info["name"]
            campus_address = campus_info["address"]
        else:
            # Tìm trong training_campuses
            for campus in CAMPUSES_DATA.get("training_campuses", []):
                if campus["id"] == target_campus_id:
                    campus_info = campus
                    campus_name = campus["name"]
                    campus_address = campus["address"]
                    campus_transport = campus.get("transport", [])
                    break
        
        if not campus_info:
            dispatcher.utter_message(text="⚠️ Không tìm thấy thông tin cơ sở này!")
            return []
          # Thông báo đang xử lý
        dispatcher.utter_message(response="utter_directions_processing")
        
        # 1. Geocode vị trí user
        user_coords = geocode_address(user_location)
        if not user_coords:
            dispatcher.utter_message(
                text=f"⚠️ Mình không tìm thấy địa chỉ **'{user_location}'**.\n\n"
                     "💡 Bạn thử nhập cụ thể hơn nhé (VD: '123 Lê Văn Việt, Quận 9')"
            )
            return []
        
        # 2. Lấy tọa độ cơ sở VHU (ƯU TIÊN từ campuses.json)
        campus_coords = campus_info.get("coordinates")
        if not campus_coords:
            # Fallback: Geocode địa chỉ nếu không có tọa độ trong JSON
            campus_coords = geocode_address(campus_address)
        
        if not campus_coords:
            dispatcher.utter_message(
                text=f"⚠️ Không thể tìm tọa độ của {campus_name}. Vui lòng thử lại sau!"
            )
            return []
          # 3. Gọi Directions API
        directions = get_directions(
            user_coords["lat"], user_coords["lng"],
            campus_coords["lat"], campus_coords["lng"],
            vehicle="bike"
        )
        
        # 4. Format và gửi message (với địa chỉ chính xác từ campuses.json)
        message = format_directions_message(directions, campus_name, user_location, campus_address)
        dispatcher.utter_message(text=message)
        
        # Lưu thông tin để dùng cho transit info
        return [
            SlotSet("want_transit_info", None),  # Reset
            SlotSet("target_campus", target_campus_id)  # Lưu lại campus đã chọn
        ]


class ActionShowTransitInfo(Action):
    """Hiển thị thông tin xe buýt đến cơ sở VHU"""
    
    def name(self) -> Text:
        return "action_show_transit_info"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        from actions.goong_maps_api import get_transit_info
        
        user_location = tracker.get_slot("user_location")
        target_campus_id = tracker.get_slot("target_campus")
        
        if not target_campus_id:
            dispatcher.utter_message(text="⚠️ Mình cần biết cơ sở bạn muốn đến trước nha!")
            return []
        
        # Lấy thông tin cơ sở
        campus_info = None
        campus_name = ""
        campus_transport = []
        
        if target_campus_id == CAMPUSES_DATA.get("headquarters", {}).get("id"):
            campus_info = CAMPUSES_DATA["headquarters"]
            campus_name = campus_info["name"]
        else:
            for campus in CAMPUSES_DATA.get("training_campuses", []):
                if campus["id"] == target_campus_id:
                    campus_info = campus
                    campus_name = campus["name"]
                    campus_transport = campus.get("transport", [])
                    break
        
        if not campus_info:
            dispatcher.utter_message(text="⚠️ Không tìm thấy thông tin cơ sở!")
            return []
        
        # Lấy và gửi thông tin xe buýt
        transit_message = get_transit_info(user_location, campus_name, campus_transport)
        dispatcher.utter_message(text=transit_message)
        
        return []

# =============================================================================
# GEMINI AI FALLBACK - XỬ LÝ CÂU HỎI NGOÀI PHẠM VI
# =============================================================================

class ActionGeminiFallback(Action):
    """Xử lý câu hỏi ngoài phạm vi bằng Gemini AI"""
    
    def name(self) -> Text:
        return "action_gemini_fallback"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        from actions.gemini_config import get_gemini_response
        
        # Lấy câu hỏi cuối cùng của user
        user_message = tracker.latest_message.get("text", "")
        
        if not user_message:
            dispatcher.utter_message(text="Mình không hiểu bạn nói gì. Bạn thử hỏi lại nha! 😊")
            return []
        
        # Gọi Gemini AI
        gemini_response = get_gemini_response(user_message)
        
        # Gửi response
        dispatcher.utter_message(text=gemini_response)
        
        return []

# =============================================================================
# CUSTOM ASK ACTIONS - CHO DIRECTIONS FORM
# =============================================================================

class ActionAskUserLocation(Action):
    """Custom action để hỏi vị trí user"""
    
    def name(self) -> Text:
        return "action_ask_user_location"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        dispatcher.utter_message(response="utter_ask_user_location")
        return []


class ActionAskTargetCampus(Action):
    """Custom action để hỏi cơ sở muốn đến"""
    
    def name(self) -> Text:
        return "action_ask_target_campus"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        dispatcher.utter_message(response="utter_ask_target_campus")
        return []


# ============================================
# ACTION: RESET SLOTS CHO TƯ VẤN NGÀNH HỌC
# ============================================

class ActionSetSlotsToNone(Action):
    """
    Reset các slots liên quan đến tư vấn ngành học
    Dùng để tránh NLU extract entity nhầm từ câu hỏi trigger
    """
    
    def name(self) -> Text:
        return "action_set_slots_to_none"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        return [
            SlotSet("subject_combination", None),
            SlotSet("interest", None),
            SlotSet("recommended_programs", None)
        ]


# ============================================
# ACTION: TƯ VẤN NGÀNH HỌC
# ============================================

class ActionRecommendPrograms(Action):
    """
    Tư vấn ngành học dựa trên tổ hợp môn và sở thích
    """
    
    def name(self) -> Text:
        return "action_recommend_programs"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Lấy subject_combination và interest từ entities hoặc slots
        subject_combo = None
        interest = None
        
        # 1. Thử lấy từ entities trong message cuối
        latest_message = tracker.latest_message or {}
        entities = latest_message.get("entities", [])
        for entity in entities:
            if entity["entity"] == "subject_combination":
                subject_combo = entity["value"]
            elif entity["entity"] == "interest":
                interest = entity["value"]
          # 2. Nếu không có, lấy từ slots
        if not subject_combo:
            subject_combo = tracker.get_slot("subject_combination")
        if not interest:
            interest = tracker.get_slot("interest")
        
        # 3. VALIDATE: Phải có ít nhất 1 trong 2 thông tin hợp lệ
        # Nếu không có cả 2, hoặc có nhưng quá ngắn (< 2 ký tự) → hỏi lại
        valid_subject = subject_combo and len(str(subject_combo).strip()) >= 2
        valid_interest = interest and len(str(interest).strip()) >= 2
        
        if not valid_subject and not valid_interest:
            dispatcher.utter_message(
                text="Để mình tư vấn ngành phù hợp, bạn cho mình biết:\n\n"
                     "1️⃣ **Tổ hợp môn** của bạn là gì? (VD: A00, A01, C00, D01...)\n"
                     "2️⃣ **Sở thích** hoặc ngành bạn quan tâm? (VD: công nghệ, kinh doanh, tài chính...)\n\n"
                     "📝 Ví dụ: _'Tôi học khối A00 và thích công nghệ'_"
            )
            return []
        
        # Normalize tổ hợp môn
        combo_mapping = {
            "a00": "A00", "a 00": "A00", "toán lý hóa": "A00", "toan ly hoa": "A00",
            "a01": "A01", "a 01": "A01", "toán lý anh": "A01", "toan ly anh": "A01",
            "a02": "A02", "a 02": "A02", "toán lý sinh": "A02",
            "b00": "B00", "b 00": "B00", "toán hóa sinh": "B00",
            "c00": "C00", "c 00": "C00", "văn sử địa": "C00", "van su dia": "C00",
            "c01": "C01", "c 01": "C01", "văn toán lý": "C01",
            "c04": "C04", "c 04": "C04", "văn sử anh": "C04",
            "d01": "D01", "d 01": "D01", "toán anh văn": "D01", "toan anh van": "D01",
            "d07": "D07", "d 07": "D07", "toán hóa anh": "D07",
        }
        
        if subject_combo:
            subject_combo_normalized = combo_mapping.get(subject_combo.lower().strip(), subject_combo.upper())
        else:
            subject_combo_normalized = None
        
        # Tìm ngành phù hợp
        recommended = self._find_matching_programs(subject_combo_normalized, interest)
        
        if not recommended:
            dispatcher.utter_message(
                text=f"🤔 Mình không tìm thấy ngành phù hợp với:\n"
                     f"- Tổ hợp: {subject_combo_normalized or 'Chưa có'}\n"
                     f"- Sở thích: {interest or 'Chưa có'}\n\n"
                     f"💡 Bạn thử nhập lại tổ hợp môn và sở thích cụ thể hơn nhé!"
            )
            return []
        
        # Format message
        message = "🎓 **TƯ VẤN NGÀNH HỌC DÀNH CHO BẠN**\n\n"
        
        if subject_combo_normalized:
            message += f"📚 **Tổ hợp môn:** {subject_combo_normalized}\n"
        
        if interest:
            message += f"💡 **Sở thích:** {interest}\n"
        
        message += f"\n🌟 **Top {min(5, len(recommended))} ngành phù hợp:**\n\n"
        
        for i, prog in enumerate(recommended[:5], 1):
            emoji = "🌟" if i == 1 else "⭐" if i == 2 else "✨"
            message += f"{emoji} **{i}. {prog['name']}**\n"
            message += f"   📖 {prog['description'][:100]}...\n"
            
            if subject_combo_normalized and subject_combo_normalized in prog.get('admission_methods', {}).get('combination', []):
                message += f"   ✅ Phù hợp tổ hợp {subject_combo_normalized}\n"
            
            if interest and prog['score'] > 60:
                message += f"   💡 Phù hợp với sở thích '{interest}'\n"
            
            message += f"   💼 **Ra trường làm:** {', '.join(prog.get('career_opportunities', [])[:3])}\n"
            message += f"   💰 **Học phí:** ~{prog.get('tuition', {}).get('per_year', 'N/A')}\n\n"
        
        message += "📞 Liên hệ **1800 1568** để được tư vấn chi tiết hơn nha! 😊"
        
        dispatcher.utter_message(text=message)
        
        return [
            SlotSet("recommended_programs", [p.get('code', p.get('id', '')) for p in recommended[:5]]),
            SlotSet("subject_combination", subject_combo_normalized),
            SlotSet("interest", interest)
        ]
    
    def _find_matching_programs(self, subject_combo: Optional[str], interest: Optional[str]) -> List[Dict]:
        """
        Tìm và xếp hạng các ngành phù hợp
        """
        # Interest keywords
        interest_keywords = {
            "công nghệ": ["công nghệ", "cntt", "it", "lập trình", "máy tính", "mạng", "phần mềm"],
            "kinh doanh": ["kinh doanh", "marketing", "quản trị", "thương mại", "bán hàng"],
            "tài chính": ["tài chính", "kế toán", "ngân hàng", "kiểm toán", "thuế"],
            "luật": ["luật", "pháp luật", "công chứng", "tư vấn pháp lý"],
            "du lịch": ["du lịch", "khách sạn", "nhà hàng", "lữ hành", "tour"],
            "ngoại ngữ": ["ngoại ngữ", "tiếng anh", "tiếng nhật", "tiếng trung", "anh văn"],
            "thiết kế": ["thiết kế", "đồ họa", "kiến trúc", "nội thất", "design"],
            "truyền thông": ["truyền thông", "báo chí", "media", "quảng cáo", "pr"],
        }
        
        results = []
        
        # Lấy danh sách programs từ PROGRAMS_DATA
        programs_list = PROGRAMS_DATA.get("programs", [])
        
        for program in programs_list:
            score = 0
            
            # 1. Điểm tổ hợp môn (60 điểm)
            if subject_combo:
                admission_combos = program.get('admission_methods', {}).get('combination', [])
                if subject_combo in admission_combos:
                    score += 60
            
            # 2. Điểm sở thích (40 điểm)
            if interest:
                interest_lower = interest.lower()
                
                # Tìm keywords liên quan
                related_keywords = []
                for key, keywords in interest_keywords.items():
                    if any(kw in interest_lower for kw in keywords):
                        related_keywords.extend(keywords)
                
                if not related_keywords:
                    related_keywords = [interest_lower]
                
                # Check trong tên, mô tả, career
                searchable_text = (
                    program.get('name', '').lower() + " " +
                    program.get('description', '').lower() + " " +
                    " ".join(program.get('career_opportunities', [])).lower()
                )
                
                matches = sum(1 for kw in related_keywords if kw in searchable_text)
                if matches > 0:
                    score += min(40, matches * 20)  # Max 40 điểm
            
            if score > 0:
                results.append({
                    **program,
                    'score': score
                })
        
        # Sắp xếp theo điểm giảm dần
        results.sort(key=lambda x: x['score'], reverse=True)
        
        return results

