#!/usr/bin/env python3
"""Phase 3 · P2: "סיימתי" button + video-based streak + clearer stats."""
import sys, re
from pathlib import Path

TARGET = Path("/Users/shahafwaitzman/Documents/CLOUD CODE/super-team-academy/academy-hub.html")
content = TARGET.read_text(encoding='utf-8')

# === 1. Add "סיימתי" button inside video modal head ===
OLD_MODAL = """<div class="video-modal" id="videoModal" aria-hidden="true">
  <div class="video-modal-backdrop" onclick="closeVideo()"></div>
  <div class="video-modal-content">
    <button class="video-close" onclick="closeVideo()" aria-label="סגור">✕</button>
    <div class="video-modal-title" id="videoModalTitle"></div>"""

NEW_MODAL = """<div class="video-modal" id="videoModal" aria-hidden="true">
  <div class="video-modal-backdrop" onclick="closeVideo()"></div>
  <div class="video-modal-content">
    <button class="video-close" onclick="closeVideo()" aria-label="סגור">✕</button>
    <button class="video-complete-btn" id="videoCompleteBtn" data-video-id="">סיימתי ✓</button>
    <div class="video-modal-title" id="videoModalTitle"></div>"""

if OLD_MODAL not in content:
    print("ERROR: video modal not found", file=sys.stderr); sys.exit(1)
content = content.replace(OLD_MODAL, NEW_MODAL)

# === 2. CSS for completed button + streak display + per-video checkmark on cards ===
CSS_MARKER = """/* Filtering — hide rows/cards based on active filter */"""
CSS_NEW = """/* ═══════════════════════════════════════════
   PHASE 3 P2 · Completed button + streak
   ═══════════════════════════════════════════ */
.video-complete-btn {
  position: absolute;
  top: 16px; inset-inline-end: 68px;
  z-index: 10;
  padding: 10px 20px;
  border-radius: 26px;
  background: linear-gradient(135deg, #46d369, #22c55e);
  color: #0a1f11;
  border: none;
  font-family: inherit;
  font-size: 13px; font-weight: 900;
  letter-spacing: 0.3px;
  cursor: pointer;
  box-shadow: 0 4px 16px rgba(70,211,105,0.4);
  transition: transform 0.2s, box-shadow 0.2s;
}
.video-complete-btn:hover {
  transform: scale(1.04);
  box-shadow: 0 6px 20px rgba(70,211,105,0.55);
}
.video-complete-btn.done {
  background: linear-gradient(135deg, #46d369, #22c55e);
  color: #fff;
  pointer-events: none;
}
.video-complete-btn.done::before { content: '✓  '; }

/* Completed checkmark overlay on cards (100% progress) */
.card-completed-mark {
  position: absolute;
  top: 10px; inset-inline-end: 44px;
  z-index: 6;
  width: 26px; height: 26px;
  border-radius: 50%;
  background: #46d369;
  color: #0a1f11;
  display: flex; align-items: center; justify-content: center;
  font-size: 13px; font-weight: 900;
  box-shadow: 0 3px 10px rgba(70,211,105,0.4);
  pointer-events: none;
}

/* Clearer streak section in profile panel */
.pp-streak-rich {
  padding: 14px 16px;
  border-radius: 12px;
  background: linear-gradient(135deg, rgba(229,9,20,0.15), rgba(245,130,32,0.08));
  border: 1px solid rgba(229,9,20,0.3);
}
.pp-streak-head {
  display: flex; align-items: center; gap: 12px;
  margin-bottom: 10px;
}
.pp-streak-emoji { font-size: 26px; }
.pp-streak-num {
  font-size: 26px; font-weight: 900; color: #fff;
  line-height: 1;
}
.pp-streak-label { font-size: 11px; color: rgba(255,255,255,0.65); margin-top: 3px; }
.pp-week-dots {
  display: flex; gap: 5px;
  margin-top: 10px;
}
.pp-week-dot {
  flex: 1;
  height: 22px;
  border-radius: 4px;
  background: rgba(255,255,255,0.06);
  border: 1px solid rgba(255,255,255,0.08);
  display: flex; align-items: center; justify-content: center;
  font-size: 9px; font-weight: 800;
  color: rgba(255,255,255,0.5);
}
.pp-week-dot.active {
  background: var(--nflx-red, #E50914);
  border-color: var(--nflx-red, #E50914);
  color: #fff;
  box-shadow: 0 0 8px rgba(229,9,20,0.45);
}
.pp-week-dot.today {
  outline: 2px solid rgba(255,255,255,0.45);
  outline-offset: 1px;
}

/* Filtering — hide rows/cards based on active filter */"""

content = content.replace(CSS_MARKER, CSS_NEW)

# === 3. Replace old updateStreak / renderStreakPill with video-based logic ===
# Remove old streak block + replace render in profile with richer version
old_streak_js_re = re.compile(
    r'/\* ═══════════════════════════════════════════\s+COMMIT 5 · Streak system.*?updateStreak\(\);',
    re.DOTALL
)

new_streak_js = """/* ═══════════════════════════════════════════
   PHASE 3 P2 · Video-based streak (increments only on completion)
   ═══════════════════════════════════════════ */
function todayStr() {
  const d = new Date();
  return d.getFullYear() + '-' + String(d.getMonth()+1).padStart(2,'0') + '-' + String(d.getDate()).padStart(2,'0');
}
function dateStrOffset(daysBack) {
  const d = new Date(); d.setDate(d.getDate() - daysBack);
  return d.getFullYear() + '-' + String(d.getMonth()+1).padStart(2,'0') + '-' + String(d.getDate()).padStart(2,'0');
}
function ensureStreakShape() {
  const s = stGet(ST_KEYS.STREAK, {});
  if (!s || typeof s !== 'object') return { count: 0, lastActivity: null, activeDays: [] };
  if (!Array.isArray(s.activeDays)) s.activeDays = [];
  if (typeof s.count !== 'number') s.count = 0;
  return s;
}
function recordVideoActivity() {
  // Called when user completes a video — counts that day as an active day
  const s = ensureStreakShape();
  const today = todayStr();
  const yest = dateStrOffset(1);
  if (!s.activeDays.includes(today)) s.activeDays.push(today);
  // recompute consecutive streak ending today, walking back
  let cnt = 0;
  let cursor = today;
  while (s.activeDays.includes(cursor)) {
    cnt++;
    // go back one day from cursor
    const d = new Date(cursor); d.setDate(d.getDate() - 1);
    cursor = d.getFullYear() + '-' + String(d.getMonth()+1).padStart(2,'0') + '-' + String(d.getDate()).padStart(2,'0');
  }
  s.count = cnt;
  s.lastActivity = today;
  stSet(ST_KEYS.STREAK, s);
  return s;
}
function currentStreak() {
  // Displays the count but only if lastActivity was today or yesterday
  const s = ensureStreakShape();
  if (!s.lastActivity) return 0;
  const today = todayStr();
  const yest = dateStrOffset(1);
  if (s.lastActivity === today || s.lastActivity === yest) return s.count || 0;
  return 0;  // broken streak
}
"""

content = old_streak_js_re.sub(new_streak_js, content)

# === 4. Rewrite renderProfilePanel streak section to rich version with week dots ===
OLD_PP_STREAK_HTML = """    <section class="pp-section">
      <div class="pp-section-title">רצף</div>
      <div class="pp-streak">
        <span class="pp-streak-emoji">🔥</span>
        <div>
          <div class="pp-streak-num" id="ppStreakNum">0</div>
          <div class="pp-streak-label">ימים ברצף</div>
        </div>
      </div>
    </section>"""

NEW_PP_STREAK_HTML = """    <section class="pp-section">
      <div class="pp-section-title">רצף צפייה</div>
      <div class="pp-streak-rich">
        <div class="pp-streak-head">
          <span class="pp-streak-emoji">🔥</span>
          <div>
            <div class="pp-streak-num" id="ppStreakNum">0</div>
            <div class="pp-streak-label">ימים רצופים של צפייה</div>
          </div>
        </div>
        <div class="pp-week-dots" id="ppWeekDots"></div>
      </div>
    </section>"""

if OLD_PP_STREAK_HTML in content:
    content = content.replace(OLD_PP_STREAK_HTML, NEW_PP_STREAK_HTML)

# === 5. Replace "Streak" JS inside renderProfilePanel ===
OLD_PP_STREAK_JS = """  // Streak
  const streak = stGet(ST_KEYS.STREAK, { count: 0 });
  document.getElementById('ppStreakNum').textContent = streak.count || 0;"""

NEW_PP_STREAK_JS = """  // Streak — video-based + 7-day dots
  const streakNow = currentStreak();
  document.getElementById('ppStreakNum').textContent = streakNow;
  const s = ensureStreakShape();
  const activeSet = new Set(s.activeDays || []);
  const dayLabels = ['א','ב','ג','ד','ה','ו','ש'];
  const dotsHtml = [6,5,4,3,2,1,0].map(offset => {
    const ds = dateStrOffset(offset);
    const d = new Date(); d.setDate(d.getDate() - offset);
    const letter = dayLabels[d.getDay()];
    const active = activeSet.has(ds);
    const isToday = offset === 0;
    return `<div class="pp-week-dot ${active ? 'active' : ''} ${isToday ? 'today' : ''}">${letter}</div>`;
  }).join('');
  document.getElementById('ppWeekDots').innerHTML = dotsHtml;"""

if OLD_PP_STREAK_JS in content:
    content = content.replace(OLD_PP_STREAK_JS, NEW_PP_STREAK_JS)

# === 6. Update stats in profile (completed should use 100 threshold) — already does (>=90) ===
# Keep as is.

# === 7. Hook video modal open/close for "סיימתי" button + auto-fill videoId ===
# Append handler at end of script
JS_END_MARKER = "setTimeout(rebuildHeroFromLatest, 2200);"
JS_END_NEW = """setTimeout(rebuildHeroFromLatest, 2200);

/* ═══════════════════════════════════════════
   PHASE 3 P2 · "סיימתי" button wiring
   ═══════════════════════════════════════════ */
let __currentVideoId = null;

// Hook card clicks to remember which video is playing
document.addEventListener('click', (e) => {
  const container = e.target.closest('.title-card-container[data-video-id]');
  if (!container) return;
  const id = container.dataset.videoId;
  __currentVideoId = id;
  // Wait a tick for modal to open, then sync the complete button
  setTimeout(() => {
    const btn = document.getElementById('videoCompleteBtn');
    if (!btn) return;
    const progress = stGet(ST_KEYS.PROGRESS, {});
    const isDone = (progress[id] || 0) >= 100;
    btn.dataset.videoId = id;
    btn.classList.toggle('done', isDone);
    btn.textContent = isDone ? 'הושלם ✓' : 'סיימתי ✓';
  }, 200);
}, true);

// Complete button → sets progress to 100 + records streak
document.addEventListener('click', (e) => {
  const btn = e.target.closest('#videoCompleteBtn');
  if (!btn) return;
  e.stopPropagation();
  const id = btn.dataset.videoId || __currentVideoId;
  if (!id) return;
  const progress = stGet(ST_KEYS.PROGRESS, {});
  progress[id] = 100;
  stSet(ST_KEYS.PROGRESS, progress);
  recordVideoActivity();
  btn.classList.add('done');
  btn.textContent = 'הושלם ✓';
  showToast('וידאו הושלם · רצף: ' + currentStreak() + ' ימים');
  // Also refresh visuals
  renderAllProgress();
  // Inject completed checkmark on all copies of this card
  document.querySelectorAll(`.title-card-container[data-video-id="${id}"]`).forEach(c => {
    if (!c.querySelector('.card-completed-mark')) {
      const mark = document.createElement('div');
      mark.className = 'card-completed-mark';
      mark.innerHTML = '✓';
      c.appendChild(mark);
    }
  });
});

// Render existing completion marks on load
function renderCompletionMarks() {
  const progress = stGet(ST_KEYS.PROGRESS, {});
  document.querySelectorAll('.title-card-container[data-video-id]').forEach(c => {
    const id = c.dataset.videoId;
    const done = (progress[id] || 0) >= 100;
    const existing = c.querySelector('.card-completed-mark');
    if (done && !existing) {
      const mark = document.createElement('div');
      mark.className = 'card-completed-mark';
      mark.innerHTML = '✓';
      c.appendChild(mark);
    } else if (!done && existing) {
      existing.remove();
    }
  });
}
setTimeout(renderCompletionMarks, 2400);
setInterval(renderCompletionMarks, 30000);"""

content = content.replace(JS_END_MARKER, JS_END_NEW)

TARGET.write_text(content, encoding='utf-8')
print(f"OK: Phase 3 P2 applied. Size: {len(content)} bytes")
