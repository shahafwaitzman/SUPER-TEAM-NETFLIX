#!/usr/bin/env python3
"""Phase 3 · P1: Cleanup + Latest-video hero + NEW badge.
  - Remove: clubs leaderboard row, badges engine, streak pill
  - Add: createdTime to Drive fetch fields
  - Dynamic hero: shows newest video (title, category, thumbnail as bg)
  - NEW badge on cards < 30 days old
"""
import re, sys
from pathlib import Path

TARGET = Path("/Users/shahafwaitzman/Documents/CLOUD CODE/super-team-academy/academy-hub.html")
content = TARGET.read_text(encoding='utf-8')

# === 1. Add createdTime to Drive fields ===
OLD_FIELDS = "const fields = 'files(id,name,mimeType,thumbnailLink,videoMediaMetadata,size,modifiedTime)';"
NEW_FIELDS = "const fields = 'files(id,name,mimeType,thumbnailLink,videoMediaMetadata,size,modifiedTime,createdTime)';"
content = content.replace(OLD_FIELDS, NEW_FIELDS)

# === 2. Inject data-created + NEW badge into card template ===
OLD_CARD_META = '<div class="title-card-container" data-video-id="${f.id}" data-video-title="${encodeURIComponent(title)}" data-modified="${f.modifiedTime || \'\'}" data-category="${encodeURIComponent(cleanTitle || folderName || \'\')}">'
NEW_CARD_META = '<div class="title-card-container" data-video-id="${f.id}" data-video-title="${encodeURIComponent(title)}" data-modified="${f.modifiedTime || \'\'}" data-created="${f.createdTime || \'\'}" data-category="${encodeURIComponent(cleanTitle || folderName || \'\')}">'
if OLD_CARD_META not in content:
    print("ERROR: card meta not found", file=sys.stderr); sys.exit(1)
content = content.replace(OLD_CARD_META, NEW_CARD_META)

# Inject NEW badge element (30-day window) into card HTML — check via JS class
# We'll add a "new-badge" div and toggle visible via JS after render
OLD_CARD_START = """        <div class="title-card-container" data-video-id="${f.id}" data-video-title="${encodeURIComponent(title)}" data-modified="${f.modifiedTime || ''}" data-created="${f.createdTime || ''}" data-category="${encodeURIComponent(cleanTitle || folderName || '')}">
          <button type="button" class="watchlist-btn"""
NEW_CARD_START = """        <div class="title-card-container" data-video-id="${f.id}" data-video-title="${encodeURIComponent(title)}" data-modified="${f.modifiedTime || ''}" data-created="${f.createdTime || ''}" data-category="${encodeURIComponent(cleanTitle || folderName || '')}">
          ${(() => {
            const created = f.createdTime ? new Date(f.createdTime).getTime() : 0;
            const daysOld = created ? (Date.now() - created) / (24*3600*1000) : 999;
            return daysOld < 30 ? '<div class="new-badge" aria-label="חדש"><span>חדש</span></div>' : '';
          })()}
          <button type="button" class="watchlist-btn"""
if OLD_CARD_START not in content:
    print("ERROR: card start marker not found", file=sys.stderr); sys.exit(1)
content = content.replace(OLD_CARD_START, NEW_CARD_START)

# === 3. Remove badges system === (keep ST_KEYS.BADGES in schema for backward compat)
# Remove BADGE_DEFS + computeBadges + showBadgeToast + recomputeBadges + intervals
badge_block_re = re.compile(
    r'/\* ═══════════════════════════════════════════\s+COMMIT 5 · Badges engine.*?setInterval\(recomputeBadges, 30000\);',
    re.DOTALL
)
content = badge_block_re.sub('/* Badges engine removed in Phase 3 P1 */', content)

# Remove badge-toast CSS rule
badge_css_re = re.compile(r'/\* Badge-earned toast variant \*/\s*\.sta-toast\.badge-toast \{[^}]+\}', re.DOTALL)
content = badge_css_re.sub('', content)

# Remove pp-badges HTML + its JS rendering
pp_badges_html_re = re.compile(
    r'<section class="pp-section">\s*<div class="pp-section-title">מדליות</div>\s*<div class="pp-badges" id="ppBadges"></div>\s*</section>',
    re.DOTALL
)
content = pp_badges_html_re.sub('', content)

# Remove badges render in renderProfilePanel
pp_badges_js_re = re.compile(
    r'\s*// Badges\s*const earned = new Set\(stGet\(ST_KEYS\.BADGES, \[\]\)\);\s*const badgesHtml = Object\.entries\(BADGE_DEFS\)\.map.*?document\.getElementById\(\'ppBadges\'\)\.innerHTML = badgesHtml;',
    re.DOTALL
)
content = pp_badges_js_re.sub('', content)

# === 4. Remove streak pill from header ===
OLD_STREAK = """    <li><div class="streak-pill" id="streakPill" data-streak="0" title="ימים ברצף">
      <span class="streak-pill-flame" aria-hidden="true">🔥</span>
      <span class="streak-pill-count" id="streakCount">0</span>
    </div></li>
    <li><div class="profile-icon" """
NEW_STREAK = """    <li><div class="profile-icon" """
if OLD_STREAK in content:
    content = content.replace(OLD_STREAK, NEW_STREAK)

# === 5. Remove leaderboard row code + js (keep json file for deletion by git rm) ===
lb_block_re = re.compile(
    r'/\* ═══════════════════════════════════════════\s+COMMIT 8 · Leaderboard \(Phase 2C mock\).*?setTimeout\(buildLeaderboardRow, 2000\);',
    re.DOTALL
)
content = lb_block_re.sub('/* Leaderboard removed in Phase 3 P1 */', content)

# Remove leaderboard CSS block
lb_css_re = re.compile(
    r'/\* ═══════════════════════════════════════════\s+COMMIT 8 · Leaderboard row[\s\S]*?\.lb-trend\.same \{[^}]+\}',
    re.DOTALL
)
content = lb_css_re.sub('', content)

# === 6. Add NEW badge CSS + Latest-video hero CSS ===
CSS_MARKER = "/* Filtering — hide rows/cards based on active filter */"
NEW_CSS = """/* ═══════════════════════════════════════════
   PHASE 3 P1 · NEW badge + Dynamic Hero
   ═══════════════════════════════════════════ */
.new-badge {
  position: absolute;
  top: 10px; inset-inline-start: 10px;
  z-index: 7;
  padding: 3px 8px;
  border-radius: 4px;
  background: var(--nflx-red, #E50914);
  color: #fff;
  font-size: 10px; font-weight: 900;
  letter-spacing: 1.5px;
  text-transform: uppercase;
  box-shadow: 0 3px 10px rgba(229,9,20,0.55);
  pointer-events: none;
}
.new-badge span { font-weight: 900; }

/* Hero override when dynamic content injects latest video */
.hero-image.latest-video-bg {
  background-image: var(--latest-video-bg, var(--stadium-img));
  background-size: cover;
  background-position: center;
}
.latest-tag {
  display: inline-flex; align-items: center; gap: 6px;
  padding: 5px 12px;
  border-radius: 20px;
  background: var(--nflx-red, #E50914);
  color: #fff;
  font-size: 11px; font-weight: 900;
  letter-spacing: 1.4px; text-transform: uppercase;
  box-shadow: 0 4px 14px rgba(229,9,20,0.5);
  margin-bottom: 14px;
  align-self: flex-start;
}
.latest-tag::before { content: '⚡'; }
.billboard-title.latest-video-title {
  font-size: clamp(28px, 4.2vw, 56px) !important;
  text-transform: none;
  letter-spacing: -0.01em;
  line-height: 1.1;
}
.latest-meta {
  display: inline-flex; align-items: center; gap: 10px;
  font-size: 13px; font-weight: 700;
  color: rgba(255,255,255,0.88);
  margin-bottom: 14px;
}
.latest-meta-dot { opacity: 0.5; }

/* Filtering — hide rows/cards based on active filter */"""

content = content.replace(CSS_MARKER, NEW_CSS)

# === 7. Add dynamic hero rebuild JS ===
JS_MARKER = "setTimeout(renderNotifications, 3000);"
JS_NEW = """/* ═══════════════════════════════════════════
   PHASE 3 P1 · Dynamic hero (latest uploaded video)
   ═══════════════════════════════════════════ */
function findLatestVideo() {
  const cards = Array.from(document.querySelectorAll('.title-card-container[data-video-id][data-created]'));
  let best = null; let bestTs = 0;
  cards.forEach(c => {
    const ts = c.dataset.created ? new Date(c.dataset.created).getTime() : 0;
    if (ts > bestTs) { bestTs = ts; best = c; }
  });
  return best;
}

function rebuildHeroFromLatest() {
  const latest = findLatestVideo();
  if (!latest) return;
  const id = latest.dataset.videoId;
  const title = decodeURIComponent(latest.dataset.videoTitle || '');
  const category = decodeURIComponent(latest.dataset.category || '');
  const created = latest.dataset.created ? new Date(latest.dataset.created) : null;
  const img = latest.querySelector('img');
  const thumb = img ? img.src : '';

  // Update hero background if thumb available
  if (thumb) {
    const heroImage = document.querySelector('.hero-image');
    if (heroImage) {
      heroImage.classList.add('latest-video-bg');
      heroImage.style.setProperty('--latest-video-bg', `url('${thumb}')`);
    }
  }

  // Update meta layer content
  const metaLayer = document.querySelector('.meta-layer .logo-and-text');
  if (!metaLayer) return;
  const dateLabel = created ? created.toLocaleDateString('he-IL') : '';
  metaLayer.innerHTML = `
    <span class="latest-tag">החדש באקדמיה</span>
    <h1 class="billboard-title latest-video-title">${title.replace(/[<>&"']/g, c => ({'<':'&lt;','>':'&gt;','&':'&amp;','"':'&quot;',"'":'&#39;'}[c]))}</h1>
    <div class="latest-meta">
      <span>${category.replace(/[<>&"']/g, c => ({'<':'&lt;','>':'&gt;','&':'&amp;','"':'&quot;',"'":'&#39;'}[c]))}</span>
      ${dateLabel ? `<span class="latest-meta-dot">·</span><span>הועלה ${dateLabel}</span>` : ''}
    </div>
    <p class="synopsis">הוידאו החדש ביותר שהועלה לאקדמיה. לחצי "הפעל" כדי לצפות עכשיו.</p>
  `;

  // Wire the Play button to open this specific video
  window.__latestVideoId = id;
}
setTimeout(rebuildHeroFromLatest, 2200);

/* Override hero play to use latest video as primary target */
window.__originalHeroTarget = (typeof getHeroTarget !== 'undefined') ? getHeroTarget : null;
async function getHeroTarget() {
  if (window.__latestVideoId) {
    const card = document.querySelector(`.title-card-container[data-video-id="${window.__latestVideoId}"]`);
    if (card) return { id: window.__latestVideoId, source: 'latest' };
  }
  // fallback: last watched → first card
  const lw = stGet(ST_KEYS.LAST_WATCHED, {});
  const last = Object.entries(lw).sort((a, b) => (b[1].ts || 0) - (a[1].ts || 0))[0];
  if (last && last[0]) return { id: last[0], source: 'lastWatched' };
  const first = document.querySelector('.row:not(#continueWatchingRow) .title-card-container[data-video-id]');
  if (first) return { id: first.dataset.videoId, source: 'first' };
  return null;
}

setTimeout(renderNotifications, 3000);"""
content = content.replace(JS_MARKER, JS_NEW)

TARGET.write_text(content, encoding='utf-8')
print(f"OK: Phase 3 P1 applied. Size: {len(content)} bytes")
