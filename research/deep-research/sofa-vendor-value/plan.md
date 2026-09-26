# Plan: sofa-vendor-value

- **Depth:** medium
- **Genre:** decision
- **Opened:** 2026-09-26
- **Asked by:** line owner (SLFeed 65-SKU upholstery line)

## 1. Reframe

**Question as asked:** Are the vendors and SKUs picked for the 65-SKU line the
best-value sources for a mid-price furniture retailer?

**The decision behind it:** Which 6–8 one-for-one SKU swaps should go into the
line before RFQs and the October 17–21, 2026 High Point Market? Each swap must
make the line stronger in at least one of three ways:

1. **Selection:** fills a piece customers are buying that the line lacks.
2. **Clarity:** removes a piece that blurs the choice (duplicate, or an overlap
   between two rungs).
3. **Value:** same job, better spec or lower risk at the same retail, or a
   better vendor for that slot.

**Hard constraints** (from `scripts/ladder_health.py` and `assortment_data.py`).
Every swap package must still pass these:
- 65 SKUs total. Tier mix Good 25–35%, Better 40–50%, Best 20–30%.
- Each style territory 25–45%.
- National brands at or below 30% of SKUs (18 today, so 1 more at most).
- La-Z-Boy and Flexsteel are motion-only.
- Retail sits inside the category and tier price band, or is a registered exception.
- Margin sits inside the category and tier margin band.

**Out of scope:** re-designing families from scratch, re-costing (costs are
modeled, not quoted), and cover strategy.

## 2. Falsifiable hypotheses

- **H1 (selection):** Reclining sectionals, swivel chairs, and apartment-size
  sofas are real mid-market volume in 2025–26. If so, filling them beats keeping
  the lowest-value pieces now in the line.
  *Refuted if* trade and retailer evidence shows these are niche or falling.
- **H2 (value, national brands):** For at least one national-brand slot (Ashley
  Good stationary or sectional, Flexsteel Best motion), a High Point resource
  offers a better spec, a better warranty, or a more reachable price at the same
  retail. *Refuted if* the evidence shows the national brand wins on price and
  spec in that slot.
- **H3 (risk):** At least one assigned vendor has a status, ownership, lead-time
  or tariff change since the August 2026 research that makes it a weaker bet.
  *Refuted if* every assigned vendor checks out as stable.
- **H4 (clarity):** The line carries pieces that duplicate each other, such as
  the Harlow chair plus the Harlow accent chair, or three near-identical Good
  chairs. Those slots can be freed with little lost sales.
  *Mostly internal evidence. External support needed on add-on and chair sales
  patterns; mark under-determined if not found.*

## 3. Report structure (blocks)

1. The answer: 6–8 swaps in one table (out, in, vendor, price, why, evidence).
2. Rule check: tier mix, style mix, national cap after swaps.
3. Evidence by swap.
4. Hypotheses: confirmed, refuted, or under-determined.
5. Adversarial pass: the strongest case against each swap.
6. What this does not replace (line sheets, quotes).

## 4. Sourcing strategy

Five parallel search streams. Each source is saved to its own file, with
verbatim quotes. Source types: primary (vendor or retailer page, SEC or IR
filing), industry (trade press, market data), discussion (reviews, forums,
consumer testing).

| Stream | Scope | Source numbers |
|---|---|---|
| A. Demand | Category trends 2025–26: motion sectionals, swivel chairs, modular, apartment-size, performance fabric, price points | 01–19 |
| B. Motion | Power reclining sectionals and Best motion: La-Z-Boy, Flexsteel, Southern Motion, Catnapper, Franklin, others. Price, warranty, spec | 20–39 |
| C. Good tier | Ashley opening stationary and sectionals vs. domestic and import opening-price makers; $549–$599 apartment sofas | 40–59 |
| D. Leather and sleeper | Leather sofas $1,999–$2,499 and queen sleepers around $1,499: who gives the best value | 60–79 |
| E. Vendor status | Status changes since Aug 2026 for all 13 assigned vendors (closures, sales, tariffs, lead times, quick-ship); swivel and chair-and-a-half sources | 80–99 |

**Opposition queries (must run):** "reclining sectional sales decline",
"swivel chair trend over", "Flexsteel warranty better than La-Z-Boy",
"Ashley quality improved 2026", "small sofa returns", and similar. Look
for evidence that each swap is wrong.

## 5. Risk register

| Risk | Effect | How it's handled |
|---|---|---|
| Wholesale prices and line sheets are not public | Value calls rest on dealer street prices | Say so; compare like-for-like street prices only |
| Trade press is paywalled (Furniture Today) | Thin demand data | Use HFN / Home News Now, retailer earnings calls, public data |
| Swaps break the ladder rules | Recommendation is not usable | Check each swap package against the rules in section 1 |
| Stale August 2026 research | Wrong vendor status | Stream E re-checks |
| Single-dealer price samples | Biased value reads | Need 2+ dealers per price claim |

## 6. Stop criteria

- 6–8 swaps, each backed by 3+ independent sources of 2+ types, or clearly
  marked "insufficient evidence".
- Each hypothesis marked confirmed, refuted or under-determined.
- Adversarial pass done for every swap.
- Budget cap: one search round plus one targeted follow-up round.

## 7. Capability discovery (phase 3.5)

- Web search and fetch: WebSearch, WebFetch, Exa, Firecrawl (all available).
- No paid data APIs (Circana, Furniture Today data) are available. HTML only.
- Dealer sites sometimes return 403/429, as the August research found. Fall
  back to Firecrawl and to a second dealer.
- Search streams run on a cheaper model. Synthesis and the adversarial pass
  run on the main model.

## Changelog

- 2026-09-26: plan written.
- 2026-09-26: five search streams run in parallel (sources 01–96).
- 2026-09-26: follow-up round: H.M. Richards ownership (100, 101), Flexsteel price re-check (102).
  Source 47 marked misattributed and excluded; source 04 marked stale on the 30% tariff step.
- 2026-09-26: report `2026-09-26_decision.md`, findings F1–F6, `refresh_targets.md` written.
  Six swaps delivered (goal was 6–8). Chair-and-a-half dropped: one source only.
