"""
Canonical source of truth for the 65-SKU Slumberland recliner gallery.

Everything downstream -- the CSV exports, the health checks, the workbook --
reads from this module. Change a SKU here and rerun build_recliner_data.py; do
not hand-edit the generated files in data/.

RETAIL is a PLANNED retail, not a copy of a live price. Every row carries the
verified street price it was anchored to (`street`) and its source retailer, so
the gap between plan and market is visible rather than hidden. Where planned
retail differs from verified street by more than 20%, the row says why.
See research/recliner-street-pricing.md for the full evidence, pulled
2026-09-12.

MARGIN is MODELED from tier position, not quoted. It is a planning number used
to prove the price architecture holds together before vendor costing comes
back. Replace with quoted landed cost when line sheets arrive, then rerun the
health checks.

Columns
  sku_id · slot_type (MDL|Off-slot) · slot_no · tier · brand · model · retail
  category (Recliner|Lift) · mechanism · cover · color_tier · customer_job
  trade_up_feature · strategic_segment · genz · margin_pct · street · notes
"""

GOOD, BETTER, BEST = "Good", "Better", "Best"
MDL, OFF = "MDL", "Off-slot"
REC, LIFT = "Recliner", "Lift"

# Modeled margin by tier. Best carries the most because it is the least
# discounted and the most brand-insulated; Good carries the least because it is
# bought to be advertised.
MARGIN = {GOOD: 44.0, BETTER: 51.0, BEST: 56.0}
LIFT_MARGIN = 53.0

# (sku_id, slot_type, slot_no, tier, brand, model, retail, category, mechanism,
#  cover, color_tier, customer_job, trade_up_feature, segment, genz, street, notes)
SKUS = [

# ============================ GOOD -- 5 MDL slots ============================
# Two price points, five slots. Good does not need price CHOICE, it needs price
# PROOF: several chairs at one number reads as a real price, not a bait price.

("R01", MDL, "R-01", GOOD, "Ashley", "Stayfish Rocker Recliner", 349, REC,
 "Manual rocker", "NOT STATED", "Anchor", "Cheap and now", "manual_rocker",
 "Value Anchor", "N", "$369.99 SLBD / $249.99 HMKR",
 "Opening MDL slot. Priced between the two retailers' street."),

("R02", MDL, "R-02", GOOD, "Ashley", "Altari Rocker Recliner", 349, REC,
 "Manual rocker", "NOT STATED", "Accelerator", "Not a recliner", "manual_rocker",
 "Under-35 Entry", "Y", "$349.99 HMKR",
 "Track arms -- the cleanest modern line available at this price. "
 "Accelerator colour permitted at Good."),

("R03", MDL, "R-03", GOOD, "La-Z-Boy", "Collage Rocker Recliner", 399, REC,
 "Manual rocker", "NOT STATED", "Anchor", "Cheap and now", "manual_rocker",
 "Brand-at-a-Price", "N", "$399.99 SLBD",
 "Lowest verified La-Z-Boy on the floor. THE advertised everyday price point -- "
 "matches the promo matrix's $399 exactly."),

("R04", MDL, "R-04", GOOD, "Ashley", "Kegler Rocker Recliner", 399, REC,
 "Manual rocker", "NOT STATED", "Anchor", "Cheap and now", "manual_rocker",
 "Value Anchor", "N", "$399.99 SLBD / $299.99 HMKR",
 "Second national-brand face at $399 so the price reads as a price, not a chair."),

("R05", MDL, "R-05", GOOD, "Ashley", "Tulen Rocker Recliner", 399, REC,
 "Manual rocker", "Soft chenille", "Bridge", "Not a recliner", "manual_rocker",
 "Under-35 Entry", "Y", "$339.99 HMKR",
 "Waterfall back, pillow-top arms, soft chenille. Merchandised in nursery "
 "gliders at Homemakers -- a small-scale signal we should be reading."),

# =========================== BETTER -- 33 MDL slots ==========================
# The volume engine: 78% of slots, 76% of sales. Fourteen price points, every
# step $50, one new reveal per rung.

# --- $449 · cover and tailoring upgrade off the Good anchor ---
("R06", MDL, "R-06", BETTER, "La-Z-Boy", "Hawthorn Rocker Recliner", 449, REC,
 "Manual rocker", "NOT STATED", "Anchor", "First real chair", "manual_rocker",
 "Step-Up Driver", "N", "$499.99 SLBD",
 "First step off the $399 anchor into the brand the customer came in asking "
 "for. Carried by La-Z-Boy rather than Ashley to hold the 64% slot commitment."),

("R07", MDL, "R-07", BETTER, "Franklin", "Kensington Rocker Recliner", 449, REC,
 "Manual rocker", "NOT STATED", "Anchor", "First real chair", "manual_rocker",
 "Step-Up Driver", "N", "$469.99 SLBD",
 "Base of Franklin's cleanest trade-up family: rocker $449 -> swivel $599 "
 "-> power $699."),

# --- $499 · PUSH-BACK HI-LEG ENTERS -- the first chair that isn't chair-shaped ---
("R08", MDL, "R-08", BETTER, "La-Z-Boy", "Charlotte High-Leg Recliner", 499, REC,
 "Push-back hi-leg", "NOT STATED", "Anchor", "Not a recliner", "pushback_hileg",
 "Silhouette Reveal", "Y", "$537.99 HMKR",
 "REVEAL: reads as an accent chair, not a recliner. Apartment scale. "
 "The cheapest answer we have to the under-35 objection."),

("R09", MDL, "R-09", BETTER, "La-Z-Boy", "Vail Rocker Recliner", 499, REC,
 "Manual rocker", "NOT STATED", "Anchor", "First real chair", "manual_rocker",
 "Brand Step-Up", "N", "$499.99 SLBD",
 "Named in the category file as a $299 entry; verified street is $499.99. "
 "See conflict C-016."),

# --- $549 · WALL-SAVER ENTERS -- the small-space answer ---
("R10", MDL, "R-10", BETTER, "La-Z-Boy", "Rowan Wall Recliner", 549, REC,
 "Wall-saver", "NOT STATED", "Anchor", "Will it fit", "wall_saver",
 "Space Saver", "Y", "$498.00 HMKR",
 "REVEAL: reclines from the wall. Rowan is also merchandised in nursery "
 "gliders -- a small-scale frame doing double duty."),

("R11", MDL, "R-11", BETTER, "La-Z-Boy", "Finley Wall Recliner", 549, REC,
 "Wall-saver", "NOT STATED", "Bridge", "Will it fit", "wall_saver",
 "Space Saver", "N", "$596.99 HMKR", ""),

# --- $599 · SWIVEL GLIDER ENTERS -- the strongest under-35 silhouette ---
("R12", MDL, "R-12", BETTER, "Franklin", "Kensington Swivel Rocking Recliner", 599,
 REC, "Swivel glider", "NOT STATED", "Anchor", "Not a recliner", "swivel_glider",
 "Silhouette Reveal", "Y", "$519.99 SLBD",
 "REVEAL: 360 swivel + glide. Exactly +$150 over the Kensington rocker -- "
 "the same frame, visibly different chair."),

("R13", MDL, "R-13", BETTER, "Ashley", "ModMax Swivel Glider Recliner", 599, REC,
 "Swivel glider", "Performance fabric", "Bridge", "Survive my life", "swivel_glider",
 "Performance Cover", "Y", "$478.00-$549.99 HMKR",
 "Performance fabric, easy clean. Serves the family/pet job and the "
 "under-35 silhouette job at once."),

("R14", MDL, "R-14", BETTER, "La-Z-Boy", "James Rocker Recliner", 599, REC,
 "Manual rocker", "NOT STATED", "Anchor", "First real chair", "manual_rocker",
 "Brand Step-Up", "N", "$599.99 SLBD", ""),

# --- $649 · swivel depth + scale ---
("R15", MDL, "R-15", BETTER, "La-Z-Boy", "Pinnacle Swivel Glider Recliner", 649,
 REC, "Swivel glider", "NOT STATED", "Anchor", "Not a recliner", "swivel_glider",
 "Silhouette Reveal", "Y", "$648.99 HMKR",
 "One of only two verified La-Z-Boy swivel gliders. The anchor brand is thin "
 "here and Franklin is not -- see docs/recliners/04-genz-millennial.md."),

("R16", MDL, "R-16", BETTER, "Franklin", "Brutus Oversized Snuggler Rocking Recliner",
 649, REC, "Manual rocker, cuddler", "NOT STATED", "Bridge", "Built my size",
 "manual_rocker", "Cuddler", "N", "$599.99 SLBD",
 "One of only two verified cuddler SKUs in the governed set, both Franklin. "
 "La-Z-Boy has none -- this is the gap-fill role the category file names."),

("R17", MDL, "R-17", BETTER, "La-Z-Boy", "Jasper Rocker Recliner", 649, REC,
 "Manual rocker", "NOT STATED", "Anchor", "First real chair", "manual_rocker",
 "Brand Step-Up", "N", "$649.99 SLBD", ""),

# --- $699 · POWER RECLINE ENTERS -- THE HINGE OF THE WHOLE LADDER ---
("R18", MDL, "R-18", BETTER, "Ashley", "Draycoll Power Rocker Recliner", 699, REC,
 "Power recline", "NOT STATED", "Anchor", "My chair", "power_recline",
 "Power Gateway", "N", "$649.99 SLBD",
 "REVEAL: POWER. The single most important rung on the floor. Ashley carries "
 "it because La-Z-Boy has no verified power below $918.99 -- see C-017."),

("R19", MDL, "R-19", BETTER, "La-Z-Boy", "Joshua Rocker Recliner", 699, REC,
 "Manual rocker", "NOT STATED", "Anchor", "First real chair", "manual_rocker",
 "Special Purchase", "N", "$699.99 SLBD",
 "Slumberland's page indexes as 'Joshua Special Purchase Rocker Recliner'. "
 "The Special Purchase PROGRAM is real; the $299 price in the brief is not. "
 "54 comfort positions, 3-position locking footrest, instant lumbar."),

("R20", MDL, "R-20", BETTER, "La-Z-Boy", "Reed Rocker Recliner", 699, REC,
 "Manual rocker", "NOT STATED", "Bridge", "First real chair", "manual_rocker",
 "Brand Step-Up", "N", "$699.99 SLBD", ""),

("R21", MDL, "R-21", BETTER, "La-Z-Boy", "Morrison Rocker Recliner", 699, REC,
 "Manual rocker", "NOT STATED", "Anchor", "My chair", "manual_rocker",
 "Core Comfort", "N", "$669.99 SLBD / $497.99 HMKR", ""),

# --- $749 · power depth ---
("R22", MDL, "R-22", BETTER, "Franklin", "Yogi Power Recliner", 749, REC,
 "Power recline", "NOT STATED", "Anchor", "My chair", "power_recline",
 "Power Depth", "N", "$729.99 SLBD", ""),

("R23", MDL, "R-23", BETTER, "La-Z-Boy", "Trouper Rocker Recliner", 749, REC,
 "Manual rocker", "NOT STATED", "Anchor", "My chair", "manual_rocker",
 "Core Comfort", "N", "$779.99 SLBD / $535.00 HMKR", ""),

("R24", MDL, "R-24", BETTER, "La-Z-Boy", "Astor Rocker Recliner", 749, REC,
 "Manual rocker", "NOT STATED", "Anchor", "Survive my life", "manual_rocker",
 "Scale + Comfort", "N", "$698.99 HMKR / $999.99 SLBD",
 "Deep wide seat, 3-cushion tall pillow back, padded flared arms. The two "
 "retailers are $300 apart on this chair -- planned retail sits between."),

# --- $799 · POWER HEADREST ENTERS ---
("R25", MDL, "R-25", BETTER, "La-Z-Boy", "Pinnacle Power Headrest Recliner", 799,
 REC, "Power recline + headrest", "NOT STATED", "Anchor", "My chair",
 "power_headrest", "Feature Reveal", "N", "$918.99 HMKR",
 "REVEAL: the headrest moves. La-Z-Boy's only verified simple-power rung "
 "below $1,200 -- the brand jumps straight to Tri-Power above this."),

("R26", MDL, "R-26", BETTER, "La-Z-Boy", "Pinnacle Rocker Recliner", 799, REC,
 "Manual rocker", "NOT STATED", "Anchor", "My chair", "manual_rocker",
 "Core Comfort", "N", "$799.99 SLBD",
 "Broadest sub-family in the La-Z-Boy line -- the workhorse slot."),

("R27", MDL, "R-27", BETTER, "La-Z-Boy", "Scarlett High Leg Reclining Chair", 799,
 REC, "Push-back hi-leg", "NOT STATED", "Bridge", "Will it fit", "pushback_hileg",
 "Silhouette Depth", "Y", "$729.99 SLBD", ""),

# --- $849 · scale and cover, not mechanism ---
("R28", MDL, "R-28", BETTER, "La-Z-Boy", "Pinnacle Wall Recliner", 849, REC,
 "Wall-saver", "NOT STATED", "Anchor", "Will it fit", "wall_saver",
 "Space Saver", "N", "$849.99 SLBD", ""),

("R29", MDL, "R-29", BETTER, "La-Z-Boy", "Randell Rocker Recliner", 849, REC,
 "Manual rocker", "NOT STATED", "Bridge", "Built my size", "manual_rocker",
 "Big & Tall", "N", "$777.99-$778.99 HMKR / $1,149.99 SLBD",
 "Oversized big-man seat, reinforced steel frame, 'engineered for taller "
 "users'. Named in the brief as a $299 special purchase -- it is not. C-016."),

# --- $899 · POWER LUMBAR ENTERS ---
("R30", MDL, "R-30", BETTER, "Ashley", "Rowlett Power Headrest + Lumbar Recliner",
 899, REC, "Power recline + headrest + lumbar", "NOT STATED", "Anchor",
 "Survive my life", "power_lumbar", "Feature Reveal", "N", "$657.00 HMKR",
 "REVEAL: power lumbar. The ergonomic story starts here."),

("R31", MDL, "R-31", BETTER, "La-Z-Boy", "Fulton Rocker Recliner", 899, REC,
 "Manual rocker", "NOT STATED", "Anchor", "My chair", "manual_rocker",
 "Core Comfort", "N", "$899.99 SLBD", ""),

("R32", MDL, "R-32", BETTER, "La-Z-Boy", "Kodie Rocker Recliner", 899, REC,
 "Manual rocker", "NOT STATED", "Bridge", "Survive my life", "manual_rocker",
 "Core Comfort", "N", "$899.99 SLBD", ""),

# --- $949 · power + scale ---
("R33", MDL, "R-33", BETTER, "Franklin", "Sultan Power Oversized Rocker Recliner",
 949, REC, "Power recline, oversized", "NOT STATED", "Anchor", "My chair",
 "power_recline", "Power + Scale", "N", "$949.99 SLBD", ""),

("R34", MDL, "R-34", BETTER, "La-Z-Boy", "Ava Rocker Recliner", 949, REC,
 "Manual rocker", "NOT STATED", "Anchor", "My chair", "manual_rocker",
 "Core Comfort", "N", "$899.99 SLBD", ""),

# --- $999 · LEATHER ENTERS ---
("R35", MDL, "R-35", BETTER, "La-Z-Boy", "Trouper Leather Rocker Recliner", 999,
 REC, "Manual rocker", "Leather", "Bridge", "Survive my life", "leather_match",
 "Cover Reveal", "N", "$999.99 SLBD",
 "REVEAL: leather. Wipe-clean, and the first cover upgrade the customer can "
 "feel without touching a button."),

("R36", MDL, "R-36", BETTER, "La-Z-Boy", "Dorian Rocker Recliner", 999, REC,
 "Manual rocker", "NOT STATED", "Anchor", "My chair", "manual_rocker",
 "Core Comfort", "N", "$999.99 SLBD", ""),

# --- $1,049-$1,099 · Better ceiling ---
("R37", MDL, "R-37", BETTER, "La-Z-Boy", "Greyson Leather Rocker Recliner", 1049,
 REC, "Manual rocker", "Leather", "Bridge", "My chair", "leather_match",
 "Leather Depth", "N", "$998.00-$999.99 HMKR", ""),

("R38", MDL, "R-38", BETTER, "La-Z-Boy", "Pinnacle Leather Rocker Recliner", 1099,
 REC, "Manual rocker", "Leather", "Anchor", "My chair", "leather_match",
 "Better Ceiling", "N", "$1,099.99 SLBD",
 "Top of Better. The last chair before the customer is deciding how much "
 "chair they want rather than which chair."),

# ============================ BEST -- 5 MDL slots ============================
# 11% of slots returning 19% of sales -- the best real estate in the gallery,
# and the reason the middle of the ladder reads as a value.

("R39", MDL, "R-39", BEST, "Franklin", "Denali Power Rocker Recliner", 1299, REC,
 "Power recline + headrest", "NOT STATED", "Anchor", "Does everything",
 "usb_charging", "Tech Reveal", "Y", "$1,259.99 HMKR",
 "REVEAL: TECH. Storage consoles in both arms, USB ports, cup holders, power "
 "headrest. Tech is held above $1,100 by merchant decision (C-017) because "
 "La-Z-Boy has no verified charging SKU at any price."),

("R40", MDL, "R-40", BEST, "Flexsteel",
 "Perfect Match Refined Leather Power Swivel Glider Recliner", 1599, REC,
 "Power recline + swivel glide + power headrest & lumbar", "Refined leather",
 "Bridge", "Does everything", "premium_leather", "Leather Grade Up", "Y",
 "$1,599.99 SLBD",
 "REVEAL: leather grade. The category file's named 2026 Best entry at $1,599 "
 "refined leather -- VERIFIED exactly. Swivel-glider silhouette at Best."),

("R41", MDL, "R-41", BEST, "La-Z-Boy", "Roman Leather Reclining Oversize Chair",
 1899, REC, "Manual, oversized", "Leather", "Anchor", "Built my size",
 "premium_leather", "Big & Tall Best", "N", "$1,899.99 SLBD",
 "The big-and-tall customer at Best. Sells without a discount."),

("R42", MDL, "R-42", BEST, "La-Z-Boy",
 "Contour Leather SoCozi Power+ Rocker Recliner", 2299, REC,
 "Power recline + headrest + SoCozi heat and massage", "Leather", "Accelerator",
 "Does everything", "massage", "Wellness", "N", "$1,999.99 SLBD",
 "REVEAL: heat and massage. The only verified heat/massage recliner in the "
 "governed set. Planned retail is 15% above verified street -- confirm before "
 "ticketing."),

("R43", MDL, "R-43", BEST, "Flexsteel", "Everest Power Swivel Glider Recliner",
 2999, REC, "Power recline + swivel glider", "NOT STATED", "Accelerator",
 "Does everything", "zero_gravity", "Halo Anchor", "Y", "$2,999.99 SLBD",
 "THE CEILING. Verified at exactly $2,999.99. A swivel glider at the top of "
 "the floor, which is the whole under-35 argument made in one chair: the most "
 "expensive recliner we sell does not look like a recliner."),

# ======================= LIFT -- 9 MDL slots, own ladder =====================
# +18.4% YoY against +4.5% for base recliners -- 3x the growth rate, on $4.47M
# of six-month written business. Never folded into the recliner GBB mix (C-013).

("L01", MDL, "L-01", BETTER, "La-Z-Boy", "Jean Lift Recliner", 599, LIFT,
 "Lift, 2-position", "NOT STATED", "Anchor", "Easier to stand",
 "lift_2position", "Lift Entry", "N", "$535.00 HMKR",
 "The price that makes lift approachable. Merchandised as comfort, never as "
 "medical equipment."),

("L02", MDL, "L-02", BETTER, "Flexsteel", "Granite Lift Chair Recliner", 749, LIFT,
 "Lift, 2-position", "NOT STATED", "Anchor", "Easier to stand",
 "lift_2position", "Lift Value", "N", "$749.99 SLBD", ""),

("L03", MDL, "L-03", BETTER, "La-Z-Boy", "Miller Lift Chair Recliner", 899, LIFT,
 "Lift, 3-position", "NOT STATED", "Anchor", "Easier to stand",
 "lift_3position", "Lift Step-Up", "N", "$868.00 HMKR",
 "Rolled arms, chaise seat and footrest, 300 lb capacity."),

("L04", MDL, "L-04", BETTER, "La-Z-Boy", "James Lift Recliner", 1099, LIFT,
 "Lift + power recline", "NOT STATED", "Bridge", "Easier to stand",
 "lift_power_recline", "Lift Power", "N", "$1,159.00 HMKR", ""),

("L05", MDL, "L-05", BEST, "La-Z-Boy", "Emerald Lift Chair Recliner", 1299, LIFT,
 "Lift + power recline", "NOT STATED", "Anchor", "Easier to stand",
 "lift_infinite", "Lift Comfort", "N", "$1,199.99 SLBD", ""),

("L06", MDL, "L-06", BEST, "Flexsteel", "Platinum Lift Recliner", 1499, LIFT,
 "Lift, infinite position", "NOT STATED", "Bridge", "Easier to stand",
 "lift_infinite", "Lift Position", "N", "$1,449.99 SLBD", ""),

("L07", MDL, "L-07", BEST, "La-Z-Boy",
 "Clayton Lift Recliner with Heat and Massage", 1799, LIFT,
 "Lift + heat + 6-motor massage", "NOT STATED", "Anchor", "Easier to stand",
 "lift_heat_massage", "Lift Wellness", "N", "$1,658.99 HMKR",
 "Two-temperature, two-position heat. The wellness rung of the lift ladder."),

("L08", MDL, "L-08", BEST, "Franklin", "Polaris Power Lift Chair Recliner", 2199,
 LIFT, "Lift + power, heavy duty", "NOT STATED", "Bridge", "Easier to stand",
 "lift_heavy_duty", "Lift Capacity", "N", "$2,199.99 SLBD",
 "Franklin also fields a 500 lb Independence lift at $1,416.99 if capacity "
 "needs a dedicated slot next review."),

("L09", MDL, "L-09", BEST, "Flexsteel",
 "Zecliner Model 3+ Petite Lift Recliner", 2799, LIFT,
 "Lift, sleep positioning", "NOT STATED", "Accelerator", "Easier to stand",
 "lift_sleep_wellness", "Halo Lift", "Y", "$2,799.99 SLBD",
 "The lift ceiling, and the only halo SKU on the floor with clinical backing: "
 "SleepScore Labs measured improvement across ~1,700 nights. 'Petite' is a "
 "small-scale frame -- the aging-in-place customer in an apartment."),

# ===================== OFF-SLOT -- 13 SKUs, 0 MDL slots ======================
# Floored but not slotted. The matrix defines Target Slot Count as EXCLUDING
# special buys, promotional and in/out items -- which is exactly what makes it
# possible to advertise $299 at full volume without spending a strategic slot.

("X01", OFF, "", GOOD, "La-Z-Boy", "Special Purchase Rocker Recliner (TBD)", 299,
 REC, "Manual rocker", "NOT STATED", "Anchor", "", "manual_rocker",
 "Doorbuster", "N", "NOT VERIFIED",
 "*** NOT VERIFIED — TO BE SOURCED. *** The category file names Vail and "
 "Collage at $299 and Randell/Joshua as $299 special purchases. None of those "
 "verified: Collage $399.99, Vail $499.99, Joshua $699.99, Randell $1,149.99. "
 "The Special Purchase PROGRAM is confirmed real. Vendor Relations owns "
 "closing this to a specific model at $299. See conflict C-016."),

("X02", OFF, "", GOOD, "Ashley", "Nerviano Wall Hugging Recliner", 299, REC,
 "Wall-saver", "NOT STATED", "Accelerator", "", "wall_saver",
 "Doorbuster", "Y", "$269.99 SLBD / $179.99 HMKR",
 "The only verified sub-$299 recliner in the governed set, and it is a "
 "wall-hugger -- an apartment chair at a doorbuster price. Event only."),

("X03", OFF, "", GOOD, "La-Z-Boy", "Collage Rocker Recliner (2nd colourway)", 399,
 REC, "Manual rocker", "NOT STATED", "Anchor", "", "manual_rocker",
 "Promo Price Point", "N", "$399.99 SLBD",
 "The matrix promo price point. Carries the advertised offer without taking "
 "a second MDL slot."),

("X04", OFF, "", GOOD, "Ashley", "Seyler Lane Rocker Recliner", 399, REC,
 "Manual rocker", "NOT STATED", "Bridge", "", "manual_rocker",
 "Promo Price Point", "N", "$389.99 SLBD", ""),

("X05", OFF, "", BETTER, "Ashley", "Stonemeade Recliner", 499, REC,
 "Manual", "NOT STATED", "Anchor", "", "manual_rocker",
 "Colour Flex", "N", "$499.99 SLBD",
 "Store-level colour flex. Store flex for this category is colour flex only."),

("X06", OFF, "", BETTER, "La-Z-Boy", "James Rocker Recliner (quick-ship)", 599,
 REC, "Manual rocker", "NOT STATED", "Anchor", "", "manual_rocker",
 "Quick-Ship", "N", "$599.99 SLBD",
 "Rapid-replenishment stocking SKU. NOTE: the La-Z-Boy quick-ship programme "
 "is named in the category file but was NOT VERIFIED as a published programme."),

("X07", OFF, "", BETTER, "Franklin", "Yogi Rocker Recliner", 649, REC,
 "Manual rocker", "NOT STATED", "Bridge", "", "manual_rocker",
 "Colour Flex", "N", "$629.99 SLBD", ""),

("X08", OFF, "", BETTER, "La-Z-Boy", "Jay Rocker Recliner (quick-ship)", 699, REC,
 "Manual rocker", "NOT STATED", "Anchor", "", "manual_rocker",
 "Quick-Ship", "N", "$699.99 SLBD", ""),

("X09", OFF, "", BETTER, "Franklin", "Magnus Power Rocker Recliner", 749, REC,
 "Power recline + adjustable headrest + USB", "NOT STATED", "Anchor", "",
 "power_recline", "Colour Flex", "Y", "$759.99 HMKR",
 "Built-in USB. Off-slot, so it does not violate the above-$1,100 tech rule "
 "for the governed ladder -- but it is the evidence that the rule costs us "
 "something. See C-017."),

("X10", OFF, "", BETTER, "La-Z-Boy", "Pinnacle Rocker Recliner (quick-ship)", 799,
 REC, "Manual rocker", "NOT STATED", "Anchor", "", "manual_rocker",
 "Quick-Ship", "N", "$799.99 SLBD", ""),

("X11", OFF, "", BETTER, "La-Z-Boy", "Fulton Rocker Recliner (quick-ship)", 899,
 REC, "Manual rocker", "NOT STATED", "Bridge", "", "manual_rocker",
 "Quick-Ship", "N", "$899.99 SLBD", ""),

("X12", OFF, "", BETTER, "Ashley", "Dash Power Recliner", 949, REC,
 "Power recline", "NOT STATED", "Anchor", "", "power_recline",
 "Colour Flex", "N", "$949.99 SLBD", ""),

("X13", OFF, "", BETTER, "La-Z-Boy",
 "Trouper Power Headrest & Lumbar Wall Recliner", 1099, REC,
 "Power recline + headrest + lumbar, wall-saver", "NOT STATED", "Anchor", "",
 "power_lumbar", "Colour Flex", "N", "$1,099.99 HMKR", ""),
]

FIELDS = ("sku_id", "slot_type", "slot_no", "tier", "brand", "model", "retail",
          "category", "mechanism", "cover", "color_tier", "customer_job",
          "trade_up_feature", "strategic_segment", "genz_flag", "margin_pct",
          "street", "notes")


def rows():
    """SKUS as dicts, with modeled margin filled in."""
    out = []
    for s in SKUS:
        (sku_id, slot_type, slot_no, tier, brand, model, retail, category,
         mechanism, cover, color_tier, job, feature, segment, genz,
         street, notes) = s
        margin = LIFT_MARGIN if category == LIFT else MARGIN[tier]
        # Off-slot promo inventory is bought to be advertised, not to earn.
        if slot_type == OFF and retail <= 399:
            margin -= 8.0
        out.append(dict(
            sku_id=sku_id, slot_type=slot_type, slot_no=slot_no, tier=tier,
            brand=brand, model=model, retail=retail, category=category,
            mechanism=mechanism, cover=cover, color_tier=color_tier,
            customer_job=job, trade_up_feature=feature,
            strategic_segment=segment, genz_flag=genz,
            margin_pct=round(margin, 1), street=street, notes=notes))
    return out
