#!/usr/bin/env python3
"""Commit 8 · Leaderboard mock (Phase 2C).
  - New row at bottom "🏆 הלוח של המועדונים"
  - Fetches leaderboard.json
  - Styled as horizontal cards: rank + club + points + leader + trend
"""
import sys
from pathlib import Path

TARGET = Path("/Users/shahafwaitzman/Documents/CLOUD CODE/super-team-academy/academy-hub.html")
content = TARGET.read_text(encoding='utf-8')

# === 1. CSS ===
CSS_MARKER = """.pp-logout-btn:hover {
  background: rgba(229,9,20,0.15);
  border-color: var(--nflx-red, #E50914);
  color: #fff;
}"""

CSS_NEW = CSS_MARKER + """

/* ═══════════════════════════════════════════
   COMMIT 8 · Leaderboard row
   ═══════════════════════════════════════════ */
.leaderboard-row .rowTitle::before {
  content: '🏆';
  margin-inline-end: 8px;
  font-size: 1em;
}
.leaderboard-card {
  display: flex; align-items: center; gap: 14px;
  width: 280px;
  padding: 14px 16px;
  background: linear-gradient(135deg, rgba(20,20,20,0.95), rgba(10,10,10,0.92));
  border: 1px solid rgba(245,197,24,0.2);
  border-radius: 10px;
  flex-shrink: 0;
  transition: transform 0.3s, border-color 0.3s, box-shadow 0.3s;
  cursor: default;
  position: relative;
  overflow: hidden;
}
.leaderboard-card:hover {
  transform: translateY(-4px);
  border-color: rgba(245,197,24,0.5);
  box-shadow: 0 12px 30px rgba(0,0,0,0.5), 0 0 18px rgba(245,197,24,0.2);
}
.leaderboard-card[data-rank="1"] { border-color: rgba(245,197,24,0.55); box-shadow: 0 0 16px rgba(245,197,24,0.2); }
.leaderboard-card[data-rank="2"] { border-color: rgba(200,200,210,0.4); }
.leaderboard-card[data-rank="3"] { border-color: rgba(205,127,50,0.5); }

.lb-rank {
  font-family: 'Heebo', sans-serif;
  font-size: 30px; font-weight: 900;
  color: rgba(255,255,255,0.2);
  line-height: 1;
  min-width: 40px;
  text-align: center;
}
.leaderboard-card[data-rank="1"] .lb-rank { color: #f5c518; }
.leaderboard-card[data-rank="2"] .lb-rank { color: #c8c8d2; }
.leaderboard-card[data-rank="3"] .lb-rank { color: #cd7f32; }

.lb-body { flex: 1; min-width: 0; }
.lb-name {
  font-size: 13px; font-weight: 800;
  color: #fff;
  overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
}
.lb-meta {
  font-size: 10.5px;
  color: rgba(255,255,255,0.55);
  margin-top: 3px;
  display: flex; align-items: center; gap: 8px;
}
.lb-meta b { color: rgba(255,255,255,0.88); font-weight: 900; }
.lb-trend {
  font-size: 10px; font-weight: 700;
  padding: 2px 6px;
  border-radius: 4px;
}
.lb-trend.up { color: #46d369; background: rgba(70,211,105,0.12); }
.lb-trend.down { color: #ff6b6b; background: rgba(229,9,20,0.12); }
.lb-trend.same { color: rgba(255,255,255,0.5); background: rgba(255,255,255,0.06); }"""

if CSS_MARKER not in content:
    print("ERROR: CSS marker not found", file=sys.stderr); sys.exit(1)
content = content.replace(CSS_MARKER, CSS_NEW)

# === 2. JS ===
JS_MARKER = """// Rebind hero play button
document.addEventListener('click', (e) => {
  const btn = e.target.closest('.nflx-btn.color-primary');
  if (!btn) return;
  e.preventDefault();
  heroPlayHandler();
}, true);"""

JS_NEW = JS_MARKER + """

/* ═══════════════════════════════════════════
   COMMIT 8 · Leaderboard (Phase 2C mock)
   ═══════════════════════════════════════════ */
async function buildLeaderboardRow() {
  try {
    const res = await fetch('leaderboard.json', { cache: 'no-store' });
    if (!res.ok) return;
    const data = await res.json();
    const clubs = (data && data.clubs) || [];
    if (!clubs.length) return;
    const container = document.getElementById('rowsContainer');
    if (!container) return;
    // Remove existing leaderboard row (re-render safe)
    const existing = document.getElementById('leaderboardRow');
    if (existing) existing.remove();

    const trendLabel = { up: '↑', down: '↓', same: '—' };
    const trophy = (r) => r === 1 ? '🥇' : r === 2 ? '🥈' : r === 3 ? '🥉' : '';
    const cards = clubs.map((c, i) => {
      const rank = i + 1;
      const safeName = (c.name || '').replace(/[<>&"']/g, ch => ({'<':'&lt;','>':'&gt;','&':'&amp;','"':'&quot;',"'":'&#39;'}[ch]));
      const safeLeader = (c.leader || '').replace(/[<>&"']/g, ch => ({'<':'&lt;','>':'&gt;','&':'&amp;','"':'&quot;',"'":'&#39;'}[ch]));
      const trend = c.trend || 'same';
      return `
        <div class="slider-item">
          <div class="leaderboard-card" data-rank="${rank}">
            <div class="lb-rank">${trophy(rank) || '#' + rank}</div>
            <div class="lb-body">
              <div class="lb-name">${safeName}</div>
              <div class="lb-meta">
                <span><b>${(c.points || 0).toLocaleString('he-IL')}</b> נק'</span>
                <span>· ${safeLeader}</span>
                <span class="lb-trend ${trend}">${trendLabel[trend]}</span>
              </div>
            </div>
          </div>
        </div>
      `;
    }).join('');

    const weekLabel = data.week_of ? `· ${data.week_of}` : '';
    const rowHtml = `
      <section class="row leaderboard-row" id="leaderboardRow">
        <div class="row-header">
          <h2 class="rowTitle">הלוח של המועדונים ${weekLabel}</h2>
        </div>
        <div class="row-container">
          <div class="rowContent">${cards}</div>
        </div>
      </section>
    `;
    container.insertAdjacentHTML('beforeend', rowHtml);
  } catch (e) {
    console.warn('leaderboard load failed', e);
  }
}
setTimeout(buildLeaderboardRow, 2000);"""

if JS_MARKER not in content:
    print("ERROR: JS marker not found", file=sys.stderr); sys.exit(1)
content = content.replace(JS_MARKER, JS_NEW)

TARGET.write_text(content, encoding='utf-8')
print(f"OK: commit 8 applied. Size: {len(content)} bytes")
