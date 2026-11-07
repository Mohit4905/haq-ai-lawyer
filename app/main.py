"""FastAPI app: JSON API + static single-page UI."""
from __future__ import annotations

import io
import os

from fastapi import FastAPI, File, Form, Request, UploadFile
from fastapi.responses import FileResponse, JSONResponse, Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from . import config, documents, engine, kb, practice, rules
from .llm import LLMError, transcribe

app = FastAPI(title="Haq: AI legal help for everyday problems in India")
STATIC = config.ROOT / "static"


# ------------------------------------------------------------------ request guard (QA audit)
# Per-client hourly limits for everything that spends AI quota or paid eCourts credits, a global
# daily cap on eCourts, and body-size caps. Limits can be tuned with env vars.
_HITS: dict[str, list[float]] = {}
_LIMITS = {
    "/api/chat": ("chat", int(os.getenv("CHAT_LIMIT_PER_HOUR", "80"))),
    "/api/draft": ("ai", int(os.getenv("AI_LIMIT_PER_HOUR", "60"))), "/api/draft/fill": ("ai", int(os.getenv("AI_LIMIT_PER_HOUR", "60"))),
    "/api/explain": ("ai", int(os.getenv("AI_LIMIT_PER_HOUR", "60"))), "/api/evidence": ("ai", int(os.getenv("AI_LIMIT_PER_HOUR", "60"))),
    "/api/practice": ("ai", int(os.getenv("AI_LIMIT_PER_HOUR", "60"))), "/api/transcribe": ("ai", int(os.getenv("AI_LIMIT_PER_HOUR", "60"))),
    "/api/court/case": ("court", int(os.getenv("COURT_LIMIT_PER_HOUR", "40"))), "/api/court/search": ("court", int(os.getenv("COURT_LIMIT_PER_HOUR", "40"))),
    "/api/court/order": ("court", int(os.getenv("COURT_LIMIT_PER_HOUR", "40"))),
    "/api/signup": ("signup", 10), "/api/docx": ("docx", 120),
}
_PAID = ("/api/court/case", "/api/court/search", "/api/court/order")
_UPLOADS = ("/api/evidence", "/api/explain", "/api/transcribe")
MAX_UPLOAD = 10_000_000
MAX_JSON = 800_000


def client_ip(request: Request) -> str:
    """Render sits behind Cloudflare, which sets CF-Connecting-IP / True-Client-IP and overwrites
    any value the client sends. The FIRST X-Forwarded-For hop is client-controlled, so it's never used."""
    for h in ("cf-connecting-ip", "true-client-ip"):
        v = (request.headers.get(h) or "").strip()
        if v:
            return v
    hops = [x.strip() for x in (request.headers.get("x-forwarded-for") or "").split(",") if x.strip()]
    return hops[-1] if hops else (request.client.host if request.client else "?")


def _over(key: str, limit: int, window: float = 3600) -> bool:
    import time

    now = time.time()
    hits = [t for t in _HITS.get(key, []) if now - t < window]
    over = len(hits) >= limit
    if not over:
        hits.append(now)
    _HITS[key] = hits
    if len(_HITS) > 5000:  # forget idle clients so the table can't grow without bound
        for k in [k for k, v in _HITS.items() if not v or now - v[-1] > 86400]:
            _HITS.pop(k, None)
    return over


@app.middleware("http")
async def request_guard(request: Request, call_next):
    path = request.url.path
    if request.method == "POST" and path.startswith("/api/"):
        try:
            size = int(request.headers.get("content-length") or 0)
        except ValueError:
            size = 0
        if size > (MAX_UPLOAD if path in _UPLOADS else MAX_JSON):
            return JSONResponse({"error": "too_large"}, status_code=413)
        lim = _LIMITS.get(path)
        if lim and _over(f"{lim[0]}|{client_ip(request)}", lim[1]):
            return JSONResponse({"error": "too_many"}, status_code=429)
        if path in _PAID and _over("court-global-day", int(os.getenv("COURT_DAILY_CAP", "300")), window=86400):
            return JSONResponse({"error": "no_credits"}, status_code=429)
    return await call_next(request)


def _soft(res):
    """Don't show raw provider errors (model names, HTTP bodies) to users; log them instead."""
    import re as _re

    if isinstance(res, dict) and isinstance(res.get("error"), str):
        e = res["error"]
        if len(e) > 140 or _re.search(r"(?i)HTTP \d|groq|gemini|openrouter|openai|anthropic|rate.?limit|api key|traceback|quota", e):
            print("[upstream-error]", e[:600], flush=True)
            res["error"] = "The AI service is busy or unavailable right now. Please try again in a minute."
            res.pop("trace", None)
    return res


class ChatIn(BaseModel):
    state: dict | None = None
    message: str
    provider: str | None = None
    lang_pref: str | None = None


class DraftIn(BaseModel):
    state: dict
    doc_type: str
    doc_language: str = "English"
    provider: str | None = None


class PracticeIn(BaseModel):
    case: dict
    history: list = []
    provider: str | None = None
    feedback: bool = False
    language: str | None = None  # interface language the hearing runs in


class DocxIn(BaseModel):
    title: str
    body_markdown: str


@app.get("/api/health")
def health():
    return {"ok": True, "kb_entries": len(kb.load_kb()), **config.public_config()}


_GOOGLE = {"t": 0.0, "on": False}


def _google_enabled() -> bool:
    """Google sign-in shows as available once it is enabled in Supabase (read from the public
    auth settings, cached 5 minutes). SUPABASE_GOOGLE_LOGIN=1/0 forces it on/off."""
    import time

    import httpx

    forced = os.getenv("SUPABASE_GOOGLE_LOGIN")
    if forced in ("0", "1"):
        return forced == "1"
    url, anon = config.supabase_url(), (os.getenv("SUPABASE_ANON_KEY") or "").strip()
    if not url or not anon:
        return False
    if time.time() - _GOOGLE["t"] > 300:
        try:
            r = httpx.get(f"{url}/auth/v1/settings", headers={"apikey": anon}, timeout=2.5)
            _GOOGLE["on"] = bool(r.json().get("external", {}).get("google"))
        except Exception:
            pass
        _GOOGLE["t"] = time.time()
    return _GOOGLE["on"]


@app.get("/api/config")
def get_config():
    return {
        **config.public_config(),
        "categories": rules.CATEGORIES,
        "doc_types": {k: v["label"] for k, v in documents.DOCS.items()},
        "doc_types_by_category": engine.DOC_TYPES,
        "case_steps": {k: [{"id": i, "en": en, "hi": hi} for i, en, hi in v] for k, v in rules.CASE_STEPS.items()},
        "case_statuses": rules.CASE_STATUSES,
        # public values only (the anon key is designed to be public; access is enforced by row-level security)
        "supabase": {"url": config.supabase_url(), "anon_key": (os.getenv("SUPABASE_ANON_KEY") or "").strip() or None,
                     "google": _google_enabled()},
        "email_reminders": bool(os.getenv("BREVO_API_KEY") and os.getenv("SUPABASE_SERVICE_ROLE_KEY")),
    }


@app.post("/api/cron/reminders")
def cron_reminders(request: Request):
    """Called once a day by the GitHub Actions workflow (.github/workflows/reminders.yml)."""
    from . import accounts

    secret = os.getenv("CRON_SECRET")
    if not secret or request.headers.get("x-cron-secret") != secret:
        return JSONResponse({"error": "forbidden"}, status_code=403)
    try:
        return accounts.run_reminders()
    except Exception as e:  # noqa: BLE001
        return JSONResponse({"error": str(e)[:300]}, status_code=500)


class SignupIn(BaseModel):
    email: str
    password: str
    first_name: str


@app.post("/api/signup")
def signup_ep(inp: SignupIn, request: Request):
    from . import accounts

    ip = client_ip(request)
    try:
        res = accounts.signup(inp.email, inp.password, inp.first_name, ip)
    except Exception as e:  # noqa: BLE001
        print("[signup-error]", str(e)[:300], flush=True)
        return JSONResponse({"ok": False, "error": "server"}, status_code=500)
    return JSONResponse(res, status_code=200 if res.get("ok") else 400)


@app.post("/api/account/delete")
def account_delete(request: Request):
    from . import accounts

    auth = request.headers.get("authorization", "")
    if not auth.lower().startswith("bearer "):
        return JSONResponse({"error": "not signed in"}, status_code=401)
    try:
        return accounts.delete_account(auth.split(" ", 1)[1])
    except Exception as e:  # noqa: BLE001
        print("[delete-error]", str(e)[:300], flush=True)
        return JSONResponse({"ok": False, "error": "server"}, status_code=500)


@app.post("/api/evidence")
async def evidence_ep(
    file: UploadFile = File(...),
    category: str = Form(""),
    language: str = Form("English"),
    provider: str = Form(""),
):
    from datetime import date as _date

    from . import evidence

    raw = await file.read(MAX_UPLOAD + 1)  # chunked uploads have no Content-Length, so cap the read too
    if len(raw) > MAX_UPLOAD:
        return JSONResponse({"error": "too_large"}, status_code=413)
    try:
        return _soft(evidence.extract(category or None, language, file.filename or "", file.content_type, raw, _date.today().isoformat(), provider or None))
    except Exception as e:  # noqa: BLE001
        print("[evidence-error]", str(e)[:300], flush=True)
        return JSONResponse({"error": "Couldn't read this file. Try a clearer photo or a PDF."}, status_code=422)


@app.get("/api/kb")
def get_kb():
    return [kb.public_entry(e) | {"categories": e.get("categories"), "notes": e.get("notes")} for e in kb.load_kb()]


@app.post("/api/chat")
def chat(inp: ChatIn):
    msg = (inp.message or "").strip()
    if not msg:
        return JSONResponse({"error": "Empty message"}, status_code=400)
    if len(msg) > 6000:
        msg = msg[:6000]
    return _soft(engine.turn(inp.state, msg, provider=inp.provider, lang_pref=inp.lang_pref))


@app.post("/api/draft")
def draft(inp: DraftIn):
    return _soft(documents.draft(inp.state, inp.doc_type, inp.doc_language, provider=inp.provider))


class CourtCaseIn(BaseModel):
    cnr: str
    fresh: bool = False


class CourtSearchIn(BaseModel):
    name: str
    state: str | None = None


class CourtOrderIn(BaseModel):
    cnr: str
    file: str
    case: dict = {}
    language: str = "English"
    script: str = "Latin"
    provider: str | None = None


@app.get("/api/court/status")
def court_status():
    from . import courts

    return courts.status()


@app.post("/api/court/case")
def court_case(inp: CourtCaseIn):
    from . import courts

    return courts.case(inp.cnr, fresh=inp.fresh)


@app.post("/api/court/search")
def court_search(inp: CourtSearchIn):
    from . import courts

    return courts.search(inp.name, inp.state)


@app.post("/api/court/order")
def court_order(inp: CourtOrderIn):
    """Order text (eCourts) + a plain-language summary that restates only the order."""
    from . import courts

    o = courts.order_text(inp.cnr, inp.file)
    if "error" in o:
        return o
    s = _soft(courts.explain_order(o["markdown"], inp.case, inp.language, inp.script, inp.provider))
    return {"markdown": o["markdown"], **s}


class FillIn(BaseModel):
    body_markdown: str
    answer: str
    provider: str | None = None


@app.post("/api/draft/fill")
def draft_fill(inp: FillIn):
    return _soft(documents.fill(inp.body_markdown[:20000], inp.answer[:3000], provider=inp.provider))


@app.post("/api/docx")
def docx(inp: DocxIn):
    from urllib.parse import quote

    data = documents.to_docx(inp.title, inp.body_markdown)
    name = "".join(c for c in inp.title if c.isalnum() or c in " -_")[:60].strip() or "document"
    ascii_name = "".join(c for c in name if c.isascii()).strip() or "document"
    # headers must be latin-1: ASCII fallback + RFC 5987 UTF-8 name (a Hindi title used to 500, audit)
    return Response(
        data,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={"Content-Disposition": f"attachment; filename=\"{ascii_name}.docx\"; filename*=UTF-8''{quote(name + '.docx')}"},
    )


@app.post("/api/practice")
def practice_ep(inp: PracticeIn):
    history = [m for m in (inp.history or []) if isinstance(m, dict)][-40:]
    lang = (inp.language or "")[:40] or None
    if inp.feedback:
        return _soft(practice.practice_feedback(inp.case or {}, history, inp.provider, lang))
    return _soft(practice.practice_turn(inp.case or {}, history, inp.provider, lang))


@app.post("/api/explain")
async def explain(
    text: str = Form(""),
    language: str = Form("English"),
    script: str = Form("Latin"),
    provider: str = Form(""),
    file: UploadFile | None = File(None),
):
    img, mime = None, None
    if file is not None:
        raw = await file.read(MAX_UPLOAD + 1)
        if len(raw) > MAX_UPLOAD:
            return JSONResponse({"error": "too_large"}, status_code=413)
        if (file.content_type or "").endswith("pdf") or (file.filename or "").lower().endswith(".pdf"):
            try:
                from pypdf import PdfReader

                reader = PdfReader(io.BytesIO(raw))
                text = (text + "\n" + "\n".join((p.extract_text() or "") for p in reader.pages[:6])).strip()
            except Exception:  # noqa: BLE001  (corrupt/encrypted PDF used to 500, audit)
                return JSONResponse({"error": "Couldn't read this PDF. Try a photo of the notice, or paste its text."}, status_code=422)
        elif (file.content_type or "").startswith("image/"):
            img, mime = raw, file.content_type
        else:
            return JSONResponse({"error": "Please upload a photo or a PDF of the notice."}, status_code=415)
    if not (text or "").strip() and img is None:
        return JSONResponse({"error": "Paste the notice text or upload a photo/PDF of it."}, status_code=400)
    return _soft(practice.explain_notice(text or None, img, mime, language, script, provider or None))


@app.post("/api/transcribe")
async def stt(audio: UploadFile = File(...), language: str = Form("")):
    raw = await audio.read(MAX_UPLOAD + 1)
    if len(raw) > MAX_UPLOAD:
        return JSONResponse({"error": "too_large"}, status_code=413)
    try:
        return transcribe(raw, audio.filename or "audio.webm", language or None)
    except LLMError as e:
        return JSONResponse(_soft({"error": str(e)}), status_code=503)


app.mount("/static", StaticFiles(directory=STATIC), name="static")


@app.get("/")
def index():
    return FileResponse(STATIC / "index.html")


@app.get("/login")
def login_page():
    return FileResponse(STATIC / "login.html")


@app.get("/privacy")
def privacy_page():
    return FileResponse(STATIC / "privacy.html")


@app.get("/terms")
def terms_page():
    return FileResponse(STATIC / "terms.html")
