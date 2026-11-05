"""Run one conversation turn from the command line and print the interesting parts.

    python -m scripts.one_turn "your message" [provider]
"""
import json
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from app import engine  # noqa: E402

msg = sys.argv[1]
prov = sys.argv[2] if len(sys.argv) > 2 else None
r = engine.turn(None, msg, provider=prov, today=date(2026, 11, 6))
if r.get("error"):
    print("ERROR", r["error"])
    sys.exit(1)
print("REPLY:\n", r["reply"])
print("\nCATEGORY:", r["state"]["case"]["category"], "| LANG:", r["state"]["case"]["language"], r["state"]["case"]["script"])
print("FACTS:", json.dumps(r["state"]["case"]["facts"], ensure_ascii=False))
print("CALC:", json.dumps(r["calculated"], ensure_ascii=False))
print("CITATIONS:", [c["id"] for c in r["citations"]])
print("GUARD initial violations:", json.dumps(r["guard"]["initial"]["violations"], ensure_ascii=False))
print("GUARD final:", r["guard"]["final"]["ok"], "repaired:", r["guard"]["repaired"], "stripped:", r["guard"]["stripped"])
print("ESCALATION:", r["needs_lawyer"])
print("ACTIONS:", r["actions"])
print("MODEL:", r["model"]["provider"], r["model"]["model"], "latency", r["latency_s"])
