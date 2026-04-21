#!/usr/bin/env python3
"""P1 flow-viewer home redesign v2:
  - All 5 cards same size (remove featured span on FLOW)
  - Rename: FLOW סגירת מפקח + FLOW לקוח (parallel structure)
  - Inline SVG illustrations centered (replace emojis)
  - Centered card layout: kicker → illustration → title → sub → CTA
  - Tighter, consistent copy
"""
import re
import sys
from pathlib import Path

TARGET = Path("/Users/shahafwaitzman/Documents/CLOUD CODE/flow-viewer/index.html")
content = TARGET.read_text(encoding='utf-8')

# --- SVG ILLUSTRATIONS ---
SVG_FLOW = '''<svg class="home-card-art" viewBox="0 0 120 120" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
  <circle cx="60" cy="60" r="52" stroke-opacity="0.25"/>
  <circle cx="60" cy="60" r="38" stroke-opacity="0.45"/>
  <circle cx="60" cy="60" r="24" stroke-opacity="0.7"/>
  <circle cx="60" cy="60" r="7" fill="currentColor"/>
  <path d="M97 22 L67 52" stroke="#f5c518" stroke-width="3.2"/>
  <path d="M97 22 L89 20 M97 22 L95 30" stroke="#f5c518" stroke-width="3.2"/>
</svg>'''

SVG_MEET = '''<svg class="home-card-art" viewBox="0 0 120 120" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
  <path d="M70 22 H102 a8 8 0 0 1 8 8 v22 a8 8 0 0 1 -8 8 H92 L82 72 V60 H70 a8 8 0 0 1 -8 -8 v-22 a8 8 0 0 1 8 -8 z" stroke-opacity="0.5" fill="rgba(255,255,255,0.08)"/>
  <circle cx="78" cy="41" r="2.2" fill="currentColor" fill-opacity="0.6"/>
  <circle cx="88" cy="41" r="2.2" fill="currentColor" fill-opacity="0.6"/>
  <circle cx="98" cy="41" r="2.2" fill="currentColor" fill-opacity="0.6"/>
  <path d="M18 52 H54 a10 10 0 0 1 10 10 v26 a10 10 0 0 1 -10 10 H40 L28 110 v-12 H18 a10 10 0 0 1 -10 -10 v-26 a10 10 0 0 1 10 -10 z" fill="currentColor" fill-opacity="0.2" stroke="currentColor"/>
  <circle cx="24" cy="75" r="2.8" fill="currentColor"/>
  <circle cx="36" cy="75" r="2.8" fill="currentColor"/>
  <circle cx="48" cy="75" r="2.8" fill="currentColor"/>
</svg>'''

SVG_MAP = '''<svg class="home-card-art" viewBox="0 0 120 120" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
  <path d="M28 56 L54 32" stroke-opacity="0.55"/>
  <path d="M70 32 L94 76" stroke-opacity="0.55"/>
  <path d="M88 88 L68 96" stroke-opacity="0.55"/>
  <path d="M48 94 L32 72" stroke-opacity="0.55"/>
  <circle cx="24" cy="62" r="13" fill="rgba(255,255,255,0.08)" stroke="currentColor" stroke-opacity="0.8"/>
  <circle cx="62" cy="28" r="13" fill="rgba(255,255,255,0.14)" stroke="currentColor"/>
  <circle cx="96" cy="80" r="13" fill="currentColor" fill-opacity="0.9"/>
  <circle cx="62" cy="98" r="11" fill="rgba(255,255,255,0.1)" stroke="currentColor" stroke-opacity="0.85"/>
</svg>'''

SVG_LIB = '''<svg class="home-card-art" viewBox="0 0 120 120" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
  <rect x="14" y="80" width="92" height="22" rx="3" fill="rgba(255,255,255,0.08)" stroke="currentColor" stroke-opacity="0.55"/>
  <line x1="28" y1="80" x2="28" y2="102" stroke-opacity="0.5"/>
  <rect x="20" y="52" width="80" height="22" rx="3" fill="rgba(255,255,255,0.14)" stroke="currentColor" stroke-opacity="0.75"/>
  <line x1="33" y1="52" x2="33" y2="74" stroke-opacity="0.6"/>
  <rect x="26" y="22" width="68" height="22" rx="3" fill="currentColor" fill-opacity="0.22" stroke="currentColor"/>
  <line x1="37" y1="22" x2="37" y2="44"/>
  <rect x="44" y="30" width="34" height="2.4" rx="1" fill="currentColor" fill-opacity="0.7"/>
  <rect x="44" y="36" width="22" height="2.4" rx="1" fill="currentColor" fill-opacity="0.5"/>
</svg>'''

SVG_PROFITS = '''<svg class="home-card-art" viewBox="0 0 120 120" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
  <line x1="12" y1="100" x2="108" y2="100" stroke-opacity="0.35"/>
  <rect x="20" y="80" width="14" height="20" rx="1.5" fill="currentColor" fill-opacity="0.32" stroke="currentColor"/>
  <rect x="42" y="64" width="14" height="36" rx="1.5" fill="currentColor" fill-opacity="0.5" stroke="currentColor"/>
  <rect x="64" y="44" width="14" height="56" rx="1.5" fill="currentColor" fill-opacity="0.7" stroke="currentColor"/>
  <rect x="86" y="22" width="14" height="78" rx="1.5" fill="currentColor" stroke="currentColor"/>
  <path d="M24 76 L94 18" stroke="#f5c518" stroke-width="2.8"/>
  <path d="M94 18 L86 20 M94 18 L92 26" stroke="#f5c518" stroke-width="2.8"/>
</svg>'''

# --- NEW HTML: 5 equal-sized cards, centered layout, SVG illustrations ---
NEW_CARDS_HTML = f'''      <div class="home-cards" role="list" aria-label="מרכזי פעולה">

        <button type="button" class="home-card home-card-flow" data-card="flow" role="listitem" aria-label="FLOW סגירת מפקח">
          <div class="home-card-bg" aria-hidden="true"></div>
          <div class="home-card-pattern" aria-hidden="true"></div>
          <div class="home-card-overlay" aria-hidden="true"></div>
          <div class="home-card-inner">
            <span class="home-card-kicker">11 שלבים</span>
            <div class="home-card-art-wrap">
              {SVG_FLOW}
            </div>
            <div class="home-card-body">
              <h3 class="home-card-title">FLOW סגירת מפקח</h3>
              <p class="home-card-sub">המסע המלא לקידום ל-AWT</p>
            </div>
            <div class="home-card-cta"><span class="home-card-cta-arrow" aria-hidden="true">←</span><span>התחילי</span></div>
          </div>
        </button>

        <button type="button" class="home-card home-card-meet" data-card="meetings" role="listitem" aria-label="FLOW לקוח">
          <div class="home-card-bg" aria-hidden="true"></div>
          <div class="home-card-pattern" aria-hidden="true"></div>
          <div class="home-card-overlay" aria-hidden="true"></div>
          <div class="home-card-inner">
            <span class="home-card-kicker">פגישה 1 ו-2</span>
            <div class="home-card-art-wrap">
              {SVG_MEET}
            </div>
            <div class="home-card-body">
              <h3 class="home-card-title">FLOW לקוח</h3>
              <p class="home-card-sub">סקריפט, משימות ודגשים לפגישות</p>
            </div>
            <div class="home-card-cta"><span class="home-card-cta-arrow" aria-hidden="true">←</span><span>פתחי</span></div>
          </div>
        </button>

        <button type="button" class="home-card home-card-map" data-card="diagram" role="listitem" aria-label="תרשים כללי">
          <div class="home-card-bg" aria-hidden="true"></div>
          <div class="home-card-pattern" aria-hidden="true"></div>
          <div class="home-card-overlay" aria-hidden="true"></div>
          <div class="home-card-inner">
            <span class="home-card-kicker">מפה ויזואלית</span>
            <div class="home-card-art-wrap">
              {SVG_MAP}
            </div>
            <div class="home-card-body">
              <h3 class="home-card-title">תרשים כללי</h3>
              <p class="home-card-sub">לקוח ← מפיץ ← מפקח</p>
            </div>
            <div class="home-card-cta"><span class="home-card-cta-arrow" aria-hidden="true">←</span><span>תראי</span></div>
          </div>
        </button>

        <button type="button" class="home-card home-card-lib" data-card="library" role="listitem" aria-label="ספריית קבצים">
          <div class="home-card-bg" aria-hidden="true"></div>
          <div class="home-card-pattern" aria-hidden="true"></div>
          <div class="home-card-overlay" aria-hidden="true"></div>
          <div class="home-card-inner">
            <span class="home-card-kicker">מסמכים</span>
            <div class="home-card-art-wrap">
              {SVG_LIB}
            </div>
            <div class="home-card-body">
              <h3 class="home-card-title">ספריית קבצים</h3>
              <p class="home-card-sub">כל הקבצים, הטפסים והקישורים</p>
            </div>
            <div class="home-card-cta"><span class="home-card-cta-arrow" aria-hidden="true">←</span><span>פתחי</span></div>
          </div>
        </button>

        <button type="button" class="home-card home-card-profits" data-card="profits" role="listitem" aria-label="POWER MONDAY">
          <div class="home-card-bg" aria-hidden="true"></div>
          <div class="home-card-pattern" aria-hidden="true"></div>
          <div class="home-card-overlay" aria-hidden="true"></div>
          <div class="home-card-inner">
            <span class="home-card-kicker">רווחים</span>
            <div class="home-card-art-wrap">
              {SVG_PROFITS}
            </div>
            <div class="home-card-body">
              <h3 class="home-card-title">POWER MONDAY</h3>
              <p class="home-card-sub">מעקב רווחים וקריטריונים</p>
            </div>
            <div class="home-card-cta"><span class="home-card-cta-arrow" aria-hidden="true">←</span><span>נכנסתי</span></div>
          </div>
        </button>

      </div>'''

# Replace the home-cards HTML block (match between the opening tag and the closing </div>
# that wraps all 5 buttons, which is the FIRST </div> after the 5th </button>)
cards_re = re.compile(
    r'      <div class="home-cards" role="list"[^>]*>.*?\n      </div>',
    re.DOTALL
)
new_content, n = cards_re.subn(NEW_CARDS_HTML, content)
if n != 1:
    print(f"ERROR: home-cards HTML replace count = {n} (expected 1)", file=sys.stderr)
    sys.exit(1)
content = new_content

# --- NEW CSS: centered layout, equal sizes, SVG illustrations ---
NEW_CSS = '''/* ============ HOME CARDS (Netflix-style, v2 centered) ============ */
.home-hero-content { max-width: 1400px; width: 100%; }
.home-hero-content h1 {
  font-size: clamp(34px, 5.4vw, 64px);
  margin-bottom: 14px;
}
.home-hero-content .hero-sub { margin-bottom: 40px; }

.home-cards {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 18px;
  margin-top: 8px;
}

.home-card {
  position: relative;
  display: block;
  padding: 0;
  aspect-ratio: 3 / 4;
  border-radius: 16px;
  border: 1px solid rgba(255,255,255,0.08);
  background: #1a1a1a;
  color: #fff;
  text-align: center;
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
    radial-gradient(circle at 85% 12%, rgba(255,255,255,0.18), transparent 45%),
    radial-gradient(circle at 15% 92%, rgba(0,0,0,0.32), transparent 50%);
  pointer-events: none;
  transition: opacity 0.3s;
}
.home-card-overlay {
  position: absolute; inset: 0; z-index: 2;
  background: linear-gradient(180deg,
    rgba(0,0,0,0.05) 0%,
    rgba(0,0,0,0.15) 55%,
    rgba(0,0,0,0.6) 100%);
  transition: opacity 0.3s;
}

.home-card-inner {
  position: relative; z-index: 3;
  height: 100%;
  display: flex; flex-direction: column; align-items: center;
  padding: 22px 18px 20px;
  gap: 14px;
}

.home-card-kicker {
  display: inline-block;
  padding: 5px 14px;
  border-radius: 20px;
  background: rgba(0,0,0,0.45);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  font-size: 11px; font-weight: 700;
  letter-spacing: 1.5px; text-transform: uppercase;
  color: rgba(255,255,255,0.96);
  border: 1px solid rgba(255,255,255,0.14);
  white-space: nowrap;
}

.home-card-art-wrap {
  flex: 1;
  display: flex; align-items: center; justify-content: center;
  width: 100%;
  padding: 6px 0;
}
.home-card-art {
  width: 72%;
  max-width: 180px;
  height: auto;
  aspect-ratio: 1 / 1;
  color: #fff;
  filter: drop-shadow(0 8px 24px rgba(0,0,0,0.45));
  transition: transform 0.5s cubic-bezier(0.2, 0.8, 0.2, 1);
}

.home-card-body {
  width: 100%;
  text-align: center;
}
/* Consistent title sizing across ALL cards — no card-specific overrides */
.home-card-title {
  font-size: clamp(17px, 1.5vw, 22px);
  font-weight: 900; line-height: 1.15;
  letter-spacing: -0.01em;
  margin-bottom: 6px;
  text-shadow: 0 2px 10px rgba(0,0,0,0.55);
  color: #fff;
}
.home-card-sub {
  font-size: clamp(12px, 1vw, 14px);
  color: rgba(255,255,255,0.82);
  font-weight: 400;
  line-height: 1.45;
  text-shadow: 0 1px 6px rgba(0,0,0,0.5);
  min-height: 2.9em;
}

.home-card-cta {
  display: inline-flex; align-items: center; gap: 7px;
  margin-top: 6px;
  padding: 9px 18px;
  border-radius: 30px;
  background: rgba(255,255,255,0.14);
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
  border: 1px solid rgba(255,255,255,0.22);
  font-size: 13px; font-weight: 700; color: #fff;
  transition: background 0.25s, border-color 0.25s,
              transform 0.25s, padding 0.25s;
}
.home-card-cta-arrow {
  display: inline-block;
  font-size: 16px; line-height: 1;
  transform: translateY(-1px);
  transition: transform 0.3s cubic-bezier(0.2, 0.8, 0.2, 1);
}

/* Hover: Netflix lift + red glow */
.home-card:hover {
  transform: translateY(-8px) scale(1.025);
  border-color: rgba(229, 9, 20, 0.6);
  box-shadow:
    0 28px 60px -14px rgba(229, 9, 20, 0.45),
    0 0 0 1px rgba(229, 9, 20, 0.45);
}
.home-card:hover .home-card-bg { transform: scale(1.08); }
.home-card:hover .home-card-art { transform: scale(1.08) rotate(-3deg); }
.home-card:hover .home-card-overlay { opacity: 0.9; }
.home-card:hover .home-card-cta {
  background: var(--red);
  border-color: var(--red);
  padding: 9px 24px;
  box-shadow: 0 6px 20px rgba(229, 9, 20, 0.55);
}
.home-card:hover .home-card-cta-arrow { transform: translateX(-5px) translateY(-1px); }
.home-card:focus-visible {
  outline: 3px solid var(--red);
  outline-offset: 3px;
}
.home-card:active { transform: translateY(-4px) scale(1.012); }

/* Per-card cinematic gradients (Netflix rich tones) */
.home-card-flow {
  --card-gradient:
    radial-gradient(ellipse 85% 60% at 30% 30%, rgba(229,9,20,0.58), transparent 62%),
    radial-gradient(ellipse 60% 50% at 80% 80%, rgba(123,47,247,0.3), transparent 60%),
    linear-gradient(135deg, #3a0608 0%, #7a0e12 45%, #1a0405 100%);
}
.home-card-meet {
  --card-gradient:
    radial-gradient(ellipse 85% 65% at 30% 30%, rgba(84,185,197,0.42), transparent 60%),
    linear-gradient(135deg, #0a2540 0%, #14476b 48%, #05182d 100%);
}
.home-card-map {
  --card-gradient:
    radial-gradient(ellipse 85% 65% at 75% 30%, rgba(123,47,247,0.46), transparent 60%),
    linear-gradient(135deg, #1e0a3d 0%, #4c1d8a 48%, #0f0520 100%);
}
.home-card-lib {
  --card-gradient:
    radial-gradient(ellipse 85% 65% at 30% 30%, rgba(245,197,24,0.38), transparent 60%),
    linear-gradient(135deg, #2d1f05 0%, #5c3a00 48%, #1a1005 100%);
}
.home-card-profits {
  --card-gradient:
    radial-gradient(ellipse 85% 65% at 75% 30%, rgba(70,211,105,0.44), transparent 60%),
    linear-gradient(135deg, #063820 0%, #0d6d3a 48%, #03200f 100%);
}

/* Tablet: 3 per row, last two fill row 2 (natural flow, right-aligned in RTL) */
@media (max-width: 1100px) {
  .home-cards { grid-template-columns: repeat(3, 1fr); gap: 14px; }
  .home-card { aspect-ratio: 3 / 4; }
}

/* Small tablet: 2 per row */
@media (max-width: 720px) {
  .home-cards { grid-template-columns: repeat(2, 1fr); gap: 12px; }
  .home-card { aspect-ratio: 4 / 5; }
  .home-card-art { width: 60%; max-width: 140px; }
  .home-card-inner { padding: 18px 14px 16px; }
}

/* Mobile */
@media (max-width: 440px) {
  .home-hero-content h1 { font-size: 34px; }
  .home-cards { grid-template-columns: 1fr; gap: 10px; }
  .home-card { aspect-ratio: 4 / 3; }
  .home-card-inner {
    flex-direction: row-reverse;
    text-align: right;
    padding: 18px;
    gap: 14px;
    align-items: center;
  }
  .home-card-art-wrap { flex: 0 0 80px; padding: 0; }
  .home-card-art { width: 80px; max-width: 80px; }
  .home-card-body { flex: 1; text-align: right; }
  .home-card-kicker {
    position: absolute; top: 14px; left: 14px;
    font-size: 10px;
    padding: 4px 10px;
  }
  .home-card-title { font-size: 18px; }
  .home-card-sub { min-height: 0; font-size: 13px; }
  .home-card-cta { display: none; }
}

/* Light theme */
body[data-theme="light"] .home-card {
  background: #fff;
  border-color: rgba(0,0,0,0.1);
  box-shadow: 0 4px 16px rgba(0,0,0,0.06);
}
body[data-theme="light"] .home-card-overlay {
  background: linear-gradient(180deg,
    rgba(0,0,0,0.04) 0%,
    rgba(0,0,0,0.12) 55%,
    rgba(0,0,0,0.55) 100%);
}
body[data-theme="light"] .home-card:hover {
  border-color: rgba(220, 38, 38, 0.6);
  box-shadow:
    0 28px 60px -14px rgba(220, 38, 38, 0.36),
    0 0 0 1px rgba(220, 38, 38, 0.34);
}

/* ============ SECTION ============ */'''

css_re = re.compile(
    r'/\* ============ HOME CARDS \(Netflix-style\).*?/\* ============ SECTION ============ \*/',
    re.DOTALL
)
new_content, n = css_re.subn(NEW_CSS, content)
if n != 1:
    print(f"ERROR: CSS replace count = {n} (expected 1)", file=sys.stderr)
    sys.exit(1)
content = new_content

TARGET.write_text(content, encoding='utf-8')
print(f"OK: v2 redesign written. Final size: {len(content)} bytes")
