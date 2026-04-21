#!/usr/bin/env python3
"""P1 flow-viewer home redesign - step 3:
  (a) Add click handlers for .home-card to switch views.
  (b) Guard obsolete stat ID references with optional chaining.
"""
import sys
from pathlib import Path

TARGET = Path("/Users/shahafwaitzman/Documents/CLOUD CODE/flow-viewer/index.html")

# (a) INSERT card click handler right after the nav-link handler block
OLD_NAV_BLOCK = """document.querySelectorAll('.nav-link').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.nav-link').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    document.querySelectorAll('.view').forEach(v => v.classList.remove('active'));
    document.getElementById('view-' + btn.dataset.view).classList.add('active');
    window.scrollTo({ top: 0, behavior: 'smooth' });
    if (btn.dataset.view === 'diagram') triggerReveals();
  });
});"""

NEW_NAV_BLOCK = """document.querySelectorAll('.nav-link').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.nav-link').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    document.querySelectorAll('.view').forEach(v => v.classList.remove('active'));
    document.getElementById('view-' + btn.dataset.view).classList.add('active');
    window.scrollTo({ top: 0, behavior: 'smooth' });
    if (btn.dataset.view === 'diagram') triggerReveals();
  });
});

// ============ HOME CARD CLICK HANDLERS ============
// Cards on the FLOW home view act as shortcuts to the 5 main sections.
// Each card triggers the matching nav-link click, reusing the existing
// view-switching logic (scrollTo + reveals). The "flow" card stays on
// the current view and smooth-scrolls to the stages grid instead.
document.querySelectorAll('.home-card').forEach(card => {
  card.addEventListener('click', () => {
    const target = card.dataset.card;
    if (!target) return;
    if (target === 'flow') {
      const grid = document.getElementById('stagesGrid');
      if (grid) grid.scrollIntoView({ behavior: 'smooth', block: 'start' });
      return;
    }
    const navBtn = document.querySelector(`.nav-link[data-view="${target}"]`);
    if (navBtn) navBtn.click();
  });
});"""

# (b) Guard the two obsolete stat writes
OLD_STATS = """document.getElementById('statFiles').textContent = LIBRARY.length + PROFITS.length;
document.getElementById('statLinks').textContent = STAGES.flatMap(s => s.links || []).filter(l => l.url && l.url.startsWith('http')).length;"""

NEW_STATS = """// Legacy stat counters (elements removed in home redesign — guarded for safety)
const _statFiles = document.getElementById('statFiles');
if (_statFiles) _statFiles.textContent = LIBRARY.length + PROFITS.length;
const _statLinks = document.getElementById('statLinks');
if (_statLinks) _statLinks.textContent = STAGES.flatMap(s => s.links || []).filter(l => l.url && l.url.startsWith('http')).length;"""

content = TARGET.read_text(encoding='utf-8')

for label, old, new in (
    ("nav click + card handlers", OLD_NAV_BLOCK, NEW_NAV_BLOCK),
    ("stat guards", OLD_STATS, NEW_STATS),
):
    count = content.count(old)
    if count != 1:
        print(f"ERROR [{label}]: expected exactly 1 match, found {count}", file=sys.stderr)
        sys.exit(1)
    content = content.replace(old, new)

TARGET.write_text(content, encoding='utf-8')
print(f"OK: Wired home-card clicks + guarded stat IDs. Final size: {len(content)} bytes")
