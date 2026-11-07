"""Practice hearing in the main chat (replaces the Practice tool).
/api/practice is answered by a Playwright route (no AI calls), so the flow and the exact requests can be checked.
Usage: python scripts/qa/prep_test.py http://127.0.0.1:8011 out_dir"""
import json
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

URL = sys.argv[1].rstrip("/"); OUT = Path(sys.argv[2]); OUT.mkdir(parents=True, exist_ok=True)
res, errs, calls, chat_calls = [], [], [], []


def ok(name, cond, detail=""):
    res.append(bool(cond)); print(("PASS " if cond else "FAIL ") + name + (f" | {detail}" if detail else ""))


CASE = """(offer) => {
  S = {version:1, messages:[
    {role:'user', content:'I moved out of my flat in Pune on 31 August 2026. Landlord Ramesh is keeping my 40000 deposit.'},
    {role:'assistant', content:'**My view:** You have good grounds.'}],
    case:{category:'tenancy', language:'English', script:'Latin', facts:{deposit_amount:40000, possession_handed_over_date:'2026-08-31', other_party_name:'Ramesh'},
          timeline:[], evidence_have:[], evidence_missing:[]}, flags:{level:'none', reasons:[]}, log:[]};
  VIEW.turns = [{reply:'**My view:** You have good grounds. Send a written demand.', actions:[{type:'practice'}], citations:[], guard:{}, prepOffer: offer,
    calculated:{deadlines:[{label:'Last date to sue', date:'2029-08-31', days_left:1029, status:'ok', basis:'LIM1963-ART55', user_deadline:true}], derived:[]},
    completeness:{pct:60, missing:[]}}];
  VIEW.prep = offer ? {offered:true} : undefined;
  Cases.touch(); renderAll();
}"""


def practice_route(route):
    body = json.loads(route.request.post_data or "{}")
    calls.append(body)
    if body.get("feedback"):
        out = {"scores": {"facts": 4, "proof": 2, "answers": 3, "relief": 5, "composure": 4}, "summary": "Clear facts; bring the bank proof.",
               "went_well": ["Gave the exact date"], "improve": ["Name your proof"], "better_lines": ["I paid Rs 40,000 by bank transfer on 1 Jan 2025."],
               "bring": ["Bank statement"], "model": {}}
    else:
        n = sum(1 for m in body.get("history", []) if m.get("role") == "user")
        out = {"reply": "This is a practice hearing. When did you hand over the keys?" if n == 0 else f"Judge question {n + 1}: the landlord says the walls were damaged. What is your answer?", "model": {}}
    route.fulfill(status=200, content_type="application/json", body=json.dumps(out))


def chat_route(route):
    chat_calls.append(json.loads(route.request.post_data or "{}"))
    route.fulfill(status=200, content_type="application/json", body=json.dumps({"error": "mocked: lawyer chat not called in this test"}))


with sync_playwright() as p:
    b = p.chromium.launch(channel="msedge", headless=True)
    ctx = b.new_context(viewport={"width": 1366, "height": 860})
    ctx.add_init_script("try{localStorage.setItem('haq_mode','\"guest\"')}catch(e){}")
    pg = ctx.new_page()
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.route("**/api/practice", practice_route)
    pg.route("**/api/chat", chat_route)
    pg.goto(URL + "/"); pg.wait_for_function("typeof CONFIG !== 'undefined' && CONFIG && CONFIG.doc_types", timeout=60_000)

    ok("Practice is no longer in the sidebar", pg.locator(".side-nav [data-tab=practice]").count() == 0 and pg.locator("#p-practice").count() == 0)

    # before any case: "practice" explains what to do, no AI call
    pg.fill("#input", "practice"); pg.press("#input", "Enter"); time.sleep(0.5)
    ok("'practice' before telling the problem -> asks for the problem first, no AI call",
       "problem" in pg.locator(".msg.bot").last.inner_text().lower() and not calls, pg.locator(".msg.bot").last.inner_text()[:80])

    # case with the offer
    pg.evaluate(CASE, True); time.sleep(0.3)
    ok("offer card shows under the case reply, with a button", pg.is_visible(".prep-offer") and pg.is_visible(".prep-offer button"), pg.inner_text(".prep-offer")[:90])
    ok("no duplicate 'practice' action button next to the offer", pg.locator(".msg.bot .actions button").count() == 0)

    # "prepare a notice" is a draft request, not a hearing
    pg.fill("#input", "prepare a notice"); pg.press("#input", "Enter"); time.sleep(0.6)
    ok("'prepare a notice' goes to the lawyer chat, not the hearing", len(chat_calls) == 1 and not calls)
    pg.evaluate(CASE, True); time.sleep(0.3)

    # a bare "yes" right after the offer starts the hearing
    pg.fill("#input", "yes"); pg.press("#input", "Enter")
    pg.wait_for_selector(".prep-meta", timeout=10_000)
    ok("'yes' right after the offer starts the hearing", len(calls) == 1 and calls[0]["history"] == [] and calls[0].get("language") == "English", json.dumps(calls[0])[:120])
    ok("judge's first question appears in the main chat with a 'Practice hearing' tag", "keys" in pg.locator(".msg.bot").last.inner_text() and pg.is_visible(".prep-chip"))
    ok("status bar above the composer with 'End & get feedback'", pg.is_visible("#prepBar") and pg.is_visible("#prepEnd") and "stop" in pg.inner_text("#prepHint"))
    ok("hearing request carries the case", calls[0]["case"]["category"] == "tenancy")

    # answers go to the judge with the right history
    pg.fill("#input", "On 31 August 2026, in front of the broker."); pg.press("#input", "Enter")
    pg.wait_for_function("document.querySelectorAll('.prep-meta').length >= 2", timeout=10_000)
    h = calls[-1]["history"]
    ok("my answer goes to the judge (not the lawyer chat) with the full hearing history",
       len(chat_calls) == 1 and [m["role"] for m in h] == ["judge", "user"] and "31 August" in h[1]["content"], json.dumps(h)[:160])
    ok("the trigger word 'yes' is not part of the hearing transcript", all(m["content"] != "yes" for m in h))
    pg.screenshot(path=OUT / "prep_hearing.png")

    # reload keeps the hearing going
    pg.reload(); pg.wait_for_selector(".prep-meta", timeout=30_000); time.sleep(0.5)
    ok("after a reload the hearing and its status bar are still there", pg.locator(".prep-meta").count() == 2 and pg.is_visible("#prepBar"))
    ok("the lawyer's answer and its deadlines survive the hearing", pg.evaluate("lastCaseTurn().calculated.deadlines.length") == 1)

    # stored flags: hearing messages marked practice:true, earlier legal ones not
    flags = pg.evaluate("S.messages.map(m => !!m.practice)")
    ok("hearing messages are stored as practice:true (kept out of the lawyer's context)", flags == [False, False, True, True, True, True], str(flags))

    # stop -> scorecard
    pg.fill("#input", "stop"); pg.press("#input", "Enter")
    pg.wait_for_selector(".prep-fb .score", timeout=10_000)
    fbreq = calls[-1]
    ok("'stop' asks for feedback on my answers only (no 'stop' in the transcript)", fbreq.get("feedback") and all(m["content"] != "stop" for m in fbreq["history"]), json.dumps(fbreq["history"])[:120])
    ok("scorecard shows 5 scores with labels, tips, better lines and what to bring",
       pg.locator(".prep-fb .score").count() == 5 and "Bank statement" in pg.inner_text(".prep-fb") and "Answering the question" in pg.inner_text(".prep-fb"), pg.inner_text(".prep-fb")[:120])
    ok("status bar disappears after the hearing ends", pg.is_hidden("#prepBar"))
    pg.screenshot(path=OUT / "prep_feedback.png", full_page=True)

    # after the hearing, normal messages go to the lawyer again
    n = len(chat_calls)
    pg.fill("#input", "Can I claim interest on the deposit?"); pg.press("#input", "Enter"); time.sleep(0.6)
    ok("after the hearing, questions go to the lawyer chat again", len(chat_calls) == n + 1)
    sent = chat_calls[-1]["state"]["messages"]
    ok("the lawyer-chat request still carries the hearing (server filters it out)", any(m.get("practice") for m in sent))

    # 'practice' again restarts; End button with no answers just closes it
    pg.fill("#input", "practice"); pg.press("#input", "Enter")
    pg.wait_for_function("document.querySelectorAll('.prep-meta').length >= 3", timeout=10_000)
    ok("'practice' starts a new hearing any time", pg.is_visible("#prepBar") and calls[-1]["history"] == [])
    k = len(calls); pg.click("#prepEnd"); time.sleep(0.5)
    ok("'End' before answering closes the hearing without an AI call", len(calls) == k and pg.is_hidden("#prepBar"))

    # Hindi interface: offer text + language sent
    pg.evaluate(CASE, True); time.sleep(0.2)
    pg.click("#settingsBtn"); pg.select_option("#lang", "hi"); pg.keyboard.press("Escape"); time.sleep(0.3)
    ok("offer is translated (Hindi interface)", "कोर्ट" in pg.inner_text(".prep-offer"), pg.inner_text(".prep-offer")[:60])
    pg.click(".prep-offer button"); pg.wait_for_selector(".prep-meta", timeout=10_000)
    ok("the button starts the hearing, in the interface language", calls[-1].get("language") == "Hindi")
    pg.click("#prepEnd"); time.sleep(0.3)
    pg.click("#settingsBtn"); pg.select_option("#lang", "en"); pg.keyboard.press("Escape")

    # switching case mid-hearing: the bar belongs to the case
    pg.fill("#input", "practice"); pg.press("#input", "Enter"); pg.wait_for_selector("#prepBar:not(.hidden)", timeout=10_000)
    pg.click("#newCase2"); time.sleep(0.4)
    ok("New case: no hearing bar in the fresh case", pg.is_hidden("#prepBar"))
    b.close()

print("JS errors:", errs or "none")
ok("no JS errors", not errs)
print(f"\n{sum(res)}/{len(res)} practice-hearing checks passed")
