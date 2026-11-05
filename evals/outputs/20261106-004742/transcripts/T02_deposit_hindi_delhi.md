# T02_deposit_hindi_delhi
Group: language

## Turn 1

**User:** मैंने दिल्ली के लक्ष्मी नगर में किराये का कमरा 15 सितंबर 2026 को खाली कर दिया। 25,000 रुपये सिक्योरिटी डिपॉज़िट दिया था, नकद में, रसीद नहीं है। मकान मालिक अब फ़ोन नहीं उठा रहा। मैं क्या करूँ?

**Haq** (groq/qwen/qwen3.8-27b, 6.63s):

समझता हूँ, डिपॉज़िट वापस न मिलना परेशान करता है।

**आपकी स्थिति:**
- अच्छी बात: आपने 15 सितंबर 2026 को खाली कर दिया, मकान मालिक फ़ोन नहीं उठा रहा — यानी आपने अपना काम कर दिया।
- कमज़ोर बात: नकद में दिया, रसीद नहीं। अगर मकान मालिक कह दे कि "कुछ नहीं लिया", तो साबित करना मुश्किल होगा।

**आपके पास ये रास्ते हैं (सस्ते से महँगे):**
1. **WhatsApp/ईमेल पर लिखकर माँगें** — राशि, खाली करने की तारीख, बैंक विवरण दें; स्क्रीनशॉट रखें। (मुफ़्त, आज ही)
2. **लीगल नोटिस** — 15 दिन में वापस करने की माँग; खुद भेज सकते हैं। (₹500–1500, 1–2 हफ़्ता)
3. **लोक अदालत / मुफ़्त कानूनी सहायता** — जिला कानूनी सेवा प्राधिकरण (DLSA) से; NALSA हेल्पलाइन **15100** पर कॉल करें। (मुफ़्त, 2–4 हफ़्ता)
4. **दरबार में रिक्वेस्ट (civil suit)** — 3 साल का समय है; अगर लिखित एग्रीमेंट है तो summary suit (तेज़) भी हो सकता है। (वकील चाहिए, 3–6 महीना+)

**मेरी सलाह:** अभी WhatsApp पर एक साफ़-सुथरा संदेश भेजें। मैं लिखकर दे सकता हूँ।

**3 सवाल:**
1. लिखित किराया एग्रीमेंट है? (हाँ/नहीं)
2. महीने का किराया कितना था?
3. अब तक कैसे माँगा — फ़ोन, WhatsApp, या और कुछ?

**Calculated by code:** {"deadlines": [{"label": "Approximate last date to sue for the deposit (3 years)", "date": "2029-09-15", "days_left": 1044, "status": "ok", "basis": "LIM1963-ART55", "note": "Limitation depends on the exact claim; confirm with legal aid before relying on it.", "user_deadline": true}], "derived": []}

_Escalation:_ {"level": "none", "reasons": []}  _Citations:_ ['ICA1872-S73', 'LIM1963-ART55', 'CPC1908-O37', 'FACT-LOKADALAT-PRELITIGATION', 'FACT-NALSA-HELPLINE', 'FACT-MTA-STATE-ADOPTION']

## Final case file

```json
{
 "category": "tenancy",
 "language": "Hindi",
 "script": "Devanagari",
 "facts": {
  "deposit_amount": 25000,
  "possession_handed_over_date": "2026-09-15",
  "city_state": "Delhi",
  "other_party_name": "landlord",
  "proof_of_payment": "cash, no receipt"
 },
 "timeline": [
  {
   "date": "2026-09-15",
   "event": "Possession handed over to landlord"
  }
 ],
 "evidence_have": [],
 "evidence_missing": [
  "Proof of deposit payment (receipt, bank transfer, or WhatsApp message where landlord acknowledged)",
  "Written rent agreement (if exists)",
  "Any written communication (WhatsApp/email) where landlord acknowledged the deposit or the move-out"
 ],
 "next_step": "Send a clear WhatsApp message to landlord demanding ₹25,000 deposit refund with move-out date and bank details; save screenshot"
}
```

## Automatic checks

| check | pass | detail |
|---|---|---|
| category | ✅ | got tenancy |
| reply_language | ✅ | expected Devanagari, reply script Devanagari |
| fact:deposit_amount | ✅ | expected ~25, got 25000 |
| mentions:सबूत|प्रमाण|रसीद|गवाह|WhatsApp|व्हाट्सऐप | ✅ |  |
| escalation<=recommended | ✅ | got none |
| no_unverified_law_shown | ✅ |  |
