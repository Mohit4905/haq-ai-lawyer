# T07_salary_hindi_startup
Group: core

## Turn 1

**User:** मैं नोएडा की एक स्टार्टअप में सॉफ्टवेयर डेवलपर था, सैलरी 70,000 महीना। अगस्त और सितंबर 2026 की सैलरी नहीं मिली। मैंने 30 सितंबर 2026 को रिज़ाइन कर दिया था, आख़िरी दिन वही था। HR कहता है कंपनी घाटे में है, बाद में देंगे। ऑफ़र लेटर और पुरानी सैलरी स्लिप मेरे पास हैं।

**Haq** (gemini/gemini-3.1-flash-lite, 13.23s):

नमस्ते। आपकी स्थिति स्पष्ट है: आपने काम किया, लेकिन कंपनी ने अगस्त और सितंबर 2026 की सैलरी (कुल ₹1,40,000) नहीं दी है। चूँकि आप अब वहां काम नहीं कर रहे हैं, तो आपका पूरा बकाया (Full and Final Settlement) काम छोड़ने के 2 कार्य दिवसों के भीतर मिलना चाहिए था।

आपके पास ऑफ़र लेटर और सैलरी स्लिप्स हैं, जो बहुत अच्छे सबूत हैं। HR का 'घाटे' का बहाना कानूनी रूप से आपकी सैलरी रोकने का आधार नहीं है।

**आपके विकल्प:**
1. **ईमेल:** HR को एक औपचारिक ईमेल भेजें जिसमें बकाया राशि और भुगतान की तारीख का स्पष्ट उल्लेख हो।
2. **डिमांड नोटिस:** यदि ईमेल का जवाब न मिले, तो वकील के माध्यम से एक 'डिमांड नोटिस' भेजें।
3. **लेबर अथॉरिटी:** 'Code on Wages, 2019' के तहत आप लेबर अथॉरिटी (Inspector-cum-Facilitator) के पास शिकायत दर्ज कर सकते हैं।
4. **SAMADHAN पोर्टल:** आप https://samadhan.labour.gov.in पर भी शिकायत दर्ज कर सकते हैं।

**अगला कदम:** क्या आपने HR को लिखित में (ईमेल द्वारा) बकाया सैलरी के लिए कोई औपचारिक रिमाइंडर भेजा है? अगर नहीं, तो मैं आपको एक ईमेल ड्राफ्ट करने में मदद कर सकता हूँ।

⚠️ **Deadline check (calculated by Haq, not AI):** Full & final wages were due by (2 working days after leaving): **02 Oct 2026**, which has passed. Please speak to a lawyer or free legal aid (15100) soon to check what options remain.

**Calculated by code:** {"deadlines": [{"label": "Full & final wages were due by (2 working days after leaving)", "date": "2026-10-02", "days_left": -35, "status": "passed", "basis": "COW2019-S17", "note": "Assumes a Mon–Sat working week.", "user_deadline": true}, {"label": "Approximate last date to file a wage claim with the labour authority (3 years)", "date": "2029-09-30", "days_left": 1059, "status": "ok", "basis": "COW2019-S45", "note": "", "user_deadline": true}], "derived": []}

_Escalation:_ {"level": "recommended", "reasons": ["Deadline passed: Full & final wages were due by (2 working days after leaving) (2026-10-02)"]}  _Citations:_ ['COW2019-S17', 'COW2019-S45', 'FACT-SAMADHAN-PORTAL']

## Final case file

```json
{
 "category": "salary",
 "language": "Hindi",
 "script": "Devanagari",
 "facts": {
  "role": "Software Developer",
  "monthly_salary": 70000,
  "unpaid_period": "August 2026, September 2026",
  "still_employed": false,
  "employment_proof": "Offer letter, salary slips",
  "communications_so_far": "HR claims company is in loss, promised payment later",
  "city_state": "Noida",
  "summary": "Unpaid salary for August and September 2026 after resigning from a Noida startup.",
  "amount_due": 140000,
  "last_working_day": "2026-09-30"
 },
 "timeline": [
  {
   "date": "2026-09-30",
   "event": "Resignation and last working day"
  }
 ],
 "evidence_have": [
  "Offer letter",
  "Salary slips"
 ],
 "evidence_missing": [
  "Written communication/emails regarding salary demand"
 ],
 "next_step": "Draft a formal email to HR demanding the unpaid salary."
}
```

## Draft document

LEGAL NOTICE

By Registered Post A.D.

Date: [[FILL: Date of sending]]

From:
[[FILL: Your Full Name]]
[[FILL: Your Address]]

To:
[[FILL: Name of HR Manager or Director]]
[[FILL: Company Name]]
[[FILL: Company Address]]

Subject: Demand for payment of outstanding salary for August and September 2026.

Dear Sir/Madam,

1. I was employed as a Software Developer at your establishment. My last working day was 30 September 2026.

2. My monthly salary was Rs 70,000. The salary for the months of August 2026 and September 2026, amounting to a total of Rs 1,40,000, remains unpaid.

3. I have previously requested the release of these dues, but I have been informed by your HR department that the payment is delayed due to company losses.

4. Under Section 17 of the Code on Wages, 2019, wages are required to be paid by the prescribed deadlines. The non-payment of my earned wages is a violation of these provisions.

5. I hereby demand that you pay the outstanding amount of Rs 1,40,000 within 15 days of the receipt of this notice. Please remit the payment to the following bank account:
   Account Holder Name: [[FILL: Your Name]]
   Bank Name: [[FILL: Bank Name]]
   Account Number: [[FILL: Account Number]]
   IFSC Code: [[FILL: IFSC Code]]

6. If you fail to comply with this demand within the stipulated period, I shall be constrained to initiate legal proceedings for the recovery of my dues, including filing a claim before the appointed authority under Section 45 of the Code on Wages, 2019, at your sole risk, cost, and consequence.

Copy retained for record.

Sincerely,

[[FILL: Your Name]]
[[FILL: Your Phone Number]]
[[FILL: Your Email Address]]

**Send instructions:** ["इस नोटिस का प्रिंट आउट निकालें और उस पर अपने हस्ताक्षर करें।", "इसे 'Registered Post A.D.' के माध्यम से कंपनी के पते पर भेजें।", "पोस्ट ऑफिस से मिली रसीद और 'A.D. card' (जो डिलीवरी के बाद वापस आएगा) को संभाल कर रखें, यह कोर्ट में सबूत के तौर पर काम आएगा।", "यदि 15 दिनों के भीतर कोई जवाब या भुगतान नहीं मिलता है, तो आप 'SAMADHAN' पोर्टल (https://samadhan.labour.gov.in) पर शिकायत दर्ज कर सकते हैं या श्रम आयुक्त (Labour Commissioner) के कार्यालय में संपर्क कर सकते हैं।"]

## Automatic checks

| check | pass | detail |
|---|---|---|
| category | ✅ | got salary |
| reply_language | ✅ | expected Devanagari, reply script Devanagari |
| fact:monthly_salary | ✅ | expected ~70, got 70000 |
| fact:last_working_day | ✅ | expected ~2026-09-30, got 2026-09-30 |
| escalation<=urgent | ✅ | got recommended |
| no_unverified_law_shown | ✅ |  |
| draft_no_unverified_law | ✅ | [] |
| draft_has_no_invented_fill | ✅ | 12 placeholders |
