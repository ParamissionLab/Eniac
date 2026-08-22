# Lifecycle

The shape of the whole cycle, and the two activities that live before code exists:
turning a vague ask into criteria someone can check, and choosing a shape before
building it.

**Most work does not need this file.** A bug fix has no design phase; a one-line change
has no specification. The map below exists so that a phase which genuinely mattered is
never skipped *silently* — not to make every task walk through seven boxes. Applying a
lifecycle to work that does not have one is the most expensive kind of thoroughness,
because it looks like rigour while producing nothing.

Load it when the work is large enough that the order matters: a feature whose
requirements are not settled, a change where more than one shape would work, a project
crossing more than one session, or a handover where someone needs to see what was
covered and what was not.

> **Owns** — phase coverage from specify to evolve — turning a vague ask into checkable criteria, choosing a shape before building it, traceability from ask to proof, gates as evidence.
> **Defers** — the execution chains themselves → `workflows.md`; deciding between shapes when the choice is costly → `judgment.md`; proving each criterion → `reality-testing.md`.

## Contents

- [The Map](#the-map)
- [Specify](#specify) — from a vague ask to checkable criteria
- [Design Before Building](#design-before-building)
- [Traceability](#traceability) — the thread from ask to proof
- [Gates Are Evidence, Not Ceremony](#gates-are-evidence-not-ceremony)
- [After Ship](#after-ship)

## The Map

Each phase answers one question, is run by one route, and closes on one kind of evidence.
Nothing here is new machinery — it is the routes you already have, arranged so a gap is
visible.

| Phase | The question | Runs as | Closes when |
| --- | --- | --- | --- |
| **Specify** | what are we building, and how will we know it works | Specify — this file | criteria are observable and the out-of-scope list exists |
| **Design** | what shape should it take | Design — this file, with `judgment.md` | one option chosen, its reason and its falsifier written down |
| **Build** | does the thing exist | Implement — `workflows.md#implement`, `craft.md` | it works through its real entry point |
| **Verify** | does it do what was specified | `reality-testing.md` | every acceptance criterion has a proof that ran |
| **Release** | is it in front of users, safely | Ship — `workflows.md#ship`, `safety.md` | observed behaviour in the target environment, rollback known |
| **Operate** | does it keep working | `production.md` | a real signal exists, and someone can act on it |
| **Evolve** | what did this teach, and what is next | `learning-loop.md`, `campaigns.md` | the lesson is written where it will be read again |

Two phases have no owner anywhere else in this skill, which is why they are written out
below. The rest are cross-references on purpose: duplicating them here would create a
second version that drifts.

The `Full-cycle` route in `workflows.md` is the *execution* chain through Build to Ship.
This file is the coverage map around it, and it starts one step earlier.

## Specify

Most failed work was specified badly rather than built badly. The build was faithful —
to the wrong thing.

A specification needs three parts, and the third is the one that gets dropped:

```text
Outcome:     what will be true when this is done, in the user's terms
Boundary:    what is explicitly NOT included
Criteria:    how anyone can check it, without asking you
```

**A criterion nobody can check is a wish.** "The page should feel fast" is not a
criterion; "the orders list renders within 400ms at p95 on the staging dataset" is. The
test is simple: could someone who was not in the conversation tell whether it passed?

**Write the criteria before the design**, because a design with nothing to be checked
against gets judged on taste — yours, or whoever reviews it. Criteria first also
frequently kills the design: half of "we need a caching layer" turns out to be "one query
is missing an index" once someone writes down the number that has to move.

### Converting the vague ask

The common ones, and the question that turns each into something checkable:

| The ask | What it is missing |
| --- | --- |
| "make it faster" | which operation, on what data volume, from what number to what number, measured how |
| "make it secure" | against whom, protecting what, and what you are willing to break to get it |
| "improve the UX" | which flow, which step people fail at, and what success looks like |
| "make it scalable" | to what load, by when, and what breaks first today |
| "clean this up" | what becomes possible afterwards that is hard now |
| "add reporting" | who reads it, to decide what, how fresh the data must be |

None of these are pedantry. Each is the difference between one implementation and five.

### Separate the four kinds

They behave differently under pressure, so blurring them costs you later:

- **Requirement** — must be true, and has a criterion attached.
- **Constraint** — the box the solution must fit in: a deadline, a platform, an existing
  contract, a regulation. Not negotiable by design cleverness.
- **Assumption** — believed, unverified, written down so it can be challenged. An
  assumption that stays unlabelled becomes a requirement nobody agreed to.
- **Non-goal** — deliberately excluded. This is the cheapest section to write and the
  one that prevents the most rework, because scope returns through the gap where a
  non-goal was never stated.

**When two stated requirements conflict, name the conflict — do not average it.** A
compromise invented quietly to make both sound satisfied usually satisfies neither, and
the person who could have chosen never got to.

**If you cannot write a single checkable criterion, that is the finding** — but reach it
through the ambiguity ladder in `operating-manual.md`, not instead of it. Try the evidence
first, then a stated assumption. Most vague asks survive a labelled assumption perfectly
well, and stopping to ask about one that was cheap to get wrong costs the user a round
trip for nothing.

Stopping is the right move only when both halves are true: no reasonable reading is
available, **and** being wrong would be expensive or hard to undo. Then say so, name the
specific thing that would settle it, and stop — building against an unspecifiable ask
whose failure is costly produces work that cannot be judged and therefore cannot be
finished.

## Design Before Building

Design is worth its cost when the shape is hard to change later, when more than one
shape would genuinely work, or when getting it wrong means throwing away real work.
Otherwise the code *is* the design, and writing a document about it is procrastination
with formatting. `judgment.md` decides how much deliberation a call deserves; this is
what to produce when the answer is "some".

**One option is not a design — it is a decision already made, wearing analysis.**
Generate at least two shapes that could actually work, including the boring one. If the
second option is a strawman you invented to lose, you have not compared anything.

Compare on **what actually differs**, not on a generic matrix. Most axes are the same for
every option and reveal nothing. The ones that usually differ:

- what it costs to reverse
- what it forces the next change to look like
- where it fails under partial failure or real load
- who has to understand it, and what they already know
- what it makes impossible

**Design to the requirement, not past it.** The most common failure is not an inelegant
design — it is a design solving a problem that was never specified, chosen because it was
more interesting. Every element should trace to a criterion. Elements that trace to
nothing are the ones to cut first, and the ones hardest to cut later.

Record the outcome where the next person will find it — `architecture.md` names the
artifacts and `craft.md` carries the code-level judgment. Four lines is usually enough:

```text
Decision:   what was chosen
Because:    the specific reason, tied to a requirement or constraint
Rejected:   the other option and what would have made it right
Reverses:   what would tell us this was wrong, and what it costs to undo
```

`Reverses` is the field that makes the record useful a year later. A decision with no
stated falsifier cannot be revisited honestly — it just becomes tradition.

## Traceability

The thread that connects an ask to the evidence it works. It sounds bureaucratic and it
is actually the cheapest defect prevention available, because most escaped defects were
never traced to anything.

Each acceptance criterion should end up attached to something that ran:

```text
Criterion                              Proved by
expired tokens are rejected            test: rejects_expired_token
the list renders under 400ms p95       the before/after measurement, same workload
a failed payment leaves no order row   the forced-failure test
```

Three rules keep it honest:

- **A criterion with no proof is either untested or was never a criterion.** Decide
  which, and say so. Silently dropping it is how a feature ships missing a third of
  what was asked for.
- **When scope changes, change the criteria first.** Code written against an obsolete
  criterion is waste that looks like progress, and it is usually discovered at review.
- **Do not invent criteria to match what you built.** That inverts the whole thing: it
  produces a specification guaranteed to pass, and guarantees nothing.

At the close, the honest report is the criteria list with its proof column filled in,
including the rows that say `Unverified` and why. That is more useful than any summary,
and it takes less space.

## Gates Are Evidence, Not Ceremony

A phase gate is a question with an evidence-based answer, not a sign-off ritual. "Design
is done" is not a status; "both options are written, one is chosen, the reason names a
requirement" is checkable.

- **Move forward when the gate's evidence exists**, not when the phase feels finished.
  Those diverge exactly on the hard work.
- **Going backward is normal, not failure.** Building reveals that a requirement was
  wrong far more often than anyone plans for. Return to Specify, change the criterion,
  and say that it changed — the expensive version is carrying on against a criterion you
  privately stopped believing.
- **Skipping a phase is allowed; skipping it silently is not.** "No design pass — one
  obvious shape, reversible in an hour" is a complete and often correct answer. The
  failure mode this map prevents is the phase that was never considered at all.
- **Do not let a gate become the goal.** When the artifact matters more than what it
  represents, you have Goodhart's law inside your process — `judgment.md` names it.

## After Ship

Release is the middle of the lifecycle, not the end, and the phases after it are where
software spends almost all of its life.

- **Operate** — the change has to be visible when it misbehaves. `production.md` carries
  the resilience, observability, and runbook work; the gate is that a real signal exists
  and someone can act on it, not that logging was added.
- **Evolve** — what the work taught goes somewhere durable, per `learning-loop.md`. A
  lesson that lives only in the shipped diff gets re-learned at full price.
- **Feed it back.** Real usage is the best specification input available, and it arrives
  only after release: what people actually did, where they gave up, which error fired
  most. The next Specify starts from that rather than from a fresh guess.

Work that is never revisited after shipping is not finished work — it is abandoned work
that happened to reach production.
