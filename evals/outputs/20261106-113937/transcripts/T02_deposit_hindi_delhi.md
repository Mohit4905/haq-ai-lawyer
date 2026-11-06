# T02_deposit_hindi_delhi
Group: language

## Turn 1

**User:** मैंने दिल्ली के लक्ष्मी नगर में किराये का कमरा 15 सितंबर 2026 को खाली कर दिया। 25,000 रुपये सिक्योरिटी डिपॉज़िट दिया था, नकद में, रसीद नहीं है। मकान मालिक अब फ़ोन नहीं उठा रहा। मैं क्या करूँ?

**Haq** (gemini/gemini-3.1-flash-lite, 16.84s):

नमस्ते। मैं समझ सकता हूँ कि यह स्थिति कितनी तनावपूर्ण है, लेकिन घबराएं नहीं। 

**आपकी कानूनी स्थिति:**
बिना रसीद के नकद भुगतान साबित करना थोड़ा चुनौतीपूर्ण है, लेकिन कानून के तहत आप अभी भी अपना पैसा वापस पाने के हकदार हैं। अगर आपके पास कोई भी सबूत (जैसे चैट, कॉल रिकॉर्ड, या कोई गवाह) है, तो आपका पक्ष मजबूत हो सकता है। फिलहाल, हमें यह साबित करने पर ध्यान देना होगा कि आपने पैसे दिए थे और कमरा खाली किया था।

**कानून जो आप बता सकते हैं:**
* **Section 73, Indian Contract Act, 1872:** यह कहता है कि अगर कोई अपना वादा (अनुबंध) नहीं निभाता, तो आप नुकसान की भरपाई मांग सकते हैं। यह आपके पैसे की वापसी का आधार है।
* **Limitation Act, 1963:** आपके पास पैसे की वसूली के लिए कानूनी कार्रवाई शुरू करने के लिए 3 साल का समय है।

**क्या करें (विकल्प):**
1. **लिखित अनुरोध:** मकान मालिक को WhatsApp या SMS पर एक स्पष्ट संदेश भेजें (तारीख, राशि और बैंक विवरण के साथ)। इसका स्क्रीनशॉट संभाल कर रखें।
2. **कानूनी नोटिस:** अगर वे जवाब न दें, तो आप खुद एक कानूनी नोटिस भेज सकते हैं।
3. **मुफ्त कानूनी सहायता:** DLSA (15100) पर कॉल करें या अपने जिले के कानूनी सेवा प्राधिकरण से संपर्क करें।

**अगला कदम:** सबसे पहले मकान मालिक को एक औपचारिक WhatsApp संदेश भेजें। अगर आप चाहें, तो मैं इसका ड्राफ्ट तैयार करने में आपकी मदद कर सकता हूँ।

**मुझे आपसे ये जानकारी चाहिए:**
1. क्या आपके पास कोई लिखित रेंट एग्रीमेंट (Rent Agreement) है?
2. क्या आपके पास कोई भी डिजिटल सबूत है (जैसे WhatsApp चैट, बैंक स्टेटमेंट, या कोई गवाह) जो यह साबित करे कि आपने पैसे दिए थे?

**Calculated by code:** {"deadlines": [{"label": "Approximate last date to sue for the deposit (3 years)", "date": "2029-09-15", "days_left": 1044, "status": "ok", "basis": "LIM1963-ART55", "note": "Limitation depends on the exact claim; confirm with legal aid before relying on it.", "user_deadline": true}], "derived": []}

_Escalation:_ {"level": "recommended", "reasons": ["बिना रसीद के नकद भुगतान साबित करना मुश्किल है, इसलिए कानूनी नोटिस के लिए वकील की सलाह बेहतर होगी।"]}  _Citations:_ ['ICA1872-S73', 'LIM1963-ART55']

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
 "evidence_have": [
  "कोई नहीं"
 ],
 "evidence_missing": [
  "रेंट एग्रीमेंट",
  "भुगतान का कोई सबूत (बैंक स्टेटमेंट/चैट/गवाह)"
 ],
 "next_step": "मकान मालिक को WhatsApp/SMS पर औपचारिक लिखित अनुरोध भेजें।"
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
