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

    ip = request.headers.get("x-forwarded-for", "").split(",")[0].strip() or (request.client.host if request.client else "?")
    try:
        res = accounts.signup(inp.email, inp.password, inp.first_name, ip)
    except Exception as e:  # noqa: BLE001
        return JSONResponse({"ok": False, "error": "server", "detail": str(e)[:160]}, status_code=500)
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
        return JSONResponse({"error": str(e)[:200]}, status_code=500)


@app.post("/api/evidence")
async def evidence_ep(
    file: UploadFile = File(...),
    category: str = Form(""),
    language: str = Form("English"),
    provider: str = Form(""),
):
    from datetime import date as _date

    from . import evidence

    raw = await file.read()
    return evidence.extract(category or None, language, file.filename or "", file.content_type, raw, _date.today().isoformat(), provider or None)


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
    return engine.turn(inp.state, msg, provider=inp.provider, lang_pref=inp.lang_pref)


@app.post("/api/draft")
def draft(inp: DraftIn):
    return documents.draft(inp.state, inp.doc_type, inp.doc_language, provider=inp.provider)


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


class JudgmentsIn(BaseModel):
    q: str


_COURT_HITS: dict[str, list[float]] = {}


def _court_ok(request: Request, limit: int = int(os.getenv("COURT_LIMIT_PER_HOUR", "40"))) -> bool:
    """eCourts lookups cost credits: cap them per client (IP) per hour."""
    import time

    ip = (request.headers.get("x-forwarded-for") or "").split(",")[0].strip() or (request.client.host if request.client else "?")
    now = time.time()
    hits = [t for t in _COURT_HITS.get(ip, []) if now - t < 3600]
    ok = len(hits) < limit
    if ok:
        hits.append(now)
    _COURT_HITS[ip] = hits
    return ok


@app.get("/api/court/status")
def court_status():
    from . import courts

    return courts.status()


@app.post("/api/court/case")
def court_case(inp: CourtCaseIn, request: Request):
    from . import courts

    if not _court_ok(request):
        return {"error": "too_many"}
    return courts.case(inp.cnr, fresh=inp.fresh)


@app.post("/api/court/search")
def court_search(inp: CourtSearchIn, request: Request):
    from . import courts

    if not _court_ok(request):
        return {"error": "too_many"}
    return courts.search(inp.name, inp.state)


@app.post("/api/court/order")
def court_order(inp: CourtOrderIn, request: Request):
    """Order text (eCourts) + a plain-language summary that restates only the order."""
    from . import courts

    if not _court_ok(request):
        return {"error": "too_many"}
    o = courts.order_text(inp.cnr, inp.file)
    if "error" in o:
        return o
    s = courts.explain_order(o["markdown"], inp.case, inp.language, inp.script, inp.provider)
    return {"markdown": o["markdown"], **s}


@app.post("/api/court/judgments")
def court_judgments(inp: JudgmentsIn):
    from . import courts

    return courts.judgments(inp.q)


class FillIn(BaseModel):
    body_markdown: str
    answer: str
    provider: str | None = None


@app.post("/api/draft/fill")
def draft_fill(inp: FillIn):
    return documents.fill(inp.body_markdown[:20000], inp.answer[:3000], provider=inp.provider)


@app.post("/api/docx")
def docx(inp: DocxIn):
    data = documents.to_docx(inp.title, inp.body_markdown)
    safe = "".join(c for c in inp.title if c.isalnum() or c in " -_")[:60] or "document"
    return Response(
        data,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={"Content-Disposition": f'attachment; filename="{safe}.docx"'},
    )


@app.post("/api/practice")
def practice_ep(inp: PracticeIn):
    if inp.feedback:
        return practice.practice_feedback(inp.case, inp.history, inp.provider)
    return practice.practice_turn(inp.case, inp.history, inp.provider)


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
        raw = await file.read()
        if (file.content_type or "").endswith("pdf") or (file.filename or "").lower().endswith(".pdf"):
            from pypdf import PdfReader

            reader = PdfReader(io.BytesIO(raw))
            text = (text + "\n" + "\n".join((p.extract_text() or "") for p in reader.pages[:6])).strip()
        else:
            img, mime = raw, file.content_type
    return practice.explain_notice(text or None, img, mime, language, script, provider or None)


@app.post("/api/transcribe")
async def stt(audio: UploadFile = File(...), language: str = Form("")):
    raw = await audio.read()
    try:
        return transcribe(raw, audio.filename or "audio.webm", language or None)
    except LLMError as e:
        return JSONResponse({"error": str(e)}, status_code=503)


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
