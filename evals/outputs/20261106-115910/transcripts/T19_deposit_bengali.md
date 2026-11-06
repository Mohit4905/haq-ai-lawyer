# T19_deposit_bengali
Group: language

## Turn 1

**User:** আমি কলকাতায় ভাড়া বাড়ি ছেড়েছি ১ অক্টোবর ২০২৬। ৩০,০০০ টাকা অগ্রিম দিয়েছিলাম। বাড়িওয়ালা টাকা ফেরত দিচ্ছে না। কী করব?

**Haq** (gemini/gemini-3.1-flash-lite, 15.04s):

আমি দুঃখিত যদি আপনার মনে হয় কোনো ভুল তথ্য দেওয়া হয়েছে। আমি সেই তথ্যটিই ব্যবহার করছি।

**আপনার আইনি অবস্থান:**
আপনার জমার টাকা ফেরত পাওয়ার অধিকার আছে। বাড়ি ছাড়ার পর বাড়িওয়ালা যুক্তিসঙ্গত কারণ ছাড়া টাকা আটকে রাখতে পারেন না। ১ অক্টোবর ২০২৬-এ বাড়ি ছাড়ার পর থেকে আপনার কাছে আইন অনুযায়ী টাকা আদায়ের জন্য যথেষ্ট সময় আছে।

**আইন যা আপনি উল্লেখ করতে পারেন:**
* এটি আপনার টাকা ফেরতের দাবির মূল ভিত্তি।
* **লিমিটেশন অ্যাক্ট, ১৯৬৩ (আর্টিকেল ৫৫):** বাড়ি ছাড়ার তারিখ থেকে ৩ বছরের মধ্যে আপনি টাকা ফেরতের জন্য মামলা করতে পারেন।

**এখন যা করবেন:**
1. বাড়িওয়ালাকে একটি লিখিত অনুরোধ (WhatsApp বা ইমেইল) পাঠান, যেখানে বাড়ি ছাড়ার তারিখ এবং আপনার ব্যাংক ডিটেইলস থাকবে। এর স্ক্রিনশট বা কপি রেখে দিন।
2. যদি তাতে কাজ না হয়, তবে একটি আইনি নোটিশ (Legal Notice) পাঠান।
3. কোনো সমাধান না হলে, ডিস্ট্রিক্ট লিগ্যাল সার্ভিসেস অথরিটি (DLSA)-এর সাথে যোগাযোগ করুন (হেল্পলাইন: ১৫১০০)।

**আপনার কাছে আমার প্রশ্ন:**
১. আপনার কি বাড়িওয়ালার সাথে কোনো লিখিত ভাড়ার চুক্তি (Rent Agreement) আছে?
২. টাকা ফেরতের জন্য আপনি এখন পর্যন্ত কীভাবে যোগাযোগ করেছেন (ফোন বা মেসেজ)?

_⚠️ I removed a legal reference I could not verify. Please confirm the exact law with a lawyer or free legal aid (NALSA helpline 15100)._

**Law you can cite (checked against official sources):**
- **Section 73, Indian Contract Act, 1872**: If someone breaks a contract with you, you can claim money for the loss it caused.
- **Article 55, Limitation Act, 1963**: A suit for compensation for breach of a contract (written or implied), where no other article covers it specifically, must be filed within 3 years.

> 🛡️ Guard caught (before user saw it): [{"type": "unknown_section", "text": "ধারা ৭৩", "why": "Not in the verified library."}]  
> repaired=True stripped=True

**Calculated by code:** {"deadlines": [{"label": "Approximate last date to sue for the deposit (3 years)", "date": "2029-10-01", "days_left": 1060, "status": "ok", "basis": "LIM1963-ART55", "note": "Limitation depends on the exact claim; confirm with legal aid before relying on it.", "user_deadline": true}], "derived": []}

_Escalation:_ {"level": "none", "reasons": []}  _Citations:_ ['ICA1872-S73', 'LIM1963-ART55', 'FACT-NALSA-HELPLINE']

## Final case file

```json
{
 "category": "tenancy",
 "language": "Bengali",
 "script": "Bengali",
 "facts": {
  "deposit_amount": 30000,
  "possession_handed_over_date": "2026-10-01",
  "city_state": "Kolkata",
  "summary": "Landlord refusing to return security deposit of 30,000 after vacating the property."
 },
 "timeline": [
  {
   "date": "2026-10-01",
   "event": "Vacated the property"
  }
 ],
 "evidence_have": [],
 "evidence_missing": [
  "Written rent agreement",
  "Proof of deposit payment",
  "Records of communication with landlord"
 ],
 "next_step": "Send a formal written request (WhatsApp/Email) demanding the deposit back."
}
```

## Automatic checks

| check | pass | detail |
|---|---|---|
| category | ✅ | got tenancy |
| reply_language | ✅ | expected Bengali, reply script Bengali |
| escalation<=recommended | ✅ | got none |
| no_unverified_law_shown | ✅ |  |
