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

/* ---------------- i18n (page text; the AI replies in the chosen language separately) */
const LANGS = window.HAQ_LANGS, STR = window.HAQ_I18N;
function uiLang() { return ($("#lang") && $("#lang").value) || "en"; }
function tr(k) { const L = STR[uiLang()] || {}; return L[k] ?? STR.en[k] ?? k; }
function langInfo() { return LANGS.find(l => l[0] === uiLang()) || LANGS[0]; }
function applyI18n() {
  document.documentElement.lang = uiLang() === "hinglish" ? "hi" : uiLang();
  $$("[data-i18n]").forEach(el => { el.textContent = tr(el.dataset.i18n); });
  $$("[data-i18n-ph]").forEach(el => { el.placeholder = tr(el.dataset.i18nPh); });
  if (innerWidth <= 600) $("#input").placeholder = tr("ph_short");  // long example wraps on phones
  $$("[data-i18n-title]").forEach(el => { el.title = tr(el.dataset.i18nTitle); el.setAttribute("aria-label", tr(el.dataset.i18nTitle)); });
  renderCards();
  const name = langInfo()[2];
  if (name && [...$("#docLang").options].some(o => o.value === name || o.textContent === name)) $("#docLang").value = name;
  try { renderCase(VIEW.turns[VIEW.turns.length - 1]); } catch (e) {}
}
function renderCards() {
  const box = $("#cards"); if (!box) return;
  box.innerHTML = "";
  window.HAQ_CARDS.forEach(([id, emoji, isNotice]) => {
    const [title, sub, prompt] = tr("c_" + id);
    const b = document.createElement("button");
    b.type = "button";
    b.className = "card" + (id === "upi_fraud" || id === "cheque" ? " urgent" : "");
    b.dataset.card = id;
    if (!isNotice) b.dataset.prompt = prompt;
    b.innerHTML = `<span class="emoji">${emoji}</span><b>${esc(title)}</b><small>${esc(sub)}</small>`;
    b.onclick = () => { if (isNotice) { $("#noticeDlg").showModal(); return; } $("#input").value = prompt; autosize(); $("#input").focus(); };
    box.appendChild(b);
  });
}
/* ---------------- theme (light default) */
function setTheme(th) {
  document.documentElement.dataset.theme = th;
  try { localStorage.setItem("haq_theme", th); } catch (e) {}
  $("#themeBtn").innerHTML = th === "dark" ? '<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>' : '<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg>';
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
    if ((m = l.match(/^\*\*([^*]{2,60}?)[:：]\*\*\s*(.*)$/) || l.match(/^\*\*([^*]{2,60}?)\*\*[:：]\s*(.*)$/))) { close(); html += `<h4>${inline(m[1])}</h4>`; if (m[2]) html += `<p>${inline(m[2])}</p>`; continue; }
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
  if (t.doc) {  // intro text (in the bubble) -> the document -> the questions for its blanks
    box.appendChild(docCard(t.doc));
    if (t.ask) { const a = document.createElement("div"); a.className = "doc-ask"; a.innerHTML = md(t.ask); box.appendChild(a); }
    return box;
  }
  const meta = document.createElement("div");
  meta.className = "meta";
  (t.citations || []).forEach(c => {
    const s = document.createElement("span");
    s.className = "chip law";
    s.textContent = `§ ${c.act.replace(/,\s*\d{4}$/, "")}${secLabel(c.section)}`;
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
    if (a.type === "draft" && CONFIG?.doc_types?.[a.doc]) { btn.textContent = "Draft: " + shortDoc(a.doc); btn.onclick = () => draftDoc(a.doc); }
    else if (a.type === "practice") { btn.textContent = "Practise the conversation"; btn.onclick = () => { openTab("practice"); startPractice(); }; }
    else if (a.type === "get_help") { btn.textContent = "Free legal help"; btn.onclick = () => openTab("help"); }
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
// "69" -> "s.69"; "Schedule, Article 55" -> "Art. 55"; "Order XXXVII" -> "Order XXXVII"; "Rule 4(5)" -> "r.4(5)"
function secLabel(s) {
  s = String(s || "").trim();
  if (!s) return "";
  let m;
  if ((m = s.match(/article\s*(\S+)/i))) return " Art. " + m[1];
  if ((m = s.match(/^rules?\s*(.+)/i))) return " r." + m[1];
  if (/^order/i.test(s)) return " " + s;
  return /^\d/.test(s) ? " s." + s : " " + s;
}

function showCite(e, c) {
  const p = $("#cite-pop");
  p.innerHTML = `<b>${esc(c.act)}${c.section ? " ·" + esc(secLabel(c.section)) : ""}</b><br><span class="muted small">${esc(c.title)}</span><p>${esc(c.plain)}</p>
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
  if (!S || !S.messages.length) { $("#welcome").classList.remove("hidden"); renderCase(null); renderDocPanel(null); return; }
  let ti = 0;
  S.messages.forEach(m => {
    if (m.role === "user") addMsg("user", esc(m.content));
    else { const t = VIEW.turns[ti++] || { reply: m.content }; addMsg("bot", md(t.doc && t.intro != null ? t.intro : m.content), renderBotExtras(t)); }
  });
  renderCase(VIEW.turns[VIEW.turns.length - 1]);
  renderDocPanel([...VIEW.turns].reverse().find(t => t.doc)?.doc);
}

/* ---------------- send */
async function send(text) {
  text = (text || "").trim();
  if (!text || busy) return;
  busy = true; $("#send").disabled = true;
  const langPref = langInfo()[2] || "English";  // reply in the interface language the user picked, whatever they type in
  addMsg("user", esc(text));
  $("#input").value = ""; autosize();
  const tb = typing();
  if (await tryFillDoc(text, tb)) { busy = false; $("#send").disabled = false; return; }
  const res = await api("/api/chat", { state: S, message: text, provider: provider(), lang_pref: langPref });
  tb.parentElement.remove();
  busy = false; $("#send").disabled = false;
  if (res.error) { addMsg("bot", `<p>⚠️ ${esc(res.error)}</p><p class="small muted">Try again, or switch the model (⚙︎ at the top).</p>`); return; }
  S = res.state;
  VIEW.turns.push({ reply: res.reply, citations: res.citations, guard: res.guard, actions: res.actions, model: res.model, latency_s: res.latency_s, calculated: res.calculated, completeness: res.completeness, needs_lawyer: res.needs_lawyer, emergency_contacts: res.emergency_contacts });
  persist();
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
  if (!has) { $("#deadlines").innerHTML = `<div class="empty">${esc(tr("dead_empty"))}</div>`; $("#derived").innerHTML = ""; $("#calAll").classList.add("hidden"); try { renderTracker(); } catch (e) {} return; }
  $("#catPill").textContent = CAT_LABEL[c.category] || c.category || "-";
  $("#langPill").textContent = c.language ? `🗣 ${c.language}` : "";
  const comp = t?.completeness || { pct: 0, missing: [] };
  $("#meter").style.width = comp.pct + "%";
  $("#meterLabel").textContent = comp.missing?.length ? `Case file ${comp.pct}% complete · still need: ${comp.missing.slice(0, 3).map(m => m.question.replace(/\?.*/, "")).join("; ")}` : (comp.pct ? "Case file complete ✓" : "");
  $("#facts").innerHTML = Object.entries(c.facts || {}).filter(([k]) => k !== "summary").map(([k, v]) => `<dt>${esc(FACT_LABELS[k] || humanize(k))}</dt><dd>${esc(fmtFact(k, v))}</dd>`).join("") || `<dd class="muted">-</dd>`;
  $("#timeline").innerHTML = (c.timeline || []).map(e => `<li><span class="d">${esc(/^\d{4}-\d{2}-\d{2}$/.test(e.date) ? fmtDate(e.date) : e.date)}</span>${esc(e.event)}</li>`).join("") || `<li class="muted">-</li>`;
  $("#evidence").innerHTML = (c.evidence_have || []).map(e => `<li>✅ ${esc(/_/.test(e) && !/\s/.test(e) ? humanize(e) : e)}</li>`).join("") + (c.evidence_missing || []).map(e => `<li>⬜ <span class="muted">${esc(tr("get"))}:</span> ${esc(/_/.test(e) && !/\s/.test(e) ? humanize(e) : e)}</li>`).join("") || `<li class="muted">-</li>`;
  $("#nextStep").classList.toggle("hidden", !c.next_step);
  $("#nextStep").innerHTML = `<b>Next step:</b> ${esc(c.next_step || "")}`;
  // deadlines
  const calc = t?.calculated || { deadlines: [], derived: [] };
  const kbById = Object.fromEntries((window.KB || []).map(e => [e.id, e]));
  const basis = b => b && kbById[b] ? `<a href="${esc(kbById[b].source_url)}" target="_blank" rel="noopener">${esc(kbById[b].act)}${esc(secLabel(kbById[b].section))}</a>` : (b ? esc(b) : "as stated in the notice");
  $("#deadlines").innerHTML = calc.deadlines.length ? calc.deadlines.map((d, i) => `<div class="deadline ${d.status}">
      <div class="lbl">${esc(d.label)}</div>
      <div class="when">${fmtDate(d.date)} <span class="badge ${d.status}">${d.days_left < 0 ? `passed ${-d.days_left}d ago` : `${d.days_left} days left`}</span></div>
      <div class="small muted">Basis: ${basis(d.basis)}${d.note ? " · " + esc(d.note) : ""}</div>
      ${d.user_deadline !== false && d.days_left >= 0 ? `<button class="ghost small cal-btn" data-i="${i}">${esc(tr("add_cal"))}</button>` : (d.user_deadline === false ? `<div class="tiny muted">${esc(tr("their_deadline"))}</div>` : "")}</div>`).join("")
    : `<div class="empty">${esc(tr("dead_empty"))}</div>`;
  $$("#deadlines .cal-btn").forEach(b => b.onclick = () => downloadIcs([calc.deadlines[+b.dataset.i]], "haq-deadline.ics"));
  $("#calAll").classList.toggle("hidden", !userDeadlines().length);
  try { renderTracker(); window.renderReminderToggle && window.renderReminderToggle(); } catch (e) {}
  $("#derived").innerHTML = calc.derived.map(d => `<div class="deadline"><div class="lbl">${esc(d.label)}</div><div class="when">${esc(d.value)}</div><div class="small muted">Basis: ${basis(d.basis)}${d.note ? " · " + esc(d.note) : ""}</div></div>`).join("");
}
function fmtDate(iso) { try { return new Date(iso + "T00:00:00").toLocaleDateString("en-IN", { day: "numeric", month: "short", year: "numeric" }); } catch { return iso; } }

function renderBanner(t) {
  const b = $("#banner");
  const f = S?.flags || { level: "none" };
  if (!f || f.level === "none") { b.className = "banner hidden"; return; }
  const rs = (f.reasons || []).slice(-3);
  // dismissed notes stay closed until the level or the reasons change; emergency help can't be dismissed
  const sig = f.level + "|" + rs.join("|");
  if (f.level !== "emergency" && bannerDismissed().includes(sig)) { b.className = "banner hidden"; return; }
  b.className = `banner ${f.level}`;
  const reasons = rs.map(esc).join(" · ");
  const icon = `<svg class="bn-ic" viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3v18M7 21h10M5 7h14M5 7l-3 7a3 3 0 0 0 6 0L5 7zM19 7l-3 7a3 3 0 0 0 6 0l-3-7z"/></svg>`;
  const close = f.level === "emergency" ? "" : `<button class="bn-x" type="button" aria-label="Close" title="Close">×</button>`;
  let title, body;
  if (f.level === "emergency") { title = "If you are in danger or thinking of harming yourself"; body = `Call <a href="tel:112">112</a> (emergency) or <a href="tel:14416">14416</a> (Tele-MANAS, free 24×7). You are not alone.${reasons ? `<br><small>${reasons}</small>` : ""}`; }
  else if (f.level === "urgent") { title = "Talk to a lawyer soon"; body = `${reasons}. Free legal aid: <a href="tel:15100">15100</a> (NALSA) or your District Legal Services Authority.`; }
  else { title = "A lawyer's review is recommended"; body = `${reasons}. Free legal aid: <a href="tel:15100">15100</a>.`; }
  b.innerHTML = `${icon}<div class="bn-txt"><div class="bn-t">${title}</div><div class="bn-b">${body}</div></div>${close}`;
  const x = b.querySelector(".bn-x");
  if (x) x.onclick = () => {
    const d = bannerDismissed().filter(s => s !== sig).concat(sig).slice(-50);
    try { localStorage.setItem("haq_banner_x", JSON.stringify(d)); } catch (e) {}
    b.className = "banner hidden";
  };
}
function bannerDismissed() { try { return JSON.parse(localStorage.getItem("haq_banner_x") || "[]"); } catch (e) { return []; } }

/* ---------------- documents */
function renderDocButtons() {
  const cat = S?.case?.category;
  const list = (CONFIG?.doc_types_by_category?.[cat]) || [];
  $("#docButtons").innerHTML = list.length ? "" : `<div class="empty">${esc(tr("docs_empty"))}</div>`;
  list.forEach(d => {
    const b = document.createElement("button"); b.className = "ghost"; b.textContent = shortDoc(d);
    b.onclick = () => draftDoc(d); $("#docButtons").appendChild(b);
  });
}
/* Drafts live in the chat (a document card + the questions for its blanks) and are mirrored
   in the Documents panel. Replies to those questions fill the blanks (/api/draft/fill). */
const FILL_RX = /\[\[FILL:?\s*([^\]]*)\]\]/g;
function docBlanks(body) {
  const out = [];
  for (const m of String(body || "").matchAll(FILL_RX)) { const l = (m[1] || "").trim() || "missing detail"; if (!out.some(x => x.toLowerCase() === l.toLowerCase())) out.push(l); }
  return out;
}
const cap = s => s.charAt(0).toUpperCase() + s.slice(1);
function docAsk(blanks) { return blanks.map((b, i) => `${i + 1}. ${cap(b)}`).join("\n"); }
function docPaperHtml(body) { return md(body).replace(/\[\[FILL:?\s*([^\]]*)\]\]/g, (_, l) => `<mark class="fill">${l.trim() || "…"}</mark>`); }
async function docDownload(doc) {
  const r = await fetch("/api/docx", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ title: doc.title, body_markdown: doc.body }) });
  const blob = await r.blob(); const a = document.createElement("a"); a.href = URL.createObjectURL(blob); a.download = doc.title.replace(/[^\w\- ]/g, "").slice(0, 60) + ".docx"; a.click();
}
function docPrint(doc) { const w = open("", "_blank"); w.document.write(`<html><head><title>${esc(doc.title)}</title><style>body{font-family:Georgia,serif;max-width:720px;margin:40px auto;line-height:1.6;white-space:pre-wrap}</style></head><body>${esc(doc.body)}</body></html>`); w.document.close(); w.print(); }
const ICON_DOC = `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5M9 13h6M9 17h6"/></svg>`;

function docCard(doc) {
  const n = docBlanks(doc.body).length;
  const card = document.createElement("div");
  card.className = "doc-card";
  card.innerHTML = `<div class="doc-card-h">${ICON_DOC}<b>${esc(doc.title)}</b><span class="doc-state ${n ? "" : "ok"}">${n ? esc(tr("doc_blanks_left").replace("{n}", n)) : esc(tr("doc_ready_send"))}</span></div>
    <div class="doc-paper clipped">${docPaperHtml(doc.body)}</div>
    <button class="doc-more link-btn" type="button">${esc(tr("doc_show_full"))}</button>
    <div class="doc-card-a"><button class="ghost small" data-a="word">Word</button><button class="ghost small" data-a="pdf">Print / PDF</button><button class="ghost small" data-a="copy">${esc(tr("doc_copy"))}</button><button class="ghost small" data-a="open">${esc(tr("doc_open"))}</button></div>`;
  const paper = card.querySelector(".doc-paper"), more = card.querySelector(".doc-more");
  more.onclick = () => { paper.classList.toggle("clipped"); more.textContent = tr(paper.classList.contains("clipped") ? "doc_show_full" : "doc_show_less"); };
  card.querySelector("[data-a=word]").onclick = () => docDownload(doc);
  card.querySelector("[data-a=pdf]").onclick = () => docPrint(doc);
  card.querySelector("[data-a=copy]").onclick = e => { navigator.clipboard?.writeText(doc.body); e.target.textContent = "✓"; };
  card.querySelector("[data-a=open]").onclick = () => { renderDocPanel(doc); openTab("docs"); if (innerWidth <= 900) { $("#side").classList.add("open"); } };
  return card;
}

function renderDocPanel(doc) {
  const out = $("#docOut");
  if (!doc) { out.innerHTML = ""; return; }
  const g = doc.guard?.initial || {}, n = docBlanks(doc.body).length;
  out.innerHTML = `<div class="docbox">
    <div class="doc-head"><b>${esc(doc.title)}</b><span>
      <button class="ghost small" id="dlDocx">Word</button>
      <button class="ghost small" id="cpDoc">${esc(tr("doc_copy"))}</button>
      <button class="ghost small" id="prDoc">Print / PDF</button></span></div>
    <textarea id="docText">${esc(doc.body)}</textarea>
    <div class="doc-foot">${n ? esc(tr("doc_blanks_left").replace("{n}", n)) + ": " + esc(tr("doc_answer_in_chat")) + " " : ""}${g.violations?.length ? `${g.violations.length} unverified reference(s) removed. ` : "References checked. "}${esc(doc.disclaimer || "")}</div>
  </div>
  ${doc.send_instructions?.length ? `<h3>How to send it</h3><ol class="small">${doc.send_instructions.map(s => `<li>${esc(s)}</li>`).join("")}</ol>` : ""}
  <div class="meta">${(doc.citations || []).map(c => `<a class="chip law" href="${esc(c.source_url)}" target="_blank" rel="noopener">§ ${esc(c.act.replace(/,\s*\d{4}$/, ""))}${esc(secLabel(c.section))}</a>`).join("")}${doc.model ? `<span class="chip model">${esc(doc.model.provider)}/${esc((doc.model.model || "").split("/").pop())}</span>` : ""}</div>`;
  $("#docText").oninput = e => { doc.body = e.target.value; clearTimeout(renderDocPanel.t); renderDocPanel.t = setTimeout(persist, 600); };
  $("#dlDocx").onclick = () => docDownload(doc);
  $("#cpDoc").onclick = () => navigator.clipboard?.writeText(doc.body);
  $("#prDoc").onclick = () => docPrint(doc);
}

function pushDocTurn(doc, [intro, ask]) {
  const last = VIEW.turns[VIEW.turns.length - 1] || {};
  const text = intro + (ask ? "\n\n" + ask : "");  // the model sees both in the history
  const t = { reply: text, intro, ask, doc, calculated: last.calculated, completeness: last.completeness, needs_lawyer: last.needs_lawyer };
  S.messages.push({ role: "assistant", content: text });
  VIEW.turns.push(t);
  persist();
  addMsg("bot", md(intro), renderBotExtras(t));
  renderDocPanel(doc);
}
// -> [text above the document, questions below it]
function docMessage(doc, updated) {
  const b = docBlanks(doc.body);
  if (!b.length) return [(updated ? tr("doc_updated") + " " : "") + tr("doc_complete"), ""];
  return [updated ? tr("doc_updated") : tr("doc_ready").replace("{doc}", doc.title),
          (updated ? tr("doc_still") : tr("doc_need")) + "\n\n" + docAsk(b) + "\n\n" + tr("doc_reply_hint")];
}
// the latest draft that still has blanks, if it is among the last few replies
function pendingDoc() {
  for (let i = VIEW.turns.length - 1; i >= Math.max(0, VIEW.turns.length - 3); i--) {
    const d = VIEW.turns[i]?.doc;
    if (d) return docBlanks(d.body).length ? d : null;
  }
  return null;
}

async function draftDoc(docType) {
  if (!S || busy) return;
  if (innerWidth <= 900) $("#side").classList.remove("open");
  busy = true; $("#send").disabled = true;
  const tb = typing();
  tb.insertAdjacentHTML("beforeend", ` <span class="muted small">${esc(tr("doc_drafting").replace("{doc}", shortDoc(docType)))}</span>`);
  $("#docOut").innerHTML = `<div class="empty">${esc(tr("doc_drafting").replace("{doc}", shortDoc(docType)))} <span class="typing"><i></i><i></i><i></i></span></div>`;
  const res = await api("/api/draft", { state: S, doc_type: docType, doc_language: $("#docLang").value, provider: provider() });
  tb.parentElement.remove();
  busy = false; $("#send").disabled = false;
  if (res.error) { addMsg("bot", `<p>⚠️ ${esc(res.error)}</p>`); $("#docOut").innerHTML = `<div class="empty">⚠️ ${esc(res.error)}</div>`; return; }
  const doc = { type: docType, title: res.title, body: res.body_markdown, citations: res.citations, send_instructions: res.send_instructions, guard: res.guard, model: res.model, disclaimer: res.disclaimer };
  pushDocTurn(doc, docMessage(doc, false));
  $("#input").focus();
}

// a chat reply to the draft's questions fills its blanks; returns true if it did
async function tryFillDoc(text, tb) {
  const pd = pendingDoc();
  if (!pd) return false;
  const f = await api("/api/draft/fill", { body_markdown: pd.body, answer: text, provider: provider() });
  if (f.error || !f.filled || !Object.keys(f.filled).length) return false;
  tb.parentElement.remove();
  S.messages.push({ role: "user", content: text });
  const doc = Object.assign({}, pd, { body: f.body_markdown });
  pushDocTurn(doc, docMessage(doc, true));
  return true;
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
  practice.push({ role: "other", content: r.reply }); persist(); renderPractice();
}
$("#practiceForm").onsubmit = async e => {
  e.preventDefault();
  const v = $("#practiceInput").value.trim(); if (!v) return;
  if (!practice.length) await startPractice();
  practice.push({ role: "user", content: v }); $("#practiceInput").value = ""; renderPractice();
  const r = await api("/api/practice", { case: S.case, history: practice, provider: provider() });
  practice.push({ role: "other", content: r.error ? "⚠️ " + r.error : r.reply }); persist(); renderPractice();
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
$("#attach").onclick = () => $("#noticeDlg").showModal();
$("#noticeGo").onclick = async e => {
  e.preventDefault();
  const fd = new FormData();
  fd.append("text", $("#noticeText").value);
  fd.append("language", langInfo()[2] || "English");  // interface language decides the reply language
  const SCRIPT_OF = { Hindi: "Devanagari", Marathi: "Devanagari", Bengali: "Bengali", Tamil: "Tamil", Telugu: "Telugu", Kannada: "Kannada", Malayalam: "Malayalam", Gujarati: "Gujarati", Punjabi: "Gurmukhi", Odia: "Odia", Urdu: "Arabic" };
  fd.append("script", SCRIPT_OF[langInfo()[2]] || "Latin");
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
  persist();
  renderCase(VIEW.turns.at(-1));
};

/* ---------------- voice: server Whisper first, browser speech recognition as fallback */
let rec = null, chunks = [], recognizer = null;
function langCode() { return ["en", "hinglish"].includes(uiLang()) ? "" : langInfo()[3].split("-")[0]; }  // "" = Whisper auto-detects
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
  recognizer.lang = langInfo()[3];
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
  u.lang = uiLang() === "en" ? (map[sc] || "en-IN") : langInfo()[3];
  const voice = speechSynthesis.getVoices().find(v => v.lang === u.lang); if (voice) u.voice = voice;
  speechSynthesis.speak(u);
}

/* ---------------- misc wiring */
function autosize() { const t = $("#input"); t.style.height = "auto"; t.style.height = Math.min(t.scrollHeight, 160) + "px"; }
$("#input").addEventListener("input", autosize);
$("#input").addEventListener("keydown", e => { if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); send($("#input").value); } });
$("#composer").onsubmit = e => { e.preventDefault(); send($("#input").value); };
function openTab(name) {
  $$(".tab").forEach(t => t.classList.toggle("active", t.dataset.tab === name));
  $$(".panel").forEach(p => p.classList.toggle("active", p.id === "p-" + name));
  $("#secCase") && ($("#secCase").open = true);
  window.openSide && window.openSide();
  if (name === "practice") renderPractice();
  if (name === "evidence") renderEvidence();
}
$$(".tab").forEach(t => t.onclick = () => openTab(t.dataset.tab));

$("#newCase") && ($("#newCase").onclick = () => Cases.create());
$("#calAll").onclick = () => downloadIcs(userDeadlines());
$("#lang").onchange = () => { store.set("haq_lang", $("#lang").value); applyI18n(); };
$("#themeBtn").onclick = () => setTheme(document.documentElement.dataset.theme === "dark" ? "light" : "dark");
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
  $("#kbList").innerHTML = (window.KB || []).map(e => `<div><b>${esc(e.act)}${e.section ? " ·" + esc(secLabel(e.section)) : ""}</b>: ${esc(e.title)} <a href="${esc(e.source_url)}" target="_blank" rel="noopener">source↗</a></div>`).join("");
}

window.addEventListener("DOMContentLoaded", async function init() {
  $("#lang").innerHTML = LANGS.map(([c, n]) => `<option value="${c}">${n}</option>`).join("");
  const legacy = { auto: "en", "en-IN": "en", "hi-IN": "hi", "pa-IN": "pa", "bn-IN": "bn", "mr-IN": "mr", "gu-IN": "gu", "ta-IN": "ta", "te-IN": "te", "kn-IN": "kn", "ml-IN": "ml" };
  let sl = store.get("haq_lang", "en"); sl = legacy[sl] || sl; if (!STR[sl]) sl = "en"; $("#lang").value = sl;
  setTheme(document.documentElement.dataset.theme === "dark" ? "dark" : "light");
  applyI18n();
  try { CONFIG = await (await fetch("/api/config")).json(); } catch { CONFIG = { providers: [] }; }
  try { window.KB = await (await fetch("/api/kb")).json(); } catch { window.KB = []; }
  const ps = $("#provider");
  ps.innerHTML = (CONFIG.providers || []).map(p => `<option value="${esc(p.name)}">${esc(p.name)} · ${esc(p.main_model.split("/").pop())}</option>`).join("") || `<option value="">no model configured</option>`;
  const sp = store.get("haq_provider", CONFIG.primary); if ([...ps.options].some(o => o.value === sp)) ps.value = sp;
  Cases.load(); renderHelp(); renderAll(); renderCaseList(); renderEvidence();
  if (window.initAuth) window.initAuth(CONFIG.supabase);
  $("#pfClose") && ($("#pfClose").onclick = () => $("#profileDlg").close());
});
