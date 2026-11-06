"""Browser test of the real UI (clicks through the whole flow in Edge/Chromium).

    pip install playwright
    python -m scripts.ui_smoke http://127.0.0.1:8000 [screenshot_dir]

Uses the system Microsoft Edge (no browser download). Prints PASS/FAIL per step and any
JavaScript errors, and saves screenshots.
"""
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

URL = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8000"
SHOTS = Path(sys.argv[2] if len(sys.argv) > 2 else "ui_shots")
SHOTS.mkdir(parents=True, exist_ok=True)
results, js_errors = [], []


def step(name, fn):
    t = time.time()
    try:
        detail = fn() or ""
        results.append((True, name, f"{detail} ({time.time() - t:.1f}s)"))
    except Exception as e:  # noqa: BLE001
        results.append((False, name, f"{type(e).__name__}: {str(e)[:300]}"))


with sync_playwright() as p:
    browser = p.chromium.launch(channel="msedge", headless=True)
    ctx = browser.new_context(viewport={"width": 1440, "height": 900}, accept_downloads=True)
    page = ctx.new_page()
    page.on("pageerror", lambda e: js_errors.append(f"pageerror: {e}"))
    page.on("console", lambda m: js_errors.append(f"console.{m.type}: {m.text}") if m.type == "error" else None)
    page.on("dialog", lambda d: d.accept())

    def load():
        page.goto(URL, timeout=120_000)
        page.wait_for_selector(".card[data-prompt]")
        n = page.locator("#provider option").count()
        page.screenshot(path=SHOTS / "01_home.png")
        return f"{n} model option(s) in the switcher"

    step("home page loads", load)

    def chat():
        page.fill("#input", "mera landlord 40000 deposit wapas nahi kar raha. 31 aug 2026 ko Pune wala flat chhoda tha, rent 20000 tha, registered agreement hai")
        page.click("#send")
        page.wait_for_selector(".msg.bot .bubble .meta", timeout=240_000)
        txt = page.locator(".msg.bot .bubble").last.inner_text()
        page.screenshot(path=SHOTS / "02_chat_reply.png")
        assert len(txt) > 80, "reply too short"
        return txt[:120].replace("\n", " ")

    step("send Hinglish message, get a reply", chat)

    def case_panel():
        assert page.is_visible("#caseBody"), "case panel not visible"
        facts = page.locator("#facts dt").count()
        cat = page.inner_text("#catPill")
        assert facts >= 2, f"only {facts} facts shown"
        return f"category '{cat}', {facts} facts"

    step("case file panel fills in", case_panel)

    def chips():
        g = page.locator(".chip.guard-ok, .chip.guard-fix").count()
        laws = page.locator(".chip.law").count()
        if laws:
            page.locator(".chip.law").first.click()
            assert page.is_visible("#cite-pop"), "citation popover didn't open"
            page.screenshot(path=SHOTS / "03_citation_popover.png")
            page.mouse.click(5, 300)
        assert g >= 1, "no guard chip"
        return f"{laws} law chip(s), guard chip present"

    step("guard chip + citation popover", chips)

    def deadlines():
        page.click(".tab[data-tab=deadlines]")
        n = page.locator("#deadlines .deadline").count()
        page.screenshot(path=SHOTS / "04_deadlines.png")
        assert n >= 1, "no deadline cards"
        return page.locator("#deadlines .deadline .when").first.inner_text()

    step("deadlines tab shows computed dates", deadlines)

    def draft():
        page.click(".tab[data-tab=docs]")
        page.locator("#docButtons button").first.click()
        page.wait_for_selector("#docText", timeout=240_000)
        body = page.input_value("#docText")
        page.screenshot(path=SHOTS / "05_draft.png")
        with page.expect_download(timeout=60_000) as dl:
            page.click("#dlDocx")
        path = SHOTS / dl.value.suggested_filename
        dl.value.save_as(path)
        assert len(body) > 400 and path.stat().st_size > 5000
        return f"draft {len(body)} chars, {body.count('[[FILL')} gaps, docx {path.stat().st_size} bytes"

    step("draft document + Word download", draft)

    def practice():
        page.click(".tab[data-tab=practice]")
        page.click("#practiceStart")
        page.wait_for_selector(".pmsg.other", timeout=120_000)
        page.fill("#practiceInput", "Uncle, maine 31 August ko keys di thi. 40000 deposit 15 din mein bank transfer kar dijiye, warna legal notice bhejna padega.")
        page.press("#practiceInput", "Enter")
        page.wait_for_function("document.querySelectorAll('.pmsg.other').length >= 2", timeout=120_000)
        page.click("#practiceEnd")
        page.wait_for_selector(".score", timeout=120_000)
        page.screenshot(path=SHOTS / "06_practice_feedback.png")
        return f"{page.locator('.score').count()} scores shown"

    step("practice role-play + feedback", practice)

    def help_tab():
        page.click(".tab[data-tab=help]")
        n = page.locator("#kbList div").count()
        assert n >= 50, f"library list has {n}"
        return f"{n} library entries listed"

    step("get-help tab + library list", help_tab)

    def persists():
        page.reload()
        page.wait_for_selector(".msg.bot", timeout=30_000)
        return f"{page.locator('.msg').count()} messages restored after reload"

    step("conversation survives page reload", persists)

    def notice():
        page.click("#newCase")
        page.wait_for_selector("#welcome:not(.hidden)")
        page.click("#noticeCard")
        page.fill("#noticeText", "LEGAL NOTICE. Under instructions from my client Mr. S.K. Verma, I call upon you to pay Rs. 1,00,000 towards damages to Flat 4B within 15 days of receipt of this notice, failing which my client shall initiate civil proceedings against you at your risk as to costs.")
        page.click("#noticeGo")
        page.wait_for_selector(".notice-card", timeout=180_000)
        page.screenshot(path=SHOTS / "07_notice.png")
        return page.locator(".notice-card").inner_text()[:120].replace("\n", " ")

    step("explain a pasted notice", notice)

    def hindi_ui():
        page.click("#newCase")
        page.select_option("#lang", "hi-IN")
        h = page.inner_text(".welcome h1")
        page.select_option("#lang", "auto")
        assert any("ऀ" <= c <= "ॿ" for c in h), h
        return h

    step("Hindi interface text", hindi_ui)

    def mobile():
        m = browser.new_context(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True)
        mp = m.new_page()
        mp.goto(URL, timeout=120_000)
        mp.wait_for_selector(".card[data-prompt]")
        overflow = mp.evaluate("document.documentElement.scrollWidth > window.innerWidth + 1")
        mp.screenshot(path=SHOTS / "08_mobile.png")
        mp.click("#toggleCase")
        time.sleep(0.4)
        mp.screenshot(path=SHOTS / "09_mobile_casepanel.png")
        m.close()
        assert not overflow, "horizontal overflow on mobile"
        return "no horizontal scroll"

    step("mobile layout (390px)", mobile)
    browser.close()

for ok, name, detail in results:
    print(("PASS " if ok else "FAIL ") + name + " | " + detail)
print(f"\n{sum(r[0] for r in results)}/{len(results)} steps passed")
print("JS errors:", js_errors or "none")
