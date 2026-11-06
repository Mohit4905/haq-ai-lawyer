"""Server-side account features that need the Supabase *service role* key (kept only on the server):
daily deadline reminder emails and full account deletion.

Env: SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY, BREVO_API_KEY, REMINDER_FROM_EMAIL, CRON_SECRET, PUBLIC_APP_URL
"""
from __future__ import annotations

import html
import os
from datetime import date, datetime, timedelta, timezone

import httpx

IST = timezone(timedelta(hours=5, minutes=30))
OFFSETS = (7, 1, 0)  # days before the deadline


def _sb():
    from .config import supabase_url

    url, key = supabase_url(), (os.getenv("SUPABASE_SERVICE_ROLE_KEY") or "").strip()
    if not url or not key:
        raise RuntimeError("Supabase service role not configured")
    h = {"apikey": key, "Content-Type": "application/json"}
    if not key.startswith("sb_"):  # legacy JWT keys also go in Authorization; new sb_secret_ keys only in apikey
        h["Authorization"] = f"Bearer {key}"
    return url.rstrip("/"), h


def _send_email(to: str, subject: str, html_body: str) -> None:
    key, sender = os.getenv("BREVO_API_KEY"), os.getenv("REMINDER_FROM_EMAIL")
    if not key or not sender:
        raise RuntimeError("Email not configured")
    r = httpx.post("https://api.brevo.com/v3/smtp/email", timeout=30,
                   headers={"api-key": key, "Content-Type": "application/json", "accept": "application/json"},
                   json={"sender": {"email": sender, "name": "Haq (हक़)"}, "to": [{"email": to}], "subject": subject, "htmlContent": html_body})
    if r.status_code >= 300:
        raise RuntimeError(f"Brevo {r.status_code}: {r.text[:200]}")


def _email_html(label: str, due: date, offset: int, case_title: str | None, basis: str | None) -> str:
    when = {7: "in 7 days", 1: "TOMORROW", 0: "TODAY"}[offset]
    when_hi = {7: "7 दिन में", 1: "कल", 0: "आज"}[offset]
    app = os.getenv("PUBLIC_APP_URL", "")
    return f"""<div style="font-family:Arial,sans-serif;max-width:560px">
<h2 style="color:#312e81">⚖️ Deadline {when}: {html.escape(label)}</h2>
<p><b>Date:</b> {due.strftime('%d %b %Y')} &nbsp;·&nbsp; <b>Case:</b> {html.escape(case_title or 'your case')}</p>
<p>समय-सीमा {when_hi}: {html.escape(label)}</p>
<p style="color:#555">Calculated by Haq from the dates you gave{(' (basis: ' + html.escape(basis) + ')') if basis else ''}. This is legal information, not legal advice. Please confirm with a lawyer or free legal aid: <b>NALSA 15100</b>.</p>
{f'<p><a href="{html.escape(app)}">Open your case in Haq</a></p>' if app else ''}
<p style="color:#999;font-size:12px">You get this because you turned on email reminders. Turn them off in Haq → Profile.</p></div>"""


def run_reminders(today: date | None = None) -> dict:
    url, h = _sb()
    today = today or datetime.now(IST).date()
    days = [(today + timedelta(days=o)).isoformat() for o in OFFSETS]
    r = httpx.get(f"{url}/rest/v1/reminders", headers=h, params={"due_date": f"in.({','.join(days)})", "select": "*"}, timeout=30)
    r.raise_for_status()
    sent, skipped, errors = 0, 0, []  # noqa: F841 (errors is filled below)
    emails: dict[str, str | None] = {}
    prefs: dict[str, bool] = {}
    for rem in r.json():
        uid = rem["user_id"]
        due = date.fromisoformat(rem["due_date"])
        off = (due - today).days
        if str(off) in (rem.get("sent") or {}):
            skipped += 1
            continue
        if uid not in prefs:
            try:  # one bad lookup must not abort the whole daily run (audit)
                pr = httpx.get(f"{url}/rest/v1/profiles", headers=h, params={"id": f"eq.{uid}", "select": "email_reminders"}, timeout=30).json()
                prefs[uid] = (pr[0].get("email_reminders") is not False) if isinstance(pr, list) and pr else True
            except Exception as e:  # noqa: BLE001
                errors.append(f"profile lookup: {str(e)[:120]}")
                prefs[uid] = True
        if not prefs[uid]:
            skipped += 1
            continue
        if uid not in emails:
            u = httpx.get(f"{url}/auth/v1/admin/users/{uid}", headers=h, timeout=30)
            emails[uid] = u.json().get("email") if u.status_code == 200 else None
        if not emails[uid]:
            skipped += 1
            continue
        try:
            subj = f"⚖️ Haq reminder: {rem['label'][:70]} ({'today' if off == 0 else 'tomorrow' if off == 1 else 'in 7 days'})"
            _send_email(emails[uid], subj, _email_html(rem["label"], due, off, rem.get("case_title"), rem.get("basis")))
            new_sent = {**(rem.get("sent") or {}), str(off): today.isoformat()}
            httpx.patch(f"{url}/rest/v1/reminders", headers=h, params={"id": f"eq.{rem['id']}"}, json={"sent": new_sent}, timeout=30)
            sent += 1
        except Exception as e:  # noqa: BLE001
            errors.append(str(e)[:200])
    return {"date": today.isoformat(), "sent": sent, "skipped": skipped, "errors": errors}


_SIGNUPS: dict[str, list[float]] = {}


def signup(email: str, password: str, first_name: str, client_ip: str) -> dict:
    """Create an email+password account (no confirmation email: Supabase's free sender only reaches team members).
    The browser then signs in with the same email/password. Basic validation + per-IP rate limit."""
    import re as _re
    import time as _time

    email = (email or "").strip().lower()
    first_name = (first_name or "").strip()[:60]
    if not _re.fullmatch(r"[^@\s]{1,64}@[^@\s]{1,190}\.[a-z]{2,}", email):
        return {"ok": False, "error": "bad_email"}
    if len(password or "") < 8:
        return {"ok": False, "error": "short_password"}
    if not first_name:
        return {"ok": False, "error": "no_name"}
    now = _time.time()
    hits = [t for t in _SIGNUPS.get(client_ip, []) if now - t < 600]
    if len(hits) >= 5:
        return {"ok": False, "error": "rate_limited"}
    _SIGNUPS[client_ip] = hits + [now]
    url, h = _sb()
    r = httpx.post(f"{url}/auth/v1/admin/users", headers=h, timeout=30,
                   json={"email": email, "password": password, "email_confirm": True, "user_metadata": {"first_name": first_name}})
    try:
        body = r.json() if r.content else {}
    except ValueError:
        body = {}
    code = str(body.get("error_code") or body.get("code") or "") if isinstance(body, dict) else ""
    if r.status_code >= 300:
        # not every 422 means "exists" (audit: a weak password was reported as an existing account)
        if code in ("email_exists", "user_already_exists") or "already" in r.text.lower():
            return {"ok": False, "error": "exists"}
        if code == "weak_password" or "password" in r.text.lower():
            return {"ok": False, "error": "short_password"}
        if code in ("email_address_invalid", "validation_failed"):
            return {"ok": False, "error": "bad_email"}
        print("[signup-upstream]", r.status_code, r.text[:200], flush=True)
        return {"ok": False, "error": "server"}
    uid = r.json()["id"]
    httpx.post(f"{url}/rest/v1/profiles", headers={**h, "Prefer": "resolution=merge-duplicates"}, timeout=30,
               json={"id": uid, "full_name": first_name})
    return {"ok": True}


def delete_account(user_jwt: str) -> dict:
    url, h = _sb()
    me = httpx.get(f"{url}/auth/v1/user", headers={"apikey": h["apikey"], "Authorization": f"Bearer {user_jwt}"}, timeout=30)
    if me.status_code != 200:
        return {"ok": False, "error": "not signed in"}
    uid = me.json()["id"]
    d = httpx.delete(f"{url}/auth/v1/admin/users/{uid}", headers=h, timeout=30)  # cascades to profiles/cases/reminders
    return {"ok": d.status_code < 300}
