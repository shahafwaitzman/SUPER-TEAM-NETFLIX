#!/usr/bin/env python3
"""Commit 6 · Notifications dropdown.
  - Bell → red badge with count of unseen new videos (modifiedTime within 7d)
  - Click bell → dropdown with list
  - Click item → mark seen, play (via click on hidden card trigger)
  - Click outside → close dropdown
"""
import sys
from pathlib import Path

TARGET = Path("/Users/shahafwaitzman/Documents/CLOUD CODE/super-team-academy/academy-hub.html")
content = TARGET.read_text(encoding='utf-8')

# === 1. CSS for notification badge + dropdown ===
CSS_MARKER = """.sta-toast.badge-toast {
  border-color: rgba(245,197,24,0.55);
  box-shadow: 0 10px 30px rgba(0,0,0,0.5), 0 0 28px rgba(245,197,24,0.3);
}"""

CSS_NEW = CSS_MARKER + """

/* ═══════════════════════════════════════════
   COMMIT 6 · Notifications
   ═══════════════════════════════════════════ */
.notif-wrap { position: relative; }
.notif-badge {
  position: absolute;
  top: -2px; inset-inline-end: -2px;
  min-width: 16px; height: 16px;
  padding: 0 5px;
  border-radius: 10px;
  background: #E50914;
  color: #fff;
  font-size: 9px; font-weight: 900;
  display: flex; align-items: center; justify-content: center;
  box-shadow: 0 2px 6px rgba(0,0,0,0.5);
  border: 1.5px solid rgba(0,0,0,0.7);
  pointer-events: none;
}
.notif-badge[data-count="0"] { display: none; }

.notif-dropdown {
  position: absolute;
  top: calc(100% + 10px);
  inset-inline-end: 0;
  z-index: 200;
  width: 340px;
  max-height: 440px;
  background: rgba(20,20,20,0.98);
  border: 1px solid rgba(255,255,255,0.12);
  border-radius: 10px;
  box-shadow: 0 24px 60px rgba(0,0,0,0.65);
  overflow: hidden;
  display: none;
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
}
.notif-dropdown.open { display: flex; flex-direction: column; }
.notif-dropdown-head {
  display: flex; align-items: center; justify-content: space-between;
  padding: 14px 16px;
  border-bottom: 1px solid rgba(255,255,255,0.08);
}
.notif-dropdown-head h4 {
  font-size: 13px; font-weight: 800;
  color: #fff; margin: 0;
  letter-spacing: 0.4px;
}
.notif-clear {
  background: transparent; border: none;
  color: rgba(255,255,255,0.55);
  font-size: 11px; font-weight: 700;
  cursor: pointer;
  padding: 4px 8px;
  font-family: inherit;
  transition: color 0.2s;
}
.notif-clear:hover { color: var(--nflx-red, #E50914); }
.notif-list {
  flex: 1;
  overflow-y: auto;
  padding: 6px 0;
}
.notif-empty {
  padding: 32px 16px;
  text-align: center;
  color: rgba(255,255,255,0.5);
  font-size: 12px;
}
.notif-item {
  display: flex; align-items: center; gap: 10px;
  padding: 10px 14px;
  cursor: pointer;
  border-inline-start: 3px solid transparent;
  transition: background 0.15s, border-color 0.15s;
}
.notif-item:hover {
  background: rgba(229,9,20,0.08);
  border-inline-start-color: var(--nflx-red, #E50914);
}
.notif-item-icon {
  flex-shrink: 0;
  width: 36px; height: 36px;
  border-radius: 8px;
  background: linear-gradient(135deg, rgba(229,9,20,0.3), rgba(229,9,20,0.08));
  display: flex; align-items: center; justify-content: center;
  font-size: 15px;
  color: #fff;
}
.notif-item-body { flex: 1; min-width: 0; }
.notif-item-title {
  font-size: 12px; font-weight: 700;
  color: rgba(255,255,255,0.96);
  line-height: 1.3;
  overflow: hidden; text-overflow: ellipsis;
  white-space: nowrap;
}
.notif-item-meta {
  font-size: 10px;
  color: rgba(255,255,255,0.5);
  margin-top: 2px;
  letter-spacing: 0.2px;
}
.notif-item-dot {
  width: 8px; height: 8px;
  border-radius: 50%;
  background: var(--nflx-red, #E50914);
  flex-shrink: 0;
  box-shadow: 0 0 5px rgba(229,9,20,0.55);
}"""

if CSS_MARKER not in content:
    print("ERROR: CSS marker not found", file=sys.stderr); sys.exit(1)
content = content.replace(CSS_MARKER, CSS_NEW)

# === 2. Replace bell <button> with wrapped version that has badge + dropdown placeholder ===
OLD_BELL = """    <li><button class="nav-icon-btn" aria-label="התראות">
      <svg viewBox="0 0 24 24" fill="none"><path fill="currentColor" fill-rule="evenodd" d="M13 4.07A7 7 0 0 1 19 11v4.25q1.58.12 3.1.28l-.2 2a93 93 0 0 0-19.8 0l-.2-2q1.52-.15 3.1-.28V11a7 7 0 0 1 6-6.93V2h2zm4 11.06V11a5 5 0 0 0-10 0v4.13a97 97 0 0 1 10 0m-8.37 4.24C8.66 20.52 10.15 22 12 22s3.34-1.48 3.37-2.63c.01-.22-.2-.37-.42-.37h-5.9c-.23 0-.43.15-.42.37" clip-rule="evenodd"/></svg>
    </button></li>"""

NEW_BELL = """    <li class="notif-wrap">
      <button class="nav-icon-btn" id="notifBtn" aria-label="התראות">
        <svg viewBox="0 0 24 24" fill="none"><path fill="currentColor" fill-rule="evenodd" d="M13 4.07A7 7 0 0 1 19 11v4.25q1.58.12 3.1.28l-.2 2a93 93 0 0 0-19.8 0l-.2-2q1.52-.15 3.1-.28V11a7 7 0 0 1 6-6.93V2h2zm4 11.06V11a5 5 0 0 0-10 0v4.13a97 97 0 0 1 10 0m-8.37 4.24C8.66 20.52 10.15 22 12 22s3.34-1.48 3.37-2.63c.01-.22-.2-.37-.42-.37h-5.9c-.23 0-.43.15-.42.37" clip-rule="evenodd"/></svg>
        <span class="notif-badge" id="notifBadge" data-count="0">0</span>
      </button>
      <div class="notif-dropdown" id="notifDropdown" role="menu">
        <div class="notif-dropdown-head">
          <h4>התראות · חדשים השבוע</h4>
          <button class="notif-clear" id="notifClearBtn">סמן הכל כנקרא</button>
        </div>
        <div class="notif-list" id="notifList">
          <div class="notif-empty">אין התראות חדשות</div>
        </div>
      </div>
    </li>"""

if OLD_BELL not in content:
    print("ERROR: bell not found", file=sys.stderr); sys.exit(1)
content = content.replace(OLD_BELL, NEW_BELL)

# === 3. Append notification JS ===
JS_MARKER = """// Run once after rows + seed settle, then every 30s alongside progress renders
setTimeout(recomputeBadges, 3500);
setInterval(recomputeBadges, 30000);"""

JS_NEW = JS_MARKER + """

/* ═══════════════════════════════════════════
   COMMIT 6 · Notifications (new videos, last 7d)
   ═══════════════════════════════════════════ */
function collectNewVideos() {
  const weekAgo = Date.now() - 7 * 24 * 3600 * 1000;
  const seen = new Set(stGet(ST_KEYS.NOTIFICATIONS_SEEN, []));
  const cards = Array.from(document.querySelectorAll('.title-card-container[data-video-id]'));
  const byId = new Map();
  cards.forEach(c => {
    const id = c.dataset.videoId;
    if (!id || byId.has(id) || seen.has(id)) return;
    const m = c.dataset.modified;
    if (!m) return;
    const ts = new Date(m).getTime();
    if (!isFinite(ts) || ts < weekAgo) return;
    const title = decodeURIComponent(c.dataset.videoTitle || '');
    const cat = decodeURIComponent(c.dataset.category || '');
    byId.set(id, { id, title, cat, ts });
  });
  return Array.from(byId.values()).sort((a, b) => b.ts - a.ts);
}

function renderNotifications() {
  const list = document.getElementById('notifList');
  const badge = document.getElementById('notifBadge');
  if (!list || !badge) return;
  const items = collectNewVideos();
  badge.setAttribute('data-count', String(items.length));
  badge.textContent = items.length > 9 ? '9+' : String(items.length);

  if (items.length === 0) {
    list.innerHTML = '<div class="notif-empty">אין התראות חדשות</div>';
    return;
  }
  list.innerHTML = items.map(it => {
    const daysAgo = Math.floor((Date.now() - it.ts) / (24 * 3600 * 1000));
    const whenLabel = daysAgo === 0 ? 'היום' : (daysAgo === 1 ? 'אתמול' : `לפני ${daysAgo} ימים`);
    const safeTitle = (it.title || '').replace(/[<>&"']/g, c => ({'<':'&lt;','>':'&gt;','&':'&amp;','"':'&quot;',"'":'&#39;'}[c]));
    const safeCat = (it.cat || '').replace(/[<>&"']/g, c => ({'<':'&lt;','>':'&gt;','&':'&amp;','"':'&quot;',"'":'&#39;'}[c]));
    return `
      <div class="notif-item" data-video-id="${it.id}" role="menuitem" tabindex="0">
        <div class="notif-item-icon">▶</div>
        <div class="notif-item-body">
          <div class="notif-item-title">${safeTitle}</div>
          <div class="notif-item-meta">${safeCat} · ${whenLabel}</div>
        </div>
        <div class="notif-item-dot" aria-hidden="true"></div>
      </div>
    `;
  }).join('');
}

function markNotifSeen(videoId) {
  if (!videoId) return;
  stPush(ST_KEYS.NOTIFICATIONS_SEEN, videoId);
  renderNotifications();
}

// Click bell → toggle dropdown
document.addEventListener('click', (e) => {
  const btn = e.target.closest('#notifBtn');
  const dd = document.getElementById('notifDropdown');
  if (btn && dd) {
    e.stopPropagation();
    dd.classList.toggle('open');
    if (dd.classList.contains('open')) renderNotifications();
    return;
  }
  const item = e.target.closest('.notif-item');
  if (item && dd) {
    const id = item.dataset.videoId;
    markNotifSeen(id);
    dd.classList.remove('open');
    // Trigger click on the matching card (so existing openVideo logic fires)
    const card = document.querySelector(`.title-card-container[data-video-id="${id}"]`);
    if (card) card.click();
    return;
  }
  const clear = e.target.closest('#notifClearBtn');
  if (clear) {
    e.stopPropagation();
    const items = collectNewVideos();
    items.forEach(it => stPush(ST_KEYS.NOTIFICATIONS_SEEN, it.id));
    renderNotifications();
    return;
  }
  // Click outside → close
  if (dd && dd.classList.contains('open') && !e.target.closest('.notif-wrap')) {
    dd.classList.remove('open');
  }
});

// Initial render + refresh
setTimeout(renderNotifications, 3000);
setInterval(renderNotifications, 30000);"""

if JS_MARKER not in content:
    print("ERROR: JS marker not found", file=sys.stderr); sys.exit(1)
content = content.replace(JS_MARKER, JS_NEW)

TARGET.write_text(content, encoding='utf-8')
print(f"OK: commit 6 applied. Size: {len(content)} bytes")
