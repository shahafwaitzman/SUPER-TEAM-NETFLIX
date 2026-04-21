#!/usr/bin/env python3
"""Unify navigation bar across all projects.
- Academy pages: logo says "ACADEMY"
- Flow-viewer: logo says "FLOW"
- Retention (Next.js): logo says "רטנשן"

Shared pattern: SUPER TEAM (small, white) ↓ thin line ↓ BRAND (large, red)
Uniform nav: logo left · [← back] [🏠 home] center-left · [hamburger] [profile?] right
"""
import re, sys, os
from pathlib import Path

ACADEMY_DIR = Path("/Users/shahafwaitzman/Documents/CLOUD CODE/super-team-academy")
FLOW_DIR    = Path("/Users/shahafwaitzman/Documents/CLOUD CODE/flow-viewer")

# Project-specific brand word
BRAND_MAP = {
    ACADEMY_DIR / "entry.html":         "ACADEMY",
    ACADEMY_DIR / "access.html":        "ACADEMY",
    ACADEMY_DIR / "register.html":      "ACADEMY",
    ACADEMY_DIR / "confirmation.html":  "ACADEMY",
    ACADEMY_DIR / "approve.html":       "ACADEMY",
    ACADEMY_DIR / "dashboard.html":     "ACADEMY",
    ACADEMY_DIR / "academy-hub.html":   "ACADEMY",
    ACADEMY_DIR / "admin.html":         "ACADEMY",
    FLOW_DIR    / "index.html":         "FLOW",
}

# Shared logo HTML pattern (replaces logo content everywhere consistently)
def logo_html(brand_word):
    return f'''<a href="entry.html" class="logo st-logo" aria-label="Super Team {brand_word}">
    <span class="logo-super">SUPER TEAM</span>
    <span class="logo-line"></span>
    <span class="logo-academy">{brand_word}</span>
  </a>'''

# ════════════════════════════════════════════════
# Standalone shared logo CSS — prefixed .st-logo override so we don't conflict
# ════════════════════════════════════════════════
SHARED_CSS = '''
/* ═════ Shared Super Team Nav (unified across projects) ═════ */
.st-nav-root {
  position: fixed; top: 0; left: 0; right: 0;
  z-index: 1000; height: 68px;
  display: flex; align-items: center;
  padding: 0 4%;
  gap: 12px;
  background: linear-gradient(180deg, rgba(0,0,0,0.95) 0%, rgba(0,0,0,0.7) 70%, transparent 100%);
  font-family: 'Heebo', 'Segoe UI', Arial, sans-serif;
}
.st-logo {
  display: inline-flex; flex-direction: column;
  align-items: center; justify-content: center;
  text-decoration: none; user-select: none;
  line-height: 1;
  flex-shrink: 0;
}
.st-logo .logo-super {
  font-family: 'Bebas Neue', 'Heebo', sans-serif;
  font-weight: 900; font-size: 11px;
  color: #fff; letter-spacing: 2px;
}
.st-logo .logo-line {
  width: 44px; height: 1.5px;
  background: linear-gradient(to right, transparent 0%, #fff 50%, transparent 100%);
  margin: 4px 0; border-radius: 2px;
  box-shadow: 0 0 6px rgba(255,255,255,0.5);
}
.st-logo .logo-academy {
  font-family: 'Bebas Neue', 'Heebo', sans-serif;
  font-weight: 900; font-size: 18px;
  color: #E50914; letter-spacing: 1.5px;
  text-shadow: 0 2px 8px rgba(229,9,20,0.5);
}

/* Uniform action buttons */
.st-btn {
  display: inline-flex; align-items: center; gap: 6px;
  padding: 8px 14px;
  border-radius: 6px;
  background: rgba(255,255,255,0.06);
  border: 1px solid rgba(255,255,255,0.1);
  color: rgba(255,255,255,0.9);
  font-family: inherit; font-size: 12.5px; font-weight: 700;
  cursor: pointer; text-decoration: none;
  transition: all 0.2s;
  white-space: nowrap;
}
.st-btn:hover {
  background: rgba(229,9,20,0.18);
  border-color: rgba(229,9,20,0.5);
  color: #fff;
}
.st-btn.primary {
  background: linear-gradient(135deg, #E50914, #B9090B);
  border-color: transparent;
  color: #fff;
}
.st-btn.primary:hover { transform: translateY(-1px); box-shadow: 0 4px 12px rgba(229,9,20,0.4); }
.st-btn svg { width: 14px; height: 14px; fill: currentColor; }

.st-nav-spacer { flex: 1; }

.st-hamburger {
  width: 40px; height: 40px;
  display: none; align-items: center; justify-content: center;
  background: transparent;
  border: 1px solid rgba(255,255,255,0.15);
  border-radius: 6px;
  color: #fff; cursor: pointer;
  font-family: inherit;
  padding: 0;
}
.st-hamburger svg { width: 20px; height: 20px; }

.st-mobile-menu {
  display: none;
  position: fixed; top: 68px;
  inset-inline-start: 0; inset-inline-end: 0;
  background: rgba(0,0,0,0.96);
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
  z-index: 999;
  padding: 16px;
  flex-direction: column; gap: 8px;
  border-bottom: 1px solid rgba(255,255,255,0.08);
  animation: stSlideDown 0.25s ease;
}
@keyframes stSlideDown {
  from { transform: translateY(-10px); opacity: 0; }
  to { transform: translateY(0); opacity: 1; }
}
.st-mobile-menu.open { display: flex; }
.st-mobile-menu a { padding: 14px; }

@media (max-width: 768px) {
  .st-nav-root { padding: 0 4%; height: 60px; }
  .st-mobile-menu { top: 60px; }
  .st-desktop-only { display: none !important; }
  .st-hamburger { display: inline-flex; }
  .st-logo .logo-academy { font-size: 16px; }
  .st-logo .logo-super { font-size: 10px; }
}

/* Offset body content so fixed nav doesn't overlap */
body.st-nav-installed { padding-top: 0; }
/* ═════ /Shared Super Team Nav ═════ */
'''


def patch_logo(html, brand_word):
    """Replace existing logo <a class="logo">...</a> block with branded version."""
    # Find and replace the logo span structure
    # Common patterns:
    # <a ... class="logo"...>...SUPER TEAM...ACADEMY...</a>
    new_logo = logo_html(brand_word)
    # Generic replacement: any <a> with class containing "logo" that wraps logo-super etc.
    pattern = re.compile(
        r'<a\s+[^>]*class="[^"]*\blogo\b[^"]*"[^>]*>\s*(?:<[^>]+>\s*)*?\s*<span[^>]*class="logo-super"[^>]*>.*?</a>',
        re.DOTALL
    )
    if pattern.search(html):
        return pattern.sub(new_logo, html), True
    # Fallback — sometimes logo is just div
    pattern2 = re.compile(
        r'<div\s+class="logo[^"]*"[^>]*>\s*<span[^>]*logo-super[^>]*>.*?</div>',
        re.DOTALL
    )
    if pattern2.search(html):
        return pattern2.sub(new_logo, html), True
    return html, False


def ensure_shared_css(html):
    """Inject shared CSS once into <style> block if not already present."""
    if '.st-logo' in html and '.st-nav-root' in html:
        return html, False
    # Inject before closing </style> of the last style block
    idx = html.rfind('</style>')
    if idx < 0:
        # No style block — inject in <head>
        head_end = html.find('</head>')
        if head_end < 0: return html, False
        return html[:head_end] + f'<style>{SHARED_CSS}</style>\n' + html[head_end:], True
    return html[:idx] + SHARED_CSS + html[idx:], True


def process_file(path, brand):
    try:
        html = path.read_text(encoding='utf-8')
    except Exception as e:
        print(f"  ✗ {path.name}: read error {e}")
        return
    orig_len = len(html)
    html, logo_changed = patch_logo(html, brand)
    html, css_added = ensure_shared_css(html)

    # Also make sure logo color variable matches (some files use var(--nflx-red))
    # Our shared CSS uses #E50914 directly — no mods needed.

    if logo_changed or css_added:
        path.write_text(html, encoding='utf-8')
        print(f"  ✓ {path.name:28s} logo:{'✓' if logo_changed else '-'} css:{'✓' if css_added else '-'}  ({len(html)-orig_len:+d}B)")
    else:
        print(f"  · {path.name:28s} no changes (logo pattern not found)")


# ════════════════════════════════════════════════
print("═════════════════════════════════════════════")
print("  Unifying logos + shared nav")
print("═════════════════════════════════════════════")
for path, brand in BRAND_MAP.items():
    if not path.exists():
        print(f"  ✗ {path.name} not found"); continue
    process_file(path, brand)
print("═════════════════════════════════════════════")
print("Done.")
