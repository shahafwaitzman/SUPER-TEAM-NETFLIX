#!/usr/bin/env python3
"""
OrdersHistory de-duplication clusterer.

Reads OrdersHistory.xlsx, finds groups of names that are likely the same human:
  - Same English name with multiple Hebrew transliterations
  - Same Hebrew name with multiple English transliterations
  - Distributors who order on behalf of many customers (1 buyer → many recipients)
  - Spelling variants (Levenshtein-close)

Outputs a single self-contained dedupe_review.html that the user can open in a
browser to manually confirm/reject each suggested cluster. Decisions are saved
in localStorage and exportable as JSON.
"""

import json
import sys
from collections import defaultdict
from pathlib import Path

import pandas as pd
from rapidfuzz import fuzz, process

# ---------- Configuration ----------
XLSX_PATH = Path("/Users/shahafwaitzman/Desktop/OrdersHistory (4).xlsx")
OUT_DIR = Path(__file__).parent
OUT_HTML = OUT_DIR / "dedupe_review.html"
OUT_DATA_JSON = OUT_DIR / "clusters.json"

# Fuzzy match thresholds (0-100). Higher = stricter.
SIMILARITY_THRESHOLD = 82
MIN_GROUP_SIZE = 2  # only show clusters with at least 2 different name forms

# ---------- Load data ----------
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

# ---------- Normalization ----------
def norm_en(s):
    if pd.isna(s):
        return ""
    return " ".join(str(s).upper().strip().split())

def norm_he(s):
    if pd.isna(s):
        return ""
    s = str(s).strip()
    s = " ".join(s.split())
    return s

# ---------- Fuzzy clustering ----------
def cluster_names(names, threshold=SIMILARITY_THRESHOLD):
    """Greedy single-link clustering by token-set ratio."""
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
            score = fuzz.token_set_ratio(n, other)
            if score >= threshold:
                cluster.append(other)
                seen.add(other)
        clusters.append(cluster)
    return [c for c in clusters if len(c) >= MIN_GROUP_SIZE]

# ---------- Build cluster report ----------
def build_clusters(df):
    df["buyer_en_norm"] = df["buyer_en"].apply(norm_en)
    df["recipient_he_norm"] = df["recipient_he"].apply(norm_he)

    # 1. English name fuzzy clusters
    en_names = df["buyer_en_norm"].unique().tolist()
    en_clusters = cluster_names(en_names)

    # 2. Hebrew name fuzzy clusters
    he_names = df["recipient_he_norm"].unique().tolist()
    he_clusters = cluster_names(he_names)

    # 3. English-name → Hebrew-recipients mapping (distributors-on-behalf)
    en_to_he = defaultdict(set)
    for _, row in df.iterrows():
        en, he = row["buyer_en_norm"], row["recipient_he_norm"]
        if en and he:
            en_to_he[en].add(he)
    distributor_groups = [
        {"buyer_en": en, "recipients_he": sorted(hes), "recipient_count": len(hes)}
        for en, hes in en_to_he.items()
        if len(hes) >= 3  # distributor threshold
    ]
    distributor_groups.sort(key=lambda x: -x["recipient_count"])

    # 4. Hebrew name → English variants
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

    # Order counts per name
    en_counts = df["buyer_en_norm"].value_counts().to_dict()
    he_counts = df["recipient_he_norm"].value_counts().to_dict()

    return {
        "stats": {
            "total_orders": int(len(df)),
            "unique_en_buyers": len(en_names),
            "unique_he_recipients": len(he_names),
            "en_fuzzy_clusters": len(en_clusters),
            "he_fuzzy_clusters": len(he_clusters),
            "distributor_groups": len(distributor_groups),
        },
        "en_fuzzy_clusters": [
            {"names": c, "counts": [en_counts.get(n, 0) for n in c]}
            for c in en_clusters
        ],
        "he_fuzzy_clusters": [
            {"names": c, "counts": [he_counts.get(n, 0) for n in c]}
            for c in he_clusters
        ],
        "distributor_groups": distributor_groups[:30],  # top 30
        "he_multi_en": he_with_multi_en[:30],
    }

# ---------- HTML generator ----------
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
<meta charset="UTF-8">
<title>Dedupe Review — OrdersHistory</title>
<style>
  body { font-family: -apple-system, "Segoe UI", Heebo, sans-serif; background: #0d1117; color: #e6edf3; padding: 24px; max-width: 1200px; margin: 0 auto; }
  h1 { color: #58a6ff; border-bottom: 2px solid #30363d; padding-bottom: 8px; }
  h2 { color: #f0883e; margin-top: 32px; border-bottom: 1px solid #30363d; padding-bottom: 6px; }
  .stats { background: #161b22; padding: 16px; border-radius: 8px; margin: 16px 0; display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 12px; }
  .stat { text-align: center; }
  .stat .num { font-size: 28px; font-weight: 700; color: #58a6ff; display: block; }
  .stat .label { font-size: 12px; color: #8b949e; }
  .cluster { background: #161b22; padding: 14px 18px; border-radius: 8px; margin: 12px 0; border-right: 4px solid #30363d; }
  .cluster.merged { border-color: #46d369; background: #0a2818; }
  .cluster.kept { border-color: #f85149; background: #2a0e0e; opacity: 0.5; }
  .cluster .names { display: flex; flex-wrap: wrap; gap: 8px; margin: 8px 0; }
  .name-pill { background: #21262d; padding: 4px 10px; border-radius: 16px; font-size: 14px; }
  .name-pill .count { color: #8b949e; font-size: 11px; margin-right: 4px; }
  .actions { display: flex; gap: 8px; margin-top: 8px; }
  button { background: #21262d; color: #e6edf3; border: 1px solid #30363d; padding: 6px 14px; border-radius: 6px; cursor: pointer; font-size: 13px; }
  button:hover { background: #30363d; }
  button.merge { background: #1f6feb; border-color: #1f6feb; }
  button.merge:hover { background: #388bfd; }
  button.keep { background: #6e7681; }
  .export-bar { position: sticky; top: 0; background: #0d1117; padding: 12px 0; z-index: 10; border-bottom: 1px solid #30363d; margin-bottom: 16px; display: flex; gap: 12px; align-items: center; }
  .progress { color: #8b949e; font-size: 13px; }
  .meta { color: #8b949e; font-size: 12px; margin-top: 4px; }
  details { background: #161b22; padding: 8px 14px; border-radius: 8px; margin: 8px 0; }
  details summary { cursor: pointer; font-weight: 600; color: #58a6ff; }
  details ul { margin: 8px 0 0; padding-right: 20px; }
  details li { margin: 2px 0; font-size: 13px; }
</style>
</head>
<body>
<h1>סקירת כפילויות — OrdersHistory</h1>

<div class="stats">__STATS_HTML__</div>

<div class="export-bar">
  <button onclick="exportDecisions()">📥 ייצא JSON עם החלטות</button>
  <span class="progress" id="progressLabel">0 החלטות נשמרו</span>
</div>

<h2>1. שמות אנגלית — וריאציות איות (fuzzy match)</h2>
<p class="meta">קבוצות שמות אנגלית עם דמיון ≥82%. סקור והחלט אם זה אותו אדם.</p>
<div id="enClusters">__EN_CLUSTERS_HTML__</div>

<h2>2. שמות עברית — וריאציות איות (fuzzy match)</h2>
<p class="meta">קבוצות שמות עברית עם דמיון ≥82%.</p>
<div id="heClusters">__HE_CLUSTERS_HTML__</div>

<h2>3. מפיצים שמזמינים עבור אחרים (1 קונה → מספר נמענים)</h2>
<p class="meta">מקרה ה-LIZ MEIROVICH — קונה אחד עם 3+ נמענים שונים. אלו המפיצים.</p>
<div id="distributors">__DISTRIBUTORS_HTML__</div>

<h2>4. שמות עברית עם איותי אנגלית מרובים</h2>
<p class="meta">אותו נמען בעברית, מספר איותים שונים באנגלית — אותו אדם.</p>
<div id="heMultiEn">__HE_MULTI_EN_HTML__</div>

<script>
const decisions = JSON.parse(localStorage.getItem('dedupe_decisions') || '{}');

function decide(clusterId, action) {
  decisions[clusterId] = action;
  localStorage.setItem('dedupe_decisions', JSON.stringify(decisions));
  const el = document.getElementById(clusterId);
  if (el) {
    el.classList.remove('merged', 'kept');
    if (action === 'merge') el.classList.add('merged');
    else if (action === 'keep') el.classList.add('kept');
  }
  updateProgress();
}

function updateProgress() {
  const n = Object.keys(decisions).length;
  document.getElementById('progressLabel').textContent = `${n} החלטות נשמרו`;
}

function exportDecisions() {
  const blob = new Blob([JSON.stringify(decisions, null, 2)], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'dedupe_decisions.json';
  a.click();
  URL.revokeObjectURL(url);
}

// Restore visual state from saved decisions
window.addEventListener('DOMContentLoaded', () => {
  Object.entries(decisions).forEach(([id, action]) => {
    const el = document.getElementById(id);
    if (el) el.classList.add(action === 'merge' ? 'merged' : 'kept');
  });
  updateProgress();
});
</script>
</body>
</html>"""

def render_cluster(prefix, idx, names, counts, extra=""):
    pills = "".join(
        f'<span class="name-pill"><span class="count">{c}</span>{n}</span>'
        for n, c in zip(names, counts)
    )
    cid = f"{prefix}_{idx}"
    return f'''<div class="cluster" id="{cid}">
  <div class="names">{pills}</div>{extra}
  <div class="actions">
    <button class="merge" onclick="decide('{cid}', 'merge')">✓ אותו אדם</button>
    <button class="keep" onclick="decide('{cid}', 'keep')">✕ אנשים נפרדים</button>
  </div>
</div>'''

def render_distributor(idx, group):
    cid = f"dist_{idx}"
    recipients_html = "".join(f'<li>{r}</li>' for r in group["recipients_he"])
    return f'''<div class="cluster" id="{cid}">
  <div><strong>{group["buyer_en"]}</strong> — {group["recipient_count"]} נמענים שונים</div>
  <details><summary>הצג נמענים</summary><ul>{recipients_html}</ul></details>
  <div class="meta">סביר שזה מפיץ. החלטה תקבע אם להחזיק רק אותו או גם את כל הנמענים בנפרד.</div>
  <div class="actions">
    <button class="merge" onclick="decide('{cid}', 'mark_distributor')">📌 סמן כמפיץ</button>
    <button class="keep" onclick="decide('{cid}', 'keep')">✕ דלג</button>
  </div>
</div>'''

def render_he_multi_en(idx, group):
    cid = f"hemulti_{idx}"
    en_pills = "".join(f'<span class="name-pill">{n}</span>' for n in group["buyers_en"])
    return f'''<div class="cluster" id="{cid}">
  <div><strong>{group["recipient_he"]}</strong> = {group["buyer_count"]} איותי אנגלית:</div>
  <div class="names">{en_pills}</div>
  <div class="actions">
    <button class="merge" onclick="decide('{cid}', 'merge')">✓ אותו אדם</button>
    <button class="keep" onclick="decide('{cid}', 'keep')">✕ אנשים נפרדים</button>
  </div>
</div>'''

def main():
    print(f"Loading {XLSX_PATH}...")
    df = load_orders()
    print(f"Loaded {len(df)} orders")
    print("Building clusters...")
    data = build_clusters(df)

    s = data["stats"]
    print(f"\nStats: {s}")

    OUT_DATA_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2))
    print(f"Wrote {OUT_DATA_JSON}")

    stats_html = "".join(
        f'<div class="stat"><span class="num">{v}</span><span class="label">{k.replace("_", " ")}</span></div>'
        for k, v in s.items()
    )
    en_html = "".join(
        render_cluster("en", i, c["names"], c["counts"])
        for i, c in enumerate(data["en_fuzzy_clusters"])
    ) or "<p>אין וריאציות אנגלית</p>"
    he_html = "".join(
        render_cluster("he", i, c["names"], c["counts"])
        for i, c in enumerate(data["he_fuzzy_clusters"])
    ) or "<p>אין וריאציות עברית</p>"
    dist_html = "".join(
        render_distributor(i, g) for i, g in enumerate(data["distributor_groups"])
    ) or "<p>אין מפיצים</p>"
    hemulti_html = "".join(
        render_he_multi_en(i, g) for i, g in enumerate(data["he_multi_en"])
    ) or "<p>אין כפילויות עברית→אנגלית</p>"

    html = (HTML_TEMPLATE
            .replace("__STATS_HTML__", stats_html)
            .replace("__EN_CLUSTERS_HTML__", en_html)
            .replace("__HE_CLUSTERS_HTML__", he_html)
            .replace("__DISTRIBUTORS_HTML__", dist_html)
            .replace("__HE_MULTI_EN_HTML__", hemulti_html))

    OUT_HTML.write_text(html, encoding="utf-8")
    print(f"Wrote {OUT_HTML}")
    print(f"\nOpen in browser: file://{OUT_HTML.resolve()}")

if __name__ == "__main__":
    main()
