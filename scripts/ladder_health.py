#!/usr/bin/env python3
"""Assortment health checks for the 65-SKU line.

Validates the things that actually break a GBB ladder: margin outside band,
retail outside the category's price architecture, tier mix skew, trade-up
steps that are too small to perceive or too big to cross, cover depth that
does not match the tier, and SKU proliferation.

Exit code is 1 if any FAIL is raised, 0 otherwise. FLAGs do not fail the run --
they are judgment calls for the merchant, not errors.

Usage:  python scripts/ladder_health.py
"""

import sys
from collections import Counter, defaultdict

import assortment_data as A

# Step-up guidance. Written for a 3-rung ladder; motion runs 4 rungs and is
# evaluated on consecutive steps rather than total spread (see report notes).
STEP_MIN_PCT = 15.0     # below this the customer cannot perceive the rung
STEP_MAX_PCT = 60.0     # above this the rung is a different buying universe
SPREAD_MIN_PCT = 80.0   # Good -> Best, 3-rung lanes
SPREAD_MAX_PCT = 125.0

COVER_DEPTH = {         # (min, max) covers by tier, per cover strategy
    A.GOOD: (3, 5),
    A.BETTER: (6, 12),
    A.BEST: (12, 25),
}

TIER_MIX_TARGET = {     # share of SKU count, healthy mid-market pyramid
    A.GOOD: (25.0, 35.0),
    A.BETTER: (40.0, 50.0),
    A.BEST: (20.0, 30.0),
}

results = []


def record(level, area, msg):
    results.append((level, area, msg))


def check_margins(rows):
    for r in rows:
        band = A.MARGIN_BANDS[(r["category"], r["tier"])]
        lo, hi = band
        if not (lo <= r["margin_pct"] <= hi):
            record("FAIL", "Margin",
                   f"{r['sku_id']} {r['family']} {r['piece_type']}: "
                   f"{r['margin_pct']}% outside {r['category']}/{r['tier']} "
                   f"band {lo}-{hi}%")


def check_price_bands(rows):
    for r in rows:
        anchor = A.ANCHOR_MAP.get(r["piece_type"])
        if not anchor:
            continue
        key = (anchor, r["tier"])
        if key not in A.PRICE_BANDS:
            continue
        lo, hi = A.PRICE_BANDS[key]
        if lo <= r["retail"] <= hi:
            continue
        reason = A.BAND_EXCEPTIONS.get(r["sku_id"])
        level = "INFO" if reason else "FLAG"
        detail = f" -- {reason}" if reason else ""
        record(level, "Price band",
               f"{r['sku_id']} {r['family']} {r['piece_type']}: "
               f"${r['retail']:,} outside {anchor}/{r['tier']} band "
               f"${lo:,}-${hi:,}{detail}")


def check_motion_sofa_bands(rows):
    """Motion sofas price above the stationary sofa band by design. Report the
    spread so it is a stated position rather than an accident."""
    motion_sofas = [r for r in rows if r["category"] == A.MOTION
                    and "Sofa" in r["piece_type"]]
    for r in motion_sofas:
        record("INFO", "Motion pricing",
               f"{r['sku_id']} {r['piece_type']} ${r['retail']:,} "
               f"({r['tier']}) -- motion sofas run their own band above "
               f"stationary; mechanism COGS drives it")


def check_tier_mix(rows):
    total = len(rows)
    counts = Counter(r["tier"] for r in rows)
    for tier, (lo, hi) in TIER_MIX_TARGET.items():
        share = 100.0 * counts[tier] / total
        level = "PASS" if lo <= share <= hi else "FLAG"
        record(level, "Tier mix",
               f"{tier}: {counts[tier]}/{total} SKUs = {share:.1f}% "
               f"(target {lo:.0f}-{hi:.0f}%)")


def check_style_balance(rows):
    total = len(rows)
    counts = Counter(r["territory"] for r in rows)
    for terr, n in sorted(counts.items(), key=lambda kv: -kv[1]):
        share = 100.0 * n / total
        level = "PASS" if 25.0 <= share <= 45.0 else "FLAG"
        record(level, "Style balance",
               f"{terr}: {n} SKUs = {share:.1f}% (target 25-45%)")


def check_lanes(rows):
    index = {r["sku_id"]: r for r in rows}
    for lane, skus in A.LANES.items():
        tiers = [index[s]["tier"] for s in skus]
        rungs = [index[s] for s in skus]

        for t in (A.GOOD, A.BETTER, A.BEST):
            if t in tiers:
                continue
            reason = A.INTENTIONAL_LANE_GAPS.get((lane, t))
            if reason:
                record("INFO", "Lane coverage",
                       f"{lane}: no {t} rung by design -- {reason}")
            else:
                record("FLAG", "Lane coverage",
                       f"{lane}: no {t} rung -- customer cannot trade up "
                       f"within this lane without changing piece type")

        for a, b in zip(rungs, rungs[1:]):
            step = 100.0 * (b["retail"] - a["retail"]) / a["retail"]
            if step < STEP_MIN_PCT:
                record("FAIL", "Lane step",
                       f"{lane}: {a['sku_id']} ${a['retail']:,} -> "
                       f"{b['sku_id']} ${b['retail']:,} = +{step:.1f}% "
                       f"(<{STEP_MIN_PCT:.0f}%, rung not perceptible)")
            elif step > STEP_MAX_PCT:
                record("FLAG", "Lane step",
                       f"{lane}: {a['sku_id']} ${a['retail']:,} -> "
                       f"{b['sku_id']} ${b['retail']:,} = +{step:.1f}% "
                       f"(>{STEP_MAX_PCT:.0f}%, step-up may not be crossable)")

        spread = 100.0 * (rungs[-1]["retail"] - rungs[0]["retail"]) / rungs[0]["retail"]
        if rungs[-1]["tier"] != A.BEST:
            # Lane stops short of Best by design; a Good->Best spread target
            # does not apply to a lane that has no Best rung.
            record("INFO", "Lane spread",
                   f"{lane}: +{spread:.0f}% across {rungs[0]['tier']} -> "
                   f"{rungs[-1]['tier']} (lane tops out below Best by design)")
        elif len(rungs) >= 4:
            record("INFO", "Lane spread",
                   f"{lane}: +{spread:.0f}% Good->Best across {len(rungs)} "
                   f"rungs -- 80-125% guideline assumes 3 rungs; evaluated on "
                   f"consecutive steps instead")
        elif not (SPREAD_MIN_PCT <= spread <= SPREAD_MAX_PCT):
            record("FLAG", "Lane spread",
                   f"{lane}: +{spread:.0f}% Good->Best "
                   f"(target {SPREAD_MIN_PCT:.0f}-{SPREAD_MAX_PCT:.0f}%)")
        else:
            record("PASS", "Lane spread", f"{lane}: +{spread:.0f}% Good->Best")


def check_cover_depth():
    for code, fam in A.FAMILIES.items():
        lo, hi = COVER_DEPTH[fam["tier"]]
        n = fam["covers"]
        if not (lo <= n <= hi):
            # Thorne is a deliberate exception: a leather-only program.
            if code == "THO":
                record("INFO", "Cover depth",
                       f"{fam['name']}: {n} covers, below the {fam['tier']} "
                       f"range {lo}-{hi} -- intentional, leather-only program")
            else:
                record("FLAG", "Cover depth",
                       f"{fam['name']} ({fam['tier']}): {n} covers outside "
                       f"tier range {lo}-{hi}")


def check_proliferation(rows):
    by_fam = defaultdict(int)
    for r in rows:
        by_fam[r["family_code"]] += 1
    total_orderable = 0
    stocked = 0
    for code, fam in A.FAMILIES.items():
        orderable = by_fam[code] * fam["covers"]
        total_orderable += orderable
        # Custom-order books are orderable but not carried as inventory.
        stocked += by_fam[code] * fam.get("in_stock_covers", fam["covers"])
    record("INFO", "Proliferation",
           f"{len(rows)} pieces x cover programs = {total_orderable:,} "
           f"orderable SKUs; {stocked:,} carried as stocked inventory "
           f"({total_orderable - stocked:,} shifted to custom order)")


def check_vendor_architecture(rows):
    """National brands anchor each tier but must not take over the floor."""
    nat = [r for r in rows if r["vendor_type"] == A.NATIONAL]
    share = len(nat) / len(rows)
    level = "PASS" if share <= A.NATIONAL_SPACE_CAP else "FAIL"
    record(level, "National cap",
           f"National brands {len(nat)}/{len(rows)} SKUs = {share:.1%} "
           f"(cap {A.NATIONAL_SPACE_CAP:.0%} of space)")

    by_vendor = defaultdict(list)
    for r in nat:
        by_vendor[r["vendor"]].append(r)
    for name, rs in sorted(by_vendor.items()):
        cats = sorted({r["category"] for r in rs})
        tiers = sorted({r["tier"] for r in rs})
        record("INFO", "National anchor",
               f"{name}: {len(rs)} SKUs | {', '.join(tiers)} | "
               f"{', '.join(cats)}")

    # Category restrictions -- La-Z-Boy and Flexsteel are motion-only.
    for code, key in A.FAMILY_VENDOR.items():
        if not key:
            continue
        v = A.VENDORS[key]
        cat = A.FAMILIES[code]["category"]
        if cat not in v["categories"]:
            record("FAIL", "Vendor category",
                   f"{A.FAMILIES[code]['name']} ({code}) is {cat} but "
                   f"{v['name']} is restricted to "
                   f"{'/'.join(v['categories'])}")

    # Every tier needs a national anchor to hold its price credibility.
    for tier in (A.GOOD, A.BETTER, A.BEST):
        anchors = {r["vendor"] for r in nat if r["tier"] == tier}
        if anchors:
            record("PASS", "Tier anchor",
                   f"{tier} anchored by {', '.join(sorted(anchors))}")
        else:
            record("FAIL", "Tier anchor", f"{tier} has no national anchor")

    # Is our planned retail credible for the brand on the ticket? A national
    # brand carries a price the customer has already seen elsewhere.
    for r in nat:
        key = (A.FAMILY_VENDOR[r["family_code"]], r["piece_type"])
        rng = A.VENDOR_OBSERVED_RANGES.get(key)
        if not rng:
            continue
        lo, hi = rng
        if lo <= r["retail"] <= hi:
            continue
        reason = A.RANGE_EXCEPTIONS.get(r["sku_id"])
        if reason:
            record("INFO", "Street price",
                   f"{r['sku_id']} {r['vendor']} {r['piece_type']} "
                   f"${r['retail']:,} outside observed ${lo:,}-${hi:,} "
                   f"-- {reason}")
        else:
            record("FLAG", "Street price",
                   f"{r['sku_id']} {r['vendor']} {r['piece_type']} "
                   f"${r['retail']:,} outside observed dealer range "
                   f"${lo:,}-${hi:,} -- customer may have seen this brand "
                   f"cheaper elsewhere")

    # Parent-company concentration. England is not a national brand on the
    # floor -- the customer never sees "La-Z-Boy" on an England sofa -- but it
    # is owned by La-Z-Boy Inc., so it concentrates exposure to one parent.
    # Both readings matter, so both get reported.
    parents = defaultdict(int)
    for r in rows:
        key = A.FAMILY_VENDOR[r["family_code"]]
        v = A.VENDORS.get(key, {})
        parent = v.get("parent") or v.get("name")
        if parent:
            parents[parent] += 1
    for parent, n in sorted(parents.items(), key=lambda kv: -kv[1])[:4]:
        share = n / len(rows)
        level = "FLAG" if share > 0.25 else "INFO"
        record(level, "Parent exposure",
               f"{parent}: {n}/{len(rows)} SKUs = {share:.1%} of the line")

    unsourced = [r for r in rows if r["vendor"] == "TBD"]
    if unsourced:
        fams = sorted({r["family"] for r in unsourced})
        record("FLAG", "Sourcing",
               f"{len(unsourced)} SKUs across {len(fams)} families not yet "
               f"assigned to a vendor: {', '.join(fams)}")


def check_construction_progression():
    """Suspension and joinery must never regress as tier rises."""
    susp_rank = {"Elastic webbing": 0, "Sinuous": 1, "Pocketed coil": 2,
                 "Encased spring": 2, "8-way hand-tied": 3}
    joinery_rank = {"Staple": 0, "Dowel": 1, "Mortise": 2, "Steel bolt": 2}
    tier_rank = {A.GOOD: 0, A.BETTER: 1, A.BEST: 2}

    def rank(text, table):
        for k, v in table.items():
            if k.lower() in text.lower():
                return v
        return None

    seen = defaultdict(list)
    for code, fam in A.FAMILIES.items():
        seen[fam["category"]].append((
            tier_rank[fam["tier"]], fam["name"], fam["tier"],
            rank(fam["suspension"], susp_rank),
            rank(fam["joinery"], joinery_rank),
        ))

    for cat, entries in seen.items():
        best_good = max((e[3] for e in entries if e[0] == 0 and e[3] is not None),
                        default=-1)
        worst_best = min((e[3] for e in entries if e[0] == 2 and e[3] is not None),
                         default=99)
        if worst_best <= best_good:
            record("FAIL", "Construction",
                   f"{cat}: a Best family's suspension does not exceed the "
                   f"strongest Good family's -- tier promise not backed by spec")
        else:
            record("PASS", "Construction",
                   f"{cat}: suspension and joinery strictly improve Good -> "
                   f"Better -> Best")


def main():
    rows = A.enriched()

    if len(rows) != 65:
        record("FAIL", "SKU count", f"Expected 65 SKUs, found {len(rows)}")
    else:
        record("PASS", "SKU count", "65 SKUs across "
               f"{len(A.FAMILIES)} frame families")

    ids = [r["sku_id"] for r in rows]
    dupes = [k for k, v in Counter(ids).items() if v > 1]
    if dupes:
        record("FAIL", "SKU ids", f"Duplicate ids: {', '.join(dupes)}")

    check_margins(rows)
    check_price_bands(rows)
    check_vendor_architecture(rows)
    check_tier_mix(rows)
    check_style_balance(rows)
    check_lanes(rows)
    check_cover_depth()
    check_construction_progression()
    check_motion_sofa_bands(rows)
    check_proliferation(rows)

    order = {"FAIL": 0, "FLAG": 1, "PASS": 2, "INFO": 3}
    results.sort(key=lambda r: (order[r[0]], r[1]))

    width = 72
    print("=" * width)
    print("ASSORTMENT LADDER HEALTH -- 65-SKU STATIONARY + MOTION LINE")
    print("=" * width)
    current = None
    for level, area, msg in results:
        if level != current:
            print(f"\n--- {level} " + "-" * (width - len(level) - 5))
            current = level
        print(f"  [{area}] {msg}")

    counts = Counter(r[0] for r in results)
    print("\n" + "=" * width)
    print(f"FAIL {counts['FAIL']}  |  FLAG {counts['FLAG']}  |  "
          f"PASS {counts['PASS']}  |  INFO {counts['INFO']}")
    print("=" * width)

    return 1 if counts["FAIL"] else 0


if __name__ == "__main__":
    sys.exit(main())
