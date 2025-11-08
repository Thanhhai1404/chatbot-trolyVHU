# 🚀 GEMINI AI - QUICK REFERENCE

## ✅ STATUS: WORKING!

**Gemini API:** ✅ Active  
**Test Results:** 5/5 PASSED  
**Model Training:** ⏳ In Progress  

---

## ⚡ QUICK TEST

```powershell
cd d:\workspace\chatbot
python test_gemini_direct.py
```

**Expected Output:**
```
✅ TEST PASSED: Gemini xử lý câu ngoài phạm vi
✅ TEST PASSED: Phát hiện câu hỏi VHU đúng
```

---

## 🎯 HOW IT WORKS

### **Out-of-Scope → Gemini**
```
User: "thời tiết hôm nay?"
Bot: [Gemini AI response] 💙
```

### **VHU Questions → Existing Actions**
```
User: "học phí bao nhiêu?"
Bot: [Tuition action response]
```

---

## 🔑 KEY FILES

| File | Purpose |
|------|---------|
| `actions/gemini_config.py` | Gemini API integration |
| `.env` | API key storage |
| `test_gemini_direct.py` | Direct test script |
| `test_gemini_shell.bat` | Rasa shell test |

---

## 📊 TEST COMMANDS

### **Direct Test (Python)**
```powershell
python test_gemini_direct.py
```

### **Shell Test (After Training)**
```powershell
.\test_gemini_shell.bat
```

---

## 🐛 TROUBLESHOOTING

| Problem | Solution |
|---------|----------|
| "API key not found" | Add key to `.env` file |
| "Model not found" | Wait for training to finish |
| "Action server error" | Run `rasa run actions` first |
| "No response" | Check API key validity |

---

## 📝 TEST QUESTIONS

**Out-of-Scope (Gemini):**
- "thời tiết hôm nay thế nào?"
- "python là gì?"
- "cho tôi món ăn ngon"

**VHU (Existing Actions):**
- "học phí là bao nhiêu?"
- "trường có những ngành nào?"
- "VHU ở đâu?"

---

## 🎨 RESPONSE FORMAT

```
[Gemini's natural response]
- Friendly tone
- Relevant emoji
- 150 words max

💙 Bạn có muốn hỏi gì về VHU không nè?
```

---

## ⚙️ CONFIGURATION

**API Key:** `.env`  
**Models:** 5 backup models  
**Timeout:** 15 seconds  
**Max Tokens:** 200  

---

## 📞 SUPPORT

**Working:** ✅ Direct Python test  
**Pending:** ⏳ Rasa shell test (after training)  

**Quick Check:**
```powershell
python -c "from actions.gemini_config import configure_gemini; print('OK' if configure_gemini() else 'FAIL')"
```

---

**Last Updated:** 2025-10-30 22:35  
**Version:** 1.0
