#!/usr/bin/env python3
"""Commit 4 · Overall progress + Watchlist + Nav filters.
  - Overall progress pill in header (shows X/Y + red bar)
  - Watchlist add/remove button on each card (+ / ✓)
  - Toast notification on watchlist actions
  - Working nav tabs: home / courses / new / my-list (+ search placeholder)
  - Active state: red underline under current tab
"""
import sys
from pathlib import Path

TARGET = Path("/Users/shahafwaitzman/Documents/CLOUD CODE/super-team-academy/academy-hub.html")
content = TARGET.read_text(encoding='utf-8')

# === 1. Inject CSS for overall progress pill + watchlist button + toast + nav active state ===
CSS_MARKER = """/* Continue Watching row gets a subtle accent badge */
.row.continue-row .rowTitle::before {
  content: '▶';
  color: var(--nflx-red, #E50914);
  margin-inline-end: 8px;
  font-size: 0.85em;
}"""

CSS_NEW = CSS_MARKER + """

/* ═══════════════════════════════════════════
   COMMIT 4 · Overall progress / Watchlist / Nav filters
   ═══════════════════════════════════════════ */

/* Overall progress pill in header */
.overall-progress-pill {
  display: flex; align-items: center; gap: 8px;
  padding: 6px 12px;
  border-radius: 20px;
  background: rgba(255,255,255,0.06);
  border: 1px solid rgba(255,255,255,0.12);
  font-size: 11px; font-weight: 700;
  color: rgba(255,255,255,0.9);
  white-space: nowrap;
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
}
.op-label {
  font-size: 12px; font-weight: 800;
  color: #fff;
  letter-spacing: 0.5px;
}
.op-bar {
  width: 80px; height: 5px;
  background: rgba(255,255,255,0.18);
  border-radius: 3px;
  overflow: hidden;
  position: relative;
}
.op-fill {
  height: 100%;
  background: linear-gradient(90deg, #E50914, #ff6b6b);
  border-radius: 3px;
  box-shadow: 0 0 6px rgba(229,9,20,0.55);
  transition: width 0.6s cubic-bezier(0.2,0.8,0.2,1);
}
.op-caption {
  font-size: 9px; font-weight: 700;
  color: rgba(255,255,255,0.55);
  text-transform: uppercase;
  letter-spacing: 1px;
}

/* Watchlist + button on card */
.watchlist-btn {
  position: absolute;
  top: 8px; inset-inline-end: 8px;
  z-index: 6;
  width: 30px; height: 30px;
  border-radius: 50%;
  background: rgba(0,0,0,0.65);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1.5px solid rgba(255,255,255,0.35);
  color: #fff;
  display: flex; align-items: center; justify-content: center;
  cursor: pointer;
  font-size: 18px; font-weight: 700; line-height: 1;
  opacity: 0;
  transform: scale(0.85);
  transition: opacity 0.2s, transform 0.2s, background 0.2s, border-color 0.2s;
  padding: 0;
}
.title-card-container:hover .watchlist-btn {
  opacity: 1; transform: scale(1);
}
.watchlist-btn:hover {
  background: rgba(229,9,20,0.85);
  border-color: #E50914;
}
.watchlist-btn.in-list {
  opacity: 1; transform: scale(1);
  background: rgba(229,9,20,0.85);
  border-color: #E50914;
}

/* Toast notification */
.sta-toast {
  position: fixed;
  bottom: 30px; left: 50%;
  transform: translateX(-50%) translateY(20px);
  z-index: 9999;
  padding: 12px 22px;
  border-radius: 30px;
  background: rgba(20,20,20,0.95);
  border: 1px solid rgba(229,9,20,0.45);
  color: #fff;
  font-size: 13px; font-weight: 700;
  box-shadow: 0 10px 30px rgba(0,0,0,0.5), 0 0 20px rgba(229,9,20,0.2);
  opacity: 0;
  transition: opacity 0.3s, transform 0.3s cubic-bezier(0.2,0.8,0.2,1);
  pointer-events: none;
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
  white-space: nowrap;
}
.sta-toast.show {
  opacity: 1;
  transform: translateX(-50%) translateY(0);
}

/* Nav active state — red underline */
.navigation-tab a {
  position: relative;
  padding-bottom: 4px;
  transition: color 0.2s;
}
.navigation-tab a.current {
  color: #fff;
}
.navigation-tab a.current::after {
  content: '';
  position: absolute;
  bottom: 0; left: 0; right: 0;
  height: 2px;
  background: #E50914;
  border-radius: 2px;
  box-shadow: 0 0 8px rgba(229,9,20,0.6);
}

/* Filtering — hide rows/cards based on active filter */
.row.filter-hidden,
.slider-item.filter-hidden { display: none !important; }"""

if CSS_MARKER not in content:
    print("ERROR: CSS marker not found", file=sys.stderr); sys.exit(1)
content = content.replace(CSS_MARKER, CSS_NEW)

# === 2. Add overall-progress pill + data-modified to nav ===
OLD_NAV = """  <ul class="secondary-navigation">
    <li><button class="nav-icon-btn" aria-label="חיפוש">
      <svg viewBox="0 0 24 24" fill="none"><path fill="currentColor" fill-rule="evenodd" d="M17 10a7 7 0 1 1-14 0 7 7 0 0 1 14 0m-1.38 7.03a9 9 0 1 1 1.41-1.41l5.68 5.67-1.42 1.42z" clip-rule="evenodd"/></svg>
    </button></li>
    <li><button class="nav-icon-btn" aria-label="התראות">
      <svg viewBox="0 0 24 24" fill="none"><path fill="currentColor" fill-rule="evenodd" d="M13 4.07A7 7 0 0 1 19 11v4.25q1.58.12 3.1.28l-.2 2a93 93 0 0 0-19.8 0l-.2-2q1.52-.15 3.1-.28V11a7 7 0 0 1 6-6.93V2h2zm4 11.06V11a5 5 0 0 0-10 0v4.13a97 97 0 0 1 10 0m-8.37 4.24C8.66 20.52 10.15 22 12 22s3.34-1.48 3.37-2.63c.01-.22-.2-.37-.42-.37h-5.9c-.23 0-.43.15-.42.37" clip-rule="evenodd"/></svg>
    </button></li>
    <li><div class="profile-icon" id="profileIcon">S</div></li>
  </ul>"""

NEW_NAV = """  <ul class="secondary-navigation">
    <li id="overallProgressWrap" class="overall-progress-pill" style="display:none;" title="וידאוז שהותחלו">
      <span class="op-caption">התקדמות</span>
      <span class="op-label" id="opLabel">0/0</span>
      <div class="op-bar"><div class="op-fill" id="opFill" style="width:0%"></div></div>
    </li>
    <li><button class="nav-icon-btn" aria-label="חיפוש">
      <svg viewBox="0 0 24 24" fill="none"><path fill="currentColor" fill-rule="evenodd" d="M17 10a7 7 0 1 1-14 0 7 7 0 0 1 14 0m-1.38 7.03a9 9 0 1 1 1.41-1.41l5.68 5.67-1.42 1.42z" clip-rule="evenodd"/></svg>
    </button></li>
    <li><button class="nav-icon-btn" aria-label="התראות">
      <svg viewBox="0 0 24 24" fill="none"><path fill="currentColor" fill-rule="evenodd" d="M13 4.07A7 7 0 0 1 19 11v4.25q1.58.12 3.1.28l-.2 2a93 93 0 0 0-19.8 0l-.2-2q1.52-.15 3.1-.28V11a7 7 0 0 1 6-6.93V2h2zm4 11.06V11a5 5 0 0 0-10 0v4.13a97 97 0 0 1 10 0m-8.37 4.24C8.66 20.52 10.15 22 12 22s3.34-1.48 3.37-2.63c.01-.22-.2-.37-.42-.37h-5.9c-.23 0-.43.15-.42.37" clip-rule="evenodd"/></svg>
    </button></li>
    <li><div class="profile-icon" id="profileIcon">S</div></li>
  </ul>"""

if OLD_NAV not in content:
    print("ERROR: nav HTML not found", file=sys.stderr); sys.exit(1)
content = content.replace(OLD_NAV, NEW_NAV)

# === 3. Add data-filter attribute to nav tabs + data-modified/watchlist button to cards ===
OLD_TABS = """  <ul class="tabbed-primary-navigation">
    <li class="navigation-tab"><a href="#" class="current">דף הבית</a></li>
    <li class="navigation-tab"><a href="#">קורסים</a></li>
    <li class="navigation-tab"><a href="#">חדשים</a></li>
    <li class="navigation-tab"><a href="#">הרשימה שלי</a></li>
    <li class="navigation-tab"><a href="#">חיפוש לפי נושא</a></li>
  </ul>"""

NEW_TABS = """  <ul class="tabbed-primary-navigation">
    <li class="navigation-tab"><a href="#" class="current" data-nav="home">דף הבית</a></li>
    <li class="navigation-tab"><a href="#" data-nav="courses">קורסים</a></li>
    <li class="navigation-tab"><a href="#" data-nav="new">חדשים</a></li>
    <li class="navigation-tab"><a href="#" data-nav="mylist">הרשימה שלי</a></li>
    <li class="navigation-tab"><a href="#" data-nav="search">חיפוש לפי נושא</a></li>
  </ul>"""

if OLD_TABS not in content:
    print("ERROR: tabs HTML not found", file=sys.stderr); sys.exit(1)
content = content.replace(OLD_TABS, NEW_TABS)

# === 4. Update card template — add data-modified + watchlist button ===
OLD_CARD_OPEN = """        <div class="title-card-container" data-video-id="${f.id}" data-video-title="${encodeURIComponent(title)}">
          <div class="title-card">"""

NEW_CARD_OPEN = """        <div class="title-card-container" data-video-id="${f.id}" data-video-title="${encodeURIComponent(title)}" data-modified="${f.modifiedTime || ''}">
          <button type="button" class="watchlist-btn ${stHas(ST_KEYS.WATCHLIST, f.id) ? 'in-list' : ''}" data-video-id="${f.id}" aria-label="הוסף להרשימה שלי" title="הוסף להרשימה שלי">${stHas(ST_KEYS.WATCHLIST, f.id) ? '✓' : '+'}</button>
          <div class="title-card">"""

if OLD_CARD_OPEN not in content:
    print("ERROR: card-open marker not found", file=sys.stderr); sys.exit(1)
content = content.replace(OLD_CARD_OPEN, NEW_CARD_OPEN)

# === 5. Append JS: computeOverallProgress + renderOverallProgress + toast + watchlist toggle + nav filter ===
JS_MARKER = """// Run after rows are likely rendered (Drive fetch takes time)
setTimeout(seedDemoWatchHistory, 2500);"""

JS_NEW = JS_MARKER + """

/* ═══════════════════════════════════════════
   COMMIT 4 · Overall progress pill
   ═══════════════════════════════════════════ */
function computeOverallProgress() {
  const progress = stGet(ST_KEYS.PROGRESS, {});
  const started = Object.values(progress).filter(p => p > 0).length;
  const allCards = document.querySelectorAll('.title-card-container[data-video-id]');
  // Dedupe by videoId (Continue Watching row copies cards)
  const ids = new Set();
  allCards.forEach(c => { if (c.dataset.videoId) ids.add(c.dataset.videoId); });
  const total = ids.size;
  const pct = total ? Math.round((started / total) * 100) : 0;
  return { started, total, pct };
}

function renderOverallProgress() {
  const wrap = document.getElementById('overallProgressWrap');
  if (!wrap) return;
  const { started, total, pct } = computeOverallProgress();
  if (total === 0) { wrap.style.display = 'none'; return; }
  wrap.style.display = 'flex';
  document.getElementById('opLabel').textContent = `${started}/${total}`;
  document.getElementById('opFill').style.width = pct + '%';
  wrap.title = `${started} וידאוז הותחלו מתוך ${total} · ${pct}%`;
}
setTimeout(renderOverallProgress, 2800);
setInterval(renderOverallProgress, 30000);

/* ═══════════════════════════════════════════
   COMMIT 4 · Toast notification
   ═══════════════════════════════════════════ */
function showToast(msg) {
  let t = document.getElementById('staToast');
  if (!t) {
    t = document.createElement('div');
    t.id = 'staToast';
    t.className = 'sta-toast';
    document.body.appendChild(t);
  }
  t.textContent = msg;
  t.classList.add('show');
  clearTimeout(t._hideTimer);
  t._hideTimer = setTimeout(() => t.classList.remove('show'), 2400);
}

/* ═══════════════════════════════════════════
   COMMIT 4 · Watchlist toggle (delegated)
   ═══════════════════════════════════════════ */
document.addEventListener('click', (e) => {
  const btn = e.target.closest('.watchlist-btn');
  if (!btn) return;
  e.stopPropagation(); e.preventDefault();
  const id = btn.dataset.videoId;
  if (!id) return;
  const inList = stHas(ST_KEYS.WATCHLIST, id);
  if (inList) {
    stRemove(ST_KEYS.WATCHLIST, id);
    showToast('הוסר מהרשימה שלי');
  } else {
    stPush(ST_KEYS.WATCHLIST, id);
    showToast('✓ נוסף להרשימה שלי');
  }
  // Sync visual state across all copies of this card (rows + continue row)
  document.querySelectorAll(`.watchlist-btn[data-video-id="${id}"]`).forEach(b => {
    b.classList.toggle('in-list', !inList);
    b.textContent = (!inList) ? '✓' : '+';
  });
}, true);

/* ═══════════════════════════════════════════
   COMMIT 4 · Nav filters
   ═══════════════════════════════════════════ */
function applyNavFilter(mode) {
  const rows = document.querySelectorAll('.row, .billboard-row');
  const allItems = document.querySelectorAll('.slider-item');
  // Reset: show everything
  document.querySelectorAll('.row').forEach(r => r.classList.remove('filter-hidden'));
  allItems.forEach(i => i.classList.remove('filter-hidden'));
  // Remove virtual "my list" row if present
  const existingMyList = document.getElementById('myListRow');
  if (existingMyList) existingMyList.remove();

  if (mode === 'home') { return; }

  if (mode === 'courses') {
    document.querySelectorAll('.row').forEach(r => {
      const t = (r.querySelector('.rowTitle')?.textContent || '').toLowerCase();
      const match = t.includes('קורס') || t.includes('הדרכה') || t.includes('הדרכת');
      if (!match && r.id !== 'continueWatchingRow') r.classList.add('filter-hidden');
    });
    return;
  }

  if (mode === 'new') {
    const weekAgo = Date.now() - 7 * 24 * 3600 * 1000;
    document.querySelectorAll('.slider-item').forEach(item => {
      const card = item.querySelector('.title-card-container');
      const m = card?.dataset.modified;
      if (!m) { item.classList.add('filter-hidden'); return; }
      const ts = new Date(m).getTime();
      if (!isFinite(ts) || ts < weekAgo) item.classList.add('filter-hidden');
    });
    // Hide rows that have zero visible cards after filtering
    document.querySelectorAll('.row').forEach(r => {
      const vis = r.querySelectorAll('.slider-item:not(.filter-hidden)').length;
      if (vis === 0) r.classList.add('filter-hidden');
    });
    return;
  }

  if (mode === 'mylist') {
    const wl = new Set(stGet(ST_KEYS.WATCHLIST, []));
    document.querySelectorAll('.row').forEach(r => r.classList.add('filter-hidden'));
    if (wl.size === 0) {
      showToast('הרשימה שלי ריקה · לחצי + על כרטיס');
      return;
    }
    // Build virtual my-list row from cards
    const container = document.getElementById('rowsContainer');
    const uniqueById = new Map();
    document.querySelectorAll('.title-card-container[data-video-id]').forEach(c => {
      const id = c.dataset.videoId;
      if (wl.has(id) && !uniqueById.has(id)) uniqueById.set(id, c.closest('.slider-item').cloneNode(true));
    });
    if (uniqueById.size === 0) return;
    const rowHtml = `<section class="row my-list-row" id="myListRow">
      <div class="row-header"><h2 class="rowTitle">הרשימה שלי · ${uniqueById.size} פריטים</h2></div>
      <div class="row-container"><div class="rowContent"></div></div>
    </section>`;
    container.insertAdjacentHTML('afterbegin', rowHtml);
    const rc = document.querySelector('#myListRow .rowContent');
    uniqueById.forEach(node => rc.appendChild(node));
    return;
  }

  if (mode === 'search') {
    const q = prompt('חפשי וידאו לפי שם:', '');
    if (q === null || q.trim() === '') {
      applyNavFilter('home');
      document.querySelectorAll('.navigation-tab a').forEach(a => a.classList.toggle('current', a.dataset.nav === 'home'));
      return;
    }
    const qLower = q.toLowerCase();
    document.querySelectorAll('.slider-item').forEach(item => {
      const card = item.querySelector('.title-card-container');
      const title = decodeURIComponent(card?.dataset.videoTitle || '').toLowerCase();
      if (!title.includes(qLower)) item.classList.add('filter-hidden');
    });
    document.querySelectorAll('.row').forEach(r => {
      const vis = r.querySelectorAll('.slider-item:not(.filter-hidden)').length;
      if (vis === 0) r.classList.add('filter-hidden');
    });
    return;
  }
}

document.addEventListener('click', (e) => {
  const tab = e.target.closest('.navigation-tab a[data-nav]');
  if (!tab) return;
  e.preventDefault();
  document.querySelectorAll('.navigation-tab a').forEach(a => a.classList.remove('current'));
  tab.classList.add('current');
  applyNavFilter(tab.dataset.nav);
});"""

if JS_MARKER not in content:
    print("ERROR: JS marker not found", file=sys.stderr); sys.exit(1)
content = content.replace(JS_MARKER, JS_NEW)

TARGET.write_text(content, encoding='utf-8')
print(f"OK: commit 4 applied. Size: {len(content)} bytes")
