#!/usr/bin/env python3
"""Construction integrity audit -- Layers 1-5 -- for every frame family.

Layers 1-4 check the spec against the tier's minimum thresholds. Layer 5 is
price coherence: it builds the product up from component cost benchmarks and
asks whether the silhouette being promised can actually be manufactured inside
the landed-cost envelope the retail price allows.

A family that passes Layers 1-4 but fails Layer 5 is the dangerous case -- the
specs read fine on paper but the design cannot be built for the money.

Usage:
    python scripts/spec_checker.py              # audit all families
    python scripts/spec_checker.py PEM QUI      # audit named families
"""

import re
import sys

import assortment_data as A

# --- Layer 1-4 tier minimums -------------------------------------------------

FOAM_MIN_DENSITY = {A.GOOD: 1.8, A.BETTER: 2.0, A.BEST: 2.2}
RUB_MIN = {A.GOOD: 15000, A.BETTER: 30000, A.BEST: 50000}

SUSPENSION_RANK = {
    "elastic webbing": 0, "sinuous": 1,
    "pocketed coil": 2, "encased spring": 2, "8-way hand-tied": 3,
}
SUSPENSION_MIN = {A.GOOD: 1, A.BETTER: 1, A.BEST: 2}

JOINERY_RANK = {"staple": 0, "dowel": 1, "mortise": 2, "bolt-through": 2}
JOINERY_MIN = {A.GOOD: 0, A.BETTER: 1, A.BEST: 2}

FRAME_RANK = {"engineered": 0, "kiln-dried": 1}
FRAME_MIN = {A.GOOD: 0, A.BETTER: 1, A.BEST: 1}

# Constructions that must never appear at a given tier or above.
RED_FLAGS = [
    (r"bonded leather", (A.BETTER, A.BEST),
     "Bonded leather delaminates in 2-4 years; it cannot carry a Better or "
     "Best warranty story"),
    (r"\b1\.[0-5]\s*lb", (A.GOOD, A.BETTER, A.BEST),
     "Foam below 1.6 lb density collapses inside the first year at any tier"),
    (r"no-sag.*6\s*ga|6\s*ga.*sinuous", (A.GOOD, A.BETTER, A.BEST),
     "Spring gauge lighter than 8.5 will oil-can and creak under normal load"),
]

# --- Layer 5 component cost benchmarks (per unit unless noted) ---------------

ARM_COST = {                       # per pair
    "rolled": 36, "track": 46, "slope": 41, "english": 55,
    "pillow-top": 60, "scoop": 75, "shelter": 85,
}
SEAT_COST = {                      # per seat cushion
    "standard_poly": 14, "hr_wrap": 25, "down_blend": 55, "pocketed_coil": 45,
}
BACK_COST = {                      # per seat position
    "tight": 7, "attached": 11, "loose": 14, "loose_down": 22,
}
SUSPENSION_COST = {                # per seat section
    "sinuous_std": 10, "sinuous_hd": 15, "pocketed coil": 30,
    "encased spring": 24, "8-way hand-tied": 65,
}
FRAME_COST = {                     # per frame, benchmarked to a 3-seat sofa
    "engineered_staple": 55, "kiln_dowel": 85,
    "kiln_mortise": 115, "kiln_bolt": 105,
}


def frame_scale(seats):
    """Frame cost is part fixed (tooling, corner blocks, rails) and part
    proportional to size. A one-seat recliner frame is not a third of a sofa
    frame, and an eight-piece sectional is not eight times one."""
    return 0.5 + 0.5 * (seats / 3.0)
LEG_COST = {"resin": 6, "wood": 25, "metal": 40, "concealed": 10}
FABRIC_YD_COST = {                 # per yard, landed at volume
    "poly_perf": 3.2, "chenille_textured": 5.5, "premium": 9.0, "leather": 20.0,
}
MECH_COST = {
    "push-back": 35, "3-position": 55, "wall-saver": 75, "rocker": 75,
    "single-motor": 115, "dual-motor": 255,
}
def yards_per_seat(seats):
    if seats >= 6:
        return 4.4
    if seats >= 4:
        return 4.8
    return 5.5


def labor_efficiency(seats):
    if seats >= 6:
        return 0.85
    if seats >= 4:
        return 0.90
    return 1.0

# Labor and freight scale with seat count and construction complexity, NOT with
# material price -- a leather sofa does not take 35% more labor because the
# hide costs more. Modeling overhead as a flat percentage of materials was the
# original error; it penalized every premium-material family twice.
# Labor and freight both move with the sourcing model, and they move in
# opposite directions. Good tier is imported: cheap labor, heavy ocean freight.
# Best skews domestic/near-shore: expensive labor, lighter freight.
LABOR_PER_SEAT = {A.GOOD: 16, A.BETTER: 26, A.BEST: 34}
FREIGHT_PER_SEAT = {A.GOOD: 22, A.BETTER: 21, A.BEST: 19}

LABOR_COMPLEX_JOINERY = 10         # mortise-and-tenon or steel bolt-through
LABOR_PREMIUM_CUSHION = 8          # down-blend or pocketed coil cushion
LABOR_LEATHER = 10                 # hide cutting, matching, heavier sewing

# Component costs are directional, not quoted -- vendor, volume and country of
# origin all move them. A build-up within this tolerance of the allowed COGS
# is coherent; beyond it, the design genuinely cannot be built for the money.
COGS_TOLERANCE = 0.10

SEATS = {
    "Sofa": 3, "Loveseat": 2, "Chair": 1, "Ottoman": 1, "Accent Chair": 1,
    "Queen Sleeper Sofa": 3,
    # Seating positions, not box count: a "5-Pc modular" is five units that
    # together seat about six.
    "2-Pc Chaise Sectional": 4, "3-Pc Sectional": 5,
    "3-Pc Modular Sectional": 4, "5-Pc Modular Sectional": 6,
    "6-Pc Modular Sectional": 7,
    "Manual Recliner": 1, "Rocker Recliner": 1, "Wall-Saver Recliner": 1,
    "Power Recliner": 1, "Reclining Sofa": 3, "Reclining Loveseat": 2,
    "Reclining Loveseat w/ Console": 2, "Power Reclining Sofa": 3,
    "Power Reclining Loveseat w/ Console": 2,
}


# Which components a piece actually carries, and at what share of the
# family's per-seat benchmark.
NO_ARMS = {"Ottoman"}
FRAME_OVERRIDE = {"Ottoman": 0.40}
SUSPENSION_SHARE = {"Ottoman": 0.6}
FABRIC_YARDS_FLAT = {"Ottoman": 2.5}
SLEEPER_MECH = 130               # queen sleeper mechanism + deck


def _match(text, table):
    low = text.lower()
    for key, val in table.items():
        if key in low:
            return val
    return None


def _base(text):
    """Strip parenthetical custom-order options -- they are upcharges, not the
    standard build, and costing them overstates every unit."""
    return re.sub(r"\([^)]*\)", "", text)


def classify_seat(text):
    low = _base(text).lower()
    if "down-blend" in low:
        return "down_blend"
    if "pocketed coil" in low:
        return "pocketed_coil"
    if "hr foam" in low:
        return "hr_wrap"
    return "standard_poly"


def classify_back(text):
    low = _base(text).lower()
    if "loose" in low and "down" in low:
        return "loose_down"
    if "loose" in low:
        return "loose"
    if "attached" in low:
        return "attached"
    return "tight"


def classify_suspension(text):
    low = text.lower()
    if "8-way hand-tied" in low:
        return "8-way hand-tied"
    if "pocketed coil" in low:
        return "pocketed coil"
    if "encased spring" in low:
        return "encased spring"
    if "9 ga" in low:
        return "sinuous_hd"
    return "sinuous_std"


def classify_frame(text, joinery):
    jl = joinery.lower()
    kiln = "kiln-dried" in text.lower()
    if not kiln:
        return "engineered_staple"
    if "mortise" in jl:
        return "kiln_mortise"
    if "bolt-through" in jl:
        return "kiln_bolt"
    return "kiln_dowel"


def classify_legs(text):
    low = text.lower()
    if "concealed" in low:
        return "concealed"
    if "metal" in low or "brass" in low:
        return "metal"
    if "resin" in low:
        return "resin"
    return "wood"


def classify_fabric(text):
    low = text.lower()
    if "top-grain" in low or "aniline" in low:
        return "leather"
    if "premium" in low or "velvet" in low or "crypton" in low:
        return "premium"
    if "chenille" in low or "textured" in low or "linen-look" in low:
        return "chenille_textured"
    return "poly_perf"


def classify_arm(text):
    low = text.lower()
    for key in ("pillow-top", "english", "shelter", "scoop", "slope",
                "track", "rolled"):
        if key in low:
            return key
    return "rolled"


def anchor_sku(code, rows):
    """The piece the family's price architecture is judged on."""
    fam_rows = [r for r in rows if r["family_code"] == code]
    for want in ("Sofa", "Power Recliner", "Rocker Recliner",
                 "Manual Recliner"):
        hits = [r for r in fam_rows if r["piece_type"] == want]
        if hits:
            return hits[0]
    anchors = [r for r in fam_rows if r["piece_type"] in A.ANCHOR_MAP]
    return min(anchors or fam_rows, key=lambda r: r["retail"])


def build_up(fam, sku):
    """Modeled component build-up for one piece."""
    piece = sku["piece_type"]
    seats = SEATS.get(piece, 3)
    arm = 0 if piece in NO_ARMS else ARM_COST[classify_arm(fam["arm"])]
    seat = SEAT_COST[classify_seat(fam["seat"])] * seats
    back = 0 if piece in NO_ARMS else BACK_COST[classify_back(fam["back"])] * seats
    susp = (SUSPENSION_COST[classify_suspension(fam["suspension"])]
            * seats * SUSPENSION_SHARE.get(piece, 1.0))
    frame = FRAME_COST[classify_frame(fam["frame"], fam["joinery"])] \
        * FRAME_OVERRIDE.get(piece, frame_scale(seats))
    legs = LEG_COST[classify_legs(fam["legs"])]
    grade = fam.get("base_cover_grade") or classify_fabric(fam["fabric"])
    yards = FABRIC_YARDS_FLAT.get(piece, yards_per_seat(seats) * seats)
    fabric = FABRIC_YD_COST[grade] * yards

    mech = 0
    if fam["category"] == A.MOTION:
        text = (sku["mechanism"] or "").lower()
        mech = _match(text, MECH_COST) or 55
        # Motion sofas and loveseats carry one mechanism per reclining seat.
        mech *= 2 if seats >= 2 else 1
    if piece == "Queen Sleeper Sofa":
        mech = SLEEPER_MECH

    materials = arm + seat + back + susp + frame + legs + fabric + mech

    per_seat = LABOR_PER_SEAT[fam["tier"]]
    if classify_frame(fam["frame"], fam["joinery"]) in ("kiln_mortise", "kiln_bolt"):
        per_seat += LABOR_COMPLEX_JOINERY
    if classify_seat(fam["seat"]) in ("down_blend", "pocketed_coil"):
        per_seat += LABOR_PREMIUM_CUSHION
    if grade == "leather":
        per_seat += LABOR_LEATHER
    labor = round(per_seat * labor_efficiency(seats) * seats)
    freight = FREIGHT_PER_SEAT[fam["tier"]] * seats

    parts = {
        "Arms": arm, "Seat cushions": seat, "Back": back, "Suspension": round(susp),
        "Frame + joinery": round(frame), "Legs": legs, "Fabric": round(fabric),
    }
    if mech:
        parts["Mechanism"] = mech
    parts = {k: v for k, v in parts.items() if v}
    parts["Manufacturing labor"] = labor
    parts["Packaging + freight"] = freight
    return round(materials + labor + freight), parts


def audit(code, rows):
    fam = A.FAMILIES[code]
    tier = fam["tier"]
    sku = anchor_sku(code, rows)
    lines = []
    verdicts = []

    def layer(name, status, detail):
        verdicts.append(status)
        lines.append(f"  Layer {name:<26} {status:<5}  {detail}")

    # Layer 1 -- Frame
    fr = _match(fam["frame"], FRAME_RANK)
    jo = _match(fam["joinery"], JOINERY_RANK)
    ok = (fr is not None and fr >= FRAME_MIN[tier]
          and jo is not None and jo >= JOINERY_MIN[tier])
    layer("1 - Frame", "PASS" if ok else "FAIL",
          f"{fam['frame'].split(',')[0]} / {fam['joinery'].split(',')[0]}")

    # Layer 2 -- Suspension
    sr = _match(fam["suspension"], SUSPENSION_RANK)
    ok = sr is not None and sr >= SUSPENSION_MIN[tier]
    layer("2 - Suspension", "PASS" if ok else "FAIL", fam["suspension"])

    # Layer 3 -- Cushion
    m = re.search(r"(\d\.\d)\s*lb", fam["seat"])
    density = float(m.group(1)) if m else None
    premium = classify_seat(fam["seat"]) in ("down_blend", "pocketed_coil")
    ok = premium or (density is not None and density >= FOAM_MIN_DENSITY[tier])
    layer("3 - Cushion", "PASS" if ok else "FAIL", fam["seat"])

    # Layer 4 -- Fabric
    ok = fam["rub_count"] >= RUB_MIN[tier]
    layer("4 - Fabric", "PASS" if ok else "FAIL",
          f"{fam['rub_count']:,} double rubs -- {fam['fabric']}")

    # Layer 5 -- Price coherence, worst piece in the family
    fam_rows = [r for r in rows if r["family_code"] == code]
    worst = None
    for r in fam_rows:
        m, pr = build_up(fam, r)
        pc = 100.0 * (r["landed_cogs"] - m) / r["landed_cogs"]
        if worst is None or pc < worst[0]:
            worst = (pc, r, m, pr)
    pct, sku, modeled, parts = worst
    allowed = sku["landed_cogs"]
    headroom = allowed - modeled
    if modeled > allowed * (1 + COGS_TOLERANCE):
        status, note = "FAIL", "VISUAL PROMISE EXCEEDS CONSTRUCTION BUDGET"
    elif headroom < 0:
        status, note = "FLAG", "over budget but inside sourcing variance"
    elif pct < 5:
        status, note = "FLAG", "thin -- no room for cost movement"
    else:
        status, note = "PASS", "buildable with headroom"
    layer("5 - Price coherence", status,
          f"worst piece {sku['sku_id']} ${sku['retail']:,} | allowed "
          f"${allowed} vs modeled ${modeled} | {headroom:+d} ({pct:+.1f}%) "
          f"-- {note}")

    # Red flags
    blob = " ".join(str(v) for v in fam.values()).lower()
    flags = [msg for pat, tiers, msg in RED_FLAGS
             if tier in tiers and re.search(pat, blob)]

    overall = "REJECTED" if "FAIL" in verdicts else (
        "APPROVED WITH CONDITIONS" if "FLAG" in verdicts else "APPROVED")

    return {
        "code": code, "fam": fam, "sku": sku, "lines": lines,
        "overall": overall, "flags": flags, "parts": parts,
        "modeled": modeled, "allowed": allowed,
    }


def main(argv):
    rows = A.enriched()
    codes = [c.upper() for c in argv[1:]] or list(A.FAMILIES)
    unknown = [c for c in codes if c not in A.FAMILIES]
    if unknown:
        print(f"Unknown family code(s): {', '.join(unknown)}")
        print(f"Valid: {', '.join(A.FAMILIES)}")
        return 2

    reports = [audit(c, rows) for c in codes]
    rejected = 0

    for r in reports:
        fam, sku = r["fam"], r["sku"]
        print("=" * 78)
        print(f"{fam['name'].upper()} ({r['code']}) -- {fam['territory']}")
        print(f"Tier: {fam['tier']}   Category: {fam['category']}   "
              f"Anchor: {sku['sku_id']} {sku['piece_type']} ${sku['retail']:,}")
        print(f"Margin: {sku['margin_pct']}%   "
              f"Landed COGS (modeled from target): ${sku['landed_cogs']}")
        print("-" * 78)
        print("CONSTRUCTION INTEGRITY SCORECARD")
        for line in r["lines"]:
            print(line)
        print("-" * 78)
        print("  COMPONENT BUILD-UP")
        for k, v in r["parts"].items():
            print(f"    {k:<28} ${v:>7,.0f}")
        print(f"    {'TOTAL MODELED':<28} ${r['modeled']:>7,.0f}   "
              f"(allowed ${r['allowed']:,})")
        if r["flags"]:
            print("-" * 78)
            print("  RED FLAGS")
            for f in r["flags"]:
                print(f"    ! {f}")
        print("-" * 78)
        print(f"  OVERALL: {r['overall']}")
        print(f"  RSA SELL STORY: \"{' '.join(fam['rsa_story'].split())}\"")
        print()
        if r["overall"] == "REJECTED":
            rejected += 1

    print("=" * 78)
    print(f"{len(reports)} families audited | "
          f"{sum(1 for r in reports if r['overall'] == 'APPROVED')} approved | "
          f"{sum(1 for r in reports if r['overall'].startswith('APPROVED WITH'))}"
          f" conditional | {rejected} rejected")
    print("=" * 78)
    return 1 if rejected else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
