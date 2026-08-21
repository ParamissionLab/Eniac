# Triage And Work Management

The ladder in SKILL.md decides *what* is next. This file handles what comes after:
ordering work that depends on other work, running more than one thread safely,
surviving an interruption, and handing off.

Load this when the work has parts that depend on each other, might be interrupted, or
will be picked up by someone else.

## Ranking Inside A Tier

Within one ladder tier, order by `impact ÷ cost`, then break ties with:

1. **Unblocks the most** — a fix that lets three other things proceed outranks a
   bigger fix that unblocks nothing.
2. **Cheapest reversibility** — prefer the move you can undo while information is
   still scarce.
3. **Highest information gain** — when the plan itself is uncertain, the item that
   resolves the most uncertainty is worth doing before the item with the most value.
4. **Decay** — anything that gets more expensive with time (a growing corruption, a
   branch drifting from main, an expiring credential) moves up.

Do not score to three decimal places. This is an ordering heuristic; if two items
score the same, pick one and move.

**Improving what is not the constraint changes nothing.** A faster step feeding a queue
that is already backed up produces a longer queue, not a faster result — and the same holds
for a process, a pipeline, or a team. Before optimizing anything, identify what is actually
limiting the outcome, and be willing to find that it is not the part you were looking at.

## Dependency Ordering

Before starting multi-part work, write the edges, not the list:

```text
A: schema change        -> blocks B, C
B: API handler          -> blocks D
C: migration script     -> blocks ship
D: client update
```

Then execute in waves: everything with no unmet dependency, verified, before the next
wave. Two rules matter more than the diagram:

- **Shared contracts change first, alone, and get proven before dependents move.**
  Changing a contract and its consumers in one motion means a failure has no
  bisection point.
- **A wave closes on proof, not on edits being written.** An unverified wave that
  feeds the next wave multiplies the debugging cost of everything downstream.

## Parallel Lanes

Parallelism is only safe when the lanes cannot collide. Before splitting, all four
must hold:

1. **Disjoint mutable scope** — no two lanes write the same file or table.
2. **Stable inputs** — nothing a lane depends on is being changed by another lane.
3. **Independent proof** — each lane can be verified without the others finishing.
4. **Defined integration** — you know how the results merge and who checks it.

If any one fails, run sequentially. Sequential-and-correct finishes sooner than
parallel-and-tangled.

This does not repeal `WIP = 1`. That rule governs *your own attention* — one item being
actively worked, not several half-edited. A lane someone or something else is executing
is not your work in progress; the moment you are switching between lanes yourself, it is,
and you are back to sequential.

The owner of the overall task keeps the plan, the shared contracts, integration, and
the final proof. A lane never widens its own scope or changes a shared contract on
its own; a finished lane is accepted only after integration review.

For fan-out across services, teams, or many sessions — the worker contract, integration
gates, and when coordination cost exceeds the benefit — see `campaigns.md#delegation`.

## Plan Files

Write a plan to a file when the work has more than two proof-bound milestones, spans
sessions, or may be interrupted. Skip it for read-only answers, reviews, and anything
one focused edit closes — a plan file for a one-line fix is pure overhead.

Keep it small and replace stale content rather than appending a log:

```text
Goal:            one sentence, the outcome
Done when:       observable criteria
Scope:           paths and surfaces authorized to change
Out of scope:    what must not be touched
Contracts:       what other code depends on and must keep working
Milestones:      [ ] name — proof that closes it
Now:             current action
Signal:          latest observed evidence
Blocked:         what is stuck and on what
Risk:            the thing most likely to go wrong
```

Reconcile the plan against any new user message before the next mutation. If the user
changed the goal, the plan is wrong until you update it, and acting on a stale plan is
how agents deliver the wrong thing confidently. Delete the plan file when the work
closes.

Once the work spans many sessions or a staged rollout, this shape is no longer enough —
use the campaign contract and checkpoint format in `campaigns.md` instead, which is
built to survive total context loss.

## Parking And Resume

Parking an item costs something, so park deliberately — but a half-finished thing
carried only in context is lost at the next boundary.

To park, record four things: where it stopped, what is already proven, what would
prove it done, and the next single action. Anything less and resuming means
re-deriving from scratch.

On resume: re-read the plan, verify the world still matches it (branch, files, test
state), then continue. Do not re-plan work that is already accepted, and do not trust
a remembered state over an observed one.

## Interrupts And Re-triage

Re-triage when — and only when — one of these happens:

- a tier-1 or tier-2 item appears,
- the user changes or clarifies the request,
- the same fix fails twice,
- the cost estimate doubles.

Otherwise, hold. Reprioritizing on every new observation is churn, and churn looks
like progress while producing none.

When a tier-1 item interrupts committed work, park properly first. Abandoning the
current item mid-edit tends to leave the repository in a state that is worse than
either finishing or reverting.

## Estimation

Estimates are for ordering, not for promising. Two heuristics carry most of the value:

- **The doubling rule** — when an item passes twice its expected cost, stop and
  re-decide rather than pushing on. Sunk cost is the most expensive input to a
  priority decision.
- **Uncertainty is cost** — an item with an unknown cause is not "small". Timebox the
  investigation, then re-estimate with what you learned.
- **Use the outside view.** How long did the last three similar things in this repository
  actually take? A step-by-step estimate counts only the steps you can see, and the
  overrun always comes from the ones you cannot. History is free and predicts better than
  the breakdown does.

## Handoff

A handoff is only useful if the next person or session can act without asking you
anything. Include: the goal, what is done and proven, what is unproven, the exact next
action, known traps, and every command needed to reproduce the current state. Leave out
narrative, superseded hypotheses, and anything you did not actually verify.

The field most often missing is what the next person should *not* touch until an open
question is answered. `findings.md` carries the full minimum bar.
