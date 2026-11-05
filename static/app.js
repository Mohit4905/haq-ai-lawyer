/* Haq front-end: vanilla JS, no build step. State lives in the browser; the API is stateless. */
const $ = (s, el = document) => el.querySelector(s);
const $$ = (s, el = document) => [...el.querySelectorAll(s)];
const store = {
  get(k, d) { try { const v = localStorage.getItem(k); return v ? JSON.parse(v) : d; } catch { return d; } },
  set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch {} },
  del(k) { try { localStorage.removeItem(k); } catch {} },
};

let S = store.get("haq_state", null);          // engine state (messages + case)
let VIEW = store.get("haq_view", { turns: [] }); // rendered extras per assistant turn
let CONFIG = null;
let practice = store.get("haq_practice", []);
let busy = false;

/* ---------------- i18n (UI chrome only; the AI replies in any language) */
const I18N = {
  hi: {
    tagline: "रोज़मर्रा की कानूनी समस्याओं में मुफ़्त मदद, आपकी भाषा में",
    new_case: "नया केस", welcome_h: "क्या समस्या है? अपने शब्दों में बताइए।",
    welcome_p: "किसी भी भारतीय भाषा में लिखें या बोलें। मैं समझाऊँगा कि आप कहाँ खड़े हैं, आपके पास क्या रास्ते हैं, और ज़रूरी नोटिस या पत्र तैयार करूँगा, मुफ़्त।",
    c1: "डिपॉज़िट वापस नहीं मिला", c1s: "मकान मालिक / PG पैसा नहीं लौटा रहा", c2: "रिफ़ंड / ख़राब सामान", c2s: "ऑनलाइन ऑर्डर, सर्विस, वारंटी",
    c3: "सैलरी नहीं मिली", c3s: "बकाया वेतन, फ़ुल एंड फ़ाइनल", c4: "चेक बाउंस", c4s: "समय-सीमा सख़्त है, जल्दी करें", c5: "मुझे लीगल नोटिस मिला", c5s: "टेक्स्ट पेस्ट करें या फ़ोटो डालें",
    trust: "हक़ जो भी क़ानून बताता है, वह पहले एक जाँची हुई लाइब्रेरी से मिलाया जाता है। हक़ वकील नहीं है; ज़रूरत हो तो बताता है कि वकील से मिलें।",
    ph: "यहाँ लिखें… जैसे 'मकान मालिक 40,000 का डिपॉज़िट वापस नहीं कर रहा'",
    foot: "हक़ कानूनी जानकारी देता है, कानूनी सलाह नहीं। मुफ़्त कानूनी सहायता: NALSA हेल्पलाइन 15100।",
    t_case: "केस फ़ाइल", t_dead: "समय-सीमा", t_docs: "दस्तावेज़", t_prac: "अभ्यास", t_help: "मदद",
    case_empty: "बात करते-करते आपकी केस फ़ाइल अपने आप बनती है: क्या हुआ, कब, कितना पैसा, और क्या सबूत हैं।",
    h_facts: "मुख्य तथ्य", h_timeline: "घटनाक्रम", h_evidence: "सबूत",
    dead_note: "ये तारीख़ें कोड से गिनी गई हैं (AI से नहीं), हर एक के साथ उसका क़ानून। फिर भी जाँच लें।",
    dead_empty: "तारीख़ें बताइए (जैसे घर कब खाली किया, चेक कब बाउंस हुआ), समय-सीमा यहाँ दिखेगी।",
    docs_note: "हक़ आपकी केस फ़ाइल से दस्तावेज़ बनाता है। जो जानकारी नहीं है वह [[FILL]] से चिह्नित होती है, गढ़ी नहीं जाती।",
    prac_note: "असली बातचीत से पहले अभ्यास करें। हक़ दूसरी तरफ़ का किरदार निभाएगा; अंत में फ़ीडबैक मिलेगा।",
    prac_start: "अभ्यास शुरू करें", prac_end: "ख़त्म करें और फ़ीडबैक लें",
  },
};
function uiLang() { const v = $("#lang").value; return v === "hi-IN" || v === "mr-IN" ? "hi" : "en"; }
const EN_DEFAULTS = {};
function applyI18n() {
  const L = I18N[uiLang()] || {};
  $$("[data-i18n]").forEach(el => {
    const k = el.dataset.i18n;
    if (!(k in EN_DEFAULTS)) EN_DEFAULTS[k] = el.textContent;
    el.textContent = L[k] || EN_DEFAULTS[k];
  });
  const ta = $("#input");
  if (!("ph" in EN_DEFAULTS)) EN_DEFAULTS.ph = ta.placeholder;
  ta.placeholder = L.ph || EN_DEFAULTS.ph;
}

/* ---------------- tiny safe markdown */
function esc(s) { return String(s ?? "").replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c])); }
function inline(s) {
  return esc(s)
    .replace(/\[\[(FILL:?[^\]]*)\]\]/g, '<span class="fill">[[$1]]</span>')
    .replace(/\*\*(.+?)\*\*/g, "<b>$1</b>")
    .replace(/(^|[^*])\*(?!\s)(.+?)\*(?!\*)/g, "$1<i>$2</i>")
    .replace(/_(.+?)_/g, "<i>$1</i>")
    .replace(/\[([^\]]+)\]\((https?:\/\/[^)\s]+)\)/g, '<a href="$2" target="_blank" rel="noopener">$1</a>');
}
function md(text) {
  const lines = String(text || "").split(/\r?\n/);
  let html = "", list = null;
  const close = () => { if (list) { html += `</${list}>`; list = null; } };
  for (const raw of lines) {
    const l = raw.trimEnd();
    let m;
    if (!l.trim()) { close(); continue; }
    if ((m = l.match(/^#{1,4}\s+(.*)/))) { close(); html += `<h4>${inline(m[1])}</h4>`; continue; }
    if ((m = l.match(/^\s*[-*•]\s+(.*)/))) { if (list !== "ul") { close(); html += "<ul>"; list = "ul"; } html += `<li>${inline(m[1])}</li>`; continue; }
    if ((m = l.match(/^\s*\d+[.)]\s+(.*)/))) { if (list !== "ol") { close(); html += "<ol>"; list = "ol"; } html += `<li>${inline(m[1])}</li>`; continue; }
    close(); html += `<p>${inline(l)}</p>`;
  }
  close();
  return html;
}

/* ---------------- API */
async function api(path, body, isForm = false) {
  const r = await fetch(path, isForm ? { method: "POST", body } : { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) });
  let j; try { j = await r.json(); } catch { j = { error: `Server error ${r.status}` }; }
  if (!r.ok && !j.error) j.error = `Server error ${r.status}`;
  return j;
}
function provider() { return $("#provider").value || null; }

/* ---------------- chat rendering */
function addMsg(role, html, extras) {
  $("#welcome")?.classList.add("hidden");
  const wrap = document.createElement("div");
  wrap.className = `msg ${role}`;
  if (role === "bot") wrap.innerHTML = `<div class="avatar">हक़</div>`;
  const b = document.createElement("div");
  b.className = "bubble";
  b.innerHTML = html;
  if (extras) b.appendChild(extras);
  wrap.appendChild(b);
  $("#chat").appendChild(wrap);
  $("#chat").scrollTop = $("#chat").scrollHeight;
  return b;
}
function typing() { return addMsg("bot", '<span class="typing"><i></i><i></i><i></i></span>'); }

function guardChip(g) {
  if (!g) return null;
  const init = g.initial || {};
  const fin = g.final || init;
  const n = (fin.verified || []).length;
  const fixed = (init.violations || []).length;
  const c = document.createElement("span");
  if (fixed) {
    c.className = "chip guard-fix";
    c.textContent = `🛡️ ${fixed} unverified reference${fixed > 1 ? "s" : ""} caught & ${g.stripped ? "removed" : "fixed"}`;
    c.title = (init.violations || []).map(v => `• ${v.text}: ${v.why}`).join("\n");
  } else {
    c.className = "chip guard-ok";
    c.textContent = n ? `🛡️ ${n} legal reference${n > 1 ? "s" : ""} verified` : "🛡️ no unverified law";
    c.title = (fin.verified || []).map(v => `✓ ${v[0]} (${v[1]})`).join("\n") || "No law references in this reply.";
  }
  return c;
}

function renderBotExtras(t) {
  const box = document.createElement("div");
  const meta = document.createElement("div");
  meta.className = "meta";
  (t.citations || []).forEach(c => {
    const s = document.createElement("span");
    s.className = "chip law";
    s.textContent = `§ ${c.act.replace(/,\s*\d{4}$/, "")}${c.section ? " s." + c.section : ""}`;
    s.onclick = e => showCite(e, c);
    meta.appendChild(s);
  });
  const g = guardChip(t.guard); if (g) meta.appendChild(g);
  const sp = document.createElement("span");
  sp.className = "chip"; sp.textContent = "🔊"; sp.title = "Read aloud";
  sp.onclick = () => speak(t.reply);
  meta.appendChild(sp);
  if (t.model) { const m = document.createElement("span"); m.className = "chip model"; m.textContent = `${t.model.provider}/${t.model.model.split("/").pop()} · ${t.latency_s}s`; meta.appendChild(m); }
  box.appendChild(meta);
  const acts = document.createElement("div");
  acts.className = "actions";
  const seen = new Set();
  (t.actions || []).forEach(a => {
    const key = a.type + (a.doc || "");
    if (seen.has(key)) return; seen.add(key);
    const btn = document.createElement("button");
    if (a.type === "draft" && CONFIG?.doc_types?.[a.doc]) { btn.textContent = "📝 Draft: " + shortDoc(a.doc); btn.onclick = () => { openTab("docs"); draftDoc(a.doc); }; }
    else if (a.type === "practice") { btn.textContent = "🎭 Practise the conversation"; btn.onclick = () => { openTab("practice"); startPractice(); }; }
    else if (a.type === "get_help") { btn.textContent = "🤝 Free legal help"; btn.onclick = () => openTab("help"); }
    else return;
    acts.appendChild(btn);
  });
  if (acts.children.length) box.appendChild(acts);
  return box;
}
const DOC_SHORT = {
  deposit_demand_notice: "Deposit refund notice", company_complaint_email: "Complaint email to company", consumer_legal_notice: "Legal notice to company",
  consumer_commission_complaint: "Consumer Commission complaint", salary_demand_notice: "Salary demand notice", labour_authority_complaint: "Complaint to labour office",
  cheque_demand_notice_s138: "Cheque bounce notice (s.138)", reply_to_notice: "Reply to the notice",
};
function shortDoc(d) { return DOC_SHORT[d] || d; }

function showCite(e, c) {
  const p = $("#cite-pop");
  p.innerHTML = `<b>${esc(c.act)}${c.section ? " · Section " + esc(c.section) : ""}</b><br><span class="muted small">${esc(c.title)}</span><p>${esc(c.plain)}</p>
    <a href="${esc(c.source_url)}" target="_blank" rel="noopener">Official source ↗</a> <span class="muted small">(${esc(c.source_type)})</span>`;
  p.classList.remove("hidden");
  const r = e.target.getBoundingClientRect();
  p.style.left = Math.min(r.left, innerWidth - 360) + "px";
  p.style.top = Math.min(r.bottom + 6, innerHeight - p.offsetHeight - 10) + "px";
  e.stopPropagation();
}
document.addEventListener("click", e => { if (!e.target.closest("#cite-pop")) $("#cite-pop").classList.add("hidden"); });

function renderAll() {
  $("#chat").querySelectorAll(".msg").forEach(n => n.remove());
  if (!S || !S.messages.length) { $("#welcome").classList.remove("hidden"); renderCase(null); return; }
  let ti = 0;
  S.messages.forEach(m => {
    if (m.role === "user") addMsg("user", esc(m.content));
    else { const t = VIEW.turns[ti++] || { reply: m.content }; addMsg("bot", md(m.content), renderBotExtras(t)); }
  });
  renderCase(VIEW.turns[VIEW.turns.length - 1]);
}

/* ---------------- send */
async function send(text) {
  text = (text || "").trim();
  if (!text || busy) return;
  busy = true; $("#send").disabled = true;
  const LANG_NAME = { "en-IN": "English", "hi-IN": "Hindi", hinglish: "Hinglish", "bn-IN": "Bengali", "ta-IN": "Tamil", "te-IN": "Telugu", "mr-IN": "Marathi", "gu-IN": "Gujarati", "kn-IN": "Kannada", "ml-IN": "Malayalam", "pa-IN": "Punjabi" };
  const langPref = LANG_NAME[$("#lang").value] || null;
  addMsg("user", esc(text));
  $("#input").value = ""; autosize();
  const tb = typing();
  const res = await api("/api/chat", { state: S, message: text, provider: provider(), lang_pref: langPref });
  tb.parentElement.remove();
  busy = false; $("#send").disabled = false;
  if (res.error) { addMsg("bot", `<p>⚠️ ${esc(res.error)}</p><p class="small muted">Try again, or switch the model (⚙︎ at the top).</p>`); return; }
  S = res.state;
  VIEW.turns.push({ reply: res.reply, citations: res.citations, guard: res.guard, actions: res.actions, model: res.model, latency_s: res.latency_s, calculated: res.calculated, completeness: res.completeness, needs_lawyer: res.needs_lawyer, emergency_contacts: res.emergency_contacts });
  store.set("haq_state", S); store.set("haq_view", VIEW);
  addMsg("bot", md(res.reply), renderBotExtras(res));
  renderCase(VIEW.turns[VIEW.turns.length - 1]);
  if ($("#autoSpeak")?.checked) speak(res.reply);
}

/* ---------------- case panel */
const FACT_LABELS = {
  deposit_amount: "Deposit", monthly_rent: "Monthly rent", written_agreement: "Written agreement", possession_handed_over_date: "Vacated / keys handed", deductions_claimed: "Deductions claimed",
  communications_so_far: "Asked so far", proof_of_payment: "Proof of payment", city_state: "Location", other_party_name: "Other party", product_or_service: "Product / service",
  amount_paid: "Amount paid", purchase_date: "Bought on", problem_date: "Problem since", complained_to_company: "Complained to company", proof: "Proof", role: "Role",
  monthly_salary: "Monthly salary", unpaid_period: "Unpaid period", amount_due: "Amount due", still_employed: "Still employed?", employment_proof: "Employment proof",
  cheque_amount: "Cheque amount", cheque_date: "Cheque date", reason_for_cheque: "Cheque given for", presentation_date: "Deposited on", dishonour_reason: "Bounce reason",
  memo_received_date: "Return memo received", notice_sent_date: "Notice sent", notice_from: "Notice from", notice_date: "Notice dated", received_date: "Received on",
  notice_demands: "They demand", notice_deadline_days: "Deadline in notice", summary: "Summary", user_name: "Your name", last_working_day: "Last working day",
};
const CAT_LABEL = { tenancy: "🏠 Security deposit / tenancy", consumer: "📦 Consumer complaint", salary: "💼 Unpaid salary", cheque_bounce: "🧾 Cheque bounce", notice: "✉️ Legal notice", cyber_fraud: "🚨 Online fraud", out_of_scope: "⚖️ Needs a lawyer", other: "🤔 Understanding your problem" };

function renderCase(t) {
  const c = S?.case;
  const has = c && (c.category || Object.keys(c.facts || {}).length);
  $("#p-case .empty").classList.toggle("hidden", !!has);
  $("#caseBody").classList.toggle("hidden", !has);
  renderBanner(t);
  renderDocButtons();
  if (!has) { $("#deadlines").innerHTML = `<div class="empty">${esc(EN_DEFAULTS.dead_empty || "Share dates and deadlines appear here.")}</div>`; $("#derived").innerHTML = ""; return; }
  $("#catPill").textContent = CAT_LABEL[c.category] || c.category || "-";
  $("#langPill").textContent = c.language ? `🗣 ${c.language}` : "";
  const comp = t?.completeness || { pct: 0, missing: [] };
  $("#meter").style.width = comp.pct + "%";
  $("#meterLabel").textContent = comp.missing?.length ? `Case file ${comp.pct}% complete · still need: ${comp.missing.slice(0, 3).map(m => m.question.replace(/\?.*/, "")).join("; ")}` : (comp.pct ? "Case file complete ✓" : "");
  $("#facts").innerHTML = Object.entries(c.facts || {}).filter(([k]) => k !== "summary").map(([k, v]) => `<dt>${esc(FACT_LABELS[k] || k.replace(/_/g, " "))}</dt><dd>${esc(v)}</dd>`).join("") || `<dd class="muted">-</dd>`;
  $("#timeline").innerHTML = (c.timeline || []).map(e => `<li><span class="d">${esc(e.date)}</span>${esc(e.event)}</li>`).join("") || `<li class="muted">-</li>`;
  $("#evidence").innerHTML = (c.evidence_have || []).map(e => `<li>✅ ${esc(e)}</li>`).join("") + (c.evidence_missing || []).map(e => `<li>⬜ <span class="muted">Get:</span> ${esc(e)}</li>`).join("") || `<li class="muted">-</li>`;
  $("#nextStep").classList.toggle("hidden", !c.next_step);
  $("#nextStep").innerHTML = `<b>Next step:</b> ${esc(c.next_step || "")}`;
  // deadlines
  const calc = t?.calculated || { deadlines: [], derived: [] };
  const kbById = Object.fromEntries((window.KB || []).map(e => [e.id, e]));
  const basis = b => b && kbById[b] ? `<a href="${esc(kbById[b].source_url)}" target="_blank" rel="noopener">${esc(kbById[b].act)}${kbById[b].section ? " s." + esc(kbById[b].section) : ""}</a>` : (b ? esc(b) : "as stated in the notice");
  $("#deadlines").innerHTML = calc.deadlines.length ? calc.deadlines.map(d => `<div class="deadline ${d.status}">
      <div class="lbl">${esc(d.label)}</div>
      <div class="when">${fmtDate(d.date)} <span class="badge ${d.status}">${d.days_left < 0 ? `passed ${-d.days_left}d ago` : `${d.days_left} days left`}</span></div>
      <div class="small muted">Basis: ${basis(d.basis)}${d.note ? " · " + esc(d.note) : ""}</div></div>`).join("")
    : `<div class="empty">${esc(EN_DEFAULTS.dead_empty || "Share dates and deadlines appear here.")}</div>`;
  $("#derived").innerHTML = calc.derived.map(d => `<div class="deadline"><div class="lbl">${esc(d.label)}</div><div class="when">${esc(d.value)}</div><div class="small muted">Basis: ${basis(d.basis)}${d.note ? " · " + esc(d.note) : ""}</div></div>`).join("");
}
function fmtDate(iso) { try { return new Date(iso + "T00:00:00").toLocaleDateString("en-IN", { day: "numeric", month: "short", year: "numeric" }); } catch { return iso; } }

function renderBanner(t) {
  const b = $("#banner");
  const f = S?.flags || { level: "none" };
  if (!f || f.level === "none") { b.className = "banner hidden"; return; }
  b.className = `banner ${f.level}`;
  const reasons = (f.reasons || []).slice(-3).map(esc).join(" · ");
  if (f.level === "emergency") b.innerHTML = `🚨 If you are in danger or thinking of harming yourself, call <a href="tel:112">112</a> (emergency) or <a href="tel:14416">14416</a> (Tele-MANAS, free 24×7). You are not alone. <br><small>${reasons}</small>`;
  else if (f.level === "urgent") b.innerHTML = `⚖️ <b>Please talk to a lawyer soon.</b> ${reasons}. Free legal aid: call <a href="tel:15100">15100</a> (NALSA) or visit your District Legal Services Authority.`;
  else b.innerHTML = `💡 A lawyer's review is recommended: ${reasons}. Free legal aid: <a href="tel:15100">15100</a>.`;
}

/* ---------------- documents */
function renderDocButtons() {
  const cat = S?.case?.category;
  const list = (CONFIG?.doc_types_by_category?.[cat]) || [];
  $("#docButtons").innerHTML = list.length ? "" : `<div class="empty">Tell Haq about your problem first. Documents for your type of case will appear here.</div>`;
  list.forEach(d => {
    const b = document.createElement("button"); b.className = "ghost"; b.textContent = "📝 " + shortDoc(d);
    b.onclick = () => draftDoc(d); $("#docButtons").appendChild(b);
  });
}
async function draftDoc(docType) {
  if (!S) return;
  const out = $("#docOut");
  out.innerHTML = `<div class="empty">Drafting ${esc(shortDoc(docType))}… <span class="typing"><i></i><i></i><i></i></span></div>`;
  const res = await api("/api/draft", { state: S, doc_type: docType, doc_language: $("#docLang").value, provider: provider() });
  if (res.error) { out.innerHTML = `<div class="empty">⚠️ ${esc(res.error)}</div>`; return; }
  const g = res.guard?.initial || {};
  out.innerHTML = `<div class="docbox">
    <div class="doc-head"><b>${esc(res.title)}</b><span>
      <button class="ghost small" id="dlDocx">⬇ Word</button>
      <button class="ghost small" id="cpDoc">Copy</button>
      <button class="ghost small" id="prDoc">Print / PDF</button></span></div>
    <textarea id="docText">${esc(res.body_markdown)}</textarea>
    <div class="doc-foot">${res.placeholders?.length ? `✏️ Fill ${res.placeholders.length} gap(s) marked [[FILL]] before sending. ` : ""}${g.violations?.length ? `🛡️ ${g.violations.length} unverified reference(s) removed. ` : "🛡️ References checked. "}${esc(res.disclaimer)}</div>
  </div>
  ${res.send_instructions?.length ? `<h3>How to send it</h3><ol class="small">${res.send_instructions.map(s => `<li>${esc(s)}</li>`).join("")}</ol>` : ""}
  <div class="meta">${(res.citations || []).map(c => `<a class="chip law" href="${esc(c.source_url)}" target="_blank" rel="noopener">§ ${esc(c.act)}${c.section ? " s." + esc(c.section) : ""}</a>`).join("")}<span class="chip model">${esc(res.model?.provider)}/${esc((res.model?.model || "").split("/").pop())}</span></div>`;
  $("#dlDocx").onclick = async () => {
    const r = await fetch("/api/docx", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ title: res.title, body_markdown: $("#docText").value }) });
    const blob = await r.blob(); const a = document.createElement("a"); a.href = URL.createObjectURL(blob); a.download = res.title.replace(/[^\w\- ]/g, "").slice(0, 60) + ".docx"; a.click();
  };
  $("#cpDoc").onclick = () => navigator.clipboard?.writeText($("#docText").value);
  $("#prDoc").onclick = () => { const w = open("", "_blank"); w.document.write(`<html><head><title>${esc(res.title)}</title><style>body{font-family:Georgia,serif;max-width:720px;margin:40px auto;line-height:1.6;white-space:pre-wrap}</style></head><body>${esc($("#docText").value)}</body></html>`); w.document.close(); w.print(); };
}

/* ---------------- practice */
function renderPractice() {
  $("#practiceChat").innerHTML = practice.map(m => `<div class="pmsg ${m.role === "user" ? "user" : "other"}">${esc(m.content)}</div>`).join("") || `<div class="empty">Press "Start practice". Haq will play the ${esc(S?.case?.category === "tenancy" ? "landlord" : S?.case?.category === "salary" ? "employer" : "other side")}.</div>`;
  $("#practiceChat").scrollTop = 1e9;
}
async function startPractice() {
  if (!S?.case?.category) { $("#practiceChat").innerHTML = `<div class="empty">First tell Haq about your problem in the chat.</div>`; return; }
  practice = []; $("#practiceFeedback").innerHTML = ""; renderPractice();
  const r = await api("/api/practice", { case: S.case, history: [], provider: provider() });
  if (r.error) { $("#practiceChat").innerHTML = `<div class="empty">⚠️ ${esc(r.error)}</div>`; return; }
  practice.push({ role: "other", content: r.reply }); store.set("haq_practice", practice); renderPractice();
}
$("#practiceForm").onsubmit = async e => {
  e.preventDefault();
  const v = $("#practiceInput").value.trim(); if (!v) return;
  if (!practice.length) await startPractice();
  practice.push({ role: "user", content: v }); $("#practiceInput").value = ""; renderPractice();
  const r = await api("/api/practice", { case: S.case, history: practice, provider: provider() });
  practice.push({ role: "other", content: r.error ? "⚠️ " + r.error : r.reply }); store.set("haq_practice", practice); renderPractice();
};
$("#practiceStart").onclick = startPractice;
$("#practiceEnd").onclick = async () => {
  if (practice.filter(m => m.role === "user").length < 1) return;
  $("#practiceFeedback").innerHTML = `<div class="empty">Reviewing… <span class="typing"><i></i><i></i><i></i></span></div>`;
  const r = await api("/api/practice", { case: S.case, history: practice, feedback: true, provider: provider() });
  if (r.error) { $("#practiceFeedback").innerHTML = `<div class="empty">⚠️ ${esc(r.error)}</div>`; return; }
  const sc = r.scores || {};
  $("#practiceFeedback").innerHTML = `<h3>Your feedback</h3><p><b>${esc(r.summary || "")}</b></p>` +
    Object.entries(sc).map(([k, v]) => `<div class="score"><span>${esc(k)}</span><span class="bar"><i style="width:${(+v || 0) * 20}%"></i></span><b>${esc(v)}</b></div>`).join("") +
    `<h3>Went well</h3><ul class="small">${(r.went_well || []).map(x => `<li>${esc(x)}</li>`).join("")}</ul>` +
    `<h3>Improve</h3><ul class="small">${(r.improve || []).map(x => `<li>${esc(x)}</li>`).join("")}</ul>` +
    `<h3>Try saying</h3><ul class="small">${(r.better_lines || []).map(x => `<li>“${esc(x)}”</li>`).join("")}</ul>`;
};

/* ---------------- notice explainer */
$("#noticeCard").onclick = () => $("#noticeDlg").showModal();
$("#attach").onclick = () => $("#noticeDlg").showModal();
$("#noticeGo").onclick = async e => {
  e.preventDefault();
  const fd = new FormData();
  fd.append("text", $("#noticeText").value);
  const sel = $("#lang");
  fd.append("language", sel.value === "auto" ? (S?.case?.language || "English") : sel.selectedOptions[0].textContent);
  fd.append("script", S?.case?.script || "Latin");
  if (provider()) fd.append("provider", provider());
  if ($("#noticeFile").files[0]) fd.append("file", $("#noticeFile").files[0]);
  $("#noticeDlg").close();
  addMsg("user", esc($("#noticeText").value ? "📄 " + $("#noticeText").value.slice(0, 300) + ($("#noticeText").value.length > 300 ? "…" : "") : "📄 (uploaded notice)"));
  const tb = typing();
  const r = await api("/api/explain", fd, true);
  tb.parentElement.remove();
  if (r.error) { addMsg("bot", `<p>⚠️ ${esc(r.error)}</p>`); return; }
  const html = `<p><b>${esc(r.notice_kind || "Notice")}</b>: ${esc(r.plain_summary)}</p>
    <div class="notice-card small"><div><b>From:</b> ${esc(r.who_sent)}</div><div><b>They want:</b> ${esc(r.what_they_want)}</div>
    ${r.deadline_in_notice ? `<div><b>Deadline:</b> ${esc(r.deadline_in_notice)}</div>` : ""}
    <div><b>How serious:</b> <span class="risk-${esc(r.risk_level)}">${esc(r.risk_level)}</span>: ${esc(r.risk_reason)}</div></div>
    <h4>Do now</h4><ul>${(r.do_now || []).map(x => `<li>${esc(x)}</li>`).join("")}</ul>
    <h4>Don't</h4><ul>${(r.do_not || []).map(x => `<li>${esc(x)}</li>`).join("")}</ul>
    ${(r.laws_mentioned_in_notice || []).length ? `<p class="small muted">Laws the notice mentions (as written, not verified by Haq): ${r.laws_mentioned_in_notice.map(esc).join("; ")}</p>` : ""}
    ${r.needs_lawyer?.level && r.needs_lawyer.level !== "none" ? `<p><b>⚖️ Lawyer: ${esc(r.needs_lawyer.level)}</b>: ${esc(r.needs_lawyer.reason)}</p>` : ""}
    <p class="small">Want me to help you reply? Tell me your side of the story in the chat.</p>`;
  addMsg("bot", html);
  // seed the conversation so the chat continues with context
  S = S || { version: 1, messages: [], case: { category: null, facts: {}, timeline: [], evidence_have: [], evidence_missing: [] }, flags: { level: "none", reasons: [] }, log: [] };
  S.case.category = r.category && r.category !== "other" ? "notice" : "notice";
  Object.assign(S.case.facts, { notice_from: r.who_sent, notice_demands: r.what_they_want, notice_deadline_days: r.deadline_in_notice || "", summary: r.plain_summary });
  S.messages.push({ role: "user", content: "I received this notice:\n" + ($("#noticeText").value || r.extracted_text || "").slice(0, 3000) });
  S.messages.push({ role: "assistant", content: `Explanation: ${r.plain_summary} They want: ${r.what_they_want}. Risk: ${r.risk_level}.` });
  VIEW.turns.push({ reply: r.plain_summary, citations: [], guard: { initial: r.guard, final: r.guard }, actions: [{ type: "draft", doc: "reply_to_notice" }], model: r.model, latency_s: r.model?.latency_s });
  if (r.needs_lawyer?.level === "urgent") S.flags = { level: "urgent", reasons: [r.needs_lawyer.reason] };
  store.set("haq_state", S); store.set("haq_view", VIEW);
  renderCase(VIEW.turns.at(-1));
};

/* ---------------- voice: server Whisper first, browser speech recognition as fallback */
let rec = null, chunks = [], recognizer = null;
function langCode() { const v = $("#lang").value; return v === "auto" || v === "hinglish" ? "" : v.split("-")[0]; }
$("#mic").onclick = async () => {
  if (rec && rec.state === "recording") { rec.stop(); return; }
  if (recognizer) { recognizer.stop(); return; }
  if (CONFIG?.stt && navigator.mediaDevices?.getUserMedia) {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      rec = new MediaRecorder(stream); chunks = [];
      rec.ondataavailable = e => chunks.push(e.data);
      rec.onstop = async () => {
        $("#mic").classList.remove("rec"); stream.getTracks().forEach(t => t.stop());
        const fd = new FormData(); fd.append("audio", new Blob(chunks, { type: rec.mimeType || "audio/webm" }), "voice.webm"); fd.append("language", langCode());
        $("#input").value = "🎙️ …";
        const r = await api("/api/transcribe", fd, true);
        $("#input").value = r.text || ""; autosize();
        if (r.error) { browserSTT(); return; }
        if (r.text) send(r.text);
      };
      rec.start(); $("#mic").classList.add("rec");
      return;
    } catch (e) { /* fall through */ }
  }
  browserSTT();
};
function browserSTT() {
  const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SR) { alert("Voice input needs Chrome/Edge, or a server speech key."); return; }
  recognizer = new SR();
  const v = $("#lang").value; recognizer.lang = v === "auto" || v === "hinglish" ? "hi-IN" : v;
  recognizer.interimResults = true;
  recognizer.onresult = e => { $("#input").value = [...e.results].map(r => r[0].transcript).join(" "); autosize(); };
  recognizer.onend = () => { $("#mic").classList.remove("rec"); recognizer = null; if ($("#input").value.trim()) send($("#input").value); };
  recognizer.start(); $("#mic").classList.add("rec");
}
function speak(text) {
  if (!window.speechSynthesis) return;
  speechSynthesis.cancel();
  const u = new SpeechSynthesisUtterance(String(text).replace(/[*_#>`\[\]]/g, ""));
  const sc = S?.case?.script || "";
  const map = { Devanagari: "hi-IN", Tamil: "ta-IN", Bengali: "bn-IN", Telugu: "te-IN", Kannada: "kn-IN", Gujarati: "gu-IN", Malayalam: "ml-IN", Gurmukhi: "pa-IN" };
  u.lang = $("#lang").value.includes("-") ? $("#lang").value : (map[sc] || "en-IN");
  const voice = speechSynthesis.getVoices().find(v => v.lang === u.lang); if (voice) u.voice = voice;
  speechSynthesis.speak(u);
}

/* ---------------- misc wiring */
function autosize() { const t = $("#input"); t.style.height = "auto"; t.style.height = Math.min(t.scrollHeight, 160) + "px"; }
$("#input").addEventListener("input", autosize);
$("#input").addEventListener("keydown", e => { if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); send($("#input").value); } });
$("#composer").onsubmit = e => { e.preventDefault(); send($("#input").value); };
$$(".card[data-prompt]").forEach(c => c.onclick = () => { $("#input").value = c.dataset.prompt; autosize(); $("#input").focus(); });
function openTab(name) {
  $$(".tab").forEach(t => t.classList.toggle("active", t.dataset.tab === name));
  $$(".panel").forEach(p => p.classList.toggle("active", p.id === "p-" + name));
  if (innerWidth <= 900) $("#caseCol").classList.add("open");
  if (name === "practice") renderPractice();
}
$$(".tab").forEach(t => t.onclick = () => openTab(t.dataset.tab));
$("#toggleCase").onclick = () => $("#caseCol").classList.toggle("open");
$("#newCase").onclick = () => { if (S?.messages?.length && !confirm("Start a new case? This clears the current conversation on this device.")) return; S = null; VIEW = { turns: [] }; practice = []; ["haq_state", "haq_view", "haq_practice"].forEach(store.del); $("#docOut").innerHTML = ""; $("#practiceFeedback").innerHTML = ""; renderAll(); };
$("#lang").onchange = () => { store.set("haq_lang", $("#lang").value); applyI18n(); };
$("#provider").onchange = () => store.set("haq_provider", $("#provider").value);
$("#exportCase").onclick = () => {
  const c = S.case, calc = VIEW.turns.at(-1)?.calculated || { deadlines: [] };
  const txt = `HAQ CASE SUMMARY (generated ${new Date().toLocaleString("en-IN")})\nType: ${CAT_LABEL[c.category] || c.category}\n\nFACTS\n` +
    Object.entries(c.facts).map(([k, v]) => `- ${FACT_LABELS[k] || k}: ${v}`).join("\n") +
    `\n\nTIMELINE\n` + c.timeline.map(e => `- ${e.date}: ${e.event}`).join("\n") +
    `\n\nPROOF I HAVE\n` + c.evidence_have.map(e => `- ${e}`).join("\n") + `\n\nPROOF TO GET\n` + c.evidence_missing.map(e => `- ${e}`).join("\n") +
    `\n\nDEADLINES (calculated, please verify)\n` + calc.deadlines.map(d => `- ${d.label}: ${d.date}`).join("\n") +
    `\n\nThis summary was prepared with Haq, an AI legal-information tool. It is not legal advice.\n`;
  const a = document.createElement("a"); a.href = URL.createObjectURL(new Blob([txt], { type: "text/plain" })); a.download = "haq-case-summary.txt"; a.click();
};

const HELP = [
  ["Free legal aid (women, children, SC/ST, workers, persons with disability, low income & more)", "NALSA helpline 15100 · nalsa.gov.in", "https://nalsa.gov.in"],
  ["Free advice from a panel lawyer by video/phone", "Tele-Law at your nearest Common Service Centre", "https://www.tele-law.in/faq"],
  ["National Consumer Helpline (free, before going to the Commission)", "1915 / 1800-11-4000 · WhatsApp 8800001915", "https://consumerhelpline.gov.in"],
  ["File a consumer complaint online", "e-Jagriti (replaced e-Daakhil in Jan 2025)", "https://e-jagriti.gov.in"],
  ["Online / UPI fraud: report immediately", "1930 · cybercrime.gov.in", "https://cybercrime.gov.in"],
  ["Bank, UPI, card complaints (complain to the bank first; then within 90 days)", "RBI Ombudsman · cms.rbi.org.in · 14448", "https://cms.rbi.org.in"],
  ["Mental health support (free, 24×7)", "Tele-MANAS 14416", "tel:14416"],
  ["Emergency", "112", "tel:112"],
];
function renderHelp() {
  $("#helpList").innerHTML = (window.HELP_OVERRIDE || HELP).map(([a, b, u]) => `<li><b>${esc(a)}</b><br><a href="${esc(u)}" target="_blank" rel="noopener">${esc(b)}</a></li>`).join("");
  $("#kbList").innerHTML = (window.KB || []).map(e => `<div><b>${esc(e.act)}${e.section ? " · s." + esc(e.section) : ""}</b>: ${esc(e.title)} <a href="${esc(e.source_url)}" target="_blank" rel="noopener">source↗</a></div>`).join("");
}

(async function init() {
  const sl = store.get("haq_lang", "auto"); $("#lang").value = sl; applyI18n();
  try { CONFIG = await (await fetch("/api/config")).json(); } catch { CONFIG = { providers: [] }; }
  try { window.KB = await (await fetch("/api/kb")).json(); } catch { window.KB = []; }
  const ps = $("#provider");
  ps.innerHTML = (CONFIG.providers || []).map(p => `<option value="${esc(p.name)}">${esc(p.name)} · ${esc(p.main_model.split("/").pop())}</option>`).join("") || `<option value="">no model configured</option>`;
  const sp = store.get("haq_provider", CONFIG.primary); if ([...ps.options].some(o => o.value === sp)) ps.value = sp;
  renderHelp(); renderAll();
})();
