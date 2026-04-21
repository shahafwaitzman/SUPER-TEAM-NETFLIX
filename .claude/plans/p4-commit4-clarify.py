#!/usr/bin/env python3
"""Clarify progress indicators:
  - Remove confusing profile ring + badge around S avatar
  - Make per-folder (per-row) progress pill bigger + clearer
  - Clear Hebrew text: "הותחלו X מתוך Y"
  - Keep overall progress logic but only via tooltip on profile (hidden visual)
"""
import sys
from pathlib import Path

TARGET = Path("/Users/shahafwaitzman/Documents/CLOUD CODE/super-team-academy/academy-hub.html")
content = TARGET.read_text(encoding='utf-8')

# === 1. Remove profile-wrap / ring — revert to plain profile icon ===
OLD_PROFILE = """    <li class="profile-wrap" id="profileWrap" title="התקדמות">
      <svg class="profile-ring" viewBox="0 0 44 44" aria-hidden="true">
        <circle cx="22" cy="22" r="19" class="pr-bg"/>
        <circle cx="22" cy="22" r="19" class="pr-fill" id="profileRingFill"/>
      </svg>
      <div class="profile-icon" id="profileIcon">S</div>
    </li>"""

NEW_PROFILE = """    <li><div class="profile-icon" id="profileIcon" title="התקדמות תצוף ליד כל תיקייה למטה">S</div></li>"""

if OLD_PROFILE not in content:
    print("ERROR: profile block not found", file=sys.stderr); sys.exit(1)
content = content.replace(OLD_PROFILE, NEW_PROFILE)

# === 2. Replace per-row progress styles with larger, clearer version ===
OLD_ROW_CSS = """/* Per-row progress indicator next to row title */
.row-progress {
  display: inline-flex; align-items: center; gap: 8px;
  margin-inline-start: 12px;
  padding: 4px 10px;
  border-radius: 12px;
  background: rgba(255,255,255,0.05);
  border: 1px solid rgba(255,255,255,0.08);
  font-size: 10px;
  vertical-align: middle;
}
.row-progress-count {
  color: rgba(255,255,255,0.85);
  font-weight: 800;
  letter-spacing: 0.3px;
  white-space: nowrap;
}
.row-progress-bar {
  width: 60px; height: 4px;
  background: rgba(255,255,255,0.15);
  border-radius: 2px;
  overflow: hidden;
  position: relative;
}
.row-progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #E50914, #ff6b6b);
  border-radius: 2px;
  box-shadow: 0 0 5px rgba(229,9,20,0.5);
  transition: width 0.6s cubic-bezier(0.2,0.8,0.2,1);
}
.row-progress.complete .row-progress-count { color: #46d369; }
.row-progress.complete .row-progress-fill { background: linear-gradient(90deg, #46d369, #22c55e); box-shadow: 0 0 5px rgba(70,211,105,0.5); }
.row-header { display: flex; align-items: center; flex-wrap: wrap; gap: 6px; }"""

NEW_ROW_CSS = """/* Per-folder (per-row) progress — large & clear */
.row-header {
  display: flex; align-items: center; flex-wrap: wrap;
  gap: 14px;
  padding-inline-end: 56px;  /* matches existing right padding of rows */
}
.row-progress {
  display: inline-flex; align-items: center; gap: 10px;
  padding: 7px 14px;
  border-radius: 20px;
  background: rgba(20,20,20,0.6);
  border: 1px solid rgba(229,9,20,0.25);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  font-size: 12px;
  white-space: nowrap;
}
.row-progress-label {
  font-size: 11px; font-weight: 700;
  color: rgba(255,255,255,0.92);
  letter-spacing: 0.3px;
}
.row-progress-label b {
  color: #E50914;
  font-size: 13px;
  font-weight: 900;
  margin-inline: 2px;
}
.row-progress-bar {
  width: 70px; height: 5px;
  background: rgba(255,255,255,0.15);
  border-radius: 3px;
  overflow: hidden;
}
.row-progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #E50914, #ff6b6b);
  border-radius: 3px;
  box-shadow: 0 0 6px rgba(229,9,20,0.55);
  transition: width 0.6s cubic-bezier(0.2,0.8,0.2,1);
}
.row-progress-pct {
  font-size: 11px; font-weight: 900;
  color: rgba(255,255,255,0.75);
  letter-spacing: 0.3px;
  min-width: 34px; text-align: end;
}
.row-progress.complete { border-color: rgba(70,211,105,0.55); background: rgba(10,40,18,0.6); }
.row-progress.complete .row-progress-label b { color: #46d369; }
.row-progress.complete .row-progress-fill { background: linear-gradient(90deg, #46d369, #22c55e); box-shadow: 0 0 6px rgba(70,211,105,0.55); }
.row-progress.complete .row-progress-pct { color: #46d369; }
.row-progress.empty { border-color: rgba(255,255,255,0.08); background: rgba(255,255,255,0.03); }
.row-progress.empty .row-progress-label b { color: rgba(255,255,255,0.4); }"""

if OLD_ROW_CSS not in content:
    print("ERROR: old row CSS not found", file=sys.stderr); sys.exit(1)
content = content.replace(OLD_ROW_CSS, NEW_ROW_CSS)

# === 3. Simplify renderOverallProgress (profile ring gone) + update renderRowProgress markup ===
OLD_RENDER = """function renderOverallProgress() {
  const wrap = document.getElementById('profileWrap');
  if (!wrap) return;
  const { started, total, pct } = computeOverallProgress();
  if (total === 0) { wrap.removeAttribute('data-count'); return; }
  const fill = document.getElementById('profileRingFill');
  if (fill) {
    const circ = 119.38;  // 2πr, r=19
    fill.style.strokeDashoffset = circ * (1 - pct / 100);
  }
  wrap.setAttribute('data-count', started > 0 ? String(started) : '');
  wrap.title = `${started} וידאוז הותחלו מתוך ${total} · ${pct}%`;
}

function renderRowProgress() {
  const progress = stGet(ST_KEYS.PROGRESS, {});
  document.querySelectorAll('.row').forEach(row => {
    if (row.id === 'continueWatchingRow' || row.id === 'myListRow') return;
    const header = row.querySelector('.row-header');
    if (!header) return;
    const cards = row.querySelectorAll('.title-card-container[data-video-id]');
    if (cards.length === 0) return;
    let started = 0;
    cards.forEach(c => { if ((progress[c.dataset.videoId] || 0) > 0) started++; });
    const pct = cards.length ? Math.round((started / cards.length) * 100) : 0;
    let pill = header.querySelector('.row-progress');
    if (!pill) {
      pill = document.createElement('span');
      pill.className = 'row-progress';
      pill.innerHTML = `
        <span class="row-progress-count"></span>
        <div class="row-progress-bar"><div class="row-progress-fill"></div></div>
      `;
      header.appendChild(pill);
    }
    pill.querySelector('.row-progress-count').textContent = `${started}/${cards.length}`;
    pill.querySelector('.row-progress-fill').style.width = pct + '%';
    pill.classList.toggle('complete', started === cards.length && cards.length > 0);
  });
}"""

NEW_RENDER = """function renderOverallProgress() {
  const icon = document.getElementById('profileIcon');
  if (!icon) return;
  const { started, total, pct } = computeOverallProgress();
  icon.title = total > 0
    ? `סה"כ: ${started} מתוך ${total} וידאוז הותחלו · ${pct}%`
    : 'התקדמות תצוף ליד כל תיקייה למטה';
}

function renderRowProgress() {
  const progress = stGet(ST_KEYS.PROGRESS, {});
  document.querySelectorAll('.row').forEach(row => {
    if (row.id === 'continueWatchingRow' || row.id === 'myListRow') return;
    const header = row.querySelector('.row-header');
    if (!header) return;
    const cards = row.querySelectorAll('.title-card-container[data-video-id]');
    if (cards.length === 0) return;
    let started = 0;
    cards.forEach(c => { if ((progress[c.dataset.videoId] || 0) > 0) started++; });
    const pct = cards.length ? Math.round((started / cards.length) * 100) : 0;
    let pill = header.querySelector('.row-progress');
    if (!pill) {
      pill = document.createElement('span');
      pill.className = 'row-progress';
      pill.innerHTML = `
        <span class="row-progress-label">הותחלו <b></b>מתוך <b></b></span>
        <div class="row-progress-bar"><div class="row-progress-fill"></div></div>
        <span class="row-progress-pct"></span>
      `;
      header.appendChild(pill);
    }
    const boldEls = pill.querySelectorAll('.row-progress-label b');
    boldEls[0].textContent = started;
    boldEls[1].textContent = cards.length;
    pill.querySelector('.row-progress-fill').style.width = pct + '%';
    pill.querySelector('.row-progress-pct').textContent = pct + '%';
    pill.classList.toggle('complete', started === cards.length && cards.length > 0);
    pill.classList.toggle('empty', started === 0);
  });
}"""

if OLD_RENDER not in content:
    print("ERROR: render block not found", file=sys.stderr); sys.exit(1)
content = content.replace(OLD_RENDER, NEW_RENDER)

TARGET.write_text(content, encoding='utf-8')
print(f"OK: clarity applied. Size: {len(content)} bytes")
