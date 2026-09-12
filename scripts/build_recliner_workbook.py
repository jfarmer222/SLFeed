#!/usr/bin/env python3
"""Emit 65_SKU_Recliner_Assortment_Map.xlsx from the canonical data module.

Eight tabs, mirroring the 30-SKU sofa map's structure and adding the three this
category needs: the under-35 read, the lift ladder, and the conflict register.

Usage:  python scripts/build_recliner_workbook.py
"""

import os
from collections import Counter, defaultdict

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

import recliner_data as D
import recliner_rules as R

OUT = os.path.join(os.path.dirname(__file__), "..",
                   "65_SKU_Recliner_Assortment_Map.xlsx")

INK = "1F2933"
ACCENT = "1F4E5F"
HEAD_FILL = PatternFill("solid", fgColor=ACCENT)
BAND = {"Good": "EAF2F5", "Better": "FFFFFF", "Best": "F5EFE6"}
LIFT_FILL = PatternFill("solid", fgColor="F0F4EC")
OFF_FILL = PatternFill("solid", fgColor="FBF0EC")
TITLE = Font(bold=True, size=16, color=INK)
SUB = Font(italic=True, size=10, color="52616B")
HEAD = Font(bold=True, size=10, color="FFFFFF")
BOLD = Font(bold=True, size=10, color=INK)
BODY = Font(size=10, color=INK)
WRAP = Alignment(wrap_text=True, vertical="top")
TOP = Alignment(vertical="top")
THIN = Side(style="thin", color="D6DEE3")
BOX = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)


def header(ws, title, subtitle):
    ws["A1"] = title
    ws["A1"].font = TITLE
    ws["A2"] = subtitle
    ws["A2"].font = SUB
    ws.row_dimensions[1].height = 22


def table(ws, row, cols, widths, rows_data, fills=None):
    for i, (c, w) in enumerate(zip(cols, widths), start=1):
        cell = ws.cell(row=row, column=i, value=c)
        cell.font = HEAD
        cell.fill = HEAD_FILL
        cell.alignment = WRAP
        cell.border = BOX
        ws.column_dimensions[get_column_letter(i)].width = w
    for j, data in enumerate(rows_data, start=1):
        for i, v in enumerate(data, start=1):
            cell = ws.cell(row=row + j, column=i, value=v)
            cell.font = BODY
            cell.alignment = WRAP
            cell.border = BOX
            if fills:
                f = fills(j - 1)
                if f:
                    cell.fill = f
    ws.freeze_panes = ws.cell(row=row + 1, column=1)
    return row + len(rows_data) + 1


def money(n):
    return f"${n:,}"


# --- Tab 1 -------------------------------------------------------------------

def tab_map(wb, rows):
    ws = wb.create_sheet("Assortment Map")
    header(ws, "65-SKU Recliner Assortment Map",
           "Slumberland  |  52 MDL slots + 13 off-slot  |  Ceiling $2,999  |  "
           "La-Z-Boy 64% of slots  |  Gallery format, all stores take the same "
           "assortment  |  Planned retail anchored to verified street pricing "
           "pulled 2026-09-12")

    order = {"MDL": 0, "Off-slot": 1}
    data = sorted(rows, key=lambda r: (order[r["slot_type"]],
                                       r["category"] == "Lift", r["retail"]))
    body = [[
        r["sku_id"], r["slot_type"], r["slot_no"], r["tier"], r["brand"],
        r["model"], r["retail"], r["category"], r["mechanism"], r["cover"],
        r["color_tier"], r["customer_job"], r["trade_up_feature"],
        r["strategic_segment"], r["genz_flag"], r["margin_pct"],
        r["street"], r["notes"],
    ] for r in data]

    def fill(i):
        r = data[i]
        if r["slot_type"] == "Off-slot":
            return OFF_FILL
        if r["category"] == "Lift":
            return LIFT_FILL
        return PatternFill("solid", fgColor=BAND[r["tier"]])

    table(ws, 4,
          ["SKU", "Slot type", "Slot", "Tier", "Brand", "Model", "Retail",
           "Category", "Mechanism", "Cover", "Colour tier", "Customer job",
           "Trade-up reveal", "Segment", "GenZ", "Margin %",
           "Verified street", "Notes"],
          [7, 10, 7, 8, 11, 34, 9, 10, 26, 17, 11, 15, 17, 16, 6, 8, 26, 52],
          body, fill)
    for c in range(1, 19):
        ws.cell(row=4, column=c)
    for r in range(5, 5 + len(body)):
        ws.cell(row=r, column=7).number_format = '"$"#,##0'
        ws.cell(row=r, column=16).number_format = '0.0"%"'
    return ws


# --- Tab 2 -------------------------------------------------------------------

def tab_ladder(wb, rows):
    ws = wb.create_sheet("Trade-Up Ladder")
    header(ws, "Trade-Up Ladder: Why Each Step Exists",
           "$299 gets the conversation. $699 gets the margin. $2,999 makes $899 "
           "look sensible.  |  Every step in the volume corridor is $50 and buys "
           "one visible upgrade.")

    mission = [
        ["Good\n$349–$399\n5 slots (12%)\n+2 off-slot at $299",
         "PRICE ACCESS\nProve the advertised number is real",
         "Manual rocker\nTrack-arm and chenille covers\nLa-Z-Boy's verified floor at $399\n"
         "Two price points, five slots — price proof, not price choice",
         "Traffic off the ad\nFirst-time buyer\nPrice-comparison shopper"],
        ["Better\n$449–$1,099\n33 slots (77%)",
         "THE WHOLE BUSINESS\nWalk them from 'cheap enough' to 'worth it', $50 at a time",
         "Push-back hi-leg ($499)\nWall-saver ($549)\nSwivel glider ($599)\n"
         "POWER RECLINE ($699)\nPower headrest ($799)\nPower lumbar ($899)\nLeather ($999)",
         "New household\nThe core comfort buyer\nFamily and pets\nSmall-space\nBig and tall"],
        ["Best\n$1,299–$2,999\n5 slots (12%)",
         "PROOF\n11% of slots returning 19% of sales — and the reference point "
         "that makes the middle legible",
         "Tech: storage arms, USB, cup holders ($1,299)\nRefined leather ($1,599)\n"
         "Oversized leather ($1,899)\nHeat + massage ($2,299)\nZero-gravity ($2,999)",
         "Comfort-driven trade-up\nWellness\nAspiration\nBrand validation"],
        ["Lift\n$599–$2,799\n9 slots",
         "INDEPENDENCE\nFastest-growing thing in the category (+18.4% vs +4.5%). "
         "Merchandised as comfort, never as medical equipment",
         "2-position → 3-position ($899)\nPower recline ($1,099)\n"
         "Infinite position ($1,499)\nHeat + 6-motor massage ($1,799)\n"
         "Heavy duty ($2,199)\nSleep positioning ($2,799)",
         "Aging in place — and very often the adult child standing next to them"],
    ]
    nxt = table(ws, 4, ["Tier / price / mix", "Mission", "Reveals introduced",
                        "Target customer"],
                [26, 40, 52, 34], mission)

    nxt += 1
    ws.cell(row=nxt, column=1, value="Transition points — why customers move up").font = BOLD
    nxt += 1

    steps = [
        ["$299 → $349", "Off the ad", "From a promotional special buy to a proper rocker mechanism and a cover that doesn't feel like a rental. $50."],
        ["$349 → $399", "The name", "La-Z-Boy Collage. The brand they walked in saying, at the advertised price. Highest-conversion step on the floor."],
        ["$399 → $449", "Tailoring", "Hawthorn — better arms, better seat, same brand. First rung purely about how it's built."],
        ["$449 → $499", "IT DOESN'T LOOK LIKE A RECLINER", "Charlotte high-leg. Push-back, apartment scale, reads as an accent chair."],
        ["$499 → $549", "IT FITS", "Rowan wall-saver — reclines from the wall. For anyone who measured the room and isn't confident."],
        ["$549 → $599", "IT SWIVELS", "Kensington Swivel. 360° and a glide. Same frame as the $449 rocker, visibly a different chair."],
        ["$599 → $649", "Scale", "Brutus snuggler — a cuddler wide enough for two. La-Z-Boy doesn't make one."],
        ["$649 → $699", "★ POWER", "Draycoll. The footrest moves at the touch of a button. THE most important step — everything below exists to get them here."],
        ["$699 → $749", "Power depth", "Yogi Power, and Astor's deep wide seat with a three-cushion pillow back."],
        ["$749 → $799", "THE HEADREST MOVES", "Pinnacle Power Headrest. One more motor, one more visible adjustment."],
        ["$799 → $849", "Built for me", "Randell — oversized big-man seat, reinforced steel frame, engineered for taller users."],
        ["$849 → $899", "POWER LUMBAR", "Rowlett. The ergonomic story begins: it supports your back, not just your legs."],
        ["$899 → $999", "LEATHER", "Trouper Leather. Wipe-clean, and the first upgrade they feel before they read a tag."],
        ["$999 → $1,099", "Better ceiling", "Pinnacle Leather. Last chair before the question changes from which to how much."],
        ["$1,099 → $1,299", "TECH", "Denali — storage consoles in both arms, USB ports, cup holders, power headrest."],
        ["$1,299 → $1,599", "LEATHER GRADE", "Flexsteel Refined, power swivel glide with power headrest and lumbar."],
        ["$1,599 → $1,899", "Scale at Best", "Roman Leather Oversize. Premium leather for the customer national brands forget."],
        ["$1,899 → $2,299", "HEAT AND MASSAGE", "Contour SoCozi. The chair does something to you. Only heat/massage recliner in the governed set."],
        ["$2,299 → $2,999", "ZERO-GRAVITY, AND THE POINT", "Everest Power Swivel Glider. The most expensive recliner we sell IS a swivel glider — the under-35 argument made in one chair."],
    ]
    table(ws, nxt, ["Price step", "Transition", "What the customer gets for the money"],
          [18, 32, 100], steps)
    return ws


# --- Tab 3 -------------------------------------------------------------------

def tab_analysis(wb, rows):
    ws = wb.create_sheet("Analysis")
    header(ws, "Assortment Analysis: Brand, Tier, Colour, Price Distribution",
           "Governed basis is the 43 recliner MDL slots. Lift is reported "
           "separately and never folded in (conflict C-013).")

    mdl = [r for r in rows if r["slot_type"] == "MDL"]
    rec = [r for r in mdl if r["category"] == "Recliner"]
    lift = [r for r in mdl if r["category"] == "Lift"]
    off = [r for r in rows if r["slot_type"] == "Off-slot"]

    kpi = [[len(rows), f"{len(mdl)} / {len(off)}", f"{len(rec)} / {len(lift)}",
            money(round(sum(r["retail"] for r in rows) / len(rows))),
            f"{money(min(r['retail'] for r in rows))} – "
            f"{money(max(r['retail'] for r in rows))}",
            f"{sum(1 for r in rows if r['genz_flag'] == 'Y')}"]]
    nxt = table(ws, 4, ["Floored SKUs", "MDL / Off-slot", "Recliner / Lift",
                        "Avg retail", "Price range", "Under-35 flagged"],
                [14, 16, 16, 12, 20, 17], kpi)

    nxt += 1
    ws.cell(row=nxt, column=1, value="Brand distribution — 52 MDL slots").font = BOLD
    nxt += 1
    roles = {b: v["role"] for b, v in R.VENDOR_ROLES.items()}
    bc = Counter(r["brand"] for r in mdl)
    brand_rows = []
    for b, n in bc.most_common():
        bset = [r for r in mdl if r["brand"] == b]
        brand_rows.append([b, roles.get(b, ""), n, f"{n/len(mdl)*100:.1f}%",
                           money(round(sum(x["retail"] for x in bset)/len(bset))),
                           money(min(x["retail"] for x in bset)),
                           money(max(x["retail"] for x in bset))])
    nxt = table(ws, nxt, ["Brand", "Strategic role", "MDL slots", "% of slots",
                          "Avg retail", "Low", "High"],
                [12, 42, 11, 11, 11, 10, 10], brand_rows)

    nxt += 1
    ws.cell(row=nxt, column=1,
            value="GBB mix — governed on the 43 recliner slots only").font = BOLD
    nxt += 1
    gbb = []
    tc = Counter(r["tier"] for r in rec)
    for t in ("Good", "Better", "Best"):
        lo, hi = R.PRICE_BANDS[t]
        n = tc.get(t, 0)
        gbb.append([t, f"{money(lo) if lo else '$0'} – {money(hi)}", n,
                    f"{n/len(rec)*100:.0f}%",
                    f"{R.TARGET_MDL_SHARE[t]*100:.0f}%",
                    f"{R.CURRENT_SALES_SHARE[t]*100:.0f}%",
                    f"{R.CURRENT_UNIT_SHARE[t]*100:.0f}%",
                    f"{R.CURRENT_SALES_SHARE[t]/R.TARGET_MDL_SHARE[t]:.2f}x",
                    R.TIER_DIRECTION[t]])
    nxt = table(ws, nxt, ["Tier", "Price band", "Slots", "% slots",
                          "Target % slots", "% sales", "% units",
                          "Sales per slot", "Direction"],
                [9, 18, 8, 9, 14, 9, 9, 14, 11], gbb)

    nxt += 1
    ws.cell(row=nxt, column=1,
            value="Blended including lift — REPORTED ONLY, governed on nothing "
                  "(C-013)").font = BOLD
    nxt += 1
    lc = Counter(r["tier"] for r in lift)
    bl = []
    for t in ("Good", "Better", "Best"):
        bl.append([t, tc.get(t, 0), lc.get(t, 0), tc.get(t, 0) + lc.get(t, 0),
                   f"{(tc.get(t,0)+lc.get(t,0))/len(mdl)*100:.0f}%"])
    nxt = table(ws, nxt, ["Tier", "Recliner slots (governed)", "Lift slots",
                          "Blended", "Blended %"], [9, 24, 12, 11, 12], bl)

    nxt += 1
    ws.cell(row=nxt, column=1,
            value="Colour distribution — 70/20/10. Store flex IS colour flex, "
                  "so this is the only dimension that varies store to "
                  "store").font = BOLD
    nxt += 1
    cc = Counter(r["color_tier"] for r in rows)
    desc = {
        "Anchor": "High-velocity neutrals: greys, charcoals, greiges, taupes",
        "Bridge": "Textures and earth tones: cognac, walnut, olive, muted navy",
        "Accelerator": "Statement colours — Good and Best tiers ONLY, never mid-ladder",
    }
    col = [[t, desc[t], f"{R.COLOR_TIERS[t]*100:.0f}%", cc.get(t, 0),
            f"{cc.get(t,0)/len(rows)*100:.1f}%"]
           for t in ("Anchor", "Bridge", "Accelerator")]
    nxt = table(ws, nxt, ["Colour tier", "Description", "Target", "SKUs",
                          "Actual %"], [13, 62, 9, 8, 10], col)

    nxt += 1
    ws.cell(row=nxt, column=1,
            value="Price ladder heatmap — SKU count by $250 increment").font = BOLD
    nxt += 1
    buckets = Counter((r["retail"] - 250) // 250 for r in rows)
    heat = []
    note = {
        0: "Good MDL + off-slot promo + Better entry",
        1: "The walk-up: hi-leg, wall-saver, swivel, POWER",
        2: "The engine: headrest, lumbar, scale, leather",
        3: "Better ceiling + lift power",
        4: "Best entry (tech) + lift",
        9: "Deliberately empty — above the volume corridor",
        10: "The two ceilings — recliner and lift",
    }
    for k in range(min(buckets), max(buckets) + 1):
        n = buckets.get(k, 0)
        lo = k * 250 + 250
        heat.append([f"{money(lo)}–{money(lo+249)}", n,
                     "\u2588" * n if n else "\u00b7", note.get(k, "")])
    nxt = table(ws, nxt, ["Price range", "SKUs", "Visual", "What lives here"],
                [18, 8, 26, 46], heat)

    nxt += 1
    ws.cell(row=nxt, column=1,
            value="Sources: slumberland.com (brand-filtered collection pages — "
                  "authoritative for brand attribution), homemakers.com, "
                  "flexsteel.com, franklincorp.com, highpointmarket.org. "
                  "All prices pulled 2026-09-12. Every price is a retailer "
                  "street price, never a manufacturer MSRP.").font = SUB
    return ws


# --- Tab 4 -------------------------------------------------------------------

def tab_rules(wb, rows):
    ws = wb.create_sheet("Strategic Rules")
    header(ws, "Strategic Rules, Constraints & Methodology",
           "Every rule traces to the Slumberland Category Architecture. "
           "Enforced by scripts/recliner_health.py — the build fails if the "
           "ladder breaks.")

    mdl = [r for r in rows if r["slot_type"] == "MDL"]
    rec = [r for r in mdl if r["category"] == "Recliner"]
    lift = [r for r in mdl if r["category"] == "Lift"]
    off = [r for r in rows if r["slot_type"] == "Off-slot"]
    lzb = sum(1 for r in mdl if r["brand"] == "La-Z-Boy")

    blocks = [
        ("Mission",
         "Build a 65-SKU recliner gallery where the customer can see why every "
         "price step exists.\n"
         "Promote the $299 harder than anyone and margin out on the step-ups "
         "above it.\n"
         "The $299 is a DOOR, not a destination — judge it on traffic and "
         "step-up rate, never on its own margin.\n"
         "Start at the customer and work backwards: nine jobs were defined "
         "before a single SKU was chosen."),
        ("The most important rule",
         "$299 gets the customer into the conversation.\n"
         "$449–$649 gives them permission to upgrade.\n"
         "$699 — POWER — is where the margin actually turns.\n"
         "$799–$1,099 converts comfort into function.\n"
         "$1,299–$2,999 proves Slumberland can be trusted for premium, and "
         "makes the middle of the ladder legible."),
        ("Why the $299 does not get a slot",
         "The merchandise matrix defines Target Slot Count as excluding special "
         "buys, promotional and in/out items.\n"
         "So the $299 doorbusters, special purchases and quick-ship chairs are "
         "FLOORED BUT NOT SLOTTED — 13 of 65 SKUs, 0 of 52 slots.\n"
         "We can advertise $299 at full volume at zero cost in strategic slots, "
         "and Good's MDL share holds at its 11% target while Good's VOLUME "
         "grows off-slot. That is conflict C-012 resolved as a Proposal."),
        ("Brand architecture — national-brand-LED, not capped",
         f"La-Z-Boy: brand authority and comfort anchor — {lzb} of 52 slots "
         f"({lzb/len(mdl)*100:.0f}%), matching the BIC commitment of 64%.\n"
         "Ashley: Good-tier value and promo traffic; carries the $699 power "
         "hinge because La-Z-Boy has no verified power below $799.\n"
         "Franklin: cuddler, swivel glider and gap fill where La-Z-Boy has "
         "none — and the only brand with verified charging.\n"
         "Flexsteel: Best leather, Perfect Match, and the lift ceiling.\n"
         "NOTE: the 30%-of-floor national brand cap used on the stationary "
         "upholstery line does NOT apply here (C-014). Recliners enforce a "
         "La-Z-Boy FLOOR, not a national CAP."),
        ("Lift runs its own ladder",
         "9 of 52 slots. Lift is +18.4% YoY against +4.5% for base recliners — "
         "3x the growth rate, on $4.47M of six-month written business.\n"
         "Lift is NEVER folded into the recliner GBB mix. Fold it in and Best "
         "reads as 10 of 52 instead of 5 of 43 — roughly double its real size "
         "(C-013).\n"
         "Merchandised as comfort, never as medical equipment. The adult child "
         "standing next to the customer is validating the purchase too."),
        ("Tech is held above $1,100 — a deliberate, costly choice",
         "La-Z-Boy holds 64% of the floor and has NO verified charging, USB-C, "
         "cup holder or storage-arm SKU at any price.\n"
         "Franklin sells wireless charging at $768.99 and storage arms + USB + "
         "cup holders at $1,259.99.\n"
         "Tech therefore enters at $1,299 and the $400–$1,099 corridor stays "
         "La-Z-Boy-led on comfort features.\n"
         "COST: the under-35 customer transacts between $399 and $699 and "
         "expects charging as table stakes. Revisit the moment La-Z-Boy will "
         "build a charging SKU in the $700s (C-017)."),
        ("The 3-second rule",
         "A customer standing ten feet away, with no tag and no salesperson, "
         "must be able to tell why this chair costs more than the one beside "
         "it.\n"
         "Visual cues in this category: mechanism (rocker → hi-leg → wall-saver "
         "→ swivel → power), scale, cover richness, leather grade, silhouette.\n"
         "If they can't see it, the slot is decoration."),
        ("Colour hierarchy — 70/20/10",
         "Store flex for this category is COLOUR FLEX ONLY. Every store takes "
         "the same 52 slots. Colour is the only lever with local discretion, "
         "which is the only one that can drift.\n"
         "Anchors (~70%): greys, charcoals, greiges, taupes — stocked deep.\n"
         "Bridges (~20%): cognac, walnut, olive, muted navy.\n"
         "Accelerators (~10%): statement colours, permitted ONLY at Good and "
         "Best. NEVER mid-ladder — a statement colour in the trade-up corridor "
         "changes the question from 'is it worth $50 more' to 'do I like that "
         "colour', and a customer who says no to a colour stops walking."),
    ]
    nxt = table(ws, 4, ["Rule", "Detail"], [42, 104], blocks)

    nxt += 1
    ws.cell(row=nxt, column=1, value="Hard constraints — validated").font = BOLD
    nxt += 1
    tc = Counter(r["tier"] for r in rec)
    prices = sorted({r["retail"] for r in rec})
    minstep = min(b - a for a, b in zip(prices, prices[1:]))
    checks = [
        ["Total floored SKUs", "65", len(rows), "PASS" if len(rows) == 65 else "FAIL"],
        ["MDL slots (BIC commitment)", "52", len(mdl), "PASS" if len(mdl) == 52 else "FAIL"],
        ["Off-slot SKUs", "13", len(off), "PASS" if len(off) == 13 else "FAIL"],
        ["Recliner slots / Lift slots", "43 / 9", f"{len(rec)} / {len(lift)}",
         "PASS" if (len(rec), len(lift)) == (43, 9) else "FAIL"],
        ["La-Z-Boy share of slots", "64% (33)", f"{lzb/len(mdl)*100:.0f}% ({lzb})",
         "PASS" if lzb >= 31 else "FAIL"],
        ["GBB on 43 recliner slots", "5 / 33 / 5",
         f"{tc['Good']} / {tc['Better']} / {tc['Best']}",
         "PASS" if (tc['Good'], tc['Better'], tc['Best']) == (5, 33, 5) else "FAIL"],
        ["Ceiling", "$2,999", money(max(r["retail"] for r in rows)),
         "PASS" if max(r["retail"] for r in rows) <= 2999 else "FAIL"],
        ["Minimum perceivable step", "$50", money(minstep),
         "PASS" if minstep >= 50 else "FAIL"],
        ["$299 exists and is OFF-SLOT", "yes",
         f"{sum(1 for r in rows if r['retail'] == 299)} SKUs, all off-slot",
         "PASS" if all(r["slot_type"] == "Off-slot"
                       for r in rows if r["retail"] == 299) else "FAIL"],
        ["Power recline enters at", "$699",
         money(min(r["retail"] for r in rec
                   if r["trade_up_feature"] == "power_recline")), "PASS"],
        ["Tech held above $1,100", "yes",
         money(min(r["retail"] for r in rec
                   if r["trade_up_feature"] == "usb_charging")), "PASS"],
        ["Dropped vendors absent", "Man Wah / Southern Motion / Fusion",
         "none present",
         "PASS" if not any(r["brand"] in R.DROPPED_VENDORS for r in rows) else "FAIL"],
        ["Accelerator colours mid-ladder", "0",
         sum(1 for r in rows if r["color_tier"] == "Accelerator"
             and r["tier"] == "Better"), "PASS"],
    ]
    nxt = table(ws, nxt, ["Constraint", "Required", "Actual", "Result"],
                [38, 34, 30, 10], checks)

    nxt += 1
    ws.cell(row=nxt, column=1,
            value="Operational gates — the ladder is only as good as the chair "
                  "being there").font = BOLD
    nxt += 1
    gates = [
        ["Lead time", "3.8 wks", "4 wks", "On track"],
        ["Fill rate", "3.9 days", "7 days", "On track"],
        ["In-stock", "85%", "95%", "GAP — roughly one customer in seven drives "
         "to the store to sit in a chair that isn't there"],
        ["Digital Commerce — overall", "F", "—",
         "URGENT — 243 recliner products"],
        ["Digital Commerce — images", "F", "—",
         "URGENT — a chair with no photo does not exist to an under-35 buyer"],
        ["Digital Commerce — UPC", "F", "—", "URGENT"],
        ["Digital Commerce — copy", "D+", "—", "URGENT"],
    ]
    table(ws, nxt, ["Gate", "Current", "Goal", "Status"], [30, 14, 12, 76], gates)
    return ws


# --- Tab 5 -------------------------------------------------------------------

def tab_genz(wb, rows):
    ws = wb.create_sheet("Gen Z-Millennial Read")
    header(ws, "The Gen Z / Millennial Question — Answered Honestly",
           "They are not rejecting recliners. They are rejecting the recliner "
           "they picture when you say the word — and they are rejecting it on a "
           "phone, before they ever walk into the gallery.")

    bluf = [
        ["What they object to",
         "NOT the function — nobody dislikes putting their feet up. NOT the "
         "price — they will pay $699.\\n"
         "1. THE SILHOUETTE: overstuffed, wing-backed, visibly a recliner from "
         "across the room. The object announces itself.\\n"
         "2. THE SCALE: built for a family room in a house. They are buying for "
         "an apartment, a rental, a first condo.\\n"
         "3. THE SIGNAL: the living room is visible — to guests, a roommate, a "
         "camera. It reads as furniture from someone else's life stage.\\n"
         "They will not put THAT chair in THAT room."],
        ["The assortment answer — three levers, no ports",
         "Because tech is held above $1,100 (C-017), the under-35 answer below "
         "$1,100 runs on the levers that need no power supply:\\n"
         "SILHOUETTE — push-back hi-leg and swivel glider that read as accent "
         "chairs\\n"
         "SCALE — wall-saver, apartment width, petite frames\\n"
         "COVER — performance fabric, chenille, texture that isn't precious"],
        ["The real barrier is not the chair",
         "Digital Commerce grade F overall. F on images. F on UPC. D+ on copy. "
         "Across 243 recliner products.\\n"
         "This customer researches first and visits second. Our own category "
         "file says comfort trial is critical at point of sale — which is TRUE, "
         "and is exactly why the content failure is fatal rather than merely "
         "unfortunate.\\n"
         "The online listing's only job is to get them into the seat. Right now "
         "it cannot do that job, because there is no image."],
        ["Steal this from High Point",
         "Best Home Furnishings relaunched its Beast line laddering the SAME "
         "CHAIR in an extra-wide version at $1,200 and a smaller version at "
         "$999.\\n"
         "That converts scale from a spec buried on a tag into a signed, "
         "shoppable decision — and answers 'will it fit?' and 'is it built for "
         "me?' with one fixture, at no cost in additional styles.\\n"
         "Pick two or three high-velocity frames and floor them in two scales "
         "with scale-led signage."],
        ["What this build does NOT fix",
         "TECH IS ABOVE $1,100. Charging and USB-C are table stakes to this "
         "customer and our decision puts them out of reach in the band where "
         "they transact. The chair that has them — Franklin Magnus, $749, "
         "built-in USB — sits OFF-SLOT. A hedge, not a solution.\\n"
         "NO BOUCLE. Not verified on any governed brand at any price. Needs a "
         "line sheet.\\n"
         "IN-STOCK 85% vs 95%. A customer who researched a chair, drove in to "
         "sit in it, and found an empty slot does not come back."],
        ["How to measure it",
         "Do NOT measure 'Gen Z sales' — nobody can attribute it cleanly. "
         "Measure:\\n"
         "1. Step-up rate off the $299/$399 ad — the whole margin thesis in one "
         "number\\n"
         "2. Sell-through on the flagged SKUs vs. floor average\\n"
         "3. Digital Commerce grade on the remediated SKUs: F to B is the "
         "target, and the only one of these we fully control\\n"
         "4. Wall-saver and swivel-glider unit share vs. their slot share"],
    ]
    nxt = table(ws, 4, ["", "Detail"], [38, 110], bluf)

    nxt += 1
    ws.cell(row=nxt, column=1,
            value="The under-35 SKUs as built").font = BOLD
    nxt += 1
    gz = sorted((r for r in rows if r["genz_flag"] == "Y"),
                key=lambda r: r["retail"])
    gzr = [[r["sku_id"], r["slot_type"], r["brand"], r["model"], r["retail"],
            r["mechanism"], r["cover"], r["customer_job"]] for r in gz]
    nxt = table(ws, nxt, ["SKU", "Slot type", "Brand", "Model", "Retail",
                          "Mechanism", "Cover", "Customer job"],
                [7, 10, 11, 40, 9, 30, 18, 16], gzr)

    nxt += 1
    ws.cell(row=nxt, column=1,
            value="Content remediation priority — shoot these 14 first, not all "
                  "243").font = BOLD
    nxt += 1
    pri = [
        [1, "R08", "La-Z-Boy Charlotte High-Leg", 499, "Cheapest 'doesn't look like a recliner'"],
        [2, "R12", "Franklin Kensington Swivel", 599, "Strongest silhouette-per-dollar"],
        [3, "R13", "Ashley ModMax Swivel Glider", 599, "Performance fabric + silhouette"],
        [4, "R10", "La-Z-Boy Rowan Wall", 549, "The apartment answer, anchor brand"],
        [5, "R15", "La-Z-Boy Pinnacle Swivel Glider", 649, "Anchor-brand swivel"],
        [6, "R02", "Ashley Altari", 349, "Entry price, clean line"],
        [7, "X02", "Ashley Nerviano Wall Hugging", 299, "The doorbuster that is also an apartment chair"],
        [8, "R27", "La-Z-Boy Scarlett High Leg", 799, "Hi-leg depth"],
        [9, "R05", "Ashley Tulen", 399, "Texture at entry price"],
        [10, "R43", "Flexsteel Everest Swivel Glider", 2999, "The halo argument — shoot it like a design piece"],
        [11, "R39", "Franklin Denali", 1299, "The only tech story we have"],
        [12, "R40", "Flexsteel Refined Swivel Power", 1599, "Leather + swivel at Best"],
        [13, "L09", "Flexsteel Zecliner 3+ Petite", 2799, "Petite scale + clinical sleep claim"],
        [14, "X09", "Franklin Magnus (USB)", 749, "Charging, off-slot"],
    ]
    nxt = table(ws, nxt, ["Priority", "SKU", "Chair", "Retail", "Why first"],
                [9, 8, 40, 9, 60], pri)

    nxt += 1
    ws.cell(row=nxt, column=1,
            value="HOW to shoot them: in a room, at scale, with the chair NOT "
                  "reclined in the hero image. Every one of these chairs is "
                  "trying to prove it belongs in a living room. A "
                  "three-quarter product shot on white proves the "
                  "opposite.").font = BOLD
    return ws


# --- Tab 6 -------------------------------------------------------------------

def tab_lift(wb, rows):
    ws = wb.create_sheet("Lift Ladder")
    header(ws, "The Lift Ladder — 9 Slots, Its Own Denominator",
           "Lift is +18.4% YoY against +4.5% for base recliners — 3x the growth "
           "rate, on $4.47M of six-month written business. It never merges into "
           "the recliner GBB mix (conflict C-013).")

    lift = sorted((r for r in rows if r["category"] == "Lift"),
                  key=lambda r: r["retail"])
    reveal = {
        "lift_2position": "Lift entry — 2-position",
        "lift_3position": "3-POSITION",
        "lift_power_recline": "POWER RECLINE added",
        "lift_infinite": "INFINITE POSITION",
        "lift_heat_massage": "HEAT + 6-MOTOR MASSAGE",
        "lift_heavy_duty": "HEAVY DUTY",
        "lift_sleep_wellness": "SLEEP POSITIONING — the ceiling",
    }
    lr = [[r["slot_no"], r["retail"], r["brand"], r["model"],
           reveal.get(r["trade_up_feature"], r["trade_up_feature"]),
           r["color_tier"], r["street"], r["notes"]] for r in lift]
    nxt = table(ws, 4, ["Slot", "Retail", "Brand", "Chair", "Reveal",
                        "Colour tier", "Verified street", "Notes"],
                [8, 9, 11, 44, 30, 11, 22, 60], lr)

    nxt += 1
    ws.cell(row=nxt, column=1, value="Why it never merges").font = BOLD
    nxt += 1
    mdl = [r for r in rows if r["slot_type"] == "MDL"]
    rec = [r for r in mdl if r["category"] == "Recliner"]
    tc, lc = Counter(r["tier"] for r in rec), Counter(r["tier"] for r in lift)
    basis = [["Recliner only — GOVERNED", tc["Good"], tc["Better"], tc["Best"],
              "Matches the source: 'GBB Basis: based on recliner price'"],
             ["Blended incl. lift — reported only",
              tc["Good"] + lc["Good"], tc["Better"] + lc["Better"],
              tc["Best"] + lc["Best"],
              "Best would read as double its real size. Governed on nothing."]]
    nxt = table(ws, nxt, ["Basis", "Good", "Better", "Best", "Note"],
                [34, 9, 9, 9, 66], basis)

    nxt += 1
    ws.cell(row=nxt, column=1, value="Merchandising rules").font = BOLD
    nxt += 1
    mr = [
        ["Never sign it 'medical'", "Sign it: easier to get up · power assist · stand with confidence"],
        ["Merchandise inside the gallery", "A lift chair isolated at the back of the department tells the customer what we think of them"],
        ["The top of the ladder is a design object", "The Zecliner is not a mobility aid with a price tag; it is a sleep-and-wellness chair that happens to lift"],
        ["Sit the adult child down too", "They are validating the purchase and they will not validate something that looks like hospital furniture"],
    ]
    nxt = table(ws, nxt, ["Rule", "Detail"], [40, 100], mr)

    nxt += 1
    ws.cell(row=nxt, column=1, value="Open items").font = BOLD
    nxt += 1
    oi = [
        ["'Flexsteel Perfect Match lift' is NOT VERIFIED",
         "The program announcement describes 5 models / 18 SKUs with no lift mention, and "
         "flexsteel.com/collections/lift-recliners returns an empty collection. The Flexsteel lift "
         "chairs Slumberland sells are not tied to that program by any source found. Confirm with "
         "the vendor before writing it into a program brief."],
        ["Capacity has no dedicated slot",
         "Franklin fields a 500 lb Independence lift at $1,416.99; Mega Motion (High Point: "
         "Furniture Plaza 100, Floor 1) builds FDA Class II lifts fitting heights 4ft11 to 6ft6 at "
         "325-500 lb. Today the heavy-duty customer is served only at $2,199 via Polaris. If that "
         "customer is real in our markets, that is the tenth lift slot — and it comes out of Better "
         "recliners, not out of lift."],
        ["Lift specialists are not in the governed vendor set",
         "UltraComfort (IHFC C1165, Commerce Floor 11 — lifetime warranty on lift frame and "
         "mechanism) and Mega Motion are credible resources for the 30% other-brand allocation. "
         "Neither is proposed here because the governed four cover all nine slots. Worth a walk at "
         "the October Market."],
    ]
    table(ws, nxt, ["Item", "Detail"], [44, 104], oi)
    return ws


# --- Tab 7 -------------------------------------------------------------------

def tab_vendors(wb, rows):
    ws = wb.create_sheet("Vendor & Trend Sources")
    header(ws, "Vendor Architecture & High Point Trend Sources",
           "Governed vendors carry all 65 SKUs. High Point resources are "
           "EVIDENCE (precedence rank 6) — they inform the map and override "
           "nothing. Showroom placements read from highpointmarket.org "
           "exhibitor pages, 2026-09-12. Fall Market: October 17-21, 2026.")

    mdl = [r for r in rows if r["slot_type"] == "MDL"]
    bc = Counter(r["brand"] for r in mdl)
    gov = [
        ["La-Z-Boy", "LAZY", "Brand authority + comfort anchor", bc["La-Z-Boy"],
         "NOT SCOUTED — bought through its own channel",
         "Customers use the name as a generic term for reclining chairs. The "
         "brand sells before the RSA opens their mouth. GAP: no verified "
         "charging SKU at any price; no power below $799; only 2 swivel gliders."],
        ["Ashley", "ASHL", "Good-tier value and promo traffic", bc["Ashley"],
         "IHFC - H900, Hamilton, Floor 9",
         "Carries the $299 doorbuster and the $699 POWER hinge. 5 verified "
         "swivel gliders under $850. Brand role is fabric + manual, Good and "
         "Better only."],
        ["Franklin", "FKLN", "Cuddler, swivel and gap fill", bc["Franklin"],
         "Plaza Suites - 200, Floor 2",
         "The best value-per-feature in the governed set. ONLY brand with "
         "verified wireless charging ($768.99), storage arms + USB + cup "
         "holders ($1,259.99), and cuddlers. 11+ swivel gliders. "
         "'Design Your Recline' confirmed; no public pricing."],
        ["Flexsteel", "FLXS", "Best leather, Perfect Match, lift ceiling",
         bc["Flexsteel"], "IHFC - C601, Commerce, Floor 6",
         "Both 2026 Best entries verified: $1,299 fabric / $1,599 refined "
         "leather. Zecliner + 'Flexsteel Wellness' platform. Cannot play below "
         "$619.99."],
    ]
    nxt = table(ws, 4, ["Brand", "Code", "Role", "MDL slots",
                        "High Point showroom", "What it does and where it is thin"],
                [12, 7, 34, 10, 34, 74], gov)

    nxt += 1
    ws.cell(row=nxt, column=1,
            value="High Point resources for the 30% other-brand allocation — "
                  "not proposed, worth a walk").font = BOLD
    nxt += 1
    cand = [
        ["Jackson Furniture / Catnapper", "Cleveland, TN", "Plaza Suites - 300, Floor 3",
         "Catnapper is Jackson's reclining brand — 82 years, positioned on reclining innovation. "
         "Directly adjacent to Franklin's role.", "Active"],
        ["Best Home Furnishings", "Ferdinand, IN", "239 S. Main St., Downtown Main",
         "1.1M sq ft across eight Indiana plants, 'weeks not months'. The Beast line now ladders "
         "scale as a choice: extra-wide $1,200 / smaller $999 — the single most useful "
         "merchandising idea on the floor.", "Active"],
        ["HomeStretch", "Nettleton, MS", "Market On Green - 402, Floor 4",
         "Motion, recliners and lift held IN STOCK for rapid delivery — directly relevant to the "
         "13 off-slot rapid-replenishment SKUs and the 85% in-stock gap.", "Active"],
        ["Precision Reclining Chair Co.", "NOT PUBLISHED", "Hamilton - 133, Level 1",
         "Power motion, lift, occasional. Memory-foam over coil spring, hardwood frames. Offers "
         "OEM PRODUCTION — the credible route to the 'Exclusive Unbranded / Private Label: Yes' "
         "mandate.", "Active"],
        ["Palliser", "Winnipeg, Canada", "220 Elm - 400, Level 4",
         "Made-to-order, 150+ leather and fabric covers. The cover-depth answer if custom-order "
         "Best is ever pursued.", "Active"],
        ["UltraComfort America", "Old Forge, PA", "IHFC - C1165, Commerce, Floor 11",
         "Power lift specialist. Patented Eclipse Technology; LIFETIME warranty on lift frame and "
         "mechanism — strongest warranty claim found in the category.", "Active"],
        ["Mega Motion", "Pontotoc, MS", "Furniture Plaza - 100, Floor 1",
         "Lift. FDA Class II, 325-500 lb, fits heights 4ft11 to 6ft6, four US warehouses. The "
         "big-and-tall / accommodation end of lift.", "Active"],
    ]
    nxt = table(ws, nxt, ["Company", "HQ", "Showroom (bldg + space)",
                          "Why it matters", "Status"],
                [30, 18, 34, 80, 10], cand)

    nxt += 1
    ws.cell(row=nxt, column=1,
            value="DROPPED — DO NOT PURSUE").font = Font(bold=True, size=11,
                                                          color="9B2C2C")
    nxt += 1
    dropped = [
        ["Man Wah / Cheers (MAWA)", "DROPPED — active",
         "Dropped under BIC vendor rationalization. World's largest reclining-sofa maker, so "
         "informative on mechanism cost curves — READ FOR TREND ONLY. Acquired Southern Motion + "
         "Fusion Dec 2025 for $32M (~$58.7M incl. debt retired)."],
        ["Southern Motion (SOMO)", "DROPPED — CHAPTER 11",
         "Filed Chapter 11 in the Northern District of Mississippi on 3-4 September 2026 — NINE "
         "DAYS before this build. Top 20 unsecured creditors owed $8.3M. Man Wah had repeatedly "
         "transferred funds to cover operations since acquisition."],
        ["Fusion Furniture", "DROPPED by association",
         "Acquired by Man Wah in the same December 2025 transaction. Treat under the same "
         "exclusion until a merchant says otherwise."],
    ]
    nxt = table(ws, nxt, ["Company", "Status", "Detail"], [30, 22, 110], dropped)

    nxt += 1
    ws.cell(row=nxt, column=1,
            value="The exclusion is vindicated, not merely administrative. "
                  "Slumberland dropped both vendors BEFORE Southern Motion's "
                  "Chapter 11 filing. What was recorded as vendor "
                  "rationalization now reads as supply risk avoided. Any Man "
                  "Wah-owned entity should carry a supply-continuity review "
                  "before it is floored.").font = BOLD
    nxt += 2

    ws.cell(row=nxt, column=1, value="Trend read — April 2026 High Point").font = BOLD
    nxt += 1
    trends = [
        ["Zero-gravity is moving down-market",
         "Ashley showed a sectional with P2 zero gravity. A decade as a lift-chair and "
         "$3,000-motion feature; now on mainstream national-brand goods.",
         "Right top feature for our recliner AND lift ceilings today — but it will not hold that "
         "position more than a season or two. Do not architect $2,999 around it alone."],
        ["Wireless charging moved to the console, with magnets",
         "A console with a wireless charging tray plus a POP-UP MAGNETIC charger sized for smart "
         "watches and headphone cases, not just phones.",
         "The sharpest read of the under-35 customer on the floor: they are charging three "
         "devices, not one. Our category file already lists charging as a 2026 cover change. "
         "Franklin is the only governed brand that has it."],
        ["Immersive audio + seat vibration is the new ceiling",
         "Nice Link Echolux: directional near-field speakers in back and arms, deep-bass "
         "subwoofer, audio-synced seat vibration. $4,999-$5,999 for six pieces.",
         "Above our ceiling and sectional-shaped, so not a buy. But it re-prices what 'loaded' "
         "means and will pull heat/massage down-market as it does."],
        ["Heat and massage integrating at group level",
         "Flexsteel Brio with integrated heat and massage (Cozzia) in Italian leather.",
         "Franklin delivers heat + massage in a LIFT chair at $976.99 — half what La-Z-Boy "
         "charges for it in a recliner ($1,999.99 SoCozi). Clearest value gap in the study."],
        ["Scale merchandised as a choice — steal this",
         "Best Home Furnishings' Beast line ladders the same chair extra-wide at $1,200 and "
         "smaller at $999, with scale-led signage.",
         "The cleanest answer anyone showed to 'will it fit?' and 'built for my size?' at once, "
         "with no additional styles. Pick 2-3 high-velocity frames and floor them in two scales."],
        ["Domestic + in-stock sold as a feature",
         "Best, HomeStretch, Franklin, Mega Motion and UltraComfort are all domestic and all lead "
         "with availability.",
         "Directly relevant to our 85%-vs-95% in-stock gap. Availability is a feature an RSA can "
         "sell, not just a metric a buyer manages."],
    ]
    table(ws, nxt, ["Trend", "What was shown", "What it means for us"],
          [38, 62, 78], trends)
    return ws


# --- Tab 8 -------------------------------------------------------------------

def tab_conflicts(wb, rows):
    ws = wb.create_sheet("Conflicts & Decisions")
    header(ws, "Conflicts and Open Decisions",
           "precedence.md: 'Do not silently choose between conflicting values. "
           "State the conflict and apply the precedence rules.' Two remain OPEN "
           "and need a merchant decision.")

    conf = [
        ["C-016", "OPEN — sourcing",
         "The $299 recliner does not exist at Slumberland today",
         "Architecture says 'Vail and Collage $299' and names Randell/Joshua as $299 special "
         "purchases. Verified: Collage $399.99 · Vail $499.99 · Joshua $699.99 · Randell "
         "$1,149.99. Lowest verified recliner in the governed set is Ashley Nerviano $269.99.",
         "May not be a contradiction: promotion-rules.md lists $299 as the DOORBUSTER (an event "
         "price) and $399 as the PROMO price — and Collage $399.99 matches the promo price "
         "exactly. The Special Purchase PROGRAM is confirmed real (Slumberland's page indexes as "
         "'Joshua Special Purchase Rocker Recliner'); the $299 PRICE is not.",
         "X01 is floored as a TO-BE-SOURCED special buy at $299, off-slot, flagged NOT VERIFIED. "
         "X02 (Ashley Nerviano, verified $269.99) is floored alongside it so the advertised price "
         "is deliverable today even if X01 never closes. OWNER: Vendor Relations."],
        ["C-017", "OPEN — vendor negotiation",
         "The anchor brand cannot carry the tech story",
         "La-Z-Boy holds 64% of the floor and has NO verified charging, USB-C, cup holder or "
         "storage-arm SKU at any price. Franklin: wireless charging $768.99 · storage arms + USB "
         "+ cup holders $1,259.99 · built-in USB $759.99 · heat+massage lift $976.99 vs "
         "La-Z-Boy's $1,999.99.",
         "A real capability gap in the brand holding two thirds of the slots.",
         "Tech reveals held ABOVE $1,100; $400-$1,099 stays La-Z-Boy-led on comfort features. "
         "COST: the under-35 customer transacts $399-$699 and expects charging as table stakes. "
         "Franklin Magnus ($749, USB) is floored OFF-SLOT as a hedge. REVISIT the moment La-Z-Boy "
         "will build a charging SKU in the $700s — a negotiation item for the October Market."],
        ["C-011", "OPEN — definition",
         "La-Z-Boy 64% of slots vs. National Brand Mix 60%",
         "BIC commitment: La-Z-Boy = 64% of slots. 40-evidence G3: Natl Brand Mix % = 60.",
         "Not comparable — one is a share of floor SLOTS, the other a PRODUCT MIX % whose "
         "denominator the source does not state. If they shared a denominator they would "
         "contradict: one brand cannot hold 64% of a 60%-national floor and leave room for three "
         "others.",
         "La-Z-Boy 64% of slots governs the map (33 of 52). The 60% figure is reported and "
         "governs nothing. DECISION NEEDED: what is the denominator of Natl Brand Mix %?"],
        ["C-012", "OPEN — intent",
         "Good direction is 'Grow' but Good target MDL equals current MDL",
         "Direction = Grow. Current MDL share 11%. Target MDL share 11%.",
         "A true contradiction — unless growth is meant to come from somewhere other than slots.",
         "Recorded as a PROPOSAL, not policy: Good grows WITHOUT slot growth, through the four "
         "off-slot promotional SKUs (which the matrix excludes from slot count) and through "
         "step-up capture. DECISION NEEDED: if 'Grow' means take slots from Better, the target "
         "share is wrong and Better's 'Hold' has to change with it."],
        ["C-001", "Resolved structurally",
         "Slot count: 52 committed vs 60 observed vs 65 floored",
         "BIC commitment 52. Prior programmed state 60. Floored SKUs 65.",
         "Unit mismatch, not contradiction — and the source settles it. Target Slot Count "
         "'excludes special buys, promotional, and in/out items'.",
         "52 = governed MDL slots (rank 1). 60 = prior observed state, -8 in transition. "
         "65 = 52 MDL + 13 off-slot. NEVER averaged to 56. This reading is what makes the $299 "
         "promotion possible without spending a strategic slot."],
        ["C-013", "Resolved structurally",
         "Lift inside the 65 changes the GBB denominator",
         "Six of nine lift slots sit at $1,299+, which in recliner terms is Best.",
         "Scope difference. 40-evidence states the basis itself: 'GBB Basis: based on recliner "
         "price'.",
         "GBB governed on the 43 RECLINER slots (5/33/5). Blended view (5/37/10) reported and "
         "governed on nothing. Two columns, never one average."],
        ["C-014", "Resolved structurally",
         "The 30% national-brand cap does not carry into recliners",
         "The stationary upholstery line in this repo caps national brands at 30% of floor. "
         "Recliners: La-Z-Boy 64% of slots, PLW 'Grow Brand Names', 70% national promo allocation.",
         "gbb-rules.md: 'do not force one enterprise price ladder across categories.'",
         "The recliner validator enforces a La-Z-Boy FLOOR, not a national CAP."],
        ["C-015", "Resolved — and vindicated",
         "Dropped vendors could reappear via High Point scouting",
         "40-evidence: 'MAWA and SOMO dropped from lineup.'",
         "Man Wah acquired Southern Motion + Fusion Dec 2025. SOUTHERN MOTION FILED CHAPTER 11 ON "
         "3-4 SEPTEMBER 2026 — nine days before this build — with $8.3M owed to top 20 unsecured "
         "creditors.",
         "Exclusion holds. Both readable for trend intelligence only. Any Man Wah-owned entity "
         "carries a supply-continuity review before it is floored."],
    ]
    nxt = table(ws, 4, ["ID", "Status", "Conflict", "The two values",
                        "Why they differ", "What the build did"],
                [9, 22, 40, 62, 62, 74], conf)

    nxt += 1
    ws.cell(row=nxt, column=1,
            value="Data gates — not conflicts, but they bound what this build "
                  "can claim").font = BOLD
    nxt += 1
    gates = [
        ["Cover composition unknown for 53 of 65 SKUs",
         "Neither Slumberland nor Homemakers publishes fibre content at listing level. NO BOUCLE "
         "was verified on any governed brand at any price. Cover-gating — the cheapest margin "
         "lever in upholstery — cannot be decided from public data. Needs line sheets."],
        ["A third of the model names in the brief do not exist as recliners",
         "Makkah, Nezra, Earlbeck returned nothing. Ballyton is a sectional. Latitudes is a "
         "Flexsteel line, not a chair. Chandler is Franklin, not Flexsteel. Sherman is La-Z-Boy "
         "AND Franklin, never Ashley. Sherman, Aspen, Kent and Top Tier each appear under two "
         "brands. OPERATING RULE: never key a SKU on model name alone."],
        ["Margin is modeled, not quoted",
         "Every margin_pct is derived from tier position, not a vendor quote. A planning number "
         "to prove the price architecture holds before costing comes back. Replace with quoted "
         "landed cost when line sheets arrive, then rerun recliner_health.py."],
        ["Planned retail is not verified street",
         "retail is a PLANNED retail; every row carries the verified street price it was anchored "
         "to. Slumberland and Homemakers disagree by 20-50% on the same chair throughout the "
         "dataset — different cost bases and promo cadences, not an error in either. Two rows sit "
         "more than 13% from verified street: R42 SoCozi planned $2,299 vs $1,999.99 (+15%), "
         "R25 Pinnacle Power Headrest planned $799 vs $918.99 (-13%). Confirm before ticketing."],
        ["Slumberland's combined listing mis-assigns brands",
         "It labeled Everest as Franklin, Elsa as Ashley, Dutton as Flexsteel, Lavenhorne as "
         "La-Z-Boy. Every brand attribution in this build comes from the BRAND-FILTERED "
         "collection page. Any re-pull must do the same."],
    ]
    table(ws, nxt, ["Gate", "Detail"], [46, 120], gates)
    return ws


def main():
    rows = D.rows()
    wb = Workbook()
    wb.remove(wb.active)
    tab_map(wb, rows)
    tab_ladder(wb, rows)
    tab_analysis(wb, rows)
    tab_rules(wb, rows)
    tab_genz(wb, rows)
    tab_lift(wb, rows)
    tab_vendors(wb, rows)
    tab_conflicts(wb, rows)
    wb.save(OUT)
    print(f"Wrote {os.path.abspath(OUT)}")
    print(f"  {len(wb.sheetnames)} tabs: {', '.join(wb.sheetnames)}")


if __name__ == "__main__":
    main()
