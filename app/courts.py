"""Live court data: case status / hearings / orders (eCourtsIndia API) and related judgments
(kanoon.dev pilot).

eCourtsIndia (https://ecourtsindia.com/api/docs) is a paid, credit-based API (free credits on
signup; free for personal/academic use per its pricing FAQ). Set ECOURTS_API_KEY to enable it.
Responses are cached in memory to save credits. kanoon.dev is a free pilot with a small
historical sample of judgments; it needs no key.

Nothing here is legal advice: the court's own record is shown as returned, and AI summaries of
an order only restate what the order says.
"""
from __future__ import annotations

import os
import re
import time

import httpx

from . import prompts
from .llm import LLMError, chat

CNR_RE = re.compile(r"^[A-Z]{4}\d{12}$")
_CACHE: dict[str, tuple[float, dict]] = {}
CASE_TTL = 6 * 3600       # case status: refresh at most every 6 hours
ORDER_TTL = 7 * 24 * 3600  # an order's text doesn't change


def ecourts_base() -> str:
    return (os.getenv("ECOURTS_BASE") or "https://webapi.ecourtsindia.com").rstrip("/")


def ecourts_key() -> str:
    return (os.getenv("ECOURTS_API_KEY") or "").strip()


def kanoon_base() -> str:
    return (os.getenv("KANOON_BASE") or "https://api.kanoon.dev").rstrip("/")


def status() -> dict:
    return {"ecourts": bool(ecourts_key()), "kanoon": True}


def normalise_cnr(s: str) -> str:
    return re.sub(r"[\s\-/]", "", str(s or "")).upper()


def find_cnr(text: str) -> str | None:
    """A CNR typed or pasted into the chat (16 chars: 4 letters + 12 digits)."""
    m = re.search(r"\b([A-Za-z]{4})[\s\-]?(\d{2})[\s\-]?(\d{6})[\s\-]?(\d{4})\b", text or "")
    return normalise_cnr("".join(m.groups())) if m else None


# ------------------------------------------------------------------ eCourtsIndia
_ERRORS = {
    400: "bad_request", 401: "bad_key", 402: "no_credits", 403: "bad_key", 404: "not_found", 429: "rate_limited",
}


def _ecourts_get(path: str, params: dict | None = None, timeout: float = 30) -> dict:
    key = ecourts_key()
    if not key:
        return {"error": "not_configured"}
    try:
        r = httpx.get(ecourts_base() + path, params=params, timeout=timeout,
                      headers={"Authorization": f"Bearer {key}", "Accept": "application/json"})
    except httpx.TimeoutException:
        return {"error": "timeout"}
    except httpx.HTTPError:
        return {"error": "unreachable"}
    try:
        body = r.json()
    except ValueError:
        body = {}
    if r.status_code >= 400:
        code = (body.get("error") or {}).get("code") if isinstance(body.get("error"), dict) else None
        return {"error": _ERRORS.get(r.status_code, "server_error"), "code": code, "http": r.status_code}
    return body.get("data") if isinstance(body.get("data"), dict) else body


def _names(xs) -> list[str]:
    out = []
    for x in xs or []:
        if isinstance(x, str):
            s = x
        elif isinstance(x, dict):
            s = x.get("name") or x.get("advocateName") or x.get("judgeName") or " ".join(str(v) for v in x.values() if isinstance(v, str))
        else:
            s = str(x)
        s = re.sub(r"\s+", " ", s).strip(" ,;")
        if s:
            out.append(s)
    return out


def _title(pet: list[str], res: list[str]) -> str:
    a = pet[0] if pet else "Petitioner"
    b = res[0] if res else "Respondent"
    if len(pet) > 1:
        a += " & others"
    if len(res) > 1:
        b += " & others"
    return f"{a} vs {b}"


def parse_case(data: dict) -> dict:
    c = data.get("courtCaseData") or data
    pet, res = _names(c.get("petitioners")), _names(c.get("respondents"))
    hearings = []
    for h in c.get("historyOfCaseHearings") or []:
        if isinstance(h, dict):
            hearings.append({"date": h.get("hearingDate") or h.get("businessOnDate"), "purpose": h.get("purposeOfListing"), "judge": h.get("judge")})
    orders = []
    for o in c.get("judgmentOrders") or []:
        if isinstance(o, dict) and o.get("orderUrl"):
            orders.append({"date": o.get("orderDate"), "kind": "judgment", "label": o.get("orderType") or "Judgment", "file": str(o["orderUrl"]).split("/")[-1]})
    for o in c.get("interimOrders") or []:
        if isinstance(o, dict) and o.get("orderUrl"):
            orders.append({"date": o.get("orderDate"), "kind": "order", "label": o.get("description") or "Order", "file": str(o["orderUrl"]).split("/")[-1]})
    orders.sort(key=lambda o: str(o.get("date") or ""), reverse=True)
    nxt = c.get("nextHearingDate") or (data.get("entityInfo") or {}).get("nextDateOfHearing")
    court = ", ".join(x for x in [c.get("courtName"), c.get("district"), c.get("state")] if x)
    return {
        "cnr": c.get("cnr"),
        "title": _title(pet, res),
        "status": c.get("caseStatus"),
        "disposal": c.get("disposalType") or c.get("disposalTypeRaw"),
        "decision_date": c.get("decisionDate"),
        "next_hearing": nxt,
        "last_hearing": c.get("lastHearingDate"),
        "purpose": c.get("purpose"),
        "court": court,
        "court_no": c.get("courtNo"),
        "case_type": c.get("caseTypeRaw") or c.get("caseType"),
        "case_number": c.get("caseNumber"),
        "filing": {"number": c.get("filingNumber"), "date": c.get("filingDate")},
        "registration": {"number": c.get("registrationNumber"), "date": c.get("registrationDate")},
        "petitioners": pet, "respondents": res,
        "petitioner_advocates": _names(c.get("petitionerAdvocates")), "respondent_advocates": _names(c.get("respondentAdvocates")),
        "judges": _names(c.get("judges")),
        "acts": c.get("actsAndSections"),
        "hearings": sorted(hearings, key=lambda h: str(h.get("date") or ""), reverse=True)[:20],
        "orders": orders[:30],
        "source": "eCourtsIndia (data from the eCourts system)",
    }


def case(cnr: str, fresh: bool = False) -> dict:
    cnr = normalise_cnr(cnr)
    if not CNR_RE.match(cnr):
        return {"error": "bad_cnr"}
    hit = _CACHE.get("case:" + cnr)
    if hit and not fresh and time.time() - hit[0] < CASE_TTL:
        return hit[1] | {"cached": True}
    data = _ecourts_get(f"/api/partner/case/{cnr}")
    if "error" in data:
        return data
    out = parse_case(data) | {"fetched_at": time.strftime("%Y-%m-%d %H:%M")}
    _CACHE["case:" + cnr] = (time.time(), out)
    return out


def search(name: str, state: str | None = None, page_size: int = 10) -> dict:
    name = re.sub(r"\s+", " ", name or "").strip()
    if len(name) < 3:
        return {"error": "bad_request"}
    params: dict = {"litigants": name, "pageSize": max(1, min(page_size, 20)), "sortBy": "filingDate desc"}
    if state:
        params["stateCodes"] = state
    data = _ecourts_get("/api/partner/v2/search", params)
    if "error" in data:
        return data
    rows = []
    for r in data.get("results") or []:
        pet, res = _names(r.get("petitioners")), _names(r.get("respondents"))
        rows.append({"cnr": r.get("cnr"), "title": _title(pet, res), "status": r.get("caseStatus"), "court": r.get("courtCode"),
                     "type": r.get("caseType"), "filing_date": r.get("filingDate"), "next_hearing": r.get("nextHearingDate"),
                     "decision_date": r.get("decisionDate")})
    return {"results": rows, "total": data.get("totalHits", len(rows))}


def order_text(cnr: str, filename: str) -> dict:
    cnr = normalise_cnr(cnr)
    filename = (filename or "").split("/")[-1]
    if not CNR_RE.match(cnr) or not re.match(r"^[\w.\-]{1,120}$", filename):
        return {"error": "bad_request"}
    key = f"order:{cnr}:{filename}"
    hit = _CACHE.get(key)
    if hit and time.time() - hit[0] < ORDER_TTL:
        return hit[1]
    data = _ecourts_get(f"/api/partner/case/{cnr}/order-md/{filename}", timeout=120)
    if "error" in data:
        return data
    md = data.get("markdownContent") or ""
    if not md.strip():
        return {"error": "no_text"}
    out = {"markdown": md}
    _CACHE[key] = (time.time(), out)
    return out


def explain_order(order_md: str, case_info: dict, language: str = "English", script: str = "Latin", provider: str | None = None) -> dict:
    """Plain-language summary of a court order, restating only what the order says."""
    text = order_md.strip()
    if len(text) > 18000:  # long judgments: the start (parties, issues) and the end (operative order)
        text = text[:9000] + "\n\n[... middle of the order omitted ...]\n\n" + text[-9000:]
    sys = prompts.ORDER_EXPLAIN.format(language=language, script=script, title=case_info.get("title") or "", court=case_info.get("court") or "")
    try:
        res = chat([{"role": "system", "content": sys}, {"role": "user", "content": text}], tier="main", temperature=0.1, max_tokens=1200, provider=provider)
    except LLMError as e:
        return {"error": str(e)}
    return {"summary": res.text.strip(), "model": res.meta()}


# ------------------------------------------------------------------ kanoon.dev (pilot)
def _first(d: dict, *keys):
    for k in keys:
        v = d.get(k)
        if v not in (None, "", []):
            return v
    return None


def judgments(q: str, limit: int = 5) -> dict:
    """Related judgments from the kanoon.dev pilot (small historical sample, free, no key).
    Field names are read defensively because the pilot's schema is not fully documented."""
    q = re.sub(r"\s+", " ", q or "").strip()[:500]
    if len(q) < 3:
        return {"error": "bad_request"}
    try:
        r = httpx.get(kanoon_base() + "/v1/search", params={"q": q, "limit": max(1, min(limit, 10))}, timeout=20,
                      headers={"User-Agent": "Haq legal-help (student project)", "Accept": "application/json"})
    except httpx.HTTPError:
        return {"error": "unreachable"}
    if r.status_code == 429:
        return {"error": "rate_limited"}
    if r.status_code >= 500:
        return {"error": "unavailable"}
    if r.status_code >= 400:
        return {"error": "bad_request"}
    try:
        body = r.json()
    except ValueError:
        return {"error": "unavailable"}
    items = _first(body, "results", "items", "data", "documents") if isinstance(body, dict) else body
    if isinstance(items, dict):
        items = _first(items, "results", "items", "documents") or []
    rows = []
    for it in items or []:
        if not isinstance(it, dict):
            continue
        doc = it.get("document") if isinstance(it.get("document"), dict) else {}
        merged = {**doc, **it}
        snippet = _first(merged, "snippet", "headline", "excerpt", "text", "matching_text", "highlight")
        if isinstance(snippet, list):
            snippet = " … ".join(str(s) for s in snippet[:2])
        rows.append({
            "title": _first(merged, "title", "case_title", "name") or "Untitled document",
            "court": _first(merged, "court_name", "court", "court_code"),
            "date": _first(merged, "date", "decision_date", "judgment_date", "decided_on"),
            "snippet": re.sub(r"<[^>]+>", "", str(snippet or ""))[:400],
            "url": _first(merged, "source_url", "matching_page_url", "document_url", "url"),
        })
    return {"results": rows, "source": "kanoon.dev pilot (small historical sample; not a complete database)"}
