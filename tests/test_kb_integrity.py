"""Integrity checks against the REAL library (kb/laws.json). No API key needed.

    python -m tests.test_kb_integrity
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from app import guard, kb, rules  # noqa: E402

ids = set(kb.by_id())
fails = []

# 1. every id the code relies on exists and is verified
for cat, lst in kb.CATEGORY_IDS.items():
    for i in lst:
        if i not in ids:
            fails.append(f"CATEGORY_IDS[{cat}] -> missing {i}")
for cat, steps in rules.PLAYBOOKS.items():
    for s in steps:
        for i in re.findall(r"[A-Z][A-Z0-9]+-[A-Za-z0-9\-()]+", s):
            if i not in ids:
                fails.append(f"PLAYBOOKS[{cat}] -> missing {i}")
for name in ("FEE_BASIS", "FORUM_BASIS"):
    if getattr(rules, name) not in ids:
        fails.append(f"rules.{name} missing")
src = Path(rules.__file__).read_text(encoding="utf-8")
for i in set(re.findall(r'"((?:NIA|CPA|COW|LIM|MTA|CPECOM|FACT)[A-Z0-9\-()]*)"', src)):
    if i not in ids:
        fails.append(f"rules.py basis id missing: {i}")

# 2. every verified entry has an http source
for e in kb.load_kb():
    if not str(e.get("source_url", "")).startswith("http"):
        fails.append(f"{e['id']} has no source URL")

# 3. the guard accepts the library's own phrasing of each section (no false positives on correct citations)
for e in kb.load_kb():
    s = str(e.get("section") or "")
    if not s or not re.match(r"^\d", s) or "-" in s:
        continue
    text = f"See Section {s} of the {e['act']}."
    rep = guard.check(text)
    if not rep.ok:
        fails.append(f"guard rejects correct citation: {text} -> {rep.violations}")

print(f"{len(ids)} verified entries checked")
for f in fails:
    print("FAIL", f)
print("OK" if not fails else f"{len(fails)} problems")
sys.exit(1 if fails else 0)
