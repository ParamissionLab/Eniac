# Technical Debt

Debt is not ugly code. It is a **gap between the shape the code has and the shape the work
now needs**, and the thing that makes it debt rather than an opinion is that it *charges
interest*: every future change in that area costs more than it should. Code nobody will
ever touch again charges nothing, however unpleasant it looks — and that single test
settles most arguments about what deserves attention, because it replaces taste with a
question that has an answer.

Two failures live here and they pull in opposite directions. One is treating cleanup as a
virtue and widening every task into a renovation nobody asked for. The other is never
paying anything, so each change costs slightly more than the last until a feature that
should take a day takes a week and nobody can point at when that happened. The discipline
is not a preference between them; it is knowing which debt is in the path of the work and
which is merely nearby.

Load it when a change is harder to make than it should be, when you are deciding whether to
clean something up as part of a task, when a shortcut is about to be taken deliberately, or
when the work is an explicit cleanup, modernization, or "pay down our debt" request. Do not
load it to justify a refactor you already wanted to do — that is the failure this file is
most often reached for.

> **Owns** — debt as an economic object: what makes something debt rather than dislike, the interest-rate ranking and how to read it from the repository, whether paying is in scope for *this* task, naming debt at the moment it is created, the four kinds and their different treatments, the category of debt that bought nothing and is therefore avoidable, when paying is the wrong call, and the record that outlives whoever wrote it.
> **Defers** — the reshape-then-change technique → `craft.md#make-the-change-easy-then-make-the-easy-change`; ranking work items in general → `triage.md`; retiring debt across many releases → `campaigns.md`; code with no owner and no tests → `enterprise.md#legacy-and-unowned-code`; several defects sharing one cause → `defect-sets.md`; writing any of it up for a reader → `findings.md`.

## Contents

- [The Interest Rate Is The Whole Ranking](#the-interest-rate-is-the-whole-ranking)
- [In The Path Or Merely Nearby](#in-the-path-or-merely-nearby)
- [Four Kinds, Four Treatments](#four-kinds-four-treatments)
- [Name It When You Create It](#name-it-when-you-create-it)
- [Debt That Bought Nothing](#debt-that-bought-nothing)
- [When Not To Pay](#when-not-to-pay)
- [The Record](#the-record)

## The Interest Rate Is The Whole Ranking

Debt costs `interest rate × remaining lifetime`. Both terms are observable, and neither is
how bad the code looks:

- **Interest rate** — how often this area is changed, and how much each change costs
  because of the debt. A tangle in a file touched weekly is expensive. The identical
  tangle in a file untouched for three years is free.
- **Remaining lifetime** — how long this code will keep existing. Debt in something being
  replaced next quarter is already paid off by the replacement.

The first term is sitting in version control, which makes this one of the few prioritization
questions with a mechanical answer:

```bash
git log --since='12 months ago' --format= --name-only | sort | uniq -c | sort -rn | head -30
```

Cross that list against where the work is painful and the top few rows are the debt worth
paying. Everything else is a matter of taste, and taste is not a reason to spend somebody's
review attention.

**The counter-intuitive consequence is worth stating plainly: the worst code in the
repository is usually not the most expensive debt.** The most expensive is mediocre code in
the file everyone edits. A reviewer who goes looking for the ugliest thing will
systematically pick the wrong target, and feel productive doing it.

Where the rate is not obvious, one question substitutes: *what did this cost me on this
task?* Time spent understanding something before you could change it is the interest
payment, and having just paid it, you are the person best placed to say what it was.

## In The Path Or Merely Nearby

`SKILL.md#triage--automatic-prioritization` puts adjacent cleanups in tier 6 — reported,
never silently done. That rule is right, and applied without this distinction it produces
the opposite failure, because some debt is not adjacent at all: it is directly under the
task.

The line is not proximity. It is **whether the task requires you to work through it**:

| | Test | What to do |
| --- | --- | --- |
| **In the path** | you must reshape or fully understand it to make the change correctly | pay it — as a **separate commit, before** the change, behaviour unchanged and the same tests green either side (`craft.md#make-the-change-easy-then-make-the-easy-change`) |
| **In the blast radius** | the change could break it, or it hides whether the change worked | do the minimum that makes the change provable, and report the rest |
| **Merely nearby** | you can see it and the task does not depend on it | tier 6 — report it under `Next:` with its interest rate, do not touch it |

"I am already in this file" is the *nearby* test, not the path test, and it is the reason
diffs get four times bigger than the request. Being in the file is genuinely when cleanup
is cheapest — which is exactly why the temptation is strong and why the discipline has to
be explicit rather than felt.

**Separate commits are not a formality here.** A reshape mixed with a behaviour change
cannot be reviewed — the reviewer cannot tell which lines are supposed to change what — and
cannot be reverted in part when the behaviour turns out wrong. Two commits cost one extra
command and preserve both.

One item at a time. The Boy Scout rule scales badly: improving everything you touch on a
large task produces a diff nobody can review, and an unreviewed cleanup is a behaviour
change nobody checked.

## Four Kinds, Four Treatments

They are not interchangeable, and the fourth behaves differently enough that treating it
like the others is how teams get surprised:

| Kind | What it is | Treatment |
| --- | --- | --- |
| **Deliberate and recorded** | a shortcut taken knowingly, written down with what it costs and what retires it | a loan, and a legitimate one. Revisit when its trigger fires |
| **Deliberate and unrecorded** | the same shortcut, undocumented | the dangerous kind — indistinguishable from design, so the next person builds on it. Record it retroactively the moment you find it, even if you cannot pay it |
| **Accidental** | it was reasonable when written; the requirements moved | normal and unavoidable. Retire opportunistically when in the path |
| **Environmental decay** | a dependency going end-of-life, a deprecated API, an expiring certificate, an unsupported runtime or language version | **not interest — a deadline.** Costs nothing, then costs everything |

That last row deserves its own sentence. Environmental decay does not get more expensive
gradually; it is free until the date, and after the date it can block every release at
once — a security patch you cannot take because the upgrade path is four majors long, a
platform that stops accepting your build. It is therefore ranked by **date, not by interest
rate**, it belongs on a calendar rather than in a backlog, and it is the one kind where
"nothing is going wrong" is not evidence of anything.

## Name It When You Create It

Every change creates some. The difference between debt and a landmine is entirely whether
anybody said so at the time — and the moment you are best able to say it is the moment you
decide to take the shortcut, when the alternative you rejected is still in your head.

When shipping something knowingly short of right, one line, where the next reader will hit
it:

```text
Shortcut:  what was done instead of the right thing
Because:   the constraint that made it the right call now
Costs:     what this makes harder, and for whom
Retires:   the specific condition that should trigger revisiting it
```

The fourth field is the one that matters and the one usually missing. `TODO: clean this up`
is not a record — it has no trigger, so it is never true that now is the time, and it will
still be there in four years being scrolled past. *"Retire when we add the second payment
provider"* is a record, because one day that becomes true and somebody notices.

Say it in the report as well as in the code. A shortcut the user does not know about is a
decision you made on their behalf and did not tell them about, which is a different thing
from a trade-off they accepted.

## Debt That Bought Nothing

Not creating debt at all is not available — every change makes some, and a method promising
otherwise would be the kind of claim this skill exists to prevent. What *is* available is
eliminating an entire category, and it is a large one.

Real debt buys something: a deadline met, a market tested, a decision deferred until the
information existed. The trade was made knowingly and the interest is the price. Then there
is debt that bought nothing at all — no speed gained, no deadline met, just structure added
before anyone knew what shape was needed:

- **An abstraction over one implementation.** The interface, the factory, the strategy
  pattern with a single strategy. It costs indirection on every read forever and defers
  nothing, because the second case has not arrived to shape it.
- **Speculative generality.** Parameters nobody passes, hooks nobody registers, a plugin
  system for two things. Each one is a guess about the future that also has to be
  maintained, and guesses about the future are wrong at roughly the rate you would expect.
- **Configuration nobody asked for.** Every option is a supported combination, forever, and
  the number of them multiplies rather than adds.
- **A layer that only forwards.** If it adds no decision, it adds a hop to every trace and
  a file to every change.
- **Premature error handling.** A `try/except` around something that has never failed, in a
  shape nobody chose deliberately — `defenses.md` reaction formation, and it converts a
  loud failure into a silent one.
- **A dependency for something small.** A supply-chain surface, a version to track, and an
  upgrade obligation, bought to avoid twenty lines — `craft.md`.

The common cause is one thing: **a decision made before the information needed to make it
existed.** Which means the discipline is not deciding *better*, it is deciding *later* —
duplicate twice and abstract on the third, add the parameter when the second caller needs
it, write the concrete thing and let the shape emerge from two real cases rather than one
imagined pair.

That is the whole avoidable category, and the rest is honest debt. When you take the honest
kind, the section above applies: name it, price it, and give it a trigger. A shortcut with
those three is a loan. Without them it is the same shortcut, indistinguishable from design,
and someone will build on it.

## When Not To Pay

Refusing is often the right engineering call, and it needs to be as available as agreeing:

- **The code is scheduled for deletion or replacement.** Paying debt on something being
  removed is pure loss. Confirm the schedule is real rather than aspirational.
- **The area is genuinely stable.** No changes in a year, no changes planned. The interest
  rate is zero regardless of how it reads.
- **You do not have the knowledge to do it safely.** Restructuring code whose behaviour you
  cannot characterize is not paying debt, it is taking a larger loan against a system you
  do not understand. Get a characterization test first, or leave it and say why.
- **There are no tests and you cannot cheaply add one.** Behaviour-preserving changes need
  something to prove behaviour was preserved. Without that, "refactor" is a claim you
  cannot make (`reality-testing.md`).
- **The proposal is a rewrite.** Rewrites are the most expensive form of debt payment, the
  least likely to finish, and they usually re-acquire the same debt for new reasons. Do not
  propose one unless asked — `enterprise.md#legacy-and-unowned-code`.
- **You want to, and no one asked.** The most common reason, and the least defensible. It
  is `displacement` in `defenses.md` when there is real work waiting: cleaning a
  comfortable file while the hard problem sits untouched.

Saying no is not the end of the interaction. It is `Next:` plus an interest rate, so the
decision is the user's rather than silently yours.

## The Record

Debt found and not written down was not found. The record lives where the next person will
be standing, in rough order of preference:

1. **In the code, at the trap**, with the trigger that retires it. Nothing else has a
   comparable chance of being read at the right moment.
2. **In the repository's own tracker or debt register**, when it is bigger than one site
   and there is a real chance of scheduling it.
3. **In the report, under `Next:`**, with the interest rate attached — what it will cost,
   and how often, not just what is wrong.

Whichever it is, a debt item is only useful with three things: **where it is**, **what it
costs** — some evidence of the rate, not an adjective — and **what would retire it**. Two
out of three produces a complaint, and complaints get filed and never actioned, which is
worse than silence because it looks like the work was done.

At `M2` and above the register itself becomes an artifact rather than a habit, with an
owner and a review cadence; `campaigns.md` covers retiring debt across many releases, and
`architecture.md` covers producing a register as the deliverable of an audit.
