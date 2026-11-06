# T02_deposit_hindi_delhi
Group: language

## Turn 1

**User:** मैंने दिल्ली के लक्ष्मी नगर में किराये का कमरा 15 सितंबर 2026 को खाली कर दिया। 25,000 रुपये सिक्योरिटी डिपॉज़िट दिया था, नकद में, रसीद नहीं है। मकान मालिक अब फ़ोन नहीं उठा रहा। मैं क्या करूँ?

**Haq** (gemini/gemini-3.1-flash-lite, 8.97s):

देखिए, रसीद न होना एक बड़ी चुनौती है, लेकिन यह केस खत्म नहीं हुआ है। मकान मालिक का फ़ोन न उठाना यह साबित करता है कि वह अपनी ज़िम्मेदारी से भाग रहा है। हमें तुरंत एक 'पेपर ट्रेल' (सबूतों का सिलसिला) बनाना होगा ताकि अगर मामला आगे बढ़े, तो आपके पास यह सबूत हो कि आपने अपना पैसा मांगा था।

**मेरी राय:** आपका केस थोड़ा कमजोर है क्योंकि आपके पास नकद भुगतान का कोई लिखित सबूत नहीं है, लेकिन यह नामुमकिन नहीं है। अगर आप रेंट (किराया) बैंक से ट्रांसफर करते थे, तो वह बैंक स्टेटमेंट ही आपकी सबसे बड़ी ताकत है जो यह साबित करेगी कि आप वहां किरायेदार थे। हमें अब मकान मालिक को एक औपचारिक संदेश भेजना होगा ताकि वह या तो जवाब दे या फिर उसका चुप रहना ही आपके पक्ष में सबूत बन जाए।

**कानून आपकी तरफ:** भारतीय अनुबंध अधिनियम (Indian Contract Act, 1872) की धारा 73 के तहत, अगर कोई व्यक्ति अपने वादे से मुकरता है, तो आप नुकसान की भरपाई मांग सकते हैं। आपका सिक्योरिटी डिपॉज़िट वापस न करना इसी का उल्लंघन है।

**वे क्या कहेंगे और आपका जवाब:** वे कह सकते हैं कि 'मुझे कोई पैसा नहीं मिला' या 'कमरे में तोड़-फोड़ हुई थी'। आप बस यह कहें कि 'मैंने रेंट एग्रीमेंट/किरायेदारी की शर्तों के अनुसार भुगतान किया था और कमरा सही स्थिति में छोड़ा है, कृपया मेरा पैसा वापस करें'।

**मैं क्या करूँगा:** आज ही उन्हें एक औपचारिक संदेश (WhatsApp या ईमेल) भेजें। अगर 7 दिन में जवाब न आए, तो हम एक कानूनी नोटिस (Legal Notice) भेजेंगे।

**मुझे आपसे यह जानना है:** क्या आपके पास कोई रेंट एग्रीमेंट (Rent Agreement) था? क्या आप किराया बैंक से ट्रांसफर करते थे?

**Calculated by code:** {"deadlines": [{"label": "Approximate last date to sue for the deposit (3 years)", "date": "2029-09-15", "days_left": 1044, "status": "ok", "basis": "LIM1963-ART55", "note": "Limitation depends on the exact claim; confirm with legal aid before relying on it.", "user_deadline": true}], "derived": []}

_Escalation:_ {"level": "recommended", "reasons": ["नकद भुगतान का सबूत न होने के कारण, कानूनी नोटिस के बाद भी अगर वे नहीं मानते हैं, तो आपको एक वकील की सलाह की ज़रूरत होगी।"]}  _Citations:_ ['ICA1872-S73', 'LIM1963-ART55']

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
  "summary": "Landlord is not picking up calls after tenant vacated the room and is withholding the security deposit."
 },
 "timeline": [
  {
   "date": "2026-09-15",
   "event": "कमरा खाली किया"
  }
 ],
 "evidence_have": [],
 "evidence_missing": [
  "किराया भुगतान का बैंक स्टेटमेंट",
  "मकान मालिक के साथ पुरानी चैट",
  "रेंट एग्रीमेंट (यदि है)"
 ],
 "next_step": "मकान मालिक को औपचारिक लिखित मांग (WhatsApp/Email) भेजें"
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
