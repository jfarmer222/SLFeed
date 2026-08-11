"""
Canonical source of truth for the 65-SKU stationary + motion upholstery line.

Everything downstream (CSV exports, ladder health checks, spec audits, the
published assortment page) reads from this module. Change a spec here and
rerun `build_data.py`; do not hand-edit the generated files in data/.

A note on cost: landed_cogs is MODELED from each family's target margin, not
quoted. It is a planning number used to prove the price architecture holds
together before vendor RFQs go out. Replace `margin_target` with quoted
landed cost once vendor costing is back, then rerun the health checks.
"""

# --- Tiers -------------------------------------------------------------------

GOOD, BETTER, BEST = "Good", "Better", "Best"

# --- Style territories -------------------------------------------------------
# The line is transitional-led. These are three expressions of one design
# language, not three separate style universes -- that is what keeps 65 SKUs
# reading as a coherent floor rather than a catalog dump.

CLASSIC = "Classic Transitional"   # rolled/English arms, warm, welt + nailhead
MODERN = "Modern Transitional"     # track/scoop arms, lower profile, clean line
CASUAL = "Casual Transitional"     # pillow arms, deep seats, loose backs

# --- Categories --------------------------------------------------------------

STATIONARY = "Stationary"
SECTIONAL = "Sectional"
MOTION = "Motion"

# --- Margin bands by category and tier (from GBB cost architecture) ----------

MARGIN_BANDS = {
    (STATIONARY, GOOD): (48.0, 52.0),
    (STATIONARY, BETTER): (50.0, 54.0),
    (STATIONARY, BEST): (52.0, 58.0),
    (SECTIONAL, GOOD): (48.0, 52.0),
    (SECTIONAL, BETTER): (50.0, 54.0),
    (SECTIONAL, BEST): (52.0, 58.0),
    (MOTION, GOOD): (48.0, 52.0),
    (MOTION, BETTER): (50.0, 55.0),
    (MOTION, BEST): (53.0, 60.0),
}

# --- Retail price bands for anchor piece types -------------------------------
# Only the anchor pieces are band-checked. Loveseats, chairs and ottomans take
# their position from the sofa they coordinate with, not from an absolute band.

PRICE_BANDS = {
    ("Sofa", GOOD): (599, 899),
    ("Sofa", BETTER): (899, 1399),
    ("Sofa", BEST): (1399, 1999),
    ("Sectional", GOOD): (999, 1499),
    ("Sectional", BETTER): (1499, 2199),
    ("Sectional", BEST): (2199, 3499),
    ("Recliner", GOOD): (399, 599),
    ("Recliner", BETTER): (599, 999),
    ("Recliner", BEST): (999, 1799),
}

# Piece types that roll up to each band key for validation purposes.
ANCHOR_MAP = {
    "Sofa": "Sofa",
    "2-Pc Chaise Sectional": "Sectional",
    "3-Pc Sectional": "Sectional",
    "3-Pc Modular Sectional": "Sectional",
    "5-Pc Modular Sectional": "Sectional",
    "6-Pc Modular Sectional": "Sectional",
    "Manual Recliner": "Recliner",
    "Rocker Recliner": "Recliner",
    "Wall-Saver Recliner": "Recliner",
    "Power Recliner": "Recliner",
}


# --- Vendor architecture -----------------------------------------------------
# The floor is anchored by national brands the customer already trusts, but
# they are deliberately capped: national brands buy price credibility and
# traffic, and they cost margin and differentiation. Everything above the cap
# comes from High Point resources that competitors down the road cannot show.

NATIONAL = "National brand"
DOMESTIC = "Domestic specialist"
IMPORT = "Import specialist"
NICHE = "Niche / design-led"

# Ceiling on national-brand presence, measured as a share of SKU count.
# NOTE: the stated rule is "no more than 30% of SPACE". SKU count is the proxy
# used here because square-footage-per-SKU is not modeled. Sectionals and
# motion consume far more floor than a chair, so before this goes to a floor
# plan the cap must be re-checked against real footprint. See docs.
NATIONAL_SPACE_CAP = 0.30

VENDORS = {
    "ashley": {
        "name": "Ashley",
        "type": NATIONAL,
        "tier_role": GOOD,
        # Ashley anchors the opening price point across every category.
        "categories": (STATIONARY, SECTIONAL, MOTION),
        "note": "Opening-price anchor. Recognized nationally, which is what "
                "makes the Good tier credible instead of merely cheap.",
    },
    "lazboy": {
        "name": "La-Z-Boy",
        "type": NATIONAL,
        "tier_role": BETTER,
        # Motion only -- La-Z-Boy's name equity is in recliners, and using it
        # on stationary would spend that equity where it does not carry.
        "categories": (MOTION,),
        "note": "Middle-tier motion anchor. The name IS the motion category "
                "for most customers; it does the selling before the RSA does.",
    },
    "flexsteel": {
        "name": "Flexsteel",
        "type": NATIONAL,
        "tier_role": BEST,
        "categories": (MOTION,),
        "note": "Upper-tier motion anchor. Carries a construction story "
                "(blue-steel seat spring) that justifies the step above "
                "La-Z-Boy without leaving the motion category.",
    },
}

# Observed street-price ranges by brand and piece type, from public dealer
# catalogs (see research/national-brands.md). Treat as directional: these are
# promo/street prices, not MSRP, and the Flexsteel sample skews to leather and
# triple-power units so its true low end is likely below what is shown.
VENDOR_OBSERVED_RANGES = {
    ("ashley", "Sofa"): (450, 516),
    ("ashley", "Reclining Sofa"): (590, 920),
    ("ashley", "Manual Recliner"): (400, 982),
    ("lazboy", "Rocker Recliner"): (559, 2599),
    ("lazboy", "Wall-Saver Recliner"): (559, 2599),
    ("lazboy", "Power Recliner"): (559, 2599),
    ("lazboy", "Reclining Sofa"): (978, 1769),
    ("lazboy", "Power Reclining Sofa"): (1679, 2590),
    ("lazboy", "Power Reclining Loveseat w/ Console"): (1709, 2510),
    ("flexsteel", "Power Recliner"): (1898, 3997),
    ("flexsteel", "Power Reclining Sofa"): (2998, 4997),
    ("flexsteel", "Power Reclining Loveseat w/ Console"): (2998, 4997),
}

# Where we knowingly price outside a brand's observed range, and why.
RANGE_EXCEPTIONS = {
    "FAI-SOF-G": (
        "Above Ashley's observed $450-$516 stationary sofa band, and "
        "deliberately so. Ashley's opening stationary rides a platform deck "
        "with no springs -- marketed as '3x better than a spring system' "
        "with no test standard cited. This line holds a sinuous-spring "
        "minimum at Good, so we buy up within Ashley rather than down to the "
        "opener. The extra ~$180 of retail is what the spring costs."
    ),
    "EAS-RSF-G": (
        "Above Ashley's observed $590-$920 manual reclining sofa band. "
        "Deliberate: we buy Ashley's better manual, not its opener. The "
        "opener is built to a spec this line will not carry."
    ),
    "STR-PRC-X": (
        "Below Flexsteel's observed $1,898 low. The dealer sample was "
        "weighted to leather and triple-power units; entry fabric power is "
        "not represented and almost certainly sits lower. Confirm against a "
        "Flexsteel line sheet before committing."
    ),
    "STR-PSF-X": (
        "Below Flexsteel's observed $2,998 low, same sampling caveat. This "
        "SKU must be an entry fabric configuration, not the leather "
        "triple-power units the dealer sample captured."
    ),
    "STR-PLC-X": (
        "Below Flexsteel's observed low, same sampling caveat as STR-PSF-X."
    ),
}

# Which vendor supplies each frame family. Non-national assignments are filled
# from the High Point research in research/ -- None means not yet sourced.
FAMILY_VENDOR = {
    # National anchors
    "FAI": "ashley", "DEN": "ashley", "EAS": "ashley",
    "MAR": "lazboy", "NOR": "lazboy",
    "STR": "flexsteel",
    # Pending High Point sourcing
    "ACR": None, "BRN": None, "COR": None,
    "GLN": None, "HAR": None, "IVY": None, "OAK": None,
    "LAN": None, "KNG": None,
    "PEM": None, "QUI": None, "THO": None, "RAV": None,
}


# Vendor-specific buying instructions that fall out of the research. These are
# spec floors the buy must hold even where the vendor's own opener sits below
# them -- the cheapest thing a national brand makes is not automatically the
# thing worth putting on our floor.
VENDOR_BUY_RULES = {
    "ashley": [
        "Sinuous spring minimum. Ashley's opening stationary uses a "
        "springless platform deck; those models are out of spec for this "
        "line and must not be substituted in on a cost-down.",
        "Do not take Ashley's upper motion (e.g. the $2,050-$3,200 band). It "
        "prices straight through La-Z-Boy's Better motion and collapses the "
        "ladder. Ashley motion stays at the $1,100-$1,400 opening band.",
    ],
    "lazboy": [
        "Confirm the lifetime mechanism warranty in writing -- it is the "
        "single strongest claim in the Better tier and it is currently "
        "sourced only from dealer pages, not from La-Z-Boy directly.",
    ],
    "flexsteel": [
        "Blue Steel Spring is the reason this tier costs what it costs. It "
        "must be on the ticket and in the RSA story.",
        "Electrical and motors are warranted 5 years, against La-Z-Boy's "
        "lifetime mechanism claim. Press this in negotiation -- at Best-tier "
        "retail a 5-year electrical cap is the weakest point in the line.",
        "Entry fabric power configurations only. The dealer pricing sampled "
        "was leather and triple-power heavy and is not our SKU.",
    ],
}


def vendor_of(family_code):
    key = FAMILY_VENDOR.get(family_code)
    return VENDORS.get(key) if key else None


def is_national(family_code):
    v = vendor_of(family_code)
    return bool(v and v["type"] == NATIONAL)


# --- Frame families ----------------------------------------------------------
# 19 families. Construction specs are family-level; pieces inherit them.

FAMILIES = {
    # ---------------------------- GOOD TIER --------------------------------
    "FAI": {
        "name": "Fairhaven",
        "tier": GOOD,
        "territory": CLASSIC,
        "margin_target": 49.0,
        "category": STATIONARY,
        "arm": "Rolled (sock) arm, self welt",
        "back": "Tight back, foam + fiber",
        "seat": "1.8 lb standard poly HD foam, dacron wrap",
        "suspension": 'Sinuous spring, 8.5 ga, 4" spacing',
        "frame": "Engineered hardwood (LVL + plywood), corner-blocked",
        "joinery": "Staple-and-glue with corner blocks",
        "legs": "Tapered resin leg, espresso finish",
        "fabric": "Poly-blend performance flat weave",
        "base_cover_grade": "poly_perf",
        "rub_count": 15000,
        "covers": 4,
        "cover_mix": "3 neutral, 1 blue -- all one price grade",
        "design_note": (
            "The opening price statement. Scale is pulled in deliberately "
            "(82\" sofa) so the piece reads tailored rather than cheap. All the "
            "COGS that is here is in the silhouette and the welt -- nothing is "
            "spent where the customer cannot see it."
        ),
        "rsa_story": (
            "This is the best-looking sofa on our opening price point -- that "
            "rolled arm and the welted edge are what you'd normally pay a "
            "lot more for."
        ),
    },
    "ACR": {
        "name": "Ashcroft",
        "tier": GOOD,
        "territory": CLASSIC,
        "category": STATIONARY,
        "margin_target": 50.0,
        "arm": "Rolled (sock) arm, contrast welt",
        "back": "Attached pillow back",
        "seat": "1.8 lb HD poly foam, dacron wrap",
        "suspension": 'Sinuous spring, 8.5 ga, 4" spacing',
        "frame": "Engineered hardwood (LVL + plywood), corner-blocked",
        "joinery": "Staple-and-glue with corner blocks",
        "legs": "Turned wood leg, pecan finish",
        "fabric": "Poly-blend performance flat weave",
        "base_cover_grade": "poly_perf",
        "rub_count": 18000,
        "covers": 4,
        "cover_mix": "2 neutral, 1 greige, 1 blue -- all one price grade",
        "design_note": (
            "The Good-tier volume anchor and the trade-up origin for the "
            "Classic lane. Attached pillow back buys the look of a loose "
            "cushion sofa with none of the fluffing complaints."
        ),
        "rsa_story": (
            "The back cushions are attached -- so it looks plush but it never "
            "goes lumpy on you, and you never have to fight with it."
        ),
    },
    "BRN": {
        "name": "Brantley",
        "tier": GOOD,
        "territory": MODERN,
        "category": STATIONARY,
        "margin_target": 48.5,
        "arm": "Square track arm",
        "back": "Attached pillow back, horizontal channel",
        "seat": "1.8 lb HD poly foam, dacron wrap",
        "suspension": 'Sinuous spring, 8.5 ga, 4" spacing',
        "frame": "Engineered hardwood (LVL + plywood), corner-blocked",
        "joinery": "Staple-and-glue with corner blocks",
        "legs": "Tapered wood leg, natural oak",
        "fabric": "Poly-blend performance flat weave",
        "base_cover_grade": "poly_perf",
        "rub_count": 18000,
        "covers": 4,
        "cover_mix": "2 neutral, 1 charcoal, 1 ivory -- all one price grade",
        "design_note": (
            "Lowest profile in the Good tier at 34\" high. Buys the younger "
            "customer without asking the Good tier to pay for a track arm's "
            "tailoring premium -- corners are simple, not mitred."
        ),
        "rsa_story": (
            "Clean square arm, low back, oak legs -- this is the look people "
            "are pulling off Instagram, at our opening price."
        ),
    },
    "COR": {
        "name": "Cordell",
        "tier": GOOD,
        "territory": CASUAL,
        "category": STATIONARY,
        "margin_target": 50.5,
        "arm": "Slope (flared) arm",
        "back": "Attached pillow back, two-over-two",
        "seat": '1.8 lb HD poly foam, dacron wrap, 23" seat depth',
        "suspension": 'Sinuous spring, 8.5 ga, 4" spacing',
        "frame": "Engineered hardwood (LVL + plywood), corner-blocked",
        "joinery": "Staple-and-glue with corner blocks",
        "legs": "Tapered wood leg, walnut finish",
        "fabric": "Poly-blend performance flat weave",
        "base_cover_grade": "poly_perf",
        "rub_count": 20000,
        "covers": 5,
        "cover_mix": "2 neutral, 1 sage, 1 rust, 1 blue -- all one price grade",
        "design_note": (
            "The biggest Good-tier footprint at 90\" and a 23\" seat. Sells on "
            "size -- the customer cross-shopping a warehouse club sofa sees "
            "this one is genuinely deeper."
        ),
        "rsa_story": (
            "Sit all the way back on this one -- it's a full 23 inches deep. "
            "Most sofas at this price make you perch."
        ),
    },
    "DEN": {
        "name": "Denby",
        "tier": GOOD,
        "territory": MODERN,
        "category": SECTIONAL,
        "margin_target": 49.0,
        "arm": "Square track arm",
        "back": "Attached pillow back",
        "seat": "1.8 lb HD poly foam, dacron wrap",
        "suspension": 'Sinuous spring, 8.5 ga, 4" spacing',
        "frame": "Engineered hardwood (LVL + plywood), corner-blocked",
        "joinery": "Staple-and-glue with corner blocks",
        "legs": "Tapered wood leg, natural oak",
        "fabric": "Poly-blend performance flat weave",
        "base_cover_grade": "poly_perf",
        "rub_count": 18000,
        "covers": 4,
        "cover_mix": "2 neutral, 1 charcoal, 1 blue -- all one price grade",
        "design_note": (
            "Sectional entry point. Reversible chaise on the 2-Pc so one SKU "
            "covers both room orientations -- halves the floor and inventory "
            "burden of a LAF/RAF split at the tier that can least afford it."
        ),
        "rsa_story": (
            "The chaise moves to either end -- so it fits your room no matter "
            "which way the TV faces. One box, no wrong choice."
        ),
    },
    "EAS": {
        "name": "Easton",
        "tier": GOOD,
        "territory": CASUAL,
        "category": MOTION,
        "margin_target": 48.5,
        "arm": "Pillow-top rolled arm",
        "back": "Attached channel back",
        "seat": '4.5" 1.8 lb HD poly foam',
        "suspension": "Sinuous spring over steel seat box",
        "frame": "Engineered hardwood + steel mechanism reinforcement plates",
        "joinery": "Staple-and-glue, bolted at mechanism points",
        "legs": "Concealed base",
        "fabric": "Poly-blend performance / PU leather-look",
        "base_cover_grade": "poly_perf",
        "rub_count": 20000,
        "covers": 4,
        "cover_mix": "2 performance fabric, 1 PU leather-look, 1 chocolate",
        "mechanism": "Two-position push-back (chair); 3-position manual (sofa/loveseat)",
        "design_note": (
            "Motion entry. Push-back on the chair means no handle and no "
            "recliner silhouette -- it captures the customer who wants the "
            "function but refuses to own something that looks like a recliner."
        ),
        "rsa_story": (
            "No handle, no lever -- you just lean back. Sitting up it looks "
            "like a regular chair, which is the whole point."
        ),
    },
    # --------------------------- BETTER TIER --------------------------------
    "GLN": {
        "name": "Glenwood",
        "tier": BETTER,
        "territory": CLASSIC,
        "category": STATIONARY,
        "margin_target": 53.0,
        "arm": "English (Charles of London) arm",
        "back": "Loose pillow back, channeled poly fill",
        "seat": "2.0 lb HR foam core, dacron wrap",
        "suspension": 'Sinuous spring, 9 ga, 3" spacing',
        "frame": "Kiln-dried hardwood, corner-blocked",
        "joinery": "Dowelled with corner blocks",
        "legs": "Turned wood leg, pecan finish",
        "fabric": "Performance chenille / textured weave",
        "base_cover_grade": "chenille_textured",
        "rub_count": 35000,
        "covers": 10,
        "cover_mix": "5 standard grade, 5 premium grade (+$100)",
        "design_note": (
            "The Classic lane's Better rung. English arm is the visible "
            "step-up from Ashcroft's roll -- set back, so the seat is wider "
            "without the sofa being wider. That is a real functional gain the "
            "RSA can demonstrate with their own body."
        ),
        "rsa_story": (
            "Watch -- the arm sets back, so you get almost four more inches of "
            "actual sitting room than the sofa next to it, same wall space."
        ),
    },
    "HAR": {
        "name": "Harlow",
        "tier": BETTER,
        "territory": MODERN,
        "category": STATIONARY,
        "margin_target": 52.0,
        "arm": "Track arm, contrast welt, rounded front edge",
        "back": "Tight back, vertical channeling",
        "seat": "2.0 lb HR foam core, dacron wrap",
        "suspension": 'Sinuous spring, 9 ga, 3" spacing',
        "frame": "Kiln-dried hardwood, corner-blocked",
        "joinery": "Dowelled with corner blocks",
        "legs": "Brushed metal leg, matte black",
        "fabric": "Performance textured weave / linen-look poly",
        "base_cover_grade": "chenille_textured",
        "rub_count": 35000,
        "covers": 8,
        "cover_mix": "5 standard grade, 3 premium grade (+$100)",
        "design_note": (
            "Lowest back in the line at 33\". The channeled tight back does the "
            "differentiation work that a loose cushion would do elsewhere -- it "
            "holds a crisp line, which is the whole promise of the silhouette."
        ),
        "rsa_story": (
            "Run your hand down that back -- that channeling is sewn, not "
            "stuffed. It'll look exactly like this in five years."
        ),
    },
    "IVY": {
        "name": "Ivywood",
        "tier": BETTER,
        "territory": CASUAL,
        "category": STATIONARY,
        "margin_target": 53.0,
        "arm": "Pillow-top track arm",
        "back": "Loose pillow back, channeled poly fill",
        "seat": '2.0 lb HR foam core, dacron wrap, 24" seat depth',
        "suspension": "Pocketed coil drop-in unit",
        "frame": "Kiln-dried hardwood, corner-blocked",
        "joinery": "Dowelled with corner blocks",
        "legs": "Tapered wood leg, walnut finish",
        "fabric": "Performance chenille",
        "base_cover_grade": "chenille_textured",
        "rub_count": 40000,
        "covers": 10,
        "cover_mix": "5 standard grade, 5 premium grade (+$100)",
        "design_note": (
            "The deepest seat in the line at 24\" and the only Better "
            "stationary family on pocketed coil suspension. This is the "
            "comfort-first customer's destination -- and the demo that makes "
            "the Casual lane's step-up self-evident."
        ),
        "rsa_story": (
            "Push down on the seat -- feel it push back? That's individual "
            "coils under there, same as a good mattress. Foam alone can't do "
            "that."
        ),
    },
    "OAK": {
        "name": "Oakhurst",
        "tier": BETTER,
        "territory": MODERN,
        "category": STATIONARY,
        "margin_target": 52.5,
        "arm": "Square track arm, contrast welt",
        "back": "Attached pillow back",
        "seat": "2.0 lb HR foam core, dacron wrap",
        "suspension": 'Sinuous spring, 9 ga, 3" spacing',
        "frame": "Kiln-dried hardwood, corner-blocked",
        "joinery": "Dowelled with corner blocks",
        "legs": "Tapered wood leg, natural oak",
        "fabric": "Full performance program -- stain + moisture barrier",
        "base_cover_grade": "chenille_textured",
        "rub_count": 50000,
        "covers": 12,
        "cover_mix": "12 performance covers, single price grade",
        "design_note": (
            "The family-proof family. Every cover is performance and every "
            "cover is one price -- the customer with kids and a dog never has "
            "to weigh fabric choice against budget. Carries the line's only "
            "sleeper."
        ),
        "rsa_story": (
            "Every single cover on this one is performance fabric, and they're "
            "all the same price. Pick the color you love, not the one you can "
            "afford to ruin."
        ),
    },
    "LAN": {
        "name": "Lanmore",
        "tier": BETTER,
        "territory": MODERN,
        "category": SECTIONAL,
        "margin_target": 52.5,
        "arm": "Track arm, contrast welt",
        "back": "Tight back, vertical channeling",
        "seat": "2.0 lb HR foam core, dacron wrap",
        "suspension": 'Sinuous spring, 9 ga, 3" spacing',
        "frame": "Kiln-dried hardwood, corner-blocked",
        "joinery": "Dowelled with corner blocks",
        "legs": "Brushed metal leg, matte black",
        "fabric": "Performance textured weave / linen-look poly",
        "base_cover_grade": "chenille_textured",
        "rub_count": 35000,
        "covers": 8,
        "cover_mix": "5 standard grade, 3 premium grade (+$100)",
        "design_note": (
            "Harlow's silhouette in sectional form -- deliberately shares the "
            "arm, leg and cover program so the two can merchandise as one "
            "modern vignette and amortize the same tooling and cover buy."
        ),
        "rsa_story": (
            "Same clean arm and metal leg as the Harlow sofa behind you -- so "
            "if you want the sectional in the family room and the sofa in the "
            "front room, they read as a set."
        ),
    },
    "KNG": {
        "name": "Kingsley",
        "tier": BETTER,
        "territory": CASUAL,
        "category": SECTIONAL,
        "margin_target": 52.5,
        "arm": "Pillow-top track arm",
        "back": "Loose pillow back, channeled poly fill",
        "seat": '2.0 lb HR foam core, dacron wrap, 24" seat depth',
        "suspension": "Pocketed coil drop-in unit",
        "frame": "Kiln-dried hardwood, corner-blocked",
        "joinery": "Dowelled with corner blocks",
        "legs": "Tapered wood leg, walnut finish",
        "fabric": "Performance chenille",
        "base_cover_grade": "chenille_textured",
        "rub_count": 40000,
        "covers": 10,
        "cover_mix": "5 standard grade, 5 premium grade (+$100)",
        "design_note": (
            "Ivywood's construction in modular form. The 5-Pc introduces the "
            "modular concept at Better so the customer meets reconfigurability "
            "before they are asked to pay Best-tier money for it."
        ),
        "rsa_story": (
            "These pieces come apart and go back together however your room "
            "needs -- and if you move, it moves with you."
        ),
    },
    "MAR": {
        "name": "Marchetti",
        "tier": BETTER,
        "territory": CLASSIC,
        "category": MOTION,
        "margin_target": 52.0,
        "arm": "Rolled arm, contrast welt",
        "back": "Attached channel back, layered fiber",
        "seat": '5" 2.0 lb HR foam',
        "suspension": "Sinuous spring over steel seat box",
        "frame": "Kiln-dried hardwood + steel bolt-through at stress points",
        "joinery": "Dowelled, steel bolt-through at mechanism points",
        "legs": "Concealed base",
        "fabric": "Performance fabric / split-grain leather",
        "base_cover_grade": "chenille_textured",
        "rub_count": 40000,
        "covers": 8,
        "cover_mix": "5 performance fabric, 3 genuine split-grain leather (+$200)",
        "mechanism": "Wall-saver 3-position manual; rocker chassis on RRC",
        "design_note": (
            "Manual motion done properly. Wall-saver is the headline -- it "
            "solves an actual room-layout problem, which is a far stronger "
            "step-up argument than a smoother handle. Genuine leather enters "
            "the line here, at Better, because motion customers expect it."
        ),
        "rsa_story": (
            "Push it right up against the wall -- go ahead. Now recline it. It "
            "comes forward instead of back. You get the recliner without "
            "giving up a foot of your room."
        ),
    },
    "NOR": {
        "name": "Northfield",
        "tier": BETTER,
        "territory": CASUAL,
        "category": MOTION,
        "margin_target": 51.5,
        "arm": "Pillow-top track arm",
        "back": "Attached pillow back, layered fiber",
        "seat": '5" 2.0 lb HR foam',
        "suspension": "Sinuous spring over steel seat box",
        "frame": "Kiln-dried hardwood + steel bolt-through at stress points",
        "joinery": "Dowelled, steel bolt-through at mechanism points",
        "legs": "Concealed base",
        "fabric": "Performance fabric / split-grain leather",
        "base_cover_grade": "chenille_textured",
        "rub_count": 40000,
        "covers": 8,
        "cover_mix": "5 performance fabric, 3 genuine split-grain leather (+$200)",
        "mechanism": "Single-motor power recline, infinite position, USB-A port",
        "design_note": (
            "Power at Better. This is the single most important step-up in the "
            "whole line -- the manual-to-power jump changes the showroom demo "
            "completely and it is the reason the motion ladder can support "
            "four rungs instead of two."
        ),
        "rsa_story": (
            "One button -- and you can stop it anywhere you want, not just "
            "three preset spots. Charge your phone right there in the arm."
        ),
    },
    # ---------------------------- BEST TIER ---------------------------------
    "PEM": {
        "name": "Pemberton",
        "tier": BEST,
        "territory": CLASSIC,
        "category": STATIONARY,
        "margin_target": 55.0,
        "arm": "English arm, scroll detail, antique nailhead border",
        "back": "Loose pillow back, down-blend fill",
        "seat": "2.2 lb HR foam core, thick fiber wrap "
                "(down-blend seat envelope available custom-order)",
        "suspension": "Pocketed coil drop-in unit",
        "frame": "Kiln-dried maple, corner-blocked",
        "joinery": "Mortise-and-tenon at all stress points",
        "legs": "Turned wood leg, hand-finished pecan",
        "fabric": "Premium woven / velvet / Crypton performance",
        "base_cover_grade": "premium",
        "rub_count": 60000,
        "covers": 16,
        "in_stock_covers": 8,
        "cover_mix": "8 in-stock, 8 custom-order book (+$150-$400)",
        "design_note": (
            "The line's craftsmanship statement. Most of what the customer pays "
            "for here is invisible -- mortise-and-tenon joinery, kiln-dried "
            "maple, pocketed coil suspension -- which is the ethical "
            "obligation of a Best tier and why this SKU carries a 15-year "
            "frame warranty the rest of the line cannot. 8-way hand-tied was "
            "specced and then cut: at $195 of a $810 COGS budget it is the "
            "most expensive thing in furniture the customer cannot feel in a "
            "showroom. That money went into the down-blend back pillows and "
            "the maple frame instead."
        ),
        "rsa_story": (
            "Individual pocketed coils under the seat, mortise-and-tenon maple "
            "frame, down in the back pillows. Fifteen years on the frame -- "
            "it'll sit the same the day your kids inherit it."
        ),
    },
    "QUI": {
        "name": "Quincy",
        "tier": BEST,
        "territory": MODERN,
        "category": STATIONARY,
        "margin_target": 54.0,
        "arm": "Scoop arm, sculpted",
        "back": "Tight back, sculpted foam",
        "seat": "2.2 lb HR foam core, thick fiber wrap",
        "suspension": "Pocketed coil drop-in unit",
        "frame": "Kiln-dried hardwood, corner-blocked",
        "joinery": "Mortise-and-tenon at all stress points",
        "legs": "Solid brass leg, brushed",
        "fabric": "Premium woven / velvet / Crypton performance",
        "base_cover_grade": "premium",
        "rub_count": 60000,
        "covers": 14,
        "in_stock_covers": 7,
        "cover_mix": "7 in-stock, 7 custom-order book (+$150-$400)",
        "design_note": (
            "The design halo. The scoop arm and a 32\" back make this the most "
            "sculptural piece in the line, and the sculpting is where the "
            "money goes -- hand-shaped foam and brass legs on a "
            "mortise-and-tenon frame. Coil-on-coil was specced and cut for "
            "the same reason 8-way hand-tied was: the arm is what sells this "
            "SKU, and the budget belongs where the customer looks."
        ),
        "rsa_story": (
            "Look at the line of that arm -- it's carved, not stuffed. And "
            "there are individual coils underneath the seat, so it comes "
            "right back up every time you stand."
        ),
    },
    "THO": {
        "name": "Thorne",
        "tier": BEST,
        "territory": MODERN,
        "category": STATIONARY,
        "margin_target": 54.0,
        "arm": "Shelter (tuxedo) arm",
        "back": "Tight back, arm height matched",
        "seat": "2.2 lb HR foam core, dacron wrap",
        "suspension": "Pocketed coil drop-in unit",
        "frame": "Kiln-dried hardwood, corner-blocked",
        "joinery": "Mortise-and-tenon at all stress points",
        "legs": "Solid brass leg, brushed",
        "fabric": "Top-grain leather, full aniline available",
        "base_cover_grade": "leather",
        "rub_count": 100000,
        "covers": 6,
        "in_stock_covers": 4,
        "cover_mix": "4 top-grain leather in-stock, 2 full-aniline special order",
        "design_note": (
            "The leather statement, and deliberately the narrowest cover "
            "program in the line -- leather is the product here, so six "
            "well-chosen hides beat sixteen mediocre ones. Shelter arm is the "
            "only one in the assortment; it is a design-literate customer's "
            "piece and it is not trying to be for everyone."
        ),
        "rsa_story": (
            "This is top-grain leather -- not bonded, not split. Run your hand "
            "across it. In ten years it'll look better than it does today, "
            "which is not true of anything else on this floor."
        ),
    },
    "RAV": {
        "name": "Ravenswood",
        "tier": BEST,
        "territory": CASUAL,
        "category": SECTIONAL,
        "margin_target": 55.0,
        "arm": "Pillow-top track arm, loose down-blend pillow",
        "back": "Loose pillow back, down-blend fill",
        "seat": "2.2 lb HR foam core, thick fiber wrap",
        "suspension": "Pocketed coil drop-in unit",
        "frame": "Kiln-dried hardwood, corner-blocked",
        "joinery": "Mortise-and-tenon at all stress points",
        "legs": "Tapered wood leg, hand-finished walnut",
        "fabric": "Premium woven / performance velvet / Crypton",
        "base_cover_grade": "premium",
        "rub_count": 60000,
        "covers": 18,
        "in_stock_covers": 8,
        "cover_mix": "8 in-stock, 10 custom-order book (+$150-$400)",
        "design_note": (
            "Fully modular -- every seat is an independent unit, so the "
            "customer buys a configuration rather than a shape. This is the "
            "line's highest ticket and its widest cover program; the "
            "custom-order book shifts inventory risk to the customer and lets "
            "the assortment carry 18 covers without carrying 18 SKUs."
        ),
        "rsa_story": (
            "Every piece here is its own unit -- build it around your room "
            "today, rebuild it in the next house. And the seat cushions have a "
            "down wrap over the foam, so you sink in and it still holds you up."
        ),
    },
    "STR": {
        "name": "Stratton",
        "tier": BEST,
        "territory": CLASSIC,
        "category": MOTION,
        "margin_target": 55.0,
        "arm": "Rolled arm, contrast welt, nailhead border",
        "back": "Attached channel back, layered fiber",
        "seat": '5" 2.2 lb HR foam over encased spring unit',
        "suspension": "Encased spring unit over steel seat box",
        "frame": "Kiln-dried hardwood + full steel bolt-through construction",
        "joinery": "Steel bolt-through at all mechanism and stress points",
        "legs": "Concealed base",
        "fabric": "Top-grain leather / premium performance fabric",
        "base_cover_grade": "premium",
        "rub_count": 100000,
        "covers": 16,
        "in_stock_covers": 16,
        "cover_mix": "8 premium performance fabric, 8 top-grain leather (+$300)",
        "mechanism": (
            "Dual-motor power recline with independent power headrest, "
            "power lumbar, USB-A + USB-C, battery backup"
        ),
        "design_note": (
            "Three motors: recline, headrest, lumbar. The independent headrest "
            "is the demo -- body reclined, head forward for the TV -- and it is "
            "something no Better-tier power unit can do. Battery backup removes "
            "the last objection, which is the cord."
        ),
        "rsa_story": (
            "Lean all the way back -- now bring just your head forward to watch "
            "the game. Separate motor. And there's a battery in it, so it "
            "doesn't have to live next to an outlet."
        ),
    },
}

# --- SKUs --------------------------------------------------------------------
# (sku_id, family, piece_type, retail, width, depth, height, seat_depth,
#  seat_height, optional per-SKU mechanism override)

def _s(sku, fam, piece, retail, w, d, h, sd, sh, mech=None):
    return {
        "sku_id": sku,
        "family": fam,
        "piece_type": piece,
        "retail": retail,
        "width_in": w,
        "depth_in": d,
        "height_in": h,
        "seat_depth_in": sd,
        "seat_height_in": sh,
        "mechanism_override": mech,
    }


SKUS = [
    # ---- GOOD: 20 SKUs -----------------------------------------------------
    _s("FAI-SOF-G", "FAI", "Sofa", 699, 82, 36, 37, 20, 19),
    _s("FAI-LVS-G", "FAI", "Loveseat", 649, 60, 36, 37, 20, 19),
    _s("FAI-CHR-G", "FAI", "Chair", 449, 37, 36, 37, 20, 19),

    _s("ACR-SOF-G", "ACR", "Sofa", 849, 86, 38, 38, 21, 19),
    _s("ACR-LVS-G", "ACR", "Loveseat", 799, 63, 38, 38, 21, 19),
    _s("ACR-CHR-G", "ACR", "Chair", 529, 40, 38, 38, 21, 19),
    _s("ACR-OTT-G", "ACR", "Ottoman", 299, 30, 24, 18, 0, 18),

    _s("BRN-SOF-G", "BRN", "Sofa", 799, 84, 36, 34, 22, 18),
    _s("BRN-LVS-G", "BRN", "Loveseat", 749, 61, 36, 34, 22, 18),
    _s("BRN-CHR-G", "BRN", "Chair", 499, 38, 36, 34, 22, 18),

    _s("COR-SOF-G", "COR", "Sofa", 899, 90, 40, 38, 23, 19),
    _s("COR-LVS-G", "COR", "Loveseat", 849, 67, 40, 38, 23, 19),
    _s("COR-CHR-G", "COR", "Chair", 559, 42, 40, 38, 23, 19),
    _s("COR-OTT-G", "COR", "Ottoman", 319, 32, 26, 18, 0, 18),

    _s("DEN-SC2-G", "DEN", "2-Pc Chaise Sectional", 1099, 104, 65, 34, 22, 18),
    _s("DEN-SC3-G", "DEN", "3-Pc Sectional", 1399, 118, 88, 34, 22, 18),

    _s("EAS-REC-G", "EAS", "Manual Recliner", 499, 38, 40, 41, 21, 20,
       "Two-position push-back"),
    _s("EAS-RSF-G", "EAS", "Reclining Sofa", 999, 87, 40, 41, 21, 20,
       "3-position manual, dual recline"),
    _s("EAS-RLS-G", "EAS", "Reclining Loveseat", 949, 65, 40, 41, 21, 20,
       "3-position manual, dual recline"),

    # ---- BETTER: 29 SKUs ---------------------------------------------------
    _s("GLN-SOF-B", "GLN", "Sofa", 1299, 88, 39, 38, 22, 19),
    _s("GLN-LVS-B", "GLN", "Loveseat", 1199, 65, 39, 38, 22, 19),
    _s("GLN-CHR-B", "GLN", "Chair", 799, 41, 39, 38, 22, 19),
    _s("GLN-OTT-B", "GLN", "Ottoman", 429, 32, 26, 19, 0, 19),

    _s("HAR-SOF-B", "HAR", "Sofa", 1199, 85, 37, 33, 22, 18),
    _s("HAR-LVS-B", "HAR", "Loveseat", 1099, 62, 37, 33, 22, 18),
    _s("HAR-CHR-B", "HAR", "Chair", 749, 39, 37, 33, 22, 18),
    _s("HAR-ACH-B", "HAR", "Accent Chair", 579, 31, 33, 34, 21, 18),

    _s("IVY-SOF-B", "IVY", "Sofa", 1349, 92, 41, 39, 24, 19),
    _s("IVY-LVS-B", "IVY", "Loveseat", 1249, 69, 41, 39, 24, 19),
    _s("IVY-CHR-B", "IVY", "Chair", 849, 44, 41, 39, 24, 19),
    _s("IVY-OTT-B", "IVY", "Ottoman", 449, 34, 28, 19, 0, 19),

    _s("OAK-SOF-B", "OAK", "Sofa", 1249, 86, 38, 35, 22, 19),
    _s("OAK-LVS-B", "OAK", "Loveseat", 1149, 63, 38, 35, 22, 19),
    _s("OAK-CHR-B", "OAK", "Chair", 779, 40, 38, 35, 22, 19),
    _s("OAK-OTT-B", "OAK", "Ottoman", 439, 31, 25, 19, 0, 19),
    _s("OAK-SLP-B", "OAK", "Queen Sleeper Sofa", 1499, 88, 40, 36, 22, 19),

    _s("LAN-SC2-B", "LAN", "2-Pc Chaise Sectional", 1599, 108, 66, 34, 22, 18),
    _s("LAN-SC3-B", "LAN", "3-Pc Sectional", 1899, 124, 90, 34, 22, 18),

    _s("KNG-SC2-B", "KNG", "2-Pc Chaise Sectional", 1699, 112, 68, 39, 24, 19),
    _s("KNG-SC3-B", "KNG", "3-Pc Sectional", 1999, 130, 92, 39, 24, 19),
    _s("KNG-SC5-B", "KNG", "5-Pc Modular Sectional", 2199, 156, 110, 39, 24, 19),

    _s("MAR-RRC-B", "MAR", "Rocker Recliner", 699, 40, 41, 42, 21, 20,
       "3-position manual on rocker chassis"),
    _s("MAR-WRC-B", "MAR", "Wall-Saver Recliner", 799, 40, 41, 42, 21, 20,
       "Wall-saver 3-position manual"),
    _s("MAR-RSF-B", "MAR", "Reclining Sofa", 1449, 89, 41, 42, 21, 20,
       "Wall-saver 3-position manual, dual recline"),
    _s("MAR-RLC-B", "MAR", "Reclining Loveseat w/ Console", 1399, 76, 41, 42, 21, 20,
       "Wall-saver 3-position manual, dual recline"),

    _s("NOR-PRC-B", "NOR", "Power Recliner", 999, 41, 42, 43, 21, 20),
    _s("NOR-PSF-B", "NOR", "Power Reclining Sofa", 1899, 90, 42, 43, 21, 20),
    _s("NOR-PLC-B", "NOR", "Power Reclining Loveseat w/ Console", 1849, 78, 42, 43, 21, 20),

    # ---- BEST: 16 SKUs -----------------------------------------------------
    _s("PEM-SOF-X", "PEM", "Sofa", 1799, 90, 40, 39, 22, 20),
    _s("PEM-LVS-X", "PEM", "Loveseat", 1699, 67, 40, 39, 22, 20),
    _s("PEM-CHR-X", "PEM", "Chair", 1099, 42, 40, 39, 22, 20),
    _s("PEM-OTT-X", "PEM", "Ottoman", 579, 34, 28, 19, 0, 19),

    _s("QUI-SOF-X", "QUI", "Sofa", 1749, 87, 38, 32, 23, 18),
    _s("QUI-LVS-X", "QUI", "Loveseat", 1599, 64, 38, 32, 23, 18),
    _s("QUI-CHR-X", "QUI", "Chair", 1079, 40, 38, 32, 23, 18),

    _s("THO-SOF-X", "THO", "Sofa", 2299, 88, 39, 33, 22, 18),
    _s("THO-LVS-X", "THO", "Loveseat", 2099, 65, 39, 33, 22, 18),
    _s("THO-CHR-X", "THO", "Chair", 1349, 41, 39, 33, 22, 18),

    # Sofa built on the Ravenswood modular platform -- same frame, cushion and
    # cover program. Closes the Casual Transitional lane at Best without new
    # tooling, and gives the Ivywood customer somewhere to trade up to.
    _s("RAV-SOF-X", "RAV", "Sofa", 1899, 94, 40, 36, 23, 19),
    _s("RAV-SC3-X", "RAV", "3-Pc Modular Sectional", 2699, 132, 94, 36, 23, 19),
    _s("RAV-SC5-X", "RAV", "5-Pc Modular Sectional", 3199, 160, 112, 36, 23, 19),
    _s("RAV-SC6-X", "RAV", "6-Pc Modular Sectional", 3499, 184, 112, 36, 23, 19),

    _s("STR-PRC-X", "STR", "Power Recliner", 1499, 42, 43, 43, 21, 20),
    _s("STR-PSF-X", "STR", "Power Reclining Sofa", 2799, 92, 43, 43, 21, 20),
    _s("STR-PLC-X", "STR", "Power Reclining Loveseat w/ Console", 2699, 80, 43, 43, 21, 20),
]


# --- Trade-up lanes ----------------------------------------------------------
# A lane is a like-for-like path a customer walks: same piece type, same style
# territory, one rung per tier. Lanes are how the ladder gets validated -- a
# tier average tells you nothing about whether an individual step-up is
# defensible.

LANES = {
    "Classic Transitional sofa": ["ACR-SOF-G", "GLN-SOF-B", "PEM-SOF-X"],
    "Modern Transitional sofa": ["BRN-SOF-G", "HAR-SOF-B", "QUI-SOF-X"],
    "Casual Transitional sofa": ["COR-SOF-G", "IVY-SOF-B", "RAV-SOF-X"],
    "Sectional (2-Pc chaise)": ["DEN-SC2-G", "LAN-SC2-B"],
    "Sectional (3-Pc)": ["DEN-SC3-G", "KNG-SC3-B", "RAV-SC3-X"],
    # Motion lanes run four rungs, not three: the manual-to-power transition is
    # a genuine product discontinuity that needs its own step, so Better
    # carries two rungs (manual wall-saver, then single-motor power).
    "Recliner": ["EAS-REC-G", "MAR-RRC-B", "NOR-PRC-B", "STR-PRC-X"],
    "Reclining sofa": ["EAS-RSF-G", "MAR-RSF-B", "NOR-PSF-B", "STR-PSF-X"],
}

# Lanes that deliberately stop short of a tier, with the merchandising reason.
# Registering a gap here downgrades it from FLAG to a stated position -- it does
# not make the gap disappear, it makes it a decision somebody owns.
INTENTIONAL_LANE_GAPS = {
    ("Sectional (2-Pc chaise)", BEST): (
        "Best-tier sectional is a modular program and starts at 3-Pc. A "
        "two-piece modular defeats the point of modularity, and the Best "
        "customer who wants a chaise buys RAV-SC3-X at $2,699 -- a +69% step "
        "from LAN-SC2-B. Revisit only if 2-Pc demand at Better proves out and "
        "the step to 3-Pc is measurably blocking trade-up."
    ),
}


# Anchor SKUs that sit outside their category price band on purpose.
BAND_EXCEPTIONS = {
    "THO-SOF-X": (
        "Top-grain leather cannot be built inside the $1,399-$1,999 fabric "
        "sofa band at a Best-tier margin -- the hide alone is ~$330 of a "
        "$1,058 COGS budget. Leather runs its own band above fabric, which is "
        "how the market prices it."
    ),
}

# --- Derived helpers ---------------------------------------------------------

def landed_cogs(sku):
    """Modeled landed cost from the family's target margin."""
    fam = FAMILIES[sku["family"]]
    target = fam["margin_target"]
    # The Oakhurst sleeper carries mechanism COGS the rest of the family does
    # not; margin compresses ~150bps. This is expected, not an error.
    if sku["sku_id"] == "OAK-SLP-B":
        target = 51.0
    return round(sku["retail"] * (1 - target / 100.0))


def margin_pct(sku):
    return round(100.0 * (1 - landed_cogs(sku) / sku["retail"]), 2)


def mechanism(sku):
    fam = FAMILIES[sku["family"]]
    return sku["mechanism_override"] or fam.get("mechanism", "")


def enriched():
    """SKU records joined to family specs, with cost and margin computed."""
    rows = []
    for s in SKUS:
        fam = FAMILIES[s["family"]]
        rows.append({
            "sku_id": s["sku_id"],
            "family_code": s["family"],
            "family": fam["name"],
            "vendor": (vendor_of(s["family"]) or {}).get("name", "TBD"),
            "vendor_type": (vendor_of(s["family"]) or {}).get("type", "Unsourced"),
            "tier": fam["tier"],
            "territory": fam["territory"],
            "category": fam["category"],
            "piece_type": s["piece_type"],
            "retail": s["retail"],
            "landed_cogs": landed_cogs(s),
            "margin_pct": margin_pct(s),
            "margin_dollars": s["retail"] - landed_cogs(s),
            "arm": fam["arm"],
            "back": fam["back"],
            "seat": fam["seat"],
            "suspension": fam["suspension"],
            "frame": fam["frame"],
            "joinery": fam["joinery"],
            "legs": fam["legs"],
            "fabric": fam["fabric"],
            "rub_count": fam["rub_count"],
            "mechanism": mechanism(s),
            "covers": fam["covers"],
            "width_in": s["width_in"],
            "depth_in": s["depth_in"],
            "height_in": s["height_in"],
            "seat_depth_in": s["seat_depth_in"],
            "seat_height_in": s["seat_height_in"],
        })
    return rows
