# T05_consumer_defect_tamil
Group: language

## Turn 1

**User:** நான் சென்னையில் ஜூலை 2026-ல் 32,000 ரூபாய்க்கு வாஷிங் மெஷின் வாங்கினேன். இரண்டு மாதத்தில் வேலை செய்யவில்லை. வாரண்டி இருந்தும் சர்வீஸ் சென்டர் சரிசெய்ய மறுக்கிறது. என்ன செய்வது?

**Haq** (gemini/gemini-3.1-flash-lite, 17.04s):

வணக்கம். உங்கள் வாஷிங் மெஷின் பிரச்சனைக்கு வருந்துகிறேன். வாரண்டி இருந்தும் சர்வீஸ் சென்டர் சரிசெய்ய மறுப்பது 'Consumer Protection Act, 2019'-ன் கீழ் ஒரு குறைபாடு (deficiency) ஆகும்.

தற்போது நீங்கள் செய்ய வேண்டியவை:
1. நிறுவனத்தின் வாடிக்கையாளர் சேவைக்கு (Customer Care) மின்னஞ்சல் அல்லது கடிதம் மூலம் புகார் அளித்துள்ளீர்களா? 
2. உங்களிடம் பில் (Invoice), வாரண்டி கார்டு மற்றும் சர்வீஸ் சென்டர் மறுத்ததற்கான ஆதாரம் (எ.கா: மெசேஜ், மின்னஞ்சல் அல்லது சர்வீஸ் டிக்கெட் எண்) உள்ளதா?

நீங்கள் பின்பற்ற வேண்டிய வழிமுறைகள்:
1. நிறுவனத்தின் Grievance Officer-க்கு எழுத்துப்பூர்வமாக புகார் அளிக்கவும் (48 மணிநேரத்தில் பதில் வர வேண்டும்).
2. தேசிய நுகர்வோர் உதவி மையத்தை (National Consumer Helpline - 1915) அழைக்கவும்.
3. தீர்வு கிடைக்கவில்லை எனில், 'e-Jagriti' இணையதளத்தில் நுகர்வோர் ஆணையத்தில் (Consumer Commission) புகார் அளிக்கவும்.

தற்போதைய பரிந்துரை: நிறுவனத்தின் Grievance Officer-க்கு ஒரு மின்னஞ்சல் அல்லது கடிதம் அனுப்ப நான் உங்களுக்கு உதவட்டுமா?

**Calculated by code:** {"deadlines": [{"label": "Last date to file a consumer complaint (2 years from when the problem arose)", "date": "2028-09-01", "days_left": 665, "status": "ok", "basis": "CPA2019-S69", "note": "The commission can accept a late complaint only if you show sufficient cause for the delay.", "user_deadline": true}], "derived": [{"label": "Where to file", "value": "District Consumer Disputes Redressal Commission", "basis": "CPJURIS2021-R3-5", "note": "Based on the amount you paid (₹32,000), not the amount you claim."}, {"label": "Filing fee", "value": "Nil", "basis": "CPCDRC2020-R7", "note": ""}]}

_Escalation:_ {"level": "none", "reasons": []}  _Citations:_ ['CPA2019-S2-11', 'CPECOM2020-R4-5', 'FACT-NCH-HELPLINE', 'FACT-EJAGRITI-PORTAL']

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
   "event": "வாஷிங் மெஷின் வாங்கிய தேதி"
  },
  {
   "date": "2026-09-01",
   "event": "பிரச்சனை தொடங்கிய தேதி"
  }
 ],
 "evidence_have": [],
 "evidence_missing": [
  "பில் (Invoice)",
  "வாரண்டி கார்டு",
  "சர்வீஸ் சென்டர் மறுத்ததற்கான ஆதாரம் (எ.கா: மெசேஜ், மின்னஞ்சல் அல்லது சர்வீஸ் டிக்கெட் எண்)"
 ],
 "next_step": "நிறுவனத்தின் Grievance Officer-க்கு புகார் கடிதம் அனுப்புதல்",
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
