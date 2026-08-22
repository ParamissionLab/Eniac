# Reasoning

Slow mode needs a **method**, not just more time. Deciding to think harder without a way
of thinking is how a hard problem becomes a long one.

Load this when the problem itself is hard to hold: many interacting cases, an invariant
you cannot state, a search space too wide to walk, or a defect whose mechanism you cannot
picture. Do not load it for a task you already know how to do — applying analysis to a
solved problem is the most respectable way to waste an afternoon.

> **Owns** — the method slow mode runs — framing, decomposition, case enumeration with proved coverage, checking against a written rule, finding an invariant, constraint propagation, working backwards, the why-chain from an observed failure, explaining to a listener without your context, reduction, cost reasoning, discharging proof obligations.
> **Defers** — deciding when the answer is a judgment call rather than a derivation → `judgment.md`; when to enter slow mode at all → `operating-manual.md#fast-and-slow`.

## Frame It First

Four lines, before any analysis:

```text
Given:       what is actually true, and where each fact came from
Required:    what must be true when this is done
Constraints: what may not change
Unknown:     the specific thing whose value would settle it
```

Most stuck problems are frame failures rather than reasoning failures. `Unknown` does the
most work here: a problem with no nameable unknown is not being solved, it is being
circled. If you cannot fill that line, that *is* the finding — go get one observation and
frame it again.

Facts in `Given` carry their source. A frame built on one unmarked assumption produces a
confident answer to a different problem.

## Decompose

A decomposition is good when three things hold: each part is **independently checkable**,
the parts **cover the whole**, and they **do not overlap**. Fail any of them and you have
made two problems instead of one.

Cut along a seam the system already has:

| Cut | Question it answers | Best for |
| --- | --- | --- |
| **By data flow** | where does the value enter, change, and land | wrong output, corruption |
| **By state** | which states can this be in, and what is legal in each | lifecycle, UI, protocols |
| **By case** | how does behaviour partition over the input | branching logic, validation |
| **By layer** | which layer owns which responsibility | "where does this belong" |
| **By time** | before / during / after; startup, steady, shutdown, resume | races, migrations, jobs |

Pick the cut that makes one part *obviously* fine. What remains is the problem, and it is
now smaller. Repeat. A cut that leaves both halves equally suspicious was the wrong cut —
try a different axis rather than a smaller piece of the same one.

## Enumerate The Cases, Then Prove Coverage

"It handles the normal case and probably the rest" is where most defects enter. Partition
the space; do not sample it.

List the classes on each dimension that applies, then check every combination that can
actually occur:

- **quantity** — zero, one, many, the maximum, past the maximum
- **validity** — valid, malformed, absent, null, empty, wrong type, wrong encoding
- **order** — expected, reversed, repeated, concurrent, interleaved, out of order
- **time** — first run, repeat run, resumed after failure, expiry, clock skew, timezone
- **authority** — permitted, forbidden, expired, a different tenant

Then state which combinations are **impossible, and why**. An "impossible" with no reason
attached is the single most common origin of a production surprise — it usually means
"I did not think about it", which is a different claim entirely.

## Check It Against The Written Rule

When a spec, policy, or contract exists and the question is whether the code implements
it, the reliable method is mapping, not reading. Reading finds the defects that look like
defects, which is a different set from the defects that are there.

Build the row-per-clause table. Every clause of the rule gets one row, the code that
implements it, and the verdict:

```text
Clause                              Implemented at        Verdict
account at least 180 days           line 13  age < 180    correct — 180 passes
spent at least 500                  line 20  spend > 500  WRONG — excludes exactly 500
staff exempt from 1 and 3           line 10-11            correct
```

The value is in the rows you cannot fill. A clause with no line number is unimplemented,
and a line with no clause is behaviour nobody asked for — both are invisible to a read
that goes file-first instead of rule-first.

**Boundary words carry the operator, and they are the highest-yield place to look.**
"At least" and "no fewer than" are `>=`. "More than" and "over" are `>`. "Up to" and "at
most" are `<=`. "Between" is undefined until someone says whether the ends are included.
When a spec states its own examples — *exactly 500 qualifies* — that sentence outranks
any reading of the prose around it, and a mismatch there is a defect with no argument
available.

**A compound condition needs its rows enumerated, not parsed.** `A and not (B or C)`
read fluently is a guess; the four or eight rows are an answer. This is exactly the shape
fast thinking handles worst — negation, mixed `and`/`or`, and De Morgan's transformation
all read as obvious and are wrong at a rate that has nothing to do with how obvious they
felt.

**Before filing a defect, construct the input that demonstrates it.** A suspicious
operator you cannot make fail is not a defect — it is a pattern match, and filing it costs
the reader more than saying nothing. This is the discipline that separates checking from
scanning: two comparisons can look identical and sit on opposite sides of a boundary, so
one is broken and the other is correct, and only the constructed case tells you which.

Run the demonstrating inputs rather than arguing them, whenever the code can be executed
at all. A table of cases you claim would fail is an argument; the same table with observed
output is evidence, and `reality-testing.md` explains why nothing weaker closes the loop.

## Find The Invariant

"Lock the invariant" is only useful advice if you can find one. Two questions produce most
of them:

1. **What is true of every valid state that the broken state violates?** A balance is
   never negative. An id appears once. The parts sum to the whole. Every open has a close.
   Every row has a tenant.
2. **What does each operation promise to preserve?** If you cannot say, the operation has
   no contract — and that is itself the finding, usually the important one.

An invariant is worth having only if it is **checkable**: an assertion, a database
constraint, a type, a test, or a query you can run. An invariant that exists only in prose
drifts within two releases and then misleads whoever trusts it.

## Propagate Constraints

Experts narrow quickly because each fact eliminates a region, not because they guess
better. From the symptom, derive what must be true:

> *Fails only for tenant B* → the failing path reads tenant-scoped state → the difference
> lives in that state or in how it is scoped → therefore not in the request handler, not
> in the serializer, not in anything shared across tenants.

Three derived constraints routinely reduce a codebase to a file. Write them down as you
go, and keep them separated from assumptions: **a derivation from a wrong premise narrows
just as confidently, in the wrong direction**, and it feels identical from the inside.

When a constraint turns out false, do not patch it — re-derive from the point it entered.
Everything downstream of a broken constraint is unsupported, including the parts that
still look right.

## Work Backwards

When forward search is too wide, start at the goal:

1. What is the last thing that must be true for this to be correct?
2. What produces that?
3. Repeat until you reach something you already have.

This finds the *missing* piece instead of exploring everything that exists. It is the
strongest move for "why is this value wrong" and for "what would have to change for this
to be possible at all" — and it is usually far shorter than the forward walk.

## Ask Why Until It Is Actionable

The Toyota technique, and the direct correction to the habit in
`defenses.md#symptom-substitution`. Start at the observed failure and ask *why* of each
answer, until you reach something you can change whose change would have prevented every
link above it.

```text
The request 500s
  why -> the handler threw on a null user
  why -> the session lookup returned null for a token it considered expired
  why -> the expiry check compares against local time, the token stamps UTC
  why -> parse_ts() defaults to local when no timezone is passed
  why -> the helper was written for log parsing, where local was correct, and
         nothing marks it unsafe anywhere else
```

Fixing link one is a guard. Fixing link three fixes this bug. Fixing link five closes the
class, and the chain is what made the difference visible.

Four rules separate the technique from theatre. Without them it produces a confident wrong
story, which is worse than no story because it feels finished:

- **Every "because" is an observation, not a belief.** This is the whole difference. A
  chain of five plausible assertions is fiction with an arrow drawn through it. When a link
  cannot be shown, mark it and go get it — one verified link beats four assumed ones,
  because the assumed chain will send you to fix something that was never wrong.
- **Five is a shape, not a count.** Stop at the first thing you can actually change that
  would have prevented the links above it. Sometimes that is two. Pushing past it reaches
  "the team was under-resourced" — true, unactionable, and a comfortable place to stop
  doing engineering.
- **When a why has two answers, it branches.** Real failures usually have several
  contributing causes, and a single chain gives false confidence that you found *the* root.
  Follow both branches, or say plainly which you dropped and why.
- **"Because someone forgot" is not a cause.** It is where the asking stopped. Ask why the
  system permitted it, why nothing caught it, and why it was possible to get wrong — human
  error is the point where the chain reaches the design, and it is routinely mistaken for
  the end of it.

This is not `Work Backwards` above. That one starts from the goal and asks what must be
true; this one starts from an observed failure and asks what produced it. Use the why-chain
when something *did* happen, and work backwards when something *should* and does not.

## Explain It To Someone Without Your Context

Rubber ducking. The value is not the duck — it is that explanation is **sequential and
cannot skip**. Reading lets you glide over a step with *"and then it validates the input"*;
saying it in order, to someone who cannot fill in your gaps, does not.

The naive version fails for an agent, and it is worth being precise about why: fluent
narration is free here. Generating a plausible walkthrough costs nothing and proves
nothing, so the constraint that does the work for a human — a listener who will notice
incoherence — has to be rebuilt deliberately. Three rules rebuild it:

- **No shorthand, and no pronoun without an antecedent.** Name the thing every time. "It
  fails" conceals which of four things fails, and that concealment is usually the bug.
- **Mark every step observed or assumed.** The `Fact` / `Assumption` discipline turned
  inward. The gap appears at the first step you cannot label.
- **Hunt your own hedges.** *Should*, *presumably*, *somehow*, *for some reason*, *must
  be*, *I think it* — each marks a link you did not check, and surfacing them is the entire
  yield of the technique. When one appears, stop explaining and go check that one thing.

**A person is a better duck than a duck.** The compact read at L2+ and the arbitration line
are both this technique with a real audience, and an explanation written for someone who
will notice a gap is held to a higher standard than one written for yourself. When a
reader is available, use them.

**Time-box it.** Explaining the problem instead of touching it is intellectualization
(`defenses.md`), and this technique is the most respectable disguise that defense has. A
duck session that does not end in one specific thing to check has failed — say so, and go
run something.

## Reduce To A Solved Problem

Recognising the shape saves the derivation: *this is cache invalidation; this is
scheduling; this is expand/contract; this is a producer outpacing a consumer.*

A reduction is valid only when the mapping is exact. A near-fit imports the standard
solution's assumptions along with the solution, and those assumptions fail silently
because nobody stated them. **Say what the mapping ignores** before relying on it — if
you cannot name the difference, you have not checked that there is none.

## Reason About Cost Before Measuring

Where does time, memory, or money actually go?

- Find the **dominant term**. Everything else is noise until that term changes.
- Count the operation that scales with the input, not the lines of code.
- Ask what happens at ten times the input, and at one. Both ends break things, and the
  small end is the one nobody tries.

This is prediction, not measurement — measurement is `performance.md`. Its job is to tell
you *where to measure*, so that measurement costs one run instead of five.

## Discharge The Proof Obligations

Every non-trivial change carries obligations. Name them, then discharge each explicitly:

```text
Obligation                        Discharged by
the new path produces X           the test that asserts X
existing callers still work       the surrounding suite, or a contract test
the invariant still holds         an assertion, constraint, or query
the failure path is safe          a test that forces the failure
nothing else reads this shape     the caller search, including dynamic references
```

An obligation you cannot discharge is a **stated risk**, not an oversight. Writing it down
converts an unknown defect into a known one, and that conversion is most of the value —
it is also the difference between an engineer and someone who was lucky.

## When The Reasoning Is Done

Not when it feels resolved. When:

- every case in the partition is handled or excluded with a stated reason,
- the invariant is named and checkable,
- every assumption is labelled and would become visible if it were wrong,
- the remaining unknowns are named rather than absent.

Feeling finished and being finished diverge exactly when the problem is hard — which is
the only condition under which this file gets loaded.
