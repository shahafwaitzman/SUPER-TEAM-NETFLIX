#!/usr/bin/env python3
"""P2: FLOW stages redesign - Netflix episode-guide accordion style."""
import re
import sys
from pathlib import Path

TARGET = Path("/Users/shahafwaitzman/Documents/CLOUD CODE/flow-viewer/index.html")
content = TARGET.read_text(encoding='utf-8')

# 1) Add Bebas Neue font (next to existing Heebo)
OLD_FONT = '<link href="https://fonts.googleapis.com/css2?family=Heebo:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">'
NEW_FONT = '<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Heebo:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">'
if OLD_FONT not in content:
    print("ERROR: font link not found", file=sys.stderr); sys.exit(1)
content = content.replace(OLD_FONT, NEW_FONT)

# 2) Replace .stages-grid + .stage CSS (find block between ".stages-grid {" and end of .stage-* block)
# Find the block start at ".stages-grid {" and end at next major section after ".stage-number-sub" + stage-num color rules
old_stage_css_re = re.compile(
    r'\.stages-grid \{.*?\.stage\.supervisor \.stage-num \{ background: linear-gradient\(135deg, var\(--red\), var\(--red-dark\)\); \}',
    re.DOTALL
)
new_stage_css = '''.stages-grid {
  display: flex; flex-direction: column; gap: 10px;
}

/* Category filter chips */
.stage-filters {
  display: flex; gap: 8px; flex-wrap: wrap;
  margin-bottom: 18px;
  padding: 12px; border-radius: 12px;
  background: rgba(255,255,255,0.02);
  border: 1px solid var(--border);
  position: sticky; top: 78px; z-index: 40;
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
}
body[data-theme="light"] .stage-filters { background: rgba(255,255,255,0.7); }
.stage-filter-chip {
  padding: 8px 16px; border-radius: 20px;
  background: transparent; color: var(--text-dim);
  border: 1px solid var(--border);
  font-size: 13px; font-weight: 700; cursor: pointer;
  font-family: inherit;
  transition: all 0.2s;
  white-space: nowrap;
}
.stage-filter-chip:hover { background: rgba(255,255,255,0.06); color: var(--text); }
.stage-filter-chip.active {
  background: var(--red); color: #fff; border-color: var(--red);
  box-shadow: 0 4px 14px rgba(229,9,20,0.35);
}
.stage-filter-chip .count {
  opacity: 0.7; font-size: 11px; font-weight: 600;
  margin-inline-start: 4px;
}
.stage-filter-chip.active .count { opacity: 1; }

.stage-progress {
  margin: 0 0 20px; padding: 14px 18px;
  border-radius: 12px;
  background: linear-gradient(135deg, rgba(229,9,20,0.1), rgba(229,9,20,0.02));
  border: 1px solid rgba(229,9,20,0.2);
  display: flex; align-items: center; gap: 16px;
}
.stage-progress-bar {
  flex: 1; height: 8px; border-radius: 4px;
  background: rgba(255,255,255,0.08);
  overflow: hidden; position: relative;
}
.stage-progress-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--red), #ff6b6b);
  border-radius: 4px;
  transition: width 0.4s cubic-bezier(0.2, 0.8, 0.2, 1);
  box-shadow: 0 0 10px rgba(229,9,20,0.5);
}
.stage-progress-label {
  font-weight: 900; font-size: 14px;
  white-space: nowrap;
}
.stage-progress-label b { color: var(--red); font-size: 18px; font-family: 'Bebas Neue', Heebo, sans-serif; letter-spacing: 1px; }

/* Stage row card (accordion) */
.stage {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 12px;
  position: relative; overflow: hidden;
  transition: border-color 0.25s, box-shadow 0.25s, background 0.25s;
  cursor: default;
}
.stage:hover {
  border-color: rgba(229,9,20,0.35);
  box-shadow: 0 8px 24px rgba(0,0,0,0.35);
}
.stage.hidden { display: none; }

/* Left category rail */
.stage::before {
  content: ''; position: absolute; top: 0; bottom: 0;
  inset-inline-start: 0; width: 4px;
}
.stage.customer::before { background: linear-gradient(180deg, var(--blue), #3b82f6); }
.stage.distributor::before { background: linear-gradient(180deg, var(--green), #22c55e); }
.stage.supervisor::before { background: linear-gradient(180deg, var(--red), #ff6b6b); }

/* Collapsed header (always visible) */
.stage-head {
  display: grid;
  grid-template-columns: auto 1fr auto auto;
  align-items: center;
  gap: 16px;
  padding: 16px 22px 16px 26px;
  cursor: pointer;
  user-select: none;
}
.stage-head:hover { background: rgba(255,255,255,0.03); }
body[data-theme="light"] .stage-head:hover { background: rgba(0,0,0,0.03); }

.stage-num {
  display: flex; flex-direction: column;
  align-items: center; justify-content: center;
  min-width: 64px; padding: 4px 10px;
  border-radius: 10px;
  color: #fff;
  box-shadow: 0 4px 12px rgba(0,0,0,0.35);
}
.stage-num-big {
  font-family: 'Bebas Neue', 'Heebo', sans-serif;
  font-size: 30px; font-weight: 400;
  line-height: 1; letter-spacing: 2px;
}
.stage-num-icon { font-size: 16px; line-height: 1; margin-top: 2px; }
.stage.customer .stage-num { background: linear-gradient(135deg, var(--blue), #3b82f6); }
.stage.distributor .stage-num { background: linear-gradient(135deg, var(--green), #22c55e); }
.stage.supervisor .stage-num { background: linear-gradient(135deg, var(--red), var(--red-dark)); }

.stage-head-meta { min-width: 0; }
.stage-head-top {
  display: flex; align-items: center; gap: 10px;
  margin-bottom: 3px;
  flex-wrap: wrap;
}
.stage-tag {
  display: inline-block; padding: 2px 9px; border-radius: 4px;
  font-size: 10px; font-weight: 800; text-transform: uppercase;
  letter-spacing: 1.2px;
}
.stage.customer .stage-tag { background: rgba(84,185,197,0.15); color: var(--blue); }
.stage.distributor .stage-tag { background: rgba(70,211,105,0.15); color: var(--green); }
.stage.supervisor .stage-tag { background: rgba(229,9,20,0.15); color: var(--red); }
.stage h3 {
  font-size: 16px; font-weight: 800; line-height: 1.3; color: var(--white);
  overflow: hidden; text-overflow: ellipsis;
}
.stage-one-liner {
  font-size: 12.5px; color: var(--text-dim);
  line-height: 1.4; font-weight: 400;
  overflow: hidden; text-overflow: ellipsis;
  white-space: nowrap;
}

.start-here-badge {
  position: absolute; top: 12px; inset-inline-end: 80px; z-index: 3;
  padding: 3px 10px; border-radius: 16px;
  background: linear-gradient(135deg, var(--gold), #d9a900);
  color: #000; font-size: 10px; font-weight: 900;
  letter-spacing: 0.5px;
  box-shadow: 0 3px 10px rgba(245,197,24,0.4);
}

.stage-check {
  flex-shrink: 0;
  width: 32px; height: 32px;
  border-radius: 50%;
  border: 2px solid var(--border);
  background: transparent;
  display: flex; align-items: center; justify-content: center;
  cursor: pointer;
  transition: all 0.2s;
  font-size: 14px;
  color: var(--text-muted);
}
.stage-check:hover { border-color: var(--green); color: var(--green); }
.stage-check.done {
  background: var(--green); border-color: var(--green);
  color: #000; font-weight: 900;
}

.fav-btn {
  position: static;
  width: 28px; height: 28px;
  background: transparent; border: none;
  cursor: pointer; font-size: 17px;
  color: var(--text-muted);
  transition: color 0.2s, transform 0.2s;
}
.fav-btn:hover { color: var(--gold); transform: scale(1.15); }
.fav-btn.active { color: var(--gold); }

.stage-expand {
  flex-shrink: 0;
  width: 32px; height: 32px;
  display: flex; align-items: center; justify-content: center;
  border-radius: 8px;
  color: var(--text-dim);
  transition: transform 0.3s, color 0.2s, background 0.2s;
}
.stage-head:hover .stage-expand { background: rgba(255,255,255,0.08); color: var(--red); }
.stage.open .stage-expand { transform: rotate(90deg); color: var(--red); }

/* Expanded body */
.stage-sections {
  max-height: 0;
  overflow: hidden;
  transition: max-height 0.4s cubic-bezier(0.2, 0.8, 0.2, 1);
  padding: 0 26px;
}
.stage.open .stage-sections {
  max-height: 3000px;
  padding: 4px 26px 22px;
}
.stage.open { box-shadow: 0 10px 30px rgba(0,0,0,0.45); border-color: rgba(229,9,20,0.4); }'''

content, n = old_stage_css_re.subn(new_stage_css, content)
if n != 1:
    print(f"ERROR: stage CSS replace count={n}", file=sys.stderr); sys.exit(1)

# 3) Replace HTML above stagesGrid — inject filters + progress + grid
OLD_SECTION_HEAD = '''    <div class="section-head">
      <div class="section-head-row">
        <h2>שלבי התהליך</h2>
        <span class="counter" id="stagesCounter">• 11 שלבים</span>
      </div>
      <div class="desc">לחיצה על שלב להרחבה · <b style="color:var(--gold)">⚡ מצב דגשים</b> מציג רק את הקישורים והדגשים החשובים</div>
    </div>
    <div class="stages-grid" id="stagesGrid"></div>'''

NEW_SECTION_HEAD = '''    <div class="section-head">
      <div class="section-head-row">
        <h2>שלבי התהליך</h2>
        <span class="counter" id="stagesCounter">• 11 שלבים</span>
      </div>
      <div class="desc">לחיצה על שלב להרחבה · סימון ✓ כשסיימת · <b style="color:var(--gold)">⚡ מצב דגשים</b> מציג רק את הקישורים והדגשים החשובים</div>
    </div>

    <div class="stage-filters" id="stageFilters" role="tablist" aria-label="סינון שלבים">
      <button class="stage-filter-chip active" data-filter="all" role="tab">כולם <span class="count">11</span></button>
      <button class="stage-filter-chip" data-filter="customer" role="tab">לקוח <span class="count">6</span></button>
      <button class="stage-filter-chip" data-filter="distributor" role="tab">מפיץ <span class="count">4</span></button>
      <button class="stage-filter-chip" data-filter="supervisor" role="tab">מפקח <span class="count">1</span></button>
    </div>

    <div class="stage-progress">
      <div class="stage-progress-label"><b id="stageProgressCount">0</b>/11 שלבים סומנו כהושלמו</div>
      <div class="stage-progress-bar"><div class="stage-progress-fill" id="stageProgressFill" style="width:0%"></div></div>
    </div>

    <div class="stages-grid" id="stagesGrid"></div>'''

if OLD_SECTION_HEAD not in content:
    print("ERROR: section head block not found", file=sys.stderr); sys.exit(1)
content = content.replace(OLD_SECTION_HEAD, NEW_SECTION_HEAD)

# 4) Rewrite renderStages() function to new accordion structure
OLD_RENDER = '''function renderStages() {
  const grid = document.getElementById('stagesGrid');
  grid.innerHTML = STAGES.map(s => `
    <div class="stage ${s.cat}" data-stage="${s.n}">
      ${s.n === 1 ? '<div class="start-here-badge">✨ התחילי כאן</div>' : ''}
      <button class="fav-btn ${favorites.has(s.n) ? 'active' : ''}" onclick="toggleFav(${s.n}, event)" title="סמן כמועדף">${favorites.has(s.n) ? '⭐' : '☆'}</button>
      <div class="stage-top">
        <div class="stage-num">
          <span class="stage-icon">${STAGE_ICONS[s.n] || s.n}</span>
          <span class="stage-number-sub">${s.n}</span>
        </div>
        <div class="stage-head-info">
          <div class="stage-tag">${s.catLabel}</div>
          <h3>${s.title}</h3>
        </div>
      </div>
      <div class="stage-sections">
        ${s.detail ? `<div class="stage-section detail-section"><div class="stage-section-label">▸ מה עושים</div><div class="stage-section-content">${s.detail}</div></div>` : ''}
        ${s.why ? `<div class="stage-section why-section"><div class="stage-section-label">▸ איך/למה</div><div class="stage-section-content">${s.why}</div></div>` : ''}
        ${s.goal ? `<div class="stage-section goal-section"><div class="stage-section-label keep">▸ מטרה</div><div class="stage-goal">${s.goal}</div></div>` : ''}
        ${s.emphasis ? `<div class="stage-section emphasis-section"><div class="stage-section-label keep">▸ דגש</div><div class="stage-emphasis">${s.emphasis}</div></div>` : ''}
        ${s.links && s.links.length ? `<div class="stage-section links-section"><div class="stage-section-label keep">▸ קישורים</div>${s.links.map(l => renderLink(l)).join('')}</div>` : ''}
      </div>
    </div>
  `).join('');
}'''

NEW_RENDER = '''const DONE_KEY = 'flow-stages-done';
let stagesDone = new Set(JSON.parse(localStorage.getItem(DONE_KEY) || '[]'));

function _oneLiner(s) {
  const src = s.goal || s.detail || s.why || '';
  return src.split('\\n')[0].substring(0, 110);
}

function renderStages() {
  const grid = document.getElementById('stagesGrid');
  grid.innerHTML = STAGES.map(s => `
    <div class="stage ${s.cat}" data-stage="${s.n}" data-cat="${s.cat}">
      ${s.n === 1 ? '<div class="start-here-badge">✨ התחילי כאן</div>' : ''}
      <div class="stage-head" onclick="toggleStage(${s.n}, event)">
        <div class="stage-num">
          <span class="stage-num-big">${String(s.n).padStart(2,'0')}</span>
          <span class="stage-num-icon">${STAGE_ICONS[s.n] || ''}</span>
        </div>
        <div class="stage-head-meta">
          <div class="stage-head-top">
            <span class="stage-tag">${s.catLabel}</span>
            <h3>${s.title}</h3>
          </div>
          <div class="stage-one-liner">${_oneLiner(s)}</div>
        </div>
        <button class="fav-btn ${favorites.has(s.n) ? 'active' : ''}" onclick="toggleFav(${s.n}, event)" title="סמן כמועדף" aria-label="מועדף">${favorites.has(s.n) ? '⭐' : '☆'}</button>
        <button class="stage-check ${stagesDone.has(s.n) ? 'done' : ''}" onclick="toggleStageDone(${s.n}, event)" title="סימון כהושלם" aria-label="השלמתי">${stagesDone.has(s.n) ? '✓' : ''}</button>
        <div class="stage-expand" aria-hidden="true">
          <svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor"><path d="M8.5 5.5L15 12l-6.5 6.5L7 17l5-5-5-5z"/></svg>
        </div>
      </div>
      <div class="stage-sections">
        ${s.detail ? `<div class="stage-section detail-section"><div class="stage-section-label">▸ מה עושים</div><div class="stage-section-content">${s.detail}</div></div>` : ''}
        ${s.why ? `<div class="stage-section why-section"><div class="stage-section-label">▸ איך/למה</div><div class="stage-section-content">${s.why}</div></div>` : ''}
        ${s.goal ? `<div class="stage-section goal-section"><div class="stage-section-label keep">▸ מטרה</div><div class="stage-goal">${s.goal}</div></div>` : ''}
        ${s.emphasis ? `<div class="stage-section emphasis-section"><div class="stage-section-label keep">▸ דגש</div><div class="stage-emphasis">${s.emphasis}</div></div>` : ''}
        ${s.links && s.links.length ? `<div class="stage-section links-section"><div class="stage-section-label keep">▸ קישורים (${s.links.length})</div>${s.links.map(l => renderLink(l)).join('')}</div>` : ''}
      </div>
    </div>
  `).join('');
  updateStageProgress();
}

function toggleStage(n, event) {
  if (event && (event.target.closest('.fav-btn') || event.target.closest('.stage-check'))) return;
  const el = document.querySelector(`.stage[data-stage="${n}"]`);
  if (!el) return;
  el.classList.toggle('open');
}

function toggleStageDone(n, event) {
  event.stopPropagation();
  if (stagesDone.has(n)) stagesDone.delete(n); else stagesDone.add(n);
  localStorage.setItem(DONE_KEY, JSON.stringify([...stagesDone]));
  const btn = event.currentTarget;
  btn.classList.toggle('done');
  btn.textContent = stagesDone.has(n) ? '✓' : '';
  updateStageProgress();
}

function updateStageProgress() {
  const count = stagesDone.size;
  const total = STAGES.length;
  const pct = Math.round((count / total) * 100);
  const cEl = document.getElementById('stageProgressCount');
  const fEl = document.getElementById('stageProgressFill');
  if (cEl) cEl.textContent = count;
  if (fEl) fEl.style.width = pct + '%';
}

function filterStages(cat) {
  document.querySelectorAll('.stage-filter-chip').forEach(c => c.classList.toggle('active', c.dataset.filter === cat));
  document.querySelectorAll('.stage').forEach(s => {
    const show = cat === 'all' || s.dataset.cat === cat;
    s.classList.toggle('hidden', !show);
  });
}

document.addEventListener('click', (e) => {
  const chip = e.target.closest('.stage-filter-chip');
  if (chip) filterStages(chip.dataset.filter);
});'''

if OLD_RENDER not in content:
    print("ERROR: renderStages block not found", file=sys.stderr); sys.exit(1)
content = content.replace(OLD_RENDER, NEW_RENDER)

TARGET.write_text(content, encoding='utf-8')
print(f"OK: FLOW stages redesign applied. Final size: {len(content)} bytes")
