# T19_deposit_bengali
Group: language

## Turn 1

**User:** আমি কলকাতায় ভাড়া বাড়ি ছেড়েছি ১ অক্টোবর ২০২৬। ৩০,০০০ টাকা অগ্রিম দিয়েছিলাম। বাড়িওয়ালা টাকা ফেরত দিচ্ছে না। কী করব?

**Haq** (gemini/gemini-3.1-flash-lite, 6.08s):

আপনার সমস্যার কথা শুনে খারাপ লাগল। বাড়ি ছাড়ার পর সিকিউরিটি ডিপোজিট (Security Deposit) ফেরত পাওয়া আপনার অধিকার। তবে এই বিষয়ে কিছু তথ্য জানা প্রয়োজন:

১. আপনার মাসিক ভাড়া কত ছিল?
২. আপনাদের কি কোনো লিখিত ভাড়ার চুক্তি (Rent Agreement) আছে?
৩. বাড়িওয়ালা কি কোনো কারণ দেখিয়েছেন (যেমন: রং করা বা মেরামতির খরচ) কেন তিনি টাকা ফেরত দিচ্ছেন না?
৪. আপনি কি তাকে টাকা ফেরত দেওয়ার জন্য কোনো মেসেজ বা ইমেল করেছেন? আপনার কাছে কি টাকা দেওয়ার কোনো প্রমাণ (ব্যাঙ্ক ট্রান্সফার বা রসিদ) আছে?

এই তথ্যগুলো পেলে আমি আপনাকে সঠিক পদক্ষেপ নিতে সাহায্য করতে পারব।

**Calculated by code:** {"deadlines": [{"label": "Approximate last date to sue for the deposit (3 years)", "date": "2029-10-01", "days_left": 1060, "status": "ok", "basis": "LIM1963-ART55", "note": "Limitation depends on the exact claim; confirm with legal aid before relying on it.", "user_deadline": true}], "derived": []}

_Escalation:_ {"level": "none", "reasons": []}  _Citations:_ ['ICA1872-S73', 'LIM1963-ART55']

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
  "monthly_rent",
  "written_agreement",
  "deductions_claimed",
  "communications_so_far",
  "proof_of_payment"
 ],
 "next_step": "Gather information about rent agreement and payment proof"
}
```

## Automatic checks

| check | pass | detail |
|---|---|---|
| category | ✅ | got tenancy |
| reply_language | ✅ | expected Bengali, reply script Bengali |
| escalation<=recommended | ✅ | got none |
| no_unverified_law_shown | ✅ |  |
