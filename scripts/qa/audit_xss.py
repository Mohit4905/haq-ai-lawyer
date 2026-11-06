"""XSS: hostile HTML in chat text, model replies, case titles, court data and judgments must never execute."""
import sys
import time

from playwright.sync_api import sync_playwright

URL = sys.argv[1].rstrip("/")
EVIL = "<img src=x onerror=window.__xss=1>"
res = []


def ok(n, c, d=""):
    res.append(bool(c)); print(("PASS " if c else "FAIL ") + n + (f" | {d}" if d else ""))


with sync_playwright() as p:
    b = p.chromium.launch(channel="msedge", headless=True)
    ctx = b.new_context(viewport={"width": 1366, "height": 860})
    ctx.add_init_script("try{localStorage.setItem('haq_mode','\"guest\"')}catch(e){}")
    pg = ctx.new_page(); errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.on("dialog", lambda d: d.dismiss())
    pg.goto(URL + "/"); pg.wait_for_function("typeof CONFIG !== 'undefined' && CONFIG && CONFIG.doc_types && window.KB && window.KB.length", timeout=30_000)
    pg.evaluate("""(EVIL) => {
      S = {version:1, messages:[{role:'user', content: EVIL + ' my landlord'}, {role:'assistant', content: '**' + EVIL + '** [x](javascript:window.__xss=3) <script>window.__xss=4</script>'}],
           case:{category:'tenancy', facts:{other_party_name: EVIL, summary: EVIL}, timeline:[{date:'2026-08-31', event: EVIL}], evidence_have:[EVIL], evidence_missing:[EVIL], next_step: EVIL},
           flags:{level:'urgent', reasons:[EVIL]}, log:[]};
      VIEW.turns = [{reply:'x', citations:[], guard:{initial:{violations:[{text:EVIL, why:EVIL}]}}, actions:[], calculated:{deadlines:[{label:EVIL, date:'2027-01-01', days_left:50, status:'ok', basis:EVIL, note:EVIL}], derived:[]}, completeness:{pct:10, missing:[{question:EVIL}]}}];
      Cases.cur().title = EVIL; Cases.cur().titleManual = true; Cases.touch(); renderAll();
    }""", EVIL)
    time.sleep(0.6)
    for t in ["case", "deadlines"]:
        pg.click(f".side-nav .tab[data-tab={t}]"); time.sleep(0.3)
    pg.click("#toolClose")
    pg.fill("#input", "XSSX 01 000001 2025"); pg.click("#send")
    pg.wait_for_selector(".court-card", timeout=30_000); time.sleep(0.5)
    pg.click(".side-nav .tab[data-tab=court]"); pg.fill("#judInput", "evil query"); pg.click("#judForm button")
    pg.wait_for_selector("#judResults .cr-item", timeout=30_000); time.sleep(0.5)
    xss = pg.evaluate("window.__xss")
    imgs = pg.evaluate("[...document.querySelectorAll('img')].filter(i => (i.getAttribute('src')||'') === 'x').length")
    scripts = pg.evaluate("[...document.querySelectorAll('#chat script, #toolBody script, #caseList script')].length")
    jslinks = pg.evaluate("[...document.querySelectorAll('a')].filter(a => /^\\s*javascript:/i.test(a.getAttribute('href')||'')).length")
    ok("no injected handler ran (window.__xss unset)", xss is None, str(xss))
    ok("no injected <img src=x> elements anywhere", imgs == 0, str(imgs))
    ok("no injected <script> elements", scripts == 0, str(scripts))
    ok("no javascript: links (chat markdown, judgments)", jslinks == 0, str(jslinks))
    ok("hostile text shown as text (escaped)", "onerror" in pg.inner_text("body"))
    ok("no JS errors", not errs, "; ".join(errs)[:200])
    b.close()
print(f"\n{sum(res)}/{len(res)} XSS checks passed")
