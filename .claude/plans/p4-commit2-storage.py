#!/usr/bin/env python3
"""Commit 2 · localStorage foundation for academy-hub.
  - Per-user scoped keys: sta_${email}_${field}
  - Schema: progress, watchlist, lastWatched, streak, badges, notificationsSeen
  - Helpers: stGet, stSet, stPush, stRemove, stInit
  - NO UI changes yet — just scaffolding + auto-init on load
"""
import sys
from pathlib import Path

TARGET = Path("/Users/shahafwaitzman/Documents/CLOUD CODE/super-team-academy/academy-hub.html")
content = TARGET.read_text(encoding='utf-8')

# Insert foundation block right after the userEmail setup, before the DRIVE section
MARKER = """  localStorage.setItem('userEmail', userEmail);
}

/* ═══════════════════════════════════════════
   GOOGLE DRIVE INTEGRATION
   ═══════════════════════════════════════════ */"""

REPLACEMENT = """  localStorage.setItem('userEmail', userEmail);
}

/* ═══════════════════════════════════════════
   PHASE 2B · localStorage foundation (per-user scoped)
   ═══════════════════════════════════════════ */
const ST_NS = userEmail ? `sta_${userEmail}` : 'sta_guest';
const ST_KEYS = {
  PROGRESS:          `${ST_NS}_progress`,          // { [videoId]: 0..100 }
  WATCHLIST:         `${ST_NS}_watchlist`,         // [videoId, ...]
  LAST_WATCHED:      `${ST_NS}_lastWatched`,       // { [videoId]: ISO timestamp }
  STREAK:            `${ST_NS}_streak`,            // { count: N, lastLogin: "YYYY-MM-DD" }
  BADGES:            `${ST_NS}_badges`,            // ["badge_id", ...]
  NOTIFICATIONS_SEEN:`${ST_NS}_notifsSeen`,        // [videoId, ...]
};

function stGet(key, fallback) {
  try {
    const raw = localStorage.getItem(key);
    if (raw === null) return fallback;
    return JSON.parse(raw);
  } catch (e) {
    console.warn('stGet parse failed for', key, e);
    return fallback;
  }
}
function stSet(key, val) {
  try {
    localStorage.setItem(key, JSON.stringify(val));
  } catch (e) {
    console.warn('stSet failed for', key, e);
  }
}
function stPush(key, val) {
  const arr = stGet(key, []);
  if (!Array.isArray(arr)) return;
  if (!arr.includes(val)) { arr.push(val); stSet(key, arr); }
}
function stRemove(key, val) {
  const arr = stGet(key, []);
  if (!Array.isArray(arr)) return;
  const i = arr.indexOf(val);
  if (i >= 0) { arr.splice(i, 1); stSet(key, arr); }
}
function stHas(key, val) {
  const arr = stGet(key, []);
  return Array.isArray(arr) && arr.includes(val);
}

/* Initialize missing keys with empty defaults — idempotent, safe on every load */
(function stInit() {
  if (stGet(ST_KEYS.PROGRESS, null) === null) stSet(ST_KEYS.PROGRESS, {});
  if (stGet(ST_KEYS.WATCHLIST, null) === null) stSet(ST_KEYS.WATCHLIST, []);
  if (stGet(ST_KEYS.LAST_WATCHED, null) === null) stSet(ST_KEYS.LAST_WATCHED, {});
  if (stGet(ST_KEYS.STREAK, null) === null) stSet(ST_KEYS.STREAK, { count: 0, lastLogin: null });
  if (stGet(ST_KEYS.BADGES, null) === null) stSet(ST_KEYS.BADGES, []);
  if (stGet(ST_KEYS.NOTIFICATIONS_SEEN, null) === null) stSet(ST_KEYS.NOTIFICATIONS_SEEN, []);
})();

/* Exposed on window for console debugging during dev */
window.__sta = { ST_NS, ST_KEYS, stGet, stSet, stPush, stRemove, stHas };

/* ═══════════════════════════════════════════
   GOOGLE DRIVE INTEGRATION
   ═══════════════════════════════════════════ */"""

if MARKER not in content:
    print("ERROR: marker not found", file=sys.stderr); sys.exit(1)
content = content.replace(MARKER, REPLACEMENT)

TARGET.write_text(content, encoding='utf-8')
print(f"OK: localStorage foundation added. Size: {len(content)} bytes")
