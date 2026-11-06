/* Optional accounts (Supabase): email link/code or Google. Without sign-in everything still works on
   this device. Security: the browser only has the public anon key; every table and the storage bucket use
   row-level security so a user can only ever read/write their own rows/files (see supabase/schema.sql). */
(function () {
  let sb = null, user = null, profile = null;

  const CLOUD = {
    get user() { return user; },
    async pushCase(c) {
      if (!sb || !user) return;
      const row = { id: c.id, user_id: user.id, title: c.title || null, category: c.data?.state?.case?.category || null, status: c.status,
        data: { ...c, evidence: (c.evidence || []).map(e => ({ ...e })) }, updated_at: c.updated };
      const { error } = await sb.from("cases").upsert(row);
      if (error) console.warn("sync failed", error.message);
      if (c.remind) await CLOUD.syncReminders(c);
    },
    async deleteCase(c) {
      if (!sb || !user) return;
      for (const e of c.evidence || []) await CLOUD.deleteEvidence(c, e).catch(() => {});
      await sb.from("cases").delete().eq("id", c.id);
    },
    path(c, e) { return `${user.id}/${c.id}/${e.id}`; },
    async uploadEvidence(c, e, blob) { if (!sb || !user) return; await sb.storage.from("evidence").upload(CLOUD.path(c, e), blob, { upsert: true, contentType: e.type || "application/octet-stream" }); },
    async downloadEvidence(c, e) { if (!sb || !user) return null; const { data } = await sb.storage.from("evidence").download(CLOUD.path(c, e)); return data || null; },
    async deleteEvidence(c, e) { if (!sb || !user) return; await sb.storage.from("evidence").remove([CLOUD.path(c, e)]); },
    async syncReminders(c) {
      if (!sb || !user) return;
      const dls = (c.data?.view?.turns?.at(-1)?.calculated?.deadlines || []).filter(d => d.user_deadline !== false && d.days_left >= 0);
      await sb.from("reminders").delete().eq("case_id", c.id);
      if (!c.remind || !dls.length) return;
      await sb.from("reminders").insert(dls.map(d => ({ user_id: user.id, case_id: c.id, label: d.label, due_date: d.date, basis: d.basis || null, case_title: c.title || null })));
    },
    async pullMerge() {
      if (!sb || !user) return;
      const { data, error } = await sb.from("cases").select("id,data,updated_at");
      if (error) { console.warn(error.message); return; }
      const remote = Object.fromEntries((data || []).map(r => [r.id, r.data]));
      Cases.fromGlobals();
      // newer copy wins; local-only cases (made before signing in) are uploaded
      for (const [id, rc] of Object.entries(remote)) {
        const lc = Cases.all[id];
        if (!lc || (rc.updated || "") > (lc.updated || "")) Cases.all[id] = rc;
      }
      for (const c of Object.values(Cases.all)) {
        if (!remote[c.id] && (c.data?.state?.messages?.length || c.evidence?.length)) await CLOUD.pushCase(c);
      }
      Cases.saveLocal(); Cases.toGlobals(); renderAll(); renderCaseList();
    },
  };
  window.HAQ_CLOUD = CLOUD;

  function profileHtml() {
    if (!sb) return `<div class="pf guest"><div class="pf-av">👤</div><div><b>${esc(tr("guest"))}</b><small>${esc(tr("saved_device"))}</small></div></div>`;
    if (!user) return `<div class="pf guest"><div class="pf-av">👤</div><div><b>${esc(tr("guest"))}</b><small>${esc(tr("saved_device"))}</small></div></div>
      <button class="primary small wide" id="signInBtn">🔐 ${esc(tr("sign_in"))}</button><small class="muted tiny">${esc(tr("sign_in_why"))}</small>`;
    const name = profile?.full_name || user.email?.split("@")[0] || "";
    return `<div class="pf"><div class="pf-av in">${esc((name[0] || "?").toUpperCase())}</div><div><b>${esc(name)}</b><small>${esc(user.email || "")}</small></div></div>
      <div class="row"><button class="ghost small" id="profileBtn">⚙︎ ${esc(tr("profile"))}</button><button class="ghost small" id="signOutBtn">${esc(tr("sign_out"))}</button></div>
      <small class="muted tiny">☁️ ${esc(tr("saved_cloud"))}</small>`;
  }
  function renderProfile() {
    const box = $("#profileBox"); if (!box) return;
    box.innerHTML = profileHtml();
    $("#signInBtn")?.addEventListener("click", openSignIn);
    $("#signOutBtn")?.addEventListener("click", async () => { await sb.auth.signOut(); });
    $("#profileBtn")?.addEventListener("click", openProfile);
    renderReminderToggle();
  }
  window.renderProfile = renderProfile;

  function renderReminderToggle() {
    const box = $("#remindBox"); if (!box) return;
    const c = Cases.cur();
    if (!user || !CONFIG?.email_reminders) {
      box.innerHTML = user ? "" : `<p class="tiny muted">✉️ ${esc(tr("remind_signin"))}</p>`;
      return;
    }
    box.innerHTML = `<label class="toggle"><input type="checkbox" id="remindChk" ${c?.remind ? "checked" : ""}> ✉️ ${esc(tr("remind_email"))} <b>${esc(user.email)}</b></label>`;
    $("#remindChk").onchange = async e => { c.remind = e.target.checked; Cases.touch(false); await CLOUD.syncReminders(c); };
  }
  window.renderReminderToggle = renderReminderToggle;

  function openSignIn() {
    const d = $("#authDlg");
    $("#authStep1").classList.remove("hidden"); $("#authStep2").classList.add("hidden"); $("#authMsg").textContent = "";
    $("#googleBtn").classList.toggle("hidden", !CONFIG?.supabase?.google);
    d.showModal();
  }
  async function sendCode(e) {
    e.preventDefault();
    const email = $("#authEmail").value.trim(); if (!email) return;
    $("#authMsg").textContent = "…";
    const { error } = await sb.auth.signInWithOtp({ email, options: { emailRedirectTo: location.origin, shouldCreateUser: true } });
    if (error) { $("#authMsg").textContent = "⚠️ " + error.message; return; }
    $("#authStep1").classList.add("hidden"); $("#authStep2").classList.remove("hidden");
    $("#authSentTo").textContent = email; $("#authMsg").textContent = "";
  }
  async function verifyCode(e) {
    e.preventDefault();
    const email = $("#authEmail").value.trim(), token = $("#authCode").value.trim();
    const { error } = await sb.auth.verifyOtp({ email, token, type: "email" });
    if (error) { $("#authMsg").textContent = "⚠️ " + error.message; return; }
    $("#authDlg").close();
  }
  async function openProfile() {
    const d = $("#profileDlg");
    $("#pfName").value = profile?.full_name || ""; $("#pfCity").value = profile?.city || ""; $("#pfEmailRem").checked = profile?.email_reminders !== false;
    $("#pfEmail").textContent = user.email || "";
    d.showModal();
  }
  async function saveProfile(e) {
    e.preventDefault();
    profile = { id: user.id, full_name: $("#pfName").value.trim() || null, city: $("#pfCity").value.trim() || null, language: uiLang(), email_reminders: $("#pfEmailRem").checked, updated_at: new Date().toISOString() };
    const { error } = await sb.from("profiles").upsert(profile);
    $("#pfMsg").textContent = error ? "⚠️ " + error.message : "✓";
    renderProfile();
  }
  async function deleteAll() {
    if (!confirm(tr("confirm_delete_all"))) return;
    const { data } = await sb.from("cases").select("id,data");
    for (const r of data || []) for (const e of r.data?.evidence || []) await sb.storage.from("evidence").remove([`${user.id}/${r.id}/${e.id}`]).catch(() => {});
    await sb.from("reminders").delete().eq("user_id", user.id);
    await sb.from("cases").delete().eq("user_id", user.id);
    await sb.from("profiles").delete().eq("id", user.id);
    const { data: s } = await sb.auth.getSession();
    await fetch("/api/account/delete", { method: "POST", headers: { Authorization: "Bearer " + (s.session?.access_token || "") } }).catch(() => {});
    await sb.auth.signOut();
    $("#profileDlg").close();
    alert(tr("deleted_all"));
  }

  window.initAuth = async function initAuth(cfg) {
    renderProfile();
    if (!cfg?.url || !cfg?.anon_key || !window.supabase) return;
    sb = window.supabase.createClient(cfg.url, cfg.anon_key, { auth: { persistSession: true, detectSessionInUrl: true } });
    $("#authForm1").addEventListener("submit", sendCode);
    $("#authForm2").addEventListener("submit", verifyCode);
    $("#googleBtn").addEventListener("click", () => sb.auth.signInWithOAuth({ provider: "google", options: { redirectTo: location.origin } }));
    $("#pfForm").addEventListener("submit", saveProfile);
    $("#pfDelete").addEventListener("click", deleteAll);
    const { data: { session } } = await sb.auth.getSession();
    user = session?.user || null;
    if (user) { const { data } = await sb.from("profiles").select("*").eq("id", user.id).maybeSingle(); profile = data; }
    renderProfile();
    if (user) await CLOUD.pullMerge();
    sb.auth.onAuthStateChange(async (_ev, s) => {
      const was = user?.id; user = s?.user || null;
      if (user && user.id !== was) { const { data } = await sb.from("profiles").select("*").eq("id", user.id).maybeSingle(); profile = data; renderProfile(); await CLOUD.pullMerge(); }
      if (!user && was) { profile = null; renderProfile(); }
    });
  };
})();
