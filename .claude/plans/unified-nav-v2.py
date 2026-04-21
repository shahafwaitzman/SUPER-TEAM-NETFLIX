#!/usr/bin/env python3
"""Phase 4 Stage A: Unified nav bar across academy + flow-viewer.

Design (RTL):
  [← קודם] [🏠 דף הבית]    ...tabs/filler...    [🔔] [👤 S]    ┌LOGO┐
                                                  [☰ המבורגר]   └────┘

- Logo always rightmost (RTL visual end)
- Click logo → project's main screen
- Hamburger menu → cross-project switcher + logout
- Back button → history.back() with fallback
- Home button → dashboard.html (super-team main dashboard)
- Uniform font (Heebo body, Bebas Neue logos)
- Uniform color palette (#141414 / #E50914 / white)
"""
import re, sys
from pathlib import Path

ACADEMY = Path("/Users/shahafwaitzman/Documents/CLOUD CODE/super-team-academy")
FLOW    = Path("/Users/shahafwaitzman/Documents/CLOUD CODE/flow-viewer")

# Pages to unify — (path, brand_word, logo_click_dest)
TARGETS = [
    (ACADEMY / "entry.html",         "ACADEMY", "entry.html"),
    (ACADEMY / "access.html",        "ACADEMY", "entry.html"),
    (ACADEMY / "register.html",      "ACADEMY", "entry.html"),
    (ACADEMY / "confirmation.html",  "ACADEMY", "entry.html"),
    (ACADEMY / "approve.html",       "ACADEMY", "admin.html"),
    (ACADEMY / "dashboard.html",     "ACADEMY", "dashboard.html"),
    (ACADEMY / "academy-hub.html",   "ACADEMY", "academy-hub.html"),
    (ACADEMY / "admin.html",         "ACADEMY", "admin.html"),
]

# Cross-project switcher URLs (deployed URLs)
PROJECTS = {
    "academy":   "https://superteamhlf.team/dashboard.html",
    "flow":      "https://flow-argoni.netlify.app/",
    "retention": "https://herbalife-retention-uwog.vercel.app/dashboard",
    "logout":    "https://superteamhlf.team/entry.html",
}

SHARED_CSS_V2 = '''
/* ═════ Super Team Unified Nav v2 ═════ */
:root {
  --stn-bg:      #141414;
  --stn-red:     #E50914;
  --stn-border:  rgba(255,255,255,0.08);
  --stn-hover:   rgba(229,9,20,0.15);
  --stn-text:    rgba(255,255,255,0.92);
  --stn-muted:   rgba(255,255,255,0.55);
}
body.stn-installed { padding-top: 68px; margin: 0; }
body.stn-installed.stn-overlay { padding-top: 0; }

.stn-bar {
  position: fixed; top: 0; left: 0; right: 0;
  z-index: 1000;
  height: 68px;
  display: flex; align-items: center;
  gap: 10px;
  padding: 0 4%;
  background: linear-gradient(180deg, rgba(0,0,0,0.95) 0%, rgba(0,0,0,0.7) 70%, transparent 100%);
  font-family: 'Heebo', 'Segoe UI', Arial, sans-serif;
  direction: rtl;
}
.stn-bar.scrolled {
  background: rgba(10,10,10,0.92);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  box-shadow: 0 2px 20px rgba(0,0,0,0.4);
}

/* Logo — always on the right (RTL start = right) */
.stn-logo {
  order: 0;
  display: inline-flex; flex-direction: column;
  align-items: center; justify-content: center;
  text-decoration: none; user-select: none;
  line-height: 1; flex-shrink: 0;
  padding: 6px 0;
}
.stn-logo .stn-logo-super {
  font-family: 'Bebas Neue', 'Heebo', sans-serif;
  font-weight: 900; font-size: 11px;
  color: #fff; letter-spacing: 2.2px;
  text-shadow: 0 1px 3px rgba(0,0,0,0.7);
}
.stn-logo .stn-logo-line {
  width: 44px; height: 1.5px;
  background: linear-gradient(to right, transparent 0%, #fff 50%, transparent 100%);
  margin: 3px 0; border-radius: 2px;
  box-shadow: 0 0 6px rgba(255,255,255,0.45);
}
.stn-logo .stn-logo-brand {
  font-family: 'Bebas Neue', 'Heebo', sans-serif;
  font-weight: 900; font-size: 19px;
  color: var(--stn-red); letter-spacing: 1.6px;
  text-shadow: 0 2px 8px rgba(229,9,20,0.5);
}
.stn-logo:hover .stn-logo-brand { text-shadow: 0 2px 12px rgba(229,9,20,0.75); }

/* Spacer that pushes action buttons all the way to the visual left */
.stn-spacer { flex: 1; }

/* Action buttons group (hamburger + icons + profile) */
.stn-actions {
  display: inline-flex; align-items: center; gap: 8px;
  order: 2;
}

.stn-btn {
  display: inline-flex; align-items: center; gap: 6px;
  padding: 8px 14px;
  border-radius: 7px;
  background: rgba(255,255,255,0.04);
  border: 1px solid var(--stn-border);
  color: var(--stn-text);
  font-family: inherit; font-size: 12.5px; font-weight: 700;
  cursor: pointer; text-decoration: none;
  transition: all 0.2s;
  white-space: nowrap;
}
.stn-btn:hover {
  background: var(--stn-hover);
  border-color: rgba(229,9,20,0.5);
  color: #fff;
}
.stn-btn svg { width: 14px; height: 14px; fill: currentColor; }

.stn-icon-btn {
  width: 40px; height: 40px;
  display: inline-flex; align-items: center; justify-content: center;
  border-radius: 50%;
  background: transparent;
  border: 1px solid var(--stn-border);
  color: var(--stn-text);
  cursor: pointer;
  transition: all 0.2s;
  font-family: inherit; padding: 0;
  position: relative;
}
.stn-icon-btn:hover {
  background: var(--stn-hover); border-color: var(--stn-red); color: #fff;
}
.stn-icon-btn svg { width: 18px; height: 18px; fill: currentColor; }

/* Hamburger dropdown */
.stn-ham-wrap { position: relative; }
.stn-ham-menu {
  position: absolute;
  top: calc(100% + 10px);
  inset-inline-end: 0;
  min-width: 240px;
  background: rgba(18,18,18,0.98);
  backdrop-filter: blur(18px);
  -webkit-backdrop-filter: blur(18px);
  border: 1px solid var(--stn-border);
  border-radius: 10px;
  box-shadow: 0 18px 40px rgba(0,0,0,0.6);
  padding: 8px 0;
  display: none; flex-direction: column;
  z-index: 1100;
  animation: stnSlideIn 0.2s ease;
}
@keyframes stnSlideIn {
  from { opacity: 0; transform: translateY(-8px); }
  to { opacity: 1; transform: translateY(0); }
}
.stn-ham-menu.open { display: flex; }
.stn-ham-header {
  font-size: 10px; font-weight: 800;
  color: var(--stn-muted);
  text-transform: uppercase; letter-spacing: 1.4px;
  padding: 10px 18px 6px;
}
.stn-ham-link {
  display: flex; align-items: center; gap: 12px;
  padding: 12px 18px;
  color: #fff;
  font-size: 13px; font-weight: 700;
  text-decoration: none;
  transition: background 0.15s;
  border: none; background: transparent;
  font-family: inherit; text-align: right;
  cursor: pointer; width: 100%;
}
.stn-ham-link:hover { background: var(--stn-hover); }
.stn-ham-link.active {
  background: rgba(229,9,20,0.2);
  border-inline-end: 3px solid var(--stn-red);
}
.stn-ham-link-brand {
  font-family: 'Bebas Neue', 'Heebo', sans-serif;
  font-size: 13px; letter-spacing: 1.5px;
  color: var(--stn-red);
  margin-inline-start: auto;
}
.stn-ham-divider {
  height: 1px;
  background: var(--stn-border);
  margin: 6px 0;
}

/* Back + home buttons — on the visual left (RTL end) */
.stn-nav-left {
  display: inline-flex; align-items: center; gap: 8px;
  order: 1;
}

/* Responsive */
@media (max-width: 900px) {
  .stn-bar { gap: 6px; padding: 0 14px; height: 60px; }
  body.stn-installed { padding-top: 60px; }
  .stn-btn-label { display: none; }
  .stn-btn { padding: 8px 10px; }
  .stn-logo .stn-logo-brand { font-size: 16px; }
  .stn-logo .stn-logo-super { font-size: 10px; }
}
@media (max-width: 480px) {
  .stn-bar { padding: 0 8px; }
  .stn-actions { gap: 4px; }
}

/* Legacy logo rules override — force consistent brand color even where
   legacy pages used different colors */
.stn-installed .logo-academy,
.stn-installed .st-logo .logo-academy {
  color: var(--stn-red) !important;
}
/* ═════ /Unified Nav v2 ═════ */
'''


def nav_html(brand, logo_href, active_project="academy"):
    """Build the unified nav bar HTML."""
    brand_upper = brand.upper()
    ham_active = {"academy": "", "flow": "", "retention": ""}
    ham_active[active_project] = "active"

    return f'''<div class="stn-bar" id="stnBar">
  <a href="{logo_href}" class="stn-logo" aria-label="Super Team {brand_upper}">
    <span class="stn-logo-super">SUPER TEAM</span>
    <span class="stn-logo-line"></span>
    <span class="stn-logo-brand">{brand_upper}</span>
  </a>

  <div class="stn-spacer"></div>

  <div class="stn-actions">
    <button type="button" class="stn-btn" onclick="window.history.length>1?window.history.back():window.location.href='dashboard.html'" aria-label="חזור למסך הקודם">
      <svg viewBox="0 0 24 24"><path d="M15.59 18.41L10.17 13 15.59 7.59 14 6l-7 7 7 7z"/></svg>
      <span class="stn-btn-label">קודם</span>
    </button>
    <a href="{PROJECTS['academy']}" class="stn-btn" aria-label="דף הבית">
      <svg viewBox="0 0 24 24"><path d="M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z"/></svg>
      <span class="stn-btn-label">דף הבית</span>
    </a>

    <div class="stn-ham-wrap">
      <button type="button" class="stn-icon-btn" id="stnHamBtn" aria-label="תפריט">
        <svg viewBox="0 0 24 24"><path d="M3 6h18v2H3zm0 5h18v2H3zm0 5h18v2H3z"/></svg>
      </button>
      <div class="stn-ham-menu" id="stnHamMenu" role="menu">
        <div class="stn-ham-header">מערכות סופר טים</div>
        <a href="{PROJECTS['academy']}" class="stn-ham-link {ham_active['academy']}" role="menuitem">
          <span>אקדמיה</span>
          <span class="stn-ham-link-brand">ACADEMY</span>
        </a>
        <a href="{PROJECTS['flow']}" class="stn-ham-link {ham_active['flow']}" role="menuitem">
          <span>פלואו עסקי</span>
          <span class="stn-ham-link-brand">FLOW</span>
        </a>
        <a href="{PROJECTS['retention']}" class="stn-ham-link {ham_active['retention']}" role="menuitem" target="_blank" rel="noopener">
          <span>שימור לקוחות</span>
          <span class="stn-ham-link-brand">RETENTION</span>
        </a>
        <div class="stn-ham-divider"></div>
        <button type="button" class="stn-ham-link" onclick="(function(){{try{{localStorage.removeItem('userEmail');localStorage.removeItem('userEmailSavedAt');}}catch(e){{}}window.location.href='{PROJECTS['logout']}';}})()" role="menuitem">
          <svg viewBox="0 0 24 24" width="14" height="14" fill="currentColor"><path d="M17 8l-1.41 1.41L17.17 11H9v2h8.17l-1.58 1.58L17 16l4-4zM5 5h7V3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h7v-2H5z"/></svg>
          <span>יציאה</span>
        </button>
      </div>
    </div>
  </div>
</div>
'''

STN_JS = '''
<script>
/* Super Team Nav — shared runtime */
(function() {
  document.body.classList.add('stn-installed');
  // Scroll shadow
  window.addEventListener('scroll', function() {
    const bar = document.getElementById('stnBar');
    if (bar) bar.classList.toggle('scrolled', window.scrollY > 20);
  });
  // Hamburger toggle
  document.addEventListener('click', function(e) {
    const btn = e.target.closest('#stnHamBtn');
    const menu = document.getElementById('stnHamMenu');
    if (btn && menu) {
      e.stopPropagation();
      menu.classList.toggle('open');
      return;
    }
    if (menu && menu.classList.contains('open') && !e.target.closest('.stn-ham-wrap')) {
      menu.classList.remove('open');
    }
  });
  document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
      const menu = document.getElementById('stnHamMenu');
      if (menu) menu.classList.remove('open');
    }
  });
})();
</script>
'''


def inject_nav(html, brand, logo_href):
    """Inject shared CSS + nav + JS. Remove legacy nav if it conflicts."""
    # 1. Inject CSS before last </style>
    if '.stn-bar' not in html:
        idx = html.rfind('</style>')
        if idx > 0:
            html = html[:idx] + SHARED_CSS_V2 + html[idx:]
        else:
            head_end = html.find('</head>')
            if head_end > 0:
                html = html[:head_end] + f'<style>{SHARED_CSS_V2}</style>\n' + html[head_end:]

    # 2. Remove OLD .st-nav-root blocks if present (from previous unify pass)
    html = re.sub(
        r'<div class="st-nav-root">.*?</div>\s*<div style="height:68px"></div>',
        '', html, flags=re.DOTALL)

    # 3. Remove existing <body>\n... anything until the main content — insert nav right after <body>
    new_nav = nav_html(brand, logo_href)

    # Insert nav right after <body>
    body_match = re.search(r'<body[^>]*>', html)
    if not body_match:
        return html, False
    body_end = body_match.end()

    # Check if nav already inserted
    if '<div class="stn-bar"' in html:
        # Replace existing stn-bar with new one (update logo target, etc.)
        html = re.sub(
            r'<div class="stn-bar"[^>]*>.*?</div>\s*</div>\s*</div>',
            new_nav.rstrip(), html, count=1, flags=re.DOTALL
        )
    else:
        html = html[:body_end] + '\n' + new_nav + html[body_end:]

    # 4. Inject runtime JS before </body>
    if '/* Super Team Nav — shared runtime */' not in html:
        html = html.replace('</body>', STN_JS + '</body>', 1)

    return html, True


# ════════════════════════════════════════════════
print("═════════════════════════════════════════════")
print("  Unified Nav v2 — installing across projects")
print("═════════════════════════════════════════════")
total = 0
for path, brand, logo_href in TARGETS:
    if not path.exists():
        print(f"  ✗ {path.name} not found"); continue
    html = path.read_text(encoding='utf-8')
    orig_len = len(html)
    html, ok = inject_nav(html, brand, logo_href)
    if ok:
        path.write_text(html, encoding='utf-8')
        print(f"  ✓ {path.name:28s}  ({len(html) - orig_len:+d}B)")
        total += 1
    else:
        print(f"  · {path.name:28s}  no <body> found")

# flow-viewer — special handling (has its own nav that we keep + wrap)
flow_file = FLOW / "index.html"
if flow_file.exists():
    html = flow_file.read_text(encoding='utf-8')
    # flow-viewer already has its <nav> — we'll add stn-bar ABOVE it
    # First, remove the previous .st-logo injection since we're replacing with stn-bar
    html = re.sub(
        r'<a[^>]*class="[^"]*\bst-logo\b[^"]*"[^>]*>.*?</a>',
        '', html, flags=re.DOTALL, count=1)
    orig_len = len(html)
    html, ok = inject_nav(html, "FLOW", "/")
    if ok:
        flow_file.write_text(html, encoding='utf-8')
        print(f"  ✓ flow-viewer/index.html      ({len(html) - orig_len:+d}B)")
        total += 1

print("═════════════════════════════════════════════")
print(f"Done — {total} files updated")
