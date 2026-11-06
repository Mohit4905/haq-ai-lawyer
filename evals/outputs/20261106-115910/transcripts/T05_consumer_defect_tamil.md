# T05_consumer_defect_tamil
Group: language

## Turn 1

**User:** நான் சென்னையில் ஜூலை 2026-ல் 32,000 ரூபாய்க்கு வாஷிங் மெஷின் வாங்கினேன். இரண்டு மாதத்தில் வேலை செய்யவில்லை. வாரண்டி இருந்தும் சர்வீஸ் சென்டர் சரிசெய்ய மறுக்கிறது. என்ன செய்வது?

**Haq** (gemini/gemini-3.1-flash-lite, 14.82s):

**உங்கள் சட்ட நிலை:**
நீங்கள் வாங்கிய பொருள் இரண்டு மாதங்களிலேயே பழுதானது மற்றும் வாரண்டி இருந்தும் சரிசெய்ய மறுப்பது, நுகர்வோர் பாதுகாப்புச் சட்டத்தின் கீழ் 'சேவை குறைபாடு' (Deficiency in Service) ஆகும். உங்கள் வாதம் வலுவாக உள்ளது, ஏனெனில் வாரண்டி காலத்தில் பழுதுபார்ப்பது நிறுவனத்தின் கடமை.

**நீங்கள் குறிப்பிடக்கூடிய சட்டங்கள்:**
* **நுகர்வோர் பாதுகாப்புச் சட்டம், 2019, பிரிவு 2(11):** இது சேவையில் உள்ள குறைபாடுகளை வரையறுக்கிறது; பழுதான பொருளைச் சரிசெய்ய மறுப்பது இதில் அடங்கும்.
* **நுகர்வோர் பாதுகாப்புச் சட்டம், 2019, பிரிவு 39:** பழுதான பொருளைச் சரிசெய்யவோ, மாற்றிக் கொடுக்கவோ அல்லது பணத்தைத் திரும்பப் பெறவோ நுகர்வோர் ஆணையம் உத்தரவிட முடியும்.
* **நுகர்வோர் பாதுகாப்பு (மின்-வணிகம்) விதிகள், 2020, விதி 6(3):** பழுதான அல்லது தரமற்ற பொருளுக்குப் பொறுப்பேற்கவும், பணத்தைத் திரும்பப் பெறவும் நிறுவனம் மறுக்க முடியாது.

**இப்போது என்ன செய்ய வேண்டும்:**
1. நிறுவனத்தின் வாடிக்கையாளர் சேவைக்கு மின்னஞ்சல் அல்லது கடிதம் மூலம் முறையான புகார் அளிக்கவும் (48 மணிநேரத்தில் பதில் வர வேண்டும்).
2. தேசிய நுகர்வோர் உதவி மையத்தை (National Consumer Helpline) 1915 என்ற எண்ணில் அழைத்து புகார் பதிவு செய்யவும்.
3. தீர்வு கிடைக்கவில்லை என்றால், 'e-Jagriti' இணையதளத்தில் நுகர்வோர் ஆணையத்தில் புகார் அளிக்கவும் (இதற்கு கட்டணம் இல்லை).

**என்னிடமிருந்து உங்களுக்குத் தேவை:**
1. நீங்கள் நிறுவனத்திற்கு எழுத்துப்பூர்வமாக புகார் அளித்துள்ளீர்களா?
2. உங்களிடம் வாங்கியதற்கான ரசீது (Invoice) மற்றும் வாரண்டி அட்டை உள்ளதா?

**Law you can cite (checked against official sources):**
- **Section 2(11), Consumer Protection Act, 2019**: A deficiency is any fault, shortcoming or inadequacy in the quality, nature or manner of a service that the law or a contract requires.
- **Section 35, Consumer Protection Act, 2019**: A complaint can be filed with the District Commission by the consumer, by a registered consumer association, by one or more consumers on behalf of many with the same interest (with the Commission's permission), or by the Central/State Government or the Central Authority.
- **Section 69, Consumer Protection Act, 2019**: You must file a consumer complaint within two years from the date the problem (cause of action) arose.

**Calculated by code:** {"deadlines": [{"label": "Last date to file a consumer complaint (2 years from when the problem arose)", "date": "2028-07-01", "days_left": 603, "status": "ok", "basis": "CPA2019-S69", "note": "The commission can accept a late complaint only if you show sufficient cause for the delay.", "user_deadline": true}], "derived": [{"label": "Where to file", "value": "District Consumer Disputes Redressal Commission", "basis": "CPJURIS2021-R3-5", "note": "Based on the amount you paid (₹32,000), not the amount you claim."}, {"label": "Filing fee", "value": "Nil", "basis": "CPCDRC2020-R7", "note": ""}]}

_Escalation:_ {"level": "none", "reasons": []}  _Citations:_ ['CPA2019-S2-11', 'CPA2019-S39', 'CPECOM2020-R6-3', 'CPA2019-S35', 'CPA2019-S69']

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
  "city_state": "Chennai",
  "summary": "User purchased a washing machine in July 2026 for 32,000 INR, which stopped working after two months, and the service center is refusing to repair it despite the warranty."
 },
 "timeline": [
  {
   "date": "2026-09-01",
   "event": "Machine stopped working (approximate)"
  }
 ],
 "evidence_have": [],
 "evidence_missing": [
  "Purchase invoice",
  "Warranty card",
  "Proof of communication with service center"
 ],
 "next_step": "Send a formal written complaint to the company grievance officer.",
 "approximate": [
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
