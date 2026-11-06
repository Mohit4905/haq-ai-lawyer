"""Draft shows in chat + Documents; questions asked in chat; chat reply fills blanks; survives reload; other questions go to normal chat."""
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

URL = sys.argv[1].rstrip("/"); OUT = Path(sys.argv[2]); OUT.mkdir(parents=True, exist_ok=True)
errs, res = [], []


def ok(n, c, d=""):
    res.append(bool(c)); print(("PASS " if c else "FAIL ") + n + (f" | {d}" if d else ""))


STATE = """() => {
  S = {version:1, messages:[
    {role:'user', content:'I moved out of my rented flat in Bengaluru on 31 August 2026. I paid a deposit of Rs 60,000 by bank transfer, rent was 20,000. Landlord Ramesh Gowda is keeping 25,000 for painting without bills.'},
    {role:'assistant', content:'**My view:** ...'}],
    case:{category:'tenancy', language:'English', script:'Latin', facts:{deposit_amount:60000, monthly_rent:20000, possession_handed_over_date:'2026-08-31', deductions_claimed:25000, other_party_name:'Ramesh Gowda', city_state:'Bengaluru'}, timeline:[], evidence_have:[], evidence_missing:[], next_step:null},
    flags:{level:'none', reasons:[]}, log:[]};
  VIEW.turns = [{reply:'**My view:** ...', actions:[{type:'draft', doc:'deposit_demand_notice'}], citations:[], guard:{}}];
  Cases.touch(); renderAll();
}"""

with sync_playwright() as p:
    b = p.chromium.launch(channel="msedge", headless=True)
    ctx = b.new_context(viewport={"width": 1366, "height": 900})
    ctx.add_init_script("try{localStorage.setItem('haq_mode','\"guest\"')}catch(e){}")
    pg = ctx.new_page(); pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto(URL + "/"); pg.wait_for_selector(".card[data-prompt]"); pg.wait_for_function("typeof CONFIG !== 'undefined' && CONFIG && CONFIG.doc_types", timeout=30_000)
    pg.evaluate(STATE); time.sleep(0.5)
    if not pg.locator(".msg.bot .actions button").count():
        pg.evaluate(STATE); time.sleep(0.5)  # an async startup render can replace the injected state once
    btn = pg.locator(".msg.bot .actions button").first
    print("draft button visible:", btn.is_visible())
    btn.click()
    pg.wait_for_selector(".msg.bot .doc-card", timeout=180_000); time.sleep(0.5)
    card_txt = pg.inner_text(".msg.bot >> nth=-1")
    n0 = pg.evaluate("docBlanks(VIEW.turns[VIEW.turns.length-1].doc.body).length")
    ok("draft appears as a card in the main chat", pg.locator(".msg.bot .doc-card").count() == 1)
    nq = pg.locator(".msg.bot >> nth=-1 >> .doc-ask li").count()
    below = pg.evaluate("(() => { const m=[...document.querySelectorAll('.msg.bot')].pop(); const c=m.querySelector('.doc-card'), a=m.querySelector('.doc-ask'); return !!(c && a && (c.compareDocumentPosition(a) & Node.DOCUMENT_POSITION_FOLLOWING)); })()")
    ok("questions for every missing detail asked in the chat, below the document", n0 == 0 or (nq == n0 and below), f"{n0} blanks, {nq} questions")
    ok("same draft mirrored in Documents panel", "Ramesh" in pg.input_value("#docText") or "60,000" in pg.input_value("#docText"))
    ok("Documents panel was not forced open", not pg.is_visible("#p-docs"))
    pg.screenshot(path=OUT / "d1_draft_in_chat.png", full_page=False)
    print("QUESTIONS:", pg.locator(".msg.bot >> nth=-1 >> .doc-ask li").all_inner_texts())
    pg.fill("#input", "My name is Priya Sharma. My address is Flat 3B, 12 MG Road, Pune 411001. Landlord's address is 45 Brigade Road, Bengaluru 560025. I paid the deposit on 1 September 2025.")
    pg.click("#send")
    pg.wait_for_function("VIEW.turns.length >= 3 && VIEW.turns[VIEW.turns.length-1].doc && document.querySelectorAll('.msg.bot .doc-card').length >= 2", timeout=120_000)
    time.sleep(0.5)
    body = pg.evaluate("VIEW.turns[VIEW.turns.length-1].doc.body")
    n1 = pg.evaluate("docBlanks(VIEW.turns[VIEW.turns.length-1].doc.body).length")
    ok("chat reply filled the blanks", "Priya Sharma" in body and "Brigade Road" in body and n1 < n0, f"{n0} -> {n1} blanks")
    ok("Documents panel shows the updated draft", "Priya Sharma" in pg.input_value("#docText"))
    ok("no invented values (only what the user typed)", "Priya Sharma" in body)
    pg.screenshot(path=OUT / "d2_filled.png")
    pg.reload(); pg.wait_for_selector(".msg.bot .doc-card", timeout=30_000)
    ok("draft cards survive reload", pg.locator(".msg.bot .doc-card").count() >= 2 and "Priya Sharma" in pg.input_value("#docText"))
    pg.click(".msg.bot >> nth=-1 >> .doc-more"); time.sleep(0.2)
    ok("'Show full document' expands the card", not pg.evaluate("document.querySelectorAll('.doc-paper')[document.querySelectorAll('.doc-paper').length-1].classList.contains('clipped')"))
    nmsg = pg.locator(".msg.bot").count()
    pg.fill("#input", "What should I do if he does not reply to the notice?")
    pg.click("#send")
    pg.wait_for_function(f"document.querySelectorAll('.msg.bot').length > {nmsg} && !document.querySelector('.msg.bot .typing')", timeout=180_000)
    time.sleep(0.5)
    last = pg.evaluate("VIEW.turns[VIEW.turns.length-1]")
    ok("an unrelated question goes to normal chat (not the filler)", not last.get("doc") and bool(last.get("reply")), (last.get("reply") or "")[:90])
    pg.screenshot(path=OUT / "d3_followup.png")
    ok("no JavaScript errors", not errs, "; ".join(errs)[:300])
    b.close()
print(f"\n{sum(res)}/{len(res)} passed")
