"""
TEST ALL FEATURES - Automated Testing Script
Kiểm tra tự động tất cả các chức năng của Chatbot VHU
"""

import json
import os
from pathlib import Path
from datetime import datetime

# Colors for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_header(text):
    """Print formatted header"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*80}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text.center(80)}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*80}{Colors.END}\n")

def print_success(text):
    """Print success message"""
    print(f"{Colors.GREEN}✅ {text}{Colors.END}")

def print_error(text):
    """Print error message"""
    print(f"{Colors.RED}❌ {text}{Colors.END}")

def print_warning(text):
    """Print warning message"""
    print(f"{Colors.YELLOW}⚠️  {text}{Colors.END}")

def print_info(text):
    """Print info message"""
    print(f"{Colors.BLUE}ℹ️  {text}{Colors.END}")

class ChatbotTester:
    def __init__(self):
        self.base_path = Path("d:/workspace/Chatbot")
        self.results = {
            "total_tests": 0,
            "passed": 0,
            "failed": 0,
            "categories": {}
        }
        self.start_time = datetime.now()
    
    def test_file_exists(self, file_path, description):
        """Test if a file exists"""
        self.results["total_tests"] += 1
        full_path = self.base_path / file_path
        
        if full_path.exists():
            print_success(f"{description}: EXISTS")
            self.results["passed"] += 1
            return True
        else:
            print_error(f"{description}: NOT FOUND - {file_path}")
            self.results["failed"] += 1
            return False
    
    def test_json_structure(self, file_path, required_keys, description):
        """Test JSON file structure"""
        self.results["total_tests"] += 1
        full_path = self.base_path / file_path
        
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            missing_keys = [key for key in required_keys if key not in data]
            
            if not missing_keys:
                print_success(f"{description}: VALID")
                self.results["passed"] += 1
                return True, data
            else:
                print_error(f"{description}: MISSING KEYS {missing_keys}")
                self.results["failed"] += 1
                return False, None
        except Exception as e:
            print_error(f"{description}: ERROR - {str(e)}")
            self.results["failed"] += 1
            return False, None
    
    def test_data_count(self, data, key, expected_min, description):
        """Test if data count meets minimum"""
        self.results["total_tests"] += 1
        
        try:
            if key in data:
                count = len(data[key]) if isinstance(data[key], (list, dict)) else 0
                if count >= expected_min:
                    print_success(f"{description}: {count} items (≥{expected_min})")
                    self.results["passed"] += 1
                    return True
                else:
                    print_error(f"{description}: Only {count} items (expected ≥{expected_min})")
                    self.results["failed"] += 1
                    return False
            else:
                print_error(f"{description}: Key '{key}' not found")
                self.results["failed"] += 1
                return False
        except Exception as e:
            print_error(f"{description}: ERROR - {str(e)}")
            self.results["failed"] += 1
            return False
    
    def run_category(self, category_name):
        """Start a test category"""
        print_header(f"TEST CATEGORY: {category_name}")
        self.results["categories"][category_name] = {
            "tests": 0,
            "passed": 0,
            "failed": 0
        }
    
    def test_configuration_files(self):
        """Test 1: Configuration Files"""
        self.run_category("Configuration Files")
        
        self.test_file_exists("config.yml", "Config file")
        self.test_file_exists("domain.yml", "Domain file")
        self.test_file_exists("credentials.yml", "Credentials file")
        self.test_file_exists("endpoints.yml", "Endpoints file")
    
    def test_nlu_data(self):
        """Test 2: NLU Training Data"""
        self.run_category("NLU Training Data")
        
        self.test_file_exists("data/nlu.yml", "NLU data file")
        self.test_file_exists("data/synonyms.yml", "Synonyms file")
        self.test_file_exists("data/regex_features.yml", "Regex features")
        self.test_file_exists("data/generated_examples.yml", "Generated examples")
    
    def test_conversation_data(self):
        """Test 3: Conversation Data"""
        self.run_category("Conversation Data")
        
        self.test_file_exists("data/rules.yml", "Rules file")
        self.test_file_exists("data/stories.yml", "Stories file")
        self.test_file_exists("data/response_variations.yml", "Response variations")
    
    def test_knowledge_base(self):
        """Test 4: Knowledge Base"""
        self.run_category("Knowledge Base")
        
        # Test tuition.json
        success, tuition_data = self.test_json_structure(
            "data/knowledge_base/tuition.json",
            ["academic_year", "programs", "scholarships"],
            "Tuition data structure"
        )
        
        if success and tuition_data:
            self.test_data_count(
                tuition_data, "programs", 44,
                "Number of programs"
            )
            self.test_data_count(
                tuition_data, "scholarships", 13,
                "Number of scholarships"
            )
            
            # Test CNTT tuition data
            if "programs" in tuition_data:
                programs = tuition_data["programs"]
                cntt_found = False
                
                for code, prog in programs.items():
                    if "công nghệ thông tin" in prog.get("name", "").lower():
                        cntt_found = True
                        print_success(f"CNTT tuition data: {prog.get('tuition_semester_1', 0):,} VNĐ/HK1")
                        break
                
                if not cntt_found:
                    print_error("CNTT tuition data not found")
        
        # Test programs.json
        success, programs_data = self.test_json_structure(
            "data/knowledge_base/programs.json",
            ["programs"],
            "Programs data structure"
        )
        
        if success and programs_data:
            self.test_data_count(
                programs_data, "programs", 40,
                "Number of program definitions"
            )
        
        # Test other knowledge base files
        self.test_file_exists("data/knowledge_base/scholarships.json", "Scholarships KB")
        self.test_file_exists("data/knowledge_base/admission.json", "Admission KB")
        self.test_file_exists("data/knowledge_base/campuses.json", "Campuses KB")
        self.test_file_exists("data/knowledge_base/contacts.json", "Contacts KB")
    
    def test_actions(self):
        """Test 5: Custom Actions"""
        self.run_category("Custom Actions")
        
        self.test_file_exists("actions/__init__.py", "Actions init")
        self.test_file_exists("actions/actions.py", "Main actions file")
        self.test_file_exists("actions/forms.py", "Form actions")
        
        # Check if key actions are defined
        actions_file = self.base_path / "actions/actions.py"
        if actions_file.exists():
            with open(actions_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            key_actions = [
                "ActionTuitionSpecific",
                "ActionScholarshipCondition",
                "ActionProgramInfo",
                "ActionListAllPrograms",
                "ActionCampusesInfo",
                "ActionAdmissionInfo"
            ]
            
            for action in key_actions:
                if action in content:
                    print_success(f"Action defined: {action}")
                else:
                    print_warning(f"Action not found: {action}")
    
    def test_model(self):
        """Test 6: Trained Model"""
        self.run_category("Trained Model")
        
        models_dir = self.base_path / "models"
        
        if models_dir.exists():
            models = list(models_dir.glob("*.tar.gz"))
            
            if models:
                latest_model = max(models, key=lambda p: p.stat().st_mtime)
                print_success(f"Model found: {latest_model.name}")
                
                # Check model age
                model_time = datetime.fromtimestamp(latest_model.stat().st_mtime)
                age_hours = (datetime.now() - model_time).total_seconds() / 3600
                
                if age_hours < 24:
                    print_success(f"Model is fresh ({age_hours:.1f} hours old)")
                else:
                    print_warning(f"Model is {age_hours:.1f} hours old (may need retraining)")
            else:
                print_error("No trained models found")
        else:
            print_error("Models directory not found")
    
    def test_pdf_extraction(self):
        """Test 7: PDF Data Extraction"""
        self.run_category("PDF Data Extraction")
        
        self.test_file_exists(
            "VHU. TB chinh sach hoc phi-hoc bong NH 2025-2026_FInal.pdf",
            "Source PDF file"
        )
        self.test_file_exists(
            "scripts/extract_tuition_from_pdf_v2.py",
            "PDF extraction script"
        )
        self.test_file_exists(
            "scripts/pdf_extracted_text.txt",
            "Extracted PDF text"
        )
    
    def test_documentation(self):
        """Test 8: Documentation"""
        self.run_category("Documentation")
        
        docs = [
            ("README.md", "Main README"),
            ("CHANGELOG.md", "Changelog"),
            ("TEST_ALL_FEATURES.md", "Test documentation"),
            ("START_HERE.md", "Quick start guide"),
            ("docs/UPDATE_TUITION_FROM_PDF.md", "PDF update guide"),
            ("docs/BUOC_2_TRI_TUE_HOI_THOAI.md", "Conversational AI docs"),
        ]
        
        for file_path, desc in docs:
            self.test_file_exists(file_path, desc)
    
    def test_scripts(self):
        """Test 9: Utility Scripts"""
        self.run_category("Utility Scripts")
        
        scripts = [
            ("scripts/test_tuition_data.py", "Data verification script"),
            ("scripts/test_tuition_chatbot.py", "Chatbot test guide"),
            ("scripts/extract_tuition_from_pdf_v2.py", "PDF extractor"),
            ("scripts/README.md", "Scripts documentation"),
        ]
        
        for file_path, desc in scripts:
            self.test_file_exists(file_path, desc)
    
    def test_buoc2_features(self):
        """Test 10: BƯỚC 2 Features"""
        self.run_category("BƯỚC 2 Features")
        
        # Test domain.yml for slots
        domain_file = self.base_path / "domain.yml"
        if domain_file.exists():
            with open(domain_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for key slots
            key_slots = [
                "program",
                "program_id",
                "conversation_stage",
                "previous_programs_mentioned"
            ]
            
            slots_found = sum(1 for slot in key_slots if slot in content)
            
            if slots_found >= 3:
                print_success(f"Slots defined: {slots_found}/{len(key_slots)}")
            else:
                print_warning(f"Only {slots_found}/{len(key_slots)} key slots found")
            
            # Check for forms
            if "forms:" in content:
                print_success("Forms section found in domain")
            else:
                print_warning("Forms section not found in domain")
        
        # Test forms.py
        forms_file = self.base_path / "actions/forms.py"
        if forms_file.exists():
            with open(forms_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            key_forms = [
                "ValidateTuitionForm",
                "ValidateScholarshipForm",
                "ActionAskProgram"
            ]
            
            forms_found = sum(1 for form in key_forms if form in content)
            print_success(f"Form actions defined: {forms_found}/{len(key_forms)}")
    
    def generate_report(self):
        """Generate test report"""
        print_header("TEST SUMMARY REPORT")
        
        duration = (datetime.now() - self.start_time).total_seconds()
        
        print(f"\n{'='*80}")
        print(f"Total Tests:    {self.results['total_tests']}")
        print(f"Passed:         {Colors.GREEN}{self.results['passed']}{Colors.END}")
        print(f"Failed:         {Colors.RED}{self.results['failed']}{Colors.END}")
        
        if self.results['total_tests'] > 0:
            pass_rate = (self.results['passed'] / self.results['total_tests']) * 100
            
            if pass_rate >= 95:
                color = Colors.GREEN
                status = "EXCELLENT ✅"
            elif pass_rate >= 80:
                color = Colors.YELLOW
                status = "GOOD ⚠️"
            else:
                color = Colors.RED
                status = "NEEDS WORK ❌"
            
            print(f"Pass Rate:      {color}{pass_rate:.1f}%{Colors.END} - {status}")
        
        print(f"Duration:       {duration:.1f} seconds")
        print(f"{'='*80}\n")
        
        # Category breakdown
        if self.results['categories']:
            print(f"\n{Colors.BOLD}Category Breakdown:{Colors.END}\n")
            for category, stats in self.results['categories'].items():
                print(f"  {category}:")
                print(f"    Tests: {stats.get('tests', 0)}")
                print(f"    Passed: {stats.get('passed', 0)}")
                print(f"    Failed: {stats.get('failed', 0)}")
        
        # Final verdict
        print(f"\n{Colors.BOLD}FINAL VERDICT:{Colors.END}")
        
        if self.results['failed'] == 0:
            print(f"{Colors.GREEN}{Colors.BOLD}")
            print("  🎉 ALL TESTS PASSED!")
            print("  ✅ Chatbot is ready for production!")
            print(f"{Colors.END}")
        elif self.results['failed'] <= 5:
            print(f"{Colors.YELLOW}{Colors.BOLD}")
            print("  ⚠️  MOSTLY PASSING")
            print(f"  {self.results['failed']} minor issues found")
            print("  📝 Review failed tests and fix if needed")
            print(f"{Colors.END}")
        else:
            print(f"{Colors.RED}{Colors.BOLD}")
            print("  ❌ MULTIPLE FAILURES")
            print(f"  {self.results['failed']} tests failed")
            print("  🔧 Please review and fix issues before deployment")
            print(f"{Colors.END}")
        
        print(f"\n{'='*80}\n")
    
    def run_all_tests(self):
        """Run all test categories"""
        print_header("CHATBOT VHU - AUTOMATED TESTING")
        print_info(f"Started at: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print_info(f"Base path: {self.base_path}\n")
        
        # Run all test categories
        self.test_configuration_files()
        self.test_nlu_data()
        self.test_conversation_data()
        self.test_knowledge_base()
        self.test_actions()
        self.test_model()
        self.test_pdf_extraction()
        self.test_documentation()
        self.test_scripts()
        self.test_buoc2_features()
        
        # Generate report
        self.generate_report()


def main():
    """Main test runner"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}")
    print("╔" + "═"*78 + "╗")
    print("║" + "CHATBOT VHU - COMPREHENSIVE TESTING SUITE".center(78) + "║")
    print("║" + "Version 2.1.0 - October 19, 2025".center(78) + "║")
    print("╚" + "═"*78 + "╝")
    print(f"{Colors.END}\n")
    
    tester = ChatbotTester()
    
    try:
        tester.run_all_tests()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}⚠️  Testing interrupted by user{Colors.END}")
    except Exception as e:
        print(f"\n\n{Colors.RED}❌ Error during testing: {str(e)}{Colors.END}")
        import traceback
        traceback.print_exc()
    
    print_info("Testing complete. See results above.")
    print_info("For manual testing, run: rasa shell\n")


if __name__ == "__main__":
    main()
