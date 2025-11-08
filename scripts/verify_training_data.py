#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verify Training Data Completeness
Kiểm tra xem training data đã đủ cho 44 ngành chưa
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Set

# Paths
BASE_DIR = Path(__file__).parent.parent
PROGRAMS_JSON = BASE_DIR / "data" / "knowledge_base" / "programs.json"
SYNONYMS_YML = BASE_DIR / "data" / "synonyms.yml"
NLU_YML = BASE_DIR / "data" / "nlu.yml"

def load_programs() -> List[str]:
    """Load all program names from programs.json"""
    with open(PROGRAMS_JSON, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return [prog['name'] for prog in data['programs']]

def count_synonyms() -> int:
    """Count number of synonyms defined"""
    with open(SYNONYMS_YML, 'r', encoding='utf-8') as f:
        content = f.read()
    return content.count('- synonym:')

def count_nlu_examples(intent: str) -> int:
    """Count NLU examples for a specific intent"""
    with open(NLU_YML, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find intent section
    intent_start = content.find(f'- intent: {intent}')
    if intent_start == -1:
        return 0
    
    # Find next intent
    next_intent = content.find('- intent:', intent_start + 1)
    if next_intent == -1:
        section = content[intent_start:]
    else:
        section = content[intent_start:next_intent]
    
    # Count lines with examples (lines starting with '    -')
    return section.count('\n    -')

def extract_programs_from_nlu(intent: str) -> Set[str]:
    """Extract program entities from NLU examples"""
    with open(NLU_YML, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find intent section
    intent_start = content.find(f'- intent: {intent}')
    if intent_start == -1:
        return set()
    
    next_intent = content.find('- intent:', intent_start + 1)
    if next_intent == -1:
        section = content[intent_start:]
    else:
        section = content[intent_start:next_intent]
    
    # Extract [program](program) patterns
    programs = set()
    import re
    pattern = r'\[([^\]]+)\]\(program\)'
    matches = re.findall(pattern, section)
    programs.update(matches)
    
    return programs

def main():
    print("=" * 70)
    print("🔍 VERIFICATION: Training Data Completeness for 44 Programs")
    print("=" * 70)
    print()
    
    # 1. Check programs.json
    print("📊 Step 1: Check programs.json")
    print("-" * 70)
    programs = load_programs()
    print(f"   ✅ Total programs in database: {len(programs)}")
    
    if len(programs) == 44:
        print(f"   ✅ Database is complete (44/44)")
    else:
        print(f"   ❌ Database is incomplete ({len(programs)}/44)")
    print()
    
    # 2. Check synonyms.yml
    print("📊 Step 2: Check synonyms.yml")
    print("-" * 70)
    synonym_count = count_synonyms()
    print(f"   ✅ Total synonyms defined: {synonym_count}")
    
    if synonym_count >= 44:
        print(f"   ✅ Synonyms are complete ({synonym_count}/44)")
    else:
        print(f"   ⚠️  Synonyms are incomplete ({synonym_count}/44)")
        print(f"   ℹ️  Missing: {44 - synonym_count} synonyms")
    print()
    
    # 3. Check nlu.yml - ask_program_info
    print("📊 Step 3: Check NLU examples for ask_program_info")
    print("-" * 70)
    program_info_count = count_nlu_examples('ask_program_info')
    program_info_programs = extract_programs_from_nlu('ask_program_info')
    
    print(f"   ✅ Total examples: {program_info_count}")
    print(f"   ✅ Programs mentioned: {len(program_info_programs)}")
    
    if len(program_info_programs) >= 40:
        print(f"   ✅ Coverage is good ({len(program_info_programs)}/44 programs)")
    else:
        print(f"   ⚠️  Coverage needs improvement ({len(program_info_programs)}/44)")
    print()
    
    # 4. Check nlu.yml - ask_tuition
    print("📊 Step 4: Check NLU examples for ask_tuition")
    print("-" * 70)
    tuition_count = count_nlu_examples('ask_tuition')
    tuition_programs = extract_programs_from_nlu('ask_tuition')
    
    print(f"   ✅ Total examples: {tuition_count}")
    print(f"   ✅ Programs mentioned: {len(tuition_programs)}")
    
    if tuition_count >= 50:
        print(f"   ✅ Examples are sufficient ({tuition_count} examples)")
    else:
        print(f"   ⚠️  Examples need improvement ({tuition_count} examples)")
    print()
    
    # 5. Find programs without NLU examples
    print("📊 Step 5: Find programs missing NLU examples")
    print("-" * 70)
    
    all_nlu_programs = program_info_programs | tuition_programs
    missing_programs = set(programs) - all_nlu_programs
    
    if missing_programs:
        print(f"   ⚠️  {len(missing_programs)} programs missing NLU examples:")
        for prog in sorted(missing_programs)[:10]:  # Show first 10
            print(f"      - {prog}")
        if len(missing_programs) > 10:
            print(f"      ... and {len(missing_programs) - 10} more")
    else:
        print(f"   ✅ All programs have NLU examples!")
    print()
    
    # 6. Summary
    print("=" * 70)
    print("📈 SUMMARY")
    print("=" * 70)
    
    checks = []
    checks.append(("Programs in database", len(programs), 44, len(programs) == 44))
    checks.append(("Synonyms defined", synonym_count, 44, synonym_count >= 44))
    checks.append(("Programs in ask_program_info", len(program_info_programs), 44, len(program_info_programs) >= 40))
    checks.append(("Examples in ask_tuition", tuition_count, 50, tuition_count >= 50))
    
    for name, current, target, passed in checks:
        status = "✅" if passed else "⚠️ "
        percentage = (current / target * 100) if target > 0 else 0
        print(f"{status} {name:35} {current:3}/{target:3} ({percentage:5.1f}%)")
    
    print()
    
    # Overall status
    all_passed = all(check[3] for check in checks)
    
    if all_passed:
        print("🎉 RESULT: All checks PASSED! Ready to retrain model.")
        print()
        print("Next steps:")
        print("   1. Run: rasa train")
        print("   2. Test: rasa shell")
        print("   3. Start servers and test web interface")
        return 0
    else:
        print("⚠️  RESULT: Some checks FAILED. Please review above.")
        print()
        print("Recommended actions:")
        print("   1. Add missing synonyms to data/synonyms.yml")
        print("   2. Add more NLU examples to data/nlu.yml")
        print("   3. Run this script again to verify")
        return 1

if __name__ == "__main__":
    sys.exit(main())
