# T12_notice_explain_hindi
Group: core

## Turn 1

**User:** मुझे वकील का नोटिस आया है अंग्रेज़ी में, समझ नहीं आ रहा। लिखा है: 'Under instructions from my client Mr. S.K. Verma, I hereby call upon you to pay Rs. 1,00,000 towards damages caused to the premises at Flat 4B, Indirapuram, within 15 days of receipt of this notice, failing which my client shall initiate appropriate civil proceedings against you at your risk as to costs.' मैंने वो फ्लैट 2 महीने पहले खाली किया था और कोई नुकसान नहीं किया।

**Haq** (gemini/gemini-3.1-flash-lite, 10.81s):

नमस्ते। घबराइए मत, कानूनी नोटिस मिलना तनावपूर्ण हो सकता है, लेकिन यह सिर्फ एक दावा है, कोई अदालत का फैसला नहीं। चूंकि आपने फ्लैट 2 महीने पहले खाली कर दिया था और आप कह रहे हैं कि कोई नुकसान नहीं हुआ, तो आपके पास अपना पक्ष रखने का पूरा अधिकार है।

**आपकी कानूनी स्थिति:**
कानून के अनुसार, मकान मालिक को यह साबित करना होगा कि नुकसान हुआ है और वह आपकी वजह से हुआ है। चूंकि आपने फ्लैट खाली कर दिया है, तो अब यह साबित करना उनके लिए मुश्किल होगा कि नुकसान आपके समय में हुआ था। आपको इस नोटिस का जवाब लिखित में देना चाहिए ताकि आपका पक्ष रिकॉर्ड पर रहे।

**कानून जिसका आप हवाला दे सकते हैं:**
* **भारतीय अनुबंध अधिनियम, 1872 की धारा 73 (Section 73, Indian Contract Act, 1872):** यह कहता है कि नुकसान के लिए हर्जाना तभी मांगा जा सकता है जब वह वास्तव में हुआ हो और अनुबंध के उल्लंघन का सीधा परिणाम हो। आप कह सकते हैं कि कोई नुकसान नहीं हुआ, इसलिए कोई हर्जाना नहीं बनता।
* **मॉडल टेनेंसी एक्ट, 2021 की धारा 11 (Model Tenancy Act, 2021, Section 11):** यह सुरक्षा जमा (security deposit) और फ्लैट की स्थिति के बारे में है। आप इसका उपयोग यह तर्क देने के लिए कर सकते हैं कि फ्लैट सही स्थिति में सौंपा गया था।

**अब क्या करें:**
1. **नोटिस को अनदेखा न करें:** 15 दिन की समय सीमा महत्वपूर्ण है।
2. **सबूत इकट्ठा करें:** फ्लैट खाली करते समय की कोई फोटो, वीडियो, या मकान मालिक को दी गई चाबियों की रसीद या ईमेल/व्हाट्सएप मैसेज ढूंढें।
3. **लिखित जवाब भेजें:** एक वकील के माध्यम से या खुद एक औपचारिक जवाब भेजें जिसमें आप स्पष्ट रूप से दावों को नकारें।
4. **कानूनी सहायता:** यदि मामला आगे बढ़ता है, तो 15100 (NALSA) पर कॉल करें या अपने पास के 'टेली-लॉ' (Tele-Law) केंद्र पर जाएं।

मैं आपको इस नोटिस का जवाब ड्राफ्ट करने में मदद कर सकता हूँ।

**मुझे आपसे यह जानना है:**
1. क्या आपके पास फ्लैट खाली करते समय की कोई फोटो या वीडियो है, या मकान मालिक से हुई कोई बातचीत (WhatsApp/Email) है जिसमें उन्होंने फ्लैट की स्थिति पर कोई आपत्ति नहीं जताई थी?
2. क्या आपने फ्लैट खाली करते समय मकान मालिक से 'नो ड्यूज सर्टिफिकेट' (No Dues Certificate) या सुरक्षा जमा (security deposit) वापस लिया था?

_Escalation:_ {"level": "recommended", "reasons": ["The notice threatens legal proceedings: get it reviewed", "Since a legal notice has been issued, having a lawyer review your response ensures you don't accidentally admit liability."]}  _Citations:_ ['ICA1872-S73', 'MTA2021-S11']

## Final case file

```json
{
 "category": "notice",
 "language": "Hindi",
 "script": "Devanagari",
 "facts": {
  "notice_from": "Mr. S.K. Verma",
  "notice_demands": "100000",
  "notice_deadline_days": "15",
  "notice_text": "Under instructions from my client Mr. S.K. Verma, I hereby call upon you to pay Rs. 1,00,000 towards damages caused to the premises at Flat 4B, Indirapuram, within 15 days of receipt of this notice, failing which my client shall initiate appropriate civil proceedings against you at your risk as to costs.",
  "possession_handed_over_date": "2026-09-01",
  "summary": "User received a legal notice from landlord Mr. S.K. Verma demanding 1 lakh for alleged damages to a flat vacated 2 months ago."
 },
 "timeline": [
  {
   "date": "2026-09-01",
   "event": "Flat vacated"
  }
 ],
 "evidence_have": [],
 "evidence_missing": [
  "Photos/videos of flat at time of vacating",
  "Communication (WhatsApp/Email) with landlord regarding handover"
 ],
 "next_step": "Draft a formal reply to the legal notice denying the allegations.",
 "approximate": [
  "possession_handed_over_date"
 ]
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
