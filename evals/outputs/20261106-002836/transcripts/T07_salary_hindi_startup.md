# T07_salary_hindi_startup
Group: core

## Turn 1

**User:** मैं नोएडा की एक स्टार्टअप में सॉफ्टवेयर डेवलपर था, सैलरी 70,000 महीना। अगस्त और सितंबर 2026 की सैलरी नहीं मिली। मैंने 30 सितंबर 2026 को रिज़ाइन कर दिया था, आख़िरी दिन वही था। HR कहता है कंपनी घाटे में है, बाद में देंगे। ऑफ़र लेटर और पुरानी सैलरी स्लिप मेरे पास हैं।

**Haq** (groq/openai/gpt-oss-120b, 29.28s):

नमस्ते! आपके पास ऑफ़र लेटर और पुरानी सैलरी स्लिप है, जो बहुत मददगार हैं।

**आपकी स्थिति**
- अगस्त‑सितंबर 2026 की दो महीने की सैलरी (₹1,40,000) नहीं मिली।
- आपने 30 सितंबर 2026 को इस्तीफ़ा दिया, वही आपका आख़िरी कार्यदिवस था।
- HR ने कहा कि कंपनी घाटे में है, बाद में भुगतान करेगी।

**मुख्य बिंदु**
- कोड ऑन वेजेज 2019 के तहत सभी कर्मचारियों को समय पर वेतन मिलना अनिवार्य है (सभी वेतन पर कोई सीमा नहीं) [COW2019‑S2K][FACT‑COW‑NO‑WAGE‑CEILING]।
- इस्तीफ़ा के बाद अंतिम वेतन 2 कार्य दिवसों के भीतर देना चाहिए [COW2019‑S17]।
- आप 3 साल के भीतर लेबर अथॉरिटी में दावा दायर कर सकते हैं [COW2019‑S45]।

**आपके विकल्प**
1. **लिखित मांग (ई‑मेल/पत्र)** – HR को स्पष्ट राशि, अवधि और भुगतान की अंतिम तिथि (उदाहरण 15 अक्टूबर 2026) के साथ भेजें। लागत 0 ₹, समय 1‑2 दिन।
2. **डिमांड नोटिस** – 15 दिन की नोटिस भेजें; अगर जवाब नहीं मिला तो आगे की कार्रवाई आसान होगी।
3. **लेबर अथॉरिटी में दावा** – SAMADHAN पोर्टल या स्थानीय इंस्पेक्टर‑क्यूम‑फैसिलिटेटर को फ़ाइल करें। समय 2‑4 हफ़्ते, कोई फ़ीस नहीं (यदि आप मुफ्त कानूनी सहायता चाहते हैं तो NALSA 15100 पर कॉल कर सकते हैं)।
4. **लोक अदालत / मध्यस्थता** – यदि दोनों पक्ष सहमत हों तो तेज़ समाधान।
5. **सिविल मुकदमा** – बड़े या जटिल मामलों में वकील की जरूरत होगी।

**सुझावित अगला कदम**: HR को डिमांड नोटिस भेजें (15 दिन की समय सीमा) – यह सबसे सस्ता और तेज़ तरीका है।

मैं आपके लिए डिमांड नोटिस का ड्राफ्ट तैयार कर सकता हूँ या आप इसे खुद लिखने का अभ्यास कर सकते हैं।

⚠️ **Deadline check (calculated by Haq, not AI):** Full & final wages were due by (2 working days after leaving): **02 Oct 2026**, which has passed. Please speak to a lawyer or free legal aid (15100) soon to check what options remain.

**Calculated by code:** {"deadlines": [{"label": "Full & final wages were due by (2 working days after leaving)", "date": "2026-10-02", "days_left": -35, "status": "passed", "basis": "COW2019-S17", "note": "Assumes a Mon–Sat working week.", "user_deadline": true}, {"label": "Approximate last date to file a wage claim with the labour authority (3 years)", "date": "2029-09-30", "days_left": 1059, "status": "ok", "basis": "COW2019-S45", "note": "", "user_deadline": true}], "derived": []}

_Escalation:_ {"level": "recommended", "reasons": ["If no response to notice, filing a claim with labour authority may need guidance", "Deadline passed: Full & final wages were due by (2 working days after leaving) (2026-10-02)"]}  _Citations:_ ['COW2019-S2K', 'FACT-COW-NO-WAGE-CEILING', 'COW2019-S17', 'COW2019-S45']

## Final case file

```json
{
 "category": "salary",
 "language": "Hindi",
 "script": "Devanagari",
 "facts": {
  "other_party_name": "Startup company in Noida",
  "user_name": "Unknown",
  "role": "Software Developer",
  "monthly_salary": 70000,
  "unpaid_period": "2026-08-01 to 2026-09-30",
  "amount_due": 140000,
  "still_employed": false,
  "employment_proof": "Offer letter and old salary slips",
  "communications_so_far": "HR said company is in loss and will pay later",
  "city_state": "Noida, India",
  "summary": "Software developer in Noida startup not paid August and September 2026 salaries after resignation on 30 Sep 2026.",
  "last_working_day": "2026-09-30"
 },
 "timeline": [
  {
   "date": "2026-09-30",
   "event": "Resignation submitted, last working day"
  }
 ],
 "evidence_have": [
  "Offer letter",
  "Previous salary slips",
  "HR email/communication stating delay"
 ],
 "evidence_missing": [
  "Resignation email or letter copy",
  "Bank statements showing non‑receipt of salary"
 ],
 "next_step": "Send a 15‑day demand notice to HR"
}
```

## Draft document

**LEGAL NOTICE** (By Registered Post A.D.)

Date: [[FILL: date]]

**From:**
[[FILL: Your Full Name]]
[[FILL: Your Complete Residential Address]]
Phone: [[FILL: Your Phone Number]]
Email: [[FILL: Your Email Address]]

**To:**
[[FILL: HR/Employer Name]]
Startup Company in Noida
[[FILL: Company Registered Address]]
Noida, Uttar Pradesh, India

**Subject:** Demand for payment of unpaid salary for August & September 2026 and full & final settlement.

1. I was employed by the above‑named startup as a **Software Developer** on the terms stated in the offer letter dated [[FILL: offer letter date]].
2. My agreed monthly salary was **₹70,000** per month, as reflected in the salary slips for the months prior to August 2026.
3. I submitted my resignation on **30 September 2026**, which was also my last working day, as per the resignation submission record.
4. The salary for the months of **August 2026** and **September 2026** (total **₹1,40,000**) has not been paid to date.
5. I have repeatedly requested payment from the HR department. The HR representative replied that the company is currently incurring losses and the dues will be cleared later, but no concrete date or payment has been provided.
6. I possess the following documentary evidence: the original offer letter, salary slips for the months prior to August 2026, and the email communication from HR indicating the delay.

**Legal Basis**
Under the **Code on Wages, 2019**, an *employee* includes any person engaged on wages for skilled or unskilled work (s.2(k)). The Code applies to all employees irrespective of salary level (Fact‑COW‑NO‑WAGE‑CEILING). Section 17 of the Code mandates that monthly wages must be paid **before the end of the 7th day of the next month**. My salary for August and September 2026 became due on **7 October 2026** and **7 November 2026** respectively, both of which have long passed (COW2019‑S17).

**Demand**
I hereby demand payment of the full unpaid salary amounting to **₹1,40,000** within **15 days** from the receipt of this notice. Payment should be made by direct bank transfer to the following account:

Account Holder: [[FILL: Your Name]]
Account Number: [[FILL: Your Bank Account Number]]
IFSC Code: [[FILL: Your Bank IFSC]]
Bank Name: [[FILL: Your Bank Name]]

**Consequences of Non‑Compliance**
If the amount is not received within the stipulated period, I will be compelled to pursue all lawful remedies available to me, including:
- Filing a wage claim before the appropriate labour authority under **Section 45** of the Code on Wages, 2019 (COW2019‑S45);
- Initiating a civil suit for recovery of wages within the three‑year limitation period (Limitation Act 1963, Article 7);
- Seeking recovery of costs and interest as permitted by law.

All expenses incurred in pursuing these remedies will be borne by the employer.

**Copy retained for record.**

______________________________
[[FILL: Your Full Name]]
Phone: [[FILL: Your Phone Number]]
Email: [[FILL: Your Email Address]]

**Send instructions:** ["1. इस नोटिस को रजिस्टर्ड पोस्ट (रिटर्न रिसीट के साथ) द्वारा कंपनी के पंजीकृत पते पर भेजें।", "2. पोस्टिंग के बाद रिटर्न रिसीट की एक कॉपी सुरक्षित रखें; यह डिलीवरी प्रमाण के रूप में काम करेगी।", "3. यदि 15 दिनों के भीतर कोई उत्तर नहीं मिलता, तो SAMADHAN पोर्टल (https://samadhan.labour.gov.in) पर wage claim दर्ज करें और रिटर्न रिसीट की स्कैन की हुई कॉपी अपलोड करें।", "4. साथ ही, 3 साल की सीमित अवधि के भीतर सिविल suit दायर करने की तैयारी करें; आवश्यक दस्तावेज़ (ऑफ़र लेटर, सैलरी स्लिप, HR ई‑मेल) को क्रमबद्ध रखें।", "5. यदि आर्थिक कठिनाई हो तो 15100 (NALSA) पर कॉल करके मुफ्त कानूनी सहायता या लोक अदालत (Lok Adalat) के माध्यम से निपटारा करने की जानकारी प्राप्त करें।"]

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
