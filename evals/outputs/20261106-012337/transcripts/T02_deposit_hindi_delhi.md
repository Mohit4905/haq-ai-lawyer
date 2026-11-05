# T02_deposit_hindi_delhi
Group: language

## Turn 1

**User:** मैंने दिल्ली के लक्ष्मी नगर में किराये का कमरा 15 सितंबर 2026 को खाली कर दिया। 25,000 रुपये सिक्योरिटी डिपॉज़िट दिया था, नकद में, रसीद नहीं है। मकान मालिक अब फ़ोन नहीं उठा रहा। मैं क्या करूँ?

**Haq** (gemini/gemini-3.1-flash-lite, 6.61s):

नमस्ते। यह सुनकर दुख हुआ कि आपको अपना सिक्योरिटी डिपॉज़िट वापस पाने में परेशानी हो रही है। बिना रसीद के नकद भुगतान (cash payment) होने के कारण मामला थोड़ा चुनौतीपूर्ण है, लेकिन आप अभी भी कोशिश कर सकते हैं।

आपके पास क्या सबूत हैं कि आपने पैसे दिए थे? क्या आपके पास कोई पुरानी WhatsApp चैट, बैंक स्टेटमेंट (जहाँ से पैसे निकाले थे), या कोई गवाह है जिसने पैसे देते समय देखा हो? 

आगे बढ़ने के लिए ये विकल्प हैं:
1. मकान मालिक को एक औपचारिक लिखित संदेश (WhatsApp/Email) भेजें जिसमें स्पष्ट रूप से राशि, कमरा खाली करने की तारीख और बैंक विवरण लिखें।
2. कानूनी नोटिस (Legal Notice) भेजें (आप इसे खुद भी ड्राफ्ट कर सकते हैं)।
3. जिला कानूनी सेवा प्राधिकरण (DLSA) के माध्यम से लोक अदालत (Lok Adalat) में मध्यस्थता के लिए आवेदन करें।

अभी के लिए, सबसे अच्छा कदम यह है कि आप मकान मालिक को एक आखिरी बार लिखित में (WhatsApp पर) अपनी बात भेजें और उसका स्क्रीनशॉट संभाल कर रखें। क्या आपके पास मकान मालिक का पूरा नाम और पता है?

**Calculated by code:** {"deadlines": [{"label": "Approximate last date to sue for the deposit (3 years)", "date": "2029-09-15", "days_left": 1044, "status": "ok", "basis": "LIM1963-ART55", "note": "Limitation depends on the exact claim; confirm with legal aid before relying on it.", "user_deadline": true}], "derived": []}

_Escalation:_ {"level": "recommended", "reasons": ["Lack of written proof (receipt/agreement) makes recovery difficult; legal advice is needed to assess if other evidence is sufficient."]}  _Citations:_ ['ICA1872-S73', 'LIM1963-ART55', 'FACT-LOKADALAT-PRELITIGATION', 'FACT-NALSA-HELPLINE']

## Final case file

```json
{
 "category": "tenancy",
 "language": "Hindi",
 "script": "Devanagari",
 "facts": {
  "deposit_amount": 25000,
  "possession_handed_over_date": "2026-09-15",
  "proof_of_payment": "none",
  "city_state": "Delhi",
  "summary": "Tenant vacated room in Laxmi Nagar, Delhi. Security deposit of 25k paid in cash, no receipt. Landlord unresponsive."
 },
 "timeline": [
  {
   "date": "2026-09-15",
   "event": "Vacated rented room in Laxmi Nagar"
  }
 ],
 "evidence_have": [],
 "evidence_missing": [
  "Written rent agreement",
  "Proof of cash payment (bank withdrawal records, witnesses, or chat history)",
  "Landlord's full name and address"
 ],
 "next_step": "Send a formal written request via WhatsApp/Email to the landlord and save the screenshot."
}
```

## Automatic checks

| check | pass | detail |
|---|---|---|
| category | ✅ | got tenancy |
| reply_language | ✅ | expected Devanagari, reply script Devanagari |
| fact:deposit_amount | ✅ | expected ~25, got 25000 |
| mentions:सबूत|प्रमाण|रसीद|गवाह|WhatsApp|व्हाट्सऐप | ✅ |  |
| escalation<=recommended | ✅ | got recommended |
| no_unverified_law_shown | ✅ |  |
