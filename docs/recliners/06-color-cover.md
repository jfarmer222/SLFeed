# Colour and Cover — The Only Thing That Varies by Store

## Why this file matters more than it looks

`20-rules/assortment-rules.md` requires store variation to be encoded as an
explicit rule, never inferred. For recliners the rule is:

> **Store flex = colour flex only.**
> *"Single assortment of 52 with flex on colour options by store."*
> — `30-categories/recliners.md`

Every store takes the same 52 slots, the same 65 floored SKUs, the same ladder.
**Colour is the single dimension a store manager can move.** That makes the
70/20/10 split the most operationally consequential thing in this build — it is
the only lever with local discretion, so it is the only one that can drift.

---

## The 70/20/10 split, as built

| Colour tier | What it is | Target | Actual | Actual % |
|---|---|---:|---:|---:|
| **Anchor** | High-velocity neutrals: greys, charcoals, greiges, taupes | 70% | 43 | 66.2% |
| **Bridge** | Textures and earth tones: cognac, walnut, olive, muted navy | 20% | 17 | 26.2% |
| **Accelerator** | Statement colours | 10% | 5 | 7.7% |

All three inside the ±7-point tolerance the validator enforces.

**Anchors are stocked deep.** They are what the customer buys when they are
buying a chair rather than a colour, and they are what an RSA reaches for when a
customer says "something neutral." Bridges add floor texture without risk.

---

## The accelerator rule — and why it is a hard constraint

**Accelerator colours are permitted only at Good and at Best. Never mid-ladder.**
The validator FAILS the build if one appears in Better.

The reason is the trade-up path. A customer walking the $449 → $1,099 corridor
is making one decision at a time: *is the next chair worth fifty more dollars?*
A statement colour mid-ladder changes the question to *do I like that colour?* —
and a customer who says no to a colour stops walking. Neutral rungs keep the
comparison about the chair.

At **Good** the accelerator is impulse: the price is already the argument, and a
colour can close it. At **Best** it is halo: the customer has stopped comparing
and started choosing, and a statement finish is part of what they are buying.

**The five accelerators, as placed:**

| SKU | Chair | Price | Tier | Why here |
|---|---|---:|---|---|
| R02 | Ashley Altari | $349 | Good | Impulse at the entry price |
| X02 | Ashley Nerviano Wall Hugging | $299 | Good (off-slot) | Doorbuster — colour helps it move |
| R42 | La-Z-Boy Contour SoCozi | $2,299 | Best | Halo, heat and massage |
| R43 | Flexsteel Everest Swivel Glider | $2,999 | Best | The ceiling |
| L09 | Flexsteel Zecliner 3+ Petite | $2,799 | Best (lift) | The lift ceiling |

---

## Cover — where the data runs out

This is the honest limit of the build.

**Neither Slumberland nor Homemakers publishes fibre content at the listing
level.** Of 65 SKUs, cover is stated on **12**. The rest carry `NOT STATED` —
not "unknown-so-assume-polyester," but literally not published. Treating missing
data as unknown rather than as a default is required by `CLAUDE.md`.

What *is* verified:

| Cover | Where | SKUs |
|---|---|---|
| Leather | La-Z-Boy Trouper / Greyson / Pinnacle / Roman / Contour | 5 |
| Refined leather | Flexsteel Perfect Match Refined | 1 |
| Performance fabric | Ashley ModMax | 1 |
| Soft chenille | Ashley Tulen | 1 |

**And the gap that matters: no boucle cover was verified on any recliner from
any governed brand at any price.** Boucle is the texture the under-35 customer
asks for by name. We cannot source it from public data.

### What this blocks

**Cover-gating cannot be decided from this dataset.** The classic upholstery
lever — same frame, three cover grades, three price points — needs published
cover grades and COM/COL yardage. Neither retailer publishes them and neither
vendor publishes prices. This has to come off line sheets.

That is not a failure of the research; it is a finding about what is knowable
publicly. The trade-up ladder in this build therefore runs on **mechanism and
scale**, with cover as a supporting reveal at $999 (leather) rather than as a
primary gating structure. When line sheets arrive, cover gating is the cheapest
available margin: the same frame in a better cover is a visible, touchable
upgrade at low incremental cost.

---

## Store-level colour flex — the operating rule

1. **The slot is fixed. The colourway is the store's.** A store may substitute a
   different colourway of the *same model* in the *same colour tier*. It may not
   substitute a different model, a different price, or a different tier.
2. **Anchor stays anchor.** A store cannot convert an anchor slot to an
   accelerator because a statement colour sold well once. That is how a floor
   loses its neutral spine.
3. **Accelerators stay at Good and Best.** No exceptions at store level; the
   constraint exists to protect the trade-up path, and the path is the same in
   every store.
4. **Deep stock follows anchors.** The 85% in-stock position against a 95% goal
   is most damaging on anchors, because that is where the volume is and where a
   substitution is least acceptable to the customer.
