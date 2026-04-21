#!/usr/bin/env python3
"""Commit 5 · Streak + Badges.
  - Streak logic: +1 if lastLogin=yesterday, reset to 1 if older, no change if today
  - Streak pill (🔥 + count) next to profile S icon
  - 7 auto-computed badges: first_video, week_streak, month_streak,
    module_HOM, module_zoomim, early_bird (5 views <9am), marathon (3 same day)
  - Toast on new badge earned
  - Badge storage in ST_KEYS.BADGES, ready for profile panel (commit 7)
"""
import sys
from pathlib import Path

TARGET = Path("/Users/shahafwaitzman/Documents/CLOUD CODE/super-team-academy/academy-hub.html")
content = TARGET.read_text(encoding='utf-8')

# === 1. CSS for streak pill ===
CSS_MARKER = """.row-progress.empty .row-progress-label b { color: rgba(255,255,255,0.4); }"""

CSS_NEW = CSS_MARKER + """

/* ═══════════════════════════════════════════
   COMMIT 5 · Streak pill (next to profile)
   ═══════════════════════════════════════════ */
.streak-pill {
  display: inline-flex; align-items: center; gap: 6px;
  padding: 6px 12px;
  border-radius: 20px;
  background: linear-gradient(135deg, rgba(229,9,20,0.18), rgba(245,130,32,0.12));
  border: 1px solid rgba(229,9,20,0.35);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  font-size: 13px; font-weight: 900;
  color: #fff;
  white-space: nowrap;
  cursor: default;
  transition: transform 0.2s;
}
.streak-pill:hover { transform: scale(1.04); }
.streak-pill-flame {
  font-size: 15px; line-height: 1;
  filter: drop-shadow(0 0 4px rgba(245,130,32,0.6));
}
.streak-pill-count { letter-spacing: 0.3px; }
.streak-pill[data-streak="0"] { display: none; }

/* Badge-earned toast variant */
.sta-toast.badge-toast {
  border-color: rgba(245,197,24,0.55);
  box-shadow: 0 10px 30px rgba(0,0,0,0.5), 0 0 28px rgba(245,197,24,0.3);
}"""

if CSS_MARKER not in content:
    print("ERROR: CSS marker not found", file=sys.stderr); sys.exit(1)
content = content.replace(CSS_MARKER, CSS_NEW)

# === 2. Add streak pill <li> before profile icon in secondary nav ===
OLD_NAV = """    <li><div class="profile-icon" id="profileIcon" title="התקדמות תצוף ליד כל תיקייה למטה">S</div></li>
  </ul>"""

NEW_NAV = """    <li><div class="streak-pill" id="streakPill" data-streak="0" title="ימים ברצף">
      <span class="streak-pill-flame" aria-hidden="true">🔥</span>
      <span class="streak-pill-count" id="streakCount">0</span>
    </div></li>
    <li><div class="profile-icon" id="profileIcon" title="התקדמות תצוף ליד כל תיקייה למטה">S</div></li>
  </ul>"""

if OLD_NAV not in content:
    print("ERROR: nav profile block not found", file=sys.stderr); sys.exit(1)
content = content.replace(OLD_NAV, NEW_NAV)

# === 3. Add category metadata to card (folder name) + JS logic ===
# Find renderRow — we need to inject data-category into card. Find the renderRow function.
# The folder name is available as `folderName` / `cleanTitle` in scope.
OLD_CARD_META = """        <div class="title-card-container" data-video-id="${f.id}" data-video-title="${encodeURIComponent(title)}" data-modified="${f.modifiedTime || ''}">"""

NEW_CARD_META = """        <div class="title-card-container" data-video-id="${f.id}" data-video-title="${encodeURIComponent(title)}" data-modified="${f.modifiedTime || ''}" data-category="${encodeURIComponent(cleanTitle || folderName || '')}">"""

if OLD_CARD_META not in content:
    print("ERROR: card meta marker not found", file=sys.stderr); sys.exit(1)
content = content.replace(OLD_CARD_META, NEW_CARD_META)

# === 4. Inject streak + badges JS at end of script ===
JS_MARKER = """document.addEventListener('click', (e) => {
  const tab = e.target.closest('.navigation-tab a[data-nav]');
  if (!tab) return;
  e.preventDefault();
  document.querySelectorAll('.navigation-tab a').forEach(a => a.classList.remove('current'));
  tab.classList.add('current');
  applyNavFilter(tab.dataset.nav);
});"""

JS_NEW = JS_MARKER + """

/* ═══════════════════════════════════════════
   COMMIT 5 · Streak system
   ═══════════════════════════════════════════ */
function todayStr() {
  const d = new Date();
  return d.getFullYear() + '-' + String(d.getMonth()+1).padStart(2,'0') + '-' + String(d.getDate()).padStart(2,'0');
}
function yesterdayStr() {
  const d = new Date(); d.setDate(d.getDate() - 1);
  return d.getFullYear() + '-' + String(d.getMonth()+1).padStart(2,'0') + '-' + String(d.getDate()).padStart(2,'0');
}
function updateStreak() {
  const streak = stGet(ST_KEYS.STREAK, { count: 0, lastLogin: null });
  const today = todayStr();
  const yest = yesterdayStr();
  if (streak.lastLogin === today) {
    // same-day revisit, no change
  } else if (streak.lastLogin === yest) {
    streak.count = (streak.count || 0) + 1;
    streak.lastLogin = today;
  } else {
    streak.count = 1;
    streak.lastLogin = today;
  }
  stSet(ST_KEYS.STREAK, streak);
  renderStreakPill();
  return streak;
}
function renderStreakPill() {
  const streak = stGet(ST_KEYS.STREAK, { count: 0 });
  const pill = document.getElementById('streakPill');
  const cnt = document.getElementById('streakCount');
  if (!pill || !cnt) return;
  pill.setAttribute('data-streak', String(streak.count || 0));
  cnt.textContent = streak.count || 0;
  pill.title = streak.count > 0 ? `${streak.count} ימים ברצף · המשיכי ככה!` : 'עוד אין רצף';
}
updateStreak();

/* ═══════════════════════════════════════════
   COMMIT 5 · Badges engine
   ═══════════════════════════════════════════ */
const BADGE_DEFS = {
  first_video:  { icon: '🎬', title: 'צפייה ראשונה',      desc: 'התחלת לצפות!' },
  week_streak:  { icon: '🔥', title: 'שבוע ברצף',         desc: '7 ימי חיבור רצופים' },
  month_streak: { icon: '⚡', title: 'חודש ברצף',         desc: '30 ימי חיבור רצופים' },
  module_HOM:   { icon: '💼', title: 'מודול HOM הושלם',   desc: 'השלמת את כל הזדמנויות עסקית' },
  module_zoomim:{ icon: '🎥', title: 'זומים הושלם',       desc: 'השלמת את כל הזומים' },
  early_bird:   { icon: '🌅', title: 'ציפור מוקדם',       desc: '5 צפיות לפני 9:00 בבוקר' },
  marathon:     { icon: '🏃', title: 'מרתון',             desc: '3 וידאוז רצופים באותו יום' },
};

function computeBadges() {
  const progress = stGet(ST_KEYS.PROGRESS, {});
  const streak = stGet(ST_KEYS.STREAK, { count: 0 });
  const lw = stGet(ST_KEYS.LAST_WATCHED, {});
  const existing = new Set(stGet(ST_KEYS.BADGES, []));
  const newly = [];

  // first_video: any progress > 0
  if (!existing.has('first_video') && Object.values(progress).some(p => p > 0)) newly.push('first_video');

  // streaks
  if (!existing.has('week_streak') && (streak.count || 0) >= 7) newly.push('week_streak');
  if (!existing.has('month_streak') && (streak.count || 0) >= 30) newly.push('month_streak');

  // marathon: 3 videos started in same calendar day
  if (!existing.has('marathon')) {
    const byDay = {};
    Object.values(lw).forEach(e => {
      if (!e || !e.ts) return;
      const d = new Date(e.ts);
      const key = d.getFullYear()+'-'+d.getMonth()+'-'+d.getDate();
      byDay[key] = (byDay[key] || 0) + 1;
    });
    if (Object.values(byDay).some(n => n >= 3)) newly.push('marathon');
  }

  // early_bird: 5 LAST_WATCHED entries with hour < 9
  if (!existing.has('early_bird')) {
    const earlyCount = Object.values(lw).filter(e => {
      if (!e || !e.ts) return false;
      return new Date(e.ts).getHours() < 9;
    }).length;
    if (earlyCount >= 5) newly.push('early_bird');
  }

  // module completion: if a category has all cards with progress >= 90
  if (!existing.has('module_HOM') || !existing.has('module_zoomim')) {
    const byCat = {};
    document.querySelectorAll('.title-card-container[data-video-id][data-category]').forEach(c => {
      const cat = decodeURIComponent(c.dataset.category || '').toLowerCase();
      if (!cat) return;
      if (!byCat[cat]) byCat[cat] = { total: 0, done: 0 };
      byCat[cat].total++;
      if ((progress[c.dataset.videoId] || 0) >= 90) byCat[cat].done++;
    });
    Object.entries(byCat).forEach(([cat, s]) => {
      if (s.total === 0 || s.done < s.total) return;
      if (cat.includes('hom') && !existing.has('module_HOM')) newly.push('module_HOM');
      if (cat.includes('זום') && !existing.has('module_zoomim')) newly.push('module_zoomim');
    });
  }

  if (newly.length === 0) return [];
  const updated = [...existing, ...newly];
  stSet(ST_KEYS.BADGES, updated);
  return newly;
}

function showBadgeToast(badgeId) {
  const b = BADGE_DEFS[badgeId];
  if (!b) return;
  let t = document.getElementById('staToast');
  if (!t) {
    t = document.createElement('div');
    t.id = 'staToast';
    t.className = 'sta-toast';
    document.body.appendChild(t);
  }
  t.classList.add('badge-toast');
  t.textContent = `${b.icon}  פתחת: ${b.title}`;
  t.classList.add('show');
  clearTimeout(t._hideTimer);
  t._hideTimer = setTimeout(() => {
    t.classList.remove('show');
    setTimeout(() => t.classList.remove('badge-toast'), 500);
  }, 3200);
}

function recomputeBadges() {
  const newly = computeBadges();
  newly.forEach((b, i) => setTimeout(() => showBadgeToast(b), i * 3600));
}
// Run once after rows + seed settle, then every 30s alongside progress renders
setTimeout(recomputeBadges, 3500);
setInterval(recomputeBadges, 30000);"""

if JS_MARKER not in content:
    print("ERROR: JS marker not found", file=sys.stderr); sys.exit(1)
content = content.replace(JS_MARKER, JS_NEW)

TARGET.write_text(content, encoding='utf-8')
print(f"OK: commit 5 applied. Size: {len(content)} bytes")
