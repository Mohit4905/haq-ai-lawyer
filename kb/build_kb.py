"""Merge research files into kb/laws.json and validate them.

    python kb/build_kb.py

Every entry needs an id, act, title, plain summary, categories, a source URL and a
verified flag. Unverified entries are kept in the file (so reviewers can see what was
checked and rejected) but the app never shows them to the model.
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCES = sorted(HERE.glob("research_*.json")) + [HERE / "manual_facts.json"]
REQUIRED = ["id", "act", "title", "plain", "categories", "source_url", "verified"]

FACT_NAMES = {
    "FACT-NCH-HELPLINE": "National Consumer Helpline",
    "FACT-EJAGRITI-PORTAL": "e-Jagriti consumer e-filing portal",
    "FACT-RBI-CHEQUE-VALIDITY": "RBI cheque validity rule",
    "FACT-NALSA-HELPLINE": "NALSA legal aid helpline",
    "FACT-TELE-LAW": "Tele-Law service",
    "FACT-CYBER-1930": "National Cyber Crime helpline",
}

entries, seen, problems = [], set(), []
for src in SOURCES:
    if not src.exists():
        continue
    for e in json.loads(src.read_text(encoding="utf-8")):
        if not e.get("act"):
            # non-statutory facts (helplines, portals): name them by what they are
            e["act"] = FACT_NAMES.get(e.get("id"), e.get("title", ""))
        miss =[k for k in REQUIRED if k not in e or e[k] in (None, "")]
        if miss:
            problems.append(f"{src.name}:{e.get('id')} missing {miss}")
            continue
        if e["id"] in seen:
            problems.append(f"duplicate id {e['id']} in {src.name} (kept first)")
            continue
        if not str(e["source_url"]).startswith("http"):
            problems.append(f"{e['id']}: bad source_url")
            e["verified"] = False
        seen.add(e["id"])
        e["_from"] = src.name
        entries.append(e)

(HERE / "laws.json").write_text(json.dumps(entries, ensure_ascii=False, indent=1), encoding="utf-8")
v = sum(1 for e in entries if e["verified"])
print(f"laws.json: {len(entries)} entries ({v} verified, {len(entries) - v} unverified, excluded from the app)")
for p in problems:
    print("  !", p)
sys.exit(0)
