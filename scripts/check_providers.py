"""Check which configured providers work and list their available models.

    python -m scripts.check_providers
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import httpx  # noqa: E402

from app.config import PRESETS  # noqa: E402

for p in PRESETS.values():
    if not p.configured:
        continue
    try:
        h = {"Authorization": f"Bearer {p.api_key}"} if p.api_key else {}
        r = httpx.get(f"{p.base_url.rstrip('/')}/models", headers=h, timeout=20)
        if r.status_code >= 400:
            print(f"[{p.name}] HTTP {r.status_code}: {r.text[:200]}")
            continue
        ids = sorted(m.get("id", "") for m in r.json().get("data", []))
        print(f"[{p.name}] OK, {len(ids)} models. preset main={p.main_model} fast={p.fast_model}")
        for i in ids:
            print("   ", i)
    except Exception as e:
        print(f"[{p.name}] error: {e}")
