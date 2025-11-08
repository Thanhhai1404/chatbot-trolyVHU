"""
Form Actions - Thu thập thông tin thiếu từ user
Giúp bot có thể hỏi lại khi thiếu thông tin cần thiết
"""
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, EventType
from rasa_sdk.types import DomainDict
import logging

logger = logging.getLogger(__name__)

# =============================================================================
# TUITION INQUIRY FORM - Thu thập thông tin để tra học phí
# =============================================================================

class ValidateTuitionForm(FormValidationAction):
    """Validate và thu thập thông tin ngành để tra học phí"""
    
    def name(self) -> Text:
        return "validate_tuition_form"
    
    def validate_program(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate program slot"""
        
        if not slot_value:
            dispatcher.utter_message(
                text="Bạn ơi, bạn muốn hỏi học phí của ngành nào nè? 💰\n\n"
                     "Ví dụ: CNTT, Marketing, Kế toán, Tâm lý học..."
            )
            return {"program": None}
        
        # TODO: Validate with programs.json
        return {"program": slot_value}


# =============================================================================
# SCHOLARSHIP INQUIRY FORM - Thu thập thông tin để tra học bổng
# =============================================================================

class ValidateScholarshipForm(FormValidationAction):
    """Validate và thu thập thông tin học bổng"""
    
    def name(self) -> Text:
        return "validate_scholarship_form"
    
    def validate_scholarship_type(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate scholarship_type slot"""
        
        if not slot_value:
            dispatcher.utter_message(
                text="Bạn muốn biết về học bổng nào nè? 🎓\n\n"
                     "VHU có các loại học bổng:\n"
                     "• Khuyến khích học tập\n"
                     "• Tài năng\n"
                     "• Hoàn cảnh khó khăn\n"
                     "• Toàn phần/một phần"
            )
            return {"scholarship_type": None}
        
        return {"scholarship_type": slot_value}
    
    def validate_program(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate program for scholarship inquiry (optional)"""
        
        # Program is optional for scholarship
        return {"program": slot_value}


# =============================================================================
# ADMISSION FORM - Thu thập thông tin tuyển sinh
# =============================================================================

class ValidateAdmissionForm(FormValidationAction):
    """Validate thông tin tuyển sinh"""
    
    def name(self) -> Text:
        return "validate_admission_form"
    
    def validate_program(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate program for admission"""
        
        if not slot_value:
            dispatcher.utter_message(
                text="Bạn muốn tìm hiểu tuyển sinh ngành nào nè? 📝\n\n"
                     "Có thể nói tên ngành hoặc mã ngành luôn nha!"
            )
            return {"program": None}
        
        return {"program": slot_value}
    
    def validate_user_student_type(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate student type (optional)"""
        
        # Student type is optional
        return {"user_student_type": slot_value}


# =============================================================================
# CAMPUS INFO FORM - Thu thập thông tin cơ sở
# =============================================================================

class ValidateCampusForm(FormValidationAction):
    """Validate thông tin cơ sở"""
    
    def name(self) -> Text:
        return "validate_campus_form"
    
    def validate_campus(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate campus"""
        
        if not slot_value:
            dispatcher.utter_message(
                text="Bạn muốn biết về cơ sở nào nè? 🏫\n\n"
                     "VHU có 7 địa điểm:\n"
                     "• HungHau House (Trụ sở - Tân Phú)\n"
                     "• Harmony Campus (Tân Bình)\n"
                     "• HungHau Campus (Bình Chánh)\n"
                     "• myU Campus (Quận 3)\n"
                     "• Nguyễn Bá Tuyển (Tân Bình)\n"
                     "• Quốc lộ 1A (Quận 12)\n"
                     "• 615 Âu Cơ (Tân Phú)"
            )
            return {"campus": None}
        
        # Không cần normalize nữa, trả về giá trị user nhập
        return {"campus": slot_value}


# =============================================================================
# ACTION: ASK FOR PROGRAM - Hỏi ngành khi thiếu thông tin
# =============================================================================

class ActionAskProgram(Action):
    """Custom action để hỏi ngành với variations"""
    
    def name(self) -> Text:
        return "action_ask_program"
    
    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[EventType]:
        
        # Các cách hỏi khác nhau để tránh lặp lại
        questions = [
            "Bạn muốn hỏi về ngành nào nè? 🎓",
            "Ngành nào bạn quan tâm vậy? 😊",
            "Cho mình biết tên ngành bạn đang tìm hiểu nha! 📚",
            "Bạn đang tìm hiểu ngành gì đấy? 💡",
        ]
        
        # Random pick (hoặc dựa vào conversation_stage)
        import random
        question = random.choice(questions)
        
        dispatcher.utter_message(text=question)
        
        return []


# =============================================================================
# ACTION: ASK FOR SCHOLARSHIP TYPE
# =============================================================================

class ActionAskScholarshipType(Action):
    """Custom action để hỏi loại học bổng"""
    
    def name(self) -> Text:
        return "action_ask_scholarship_type"
    
    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[EventType]:
        
        message = "Bạn muốn biết về học bổng nào nè? 🎓\n\n"
        message += "VHU có các loại:\n"
        message += "• 💯 Học bổng khuyến khích học tập\n"
        message += "• 🌟 Học bổng tài năng\n"
        message += "• 🤝 Học bổng hoàn cảnh\n"
        message += "• 📊 Học bổng toàn phần/một phần"
        
        dispatcher.utter_message(text=message)
        
        return []


# =============================================================================
# ACTION: ASK FOR CAMPUS
# =============================================================================

class ActionAskCampus(Action):
    """Custom action để hỏi cơ sở"""
    
    def name(self) -> Text:
        return "action_ask_campus"
    
    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[EventType]:
        
        message = "Bạn muốn biết về cơ sở nào nè? 🏫\n\n"
        
        # Trụ sở chính
        message += "**🏢 TRỤ SỞ CHÍNH:**\n"
        message += "• HungHau House - 613 Âu Cơ, Tân Phú\n\n"
        
        # 6 cơ sở đào tạo
        message += "**📚 CÁC CƠ SỞ ĐÀO TẠO:**\n"
        message += "1. Harmony Campus - 624 Âu Cơ, Tân Bình\n"
        message += "2. HungHau Campus - 13E Nguyễn Văn Linh, Bình Chánh\n"
        message += "3. myU Campus - 665-667-669 Điện Biên Phủ, Quận 3\n"
        message += "4. Nguyễn Bá Tuyển - 8-14 Nguyễn Bá Tuyển, Tân Bình\n"
        message += "5. Quốc lộ 1A - 2A2 Quốc lộ 1A, Quận 12\n"
        message += "6. 615 Âu Cơ - 615 Âu Cơ, Tân Phú\n\n"
        
        message += "📞 Hotline: 1800 1568 (miễn phí)"
        
        dispatcher.utter_message(text=message)
        
        return []


# =============================================================================
# ACTION: TRACK CONVERSATION STAGE
# =============================================================================

class ActionTrackConversation(Action):
    """Track conversation stage để điều chỉnh responses"""
    
    def name(self) -> Text:
        return "action_track_conversation"
    
    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[EventType]:
        
        # Get current intent
        intent = tracker.latest_message.get('intent', {}).get('name')
        
        # Get current slots
        program = tracker.get_slot("program")
        scholarship_type = tracker.get_slot("scholarship_type")
        
        # Determine conversation stage
        if intent == "greet":
            stage = "greeting"
        elif intent in ["goodbye", "thank"]:
            stage = "closing"
        elif program or scholarship_type:
            stage = "specific_query"
        elif intent in ["ask_list_programs", "ask_about_school"]:
            stage = "exploring"
        else:
            stage = "follow_up"
        
        # Update topics discussed
        topics = tracker.get_slot("topics_discussed") or []
        if intent and intent not in topics:
            topics.append(intent)
        
        return [
            SlotSet("conversation_stage", stage),
            SlotSet("last_intent", intent),
            SlotSet("topics_discussed", topics)
        ]

# =============================================================================
# DIRECTIONS FORM - Thu thập thông tin để chỉ đường (CHỨC NĂNG MỚI)
# =============================================================================

class ValidateDirectionsForm(FormValidationAction):
    """Validate và thu thập thông tin để chỉ đường"""
    
    def name(self) -> Text:
        return "validate_directions_form"
    
    def validate_user_location(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate địa chỉ user nhập"""
        
        if not slot_value or len(slot_value.strip()) < 3:
            dispatcher.utter_message(
                text="Bạn ơi, cho mình biết địa chỉ cụ thể hơn nha! 📍\n\n"
                     "Ví dụ:\n"
                     "• 'Tôi ở đường Tân Hương, Tân Phú'\n"
                     "• 'Quận 9'\n"
                     "• '123 Lê Văn Việt, Quận 9'"
            )
            return {"user_location": None}
        
        # Accept địa chỉ
        return {"user_location": slot_value.strip()}
    
    def validate_target_campus(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate cơ sở user chọn"""
        
        if not slot_value:
            dispatcher.utter_message(response="utter_ask_target_campus")
            return {"target_campus": None}
          # Mapping các cách nhập (7 cơ sở mới)
        valid_inputs = [
            "1", "2", "3", "4", "5", "6", "7",
            "trụ sở", "harmony", "hunghau", "myu", 
            "nguyễn bá tuyển", "quốc lộ", "615"
        ]
        
        slot_lower = slot_value.lower().strip()
        
        # Check xem có match không
        is_valid = any(valid in slot_lower for valid in valid_inputs)
        
        if not is_valid:
            dispatcher.utter_message(
                text="⚠️ Mình không hiểu bạn chọn cơ sở nào.\n\n"
                     "Bạn có thể chọn bằng số (1-7) hoặc tên cơ sở nha! 😊"
            )
            dispatcher.utter_message(response="utter_ask_target_campus")
            return {"target_campus": None}
        
        return {"target_campus": slot_value.strip()}
