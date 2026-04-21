#!/usr/bin/env python3
"""P3 Phase 2A refinement: diversify + soften card fallback placeholder.
  - Replace solid red gradient with deterministic palette of 8 cinematic gradients
  - Pass boxartClass to fallback so every card looks different
  - Replace giant 'S' with: play ▶ centered + SUPER·TEAM watermark + title
  - Add subtle dot pattern + radial highlight overlay
"""
import sys
from pathlib import Path

TARGET = Path("/Users/shahafwaitzman/Documents/CLOUD CODE/super-team-academy/academy-hub.html")
content = TARGET.read_text(encoding='utf-8')

# === 1. Replace existing boxart palette with refined cinematic gradients ===
OLD_PALETTE = """.boxart-1 { background: linear-gradient(135deg, #1a3a5c 0%, #0f1f33 100%); }
.boxart-2 { background: linear-gradient(135deg, #5c1a3a 0%, #330f1f 100%); }
.boxart-3 { background: linear-gradient(135deg, #3a5c1a 0%, #1f330f 100%); }
.boxart-4 { background: linear-gradient(135deg, #5c3a1a 0%, #331f0f 100%); }
.boxart-5 { background: linear-gradient(135deg, #3a1a5c 0%, #1f0f33 100%); }
.boxart-6 { background: linear-gradient(135deg, #1a5c5c 0%, #0f3333 100%); }
.boxart-7 { background: linear-gradient(135deg, #5c5c1a 0%, #33330f 100%); }
.boxart-8 { background: linear-gradient(135deg, #5c1a1a 0%, #330f0f 100%); }
.boxart-9 { background: linear-gradient(135deg, #2a2a5c 0%, #151533 100%); }
.boxart-10 { background: linear-gradient(135deg, #5c2a5c 0%, #331533 100%); }"""

NEW_PALETTE = """/* Refined cinematic palette — muted, low-saturation tones */
.boxart-1 { background: radial-gradient(ellipse 120% 90% at 75% 25%, rgba(255,255,255,0.1), transparent 55%), linear-gradient(135deg, #1e3a5f 0%, #0a1628 100%); }
.boxart-2 { background: radial-gradient(ellipse 120% 90% at 25% 25%, rgba(255,255,255,0.1), transparent 55%), linear-gradient(135deg, #1d4226 0%, #0a1f11 100%); }
.boxart-3 { background: radial-gradient(ellipse 120% 90% at 75% 25%, rgba(255,255,255,0.1), transparent 55%), linear-gradient(135deg, #3d1f4a 0%, #14081a 100%); }
.boxart-4 { background: radial-gradient(ellipse 120% 90% at 25% 25%, rgba(255,255,255,0.1), transparent 55%), linear-gradient(135deg, #4a2e1d 0%, #1f1207 100%); }
.boxart-5 { background: radial-gradient(ellipse 120% 90% at 75% 25%, rgba(255,255,255,0.1), transparent 55%), linear-gradient(135deg, #1a4244 0%, #0a1f20 100%); }
.boxart-6 { background: radial-gradient(ellipse 120% 90% at 25% 25%, rgba(255,255,255,0.1), transparent 55%), linear-gradient(135deg, #3d1a3d 0%, #1a0a1a 100%); }
.boxart-7 { background: radial-gradient(ellipse 120% 90% at 75% 25%, rgba(255,255,255,0.1), transparent 55%), linear-gradient(135deg, #2a3544 0%, #0f141b 100%); }
.boxart-8 { background: radial-gradient(ellipse 120% 90% at 25% 25%, rgba(255,255,255,0.1), transparent 55%), linear-gradient(135deg, #4a1a22 0%, #1f0a0d 100%); }
.boxart-9 { background: radial-gradient(ellipse 120% 90% at 75% 25%, rgba(255,255,255,0.1), transparent 55%), linear-gradient(135deg, #304a6b 0%, #0e1c2c 100%); }
.boxart-10 { background: radial-gradient(ellipse 120% 90% at 25% 25%, rgba(255,255,255,0.1), transparent 55%), linear-gradient(135deg, #2d2d4a 0%, #12122a 100%); }"""

if OLD_PALETTE not in content:
    print("ERROR: palette not found", file=sys.stderr); sys.exit(1)
content = content.replace(OLD_PALETTE, NEW_PALETTE)

# === 2. Replace .boxart-fallback block (lose solid red, add cinematic layered look) ===
OLD_FALLBACK_CSS = """.boxart-fallback {
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

NEW_FALLBACK_CSS = """.boxart-fallback {
  position: absolute; inset: 0; z-index: 1;
  display: grid;
  grid-template-rows: auto 1fr auto;
  padding: 12px 14px 14px;
  color: #fff;
  /* Dot-grid pattern overlay on top of card's gradient */
  background-image:
    radial-gradient(circle, rgba(255,255,255,0.04) 1px, transparent 1px);
  background-size: 14px 14px;
}
.boxart-image.no-thumb img { display: none; }
.boxart-image.no-thumb .boxart-fallback { z-index: 3; }

/* Watermark (top-right in LTR flow = visually "start" in RTL) */
.boxart-fallback-watermark {
  font-size: 9px; font-weight: 800;
  letter-spacing: 2px; text-transform: uppercase;
  color: rgba(255,255,255,0.42);
  line-height: 1;
  align-self: start; justify-self: start;
  padding: 3px 7px;
  border: 1px solid rgba(255,255,255,0.18);
  border-radius: 3px;
  backdrop-filter: blur(4px);
  -webkit-backdrop-filter: blur(4px);
}

/* Central play icon — the focal element */
.boxart-fallback-play {
  align-self: center; justify-self: center;
  width: 56px; height: 56px;
  border-radius: 50%;
  background: rgba(255,255,255,0.1);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1.5px solid rgba(255,255,255,0.28);
  display: flex; align-items: center; justify-content: center;
  color: rgba(255,255,255,0.88);
  box-shadow: 0 8px 24px rgba(0,0,0,0.35);
  transition: transform 0.3s, background 0.3s;
}
.boxart-fallback-play svg { width: 22px; height: 22px; margin-inline-start: 3px; }
.title-card-container:hover .boxart-fallback-play {
  background: rgba(255,255,255,0.2);
  transform: scale(1.1);
}

/* Title at bottom */
.boxart-fallback-title {
  font-size: 12px; font-weight: 700;
  color: rgba(255,255,255,0.96);
  line-height: 1.35;
  max-height: 2.7em;
  overflow: hidden;
  text-shadow: 0 2px 8px rgba(0,0,0,0.6);
  align-self: end;
  text-align: start;
}"""

if OLD_FALLBACK_CSS not in content:
    print("ERROR: old fallback CSS not found", file=sys.stderr); sys.exit(1)
content = content.replace(OLD_FALLBACK_CSS, NEW_FALLBACK_CSS)

# === 3. Update card rendering — add boxartClass to fallback, new content structure ===
OLD_CARD = """            <div class="boxart-container">
              <div class="boxart-image ${thumbnail ? '' : 'no-thumb'}">
                ${thumbnail ? `<img src="${thumbnail}" alt="${escapeHtml(title)}" loading="lazy" onerror="this.closest('.boxart-image').classList.add('no-thumb')">` : ''}
                <div class="boxart-fallback" aria-hidden="true">
                  <div class="boxart-fallback-logo">S</div>
                  <div class="boxart-fallback-title">${escapeHtml(title)}</div>
                </div>
              </div>
            </div>"""

NEW_CARD = """            <div class="boxart-container">
              <div class="boxart-image ${boxartClass} ${thumbnail ? '' : 'no-thumb'}">
                ${thumbnail ? `<img src="${thumbnail}" alt="${escapeHtml(title)}" loading="lazy" onerror="this.closest('.boxart-image').classList.add('no-thumb')">` : ''}
                <div class="boxart-fallback" aria-hidden="true">
                  <span class="boxart-fallback-watermark">SUPER·TEAM</span>
                  <div class="boxart-fallback-play">
                    <svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M5 2.7a1 1 0 0 1 1.48-.88l16.93 9.3a1 1 0 0 1 0 1.76l-16.93 9.3A1 1 0 0 1 5 21.31z"/></svg>
                  </div>
                  <div class="boxart-fallback-title">${escapeHtml(title)}</div>
                </div>
              </div>
            </div>"""

if OLD_CARD not in content:
    print("ERROR: card template not found", file=sys.stderr); sys.exit(1)
content = content.replace(OLD_CARD, NEW_CARD)

# === 4. Change boxartClass assignment: hash-based (deterministic per video id) instead of sequential ===
# Current: const boxartClass = boxartPalette[i % boxartPalette.length];
# New: hash the video id so same video always gets same color, and neighboring cards differ
OLD_ASSIGN = "    const boxartClass = boxartPalette[i % boxartPalette.length];"
NEW_ASSIGN = """    // Deterministic palette pick per video (hash of id + title — prevents neighbor color clashes)
    const _hashInput = (f.id || '') + '|' + title;
    let _h = 0;
    for (let _k = 0; _k < _hashInput.length; _k++) _h = ((_h << 5) - _h + _hashInput.charCodeAt(_k)) | 0;
    const boxartClass = boxartPalette[Math.abs(_h) % boxartPalette.length];"""

if OLD_ASSIGN not in content:
    print("ERROR: boxartClass assignment not found", file=sys.stderr); sys.exit(1)
content = content.replace(OLD_ASSIGN, NEW_ASSIGN)

TARGET.write_text(content, encoding='utf-8')
print(f"OK: Phase 2A refinement applied. Size: {len(content)} bytes")
