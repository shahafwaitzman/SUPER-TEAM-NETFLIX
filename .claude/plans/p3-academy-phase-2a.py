#!/usr/bin/env python3
"""P3 · Phase 2A · academy-hub.html bug fixes:
  1. Black card bug → img.onerror → placeholder (gradient + S + title)
  2. Hero text legibility → RTL dark scrim
  3. Hero fade-to-black at bottom
"""
import sys
from pathlib import Path

TARGET = Path("/Users/shahafwaitzman/Documents/CLOUD CODE/super-team-academy/academy-hub.html")
content = TARGET.read_text(encoding='utf-8')

# === Fix #2 + #3: Add new hero overlay divs ===
OLD_HERO_HTML = '''  <div class="hero-image-wrapper">
    <div class="hero-image"></div>
    <div class="trailer-vignette"></div>
    <div class="hero-vignette"></div>
  </div>'''

NEW_HERO_HTML = '''  <div class="hero-image-wrapper">
    <div class="hero-image"></div>
    <div class="trailer-vignette"></div>
    <div class="hero-vignette"></div>
    <div class="hero-rtl-scrim" aria-hidden="true"></div>
    <div class="hero-bottom-fade" aria-hidden="true"></div>
  </div>'''

if OLD_HERO_HTML not in content:
    print("ERROR: hero HTML block not found", file=sys.stderr); sys.exit(1)
content = content.replace(OLD_HERO_HTML, NEW_HERO_HTML)

# === Fix #1: Card rendering — use <img> with onerror → placeholder ===
OLD_CARD = """            <div class="boxart-container">
              <div class="boxart-image ${thumbnail ? '' : boxartClass}" style="${thumbStyle}">
                ${thumbnail ? '' : `<span class="boxart-label">${escapeHtml(title)}</span>`}
              </div>
            </div>"""

NEW_CARD = """            <div class="boxart-container">
              <div class="boxart-image ${thumbnail ? '' : 'no-thumb'}">
                ${thumbnail ? `<img src="${thumbnail}" alt="${escapeHtml(title)}" loading="lazy" onerror="this.closest('.boxart-image').classList.add('no-thumb')">` : ''}
                <div class="boxart-fallback" aria-hidden="true">
                  <div class="boxart-fallback-logo">S</div>
                  <div class="boxart-fallback-title">${escapeHtml(title)}</div>
                </div>
              </div>
            </div>"""

if OLD_CARD not in content:
    print("ERROR: card template not found", file=sys.stderr); sys.exit(1)
content = content.replace(OLD_CARD, NEW_CARD)

# === Add new CSS for overlays + fallback (inject before the media query .billboard-row section) ===
CSS_INJECT_MARKER = """.trailer-vignette {
  position: absolute; inset: 0; z-index: 8;
  background: linear-gradient(-77deg, rgba(0,0,0,0.35), rgba(0,0,0,0) 70%);
  transition: opacity 0.5s;
}"""

CSS_NEW_BLOCK = """.trailer-vignette {
  position: absolute; inset: 0; z-index: 8;
  background: linear-gradient(-77deg, rgba(0,0,0,0.35), rgba(0,0,0,0) 70%);
  transition: opacity 0.5s;
}

/* ═══════════════════════════════════════════════
   PHASE 2A · Bug fixes (hero legibility + card fallback)
   ═══════════════════════════════════════════════ */

/* 2A-2: RTL text legibility — dark scrim on right side (where text sits in RTL) */
.hero-rtl-scrim {
  position: absolute; inset: 0; z-index: 9;
  background: linear-gradient(to left,
    rgba(20,20,20,0.95) 0%,
    rgba(20,20,20,0.6) 40%,
    transparent 100%);
  pointer-events: none;
}

/* 2A-3: Bottom fade-to-black — smooth transition to row background */
.hero-bottom-fade {
  position: absolute; inset: 0; z-index: 9;
  background: linear-gradient(to bottom,
    transparent 70%,
    #141414 100%);
  pointer-events: none;
}

/* 2A-1: Card thumbnail with fallback placeholder (#141414 → #E50914 + S logo + title) */
.boxart-image { position: relative; overflow: hidden; width: 100%; height: 100%; background: #141414; }
.boxart-image img {
  position: absolute; inset: 0;
  width: 100%; height: 100%;
  object-fit: cover;
  display: block;
  z-index: 2;
  background: #141414;
}
.boxart-fallback {
  position: absolute; inset: 0; z-index: 1;
  background:
    radial-gradient(ellipse 120% 90% at 60% 40%, rgba(229,9,20,0.28), transparent 70%),
    linear-gradient(135deg, #141414 0%, #3a0608 55%, #E50914 100%);
  display: flex; flex-direction: column;
  align-items: center; justify-content: center;
  padding: 14px; gap: 10px;
  text-align: center;
  color: #fff;
}
.boxart-image.no-thumb img { display: none; }
.boxart-image.no-thumb .boxart-fallback { z-index: 3; }
.boxart-fallback-logo {
  font-family: 'Heebo', 'Segoe UI', Arial, sans-serif;
  font-size: 52px; font-weight: 900;
  color: rgba(255,255,255,0.98);
  line-height: 1;
  letter-spacing: 2px;
  text-shadow: 0 4px 14px rgba(0,0,0,0.55);
  background: linear-gradient(135deg, #fff, #e5e5e5);
  -webkit-background-clip: text; background-clip: text;
  -webkit-text-fill-color: transparent;
}
.boxart-fallback-title {
  font-size: 12px; font-weight: 700;
  color: rgba(255,255,255,0.95);
  line-height: 1.3;
  max-height: 2.6em;
  overflow: hidden;
  text-shadow: 0 2px 6px rgba(0,0,0,0.55);
  padding: 0 4px;
}"""

if CSS_INJECT_MARKER not in content:
    print("ERROR: CSS marker not found", file=sys.stderr); sys.exit(1)
content = content.replace(CSS_INJECT_MARKER, CSS_NEW_BLOCK)

TARGET.write_text(content, encoding='utf-8')
print(f"OK: Phase 2A applied. Size: {len(content)} bytes")
