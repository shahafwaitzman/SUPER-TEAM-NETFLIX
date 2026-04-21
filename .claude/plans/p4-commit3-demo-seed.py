#!/usr/bin/env python3
"""Add demo seed so commit-3 features are visible WITHOUT having clicked yet.
- Runs once per user (when LAST_WATCHED is empty).
- Seeds 4 videos from the first rendered row with progress 18/45/72/90
  and staggered timestamps (2h / 8h / 24h / 72h ago).
- Immediately rebuilds the Continue Watching row.
- Once user clicks a real video, that data merges in.
"""
import sys
from pathlib import Path

TARGET = Path("/Users/shahafwaitzman/Documents/CLOUD CODE/super-team-academy/academy-hub.html")
content = TARGET.read_text(encoding='utf-8')

MARKER = """// Build once at load + every 30s to catch new watches without full reload
setTimeout(buildContinueWatchingRow, 1500);
setInterval(buildContinueWatchingRow, 30000);"""

REPLACEMENT = """// Build once at load + every 30s to catch new watches without full reload
setTimeout(buildContinueWatchingRow, 1500);
setInterval(buildContinueWatchingRow, 30000);

/* ═══════════════════════════════════════════
   COMMIT 3 · First-visit demo seed
   Populates LAST_WATCHED with 4 real videos from the page so users
   can SEE the feature immediately. Runs only if history is empty
   (preserves real data afterwards).
   ═══════════════════════════════════════════ */
function seedDemoWatchHistory() {
  const lw = stGet(ST_KEYS.LAST_WATCHED, {});
  if (Object.keys(lw).length > 0) return;  // user already has real data

  const cards = Array.from(document.querySelectorAll('.title-card-container[data-video-id]')).slice(0, 4);
  if (cards.length === 0) return;

  const progressValues = [72, 45, 18, 90];
  const hoursAgo = [2, 8, 24, 72];
  const progress = stGet(ST_KEYS.PROGRESS, {});
  const lastWatched = {};

  cards.forEach((card, i) => {
    const id = card.dataset.videoId;
    const title = decodeURIComponent(card.dataset.videoTitle || '');
    if (!id) return;
    lastWatched[id] = { ts: Date.now() - hoursAgo[i] * 3600000, title };
    progress[id] = progressValues[i];
  });

  stSet(ST_KEYS.LAST_WATCHED, lastWatched);
  stSet(ST_KEYS.PROGRESS, progress);
  buildContinueWatchingRow();
  // Force re-render of the rows containing seeded cards so their
  // progress bars appear (since render is templated at build time)
  document.querySelectorAll('.title-card-container[data-video-id]').forEach(card => {
    const id = card.dataset.videoId;
    const pct = progress[id];
    if (!pct || pct <= 0) return;
    if (card.querySelector('.card-progress')) return;
    const titleCard = card.querySelector('.title-card');
    if (!titleCard) return;
    const bar = document.createElement('div');
    bar.className = 'card-progress';
    bar.innerHTML = `<div class="card-progress-fill" style="width:${Math.min(100,pct)}%"></div>`;
    titleCard.appendChild(bar);
  });
}
// Run after rows are likely rendered (Drive fetch takes time)
setTimeout(seedDemoWatchHistory, 2500);"""

if MARKER not in content:
    print("ERROR: marker not found", file=sys.stderr); sys.exit(1)
content = content.replace(MARKER, REPLACEMENT)

TARGET.write_text(content, encoding='utf-8')
print(f"OK: demo seed added. Size: {len(content)} bytes")
