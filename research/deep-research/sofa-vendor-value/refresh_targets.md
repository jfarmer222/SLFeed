# Refresh targets: sofa-vendor-value

Run `update sofa-vendor-value` to re-check these and write a delta to
`diffs/YYYY-MM-DD_delta.md`. Suggested cadence: after the Oct 17–21, 2026
High Point Market, then quarterly.

## Entities to re-check

| Entity | What to check | Current value | Sources |
|---|---|---|---|
| H.M. Richards | Who owns it; does it still sell outside Rooms To Go | Rooms To Go majority stake (2015); site on RTG servers (2026) | 100, 101 |
| Ashley | Further plant closures; Good-tier spring vs platform models | Mesquite TX closed May 2026 | 40, 42, 52, 80 |
| Flexsteel | Lowest fabric power sofa street price; motor warranty | $3,010 lowest seen; 5-yr motors | 23, 37, 102 |
| Catnapper (Jackson) | Rockport / Burbank sectional prices and configs | $2,849 / $3,655 | 21, 22 |
| Southern Motion (Man Wah) | Ownership terms, West End price, warranty | $3,902; 3-yr motors | 20, 24 |
| Craftmaster | Thorne leather spec and warranty; Essentials sleeper mechanism and price | Sinuous + 2.0 lb standard; leather 1 yr; sleeper $1,699.99 | 60–64 |
| Best Home Furnishings | Swivel chair prices; 2026 Reader Rankings | 2025 "Best Swivel Chair Company" | 90 |
| England | Swivel chair entry price | Jess from $769 | 91 |
| Younger + Co | Quick Ship swivel prices | Not published | 95 |

## Numbers to refresh

- Section 232 upholstered furniture rate: 25%, step to 30% set for Jan 1, 2027 [87, 88].
- Competitor opening sofa prices: Rooms To Go $395–$499, Bob's $399, Living Spaces $195–$295 [49–51].
- Industry orders and shipments (Smith Leonard): 2025 orders flat, shipments −1% [11].

## Hypotheses to re-test

- H1: add sell-through data for power sectionals and swivels if the retailer's POS or Circana data becomes available.
- H2 (Ashley): look again for a domestic Good-tier stationary or sectional with a verified price and spring deck.
- H4: re-test once swaps are entered and `ladder_health.py` is rerun.

## Adversarial triggers (would change the answer)

- H.M. Richards confirmed independent of Rooms To Go → drop swap 5.
- Flexsteel line sheet shows a $2,799 fabric dual-power config → drop the Stratton reprice.
- Retailer data shows reclining sectionals under-index → cut swap 2 first, then swap 1.
- Younger swivel quote above $1,299 → drop swap 6.
