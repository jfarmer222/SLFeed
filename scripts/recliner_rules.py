"""
Machine-checkable constraints for the 65-SKU Slumberland recliner gallery.

Every constant here traces to the Slumberland Category Architecture repository
and carries its source path in the comment above it. Nothing in this file is an
opinion -- opinions live in scripts/recliner_data.py, where the actual SKUs are
chosen. This file is what the SKU choices are validated AGAINST.

Precedence, per 00-system/precedence.md:
    1. dated approved commitment   <- BIC slot count, La-Z-Boy share
    2. canonical category rule     <- 30-categories/recliners.md
    3. enterprise rule             <- 20-rules/*
    4. target or benchmark
    5. observed actual
    6. presentation intelligence / evidence
    7. opportunity or open question
    8. historical source extract

Where two records disagree they are BOTH retained here with their basis. They
are never averaged. See CONFLICTS at the bottom of this file.
"""

# --- Assortment units --------------------------------------------------------
# 20-rules/assortment-rules.md: "A numeric assortment target is invalid without
# its unit." Recliners carry three different numbers in three different units,
# which is conflict C-001. They are not interchangeable.

TOTAL_FLOORED_SKUS = 65      # 30-categories/recliners.md -- "65 floored SKUs total"
MDL_SLOTS = 52               # BIC commitment -- "52 consistent slots across all stores"
OFF_SLOT_SKUS = 13           # 65 - 52. Special buys / promo / rapid-replenishment.

# 40-evidence/recliners.md RECLINERS!A132 -- prior observed state, NOT current policy.
# Retained per precedence.md: the correct encoding is 52 committed, 60 observed,
# -8 in transition. Never averaged to 56.
OBSERVED_PRIOR_MDL_SLOTS = 60
SLOT_TRANSITION_GAP = MDL_SLOTS - OBSERVED_PRIOR_MDL_SLOTS   # -8

# Lift carve-out inside the 52 (merchant decision, this build).
LIFT_MDL_SLOTS = 9
RECLINER_MDL_SLOTS = MDL_SLOTS - LIFT_MDL_SLOTS              # 43

# Why off-slot SKUs are not slots, in the source's own words --
# 40-evidence/recliners.md, Target Slot Count definition:
#   "Total number of active MDL slots in a category. Sets the maximum SKU count
#    for core assortment. EXCLUDES special buys, promotional, and in/out items
#    (per the promotional matrix)."
# This is what makes 65 = 52 + 13 the only reading consistent with the source,
# and it is why the $299 doorbuster does not consume a strategic slot.

# --- Store flex --------------------------------------------------------------
# 30-categories/recliners.md: "Single assortment of 52 with flex on color options
# by store." 20-rules/assortment-rules.md requires this be explicit, never
# inferred from a range.

STORE_FLEX = "color_flex_only"

# --- Good / Better / Best ----------------------------------------------------
# 30-categories/recliners.md GBB table + 40-evidence/recliners.md H3.
# GBB Basis is explicitly "based on recliner price" -- which is why lift is
# scored on its own ladder and never folded into these shares (conflict C-013).

GOOD, BETTER, BEST = "Good", "Better", "Best"

PRICE_BANDS = {
    GOOD:   (0, 399),        # "Up to $399"
    BETTER: (400, 1099),     # "$400 - $1,099"
    BEST:   (1100, 2999),    # "$1,100+", ceiling set to $2,999 this build
}

CEILING = 2999               # merchant decision, this build
DOORBUSTER = 299             # 20-rules/promotion-rules.md -- Recliners doorbuster
PROMO_PRICE = 399            # 20-rules/promotion-rules.md -- Recliners promo price

# Target slot share. Current == target in the source (11/78/11), which is what
# makes the "Grow" direction on Good a conflict -- see C-012.
TARGET_MDL_SHARE = {GOOD: 0.11, BETTER: 0.78, BEST: 0.11}

# Applied to the 43 governed recliner slots.
TARGET_SLOTS = {GOOD: 5, BETTER: 33, BEST: 5}
SLOT_TOLERANCE = 1           # +/- 1 slot per tier before a FAIL

# Observed performance, 30-categories/recliners.md. This is the whole commercial
# argument for the assortment: Best turns 11% of slots into 19% of sales.
CURRENT_SALES_SHARE = {GOOD: 0.05, BETTER: 0.76, BEST: 0.19}
CURRENT_UNIT_SHARE = {GOOD: 0.08, BETTER: 0.76, BEST: 0.16}

# Category role direction, 40-evidence/recliners.md G2.
TIER_DIRECTION = {GOOD: "Grow", BETTER: "Hold", BEST: "Hold"}

# --- Customer jobs -----------------------------------------------------------
# docs/recliners/01-customer-jobs.md. Labeled Proposal per CLAUDE.md -- a
# merchant's reading of the customer, not an approved policy record. Slot counts
# sum to the 52 MDL slots; each slot carries exactly one PRIMARY job.

CUSTOMER_JOB_SLOTS = {
    "Cheap and now":      3,    # Job 1 -- traffic / price access      (Good 3)
    "First real chair":   7,    # Job 2 -- new household               (Better 7)
    "My chair":          12,    # Job 3 -- core comfort, volume engine (Better 12)
    "Will it fit":        4,    # Job 4 -- small space / apartment     (Better 4)
    "Survive my life":    5,    # Job 5 -- family and pets, cover-led  (Better 5)
    "Not a recliner":     5,    # Job 6 -- under-35 design         (Good 2, Better 3)
    "Built my size":      3,    # Job 7 -- big and tall           (Better 2, Best 1)
    "Easier to stand":    9,    # Job 8 -- aging in place, the lift ladder
    "Does everything":    4,    # Job 9 -- wellness / aspiration, the halo (Best 4)
}
# Sums to 52 MDL slots. Recliner-only (all jobs but 8) = 43, distributed
# Good 5 / Better 33 / Best 5 to match TARGET_SLOTS exactly.
#
# Job 6 holds only 5 PRIMARY slots, but the under-35 attribute set is a
# secondary characteristic on many Job 2/3/4 chairs. Coverage is therefore
# tracked separately via the genz_flag column, not by this count alone.

# --- Vendors -----------------------------------------------------------------
# 30-categories/recliners.md + 20-rules/brand-roles.md.
# NOTE: the 30%-of-floor national-brand cap in scripts/assortment_data.py is a
# STATIONARY UPHOLSTERY premise and does not carry here (conflict C-014).
# 20-rules/gbb-rules.md: "do not force one enterprise price ladder across
# categories." Recliners are national-brand-LED by commitment.

LAZBOY_SLOT_SHARE = 0.64     # BIC commitment -- "64% of slots = La-Z-Boy"
LAZBOY_MIN_SLOTS = 31        # floor before FAIL (60% of 52)
LAZBOY_TARGET_SLOTS = 33     # 0.64 * 52, rounded

# 40-evidence/recliners.md G3 -- different basis (product mix %, not slot share).
# Retained, not reconciled. See C-011.
NATL_BRAND_MIX_PCT = 60

VENDOR_ROLES = {
    "La-Z-Boy": {
        "code": "LAZY",
        "role": "Brand authority + comfort anchor",
        # brand-roles.md: Promotional = fabric/manual/price; Better = power +
        # customization; Best = fabric & leather, advanced features.
        "tiers": (GOOD, BETTER, BEST),
        "note": "Customers use the name as a generic term for reclining chairs. "
                "The brand sells before the RSA opens their mouth.",
    },
    "Ashley": {
        "code": "ASHL",
        "role": "Good tier value and promo traffic",
        # brand-roles.md Ashley/Recliners: fabric, manual, Good + Better only.
        "tiers": (GOOD, BETTER),
        "note": "Carries the doorbuster. Manual and fabric only per brand role.",
    },
    "Flexsteel": {
        "code": "FLXS",
        "role": "Better/Best quality + Perfect Match program",
        # brand-roles.md Flexsteel/Recliners: Best, leather, power, Recliner + Lift.
        "tiers": (BETTER, BEST),
        "note": "Adding non-lift via Perfect Match. Named 2026 Best entries: "
                "$1,299 fabric / $1,599 refined leather.",
        "lift": True,
    },
    "Franklin": {
        "code": "FKLN",
        "role": "Cuddler and gap fill where La-Z-Boy has none",
        # NOTE: 20-rules/brand-roles.md contains NO Franklin row at all. These
        # tiers are INFERRED from 30-categories/recliners.md ("Franklin =
        # cuddler and fill gaps"), not read from a brand-role contract. That is
        # why Franklin appearing at Best raises a FLAG rather than a FAIL -- it
        # is a merchant judgment the source does not settle either way.
        "tiers": (GOOD, BETTER),
        "note": "'Design Your Recline' with swivel and power options.",
    },
}

# 40-evidence/recliners.md: "Vendor Changes: MAWA and SOMO dropped from lineup."
# Readable for trend intelligence, never proposable as a resource. See C-015.
DROPPED_VENDORS = ("Man Wah", "Cheers", "Southern Motion", "Fusion Furniture")

# --- Price ladder mechanics --------------------------------------------------
# A step the customer cannot perceive is a wasted slot. A step they cannot cross
# is a lost sale. Carried from scripts/ladder_health.py and tightened for
# recliners, where the absolute dollars are smaller than sofas.

STEP_MIN_PCT = 8.0           # below this the rung is invisible at the low end
STEP_MAX_PCT = 45.0          # above this the customer stops climbing
STEP_MIN_DOLLARS = 50        # no rung closer than $50 to the one below it

# Above $1,100 the customer is buying a different thing, so wider steps are fine.
BEST_STEP_MAX_PCT = 60.0

# --- One feature reveal per rung ---------------------------------------------
# 30-categories/recliners.md Opportunity 2: "Add features (charging, massage,
# heat, add-on tables) to justify Better/Best step-up." The sofa map's 3-second
# rule made this visual; here it is made ordinal: the reveal at each price point
# may repeat the one below it but may never regress.
#
# ORDERING NOTE: charging sits ABOVE leather rather than in the $700-900 band
# where competitors place it. That is a merchant decision (conflict C-017) taken
# because La-Z-Boy -- 64% of our slots -- has no verified charging SKU at any
# price. Holding tech high keeps the volume corridor anchor-brand-led. The cost
# is that the under-35 answer below $1,100 must run on silhouette, scale and
# cover instead of ports.

FEATURE_LADDER = (
    "manual_rocker",         # the floor
    "pushback_hileg",        # reads as a chair, not a recliner
    "wall_saver",            # apartment-friendly, reclines from the wall
    "swivel_glider",         # chair-like silhouette
    "power_recline",         # THE step-up moment -- the hinge of the ladder
    "power_headrest",
    "power_lumbar",
    "leather_match",
    "usb_charging",          # TECH ENTERS -- held above $1,100 by merchant decision
    "premium_leather",
    "massage",               # with heat
    "zero_gravity",          # the ceiling
)

# --- Color, 70/20/10 ---------------------------------------------------------
# Carried from the 30-SKU sofa map. Store flex is color flex, so this is the
# dimension that actually varies store to store -- it has to be governed.

COLOR_TIERS = {
    "Anchor":      0.70,     # grays, charcoals, greiges, taupes -- deep stock
    "Bridge":      0.20,     # cognac, walnut, olive, muted navy
    "Accelerator": 0.10,     # statement colors
}
COLOR_TOLERANCE = 0.07

# Accelerators are permitted only where they cost nothing strategically: at the
# promo entry (where color IS the impulse) and at Best (where it is halo).
# Never mid-ladder, where it fragments the neutral trade-up path.
ACCELERATOR_ALLOWED_TIERS = (GOOD, BEST)

# --- Promotion ---------------------------------------------------------------
# 20-rules/promotion-rules.md, Recliners row + 40-evidence G7.

PROMO = {
    "hero_items": True,
    "doorbusters": True,
    "advertised_items": True,
    "primary_focus": "National Brands",
    "hero_roadmaps": True,
    "roadmap_advertised": True,
    "promoted_segment": ("Fabric Recliners", "Add-Ons", "Special Order"),
    "promoted_tier": "All",
    "promo_price": PROMO_PRICE,
    "doorbuster_price": DOORBUSTER,
    "natl_brand_allocation": 0.70,
    "other_brand_allocation": 0.30,
    "min_per_a_event": 0,
    "max_per_a_event": 2,
}

# --- Operational gates -------------------------------------------------------
# 30-categories/recliners.md active flags. Not assortment rules, but the
# trade-up plan does not survive contact with the floor if these stay red.

OPS_GATES = {
    "lead_time_wks": (3.8, 4.0, "on_track"),
    "fill_rate_days": (3.9, 7.0, "on_track"),
    "in_stock_pct": (85, 95, "GAP"),
    "digital_commerce_overall": ("F", "urgent"),
    "digital_commerce_images": ("F", "urgent"),
    "digital_commerce_upc": ("F", "urgent"),
    "digital_commerce_copy": ("D+", "urgent"),
    "products_needing_content": 243,
}

# --- Category performance context --------------------------------------------
# 30-categories/recliners.md + 40-evidence/recliners.md H1.
# Periods are labeled because 50-issues/conflicts.md C-009 forbids comparing
# metrics whose period or basis differ.

PERFORMANCE = {
    "annual_sales_pct_of_business": 0.13,        # FY2025-2026
    "yoy_sales": 0.20,                           # FY2025-2026
    "yoy_units": 0.15,                           # FY2025-2026
    "written_6mo_total": 25_657_629,             # 6-mo written 2025, all stores
    "written_6mo_recliners_only": 21_187_574,    # +4.52% YoY
    "written_6mo_lift": 4_470_055,               # +18.40% YoY -- 3x the base rate
    "sales_per_sqft": 252,                       # vs 152 store average
    "store_avg_sales_per_sqft": 152,
}

# --- Conflicts ---------------------------------------------------------------
# 00-system/precedence.md: "Do not silently choose between conflicting values."
# Each entry names both values and the basis on which the build proceeds.

CONFLICTS = {
    "C-001": {
        "issue": "Recliner slot count: 52 committed vs 60 observed vs 65 floored",
        "values": {"commitment": 52, "observed_prior": 60, "floored_skus": 65},
        "type": "unit mismatch",
        "basis": "52 = governed MDL slots (rank 1). 60 = prior observed state, "
                 "-8 in transition. 65 = floored SKUs = 52 MDL + 13 off-slot, "
                 "per the Target Slot Count definition excluding special buys "
                 "and promotional items.",
        "status": "resolved structurally; both values retained",
    },
    "C-011": {
        "issue": "La-Z-Boy 64% of slots vs National Brand Mix 60%",
        "values": {"lazboy_slot_share": 0.64, "natl_brand_mix_pct": 60},
        "type": "basis mismatch",
        "basis": "Slot share and product-mix % are not the same denominator. "
                 "Not comparable, so not reconciled. LZB 64% of slots governs "
                 "this map; 60% natl brand mix is reported separately.",
        "status": "OPEN -- merchant decision required",
    },
    "C-012": {
        "issue": "Good direction is 'Grow' but Good target MDL == current MDL (11%)",
        "values": {"direction": "Grow", "current_mdl": 0.11, "target_mdl": 0.11},
        "type": "true contradiction",
        "basis": "Encoded as growth WITHOUT slot growth: Good grows through the "
                 "13 off-slot promo and special-buy SKUs and through step-up "
                 "capture, not by taking MDL share from Better. Recorded as a "
                 "Proposal, not as policy.",
        "status": "OPEN -- proposal, not approved",
    },
    "C-013": {
        "issue": "Lift inside the 65 changes the GBB denominator",
        "type": "scope difference",
        "basis": "GBB is governed on a recliner-only basis, matching the source's "
                 "own statement that GBB Basis is 'based on recliner price'. "
                 "Blended-with-lift mix is reported, never governed. Two columns, "
                 "never one average.",
        "status": "resolved structurally",
    },
    "C-014": {
        "issue": "SLFeed upholstery line caps national brands at 30% of floor; "
                 "recliners are national-brand-led at 64% La-Z-Boy",
        "type": "scope difference",
        "basis": "The 30% cap is a stationary-upholstery premise. gbb-rules.md: "
                 "'do not force one enterprise price ladder across categories.' "
                 "Recliner validators use a La-Z-Boy FLOOR, not a national cap.",
        "status": "resolved structurally",
    },
    "C-015": {
        "issue": "Dropped vendors could reappear via High Point scouting",
        "values": {"dropped": DROPPED_VENDORS},
        "type": "transition from old to new",
        "basis": "MAWA and SOMO were dropped under BIC vendor rationalization. "
                 "Readable for trend intelligence, never proposable as vendors.",
        "status": "resolved structurally",
    },
}
