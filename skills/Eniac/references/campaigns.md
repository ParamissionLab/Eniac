# Campaigns — Long-Horizon Work

Work that spans many sessions, hundreds of files, or a staged rollout is not a big task.
It is a different activity, and the constraint changes: thinking stops being the
bottleneck and **memory** becomes one — what was known last session, what is already
proven, what must not be redone.

Load this at M1 and above — work crossing sessions, hundreds of files, or a staged
rollout. Do not load it for anything one session can finish.

This is the reality principle at full stretch. Gratification is deferred for days or
weeks, so the discipline is making progress *durable* rather than *visible*. Everything
below exists to make the work survive an interruption, a context loss, or a different
person picking it up.

> **Owns** — work that outlives one session — the campaign contract, checkpoints designed to survive context loss, codemods and verified waves, migration patterns, staged rollout, durable decision records, honest abandonment.
> **Defers** — the mechanics of one release → `workflows.md#ship`; unattended fan-out and envelopes → `autonomy.md`; modelling a system too large to read → `scale.md`.

## The Campaign Contract

Write this once, at the start, in a file. Everything else derives from it.

```text
Goal:          the end state, in one sentence
Done when:     observable criteria — how anyone can confirm it is finished
Invariant:     what must remain true at every intermediate point
Phases:        ordered, each independently shippable and independently revertible
Not doing:     the adjacent work this campaign refuses
Kill criteria: what would make abandoning this the right decision
Rollback:      how to get back to a good state from any phase
```

**Every intermediate state must be a good state.** A campaign is interrupted — by a
priority change, an incident, a context loss, a person leaving. If the system is only
coherent at the end, an interruption leaves it broken. This single property is what
separates a campaign that survives contact from one that does not.

**Kill criteria are written first, before sunk cost exists.** After two weeks of
investment, no one can judge whether to stop.

## Checkpoints

A checkpoint must be readable by someone with no memory of the work. Assume total
context loss between every session, because eventually you get one.

```text
Phase:      which one, and where inside it
Proven:     what is verified done, and the command that proves it
Unproven:   what is written but not yet verified
Next:       the single next action, concretely
Learned:    what turned out to be different from the plan
Traps:      what will bite whoever continues
```

Update it at every phase boundary and before any long-running or risky step. Do not
append a log — replace the content. A checkpoint is a current-state snapshot, and a
history of snapshots is just an expensive way to hide the current one.

**Resume protocol:** read the checkpoint, then *verify the world matches it* — branch,
working tree, test state, what is deployed. Never trust remembered state over observed
state. Memory of a large system is reliably wrong in small ways, and the small ways are
where the day goes.

## Large Mechanical Change

For a transformation across dozens or hundreds of files:

1. **Prefer a codemod to hand edits** past roughly twenty files. A script is reviewable,
   re-runnable, and consistent; hand edits are none of those and drift as you tire.
2. **Pilot on three files.** Verify. The rule always survives three and frequently dies
   at thirty — better to learn that at three.
3. **Wave, verify, wave.** Each wave is one mechanical rule, committed separately, with
   the suite run between. This preserves a bisection point; one 400-file commit does not.
4. **Separate mechanical from semantic, absolutely.** A rename and a behavior change in
   the same wave makes review impossible and hides a real regression inside noise.
5. **List the exceptions explicitly** rather than special-casing them silently inside the
   script. Exceptions are findings.
6. **Report the count** — files matched, changed, skipped, and why. A silent partial
   application reads as complete and is the failure mode of every large sweep.

## Migration Patterns

Never change a persisted shape or a published contract in one step. Each pattern below
exists so that at every moment, both the old and new worlds work.

- **Expand → migrate → contract.** Add the new shape alongside the old; move readers and
  writers over; remove the old only once nothing references it. Three separate releases,
  never compressed.
- **Dual write → backfill → read switch → stop dual write.** For data moves: write to
  both, backfill history, flip reads behind a flag, verify, then retire the old write.
  The backfill must be idempotent and resumable, because it will be interrupted.
- **Strangler fig.** For replacing a system: route a slice of traffic to the new
  implementation, grow the slice, delete the old path last. The old system stays
  authoritative until the new one has proven itself on real traffic.
- **Feature flags with a removal date.** A flag is temporary scaffolding. Flags without
  an owner and a removal date become permanent conditional complexity, and a codebase of
  stale flags has no comprehensible behavior at all.

For every pattern, the deployment order matters as much as the code: consumers must
tolerate both shapes before producers emit the new one.

## Rollout

- **Stage it**: one instance, then one tenant or region, then a percentage, then all.
- **Name the signal before starting** — the specific error rate, latency figure, queue
  depth, or business metric you will watch, and the value that means abort.
- **Write the abort criteria up front.** Mid-rollout, under pressure, with partial data,
  is the worst possible moment to decide what "bad enough" means.
- **Watch through one full cycle** before widening — a daily job, a peak hour, a batch
  window. Many failures are only visible on the system's own clock.
- A deploy that exits zero has proven an upload. Confirm the behavior in the target
  environment.

## Delegation

Fan-out is worth its coordination cost only when the pieces are genuinely independent.
Every condition in `triage.md#parallel-lanes` applies — disjoint mutable scope, stable
inputs, independent proof, defined integration — plus one that only matters once someone
else does the work:

- **A stated contract** — inputs, outputs, done criteria, and explicit non-goals. A
  worker who has to infer the boundary will pick a different one than you would, and you
  will find out at integration.

The owner keeps the campaign contract, the shared interfaces, integration, and the final
proof. A worker never widens its own scope and never changes a shared contract; a
completed piece is accepted only after integration review, because "it works in isolation"
is the weakest claim in distributed work.

When any of them fails, run sequentially. Sequential-and-correct finishes sooner than
parallel-and-tangled, and this is not close.

## Decisions That Outlive The Session

When a choice will constrain future work and its reasoning is not obvious from the code,
record it where the next person will look. Five lines is enough:

```text
Decision:     what was chosen
Context:      the situation that forced a choice
Alternatives: what else was considered, and why not
Consequences: what this makes easy, and what it makes hard
Revisit if:   the condition that would reopen this
```

`Revisit if` is the field that matters. Without it, a decision made under conditions that
no longer hold gets defended forever by people who do not know why it was made.

## Failure And Abandonment

Partial completion is the *normal* state of a campaign, not an exception. Design so any
abort point leaves the system consistent, and report progress as position rather than
percentage: which phases are proven done, which is in flight, what remains.

Abandon when a kill criterion fires, when the cost has passed twice the estimate and the
remaining uncertainty has not shrunk, or when the reason the campaign existed has gone
away. Then leave it clean: revert the incomplete phase or make it inert behind a flag,
delete dead scaffolding, and write down what was learned. An abandoned campaign that
taught something and left no wreckage is a legitimate outcome. Half-finished migrations
left in place are the most expensive artifact in this entire file.
