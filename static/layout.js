/* ChatGPT-style sidebar: brand + search + collapse on top, labelled sections, "My cases" list,
   profile row at the bottom. Collapsed = narrow icon strip (remembered). Phones: slide-in drawer.
   A tool (Case file, Deadlines, Track case…) opens in the main area, with back/close to the chat.
   Profile icon -> account only; gear -> settings. */
(function () {
  const body = document.body;
  const mobile = () => innerWidth <= 900;
  const side = () => $("#side");
  const VIEW_KEYS = { cases: "my_cases", case: "t_case", deadlines: "t_dead", docs: "t_docs", evidence: "t_ev", court: "t_court", help: "t_help" };
  const USER_SVG = '<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/></svg>';

  function setCollapsed(c) {
    body.classList.toggle("side-collapsed", c);
    try { localStorage.setItem("haq_side", c ? "closed" : "open"); } catch (e) {}
  }
  const isOpen = () => (mobile() ? side().classList.contains("open") : !body.classList.contains("side-collapsed"));
  function openSide() { if (mobile()) side().classList.add("open"); else setCollapsed(false); }
  function closeSide() { if (mobile()) side().classList.remove("open"); else setCollapsed(true); }
  window.openSide = openSide; window.closeSide = closeSide;

  // Tools (Case file, Deadlines, Documents, Evidence, Track case, Get help) open in the
  // main area over the chat; the sidebar always shows the menu + My cases.
  let curTool = null;
  function openTool(name) {
    if (!name || name === "cases" || !$("#p-" + name)) return closeTool();
    curTool = name;
    $$(".side-nav .tab").forEach(t => t.classList.toggle("active", t.dataset.tab === name));
    $$("#toolBody .panel").forEach(p => p.classList.toggle("active", p.id === "p-" + name));
    $("#toolTitle").textContent = tr(VIEW_KEYS[name]);
    $("#toolView").classList.remove("hidden");
    body.classList.add("tool-open");
    $("#toolBody").scrollTop = 0;
    $("#secCase") && ($("#secCase").open = true);
    try { if (name === "evidence") renderEvidence(); } catch (e) {}
    if (mobile()) side().classList.remove("open");
    try { sessionStorage.setItem("haq_tool", name); } catch (e) {}  // reopened after a reload in this tab
  }
  function closeTool() {
    curTool = null;
    try { sessionStorage.removeItem("haq_tool"); } catch (e) {}
    $("#toolView")?.classList.add("hidden");
    body.classList.remove("tool-open");
    $$(".side-nav .tab").forEach(t => t.classList.remove("active"));
  }
  window.showChat = closeTool;
  window.renderSideTitle = () => { if (curTool) $("#toolTitle").textContent = tr(VIEW_KEYS[curTool]); };

  // bottom profile row mirrors the account box that auth.js renders
  function syncAcct() {
    const btn = $("#acctBtn"); if (!btn) return;
    const av = $("#profileBox .pf-av"), signed = !!(av && av.classList.contains("in"));
    const name = $("#profileBox .pf b")?.textContent || tr("guest");
    const sub = signed ? ($("#profileBox .pf small")?.textContent || "") : tr("sign_in");
    btn.innerHTML = `<span class="acct-av ${signed ? "in" : ""}">${signed ? esc(av.textContent.trim()) : USER_SVG}</span><span class="acct-txt"><b>${esc(name)}</b><small>${esc(sub)}</small></span>`;
  }

  function closePops() { $$(".settings-pop").forEach(p => p.classList.add("hidden")); }
  function togglePop(id, e) {
    e.stopPropagation();
    const pop = $(id), was = pop.classList.contains("hidden");
    closePops(); if (was) pop.classList.remove("hidden");
  }

  document.addEventListener("DOMContentLoaded", () => {
    let saved = null; try { saved = localStorage.getItem("haq_side"); } catch (e) {}
    if (saved === "closed" && !mobile()) body.classList.add("side-collapsed");

    // move every tool panel out of the sidebar into the main tool view (listeners move with them)
    $$(".side-scroll .panel").forEach(p => { if (p.id !== "p-cases") { p.classList.remove("active"); $("#toolBody").appendChild(p); } });
    $("#p-cases").classList.add("active");
    window.openTab = openTool;  // every openTab("docs") etc. in the app now opens the main-area view
    let again = null; try { again = sessionStorage.getItem("haq_tool"); } catch (e) {}
    if (again) openTool(again);

    // a tool: click opens it in the main area; clicking the open one again goes back to the chat
    $$(".side-nav .tab").forEach(b => (b.onclick = () => (b.classList.contains("active") ? closeTool() : openTool(b.dataset.tab))));
    $("#toolBack").onclick = closeTool;
    $("#toolClose").onclick = closeTool;
    document.addEventListener("keydown", e => { if (e.key === "Escape" && curTool && !document.querySelector("dialog[open]")) closeTool(); });
    $("#brandBtn").onclick = () => (isOpen() ? closeTool() : openSide());
    $("#searchBtn").onclick = () => {
      if (!isOpen()) openSide();
      const s = $("#caseSearch"); s.classList.toggle("hidden");
      if (!s.classList.contains("hidden")) s.focus(); else if (s.value) { s.value = ""; renderCaseList(); }
    };
    $("#collapseSide").onclick = closeSide;
    $("#toggleSide").onclick = e => { e.stopPropagation(); side().classList.toggle("open"); };

    // New case (Cases.create runs first, from cases.js): show My cases, clear + focus the message box
    $("#newCase2").addEventListener("click", () => {
      if (typeof busy !== "undefined" && busy) return;  // Cases.create already told the user to wait
      if (mobile()) side().classList.remove("open");
      closeTool();
      const s = $("#caseSearch"); if (s && s.value) { s.value = ""; renderCaseList(); }
      const inp = $("#input"); inp.value = ""; try { autosize(); } catch (e) {}
      $("#chat").scrollTop = 0;
      const comp = $("#composer"); comp.classList.remove("flash"); void comp.offsetWidth; comp.classList.add("flash");
      setTimeout(() => inp.focus(), 50);
    });

    // phones: picking a case closes the drawer; tapping outside closes it
    // picking a case shows its chat (and closes the drawer on phones)
    $("#caseList")?.addEventListener("click", e => {
      if (!e.target.closest(".case-item") || e.target.closest(".ci-btn")) return;
      closeTool();
      if (mobile()) side().classList.remove("open");
    });
    document.addEventListener("click", e => {
      if (mobile() && side().classList.contains("open") && !e.target.closest("#side") && !e.target.closest("#toggleSide") && !e.target.closest(".settings-pop") && !e.target.closest("dialog") && !e.target.closest("#ciMenu")) side().classList.remove("open");
    });
    document.addEventListener("keydown", e => { if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "b") { e.preventDefault(); isOpen() ? closeSide() : openSide(); } });

    // profile icon -> account only; gear -> settings
    $("#acctBtn").onclick = e => togglePop("#acctPop", e);
    $("#settingsBtn").onclick = e => togglePop("#settingsPop", e);
    // composedPath(): a button that redraws its own icon (theme toggle) detaches e.target, so closest() would miss the popover
    document.addEventListener("click", e => {
      const inside = e.composedPath().some(el => el.classList && (el.classList.contains("settings-pop") || el.id === "settingsBtn" || el.id === "acctBtn"));
      if (!inside) closePops();
    });
    document.addEventListener("keydown", e => { if (e.key === "Escape") closePops(); });

    const box = $("#profileBox");
    if (box) new MutationObserver(syncAcct).observe(box, { childList: true, subtree: true });
    syncAcct();
    $("#lang")?.addEventListener("change", () => { window.renderSideTitle(); syncAcct(); });
  });

  window.renderChatTitle = function () {
    try {
      const c = Cases.cur();
      $("#chatTitle").textContent = (c && c.title) || tr("untitled");
    } catch (e) {}
  };
})();
