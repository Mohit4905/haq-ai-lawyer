"""API robustness + security audit against a local server (no paid calls: eCourts calls go to the fake server)."""
import io
import json
import sys

import httpx

U = sys.argv[1].rstrip("/")
res = []


def ok(name, cond, detail=""):
    res.append((name, bool(cond), detail)); print(("PASS " if cond else "FAIL ") + name + (f" | {detail}" if detail else ""))


c = httpx.Client(timeout=120)
P = lambda p, **kw: c.post(U + p, **kw)  # noqa: E731

# --- secrets / config
cfg = c.get(U + "/api/config").text
ok("config exposes no secret keys", not any(s in cfg for s in ("service_role", "eci_live", "gsk_", "AIza", "sk-", "xsmtpkey")))
ok("health endpoint works", c.get(U + "/api/health").status_code == 200)

# --- malformed input never 500s
cases = [
    ("chat: empty message", "/api/chat", {"message": "  "}, {400}),
    ("chat: missing message field", "/api/chat", {}, {422}),
    ("chat: message is a number", "/api/chat", {"message": 123}, {422}),
    ("draft: unknown doc type", "/api/draft", {"state": {"case": {}, "messages": []}, "doc_type": "nope"}, {200}),
    ("draft: state without 'case'", "/api/draft", {"state": {}, "doc_type": "deposit_demand_notice"}, {200, 400, 422}),
    ("fill: no blanks in body", "/api/draft/fill", {"body_markdown": "Hello", "answer": "my name is X"}, {200}),
    ("practice: empty case + history", "/api/practice", {"case": {}, "history": []}, {200}),
    ("practice: junk history items", "/api/practice", {"case": {"category": "tenancy"}, "history": ["x", 5, None]}, {200}),
    ("court case: bad CNR", "/api/court/case", {"cnr": "../../etc"}, {200}),
    ("court order: '..' filename", "/api/court/order", {"cnr": "DLCT010012342025", "file": ".."}, {200}),
    ("court order: path traversal", "/api/court/order", {"cnr": "DLCT010012342025", "file": "../../case/DLCT010012342025"}, {200}),
    ("court search: 1-letter name", "/api/court/search", {"name": "a"}, {200}),
]
for name, path, body, okcodes in cases:
    r = P(path, json=body)
    try:
        j = r.json()
    except Exception:
        j = {}
    ok(f"{name} -> handled ({r.status_code})", r.status_code in okcodes and r.status_code < 500, json.dumps(j)[:110])

r = P("/api/court/order", json={"cnr": "DLCT010012342025", "file": ".."}).json()
ok("court order: '..' rejected before any upstream call", r.get("error") == "bad_request", str(r))
r = P("/api/court/case", json={"cnr": "UKHA05001561202X"}, headers={"X-Forwarded-For": "198.51.100.9"}).json()
ok("court case: malformed CNR -> bad_cnr", r.get("error") == "bad_cnr", str(r))

# --- size limits
big = {"message": "hi", "state": {"messages": [{"role": "user", "content": "x" * 900_000}]}}
r = P("/api/chat", content=json.dumps(big), headers={"Content-Type": "application/json"})
ok("chat: 900 KB body refused (413)", r.status_code == 413, str(r.status_code))
r = P("/api/evidence", files={"file": ("big.jpg", io.BytesIO(b"\xff" * 10_500_000), "image/jpeg")})
ok("evidence: 10.5 MB upload refused (413)", r.status_code == 413, str(r.status_code))

# --- notice explainer input handling
r = P("/api/explain", data={"text": ""})
ok("explain: nothing provided -> 400", r.status_code == 400, r.text[:80])
r = P("/api/explain", data={"text": ""}, files={"file": ("x.exe", io.BytesIO(b"MZ" * 50), "application/octet-stream")})
ok("explain: .exe -> 415", r.status_code == 415, r.text[:80])
r = P("/api/explain", data={"text": ""}, files={"file": ("bad.pdf", io.BytesIO(b"%PDF-1.4 garbage"), "application/pdf")})
ok("explain: corrupt PDF -> 422 with a clear message (not 500)", r.status_code == 422, r.text[:100])

# --- docx with a Hindi title (used to 500 on latin-1 headers)
r = P("/api/docx", json={"title": "जमा राशि वापसी नोटिस", "body_markdown": "# नोटिस\nनमस्ते"})
ok("docx: Hindi title downloads (200, UTF-8 filename)", r.status_code == 200 and "filename*=UTF-8''" in r.headers.get("content-disposition", ""), r.headers.get("content-disposition", "")[:90])


# --- notice deadline parsing (used to OverflowError -> 500 on every turn)
sys.path.insert(0, sys.argv[2])
from datetime import date  # noqa: E402

from app import rules  # noqa: E402
out = rules.compute("notice", {"received_date": "2026-11-01", "notice_deadline_days": "15 days, by 20.03.2026"}, date(2026, 11, 6))
ok("notice '15 days, by 20.03.2026' -> deadline 16 Nov 2026", out["deadlines"] and out["deadlines"][0]["date"] == "2026-11-16", str(out["deadlines"][:1]))

# --- rate limits (server started with COURT_LIMIT_PER_HOUR=5)
# simulate production: the client spoofs the first hop, the proxy appends the real address last
codes = [P("/api/court/case", json={"cnr": "DLCT010012342025"}, headers={"X-Forwarded-For": f"10.0.0.{i}, 203.0.113.7"}).status_code for i in range(8)]
ok("court: per-client hourly limit holds with a spoofed first X-Forwarded-For hop", codes.count(429) >= 2 and codes[0] == 200, str(codes))
codes = [P("/api/court/case", json={"cnr": "DLCT010012342025"}, headers={"X-Forwarded-For": f"10.0.1.{i}, 203.0.113.{100 + i}"}).status_code for i in range(3)]
ok("court: a different real client still gets through", codes[0] == 200, str(codes))

print(f"\n{sum(1 for r in res if r[1])}/{len(res)} API checks passed")
