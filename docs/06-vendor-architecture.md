# Vendor Architecture & Sourcing

Who supplies the 65 SKUs, why they were chosen, and what has to be confirmed
before anything is committed.

Underlying research, with ~90 cited source URLs and explicit "NOT PUBLISHED"
entries wherever the data did not exist:

- `research/national-brands.md` — Ashley, La-Z-Boy, Flexsteel
- `research/highpoint-major-upholstery.md` — 18 major stationary resources
- `research/highpoint-niche-upholstery.md` — 15 niche / design-led makers

## The principle

National brands anchor every tier. They buy price credibility the customer
already believes and they pull traffic. They also cost margin, and they are
exactly the SKUs every competitor down the road can show. So they are capped
at 30% and the rest of the floor comes from High Point resources, which is
where the differentiation and the margin live.

| Source type | SKUs | Share |
|---|---|---|
| National brand | 18 | 27.7% |
| Domestic specialist | 36 | 55.4% |
| Niche / design-led | 11 | 16.9% |

## National anchors

| Brand | Tier | Categories | SKUs | Showroom |
|---|---|---|---|---|
| Ashley | Good | Stationary, sectional, motion | 8 | IHFC H900 |
| La-Z-Boy | Better | **Motion only** | 7 | — |
| Flexsteel | Best | **Motion only** | 3 | IHFC C601 |

The motion-only restrictions on La-Z-Boy and Flexsteel are enforced in
`ladder_health.py`. Assigning either to a stationary family fails the build.

**La-Z-Boy validated cleanly.** All 7 SKUs land inside its observed dealer
range ($559–$2,599 recliners, $978–$1,769 manual reclining sofas,
$1,679–$2,590 power reclining sofas). No repricing was needed.

## High Point resources

| Vendor | Role | Tier | Showroom | SKUs | Why |
|---|---|---|---|---|---|
| H.M. Richards | Domestic | Good | Market on Green 205/206 | 4 | Cuts its own frames **and** its own foam — that vertical integration is how a domestic sofa lands at opening price |
| Hughes Furniture | Domestic | Good | Market on Main, 233 S. Main Fl 6 | 3 | Builds its own frames; opening-price domestic backbone |
| Albany Industries | Domestic | Good | COHP Hamilton 201/218 | 4 | 450+ employee Mississippi domestic |
| England Furniture | Domestic | Better | Plaza Suites 100 | 4 | **21-day custom quick-ship** — the best answer to delivery risk in this band. Publishes construction and starting prices (~$1,233 on Rochelle 4005) |
| Jackson Furniture | Domestic | Better | Plaza Suites 300 | 6 | 10 plants, 1,500+ people. Best free public spec data found — piece-by-piece frame tables, named coil-spring seating, Steel Tech framing |
| Best Home Furnishings | Domestic | Better | 239 S. Main | 7 | 1.1M sq ft Indiana domestic, 700+ fabrics, complete published dimensions |
| Craftmaster Essentials | Domestic | Better | Suites at Market Square M-4020 | 5 | Deepest cover library found; Blend-Down and 2.0 HD/HR foam; lifetime frame warranty |
| Craftmaster | Domestic | Best | 2622 Uwharrie Rd (own building) | 3 | Main line above Essentials; carries leather with published construction |
| Norwalk Furniture | Niche | Best | IHFC M108 | 8 | Employee-owned (ESOP 2021). 500+ frames × 800+ covers at a **35-day delivery target** — the custom story a national brand structurally cannot match |
| Younger + Co | Niche | Best | 220 Elm, Suite 214 | 3 | Bench-built NC, inputs sourced within 85 miles of the plant, SFI frames, CertiPUR foam. Quick Ship program: 6 sofa frames, 6 chairs, 21 fabrics rated 15k–100k Martindale |

### Platform sharing

Lanmore shares Jackson with Harlow, and Kingsley shares Best Home with
Ivywood. That is deliberate and it mirrors the design: those pairs already
share arm, legs and cover program, so sharing a vendor amortizes one tooling
and cover buy across a sofa family and its sectional.

## Vendor buy rules

Spec floors the buy must hold even where the vendor's own opener sits below
them. The cheapest thing a national brand makes is not automatically the thing
worth putting on the floor. Enforced as data in `assortment_data.py`.

**Ashley**
- **Sinuous spring minimum.** Ashley's opening stationary rides a *springless
  platform deck*, marketed as "3× better than a spring system" with no test
  standard cited. Those models are out of spec for this line and must not be
  substituted in on a cost-down. Fairhaven therefore buys *up* within Ashley
  at $699 rather than down to Ashley's observed $450–$516 opener — the extra
  ~$180 of retail is what the spring costs.
- **Do not take Ashley's upper motion** ($2,050–$3,200). It prices straight
  through La-Z-Boy's entire duo® line and collapses the ladder. Ashley motion
  stays at its $1,100–$1,400 opening band.

**La-Z-Boy**
- Confirm the lifetime mechanism warranty **in writing**. It is the strongest
  claim in the Better tier and is currently sourced only from dealer pages,
  never from La-Z-Boy directly.

**Flexsteel**
- Blue Steel Spring must be on the ticket and in the RSA story. It is the
  reason the tier costs what it costs.
- **Electrical and motors are warranted 5 years**, against La-Z-Boy's lifetime
  mechanism claim. At Best-tier retail that is the weakest point in the line.
  Press it in negotiation.
- Entry fabric power configurations only. The dealer pricing sampled was
  leather- and triple-power-heavy and is not our SKU.

**Younger + Co**
- Quote the **Quick Ship** program specifically. Do not accept the
  made-to-order sheet for QUI-SOF-X — Quick Ship prices below full custom by
  design, which is what makes $1,749 reachable.

## Do not source

Verified closed or materially changed. Recorded because **a High Point
directory listing is not evidence a company is trading.**

| Company | Finding |
|---|---|
| Klaussner | Closed August 2023. Confirmed absent from the current exhibitor roster. |
| Fusion Furniture | Closed 18 Dec 2025 under Man Wah ownership. Strong pure-stationary resource historically; program terms likely still in flux. |
| Leathercraft by OHD | **Closed permanently 31 Aug 2025 — and its showroom listing at 404 N. Wrenn St. was still live at time of research.** |
| Mitchell Gold + Bob Williams | Exhibits at IHFC G265, but this is a Surya-owned relaunch, not the pre-2023 company. Re-qualify from scratch; prior experience does not transfer. |

## Parent-company exposure

England is owned by La-Z-Boy Inc. It is *not* a national brand on the floor —
the customer never sees "La-Z-Boy" on an England sofa — so it does not count
against the 30% national cap. But it does concentrate exposure to one parent,
so both readings are reported. Largest parent exposures:

| Parent | SKUs | Share |
|---|---|---|
| Ashley | 8 | 12.3% |
| Norwalk Furniture | 8 | 12.3% |
| Best Home Furnishings | 7 | 10.8% |
| La-Z-Boy (incl. England) | 11 | 16.9% |

All well inside a 25% concentration threshold.

## What this research does **not** replace

Being blunt, because the goal was to avoid the trip to market.

**Showroom square footage does not exist publicly.** Zero of the 18 major
resources publish it. The only figures found anywhere were Bernhardt's 95,000
sq ft and an unverified ~150,000 for Ashley. Building and space numbers are
solid; size is not public. Scale here is judged on plants, employees and
manufacturing footprint instead — which is arguably the better proxy anyway,
but it is not what was asked for.

**No national brand publishes real MSRP or wholesale.** Every observed price
is a promotional "sale/was" pair or a dealer street price. For Flexsteel
specifically, prices and model numbers came from two sources with incompatible
naming — **you cannot currently quote a price against a Flexsteel model
number.**

**Foam density, fabric grades and motor counts are published by none of the
three national brands.** Only marketing adjectives — "high-resiliency",
"high-density", "high grade". No lb/ft³, no ILD, no double-rubs, no leather
grades. Motor counts appeared on 2 of ~45 SKUs. Retail price was verifiable
for only 3 of the 18 major resources; the rest are legitimately wholesale-only.

Those are precisely the specs that drive a 65-SKU buy. **This research tells
you exactly what to demand from each rep. It does not replace the line sheet
or the cost negotiation.**

**Two claims deliberately excluded:** Taylor King and Omnia are described as
8-way hand-tied only in third-party retailer copy, never by the companies
themselves. Do not repeat until confirmed.
