# T19_deposit_bengali
Group: language

## Turn 1

**User:** আমি কলকাতায় ভাড়া বাড়ি ছেড়েছি ১ অক্টোবর ২০২৬। ৩০,০০০ টাকা অগ্রিম দিয়েছিলাম। বাড়িওয়ালা টাকা ফেরত দিচ্ছে না। কী করব?

**Haq** (gemini/gemini-3.1-flash-lite, 8.9s):

আপনার সিকিউরিটি ডিপোজিট ফেরত পাওয়ার দাবিটি বেশ জোরালো। বাড়ি খালি করে দেওয়ার পর, বাড়িওয়ালার দায়িত্ব হলো আপনার পাওনা টাকা (কোনো বৈধ কর্তন বা deductions বাদে) ফেরত দেওয়া। আপনার হাতে ৩ বছরের সময়সীমা আছে, তাই এখনই আইনি পদক্ষেপ শুরু করা ভালো।

**আপনার আইনি অবস্থান:**
আপনার দাবিটি চুক্তির ওপর ভিত্তি করে। বাড়িওয়ালা যদি কোনো কারণ ছাড়া টাকা আটকে রাখেন, তবে আপনি তা উদ্ধারের জন্য আইনি ব্যবস্থা নিতে পারেন।

**যে আইন আপনি উল্লেখ করতে পারেন:**
* **Indian Contract Act, 1872, Section 73:** চুক্তিভঙ্গের কারণে আপনি আপনার পাওনা টাকার দাবি করতে পারেন। এটি আপনার নোটিশে উল্লেখ করা জরুরি।
* **Limitation Act, 1963, Article 55:** বাড়ি খালি করার পর থেকে ৩ বছরের মধ্যে আপনি টাকা উদ্ধারের জন্য মামলা করতে পারেন।

**এখন যা করবেন:**
1. বাড়িওয়ালাকে হোয়াটসঅ্যাপ বা ইমেইলে একটি লিখিত অনুরোধ পাঠান (টাকার পরিমাণ, বাড়ি ছাড়ার তারিখ এবং আপনার ব্যাংক ডিটেইলস উল্লেখ করুন)।
2. যদি তাতে কাজ না হয়, তবে একটি আইনি নোটিশ (Legal Notice) পাঠান।
3. প্রয়োজনে ডিস্ট্রিক্ট লিগ্যাল সার্ভিসেস অথরিটি (DLSA)-এর সাহায্য নিন (হেল্পলাইন: ১৫১০০)।

আমি আপনাকে প্রথম ধাপ হিসেবে একটি লিখিত অনুরোধের খসড়া তৈরি করতে সাহায্য করতে পারি।

**আমার যা জানা প্রয়োজন:**
১. আপনার কি বাড়িওয়ালার সাথে কোনো লিখিত ভাড়ার চুক্তি (Rent Agreement) আছে?
২. বাড়িওয়ালা কি কোনো মেরামতির খরচ বা অন্য কোনো কারণে টাকা কাটার কথা বলেছেন?

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
   "event": "Vacated property"
  }
 ],
 "evidence_have": [],
 "evidence_missing": [
  "Written rent agreement",
  "Proof of deposit payment",
  "Communication history with landlord"
 ],
 "next_step": "Send a formal written request via WhatsApp or email."
}
```

## Automatic checks

| check | pass | detail |
|---|---|---|
| category | ✅ | got tenancy |
| reply_language | ✅ | expected Bengali, reply script Bengali |
| escalation<=recommended | ✅ | got none |
| no_unverified_law_shown | ✅ |  |
