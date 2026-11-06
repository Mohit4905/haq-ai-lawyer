/* My cases (multi-case store), case tracker + checklist, calendar reminders (.ics), evidence locker.
   Works fully on this device (localStorage + IndexedDB). When signed in (auth.js), cases sync to the
   user's private Supabase rows and evidence files to their private storage folder. */

/* ---------------- tiny IndexedDB wrapper for evidence files (device copy) */
const EvDB = {
  _db: null,
  open() {
    if (this._db) return Promise.resolve(this._db);
    return new Promise((res, rej) => {
      try {
        const r = indexedDB.open("haq", 1);
        r.onupgradeneeded = () => r.result.createObjectStore("files");
        r.onsuccess = () => { this._db = r.result; res(this._db); };
        r.onerror = () => rej(r.error);
      } catch (e) { rej(e); }
    });
  },
  async put(key, blob) { const db = await this.open(); return new Promise((res, rej) => { const tx = db.transaction("files", "readwrite"); tx.objectStore("files").put(blob, key); tx.oncomplete = res; tx.onerror = () => rej(tx.error); }); },
  async get(key) { const db = await this.open(); return new Promise((res) => { const r = db.transaction("files").objectStore("files").get(key); r.onsuccess = () => res(r.result || null); r.onerror = () => res(null); }); },
  async del(key) { const db = await this.open(); return new Promise((res) => { const tx = db.transaction("files", "readwrite"); tx.objectStore("files").delete(key); tx.oncomplete = res; tx.onerror = res; }); },
};

const uid = () => (crypto.randomUUID ? crypto.randomUUID() : "c" + Date.now() + Math.random().toString(16).slice(2));
const CAT_EMOJI = { tenancy: "🏠", consumer: "📦", salary: "💼", cheque_bounce: "🧾", notice: "✉️", cyber_fraud: "📱", out_of_scope: "⚖️", other: "💬" };
const STATUS_TXT = {
  en: { new: "New", notice_sent: "Notice sent", waiting: "Waiting for reply", complaint_filed: "Complaint filed", resolved: "Resolved 🎉", closed: "Closed" },
  hi: { new: "नया", notice_sent: "नोटिस भेजा", waiting: "जवाब का इंतज़ार", complaint_filed: "शिकायत दर्ज", resolved: "सुलझ गया 🎉", closed: "बंद" },
  hinglish: { new: "Naya", notice_sent: "Notice bheja", waiting: "Jawab ka intezaar", complaint_filed: "Complaint file ki", resolved: "Suljh gaya 🎉", closed: "Band" },
  pa: { new: "ਨਵਾਂ", notice_sent: "ਨੋਟਿਸ ਭੇਜਿਆ", waiting: "ਜਵਾਬ ਦੀ ਉਡੀਕ", complaint_filed: "ਸ਼ਿਕਾਇਤ ਦਰਜ", resolved: "ਹੱਲ ਹੋ ਗਿਆ 🎉", closed: "ਬੰਦ" },
};
const statusText = s => (STATUS_TXT[uiLang()] || STATUS_TXT.en)[s] || STATUS_TXT.en[s] || s;

const Cases = {
  all: {}, currentId: null, _t: null,

  load() {
    this.all = store.get("haq_cases", {}) || {};
    this.currentId = store.get("haq_current", null);
    // migrate the single-conversation storage used by earlier versions
    const oldS = store.get("haq_state", null);
    if (oldS && oldS.messages?.length && !Object.keys(this.all).length) {
      const c = this.blank();
      c.data = { state: oldS, view: store.get("haq_view", { turns: [] }), practice: store.get("haq_practice", []) };
      c.title = this.autoTitle(c);
      this.all[c.id] = c; this.currentId = c.id;
      ["haq_state", "haq_view", "haq_practice"].forEach(store.del);
    }
    if (!this.currentId || !this.all[this.currentId]) {
      const ids = this.sorted().map(c => c.id);
      this.currentId = ids[0] || null;
    }
    if (!this.currentId) { const c = this.blank(); this.all[c.id] = c; this.currentId = c.id; }
    this.toGlobals();
    this.saveLocal();
  },
  blank() {
    const now = new Date().toISOString();
    return { id: uid(), title: "", status: "new", checks: {}, custom: [], remind: false, evidence: [], created: now, updated: now,
             data: { state: null, view: { turns: [] }, practice: [] } };
  },
  cur() { return this.all[this.currentId]; },
  sorted() { return Object.values(this.all).sort((a, b) => (b.updated || "").localeCompare(a.updated || "")); },
  toGlobals() { const c = this.cur(); S = c.data.state; VIEW = c.data.view || { turns: [] }; practice = c.data.practice || []; },
  fromGlobals() { const c = this.cur(); if (!c) return; c.data = { state: S, view: VIEW, practice }; },
  autoTitle(c) {
    const st = c.data?.state; const f = st?.case?.facts || {};
    if (f.summary && String(f.summary).length > 6) return String(f.summary).slice(0, 60);
    const firstUser = st?.messages?.find(m => m.role === "user")?.content || "";
    return firstUser ? firstUser.slice(0, 48) + (firstUser.length > 48 ? "…" : "") : "";
  },
  touch(meta = true) {
    const c = this.cur(); if (!c) return;
    this.fromGlobals();
    if (meta) c.updated = new Date().toISOString();
    if (!c.titleManual) c.title = this.autoTitle(c) || c.title;
    this.saveLocal();
    renderCaseList();
    if (window.HAQ_CLOUD?.user) { clearTimeout(this._t); this._t = setTimeout(() => window.HAQ_CLOUD.pushCase(c), 1200); }
  },
  saveLocal() { store.set("haq_cases", this.all); store.set("haq_current", this.currentId); },
  create() {
    this.fromGlobals();
    const empty = Object.values(this.all).find(c => !c.data?.state?.messages?.length && !c.evidence?.length);
    const c = empty || this.blank();
    this.all[c.id] = c; this.currentId = c.id;
    this.toGlobals(); this.saveLocal();
    resetPanels(); renderAll(); renderCaseList(); closeDrawers();
  },
  switchTo(id) {
    if (!this.all[id] || id === this.currentId) { closeDrawers(); return; }
    this.fromGlobals(); this.currentId = id; this.toGlobals(); this.saveLocal();
    resetPanels(); renderAll(); renderCaseList(); closeDrawers();
  },
  async remove(id) {
    const c = this.all[id]; if (!c) return;
    for (const e of c.evidence || []) await EvDB.del(e.id).catch(() => {});
    if (window.HAQ_CLOUD?.user) await window.HAQ_CLOUD.deleteCase(c).catch(() => {});
    delete this.all[id];
    if (this.currentId === id) { this.currentId = this.sorted()[0]?.id || null; if (!this.currentId) { const b = this.blank(); this.all[b.id] = b; this.currentId = b.id; } this.toGlobals(); resetPanels(); renderAll(); }
    this.saveLocal(); renderCaseList();
  },
  rename(id, title) { const c = this.all[id]; if (!c) return; c.title = title.slice(0, 80); c.titleManual = true; c.updated = new Date().toISOString(); this.saveLocal(); renderCaseList(); if (window.HAQ_CLOUD?.user) window.HAQ_CLOUD.pushCase(c); },
};
function persist() { Cases.touch(); }
function resetPanels() { $("#docOut").innerHTML = ""; $("#practiceFeedback").innerHTML = ""; renderTracker(); renderEvidence(); }
function closeDrawers() { $("#side")?.classList.remove("open"); }

/* ---------------- sidebar: My cases */
function renderCaseList() {
  const box = $("#caseList"); if (!box) return;
  const q = ($("#caseSearch")?.value || "").toLowerCase();
  const items = Cases.sorted().filter(c => c.data?.state?.messages?.length || c.evidence?.length || c.id === Cases.currentId)
    .filter(c => !q || (c.title || "").toLowerCase().includes(q));
  box.innerHTML = items.map(c => {
    const cat = c.data?.state?.case?.category || "other";
    const title = c.title || tr("untitled");
    const d = new Date(c.updated || c.created).toLocaleDateString("en-IN", { day: "numeric", month: "short" });
    return `<div class="case-item ${c.id === Cases.currentId ? "active" : ""}" data-id="${c.id}" tabindex="0" role="button">
      <span class="ci-emoji">${CAT_EMOJI[cat] || "💬"}</span>
      <span class="ci-main"><b>${esc(title)}</b><small><span class="st st-${c.status}">${esc(statusText(c.status))}</span> · ${d}</small></span>
      <span class="ci-actions"><button class="ci-btn" data-act="rename" title="${esc(tr("rename"))}">✎</button><button class="ci-btn" data-act="delete" title="${esc(tr("delete"))}">🗑</button></span></div>`;
  }).join("") || `<div class="muted small" style="padding:8px">${esc(tr("no_cases"))}</div>`;
  box.querySelectorAll(".case-item").forEach(el => {
    el.onclick = e => {
      const act = e.target.closest(".ci-btn")?.dataset.act, id = el.dataset.id;
      if (act === "rename") { const t = prompt(tr("rename"), Cases.all[id].title || ""); if (t != null && t.trim()) Cases.rename(id, t.trim()); }
      else if (act === "delete") { if (confirm(tr("confirm_delete"))) Cases.remove(id); }
      else Cases.switchTo(id);
    };
    el.onkeydown = e => { if (e.key === "Enter") Cases.switchTo(el.dataset.id); };
  });
}

/* ---------------- tracker: status + checklist */
function renderTracker() {
  const box = $("#tracker"); if (!box) return;
  const c = Cases.cur(); const cat = S?.case?.category;
  const steps = (CONFIG?.case_steps || {})[cat] || [];
  if (!c || (!steps.length && !(c.custom || []).length)) { box.classList.add("hidden"); return; }
  box.classList.remove("hidden");
  const statuses = CONFIG?.case_statuses || ["new"];
  $("#statusSteps").innerHTML = statuses.map((s, i) => `<button class="st-step ${s === c.status ? "on" : ""} ${statuses.indexOf(c.status) > i ? "done" : ""}" data-s="${s}">${esc(statusText(s))}</button>`).join("");
  $("#statusSteps").querySelectorAll("button").forEach(b => b.onclick = () => { c.status = b.dataset.s; persist(); renderTracker(); });
  const useHi = ["hi"].includes(uiLang());
  const all = steps.map(s => ({ id: s.id, label: useHi ? s.hi : s.en, done: !!c.checks?.[s.id] })).concat((c.custom || []).map(s => ({ id: s.id, label: s.label, done: !!s.done, custom: true })));
  const done = all.filter(s => s.done).length;
  $("#checkFill").style.width = (all.length ? Math.round(100 * done / all.length) : 0) + "%";
  $("#checkLabel").textContent = `${done}/${all.length} ${tr("steps_done")}`;
  $("#checklist").innerHTML = all.map(s => `<li class="${s.done ? "done" : ""}"><label><input type="checkbox" data-id="${s.id}" ${s.custom ? 'data-custom="1"' : ""} ${s.done ? "checked" : ""}> <span>${esc(s.label)}</span></label>${s.custom ? `<button class="ci-btn" data-del="${s.id}" title="${esc(tr("delete"))}">✕</button>` : ""}</li>`).join("");
  $("#checklist").querySelectorAll("input").forEach(i => i.onchange = () => {
    if (i.dataset.custom) { const s = c.custom.find(x => x.id === i.dataset.id); if (s) s.done = i.checked; }
    else { c.checks = c.checks || {}; c.checks[i.dataset.id] = i.checked; }
    persist(); renderTracker();
  });
  $("#checklist").querySelectorAll("[data-del]").forEach(b => b.onclick = () => { c.custom = c.custom.filter(x => x.id !== b.dataset.del); persist(); renderTracker(); });
}
document.addEventListener("DOMContentLoaded", () => {
  $("#addStep")?.addEventListener("submit", e => {
    e.preventDefault(); const v = $("#addStepInput").value.trim(); if (!v) return;
    const c = Cases.cur(); c.custom = c.custom || []; c.custom.push({ id: uid(), label: v, done: false });
    $("#addStepInput").value = ""; persist(); renderTracker();
  });
  $("#caseSearch")?.addEventListener("input", renderCaseList);
  $("#newCase2")?.addEventListener("click", () => Cases.create());
  $("#toggleSide")?.addEventListener("click", () => $("#side").classList.toggle("open"));
});

/* ---------------- calendar reminders (.ics, works without an account) */
function icsDate(iso) { return iso.replace(/-/g, ""); }
function icsEscape(s) { return String(s || "").replace(/\\/g, "\\\\").replace(/;/g, "\\;").replace(/,/g, "\\,").replace(/\n/g, "\\n"); }
function makeIcs(deadlines) {
  const stamp = new Date().toISOString().replace(/[-:]/g, "").replace(/\.\d+Z$/, "Z");
  const ev = deadlines.map(d => {
    const end = new Date(d.date + "T00:00:00"); end.setDate(end.getDate() + 1);
    const endIso = end.toISOString().slice(0, 10);
    const alarms = [7, 1].filter(n => d.days_left > n).map(n => `BEGIN:VALARM\r\nTRIGGER:-P${n}D\r\nACTION:DISPLAY\r\nDESCRIPTION:${icsEscape("Haq: " + d.label)}\r\nEND:VALARM`).join("\r\n");
    return ["BEGIN:VEVENT", `UID:${uid()}@haq`, `DTSTAMP:${stamp}`, `DTSTART;VALUE=DATE:${icsDate(d.date)}`, `DTEND;VALUE=DATE:${icsDate(endIso)}`,
      `SUMMARY:${icsEscape("⚖️ Haq deadline: " + d.label)}`,
      `DESCRIPTION:${icsEscape((d.note || "") + "\nCalculated by Haq from the dates you gave (legal information, not legal advice). Please verify with a lawyer or NALSA 15100.")}`,
      alarms, "END:VEVENT"].filter(Boolean).join("\r\n");
  }).join("\r\n");
  return `BEGIN:VCALENDAR\r\nVERSION:2.0\r\nPRODID:-//Haq//Legal deadlines//EN\r\nCALSCALE:GREGORIAN\r\n${ev}\r\nEND:VCALENDAR\r\n`;
}
function downloadIcs(deadlines, name = "haq-deadlines.ics") {
  const a = document.createElement("a");
  a.href = URL.createObjectURL(new Blob([makeIcs(deadlines)], { type: "text/calendar" }));
  a.download = name; a.click();
}
function userDeadlines() {
  const calc = VIEW.turns.at(-1)?.calculated || { deadlines: [] };
  return (calc.deadlines || []).filter(d => d.user_deadline !== false && d.days_left >= 0);
}

/* ---------------- evidence locker */
function fmtSize(n) { return n > 1e6 ? (n / 1e6).toFixed(1) + " MB" : Math.max(1, Math.round(n / 1e3)) + " KB"; }
async function addEvidenceFiles(files) {
  const c = Cases.cur();
  for (const f of files) {
    if (f.size > 8e6) { alert(`${f.name}: ${tr("too_big")}`); continue; }
    const e = { id: uid(), name: f.name, type: f.type || "", size: f.size, added: new Date().toISOString(), extract: null, applied: false };
    try { await EvDB.put(e.id, f); } catch (err) { alert("Could not save the file on this device: " + err); continue; }
    c.evidence = c.evidence || []; c.evidence.unshift(e);
    if (window.HAQ_CLOUD?.user) window.HAQ_CLOUD.uploadEvidence(c, e, f).catch(() => {});
  }
  persist(); renderEvidence();
}
async function evidenceBlob(c, e) {
  let b = await EvDB.get(e.id);
  if (!b && window.HAQ_CLOUD?.user) { b = await window.HAQ_CLOUD.downloadEvidence(c, e).catch(() => null); if (b) await EvDB.put(e.id, b).catch(() => {}); }
  return b;
}
async function renderEvidence() {
  const box = $("#evList"); if (!box) return;
  const c = Cases.cur(); const list = c?.evidence || [];
  $("#evCount").textContent = list.length ? `(${list.length})` : "";
  if (!list.length) { box.innerHTML = `<div class="empty">${esc(tr("ev_empty"))}</div>`; return; }
  box.innerHTML = list.map(e => `<div class="ev-item" data-id="${e.id}">
      <div class="ev-thumb" data-thumb="${e.id}">${e.type.startsWith("image/") ? "" : "📄"}</div>
      <div class="ev-main"><b>${esc(e.name)}</b><small class="muted">${fmtSize(e.size)} · ${new Date(e.added).toLocaleDateString("en-IN")}</small>
        <div class="ev-btns">
          <button class="ghost small" data-act="read">${e.extract ? "🔁 " : "🔎 "}${esc(tr("ev_read"))}</button>
          <button class="ghost small" data-act="open">👁 ${esc(tr("ev_open"))}</button>
          <button class="ghost small" data-act="del">🗑</button>
        </div>
        <div class="ev-extract">${e.extract ? extractHtml(e) : ""}</div></div></div>`).join("");
  for (const e of list) {
    if (!e.type.startsWith("image/")) continue;
    evidenceBlob(c, e).then(b => { const t = box.querySelector(`[data-thumb="${e.id}"]`); if (b && t) t.innerHTML = `<img alt="" src="${URL.createObjectURL(b)}">`; });
  }
  box.querySelectorAll(".ev-item").forEach(el => {
    const e = list.find(x => x.id === el.dataset.id);
    el.querySelector("[data-act=read]").onclick = () => readEvidence(c, e, el);
    el.querySelector("[data-act=open]").onclick = async () => { const b = await evidenceBlob(c, e); if (b) open(URL.createObjectURL(b), "_blank"); else alert(tr("ev_missing")); };
    el.querySelector("[data-act=del]").onclick = async () => { if (!confirm(tr("confirm_delete"))) return; await EvDB.del(e.id); if (window.HAQ_CLOUD?.user) window.HAQ_CLOUD.deleteEvidence(c, e).catch(() => {}); c.evidence = c.evidence.filter(x => x.id !== e.id); persist(); renderEvidence(); };
    const ap = el.querySelector("[data-act=apply]"); if (ap) ap.onclick = () => applyEvidence(c, e, el);
  });
}
function extractHtml(e) {
  const x = e.extract;
  if (x.error) return `<div class="small bad-text">⚠️ ${esc(x.error)}</div>`;
  const facts = Object.entries(x.facts_update || {}).filter(([, v]) => v !== null && v !== "");
  const rows = [
    ...(x.dates || []).map((d, i) => `<label><input type="checkbox" data-kind="date" data-i="${i}" ${e.applied ? "disabled" : "checked"}> 📅 ${esc(fmtDate(d.date))}: ${esc(d.what)}</label>`),
    ...(x.amounts || []).map((a, i) => `<label class="muted">💰 ${esc(inrFmt(a.amount))}: ${esc(a.what)}</label>`),
    ...facts.map(([k, v], i) => `<label><input type="checkbox" data-kind="fact" data-k="${esc(k)}" ${e.applied ? "disabled" : "checked"}> 🗂 ${esc(FACT_LABELS[k] || humanize(k))}: <b>${esc(fmtFact(k, v))}</b></label>`),
  ].join("");
  return `<div class="ev-card"><div><span class="pill">${esc(x.doc_type || "document")}</span></div>
    <p class="small">${esc(x.summary || "")}</p>
    ${(x.proves || []).length ? `<div class="small"><b>${esc(tr("ev_proves"))}:</b> ${x.proves.map(esc).join("; ")}</div>` : ""}
    <div class="ev-rows small">${rows}</div>
    ${e.applied ? `<div class="small ok-text">✓ ${esc(tr("ev_applied"))}</div>` : `<button class="primary small" data-act="apply">＋ ${esc(tr("ev_apply"))}</button>`}
    <div class="tiny muted">${esc(tr("ev_ai_note"))}</div></div>`;
}
async function readEvidence(c, e, el) {
  const b = await evidenceBlob(c, e); if (!b) { alert(tr("ev_missing")); return; }
  el.querySelector(".ev-extract").innerHTML = `<div class="small muted">${esc(tr("ev_reading"))} <span class="typing"><i></i><i></i><i></i></span></div>`;
  const fd = new FormData();
  fd.append("file", b, e.name); fd.append("category", S?.case?.category || ""); fd.append("language", langInfo()[2] || S?.case?.language || "English");
  if (provider()) fd.append("provider", provider());
  const r = await api("/api/evidence", fd, true);
  e.extract = r; e.applied = false; persist(); renderEvidence();
}
function ensureState() {
  if (!S) S = { version: 1, messages: [], case: { category: null, language: null, script: null, facts: {}, timeline: [], evidence_have: [], evidence_missing: [], next_step: null }, flags: { level: "none", reasons: [] }, log: [] };
  return S;
}
function applyEvidence(c, e, el) {
  const x = e.extract; if (!x || x.error) return;
  ensureState(); const cs = S.case;
  el.querySelectorAll("input[type=checkbox]:checked").forEach(i => {
    if (i.dataset.kind === "date") { const d = x.dates[+i.dataset.i]; if (d && !cs.timeline.some(t => t.date === d.date && t.event === d.what)) cs.timeline.push({ date: d.date, event: d.what + " (from " + e.name + ")" }); }
    if (i.dataset.kind === "fact") { cs.facts[i.dataset.k] = x.facts_update[i.dataset.k]; }
  });
  cs.timeline.sort((a, b) => (a.date || "9").localeCompare(b.date || "9"));
  const have = `${x.doc_type || "Document"}: ${e.name}`;
  if (!cs.evidence_have.includes(have)) cs.evidence_have.push(have);
  e.applied = true; persist(); renderEvidence(); renderCase(VIEW.turns.at(-1));
}
document.addEventListener("DOMContentLoaded", () => {
  const dz = $("#dropzone"), fi = $("#evFile");
  if (!dz) return;
  fi.onchange = () => { addEvidenceFiles([...fi.files]); fi.value = ""; };
  ["dragover", "dragenter"].forEach(ev => dz.addEventListener(ev, e => { e.preventDefault(); dz.classList.add("drag"); }));
  ["dragleave", "drop"].forEach(ev => dz.addEventListener(ev, e => { e.preventDefault(); dz.classList.remove("drag"); }));
  dz.addEventListener("drop", e => addEvidenceFiles([...e.dataTransfer.files]));
});

/* ---------------- value formatting for the case file */
function humanize(k) { const s = String(k).replace(/_/g, " ").trim(); return s.charAt(0).toUpperCase() + s.slice(1); }
function inrFmt(n) { const x = Number(String(n).replace(/[^\d.]/g, "")); return isFinite(x) && x > 0 ? "₹" + x.toLocaleString("en-IN") : String(n); }
function fmtFact(k, v) {
  if (v === true || v === "true") return tr("yes");
  if (v === false || v === "false") return tr("no");
  if (/amount|deposit|rent|salary|due|paid|cheque_amount/.test(k) && /^\s*[\d,.]+\s*$/.test(String(v))) return inrFmt(v);
  if (/date|day$/.test(k) && /^\d{4}-\d{2}-\d{2}$/.test(String(v))) return fmtDate(v);
  return String(v);
}
