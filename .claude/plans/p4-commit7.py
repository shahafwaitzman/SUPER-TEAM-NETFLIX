#!/usr/bin/env python3
"""Commit 7 · Profile panel + Hero Play button.
  - Click S icon → slide-in panel from inline-start
  - Shows email, streak, badges (earned+locked), stats, module progress, logout
  - Hero "הפעל" button: featured.json → lastWatched → first video fallback
"""
import sys
from pathlib import Path

TARGET = Path("/Users/shahafwaitzman/Documents/CLOUD CODE/super-team-academy/academy-hub.html")
content = TARGET.read_text(encoding='utf-8')

# === 1. CSS for profile panel ===
CSS_MARKER = """.notif-item-dot {
  width: 8px; height: 8px;
  border-radius: 50%;
  background: var(--nflx-red, #E50914);
  flex-shrink: 0;
  box-shadow: 0 0 5px rgba(229,9,20,0.55);
}"""

CSS_NEW = CSS_MARKER + """

/* ═══════════════════════════════════════════
   COMMIT 7 · Profile panel (slide-in)
   ═══════════════════════════════════════════ */
.profile-panel-backdrop {
  position: fixed; inset: 0;
  background: rgba(0,0,0,0.5);
  backdrop-filter: blur(3px);
  -webkit-backdrop-filter: blur(3px);
  z-index: 300;
  opacity: 0; pointer-events: none;
  transition: opacity 0.25s;
}
.profile-panel-backdrop.open { opacity: 1; pointer-events: auto; }

.profile-panel {
  position: fixed;
  top: 0; bottom: 0;
  inset-inline-start: 0;
  width: 380px; max-width: 92vw;
  background: linear-gradient(180deg, #181818 0%, #0b0b0b 100%);
  border-inline-end: 1px solid rgba(255,255,255,0.1);
  z-index: 301;
  transform: translateX(-100%);
  transition: transform 0.4s cubic-bezier(0.2, 0.8, 0.2, 1);
  display: flex; flex-direction: column;
  box-shadow: 18px 0 60px rgba(0,0,0,0.5);
}
html[dir="rtl"] .profile-panel { transform: translateX(100%); }
.profile-panel.open { transform: translateX(0); }

.pp-head {
  padding: 20px 20px 16px;
  border-bottom: 1px solid rgba(255,255,255,0.08);
  display: flex; align-items: center; gap: 12px;
}
.pp-avatar {
  width: 48px; height: 48px; border-radius: 50%;
  background: linear-gradient(135deg, var(--nflx-red, #E50914), #7a0e12);
  display: flex; align-items: center; justify-content: center;
  color: #fff; font-size: 22px; font-weight: 900;
  box-shadow: 0 4px 14px rgba(229,9,20,0.35);
}
.pp-info { flex: 1; min-width: 0; }
.pp-info-name { font-size: 15px; font-weight: 800; color: #fff; }
.pp-info-email { font-size: 11px; color: rgba(255,255,255,0.55); margin-top: 2px; word-break: break-all; }
.pp-close {
  width: 32px; height: 32px; border-radius: 50%;
  background: rgba(255,255,255,0.08);
  border: none; color: #fff;
  font-size: 18px; cursor: pointer;
  display: flex; align-items: center; justify-content: center;
  font-family: inherit;
}
.pp-close:hover { background: rgba(229,9,20,0.3); }

.pp-body { flex: 1; overflow-y: auto; padding: 16px 20px 8px; }

.pp-section { margin-bottom: 20px; }
.pp-section-title {
  font-size: 10.5px; font-weight: 800;
  color: rgba(255,255,255,0.55);
  text-transform: uppercase; letter-spacing: 1.8px;
  margin-bottom: 10px;
}

.pp-stat-row {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 8px;
}
.pp-stat-cell {
  padding: 12px 10px;
  background: rgba(255,255,255,0.03);
  border: 1px solid rgba(255,255,255,0.06);
  border-radius: 10px;
  text-align: center;
}
.pp-stat-num {
  font-size: 22px; font-weight: 900;
  color: #fff;
  line-height: 1;
}
.pp-stat-label {
  font-size: 10px; font-weight: 700;
  color: rgba(255,255,255,0.55);
  margin-top: 6px;
  letter-spacing: 0.3px;
}

.pp-streak {
  display: flex; align-items: center; gap: 14px;
  padding: 14px 16px;
  border-radius: 12px;
  background: linear-gradient(135deg, rgba(229,9,20,0.15), rgba(245,130,32,0.08));
  border: 1px solid rgba(229,9,20,0.3);
}
.pp-streak-emoji { font-size: 28px; }
.pp-streak-num {
  font-size: 30px; font-weight: 900; color: #fff;
  line-height: 1;
}
.pp-streak-label { font-size: 11px; color: rgba(255,255,255,0.7); }

.pp-badges {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 8px;
}
.pp-badge {
  aspect-ratio: 1;
  border-radius: 10px;
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.06);
  display: flex; flex-direction: column;
  align-items: center; justify-content: center;
  padding: 6px; gap: 3px;
  text-align: center;
  position: relative;
  cursor: default;
  transition: transform 0.2s, border-color 0.2s;
}
.pp-badge:hover { transform: scale(1.05); }
.pp-badge.earned {
  background: linear-gradient(135deg, rgba(245,197,24,0.18), rgba(229,9,20,0.08));
  border-color: rgba(245,197,24,0.45);
  box-shadow: 0 0 14px rgba(245,197,24,0.18);
}
.pp-badge.locked { opacity: 0.4; filter: grayscale(0.9); }
.pp-badge-icon { font-size: 22px; line-height: 1; }
.pp-badge-title {
  font-size: 8.5px; font-weight: 800;
  color: rgba(255,255,255,0.85);
  line-height: 1.1;
  margin-top: 2px;
}

.pp-module {
  margin-bottom: 8px;
  padding: 10px 12px;
  background: rgba(255,255,255,0.03);
  border: 1px solid rgba(255,255,255,0.06);
  border-radius: 8px;
}
.pp-module-head {
  display: flex; align-items: center; justify-content: space-between;
  font-size: 11.5px; font-weight: 700;
  color: rgba(255,255,255,0.92);
  margin-bottom: 6px;
}
.pp-module-count {
  font-size: 10px; color: rgba(255,255,255,0.55);
  font-weight: 600;
}
.pp-module-bar {
  height: 4px;
  background: rgba(255,255,255,0.1);
  border-radius: 3px; overflow: hidden;
}
.pp-module-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--nflx-red, #E50914), #ff6b6b);
  border-radius: 3px;
  transition: width 0.5s;
}

.pp-foot {
  padding: 14px 20px 20px;
  border-top: 1px solid rgba(255,255,255,0.08);
}
.pp-logout-btn {
  width: 100%;
  padding: 11px;
  border-radius: 8px;
  background: transparent;
  border: 1px solid rgba(255,255,255,0.15);
  color: rgba(255,255,255,0.85);
  font-size: 13px; font-weight: 700;
  cursor: pointer;
  font-family: inherit;
  transition: all 0.2s;
}
.pp-logout-btn:hover {
  background: rgba(229,9,20,0.15);
  border-color: var(--nflx-red, #E50914);
  color: #fff;
}"""

if CSS_MARKER not in content:
    print("ERROR: CSS marker not found", file=sys.stderr); sys.exit(1)
content = content.replace(CSS_MARKER, CSS_NEW)

# === 2. Add profile panel HTML (after video modal) ===
OLD_VIDEO_MODAL_END = """<div class="user-indicator" id="userIndicator" style="display:none;">
  <span>😊 </span><span id="userNameDisplay"></span>
</div>"""

NEW_PANEL = """<div class="user-indicator" id="userIndicator" style="display:none;">
  <span>😊 </span><span id="userNameDisplay"></span>
</div>

<!-- Profile Panel -->
<div class="profile-panel-backdrop" id="profilePanelBackdrop"></div>
<aside class="profile-panel" id="profilePanel" aria-hidden="true" aria-label="פרופיל">
  <div class="pp-head">
    <div class="pp-avatar" id="ppAvatar">S</div>
    <div class="pp-info">
      <div class="pp-info-name" id="ppName">משתמש</div>
      <div class="pp-info-email" id="ppEmail">—</div>
    </div>
    <button class="pp-close" id="ppCloseBtn" aria-label="סגור">✕</button>
  </div>
  <div class="pp-body">
    <section class="pp-section">
      <div class="pp-section-title">סטטיסטיקות</div>
      <div class="pp-stat-row">
        <div class="pp-stat-cell"><div class="pp-stat-num" id="ppStatStarted">0</div><div class="pp-stat-label">הותחלו</div></div>
        <div class="pp-stat-cell"><div class="pp-stat-num" id="ppStatCompleted">0</div><div class="pp-stat-label">הושלמו</div></div>
        <div class="pp-stat-cell"><div class="pp-stat-num" id="ppStatWatchlist">0</div><div class="pp-stat-label">ברשימה</div></div>
      </div>
    </section>

    <section class="pp-section">
      <div class="pp-section-title">רצף</div>
      <div class="pp-streak">
        <span class="pp-streak-emoji">🔥</span>
        <div>
          <div class="pp-streak-num" id="ppStreakNum">0</div>
          <div class="pp-streak-label">ימים ברצף</div>
        </div>
      </div>
    </section>

    <section class="pp-section">
      <div class="pp-section-title">מדליות</div>
      <div class="pp-badges" id="ppBadges"></div>
    </section>

    <section class="pp-section">
      <div class="pp-section-title">התקדמות במודולים</div>
      <div id="ppModules"></div>
    </section>
  </div>
  <div class="pp-foot">
    <button class="pp-logout-btn" id="ppLogoutBtn">יציאה</button>
  </div>
</aside>"""

if OLD_VIDEO_MODAL_END not in content:
    print("ERROR: user-indicator block not found", file=sys.stderr); sys.exit(1)
content = content.replace(OLD_VIDEO_MODAL_END, NEW_PANEL)

# === 3. Append JS for profile panel + hero play button ===
JS_MARKER = """// Initial render + refresh
setTimeout(renderNotifications, 3000);
setInterval(renderNotifications, 30000);"""

JS_NEW = JS_MARKER + """

/* ═══════════════════════════════════════════
   COMMIT 7 · Profile panel
   ═══════════════════════════════════════════ */
function openProfilePanel() {
  const panel = document.getElementById('profilePanel');
  const back = document.getElementById('profilePanelBackdrop');
  if (!panel || !back) return;
  renderProfilePanel();
  panel.classList.add('open');
  panel.setAttribute('aria-hidden', 'false');
  back.classList.add('open');
}
function closeProfilePanel() {
  const panel = document.getElementById('profilePanel');
  const back = document.getElementById('profilePanelBackdrop');
  if (!panel || !back) return;
  panel.classList.remove('open');
  panel.setAttribute('aria-hidden', 'true');
  back.classList.remove('open');
}

function renderProfilePanel() {
  // Header
  const email = userEmail || '—';
  const name = (email && email.split) ? email.split('@')[0] : 'משתמש';
  const initial = (name.charAt(0) || 'S').toUpperCase();
  document.getElementById('ppAvatar').textContent = initial;
  document.getElementById('ppName').textContent = name;
  document.getElementById('ppEmail').textContent = email;

  // Stats
  const progress = stGet(ST_KEYS.PROGRESS, {});
  const started = Object.values(progress).filter(p => p > 0).length;
  const completed = Object.values(progress).filter(p => p >= 90).length;
  const watchlist = (stGet(ST_KEYS.WATCHLIST, []) || []).length;
  document.getElementById('ppStatStarted').textContent = started;
  document.getElementById('ppStatCompleted').textContent = completed;
  document.getElementById('ppStatWatchlist').textContent = watchlist;

  // Streak
  const streak = stGet(ST_KEYS.STREAK, { count: 0 });
  document.getElementById('ppStreakNum').textContent = streak.count || 0;

  // Badges
  const earned = new Set(stGet(ST_KEYS.BADGES, []));
  const badgesHtml = Object.entries(BADGE_DEFS).map(([id, b]) => {
    const isE = earned.has(id);
    const safeTitle = b.title.replace(/[<>&"']/g, c => ({'<':'&lt;','>':'&gt;','&':'&amp;','"':'&quot;',"'":'&#39;'}[c]));
    return `
      <div class="pp-badge ${isE ? 'earned' : 'locked'}" title="${b.title} · ${b.desc}">
        <div class="pp-badge-icon">${b.icon}</div>
        <div class="pp-badge-title">${safeTitle}</div>
      </div>
    `;
  }).join('');
  document.getElementById('ppBadges').innerHTML = badgesHtml;

  // Modules (per-folder)
  const byCat = {};
  document.querySelectorAll('.title-card-container[data-video-id][data-category]').forEach(c => {
    const cat = decodeURIComponent(c.dataset.category || '');
    if (!cat) return;
    if (!byCat[cat]) byCat[cat] = { total: 0, done: 0 };
    byCat[cat].total++;
    if ((progress[c.dataset.videoId] || 0) > 0) byCat[cat].done++;
  });
  const modulesHtml = Object.entries(byCat).map(([cat, s]) => {
    const pct = s.total ? Math.round((s.done / s.total) * 100) : 0;
    const safeCat = cat.replace(/[<>&"']/g, c => ({'<':'&lt;','>':'&gt;','&':'&amp;','"':'&quot;',"'":'&#39;'}[c]));
    return `
      <div class="pp-module">
        <div class="pp-module-head"><span>${safeCat}</span><span class="pp-module-count">${s.done}/${s.total}</span></div>
        <div class="pp-module-bar"><div class="pp-module-fill" style="width:${pct}%"></div></div>
      </div>
    `;
  }).join('') || '<div class="notif-empty">אין עדיין נתונים</div>';
  document.getElementById('ppModules').innerHTML = modulesHtml;
}

// Hook: click S icon opens panel
document.addEventListener('click', (e) => {
  const icon = e.target.closest('#profileIcon');
  if (icon) { openProfilePanel(); return; }
  const close = e.target.closest('#ppCloseBtn') || e.target.closest('#profilePanelBackdrop');
  if (close) { closeProfilePanel(); return; }
  const logout = e.target.closest('#ppLogoutBtn');
  if (logout) {
    if (confirm('לצאת מהחשבון? הנתונים המקומיים יישמרו.')) {
      localStorage.removeItem('userEmail');
      window.location.href = 'entry.html';
    }
  }
});
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') closeProfilePanel();
});

/* ═══════════════════════════════════════════
   COMMIT 7 · Hero Play button — smart pick
   Priority: featured.json → lastWatched → first card
   ═══════════════════════════════════════════ */
async function getHeroTarget() {
  // 1. Try featured.json
  try {
    const res = await fetch('featured.json', { cache: 'no-store' });
    if (res.ok) {
      const data = await res.json();
      if (data && data.featured_video_id) {
        const weekTs = data.week_of ? new Date(data.week_of).getTime() : 0;
        if (!weekTs || Date.now() - weekTs < 14 * 24 * 3600 * 1000) {
          return { id: data.featured_video_id, source: 'featured' };
        }
      }
    }
  } catch (e) { /* file missing — fall through */ }
  // 2. Last watched
  const lw = stGet(ST_KEYS.LAST_WATCHED, {});
  const last = Object.entries(lw).sort((a, b) => (b[1].ts || 0) - (a[1].ts || 0))[0];
  if (last && last[0]) return { id: last[0], source: 'lastWatched' };
  // 3. First visible card
  const first = document.querySelector('.row:not(#continueWatchingRow) .title-card-container[data-video-id]');
  if (first) return { id: first.dataset.videoId, source: 'first' };
  return null;
}
async function heroPlayHandler() {
  const target = await getHeroTarget();
  if (!target) { scrollToRows(); return; }
  const card = document.querySelector(`.title-card-container[data-video-id="${target.id}"]`);
  if (card) { card.click(); return; }
  // Target not visible — fallback scroll
  scrollToRows();
}
// Rebind hero play button
document.addEventListener('click', (e) => {
  const btn = e.target.closest('.nflx-btn.color-primary');
  if (!btn) return;
  e.preventDefault();
  heroPlayHandler();
}, true);"""

if JS_MARKER not in content:
    print("ERROR: JS marker not found", file=sys.stderr); sys.exit(1)
content = content.replace(JS_MARKER, JS_NEW)

TARGET.write_text(content, encoding='utf-8')
print(f"OK: commit 7 applied. Size: {len(content)} bytes")
