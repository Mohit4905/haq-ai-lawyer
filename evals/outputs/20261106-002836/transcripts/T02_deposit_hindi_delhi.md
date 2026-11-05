# T02_deposit_hindi_delhi
Group: language

## Turn 1

**User:** मैंने दिल्ली के लक्ष्मी नगर में किराये का कमरा 15 सितंबर 2026 को खाली कर दिया। 25,000 रुपये सिक्योरिटी डिपॉज़िट दिया था, नकद में, रसीद नहीं है। मकान मालिक अब फ़ोन नहीं उठा रहा। मैं क्या करूँ?

**Haq** (groq/openai/gpt-oss-120b, 31.15s):

आपने 15 सितंबर 2026 को कमरा खाली किया और 25,000 ₹ नकद में सिक्योरिटी डिपॉज़िट दिया, पर रसीद नहीं है।

**अब तक की स्थिति**
- डिपॉज़िट वापस नहीं मिला, मकान मालिक फ़ोन नहीं उठा रहा।
- आपके पास डिपॉज़िट का कोई लिखित प्रमाण नहीं है (रसीद, बैंक ट्रांसफ़र)।

**आपको अभी क्या करना चाहिए**
1. **लिखित मांग पत्र (WhatsApp/ई‑मेल)** भेजें:
   - डिपॉज़िट की राशि (₹25,000), खाली करने की तिथि (15‑09‑2026), और आपका बैंक खाता विवरण लिखें।
   - “कृपया 15 दिन के भीतर राशि वापस करें, नहीं तो आगे की कार्रवाई करूँगा/करूँगी” लिखें।
   - इस संदेश का स्क्रीनशॉट रखें।
2. अगर 15 दिन में जवाब नहीं मिलता, तो **कानूनी नोटिस** (deposit_demand_notice) भेजें। आप स्वयं नोटिस तैयार कर सकते हैं; यह सिविल कोर्ट में आगे की कार्रवाई का आधार बनता है।
3. यदि नोटिस के बाद भी कोई जवाब नहीं, तो **लोक अदालत (Lok Adalat) या डिस्ट्रीक्ट लीगल सर्विसेज अथॉरिटी (DLSA)** के माध्यम से निःशुल्क प्री‑लिटिगेशन समाधान के लिए आवेदन करें।
4. अंतिम विकल्प: 3 साल (2029‑09‑15) के भीतर **सिविल suit** दायर करें। यह समय अभी बचा है, पर वकील की मदद लेनी पड़ेगी।

क्या आप लिखित मांग पत्र का मसौदा चाहते हैं या नोटिस तैयार करने में मदद चाहिए?

**Calculated by code:** {"deadlines": [{"label": "Approximate last date to sue for the deposit (3 years)", "date": "2029-09-15", "days_left": 1044, "status": "ok", "basis": "LIM1963-ART55", "note": "Limitation depends on the exact claim; confirm with legal aid before relying on it.", "user_deadline": true}], "derived": []}

_Escalation:_ {"level": "recommended", "reasons": ["यदि नोटिस के बाद भी जवाब नहीं मिले तो सिविल suit या Lok Adalat में मदद के लिए वकील की जरूरत होगी"]}  _Citations:_ ['ICA1872-S73', 'LIM1963-ART55', 'FACT-LOKADALAT-PRELITIGATION']

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
  "other_party_name": "landlord"
 },
 "timeline": [
  {
   "date": "2026-09-15",
   "event": "कमरा खाली किया, सिक्योरिटी डिपॉज़िट ₹25,000 नकद दिया"
  }
 ],
 "evidence_have": [],
 "evidence_missing": [
  "रसीद या कोई लिखित भुगतान प्रमाण",
  "किराए का मासिक किराया और लिखित किरायेदारी समझौता (यदि है)",
  "मकान मालिक के साथ हुई कॉल/WhatsApp/ई‑मेल की स्क्रीनशॉट"
 ],
 "next_step": "लिखित मांग पत्र (WhatsApp/ई‑मेल) भेजें और उसका स्क्रीनशॉट रखें"
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
