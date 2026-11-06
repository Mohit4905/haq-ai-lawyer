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
                     "google": os.getenv("SUPABASE_GOOGLE_LOGIN") == "1"},
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
