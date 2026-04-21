#!/usr/bin/env python3
"""Fix nav duplication:
- academy-hub.html has both old .main-header AND new .stn-bar → remove old
- flow-viewer index.html has old <nav id="navbar"> AND new .stn-bar → merge into one
- approve.html / admin.html have old header + new stn-bar → remove old minimal one
- academy dashboard has old .main-header + stn-bar → remove old
"""
import re
from pathlib import Path

def strip_old_nav(html, patterns):
    """Remove old nav elements matching any of the given patterns."""
    for pat in patterns:
        html = re.sub(pat, '', html, flags=re.DOTALL)
    return html

# ─── academy-hub.html ──────────────────────────────────
p = Path("/Users/shahafwaitzman/Documents/CLOUD CODE/super-team-academy/academy-hub.html")
c = p.read_text(encoding='utf-8')
# Remove the old <div class="main-header" id="mainHeader" ...> ... </div>
c = re.sub(
    r'<div class="main-header" id="mainHeader"[^>]*>.*?</div>\s*(?=<section class="billboard-row")',
    '',
    c, flags=re.DOTALL, count=1
)
p.write_text(c, encoding='utf-8')
print("✓ academy-hub.html — removed old main-header")

# ─── flow-viewer/index.html ──────────────────────────────────
p = Path("/Users/shahafwaitzman/Documents/CLOUD CODE/flow-viewer/index.html")
c = p.read_text(encoding='utf-8')
# Extract the filter-tabs row from old <nav> and embed them into stn-bar
# First grab the nav-links content
m = re.search(r'<nav id="navbar"[^>]*>(.*?)</nav>', c, re.DOTALL)
if m:
    old_nav_content = m.group(1)
    # Find just the nav-link buttons
    tab_buttons = re.findall(r'<button class="nav-link[^>]*?>.*?</button>', old_nav_content, re.DOTALL)
    tabs_html = '\n    '.join(tab_buttons)
    # Remove the old <nav> entirely
    c = re.sub(r'<nav id="navbar"[^>]*>.*?</nav>', '', c, flags=re.DOTALL, count=1)
    # Inject the tab buttons into the stn-bar between spacer and actions.
    # Create a tabs container and insert it.
    tabs_block = f'''<div class="stn-flow-tabs">
    {tabs_html}
  </div>
'''
    # Put tabs right after .stn-spacer in the stn-bar
    c = c.replace(
        '<div class="stn-spacer"></div>',
        '<div class="stn-spacer"></div>\n  ' + tabs_block,
        1
    )
    # Add CSS for tabs so they fit nicely in the bar
    tab_css = '''
/* FLOW — inline tabs in stn-bar */
.stn-flow-tabs {
  display: flex; gap: 4px;
  order: 1;
}
.stn-flow-tabs .nav-link {
  padding: 7px 12px;
  border-radius: 7px;
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.08);
  color: rgba(255,255,255,0.92);
  font-family: inherit; font-size: 12.5px; font-weight: 700;
  cursor: pointer;
  transition: all 0.2s;
  white-space: nowrap;
}
.stn-flow-tabs .nav-link:hover {
  background: rgba(229,9,20,0.15);
  border-color: rgba(229,9,20,0.5);
}
.stn-flow-tabs .nav-link.active {
  background: var(--stn-red, #E50914);
  border-color: var(--stn-red, #E50914);
  color: #fff;
  box-shadow: 0 4px 14px rgba(229,9,20,0.4);
}
@media (max-width: 900px) {
  .stn-flow-tabs { overflow-x: auto; scrollbar-width: none; flex: 1; }
  .stn-flow-tabs::-webkit-scrollbar { display: none; }
  .stn-flow-tabs .nav-link { padding: 6px 10px; font-size: 12px; flex-shrink: 0; }
}
'''
    if '.stn-flow-tabs' not in c:
        # inject before last </style>
        idx = c.rfind('</style>')
        if idx > 0:
            c = c[:idx] + tab_css + c[idx:]
    p.write_text(c, encoding='utf-8')
    print("✓ flow-viewer/index.html — merged tabs into stn-bar")

# ─── academy dashboard.html ──────────────────────────────────
p = Path("/Users/shahafwaitzman/Documents/CLOUD CODE/super-team-academy/dashboard.html")
c = p.read_text(encoding='utf-8')
# Remove old <div class="main-header"...>...</div>
c = re.sub(
    r'<div class="main-header"[^>]*>.*?</div>\s*\n',
    '', c, flags=re.DOTALL, count=1
)
# Also remove the "חזור למסך הכניסה" old button if leftover
p.write_text(c, encoding='utf-8')
print("✓ dashboard.html — cleaned")

# ─── approve.html + admin.html — they had minimal <div class="st-nav-root"> ──────
# These were injected earlier and now duplicate with stn-bar. Remove st-nav-root.
for fn in ["approve.html", "admin.html"]:
    p = Path(f"/Users/shahafwaitzman/Documents/CLOUD CODE/super-team-academy/{fn}")
    c = p.read_text(encoding='utf-8')
    # Strip the earlier st-nav-root block (from unify-nav.py, phase pre-v2)
    c = re.sub(
        r'<div class="st-nav-root">.*?</div>\s*<div style="height:68px"></div>',
        '', c, flags=re.DOTALL
    )
    p.write_text(c, encoding='utf-8')
    print(f"✓ {fn} — cleaned duplicate nav")
