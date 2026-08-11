#!/usr/bin/env python3
"""Generate the CSV deliverables in data/ from the canonical assortment module.

Usage:  python scripts/build_data.py
"""

import csv
import os

import assortment_data as A

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(os.path.dirname(HERE), "data")

SKU_COLUMNS = [
    "sku_id", "family_code", "family", "tier", "territory", "category",
    "piece_type", "retail", "landed_cogs", "margin_pct", "margin_dollars",
    "arm", "back", "seat", "suspension", "frame", "joinery", "legs",
    "fabric", "rub_count", "mechanism", "covers",
    "width_in", "depth_in", "height_in", "seat_depth_in", "seat_height_in",
]


def write_sku_master():
    rows = A.enriched()
    path = os.path.join(DATA, "sku_master.csv")
    with open(path, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=SKU_COLUMNS)
        w.writeheader()
        w.writerows(rows)
    return path, len(rows)


def write_frame_families():
    path = os.path.join(DATA, "frame_families.csv")
    cols = [
        "family_code", "family", "tier", "territory", "category", "sku_count",
        "retail_low", "retail_high", "margin_target_pct", "covers",
        "arm", "back", "seat", "suspension", "frame", "joinery", "legs",
        "fabric", "rub_count", "mechanism", "design_note", "rsa_story",
    ]
    by_fam = {}
    for r in A.enriched():
        by_fam.setdefault(r["family_code"], []).append(r)

    with open(path, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        for code, fam in A.FAMILIES.items():
            skus = by_fam[code]
            retails = [s["retail"] for s in skus]
            w.writerow({
                "family_code": code,
                "family": fam["name"],
                "tier": fam["tier"],
                "territory": fam["territory"],
                "category": fam["category"],
                "sku_count": len(skus),
                "retail_low": min(retails),
                "retail_high": max(retails),
                "margin_target_pct": fam["margin_target"],
                "covers": fam["covers"],
                "arm": fam["arm"],
                "back": fam["back"],
                "seat": fam["seat"],
                "suspension": fam["suspension"],
                "frame": fam["frame"],
                "joinery": fam["joinery"],
                "legs": fam["legs"],
                "fabric": fam["fabric"],
                "rub_count": fam["rub_count"],
                "mechanism": fam.get("mechanism", ""),
                "design_note": " ".join(fam["design_note"].split()),
                "rsa_story": " ".join(fam["rsa_story"].split()),
            })
    return path, len(A.FAMILIES)


def write_cover_matrix():
    """Cover program per family, plus the orderable-SKU count it implies."""
    path = os.path.join(DATA, "cover_matrix.csv")
    cols = [
        "family_code", "family", "tier", "category", "pieces", "covers",
        "cover_mix", "fabric_program", "rub_count", "orderable_skus",
    ]
    by_fam = {}
    for r in A.enriched():
        by_fam.setdefault(r["family_code"], []).append(r)

    with open(path, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        for code, fam in A.FAMILIES.items():
            pieces = len(by_fam[code])
            w.writerow({
                "family_code": code,
                "family": fam["name"],
                "tier": fam["tier"],
                "category": fam["category"],
                "pieces": pieces,
                "covers": fam["covers"],
                "cover_mix": fam["cover_mix"],
                "fabric_program": fam["fabric"],
                "rub_count": fam["rub_count"],
                "orderable_skus": pieces * fam["covers"],
            })
    return path, len(A.FAMILIES)


def write_lanes():
    path = os.path.join(DATA, "tradeup_lanes.csv")
    cols = ["lane", "step", "sku_id", "family", "tier", "retail",
            "step_up_pct", "margin_pct"]
    index = {r["sku_id"]: r for r in A.enriched()}
    with open(path, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        for lane, skus in A.LANES.items():
            prev = None
            for i, sid in enumerate(skus, start=1):
                r = index[sid]
                step = "" if prev is None else round(
                    100.0 * (r["retail"] - prev) / prev, 1)
                w.writerow({
                    "lane": lane,
                    "step": i,
                    "sku_id": sid,
                    "family": r["family"],
                    "tier": r["tier"],
                    "retail": r["retail"],
                    "step_up_pct": step,
                    "margin_pct": r["margin_pct"],
                })
                prev = r["retail"]
    return path, sum(len(v) for v in A.LANES.values())


def main():
    os.makedirs(DATA, exist_ok=True)
    for fn in (write_sku_master, write_frame_families,
               write_cover_matrix, write_lanes):
        path, n = fn()
        print(f"wrote {os.path.relpath(path):-<40} {n} rows")


if __name__ == "__main__":
    main()
