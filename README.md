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

---

# Slumberland Recliner Gallery — 65 SKUs

A second, separate line in this repository: the 65-SKU recliner assortment for
Slumberland's recliner gallery, built backwards from the customer and validated
against the Slumberland Category Architecture.

**This is not the upholstery line above.** Different category, different rules.
Most importantly: the stationary line caps national brands at 30% of the floor,
while recliners are national-brand **led** — La-Z-Boy holds 64% of slots by BIC
commitment. The recliner validator enforces a La-Z-Boy *floor*, not a national
*cap*. See conflict C-014.

## The line at a glance

| | Slots | Price range | Avg retail |
|---|---:|---|---:|
| Good — up to $399 | 5 | $349–$399 | $369 |
| Better — $400–$1,099 | 33 | $449–$1,099 | $754 |
| Best — $1,100+ | 5 | $1,299–$2,999 | $2,019 |
| Lift — parallel ladder | 9 | $599–$2,799 | $1,438 |
| **52 MDL slots** | **52** | | |
| Off-slot (promo, special buy, quick-ship, colour flex) | 13 | $299–$1,099 | $616 |
| **65 floored SKUs** | | **$299–$2,999** | |

**Brand mix across the 52 governed slots:** La-Z-Boy 33 (63%) · Ashley 7 ·
Franklin 7 · Flexsteel 5.

## The thesis

> **$299 gets the conversation. $699 gets the margin. $2,999 makes $899 look
> sensible.**

Good holds 11% of slots and returns 5% of sales. Best holds 11% and returns
**19%** — a 1.7x sales-per-slot premium. So the strategy is to advertise the
bottom of the ladder as loudly as the budget allows and make sure nobody who
walks in on a $299 ad stays at $299.

The structural move that makes it work: **the $299 does not get a slot.** The
merchandise matrix defines Target Slot Count as excluding special buys and
promotional items, so the doorbusters, special purchases and quick-ship chairs
are *floored but not slotted* — 13 of 65 SKUs, 0 of 52 slots. We can promote
$299 at full volume at zero cost in strategic slots.

## Layout

```
data/recliner_sku_master.csv      65 SKUs, generated — do not hand-edit
data/recliner_slots.csv           the 52-slot grid
data/recliner_tradeup_lanes.csv   9 lanes, one per customer job
data/recliner_color_matrix.csv    70/20/10

scripts/recliner_rules.py         every constraint + the conflict register
scripts/recliner_data.py          the 65 SKUs — CHANGE THINGS HERE
scripts/build_recliner_data.py    config -> CSV
scripts/recliner_health.py        11 check groups, exit 1 on FAIL
scripts/build_recliner_workbook.py -> 65_SKU_Recliner_Assortment_Map.xlsx

docs/recliners/01-customer-jobs.md        nine jobs, defined before any SKU
docs/recliners/02-price-architecture.md   the rails
docs/recliners/03-trade-up-ladder.md      why each step exists
docs/recliners/04-genz-millennial.md      the wide-appeal question
docs/recliners/05-lift-ladder.md          9 slots, own denominator
docs/recliners/06-color-cover.md          the only thing that varies by store
docs/recliners/07-conflicts-decisions.md  what still needs a decision

research/recliner-street-pricing.md       ~240 verified models, pulled 2026-09-12
research/highpoint-motion-recliner.md     showrooms, trend read, dropped vendors
```

## Build and validate

```sh
cd scripts
python3 build_recliner_data.py      # config -> data/*.csv
python3 recliner_health.py          # must exit 0
python3 build_recliner_workbook.py  # -> 65_SKU_Recliner_Assortment_Map.xlsx
```

`recliner_health.py` fails the build on: wrong SKU or slot counts, a tier
outside its price band, GBB drift beyond ±1 slot, La-Z-Boy below its floor, a
dropped vendor reappearing, a price step under $50, a tech reveal below $1,100,
an accelerator colour mid-ladder, or the $299 landing on a governed slot.

## Two decisions are still open

- **C-016 — the $299 doesn't verify.** Collage prices at $399.99, Joshua at
  $699.99, Randell at $1,149.99. The Special Purchase *program* is real; the
  $299 *price* is not. It is floored as a to-be-sourced special buy, flagged,
  with a verified Ashley doorbuster alongside it as cover.
- **C-017 — La-Z-Boy has no charging SKU at any price.** Franklin sells wireless
  charging at $768.99. Tech is held above $1,100 to keep the volume corridor
  anchor-brand-led; the cost is the under-35 story below $1,100.

Both are in `docs/recliners/07-conflicts-decisions.md` with the evidence.
