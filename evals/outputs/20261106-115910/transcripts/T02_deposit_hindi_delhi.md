# T02_deposit_hindi_delhi
Group: language

## Turn 1

**User:** मैंने दिल्ली के लक्ष्मी नगर में किराये का कमरा 15 सितंबर 2026 को खाली कर दिया। 25,000 रुपये सिक्योरिटी डिपॉज़िट दिया था, नकद में, रसीद नहीं है। मकान मालिक अब फ़ोन नहीं उठा रहा। मैं क्या करूँ?

**Haq** (gemini/gemini-3.1-flash-lite, 9.96s):

नमस्ते। मैं समझ सकता हूँ कि यह स्थिति कितनी तनावपूर्ण है।

**आपकी कानूनी स्थिति:** कानून के अनुसार, मकान मालिक को आपका सिक्योरिटी डिपॉज़िट वापस करना चाहिए, लेकिन रसीद न होने और नकद भुगतान के कारण इसे साबित करना थोड़ा मुश्किल हो सकता है। आपकी स्थिति इस बात पर निर्भर करेगी कि आप अन्य सबूतों (जैसे बैंक स्टेटमेंट या चैट) से यह साबित कर सकें कि आपने पैसे दिए थे।

**कानून जो आप इस्तेमाल कर सकते हैं:**
* **भारतीय अनुबंध अधिनियम, 1872 (धारा 73):** यह कहता है कि यदि कोई व्यक्ति अपने वादे (अनुबंध) को पूरा नहीं करता, तो आप नुकसान की भरपाई के लिए दावा कर सकते हैं।
* **परिसीमा अधिनियम, 1963 (अनुच्छेद 55):** आप अपना पैसा वापस पाने के लिए 3 साल के भीतर कानूनी कार्रवाई कर सकते हैं।

**अब क्या करें:**
1. बैंक स्टेटमेंट निकालें (जिस दिन पैसे दिए थे, उस समय की निकासी दिखाएं) और मकान मालिक के साथ हुई कोई भी चैट या कॉल रिकॉर्ड इकट्ठा करें।
2. मकान मालिक को एक औपचारिक संदेश (WhatsApp/Email) भेजें जिसमें स्पष्ट रूप से राशि, तारीख और बैंक विवरण का उल्लेख हो।
3. यदि वे जवाब न दें, तो कानूनी नोटिस भेजें।
4. मदद के लिए जिला कानूनी सेवा प्राधिकरण (DLSA) की हेल्पलाइन 15100 पर कॉल करें।

**मुझे आपसे चाहिए:**
1. क्या आपके पास मकान मालिक के साथ कोई ऐसी चैट या SMS है जिसमें उन्होंने डिपॉज़िट का ज़िक्र किया हो?
2. क्या आपके बैंक स्टेटमेंट में उस तारीख के आसपास 25,000 रुपये की निकासी दिख रही है?

**आप ये क़ानून उद्धृत कर सकते हैं (सरकारी स्रोत से जाँचे हुए):**
- **Section 73, Indian Contract Act, 1872**: If someone breaks a contract with you, you can claim money for the loss it caused.
- **Article 55, Limitation Act, 1963**: A suit for compensation for breach of a contract (written or implied), where no other article covers it specifically, must be filed within 3 years.

**Calculated by code:** {"deadlines": [{"label": "Approximate last date to sue for the deposit (3 years)", "date": "2029-09-15", "days_left": 1044, "status": "ok", "basis": "LIM1963-ART55", "note": "Limitation depends on the exact claim; confirm with legal aid before relying on it.", "user_deadline": true}], "derived": []}

_Escalation:_ {"level": "recommended", "reasons": ["लिखित रसीद न होने के कारण मामला थोड़ा जटिल है, कानूनी सलाह लेना बेहतर होगा।"]}  _Citations:_ ['ICA1872-S73', 'LIM1963-ART55']

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
  "summary": "Landlord is not picking up calls after tenant vacated the room and is withholding the security deposit.",
  "written_agreement": false
 },
 "timeline": [
  {
   "date": "2026-09-15",
   "event": "कमरा खाली किया"
  }
 ],
 "evidence_have": [],
 "evidence_missing": [
  "बैंक स्टेटमेंट (निकासी का सबूत)",
  "मकान मालिक के साथ चैट/SMS (जहाँ डिपॉज़िट का ज़िक्र हो)"
 ],
 "next_step": "मकान मालिक को WhatsApp/Email पर एक औपचारिक अनुरोध भेजें"
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
