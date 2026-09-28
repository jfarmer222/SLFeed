# Career Evidence Agent — Build Plan

**Status:** Draft for approval · 2026-09-28

## 1. What this agent is

A junior analyst working for a top-producing partner at a top-tier executive
search firm. Its job is to build a complete, verified, well-organized **evidence
file** on one candidate: you.

It is **not** a resume writer. The resume, bio, and cover notes come later and
draw from this file. The file is the single source of truth.

**Proposed definition of winning** (confirm or change):

1. Every claim a partner or board would test is in the file, with a number, a
   baseline, your role in it, and where it can be proven.
2. A partner could read the file cold and pitch you to a CEO or board in
   5 minutes without calling you.
3. Every weak spot (gaps, short stints, exits, missing scope) is named and has
   a prepared, honest positioning line.

## 2. How a session works (the core loop)

Each fact goes through six steps. The agent drives; you answer.

| Step | What the agent does |
|---|---|
| **1. Ask** | Asks one targeted question, picked from the gap list (what's missing or thin). |
| **2. Capture** | Records your answer as-is, raw, in your words. |
| **3. Clarify** | Probes until the fact is complete. Standard probes: *scope* (P&L, headcount, budget, geography), *number* (how much, how fast), *baseline* (from what, vs. what), *attribution* (you led / co-led / team), *proof* (who or what can confirm it), *date*. Max 2–3 probes per fact; flags the rest as open. |
| **4. Place** | Decides which section(s) the fact belongs in (see §3) and says why in one line. You can overrule. |
| **5. Write** | Writes the entry in senior-leader register (see §4). Shows it to you. |
| **6. Log** | On your OK, saves it to the evidence bank with its source and confidence level, then updates the gap list. |

**Session modes**

- **Sweep** — walks each role, newest first, filling the career spine.
- **Deep dive** — takes one signature win and builds it out fully.
- **Gap hunt** — targets the thinnest sections only.
- **Partner review** — the agent switches role and cross-examines the file the
  way a search partner or board member would. Output: list of weak claims and
  missing proof.

## 3. Where facts go (the evidence bank)

| # | Section | What goes in it |
|---|---|---|
| 1 | **Career spine** | Each role: employer, title, dates, reporting line, P&L, revenue, headcount, budget, geography, board exposure, why you joined, why you left. |
| 2 | **Signature wins** | 6–10 best stories. Each: situation, what you did, result (number + baseline), your share, proof. |
| 3 | **Leadership capabilities** | Evidence mapped to the capability areas search firms assess senior leaders on (final list set in build step 2 from cited sources). Working draft: strategy, results/P&L, transformation and change, talent and team building, board and stakeholder influence, commercial and financial acumen, technology and AI fluency, risk and crisis. |
| 4 | **Numbers ledger** | Every metric in one table: value, baseline, period, source, confidence. Stops the same number drifting between documents. |
| 5 | **Proof and sources** | Documents, press, filings, awards, reviews, public data backing each claim. |
| 6 | **References and sponsors** | Names, relationship, what each can speak to. Contact details only as you give them — never invented. |
| 7 | **Risks and positioning** | Anything a partner would probe: gaps, short tenures, exits, industry switch, missing scope. Each gets a factual, prepared line. |
| 8 | **Market positioning** | Target roles, sectors, company stage, and the "why you, why now" case, tied to current market demand. |

**Every entry carries these fields:** ID · section · role/employer · dates ·
raw fact (your words) · clarified fact · metric · baseline · attribution ·
proof/source · confidence · written line · open questions · status.

**Confidence levels:**
- `Verified` — backed by a document or public source.
- `Stated` — you stated it; no document yet.
- `Estimate` — approximate; must be labeled as such anywhere it's used.

## 4. Writing standard (senior-leader register)

- Facts first. Number first where there is one.
- Scope before result: "Led a $400M, 1,200-person unit…" then the outcome.
- Every result has a baseline and a time frame.
- Honest attribution: "led", "co-led", "sponsored", "contributed to" mean
  different things and are used precisely.
- No adjectives doing the work of evidence ("visionary", "passionate",
  "results-driven" are banned).
- Short sentences, common words, active verbs.
- Confidential numbers become ranges or percentages; the file notes that the
  exact figure exists.

## 5. Market awareness

The agent writes to what boards and search firms are asking for **now**, not
from memory. Build step 2 produces a short, cited market brief (sources:
published search-firm research, board-practice reports, reputable business
press, dated 2025–2026). The brief sets:

- the capability list in Section 3,
- which proof points carry the most weight today,
- the questions a partner is most likely to ask.

Rule: no trend goes in the brief without a source. Single anecdotes don't count.
Brief is refreshed each quarter.

## 6. Guardrails

1. Never invent a fact, number, date, title, or contact detail.
2. Never round up. Never upgrade attribution ("contributed" never becomes "led").
3. Unconfirmed items stay `Stated` or `Estimate` until proven.
4. Memory files (Profile, Exec Job Search) are canonical; the agent reads them
   first and does not re-ask what's there. Conflicts are flagged, not
   silently resolved.
5. Nothing is sent outside the file without your review.

## 7. Where to build it — options

| Option | How | Pros | Cons |
|---|---|---|---|
| **A. Claude Project (recommended)** | Project instructions = agent spec; evidence bank as a living Claude Doc; market brief and question bank as project files. | Conversational, works on phone, ties to your Memory files, no setup. | Bank is a document, not a database; harder to filter at scale. |
| B. Airtable base + Claude | Evidence bank as an Airtable table (one row per entry); agent writes rows via the connector. | Filter/sort by section, confidence, status; good once you have 100+ entries. | More setup; less readable as a narrative. |
| C. Claude Code skill in a repo | SKILL.md + markdown bank in a private repo. | Version history on every change. | Worst fit for a conversational interview. |

**Recommendation: A now, B later if the bank passes ~100 entries.** The job is
an interview; A is built for conversation, and you already use Memory files
there. Airtable can be added without changing the spec.

Note: this repo (SLFeed) is the upholstery assortment project. Career material
should live in its own private space — this plan is here only because it's the
assigned branch. Move it once the build home is chosen.

## 8. Build steps

| Step | Output | Done when |
|---|---|---|
| 1. Approve spec | This plan, with your edits | You confirm "winning" (§1) and build home (§7). |
| 2. Market brief | `market-brief` — cited, 1–2 pages | Every trend has a source; capability list for §3 is final. |
| 3. Agent instructions | System prompt / project instructions implementing §2–§6 | Covers the loop, modes, placement rules, writing standard, guardrails. |
| 4. Templates | Evidence bank skeleton (8 sections), entry template, numbers ledger, gap list | Empty bank ready to fill. |
| 5. Question bank | 60–80 probing questions by section and by role level | Each question maps to a section. |
| 6. Pilot | One 30-minute session on your most recent role | 5+ entries logged, reviewed by you. |
| 7. Partner review test | Agent cross-examines the pilot entries | Weak claims found and fixed; tune instructions. |
| 8. Full sweep | All roles, all sections | Gap list shows no critical gaps. |

## 9. Quality checks (run after every session)

- Every entry has a source and a confidence level.
- No number appears with two different values across the bank.
- Every signature win has scope, number, baseline, attribution, proof.
- Every risk in Section 7 has a positioning line.
- Written lines pass the §4 checklist.
