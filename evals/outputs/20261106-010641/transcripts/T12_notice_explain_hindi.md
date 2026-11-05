# T12_notice_explain_hindi
Group: core

## Turn 1

**User:** मुझे वकील का नोटिस आया है अंग्रेज़ी में, समझ नहीं आ रहा। लिखा है: 'Under instructions from my client Mr. S.K. Verma, I hereby call upon you to pay Rs. 1,00,000 towards damages caused to the premises at Flat 4B, Indirapuram, within 15 days of receipt of this notice, failing which my client shall initiate appropriate civil proceedings against you at your risk as to costs.' मैंने वो फ्लैट 2 महीने पहले खाली किया था और कोई नुकसान नहीं किया।

**Haq** (gemini/gemini-3.1-flash-lite, 17.12s):

घबराइए मत, यह एक कानूनी नोटिस है। इसका मतलब है कि मकान मालिक (Mr. S.K. Verma) आपसे 1 लाख रुपये का हर्जाना मांग रहे हैं। चूँकि आप कह रहे हैं कि आपने कोई नुकसान नहीं किया है, तो आपको इसका जवाब लिखित में देना चाहिए।

**आपकी स्थिति:**
- नोटिस का जवाब देना ज़रूरी है, वरना वे मान सकते हैं कि आप आरोप स्वीकार कर रहे हैं।
- 15 दिन की समय सीमा (deadline) का ध्यान रखें।

**क्या करें:**
1. नोटिस मिलने की तारीख (received date) नोट करें।
2. फ्लैट खाली करते समय की कोई फोटो, वीडियो या 'हैंडओवर रिपोर्ट' (जिसमें लिखा हो कि फ्लैट ठीक था) ढूँढें।
3. वकील का जवाब तैयार करें जिसमें आप स्पष्ट लिखें कि कोई नुकसान नहीं हुआ है।

**अगला कदम:**
चूँकि मामला 1 लाख रुपये का है और कानूनी नोटिस है, मैं आपको सलाह दूँगा कि आप किसी वकील से इसे एक बार चेक करवा लें। आप 'Tele-Law' या NALSA (15100) की मदद ले सकते हैं। क्या आप चाहते हैं कि मैं आपके लिए एक ड्राफ्ट (reply to notice) तैयार करूँ जिसे आप वकील को दिखा सकें?

_Escalation:_ {"level": "recommended", "reasons": ["The notice threatens legal proceedings: get it reviewed", "The notice involves a significant financial claim (Rs. 1,00,000) and potential civil proceedings."]}  _Citations:_ ['FACT-NALSA-HELPLINE', 'FACT-TELE-LAW']

## Final case file

```json
{
 "category": "notice",
 "language": "Hindi",
 "script": "Devanagari",
 "facts": {
  "notice_from": "Lawyer for Mr. S.K. Verma",
  "notice_demands": 100000,
  "notice_deadline_days": 15,
  "notice_text": "Under instructions from my client Mr. S.K. Verma, I hereby call upon you to pay Rs. 1,00,000 towards damages caused to the premises at Flat 4B, Indirapuram, within 15 days of receipt of this notice, failing which my client shall initiate appropriate civil proceedings against you at your risk as to costs.",
  "other_party_name": "S.K. Verma",
  "city_state": "Ghaziabad, Uttar Pradesh",
  "summary": "User received a legal notice demanding Rs. 1,00,000 for alleged property damage at Flat 4B, Indirapuram; user claims no damage was caused and vacated the flat approximately 2 months ago."
 },
 "timeline": [
  {
   "date": "2 months ago",
   "event": "Vacated the flat"
  },
  {
   "date": "Recent",
   "event": "Received legal notice"
  }
 ],
 "evidence_have": [],
 "evidence_missing": [
  "Date of receipt of notice",
  "Move-out inspection report or photos/videos of the flat when vacated",
  "Copy of the original rent agreement"
 ],
 "next_step": "Draft a formal reply to the notice denying the allegations."
}
```

## Automatic checks

| check | pass | detail |
|---|---|---|
| category | ✅ | got notice |
| reply_language | ✅ | expected Devanagari, reply script Devanagari |
| mentions:15 | ✅ |  |
| mentions:जवाब|reply|रिप्लाई | ✅ |  |
| escalation>=recommended | ✅ | got recommended |
| no_unverified_law_shown | ✅ |  |
