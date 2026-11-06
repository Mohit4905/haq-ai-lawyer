/* Claude-style shell: collapsible sidebar (remembered), settings menu at the bottom, case title on top. */
(function () {
  const body = document.body;
  const mobile = () => innerWidth <= 900;
  function setCollapsed(c) {
    body.classList.toggle("side-collapsed", c);
    try { localStorage.setItem("haq_side", c ? "closed" : "open"); } catch (e) {}
  }
  function openSide() { if (mobile()) $("#side").classList.add("open"); else setCollapsed(false); }
  function closeSide() { if (mobile()) $("#side").classList.remove("open"); else setCollapsed(true); }
  window.openSide = openSide;

  document.addEventListener("DOMContentLoaded", () => {
    let saved = null; try { saved = localStorage.getItem("haq_side"); } catch (e) {}
    if (saved === "closed" && !mobile()) body.classList.add("side-collapsed");
    $("#collapseSide").onclick = closeSide;
    $("#toggleSide").onclick = () => (mobile() ? $("#side").classList.toggle("open") : setCollapsed(!body.classList.contains("side-collapsed")));
    // tap outside the drawer on phones closes it
    document.addEventListener("click", e => {
      if (mobile() && $("#side").classList.contains("open") && !e.target.closest("#side") && !e.target.closest("#toggleSide")) $("#side").classList.remove("open");
    });
    // keyboard: Ctrl+B toggles the sidebar (like many chat apps)
    document.addEventListener("keydown", e => { if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "b") { e.preventDefault(); body.classList.contains("side-collapsed") || $("#side").classList.contains("open") ? closeSide() : openSide(); } });
    // settings menu
    const pop = $("#settingsPop");
    $("#settingsBtn").onclick = e => { e.stopPropagation(); pop.classList.toggle("hidden"); };
    document.addEventListener("click", e => { if (!pop.classList.contains("hidden") && !e.target.closest("#settingsPop") && !e.target.closest("#settingsBtn")) pop.classList.add("hidden"); });
    document.addEventListener("keydown", e => { if (e.key === "Escape") pop.classList.add("hidden"); });
  });

  // case title in the top bar
  window.renderChatTitle = function () {
    try {
      const c = Cases.cur();
      $("#chatTitle").textContent = (c && c.title) || tr("untitled");
    } catch (e) {}
  };
})();
