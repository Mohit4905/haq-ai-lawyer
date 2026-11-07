"""Message action buttons, end to end in Edge (the chat API is faked in the browser: no AI calls).

    python scripts/qa/actions_test.py http://127.0.0.1:8000 out_dir

Checks every action on the exact message it belongs to: copy / edit / share on prompts; copy,
like / dislike, read aloud, share, try again, versions, more-menu report on replies; ids unique and
stable across edit, regenerate and reload; no buttons on typing / error bubbles; phone layout."""
import json
import sys
import time
import uuid
from pathlib import Path

from playwright.sync_api import sync_playwright

URL = sys.argv[1].rstrip("/"); OUT = Path(sys.argv[2]); OUT.mkdir(parents=True, exist_ok=True)
res, errs, chat_calls, feedback = [], [], [], []


def ok(n, c, d=""):
    res.append(bool(c)); print(("PASS " if c else "FAIL ") + n + (f" | {d}" if d else ""))


def fake_chat(route):
    body = json.loads(route.request.post_data or "{}")
    msg = body.get("message", "")
    chat_calls.append(msg)
    if msg == "FAIL":
        return route.fulfill(status=200, content_type="application/json", body=json.dumps({"error": "Model busy (test)"}))
    st = body.get("state") or {"version": 1, "messages": [], "case": {"category": None, "facts": {}, "timeline": [], "evidence_have": [], "evidence_missing": []}, "flags": {"level": "none", "reasons": []}, "log": []}
    n = len(chat_calls)
    reply = f"**My view:** Answer {n} to: {msg}\n- point one for {msg}\n- point two"
    uid, rid = uuid.uuid4().hex, uuid.uuid4().hex
    st["messages"] = st["messages"] + [{"role": "user", "content": msg, "id": uid}, {"role": "assistant", "content": reply, "id": rid, "reply_to": uid}]
    st["case"]["category"] = "tenancy"
    time.sleep(0.4)
    route.fulfill(status=200, content_type="application/json", body=json.dumps({
        "state": st, "reply": reply, "intent": "legal", "message_id": rid, "user_message_id": uid, "citations": [], "guard": {"final": {"ok": True, "verified": []}},
        "actions": [], "model": {"provider": "test", "model": "fake", "latency_s": 0.4}, "latency_s": 0.4,
        "calculated": {"deadlines": [], "derived": []}, "completeness": {"pct": 10, "missing": []}, "needs_lawyer": st["flags"], "emergency_contacts": []}))


INIT = """
try{localStorage.setItem('haq_mode','"guest"')}catch(e){}
window.__shared = []; window.__spoken = []; window.__cancels = 0;
navigator.share = async (d) => { window.__shared.push(d.text); };
Object.defineProperty(window, "speechSynthesis", { configurable: true, value: { speak(u){ window.__spoken.push(u.text); window.__lastU = u; }, cancel(){ window.__cancels++; }, getVoices(){ return []; } } });
Object.defineProperty(window, "SpeechSynthesisUtterance", { configurable: true, writable: true, value: function(t){ this.text = t; } });
"""

with sync_playwright() as p:
    b = p.chromium.launch(channel="msedge", headless=True)
    ctx = b.new_context(viewport={"width": 1366, "height": 900})
    ctx.grant_permissions(["clipboard-read", "clipboard-write"], origin=URL)
    ctx.add_init_script(INIT)
    pg = ctx.new_page(); pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.route("**/api/chat", fake_chat)
    pg.route("**/api/feedback", lambda r: (feedback.append(json.loads(r.request.post_data or "{}")), r.fulfill(status=200, content_type="application/json", body='{"ok":true}')))
    pg.goto(URL + "/"); pg.wait_for_function("typeof CONFIG !== 'undefined' && CONFIG && CONFIG.doc_types", timeout=60_000)
    clip = lambda: pg.evaluate("navigator.clipboard.readText()").replace("\r\n", "\n")  # Windows clipboard uses CRLF
    bots = lambda: pg.locator("#chat .msg.bot[data-mid]")
    users = lambda: pg.locator("#chat .msg.user[data-mid]")

    def send(t):
        k = bots().count()
        pg.fill("#input", t); pg.press("#input", "Enter")
        pg.wait_for_function(f"document.querySelectorAll('#chat .msg.bot[data-mid]').length > {k}", timeout=20_000)
        time.sleep(0.2)

    P = ["My landlord kept my deposit of 40000", "He says painting is needed", "Can I claim interest too?"]
    for t in P:
        send(t)
    ids = pg.evaluate("[...document.querySelectorAll('#chat .msg[data-mid]')].map(n => n.dataset.mid)")
    ok("3 prompts + 3 replies, each with its own id", len(ids) == 6 and len(set(ids)) == 6, str(len(ids)))
    ok("every message in state has a unique id; replies point to their prompt",
       pg.evaluate("S.messages.every(m => m.id) && new Set(S.messages.map(m => m.id)).size === S.messages.length && S.messages.filter(m => m.role==='assistant').every(m => S.messages.find(u => u.id === m.reply_to)?.role === 'user')"))
    ok("reply extras linked by id (no position matching)", pg.evaluate("S.messages.filter(m => m.role==='assistant').every(m => VIEW.turns.some(t => t.mid === m.id))"))
    ok("user bar: edit, share, copy", users().nth(0).locator(".msg-actions .act").count() == 3)
    ok("reply bar: copy, like, dislike, read, share, try again, more", bots().nth(0).locator(".msg-actions .act").count() == 7)
    pg.screenshot(path=OUT / "a1_bars.png")

    # copy
    users().nth(0).hover(); users().nth(0).locator(".act[aria-label='Copy']").click(); time.sleep(0.2)
    ok("copy prompt 1 -> exact prompt", clip() == P[0], clip())
    bots().nth(1).locator(".act[aria-label='Copy']").click(); time.sleep(0.2)
    c2 = clip()
    ok("copy reply 2 -> only reply 2, no markdown symbols", c2.startswith("My view\nAnswer 2 to: " + P[1]) and "**" not in c2 and P[0] not in c2, c2[:80])
    ok("'Copied!' shown", "Copied" in pg.inner_text("#toast"))

    # share (native, then fallback)
    users().nth(2).hover(); users().nth(2).locator(".act[aria-label='Share']").click(); time.sleep(0.2)
    bots().nth(0).locator(".act[aria-label='Share']").click(); time.sleep(0.2)
    sh = pg.evaluate("window.__shared")
    ok("share prompt 3 and reply 1 -> the right texts", sh[0] == P[2] and sh[1].startswith("My view\nAnswer 1 to: " + P[0]), str(sh)[:120])
    pg.evaluate("delete navigator.share; navigator.share = undefined")
    bots().nth(2).locator(".act[aria-label='Share']").click(); time.sleep(0.3)
    ok("no Web Share -> copied instead, with a message", clip().startswith("My view\nAnswer 3") and "copied" in pg.inner_text("#toast").lower())

    # like / dislike
    r1, r2 = bots().nth(0), bots().nth(1)
    r1.locator(".act[aria-label='Good response']").click(); time.sleep(0.2)
    ok("like reply 1 -> selected", bots().nth(0).locator(".act[aria-label='Good response']").get_attribute("aria-pressed") == "true")
    ok("reply 2 unaffected", bots().nth(1).locator(".act[aria-label='Good response']").get_attribute("aria-pressed") == "false")
    bots().nth(0).locator(".act[aria-label='Bad response']").click(); time.sleep(0.2)
    ok("change to dislike -> like cleared", bots().nth(0).locator(".act[aria-label='Bad response']").get_attribute("aria-pressed") == "true"
       and bots().nth(0).locator(".act[aria-label='Good response']").get_attribute("aria-pressed") == "false")
    bots().nth(0).locator(".act[aria-label='Bad response']").click(); time.sleep(0.2)
    ok("click dislike again -> cleared", bots().nth(0).locator(".act[aria-label='Bad response']").get_attribute("aria-pressed") == "false")
    rid1 = ids[1]
    ok("feedback sent with reply 1's id each time", [f.get("rating") for f in feedback] == ["up", "down", None] and all(f["message_id"] == rid1 for f in feedback), str(feedback)[:150])

    # read aloud
    bots().nth(2).locator(".act[aria-label='Read aloud']").click(); time.sleep(0.2)
    sp = pg.evaluate("window.__spoken.join(' ')")
    ok("read aloud reply 3 -> its text, no markdown or symbols", "Answer 3 to" in sp and "**" not in sp and "Answer 1" not in sp, sp[:90])
    ok("button turns into Stop", bots().nth(2).locator(".act[aria-label='Stop reading']").count() == 1)
    bots().nth(0).locator(".act[aria-label='Read aloud']").click(); time.sleep(0.2)
    ok("starting reply 1 stops reply 3", pg.evaluate("window.__cancels") >= 2 and "Answer 1 to" in pg.evaluate("window.__spoken.at(-1)")
       and bots().nth(2).locator(".act[aria-label='Read aloud']").count() == 1)
    bots().nth(0).locator(".act[aria-label='Stop reading']").click(); time.sleep(0.2)
    ok("stop -> playback cancelled, button back", bots().nth(0).locator(".act[aria-label='Read aloud']").count() == 1)

    # regenerate the MIDDLE reply only
    before = pg.evaluate("S.messages.map(m => [m.id, m.content])")
    calls0 = len(chat_calls)
    btn = bots().nth(1).locator(".act[aria-label='Try again']")
    btn.evaluate("b => { b.click(); b.click(); }")  # two clicks in the same instant must send once
    pg.wait_for_function("!document.querySelector('#chat .msg.bot .typing')", timeout=20_000); time.sleep(0.3)
    after = pg.evaluate("S.messages.map(m => [m.id, m.content])")
    ok("one request for a double-click", len(chat_calls) - calls0 == 1, str(len(chat_calls) - calls0))
    ok("try again on reply 2 -> sent its own prompt", chat_calls[-1] == P[1], chat_calls[-1])
    changed = [i for i, (a, c) in enumerate(zip(before, after)) if a != c]
    ok("only reply 2 changed; same ids; no duplicate prompt", changed == [3] and [a[0] for a in before] == [a[0] for a in after] and len(after) == 6, str(changed))
    ok("versions 2/2 shown", bots().nth(1).locator(".act-ver-n").inner_text() == "2/2")
    bots().nth(1).locator(".act[aria-label='Previous version']").click(); time.sleep(0.2)
    ok("previous version restores the old reply", "Answer 2 to" in bots().nth(1).inner_text() and bots().nth(1).locator(".act-ver-n").inner_text() == "1/2")
    bots().nth(1).locator(".act[aria-label='Next version']").click(); time.sleep(0.2)
    pg.screenshot(path=OUT / "a2_regen.png")

    # edit prompt 1: cancel, then save
    users().nth(0).hover(); users().nth(0).locator(".act[aria-label='Edit message']").click(); time.sleep(0.2)
    ok("edit opens with the original text", pg.input_value(".edit-box textarea") == P[0])
    pg.click(".edit-cancel"); time.sleep(0.2)
    ok("cancel -> prompt unchanged", users().nth(0).locator(".bubble").inner_text() == P[0] and pg.locator(".edit-box").count() == 0)
    users().nth(0).hover(); users().nth(0).locator(".act[aria-label='Edit message']").click(); time.sleep(0.2)
    pg.fill(".edit-box textarea", "My landlord kept my deposit of 50000"); pg.click(".edit-save")
    time.sleep(0.1)  # the fake reply takes 0.4 s: the editor must already be closed
    # (the editor closes synchronously in the click handler, before the request is even sent)
    st = [pg.locator(".edit-box").count(), users().nth(0).locator(".bubble").inner_text()]
    ok("send closes the editor at once and shows the edited text", st[0] == 0 and st[1] == "My landlord kept my deposit of 50000", str(st))
    pg.wait_for_function("!document.querySelector('#chat .msg.bot .typing') && !document.querySelector('.edit-box')", timeout=20_000); time.sleep(0.3)
    a2 = pg.evaluate("S.messages.map(m => [m.id, m.content])")
    ok("edited prompt sent", chat_calls[-1] == "My landlord kept my deposit of 50000")
    ok("prompt 1 + reply 1 updated in place; others untouched; same ids",
       a2[0][1] == "My landlord kept my deposit of 50000" and "50000" in a2[1][1] and a2[2:] == after[2:] and [x[0] for x in a2] == [x[0] for x in after])
    ok("edited exchange shows 2 versions", bots().nth(0).locator(".act-ver-n").inner_text() == "2/2")

    # Enter key saves too; a failed request puts the original text back
    users().nth(2).hover(); users().nth(2).locator(".act[aria-label='Edit message']").click(); time.sleep(0.2)
    pg.fill(".edit-box textarea", "FAIL"); pg.press(".edit-box textarea", "Enter"); time.sleep(0.1)
    ok("Enter closes the editor at once", pg.locator(".edit-box").count() == 0)
    pg.wait_for_function("!document.querySelector('#chat .msg.bot .typing')", timeout=20_000); time.sleep(0.3)
    ok("failed edit -> original prompt back, error shown", users().nth(2).locator(".bubble").inner_text() == P[2] and "Couldn't" in pg.inner_text("#toast"))

    # more menu
    bots().nth(2).locator(".act-more").click(); time.sleep(0.2)
    items = pg.locator(".act-menu button").all_inner_texts()
    ok("more menu opens with report options (no duplicates of the bar)", any("incorrect" in i for i in items) and not any(i.strip() in ("Copy", "Share", "Try again") for i in items), str(items))
    pg.locator(".act-menu button", has_text="incorrect").click(); time.sleep(0.2)
    ok("report sent for reply 3 with its text", feedback[-1].get("report") == "incorrect" and feedback[-1]["message_id"] == ids[5] and "Answer 3" in feedback[-1].get("reply", ""))
    ok("menu closes", pg.locator(".act-menu").count() == 0)

    # no buttons on error bubbles
    pg.fill("#input", "FAIL"); pg.press("#input", "Enter"); pg.wait_for_function("[...document.querySelectorAll('#chat .msg.bot')].at(-1).innerText.includes('busy')", timeout=10_000)
    ok("error reply and its unsent prompt have no buttons", pg.locator("#chat .msg").last.locator(".msg-actions").count() == 0
       and pg.locator("#chat .msg.user").last.locator(".msg-actions").count() == 0)

    # reload: ids, feedback, versions persist
    bots().nth(1).locator(".act[aria-label='Good response']").click(); time.sleep(0.3)
    pg.reload(); pg.wait_for_selector("#chat .msg.bot[data-mid]", timeout=20_000); time.sleep(0.4)
    ids2 = pg.evaluate("[...document.querySelectorAll('#chat .msg[data-mid]')].map(n => n.dataset.mid)")
    ok("after reload: same ids", ids2 == ids, f"{len(ids2)} vs {len(ids)}")
    ok("after reload: like and versions kept", bots().nth(1).locator(".act[aria-label='Good response']").get_attribute("aria-pressed") == "true"
       and bots().nth(1).locator(".act-ver-n").inner_text() == "2/2")

    ok("no JavaScript errors (desktop)", not errs, "; ".join(errs)[:300])

    # phone (touch device: no hover, so the prompt's buttons are always visible)
    m = b.new_context(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True)
    m.add_init_script(INIT)
    pg = m.new_page(); pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.route("**/api/chat", fake_chat)
    pg.goto(URL + "/"); pg.wait_for_function("typeof CONFIG !== 'undefined' && CONFIG && CONFIG.doc_types", timeout=60_000)
    send("My employer has not paid two months of salary")
    ok("phone: reply bar visible, no horizontal scroll", bots().nth(0).locator(".msg-actions").is_visible() and pg.evaluate("document.documentElement.scrollWidth <= innerWidth + 1"))
    ok("phone: prompt buttons visible without hover", pg.evaluate("getComputedStyle(document.querySelector('#chat .msg.user .msg-actions')).opacity") in ("1", 1))
    pg.screenshot(path=OUT / "a3_phone.png")
    ok("no JavaScript errors (phone)", not errs, "; ".join(errs)[:300])
    b.close()
print(f"\n{sum(res)}/{len(res)} action checks passed")
