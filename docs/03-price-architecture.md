# Price Architecture & Margin

## Working method

Every price in this line was set backwards from margin, then validated
forwards against a component build-up:

```
Allowable landed COGS = Target retail × (1 − target margin)
```

Then `scripts/spec_checker.py` builds the product up from component benchmarks
— arms, cushions, suspension, frame, joinery, legs, fabric yardage, mechanism,
labor and freight — and asks whether the silhouette being promised fits inside
that envelope. A family that passes its spec thresholds but fails this check is
the dangerous case: the spec sheet reads fine and the design cannot be built
for the money.

Six families were repriced and two Best-tier features were cut as a direct
result. See "What the audit changed" below.

## Retail bands

| Category | Good | Better | Best |
|---|---|---|---|
| Stationary sofa | $699–$899 | $1,199–$1,349 | $1,749–$1,899 |
| Sectional | $1,099–$1,399 | $1,599–$2,199 | $2,699–$3,499 |
| Recliner | $499 | $699–$899 | $1,299 |
| Reclining sofa | $999 | $1,449–$1,899 | $2,799 |
| Leather sofa | — | — | $2,299 |

## Margin

Rate rises at every tier, and margin dollars rise far faster:

| Tier | SKUs | Avg retail | Blended GM | Band | Status |
|---|---|---|---|---|---|
| Good | 19 | $731 | 49.3% | 48–52% | In band |
| Better | 29 | $1,198 | 52.3% | 50–54% (55% motion) | In band |
| Best | 17 | $1,967 | 54.7% | 52–58% (53–60% motion) | In band |

**Line blended margin: 52.8%.**

The margin dollar leverage is the whole point of the ladder:

| | Retail | GM% | GM$ | vs Good |
|---|---|---|---|---|
| Ashcroft sofa (Good) | $849 | 50.1% | $425 | — |
| Glenwood sofa (Better) | $1,299 | 53.0% | $688 | +62% |
| Pemberton sofa (Best) | $1,799 | 55.0% | $989 | +133% |

One Pemberton sale generates the margin of 2.3 Ashcroft sales. That is what
funds the floor space, the RSA training and the delivery network.

## Step-up discipline

The three stationary sofa lanes:

| Lane | Good → Better | Better → Best | Total |
|---|---|---|---|
| Classic (Ashcroft → Glenwood → Pemberton) | +53% | +38% | +112% |
| Modern (Brantley → Harlow → Quincy) | +50% | +46% | +119% |
| Casual (Cordell → Ivywood → Ravenswood) | +50% | +41% | +111% |

All three sit inside the 80–125% total-spread guidance. No single step exceeds
55%, and none falls below 29% — small enough to cross, large enough to fund a
real product improvement.

Motion runs 4 rungs and wider total spreads (+160% recliner, +180% reclining
sofa) because the manual-to-power transition warrants its own step. Judged on
consecutive steps rather than total spread, every motion rung lands between
+29% and +47%.

## Price-point gravity

Every retail in the line sits on a gravity point — $499, $699, $799, $899,
$1,099, $1,199, $1,299, $1,349, $1,449, $1,599, $1,699, $1,749, $1,799, $1,899,
$1,999, $2,199, $2,299, $2,699, $2,799, $3,199, $3,499. Nothing prices at
$1,150 or $1,675; those save the customer money without changing the mental
category they file the product under.

## What the audit changed

The Layer 5 price-coherence check rejected the first draft of this line in
seven places. Every one was a real problem, not a modeling artifact:

| Family | Finding | Resolution |
|---|---|---|
| **Pemberton** | 8-way hand-tied + down-blend seats + mortise-and-tenon + premium woven overran an $810 COGS budget by 28% | Cut hand-tying to pocketed coil; moved down from seats to back pillows; repriced $1,699 → $1,799 |
| **Quincy** | Coil-on-coil competed with the scoop arm and brass legs for the same budget | Cut coil cushion, kept coil suspension; repriced $1,599 → $1,749 |
| **Ravenswood** | Down-blend seats across 7 seating positions broke the Best sectional band outright | Down moved to back pillows; seats to 2.2 lb HR + fiber wrap |
| **Thorne** | Top-grain leather cannot be built inside the $1,399–$1,999 fabric-sofa band at a Best margin — hide alone is ~$330 of COGS | Repriced to $2,299 as a registered band exception; leather runs its own band, as the market prices it |
| **Stratton** | Two dual-motor mechanisms on a reclining sofa = $510 of COGS before anything else | Repriced $2,399 → $2,799 |
| **Northfield** | Same issue one tier down | Repriced $1,699 → $1,899 |
| **Glenwood, Ivywood, Oakhurst** | All three priced below what their own construction costs to build | Repriced up $100 each |
| **Fairhaven** | A $599 sofa is not buildable at Good spec with an in-band margin — materials plus import freight leave nothing | Opening sofa moved to $699. **See open item below.** |

## Open items

**No $599 opening sofa.** The line opens at $699. A $599 sofa at 48%+ margin
needs a landed cost near $305; a 3-seat sofa at entry spec models at ~$357 once
ocean freight is counted. Two honest ways to get the price point back:

1. Add an apartment-scale 2-seat sofa (~$549–$599) rather than discounting a
   3-seat build. Recommended — it fills the price point with a product that can
   actually carry the margin.
2. Accept a sub-48% loss-leader margin on one traffic SKU as a deliberate
   exception, and say so out loud rather than letting it look like drift.

**Two families run with no cost headroom.** Fairhaven (−0.3%) and Brantley
(+3.2%) have effectively zero room between modeled build-up and allowed COGS.
Any foam, freight or currency movement on these two has to be met with a price
move, not absorbed. They are the first SKUs to re-cost when input prices shift.

**Kingsley 5-Pc runs thin** (+1.3%) at $2,199, the top of the Better sectional
band. If its costs move, the piece either goes to Best or loses a cover grade.

## Caveat on cost

`landed_cogs` throughout is **modeled from target margin, not quoted**. These
are planning numbers to prove the architecture holds before vendor RFQs go out.
Replace `margin_target` in `scripts/assortment_data.py` with quoted landed cost
when vendor costing returns, then rerun both scripts. Component benchmarks in
`spec_checker.py` are directional and vary with vendor, volume and country of
origin — which is why the coherence check uses a 10% tolerance rather than
demanding a dollar-exact fit.
