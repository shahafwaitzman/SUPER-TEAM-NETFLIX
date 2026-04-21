#!/usr/bin/env python3
"""Add subtle hero/flag background to ALL pages across all projects.

Strategy:
- Insert a body::before pseudo-element via CSS with the hero image
- Low opacity + dark overlay so text stays readable
- Doesn't interfere with existing layouts (uses z-index -1)
"""
import re, sys
from pathlib import Path

PAGES = [
    Path("/Users/shahafwaitzman/Documents/CLOUD CODE/super-team-academy/entry.html"),
    Path("/Users/shahafwaitzman/Documents/CLOUD CODE/super-team-academy/access.html"),
    Path("/Users/shahafwaitzman/Documents/CLOUD CODE/super-team-academy/register.html"),
    Path("/Users/shahafwaitzman/Documents/CLOUD CODE/super-team-academy/confirmation.html"),
    Path("/Users/shahafwaitzman/Documents/CLOUD CODE/super-team-academy/approve.html"),
    Path("/Users/shahafwaitzman/Documents/CLOUD CODE/super-team-academy/dashboard.html"),
    Path("/Users/shahafwaitzman/Documents/CLOUD CODE/super-team-academy/admin.html"),
    Path("/Users/shahafwaitzman/Documents/CLOUD CODE/super-team-academy/index.html"),
    Path("/Users/shahafwaitzman/Documents/CLOUD CODE/flow-viewer/index.html"),
]

BG_CSS = '''
/* ═════ Shared hero background (crowd + Israeli flag) ═════ */
body.stn-bg-hero {
  position: relative;
  background-color: #0a0a0a;
}
body.stn-bg-hero::before {
  content: '';
  position: fixed;
  inset: 0;
  background-image: url('hero.jpg');
  background-size: cover;
  background-position: center 30%;
  opacity: 0.35;
  z-index: -2;
  pointer-events: none;
  filter: contrast(1.05) saturate(1.1) brightness(0.9);
}
body.stn-bg-hero::after {
  content: '';
  position: fixed;
  inset: 0;
  background:
    radial-gradient(ellipse 80% 50% at 50% 30%, rgba(229,9,20,0.12), transparent 70%),
    linear-gradient(180deg, rgba(10,10,10,0.55) 0%, rgba(10,10,10,0.75) 45%, rgba(10,10,10,0.92) 100%);
  z-index: -1;
  pointer-events: none;
}
/* Skip hero bg on pages that already have their own dedicated hero (like academy-hub
   has its own billboard) — those opt-out by not adding the class */
/* ═════ /Shared hero background ═════ */
'''

def patch_file(path):
    if not path.exists():
        print(f"  ✗ {path.name}: missing"); return False
    c = path.read_text(encoding='utf-8')
    if 'stn-bg-hero' in c:
        print(f"  · {path.name}: already has hero bg"); return False

    # 1. Inject CSS into the last <style> block
    idx = c.rfind('</style>')
    if idx > 0:
        c = c[:idx] + BG_CSS + c[idx:]
    else:
        head_end = c.find('</head>')
        if head_end > 0:
            c = c[:head_end] + f'<style>{BG_CSS}</style>\n' + c[head_end:]

    # 2. Add the class to <body> — don't duplicate if already there
    c = re.sub(
        r'<body\b([^>]*)>',
        lambda m: (
            '<body' + m.group(1) + '>' if 'stn-bg-hero' in m.group(1)
            else ('<body class="stn-bg-hero"' + (m.group(1) if 'class=' not in m.group(1) else m.group(1).replace('class="', 'class="stn-bg-hero ')) + '>')
            if 'class=' not in m.group(1)
            else re.sub(r'class="([^"]*)"', r'class="stn-bg-hero \1"', '<body' + m.group(1) + '>')
        ),
        c, count=1
    )
    # Simpler approach — replace body manually
    if 'class="stn-bg-hero' not in c:
        # Check if <body> has a class attribute
        body_match = re.search(r'<body([^>]*)>', c)
        if body_match:
            existing = body_match.group(1)
            if 'class=' in existing:
                # Append to existing class
                new_body = re.sub(
                    r'class="([^"]*)"', r'class="stn-bg-hero \1"',
                    '<body' + existing + '>', count=1)
            else:
                new_body = '<body class="stn-bg-hero"' + existing + '>'
            c = c.replace(body_match.group(0), new_body, 1)

    path.write_text(c, encoding='utf-8')
    print(f"  ✓ {path.name}")
    return True

print("═════════════════════════════════════════════")
print("  Adding hero/flag background to all pages")
print("═════════════════════════════════════════════")
for p in PAGES:
    patch_file(p)
print("═════════════════════════════════════════════")
