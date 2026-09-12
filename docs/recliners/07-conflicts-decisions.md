# Conflicts and Open Decisions

`00-system/precedence.md` is explicit: *"Do not silently choose between
conflicting values. State the conflict and apply the precedence rules."* Every
contradiction found while building this assortment is recorded below with both
values, their basis, and what the build did about it.

**Two remain genuinely open and need a merchant decision. The rest are resolved
structurally — meaning both values survive and the build states which one
governs and why.**

---

## Open — requires a decision

### C-011 · La-Z-Boy 64% of slots vs. National Brand Mix 60%

| | Value | Source |
|---|---|---|
| La-Z-Boy share of slots | **64%** | BIC commitment, `30-categories/recliners.md` |
| National brand mix | **60%** | `40-evidence/recliners.md` G3 |

**These are not comparable.** One is a share of *floor slots*; the other is a
*product mix percentage* whose denominator is not stated in the source. If they
shared a denominator they would contradict — one brand cannot hold 64% of a
64%-national floor and leave room for Ashley, Flexsteel and Franklin.

**Build applied:** La-Z-Boy 64% of slots governs the map (33 of 52, as built).
The 60% national brand mix is reported and governed on nothing.

**Decision needed:** what is the denominator of "Natl Brand Mix %"? If it is
slots, the two records conflict and one is wrong. If it is units or sales, both
stand and the map is fine.

---

### C-012 · Good direction is "Grow" but Good target MDL equals current MDL

| | Value | Source |
|---|---|---|
| Good — Category Role Direction | **Grow** | `40-evidence/recliners.md` G2 |
| Good — current MDL share | 11% | `30-categories/recliners.md` |
| Good — target MDL share | **11%** | same |

A tier told to grow, with a slot target identical to its current slot count, is
a true contradiction — unless growth is meant to come from somewhere other than
slots.

**Build applied — recorded as Proposal, not policy:** Good grows *without slot
growth*. The 11% MDL share holds at 5 of 43 recliner slots, and Good's volume
grows through (a) the four off-slot promotional SKUs at $299 and $399, which the
matrix excludes from slot count, and (b) step-up capture out of Good into Better.

**Decision needed:** is that the intent? If the direction genuinely means "take
slots from Better," the target share is wrong and needs restating — and the
Better tier's "Hold" would have to change with it.

---

### C-016 · The $299 recliner does not exist at Slumberland today

| Claim in the architecture | Verified street price (2026-09-12) |
|---|---|
| "Vail and Collage $299" | Collage **$399.99** · Vail **$499.99** |
| "LAZY special purchases (Randell, Joshua) at $299" | Joshua **$699.99** · Randell **$1,149.99** |
| Doorbuster price point $299 | Lowest verified recliner in the governed set: Ashley Nerviano **$269.99** |

Source: `research/recliner-street-pricing.md`, primary source slumberland.com
brand-filtered collection pages.

**This may not be a contradiction at all.** `20-rules/promotion-rules.md` lists
$299 as the **doorbuster** — an event price — and $399 as the **promo price**.
La-Z-Boy Collage at $399.99 matches the promo price exactly. The "Special
Purchase" program is confirmed real: Slumberland's own page indexes as *"Joshua
Special Purchase Rocker Recliner."* What is not confirmed is that any special
purchase currently sits at $299.

**Build applied — per merchant direction:** the $299 stays in the map as a
**to-be-sourced special buy** (SKU `X01`), off-slot, flagged `NOT VERIFIED` with
the street evidence attached. A second $299 doorbuster (`X02`, Ashley Nerviano,
verified $269.99) is floored alongside it so the advertised price is deliverable
today even if X01 never closes.

**Owner:** Vendor Relations, to close X01 to a specific model at $299.
**Risk if it doesn't close:** the entire trade-up thesis starts one rung higher,
at $399. That still works — $399 is the matrix promo price and Collage verifies
there — but we lose the sub-$300 headline competitors will keep running.

---

### C-017 · The anchor brand cannot carry the tech story

La-Z-Boy holds 64% of the floor and has **no verified charging, USB-C, cup
holder or storage-arm SKU at any price.** Franklin has all three, well below
La-Z-Boy's price for comparable comfort:

| Feature | Franklin | La-Z-Boy |
|---|---|---|
| Wireless charging | **Gradin $768.99** | none verified |
| Storage arms + USB + cup holders | **Denali $1,259.99** | none verified |
| Built-in USB | **Magnus $759.99** | none verified |
| Heat + massage | Apex lift **$976.99** | SoCozi **$1,999.99** |

**Build applied — per merchant direction:** tech reveals are held **above
$1,100**. The $400–$1,099 corridor stays La-Z-Boy-led on comfort features
(rocker → hi-leg → wall-saver → swivel → power → headrest → lumbar), and tech
enters at $1,299 with Franklin Denali. The validator enforces it.

**The cost, stated plainly:** the under-35 customer transacts between $399 and
$699 and expects charging as table stakes. This decision puts it out of reach in
exactly that band. The chair that has it — Franklin Magnus at $749 with built-in
USB — is floored **off-slot**, which is a hedge, not a solution.

**Revisit trigger:** the moment La-Z-Boy will build a charging SKU in the $700s.
This is a negotiation item for the October Market, not an assortment problem.

---

## Resolved structurally — both values retained

### C-001 · Slot count: 52 committed vs. 60 observed vs. 65 floored

Unit mismatch, not contradiction — and the source settles it. The merchandise
matrix defines Target Slot Count as *"the total number of active MDL slots …
**excludes special buys, promotional, and in/out items.**"*

- **52** = governed MDL slots (BIC commitment, precedence rank 1) — as built
- **60** = prior observed programmed state, **−8 in transition**
- **65** = floored SKUs = **52 MDL + 13 off-slot**

Never averaged to 56. This reading is what makes the $299 promotion possible
without spending a strategic slot.

### C-013 · Lift inside the 65 changes the GBB denominator

Scope difference. `40-evidence/recliners.md` states the basis itself: *"GBB
Basis: based on recliner price."* GBB is therefore governed on the **43 recliner
slots** (5/33/5). The blended-with-lift view (5/37/10) is reported and governed
on nothing. Two columns, never one average.

### C-014 · The 30% national-brand cap does not carry into recliners

The existing 65-SKU upholstery line in this repository caps national brands at
30% of the floor. Recliners are national-brand-**led** by commitment: La-Z-Boy
64% of slots, PLW Strategy "Grow Brand Names," 70% national brand promo
allocation. `20-rules/gbb-rules.md`: *"do not force one enterprise price ladder
across categories."* The recliner validator therefore enforces a La-Z-Boy
**floor**, not a national **cap**.

### C-015 · Dropped vendors — and why the exclusion now looks prescient

`40-evidence/recliners.md`: *"MAWA and SOMO dropped from lineup."*

Man Wah acquired Southern Motion and Fusion in December 2025 ($32M, ~$58.7M
including debt). **Southern Motion filed Chapter 11 in the Northern District of
Mississippi on 3–4 September 2026** — nine days before this build — with $8.3M
owed to its top 20 unsecured creditors.

What was recorded as vendor rationalization now reads as supply risk avoided.
The exclusion holds, both companies are readable for trend intelligence only,
and any Man Wah-owned entity should carry a supply-continuity review before it
is floored. Details in `research/highpoint-motion-recliner.md`.

---

## Data gates — not conflicts, but they bound what this build can claim

### Cover composition is unknown for 53 of 65 SKUs

Neither retailer publishes fibre content at listing level. **No boucle cover was
verified on any recliner from any governed brand at any price.** Cover-gating —
the cheapest margin lever in upholstery — cannot be decided from public data. It
needs line sheets. See `06-color-cover.md`.

### Roughly a third of the model names in the brief do not exist as recliners

Makkah, Nezra and Earlbeck returned nothing. Ballyton is a sectional. Latitudes
is a Flexsteel line, not a chair. Chandler is Franklin, not Flexsteel. Sherman
is La-Z-Boy **and** Franklin, never Ashley. `Sherman`, `Aspen`, `Kent` and
`Top Tier` each appear under two brands.

**Operating rule: never key a SKU on model name alone.** Brand attribution in
this build comes from brand-filtered collection pages, never from combined
listings — Slumberland's combined listing mis-assigned brands in at least four
cases.

### Operational gates on the trade-up plan

| Gate | Current | Goal | Status |
|---|---|---|---|
| Lead time | 3.8 wks | 4 wks | on track |
| Fill rate | 3.9 days | 7 days | on track |
| **In-stock** | **85%** | **95%** | **GAP** |
| **Digital Commerce** | **F** overall, **F** images, **F** UPC, D+ copy | — | **urgent, 243 products** |

The ladder is only as good as the chair being there. A customer who researched a
specific chair, drove to the store to sit in it, and found an empty slot does not
come back — and at 85% in-stock that happens to roughly one customer in seven.

### Margin is modeled, not quoted

Every `margin_pct` in `data/recliner_sku_master.csv` is derived from tier
position, not from a vendor quote. It is a planning number used to prove the
price architecture holds together before costing comes back. Replace it with
quoted landed cost when line sheets arrive, then rerun `recliner_health.py`.

### Planned retail vs. verified street

`retail` is a **planned** retail. Every row carries the verified street price it
was anchored to and the retailer it came from. Two rows sit more than 15% above
verified street and should be confirmed before ticketing:

| SKU | Chair | Planned | Verified | Gap |
|---|---|---:|---:|---:|
| R42 | La-Z-Boy Contour SoCozi Power+ | $2,299 | $1,999.99 SLBD | +15% |
| R25 | La-Z-Boy Pinnacle Power Headrest | $799 | $918.99 HMKR | −13% |

Slumberland and Homemakers disagree by 20–50% on the same chair throughout the
dataset. That is two retailers with different cost bases and promo cadences, not
an error in either — but it means planned retail is a merchant decision, not a
transcription.
