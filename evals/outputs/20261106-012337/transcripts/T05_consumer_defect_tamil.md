# T05_consumer_defect_tamil
Group: language

## Turn 1

**User:** நான் சென்னையில் ஜூலை 2026-ல் 32,000 ரூபாய்க்கு வாஷிங் மெஷின் வாங்கினேன். இரண்டு மாதத்தில் வேலை செய்யவில்லை. வாரண்டி இருந்தும் சர்வீஸ் சென்டர் சரிசெய்ய மறுக்கிறது. என்ன செய்வது?

**Haq** (gemini/gemini-3.1-flash-lite, 8.76s):

வணக்கம். உங்கள் வாஷிங் மெஷின் பழுதானது வருத்தமளிக்கிறது. வாரண்டி இருந்தும் சரிசெய்ய மறுப்பது 'சேவை குறைபாடு' (Deficiency of Service) ஆகும். நுகர்வோர் பாதுகாப்புச் சட்டத்தின் கீழ் உங்களுக்கு உரிமை உள்ளது.

அடுத்த கட்டத்திற்குச் செல்ல சில தகவல்கள் தேவை:
1. நீங்கள் கம்பெனிக்கு மின்னஞ்சல் அல்லது கடிதம் மூலம் புகார் அளித்துள்ளீர்களா?
2. உங்களிடம் பில் (Invoice), வாரண்டி கார்டு மற்றும் சர்வீஸ் சென்டர் கொடுத்த ரெஃபரன்ஸ் நம்பர் உள்ளதா?

தீர்வுக்கான வழிகள்:
1. கம்பெனியின் Grievance Officer-க்கு முறையான மின்னஞ்சல் அனுப்புங்கள் (இதுவே முதல் படி).
2. தேசிய நுகர்வோர் உதவி மையம் (1915) மூலம் புகார் அளிக்கவும்.
3. e-Jagriti போர்ட்டலில் நுகர்வோர் ஆணையத்தில் புகார் அளிக்கவும் (இது இலவசம்).

இப்போதைக்கு, கம்பெனிக்கு ஒரு முறையான மின்னஞ்சல் அனுப்புவதே சிறந்தது. அதைத் தயார் செய்ய நான் உதவவா?

**Calculated by code:** {"deadlines": [{"label": "Last date to file a consumer complaint (2 years from when the problem arose)", "date": "2028-09-01", "days_left": 665, "status": "ok", "basis": "CPA2019-S69", "note": "The commission can accept a late complaint only if you show sufficient cause for the delay.", "user_deadline": true}], "derived": [{"label": "Where to file", "value": "District Consumer Disputes Redressal Commission", "basis": "CPJURIS2021-R3-5", "note": "Based on the amount you paid (₹32,000), not the amount you claim."}, {"label": "Filing fee", "value": "Nil", "basis": "CPCDRC2020-R7", "note": ""}]}

_Escalation:_ {"level": "none", "reasons": []}  _Citations:_ ['CPECOM2020-R4-5', 'CPA2019-S2-11', 'FACT-NCH-HELPLINE', 'FACT-EJAGRITI-PORTAL']

## Final case file

```json
{
 "category": "consumer",
 "language": "Tamil",
 "script": "Tamil",
 "facts": {
  "product_or_service": "Washing machine",
  "amount_paid": 32000,
  "purchase_date": "2026-07-01",
  "problem_date": "2026-09-01",
  "city_state": "Chennai",
  "summary": "Washing machine purchased in July 2026 stopped working after two months; service center refusing warranty repair."
 },
 "timeline": [
  {
   "date": "2026-07-01",
   "event": "Purchase"
  },
  {
   "date": "2026-09-01",
   "event": "Problem started"
  }
 ],
 "evidence_have": [],
 "evidence_missing": [
  "Invoice",
  "Warranty card",
  "Service request numbers/chats"
 ],
 "next_step": "Draft a formal complaint email to the company's grievance officer.",
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
