---
name: gated-plan
description: Plan multi-step work as phases with approval gates, saved to PLAN.md so it survives across sessions. Do one phase, stop at its gate, and move on only when James approves. Use when he says "gated plan", "plan this out", "build a plan with gates", "phase it", "keep me in the loop at each step", "pick up where we left off", "resume the plan", or starts any work that will span more than one session (a website build, a message system, a strategy). Also use whenever a PLAN.md already exists in the working folder and he asks what's next.
---

# Gated Plan

Plan the work, then do it one phase at a time. Stop at every gate. James
steers; you never decide on his behalf to keep going.

## On every start: look for a plan first

1. Look for `PLAN.md` in the working folder (or the path James names).
2. **If it exists:** read it, then report in three lines: the goal, the
   current phase and its status, and the decision waiting on him. Ask:
   "Continue here?" Do no work before he answers.
3. **If it doesn't:** write one (below). Do no other work first.

## Writing PLAN.md

Ask only what you can't infer. If he hasn't said what winning looks like,
ask that one question before writing. Then write:

```markdown
# Plan: <name>

**Goal:** <one sentence>
**Winning looks like:** <how we'll know it worked>
**Out of scope (v2):** <what we are deliberately not doing>

## Phases

### 1. <name> — status: not started
- **Output:** <the thing this phase produces>
- **Done means:** <a test anyone could check>
- **Gate:** <the decision James makes before phase 2>

### 2. ...

## Log
- <date> — Plan created.
```

Rules for the phases:
- 3 to 8 phases. More than 8 means the plan is too big: split it.
- Order them so each phase's output is the next phase's input.
- Every gate is a real decision, not "looks good?". Name what is being
  decided (e.g., "Pick one of the three one-liners").

Show him the plan. **Gate 0 is approving the plan itself.** Nothing starts
until he approves it.

## Working a phase

1. Mark the phase `in progress` in PLAN.md.
2. Do only that phase. If you find work that belongs to a later phase,
   note it under that phase; don't do it.
3. Check the output against "Done means." If it fails, fix it or say why.
4. Mark it `at gate` and stop.

## At every gate, show exactly this

- **Done:** what the phase produced, and where it is.
- **Decision needed:** the gate question, stated plainly.
- **My recommendation:** one option, and why, in one or two lines.
- **Open issues:** anything unverified or assumed. Say "none" if none.

Then wait. Do not start the next phase in the same turn.

## After his answer

- **Approved:** mark the phase `done`, log the decision, start the next phase.
- **Change X:** make the change, show the gate again.
- **Skip:** mark it `skipped`, log why, move on.
- **New idea mid-plan:** add it to "Out of scope (v2)" unless he says it
  belongs in the current plan. If it does, update the phases and show the
  changed plan as its own gate.

Every decision goes in the Log with the date, so the next session knows
what was decided and why.

## Never

- Never run two phases in one turn.
- Never treat silence or "ok" on an unrelated point as approval.
- Never edit an approved phase's output without saying so at the next gate.
- Never let the plan live only in chat. If it isn't in PLAN.md, it didn't happen.
