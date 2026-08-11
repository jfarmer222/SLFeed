# National Upholstery Brands — Vendor Research

**Purpose:** Source data for a 65-SKU upholstery assortment across a ~125-store mid-market chain, using three national brands to anchor a Good / Better / Best ladder.
**Researched:** 2026-08-11. All data from publicly accessible pages. No logins, no dealer portals, no access-control circumvention.
**Assigned roles:** Ashley = GOOD (stationary + motion) · La-Z-Boy = BETTER (motion only) · Flexsteel = BEST (motion only).

> **Read the "Data quality" section before using any price in this document.** Price availability differs sharply by brand and is the single biggest weakness in this dataset.

---

## Access summary — what was and was not publicly fetchable

| Vendor site | Product specs | Prices | Fetch result |
|---|---|---|---|
| ashleyfurniture.com | — | — | **HTTP 403 on every URL tried** (category and product detail alike). Bot-blocked, not dealer-gated. Not circumvented. |
| la-z-boy.com | — | — | **Renders client-side; returns "A required part of this site couldn't load."** No product data extractable. `mobile.la-z-boy.com` 301-redirects to the main site. |
| flexsteel.com | **Yes — deep** | **No** | Fully public and fetchable. Rich construction specs on product detail pages. **Zero prices published anywhere on the site.** |

Because two of three vendor sites were not machine-readable, Ashley and La-Z-Boy product data below comes from **public authorized-dealer catalogs** and from **search-engine snippets quoting the vendor sites**. Every row is labeled with its actual source. Dealer sites are independent retailers setting their own prices — see Data quality.

---

## 1. Ashley — GOOD / opening price tier

### Corporate basics

| Item | Finding | Source |
|---|---|---|
| Legal entity | Ashley Furniture Industries, LLC | [ashleyfurnitureindustriesllc.com](https://www.ashleyfurnitureindustriesllc.com/) |
| HQ | Arcadia, Wisconsin | [Wikipedia](https://en.wikipedia.org/wiki/Ashley_Furniture_Industries) |
| Ownership | Private; Wanek family — Ron and Todd Wanek. Ron Wanek and investors bought the company in 1976. | [Wikipedia](https://en.wikipedia.org/wiki/Ashley_Furniture_Industries) |
| Manufacturing | Domestic **and** import. Plants/DCs in WI, MS, IN, PA, NC, FL; offshore manufacturing in China and Vietnam. CA manufacturing closed 2016 (DC remains). | [Wikipedia](https://en.wikipedia.org/wiki/Ashley_Furniture_Industries) |
| Scale | Described as the largest furniture manufacturer in the United States. | [Wikipedia](https://en.wikipedia.org/wiki/Ashley_Furniture_Industries) |
| Current status 2026 | Active and expanding. Consolidated manufacturing at Mesquite, TX in early 2026 (266 layoffs by May 2026). Opened first Mogadishu, Somalia store May 2026. | [Wikipedia](https://en.wikipedia.org/wiki/Ashley_Furniture_Industries) |

### Brand/tier structure

Ashley runs a multi-badge ladder rather than a published price ladder:

- **Signature Design by Ashley** — entry/opening tier. *"Combines the latest design trends with comfort and quality you can rely on."*
- **Benchcraft** — mid-tier upholstery/motion badge. Reported as hardwood and engineered-wood frames, corner-blocked joints, no-sag springs, multi-density foam.
- **Millennium** — upper tier; greater use of solid wood, thicker veneers, premium upholstery including top-grain leather.

Source: [Big Sandy Superstore — Benchcraft review](https://www.bigsandysuperstore.com/blog/expert-benchcraft-furniture-review) and [Fix It In The Home — Ashley quality](https://fixitinthehome.com/ashley-furniture-good-quality_gem1m/). **Note: this tier hierarchy is described by retailers and third parties, not by an Ashley-published tier document. Treat as UNVERIFIED at the vendor level.**

### Recurring published construction language (Signature Design by Ashley)

Ashley uses near-identical boilerplate across the line, which makes it easy to spec but hard to differentiate:

- **Motion pieces:** "corner-blocked frame with metal reinforced seat"; "high-resiliency foam cushions wrapped in thick poly fiber"; attached back and seat cushions.
- **Stationary pieces:** "corner-blocked frame"; "high-quality foam cushions wrapped in poly fiber"; **"platform foundation system"** that *"resists sagging 3x better than spring system after 20,000 testing cycles."*

The platform-foundation claim is the notable one — Ashley's opening-price stationary goods explicitly use a platform deck **instead of** a sinuous-spring seat, and market it as an upgrade. Source: [Pruitt's — Navi 9400438](https://www.pruitts.com/product/signature-design-by-ashley-navi-fossil-sofa-9400438-1384564).

**Warranty: NOT PUBLISHED** on any page reached. One dealer listed a flat "365 days" ([Discount Furniture of the Carolinas — Altari](https://www.discountfurnitureofthecarolinas.com/products/signature-design-by-ashley-altari-stationary-fabric-sofa-8721438)) but that is a retailer field, not Ashley's published warranty schedule.

### Ashley products

| Brand | Collection | Product | Model # | Piece type | MSRP / price | Mechanism | Key specs | Source URL |
|---|---|---|---|---|---|---|---|---|
| Ashley | Navi | Navi Fossil Sofa | 9400438 | Stationary sofa | $449.98 | None | Corner-blocked frame; **platform foundation** ("3x better than spring system after 20,000 cycles"); high-quality foam wrapped in poly fiber; faux leather; 89"W×38"D×39"H; 134 lb | [pruitts.com](https://www.pruitts.com/product/signature-design-by-ashley-navi-fossil-sofa-9400438-1384564) |
| Ashley | Altari | Altari Alloy Sofa | 8721438 | Stationary sofa | $464.40 sale / $516.00 reg | None | Corner-blocked frame; platform foundation; foam wrapped in poly fiber; 100% polyester chenille-feel; 85"W×38"D×37"H; 126 lb; 2 accent pillows | [discountfurnitureofthecarolinas.com](https://www.discountfurnitureofthecarolinas.com/products/signature-design-by-ashley-altari-stationary-fabric-sofa-8721438) |
| Ashley | Gauntlet | Gauntlet Sterling Manual Reclining Sofa | PC4220488 | Reclining sofa (dual-side, stationary middle) | $589.94 sale / $919.99 reg | Manual, pull-tab | Corner-blocked frame w/ metal reinforced seat; high-quality foam wrapped in poly fiber; polyester; 76"W×39"D×39"H; seat H 19"; 206 lb | [sidesfurniture.com](https://www.sidesfurniture.com/product/signature-design-by-ashley-gauntlet-sterling-manual-reclining-sofa-pc4220488-1724511) |
| Ashley | Top Tier | Top Tier 3-Pc RAF Manual Reclining Sectional w/ Chaise | 92705S4 | Reclining sectional | $1,279.94 sale / $1,999.99 reg | Manual pull-tab + press-back chaise | Corner-blocked frame w/ metal reinforced seat; high-quality foam wrapped in poly fiber; polyester; console w/ 2 cupholders + storage; 105"W×74"D×41"H; cleaning code W | [sidesfurniture.com](https://www.sidesfurniture.com/product/signature-design-by-ashley-top-tier-3-piece-chocolate-reclining-sectional-sofa-with-chaise-92705s4-1548386) |
| Ashley | Draycoll | Draycoll Power Reclining Sofa (Slate) | NOT SHOWN on this page | Power reclining sofa | $1,091.38 | Dual-sided power, one-touch; middle seat stationary | Corner-blocked frame; high-resiliency foam wrapped in thick poly fiber; polyester chenille; zero-draw USB; UL-listed cord; 87"W×40"D×40"H; 216 lb | [walmart.com](https://www.walmart.com/ip/Signature-Design-by-Ashley-Draycoll-Power-Reclining-Sofa-in-Slate/838982417) |
| Ashley | The Man-Den | The Man-Den Mahogany Power Reclining Sofa | U8530615 | Power reclining sofa | $2,049.94 sale / $3,199.99 reg | Dual-sided power; one-touch; **Easy View power adjustable headrest**; power lumbar | Corner-blocked frame w/ metal reinforced seat; high-resiliency foam wrapped in thick poly fiber; leather interior / vinyl-poly exterior; USB + wireless phone charging; drop table, reading lights, arm storage; 85.5"W×40"D×43"H; 325 lb | [sidesfurniture.com](https://www.sidesfurniture.com/product/signature-design-by-ashley-the-man-den-mahogany-power-reclining-sofa-u8530615-903063) |
| Ashley | Snowfield | Snowfield Gunmetal Power Lift Recliner | 1760912 | Power lift recliner | $599.98 | **Dual motors** — footrest and back independent; power lift | Corner-blocked frame w/ metal reinforcement; high-resiliency foam wrapped in thick poly fiber; faux leather; heat + massage w/ auto shut-off; USB; battery backup optional; 34"W×40"D×44"H; 146 lb | [pruitts.com](https://www.pruitts.com/product/signature-design-by-ashley-snowfield-gunmetal-power-lift-recliner-1625337) |
| Ashley | Foreside | Foreside Charcoal Manual Reclining Sofa | 3810488 | Reclining sofa | **UNVERIFIED** (PDP returned 403) | Manual, pull-tab | Corner-blocked frame w/ metal reinforced seat; attached back and seat cushions; high-resiliency foam wrapped in thick poly fiber | [jrfurniture.com listing](https://www.jrfurniture.com/product/signature-design-by-ashley-foreside-charcoal-manual-reclining-sofa-3810488-1566535) |
| Ashley | Bolzano | Bolzano 2-Seat Reclining Sofa | NOT SHOWN | Reclining sofa | $879.73 *(snippet only)* | Manual, pull-tab | Corner-blocked frame w/ metal reinforced seat; attached back and seat cushions; high-resiliency foam wrapped in thick poly fiber | [walmart.com](https://www.walmart.com/ip/Signature-Design-by-Ashley-Bolzano-2-Seat-Reclining-Sofa/321727622) |
| Ashley | Tip-Off | Tip-Off Power Reclining Sofa w/ Adjustable Headrest | 6930415 | Power reclining sofa | $1,388.99 *(snippet only — PDP 404)* | Power w/ adjustable headrest | NOT CAPTURED | [chubbysmattress.com](https://chubbysmattress.com/products/signature-design-by-ashley-tip-off-power-reclining-sofa-6930415) |
| Ashley | Owner's Box | Owner's Box Dual Power Reclining Sofa | 2450515 | Power reclining sofa | $1,104.99 sale / $1,399.99 orig *(snippet only — 403)* | Dual power | NOT CAPTURED | [ashleyfurniture.com](https://www.ashleyfurniture.com/p/owners_box_power_reclining_sofa/2450515.html) |
| Ashley | (unnamed) | Reclining Sofa | 6330388 | Reclining sofa | **UNVERIFIED** (page 500) | Manual reclining | Corner-blocked frame w/ metal reinforced seat; high-resiliency foam; faux leather; 89"W×39"D×40"H | [amazon.com](https://www.amazon.com/Signature-Design-Ashley-6330388-Reclining/dp/B01MTDTC9E) |
| Ashley | Markridge | Markridge Power Lift Recliner (Gray) | NOT SHOWN | Power lift recliner | $981.75 *(snippet only)* | Power lift; remote | Side storage | [walmart.com](https://www.walmart.com/ip/Signature-Design-by-Ashley-Markridge-Upholstered-Power-Lift-Recliner-with-Remote-Included-and-Side-Storage-Gray/868075811) |
| Ashley | Ballister | Ballister Power Lift Recliner (Espresso) | NOT SHOWN | Power lift recliner | $849.99 *(snippet only)* | Power lift | NOT CAPTURED | [walmart.com](https://www.walmart.com/ip/Signature-Design-by-Ashley-Ballister-Power-Lift-Recliner-in-Espresso/318823844) |
| Ashley | Oatman | Oatman Power Lift Recliner w/ Heat & Massage | 1800412 **or** 1800512 — **sources conflict** | Power lift recliner | $609.99 sale / $683.99 reg *(snippet only)* | Power lift; heat & massage | NOT CAPTURED | [discountfurnitureofthecarolinas.com](https://www.discountfurnitureofthecarolinas.com/products/signature-design-by-ashley-oatman-leather-look-lift-chair-with-heat-and-massage-1800412) |

**Ashley observed price bands (dealer street prices, not MSRP):**

| Piece type | Range |
|---|---|
| Stationary sofa | $449.98 – $516.00 |
| Manual reclining sofa | $589.94 – $919.99 |
| Power reclining sofa | $1,091.38 – $3,199.99 |
| Power lift recliner | $599.98 – $981.75 |
| Reclining sectional (3-pc) | $1,279.94 – $1,999.99 |

---

## 2. La-Z-Boy — BETTER / middle tier (MOTION ONLY)

### Corporate basics

| Item | Finding | Source |
|---|---|---|
| Legal entity | La-Z-Boy Incorporated — public, NYSE: LZB | [ir.la-z-boy.com](https://ir.la-z-boy.com/) |
| HQ | One La-Z-Boy Drive, Monroe, Michigan 48162. LEED-certified world HQ. | [ZoomInfo HQ record](https://www.zoominfo.com/hq/la-z-boy-inc-office-address/55166701) |
| Manufacturing | Domestic assembly. Majority of North American recliners assembled in the US at **Dayton, TN; Neosho, MO; Siloam Springs, AR**. Innovation Center in Dayton, TN. | [whomakethis.com](https://whomakethis.com/where-is-la-z-boy-furniture-made/) |
| FY2026 results | Full-year delivered sales **$2.1B**; operating cash flow $204M; $85M returned to shareholders. Q4 sales $570M (flat YoY); Q4 retail-segment written sales **+11%**. Q4 operating margin 7.2% GAAP / 9.9% adjusted; diluted EPS $0.81 GAAP / $1.26 adjusted. | [La-Z-Boy Q4 FY26 release, 2026-06-16](https://ir.la-z-boy.com/2026-06-16-La-Z-Boy-Incorporated-Reports-Strong-Fourth-Quarter-Results-Led-By-Retail-Sales-Growth-And-Broad-Based-Margin-Improvement-Finalizes-Multiple-Strategic-Initiatives) |
| Leadership / status | CEO **Melinda Whittington**; publicly stated plan to expand to **450 locations**. Healthy and growing. | [Q4 FY26 release](https://ir.la-z-boy.com/2026-06-16-La-Z-Boy-Incorporated-Reports-Strong-Fourth-Quarter-Results-Led-By-Retail-Sales-Growth-And-Broad-Based-Margin-Improvement-Finalizes-Multiple-Strategic-Initiatives) · [Investing.com Q4 FY26 transcript](https://www.investing.com/news/transcripts/earnings-call-transcript-lazboy-beats-q4-2026-eps-forecast-shares-jump-25-93CH-4747553) |

### Motion platforms and named mechanisms

- **Reclina-Rocker®** — the core rocker-recliner chassis.
- **PowerReclineXR® / PowerXR+** — power motion with power headrest and power lumbar, remote release, memory settings, USB. Marketed as *"double the power of other recliners."*
- **duo®** — La-Z-Boy's power-motion sofa/loveseat/sectional line. Dual side-mounted 2-button controls on the outside arms drive backs and legrests independently; built-in USB. Current members found: **Bennett duo, Colby duo, Luke duo, Roscoe duo.** Source: [Wayfair — Bennett duo](https://www.wayfair.com/furniture/pdp/la-z-boy-bennett-duo-power-reclining-sofa-lz10948.html), [McMasters — Roscoe duo](https://www.mcmhg.com/product/la-z-boy-roscoe-duo-power-reclining-sofa-p91892-d203173-1547033).
- **ComfortCore®** — patented seat cushion; paired with "double-picked blown fiber fill" backs and "high grade foam seat cushions."

### Published construction and warranty

- **Frame:** engineered hardwood / engineered wood.
- **Suspension:** **sinuous wire springs** in seat and back.
- **Warranty:** **Limited Lifetime** on **frame, spring systems, and mechanism**. Fabric, leather and certain cushions carry **shorter** terms. Exact component-by-component durations **NOT PUBLISHED** on any page I could reach — `la-z-boy.com/content/CustomerCare/parts-warranty` would not render.
- Sources: [Style Meets Comfort — Premier Construction](https://www.stylemeetscomfort.ca/learning-center/la-z-boy-premier-construction), [Furniture Academy — La-Z-Boy Lifetime Warranty Explained](https://furnitureacademy.com/la-z-boy-lifetime-warranty-explained/). **Both are dealer/third-party, not vendor-published. UNVERIFIED at vendor level.**

### Style-number convention (useful for line reviews)

La-Z-Boy factory style numbers encode the chassis: `444521` = manual James sofa, `X44521` = same shell with PowerXR headrest + lumbar, `U44530` = Greyson power w/ headrest, `44P530` = Greyson power, `P91893` = Colby duo sofa, `10X512` / `P10512` = Pinnacle Reclina-Rocker power variants. Confirmed from la-z-boy.com product URL paths and dealer PDPs.

### La-Z-Boy products

| Brand | Collection | Product | Model # | Piece type | MSRP / price | Mechanism | Key specs | Source URL |
|---|---|---|---|---|---|---|---|---|
| La-Z-Boy | Pinnacle | Pinnacle PowerXR+ Reclina-Rocker w/ Power Headrest & Power Lumbar | **10X512** | Power rocker recliner | $1,399.00 sale / $2,099.00 reg | PowerXR+; remote release; 2 memory settings; side control panel; USB | Engineered wood frame; double-picked blown fiber fill; high grade foam seat cushions; polyester; **Limited Lifetime**; 33"W×39"D×42"H; seat H 18.5"; 105 lb; handcrafted in USA w/ US + imported parts | [kubins.com](https://www.kubins.com/product/la-z-boy-pinnacle-powerxr-reclina-rocker-with-power-headrest-and-power-lumbar-10x512-d175977-774781) |
| La-Z-Boy | Pinnacle | Pinnacle Power Rocking Recliner | **P10512** | Power rocker recliner | $1,819.00 sale / $2,599.00 reg *(snippet quoting vendor site)* | PowerReclineXR | NOT CAPTURED (page would not render) | [la-z-boy.com](https://la-z-boy.com/p/recliners/pinnacle-power-rocking-recliner/_/R-P10512) |
| La-Z-Boy | Bennett duo | Bennett duo Pewter Power Reclining Sofa | **P91899** | Power reclining sofa | $2,027.99 | duo power; side power buttons; AC or optional battery pack | Patented **ComfortCore®** cushions; chenille performance/stain-resistant fabric; USB; two 20" pillows; 82.5"W×39"D×39.5"H; seat H 21"; 220 lb; scaled for 5'10"–6'2" | [storeforhomefurniture.com](https://www.storeforhomefurniture.com/product/la-z-boy-bennett-duo-pewter-power-reclining-sofa-p91899-b180868-1060198) |
| La-Z-Boy | Colby duo | Colby duo Ash Power Reclining Sofa | **P91893** | Power reclining sofa | $2,589.99 | duo power; dual side-mounted arm controls | Patented ComfortCore® seat cushions; double-picked blown fiber fill; USB; rolled arms, wood legs, padded outer arms/back; **Limited Lifetime**; 83"W×39.5"D×41"H; seat H 21.5"; 10-week made-to-order lead time | [economyfurniture.com](https://www.economyfurniture.com/product/la-z-boy-colby-duo-ash-power-reclining-sofa-p91893-c170053-1060233) |
| La-Z-Boy | Roscoe duo | Roscoe duo Power Reclining Sofa | **P91892** | Power reclining sofa | $2,569.00 | duo power; side-mounted 2-button panels; backs and legrests independent (**2 motors**) | Double-picked blown fiber fill; chambered blown-fiber semi-attached backs; high grade foam seat cushions; USB; **Limited Lifetime**; 81"W×39.5"D×40"H; 231 lb | [mcmhg.com](https://www.mcmhg.com/product/la-z-boy-roscoe-duo-power-reclining-sofa-p91892-d203173-1547033) |
| La-Z-Boy | Luke duo | Luke duo Reclining 2-Seat Sofa — Sable | **UNVERIFIED** | Power reclining sofa | **UNVERIFIED** (dealer page 403) | duo dual-sided power; USB | Sloped arms, button-tufted back, metal legs | [woodsfurnituregallery.com](https://www.woodsfurnituregallery.com/en/product/478840-la-z-boy-luke-duo-reclining-2-seat-sofa-sable) |
| La-Z-Boy | James | James Power Reclining Sofa w/ Headrest & Lumbar | **X44521** | Power reclining sofa | from $1,679.00 sale / $2,399.00 reg *(snippet quoting vendor site)* | PowerXR w/ power headrest + power lumbar | Bucket chaise seats; pillow backs and armrests | [la-z-boy.com](https://www.la-z-boy.com/p/sofas-sectionals/reclining-sofas-sectionals/reclining-sofas/james-power-reclining-sofa-w-headrest-lumbar/R-X44521) |
| La-Z-Boy | James | James Reclining Sofa | **444521** | Manual reclining sofa | **UNVERIFIED** | Manual | Same shell as X44521 | [la-z-boy.com](https://www.la-z-boy.com/p/sofas-sectionals/reclining-sofas-sectionals/reclining-sofas/james-reclining-sofa/R-444521) |
| La-Z-Boy | Greyson | Greyson Power Reclining Sofa | **44P530** | Power reclining sofa | **NOT SHOWN** (dealer says call) | Power recline | Pillow-top arms; plush seats w/ chaise legrests | [la-z-boy.com](https://www.la-z-boy.com/p/power/greyson-power-reclining-sofa/_/R-44P530) |
| La-Z-Boy | Greyson | Greyson Power Reclining Sofa w/ Headrest | **U44530** | Power reclining sofa | **NOT SHOWN** | Power recline + independently adjustable power-tilt headrests | Pillow-top arms; chaise legrests | [la-z-boy.com](https://www.la-z-boy.com/p/reclining-sofas/greyson-power-reclining-sofa-w-headrest/_/R-U44530) |
| La-Z-Boy | Trouper | Trouper Reclining Sofa | **444724** | Manual reclining sofa | **UNVERIFIED** | Manual dual-sided | 3 sculpted bucket seats; split back cushion; chaise legrest | [la-z-boy.com](https://www.la-z-boy.com/p/sofas-sectionals/reclining-sofas-sectionals/reclining-sofas/trouper-reclining-sofa/R-444724) |
| La-Z-Boy | Trouper | Trouper Power Reclining Sofa w/ Headrest | **U44724** | Power reclining sofa | **NOT SHOWN** | Power recline + power headrest | Bucket seats; chaise legrest | [la-z-boy.com](https://www.la-z-boy.com/p/sofas-sectionals/reclining-sofas-sectionals/reclining-sofas/trouper-power-reclining-sofa-w-headrest/R-U44724) |
| La-Z-Boy | Trouper | Trouper Power Reclining Loveseat | **UNVERIFIED** | Power reclining loveseat | from $1,709.00 sale / $2,279.00 reg *(snippet)* | Power recline | — | [la-z-boy.com](https://www.la-z-boy.com/b/sofas-reclining/_/N-ls4bd3) |
| La-Z-Boy | Trouper | Trouper Charcoal Power Reclining Sofa *(dealer listing)* | 727862 — **dealer SKU, not LZB style #** | Power reclining sofa | $2,129.99 | Power recline | — | [homemakers.com](https://www.homemakers.com/shop/living-room/sofas-and-loveseats/?prefn1=brand&prefv1=La-Z-Boy) |
| La-Z-Boy | Trouper | Trouper Walnut Power Reclining Sofa *(dealer listing)* | 726845 — **dealer SKU** | Power reclining sofa | $2,568.99 | Power recline | Leather | [homemakers.com](https://www.homemakers.com/shop/living-room/sofas-and-loveseats/?prefn1=brand&prefv1=La-Z-Boy) |
| La-Z-Boy | Trouper | Trouper Charcoal Power Reclining Loveseat w/ Console *(dealer listing)* | 727875 — **dealer SKU** | Power reclining loveseat | $2,509.99 | Power recline | Console | [homemakers.com](https://www.homemakers.com/shop/living-room/sofas-and-loveseats/?prefn1=brand&prefv1=La-Z-Boy) |
| La-Z-Boy | Greyson | Greyson Leather Power Rocker Recliner *(dealer listing)* | 1010822S — **dealer SKU** | Power rocker recliner | $1,519.99 | Power recline | Leather | [homemakers.com](https://www.homemakers.com/shop/living-room/chairs-and-recliners/recliners/?prefn1=brand&prefv1=La-Z-Boy) |
| La-Z-Boy | Finley | Finley Black Leather Power Rocker Recliner *(dealer listing)* | 17556S — **dealer SKU** | Power rocker recliner | $1,429.99 | Power recline | Leather | [homemakers.com](https://www.homemakers.com/shop/living-room/chairs-and-recliners/recliners/?prefn1=brand&prefv1=La-Z-Boy) |
| La-Z-Boy | Trouper | Trouper Walnut Leather Power Headrest Rocker Recliner *(dealer listing)* | 602124 — **dealer SKU** | Power rocker recliner | $1,259.99 | Power recline + power headrest | Leather | [homemakers.com](https://www.homemakers.com/shop/living-room/chairs-and-recliners/recliners/?prefn1=brand&prefv1=La-Z-Boy) |
| La-Z-Boy | Maverick | Maverick Power Rocking Recliner | **UNVERIFIED** | Power rocker recliner | $559.00 sale / $799.00 reg *(snippet)* | Power recline | Opening power price point | [la-z-boy.com](https://www.la-z-boy.com/b/living-room/recliners) |

**La-Z-Boy observed price bands:**

| Piece type | Range | Basis |
|---|---|---|
| Manual reclining sofa | $977.99 – $1,768.99 | dealer (Homemakers) |
| Power reclining sofa | $2,027.99 – $2,589.99 (dealer) · $1,679 – $2,599 (vendor-site snippets) | mixed |
| Power reclining loveseat | $1,709 – $2,509.99 | mixed |
| Manual rocker recliner | $497.99 – $1,199.99 | dealer |
| Power rocker recliner | $559 – $2,599 | mixed |

The full La-Z-Boy dealer catalog at Homemakers spans **$497.99–$1,519.99 for recliners** and **$977.99–$2,568.99 for sofas/loveseats**. Sources: [recliners](https://www.homemakers.com/shop/living-room/chairs-and-recliners/recliners/?prefn1=brand&prefv1=La-Z-Boy) · [sofas & loveseats](https://www.homemakers.com/shop/living-room/sofas-and-loveseats/?prefn1=brand&prefv1=La-Z-Boy).

---

## 3. Flexsteel — BEST / upper tier (MOTION ONLY)

### Corporate basics

| Item | Finding | Source |
|---|---|---|
| Legal entity | Flexsteel Industries, Inc. — public, NASDAQ: FLXS | [ir.flexsteel.com](https://ir.flexsteel.com/) |
| HQ | 385 Bell Street, Dubuque, Iowa 52001 | [Greater Dubuque Development Corp](https://www.greaterdubuque.org/business-development/major-employers/flexsteel-industries-inc) |
| Manufacturing | **Shifting toward Mexico.** Closed Dubuque manufacturing (213 jobs). Signed a lease for additional production space in **Juárez, Mexico**, where it already operates. Some product still described as "handcrafted in North America." | [BizTimes](https://biztimes.biz/after-shuttering-dubuque-manufacturing-plant-flexsteel-sees-signs-of-financial-progress/) · [CBS2 Iowa](https://cbs2iowa.com/news/local/dubuque-based-furniture-maker-considering-moving-some-production-out-of-the-country) |
| Strategic status | **Exited vehicle seating and hospitality** to focus on home furnishings. | [BizTimes](https://biztimes.biz/after-shuttering-dubuque-manufacturing-plant-flexsteel-sees-signs-of-financial-progress/) |
| FY2026 results | Q2 FY26 (ended 12/31/2025) net sales **$118.2M**, +9.0% YoY. Q3 FY26 (ended 3/31/2026) net sales **$115.1M**, +1.0% YoY. Navigating tariff impacts. | [Q2 FY26](https://ir.flexsteel.com/news-releases/news-release-details/flexsteel-industries-inc-reports-strong-fiscal-second-quarter-1/) · [Q3 FY26 PDF](https://ir.flexsteel.com/node/16386/pdf) |
| Leadership | CEO **Derek Schmidt** | [Q1 FY26 release](https://ir.flexsteel.com/news-releases/news-release-details/flexsteel-industries-inc-reports-strong-fiscal-first-quarter-0) |

### Published sub-brands / collections

From flexsteel.com navigation and the reclining category page: **Latitudes** (upscale, feature-rich; 165 products — sectionals, sofas, recliners, lift recliners), **Statements**, **Perfect Match** (customization program, 700+ fabrics), **Pulse** (immersive in-arm sound), **Stationary+**, **Zen**, **Zecliner** (lift/sleep recliners), **Rise**. Flexsteel publishes **no explicit good-better-best statement** — the ladder is inferred from feature content, not vendor-declared. Sources: [reclining living room](https://www.flexsteel.com/collections/living-room-reclining-furniture) · [Latitudes collection](https://www.flexsteel.com/collections/collections-latitudes).

### The construction story — Flexsteel's real differentiator

**Blue Steel Spring™** — patented seat spring system of steel ribbons and coils, powder-coated and painted blue, left visible under the deck. Vendor claims, verbatim:

> *"At the heart of our upholstered seating is the Blue Steel Spring™ — a patented spring system providing unmatched comfort, support and durability that has been trusted for more than 100 years."*
> *"Unlike sinuous wire springs, our springs never need retying."*
> *"We believe so strongly in our spring systems, we guarantee their durability for a lifetime of use."*

Three published variants: **C-Flex** (5000 Series), **DualFlex** (newer standard — "sturdy steel ribbons attached to flexible coils"), **Blue Ribbon** (7000 and 8000 Series). Source: [flexsteel.com/pages/blue-steel-spring](https://www.flexsteel.com/pages/blue-steel-spring).

This is the cleanest tier-differentiation argument available across the three brands: **Ashley opening-price stationary = platform deck (no springs); La-Z-Boy = sinuous wire; Flexsteel = patented ribbon-and-coil steel spring with a lifetime, transferable guarantee.**

### Published warranty (vendor-published — strongest warranty data in this report)

| Term | Covers |
|---|---|
| **Lifetime** | Blue Steel Springs · Wood Frames · Reclining Mechanisms · Seat Cushion Foam · Feathers · (drawer glides on case goods) |
| **Five years** | Electrical Components · Mechanical Components · Sleeper Mechanisms · Sleeper Mattresses |
| **One year** | Finished Wood · Plastic Components · Metal Components · Battery Packs · Filling Materials · Upholstery Materials · Heat & Massage Components |

Source: [flexsteel.com/pages/warranty](https://www.flexsteel.com/pages/warranty). Note the **5-year cap on motors/electrical** — a material difference vs. La-Z-Boy's lifetime mechanism coverage, and a point to press in negotiation.

### Flexsteel products — specs from vendor site, prices from dealer

> **flexsteel.com publishes NO prices** — not on listing pages, not on product detail pages. Verified across 4 product detail pages and 2 category pages. Street prices below are from **Woodstock Outlet**, an authorized dealer, and **could not be joined to vendor model numbers** because the dealer names products differently.

**A. Vendor-site products (model # + specs confirmed; price NOT PUBLISHED):**

| Brand | Collection | Product | Model # | Piece type | MSRP | Mechanism | Key specs | Source URL |
|---|---|---|---|---|---|---|---|---|
| Flexsteel | Oasis (Latitudes) | Oasis Storm Leather Power Reclining Sofa w/ Power Headrests, Lumbar, Heat & Massage | **1750-62P5-73440** | Power reclining sofa | **NOT PUBLISHED** | Power recline + power headrest + power lumbar, independent; **Zero Gravity**; heated seat; air massage; FlexSync app; USB-A + USB-C | **Blue Steel Spring™** seat system; **DualFlex** spring unit; **HC high-density** seat cushions; leather; 83"W×41"D×42"H; seat 69"×22"×20"; open depth 69"; 6" wall clearance; 284 lb | [flexsteel.com](https://www.flexsteel.com/products/1750-62p5-73440) |
| Flexsteel | Score | Score Leather Power Reclining Sofa w/ Power Headrests & Lumbar | **B3805-62L** | Power reclining sofa | **NOT PUBLISHED** | Power recline/headrest/lumbar independent; Zero Gravity; one-touch **Home** button; zero-draw USB | **DualFlex Spring System™** — "sturdy steel ribbons attached to flexible coils"; high-density foam core; attached back & seat cushions, divided backs; leather (also in Kashmira fabric); 87"W×42"D×43"H; open depth 71"; 9" wall clearance; 288 lb | [flexsteel.com](https://www.flexsteel.com/products/b3805-62l) |
| Flexsteel | Vibe (Pulse) | Vibe Fabric Power Reclining Sofa w/ Console, Power Headrest, Lumbar, Heat, Massage & Pulse | **1829-61P6-76302** | Power reclining sofa w/ console | **NOT PUBLISHED** | Power recline/headrest/lumbar; heat; massage; **Pulse** in-arm speakers; Flexsteel Pulse app; group connectivity; Zero Gravity; drop-down console w/ cupholders, USB-A/C, lighting, audio controls | Patented **Blue Steel Spring™** seat system; water-resistant leather-feel fabric; removable backrest; 87"W×41"D×44"H; seat 70"×22"×20"; 9" wall clearance; 322 lb | [flexsteel.com](https://www.flexsteel.com/products/1829-61p6-76302) |
| Flexsteel | Catalina | Catalina Fabric Reclining Sofa | **S2900-62** | Manual reclining sofa | **NOT PUBLISHED** | **Manual**, parachute release handles; end seats recline, center stationary | "Sustainably sourced wood frame"; **DualFlex** spring unit; **Blue Steel Spring™**; high-density foam seat cushions, divided backs; padded sloped track arms (24"); fully padded footrests; handcrafted in North America; 84"W×39"D×40"H; open depth 67"; 5" wall clearance | [flexsteel.com](https://www.flexsteel.com/products/s2900-62) |
| Flexsteel | Griffin | Griffin Leather Power Reclining Sofa w/ Headrest & Lumbar | **1949-62PH-94671** | Power reclining sofa | **NOT PUBLISHED** | Power recline + power headrest + lumbar | Specs not captured (listing page only) | [flexsteel.com](https://www.flexsteel.com/collections/living-room-sofas-reclining) |
| Flexsteel | Sense (Pulse) | Sense Leather Power Reclining Sofa w/ Power Headrest, Lumbar & Pulse | **1800-62P4-36701** | Power reclining sofa | **NOT PUBLISHED** | Power recline/headrest/lumbar + Pulse audio | Specs not captured | [flexsteel.com](https://www.flexsteel.com/collections/living-room-sofas-reclining) |
| Flexsteel | Sense (Pulse) | Sense Leather Power Reclining Loveseat w/ Console, Power Headrest, Lumbar & Pulse | **1800-64P4-36701** | Power reclining loveseat w/ console | **NOT PUBLISHED** | Power + Pulse audio | Specs not captured | [flexsteel.com](https://www.flexsteel.com/collections/living-room-reclining-furniture) |
| Flexsteel | Ziggy | Ziggy Leather Power Reclining Sofa w/ Power Headrest, Lumbar, Heat & Massage | **1782-62P5-43400** | Power reclining sofa | **NOT PUBLISHED** | Power + heat + massage | Specs not captured | [flexsteel.com](https://www.flexsteel.com/collections/living-room-sofas-reclining) |
| Flexsteel | Ziggy | Ziggy Leather Power Reclining Loveseat w/ Power Headrest, Lumbar, Heat & Massage | **1782-60P5-43400** | Power reclining loveseat | **NOT PUBLISHED** | Power + heat + massage | Specs not captured | [flexsteel.com](https://www.flexsteel.com/collections/living-room-sofas-reclining) |
| Flexsteel | Warren | Warren Leather Power Reclining Sofa w/ Console, Power Headrest & Lumbar | **1848-63P3-72775** | Power reclining sofa w/ console | **NOT PUBLISHED** | Power recline/headrest/lumbar | Specs not captured | [flexsteel.com](https://www.flexsteel.com/collections/living-room-sofas-reclining) |
| Flexsteel | Felix | Felix Leather Power Reclining Sofa w/ Power Headrest, Lumbar, Heat & Massage | **1536-62P5-40872** | Power reclining sofa | **NOT PUBLISHED** | Power + heat + massage | Specs not captured | [flexsteel.com](https://www.flexsteel.com/collections/living-room-sofas-reclining) |
| Flexsteel | Bernard | Bernard Leather Power Reclining Sofa w/ Console, Power Headrests & Lumbar | **B3871-63L** | Power reclining sofa w/ console | **NOT PUBLISHED** | Power recline/headrests/lumbar | Specs not captured | [flexsteel.com](https://www.flexsteel.com/collections/living-room-sofas-reclining) |
| Flexsteel | Ava | Ava Fabric Power Reclining Sofa w/ Power Headrest & Lumbar | **1685-62P3-15781** | Power reclining sofa | **NOT PUBLISHED** | Power recline/headrest/lumbar | Specs not captured | [flexsteel.com](https://www.flexsteel.com/collections/living-room-sofas-reclining) |
| Flexsteel | Arlo | Arlo Leather Reclining Sofa | **S3810-62** | Manual reclining sofa | **NOT PUBLISHED** | Manual | Specs not captured | [flexsteel.com](https://www.flexsteel.com/collections/living-room-sofas-reclining) |
| Flexsteel | Zecliner | Zecliner Sofa Fabric Power Reclining Sofa w/ Console, Power Headrest, Lumbar, Heat & Massage | **1080-63P5-35872** | Power reclining sofa w/ console | **NOT PUBLISHED** | Power + heat + massage | Specs not captured | [flexsteel.com](https://www.flexsteel.com/products/1080-63p5-35872) |

**B. Authorized-dealer street prices (price confirmed; vendor model # NOT resolvable):**

| Brand | Collection | Product (dealer naming) | Model # | Piece type | Street price | Mechanism | Source URL |
|---|---|---|---|---|---|---|---|
| Flexsteel | Pulse / Sense | Pulse Sense Greige Leather Power Reclining Immersive Sofa | NOT SHOWN | Power reclining sofa | **$4,996.88** | Triple power + Pulse immersive audio | [woodstockoutlet.com](https://www.woodstockoutlet.com/brands/flexsteel.html) |
| Flexsteel | Pulse / Sense | Pulse Sense Espresso Leather Immersive Power Reclining Sofa | NOT SHOWN | Power reclining sofa | **$4,996.88** | Triple power + Pulse | [woodstockoutlet.com](https://www.woodstockoutlet.com/brands/flexsteel.html) |
| Flexsteel | Dutch | Dutch Cortado Brown Leather Triple Power Reclining Sofa | NOT SHOWN | Power reclining sofa | **$3,297.87** | Triple power | [woodstockoutlet.com](https://www.woodstockoutlet.com/brands/flexsteel.html) |
| Flexsteel | Dutch | Dutch Desert Tan Leather Triple Power Reclining Sofa | NOT SHOWN | Power reclining sofa | **$3,297.87** | Triple power | [woodstockoutlet.com](https://www.woodstockoutlet.com/brands/flexsteel.html) |
| Flexsteel | Henry | Henry Burnt Umber Leather Zero Gravity Triple Power Reclining Sofa | NOT SHOWN | Power reclining sofa | **$2,997.87** | Triple power + Zero Gravity | [woodstockoutlet.com](https://www.woodstockoutlet.com/brands/flexsteel.html) |
| Flexsteel | Henry | Henry Caramel Leather Triple Power Reclining Sofa | NOT SHOWN | Power reclining sofa | **$2,997.87** | Triple power | [woodstockoutlet.com](https://www.woodstockoutlet.com/brands/flexsteel.html) |
| Flexsteel | Sawyer | Sawyer Greige Leather Zero Gravity Power Reclining Console Loveseat | NOT SHOWN | Power reclining console loveseat | **$2,997.87** | Power + Zero Gravity | [woodstockoutlet.com](https://www.woodstockoutlet.com/brands/flexsteel.html) |
| Flexsteel | Dutch | Dutch Cortado Leather Triple Power Reclining Console Loveseat | NOT SHOWN | Power reclining console loveseat | **$3,297.87** | Triple power | [woodstockoutlet.com](https://www.woodstockoutlet.com/brands/flexsteel.html) |
| Flexsteel | Pulse / Sense | Pulse Sense Greige Leather Power Reclining Immersive Console Loveseat | NOT SHOWN | Power reclining console loveseat | **$4,996.88** | Triple power + Pulse | [woodstockoutlet.com](https://www.woodstockoutlet.com/brands/flexsteel.html) |
| Flexsteel | Dutch | Dutch Desert Tan Leather Triple Power Recliner | NOT SHOWN | Power recliner | **$1,897.88** | Triple power | [woodstockoutlet.com](https://www.woodstockoutlet.com/brands/flexsteel.html) |
| Flexsteel | Oasis | Oasis Storm Leather Triple Power Recliner w/ Heat & Massage | NOT SHOWN | Power recliner | **$1,897.96** | Triple power + heat & massage | [woodstockoutlet.com](https://www.woodstockoutlet.com/brands/flexsteel.html) |
| Flexsteel | Pulse / Sense | Pulse Sense Espresso Leather Immersive Power Recliner | NOT SHOWN | Power recliner | **$3,996.88** | Power + Pulse | [woodstockoutlet.com](https://www.woodstockoutlet.com/brands/flexsteel.html) |
| Flexsteel | Henry | Henry Leather Triple Power Swivel Glider Recliner w/ Heat & Massage | NOT SHOWN | Power swivel glider recliner | **$1,997.87** | Triple power + heat & massage | [woodstockoutlet.com](https://www.woodstockoutlet.com/brands/flexsteel.html) |
| Flexsteel | Zecliner | Zecliner Model 2 LiveSmart Dove Grey Triple Power Reclining Lift Chair | NOT SHOWN | Power lift recliner | **$2,149.84** | Triple power lift | [woodstockoutlet.com](https://www.woodstockoutlet.com/brands/flexsteel.html) |
| Flexsteel | Zecliner | Zecliner Model 2+ Nanobionic Shell Triple Power Lift Recliner | NOT SHOWN | Power lift recliner | **$2,593.30** | Triple power lift | [woodstockoutlet.com](https://www.woodstockoutlet.com/brands/flexsteel.html) |
| Flexsteel | Oasis | Oasis Truffle / Storm Leather 6-Pc Triple Power Reclining Sectional | NOT SHOWN | Power reclining sectional | **$7,698.77** | Triple power | [woodstockoutlet.com](https://www.woodstockoutlet.com/brands/flexsteel.html) |

**Flexsteel observed street price bands (one dealer, leather-heavy sample):**

| Piece type | Range |
|---|---|
| Power recliner | $1,897.88 – $3,996.88 |
| Power lift recliner (Zecliner) | $2,149.84 – $2,593.30 |
| Power reclining console loveseat | $2,997.87 – $4,996.88 |
| Power reclining sofa | $2,997.87 – $4,996.88 |
| Power reclining sectional (6-pc) | $7,698.77 |

---

## Cross-brand ladder — what the data actually supports

Comparing **power reclining sofa** (the one piece type present in all three):

| Tier | Brand | Observed street price | Suspension | Motor/electrical warranty |
|---|---|---|---|---|
| GOOD | Ashley | $1,091 – $3,200 | Corner-blocked frame, metal reinforced seat (springs not specified on motion) | NOT PUBLISHED |
| BETTER | La-Z-Boy | $1,679 – $2,590 | Sinuous wire spring | Limited Lifetime on mechanism; electrical terms NOT PUBLISHED |
| BEST | Flexsteel | $2,998 – $4,997 | Patented Blue Steel Spring (DualFlex / C-Flex / Blue Ribbon) | **5 years** on electrical & mechanical |

**The tiers overlap in the $1,700–$2,600 band.** Ashley's The Man-Den at $2,050–$3,200 sits on top of La-Z-Boy's duo line at $2,028–$2,590. A clean Good/Better/Best ladder will require deliberate SKU selection — pushing Ashley motion down toward the $1,100–$1,400 Draycoll/Tip-Off band and taking Flexsteel up into Pulse/Dutch — rather than simply taking each brand's mid-line.

**Feature ladder is cleaner than the price ladder:** Ashley tops out at power + Easy View headrest + lumbar. La-Z-Boy adds PowerXR+ with memory settings. Flexsteel adds Zero Gravity, heat, air massage, app control, and in-arm Pulse audio — features neither competitor offers in this sample.

---

## Data quality

### What is solidly verified
- **Corporate basics for all three brands.** La-Z-Boy and Flexsteel figures come from their own investor-relations releases (FY2026, current). Ashley's come from an encyclopedic secondary source, not from Ashley — weaker but internally consistent.
- **Flexsteel construction specs and warranty.** Vendor-published, fetched directly from flexsteel.com. This is the highest-confidence product data in the report: model numbers, spring system, cushion spec, dimensions, wall clearance, weights, and a complete three-tier warranty schedule.
- **Flexsteel model numbers.** 15 current motion SKUs pulled directly from vendor listing and detail pages.
- **Ashley construction boilerplate.** Consistent across many independent dealer pages, so the language is almost certainly Ashley's own copy.
- **La-Z-Boy style-number convention and the duo® line composition.**

### What could NOT be verified
- **Ashley: no vendor-site access at all.** Every ashleyfurniture.com URL returned HTTP 403. All Ashley product data is second-hand from dealers/marketplaces. **Not circumvented** — no user-agent spoofing, no proxy, no login attempted.
- **La-Z-Boy: no vendor-site rendering.** la-z-boy.com is client-side rendered and returned a load-failure notice on every attempt. La-Z-Boy prices marked "*(snippet)*" come from **search-engine result summaries quoting the vendor site**, not from pages I read. Those are the weakest numbers in this document.
- **Flexsteel MSRP does not exist publicly.** Confirmed across 6 pages. Flexsteel is wholesale-only to consumers; there is no published price ladder.
- **True MSRP for any brand.** Every price here is either a promotional "sale/was" pair or a dealer street price. No brand publishes a wholesale sheet or a real MSRP list publicly.
- **La-Z-Boy component-level warranty durations.** Only the summary ("lifetime on frame, springs, mechanism") could be sourced, and only from dealer/third-party pages.
- **Motor counts.** Almost never published. Only two confirmed: Ashley Snowfield 1760912 (dual motors) and La-Z-Boy Roscoe duo P91892 (two, one per seat). Everything else is UNVERIFIED.
- **Foam density and fabric/leather grades.** **NOT PUBLISHED by any of the three brands.** Descriptive language only ("high-resiliency," "high-density," "HC," "high grade"). No lb/ft³, no ILD, no double-rub counts, no leather grade designations anywhere in public data.
- **Ashley Oatman model number** — sources give both 1800412 and 1800512.
- **Ashley tier hierarchy** (Signature / Benchcraft / Millennium) is asserted by retailers, not by Ashley.

### Weakest claims — do not act on these without confirmation
1. **All La-Z-Boy prices marked "*(snippet)*"** — Pinnacle P10512 $1,819, James X44521 $1,679, Maverick $559, Trouper loveseat $1,709. Search-summary provenance only.
2. **Flexsteel price-to-model mapping.** Prices and model numbers come from two different sources that do not share a naming scheme. **You cannot currently quote a price against a Flexsteel model number.** The dealer's "Dutch," "Henry," and "Pulse Sense" names could not be matched to vendor SKUs.
3. **Ashley's "3x better than a spring system after 20,000 cycles"** platform-foundation claim — vendor marketing copy, no test standard cited.
4. **Single-dealer bias on Flexsteel pricing.** One retailer (Woodstock Outlet), heavily weighted to leather and triple-power. Fabric and entry-level Flexsteel motion is unrepresented, so the low end of Flexsteel's real range is probably below $2,998.

### Recommended next step
The gaps that matter most for a 65-SKU buy — real MSRP/wholesale, foam density, fabric grades, motor counts, and cover depth — are **not public for any of these three brands**. They require a line sheet from each vendor's rep. This research establishes what to ask for; it does not substitute for the ask.
