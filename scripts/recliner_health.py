#!/usr/bin/env python3
"""Assortment health checks for the 65-SKU Slumberland recliner gallery.

Validates the assortment against scripts/recliner_rules.py, which encodes the
Slumberland Category Architecture. A FAIL means the floor breaks a governed
constraint. A FLAG is a merchant judgment call, not an error.

Exit code is 1 if any FAIL is raised, 0 otherwise.

Usage:  python scripts/recliner_health.py
"""

import csv
import os
import sys
from collections import Counter, defaultdict

import recliner_rules as R

DATA = os.path.join(os.path.dirname(__file__), "..", "data")
SKU_FILE = os.path.join(DATA, "recliner_sku_master.csv")

results = []


def record(level, area, msg):
    results.append((level, area, msg))


def load():
    with open(SKU_FILE, newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    for r in rows:
        r["retail"] = int(r["retail"])
        r["margin_pct"] = float(r["margin_pct"]) if r["margin_pct"] else 0.0
    return rows


# --- Structure ---------------------------------------------------------------

def check_counts(rows):
    """65 = 52 MDL + 13 off-slot. This is conflict C-001 resolved structurally;
    if it drifts, the whole slot-vs-SKU distinction has collapsed."""
    if len(rows) != R.TOTAL_FLOORED_SKUS:
        record("FAIL", "SKU count",
               f"Expected {R.TOTAL_FLOORED_SKUS} floored SKUs, found {len(rows)}")
    else:
        record("PASS", "SKU count", f"{R.TOTAL_FLOORED_SKUS} floored SKUs")

    mdl = [r for r in rows if r["slot_type"] == "MDL"]
    off = [r for r in rows if r["slot_type"] == "Off-slot"]

    if len(mdl) != R.MDL_SLOTS:
        record("FAIL", "Slot count",
               f"Expected {R.MDL_SLOTS} MDL slots (BIC commitment), found {len(mdl)}")
    else:
        record("PASS", "Slot count",
               f"{R.MDL_SLOTS} MDL slots -- matches BIC commitment "
               f"(prior observed state was {R.OBSERVED_PRIOR_MDL_SLOTS}, "
               f"{R.SLOT_TRANSITION_GAP} in transition)")

    if len(off) != R.OFF_SLOT_SKUS:
        record("FAIL", "Off-slot count",
               f"Expected {R.OFF_SLOT_SKUS} off-slot SKUs, found {len(off)}")
    else:
        record("PASS", "Off-slot count",
               f"{R.OFF_SLOT_SKUS} off-slot SKUs (special buys / promo / "
               f"quick-ship) -- excluded from slot count per matrix definition")

    lift = [r for r in mdl if r["category"] == "Lift"]
    rec = [r for r in mdl if r["category"] == "Recliner"]
    if len(lift) != R.LIFT_MDL_SLOTS:
        record("FAIL", "Lift slots",
               f"Expected {R.LIFT_MDL_SLOTS} lift slots, found {len(lift)}")
    else:
        record("PASS", "Lift slots",
               f"{R.LIFT_MDL_SLOTS} lift slots on a parallel ladder "
               f"(lift is +18.4% YoY vs +4.5% base)")
    if len(rec) != R.RECLINER_MDL_SLOTS:
        record("FAIL", "Recliner slots",
               f"Expected {R.RECLINER_MDL_SLOTS} governed recliner slots, "
               f"found {len(rec)}")

    dupes = [k for k, v in Counter(r["sku_id"] for r in rows).items() if v > 1]
    if dupes:
        record("FAIL", "SKU ids", f"Duplicate ids: {', '.join(dupes)}")

    slots = [r["slot_no"] for r in mdl if r["slot_no"]]
    sdupes = [k for k, v in Counter(slots).items() if v > 1]
    if sdupes:
        record("FAIL", "Slot ids", f"Duplicate slot numbers: {', '.join(sdupes)}")


# --- Tiers -------------------------------------------------------------------

def check_price_bands(rows):
    for r in rows:
        lo, hi = R.PRICE_BANDS[r["tier"]]
        if not (lo <= r["retail"] <= hi):
            record("FAIL", "Price band",
                   f"{r['sku_id']} {r['brand']} {r['model']}: ${r['retail']:,} "
                   f"outside {r['tier']} band ${lo:,}-${hi:,}")
    over = [r for r in rows if r["retail"] > R.CEILING]
    if over:
        for r in over:
            record("FAIL", "Ceiling",
                   f"{r['sku_id']} ${r['retail']:,} exceeds ${R.CEILING:,} ceiling")
    else:
        record("PASS", "Ceiling", f"No SKU above ${R.CEILING:,}")


def check_gbb_mix(rows):
    """GBB is governed on RECLINER slots only. Folding lift in would inflate
    Best and misstate the mix -- conflict C-013."""
    rec = [r for r in rows if r["slot_type"] == "MDL" and r["category"] == "Recliner"]
    counts = Counter(r["tier"] for r in rec)
    for tier, target in R.TARGET_SLOTS.items():
        got = counts.get(tier, 0)
        if abs(got - target) > R.SLOT_TOLERANCE:
            record("FAIL", "GBB mix",
                   f"{tier}: {got} slots vs target {target} "
                   f"(+/-{R.SLOT_TOLERANCE}) on {len(rec)} recliner slots")
        else:
            pct = got / len(rec) * 100 if rec else 0
            record("PASS", "GBB mix",
                   f"{tier}: {got} slots ({pct:.0f}%) vs target {target} "
                   f"({R.TARGET_MDL_SHARE[tier]*100:.0f}%)")

    # Reported, never governed.
    allm = [r for r in rows if r["slot_type"] == "MDL"]
    blended = Counter(r["tier"] for r in allm)
    record("INFO", "GBB mix",
           "Blended incl. lift (reported, not governed): "
           + ", ".join(f"{t} {blended.get(t,0)}" for t in
                       (R.GOOD, R.BETTER, R.BEST)))


# --- Vendors -----------------------------------------------------------------

def check_vendors(rows):
    """Recliners are national-brand-LED. The 30%-of-floor national cap in
    assortment_data.py is a stationary premise and does not apply -- C-014."""
    mdl = [r for r in rows if r["slot_type"] == "MDL"]
    counts = Counter(r["brand"] for r in mdl)
    lzb = counts.get("La-Z-Boy", 0)
    pct = lzb / len(mdl) * 100 if mdl else 0

    if lzb < R.LAZBOY_MIN_SLOTS:
        record("FAIL", "Vendor",
               f"La-Z-Boy {lzb} slots ({pct:.0f}%) below floor of "
               f"{R.LAZBOY_MIN_SLOTS} -- BIC commitment is "
               f"{R.LAZBOY_SLOT_SHARE*100:.0f}%")
    elif lzb != R.LAZBOY_TARGET_SLOTS:
        record("FLAG", "Vendor",
               f"La-Z-Boy {lzb} slots ({pct:.0f}%) vs target "
               f"{R.LAZBOY_TARGET_SLOTS} ({R.LAZBOY_SLOT_SHARE*100:.0f}%)")
    else:
        record("PASS", "Vendor",
               f"La-Z-Boy {lzb} of {len(mdl)} slots ({pct:.0f}%) -- "
               f"matches BIC commitment")

    for brand in counts:
        if brand in R.DROPPED_VENDORS:
            record("FAIL", "Vendor",
                   f"{brand} is a DROPPED vendor (BIC rationalization) "
                   f"and must not appear in the assortment")
        elif brand not in R.VENDOR_ROLES:
            record("FLAG", "Vendor",
                   f"{brand} is not in the governed vendor set "
                   f"{tuple(R.VENDOR_ROLES)}")

    # brand-roles.md assigns each brand to specific tiers. A brand outside its
    # contract is selling something its name does not carry.
    for r in rows:
        role = R.VENDOR_ROLES.get(r["brand"])
        if role and r["tier"] not in role["tiers"]:
            record("FLAG", "Brand role",
                   f"{r['sku_id']} {r['brand']} at {r['tier']} -- brand-roles.md "
                   f"assigns {r['brand']} to {'/'.join(role['tiers'])}")


# --- Ladder mechanics --------------------------------------------------------

def check_steps(rows):
    """A step the customer cannot perceive wastes a slot. A step they cannot
    cross loses the sale. Checked on the governed recliner ladder."""
    rec = sorted((r for r in rows
                  if r["slot_type"] == "MDL" and r["category"] == "Recliner"),
                 key=lambda r: r["retail"])
    prices = sorted({r["retail"] for r in rec})
    for lo, hi in zip(prices, prices[1:]):
        step = hi - lo
        pct = step / lo * 100
        cap = R.BEST_STEP_MAX_PCT if lo >= R.PRICE_BANDS[R.BEST][0] else R.STEP_MAX_PCT
        if step < R.STEP_MIN_DOLLARS:
            record("FAIL", "Step",
                   f"${lo:,} -> ${hi:,}: ${step} step is below the "
                   f"${R.STEP_MIN_DOLLARS} minimum -- invisible to the customer")
        elif pct > cap:
            record("FLAG", "Step",
                   f"${lo:,} -> ${hi:,}: +{pct:.0f}% exceeds {cap:.0f}% -- "
                   f"customer may not cross this rung")
    record("PASS", "Step",
           f"{len(prices)} distinct price points on the recliner ladder, "
           f"${prices[0]:,} to ${prices[-1]:,}")


def check_ladder_continuity(rows):
    """The volume corridor must read continuously. A gap wider than one $250
    increment between $299 and $1,099 is a hole the customer falls through."""
    prices = sorted(r["retail"] for r in rows)
    buckets = set()
    for p in prices:
        if R.DOORBUSTER <= p <= R.PRICE_BANDS[R.BETTER][1]:
            buckets.add((p - 250) // 250)
    lo = (R.DOORBUSTER - 250) // 250
    hi = (R.PRICE_BANDS[R.BETTER][1] - 250) // 250
    missing = [b for b in range(lo, hi + 1) if b not in buckets]
    if missing:
        ranges = ", ".join(f"${b*250+250:,}-${b*250+499:,}" for b in missing)
        record("FLAG", "Continuity",
               f"Empty $250 increments in the volume corridor: {ranges}")
    else:
        record("PASS", "Continuity",
               f"No gap wider than one $250 increment between "
               f"${R.DOORBUSTER} and ${R.PRICE_BANDS[R.BETTER][1]:,}")


def check_feature_reveals(rows):
    """One visible upgrade per rung.

    The rule is about FIRST APPEARANCE, not about the maximum at each price. A
    $849 wall-saver sitting above a $799 power chair is normal -- it is a cover
    or scale variant, not a regression. What would be broken is a feature whose
    cheapest example sits ABOVE a feature that is supposed to come after it,
    because then the customer pays more to go backwards down the ladder.

    So: for each feature, take the lowest price it appears at. Those first-
    appearance prices must strictly increase in ladder order.
    """
    rank = {f: i for i, f in enumerate(R.FEATURE_LADDER)}
    rec = [r for r in rows
           if r["slot_type"] == "MDL" and r["category"] == "Recliner"]

    unknown = {r["trade_up_feature"] for r in rec} - set(rank)
    if unknown:
        record("FAIL", "Feature ladder",
               f"Features not in the governed ladder: {', '.join(sorted(unknown))}")
        return

    first = {}
    for r in rec:
        f = r["trade_up_feature"]
        first[f] = min(first.get(f, 10**9), r["retail"])

    ordered = sorted(first, key=lambda f: rank[f])
    broken = []
    for lo, hi in zip(ordered, ordered[1:]):
        if first[hi] <= first[lo]:
            broken.append(f"{hi} first appears at ${first[hi]:,}, "
                          f"not above {lo} at ${first[lo]:,}")
    if broken:
        for b in broken:
            record("FAIL", "Feature ladder", b)
    else:
        seq = " -> ".join(f"{f} ${first[f]:,}" for f in ordered)
        record("PASS", "Feature ladder", f"Reveals advance in order: {seq}")

    # Tech is held above $1,100 by merchant decision (conflict C-017).
    tech = [f for f in ("usb_charging", "wireless_charging") if f in first]
    low_tech = [f for f in tech if first[f] < R.PRICE_BANDS[R.BEST][0]]
    if low_tech:
        record("FAIL", "Feature ladder",
               f"Tech reveal below ${R.PRICE_BANDS[R.BEST][0]:,}: "
               + ", ".join(f"{f} at ${first[f]:,}" for f in low_tech))
    elif tech:
        record("PASS", "Feature ladder",
               f"Tech held above ${R.PRICE_BANDS[R.BEST][0]:,} per C-017 "
               + ", ".join(f"({f} ${first[f]:,})" for f in tech))


# --- Color -------------------------------------------------------------------

def check_color(rows):
    """Store flex IS color flex, so the 70/20/10 split is the dimension that
    actually varies store to store. It has to be governed."""
    counts = Counter(r["color_tier"] for r in rows)
    total = len(rows)
    for tier, target in R.COLOR_TIERS.items():
        got = counts.get(tier, 0) / total
        if abs(got - target) > R.COLOR_TOLERANCE:
            record("FLAG", "Color",
                   f"{tier}: {got*100:.0f}% vs {target*100:.0f}% target "
                   f"(+/-{R.COLOR_TOLERANCE*100:.0f}pts)")
        else:
            record("PASS", "Color",
                   f"{tier}: {got*100:.0f}% vs {target*100:.0f}% target")

    stray = [r for r in rows
             if r["color_tier"] == "Accelerator"
             and r["tier"] not in R.ACCELERATOR_ALLOWED_TIERS]
    if stray:
        for r in stray:
            record("FAIL", "Color",
                   f"{r['sku_id']} accelerator color at {r['tier']} -- "
                   f"permitted only at {'/'.join(R.ACCELERATOR_ALLOWED_TIERS)}")
    else:
        record("PASS", "Color",
               "No accelerator colors mid-ladder -- neutral trade-up path intact")


# --- Promotion ---------------------------------------------------------------

def check_promo(rows):
    """The $299 must exist, and it must NOT consume a governed slot. That is the
    whole 'promote heavy, margin out above it' mechanism."""
    doorbusters = [r for r in rows if r["retail"] == R.DOORBUSTER]
    if not doorbusters:
        record("FAIL", "Promo",
               f"No ${R.DOORBUSTER} doorbuster -- the traffic driver is missing")
    else:
        on_slot = [r for r in doorbusters if r["slot_type"] == "MDL"]
        if on_slot:
            record("FAIL", "Promo",
                   f"${R.DOORBUSTER} doorbuster is consuming an MDL slot "
                   f"({', '.join(r['sku_id'] for r in on_slot)}) -- promo and "
                   f"special-buy items are excluded from slot count")
        else:
            record("PASS", "Promo",
                   f"{len(doorbusters)} x ${R.DOORBUSTER} doorbuster, all "
                   f"off-slot -- advertised hard without spending a slot")

    promo = [r for r in rows if r["retail"] == R.PROMO_PRICE]
    if not promo:
        record("FAIL", "Promo",
               f"No ${R.PROMO_PRICE} promo price point (matrix promo price)")
    else:
        record("PASS", "Promo",
               f"{len(promo)} SKUs at the ${R.PROMO_PRICE} promo price point")


# --- Customer coverage -------------------------------------------------------

def check_customer_jobs(rows):
    """Built backward from the customer: every job in 01-customer-jobs.md must
    have slots, or the gallery has a hole in it."""
    mdl = [r for r in rows if r["slot_type"] == "MDL"]
    counts = Counter(r["customer_job"] for r in mdl)
    for job, want in R.CUSTOMER_JOB_SLOTS.items():
        got = counts.get(job, 0)
        if got == 0:
            record("FAIL", "Customer job", f"'{job}' has no slots")
        elif abs(got - want) > 2:
            record("FLAG", "Customer job",
                   f"'{job}': {got} slots vs {want} planned")
    missing = set(counts) - set(R.CUSTOMER_JOB_SLOTS)
    if missing:
        record("FLAG", "Customer job",
               f"Jobs not in the plan: {', '.join(sorted(missing))}")
    if not missing and all(counts.get(j) for j in R.CUSTOMER_JOB_SLOTS):
        record("PASS", "Customer job",
               f"All {len(R.CUSTOMER_JOB_SLOTS)} customer jobs have slots")


def check_genz(rows):
    """Job 6 is the wide-appeal requirement. Track it as its own coverage test
    because it cuts across tiers rather than sitting in one."""
    flagged = [r for r in rows if r.get("genz_flag", "").strip().lower()
               in ("y", "yes", "true", "1")]
    in_reach = [r for r in flagged if r["retail"] <= 999]
    if len(flagged) < 10:
        record("FLAG", "Gen Z / Millennial",
               f"Only {len(flagged)} SKUs carry under-35 attributes")
    else:
        record("PASS", "Gen Z / Millennial",
               f"{len(flagged)} SKUs carry under-35 attributes, "
               f"{len(in_reach)} of them at or below $999")


def main():
    if not os.path.exists(SKU_FILE):
        print(f"No SKU data at {SKU_FILE}. Run scripts/build_recliner_data.py first.")
        return 1

    rows = load()

    check_counts(rows)
    check_price_bands(rows)
    check_gbb_mix(rows)
    check_vendors(rows)
    check_steps(rows)
    check_ladder_continuity(rows)
    check_feature_reveals(rows)
    check_color(rows)
    check_promo(rows)
    check_customer_jobs(rows)
    check_genz(rows)

    order = {"FAIL": 0, "FLAG": 1, "PASS": 2, "INFO": 3}
    results.sort(key=lambda r: (order[r[0]], r[1]))

    width = 76
    print("=" * width)
    print("RECLINER GALLERY HEALTH -- 65 FLOORED SKUS / 52 MDL SLOTS")
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

    if R.CONFLICTS:
        open_c = [k for k, v in R.CONFLICTS.items() if v["status"].startswith("OPEN")]
        if open_c:
            print(f"\nOpen conflicts requiring a merchant decision: "
                  f"{', '.join(open_c)}  (see docs/recliners/07-conflicts-decisions.md)")

    return 1 if counts["FAIL"] else 0


if __name__ == "__main__":
    sys.exit(main())
