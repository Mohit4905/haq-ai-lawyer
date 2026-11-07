"""Real-model test: legal answers cite the right verified provisions for the question asked.

    python scripts/qa/citations_test.py http://127.0.0.1:8000 [out_dir]

For each question (fresh conversation): the expected provisions are cited (law chips), none from an
unrelated area, the guard passed, and the reply explains them. Replies are saved for reading."""
import json
import re
import sys
import time
from datetime import datetime
from pathlib import Path

import httpx

URL = sys.argv[1].rstrip("/")
OUT = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("evals/outputs") / (datetime.now().strftime("%Y%m%d-%H%M%S") + "_citations")
OUT.mkdir(parents=True, exist_ok=True)

# question, must cite (all), must cite at least one of, must NOT cite (id prefixes from unrelated areas), words the reply must contain (any)
CASES = [
    ("Explain the Right to Equality.", ["COI-ART14", "COI-ART15", "COI-ART16", "COI-ART17"], [], ["BNS", "HMA", "IRC", "CPA"], ["equal"]),
    ("What is the Right to Freedom of Speech?", ["COI-ART19"], ["COI-ART19-2"], ["BNS", "HMA", "IRC", "CPA"], ["reasonable restriction"]),
    ("What are my Fundamental Rights?", ["COI-ART14", "COI-ART19", "COI-ART21", "COI-ART32"], [], ["HMA", "IRC", "CPA"], ["fundamental"]),
    ("Can the police arrest me without a warrant?", ["BNSS2023-S35"], ["BNSS2023-S47", "BNSS2023-S58", "COI-ART22"], ["HMA", "IRC", "CPA"], ["warrant"]),
    ("What is the punishment for theft in India?", ["BNS2023-S303"], [], ["HMA", "IRC", "CPA", "COI-ART16"], ["three years", "3 years"]),
    ("What are my rights as a consumer?", ["CPA2019-S2-9"], [], ["HMA", "IRC", "BNSS2023-S35"], ["consumer"]),
    ("What can I do if someone commits online fraud?", ["FACT-CYBER-1930"], ["BNS2023-S318", "BNSS2023-S173"], ["HMA", "IRC"], ["1930"]),
    ("What are the legal provisions related to divorce?", ["HMA1955-S13", "HMA1955-S13B"], [], ["IRC", "CPA", "BNSS2023-S35"], ["mutual consent"]),
    ("Can my employer terminate me without notice?", ["IRC2020-S70"], [], ["HMA", "CPA", "BNS2023-S303"], ["notice"]),
    ("What does Article 21 of the Indian Constitution say?", ["COI-ART21"], [], ["HMA", "IRC", "CPA", "BNS2023-S303"], ["personal liberty"]),
]


def post(msg):
    for attempt in range(3):
        j = httpx.post(URL + "/api/chat", json={"state": None, "message": msg, "lang_pref": "English"}, timeout=300).json()
        if not j.get("error") or attempt == 2:
            return j
        time.sleep(25)
    return j


rows, passed = [], 0
for q, must, any_of, never, words in CASES:
    j = post(q)
    reply = j.get("reply") or ""
    low = " ".join(reply.lower().split())
    cited = [c["id"] for c in (j.get("citations") or [])]
    checks = {
        "no_error": not j.get("error"),
        "legal": j.get("intent") == "legal",
        "cites_required": all(m in cited for m in must),
        "cites_one_of": (not any_of) or any(a in cited for a in any_of),
        "nothing_unrelated": not any(c.startswith(p) for c in cited for p in never),
        "guard_ok": ((j.get("guard") or {}).get("final") or {}).get("ok", False),
        "explains": any(w in low for w in words) and len(reply) > 300,
        # "Section 303", "Article 21" or the short form "s.173" (test fix 7 Nov: "s.173" was not counted)
        "names_provisions_in_text": len(re.findall(r"(?i)\b(?:article|section)\s+\d|\bs\.\s?\d", reply)) >= 1,
    }
    ok = all(checks.values())
    passed += ok
    rows.append({"question": q, "pass": ok, "checks": checks, "cited": cited, "category": (j.get("state") or {}).get("case", {}).get("category"),
                 "lawyer_level": (j.get("needs_lawyer") or {}).get("level"), "guard": j.get("guard"), "model": j.get("model"), "reply": reply or j.get("error")})
    print(("PASS " if ok else "FAIL ") + f"{q} -> {rows[-1]['category']} | cited {cited} | " + ", ".join(k for k, v in checks.items() if not v))
    time.sleep(3)

(OUT / "results.json").write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")
md = [f"# Citation test ({datetime.now():%d %b %Y %H:%M})", "", f"**{passed}/{len(rows)} passed** against {URL}", "",
      "| # | Question | Cited (law chips) | Pass |", "|---|---|---|---|"]
md += [f"| {i + 1} | {r['question']} | {', '.join(r['cited'])} | {'✅' if r['pass'] else '❌ ' + ', '.join(k for k, v in r['checks'].items() if not v)} |" for i, r in enumerate(rows)]
md += ["", "## Replies", ""] + [f"### {i + 1}. {r['question']}\n_model: {(r['model'] or {}).get('provider')}/{(r['model'] or {}).get('model')}_\n\n{r['reply']}\n" for i, r in enumerate(rows)]
(OUT / "SUMMARY.md").write_text("\n".join(md), encoding="utf-8")
print(f"\n{passed}/{len(rows)} passed. Saved to {OUT}")
