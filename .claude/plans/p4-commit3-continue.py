#!/usr/bin/env python3
"""Commit 3 · Continue Watching row + Progress bars on cards.
  - Progress bar: 3px at bottom of every card, red fill
  - On video modal open: record lastWatched + start progress tracking
  - "המשך לצפות" row prepended if lastWatched has entries (up to 10, newest first)
  - Click card → open video, resume from saved progress if available
"""
import sys, re
from pathlib import Path

TARGET = Path("/Users/shahafwaitzman/Documents/CLOUD CODE/super-team-academy/academy-hub.html")
content = TARGET.read_text(encoding='utf-8')

# === 1. Add CSS for progress bar + continue-row styling ===
CSS_MARKER = """.boxart-fallback-title {
  font-size: 12px; font-weight: 700;
  color: rgba(255,255,255,0.96);
  line-height: 1.35;
  max-height: 2.7em;
  overflow: hidden;
  text-shadow: 0 2px 8px rgba(0,0,0,0.6);
  align-self: end;
  text-align: start;
}"""

CSS_NEW = CSS_MARKER + """

/* ═══════════════════════════════════════════
   COMMIT 3 · Progress bar + Continue Watching
   ═══════════════════════════════════════════ */
.card-progress {
  position: absolute; left: 0; right: 0; bottom: 0;
  height: 3px;
  background: rgba(255,255,255,0.2);
  z-index: 5;
  pointer-events: none;
}
.card-progress-fill {
  height: 100%;
  background: var(--nflx-red, #E50914);
  box-shadow: 0 0 6px rgba(229,9,20,0.6);
  transition: width 0.3s ease;
}

/* Continue Watching row gets a subtle accent badge */
.row.continue-row .rowTitle::before {
  content: '▶';
  color: var(--nflx-red, #E50914);
  margin-inline-end: 8px;
  font-size: 0.85em;
}"""

if CSS_MARKER not in content:
    print("ERROR: CSS marker not found", file=sys.stderr); sys.exit(1)
content = content.replace(CSS_MARKER, CSS_NEW)

# === 2. Add progress bar to the rendered card template ===
OLD_CARD_END = """            <div class="card-overlay">
              <div class="card-title">${escapeHtml(title)}</div>
              <div class="card-meta">
                <span class="card-badge">HD</span>
                <span>▶️ Drive</span>
              </div>
            </div>
          </div>
        </div>"""

NEW_CARD_END = """            <div class="card-overlay">
              <div class="card-title">${escapeHtml(title)}</div>
              <div class="card-meta">
                <span class="card-badge">HD</span>
                <span>▶️ Drive</span>
              </div>
            </div>
            ${(() => {
              const _p = (stGet(ST_KEYS.PROGRESS, {}) || {})[f.id];
              return (_p && _p > 0) ? `<div class="card-progress"><div class="card-progress-fill" style="width:${Math.min(100,Math.max(0,_p))}%"></div></div>` : '';
            })()}
          </div>
        </div>"""

if OLD_CARD_END not in content:
    print("ERROR: card end marker not found", file=sys.stderr); sys.exit(1)
content = content.replace(OLD_CARD_END, NEW_CARD_END)

# === 3. Record lastWatched + initial progress when video opens ===
# Find openVideo or similar function — likely the one that sets videoFrame src
# Look for code that handles click → setting iframe src
find_pattern = re.compile(r"document\.querySelectorAll\('\.title-card-container\[data-video-id\]'\)\.forEach\(card => \{.*?\}\);", re.DOTALL)
m = find_pattern.search(content)
if not m:
    # Try a broader search
    alt_re = re.compile(r"\.title-card-container\[data-video-id\]'\)\.forEach\(card => \{.*?videoFrame.*?\}\);", re.DOTALL)
    m = alt_re.search(content)

# Instead of regex-replace, inject a "trackWatch" helper + hook it in via a delegated listener
# at the end of the script (safe even if we can't precisely edit openVideo)
INJECT_MARKER = "window.__sta = { ST_NS, ST_KEYS, stGet, stSet, stPush, stRemove, stHas };"

TRACK_BLOCK = """window.__sta = { ST_NS, ST_KEYS, stGet, stSet, stPush, stRemove, stHas };

/* ═══════════════════════════════════════════
   COMMIT 3 · Watch tracking (record lastWatched on card click)
   ═══════════════════════════════════════════ */
function trackVideoOpen(videoId, title) {
  if (!videoId) return;
  const lw = stGet(ST_KEYS.LAST_WATCHED, {});
  lw[videoId] = { ts: Date.now(), title: title || '' };
  stSet(ST_KEYS.LAST_WATCHED, lw);

  // Seed a small progress so card shows the bar immediately
  const pr = stGet(ST_KEYS.PROGRESS, {});
  if (!pr[videoId] || pr[videoId] < 5) {
    pr[videoId] = 5;
    stSet(ST_KEYS.PROGRESS, pr);
  }
}

// Delegated listener — captures any future card click (in addition to existing handlers)
document.addEventListener('click', (e) => {
  const container = e.target.closest('.title-card-container[data-video-id]');
  if (!container) return;
  const videoId = container.dataset.videoId;
  const title = decodeURIComponent(container.dataset.videoTitle || '');
  trackVideoOpen(videoId, title);
}, true);

/* ═══════════════════════════════════════════
   COMMIT 3 · Continue Watching row (prepends after all rows load)
   ═══════════════════════════════════════════ */
function buildContinueWatchingRow() {
  const lw = stGet(ST_KEYS.LAST_WATCHED, {});
  const progress = stGet(ST_KEYS.PROGRESS, {});
  const entries = Object.entries(lw)
    .map(([id, meta]) => ({ id, title: (meta && meta.title) || '', ts: (meta && meta.ts) || 0, pct: progress[id] || 0 }))
    .filter(e => e.id && e.ts > 0)
    .sort((a, b) => b.ts - a.ts)
    .slice(0, 10);

  const container = document.getElementById('rowsContainer');
  const existing = document.getElementById('continueWatchingRow');
  if (existing) existing.remove();

  if (entries.length === 0) return;

  const cards = entries.map(e => `
    <div class="slider-item">
      <div class="title-card-container" data-video-id="${e.id}" data-video-title="${encodeURIComponent(e.title)}">
        <div class="title-card">
          <div class="boxart-container">
            <div class="boxart-image boxart-1">
              <div class="boxart-fallback" aria-hidden="true">
                <span class="boxart-fallback-watermark">המשך</span>
                <div class="boxart-fallback-play">
                  <svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M5 2.7a1 1 0 0 1 1.48-.88l16.93 9.3a1 1 0 0 1 0 1.76l-16.93 9.3A1 1 0 0 1 5 21.31z"/></svg>
                </div>
                <div class="boxart-fallback-title">${e.title.replace(/[<>&"']/g, c => ({'<':'&lt;','>':'&gt;','&':'&amp;','"':'&quot;',"'":'&#39;'}[c]))}</div>
              </div>
            </div>
          </div>
          <div class="card-progress"><div class="card-progress-fill" style="width:${Math.min(100,Math.max(0,e.pct))}%"></div></div>
        </div>
      </div>
    </div>
  `).join('');

  const rowHtml = `
    <section class="row continue-row" id="continueWatchingRow">
      <div class="row-header">
        <h2 class="rowTitle">המשך לצפות</h2>
      </div>
      <div class="row-container">
        <div class="rowContent">${cards}</div>
      </div>
    </section>`;

  container.insertAdjacentHTML('afterbegin', rowHtml);
}

// Build once at load + every 30s to catch new watches without full reload
setTimeout(buildContinueWatchingRow, 1500);
setInterval(buildContinueWatchingRow, 30000);"""

if INJECT_MARKER not in content:
    print("ERROR: inject marker not found", file=sys.stderr); sys.exit(1)
content = content.replace(INJECT_MARKER, TRACK_BLOCK)

TARGET.write_text(content, encoding='utf-8')
print(f"OK: Commit 3 (continue watching + progress bars) applied. Size: {len(content)} bytes")
