/* Court case tracking (eCourtsIndia).
   Case status, hearings and orders appear in the main chat as a court card; "Explain" on an
   order adds a plain-language summary of that order to the chat. */
let COURT = { ecourts: false };
const COURT_SCRIPT = { Hindi: "Devanagari", Marathi: "Devanagari", Bengali: "Bengali", Tamil: "Tamil", Telugu: "Telugu", Kannada: "Kannada", Malayalam: "Malayalam", Gujarati: "Gujarati", Punjabi: "Gurmukhi", Odia: "Odia", Urdu: "Arabic" };
const CNR_FIND = /\b([A-Za-z]{4})[\s\-]?(\d{2})[\s\-]?(\d{6})[\s\-]?(\d{4})\b/;
const ICON_COURT = `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M3 21h18M5 21v-9M9.5 21v-9M14.5 21v-9M19 21v-9M2.5 9.5L12 4l9.5 5.5z"/></svg>`;

function courtErr(code) {
  const m = {
    not_configured: "court_err_off", not_found: "court_err_404", bad_cnr: "court_err_cnr", no_credits: "court_err_credits",
    bad_key: "court_err_key", rate_limited: "court_err_busy", timeout: "court_err_busy", unreachable: "court_err_down",
    unavailable: "court_err_down", no_text: "court_err_notext", too_many: "court_err_limit",
  };
  return tr(m[code] || "court_err_down");
}
function courtIso(s) {
  s = String(s || "").trim(); let m;
  if ((m = s.match(/^(\d{4})-(\d{2})-(\d{2})/))) return `${m[1]}-${m[2]}-${m[3]}`;
  if ((m = s.match(/^(\d{2})[-/.](\d{2})[-/.](\d{4})/))) return `${m[3]}-${m[2]}-${m[1]}`;
  return null;
}
function courtDate(s) { const iso = courtIso(s); return iso ? fmtDate(iso) : (s || "-"); }
function ensureS() {
  if (!S) S = { version: 1, messages: [], case: { category: null, language: null, script: null, facts: {}, timeline: [], evidence_have: [], evidence_missing: [], next_step: null }, flags: { level: "none", reasons: [] }, log: [] };
}
function replyLang() { const l = langInfo()[2] || "English"; return [l, COURT_SCRIPT[l] || "Latin"]; }

function pushCourtTurn(userText, t) {
  ensureS();
  if (userText) pushMsg({ role: "user", content: userText });
  const last = VIEW.turns[VIEW.turns.length - 1] || {};
  const m = pushMsg({ role: "assistant", content: t.reply });
  t = Object.assign({ calculated: last.calculated, completeness: last.completeness, needs_lawyer: last.needs_lawyer }, t, { mid: m.id });
  VIEW.turns.push(t);
  persist();
  addMsg("bot", md(t.intro), renderBotExtras(t), m);
}

// text the chat model sees about the case (keeps follow-up questions grounded)
function courtSummaryText(c) {
  const o = (c.orders || []).slice(0, 3).map(o => `${courtDate(o.date)}: ${o.label}`).join("; ");
  return `Court record (eCourts) for CNR ${c.cnr}: ${c.title}. Status: ${c.status || "-"}${c.disposal ? " (" + c.disposal + ")" : ""}. Court: ${c.court || "-"}. ` +
    `Next hearing: ${courtDate(c.next_hearing)}. Purpose/stage: ${c.purpose || "-"}. Judge: ${(c.judges || []).join(", ") || "-"}. Decision date: ${courtDate(c.decision_date)}. Recent orders: ${o || "none listed"}.`;
}

async function trackCase(cnr, userText, fresh = false) {
  if (busy) return;
  if (innerWidth <= 900) $("#side").classList.remove("open");
  window.showChat && window.showChat();  // the case card appears in the chat
  busy = true; $("#send").disabled = true;
  if (userText) addMsg("user", esc(userText));
  const tb = typing();
  const c = await api("/api/court/case", { cnr, fresh });
  tb.parentElement.remove(); busy = false; $("#send").disabled = false;
  if (c.error) {
    ensureS(); if (userText) pushMsg({ role: "user", content: userText });
    const msg = courtErr(c.error), prev = lastCaseTurn() || {};
    const m = pushMsg({ role: "assistant", content: msg }); VIEW.turns.push({ mid: m.id, reply: msg, calculated: prev.calculated, completeness: prev.completeness }); persist();
    addMsg("bot", `<p>${esc(msg)}</p>`, null, m); return;
  }
  const intro = tr(fresh ? "court_refreshed" : "court_intro").replace("{cnr}", c.cnr);
  pushCourtTurn(userText, { court: c, intro, reply: intro + "\n\n" + courtSummaryText(c) });
}

function courtCard(c) {
  const el = document.createElement("div");
  el.className = "court-card";
  const disposed = /dispos/i.test(c.status || "");
  const nextIso = courtIso(c.next_hearing);
  const row = (k, v) => v ? `<dt>${esc(tr(k))}</dt><dd>${v}</dd>` : "";
  const people = (a, adv) => esc((a || []).join(", ")) + (adv?.length ? `<br><span class="muted small">${esc(tr("court_adv"))}: ${esc(adv.join(", "))}</span>` : "");
  el.innerHTML = `<div class="cc-h">${ICON_COURT}<b>${esc(c.title)}</b><span class="cc-status ${disposed ? "done" : ""}">${esc(c.status || "-")}</span></div>
    <div class="cc-next">${disposed
      ? `<span class="muted small">${esc(tr("court_decided"))}</span><b>${esc(courtDate(c.decision_date))}</b>${c.disposal ? `<span class="small">${esc(c.disposal)}</span>` : ""}`
      : `<span class="muted small">${esc(tr("court_next"))}</span><b>${esc(courtDate(c.next_hearing))}</b>${c.purpose ? `<span class="small">${esc(c.purpose)}</span>` : ""}${nextIso ? `<button class="ghost small cc-cal" type="button">${esc(tr("court_cal"))}</button>` : ""}`}</div>
    <dl class="cc-grid">
      ${row("court_court", esc(c.court) + (c.court_no ? ` · ${esc(tr("court_no"))} ${esc(c.court_no)}` : ""))}
      ${row("court_judge", esc((c.judges || []).join(", ")))}
      ${row("court_case", esc([c.case_type, c.registration?.number || c.case_number].filter(Boolean).join(" ")) + `<br><span class="muted small">CNR ${esc(c.cnr)}</span>`)}
      ${row("court_filed", esc([c.filing?.number ? tr("court_filing_no") + " " + c.filing.number : "", courtDate(c.filing?.date)].filter(x => x && x !== "-").join(" · ")))}
      ${row("court_pet", people(c.petitioners, c.petitioner_advocates))}
      ${row("court_res", people(c.respondents, c.respondent_advocates))}
      ${row("court_acts", esc(c.acts || ""))}
      ${disposed ? "" : row("court_last", esc(courtDate(c.last_hearing)))}
    </dl>
    ${c.orders?.length ? `<div class="cc-sub">${esc(tr("court_orders"))} (${c.orders.length})</div><div class="cc-orders">${c.orders.slice(0, 12).map((o, i) => `
      <div class="cc-order"><span class="cc-od">${esc(courtDate(o.date))}</span><span class="cc-ol">${o.kind === "judgment" ? `<b>${esc(o.label)}</b>` : esc(o.label)}</span><button class="ghost small" type="button" data-i="${i}">${esc(tr("court_explain"))}</button></div>`).join("")}</div>` : `<p class="small muted cc-empty">${esc(tr("court_no_orders"))}</p>`}
    ${c.hearings?.length ? `<details class="cc-hist"><summary class="small">${esc(tr("court_hist"))} (${c.hearings.length})</summary><ol>${c.hearings.map(h => `<li><span class="cc-od">${esc(courtDate(h.date))}</span> ${esc(h.purpose || "")}${h.judge ? ` <span class="muted small">· ${esc(h.judge)}</span>` : ""}</li>`).join("")}</ol></details>` : ""}
    <div class="cc-foot"><span>${esc(tr("court_source"))}${c.fetched_at ? ` · ${esc(c.fetched_at)}` : ""}</span><button class="link-btn inline cc-refresh" type="button">${esc(tr("court_refresh"))}</button></div>`;
  el.querySelectorAll(".cc-order button").forEach(b => b.onclick = () => explainOrder(c, c.orders[+b.dataset.i]));
  el.querySelector(".cc-refresh").onclick = () => trackCase(c.cnr, null, true);
  const cal = el.querySelector(".cc-cal");
  if (cal) cal.onclick = () => {
    const days = Math.round((new Date(nextIso + "T00:00:00") - new Date().setHours(0, 0, 0, 0)) / 864e5);
    downloadIcs([{ label: `Court hearing: ${c.title}`, date: nextIso, days_left: days, note: `${c.court || ""} · CNR ${c.cnr}${c.purpose ? " · " + c.purpose : ""}` }], "haq-hearing.ics");
  };
  return el;
}

async function explainOrder(c, o) {
  if (busy || !o) return;
  window.showChat && window.showChat();
  busy = true; $("#send").disabled = true;
  const userText = tr("court_explain_q").replace("{label}", o.label).replace("{date}", courtDate(o.date));
  addMsg("user", esc(userText));
  const tb = typing();
  tb.insertAdjacentHTML("beforeend", ` <span class="muted small">${esc(tr("court_reading"))}</span>`);
  const [language, script] = replyLang();
  const r = await api("/api/court/order", { cnr: c.cnr, file: o.file, case: { title: c.title, court: c.court }, language, script, provider: provider() });
  tb.parentElement.remove(); busy = false; $("#send").disabled = false;
  if (r.error && !r.markdown) {
    ensureS(); pushMsg({ role: "user", content: userText });
    const msg = /^[a-z_]+$/.test(r.error) ? courtErr(r.error) : "⚠️ " + r.error;
    const prev = lastCaseTurn() || {};
    const m = pushMsg({ role: "assistant", content: msg }); VIEW.turns.push({ mid: m.id, reply: msg, calculated: prev.calculated, completeness: prev.completeness }); persist(); addMsg("bot", `<p>${esc(msg)}</p>`, null, m); return;
  }
  const summary = r.summary || tr("court_no_summary");
  pushCourtTurn(userText, { order: { cnr: c.cnr, label: o.label, date: o.date, text: r.markdown || "" }, intro: summary, reply: `Summary of the court order (${o.label}, ${courtDate(o.date)}) in CNR ${c.cnr}:\n${summary}`, model: r.model });
}

function orderExtras(t) {
  const box = document.createElement("div");
  box.className = "order-extra";
  box.innerHTML = `<p class="tiny muted">${esc(tr("court_ai_note"))}</p>${t.order.text ? `<details class="cc-hist"><summary class="small">${esc(tr("court_full_order"))}</summary><div class="doc-paper order-text">${md(t.order.text.slice(0, 60000))}</div></details>` : ""}`;
  return box;
}

/* ---------- panel: search by party name */
async function partySearch(name) {
  const box = $("#partyResults");
  box.innerHTML = `<div class="empty small">${esc(tr("court_searching"))} <span class="typing"><i></i><i></i><i></i></span></div>`;
  const r = await api("/api/court/search", { name });
  if (r.error) { box.innerHTML = `<p class="small bad-text">${esc(courtErr(r.error))}</p>`; return; }
  box.innerHTML = r.results.length ? r.results.map((x, i) => `<div class="cr-item"><b>${esc(x.title)}</b>
      <span class="small muted">${esc([x.type, x.status, x.court, x.filing_date ? tr("court_filed") + " " + courtDate(x.filing_date) : ""].filter(Boolean).join(" · "))}</span>
      <button class="ghost small" type="button" data-i="${i}">${esc(tr("court_track"))}</button></div>`).join("")
    : `<p class="small muted">${esc(tr("court_none"))}</p>`;
  box.querySelectorAll("button[data-i]").forEach(b => b.onclick = () => { const x = r.results[+b.dataset.i]; trackCase(x.cnr, tr("court_track_q").replace("{cnr}", x.cnr)); });
}

// a CNR typed into the chat is tracked directly
async function tryCourtFromChat(text) {
  if (!COURT.ecourts) return false;
  const m = String(text).match(CNR_FIND);
  if (!m) return false;
  const cnr = m.slice(1).join("").toUpperCase();
  await trackCase(cnr, text);
  return true;
}

document.addEventListener("DOMContentLoaded", async () => {
  try { COURT = await (await fetch("/api/court/status")).json(); } catch (e) {}
  $("#courtOff")?.classList.toggle("hidden", !!COURT.ecourts);
  $("#cnrForm").onsubmit = e => {
    e.preventDefault();
    const v = $("#cnrInput").value.replace(/[\s\-\/]/g, "").toUpperCase();
    if (!/^[A-Z]{4}\d{12}$/.test(v)) { alert(tr("court_err_cnr")); return; }
    $("#cnrInput").value = "";
    trackCase(v, tr("court_track_q").replace("{cnr}", v));
  };
  $("#partyForm").onsubmit = e => { e.preventDefault(); const v = $("#partyInput").value.trim(); if (v.length >= 3) partySearch(v); };});
