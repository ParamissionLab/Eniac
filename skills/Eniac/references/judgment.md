# Judgment

The Ego Loop says the Ego decides. This is *how* — the techniques that separate a
decision from a preference, for the choices where being wrong is expensive.

Load this when a choice is hard to reverse, when two credible options compete, when
committing to a plan of real size, or when the same decision keeps getting revisited.
Do not load it for a reversible choice with cheap proof: there, deciding quickly and
letting reality answer is strictly better than reasoning longer.

> **Owns** — deciding when being wrong is expensive — one-way versus two-way doors, pre-mortem, inversion, disconfirming evidence, base rates, cost of error, second-order effects, Goodhart's law, recording a decision with its falsifier, when to stop deciding.
> **Defers** — choosing a shape to build → `lifecycle.md#design-before-building`; working a problem that is hard to hold → `reasoning.md`; when to switch out of fast thinking → `operating-manual.md#fast-and-slow`.

## Sort The Door First

Reversibility, not importance, sets how much thinking a decision deserves.

- **Two-way door** — undoable in an hour: a function's shape, a file layout, a library
  you have not built on yet. **Decide fast and let the code answer.** Deliberating over
  these is the most common way careful people waste a day.
- **One-way door** — expensive or impossible to undo: a persisted data shape, a public
  contract, a dependency that spreads, a deleted record, a published release. These earn
  competing options, discriminating evidence, and a written reason.

Most decisions that *feel* momentous are two-way doors dressed up by novelty. Ask what
undoing it would actually cost, in hours, before spending anything on the choice.

## Pre-Mortem

Before committing to a plan of any size, spend two minutes in the future:

> It is three months from now. This failed badly. What happened?

Then write the three most likely answers and address the cheapest one now.

This works because it changes the question from "will this work" — which invites
supporting evidence — to "how did it fail", which invites the specific, concrete
failure modes that a forward-looking plan never surfaces. It routinely finds things no
amount of careful planning does, and it costs almost nothing.

## Invert

When stuck on "how do I make this succeed", ask the opposite: **what would guarantee
this fails?** Then avoid those.

Avoiding certain failure is usually easier and more reliable than engineering success,
and the inverted list is far more concrete. "Ensure a clean migration" produces nothing
actionable; "guarantee data loss" produces *no backup, no reversal test, run it during
peak, no row counts* — a checklist by construction.

## Hunt For Disconfirming Evidence

The evidence that changes a decision is the evidence that contradicts it, and you will
never encounter it by looking for support.

- State the observation that would kill your preferred option, then go look for it
  specifically.
- If you cannot name such an observation, the choice is not yet a hypothesis. It is a
  preference wearing an argument.
- Give the strongest version of the option you rejected a real reading. Refuting a weak
  version of it teaches nothing and leaves the real risk untouched.

## Use Base Rates, Not The Plan

An estimate built from the steps you can see is always optimistic, because the steps you
cannot see are exactly the ones you did not budget for.

Ask instead: **how did the last three similar things actually go?** The migration that
was supposed to take a day, the "simple" dependency upgrade, the refactor that touched
one more layer than expected. That outside view is a better predictor than any
step-by-step breakdown, and it is available for free from the repository's own history.

When the inside view and the base rate disagree, the base rate is usually right, and the
plan needs a reason it is different — not confidence that it is.

## Weigh The Cost Of Being Wrong

Probability is only half of a decision. A 5% chance of losing production data outranks a
60% chance of a slower endpoint, and no amount of confidence reverses that.

For each option ask: if this turns out wrong, what does it cost, and can it be detected
before it hurts? Prefer the option whose failure is loud, cheap, and early over the one
whose failure is quiet, expensive, and late — even when the second looks more likely to
succeed.

## Think One Step Past The Obvious

"And then what?" — twice.

Adding a cache makes reads fast; *and then* stale data appears in a report nobody
suspects. Retrying failed requests improves reliability; *and then* a slow dependency
receives four times the load and stops recovering. Splitting a service improves
ownership; *and then* every feature needs two deploys in the right order.

First-order effects are why a change is proposed. Second-order effects are why it gets
reverted six weeks later.

## When The Cause Is Unknowable, Probe

Some problems yield to analysis and some do not. Telling them apart saves the most time:

- **Analyzable** — the mechanism is knowable by reading. Read, then act. More
  experimentation here is waste.
- **Not analyzable** — emergent behavior, an unfamiliar system, a heisenbug, an
  interaction nobody has modelled. **The cheapest probe beats the best reasoning.** Run
  the small safe experiment and let the system answer.

Three failed rounds of reasoning about a system you could have poked in thirty seconds
is the signature failure here, and it is the same trap as the stuck protocol in SKILL.md.

## Where Fast Thinking Fails Predictably

`SKILL.md` says when to switch from fast to slow. These are the specific ways the fast
answer goes wrong — each of which feels like confidence from the inside.

- **Anchoring.** The first hypothesis, the first estimate, the first file you opened
  contaminates everything after it: later evidence gets read as an adjustment to the
  anchor rather than on its own terms. *Countermeasure:* generate the second and third
  candidate before investigating the first.
- **What you see is all there is.** A coherent story built from the evidence you happen
  to hold feels complete, and the completeness of the story is not evidence of the
  completeness of the evidence. Three files produce a confident answer about a system of
  three hundred. *Countermeasure:* before concluding, name one thing you did not look at
  that could change the answer.
- **Fluency read as truth.** An explanation that comes out smoothly feels correct. In an
  unfamiliar system that correlation runs backwards — the smooth answer is the one
  assembled from patterns elsewhere, not from this code.
- **Confirmation.** Once a hypothesis exists, everything after is read as support for it.
  This is why the falsifier is written down *before* the evidence arrives.
- **Availability.** The cause you saw most recently feels most likely. It is not; it is
  only the easiest to recall.

None of these are fixed by being careful, because each one feels like being careful. They
are fixed by procedure that does not depend on how you feel: a written falsifier, a
competing candidate generated first, a named unknown.

## Goodhart's Law

**When a measure becomes a target, it stops measuring what it measured.**

Coverage rises and tests assert nothing. Latency improves and work moves into a
background job that fails silently. Ticket counts drop and problems stop being reported.

When proposing or being handed a numeric target, name what it is a proxy for, and check
that the proxy still holds after the change. If a number can be satisfied without the
underlying thing improving, it will eventually be satisfied that way — usually without
anyone deciding to cheat.

## Record The Decision With Its Falsifier

Every non-obvious choice ends with one line that makes it revisitable:

```text
Chose:        X over Y
Because:      the evidence or constraint that decided it
Revisit if:   the specific condition that would reopen this
```

`Revisit if` is the field that keeps a decision honest. Without it, a choice made under
conditions that no longer hold gets defended forever by people who were not there. For a
decision that will outlive the session, use the fuller record in `campaigns.md`.

## Stop Deciding

Analysis has a cost and it compounds while nothing ships.

Stop when: the remaining options differ by less than the cost of comparing them; the
decision is a two-way door; more evidence would need work that is more expensive than
being wrong; or you are gathering information you have already stopped using.

A reversible decision made now, with a stated falsifier, beats a perfect decision made
tomorrow — and reality is a faster evaluator than any amount of reasoning about it.
