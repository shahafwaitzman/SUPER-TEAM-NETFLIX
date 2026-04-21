#!/usr/bin/env python3
"""Phase 4D: Keyword-matched SVG illustrations for videos without thumbnails.

Injects a title-based illustration picker into academy-hub's card fallback
rendering. When a card's data-category or title contains certain keywords,
show a relevant SVG instead of generic play button.
"""
from pathlib import Path

TARGET = Path("/Users/shahafwaitzman/Documents/CLOUD CODE/super-team-academy/academy-hub.html")
c = TARGET.read_text(encoding='utf-8')

# Map: keyword → SVG path (24×24 viewBox).
# Multiple keywords can map to same icon.
ILLUSTRATION_JS = r'''
/* ═══════════════════════════════════════════
   PHASE 4D · Title-matched illustrations
   Replaces generic play icon on missing-thumbnail cards
   with a keyword-relevant SVG.
   ═══════════════════════════════════════════ */
const STA_ICONS = {
  business:   '<path d="M20 6h-4V4c0-1.1-.9-2-2-2h-4c-1.1 0-2 .9-2 2v2H4c-1.1 0-2 .9-2 2v11c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V8c0-1.1-.9-2-2-2zm-10-2h4v2h-4V4zm0 15H4v-3h6v3zm10 0h-8v-3h8v3zm0-5H4v-3h16v3z"/>',
  meeting:    '<path d="M16 13c-1.1 0-2.8.3-4 1-1.2-.7-2.9-1-4-1-2.3 0-7 1.2-7 3.5V19h22v-2.5c0-2.3-4.7-3.5-7-3.5zm-4 4.5H1.9v-1c0-.6 3-2 5.1-2s5.1 1.4 5.1 2v1zm10 0H14v-1c0-.5-.2-1-.6-1.4 1-.3 2.1-.6 2.6-.6 2.1 0 5 1.4 5 2v1zM7 12c1.9 0 3.5-1.6 3.5-3.5S8.9 5 7 5 3.5 6.6 3.5 8.5 5.1 12 7 12z"/>',
  training:   '<path d="M19 3H5c-1.11 0-2 .89-2 2v14c0 1.11.89 2 2 2h14c1.11 0 2-.89 2-2V5c0-1.11-.89-2-2-2zm-5 14H7v-2h7v2zm3-4H7v-2h10v2zm0-4H7V7h10v2z"/>',
  customer:   '<path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/>',
  money:      '<path d="M11.8 10.9c-2.27-.59-3-1.2-3-2.15 0-1.09 1.01-1.85 2.7-1.85 1.78 0 2.44.85 2.5 2.1h2.21c-.07-1.72-1.12-3.3-3.21-3.81V3h-3v2.16c-1.94.42-3.5 1.68-3.5 3.61 0 2.31 1.91 3.46 4.7 4.13 2.5.6 3 1.48 3 2.41 0 .69-.49 1.79-2.7 1.79-2.06 0-2.87-.92-2.98-2.1h-2.2c.12 2.19 1.76 3.42 3.68 3.83V21h3v-2.15c1.95-.37 3.5-1.5 3.5-3.55 0-2.84-2.43-3.81-4.7-4.4z"/>',
  goal:       '<path d="M11.99 2C6.47 2 2 6.48 2 12s4.47 10 9.99 10C17.52 22 22 17.52 22 12S17.52 2 11.99 2zM12 20c-4.42 0-8-3.58-8-8s3.58-8 8-8 8 3.58 8 8-3.58 8-8 8zm.5-13H11v6l5.25 3.15.75-1.23-4.5-2.67z"/>',
  video:      '<path d="M17 10.5V7c0-.55-.45-1-1-1H4c-.55 0-1 .45-1 1v10c0 .55.45 1 1 1h12c.55 0 1-.45 1-1v-3.5l4 4v-11l-4 4z"/>',
  zoom:       '<path d="M17 10.5V7c0-.55-.45-1-1-1H4c-.55 0-1 .45-1 1v10c0 .55.45 1 1 1h12c.55 0 1-.45 1-1v-3.5l4 4v-11l-4 4z"/>',
  food:       '<path d="M8.1 13.34l2.83-2.83L3.91 3.5c-1.56 1.56-1.56 4.09 0 5.66l4.19 4.18zm6.78-1.81c1.53.71 3.68.21 5.27-1.38 1.91-1.91 2.28-4.65.81-6.12-1.46-1.46-4.20-1.1-6.12.81-1.59 1.59-2.09 3.74-1.38 5.27L3.7 19.87l1.41 1.41L12 14.41l6.88 6.88 1.41-1.41L13.41 13l1.47-1.47z"/>',
  fitness:    '<path d="M20.57 14.86L22 13.43 20.57 12 17 15.57 8.43 7 12 3.43 10.57 2 9.14 3.43 7.71 2 5.57 4.14 4.14 2.71 2.71 4.14l1.43 1.43L2 7.71l1.43 1.43L2 10.57 3.43 12 7 8.43 15.57 17 12 20.57 13.43 22l1.43-1.43L16.29 22l2.14-2.14 1.43 1.43 1.43-1.43-1.43-1.43L22 16.29z"/>',
  target:     '<path d="M12 9c-1.66 0-3 1.34-3 3s1.34 3 3 3 3-1.34 3-3-1.34-3-3-3zm0 8c-2.76 0-5-2.24-5-5s2.24-5 5-5 5 2.24 5 5-2.24 5-5 5zm0-12.95c-3.73 0-7 3.02-7 7 0 3.7 3.16 7 7 7s7-3.3 7-7c0-3.98-3.27-7-7-7z"/>',
  marketing:  '<path d="M3 3v18h18V3H3zm16 16H5V5h14v14zM7 7h10v2H7zm0 4h10v2H7zm0 4h7v2H7z"/>',
  document:   '<path d="M14 2H6c-1.1 0-1.99.9-1.99 2L4 20c0 1.1.89 2 1.99 2H18c1.1 0 2-.9 2-2V8l-6-6zM6 20V4h7v5h5v11H6z"/>',
  chart:      '<path d="M5 9.2h3V19H5zM10.6 5h2.8v14h-2.8zm5.6 8H19v6h-2.8z"/>',
  default:    '<path d="M8 5v14l11-7z"/>'
};

function pickIconFor(title, category) {
  const t = ((title || '') + ' ' + (category || '')).toLowerCase();
  // Order matters — most specific first
  if (/הזדמנו|עסקי|hom|מפיץ/.test(t)) return STA_ICONS.business;
  if (/ליווי|פגישה|לקוח|התקשר|שיחה/.test(t)) return STA_ICONS.customer;
  if (/הדרכ|קורס|לימוד|מצגת/.test(t)) return STA_ICONS.training;
  if (/זום|zoom|וידאו|video/.test(t)) return STA_ICONS.video;
  if (/רווח|כסף|money|שייק.*(מכירה|דולר|ש״ח|שח)|פרומוש/.test(t)) return STA_ICONS.money;
  if (/מטרה|יעד|קפטן/.test(t)) return STA_ICONS.target;
  if (/שייק|פורמול|תזונ|אוכל|ארוח|מזון/.test(t)) return STA_ICONS.food;
  if (/אימון|תנועה|פיטנס|מרתון|כושר/.test(t)) return STA_ICONS.fitness;
  if (/מודע|שיווק|פרסו|תוכנית שיווק/.test(t)) return STA_ICONS.marketing;
  if (/תיעוד|מסמך|טופס/.test(t)) return STA_ICONS.document;
  if (/סימולצ|סקירה/.test(t)) return STA_ICONS.chart;
  return STA_ICONS.default;
}

function applySmartIllustrations() {
  document.querySelectorAll('.boxart-image.no-thumb .boxart-fallback-play').forEach(el => {
    if (el.dataset.stnIcon === '1') return;  // already applied
    const card = el.closest('.title-card-container');
    if (!card) return;
    const title = decodeURIComponent(card.dataset.videoTitle || '');
    const cat = decodeURIComponent(card.dataset.category || '');
    const path = pickIconFor(title, cat);
    el.innerHTML = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" style="width:30px;height:30px;">' + path + '</svg>';
    el.dataset.stnIcon = '1';
  });
}
// Run after cards render + periodically to catch new ones
setTimeout(applySmartIllustrations, 2000);
setInterval(applySmartIllustrations, 5000);
'''

# Find a safe injection point — right after renderCompletionMarks interval
MARKER = "setInterval(renderCompletionMarks, 30000);"
if MARKER in c:
    c = c.replace(MARKER, MARKER + '\n' + ILLUSTRATION_JS)
    TARGET.write_text(c, encoding='utf-8')
    print(f"✓ Illustrations JS injected into academy-hub.html")
else:
    print("✗ marker not found")
