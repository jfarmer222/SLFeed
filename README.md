# SLFeed — 65-SKU Stationary + Motion Upholstery Line

An analytical and design-led upholstery assortment for a mid-market,
~125-store retailer running a Good/Better/Best strategy. 65 sellable pieces
across 19 frame families, transitional-led, spanning stationary seating,
sectionals and motion.

Every SKU is specced to construction detail, costed against a component
build-up, and validated by scripts that fail the build if the ladder breaks.

## The line at a glance

| Tier | Families | SKUs | Avg retail | Blended GM |
|---|---|---|---|---|
| Good | 6 | 19 | $731 | 49.3% |
| Better | 8 | 29 | $1,202 | 52.3% |
| Best | 5 | 17 | $1,989 | 54.7% |
| **Line** | **19** | **65** | **$1,270** | **52.8%** |

Three style territories, all transitional: Classic (22 SKUs), Modern (22),
Casual (21). 598 orderable cover combinations, 499 stocked — the 99-SKU
difference lives in Best-tier custom-order books.

**Sourcing:** national brands anchor every tier but are capped at 30% of the
floor — Ashley at Good, La-Z-Boy at Better (motion only), Flexsteel at Best
(motion only) = 18 SKUs, 27.7%. The other 47 come from 10 High Point
resources. See `docs/06-vendor-architecture.md`.

## Trade-up lanes

| Lane | Good | Better | Best |
|---|---|---|---|
| Classic Transitional sofa | Ashcroft $849 | Glenwood $1,299 | Pemberton $1,849 |
| Modern Transitional sofa | Brantley $799 | Harlow $1,199 | Quincy $1,749 |
| Casual Transitional sofa | Cordell $899 | Ivywood $1,349 | Ravenswood $1,899 |
| Sectional (3-Pc) | Denby $1,399 | Kingsley $1,999 | Ravenswood $2,699 |
| Recliner | Easton $499 | Marchetti $699 → Northfield $999 | Stratton $1,499 |
| Reclining sofa | Easton $999 | Marchetti $1,449 → Northfield $1,899 | Stratton $2,799 |

## Repository layout

```
docs/
  01-design-brief.md        Design language, tier architecture, engineering thesis
  02-feature-ladder.md      What changes between tiers and why; features cut
  03-price-architecture.md  Margin, step-ups, what the cost audit changed
  04-cover-strategy.md      Cover depth, gating logic, proliferation math
  05-assortment-health.md   Current check status, exceptions, open items
  06-vendor-architecture.md Who supplies each SKU, buy rules, do-not-source

research/                   Captured vendor research, ~90 cited sources
  national-brands.md        Ashley, La-Z-Boy, Flexsteel
  highpoint-major-upholstery.md    18 major stationary resources
  highpoint-niche-upholstery.md    15 niche / design-led makers

data/                       Generated -- do not hand-edit
  sku_master.csv            All 65 SKUs with full specs, cost and margin
  frame_families.csv        19 families with construction, design note, RSA story
  cover_matrix.csv          Cover programs and orderable-SKU counts
  tradeup_lanes.csv         Lane rungs with step-up percentages

scripts/
  assortment_data.py        CANONICAL SOURCE OF TRUTH -- edit this
  build_data.py             Regenerates data/*.csv
  ladder_health.py          Assortment-level checks (margin, mix, lanes, covers)
  spec_checker.py           Construction audit, Layers 1-5, per family
  build_page.py             Renders docs/assortment.html from the data
```

## Usage

```bash
cd scripts
python3 build_data.py       # regenerate CSVs after editing assortment_data.py
python3 ladder_health.py    # exit 1 if any FAIL
python3 spec_checker.py     # exit 1 if any family is rejected
python3 spec_checker.py PEM QUI   # audit named families
```

No dependencies beyond the Python 3 standard library.

## How the validation works

**`ladder_health.py`** checks the assortment as a system: margin inside the
category × tier band for all 65 SKUs, tier mix and style balance, trade-up
step-ups large enough to perceive and small enough to cross, cover depth
matched to tier, and strict construction progression up the ladder. Intentional
departures are registered in the data with a stated reason, so they report as
decisions rather than warnings.

**`spec_checker.py`** audits each family across five layers. Layers 1–4 check
frame, suspension, cushion and fabric against tier minimums. Layer 5 builds the
product up from component benchmarks — arms, cushions, suspension, frame,
joinery, legs, fabric yardage, mechanism, labor, freight — and asks whether the
design can actually be manufactured inside the landed-cost envelope the retail
price allows. It tests every piece in a family, not just the anchor, because a
sofa can be comfortably buildable while the 7-seat modular on the same spec is
not.

Layer 5 rejected the first draft of this line in seven places. Two Best-tier
features were cut and nine SKUs repriced as a result — see
`docs/03-price-architecture.md`.

## Status and caveats

Zero construction failures, zero price-coherence failures, zero ladder flags.
Six families carry thin cost headroom and are listed as a watch list in
`docs/05-assortment-health.md`.

**Costs are modeled, not quoted.** `landed_cogs` is derived from each family's
target margin — planning numbers to prove the architecture before vendor RFQs.
Replace `margin_target` in `assortment_data.py` with quoted landed cost as
costing returns, then rerun both scripts.

**Known gaps:** no motion sectional (the largest single hole — reclining
sectionals are real mid-market volume and filling them properly needs 3–4 SKUs
beyond 65), and no $599 opening sofa. Both are documented with recommended
fills in `docs/05-assortment-health.md`.
