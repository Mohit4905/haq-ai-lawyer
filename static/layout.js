/* Shell: icon rail on the far left (VS Code-style) + one panel for the selected icon.
   Clicking the active icon again (or Ctrl+B) closes the panel; the choice is remembered.
   On phones the rail + panel slide in as a drawer from the menu button. */
(function () {
  const body = document.body;
  const mobile = () => innerWidth <= 900;
  const bar = () => $("#sidebar");
  const VIEW_KEYS = { cases: "my_cases", case: "t_case", deadlines: "t_dead", docs: "t_docs", evidence: "t_ev", practice: "t_prac", help: "t_help" };
  const USER_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/></svg>';

  function setCollapsed(c) {
    body.classList.toggle("side-collapsed", c);
    try { localStorage.setItem("haq_side", c ? "closed" : "open"); } catch (e) {}
  }
  const isOpen = () => (mobile() ? bar().classList.contains("open") : !body.classList.contains("side-collapsed"));
  function openSide() { if (mobile()) bar().classList.add("open"); else setCollapsed(false); }
  function closeSide() { if (mobile()) bar().classList.remove("open"); else setCollapsed(true); }
  window.openSide = openSide; window.closeSide = closeSide;

  function setSideTitle(name) {
    const el = $("#sideTitle"); if (!el) return;
    el.textContent = tr(VIEW_KEYS[name] || "my_cases");
  }
  window.renderSideTitle = () => setSideTitle(($(".rail .tab.active") || {}).dataset?.tab || "cases");

  function syncAvatar() {
    const btn = $("#acctBtn"); if (!btn) return;
    const av = $("#profileBox .pf-av.in");
    btn.innerHTML = av ? `<span class="rail-av">${esc(av.textContent.trim())}</span>` : USER_SVG;
  }

  document.addEventListener("DOMContentLoaded", () => {
    let saved = null; try { saved = localStorage.getItem("haq_side"); } catch (e) {}
    if (saved === "closed" && !mobile()) body.classList.add("side-collapsed");

    // the panel header follows the selected view (also when the app opens a view itself)
    if (typeof window.openTab === "function") {
      const orig = window.openTab;
      window.openTab = name => { orig(name); setSideTitle(name); try { localStorage.setItem("haq_view", name); } catch (e) {} };
    }
    // reopen the view the user had last (without forcing the panel open)
    let v = null; try { v = localStorage.getItem("haq_view"); } catch (e) {}
    if (v && v !== "cases" && $("#p-" + v)) {
      $$(".tab").forEach(t => t.classList.toggle("active", t.dataset.tab === v));
      $$(".panel").forEach(p => p.classList.toggle("active", p.id === "p-" + v));
      try { if (v === "evidence" && typeof renderEvidence === "function") renderEvidence(); if (v === "practice" && typeof renderPractice === "function") renderPractice(); } catch (e) {}
    }
    $$(".rail .tab").forEach(b => (b.onclick = () => {
      if (b.classList.contains("active") && isOpen() && !mobile()) { closeSide(); return; }
      window.openTab(b.dataset.tab);
    }));
    $("#collapseSide").onclick = closeSide;
    $("#toggleSide").onclick = e => { e.stopPropagation(); mobile() ? bar().classList.toggle("open") : setCollapsed(!body.classList.contains("side-collapsed")); };
    // phones: picking a case closes the drawer; tapping outside closes it
    $("#caseList")?.addEventListener("click", e => { if (mobile() && e.target.closest(".case-item") && !e.target.closest(".ci-btn")) bar().classList.remove("open"); });
    $("#newCase2").addEventListener("click", () => { if (mobile()) bar().classList.remove("open"); });
    document.addEventListener("click", e => {
      if (mobile() && bar().classList.contains("open") && !e.target.closest("#sidebar") && !e.target.closest("#toggleSide") && !e.target.closest("#settingsPop") && !e.target.closest("dialog")) bar().classList.remove("open");
    });
    // Ctrl+B toggles the panel
    document.addEventListener("keydown", e => { if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "b") { e.preventDefault(); isOpen() ? closeSide() : openSide(); } });

    // account + settings menu (opened from the bottom of the rail)
    const pop = $("#settingsPop");
    const toggle = e => { e.stopPropagation(); pop.classList.toggle("hidden"); };
    $("#settingsBtn").onclick = toggle;
    $("#acctBtn").onclick = toggle;
    document.addEventListener("click", e => { if (!pop.classList.contains("hidden") && !e.target.closest("#settingsPop") && !e.target.closest("#settingsBtn") && !e.target.closest("#acctBtn")) pop.classList.add("hidden"); });
    document.addEventListener("keydown", e => { if (e.key === "Escape") pop.classList.add("hidden"); });

    const box = $("#profileBox");
    if (box) new MutationObserver(syncAvatar).observe(box, { childList: true, subtree: true });
    syncAvatar();
    window.renderSideTitle();
    $("#lang")?.addEventListener("change", () => window.renderSideTitle());
  });

  // case title in the top bar
  window.renderChatTitle = function () {
    try {
      const c = Cases.cur();
      $("#chatTitle").textContent = (c && c.title) || tr("untitled");
    } catch (e) {}
  };
})();
