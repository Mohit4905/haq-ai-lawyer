# T02_deposit_hindi_delhi
Group: language

## Turn 1

**User:** मैंने दिल्ली के लक्ष्मी नगर में किराये का कमरा 15 सितंबर 2026 को खाली कर दिया। 25,000 रुपये सिक्योरिटी डिपॉज़िट दिया था, नकद में, रसीद नहीं है। मकान मालिक अब फ़ोन नहीं उठा रहा। मैं क्या करूँ?

**Haq** (gemini/gemini-3.1-flash-lite, 10.36s):

नमस्ते। यह सुनकर दुख हुआ कि आपको अपना सिक्योरिटी डिपॉज़िट वापस पाने में परेशानी हो रही है। बिना रसीद के नकद भुगतान (cash payment) होने के कारण मामला थोड़ा चुनौतीपूर्ण है, लेकिन आप अभी भी कुछ कदम उठा सकते हैं।

आपके पास अभी ये विकल्प हैं:
1. लिखित अनुरोध (WhatsApp/Email): मकान मालिक को एक आखिरी बार लिखित में संदेश भेजें।
2. कानूनी नोटिस (Legal Notice): आप खुद या वकील के जरिए उन्हें नोटिस भेज सकते हैं।
3. कानूनी सहायता (Legal Aid): दिल्ली राज्य कानूनी सेवा प्राधिकरण (DSLSA) से मुफ्त सलाह लें।

आगे बढ़ने के लिए मुझे ये बताएं:
- क्या आपके पास कोई रेंट एग्रीमेंट (Rent Agreement) है?
- क्या आपके पास कोई सबूत है कि आपने उन्हें पैसे दिए थे? (जैसे कोई पुरानी चैट, बैंक स्टेटमेंट जिसमें पैसे निकालने का जिक्र हो, या कोई गवाह?)
- क्या मकान मालिक ने कभी किसी कटौती (जैसे पेंटिंग या मरम्मत) के बारे में बात की थी?

अभी के लिए, सबसे अच्छा कदम है कि आप उन्हें एक औपचारिक संदेश भेजें जिसमें स्पष्ट रूप से राशि, खाली करने की तारीख और बैंक विवरण हों। क्या आप चाहते हैं कि मैं इसका ड्राफ्ट तैयार करने में आपकी मदद करूँ?

**Calculated by code:** {"deadlines": [{"label": "Approximate last date to sue for the deposit (3 years)", "date": "2029-09-15", "days_left": 1044, "status": "ok", "basis": "LIM1963-ART55", "note": "Limitation depends on the exact claim; confirm with legal aid before relying on it.", "user_deadline": true}], "derived": []}

_Escalation:_ {"level": "recommended", "reasons": ["Lack of written proof for cash payment makes recovery difficult; legal advice is needed to assess if other evidence is sufficient."]}  _Citations:_ ['ICA1872-S73', 'FACT-NALSA-HELPLINE']

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
  "summary": "Tenant vacated room in Laxmi Nagar, Delhi; landlord unresponsive regarding ₹25,000 cash deposit."
 },
 "timeline": [
  {
   "date": "2026-09-15",
   "event": "Vacated rented room"
  }
 ],
 "evidence_have": [],
 "evidence_missing": [
  "Rent agreement",
  "Proof of cash payment (chats, bank withdrawals, witnesses)"
 ],
 "next_step": "Draft a formal request message to the landlord"
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
