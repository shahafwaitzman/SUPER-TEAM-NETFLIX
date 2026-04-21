#!/usr/bin/env python3
"""P1 flow-viewer home redesign - step 1: replace hero HTML block."""
import sys
from pathlib import Path

TARGET = Path("/Users/shahafwaitzman/Documents/CLOUD CODE/flow-viewer/index.html")

OLD = '''    <div class="hero-content">
      <div class="hero-badge">⚡ מרכז הידע הארגוני</div>
      <h1>המסע שלך<br>מלקוח עד AWT</h1>
      <p class="hero-sub">11 שלבים מוגדרים היטב. כל הטפסים, הקישורים והכלים שתצטרכי — במקום אחד. מלווה אותך בדרך מהשלב הראשון עד להצלחה עסקית.</p>
      <div class="hero-stats">
        <div class="hero-stat"><div class="num" id="statStages">11</div><div class="label">שלבי תהליך</div></div>
        <div class="hero-stat"><div class="num" id="statFiles">26</div><div class="label">קבצים</div></div>
        <div class="hero-stat"><div class="num" id="statLinks">8</div><div class="label">קישורים</div></div>
        <div class="hero-stat"><div class="num">∞</div><div class="label">חוזרים לזה תמיד</div></div>
      </div>
    </div>'''

NEW = '''    <div class="hero-content home-hero-content">
      <div class="hero-badge">⚡ FLOW ארגוני · מרכז הפעולה</div>
      <h1>בחרי את<br>היעד שלך</h1>
      <p class="hero-sub">5 מרכזי פעולה · כל הכלים, הקבצים והשלבים במקום אחד. לחצי על כרטיס כדי להתחיל.</p>

      <div class="home-cards" role="list" aria-label="מרכזי פעולה">

        <button type="button" class="home-card home-card-flow" data-card="flow" role="listitem" aria-label="FLOW לסגירת מפקח">
          <div class="home-card-bg" aria-hidden="true"></div>
          <div class="home-card-pattern" aria-hidden="true"></div>
          <div class="home-card-overlay" aria-hidden="true"></div>
          <div class="home-card-inner">
            <div class="home-card-top">
              <span class="home-card-kicker">11 שלבים · מסע מלא</span>
              <span class="home-card-icon" aria-hidden="true">🎯</span>
            </div>
            <div class="home-card-body">
              <h3 class="home-card-title">FLOW לסגירת מפקח</h3>
              <p class="home-card-sub">וקידום ל-AWT ומעלה · כל שלב, כל טופס, כל דגש קריטי</p>
            </div>
            <div class="home-card-cta"><span class="home-card-cta-arrow" aria-hidden="true">←</span><span>התחילי את המסע</span></div>
          </div>
        </button>

        <button type="button" class="home-card home-card-meet" data-card="meetings" role="listitem" aria-label="FLOW פגישה 1 ו-2">
          <div class="home-card-bg" aria-hidden="true"></div>
          <div class="home-card-pattern" aria-hidden="true"></div>
          <div class="home-card-overlay" aria-hidden="true"></div>
          <div class="home-card-inner">
            <div class="home-card-top">
              <span class="home-card-kicker">פגישות עם לקוח</span>
              <span class="home-card-icon" aria-hidden="true">💬</span>
            </div>
            <div class="home-card-body">
              <h3 class="home-card-title">FLOW פגישה</h3>
              <p class="home-card-sub">1 ו-2 עם לקוח · סקריפט מלא ומשימות</p>
            </div>
            <div class="home-card-cta"><span class="home-card-cta-arrow" aria-hidden="true">←</span><span>פתחי פגישה</span></div>
          </div>
        </button>

        <button type="button" class="home-card home-card-map" data-card="diagram" role="listitem" aria-label="תרשים כללי">
          <div class="home-card-bg" aria-hidden="true"></div>
          <div class="home-card-pattern" aria-hidden="true"></div>
          <div class="home-card-overlay" aria-hidden="true"></div>
          <div class="home-card-inner">
            <div class="home-card-top">
              <span class="home-card-kicker">מפת דרכים</span>
              <span class="home-card-icon" aria-hidden="true">📊</span>
            </div>
            <div class="home-card-body">
              <h3 class="home-card-title">תרשים כללי</h3>
              <p class="home-card-sub">מבט-על על המסע · לקוח → מפיץ → מפקח</p>
            </div>
            <div class="home-card-cta"><span class="home-card-cta-arrow" aria-hidden="true">←</span><span>תראי את המפה</span></div>
          </div>
        </button>

        <button type="button" class="home-card home-card-lib" data-card="library" role="listitem" aria-label="ספריית קבצים">
          <div class="home-card-bg" aria-hidden="true"></div>
          <div class="home-card-pattern" aria-hidden="true"></div>
          <div class="home-card-overlay" aria-hidden="true"></div>
          <div class="home-card-inner">
            <div class="home-card-top">
              <span class="home-card-kicker">כלים וטפסים</span>
              <span class="home-card-icon" aria-hidden="true">📚</span>
            </div>
            <div class="home-card-body">
              <h3 class="home-card-title">ספריית קבצים</h3>
              <p class="home-card-sub">כל המסמכים, המצגות והקישורים</p>
            </div>
            <div class="home-card-cta"><span class="home-card-cta-arrow" aria-hidden="true">←</span><span>פתחי ספרייה</span></div>
          </div>
        </button>

        <button type="button" class="home-card home-card-profits" data-card="profits" role="listitem" aria-label="POWER MONDAY">
          <div class="home-card-bg" aria-hidden="true"></div>
          <div class="home-card-pattern" aria-hidden="true"></div>
          <div class="home-card-overlay" aria-hidden="true"></div>
          <div class="home-card-inner">
            <div class="home-card-top">
              <span class="home-card-kicker">רווחים</span>
              <span class="home-card-icon" aria-hidden="true">💰</span>
            </div>
            <div class="home-card-body">
              <h3 class="home-card-title">POWER MONDAY</h3>
              <p class="home-card-sub">מעקב רווחים וקריטריוני הצלחה</p>
            </div>
            <div class="home-card-cta"><span class="home-card-cta-arrow" aria-hidden="true">←</span><span>נכנסתי</span></div>
          </div>
        </button>

      </div>
    </div>'''

content = TARGET.read_text(encoding='utf-8')
count = content.count(OLD)
if count != 1:
    print(f"ERROR: Expected exactly 1 match of OLD, found {count}", file=sys.stderr)
    sys.exit(1)
new_content = content.replace(OLD, NEW)
TARGET.write_text(new_content, encoding='utf-8')
print(f"OK: Replaced hero HTML block in {TARGET}")
print(f"New file size: {len(new_content)} bytes (was {len(content)})")
