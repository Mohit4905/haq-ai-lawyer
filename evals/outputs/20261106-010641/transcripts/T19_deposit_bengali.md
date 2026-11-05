# T19_deposit_bengali
Group: language

## Turn 1

**User:** আমি কলকাতায় ভাড়া বাড়ি ছেড়েছি ১ অক্টোবর ২০২৬। ৩০,০০০ টাকা অগ্রিম দিয়েছিলাম। বাড়িওয়ালা টাকা ফেরত দিচ্ছে না। কী করব?

**Haq** (gemini/gemini-3.1-flash-lite, 10.33s):

আপনার সমস্যার জন্য আমি দুঃখিত। বাড়িওয়ালা সিকিউরিটি ডিপোজিট (Security Deposit) ফেরত না দিলে আপনি নিচের পদক্ষেপগুলো নিতে পারেন।

শুরু করার আগে আমার কিছু তথ্য জানা দরকার:
১. আপনার কি বাড়িওয়ালার সাথে কোনো লিখিত ভাড়ার চুক্তি (Rent Agreement) আছে?
২. বাড়িওয়ালা কি কোনো কারণ দেখিয়েছেন কেন টাকা ফেরত দিচ্ছেন না (যেমন: রং বা মেরামতির খরচ)?
৩. আপনি কি এখন পর্যন্ত বাড়িওয়ালার সাথে কথা বলেছেন বা মেসেজ/ইমেইল করেছেন? আপনার কাছে কি টাকা জমা দেওয়ার কোনো প্রমাণ (ব্যাংক ট্রান্সফার বা রসিদ) আছে?

আপনার কাছে এই তথ্যগুলো থাকলে আমাকে জানান। আপাতত আপনার জন্য করণীয়:
১. লিখিত অনুরোধ (WhatsApp/Email): বাড়িওয়ালাকে একটি স্পষ্ট মেসেজ বা ইমেইল পাঠান যেখানে আপনার বাড়ি ছাড়ার তারিখ, জমার পরিমাণ এবং টাকা ফেরত পাওয়ার জন্য আপনার ব্যাংক ডিটেইলস উল্লেখ থাকবে। এর স্ক্রিনশট বা কপি রেখে দিন।
২. আইনি নোটিশ (Legal Notice): যদি তারা সাড়া না দেয়, তবে আপনি নিজে একটি আইনি নোটিশ পাঠাতে পারেন।
৩. আইনি সহায়তা (Legal Aid): আপনি জেলা আইনি পরিষেবা কর্তৃপক্ষের (DLSA) মাধ্যমে বিনামূল্যে পরামর্শ বা লোক আদালতের সাহায্য নিতে পারেন (হেল্পলাইন: ১৫১০০)।

আপনার কাছে কি কোনো লিখিত চুক্তি আছে?

**Calculated by code:** {"deadlines": [{"label": "Approximate last date to sue for the deposit (3 years)", "date": "2029-10-01", "days_left": 1060, "status": "ok", "basis": "LIM1963-ART55", "note": "Limitation depends on the exact claim; confirm with legal aid before relying on it.", "user_deadline": true}], "derived": []}

_Escalation:_ {"level": "none", "reasons": []}  _Citations:_ ['ICA1872-S73', 'LIM1963-ART55', 'FACT-NALSA-HELPLINE', 'FACT-LOKADALAT-PRELITIGATION']

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
  "summary": "User vacated rented property in Kolkata and landlord is refusing to return the security deposit of 30,000."
 },
 "timeline": [
  {
   "date": "2026-10-01",
   "event": "Vacated rented property"
  }
 ],
 "evidence_have": [],
 "evidence_missing": [
  "Written rent agreement",
  "Proof of deposit payment",
  "Communication history with landlord",
  "Details of any deductions claimed by landlord"
 ],
 "next_step": "Send a formal written request via WhatsApp/Email to the landlord."
}
```

## Automatic checks

| check | pass | detail |
|---|---|---|
| category | ✅ | got tenancy |
| reply_language | ✅ | expected Bengali, reply script Bengali |
| escalation<=recommended | ✅ | got none |
| no_unverified_law_shown | ✅ |  |
