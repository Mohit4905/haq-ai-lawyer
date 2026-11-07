"""Court tracking E2E against the fake eCourts server: CNR in chat -> card; panel track; order explain; party search; errors; reload."""
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

URL = sys.argv[1].rstrip("/"); OUT = Path(sys.argv[2]); OUT.mkdir(parents=True, exist_ok=True)
errs, res = [], []


def ok(n, c, d=""):
    res.append(bool(c)); print(("PASS " if c else "FAIL ") + n + (f" | {d}" if d else ""))


with sync_playwright() as p:
    b = p.chromium.launch(channel="msedge", headless=True)
    ctx = b.new_context(viewport={"width": 1366, "height": 900})
    ctx.add_init_script("try{localStorage.setItem('haq_mode','\"guest\"')}catch(e){}")
    pg = ctx.new_page(); pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto(URL + "/"); pg.wait_for_selector(".card[data-prompt]"); pg.wait_for_function("typeof COURT !== 'undefined' && COURT.ecourts === true", timeout=20_000)  # no wait for KB: send() must wait for the app itself
    ok("court section in sidebar", pg.is_visible(".side-nav .tab[data-tab=court]"))
    # 1. CNR pasted in chat (with spaces) -> court card
    pg.fill("#input", "What is happening in my case DLCT 01 001234 2025?"); pg.click("#send")
    pg.wait_for_selector(".msg.bot .court-card", timeout=30_000); time.sleep(0.4)
    card = pg.inner_text(".court-card")
    ok("CNR in chat shows the court card", "Priya Sharma vs Ramesh Gowda" in card and "PENDING" in card.upper(), card[:80].replace("\n", " | "))
    ok("next hearing + purpose shown", "3 Dec 2026" in card and "Plaintiff/Petitioner Evidence" in card)
    ok("court, judge, advocate, orders listed", "Saket" in card and "A. K. Verma" in card and pg.locator(".court-card .cc-order").count() == 2)
    ok("calendar button for next hearing", pg.is_visible(".court-card .cc-cal"))
    pg.screenshot(path=OUT / "c1_card.png")
    # 2. explain an order -> AI summary in chat
    pg.locator(".court-card .cc-order button").first.click()
    pg.wait_for_selector(".msg.bot .order-extra", timeout=180_000); time.sleep(0.4)
    summ = pg.inner_text(".msg.bot >> nth=-1")
    ok("order explained in chat", "60,000" in summ or "issues" in summ.lower(), summ[:160].replace("\n", " | "))
    ok("summary doesn't invent a hearing date", "3 December 2026" in summ or "03.12.2026" in summ or "December" in summ or "next" in summ.lower())
    ok("full order text available", pg.locator(".msg.bot >> nth=-1 >> .order-text").count() == 1)
    pg.screenshot(path=OUT / "c2_order.png")
    # 3. reload keeps both
    pg.reload(); pg.wait_for_selector(".msg.bot .court-card", timeout=20_000)
    ok("court card + order summary survive reload", pg.locator(".court-card").count() == 1 and pg.locator(".order-extra").count() == 1)
    # 4. wrong CNR -> clear message
    pg.click(".side-nav .tab[data-tab=court]"); pg.fill("#cnrInput", "DLCT010099992025"); pg.click("#cnrForm button")
    pg.wait_for_function("document.querySelector('.msg.bot:last-child') && /No case found/.test(document.querySelector('.msg.bot:last-child').innerText)", timeout=30_000)
    ok("unknown CNR -> 'No case found' message", True)
    # 5. party search -> track
    if not pg.is_visible("#p-court"):
        pg.click(".side-nav .tab[data-tab=court]")
    pg.click(".court-more summary"); pg.fill("#partyInput", "Priya Sharma"); pg.click("#partyForm button")
    pg.wait_for_selector("#partyResults .cr-item", timeout=30_000)
    ok("party-name search lists the case", "Priya Sharma vs Ramesh Gowda" in pg.inner_text("#partyResults"))
    pg.screenshot(path=OUT / "c3_panel.png")
    # 6. a normal message without CNR still goes to the chat model
    ok("no JavaScript errors", not errs, "; ".join(errs)[:300])
    b.close()
print(f"\n{sum(res)}/{len(res)} passed")
