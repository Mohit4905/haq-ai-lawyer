/* ChatGPT-style sidebar: brand + search + collapse on top, labelled sections, "My cases" list,
   profile row at the bottom. Collapsed = narrow icon strip (remembered). Phones: slide-in drawer.
   A section (Case file, Deadlines…) opens inside the sidebar with a back arrow to My cases.
   Profile icon -> account only; gear -> settings. */
(function () {
  const body = document.body;
  const mobile = () => innerWidth <= 900;
  const side = () => $("#side");
  const VIEW_KEYS = { cases: "my_cases", case: "t_case", deadlines: "t_dead", docs: "t_docs", evidence: "t_ev", practice: "t_prac", court: "t_court", help: "t_help" };
  const USER_SVG = '<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/></svg>';

  function setCollapsed(c) {
    body.classList.toggle("side-collapsed", c);
    try { localStorage.setItem("haq_side", c ? "closed" : "open"); } catch (e) {}
  }
  const isOpen = () => (mobile() ? side().classList.contains("open") : !body.classList.contains("side-collapsed"));
  function openSide() { if (mobile()) side().classList.add("open"); else setCollapsed(false); }
  function closeSide() { if (mobile()) side().classList.remove("open"); else setCollapsed(true); }
  window.openSide = openSide; window.closeSide = closeSide;

  function setView(name) {
    const t = $("#sideTitle"); if (t) t.textContent = tr(VIEW_KEYS[name] || "my_cases");
    $("#viewBar")?.classList.toggle("hidden", !name || name === "cases");
  }
  const curView = () => ($(".panel.active")?.id || "p-cases").slice(2);
  window.renderSideTitle = () => setView(curView());

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

    if (typeof window.openTab === "function") {
      const orig = window.openTab;
      window.openTab = name => { orig(name); setView(name); try { localStorage.setItem("haq_view", name); } catch (e) {} };
    }
    // reopen the section the user had last (without forcing the sidebar open)
    let v = null; try { v = localStorage.getItem("haq_view"); } catch (e) {}
    if (v && v !== "cases" && $("#p-" + v)) {
      $$(".tab").forEach(t => t.classList.toggle("active", t.dataset.tab === v));
      $$(".panel").forEach(p => p.classList.toggle("active", p.id === "p-" + v));
      try { if (v === "evidence" && typeof renderEvidence === "function") renderEvidence(); if (v === "practice" && typeof renderPractice === "function") renderPractice(); } catch (e) {}
    }
    window.renderSideTitle();

    // sections: click opens it; clicking the open one again goes back to My cases
    $$(".side-nav .tab").forEach(b => (b.onclick = () => {
      if (b.classList.contains("active") && isOpen()) window.openTab("cases");
      else window.openTab(b.dataset.tab);
    }));
    $("#backBtn").onclick = () => window.openTab("cases");
    $("#brandBtn").onclick = () => (isOpen() ? window.openTab("cases") : openSide());
    $("#searchBtn").onclick = () => {
      window.openTab("cases");
      const s = $("#caseSearch"); s.classList.toggle("hidden");
      if (!s.classList.contains("hidden")) s.focus(); else if (s.value) { s.value = ""; renderCaseList(); }
    };
    $("#collapseSide").onclick = closeSide;
    $("#toggleSide").onclick = e => { e.stopPropagation(); side().classList.toggle("open"); };

    // New case (Cases.create runs first, from cases.js): show My cases, clear + focus the message box
    $("#newCase2").addEventListener("click", () => {
      if (mobile()) side().classList.remove("open"); else if (isOpen()) window.openTab("cases");
      const s = $("#caseSearch"); if (s && s.value) { s.value = ""; renderCaseList(); }
      const inp = $("#input"); inp.value = ""; try { autosize(); } catch (e) {}
      $("#chat").scrollTop = 0;
      const comp = $("#composer"); comp.classList.remove("flash"); void comp.offsetWidth; comp.classList.add("flash");
      setTimeout(() => inp.focus(), 50);
    });

    // phones: picking a case closes the drawer; tapping outside closes it
    $("#caseList")?.addEventListener("click", e => { if (mobile() && e.target.closest(".case-item") && !e.target.closest(".ci-btn")) side().classList.remove("open"); });
    document.addEventListener("click", e => {
      if (mobile() && side().classList.contains("open") && !e.target.closest("#side") && !e.target.closest("#toggleSide") && !e.target.closest(".settings-pop") && !e.target.closest("dialog") && !e.target.closest("#ciMenu")) side().classList.remove("open");
    });
    document.addEventListener("keydown", e => { if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "b") { e.preventDefault(); isOpen() ? closeSide() : openSide(); } });

    // profile icon -> account only; gear -> settings
    $("#acctBtn").onclick = e => togglePop("#acctPop", e);
    $("#settingsBtn").onclick = e => togglePop("#settingsPop", e);
    document.addEventListener("click", e => { if (!e.target.closest(".settings-pop") && !e.target.closest("#settingsBtn") && !e.target.closest("#acctBtn")) closePops(); });
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
