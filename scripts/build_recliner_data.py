#!/usr/bin/env python3
"""Generate data/recliner_*.csv from scripts/recliner_data.py.

Do not hand-edit the generated files -- change the config module and rerun.

Usage:  python scripts/build_recliner_data.py
"""

import csv
import os
from collections import Counter, defaultdict

import recliner_data as D
import recliner_rules as R

DATA = os.path.join(os.path.dirname(__file__), "..", "data")


def write(name, fields, rows):
    path = os.path.join(DATA, name)
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)
    print(f"  {name:34s} {len(rows):3d} rows")


def build_slots(rows):
    """The 52-slot grid: what occupies each governed slot."""
    out = []
    for r in sorted((x for x in rows if x["slot_type"] == "MDL"),
                    key=lambda x: x["slot_no"]):
        out.append({
            "slot_no": r["slot_no"], "category": r["category"],
            "tier": r["tier"], "brand": r["brand"], "model": r["model"],
            "retail": r["retail"], "customer_job": r["customer_job"],
            "trade_up_feature": r["trade_up_feature"],
        })
    return out


def build_lanes(rows):
    """Trade-up lanes: the routes an RSA actually walks a customer along."""
    lanes = [
        ("Price access", "Cheap and now", "The $299 ad to a chair that earns its slot"),
        ("First chair", "First real chair", "New household, first non-hand-me-down"),
        ("Core comfort", "My chair", "The volume engine -- manual to power"),
        ("Small space", "Will it fit", "Wall-saver and hi-leg, apartment scale"),
        ("Family proof", "Survive my life", "Cover-led: performance fabric to leather"),
        ("Under-35 design", "Not a recliner", "Silhouette-led: hi-leg, swivel glider"),
        ("Accommodation", "Built my size", "Big and tall, cuddler, oversized"),
        ("Aging in place", "Easier to stand", "The parallel lift ladder"),
        ("Wellness / halo", "Does everything", "Tech, leather grade, massage, zero-g"),
    ]
    out = []
    for lane, job, mission in lanes:
        members = sorted((r for r in rows
                          if r["slot_type"] == "MDL" and r["customer_job"] == job),
                         key=lambda r: r["retail"])
        if not members:
            continue
        out.append({
            "lane": lane, "customer_job": job, "mission": mission,
            "slots": len(members),
            "entry_retail": members[0]["retail"],
            "entry_model": f"{members[0]['brand']} {members[0]['model']}",
            "top_retail": members[-1]["retail"],
            "top_model": f"{members[-1]['brand']} {members[-1]['model']}",
            "spread_pct": round(
                (members[-1]["retail"] / members[0]["retail"] - 1) * 100, 1),
            "reveals": " -> ".join(dict.fromkeys(m["trade_up_feature"]
                                                 for m in members)),
        })
    return out


def build_colors(rows):
    """70/20/10 by colour tier, and where each tier is permitted."""
    counts = Counter(r["color_tier"] for r in rows)
    total = len(rows)
    desc = {
        "Anchor": "High-velocity neutrals: greys, charcoals, greiges, taupes",
        "Bridge": "Textures and earth tones: cognac, walnut, olive, muted navy",
        "Accelerator": "Statement colours -- Good and Best tiers only",
    }
    out = []
    for tier, target in R.COLOR_TIERS.items():
        got = counts.get(tier, 0)
        out.append({
            "color_tier": tier, "description": desc[tier],
            "target_pct": f"{target*100:.0f}%",
            "actual_skus": got,
            "actual_pct": f"{got/total*100:.1f}%",
            "permitted_tiers": "/".join(R.ACCELERATOR_ALLOWED_TIERS)
                               if tier == "Accelerator" else "All",
        })
    return out


def main():
    rows = D.rows()
    print(f"Building from {len(rows)} SKUs...")
    write("recliner_sku_master.csv", D.FIELDS, rows)
    write("recliner_slots.csv",
          ("slot_no", "category", "tier", "brand", "model", "retail",
           "customer_job", "trade_up_feature"), build_slots(rows))
    write("recliner_tradeup_lanes.csv",
          ("lane", "customer_job", "mission", "slots", "entry_retail",
           "entry_model", "top_retail", "top_model", "spread_pct", "reveals"),
          build_lanes(rows))
    write("recliner_color_matrix.csv",
          ("color_tier", "description", "target_pct", "actual_skus",
           "actual_pct", "permitted_tiers"), build_colors(rows))
    print("Done. Now run: python scripts/recliner_health.py")


if __name__ == "__main__":
    main()
