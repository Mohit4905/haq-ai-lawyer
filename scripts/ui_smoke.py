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
        try:
            page.screenshot(path=SHOTS / ("FAIL_" + "".join(ch if ch.isalnum() else "_" for ch in name)[:40] + ".png"))
        except Exception:  # noqa: BLE001
            pass


with sync_playwright() as p:
    browser = p.chromium.launch(channel="msedge", headless=True)
    ctx = browser.new_context(viewport={"width": 1440, "height": 900}, accept_downloads=True)
    page = ctx.new_page()
    page.on("pageerror", lambda e: js_errors.append(f"pageerror: {e}"))
    page.on("console", lambda m: js_errors.append(f"console.{m.type}: {m.text}") if m.type == "error" else None)
    page.on("dialog", lambda d: d.accept())

    def login_page():
        lp = browser.new_context(viewport={"width": 1440, "height": 900}).new_page()
        lp.on("pageerror", lambda e: js_errors.append(f"pageerror(login): {e}"))
        lp.goto(URL, timeout=120_000)
        lp.wait_for_url("**/login", timeout=30_000)
        lp.wait_for_selector("#guestBtn")
        lp.screenshot(path=SHOTS / "00_login.png")
        has_google = lp.locator("#googleBtn").is_visible(); has_email = lp.locator("#emailBtn").is_visible()
        lp.click("#guestBtn")
        lp.wait_for_selector(".card[data-prompt]", timeout=30_000)
        lp.goto(URL); lp.wait_for_selector(".card[data-prompt]", timeout=30_000)  # guest choice remembered
        lp.context.close()
        return f"first visit -> /login (google={has_google}, email={has_email}) -> guest -> app; remembered"

    step("login page: first visit, continue as guest", login_page)
    page.add_init_script("try{ if(!localStorage.getItem('haq_mode')) localStorage.setItem('haq_mode','\"guest\"'); }catch(e){}")

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

    def tracker():
        page.click(".tab[data-tab=case]")
        page.wait_for_selector("#tracker:not(.hidden)", timeout=10_000)
        n = page.locator("#checklist li").count()
        page.locator("#checklist input").first.check()
        page.fill("#addStepInput", "Call the landlord's brother")
        page.press("#addStepInput", "Enter")
        page.locator(".st-step[data-s=notice_sent]").click()
        page.reload(); page.wait_for_selector("#tracker:not(.hidden)")
        checked = page.locator("#checklist input:checked").count()
        on = page.locator(".st-step.on").inner_text()
        page.screenshot(path=SHOTS / "12_tracker.png")
        assert n >= 4 and checked >= 1 and page.locator("#checklist li").count() == n + 1, (n, checked)
        return f"{n} steps + 1 custom, {checked} ticked, status '{on}' kept after reload"

    step("case tracker + checklist (persists)", tracker)

    def calendar():
        page.click(".tab[data-tab=deadlines]")
        with page.expect_download(timeout=20_000) as dl:
            page.locator("#deadlines .cal-btn").first.click()
        path = SHOTS / "deadline.ics"
        dl.value.save_as(path)
        txt = path.read_text(encoding="utf-8")
        assert "BEGIN:VCALENDAR" in txt and "VALARM" in txt and "DTSTART;VALUE=DATE:" in txt
        return f".ics with {txt.count('BEGIN:VALARM')} alarm(s)"

    step("add deadline to calendar (.ics)", calendar)

    def evidence():
        page.click(".tab[data-tab=evidence]")
        rec = SHOTS / "rent_receipt.txt"
        rec.write_text("RENT & DEPOSIT RECEIPT\nReceived from Rahul Sharma the sum of Rs 40,000 (Rupees Forty Thousand only) as refundable security deposit "
                       "for Flat 12B, Kothrud, Pune, on 1 January 2025, paid by UPI ref 501234567890.\nMonthly rent: Rs 20,000.\nLandlord: Suresh Patil (signed)", encoding="utf-8")
        page.set_input_files("#evFile", str(rec))
        page.wait_for_selector(".ev-item", timeout=10_000)
        page.locator(".ev-item [data-act=read]").first.click()
        page.wait_for_selector(".ev-card", timeout=180_000)
        page.screenshot(path=SHOTS / "13_evidence_read.png")
        rows = page.locator(".ev-rows input:checked").count()
        page.locator(".ev-card [data-act=apply]").click()
        page.wait_for_selector(".ok-text", timeout=10_000)
        page.click(".tab[data-tab=case]")
        tl = page.inner_text("#timeline")
        assert "Jan 2025" in tl or "2025" in tl, tl
        return f"AI proposed {rows} item(s); applied; timeline now has: {tl[:80]!r}"

    step("evidence locker: upload → AI read → add to case file", evidence)

    def my_cases():
        first = page.locator(".case-item.active b").inner_text()
        page.click("#newCase2")
        page.wait_for_selector("#welcome:not(.hidden)")
        page.locator(".card[data-card=cheque]").click()
        page.click("#send")
        page.wait_for_selector(".msg.bot .bubble .meta", timeout=240_000)
        n = page.locator(".case-item").count()
        page.locator(".case-item", has_text=first[:15]).first.click()
        page.wait_for_selector(".msg.bot")
        back = page.locator(".msg.user").first.inner_text()
        page.screenshot(path=SHOTS / "14_my_cases.png")
        assert n >= 2 and "40000" in back, (n, back[:60])
        return f"{n} cases in sidebar; switched back to the first case"

    step("My cases: new case + switch back", my_cases)

    def notice():
        page.click("#newCase2")
        page.wait_for_selector("#welcome:not(.hidden)")
        page.click(".card[data-card=notice]")
        page.fill("#noticeText", "LEGAL NOTICE. Under instructions from my client Mr. S.K. Verma, I call upon you to pay Rs. 1,00,000 towards damages to Flat 4B within 15 days of receipt of this notice, failing which my client shall initiate civil proceedings against you at your risk as to costs.")
        page.click("#noticeGo")
        page.wait_for_selector(".notice-card", timeout=180_000)
        page.screenshot(path=SHOTS / "07_notice.png")
        return page.locator(".notice-card").inner_text()[:120].replace("\n", " ")

    step("explain a pasted notice", notice)

    def languages():
        page.click("#newCase2")
        out = []
        for code, lo, hi in [("hi", "ऀ", "ॿ"), ("pa", "਀", "੿"), ("ta", "஀", "௿")]:
            if not page.is_visible("#lang"):
                page.click("#settingsBtn")
                page.wait_for_selector("#lang", state="visible", timeout=5000)
            page.select_option("#lang", code)
            h = page.inner_text(".welcome h1")
            card = page.locator(".card b").first.inner_text()
            assert any(lo <= c <= hi for c in h + card), (code, h, card)
            out.append(f"{code}: {h[:22]}")
        page.screenshot(path=SHOTS / "10_tamil_ui.png")
        if not page.is_visible("#lang"):
            page.click("#settingsBtn")
        page.select_option("#lang", "en")
        page.keyboard.press("Escape")
        assert page.locator(".card").count() == 8, "expected 8 problem cards"
        return " | ".join(out)

    step("language switcher (Hindi, Punjabi, Tamil) + 8 cards", languages)

    def theme():
        assert page.evaluate("document.documentElement.dataset.theme") == "light", "default should be light"
        bg_light = page.evaluate("getComputedStyle(document.body).backgroundColor")
        page.click("#settingsBtn"); page.click("#themeBtn")
        bg_dark = page.evaluate("getComputedStyle(document.body).backgroundColor")
        page.screenshot(path=SHOTS / "11_dark.png")
        page.reload()
        kept = page.evaluate("document.documentElement.dataset.theme")
        page.click("#settingsBtn"); page.click("#themeBtn"); page.keyboard.press("Escape")
        assert bg_light != bg_dark and kept == "dark", (bg_light, bg_dark, kept)
        return f"light {bg_light} -> dark {bg_dark}, remembered after reload"

    step("light default + dark toggle", theme)

    def sidebar():
        page.click("#collapseSide")
        hidden = not page.is_visible("#side")
        page.screenshot(path=SHOTS / "15_collapsed.png")
        page.reload(); page.wait_for_selector("#chat")
        still = not page.is_visible("#side")
        page.click("#toggleSide")
        back = page.is_visible("#side")
        page.click("#settingsBtn")
        menu = page.is_visible("#settingsPop") and page.is_visible("#lang") and page.is_visible("#provider")
        page.screenshot(path=SHOTS / "16_settings.png")
        page.keyboard.press("Escape")
        assert hidden and still and back and menu, (hidden, still, back, menu)
        return "collapse -> remembered after reload -> reopen; settings menu at the bottom works"

    step("sidebar collapse/expand + settings menu", sidebar)

    def mobile():
        m = browser.new_context(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True)
        mp = m.new_page()
        mp.goto(URL + "/login", timeout=120_000); mp.wait_for_selector("#guestBtn")
        mp.screenshot(path=SHOTS / "08a_mobile_login.png")
        mp.add_init_script("try{ localStorage.setItem('haq_mode','\"guest\"'); }catch(e){}")
        mp.goto(URL, timeout=120_000)
        mp.wait_for_selector(".card[data-prompt]")
        overflow = mp.evaluate("document.documentElement.scrollWidth > window.innerWidth + 1")
        mp.screenshot(path=SHOTS / "08_mobile.png")
        mp.click("#toggleSide")
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
