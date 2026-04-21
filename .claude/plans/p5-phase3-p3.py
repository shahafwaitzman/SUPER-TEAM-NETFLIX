#!/usr/bin/env python3
"""Phase 3 · P3: Post-video survey (4 open questions)."""
import sys
from pathlib import Path

TARGET = Path("/Users/shahafwaitzman/Documents/CLOUD CODE/super-team-academy/academy-hub.html")
content = TARGET.read_text(encoding='utf-8')

# === 1. Add ST_KEY for surveys (reuse stGet/stSet; just a new namespace) ===
OLD_KEYS = """  NOTIFICATIONS_SEEN:`${ST_NS}_notifsSeen`,        // [videoId, ...]
};"""
NEW_KEYS = """  NOTIFICATIONS_SEEN:`${ST_NS}_notifsSeen`,        // [videoId, ...]
  SURVEYS:          `${ST_NS}_surveys`,            // { [videoId]: { takeaway, clear, unclear, questions, ts } }
};"""
if OLD_KEYS in content:
    content = content.replace(OLD_KEYS, NEW_KEYS)

# === 2. Initialize SURVEYS in stInit block ===
OLD_INIT = "  if (stGet(ST_KEYS.NOTIFICATIONS_SEEN, null) === null) stSet(ST_KEYS.NOTIFICATIONS_SEEN, []);"
NEW_INIT = """  if (stGet(ST_KEYS.NOTIFICATIONS_SEEN, null) === null) stSet(ST_KEYS.NOTIFICATIONS_SEEN, []);
  if (stGet(ST_KEYS.SURVEYS, null) === null) stSet(ST_KEYS.SURVEYS, {});"""
content = content.replace(OLD_INIT, NEW_INIT)

# === 3. Survey modal HTML + CSS ===
# Add modal HTML after profile panel section
PROFILE_PANEL_END = """  <div class="pp-foot">
    <button class="pp-logout-btn" id="ppLogoutBtn">יציאה</button>
  </div>
</aside>"""

SURVEY_MODAL = """  <div class="pp-foot">
    <button class="pp-logout-btn" id="ppLogoutBtn">יציאה</button>
  </div>
</aside>

<!-- Post-video survey modal -->
<div class="survey-backdrop" id="surveyBackdrop"></div>
<div class="survey-modal" id="surveyModal" role="dialog" aria-hidden="true">
  <div class="survey-head">
    <div class="survey-tag">⚡ משוב מהיר</div>
    <h3 class="survey-title" id="surveyTitle">מה לקחת מהוידאו הזה?</h3>
    <p class="survey-sub">4 שאלות קצרות · 60 שניות · יעזור לנו להשתפר</p>
    <button class="survey-close" id="surveyCloseBtn" aria-label="דלג">דלג</button>
  </div>
  <div class="survey-body">
    <div class="survey-field">
      <label for="sqTakeaway">מה הכי חשוב שלקחתי איתי?</label>
      <textarea id="sqTakeaway" placeholder="נקודה אחת עיקרית..." rows="2"></textarea>
    </div>
    <div class="survey-field">
      <label for="sqClear">מה היה ברור?</label>
      <textarea id="sqClear" placeholder="חלקים שהבנתי היטב..." rows="2"></textarea>
    </div>
    <div class="survey-field">
      <label for="sqUnclear">מה לא היה ברור?</label>
      <textarea id="sqUnclear" placeholder="מה דורש עוד הסבר..." rows="2"></textarea>
    </div>
    <div class="survey-field">
      <label for="sqQuestions">איזה שאלות יש לי?</label>
      <textarea id="sqQuestions" placeholder="שאלות שעולות אחרי הצפייה..." rows="2"></textarea>
    </div>
  </div>
  <div class="survey-foot">
    <button class="survey-skip-btn" id="surveySkipBtn">אחר כך</button>
    <button class="survey-submit-btn" id="surveySubmitBtn">שלחי משוב ✓</button>
  </div>
</div>"""

if PROFILE_PANEL_END not in content:
    print("ERROR: profile panel end not found", file=sys.stderr); sys.exit(1)
content = content.replace(PROFILE_PANEL_END, SURVEY_MODAL)

# === 4. CSS ===
CSS_MARKER = """/* ═══════════════════════════════════════════
   PHASE 3 P2 · Completed button + streak
   ═══════════════════════════════════════════ */"""

CSS_NEW = """/* ═══════════════════════════════════════════
   PHASE 3 P3 · Post-video survey modal
   ═══════════════════════════════════════════ */
.survey-backdrop {
  position: fixed; inset: 0;
  background: rgba(0,0,0,0.72);
  backdrop-filter: blur(6px);
  -webkit-backdrop-filter: blur(6px);
  z-index: 500;
  opacity: 0; pointer-events: none;
  transition: opacity 0.3s;
}
.survey-backdrop.open { opacity: 1; pointer-events: auto; }

.survey-modal {
  position: fixed;
  top: 50%; left: 50%;
  transform: translate(-50%, -50%) scale(0.95);
  z-index: 501;
  width: 560px; max-width: 92vw;
  max-height: 90vh;
  background: linear-gradient(180deg, #1a1a1a 0%, #0d0d0d 100%);
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 14px;
  box-shadow: 0 30px 80px rgba(0,0,0,0.7);
  display: flex; flex-direction: column;
  opacity: 0; pointer-events: none;
  transition: opacity 0.3s, transform 0.3s cubic-bezier(0.2, 0.8, 0.2, 1);
}
.survey-modal.open {
  opacity: 1; pointer-events: auto;
  transform: translate(-50%, -50%) scale(1);
}

.survey-head {
  position: relative;
  padding: 24px 28px 18px;
  border-bottom: 1px solid rgba(255,255,255,0.06);
}
.survey-tag {
  display: inline-block;
  padding: 4px 11px;
  border-radius: 14px;
  background: rgba(229,9,20,0.15);
  border: 1px solid rgba(229,9,20,0.35);
  color: var(--nflx-red, #E50914);
  font-size: 10px; font-weight: 800;
  letter-spacing: 1.3px; text-transform: uppercase;
  margin-bottom: 10px;
}
.survey-title {
  font-size: 19px; font-weight: 900;
  color: #fff; margin: 0 0 4px;
  line-height: 1.25;
}
.survey-sub {
  font-size: 12.5px;
  color: rgba(255,255,255,0.55);
  margin: 0;
  line-height: 1.4;
}
.survey-close {
  position: absolute;
  top: 18px; inset-inline-end: 18px;
  padding: 6px 12px;
  background: rgba(255,255,255,0.05);
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 14px;
  color: rgba(255,255,255,0.7);
  font-size: 11px; font-weight: 700;
  cursor: pointer; font-family: inherit;
}
.survey-close:hover { color: #fff; background: rgba(255,255,255,0.1); }

.survey-body {
  padding: 20px 28px;
  overflow-y: auto;
  flex: 1;
}
.survey-field {
  margin-bottom: 16px;
}
.survey-field label {
  display: block;
  font-size: 12.5px; font-weight: 700;
  color: rgba(255,255,255,0.85);
  margin-bottom: 6px;
}
.survey-field textarea {
  width: 100%;
  min-height: 54px;
  padding: 10px 12px;
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 8px;
  color: #fff;
  font-family: inherit;
  font-size: 13px;
  line-height: 1.5;
  resize: vertical;
  transition: border-color 0.2s, background 0.2s;
  box-sizing: border-box;
}
.survey-field textarea:focus {
  outline: none;
  border-color: rgba(229,9,20,0.55);
  background: rgba(255,255,255,0.06);
}
.survey-field textarea::placeholder {
  color: rgba(255,255,255,0.35);
}

.survey-foot {
  display: flex; gap: 10px;
  padding: 16px 28px 22px;
  border-top: 1px solid rgba(255,255,255,0.06);
}
.survey-skip-btn, .survey-submit-btn {
  flex: 1;
  padding: 11px 18px;
  border-radius: 24px;
  font-family: inherit;
  font-size: 13px; font-weight: 700;
  cursor: pointer;
  transition: all 0.2s;
  border: 1px solid transparent;
}
.survey-skip-btn {
  background: transparent;
  border-color: rgba(255,255,255,0.15);
  color: rgba(255,255,255,0.75);
}
.survey-skip-btn:hover {
  border-color: rgba(255,255,255,0.35);
  color: #fff;
}
.survey-submit-btn {
  background: linear-gradient(135deg, var(--nflx-red, #E50914), #ff2d2d);
  color: #fff;
  border-color: var(--nflx-red, #E50914);
  box-shadow: 0 6px 18px rgba(229,9,20,0.4);
}
.survey-submit-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 8px 22px rgba(229,9,20,0.5);
}

@media (max-width: 768px) {
  .survey-modal { width: 94vw; max-height: 85vh; }
  .survey-head, .survey-body, .survey-foot { padding-inline: 18px; }
}

/* ═══════════════════════════════════════════
   PHASE 3 P2 · Completed button + streak
   ═══════════════════════════════════════════ */"""

if CSS_MARKER not in content:
    print("ERROR: CSS marker not found", file=sys.stderr); sys.exit(1)
content = content.replace(CSS_MARKER, CSS_NEW)

# === 5. JS: open survey on video modal close, save response ===
JS_MARKER = "setTimeout(renderCompletionMarks, 2400);"
JS_NEW = """setTimeout(renderCompletionMarks, 2400);

/* ═══════════════════════════════════════════
   PHASE 3 P3 · Post-video survey
   ═══════════════════════════════════════════ */
let __lastWatchedVideoForSurvey = null;

function openSurvey(videoId, videoTitle) {
  if (!videoId) return;
  const surveys = stGet(ST_KEYS.SURVEYS, {});
  if (surveys[videoId]) return;  // already submitted — skip
  __lastWatchedVideoForSurvey = { id: videoId, title: videoTitle };
  const modal = document.getElementById('surveyModal');
  const back = document.getElementById('surveyBackdrop');
  if (!modal || !back) return;
  document.getElementById('surveyTitle').textContent = 'מה לקחת מהוידאו: ' + (videoTitle || '?');
  ['sqTakeaway','sqClear','sqUnclear','sqQuestions'].forEach(id => {
    const t = document.getElementById(id);
    if (t) t.value = '';
  });
  modal.classList.add('open');
  modal.setAttribute('aria-hidden','false');
  back.classList.add('open');
}
function closeSurvey() {
  const modal = document.getElementById('surveyModal');
  const back = document.getElementById('surveyBackdrop');
  if (modal) { modal.classList.remove('open'); modal.setAttribute('aria-hidden','true'); }
  if (back) back.classList.remove('open');
  __lastWatchedVideoForSurvey = null;
}
function submitSurvey() {
  if (!__lastWatchedVideoForSurvey) { closeSurvey(); return; }
  const data = {
    takeaway: (document.getElementById('sqTakeaway').value || '').trim(),
    clear:    (document.getElementById('sqClear').value || '').trim(),
    unclear:  (document.getElementById('sqUnclear').value || '').trim(),
    questions:(document.getElementById('sqQuestions').value || '').trim(),
    ts: Date.now(),
    title: __lastWatchedVideoForSurvey.title,
  };
  // Require at least one answer, otherwise treat as skip
  const anyFilled = data.takeaway || data.clear || data.unclear || data.questions;
  if (!anyFilled) { closeSurvey(); return; }
  const all = stGet(ST_KEYS.SURVEYS, {});
  all[__lastWatchedVideoForSurvey.id] = data;
  stSet(ST_KEYS.SURVEYS, all);
  showToast('✓ תודה על המשוב');
  closeSurvey();
}

// Handle survey buttons
document.addEventListener('click', (e) => {
  if (e.target.closest('#surveyCloseBtn') || e.target.closest('#surveySkipBtn') || e.target.closest('#surveyBackdrop')) {
    closeSurvey(); return;
  }
  if (e.target.closest('#surveySubmitBtn')) {
    submitSurvey(); return;
  }
});
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') {
    const m = document.getElementById('surveyModal');
    if (m && m.classList.contains('open')) closeSurvey();
  }
});

// Hook into video-modal close: show survey 500ms later
(function hookVideoModalClose() {
  // Replace native closeVideo: wrap it to trigger survey
  if (typeof window.closeVideo === 'function' && !window.__closeVideoWrapped) {
    const orig = window.closeVideo;
    window.closeVideo = function() {
      const id = __currentVideoId;
      const cont = id ? document.querySelector(`.title-card-container[data-video-id="${id}"]`) : null;
      const title = cont ? decodeURIComponent(cont.dataset.videoTitle || '') : '';
      orig.apply(this, arguments);
      if (id) setTimeout(() => openSurvey(id, title), 600);
    };
    window.__closeVideoWrapped = true;
  } else {
    // Retry shortly if closeVideo isn't defined yet
    setTimeout(hookVideoModalClose, 500);
  }
})();"""

content = content.replace(JS_MARKER, JS_NEW)

TARGET.write_text(content, encoding='utf-8')
print(f"OK: Phase 3 P3 applied. Size: {len(content)} bytes")
