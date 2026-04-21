#!/usr/bin/env python3
"""P1 flow-viewer home redesign - step 2: inject Netflix-style CSS for home cards."""
import sys
from pathlib import Path

TARGET = Path("/Users/shahafwaitzman/Documents/CLOUD CODE/flow-viewer/index.html")

# Insert marker: right before the "/* ============ SECTION ============ */" block
MARKER = """.hero-stat .label {
  font-size: 11px; color: var(--text-dim); text-transform: uppercase;
  letter-spacing: 1px; margin-top: 4px;
}

/* ============ SECTION ============ */"""

CSS_BLOCK = """.hero-stat .label {
  font-size: 11px; color: var(--text-dim); text-transform: uppercase;
  letter-spacing: 1px; margin-top: 4px;
}

/* ============ HOME CARDS (Netflix-style) ============ */
.home-hero-content { max-width: 1400px; width: 100%; }
.home-hero-content h1 {
  font-size: clamp(34px, 5.4vw, 64px);
  margin-bottom: 14px;
}
.home-hero-content .hero-sub { margin-bottom: 40px; }

.home-cards {
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  gap: 18px;
  margin-top: 8px;
}
/* Row 1: featured FLOW card spans 6 cols (full width) */
.home-card-flow { grid-column: span 6; aspect-ratio: 24 / 7; }
/* Row 2: 4 cards, each span 3 → but we have 4 so each spans 3/2=1.5... use col 3 */
.home-card-meet,
.home-card-map,
.home-card-lib,
.home-card-profits { grid-column: span 3; aspect-ratio: 16 / 9; }

.home-card {
  position: relative;
  display: block;
  padding: 0;
  border-radius: 14px;
  border: 1px solid rgba(255,255,255,0.08);
  background: #1a1a1a;
  color: #fff;
  text-align: right;
  cursor: pointer;
  overflow: hidden;
  font-family: inherit;
  transition: transform 0.4s cubic-bezier(0.2, 0.8, 0.2, 1),
              border-color 0.3s, box-shadow 0.3s;
  isolation: isolate;
}
.home-card-bg {
  position: absolute; inset: 0; z-index: 0;
  background: var(--card-gradient, linear-gradient(135deg, #2a0a0a 0%, #0a0a0a 100%));
  transition: transform 0.6s cubic-bezier(0.2, 0.8, 0.2, 1);
}
.home-card-pattern {
  position: absolute; inset: 0; z-index: 1;
  background-image:
    radial-gradient(circle at 85% 15%, rgba(255,255,255,0.18), transparent 45%),
    radial-gradient(circle at 15% 90%, rgba(0,0,0,0.3), transparent 50%);
  pointer-events: none;
  transition: opacity 0.3s;
}
.home-card-overlay {
  position: absolute; inset: 0; z-index: 2;
  background: linear-gradient(180deg,
    rgba(0,0,0,0.1) 0%,
    rgba(0,0,0,0.2) 55%,
    rgba(0,0,0,0.72) 100%);
  transition: opacity 0.3s;
}
.home-card-inner {
  position: relative; z-index: 3;
  height: 100%;
  display: flex; flex-direction: column;
  padding: 26px 26px 22px;
}
.home-card-top {
  display: flex; align-items: flex-start; justify-content: space-between;
  gap: 16px;
  margin-bottom: auto;
}
.home-card-kicker {
  display: inline-block;
  padding: 5px 12px;
  border-radius: 20px;
  background: rgba(0,0,0,0.45);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  font-size: 11px; font-weight: 700;
  letter-spacing: 1.5px; text-transform: uppercase;
  color: rgba(255,255,255,0.95);
  border: 1px solid rgba(255,255,255,0.12);
}
.home-card-icon {
  font-size: 44px; line-height: 1;
  filter: drop-shadow(0 6px 14px rgba(0,0,0,0.5));
  transition: transform 0.4s cubic-bezier(0.2, 0.8, 0.2, 1);
}
.home-card-body {
  margin-top: 24px;
}
.home-card-title {
  font-size: clamp(20px, 2.4vw, 30px);
  font-weight: 900; line-height: 1.1;
  letter-spacing: -0.015em;
  margin-bottom: 8px;
  text-shadow: 0 2px 12px rgba(0,0,0,0.5);
  color: #fff;
}
.home-card-sub {
  font-size: clamp(13px, 1.3vw, 15px);
  color: rgba(255,255,255,0.85);
  font-weight: 400;
  line-height: 1.5;
  max-width: 560px;
  text-shadow: 0 1px 6px rgba(0,0,0,0.5);
}
.home-card-cta {
  display: inline-flex; align-items: center; gap: 8px;
  align-self: flex-start;
  margin-top: 18px;
  padding: 10px 20px;
  border-radius: 30px;
  background: rgba(255,255,255,0.14);
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
  border: 1px solid rgba(255,255,255,0.2);
  font-size: 14px; font-weight: 700; color: #fff;
  transition: background 0.25s, border-color 0.25s,
              transform 0.25s, padding 0.25s;
}
.home-card-cta-arrow {
  display: inline-block;
  font-size: 18px; line-height: 1;
  transform: translateY(-1px);
  transition: transform 0.3s cubic-bezier(0.2, 0.8, 0.2, 1);
}
.home-card-flow .home-card-icon { font-size: 56px; }
.home-card-flow .home-card-title { font-size: clamp(26px, 3.4vw, 42px); }
.home-card-flow .home-card-sub { font-size: clamp(14px, 1.5vw, 17px); }

/* Hover: Netflix lift + red glow */
.home-card:hover {
  transform: translateY(-6px) scale(1.015);
  border-color: rgba(229, 9, 20, 0.55);
  box-shadow:
    0 24px 60px -12px rgba(229, 9, 20, 0.38),
    0 0 0 1px rgba(229, 9, 20, 0.35);
}
.home-card:hover .home-card-bg { transform: scale(1.06); }
.home-card:hover .home-card-icon { transform: scale(1.12) rotate(-4deg); }
.home-card:hover .home-card-overlay { opacity: 0.85; }
.home-card:hover .home-card-cta {
  background: var(--red);
  border-color: var(--red);
  padding: 10px 26px;
  box-shadow: 0 6px 20px rgba(229, 9, 20, 0.5);
}
.home-card:hover .home-card-cta-arrow { transform: translateX(-4px) translateY(-1px); }
.home-card:focus-visible {
  outline: 3px solid var(--red);
  outline-offset: 3px;
}
.home-card:active { transform: translateY(-3px) scale(1.008); }

/* Per-card cinematic gradients (Netflix-style rich tones) */
.home-card-flow {
  --card-gradient:
    radial-gradient(ellipse 80% 60% at 18% 40%, rgba(229,9,20,0.55), transparent 62%),
    radial-gradient(ellipse 60% 50% at 78% 70%, rgba(123,47,247,0.32), transparent 60%),
    linear-gradient(135deg, #3a0608 0%, #7a0e12 40%, #1a0405 100%);
}
.home-card-meet {
  --card-gradient:
    radial-gradient(ellipse 90% 70% at 25% 35%, rgba(84,185,197,0.38), transparent 60%),
    linear-gradient(135deg, #0a2540 0%, #14476b 50%, #05182d 100%);
}
.home-card-map {
  --card-gradient:
    radial-gradient(ellipse 85% 70% at 80% 30%, rgba(123,47,247,0.42), transparent 60%),
    linear-gradient(135deg, #1e0a3d 0%, #4c1d8a 50%, #0f0520 100%);
}
.home-card-lib {
  --card-gradient:
    radial-gradient(ellipse 80% 70% at 30% 30%, rgba(245,197,24,0.32), transparent 60%),
    linear-gradient(135deg, #2d1f05 0%, #5c3a00 50%, #1a1005 100%);
}
.home-card-profits {
  --card-gradient:
    radial-gradient(ellipse 85% 70% at 75% 30%, rgba(70,211,105,0.4), transparent 60%),
    linear-gradient(135deg, #063820 0%, #0d6d3a 50%, #03200f 100%);
}

/* Tablet */
@media (max-width: 960px) {
  .home-cards { grid-template-columns: repeat(4, 1fr); gap: 14px; }
  .home-card-flow { grid-column: span 4; aspect-ratio: 20 / 8; }
  .home-card-meet,
  .home-card-map,
  .home-card-lib,
  .home-card-profits { grid-column: span 2; aspect-ratio: 4 / 3; }
}

/* Mobile */
@media (max-width: 560px) {
  .home-hero-content h1 { font-size: 34px; }
  .home-cards { grid-template-columns: 1fr; gap: 12px; }
  .home-card-flow,
  .home-card-meet,
  .home-card-map,
  .home-card-lib,
  .home-card-profits {
    grid-column: span 1;
    aspect-ratio: 16 / 10;
  }
  .home-card-inner { padding: 20px 20px 18px; }
  .home-card-icon { font-size: 38px; }
  .home-card-flow .home-card-icon { font-size: 44px; }
  .home-card-title { font-size: 20px; }
  .home-card-flow .home-card-title { font-size: 24px; }
  .home-card-cta { padding: 9px 16px; font-size: 13px; }
}

/* Light theme */
body[data-theme="light"] .home-card {
  background: #fff;
  border-color: rgba(0,0,0,0.1);
  box-shadow: 0 4px 16px rgba(0,0,0,0.06);
}
body[data-theme="light"] .home-card-overlay {
  background: linear-gradient(180deg,
    rgba(0,0,0,0.05) 0%,
    rgba(0,0,0,0.15) 55%,
    rgba(0,0,0,0.6) 100%);
}
body[data-theme="light"] .home-card:hover {
  border-color: rgba(220, 38, 38, 0.55);
  box-shadow:
    0 24px 60px -12px rgba(220, 38, 38, 0.32),
    0 0 0 1px rgba(220, 38, 38, 0.3);
}

/* ============ SECTION ============ */"""

content = TARGET.read_text(encoding='utf-8')
count = content.count(MARKER)
if count != 1:
    print(f"ERROR: Expected exactly 1 match of marker, found {count}", file=sys.stderr)
    sys.exit(1)
new_content = content.replace(MARKER, CSS_BLOCK)
TARGET.write_text(new_content, encoding='utf-8')
print(f"OK: Injected home-cards CSS ({len(new_content) - len(content)} bytes added)")
print(f"New file size: {len(new_content)} bytes")
