/* Message actions (ChatGPT-style).
   Under the user's messages: edit, share, copy. Under Haq's replies: copy, like / dislike, read aloud,
   share, try again, and a "more" menu (copy with sources, report).

   Identity: every message in S.messages has a stable id (m.id, set by the server or by pushMsg);
   a reply points to its prompt (m.reply_to); a reply's extras in VIEW.turns point to it (t.mid).
   Every action looks its message up by id. List positions are used only to cut the history at a
   prompt when regenerating (what the model saw before it), never to decide which message to act on. */

const ICON = {
  copy: '<rect x="9" y="9" width="11" height="11" rx="2"/><path d="M5 15V5a2 2 0 0 1 2-2h10"/>',
  edit: '<path d="M12 20h9"/><path d="M16.5 3.5a2.1 2.1 0 0 1 3 3L7 19l-4 1 1-4z"/>',
  share: '<path d="M4 12v7a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-7"/><path d="M16 6l-4-4-4 4"/><path d="M12 2v13"/>',
  up: '<path d="M7 10v11H4a1 1 0 0 1-1-1v-9a1 1 0 0 1 1-1z"/><path d="M7 10l4-8a2.5 2.5 0 0 1 3 2.5V9h5.2a2 2 0 0 1 2 2.3l-1.3 8A2 2 0 0 1 18 21H7"/>',
  down: '<path d="M17 14V3h3a1 1 0 0 1 1 1v9a1 1 0 0 1-1 1z"/><path d="M17 14l-4 8a2.5 2.5 0 0 1-3-2.5V15H4.8a2 2 0 0 1-2-2.3l1.3-8A2 2 0 0 1 6 3h11"/>',
  speak: '<path d="M11 5L6 9H3v6h3l5 4z"/><path d="M15.5 8.5a5 5 0 0 1 0 7"/><path d="M18.5 5.5a9 9 0 0 1 0 13"/>',
  stop: '<rect x="6" y="6" width="12" height="12" rx="2"/>',
  regen: '<path d="M21 12a9 9 0 1 1-2.6-6.4"/><path d="M21 3v6h-6"/>',
  more: '<circle cx="5" cy="12" r="1.3"/><circle cx="12" cy="12" r="1.3"/><circle cx="19" cy="12" r="1.3"/>',
  prev: '<path d="M15 18l-6-6 6-6"/>', next: '<path d="M9 18l6-6-6-6"/>',
  flag: '<path d="M4 22V4"/><path d="M4 4h13l-2 4 2 4H4"/>', src: '<path d="M4 4h12l4 4v12H4z"/><path d="M8 12h8M8 16h5"/>',
};
const svg = (k, fill) => `<svg width="16" height="16" viewBox="0 0 24 24" fill="${fill ? "currentColor" : "none"}" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${ICON[k]}</svg>`;

/* ---------------- ids */
function newId() {
  try { if (crypto.randomUUID) return crypto.randomUUID().replace(/-/g, ""); } catch (e) {}
  return "m" + Date.now().toString(36) + Math.random().toString(36).slice(2, 12);
}
// safety net + one-time migration of cases saved before ids existed
function ensureIds() {
  if (!S || !Array.isArray(S.messages)) return;
  const seen = new Set();
  let lastUser = null;
  for (const m of S.messages) {
    if (!m.id || seen.has(m.id)) m.id = newId();
    seen.add(m.id);
    if (m.role === "user") lastUser = m.id;
    else if (!m.reply_to && lastUser) m.reply_to = lastUser;
  }
  if (!VIEW) return;
  VIEW.turns = VIEW.turns || [];
  if (VIEW.turns.some(t => t && !t.mid)) {  // old cases kept extras in reply order: link them once
    const replies = S.messages.filter(m => m.role !== "user");
    const linked = new Set(VIEW.turns.map(t => t && t.mid).filter(Boolean));
    VIEW.turns.forEach((t, i) => { if (t && !t.mid && replies[i] && !linked.has(replies[i].id)) { t.mid = replies[i].id; linked.add(t.mid); } });
  }
}
const msgById = id => (S?.messages || []).find(m => m.id === id);
const turnOf = id => (VIEW?.turns || []).find(t => t && t.mid === id);
const replyTo = uid => (S?.messages || []).find(m => m.role !== "user" && m.reply_to === uid);

// every message the front-end creates goes through here, so it always has an id (and a prompt link)
function pushMsg(m) {
  m.id = m.id || newId();
  if (m.role !== "user" && !m.reply_to) m.reply_to = [...S.messages].reverse().find(x => x.role === "user")?.id;
  S.messages.push(m);
  // the user's text is drawn before it is saved: that bubble (the newest one, same text, no id yet) gets the id now.
  // Bot bubbles are always drawn after saving and get their message passed to addMsg directly.
  if (m.role === "user") {
    const last = [...$("#chat").querySelectorAll(".msg.user")].pop();
    if (last && !last.dataset.mid && last.querySelector(".bubble")?.textContent === m.content) bindMsg(last.querySelector(".bubble"), m);
  }
  return m;
}

/* ---------------- small helpers */
function toast(text) {
  let t = $("#toast");
  if (!t) { t = document.createElement("div"); t.id = "toast"; t.setAttribute("role", "status"); t.setAttribute("aria-live", "polite"); document.body.appendChild(t); }
  t.textContent = text; t.classList.add("show");
  clearTimeout(toast.h); toast.h = setTimeout(() => t.classList.remove("show"), 1800);
}
// readable text of a message (markdown markers removed, list items kept as "- ")
function plainText(content) {
  const html = md(content).replace(/<li>/g, "<li>- ").replace(/<\/(p|li|h4|ul|ol)>/g, "\n").replace(/<br\s*\/?>/g, "\n");
  const d = document.createElement("div"); d.innerHTML = html;
  return d.textContent.replace(/\n{3,}/g, "\n\n").trim();
}
// what is spoken: no symbols, links, markdown or emoji
function speechText(content) {
  return plainText(String(content).replace(/```[\s\S]*?```/g, " ").replace(/`([^`]*)`/g, "$1"))
    .replace(/https?:\/\/\S+/g, " ").replace(/^\s*- /gm, "").replace(/[§*_#>|~•→←✓✗]/g, " ")
    .replace(/[\u{1F300}-\u{1FAFF}\u{2600}-\u{27BF}\u{FE0F}]/gu, " ").replace(/[ \t]+/g, " ").trim();
}
async function copyText(text) {
  try { await navigator.clipboard.writeText(text); return true; } catch (e) {}
  try {  // older browsers / no clipboard permission
    const ta = document.createElement("textarea"); ta.value = text; ta.setAttribute("readonly", ""); ta.style.position = "fixed"; ta.style.opacity = "0";
    document.body.appendChild(ta); ta.select(); const ok = document.execCommand("copy"); ta.remove(); return ok;
  } catch (e) { return false; }
}
async function doCopy(text, btn) {
  const ok = await copyText(text);
  toast(ok ? tr("act_copied") : tr("act_copy_fail"));
  if (ok && btn) { btn.classList.add("done"); setTimeout(() => btn.classList.remove("done"), 1200); }
}
async function doShare(text) {
  if (navigator.share) {
    try { await navigator.share({ title: "Haq", text }); return; }
    catch (e) { if (e && e.name === "AbortError") return; }  // the user closed the share sheet
  }
  const ok = await copyText(text);
  toast(ok ? tr("act_share_fallback") : tr("act_copy_fail"));
}
function canRegen(m) {
  if (!m || m.role === "user" || m.practice) return false;
  const t = turnOf(m.id), u = msgById(m.reply_to);
  return !!(t && u && !u.practice && !t.doc && !t.court && !t.order && !t.prep && t.src !== "notice");
}
function closeMenus() { $$(".act-menu").forEach(n => n.remove()); }
document.addEventListener("click", e => { if (!e.target.closest(".act-menu,.act-more")) closeMenus(); });
document.addEventListener("keydown", e => { if (e.key === "Escape") closeMenus(); });

/* ---------------- the bars */
function actBtn(icon, label, onClick, extraClass) {
  const b = document.createElement("button");
  b.type = "button"; b.className = "act" + (extraClass ? " " + extraClass : "");
  b.innerHTML = svg(icon); b.title = label; b.setAttribute("aria-label", label);
  b.onclick = e => { e.stopPropagation(); onClick(b, e); };
  return b;
}
// attach a message's id and its action bar to its bubble
function bindMsg(bubble, m) {
  if (!bubble || !m) return;
  const wrap = bubble.parentElement;
  wrap.dataset.mid = m.id;
  wrap.querySelector(":scope > .msg-actions, :scope > .bubble > .msg-actions")?.remove();
  const bar = m.role === "user" ? userBar(m) : botBar(m);
  if (m.role === "user") wrap.appendChild(bar); else bubble.appendChild(bar);
}
function userBar(m) {
  const bar = document.createElement("div");
  bar.className = "msg-actions";
  const id = m.id;
  const r = replyTo(id);
  if (canRegen(r)) bar.appendChild(actBtn("edit", tr("act_edit"), () => startEdit(id)));
  bar.appendChild(actBtn("share", tr("act_share"), () => doShare(msgById(id)?.content || "")));
  bar.appendChild(actBtn("copy", tr("act_copy"), b => doCopy(msgById(id)?.content || "", b)));
  return bar;
}
function botBar(m) {
  const bar = document.createElement("div");
  bar.className = "msg-actions";
  const id = m.id;
  const vs = VIEW.versions?.[id];
  if (vs && vs.length > 1) {  // ‹ 2/3 › when the reply was regenerated or its prompt edited
    const cur = Math.min(VIEW.verIdx?.[id] ?? vs.length - 1, vs.length - 1);
    const nav = document.createElement("span"); nav.className = "act-ver";
    const p = actBtn("prev", tr("act_prev"), () => showVersion(id, cur - 1)); p.disabled = cur === 0;
    const n = actBtn("next", tr("act_next"), () => showVersion(id, cur + 1)); n.disabled = cur === vs.length - 1;
    const lab = document.createElement("span"); lab.className = "act-ver-n"; lab.textContent = `${cur + 1}/${vs.length}`;
    nav.append(p, lab, n); bar.appendChild(nav);
  }
  bar.appendChild(actBtn("copy", tr("act_copy"), b => doCopy(plainText(msgById(id)?.content || ""), b)));
  const fb = VIEW.fb?.[id];
  const up = actBtn("up", tr("act_good"), () => rate(id, "up"), fb === "up" ? "on" : "");
  const down = actBtn("down", tr("act_bad"), () => rate(id, "down"), fb === "down" ? "on" : "");
  up.setAttribute("aria-pressed", fb === "up"); down.setAttribute("aria-pressed", fb === "down");
  if (fb === "up") up.innerHTML = svg("up", true);
  if (fb === "down") down.innerHTML = svg("down", true);
  bar.append(up, down);
  const sp = actBtn(speaking === id ? "stop" : "speak", tr(speaking === id ? "act_stop" : "act_read"), () => readAloud(id), "act-speak" + (speaking === id ? " on" : ""));
  bar.appendChild(sp);
  bar.appendChild(actBtn("share", tr("act_share"), () => doShare(plainText(msgById(id)?.content || ""))));
  if (canRegen(m)) bar.appendChild(actBtn("regen", tr("act_regen"), () => regenerate(id)));
  bar.appendChild(actBtn("more", tr("act_more"), b => openMore(id, b), "act-more"));
  return bar;
}
function refreshBar(id) {
  const wrap = $(`#chat .msg[data-mid="${CSS.escape(id)}"]`);
  const m = msgById(id);
  if (wrap && m) bindMsg(wrap.querySelector(".bubble"), m);
}

/* ---------------- feedback */
function rate(id, val) {
  VIEW.fb = VIEW.fb || {};
  VIEW.fb[id] = VIEW.fb[id] === val ? null : val;  // clicking the selected one again clears it
  persist(); refreshBar(id);
  const t = turnOf(id);
  api("/api/feedback", { message_id: id, rating: VIEW.fb[id], model: t?.model ? `${t.model.provider}/${t.model.model}` : null, category: S?.case?.category || null });
  if (VIEW.fb[id]) toast(tr("act_thanks"));
}
function report(id, kind) {
  const t = turnOf(id), m = msgById(id);
  api("/api/feedback", { message_id: id, report: kind, rating: VIEW.fb?.[id] || null, model: t?.model ? `${t.model.provider}/${t.model.model}` : null,
                         category: S?.case?.category || null, reply: m?.content || "" });
  toast(tr("act_reported"));
}
function openMore(id, btn) {
  closeMenus();
  const t = turnOf(id), m = msgById(id);
  const menu = document.createElement("div");
  menu.className = "act-menu"; menu.setAttribute("role", "menu");
  const item = (icon, label, fn) => { const b = document.createElement("button"); b.type = "button"; b.setAttribute("role", "menuitem"); b.innerHTML = svg(icon) + `<span>${esc(label)}</span>`; b.onclick = e => { e.stopPropagation(); closeMenus(); fn(); }; menu.appendChild(b); };
  if (t?.citations?.length) item("src", tr("act_copy_src"), () => doCopy(plainText(m?.content || "") + "\n\n" + tr("act_sources") + ":\n" + t.citations.map(c => `- ${c.act}${secLabel(c.section)}: ${c.source_url}`).join("\n")));
  item("flag", tr("act_report_wrong"), () => report(id, "incorrect"));
  item("flag", tr("act_report_bad"), () => report(id, "inappropriate"));
  const small = document.createElement("p"); small.className = "act-menu-note"; small.textContent = tr("act_report_note"); menu.appendChild(small);
  btn.parentElement.appendChild(menu);
  const first = menu.querySelector("button"); first && first.focus();
}

/* ---------------- read aloud (one at a time) */
let speaking = null;
function stopSpeaking() {
  const was = speaking; speaking = null;
  try { speechSynthesis.cancel(); } catch (e) {}
  if (was) refreshBar(was);
}
function readAloud(id) {
  if (!window.speechSynthesis || !window.SpeechSynthesisUtterance) { toast(tr("act_no_tts")); return; }
  if (speaking === id) { stopSpeaking(); return; }
  stopSpeaking();
  const text = speechText(msgById(id)?.content || "");
  if (!text) return;
  // short chunks: some browsers stop long utterances after ~15 s
  const parts = text.match(/[^.!?।\n]+[.!?।]?/g)?.map(s => s.trim()).filter(Boolean) || [text];
  const chunks = [];
  parts.forEach(p => { const lastC = chunks[chunks.length - 1]; if (lastC && (lastC + " " + p).length < 220) chunks[chunks.length - 1] = lastC + " " + p; else chunks.push(p); });
  const lang = speechLang();
  const voice = speechSynthesis.getVoices().find(v => v.lang === lang);
  speaking = id; refreshBar(id);
  chunks.forEach((c, i) => {
    const u = new SpeechSynthesisUtterance(c);
    u.lang = lang; if (voice) u.voice = voice;
    if (i === chunks.length - 1) u.onend = () => { if (speaking === id) { speaking = null; refreshBar(id); } };
    u.onerror = () => { if (speaking === id) { speaking = null; refreshBar(id); } };
    speechSynthesis.speak(u);
  });
}
function speechLang() {
  const sc = S?.case?.script || "";
  const map = { Devanagari: "hi-IN", Tamil: "ta-IN", Bengali: "bn-IN", Telugu: "te-IN", Kannada: "kn-IN", Gujarati: "gu-IN", Malayalam: "ml-IN", Gurmukhi: "pa-IN" };
  return uiLang() === "en" ? (map[sc] || "en-IN") : langInfo()[3];
}

/* ---------------- regenerate / edit (in place: the other messages are not touched) */
const clone = o => o == null ? o : JSON.parse(JSON.stringify(o));
function turnFromRes(res, mid) {
  return { mid, src: "chat", reply: res.reply, citations: res.citations, guard: res.guard, actions: res.actions, model: res.model, latency_s: res.latency_s,
           calculated: res.calculated, completeness: res.completeness, needs_lawyer: res.needs_lawyer, emergency_contacts: res.emergency_contacts };
}
function rerender(id) {
  const wrap = $(`#chat .msg[data-mid="${CSS.escape(id)}"]`), m = msgById(id);
  if (!wrap || !m) return;
  const b = wrap.querySelector(".bubble");
  if (m.role === "user") { b.textContent = m.content; bindMsg(b, m); return; }
  const t = turnOf(id) || { reply: m.content };
  b.innerHTML = md(t.intro != null ? t.intro : m.content);
  b.appendChild(renderBotExtras(t));
  bindMsg(b, m);
}
async function regenerate(rid, editedText) {
  if (busy || prepOn()) { toast(tr("act_busy")); return false; }
  const r = msgById(rid), u = r && msgById(r.reply_to);
  if (!canRegen(r)) return false;
  const text = editedText != null ? editedText : u.content;
  const isLast = S.messages[S.messages.length - 1] === r;
  const snap = VIEW.snaps?.[u.id];  // the case file as it was before this prompt
  const cut = S.messages.indexOf(u);  // history the model saw before this prompt
  const base = Object.assign({}, S, { messages: S.messages.slice(0, cut), case: clone(snap?.case || S.case), flags: clone(snap?.flags || S.flags) });
  const wrap = $(`#chat .msg[data-mid="${CSS.escape(rid)}"]`), bub = wrap?.querySelector(".bubble");
  const oldHtml = bub?.innerHTML;
  if (speaking === rid) stopSpeaking();
  if (bub) bub.innerHTML = '<span class="typing"><i></i><i></i><i></i></span>';
  setBusy(true);
  const res = await api("/api/chat", { state: base, message: text, provider: provider(), lang_pref: langInfo()[2] || "English" });
  setBusy(false);
  if (res.error || !res.reply) { if (bub) { bub.innerHTML = oldHtml; refreshBar(rid); } toast(tr("act_regen_fail") + " " + (res.error || tr("err_server"))); return false; }
  const old = turnOf(rid);
  VIEW.versions = VIEW.versions || {}; VIEW.verIdx = VIEW.verIdx || {};
  const vs = VIEW.versions[rid] = VIEW.versions[rid] || [{ content: r.content, prompt: u.content, turn: clone(old) }];
  const nt = turnFromRes(res, rid);
  if (old?.prepOffer) nt.prepOffer = true;  // keep the practice offer where it was
  vs.push({ content: res.reply, prompt: text, turn: clone(nt) });
  VIEW.verIdx[rid] = vs.length - 1;
  r.content = res.reply; u.content = text;  // same ids, new text
  const i = VIEW.turns.indexOf(old); if (i >= 0) VIEW.turns[i] = nt; else VIEW.turns.push(nt);
  if (isLast && res.state) { S.case = res.state.case; S.flags = res.state.flags; S.log = res.state.log; renderCase(lastCaseTurn()); }
  persist();
  rerender(u.id); rerender(rid);
  return true;
}
function showVersion(rid, k) {
  if (busy) return;
  const vs = VIEW.versions?.[rid], r = msgById(rid), u = r && msgById(r.reply_to);
  if (!vs || !vs[k] || !r) return;
  if (speaking === rid) stopSpeaking();
  VIEW.verIdx[rid] = k;
  r.content = vs[k].content;
  if (u && vs[k].prompt != null) u.content = vs[k].prompt;
  const old = turnOf(rid), nt = Object.assign(clone(vs[k].turn) || { reply: vs[k].content }, { mid: rid });
  const i = VIEW.turns.indexOf(old); if (i >= 0) VIEW.turns[i] = nt;
  persist();
  if (u) rerender(u.id);
  rerender(rid);
}
function startEdit(uid) {
  if (busy || prepOn()) { toast(tr("act_busy")); return; }
  const u = msgById(uid), r = replyTo(uid);
  if (!u || !canRegen(r)) return;
  const wrap = $(`#chat .msg[data-mid="${CSS.escape(uid)}"]`); if (!wrap) return;
  if (wrap.querySelector(".edit-box")) return;
  const bub = wrap.querySelector(".bubble");
  wrap.classList.add("editing");
  const box = document.createElement("div"); box.className = "edit-box";
  box.innerHTML = `<textarea rows="3" aria-label="${esc(tr("act_edit"))}"></textarea><div class="edit-btns"><button type="button" class="ghost small edit-cancel">${esc(tr("act_cancel"))}</button><button type="button" class="primary small edit-save">${esc(tr("act_send"))}</button></div>`;
  const ta = box.querySelector("textarea"); ta.value = u.content;
  bub.classList.add("hidden"); wrap.querySelector(".msg-actions")?.classList.add("hidden");
  wrap.insertBefore(box, bub);
  const fit = () => { ta.style.height = "auto"; ta.style.height = Math.min(ta.scrollHeight, 260) + "px"; }; fit(); ta.addEventListener("input", fit);
  ta.focus(); ta.setSelectionRange(ta.value.length, ta.value.length);
  const close = () => { box.remove(); bub.classList.remove("hidden"); wrap.classList.remove("editing"); wrap.querySelector(".msg-actions")?.classList.remove("hidden"); };
  box.querySelector(".edit-cancel").onclick = close;
  const save = async () => {
    const v = ta.value.trim();
    if (!v || v === u.content) { close(); return; }
    box.querySelector(".edit-save").disabled = true;
    const ok = await regenerate(r.id, v);
    close();
    if (!ok) refreshBar(uid);
  };
  box.querySelector(".edit-save").onclick = save;
  ta.addEventListener("keydown", e => { if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); save(); } if (e.key === "Escape") close(); });
}
