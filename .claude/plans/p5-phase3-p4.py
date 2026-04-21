#!/usr/bin/env python3
"""Phase 3 · P4: Admin analytics tab."""
import sys
from pathlib import Path

TARGET = Path("/Users/shahafwaitzman/Documents/CLOUD CODE/super-team-academy/admin.html")
content = TARGET.read_text(encoding='utf-8')

# === 1. Add CSS for analytics tab content ===
CSS_MARKER = "}\n</style>"

CSS_NEW = """
/* ═══════════════════════════════════════════
   PHASE 3 P4 · Analytics dashboard
   ═══════════════════════════════════════════ */
.analytics-view { display: none; }
.analytics-view.active { display: block; }
.ana-kpi-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 14px;
  margin-bottom: 28px;
}
.ana-kpi {
  padding: 18px 16px;
  background: linear-gradient(135deg, rgba(229,9,20,0.1), rgba(20,20,20,0.4));
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 10px;
  text-align: center;
}
.ana-kpi-num {
  font-size: 34px; font-weight: 900;
  color: var(--white);
  line-height: 1;
  margin-bottom: 6px;
}
.ana-kpi-label {
  font-size: 11px; font-weight: 700;
  color: var(--text-dim);
  text-transform: uppercase;
  letter-spacing: 1.5px;
}
.ana-kpi.red .ana-kpi-num { color: var(--red); }
.ana-kpi.green .ana-kpi-num { color: var(--green); }
.ana-kpi.gold .ana-kpi-num { color: var(--gold); }
.ana-kpi-sub { font-size: 10px; color: var(--text-dim); margin-top: 4px; }

.ana-section {
  background: var(--card);
  border: 1px solid rgba(255,255,255,0.06);
  border-radius: 10px;
  padding: 20px;
  margin-bottom: 20px;
}
.ana-section-title {
  font-size: 11px; font-weight: 800;
  color: var(--text-dim);
  text-transform: uppercase;
  letter-spacing: 1.8px;
  margin-bottom: 14px;
}

/* Bar chart — weekly activity */
.ana-chart {
  display: flex; align-items: flex-end;
  gap: 8px;
  height: 140px;
  padding: 12px 8px 8px;
}
.ana-bar {
  flex: 1;
  display: flex; flex-direction: column;
  align-items: center; gap: 6px;
  position: relative;
}
.ana-bar-fill {
  width: 100%;
  background: linear-gradient(180deg, var(--red), rgba(229,9,20,0.5));
  border-radius: 4px 4px 0 0;
  box-shadow: 0 0 10px rgba(229,9,20,0.35);
  min-height: 3px;
  transition: height 0.6s cubic-bezier(0.2,0.8,0.2,1);
  position: relative;
}
.ana-bar-val {
  position: absolute;
  top: -20px; left: 50%;
  transform: translateX(-50%);
  font-size: 10px; font-weight: 900;
  color: var(--white);
}
.ana-bar-label {
  font-size: 10px; color: var(--text-dim);
  font-weight: 700;
}

/* Top users list */
.ana-top-list { list-style: none; padding: 0; margin: 0; }
.ana-top-item {
  display: grid;
  grid-template-columns: 36px 1fr auto;
  align-items: center;
  padding: 12px 4px;
  gap: 14px;
  border-bottom: 1px solid rgba(255,255,255,0.05);
}
.ana-top-item:last-child { border-bottom: none; }
.ana-top-rank {
  font-size: 16px; font-weight: 900;
  color: var(--text-dim);
  text-align: center;
}
.ana-top-item:nth-child(1) .ana-top-rank { color: var(--gold); }
.ana-top-item:nth-child(2) .ana-top-rank { color: #c8c8d2; }
.ana-top-item:nth-child(3) .ana-top-rank { color: #cd7f32; }
.ana-top-name { font-size: 13px; font-weight: 700; color: var(--white); }
.ana-top-meta { font-size: 11px; color: var(--text-dim); margin-top: 2px; }
.ana-top-score {
  font-size: 14px; font-weight: 900;
  color: var(--red);
}

.ana-muted-note {
  padding: 14px;
  background: rgba(255,255,255,0.03);
  border: 1px dashed rgba(255,255,255,0.1);
  border-radius: 8px;
  font-size: 12px;
  color: var(--text-dim);
  text-align: center;
  line-height: 1.5;
}

.ana-cat-list { display: flex; flex-direction: column; gap: 10px; }
.ana-cat-item {
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 10px;
  padding: 10px 12px;
  background: rgba(255,255,255,0.03);
  border-radius: 8px;
  align-items: center;
}
.ana-cat-name { font-size: 12.5px; font-weight: 700; color: var(--white); }
.ana-cat-bar {
  grid-column: 1 / -1;
  height: 6px;
  background: rgba(255,255,255,0.1);
  border-radius: 3px;
  overflow: hidden;
  margin-top: 6px;
}
.ana-cat-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--red), #ff6b6b);
  border-radius: 3px;
  transition: width 0.6s;
}
.ana-cat-count { font-size: 12px; font-weight: 800; color: var(--red); }

@media (max-width: 768px) {
  .ana-kpi-grid { grid-template-columns: repeat(2, 1fr); }
}
}
</style>"""

content = content.replace(CSS_MARKER, CSS_NEW)

# === 2. Add "אנליטיקה" tab button ===
OLD_TABS = """    <button class="admin-tab" onclick="setTab('progress')" id="tabProgress">התקדמות</button>
  </div>"""
NEW_TABS = """    <button class="admin-tab" onclick="setTab('progress')" id="tabProgress">התקדמות</button>
    <button class="admin-tab" onclick="setTab('analytics')" id="tabAnalytics">אנליטיקה</button>
  </div>"""
content = content.replace(OLD_TABS, NEW_TABS)

# === 3. Add analytics view container after the progress view ===
OLD_PROGRESS_CLOSE = """  <div class="admin-progress" id="progressView" style="display:none">
    <h2>התקדמות משתמשים</h2>
    <table class="progress-table" id="progressTable">
      <thead><tr><th>שם</th><th>טלפון</th><th>התקדמות</th><th>סרטונים שנצפו</th></tr></thead>
      <tbody id="progressBody"></tbody>
    </table>
  </div>
</div>"""

NEW_PROGRESS_CLOSE = """  <div class="admin-progress" id="progressView" style="display:none">
    <h2>התקדמות משתמשים</h2>
    <table class="progress-table" id="progressTable">
      <thead><tr><th>שם</th><th>טלפון</th><th>התקדמות</th><th>סרטונים שנצפו</th></tr></thead>
      <tbody id="progressBody"></tbody>
    </table>
  </div>

  <div class="analytics-view" id="analyticsView">
    <div class="ana-kpi-grid">
      <div class="ana-kpi"><div class="ana-kpi-num" id="anaKpiUsers">0</div><div class="ana-kpi-label">משתמשים</div><div class="ana-kpi-sub" id="anaKpiUsersSub">מתוך סה"כ</div></div>
      <div class="ana-kpi red"><div class="ana-kpi-num" id="anaKpiPending">0</div><div class="ana-kpi-label">ממתינים לאישור</div><div class="ana-kpi-sub">דורשים טיפול</div></div>
      <div class="ana-kpi green"><div class="ana-kpi-num" id="anaKpiApproved">0</div><div class="ana-kpi-label">מאושרים</div><div class="ana-kpi-sub">פעילים במערכת</div></div>
      <div class="ana-kpi gold"><div class="ana-kpi-num" id="anaKpiNewWeek">0</div><div class="ana-kpi-label">חדשים השבוע</div><div class="ana-kpi-sub">7 ימים אחרונים</div></div>
    </div>

    <div class="ana-section">
      <div class="ana-section-title">פעילות משתמשים — 7 ימים אחרונים</div>
      <div class="ana-chart" id="anaWeekChart"></div>
    </div>

    <div class="ana-section">
      <div class="ana-section-title">Top 10 · משתמשים פעילים ביותר</div>
      <ul class="ana-top-list" id="anaTopUsers"></ul>
    </div>

    <div class="ana-section">
      <div class="ana-section-title">פילוח קטגוריות (לפי התקדמות משתמשים)</div>
      <div class="ana-cat-list" id="anaCategories"></div>
    </div>

    <div class="ana-section">
      <div class="ana-section-title">המשובים שלך (מה-academy)</div>
      <div id="anaSurveys"><div class="ana-muted-note">טוען משובים מהדפדפן הנוכחי...</div></div>
    </div>
  </div>
</div>"""

content = content.replace(OLD_PROGRESS_CLOSE, NEW_PROGRESS_CLOSE)

# === 4. Wire the setTab('analytics') case + rendering function ===
# Find setTab function and extend it
OLD_SET_TAB_MARKER = "function setTab("
# Use regex-safe approach — just inject new function after existing setTab
# Append new functions at end of <script> block
OLD_SCRIPT_END = "</script>\n</body>"

NEW_ADMIN_SCRIPT = """
/* ═══════════════════════════════════════════
   PHASE 3 P4 · Admin analytics
   ═══════════════════════════════════════════ */
(function setupAnalyticsTab() {
  // Intercept setTab to handle 'analytics'
  const origSetTab = window.setTab;
  window.setTab = function(tab) {
    currentTab = tab;
    document.querySelectorAll('.admin-tab').forEach(t => t.classList.remove('active'));
    const btn = document.getElementById('tab' + tab.charAt(0).toUpperCase() + tab.slice(1));
    if (btn) btn.classList.add('active');

    const listView = document.getElementById('userList');
    const progressView = document.getElementById('progressView');
    const analyticsView = document.getElementById('analyticsView');
    const selectAll = document.getElementById('selectAllWrapper');
    const bulkActions = document.getElementById('bulkActions');

    if (tab === 'analytics') {
      if (listView) listView.style.display = 'none';
      if (progressView) progressView.style.display = 'none';
      if (analyticsView) { analyticsView.classList.add('active'); analyticsView.style.display = 'block'; }
      if (selectAll) selectAll.style.display = 'none';
      if (bulkActions) bulkActions.style.display = 'none';
      renderAnalytics();
      return;
    }
    if (analyticsView) { analyticsView.classList.remove('active'); analyticsView.style.display = 'none'; }
    if (typeof origSetTab === 'function') origSetTab(tab);
  };
})();

function renderAnalytics() {
  const users = Object.values(usersData || {});
  const total = users.length;
  const pending = users.filter(u => u.status === 'pending' || !u.status).length;
  const approved = users.filter(u => u.status === 'approved').length;

  const weekAgo = Date.now() - 7 * 24 * 3600 * 1000;
  const newWeek = users.filter(u => {
    const ts = u.createdAt || u.created_at || u.registeredAt || u.approvedAt || 0;
    const n = typeof ts === 'number' ? ts : new Date(ts).getTime();
    return isFinite(n) && n >= weekAgo;
  }).length;

  const setNum = (id, n) => { const el = document.getElementById(id); if (el) el.textContent = n; };
  setNum('anaKpiUsers', total);
  setNum('anaKpiPending', pending);
  setNum('anaKpiApproved', approved);
  setNum('anaKpiNewWeek', newWeek);
  const sub = document.getElementById('anaKpiUsersSub');
  if (sub) sub.textContent = `${approved} מאושרים`;

  // Weekly chart — approvals per day (last 7 days)
  const chart = document.getElementById('anaWeekChart');
  if (chart) {
    const days = [];
    for (let i = 6; i >= 0; i--) {
      const d = new Date(); d.setHours(0,0,0,0); d.setDate(d.getDate() - i);
      const start = d.getTime();
      const end = start + 24 * 3600 * 1000;
      const count = users.filter(u => {
        const ts = u.createdAt || u.created_at || u.registeredAt || u.approvedAt || 0;
        const n = typeof ts === 'number' ? ts : new Date(ts).getTime();
        return isFinite(n) && n >= start && n < end;
      }).length;
      const labels = ['א','ב','ג','ד','ה','ו','ש'];
      days.push({ count, label: labels[d.getDay()], isToday: i === 0 });
    }
    const max = Math.max(1, ...days.map(d => d.count));
    chart.innerHTML = days.map(d => `
      <div class="ana-bar">
        <div class="ana-bar-fill" style="height: ${(d.count / max) * 100}%">
          ${d.count > 0 ? `<span class="ana-bar-val">${d.count}</span>` : ''}
        </div>
        <span class="ana-bar-label">${d.label}${d.isToday ? ' •' : ''}</span>
      </div>
    `).join('');
  }

  // Top 10 — users with most progress (using .progress field if present)
  const withProgress = users.map(u => {
    const p = u.progress || {};
    const watched = Object.values(p).filter(v => v > 0).length;
    return { u, watched, name: u.name || u.fullName || u.email || 'ללא שם', phone: u.phone || '' };
  }).sort((a, b) => b.watched - a.watched).slice(0, 10);
  const topList = document.getElementById('anaTopUsers');
  if (topList) {
    if (withProgress.length === 0) {
      topList.innerHTML = '<li class="ana-muted-note">אין עדיין נתוני צפייה</li>';
    } else {
      topList.innerHTML = withProgress.map((it, i) => `
        <li class="ana-top-item">
          <div class="ana-top-rank">#${i+1}</div>
          <div>
            <div class="ana-top-name">${escapeHTMLAdmin(it.name)}</div>
            <div class="ana-top-meta">${escapeHTMLAdmin(it.phone)}</div>
          </div>
          <div class="ana-top-score">${it.watched}</div>
        </li>
      `).join('');
    }
  }

  // Categories — aggregate category watches across users
  const catCount = {};
  users.forEach(u => {
    const p = u.progress || {};
    Object.keys(p).forEach(vid => {
      const c = (u.categories && u.categories[vid]) || 'כללי';
      catCount[c] = (catCount[c] || 0) + 1;
    });
  });
  const catList = document.getElementById('anaCategories');
  if (catList) {
    const entries = Object.entries(catCount).sort((a,b) => b[1] - a[1]).slice(0, 8);
    if (entries.length === 0) {
      catList.innerHTML = '<div class="ana-muted-note">אין מספיק נתונים לפילוח קטגוריות</div>';
    } else {
      const max = Math.max(...entries.map(([,n]) => n));
      catList.innerHTML = entries.map(([cat, n]) => `
        <div class="ana-cat-item">
          <span class="ana-cat-name">${escapeHTMLAdmin(cat)}</span>
          <span class="ana-cat-count">${n}</span>
          <div class="ana-cat-bar"><div class="ana-cat-fill" style="width: ${(n/max)*100}%"></div></div>
        </div>
      `).join('');
    }
  }

  // Your own surveys (from this browser's localStorage for academy-hub)
  const surveys = collectLocalSurveys();
  const surveyHost = document.getElementById('anaSurveys');
  if (surveyHost) {
    if (surveys.length === 0) {
      surveyHost.innerHTML = '<div class="ana-muted-note">אין משובים שמורים בדפדפן זה. כל משוב נשמר בדפדפן של כל משתמש — לאחסון מרכזי דרוש backend (TODO).</div>';
    } else {
      surveyHost.innerHTML = surveys.map(s => `
        <div class="ana-cat-item" style="grid-template-columns: 1fr">
          <div>
            <div class="ana-top-name">${escapeHTMLAdmin(s.title || 'וידאו')}</div>
            <div class="ana-top-meta">${new Date(s.ts).toLocaleString('he-IL')}</div>
            ${s.takeaway ? `<div style="margin-top:8px;font-size:12px;color:var(--white)"><b style="color:var(--red)">לקחתי:</b> ${escapeHTMLAdmin(s.takeaway)}</div>` : ''}
            ${s.unclear ? `<div style="margin-top:4px;font-size:12px;color:var(--text-dim)"><b style="color:var(--gold)">לא ברור:</b> ${escapeHTMLAdmin(s.unclear)}</div>` : ''}
            ${s.questions ? `<div style="margin-top:4px;font-size:12px;color:var(--text-dim)"><b style="color:var(--green)">שאלות:</b> ${escapeHTMLAdmin(s.questions)}</div>` : ''}
          </div>
        </div>
      `).join('');
    }
  }
}

function escapeHTMLAdmin(s) {
  return String(s || '').replace(/[<>&"']/g, c => ({'<':'&lt;','>':'&gt;','&':'&amp;','"':'&quot;',"'":'&#39;'}[c]));
}

function collectLocalSurveys() {
  const results = [];
  try {
    for (let i = 0; i < localStorage.length; i++) {
      const k = localStorage.key(i);
      if (!k || !k.startsWith('sta_') || !k.endsWith('_surveys')) continue;
      const raw = localStorage.getItem(k);
      if (!raw) continue;
      const obj = JSON.parse(raw);
      Object.entries(obj || {}).forEach(([videoId, data]) => {
        results.push({ videoId, ...data });
      });
    }
  } catch (e) {}
  return results.sort((a,b) => (b.ts || 0) - (a.ts || 0)).slice(0, 20);
}
</script>
</body>"""

content = content.replace(OLD_SCRIPT_END, NEW_ADMIN_SCRIPT)

TARGET.write_text(content, encoding='utf-8')
print(f"OK: Phase 3 P4 applied. Size: {len(content)} bytes")
