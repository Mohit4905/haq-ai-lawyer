"""Offline tests for the deterministic parts (no API key needed).

    python -m tests.test_offline
"""
from __future__ import annotations

import json
import sys
import tempfile
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app import guard, kb, rules  # noqa: E402

FIXTURE = [
    {"id": "CPA2019-S69", "act": "Consumer Protection Act, 2019", "section": "69", "title": "Limitation", "plain": "Complaint within two years.", "categories": ["consumer"], "source_url": "x", "source_type": "primary", "verified": True},
    {"id": "CPA2019-S35", "act": "Consumer Protection Act, 2019", "section": "35", "title": "Complaint", "plain": "Filing.", "categories": ["consumer"], "source_url": "x", "source_type": "primary", "verified": True},
    {"id": "NIA1881-S138", "act": "Negotiable Instruments Act, 1881", "section": "138", "title": "Dishonour", "plain": "30 days to send notice, 15 days to pay.", "categories": ["cheque_bounce"], "source_url": "x", "source_type": "primary", "verified": True},
    {"id": "NIA1881-S142", "act": "Negotiable Instruments Act, 1881", "section": "142", "title": "Cognizance", "plain": "Complaint within one month.", "categories": ["cheque_bounce"], "source_url": "x", "source_type": "primary", "verified": True},
    {"id": "LIM1963-ART55", "act": "Limitation Act, 1963", "section": "Article 55", "title": "Breach of contract", "plain": "Three years.", "categories": ["tenancy"], "source_url": "x", "source_type": "primary", "verified": True},
    {"id": "CPC1908-O37", "act": "Code of Civil Procedure, 1908", "section": "Order XXXVII", "title": "Summary suits", "plain": "...", "categories": ["tenancy"], "source_url": "x", "source_type": "primary", "verified": True},
    {"id": "FAKE-UNVERIFIED", "act": "Some Act, 2000", "section": "5", "title": "x", "plain": "x", "categories": ["consumer"], "source_url": "x", "source_type": "secondary", "verified": False},
]


def setup():
    tmp = Path(tempfile.mkdtemp()) / "laws.json"
    tmp.write_text(json.dumps(FIXTURE), encoding="utf-8")
    kb.KB_PATH = tmp
    kb.load_kb.cache_clear()


def test_kb_filters_unverified():
    ids = {e["id"] for e in kb.load_kb()}
    assert "FAKE-UNVERIFIED" not in ids and "CPA2019-S69" in ids


def test_guard_accepts_verified():
    r = guard.check("You can file under Section 35 of the Consumer Protection Act, 2019 within the limit in Section 69 of the Consumer Protection Act.")
    assert r.ok, r.violations
    assert len(r.verified) == 2


def test_guard_rejects_invented_section():
    r = guard.check("Under Section 12A of the Consumer Protection Act, 2019 you get triple compensation.")
    assert not r.ok and r.violations[0]["type"] == "unknown_section"


def test_guard_rejects_case_law():
    for t in ["As held in Ramesh Kumar v. Sunita Devi, deposits must be returned.", "See AIR 2015 SC 1234.", "(2019) 4 SCC 123 says so.", "The Supreme Court has held that landlords must pay interest."]:
        r = guard.check(t)
        assert any(v["type"] == "case_law" for v in r.violations), t


def test_guard_rejects_outdated_law():
    r = guard.check("File an FIR under IPC 420 for cheating.")
    assert any(v["type"] == "outdated_law" for v in r.violations)
    r = guard.check("धारा 420 आईपीसी के तहत केस करें")
    assert any(v["type"] == "outdated_law" for v in r.violations)
    # mentioning that it was replaced is fine
    r = guard.check("The IPC was replaced by the BNS in 2024.")
    assert not any(v["type"] == "outdated_law" for v in r.violations)


def test_guard_rejects_unknown_act():
    r = guard.check("The Tenant Deposit Protection Act, 2018 requires refund within 10 days.")
    assert any(v["type"] == "unknown_act" for v in r.violations), r.violations


def test_guard_hindi_section():
    r = guard.check("परक्राम्य लिखत अधिनियम की धारा 138 के तहत नोटिस भेजें।")
    assert r.ok, r.violations
    r = guard.check("उपभोक्ता संरक्षण अधिनियम की धारा 999 के तहत")
    assert not r.ok


def test_guard_orders_and_articles():
    assert guard.check("A summary suit under Order XXXVII of the Code of Civil Procedure may be possible.").ok
    assert guard.check("Under Article 55 of the Limitation Act you have three years.").ok
    assert not guard.check("Under Article 999 of the Limitation Act").ok


def test_guard_no_false_positive_plain_text():
    for t in ["Send a legal notice by registered post and keep the receipt.", "Call the National Consumer Helpline on 1915.", "Please share your PIN Code and order ID.", "Keep screenshots of WhatsApp chats."]:
        r = guard.check(t)
        assert r.ok, (t, r.violations)


def test_number_warning():
    r = guard.check("You must reply within 45 days.", support_text="nothing here")
    assert any(w["type"] == "unsupported_number" for w in r.warnings)
    r = guard.check("Send the notice within 30 days.", support_text="30 days to send notice")
    assert not r.warnings


def test_strip():
    r = guard.check("Good advice here. As held in Ram v. Shyam, you win. More advice.")
    out = guard.strip_violations("Good advice here. As held in Ram v. Shyam, you win. More advice.", r)
    assert "Ram v. Shyam" not in out and "Good advice here." in out


def test_cheque_deadlines():
    out = rules.compute("cheque_bounce", {"cheque_date": "2026-10-15", "memo_received_date": "2026-10-27"}, today=date(2026, 11, 6))
    d = {x["basis"] + x["label"][:10]: x for x in out["deadlines"]}
    notice = next(x for x in out["deadlines"] if "legal demand notice" in x["label"])
    assert notice["date"] == "2026-11-26" and notice["days_left"] == 20 and notice["status"] == "ok"
    validity = next(x for x in out["deadlines"] if "validity" in x["label"])
    assert validity["date"] == "2027-01-14"


def test_cheque_passed():
    out = rules.compute("cheque_bounce", {"memo_received_date": "2026-08-10"}, today=date(2026, 11, 6))
    assert out["deadlines"][0]["status"] == "passed"


def test_cheque_complaint_window():
    out = rules.compute("cheque_bounce", {"notice_received_date": "2026-11-01"}, today=date(2026, 11, 6))
    pay = next(x for x in out["deadlines"] if "15 days" in x["label"])
    comp = next(x for x in out["deadlines"] if "criminal complaint" in x["label"])
    assert pay["date"] == "2026-11-16" and comp["date"] == "2026-12-16"


def test_consumer_forum_and_fee():
    out = rules.compute("consumer", {"amount_paid": "18,499", "problem_date": "2026-09-10"}, today=date(2026, 11, 6))
    der = {x["label"]: x["value"] for x in out["derived"]}
    assert der["Where to file"].startswith("District") and der["Filing fee"] == "Nil"
    assert out["deadlines"][0]["date"] == "2028-09-10"
    out = rules.compute("consumer", {"amount_paid": "85 lakh"})
    assert {x["label"]: x["value"] for x in out["derived"]}["Where to file"].startswith("State")
    out = rules.compute("consumer", {"amount_paid": "₹3 crore"})
    assert {x["label"]: x["value"] for x in out["derived"]}["Where to file"].startswith("National")


def test_salary_two_working_days():
    out = rules.compute("salary", {"last_working_day": "2026-09-30"}, today=date(2026, 11, 6))  # Wed
    assert out["deadlines"][0]["date"] == "2026-10-02"
    out = rules.compute("salary", {"last_working_day": "2026-10-02"}, today=date(2026, 11, 6))  # Fri -> Sat, Mon
    assert out["deadlines"][0]["date"] == "2026-10-05"


def test_parse_inr():
    assert rules.parse_inr("₹1,35,000") == 135000
    assert rules.parse_inr("1.5 lakh") == 150000
    assert rules.parse_inr("2 crore") == 2e7
    assert rules.parse_inr(60000) == 60000


def test_red_flags():
    assert rules.red_flags("they may arrest him, FIR filed")[0]["level"] == "urgent"
    assert any(f["level"] == "emergency" for f in rules.red_flags("suicide kar lunga"))
    assert any(f["level"] == "emergency" for f in rules.red_flags("मेरे पति मुझे रोज़ मारते हैं"))
    assert not rules.red_flags("My landlord is not returning my deposit of 40,000")
    assert any(f["level"] == "urgent" for f in rules.red_flags("got the mutation done in his name"))


def test_base_section():
    assert kb.base_section("Schedule, Article 55") == "art55"
    assert kb.base_section("Order XXXVII") == "order37"
    assert kb.base_section("2(7)") == "2"
    assert kb.base_section("142(1)") == "142"
    assert kb.base_section("Rule 4(5)") == "rule4"


def test_limitation_article_vs_section():
    assert guard.check("A suit must be filed within three years under Article 55 of the Limitation Act, 1963.").ok
    assert not guard.check("Under s.55 of Limitation Act, 1963 you have 3 years.").ok


def test_strip_keeps_list_structure():
    text = "Steps:\n1. Send a notice. The period is under s.55 of Limitation Act, 1963 here.\n2. File a suit."
    r = guard.check(text)
    out = guard.strip_violations(text, r)
    assert "1. Send a notice." in out and "2. File a suit." in out and "s.55" not in out, out


def test_no_misattribution():
    # s.138 must not be attributed to the CPC just because the CPC is named later in the sentence
    t = "The 30-day window to send a notice (s.138) has closed. You can file a summary suit (Code of Civil Procedure, 1908 Order XXXVII) instead."
    r = guard.check(t)
    assert r.ok, r.violations
    assert not guard.check("Section 138 of the Code of Civil Procedure, 1908 applies.").ok


def test_mixed_script_message():
    msg = "मुझे वकील का नोटिस आया है अंग्रेज़ी में, समझ नहीं आ रहा। लिखा है: 'Under instructions from my client Mr. S.K. Verma, I hereby call upon you to pay Rs. 1,00,000 towards damages caused to the premises within 15 days of receipt of this notice.' मैंने वो फ्लैट 2 महीने पहले खाली किया था।"
    assert guard.detect_script(msg) == "Devanagari"


def test_overclaim():
    for t in ["You have an open-and-shut case.", "You will definitely win.", "I guarantee a refund.", "Aap pakka jeet jaoge",
              "Your claim is watertight.", "I am 100% sure you will get it.",
              "As a senior advocate, I have to be honest with you.", "I am your lawyer and I say file it."]:
        assert any(v["type"] == "overclaim" for v in guard.check(t).violations), t
    # a lawyer's assessment of strength is allowed; only promised outcomes are blocked
    for t in ["No one can guarantee a win in court.", "The phone has a warranty and a guarantee card.", "From what you've told me, you have good grounds.",
              "On these facts you have a strong case.", "Keeping the deposit without bills is a clear breach of the agreement."]:
        assert not any(v["type"] == "overclaim" for v in guard.check(t).violations), t


def test_maintenance_not_family():
    # society/building maintenance charges are not a family-law matter
    assert not any("Family" in f["reason"] for f in rules.red_flags("pay Rs 50,000 towards unpaid maintenance charges of the society"))
    assert any("Family" in f["reason"] for f in rules.red_flags("I want maintenance from my husband and custody of my child"))
    assert any("Family" in f["reason"] for f in rules.red_flags("मुझे गुजारा भत्ता चाहिए"))


def test_notice_threat_flag():
    assert any(f["level"] == "recommended" for f in rules.red_flags("failing which my client shall initiate appropriate civil proceedings against you at your risk as to costs"))


def test_detect_script():
    assert guard.detect_script("मेरा पैसा") == "Devanagari"
    assert guard.detect_script("bhai mera paisa nahi de raha") == "Hinglish"
    assert guard.detect_script("My landlord is not returning my deposit") == "Latin"
    assert guard.detect_script("நான் சென்னையில்") == "Tamil"
    assert guard.detect_script("আমি কলকাতায়") == "Bengali"


def test_draft_fill_grounding():
    from app.documents import _grounded, blanks
    assert _grounded("1 September 2025", "I paid the deposit on 1 September 2025", "start date of tenancy")
    assert not _grounded("6 November 2026", "my name is Priya", "date of sending")  # invented date rejected
    assert _grounded("6 November 2026", "send it today", "date of sending")
    assert _grounded("Priya Sharma", "my name is priya sharma", "your full name")
    assert not _grounded("Ramesh Gowda", "my name is Priya", "landlord's name")
    assert blanks("A [[FILL: your full name]] B [[FILL: Your full name]] C [[FILL]]") == ["your full name", "missing detail"]


if __name__ == "__main__":
    setup()
    fails = 0
    tests = [(n, f) for n, f in sorted(globals().items()) if n.startswith("test_") and callable(f)]
    for n, f in tests:
        try:
            f()
            print("PASS", n)
        except AssertionError as e:
            fails += 1
            print("FAIL", n, e)
    print(f"\n{len(tests) - fails}/{len(tests)} passed")
    sys.exit(1 if fails else 0)
