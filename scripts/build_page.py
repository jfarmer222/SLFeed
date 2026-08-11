#!/usr/bin/env python3
"""Render the assortment review page from the canonical data module.

Generated so the page can never drift from the SKU master.
Usage:  python scripts/build_page.py
"""

import html
import os
from collections import defaultdict

import assortment_data as A

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), "docs", "assortment.html")

TIER_KEY = {A.GOOD: "good", A.BETTER: "better", A.BEST: "best"}
AXIS_MIN, AXIS_MAX = 400, 3600


def e(s):
    """Escape, and render source "--" as a real em dash."""
    return html.escape(str(s)).replace(" -- ", " &mdash; ")


def pos(retail):
    """Price to percentage along the ladder axis."""
    return 100.0 * (retail - AXIS_MIN) / (AXIS_MAX - AXIS_MIN)


def tier_stats(rows):
    out = {}
    for t in (A.GOOD, A.BETTER, A.BEST):
        sub = [r for r in rows if r["tier"] == t]
        tr = sum(r["retail"] for r in sub)
        tc = sum(r["landed_cogs"] for r in sub)
        out[t] = {
            "n": len(sub),
            "avg": tr / len(sub),
            "gm": 100 * (1 - tc / tr),
            "lo": min(r["retail"] for r in sub),
            "hi": max(r["retail"] for r in sub),
            "fams": len({r["family_code"] for r in sub}),
        }
    return out


def build_lanes(rows):
    idx = {r["sku_id"]: r for r in rows}
    lanes = []
    for lane, skus in A.LANES.items():
        rungs = []
        prev = None
        for sid in skus:
            r = idx[sid]
            rungs.append({
                "sku": sid, "family": r["family"], "tier": r["tier"],
                "retail": r["retail"], "pos": pos(r["retail"]),
                "step": None if prev is None else 100.0 * (r["retail"] - prev) / prev,
            })
            prev = r["retail"]
        spread = 100.0 * (rungs[-1]["retail"] - rungs[0]["retail"]) / rungs[0]["retail"]
        lanes.append({"name": lane, "rungs": rungs, "spread": spread})
    return lanes


def lane_markup(lanes):
    parts = []
    for ln in lanes:
        rungs = ln["rungs"]
        left, right = rungs[0]["pos"], rungs[-1]["pos"]
        dots = []
        for r in rungs:
            dots.append(
                f'<div class="rung t-{TIER_KEY[r["tier"]]}" style="left:{r["pos"]:.2f}%">'
                f'<span class="dot"></span>'
                f'<span class="rung-label"><b>{e(r["family"])}</b>'
                f'<i>${r["retail"]:,}</i></span></div>'
            )
        steps = []
        for a, b in zip(rungs, rungs[1:]):
            mid = (a["pos"] + b["pos"]) / 2
            steps.append(
                f'<span class="step" style="left:{mid:.2f}%">+{b["step"]:.0f}%</span>'
            )
        parts.append(
            f'<div class="lane">'
            f'<div class="lane-head"><h4>{e(ln["name"])}</h4>'
            f'<span class="spread">+{ln["spread"]:.0f}% total</span></div>'
            f'<div class="track">'
            f'<div class="track-line" style="left:{left:.2f}%;width:{right-left:.2f}%"></div>'
            f'{"".join(steps)}{"".join(dots)}'
            f'</div></div>'
        )
    return "\n".join(parts)


def family_markup(rows):
    by_fam = defaultdict(list)
    for r in rows:
        by_fam[r["family_code"]].append(r)

    sections = []
    for tier in (A.GOOD, A.BETTER, A.BEST):
        cards = []
        for code, fam in A.FAMILIES.items():
            if fam["tier"] != tier:
                continue
            skus = by_fam[code]
            lo = min(s["retail"] for s in skus)
            hi = max(s["retail"] for s in skus)
            pieces = "".join(
                f'<tr><td class="mono">{e(s["sku_id"])}</td>'
                f'<td>{e(s["piece_type"])}</td>'
                f'<td class="num">${s["retail"]:,}</td>'
                f'<td class="num dim">${s["landed_cogs"]:,}</td>'
                f'<td class="num">{s["margin_pct"]:.1f}%</td></tr>'
                for s in skus
            )
            spec_rows = [
                ("Arm", fam["arm"]), ("Back", fam["back"]), ("Seat", fam["seat"]),
                ("Suspension", fam["suspension"]), ("Frame", fam["frame"]),
                ("Joinery", fam["joinery"]), ("Legs", fam["legs"]),
                ("Cover", f'{fam["covers"]} covers -- {fam["cover_mix"]}'),
                ("Fabric", f'{fam["fabric"]} ({fam["rub_count"]:,} double rubs)'),
            ]
            if fam.get("mechanism"):
                spec_rows.insert(0, ("Mechanism", fam["mechanism"]))
            specs = "".join(
                f'<div class="spec"><dt>{e(k)}</dt><dd>{e(v)}</dd></div>'
                for k, v in spec_rows
            )
            cards.append(f'''
<article class="family t-{TIER_KEY[tier]}">
  <header class="fam-head">
    <div class="fam-id">
      <span class="code mono">{e(code)}</span>
      <h3>{e(fam["name"])}</h3>
      <span class="terr">{e(fam["territory"])}</span>
    </div>
    <div class="fam-meta">
      <span class="chip">{e(fam["category"])}</span>
      <span class="range mono">${lo:,}&ndash;${hi:,}</span>
      <span class="count">{len(skus)} SKU{"s" if len(skus) != 1 else ""}</span>
    </div>
  </header>
  <p class="note">{e(" ".join(fam["design_note"].split()))}</p>
  <div class="specs">{specs}</div>
  <div class="tablewrap">
    <table class="pieces">
      <thead><tr><th>SKU</th><th>Piece</th><th class="num">Retail</th>
      <th class="num">COGS</th><th class="num">GM</th></tr></thead>
      <tbody>{pieces}</tbody>
    </table>
  </div>
  <blockquote class="rsa">
    <span class="rsa-label">Floor story</span>
    {e(" ".join(fam["rsa_story"].split()))}
  </blockquote>
</article>''')

        st = tier_stats(rows)[tier]
        sections.append(f'''
<section class="tier t-{TIER_KEY[tier]}" id="tier-{TIER_KEY[tier]}">
  <header class="tier-head">
    <h2>{e(tier)}</h2>
    <dl class="tier-stats">
      <div><dt>Families</dt><dd>{st["fams"]}</dd></div>
      <div><dt>SKUs</dt><dd>{st["n"]}</dd></div>
      <div><dt>Retail range</dt><dd>${st["lo"]:,}&ndash;${st["hi"]:,}</dd></div>
      <div><dt>Blended GM</dt><dd>{st["gm"]:.1f}%</dd></div>
    </dl>
  </header>
  <div class="families">{"".join(cards)}</div>
</section>''')
    return "\n".join(sections)


def main():
    rows = A.enriched()
    st = tier_stats(rows)
    lanes = build_lanes(rows)
    tot_r = sum(r["retail"] for r in rows)
    tot_c = sum(r["landed_cogs"] for r in rows)
    blended = 100 * (1 - tot_c / tot_r)

    terr = defaultdict(int)
    for r in rows:
        terr[r["territory"]] += 1

    orderable = stocked = 0
    by_fam = defaultdict(int)
    for r in rows:
        by_fam[r["family_code"]] += 1
    for code, fam in A.FAMILIES.items():
        orderable += by_fam[code] * fam["covers"]
        stocked += by_fam[code] * fam.get("in_stock_covers", fam["covers"])

    terr_markup = "".join(
        f'<div class="bar-row"><span class="bar-name">{e(k)}</span>'
        f'<span class="bar"><span class="bar-fill" style="width:{100*v/65:.1f}%"></span></span>'
        f'<span class="bar-val mono">{v} &middot; {100*v/65:.0f}%</span></div>'
        for k, v in sorted(terr.items(), key=lambda kv: -kv[1])
    )

    mix_markup = "".join(
        f'<div class="bar-row t-{TIER_KEY[t]}"><span class="bar-name">{e(t)}</span>'
        f'<span class="bar"><span class="bar-fill" style="width:{100*st[t]["n"]/65:.1f}%"></span></span>'
        f'<span class="bar-val mono">{st[t]["n"]} &middot; {100*st[t]["n"]/65:.0f}%</span></div>'
        for t in (A.GOOD, A.BETTER, A.BEST)
    )

    page = TEMPLATE.format(
        blended=f"{blended:.1f}",
        lanes=lane_markup(lanes),
        families=family_markup(rows),
        terr=terr_markup,
        mix=mix_markup,
        orderable=orderable,
        stocked=stocked,
        custom=orderable - stocked,
        good_gm=f"{st[A.GOOD]['gm']:.1f}",
        better_gm=f"{st[A.BETTER]['gm']:.1f}",
        best_gm=f"{st[A.BEST]['gm']:.1f}",
        good_avg=f"{st[A.GOOD]['avg']:,.0f}",
        better_avg=f"{st[A.BETTER]['avg']:,.0f}",
        best_avg=f"{st[A.BEST]['avg']:,.0f}",
    )
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as fh:
        fh.write(page)
    print(f"wrote {os.path.relpath(OUT)} ({len(page):,} bytes)")


TEMPLATE = """<title>Line Review &mdash; 65-SKU Upholstery Assortment</title>
<style>
:root {{
  --ground:#F2F3F1; --surface:#FFFFFF; --surface-2:#EAECE9;
  --ink:#16191C; --ink-2:#454B4E; --ink-3:#6E7570;
  --rule:#D6D9D4; --rule-2:#C3C7C1;
  --accent:#2F4A5C;
  --good:#6E8375; --better:#3F6B7D; --best:#A67A3C;
  --good-soft:#E4EAE4; --better-soft:#DFE8ED; --best-soft:#F0E6D6;
  --shadow:0 1px 2px rgba(22,25,28,.05), 0 8px 24px -12px rgba(22,25,28,.14);
  --serif:ui-serif,"Iowan Old Style","Palatino Linotype",Palatino,Georgia,serif;
  --sans:system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
  --mono:ui-monospace,SFMono-Regular,"SF Mono",Menlo,Consolas,monospace;
}}
@media (prefers-color-scheme:dark) {{
  :root:not([data-theme="light"]) {{
    --ground:#14171A; --surface:#1B1F23; --surface-2:#22272C;
    --ink:#E9EBE8; --ink-2:#B3BAB6; --ink-3:#89918D;
    --rule:#2C3237; --rule-2:#3A4147;
    --accent:#8FB3C7;
    --good:#9BB3A2; --better:#7FAAC0; --best:#C9A268;
    --good-soft:#222A25; --better-soft:#1E2A31; --best-soft:#2C2418;
    --shadow:0 1px 2px rgba(0,0,0,.4), 0 8px 24px -12px rgba(0,0,0,.6);
  }}
}}
:root[data-theme="dark"] {{
  --ground:#14171A; --surface:#1B1F23; --surface-2:#22272C;
  --ink:#E9EBE8; --ink-2:#B3BAB6; --ink-3:#89918D;
  --rule:#2C3237; --rule-2:#3A4147;
  --accent:#8FB3C7;
  --good:#9BB3A2; --better:#7FAAC0; --best:#C9A268;
  --good-soft:#222A25; --better-soft:#1E2A31; --best-soft:#2C2418;
  --shadow:0 1px 2px rgba(0,0,0,.4), 0 8px 24px -12px rgba(0,0,0,.6);
}}

*,*::before,*::after {{ box-sizing:border-box; }}
body {{
  margin:0; background:var(--ground); color:var(--ink);
  font-family:var(--sans); font-size:16px; line-height:1.6;
  -webkit-font-smoothing:antialiased;
}}
.wrap {{ max-width:1080px; margin:0 auto; padding:0 24px 96px; }}
h1,h2,h3,h4 {{ font-family:var(--serif); font-weight:600; text-wrap:balance;
  line-height:1.15; margin:0; letter-spacing:-.01em; }}
.mono {{ font-family:var(--mono); font-variant-numeric:tabular-nums; }}
.num {{ text-align:right; font-family:var(--mono); font-variant-numeric:tabular-nums; }}
.dim {{ color:var(--ink-3); }}

/* ---- masthead ---- */
.mast {{ padding:72px 0 40px; border-bottom:2px solid var(--ink); }}
.eyebrow {{ font-family:var(--mono); font-size:11px; letter-spacing:.16em;
  text-transform:uppercase; color:var(--ink-3); margin:0 0 20px; }}
.mast h1 {{ font-size:clamp(38px,6vw,64px); margin:0 0 20px; }}
.lede {{ font-size:19px; line-height:1.55; color:var(--ink-2);
  max-width:60ch; margin:0; }}
.lede b {{ color:var(--ink); font-weight:600; }}

.keystats {{ display:grid; gap:1px; background:var(--rule);
  grid-template-columns:repeat(auto-fit,minmax(150px,1fr));
  border:1px solid var(--rule); margin:40px 0 0; }}
.keystats > div {{ background:var(--surface); padding:18px 20px; }}
.keystats dt {{ font-family:var(--mono); font-size:10px; letter-spacing:.14em;
  text-transform:uppercase; color:var(--ink-3); margin:0 0 8px; }}
.keystats dd {{ margin:0; font-family:var(--serif); font-size:30px;
  font-variant-numeric:tabular-nums; line-height:1; }}
.keystats dd small {{ font-size:13px; color:var(--ink-3); font-family:var(--sans);
  display:block; margin-top:7px; letter-spacing:0; }}

/* ---- sections ---- */
section {{ padding-top:72px; }}
.sec-head {{ margin-bottom:28px; }}
.sec-head h2 {{ font-size:30px; margin-bottom:10px; }}
.sec-head p {{ color:var(--ink-2); max-width:62ch; margin:0; }}

/* ---- ladder plot ---- */
.ladder {{ background:var(--surface); border:1px solid var(--rule);
  padding:32px 28px 20px; box-shadow:var(--shadow); overflow-x:auto; }}
.ladder-inner {{ min-width:640px; }}
.axis {{ position:relative; height:22px; margin-bottom:8px;
  border-bottom:1px solid var(--rule-2); }}
.axis span {{ position:absolute; transform:translateX(-50%); font-family:var(--mono);
  font-size:10px; color:var(--ink-3); letter-spacing:.06em; }}
.lane {{ padding:16px 0 4px; border-bottom:1px solid var(--rule); }}
.lane:last-child {{ border-bottom:0; }}
.lane-head {{ display:flex; align-items:baseline; justify-content:space-between;
  gap:16px; margin-bottom:26px; }}
.lane-head h4 {{ font-size:15px; }}
.spread {{ font-family:var(--mono); font-size:11px; color:var(--ink-3);
  letter-spacing:.06em; white-space:nowrap; }}
.track {{ position:relative; height:46px; }}
.track-line {{ position:absolute; top:5px; height:2px; background:var(--rule-2); }}
.rung {{ position:absolute; top:0; }}
.rung .dot {{ display:block; width:12px; height:12px; border-radius:50%;
  border:2px solid var(--surface); margin-left:-6px;
  box-shadow:0 0 0 1.5px currentColor; background:currentColor; }}
.rung-label {{ position:absolute; top:17px; left:0; transform:translateX(-50%);
  white-space:nowrap; text-align:center; }}
.rung-label b {{ display:block; font-size:12px; font-weight:600; color:var(--ink);
  line-height:1.3; }}
.rung-label i {{ display:block; font-style:normal; font-family:var(--mono);
  font-size:11px; color:var(--ink-3); font-variant-numeric:tabular-nums; }}
.step {{ position:absolute; top:-16px; transform:translateX(-50%);
  font-family:var(--mono); font-size:10px; color:var(--ink-3);
  letter-spacing:.04em; }}
.t-good .dot, .t-good.rung {{ color:var(--good); }}
.t-better .dot, .t-better.rung {{ color:var(--better); }}
.t-best .dot, .t-best.rung {{ color:var(--best); }}

/* ---- mix bars ---- */
.mixgrid {{ display:grid; gap:32px; grid-template-columns:repeat(auto-fit,minmax(320px,1fr)); }}
.panel {{ background:var(--surface); border:1px solid var(--rule); padding:24px;
  box-shadow:var(--shadow); }}
.panel h3 {{ font-size:16px; margin-bottom:18px; }}
.bar-row {{ display:grid; grid-template-columns:minmax(96px,auto) 1fr auto;
  align-items:center; gap:14px; margin-bottom:12px; }}
.bar-name {{ font-size:13px; color:var(--ink-2); }}
.bar {{ height:9px; background:var(--surface-2); position:relative; }}
.bar-fill {{ position:absolute; inset:0 auto 0 0; background:var(--accent); }}
.t-good .bar-fill {{ background:var(--good); }}
.t-better .bar-fill {{ background:var(--better); }}
.t-best .bar-fill {{ background:var(--best); }}
.bar-val {{ font-size:11px; color:var(--ink-3); white-space:nowrap; }}
.panel-foot {{ font-size:12px; color:var(--ink-3); line-height:1.6;
  margin:18px 0 0; padding-top:14px; border-top:1px solid var(--rule); }}

/* ---- tiers ---- */
.tier-head {{ display:flex; align-items:flex-end; justify-content:space-between;
  gap:24px; flex-wrap:wrap; padding-bottom:14px; margin-bottom:28px;
  border-bottom:2px solid currentColor; }}
.tier.t-good .tier-head {{ color:var(--good); }}
.tier.t-better .tier-head {{ color:var(--better); }}
.tier.t-best .tier-head {{ color:var(--best); }}
.tier-head h2 {{ font-size:34px; color:inherit; }}
.tier-stats {{ display:flex; gap:28px; margin:0; flex-wrap:wrap; color:var(--ink); }}
.tier-stats dt {{ font-family:var(--mono); font-size:10px; letter-spacing:.12em;
  text-transform:uppercase; color:var(--ink-3); }}
.tier-stats dd {{ margin:2px 0 0; font-family:var(--mono); font-size:15px;
  font-variant-numeric:tabular-nums; }}
.families {{ display:flex; flex-direction:column; gap:20px; }}

.family {{ background:var(--surface); border:1px solid var(--rule);
  border-left:3px solid var(--rule-2); padding:24px 26px; box-shadow:var(--shadow); }}
.family.t-good {{ border-left-color:var(--good); }}
.family.t-better {{ border-left-color:var(--better); }}
.family.t-best {{ border-left-color:var(--best); }}
.fam-head {{ display:flex; justify-content:space-between; align-items:flex-start;
  gap:20px; flex-wrap:wrap; margin-bottom:14px; }}
.fam-id {{ display:flex; align-items:baseline; gap:12px; flex-wrap:wrap; }}
.code {{ font-size:11px; letter-spacing:.1em; color:var(--ink-3);
  border:1px solid var(--rule-2); padding:2px 7px; }}
.fam-id h3 {{ font-size:23px; }}
.terr {{ font-size:12px; color:var(--ink-3); }}
.fam-meta {{ display:flex; align-items:center; gap:14px; flex-wrap:wrap;
  font-size:12px; color:var(--ink-3); }}
.chip {{ border:1px solid var(--rule-2); padding:2px 9px; font-size:11px;
  letter-spacing:.04em; }}
.range {{ font-size:13px; color:var(--ink); }}
.note {{ margin:0 0 20px; color:var(--ink-2); font-size:14.5px; max-width:70ch; }}

.specs {{ display:flex; flex-wrap:wrap; gap:1px; background:var(--rule);
  border:1px solid var(--rule); margin-bottom:20px; }}
.spec {{ background:var(--surface); padding:10px 13px; flex:1 1 232px; }}
.spec dt {{ font-family:var(--mono); font-size:9.5px; letter-spacing:.12em;
  text-transform:uppercase; color:var(--ink-3); margin-bottom:3px; }}
.spec dd {{ margin:0; font-size:13px; line-height:1.45; }}

.tablewrap {{ overflow-x:auto; margin-bottom:18px; }}
table {{ border-collapse:collapse; width:100%; font-size:13px; }}
th {{ font-family:var(--mono); font-size:9.5px; letter-spacing:.12em;
  text-transform:uppercase; color:var(--ink-3); font-weight:400;
  text-align:left; padding:0 12px 7px 0; border-bottom:1px solid var(--rule-2); }}
th.num {{ text-align:right; }}
td {{ padding:7px 12px 7px 0; border-bottom:1px solid var(--rule); }}
td:last-child, th:last-child {{ padding-right:0; }}
tr:last-child td {{ border-bottom:0; }}

.rsa {{ margin:0; padding:14px 18px; background:var(--surface-2);
  border-left:2px solid var(--rule-2); font-family:var(--serif);
  font-size:15px; line-height:1.5; color:var(--ink-2); }}
.rsa-label {{ display:block; font-family:var(--mono); font-size:9.5px;
  letter-spacing:.14em; text-transform:uppercase; color:var(--ink-3);
  margin-bottom:6px; }}

/* ---- cut features / open items ---- */
.cards {{ display:grid; gap:20px; grid-template-columns:repeat(auto-fit,minmax(300px,1fr)); }}
.cut {{ background:var(--surface); border:1px solid var(--rule); padding:24px;
  box-shadow:var(--shadow); }}
.cut h3 {{ font-size:18px; margin-bottom:6px; }}
.cut .verdict {{ font-family:var(--mono); font-size:10px; letter-spacing:.14em;
  text-transform:uppercase; color:var(--best); margin-bottom:14px; }}
.cut p {{ margin:0 0 12px; font-size:14.5px; color:var(--ink-2); }}
.cut p:last-child {{ margin-bottom:0; }}
.cut dl {{ margin:0 0 14px; display:grid; gap:7px; }}
.cut dl > div {{ display:flex; gap:10px; font-size:13px; }}
.cut dt {{ font-family:var(--mono); font-size:10px; letter-spacing:.1em;
  text-transform:uppercase; color:var(--ink-3); min-width:96px; padding-top:3px; }}
.cut dd {{ margin:0; color:var(--ink-2); }}

.openlist {{ list-style:none; padding:0; margin:0; display:grid; gap:2px;
  background:var(--rule); border:1px solid var(--rule); }}
.openlist li {{ background:var(--surface); padding:18px 22px; }}
.openlist h4 {{ font-size:15px; margin-bottom:6px; }}
.openlist p {{ margin:0; font-size:14px; color:var(--ink-2); max-width:70ch; }}
.tag {{ font-family:var(--mono); font-size:9.5px; letter-spacing:.13em;
  text-transform:uppercase; padding:2px 7px; border:1px solid var(--rule-2);
  color:var(--ink-3); margin-left:10px; vertical-align:2px; }}

footer {{ margin-top:80px; padding-top:24px; border-top:1px solid var(--rule);
  font-size:13px; color:var(--ink-3); }}
footer code {{ font-family:var(--mono); font-size:12px; color:var(--ink-2); }}

@media (max-width:620px) {{
  .wrap {{ padding:0 16px 64px; }}
  .mast {{ padding-top:48px; }}
  .family {{ padding:20px 18px; }}
}}
</style>

<div class="wrap">

<header class="mast">
  <p class="eyebrow">Line Review &middot; Stationary + Motion Upholstery</p>
  <h1>Sixty-five pieces,<br>one transitional language.</h1>
  <p class="lede">A Good/Better/Best upholstery line for a mid-market,
  ~125-store retailer. Nineteen frame families across stationary seating,
  sectionals and motion &mdash; <b>every SKU costed against a component
  build-up and validated by scripts that fail the build if the ladder
  breaks.</b></p>

  <dl class="keystats">
    <div><dt>Sellable pieces</dt><dd>65<small>19 frame families</small></dd></div>
    <div><dt>Blended margin</dt><dd>{blended}%<small>rising every tier</small></dd></div>
    <div><dt>Orderable SKUs</dt><dd>{orderable}<small>{stocked} stocked &middot; {custom} custom-order</small></dd></div>
    <div><dt>Ladder health</dt><dd>0<small>failures across 65 SKUs</small></dd></div>
  </dl>
</header>

<section>
  <div class="sec-head">
    <h2>Trade-up lanes</h2>
    <p>A tier average proves nothing. What matters is whether one customer can
    walk a like-for-like path from Good to Best. Every lane in the line, plotted
    on a real price axis &mdash; the gaps are the argument.</p>
  </div>
  <div class="ladder">
    <div class="ladder-inner">
      <div class="axis">
        <span style="left:3.1%">$500</span>
        <span style="left:18.8%">$1,000</span>
        <span style="left:34.4%">$1,500</span>
        <span style="left:50.0%">$2,000</span>
        <span style="left:65.6%">$2,500</span>
        <span style="left:81.3%">$3,000</span>
        <span style="left:96.9%">$3,500</span>
      </div>
      {lanes}
    </div>
  </div>
</section>

<section>
  <div class="sec-head">
    <h2>How the line is balanced</h2>
    <p>Better carries the most SKUs because that is where a mid-market
    assortment does its volume. The three style territories are three
    expressions of one transitional language, not three competing ones.</p>
  </div>
  <div class="mixgrid">
    <div class="panel">
      <h3>Tier mix</h3>
      {mix}
      <p class="panel-foot">
      Avg retail ${good_avg} / ${better_avg} / ${best_avg} &middot;
      blended GM {good_gm}% / {better_gm}% / {best_gm}%</p>
    </div>
    <div class="panel">
      <h3>Style territory</h3>
      {terr}
      <p class="panel-foot">
      Classic runs rolled and English arms; Modern runs track, scoop and
      shelter; Casual runs slope and pillow-top.</p>
    </div>
  </div>
</section>

<section>
  <div class="sec-head">
    <h2>What the cost audit cut</h2>
    <p>The price-coherence check rejected the first draft of this line in seven
    places. Two Best-tier features were specced, costed, and then deliberately
    removed &mdash; good product engineering is as much about what you refuse to
    build.</p>
  </div>
  <div class="cards">
    <div class="cut">
      <h3>8-way hand-tied suspension</h3>
      <p class="verdict">Specced &rarr; cut</p>
      <dl>
        <div><dt>Cost</dt><dd>~$195 on a sofa &mdash; 24% of Pemberton's entire COGS budget</dd></div>
        <div><dt>Perceptible</dt><dd>Effectively zero against well-executed pocketed coil in a showroom sit</dd></div>
        <div><dt>Benefit</dt><dd>Real, but purely longevity</dd></div>
      </dl>
      <p>The freed budget went to pocketed coil suspension, down-blend back
      pillows, kiln-dried maple and mortise-and-tenon joinery &mdash; one felt
      immediately, two that genuinely extend the life of the frame. Keeping it
      would have been textbook feature-dumping.</p>
    </div>
    <div class="cut">
      <h3>Coil-on-coil seat construction</h3>
      <p class="verdict">Specced &rarr; cut</p>
      <dl>
        <div><dt>Cost</dt><dd>~$45 per seating position on top of coil suspension</dd></div>
        <div><dt>Competed with</dt><dd>Quincy's scoop arm and solid brass legs</dd></div>
        <div><dt>Rule applied</dt><dd>The arm is the product; the budget follows the arm</dd></div>
      </dl>
      <p>A great story and a real cost. On the line's design halo it was
      competing directly with the two things that actually sell that SKU.</p>
    </div>
    <div class="cut">
      <h3>Down moved from seats to backs</h3>
      <p class="verdict">Relocated</p>
      <dl>
        <div><dt>Seat envelope</dt><dd>~$55 per position &mdash; $385 across a 7-seat modular</dd></div>
        <div><dt>Back pillow</dt><dd>About a third of that</dd></div>
        <div><dt>Where it's felt</dt><dd>Against the shoulders, not under the thighs</dd></div>
      </dl>
      <p>Down-blend seats broke the Best sectional band outright. Seats run
      2.2&nbsp;lb HR foam with a thick fiber wrap; the down went where the
      customer actually registers it.</p>
    </div>
  </div>
</section>

{families}

<section>
  <div class="sec-head">
    <h2>Open items</h2>
    <p>Stated rather than buried. Each carries a recommended fill.</p>
  </div>
  <ul class="openlist">
    <li>
      <h4>No motion sectional<span class="tag">largest gap</span></h4>
      <p>Nine sectional SKUs, thirteen motion SKUs, zero overlap. Reclining
      sectionals are real mid-market volume. Filling it properly needs 3&ndash;4
      SKUs at Better and Best &mdash; which means expanding past 65 or cutting
      elsewhere. A scope decision, not an oversight.</p>
    </li>
    <li>
      <h4>No $599 opening sofa<span class="tag">price point</span></h4>
      <p>The line opens at $699. A $599 three-seat sofa at entry spec models at
      ~$357 landed against a ~$305 allowance &mdash; unreachable at an in-band
      margin. Recommended fill: an apartment-scale two-seat sofa at
      $549&ndash;$599 that carries its margin honestly, rather than discounting
      a three-seat build.</p>
    </li>
    <li>
      <h4>Six families run with thin cost headroom<span class="tag">watch list</span></h4>
      <p>Fairhaven, Brantley, Easton, Harlow, Ivywood and Kingsley build inside
      their allowed COGS with little room to absorb input movement. They are the
      first SKUs to re-cost when foam, freight or currency shifts.</p>
    </li>
    <li>
      <h4>Costs are modeled, not quoted<span class="tag">before RFQ</span></h4>
      <p>Every landed cost here is derived from target margin &mdash; planning
      numbers that prove the architecture holds before vendor RFQs go out. The
      checks are built to be rerun as real costing returns.</p>
    </li>
  </ul>
</section>

<footer>
  <p>Generated from <code>scripts/assortment_data.py</code>, the canonical
  source of truth for all 65 SKUs. Rerun <code>build_page.py</code>,
  <code>ladder_health.py</code> and <code>spec_checker.py</code> after any
  change to the line.</p>
</footer>

</div>
"""

if __name__ == "__main__":
    main()
