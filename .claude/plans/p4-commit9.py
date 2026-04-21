#!/usr/bin/env python3
"""Commit 9 · Mobile Perfect (Phase 2D) — breakpoint 768px.
  - Hamburger menu replaces nav tabs
  - Hero 75vh, centered text, buttons full-width stacked
  - Cards 70vw, scroll-snap mandatory
  - Profile panel becomes fullscreen
  - Notifications dropdown becomes bottom-sheet
  - Card progress bars 4px (more visible)
"""
import sys
from pathlib import Path

TARGET = Path("/Users/shahafwaitzman/Documents/CLOUD CODE/super-team-academy/academy-hub.html")
content = TARGET.read_text(encoding='utf-8')

# Append mobile CSS + hamburger element, before </style>
MARKER = "</style>"

MOBILE_CSS = """
/* ═══════════════════════════════════════════
   COMMIT 9 · Mobile Perfect (≤ 768px)
   ═══════════════════════════════════════════ */
.hamburger-btn {
  display: none;
  width: 42px; height: 42px;
  background: rgba(255,255,255,0.08);
  border: 1px solid rgba(255,255,255,0.15);
  border-radius: 8px;
  color: #fff;
  align-items: center; justify-content: center;
  cursor: pointer; padding: 0;
  font-family: inherit;
}
.hamburger-btn svg { width: 22px; height: 22px; }
.mobile-nav-overlay {
  display: none;
  position: fixed; inset: 0;
  z-index: 400;
  background: rgba(0,0,0,0.88);
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
  flex-direction: column;
  padding: 70px 24px 24px;
  gap: 4px;
  opacity: 0;
  transition: opacity 0.25s;
}
.mobile-nav-overlay.open { display: flex; opacity: 1; }
.mobile-nav-overlay a {
  display: block;
  padding: 18px 14px;
  font-size: 17px; font-weight: 700;
  color: rgba(255,255,255,0.92);
  text-decoration: none;
  border-bottom: 1px solid rgba(255,255,255,0.07);
  transition: color 0.2s, padding 0.2s;
}
.mobile-nav-overlay a:hover,
.mobile-nav-overlay a.current {
  color: var(--nflx-red, #E50914);
  padding-inline-start: 22px;
}
.mobile-nav-close {
  position: absolute; top: 18px; inset-inline-end: 18px;
  width: 42px; height: 42px;
  background: rgba(255,255,255,0.1);
  border: none; border-radius: 50%; color: #fff;
  font-size: 22px; cursor: pointer;
  font-family: inherit;
}

@media (max-width: 768px) {
  /* Nav */
  .tabbed-primary-navigation { display: none; }
  .hamburger-btn { display: flex; }
  .logo { font-size: 0.8em; }
  .main-header { padding: 0 14px; }
  .secondary-navigation { gap: 6px; }
  .streak-pill { padding: 5px 9px; font-size: 12px; }

  /* Hero */
  .billboard-row { padding-top: 0; min-height: 75vh; height: 75vh; }
  .meta-layer {
    bottom: 12% !important;
    right: 20px; left: 20px;
    max-width: none; min-width: 0;
    text-align: center;
    align-items: center !important;
  }
  .billboard-title { font-size: clamp(32px, 9vw, 54px) !important; text-align: center; }
  .synopsis { font-size: 13.5px; text-align: center; }
  .billboard-links {
    flex-direction: column;
    width: 100%;
    gap: 10px;
  }
  .billboard-links .nflx-btn {
    width: 100%;
    justify-content: center;
  }

  /* Cards: 70vw + scroll-snap */
  .rowContent {
    scroll-snap-type: x mandatory;
    scroll-padding-inline-start: 16px;
    padding-inline: 14px;
    gap: 10px;
  }
  .slider-item {
    flex: 0 0 70vw !important;
    scroll-snap-align: start;
  }
  .row-header { padding-inline-end: 14px; gap: 10px; }
  .row-progress {
    width: 100%;
    justify-content: space-between;
    padding: 6px 12px;
  }
  .row-progress-bar { width: 80px; }

  /* Card progress bar: thicker */
  .card-progress { height: 4px; }

  /* Profile panel → fullscreen */
  .profile-panel {
    width: 100vw; max-width: 100vw;
    border-inline-end: none;
  }

  /* Notifications → bottom sheet */
  .notif-dropdown {
    position: fixed;
    top: auto; bottom: 0;
    inset-inline-start: 0; inset-inline-end: 0;
    width: 100vw;
    max-height: 70vh;
    border-radius: 18px 18px 0 0;
    border: 1px solid rgba(255,255,255,0.12);
    border-bottom: none;
    box-shadow: 0 -20px 50px rgba(0,0,0,0.6);
  }
  .notif-dropdown.open {
    animation: slideUpSheet 0.3s cubic-bezier(0.2,0.8,0.2,1);
  }
  @keyframes slideUpSheet {
    from { transform: translateY(100%); }
    to { transform: translateY(0); }
  }

  /* Leaderboard card narrower */
  .leaderboard-card { width: 65vw; }

  /* Back-button + brand */
  .nav-back-btn .back-label { display: none; }
}

@media (max-width: 480px) {
  .billboard-title { font-size: clamp(28px, 10vw, 42px) !important; }
  .pp-badges { grid-template-columns: repeat(3, 1fr); }
  .pp-stat-num { font-size: 18px; }
}
"""

content = content.replace(MARKER, MOBILE_CSS + "\n" + MARKER)

# Inject hamburger button into header + overlay at body end
NAV_MARKER = """  <ul class="tabbed-primary-navigation">"""

HAMB_HTML = """  <button class="hamburger-btn" id="hamburgerBtn" aria-label="תפריט">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><line x1="4" y1="6" x2="20" y2="6"/><line x1="4" y1="12" x2="20" y2="12"/><line x1="4" y1="18" x2="20" y2="18"/></svg>
  </button>

  <ul class="tabbed-primary-navigation">"""

if NAV_MARKER not in content:
    print("ERROR: nav marker not found", file=sys.stderr); sys.exit(1)
content = content.replace(NAV_MARKER, HAMB_HTML)

# Overlay markup + closing, right before closing </body>
OVERLAY = """
<div class="mobile-nav-overlay" id="mobileNavOverlay">
  <button class="mobile-nav-close" id="mobileNavClose" aria-label="סגור">✕</button>
  <a href="#" data-nav="home" class="current">דף הבית</a>
  <a href="#" data-nav="courses">קורסים</a>
  <a href="#" data-nav="new">חדשים</a>
  <a href="#" data-nav="mylist">הרשימה שלי</a>
  <a href="#" data-nav="search">חיפוש לפי נושא</a>
</div>
"""

BODY_END = "</body>"
content = content.replace(BODY_END, OVERLAY + BODY_END)

# Append hamburger JS at end of script
JS_MARKER = "setTimeout(buildLeaderboardRow, 2000);"
JS_NEW = JS_MARKER + """

/* ═══════════════════════════════════════════
   COMMIT 9 · Hamburger + mobile overlay
   ═══════════════════════════════════════════ */
document.addEventListener('click', (e) => {
  const hb = e.target.closest('#hamburgerBtn');
  const overlay = document.getElementById('mobileNavOverlay');
  if (hb && overlay) { overlay.classList.add('open'); return; }
  const close = e.target.closest('#mobileNavClose');
  if (close && overlay) { overlay.classList.remove('open'); return; }
  // Click link inside overlay → filter + close
  const link = e.target.closest('.mobile-nav-overlay a[data-nav]');
  if (link && overlay) {
    e.preventDefault();
    document.querySelectorAll('.mobile-nav-overlay a').forEach(a => a.classList.remove('current'));
    link.classList.add('current');
    // Sync desktop tabs
    document.querySelectorAll('.navigation-tab a').forEach(a => a.classList.toggle('current', a.dataset.nav === link.dataset.nav));
    applyNavFilter(link.dataset.nav);
    overlay.classList.remove('open');
  }
});"""

if JS_MARKER not in content:
    print("ERROR: JS marker not found", file=sys.stderr); sys.exit(1)
content = content.replace(JS_MARKER, JS_NEW)

TARGET.write_text(content, encoding='utf-8')
print(f"OK: commit 9 applied. Size: {len(content)} bytes")
