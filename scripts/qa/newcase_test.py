"""New case button: from a case with a conversation and from another panel -> fresh case, welcome screen, list shows both, input focused."""
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
    for vw, tag in [((1440, 900), "desktop"), ((390, 844), "phone")]:
        ctx = b.new_context(viewport={"width": vw[0], "height": vw[1]})
        ctx.add_init_script("try{localStorage.setItem('haq_mode','\"guest\"')}catch(e){}")
        pg = ctx.new_page(); pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.goto(URL + "/"); pg.wait_for_selector(".card[data-prompt]"); time.sleep(1)
        # simulate an existing conversation in the current case
        pg.evaluate("""() => { S = S || {}; S.messages = [{role:'user', content:'My landlord kept my 40000 deposit'}, {role:'assistant', content:'ok'}];
                               VIEW.turns = [{reply:'**Your legal position:** test', citations:[], guard:{}, actions:[]}]; Cases.touch(); renderAll(); }""")
        time.sleep(0.3)
        ok(f"{tag}: conversation shown before", pg.is_hidden("#welcome"))
        if tag == "desktop":
            pg.click(".side-nav .tab[data-tab=deadlines]")
        else:
            pg.click("#toggleSide"); time.sleep(0.3)
        pg.click("#newCase2"); time.sleep(0.5)
        n_items = pg.locator(".case-item").count()
        ok(f"{tag}: new case -> welcome screen", pg.is_visible("#welcome"))
        ok(f"{tag}: both cases listed", n_items == 2, str(n_items))
        ok(f"{tag}: new case is the active one", "landlord" not in pg.locator(".case-item.active").inner_text().lower())
        ok(f"{tag}: message box focused", pg.evaluate("document.activeElement.id") == "input")
        if tag == "desktop":
            ok("desktop: panel switched to My cases", pg.is_visible("#p-cases") and pg.is_hidden("#viewBar"))
            ok("desktop: header says Haq", "Haq" in pg.inner_text("#brandBtn"))
            pg.screenshot(path=OUT / "newcase_desktop.png")
            pg.click("#newCase2"); time.sleep(0.3)
            ok("desktop: clicking again keeps one empty case (no duplicates)", pg.locator(".case-item").count() == 2)
        else:
            ok("phone: drawer closed after new case", pg.evaluate("!document.querySelector('#side').classList.contains('open')"))
        ctx.close()
    b.close()
print(f"\n{sum(res)}/{len(res)} passed; JS errors: {errs or 'none'}")

