/* Login page: Log in / Create account (email + password, or Google), or continue as guest. */
(function () {
  const $ = s => document.querySelector(s);
  const store = {
    get(k, d) { try { const v = localStorage.getItem(k); return v ? JSON.parse(v) : d; } catch { return d; } },
    set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch {} },
  };
  const STR = window.HAQ_I18N, LANGS = window.HAQ_LANGS;
  const lang = () => $("#lang").value || "en";
  const tr = k => (STR[lang()] || {})[k] ?? STR.en[k] ?? k;
  function applyI18n() {
    document.documentElement.lang = lang() === "hinglish" ? "hi" : lang();
    document.querySelectorAll("[data-i18n]").forEach(el => { el.textContent = tr(el.dataset.i18n); });
  }
  function setTheme(th) { document.documentElement.dataset.theme = th; try { localStorage.setItem("haq_theme", th); } catch {} $("#themeBtn").innerHTML = th === "dark" ? '<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>' : '<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg>'; }
  const msg = (t, bad) => { $("#msg").textContent = t || ""; $("#msg").className = "small login-msg" + (bad ? " bad-text" : " ok-text"); };
  const busy = (form, on) => form.querySelectorAll("button, input").forEach(el => (el.disabled = on));
  const goApp = () => { store.set("haq_mode", "account"); location.replace("/"); };

  function showTab(which) {
    const signup = which === "signup";
    $("#tabLogin").classList.toggle("active", !signup); $("#tabSignup").classList.toggle("active", signup);
    $("#loginForm").classList.toggle("hidden", signup); $("#signupForm").classList.toggle("hidden", !signup);
    $("#loginTitle").textContent = tr(signup ? "signup_title" : "login_title");
    msg("");
    history.replaceState(null, "", signup ? "/login?signup=1" : "/login");
  }

  $("#lang").innerHTML = LANGS.map(([c, n]) => `<option value="${c}">${n}</option>`).join("");
  $("#lang").value = STR[store.get("haq_lang", "en")] ? store.get("haq_lang", "en") : "en";
  $("#lang").onchange = () => { store.set("haq_lang", lang()); applyI18n(); showTab($("#tabSignup").classList.contains("active") ? "signup" : "login"); };
  $("#themeBtn").onclick = () => setTheme(document.documentElement.dataset.theme === "dark" ? "light" : "dark");
  setTheme(document.documentElement.dataset.theme === "dark" ? "dark" : "light");
  applyI18n();
  $("#tabLogin").onclick = () => showTab("login");
  $("#tabSignup").onclick = () => showTab("signup");
  document.querySelectorAll("[data-goto]").forEach(b => b.onclick = () => showTab(b.dataset.goto));
  document.querySelectorAll(".pw-eye").forEach(b => b.onclick = () => { const i = document.getElementById(b.dataset.for); i.type = i.type === "password" ? "text" : "password"; });
  showTab(/signup=1/.test(location.search) ? "signup" : "login");
  $("#guestBtn").onclick = () => { store.set("haq_mode", "guest"); location.replace("/"); };

  let sb = null, cfg = {};
  let markReady; const ready = new Promise(r => (markReady = r));
  (async () => {
    try { cfg = (await (await fetch("/api/config")).json()).supabase || {}; } catch { cfg = {}; }
    if (!cfg.url || !cfg.anon_key || !window.supabase) {
      document.querySelectorAll("#googleBtn, .or, #loginForm, #signupForm, .auth-tabs").forEach(el => el.classList.add("hidden"));
      msg(tr("accounts_off"), true);
      markReady(); return;
    }
    sb = window.supabase.createClient(cfg.url, cfg.anon_key, { auth: { persistSession: true, detectSessionInUrl: true } });
    markReady();
    const { data } = await sb.auth.getSession();
    if (data.session) { goApp(); return; }
    sb.auth.onAuthStateChange((_e, s) => { if (s) goApp(); });
  })();

  $("#googleBtn").onclick = async () => {
    await ready; if (!sb) return;
    if (!cfg.google) { msg(tr("google_off"), true); return; }  // set SUPABASE_GOOGLE_LOGIN=1 once Google is enabled in Supabase
    msg("…", false);
    const { error } = await sb.auth.signInWithOAuth({ provider: "google", options: { redirectTo: location.origin + "/" } });
    if (error) msg(/not enabled|provider/i.test(error.message) ? tr("google_off") : "⚠️ " + error.message, true);
  };

  $("#loginForm").onsubmit = async e => {
    e.preventDefault();
    const f = e.target; busy(f, true); msg("…", false);
    await ready; if (!sb) { busy(f, false); msg(tr("accounts_off"), true); return; }
    const { error } = await sb.auth.signInWithPassword({ email: $("#liEmail").value.trim().toLowerCase(), password: $("#liPass").value });
    busy(f, false);
    if (error) { msg(/invalid/i.test(error.message) ? tr("bad_login") : "⚠️ " + error.message, true); return; }
    goApp();
  };

  $("#signupForm").onsubmit = async e => {
    e.preventDefault();
    await ready; if (!sb) { msg(tr("accounts_off"), true); return; }
    const f = e.target, email = $("#suEmail").value.trim().toLowerCase(), password = $("#suPass").value, first_name = $("#suName").value.trim();
    if (password.length < 8) { msg(tr("pw_rule"), true); return; }
    busy(f, true); msg(tr("creating"), false);
    let r;
    try { r = await (await fetch("/api/signup", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ email, password, first_name }) })).json(); }
    catch { r = { ok: false, error: "server" }; }
    if (!r.ok) {
      busy(f, false);
      const map = { exists: "err_exists", bad_email: "err_email", short_password: "pw_rule", no_name: "err_name", rate_limited: "err_rate" };
      msg(tr(map[r.error] || "err_server"), true);
      if (r.error === "exists") { $("#liEmail").value = email; }
      return;
    }
    const { error } = await sb.auth.signInWithPassword({ email, password });
    busy(f, false);
    if (error) { msg("⚠️ " + error.message, true); return; }
    goApp();
  };
})();
