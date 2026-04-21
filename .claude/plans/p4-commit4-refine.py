#!/usr/bin/env python3
"""Commit 4 refinement:
  - Replace header progress pill with a compact ring around the 'S' avatar
  - Add per-row progress indicator (X/Y + mini bar) next to each row title
"""
import sys
from pathlib import Path

TARGET = Path("/Users/shahafwaitzman/Documents/CLOUD CODE/super-team-academy/academy-hub.html")
content = TARGET.read_text(encoding='utf-8')

# === 1. Remove old pill from nav, wrap profile icon with ring ===
OLD_NAV_PILL = """    <li id="overallProgressWrap" class="overall-progress-pill" style="display:none;" title="וידאוז שהותחלו">
      <span class="op-caption">התקדמות</span>
      <span class="op-label" id="opLabel">0/0</span>
      <div class="op-bar"><div class="op-fill" id="opFill" style="width:0%"></div></div>
    </li>
    <li><button class="nav-icon-btn" aria-label="חיפוש">"""

NEW_NAV_PILL = """    <li><button class="nav-icon-btn" aria-label="חיפוש">"""

if OLD_NAV_PILL not in content:
    print("ERROR: old pill not found", file=sys.stderr); sys.exit(1)
content = content.replace(OLD_NAV_PILL, NEW_NAV_PILL)

# === 2. Wrap profile icon with SVG ring ===
OLD_PROFILE = """    <li><div class="profile-icon" id="profileIcon">S</div></li>"""

NEW_PROFILE = """    <li class="profile-wrap" id="profileWrap" title="התקדמות">
      <svg class="profile-ring" viewBox="0 0 44 44" aria-hidden="true">
        <circle cx="22" cy="22" r="19" class="pr-bg"/>
        <circle cx="22" cy="22" r="19" class="pr-fill" id="profileRingFill"/>
      </svg>
      <div class="profile-icon" id="profileIcon">S</div>
    </li>"""

if OLD_PROFILE not in content:
    print("ERROR: profile icon not found", file=sys.stderr); sys.exit(1)
content = content.replace(OLD_PROFILE, NEW_PROFILE)

# === 3. Add CSS for profile ring + per-row progress ===
CSS_MARKER = """/* Filtering — hide rows/cards based on active filter */
.row.filter-hidden,
.slider-item.filter-hidden { display: none !important; }"""

CSS_NEW = CSS_MARKER + """

/* ═══════════════════════════════════════════
   COMMIT 4 REFINE · Profile ring + Per-row progress
   ═══════════════════════════════════════════ */

/* Profile avatar with progress ring */
.profile-wrap {
  position: relative;
  width: 44px; height: 44px;
  display: flex; align-items: center; justify-content: center;
  cursor: pointer;
}
.profile-ring {
  position: absolute; inset: 0;
  width: 44px; height: 44px;
  transform: rotate(-90deg);
  pointer-events: none;
}
.profile-ring circle {
  fill: none;
  stroke-width: 2.2;
}
.profile-ring .pr-bg {
  stroke: rgba(255,255,255,0.15);
}
.profile-ring .pr-fill {
  stroke: #E50914;
  stroke-linecap: round;
  stroke-dasharray: 119.38;  /* 2πr · r=19 */
  stroke-dashoffset: 119.38;
  transition: stroke-dashoffset 0.8s cubic-bezier(0.2, 0.8, 0.2, 1);
  filter: drop-shadow(0 0 6px rgba(229,9,20,0.55));
}
.profile-wrap .profile-icon {
  width: 32px; height: 32px;
}
.profile-wrap::after {
  content: attr(data-count);
  position: absolute;
  bottom: -4px; inset-inline-end: -4px;
  min-width: 18px; height: 18px;
  padding: 0 5px;
  border-radius: 10px;
  background: #E50914;
  color: #fff;
  font-size: 9px; font-weight: 900;
  letter-spacing: 0.3px;
  display: flex; align-items: center; justify-content: center;
  box-shadow: 0 2px 8px rgba(0,0,0,0.5);
  opacity: 0;
  transform: scale(0.7);
  transition: opacity 0.3s, transform 0.3s;
  pointer-events: none;
}
.profile-wrap[data-count]:not([data-count=""])::after {
  opacity: 1;
  transform: scale(1);
}

/* Per-row progress indicator next to row title */
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

if CSS_MARKER not in content:
    print("ERROR: CSS marker not found", file=sys.stderr); sys.exit(1)
content = content.replace(CSS_MARKER, CSS_NEW)

# === 4. Replace renderOverallProgress → renderProfileRing + add renderRowProgress ===
OLD_RENDER = """function renderOverallProgress() {
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
setInterval(renderOverallProgress, 30000);"""

NEW_RENDER = """function renderOverallProgress() {
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
}

function renderAllProgress() {
  renderOverallProgress();
  renderRowProgress();
}
setTimeout(renderAllProgress, 2800);
setInterval(renderAllProgress, 30000);"""

if OLD_RENDER not in content:
    print("ERROR: render block not found", file=sys.stderr); sys.exit(1)
content = content.replace(OLD_RENDER, NEW_RENDER)

# === 5. Also call renderRowProgress after watchlist toggle / seed + remove old pill CSS (cleanup) ===
# (Optional cleanup — leave old .overall-progress-pill CSS in place, it's unused now)

TARGET.write_text(content, encoding='utf-8')
print(f"OK: refine applied. Size: {len(content)} bytes")
