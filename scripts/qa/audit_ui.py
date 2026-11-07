"""Full UI audit: every interactive element on the login page and the app, desktop + phone.
No LLM calls except where noted; case state is injected so case-dependent tools can be tested.
Collects JS errors and failed network requests on every page."""
import json
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

URL = sys.argv[1].rstrip("/"); OUT = Path(sys.argv[2]); OUT.mkdir(parents=True, exist_ok=True)
res, errs, bad_net = [], [], []


def ok(area, name, cond, detail=""):
    res.append((area, name, bool(cond), detail))
    print(("PASS " if cond else "FAIL ") + f"[{area}] {name}" + (f" | {detail}" if detail else ""))


def watch(pg, tag):
    pg.on("pageerror", lambda e: errs.append(f"{tag}: {e}"))
    pg.on("console", lambda m: errs.append(f"{tag} console.{m.type}: {m.text[:200]}") if m.type == "error" and "favicon" not in m.text else None)
    pg.on("response", lambda r: bad_net.append(f"{tag}: {r.status} {r.request.method} {r.url[:120]}") if r.status >= 500 or (r.status >= 400 and "/api/" in r.url) else None)


STATE = """() => {
  S = {version:1, messages:[
    {role:'user', content:'I moved out of my flat in Pune on 31 August 2026. Landlord Ramesh is keeping my 40000 deposit.'},
    {role:'assistant', content:'**My view:** You have good grounds.'}],
    case:{category:'tenancy', language:'English', script:'Latin', facts:{deposit_amount:40000, monthly_rent:20000, possession_handed_over_date:'2026-08-31', other_party_name:'Ramesh', city_state:'Pune'},
          timeline:[{date:'2026-08-31', event:'Moved out'}], evidence_have:['Rent agreement'], evidence_missing:['Bank proof'], next_step:'Send a written demand'},
    flags:{level:'recommended', reasons:['Test reason']}, log:[]};
  VIEW.turns = [{reply:'**My view:** You have good grounds.', actions:[{type:'draft', doc:'deposit_demand_notice'},{type:'practice'},{type:'get_help'}], citations:[], guard:{},
    calculated:{deadlines:[{label:'Last date to sue (3 years)', date:'2029-08-31', days_left:1029, status:'ok', basis:'LIM1963-ART55', user_deadline:true}], derived:[]},
    completeness:{pct:60, missing:[{question:'Do you have a written agreement?'}]}, needs_lawyer:{level:'recommended', reasons:['Test reason']}}];
  Cases.touch(); renderAll();
}"""

with sync_playwright() as p:
    b = p.chromium.launch(channel="msedge", headless=True)

    # ======================= LOGIN PAGE =======================
    ctx = b.new_context(viewport={"width": 1366, "height": 860})
    pg = ctx.new_page(); watch(pg, "login")
    pg.goto(URL + "/"); pg.wait_for_url("**/login*", timeout=60_000)
    ok("login", "opening the app without a session redirects to /login", "/login" in pg.url)
    pg.wait_for_function("document.querySelector('#loginForm') && !document.querySelector('#loginForm').classList.contains('hidden')")
    t0 = pg.inner_text("#loginTitle")
    pg.select_option("#lang", "hi"); time.sleep(0.2)
    ok("login", "language dropdown changes the page text", pg.inner_text("#loginTitle") != t0, pg.inner_text("#loginTitle"))
    pg.select_option("#lang", "en")
    th = pg.evaluate("document.documentElement.dataset.theme"); pg.click("#themeBtn")
    ok("login", "theme button toggles light/dark", pg.evaluate("document.documentElement.dataset.theme") != th); pg.click("#themeBtn")
    pg.click("#tabSignup"); ok("login", "'Create account' tab shows the sign-up form", pg.is_visible("#signupForm") and pg.is_hidden("#loginForm"))
    pg.click("#signupForm [data-goto=login]"); ok("login", "'Log in' link inside sign-up switches back", pg.is_visible("#loginForm"))
    pg.click("#loginForm [data-goto=signup]"); ok("login", "'Create account' link inside log-in switches", pg.is_visible("#signupForm")); pg.click("#tabLogin")
    pg.fill("#liPass", "secret123"); pg.click("#loginForm .pw-eye")
    ok("login", "eye button shows the password", pg.get_attribute("#liPass", "type") == "text"); pg.click("#loginForm .pw-eye")
    ok("login", "eye button hides it again", pg.get_attribute("#liPass", "type") == "password")
    pg.fill("#liEmail", ""); pg.fill("#liPass", ""); pg.click("#loginForm button[type=submit]"); time.sleep(0.5)
    ok("login", "empty log-in is blocked by the form (stays on page)", "/login" in pg.url and pg.evaluate("!document.querySelector('#liEmail').checkValidity()"))
    pg.fill("#liEmail", "not-an-email"); pg.fill("#liPass", "whatever1"); pg.click("#loginForm button[type=submit]"); time.sleep(0.5)
    ok("login", "invalid email format is blocked", pg.evaluate("!document.querySelector('#liEmail').checkValidity()"))
    pg.fill("#liEmail", "nobody.qa.audit@example.com"); pg.fill("#liPass", "wrongpass1"); pg.click("#loginForm button[type=submit]")
    pg.wait_for_selector("#msg.bad-text", timeout=30_000)
    ok("login", "wrong email/password shows a clear error", "wrong" in pg.inner_text("#msg").lower(), pg.inner_text("#msg"))
    pg.fill("#liEmail", ""); pg.click("#forgotBtn"); time.sleep(0.3)
    ok("login", "'Forgot password?' without an email asks for the email first", "email" in pg.inner_text("#msg").lower(), pg.inner_text("#msg"))
    pg.click("#tabSignup"); pg.fill("#suName", "QA"); pg.fill("#suEmail", "qa.audit@example.com"); pg.fill("#suPass", "short")
    pg.click("#signupForm button[type=submit]"); time.sleep(0.5)
    ok("login", "sign-up with a 5-char password is refused", "/login" in pg.url and (pg.evaluate("!document.querySelector('#suPass').checkValidity()") or "8" in pg.inner_text("#msg")))
    pg.fill("#suName", ""); pg.fill("#suPass", "longenough1"); pg.click("#signupForm button[type=submit]"); time.sleep(0.4)
    ok("login", "sign-up without a name is refused", pg.evaluate("!document.querySelector('#suName').checkValidity()"))
    links = pg.evaluate("[...document.querySelectorAll('a')].map(a => a.getAttribute('href'))")
    ok("login", "login page links to privacy policy and terms", "/privacy" in links and "/terms" in links, str(links))
    pg.screenshot(path=OUT / "L1_login.png")
    pg.click("#tabLogin"); pg.click("#guestBtn"); pg.wait_for_url(URL + "/", timeout=30_000)
    ok("login", "'Continue as guest' opens the app", pg.url.rstrip("/") == URL)
    ctx.close()

    for path, word in [("/privacy", "Privacy policy"), ("/terms", "Terms of use")]:
        ctx = b.new_context(); pg = ctx.new_page(); watch(pg, path)
        r = pg.goto(URL + path)
        ok("pages", f"{path} loads", r.status == 200 and word in pg.inner_text("h1"))
        ctx.close()

    # ======================= APP (desktop, guest) =======================
    ctx = b.new_context(viewport={"width": 1366, "height": 860}, accept_downloads=True)
    ctx.add_init_script("try{localStorage.setItem('haq_mode','\"guest\"')}catch(e){}")
    pg = ctx.new_page(); watch(pg, "app")
    dialogs = []
    pg.on("dialog", lambda d: (dialogs.append((d.type, d.message)), d.accept("Renamed by QA") if d.type == "prompt" else d.accept()))
    pg.goto(URL + "/"); pg.wait_for_selector(".card[data-prompt]"); pg.wait_for_function("typeof CONFIG !== 'undefined' && CONFIG && CONFIG.doc_types && window.KB && window.KB.length", timeout=30_000)

    # welcome cards
    cards = pg.locator("#cards .card")
    n = cards.count(); filled = 0; dlg = 0
    for i in range(n):
        cards.nth(i).click(); time.sleep(0.1)
        if pg.evaluate("document.querySelector('#noticeDlg').open"):
            dlg += 1; pg.keyboard.press("Escape"); time.sleep(0.1)
        elif pg.input_value("#input").strip():
            filled += 1
        pg.fill("#input", "")
    ok("chat", f"all {n} welcome cards do something (fill the box or open the notice dialog)", filled + dlg == n, f"{filled} filled, {dlg} dialog")
    # empty / whitespace send
    before = pg.locator(".msg").count()
    pg.fill("#input", "   "); pg.click("#send"); time.sleep(0.5)
    ok("chat", "empty / whitespace-only message is not sent", pg.locator(".msg").count() == before)
    # attach -> notice dialog; empty submit
    pg.click("#attach"); ok("chat", "attach (paperclip) opens the notice dialog", pg.evaluate("document.querySelector('#noticeDlg').open"))
    nmsg = pg.locator(".msg").count()
    dialogs.clear(); pg.fill("#noticeText", ""); pg.click("#noticeGo"); time.sleep(1.0)
    ok("chat", "'Explain notice' with no text and no file is refused (no empty request)", pg.locator(".msg").count() == nmsg, f"msgs {nmsg}->{pg.locator('.msg').count()}")
    if pg.evaluate("document.querySelector('#noticeDlg').open"):
        pg.keyboard.press("Escape")
    time.sleep(0.3)
    if pg.locator(".msg.bot .typing").count():
        pg.wait_for_function("!document.querySelector('.msg.bot .typing')", timeout=120_000)
    ok("chat", "notice dialog closes with Escape", not pg.evaluate("document.querySelector('#noticeDlg').open"))
    # mic (no microphone in headless: must not crash)
    e0 = len(errs); pg.click("#mic"); time.sleep(1.0)
    if pg.evaluate("document.querySelector('#mic').classList.contains('rec')"):
        pg.click("#mic"); time.sleep(0.5)
    ok("chat", "mic button doesn't throw without a microphone", len([e for e in errs[e0:] if "pageerror" in e or "Uncaught" in e]) == 0, "; ".join(errs[e0:])[:150])

    # practice hearing (now in the chat) before any case exists
    ok("tools", "Practice is no longer a sidebar tool", pg.locator(".side-nav .tab[data-tab=practice]").count() == 0)
    e0 = len(errs); pg.fill("#input", "practice"); pg.press("#input", "Enter"); time.sleep(0.8)
    ok("tools", "'practice' in the chat before a case asks for the problem first", "problem" in pg.locator(".msg.bot").last.inner_text().lower() and len(errs) == e0, pg.locator(".msg.bot").last.inner_text()[:80])

    # inject a case for case-dependent tools
    pg.evaluate(STATE); time.sleep(0.4)
    if not pg.locator(".msg").count():
        pg.evaluate(STATE); time.sleep(0.4)

    # every sidebar tool: opens in main area, title, toggle closes, back + close + Escape work
    tools = pg.evaluate("[...document.querySelectorAll('.side-nav .tab')].map(t => t.dataset.tab)")
    for t in tools:
        pg.click(f".side-nav .tab[data-tab={t}]"); time.sleep(0.15)
        opened = pg.is_visible(f"#toolView #p-{t}") and pg.is_hidden("#composer") and pg.is_visible("#caseList")
        title = pg.inner_text("#toolTitle")
        pg.click(f".side-nav .tab[data-tab={t}]"); time.sleep(0.1)
        toggled = pg.is_hidden("#toolView") and pg.is_visible("#composer")
        ok("sidebar", f"'{t}' opens in the main area, titled, and toggles back to chat", opened and title and toggled, title)
    pg.click(".side-nav .tab[data-tab=case]"); pg.click("#toolBack"); ok("sidebar", "tool back arrow returns to chat", pg.is_hidden("#toolView"))
    pg.click(".side-nav .tab[data-tab=case]"); pg.keyboard.press("Escape"); ok("sidebar", "Escape closes the tool", pg.is_hidden("#toolView"))
    ok("sidebar", "'Track case' sits under New case with a LIVE badge", pg.evaluate("document.querySelector('#newCase2').nextElementSibling.dataset.tab === 'court'") and pg.is_visible(".nav-track .live-badge"), pg.inner_text(".nav-track"))

    # Case file tool
    pg.click(".side-nav .tab[data-tab=case]")
    ok("case file", "facts, timeline, evidence and next step render", pg.locator("#facts dt").count() >= 3 and "Moved out" in pg.inner_text("#timeline") and pg.is_visible("#nextStep"))
    steps = pg.locator("#checklist li").count()
    pg.locator("#checklist input").first.check()
    pg.fill("#addStepInput", ""); pg.press("#addStepInput", "Enter"); time.sleep(0.2)
    ok("case file", "empty custom step is not added", pg.locator("#checklist li").count() == steps)
    pg.fill("#addStepInput", "QA custom step"); pg.press("#addStepInput", "Enter"); time.sleep(0.2)
    ok("case file", "custom step is added", pg.locator("#checklist li").count() == steps + 1)
    sts = pg.locator(".st-step"); pg.locator(".st-step").nth(1).click(); time.sleep(0.1)
    ok("case file", "status steps are clickable", pg.locator(".st-step.on").count() >= 1, pg.inner_text(".st-step.on"))
    with pg.expect_download(timeout=15_000) as dl:
        pg.click("#exportCase")
    f = OUT / dl.value.suggested_filename; dl.value.save_as(f)
    ok("case file", "'Download case summary' downloads a file", f.stat().st_size > 200, f"{f.name} {f.stat().st_size}B")
    pg.screenshot(path=OUT / "A1_casefile.png")

    # Deadlines
    pg.click(".side-nav .tab[data-tab=deadlines]")
    ok("deadlines", "deadline card renders with source link", pg.locator("#deadlines .deadline").count() == 1 and pg.locator("#deadlines .deadline a").count() >= 1)
    with pg.expect_download(timeout=15_000) as dl:
        pg.locator("#deadlines .cal-btn").first.click()
    ok("deadlines", "per-deadline calendar button downloads .ics", "BEGIN:VCALENDAR" in Path(dl.value.path()).read_text(encoding="utf-8"))
    with pg.expect_download(timeout=15_000) as dl:
        pg.click("#calAll")
    ok("deadlines", "'Add all to calendar' downloads .ics", "BEGIN:VEVENT" in Path(dl.value.path()).read_text(encoding="utf-8"))

    # Documents
    pg.click(".side-nav .tab[data-tab=docs]")
    nb = pg.locator("#docButtons button").count()
    ok("documents", "document buttons for the case type are listed", nb >= 1, f"{nb} buttons")
    opts = pg.evaluate("[...document.querySelectorAll('#docLang option')].map(o=>o.value)")
    ok("documents", "document-language dropdown has options", len(opts) >= 2, str(opts))

    # Evidence
    pg.click(".side-nav .tab[data-tab=evidence]")
    bad = OUT / "evil.exe"; bad.write_bytes(b"MZ" + b"\0" * 100)
    e0 = len(errs); dialogs.clear()
    pg.set_input_files("#evFile", str(bad)); time.sleep(0.8)
    ok("evidence", "an .exe upload is rejected (not stored)", pg.locator(".ev-item").count() == 0, f"items={pg.locator('.ev-item').count()} dialogs={dialogs}")
    good = OUT / "receipt.txt"; good.write_text("Receipt: Rs 40,000 deposit paid on 1 Jan 2025 to Ramesh.", encoding="utf-8")
    pg.set_input_files("#evFile", str(good)); pg.wait_for_selector(".ev-item", timeout=10_000)
    ok("evidence", "a text receipt is stored in the locker", pg.locator(".ev-item").count() == 1)
    with pg.expect_popup(timeout=10_000) as pop:
        pg.locator(".ev-item [data-act=open]").first.click()
    ok("evidence", "'Open' shows the stored file", pop.value is not None); pop.value.close()
    pg.locator(".ev-item [data-act=del]").first.click(); time.sleep(0.4)
    ok("evidence", "'Delete' removes it (after confirm)", pg.locator(".ev-item").count() == 0)

    # Track case panel validation (no live calls)
    pg.click(".side-nav .tab[data-tab=court]"); dialogs.clear()
    pg.fill("#cnrInput", ""); pg.click("#cnrForm button"); time.sleep(0.3)
    ok("track case", "empty CNR is refused with a message", any("CNR" in m for _, m in dialogs), str(dialogs))
    dialogs.clear(); pg.fill("#cnrInput", "ABC123"); pg.click("#cnrForm button"); time.sleep(0.3)
    ok("track case", "malformed CNR is refused with a message", any("CNR" in m for _, m in dialogs), str(dialogs))
    pg.click(".court-more summary"); pg.fill("#partyInput", "ab"); pg.click("#partyForm button"); time.sleep(0.3)
    ok("track case", "party search with < 3 letters does nothing", pg.inner_text("#partyResults").strip() == "")
    pg.screenshot(path=OUT / "A2_trackcase.png")

    # Get help
    pg.click(".side-nav .tab[data-tab=help]")
    ok("help", "help list + verified library render", pg.locator("#helpList li").count() >= 3 and pg.locator("#kbList div").count() >= 50)
    pg.click("#toolClose")

    # chat extras: banner close, action buttons, law chip, read aloud
    if pg.is_visible("#banner .bn-x"):
        pg.click("#banner .bn-x"); ok("chat", "lawyer note closes with ×", pg.is_hidden("#banner"))
    acts = pg.locator(".msg.bot .actions button")
    ok("chat", "chat action buttons rendered (Draft / Start practice hearing / Free legal help)", acts.count() == 3 and "Start practice hearing" in acts.all_inner_texts(), str(acts.all_inner_texts()))
    pg.locator(".msg.bot .actions button", has_text="Free legal help").click(); time.sleep(0.2)
    ok("chat", "'Free legal help' opens Get help", pg.is_visible("#toolView #p-help")); pg.click("#toolClose")

    # sidebar: search, case menu rename/delete, collapse, Ctrl+B, brand
    pg.click("#searchBtn"); ok("sidebar", "search button shows the case search box", pg.is_visible("#caseSearch"))
    pg.fill("#caseSearch", "zzzz-no-match"); time.sleep(0.2)
    ok("sidebar", "search filters the list (no match -> empty message)", pg.locator(".case-item").count() == 0)
    pg.fill("#caseSearch", "pune"); time.sleep(0.2)
    ok("sidebar", "search finds a case by its title", pg.locator(".case-item").count() >= 1)
    pg.click("#searchBtn"); ok("sidebar", "search button again hides + clears the box", pg.is_hidden("#caseSearch") and pg.locator(".case-item").count() >= 1)
    pg.hover(".case-item"); pg.click(".case-item .ci-more"); ok("sidebar", "⋯ opens the case menu", pg.is_visible("#ciMenu"))
    pg.click("#ciMenu [data-act=rename]"); time.sleep(0.3)
    ok("sidebar", "Rename asks for a name and renames", "Renamed by QA" in pg.inner_text("#caseList"))
    pg.click("#newCase2"); time.sleep(0.3)
    ok("sidebar", "New case opens a fresh chat", pg.is_visible("#welcome"))
    pg.click("#collapseSide"); ok("sidebar", "collapse button -> icon strip", pg.evaluate("document.body.classList.contains('side-collapsed')"))
    pg.click(".side-nav .tab[data-tab=deadlines]"); time.sleep(0.1)
    ok("sidebar", "a tool opens from the icon strip without expanding the sidebar", pg.is_visible("#toolView") and pg.evaluate("document.body.classList.contains('side-collapsed')"))
    pg.click("#toolClose")
    pg.keyboard.press("Control+b"); ok("sidebar", "Ctrl+B expands it", not pg.evaluate("document.body.classList.contains('side-collapsed')"))
    pg.locator(".case-item", has_text="Renamed by QA").click(); time.sleep(0.3)
    pg.hover(".case-item.active"); pg.click(".case-item.active .ci-more"); pg.click("#ciMenu [data-act=delete]"); time.sleep(0.4)
    ok("sidebar", "Delete removes the case (after confirm)", "Renamed by QA" not in pg.inner_text("#caseList"))

    # settings + account popovers
    pg.click("#settingsBtn"); ok("settings", "gear opens settings", pg.is_visible("#settingsPop"))
    pg.select_option("#lang", "hi"); time.sleep(0.2)
    ok("settings", "language switch translates the UI", pg.inner_text(".side-nav .tab[data-tab=court]").strip() != "Track case", pg.inner_text(".side-nav .tab[data-tab=court]"))
    pg.select_option("#lang", "en")
    th = pg.evaluate("document.documentElement.dataset.theme"); pg.click("#themeBtn")
    ok("settings", "theme toggles and the settings box stays open", pg.evaluate("document.documentElement.dataset.theme") != th and pg.is_visible("#settingsPop"))
    if not pg.is_visible("#settingsPop"):
        pg.click("#settingsBtn")
    pg.click("#themeBtn")
    ok("settings", "settings box links to privacy + terms", pg.locator("#settingsPop a[href='/privacy']").count() == 1)
    provs = pg.evaluate("[...document.querySelectorAll('#provider option')].map(o=>o.value)")
    if len(provs) > 1:
        pg.select_option("#provider", provs[1]); pg.reload(); pg.wait_for_selector("#provider option", state="attached"); time.sleep(1)
        ok("settings", "AI model choice is remembered after reload", pg.input_value("#provider") == provs[1], f"{provs}")
        pg.click("#settingsBtn"); pg.select_option("#provider", provs[0])
    pg.keyboard.press("Escape")
    pg.click("#acctBtn"); ok("account", "profile icon opens the account box (guest: Sign in)", pg.is_visible("#acctPop") and pg.is_visible("#signInBtn") and pg.is_hidden("#settingsPop"))
    pg.click("#signInBtn"); pg.wait_for_url("**/login*", timeout=15_000)
    ok("account", "'Sign in' goes to the login page", "/login" in pg.url)
    ctx.close()

    # ======================= PHONE =======================
    ctx = b.new_context(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True)
    ctx.add_init_script("try{localStorage.setItem('haq_mode','\"guest\"')}catch(e){}")
    pg = ctx.new_page(); watch(pg, "phone")
    pg.goto(URL + "/"); pg.wait_for_selector(".card[data-prompt]"); time.sleep(1)
    ok("phone", "sidebar hidden by default, hamburger visible", pg.is_visible("#toggleSide") and not pg.evaluate("document.querySelector('#side').classList.contains('open')"))
    pg.click("#toggleSide"); time.sleep(0.3); ok("phone", "hamburger opens the drawer", pg.evaluate("document.querySelector('#side').classList.contains('open')"))
    pg.click(".side-nav .tab[data-tab=deadlines]"); time.sleep(0.3)
    ok("phone", "a tool opens full-screen and the drawer closes", pg.is_visible("#toolView") and not pg.evaluate("document.querySelector('#side').classList.contains('open')"))
    pg.click("#toolClose"); pg.click("#toggleSide"); time.sleep(0.3); pg.mouse.click(370, 400); time.sleep(0.3)
    ok("phone", "tapping outside closes the drawer", not pg.evaluate("document.querySelector('#side').classList.contains('open')"))
    w = pg.evaluate("document.documentElement.scrollWidth")
    ok("phone", "no horizontal scrolling", w <= 392, f"scrollWidth {w}")
    pg.screenshot(path=OUT / "P1_phone.png")
    ctx.close()
    b.close()

print("\n=== JS errors ===\n" + ("\n".join(errs) or "none"))
print("=== failed API/5xx responses ===\n" + ("\n".join(bad_net) or "none"))
passed = sum(1 for r in res if r[2])
print(f"\n{passed}/{len(res)} UI checks passed")
(OUT / "audit_ui.json").write_text(json.dumps({"results": res, "js_errors": errs, "bad_net": bad_net}, indent=1, ensure_ascii=False), encoding="utf-8")
