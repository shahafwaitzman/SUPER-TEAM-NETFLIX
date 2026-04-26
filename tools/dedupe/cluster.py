#!/usr/bin/env python3
"""
OrdersHistory de-duplication clusterer (v2 — customer-centric).

Reads OrdersHistory.xlsx, builds a unified customer list where each customer
appears once with all their order history aggregated.

Detects:
  - Distributors who order on behalf of others (1 buyer → many recipients)
  - Hebrew name variants of the same customer (fuzzy match)
  - English-name variations for the same Hebrew recipient

Output:
  - dedupe_review.html — customer-centric grid: each customer as a compact
    card showing canonical name + "הוזמן ע״י X" + order count + total spent.
  - clusters.json — raw analysis data.
"""

import json
import re
from collections import defaultdict
from pathlib import Path

import pandas as pd
from rapidfuzz import fuzz

XLSX_PATH = Path("/Users/shahafwaitzman/Desktop/OrdersHistory (4).xlsx")
OUT_DIR = Path(__file__).parent
OUT_HTML = OUT_DIR / "dedupe_review.html"
OUT_DATA_JSON = OUT_DIR / "clusters.json"

SIMILARITY_THRESHOLD = 82
DISTRIBUTOR_MIN_RECIPIENTS = 3


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


def parse_total(val):
    if pd.isna(val):
        return 0.0
    s = str(val).replace("ILS", "").replace(",", "").strip()
    try:
        return float(s)
    except ValueError:
        return 0.0


def cluster_he_names(names, threshold=SIMILARITY_THRESHOLD):
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
    return clusters


def build_customer_view(df):
    """Customer-centric: each Hebrew recipient name = one row.
    Shows their order count, total, and which distributors ordered for them."""
    df["buyer_en_norm"] = df["buyer_en"].apply(norm_en)
    df["recipient_he_norm"] = df["recipient_he"].apply(norm_he)
    df["total_num"] = df["total"].apply(parse_total)

    # Identify distributors: buyers with 3+ different recipients
    buyer_to_recipients = defaultdict(set)
    for _, r in df.iterrows():
        if r["buyer_en_norm"] and r["recipient_he_norm"]:
            buyer_to_recipients[r["buyer_en_norm"]].add(r["recipient_he_norm"])
    distributors = {b for b, recipients in buyer_to_recipients.items()
                    if len(recipients) >= DISTRIBUTOR_MIN_RECIPIENTS}

    # Aggregate per recipient (customer)
    customers = []
    grouped = df.groupby("recipient_he_norm")
    for he_name, group in grouped:
        if not he_name or he_name == "Herbalife International of America, Inc. California, USA":
            continue
        unique_buyers = group["buyer_en_norm"].dropna().unique().tolist()
        unique_buyers = [b for b in unique_buyers if b]
        # Distinguish distributors from "self-buyers"
        ordered_via = sorted([b for b in unique_buyers if b in distributors])
        self_orders = sorted([b for b in unique_buyers if b not in distributors])
        customers.append({
            "canonical_he": he_name,
            "english_variants": sorted(unique_buyers),
            "ordered_via": ordered_via,
            "self_orders_en": self_orders,
            "order_count": int(len(group)),
            "total_spent": round(float(group["total_num"].sum()), 2),
            "is_distributor": he_name in distributors,  # rare — most distributors only have EN name
        })
    customers.sort(key=lambda c: -c["order_count"])

    # Hebrew fuzzy clusters (potential same-person variants)
    he_clusters = cluster_he_names([c["canonical_he"] for c in customers])
    he_cluster_lookup = {}
    for ci, cluster in enumerate(he_clusters):
        if len(cluster) >= 2:
            for name in cluster:
                he_cluster_lookup[name] = ci

    # Annotate each customer with cluster id (if any)
    for c in customers:
        c["cluster_id"] = he_cluster_lookup.get(c["canonical_he"])

    # Distributor summary — for the "מפיצים" tab
    distributor_summary = []
    for dist in sorted(distributors):
        recipients = sorted(buyer_to_recipients[dist])
        dist_orders = df[df["buyer_en_norm"] == dist]
        distributor_summary.append({
            "name_en": dist,
            "recipient_count": len(recipients),
            "order_count": int(len(dist_orders)),
            "total_facilitated": round(float(dist_orders["total_num"].sum()), 2),
        })
    distributor_summary.sort(key=lambda d: -d["order_count"])

    return {
        "customers": customers,
        "distributors": distributor_summary,
        "he_clusters": [c for c in he_clusters if len(c) >= 2],
        "stats": {
            "total_orders": int(len(df)),
            "unique_customers": len(customers),
            "distributors": len(distributor_summary),
            "fuzzy_dup_groups": len([c for c in he_clusters if len(c) >= 2]),
        },
    }


def html_escape(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;").replace("'", "&#39;"))


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>סקירת לקוחות — OrdersHistory</title>
<style>
  :root {
    --bg: #0d1117; --panel: #161b22; --border: #30363d; --text: #e6edf3;
    --muted: #8b949e; --accent: #58a6ff; --good: #46d369; --warn: #f0883e;
    --bad: #f85149; --pill: #21262d;
  }
  * { box-sizing: border-box; }
  body { font-family: -apple-system, "Segoe UI", Heebo, sans-serif; background: var(--bg);
         color: var(--text); padding: 24px; max-width: 1400px; margin: 0 auto; }
  header { display: flex; justify-content: space-between; align-items: center;
           border-bottom: 2px solid var(--border); padding-bottom: 12px; margin-bottom: 20px; }
  h1 { color: var(--accent); margin: 0; font-size: 24px; }
  .stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
           gap: 10px; margin-bottom: 20px; }
  .stat { background: var(--panel); padding: 14px; border-radius: 8px; text-align: center;
          border: 1px solid var(--border); }
  .stat .num { font-size: 24px; font-weight: 700; color: var(--accent); display: block; }
  .stat .label { font-size: 11px; color: var(--muted); text-transform: uppercase; letter-spacing: 1px; }
  .toolbar { background: var(--panel); padding: 12px 16px; border-radius: 8px; margin-bottom: 16px;
             display: flex; gap: 10px; flex-wrap: wrap; align-items: center; border: 1px solid var(--border); }
  .toolbar input { background: var(--bg); color: var(--text); border: 1px solid var(--border);
                   padding: 7px 12px; border-radius: 6px; font-size: 14px; flex: 1; min-width: 200px; }
  .toolbar button { background: var(--pill); color: var(--text); border: 1px solid var(--border);
                    padding: 7px 14px; border-radius: 6px; cursor: pointer; font-size: 13px; }
  .toolbar button:hover { background: var(--border); }
  .toolbar button.primary { background: var(--accent); border-color: var(--accent); color: #fff; }
  .toolbar select { background: var(--bg); color: var(--text); border: 1px solid var(--border);
                    padding: 7px 10px; border-radius: 6px; font-size: 13px; }
  .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 12px; }
  .card { background: var(--panel); padding: 12px 14px; border-radius: 8px; border: 1px solid var(--border);
          border-right-width: 4px; transition: transform 0.15s; }
  .card:hover { transform: translateY(-2px); }
  .card.merged { border-right-color: var(--good); background: rgba(70,211,105,0.06); }
  .card.flagged-distributor { border-right-color: var(--warn); }
  .card .name-he { font-size: 16px; font-weight: 700; margin-bottom: 2px; color: var(--text); }
  .card .name-en { font-size: 11px; color: var(--muted); margin-bottom: 8px; }
  .card .ordered-via { font-size: 13px; color: var(--accent); margin: 6px 0 4px;
                       padding: 4px 8px; background: rgba(88,166,255,0.10); border-radius: 4px; }
  .card .stats-row { display: flex; gap: 12px; font-size: 12px; color: var(--muted);
                     border-top: 1px solid var(--border); padding-top: 6px; margin-top: 6px; }
  .card .stats-row b { color: var(--text); font-weight: 600; }
  .card .actions { margin-top: 6px; display: flex; gap: 4px; }
  .card .actions button { font-size: 11px; padding: 3px 8px; background: var(--pill);
                          color: var(--muted); border: 1px solid var(--border); border-radius: 4px;
                          cursor: pointer; }
  .card .actions button:hover { color: var(--text); background: var(--border); }
  .card .actions button.active { background: var(--good); color: #fff; border-color: var(--good); }
  .cluster-link { font-size: 11px; color: var(--warn); margin-top: 4px;
                  background: rgba(240,136,62,0.10); padding: 3px 6px; border-radius: 4px;
                  display: inline-block; }
  .tab-bar { display: flex; gap: 4px; margin-bottom: 16px; border-bottom: 2px solid var(--border); }
  .tab-bar button { background: transparent; color: var(--muted); border: none; padding: 10px 18px;
                    cursor: pointer; font-size: 14px; border-bottom: 3px solid transparent;
                    margin-bottom: -2px; }
  .tab-bar button.active { color: var(--accent); border-bottom-color: var(--accent); font-weight: 600; }
  .tab-content { display: none; }
  .tab-content.active { display: block; }
  table { width: 100%; border-collapse: collapse; background: var(--panel); border-radius: 8px; overflow: hidden; }
  th { background: var(--bg); padding: 10px 12px; text-align: right; color: var(--muted); font-size: 12px;
       text-transform: uppercase; letter-spacing: 1px; border-bottom: 1px solid var(--border); }
  td { padding: 10px 12px; border-bottom: 1px solid var(--border); font-size: 14px; }
  tr:hover td { background: rgba(255,255,255,0.02); }
  .progress-pill { font-size: 12px; color: var(--muted); }
  .empty { text-align: center; padding: 40px; color: var(--muted); }
</style>
</head>
<body>

<header>
  <h1>סקירת לקוחות — OrdersHistory</h1>
  <span class="progress-pill" id="progressLabel">0 החלטות</span>
</header>

<div class="stats">__STATS_HTML__</div>

<div class="tab-bar">
  <button class="tab-btn active" data-tab="customers">לקוחות (__CUSTOMER_COUNT__)</button>
  <button class="tab-btn" data-tab="distributors">מפיצים (__DISTRIBUTOR_COUNT__)</button>
  <button class="tab-btn" data-tab="clusters">כפילויות חשודות (__CLUSTER_COUNT__)</button>
</div>

<div class="tab-content active" id="tab-customers">
  <div class="toolbar">
    <input type="search" id="searchBox" placeholder="חיפוש לפי שם...">
    <select id="filterSelect">
      <option value="all">כולם</option>
      <option value="via">רק שהוזמנו ע״י מפיץ</option>
      <option value="self">רק שהזמינו לעצמם</option>
      <option value="multi-en">עם מספר איותי אנגלית</option>
      <option value="cluster">בקבוצת כפילות חשודה</option>
    </select>
    <button onclick="exportDecisions()" class="primary">📥 ייצא JSON</button>
  </div>
  <div class="grid" id="customerGrid">__CUSTOMER_CARDS__</div>
</div>

<div class="tab-content" id="tab-distributors">
  <table>
    <thead>
      <tr><th>שם המפיץ (אנגלית)</th><th>הזמנות</th><th>נמענים</th><th>סה״כ ₪</th></tr>
    </thead>
    <tbody>__DISTRIBUTOR_ROWS__</tbody>
  </table>
</div>

<div class="tab-content" id="tab-clusters">
  <p style="color:var(--muted);font-size:13px;margin-bottom:12px;">
    קבוצות שמות עברית עם דמיון גבוה. כברירת מחדל סומנו כ"אותו אדם".
  </p>
  <div id="clusterList">__CLUSTER_LIST__</div>
</div>

<script>
const decisions = JSON.parse(localStorage.getItem('dedupe_decisions_v2') || '{}');

// Pre-fill default decisions: all clusters are "merged" by default per user feedback
__CLUSTER_DEFAULTS__

function decide(id, action) {
  decisions[id] = action;
  localStorage.setItem('dedupe_decisions_v2', JSON.stringify(decisions));
  refreshUI(id);
}

function refreshUI(id) {
  const el = document.querySelector(`[data-id="${id}"]`);
  if (el) {
    el.classList.toggle('merged', decisions[id] === 'merge');
    el.querySelectorAll('button[data-action]').forEach(b => {
      b.classList.toggle('active', b.dataset.action === decisions[id]);
    });
  }
  updateProgress();
}

function updateProgress() {
  document.getElementById('progressLabel').textContent =
    `${Object.keys(decisions).length} החלטות נשמרו`;
}

function exportDecisions() {
  const blob = new Blob([JSON.stringify(decisions, null, 2)], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url; a.download = 'dedupe_decisions.json'; a.click();
  URL.revokeObjectURL(url);
}

// Tab switching
document.querySelectorAll('.tab-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
    document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
    btn.classList.add('active');
    document.getElementById('tab-' + btn.dataset.tab).classList.add('active');
  });
});

// Search + filter
function applyFilter() {
  const q = document.getElementById('searchBox').value.trim().toLowerCase();
  const filter = document.getElementById('filterSelect').value;
  document.querySelectorAll('#customerGrid .card').forEach(card => {
    const text = card.textContent.toLowerCase();
    const matchesSearch = !q || text.includes(q);
    let matchesFilter = true;
    if (filter === 'via')      matchesFilter = card.dataset.viaCount > 0;
    else if (filter === 'self') matchesFilter = card.dataset.selfCount > 0 && card.dataset.viaCount == 0;
    else if (filter === 'multi-en') matchesFilter = card.dataset.enCount > 1;
    else if (filter === 'cluster')  matchesFilter = card.dataset.clusterId !== '';
    card.style.display = (matchesSearch && matchesFilter) ? '' : 'none';
  });
}
document.getElementById('searchBox').addEventListener('input', applyFilter);
document.getElementById('filterSelect').addEventListener('change', applyFilter);

// Restore decisions visually on load
window.addEventListener('DOMContentLoaded', () => {
  Object.keys(decisions).forEach(id => refreshUI(id));
  updateProgress();
});
</script>
</body>
</html>"""


def render_customer_card(c):
    cid = f"cust_{c['canonical_he']}"
    via = ""
    if c["ordered_via"]:
        via_names = ", ".join(c["ordered_via"])
        via = f'<div class="ordered-via">📦 הוזמן ע״י: {html_escape(via_names)}</div>'
    en_name = ""
    if c["english_variants"]:
        # Show English if it differs from "ordered_via" buyers (i.e., they bought themselves too)
        non_dist_en = [e for e in c["english_variants"] if e in c["self_orders_en"]]
        if non_dist_en:
            en_name = f'<div class="name-en">EN: {html_escape(", ".join(non_dist_en))}</div>'
    cluster_link = ""
    if c["cluster_id"] is not None:
        cluster_link = '<span class="cluster-link">⚠ כפילות חשודה — בדוק לשונית "כפילויות"</span>'

    via_count = len(c["ordered_via"])
    self_count = len(c["self_orders_en"])
    en_count = len(c["english_variants"])
    cluster_id = c["cluster_id"] if c["cluster_id"] is not None else ""

    return f'''<div class="card" data-id="{html_escape(cid)}"
              data-via-count="{via_count}" data-self-count="{self_count}"
              data-en-count="{en_count}" data-cluster-id="{cluster_id}">
  <div class="name-he">{html_escape(c["canonical_he"])}</div>
  {en_name}
  {via}
  {cluster_link}
  <div class="stats-row">
    <span><b>{c["order_count"]}</b> הזמנות</span>
    <span><b>{c["total_spent"]:,.0f}</b> ₪</span>
  </div>
</div>'''


def render_distributor_row(d):
    return f'''<tr>
  <td><strong>{html_escape(d["name_en"])}</strong></td>
  <td>{d["order_count"]}</td>
  <td>{d["recipient_count"]}</td>
  <td>{d["total_facilitated"]:,.0f}</td>
</tr>'''


def render_cluster_card(idx, names):
    cid = f"cluster_{idx}"
    pills = "".join(
        f'<span style="background:var(--pill);padding:4px 10px;border-radius:14px;font-size:13px;margin:2px;display:inline-block;">{html_escape(n)}</span>'
        for n in names
    )
    return f'''<div class="card" data-id="{cid}" style="margin-bottom:8px;">
  <div style="margin-bottom:6px;">{pills}</div>
  <div class="actions">
    <button data-action="merge" onclick="decide('{cid}', 'merge')">✓ אותו אדם</button>
    <button data-action="keep" onclick="decide('{cid}', 'keep')">✕ אנשים נפרדים</button>
  </div>
</div>'''


def main():
    print(f"Loading {XLSX_PATH}...")
    df = load_orders()
    print(f"Loaded {len(df)} orders")

    data = build_customer_view(df)
    s = data["stats"]
    print(f"Stats: {s}")

    OUT_DATA_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2))
    print(f"Wrote {OUT_DATA_JSON}")

    stats_html = "".join(
        f'<div class="stat"><span class="num">{v:,}</span><span class="label">{k.replace("_", " ")}</span></div>'
        for k, v in s.items()
    )
    customer_cards = "\n".join(render_customer_card(c) for c in data["customers"])
    distributor_rows = "\n".join(render_distributor_row(d) for d in data["distributors"])

    cluster_list_html = "\n".join(
        render_cluster_card(i, names) for i, names in enumerate(data["he_clusters"])
    ) or '<p class="empty">אין כפילויות חשודות</p>'

    # Pre-fill all clusters as "merge" (per user feedback: all variations are same person)
    cluster_defaults_js = "\n".join(
        f"if (decisions['cluster_{i}'] === undefined) decisions['cluster_{i}'] = 'merge';"
        for i in range(len(data["he_clusters"]))
    )
    if cluster_defaults_js:
        cluster_defaults_js += "\nlocalStorage.setItem('dedupe_decisions_v2', JSON.stringify(decisions));"

    html = (HTML_TEMPLATE
            .replace("__STATS_HTML__", stats_html)
            .replace("__CUSTOMER_COUNT__", str(len(data["customers"])))
            .replace("__DISTRIBUTOR_COUNT__", str(len(data["distributors"])))
            .replace("__CLUSTER_COUNT__", str(len(data["he_clusters"])))
            .replace("__CUSTOMER_CARDS__", customer_cards)
            .replace("__DISTRIBUTOR_ROWS__", distributor_rows)
            .replace("__CLUSTER_LIST__", cluster_list_html)
            .replace("__CLUSTER_DEFAULTS__", cluster_defaults_js))

    OUT_HTML.write_text(html, encoding="utf-8")
    print(f"Wrote {OUT_HTML}")
    print(f"Open: file://{OUT_HTML.resolve()}")


if __name__ == "__main__":
    main()
