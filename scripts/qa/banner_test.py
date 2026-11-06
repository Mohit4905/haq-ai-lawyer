"""Lawyer banner: new style, close button hides it, stays closed after re-render/reload, reappears for new reasons."""
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

URL = sys.argv[1].rstrip("/"); OUT = Path(sys.argv[2]); OUT.mkdir(parents=True, exist_ok=True)
errs, res = [], []


def ok(n, c, d=""):
    res.append(bool(c)); print(("PASS " if c else "FAIL ") + n + (f" | {d}" if d else ""))


SET = """([lv, r]) => { S = S || {}; S.flags = {level: lv, reasons: [r]}; renderBanner(); }"""
with sync_playwright() as p:
    b = p.chromium.launch(channel="msedge", headless=True)
    for theme in ["light", "dark"]:
        ctx = b.new_context(viewport={"width": 1200, "height": 700})
        ctx.add_init_script(f"try{{localStorage.setItem('haq_mode','\"guest\"');localStorage.setItem('haq_theme','{theme}')}}catch(e){{}}")
        pg = ctx.new_page(); pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.goto(URL + "/"); pg.wait_for_selector(".card[data-prompt]"); time.sleep(0.8)
        pg.evaluate(SET, ["urgent", "Murder ek serious criminal offence hai, court process aur defence ke liye vakil ki zaroorat hai"])
        ok(f"{theme}: urgent note visible with close button", pg.is_visible("#banner .bn-x") and "lawyer" in pg.inner_text("#banner").lower())
        pg.locator("#banner").screenshot(path=OUT / f"banner_urgent_{theme}.png")
        pg.evaluate(SET, ["recommended", "Deadline soon: reply to notice (2026-11-12)"])
        pg.locator("#banner").screenshot(path=OUT / f"banner_rec_{theme}.png")
        pg.click("#banner .bn-x")
        ok(f"{theme}: close hides it", pg.is_hidden("#banner"))
        pg.evaluate("renderBanner()")
        ok(f"{theme}: stays closed when the chat re-renders", pg.is_hidden("#banner"))
        pg.reload(); pg.wait_for_selector(".card[data-prompt]"); time.sleep(0.5)
        pg.evaluate(SET, ["recommended", "Deadline soon: reply to notice (2026-11-12)"])
        ok(f"{theme}: stays closed after reload (same reason)", pg.is_hidden("#banner"))
        pg.evaluate(SET, ["recommended", "Other side has a lawyer"])
        ok(f"{theme}: shows again for a new reason", pg.is_visible("#banner"))
        pg.evaluate(SET, ["emergency", "self-harm"])
        ok(f"{theme}: emergency note has no close button", pg.is_visible("#banner") and not pg.is_visible("#banner .bn-x"))
        pg.locator("#banner").screenshot(path=OUT / f"banner_emerg_{theme}.png")
        ctx.close()
    b.close()
print(f"\n{sum(res)}/{len(res)} passed; JS errors: {errs or 'none'}")
