#!/usr/bin/env python3
"""
OrdersHistory de-duplication clusterer (Super Team Academy themed).

Original 4-section layout, restyled to match the production site:
- Bebas Neue + Heebo fonts
- Netflix-red (#E50914) accent
- Dark Netflix-style backgrounds

Sections:
  1. EN fuzzy clusters       (review only — typically empty)
  2. HE fuzzy clusters       (REAL duplicates — approve to merge)
  3. Distributor info        (NOT duplicates — buyer-on-behalf info)
  4. HE → multi-EN variants  (REAL duplicates — approve to merge)

After all decisions, user can export merged_customers.json with the unified
customer list.
"""

import json
from collections import defaultdict
from pathlib import Path

import pandas as pd
from rapidfuzz import fuzz

XLSX_PATH = Path("/Users/shahafwaitzman/Desktop/OrdersHistory (4).xlsx")
OUT_DIR = Path(__file__).parent
OUT_HTML = OUT_DIR / "dedupe_review.html"
OUT_DATA_JSON = OUT_DIR / "clusters.json"

SIMILARITY_THRESHOLD = 82
MIN_GROUP_SIZE = 2


def load_orders():
    df = pd.read_excel(XLSX_PATH, header=4)
    df = df.dropna(subset=[df.columns[0]])
    return df.rename(columns={
        df.columns[0]: "order_id",
        df.columns[1]: "buyer_en",
        df.columns[2]: "buyer_type",
        df.columns[3]: "discount",
        df.columns[4]: "date",
        df.columns[5]: "month",
        df.columns[6]: "status",
        df.columns[7]: "recipient_he",
        df.columns[8]: "credit_pts",
        df.columns[9]: "total",
    })


def norm_en(s):
    if pd.isna(s):
        return ""
    return " ".join(str(s).upper().strip().split())


def norm_he(s):
    if pd.isna(s):
        return ""
    return " ".join(str(s).strip().split())


def cluster_names(names, threshold=SIMILARITY_THRESHOLD):
    names = sorted(set(n for n in names if n))
    clusters = []
    seen = set()
    for n in names:
        if n in seen:
            continue
        cluster = [n]
        seen.add(n)
        for other in names:
            if other in seen:
                continue
            if fuzz.token_set_ratio(n, other) >= threshold:
                cluster.append(other)
                seen.add(other)
        clusters.append(cluster)
    return [c for c in clusters if len(c) >= MIN_GROUP_SIZE]


def build_clusters(df):
    df["buyer_en_norm"] = df["buyer_en"].apply(norm_en)
    df["recipient_he_norm"] = df["recipient_he"].apply(norm_he)

    en_names = df["buyer_en_norm"].unique().tolist()
    en_clusters = cluster_names(en_names)

    he_names = df["recipient_he_norm"].unique().tolist()
    he_clusters = cluster_names(he_names)

    en_to_he = defaultdict(set)
    for _, row in df.iterrows():
        en, he = row["buyer_en_norm"], row["recipient_he_norm"]
        if en and he:
            en_to_he[en].add(he)
    distributor_groups = [
        {"buyer_en": en, "recipients_he": sorted(hes), "recipient_count": len(hes)}
        for en, hes in en_to_he.items()
        if len(hes) >= 3
    ]
    distributor_groups.sort(key=lambda x: -x["recipient_count"])

    he_to_en = defaultdict(set)
    for _, row in df.iterrows():
        en, he = row["buyer_en_norm"], row["recipient_he_norm"]
        if en and he:
            he_to_en[he].add(en)
    he_with_multi_en = [
        {"recipient_he": he, "buyers_en": sorted(ens), "buyer_count": len(ens)}
        for he, ens in he_to_en.items()
        if len(ens) >= 2
    ]
    he_with_multi_en.sort(key=lambda x: -x["buyer_count"])

    en_counts = df["buyer_en_norm"].value_counts().to_dict()
    he_counts = df["recipient_he_norm"].value_counts().to_dict()

    return {
        "stats": {
            "total_orders": int(len(df)),
            "unique_buyers_en": len(en_names),
            "unique_recipients_he": len(he_names),
            "duplicates_found": len(en_clusters) + len(he_clusters) + len(he_with_multi_en),
            "distributors": len(distributor_groups),
        },
        "en_fuzzy_clusters": [
            {"names": c, "counts": [en_counts.get(n, 0) for n in c]}
            for c in en_clusters
        ],
        "he_fuzzy_clusters": [
            {"names": c, "counts": [he_counts.get(n, 0) for n in c]}
            for c in he_clusters
        ],
        "distributor_groups": distributor_groups[:30],
        "he_multi_en": he_with_multi_en[:30],
    }


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>סקירת כפילויות — Super Team Academy</title>
<link href="https://fonts.googleapis.com/css2?family=Heebo:wght@300;400;500;700;900&family=Bebas+Neue&display=swap" rel="stylesheet">
<style>
  :root {
    --nflx-red: #E50914;
    --nflx-red-dark: #B9090B;
    --bg-base: #0a0a0a;
    --bg-card: #1a1a1a;
    --bg-card-hover: #232323;
    --border: rgba(255,255,255,0.08);
    --text: #fff;
    --muted: rgba(255,255,255,0.6);
    --good: #46d369;
    --warn: #f0883e;
  }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    font-family: 'Heebo', -apple-system, sans-serif;
    background: var(--bg-base);
    color: var(--text);
    min-height: 100vh;
    line-height: 1.5;
  }

  /* ── Header — Netflix-style ── */
  .top-header {
    background: linear-gradient(180deg, rgba(0,0,0,0.95) 0%, rgba(0,0,0,0.7) 100%);
    border-bottom: 1px solid var(--border);
    padding: 18px 32px;
    display: flex; justify-content: space-between; align-items: center;
    position: sticky; top: 0; z-index: 100; backdrop-filter: blur(12px);
  }
  .brand { display: flex; align-items: baseline; gap: 8px; }
  .brand .super { font-family: 'Bebas Neue', sans-serif; font-size: 22px; letter-spacing: 2px; color: #fff; }
  .brand .academy { font-family: 'Bebas Neue', sans-serif; font-size: 22px; letter-spacing: 2px; color: var(--nflx-red); }
  .progress-pill {
    background: rgba(229,9,20,0.12); color: var(--nflx-red);
    padding: 6px 14px; border-radius: 20px; font-size: 13px; font-weight: 600;
    border: 1px solid rgba(229,9,20,0.3);
  }

  main { max-width: 1280px; margin: 0 auto; padding: 32px 24px; }

  /* ── Hero / page title ── */
  .page-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: clamp(36px, 4vw, 56px);
    letter-spacing: 2px;
    margin-bottom: 8px;
    line-height: 1;
  }
  .page-subtitle { color: var(--muted); font-size: 14px; margin-bottom: 28px; }

  /* ── Stats row ── */
  .stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(170px, 1fr)); gap: 12px; margin-bottom: 32px; }
  .stat {
    background: var(--bg-card); padding: 18px 16px; border-radius: 8px;
    text-align: center; border: 1px solid var(--border);
  }
  .stat .num { font-family: 'Bebas Neue', sans-serif; font-size: 32px; color: var(--nflx-red); display: block; line-height: 1; }
  .stat .label { font-size: 11px; color: var(--muted); text-transform: uppercase; letter-spacing: 2px; margin-top: 4px; display: block; }

  /* ── Section headers ── */
  .section { margin: 36px 0 16px; padding-bottom: 12px; border-bottom: 1px solid var(--border); }
  .section h2 {
    font-family: 'Bebas Neue', sans-serif; font-size: 28px; letter-spacing: 1.5px;
    color: var(--text); display: flex; align-items: center; gap: 12px;
  }
  .section h2 .badge-count {
    background: var(--nflx-red); color: #fff; font-family: 'Heebo', sans-serif;
    font-size: 12px; padding: 2px 10px; border-radius: 12px; font-weight: 700; letter-spacing: 0;
  }
  .section .desc { color: var(--muted); font-size: 13px; margin-top: 6px; }

  /* ── Cluster cards ── */
  .cluster {
    background: var(--bg-card); padding: 16px 20px; border-radius: 8px; margin: 10px 0;
    border-right: 4px solid var(--border); transition: all 0.2s;
  }
  .cluster:hover { background: var(--bg-card-hover); }
  .cluster.merged { border-right-color: var(--good); background: rgba(70,211,105,0.06); }
  .cluster.kept { border-right-color: rgba(255,255,255,0.3); opacity: 0.55; }
  .cluster .names { display: flex; flex-wrap: wrap; gap: 8px; margin: 4px 0 12px; }
  .name-pill {
    background: rgba(255,255,255,0.06); padding: 5px 12px; border-radius: 16px;
    font-size: 14px; color: var(--text);
  }
  .name-pill .count {
    color: var(--nflx-red); font-size: 11px; margin-left: 6px; font-weight: 700;
  }
  .actions { display: flex; gap: 8px; margin-top: 8px; }
  .btn {
    padding: 7px 16px; border-radius: 4px; font-size: 13px; font-weight: 700;
    cursor: pointer; border: 1px solid transparent; font-family: inherit;
    transition: all 0.15s;
  }
  .btn-merge { background: var(--nflx-red); color: #fff; border-color: var(--nflx-red); }
  .btn-merge:hover { background: var(--nflx-red-dark); }
  .btn-keep { background: transparent; color: var(--text); border-color: var(--border); }
  .btn-keep:hover { background: rgba(255,255,255,0.06); }
  .btn-export { background: #fff; color: #000; padding: 10px 22px; font-size: 14px; }
  .btn-export:hover { background: rgba(255,255,255,0.85); }

  /* ── Distributor section ── */
  .meta-info {
    background: rgba(229,9,20,0.06); border-right: 3px solid var(--nflx-red);
    padding: 12px 16px; border-radius: 4px; margin-bottom: 16px;
    color: var(--muted); font-size: 13px;
  }
  .meta-info b { color: var(--text); }
  details { background: var(--bg-card); padding: 0; border-radius: 8px; margin: 8px 0;
            border: 1px solid var(--border); }
  details summary {
    cursor: pointer; padding: 14px 18px; font-weight: 600; color: var(--text);
    display: flex; align-items: center; justify-content: space-between;
    font-family: 'Heebo', sans-serif; list-style: none;
  }
  details summary::-webkit-details-marker { display: none; }
  details summary::after { content: "▾"; color: var(--nflx-red); font-size: 14px; transition: transform 0.2s; }
  details[open] summary::after { transform: rotate(180deg); }
  details summary .right { display: flex; gap: 14px; align-items: baseline; }
  details summary .name-en { font-family: 'Bebas Neue', sans-serif; font-size: 18px; letter-spacing: 1px; }
  details summary .recipient-count { color: var(--nflx-red); font-size: 13px; }
  details ul { margin: 0; padding: 0 24px 14px 18px; list-style: none; }
  details li {
    padding: 8px 0; font-size: 14px; border-bottom: 1px solid var(--border);
    display: flex; justify-content: space-between; align-items: center;
  }
  details li:last-child { border-bottom: none; }
  .warn-badge {
    background: rgba(240,136,62,0.15); color: var(--warn); font-size: 11px;
    padding: 3px 9px; border-radius: 10px; font-weight: 600;
  }

  /* ── Floating action bar ── */
  .floating-bar {
    position: fixed; bottom: 24px; right: 50%; transform: translateX(50%);
    background: rgba(0,0,0,0.95); border: 1px solid var(--border);
    padding: 14px 20px; border-radius: 50px; backdrop-filter: blur(12px);
    display: flex; gap: 16px; align-items: center; z-index: 100;
    box-shadow: 0 8px 32px rgba(0,0,0,0.6);
  }
  .floating-bar .info { color: var(--muted); font-size: 13px; }
  .floating-bar .info b { color: var(--text); font-weight: 700; }

  .empty { padding: 24px; color: var(--muted); text-align: center; font-size: 14px; }
</style>
</head>
<body>

<header class="top-header">
  <div class="brand">
    <span class="super">SUPER TEAM</span>
    <span class="academy">ACADEMY</span>
  </div>
  <span class="progress-pill" id="progressLabel">0 החלטות</span>
</header>

<main>
  <h1 class="page-title">סקירת כפילויות</h1>
  <p class="page-subtitle">איחוד שמות לקוחות מתוך OrdersHistory · אישור / שמירה בנפרד</p>

  <div class="stats">__STATS_HTML__</div>

  <!-- ── Section 1: English fuzzy clusters ── -->
  <div class="section">
    <h2>וריאציות איות באנגלית <span class="badge-count">__EN_COUNT__</span></h2>
    <div class="desc">קבוצות שמות אנגלית עם דמיון ≥82%.</div>
  </div>
  <div id="enClusters">__EN_CLUSTERS_HTML__</div>

  <!-- ── Section 2: Hebrew fuzzy clusters ── -->
  <div class="section">
    <h2>וריאציות איות בעברית <span class="badge-count">__HE_COUNT__</span></h2>
    <div class="desc">קבוצות שמות עברית עם דמיון ≥82% — אישור מאחד אותן ללקוח אחד.</div>
  </div>
  <div id="heClusters">__HE_CLUSTERS_HTML__</div>

  <!-- ── Section 3: Distributors (NOT duplicates) ── -->
  <div class="section">
    <h2>מפיצים שמזמינים עבור אחרים <span class="badge-count">__DIST_COUNT__</span></h2>
    <div class="desc">קונה אחד עם 3+ נמענים שונים — סביר שזה מפיץ.</div>
  </div>
  <div class="meta-info">
    <b>זה לא כפילות</b> — זה מידע על מי הזמין עבור מי. נמענים שמסומנים ב-⚠ הופיעו גם בקבוצת כפילות חשודה (מעלה).
  </div>
  <div id="distributors">__DISTRIBUTORS_HTML__</div>

  <!-- ── Section 4: HE with multi EN ── -->
  <div class="section">
    <h2>אותו שם עברית · איותי אנגלית מרובים <span class="badge-count">__HEMULTI_COUNT__</span></h2>
    <div class="desc">נמען עברי אחד עם מספר איותי אנגלית — סביר שזה אותו אדם עם איותים שונים.</div>
  </div>
  <div id="heMultiEn">__HE_MULTI_EN_HTML__</div>
</main>

<div class="floating-bar">
  <span class="info"><b id="mergedCount">0</b> אוחדו · <b id="keptCount">0</b> נשמרו</span>
  <button class="btn btn-export" onclick="exportDecisions()">📥 ייצא JSON עם החלטות</button>
</div>

<script>
const decisions = JSON.parse(localStorage.getItem('dedupe_decisions_v3') || '{}');

function decide(clusterId, action) {
  decisions[clusterId] = action;
  localStorage.setItem('dedupe_decisions_v3', JSON.stringify(decisions));
  refreshUI(clusterId);
}

function refreshUI(id) {
  const el = document.getElementById(id);
  if (el) {
    el.classList.remove('merged', 'kept');
    if (decisions[id] === 'merge') el.classList.add('merged');
    else if (decisions[id] === 'keep') el.classList.add('kept');
  }
  updateProgress();
}

function updateProgress() {
  const all = Object.values(decisions);
  const merged = all.filter(a => a === 'merge').length;
  const kept = all.filter(a => a === 'keep').length;
  document.getElementById('progressLabel').textContent = `${merged + kept} החלטות`;
  document.getElementById('mergedCount').textContent = merged;
  document.getElementById('keptCount').textContent = kept;
}

function exportDecisions() {
  // Build merged_customers.json with the unified mapping
  const clusters = window.__clustersData;
  const mapping = {};  // alias_name → canonical_name
  const merged = [];

  // Hebrew fuzzy clusters
  clusters.he_fuzzy_clusters.forEach((c, i) => {
    const id = 'he_' + i;
    if (decisions[id] === 'merge') {
      const canonical = c.names[0];  // first name as canonical
      c.names.forEach(n => { if (n !== canonical) mapping[n] = canonical; });
      merged.push({ canonical, aliases: c.names.slice(1), source: 'he_fuzzy' });
    }
  });
  // English fuzzy clusters
  clusters.en_fuzzy_clusters.forEach((c, i) => {
    const id = 'en_' + i;
    if (decisions[id] === 'merge') {
      const canonical = c.names[0];
      c.names.forEach(n => { if (n !== canonical) mapping[n] = canonical; });
      merged.push({ canonical, aliases: c.names.slice(1), source: 'en_fuzzy' });
    }
  });
  // HE → multi EN
  clusters.he_multi_en.forEach((g, i) => {
    const id = 'hemulti_' + i;
    if (decisions[id] === 'merge') {
      merged.push({ canonical_he: g.recipient_he, en_aliases: g.buyers_en, source: 'he_multi_en' });
    }
  });

  const payload = {
    generated_at: new Date().toISOString(),
    decisions,
    mapping,
    merged_groups: merged,
    summary: {
      total_decisions: Object.keys(decisions).length,
      merged_count: merged.length,
      aliases_count: Object.keys(mapping).length,
    },
  };
  const blob = new Blob([JSON.stringify(payload, null, 2)], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url; a.download = 'merged_customers.json'; a.click();
  URL.revokeObjectURL(url);
}

window.addEventListener('DOMContentLoaded', () => {
  Object.keys(decisions).forEach(id => refreshUI(id));
  updateProgress();
});

window.__clustersData = __CLUSTERS_JSON__;
</script>
</body>
</html>"""


def render_cluster(prefix, idx, names, counts):
    pills = "".join(
        f'<span class="name-pill">{n} <span class="count">{c}</span></span>'
        for n, c in zip(names, counts)
    )
    cid = f"{prefix}_{idx}"
    return f'''<div class="cluster" id="{cid}">
  <div class="names">{pills}</div>
  <div class="actions">
    <button class="btn btn-merge" onclick="decide('{cid}', 'merge')">✓ אותו אדם — אחד</button>
    <button class="btn btn-keep" onclick="decide('{cid}', 'keep')">✕ אנשים נפרדים</button>
  </div>
</div>'''


def render_distributor(idx, group, dup_names):
    cid = f"dist_{idx}"
    recipients_html = ""
    for r in group["recipients_he"]:
        if r in dup_names:
            recipients_html += f'<li>{r}<span class="warn-badge">⚠ כפילות חשודה — בדוק קטע "כפילויות עברית"</span></li>'
        else:
            recipients_html += f'<li>{r}<span></span></li>'
    return f'''<details>
  <summary>
    <span class="right">
      <span class="name-en">{group["buyer_en"]}</span>
      <span class="recipient-count">{group["recipient_count"]} נמענים</span>
    </span>
  </summary>
  <ul>{recipients_html}</ul>
</details>'''


def render_he_multi_en(idx, group):
    cid = f"hemulti_{idx}"
    en_pills = "".join(f'<span class="name-pill">{n}</span>' for n in group["buyers_en"])
    return f'''<div class="cluster" id="{cid}">
  <div class="names">
    <span class="name-pill" style="background:rgba(229,9,20,0.15);color:#fff;font-weight:600;">{group["recipient_he"]}</span>
    <span style="color:var(--muted);font-size:13px;align-self:center;">⇐</span>
    {en_pills}
  </div>
  <div class="actions">
    <button class="btn btn-merge" onclick="decide('{cid}', 'merge')">✓ אותו אדם — אחד</button>
    <button class="btn btn-keep" onclick="decide('{cid}', 'keep')">✕ אנשים נפרדים</button>
  </div>
</div>'''


def main():
    print(f"Loading {XLSX_PATH}...")
    df = load_orders()
    print(f"Loaded {len(df)} orders")

    data = build_clusters(df)
    s = data["stats"]
    print(f"Stats: {s}")

    OUT_DATA_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2))

    stats_html = "".join(
        f'<div class="stat"><span class="num">{v:,}</span><span class="label">{k.replace("_", " ")}</span></div>'
        for k, v in s.items()
    )

    en_html = "".join(
        render_cluster("en", i, c["names"], c["counts"])
        for i, c in enumerate(data["en_fuzzy_clusters"])
    ) or '<p class="empty">אין וריאציות אנגלית</p>'

    he_html = "".join(
        render_cluster("he", i, c["names"], c["counts"])
        for i, c in enumerate(data["he_fuzzy_clusters"])
    ) or '<p class="empty">אין וריאציות עברית</p>'

    dup_names = set()
    for c in data["he_fuzzy_clusters"]:
        for name in c["names"]:
            dup_names.add(name)
    for g in data["he_multi_en"]:
        dup_names.add(g["recipient_he"])

    dist_html = "".join(
        render_distributor(i, g, dup_names)
        for i, g in enumerate(data["distributor_groups"])
    ) or '<p class="empty">אין מפיצים</p>'

    hemulti_html = "".join(
        render_he_multi_en(i, g) for i, g in enumerate(data["he_multi_en"])
    ) or '<p class="empty">אין כפילויות עברית→אנגלית</p>'

    html = (HTML_TEMPLATE
            .replace("__STATS_HTML__", stats_html)
            .replace("__EN_COUNT__", str(len(data["en_fuzzy_clusters"])))
            .replace("__HE_COUNT__", str(len(data["he_fuzzy_clusters"])))
            .replace("__DIST_COUNT__", str(len(data["distributor_groups"])))
            .replace("__HEMULTI_COUNT__", str(len(data["he_multi_en"])))
            .replace("__EN_CLUSTERS_HTML__", en_html)
            .replace("__HE_CLUSTERS_HTML__", he_html)
            .replace("__DISTRIBUTORS_HTML__", dist_html)
            .replace("__HE_MULTI_EN_HTML__", hemulti_html)
            .replace("__CLUSTERS_JSON__", json.dumps(data, ensure_ascii=False)))

    OUT_HTML.write_text(html, encoding="utf-8")
    print(f"Wrote {OUT_HTML}")
    print(f"Open: file://{OUT_HTML.resolve()}")


if __name__ == "__main__":
    main()
