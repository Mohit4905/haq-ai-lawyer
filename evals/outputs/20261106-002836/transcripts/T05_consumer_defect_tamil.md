# T05_consumer_defect_tamil
Group: language

## Turn 1

**User:** நான் சென்னையில் ஜூலை 2026-ல் 32,000 ரூபாய்க்கு வாஷிங் மெஷின் வாங்கினேன். இரண்டு மாதத்தில் வேலை செய்யவில்லை. வாரண்டி இருந்தும் சர்வீஸ் சென்டர் சரிசெய்ய மறுக்கிறது. என்ன செய்வது?

**Haq** (groq/qwen/qwen3.8-27b, 7.59s):

சரி, உங்கள் நிலை புரிகிறது. வாரண்டி இருக்கிறபோது சர்வீஸ் சென்டர் சரிசெய்ய மறுப்பது = சேவை குறைபாடு (deficiency). நீங்கள் சொன்ன விவரங்களின்படி, முக்கிய நிபந்தனைகள் பூர்த்தி ஆகி இருக்கலாம்.

**முதலில் இரண்டு விஷயங்கள் தெரிஞ்சுக்கணும்:**

1. நீங்கள் கம்பெனி/சர்வீஸ் சென்டருக்கு **எழுத்துப்பூர்வமாக** (email, WhatsApp, letter) புகார் கொடுத்தீர்களா? எப்போது? அவர்கள் என்ன சொன்னார்கள்?
2. உங்களிடம் என்ன **தெளிவு** இருக்கு? (invoice, வாரண்டி கார்டு, order ID, chat screenshots, photos)

**செய்யலாம் (குறைந்த செலவில் முதலில்):**

- ✉️ கம்பெனிக்கு எழுத்துப்பூர்வ புகார் → 48 மணி நேரத்தில் பதில், 1 மாதத்தில் தீர்வு (e-commerce ஆனால்)
- 📞 National Consumer Helpline **1915** அல்லது WhatsApp **8800001915** → இலவசம், முன்-நீதிமன்ற மediator
- ⚖️ e-Jagriti-ல் (e-jagriti.gov.in) District Commission-ல் புகார் → **இலவசம்** (₹5 லட்சம் வரை), லாயர் தேவையில்லை

**என் பரிந்துரை:** முதலில் எழுத்துப்பூர்வ புகார் அனுப்புங்கள். பதில் இல்லையென்றால் 1915-ல் புகார். இரண்டும் பயன்படவில்லை என்றால் e-Jagriti-ல் புகார்.

எழுத்துப்பூர்வ புகார் மாதிரி எழுத வேண்டுமா?

**Calculated by code:** {"deadlines": [{"label": "Last date to file a consumer complaint (2 years from when the problem arose)", "date": "2028-09-01", "days_left": 665, "status": "ok", "basis": "CPA2019-S69", "note": "The commission can accept a late complaint only if you show sufficient cause for the delay.", "user_deadline": true}], "derived": [{"label": "Where to file", "value": "District Consumer Disputes Redressal Commission", "basis": "CPJURIS2021-R3-5", "note": "Based on the amount you paid (₹32,000), not the amount you claim."}, {"label": "Filing fee", "value": "Nil", "basis": "CPCDRC2020-R7", "note": ""}]}

_Escalation:_ {"level": "none", "reasons": []}  _Citations:_ ['CPA2019-S2-11', 'CPA2019-S35', 'CPA2019-S39', 'CPA2019-S69', 'CPJURIS2021-R3-5', 'CPCDRC2020-R7', 'CPECOM2020-R4-5', 'FACT-NCH-HELPLINE', 'FACT-EJAGRITI-PORTAL']

## Final case file

```json
{
 "category": "consumer",
 "language": "Tamil",
 "script": "Tamil",
 "facts": {
  "product_or_service": "washing machine",
  "other_party_name": "service center",
  "amount_paid": 32000,
  "purchase_date": "2026-07-01",
  "problem_date": "2026-09-01",
  "city_state": "Chennai, Tamil Nadu"
 },
 "timeline": [
  {
   "date": "2026-07-01",
   "event": "Washing machine purchased for ₹32,000"
  },
  {
   "date": "2026-09-01",
   "event": "Machine stopped working; service center refused repair under warranty"
  }
 ],
 "evidence_have": [],
 "evidence_missing": [
  "Invoice / bill of purchase",
  "Warranty card or warranty terms",
  "Order ID (if bought online)",
  "Written complaint to service center (email/WhatsApp/letter)",
  "Their reply or refusal (screenshot, email, call recording)",
  "Photos/video of the defect"
 ],
 "next_step": "Send a written complaint (email or WhatsApp) to the service center/company grievance officer, stating the defect, warranty period, and demanding repair or refund within 7 days. Keep a copy.",
 "approximate": [
  "problem_date",
  "purchase_date"
 ]
}
```

## Automatic checks

| check | pass | detail |
|---|---|---|
| category | ✅ | got consumer |
| reply_language | ✅ | expected Tamil, reply script Tamil |
| fact:amount_paid | ✅ | expected ~32, got 32000 |
| escalation<=recommended | ✅ | got none |
| no_unverified_law_shown | ✅ |  |
