# Codebase Health

Every other route starts from something specific: a bug, a diff, a feature, an endpoint
that got slow. This one starts from the whole repository and a sentence like *clean this
up*, *scan the project*, *find everything wrong with it*, or *make this production-grade*.

The difference is not size, it is that nothing in the request bounds the work. There is no
named defect to close, no file to open first, no natural stopping point, and no line
between what may be changed and what must only be reported. Left unbounded, this route
fails the same way every time — a backlog too long to act on, a diff too large to review,
and a deletion of something that turned out to be load-bearing.

So the pass is run as **ordered axes over a bounded surface, producing a ranked backlog,
of which an approved subset is fixed**. Reliability first, because correctness outranks
everything below it. Security next, because an exposure is active harm. Then
maintainability, which is real work and is still the axis that must never be paid for with
the other two.

Load it when the target is the repository rather than a change: a health scan, a cleanup
mandate, an inherited codebase being made shippable, a quality gate before a release, or a
review that has turned into "and fix what you find". Do not load it for one defect
(`workflows.md#diagnose`), for a known list of defects (`defect-sets.md`), for a diff
under review (`workflows.md#review`), or for orientation with no fixing attached
(`workflows.md#audit`).

> **Owns** — the standing quality pass over a whole codebase: bounding the surface before scanning, the fixed order of the reliability, security, and maintainability axes and why it is fixed, the reliability families a reading pass can actually find, restoring files that were deleted by accident, the code-smell catalog with a detection signal per smell, proving code dead before deleting it, and the gate between what a scan finds and what it is allowed to change.
> **Defers** — one bug end to end → `workflows.md#diagnose`; a known set of defects and its fix order → `defect-sets.md`; attacker-facing depth → `security.md`; measured slowness → `performance.md`; the judgment calls inside a refactor → `craft.md`; whether any of it is worth paying for → `debt.md`; behaviour-preserving restructuring as a chain → `workflows.md#refactor`; code whose intent is lost → `comprehension.md`; how to write it up → `findings.md`; what proves a fix → `reality-testing.md`.

## Contents

- [Bound The Surface First](#bound-the-surface-first)
- [The Axes Are Ordered, And The Order Is Not Taste](#the-axes-are-ordered-and-the-order-is-not-taste)
- [Reliability: What A Reading Pass Can Find](#reliability-what-a-reading-pass-can-find)
- [Wasteful Is Not Automatically Slow](#wasteful-is-not-automatically-slow)
- [Files That Left Without A Decision](#files-that-left-without-a-decision)
- [Security: A Scan Buys Enumeration, Not Depth](#security-a-scan-buys-enumeration-not-depth)
- [The Smell Catalog](#the-smell-catalog)
- [A Smell Is A Question, Not A Verdict](#a-smell-is-a-question-not-a-verdict)
- [Dead Code, Unused Files, Leftover Dependencies](#dead-code-unused-files-leftover-dependencies)
- [What The Scan Hands Back](#what-the-scan-hands-back)
- [Health-Scan Anti-Patterns](#health-scan-anti-patterns)

## Bound The Surface First

Settle these before the first file is opened, one line each:

- **Surface** — which paths, which languages, and what is excluded. Generated code,
  vendored dependencies, lockfiles, fixtures, and build output are excluded by default and
  named as excluded. Scanning them produces findings nobody can act on and drowns the ones
  they can.
- **Depth** — report only, report and fix what is cheap and safe, or fix and restructure.
  These are different jobs with different diffs, and guessing which one was wanted is how
  a review turns into an unreviewable pull request.
- **Authority** — what may change without asking. Everything outside it is reported. The
  triage ladder already says this (`SKILL.md`, tier 6), and this route is where it is
  broken most often, because a mandate to "clean up" reads like blanket permission and is
  not one.

Then orient rather than read: manifests, entry points, CI configuration, test layout, and
the change-frequency ranking from `debt.md#the-interest-rate-is-the-whole-ranking`. That
ranking is the difference between a scan of the repository and a scan of the parts of it
anyone will ever touch again — and the second one is what was actually wanted.

A scan that returns two hundred unranked findings has not done the work. It has moved the
work to the user and made it larger on the way.

## The Axes Are Ordered, And The Order Is Not Taste

| Axis | The question it asks | What a finding must carry | Beaten by |
| --- | --- | --- | --- |
| **Reliability** | does it do the right thing, and keep doing it | the input or state that produces the wrong result, and where that state originates | nothing |
| **Security** | what happens when someone aims it at another user | the boundary crossed and a reachable path to it | an active reliability failure in production |
| **Maintainability** | what will the next change here cost | the change that is expensive today, not the shape that is unpleasant | both of the above |

The order is fixed for a mechanical reason. **A refactor applied to code that is wrong
produces clean wrong code** — and it produces it inside a diff large enough to hide the
wrongness from whoever reviews it. Restructuring is also the one axis that can *create*
reliability defects while it runs, so it goes last, when the behaviour it must preserve is
understood and pinned.

There is one exception, and it is not a licence to reorder: when the structure is *why*
the defect is invisible — the function is nine hundred lines and the bug could be any of
them — reshape first, behaviour unchanged, as its own commit with the same tests green
either side, then fix (`craft.md#make-the-change-easy-then-make-the-easy-change`). That is
still correctness-first work; it just needed a floor to stand on.

## Reliability: What A Reading Pass Can Find

A scan reads far more than it runs, so target the families a reading pass can actually
detect, and say plainly that anything decided at runtime was out of reach.

| Family | What it looks like | Cheap signal |
| --- | --- | --- |
| **Wrong condition** | off-by-one, inverted boolean, `and`/`or` swapped, a boundary word like *at least* implemented as *more than* | enumerate the cases rather than reading them — `reasoning.md` |
| **Swallowed failure** | a catch that logs and continues, a default returned on error, an unawaited promise, an ignored status code | search for the catch-all and read what follows it |
| **Partial failure** | two writes that must both land, with no transaction and no compensation; a retry around a non-idempotent call | follow every multi-step mutation to its end |
| **Resource lifetime** | file, socket, cursor, lock, subscription, or listener acquired on a path that can return early; a cache or list that only grows | pair every acquire with its release, including the exception path |
| **Repeated work** | a query inside a loop, a file re-read per item, a value recomputed per iteration that cannot change | look for calls sitting under loops and comprehensions |
| **Compatibility** | a language or runtime feature newer than the declared minimum; a dependency used past the version the manifest pins; assumptions about path separators, filesystem case, timezone, locale, encoding, or integer width | compare what the code uses against what the manifest and CI matrix promise |
| **State nobody controls** | current time, random seed, iteration order, environment variables, working directory | any of these read directly rather than injected |

Two rules keep this axis from degenerating.

**Every finding names an origin, not just a symptom.** A finding whose entire fix is a
guard at the point of failure is a symptom fix until argued otherwise, and this route is
where they multiply — a scanner points at the line that crashed, and the cheapest response
is to wrap it (`defenses.md#symptom-substitution`). Ask where the bad value came from
before writing the guard. If that cannot be answered in a sentence, the finding is *this
crashes*, not *here is the fix*, and it should say so.

**Never make a failing check pass by changing the check.** Adjusting a test, relaxing an
assertion, or widening a type to accommodate the wrong value is not a repair. It is the
defect, promoted to a permanent one.

## Wasteful Is Not Automatically Slow

Waste is a reliability finding when the resource runs out, and a performance finding when
it merely costs time. The distinction decides what evidence is required, and conflating
them is how a scan produces a pile of unfalsifiable "optimizations".

- **Reliability, no benchmark needed.** Something unbounded: a leak that exhausts memory
  or file handles given enough uptime, a per-request cache with no eviction, a query whose
  cost grows with a table nobody prunes, an N+1 that turns one page into a thousand round
  trips against a shared database. The failure is eventual and certain, so the argument is
  structural rather than measured.
- **Performance, measurement required.** Anything whose only claim is *this could be
  faster*. It goes through the measure-first gate in `performance.md#measure-first` and
  earns a change only with a before-and-after number that beats run-to-run variance.

When it is genuinely unclear, it is the second kind. A scan that reports guesses as wins
buys nothing and costs the review.

## Files That Left Without A Decision

Reading code is blind to what is absent, which makes this the one check nothing else in
the package performs — and it is cheap. Ask what the repository *expects* to exist and
does not, then ask history what happened to it.

1. **Find the holes.** Imports and includes that resolve to nothing, configuration keys
   pointing at absent paths, a script named by CI that is not there, a test fixture no
   longer on disk, a gap in a migration sequence, a manifest or plugin entry with no file
   behind it, a documented command that does not exist.
2. **Ask history.** `git log --diff-filter=D --name-only` over the recent range, then
   `git log --diff-filter=D -- <path>` for one file. For work that never reached a commit,
   `git reflog`, `git stash list`, and `git fsck --lost-found` are where it can still be.
3. **Judge whether it was intended**, before restoring anything.
4. **Restore from the commit before the deletion** —
   `git restore --source=<sha>^ -- <path>` — then diff it against what the rest of the
   code now expects rather than assuming it still fits.

| Tell | Reading |
| --- | --- |
| deleted along with its tests, its imports, and its documentation | deliberate removal; restoring it re-introduces dead code |
| gone while imports, configuration, or CI still name it | accidental; this is the case worth restoring |
| disappeared inside a merge or rebase commit touching hundreds of files | conflict resolution took the wrong side — the most common way real code is lost |
| present in history but never referenced by anything | it was dead before it was deleted; leave it deleted and say so |

**A file you rewrote from its name is not a recovered file.** If it is not in history and
not in a stash, say it is unrecoverable from this repository and name where else it might
live. Reconstructing something and presenting it as recovered is fabrication, and it is
worse than the missing file, because the next reader trusts it.

## Security: A Scan Buys Enumeration, Not Depth

At this altitude the value is coverage — every path found, none judged deeply. Depth is
`security.md`; obligations that come from the organization rather than the code are
`enterprise.md`.

Enumerate in this order, because each layer makes the next one smaller:

1. **Entry points** — routes, handlers, jobs, queue consumers, CLI commands, webhooks,
   public exports. Anything reachable from outside the process.
2. **Authorization per entry point**, checked on the *object* and not only on the route.
   The endpoint behind a button the interface does not render is the classic finding.
3. **Untrusted input reaching a sink** — query and command construction, template
   rendering, deserialization, path joining, redirect targets, file uploads.
4. **Data handling** — secrets in code, configuration, or git history; personal or
   payment data in logs and error reports; anything sent to a third party.
5. **Dependencies** — the ecosystem's own audit command, then the lockfile, then
   end-of-life status.

A dependency advisory becomes a real finding when the vulnerable path is reachable from
your code; when it is not, it is still a **deadline** rather than nothing, and it ranks by
date (`debt.md`). Upgrades go in their own commit with the changelog across the crossed
range actually read, never bundled into a cleanup.

Two closing rules. Never write that the codebase is secure — write what you checked and
what you did not (`findings.md#write-none-identified`). And never confirm a suspected
bypass against production data; that is itself an incident
(`security.md#when-you-find-something-real`).

## The Smell Catalog

A smell is a *detectable shape* that correlates with future cost. The value of the catalog
is the middle column — a signal you can actually run — because "this feels messy" is not a
finding and cannot be ranked.

| Smell | What it actually costs | Signal you can run | The move |
| --- | --- | --- | --- |
| **God class or module** | every change touches it; its tests are the slowest and most mocked | size, change frequency, and import fan-in, together | split along the axis of change, never by noun |
| **Long method** | you cannot say what it does without *and* | length, nesting depth, count of locals live at once | extract the parts that have names; a part you cannot name means the split is wrong |
| **Duplicated code** | a fix lands in one copy and not the other three | exact and near-duplicate search, then whether they change together in history | rule of three, and only when they change for the same reason — `craft.md#abstraction-timing` |
| **Tight coupling** | a change here breaks something over there; the test needs six mocks | import graph direction, mock count per test | depend on the narrower thing; invert the direction at the boundary |
| **Feature envy** | logic lives away from the data it reasons about | a method reading another object's fields more than its own | move the behaviour to the data |
| **Primitive obsession** | the same validation repeated, and eventually forgotten at one call site | the same parse or regex in more than two places | one type parsed at the boundary — `craft.md#make-illegal-states-unrepresentable` |
| **Magic number or string** | nobody can change the value safely, because nobody knows what it means | literals outside tests and constant definitions | name it where it is *decided*, not where it is used; `THREE = 3` is the smell wearing a hat |
| **Shotgun surgery** | one logical change edits nine files | commits that repeatedly touch the same set of files | move the decision into one place |
| **Long parameter list** | call sites are unreadable and a wrong order still compiles | arity, plus adjacent parameters of the same type | a parameter object, or one function per flag branch |
| **Speculative generality** | an abstraction with one implementation, taxing every reader | single implementor, parameters nobody passes, a layer that only forwards | delete it — `debt.md#debt-that-bought-nothing` |

## A Smell Is A Question, Not A Verdict

Nothing in that table is a defect on its own. Each earns a change only when it charges
interest — the area changes often and will keep existing — or when it sits in the path of
work that was actually requested (`debt.md#in-the-path-or-merely-nearby`). Code nobody
will touch again costs nothing however unpleasant it looks, and rewriting it spends real
review attention for zero return.

What turns a smell into work:

- It is in the path of the requested change, so that change cannot be made small without it.
- Its interest rate is high — the file is edited constantly, and the shape is why each
  edit is risky.
- It is directly upstream of a reliability or security finding you already have.

When it qualifies, the restructuring itself is `workflows.md#refactor`: characterization
tests first where coverage is missing, behaviour-preserving commits kept strictly separate
from behaviour changes, and one shape changed at a time. Where the code's *intent* is the
missing piece rather than its shape, that is `comprehension.md` — and history is the
primary source, not the file in front of you.

## Dead Code, Unused Files, Leftover Dependencies

Deleting is the highest-value part of a cleanup and the easiest to get catastrophically
wrong, because the evidence usually accepted for it is one modality wide. Dead code is
read, trusted, and maintained by people who do not know it is dead — and so is a file you
deleted that something reached by name.

Answer all of these before anything is removed:

1. **Is it reachable inside this repository** — including by every non-static route below?
2. **Can anything outside this repository reach it** — a published package, another
   service, a database row holding a class name, a customer's script?
3. **Do we know why it exists?** Not knowing is not evidence that there is no reason
   (`comprehension.md#removing-what-nobody-can-explain`).

The non-static callers a symbol search cannot see, which is the whole problem:

- reflection, `getattr`, `eval`, dynamic imports, and name-built dispatch
- dependency-injection containers, service registries, decorators that self-register
- configuration values, feature flags, and environment variables naming a class or handler
- framework conventions — routes, migrations, tasks, and hooks discovered by file name
- serialized names living in a database, a queue, or a cache written before this deploy
- packaging entry points and plugin manifests
- CI workflows, deployment scripts, Dockerfiles, and Makefiles
- documentation, README examples, and templates that call it by name
- the other side of a language boundary: a selector used by CSS or a test, a translation
  key, a column name, a stored procedure

So search **strings as well as symbols**, and search data as well as code: configuration,
migrations, fixtures, and the deployment repository if there is one. Then add a second
modality — coverage from the real suite or from staging traffic, or the ecosystem's
unused-export tooling — because grep finding nothing is one modality reporting nothing,
not proof (`defect-sets.md#enumerate-the-class-do-not-sample-it`).

When reachability genuinely cannot be settled, the honest move is a deprecation: leave it
in place, log or count a call for one release, and delete on evidence next time. That
converts a guess into a measurement at almost no cost.

Deletions ship as their own commits, one per class of thing, with a message stating what
proved it dead. A cleanup mixed into a behaviour change is a cleanup nobody can revert on
its own — and the safety of deleting rests entirely on being able to revert it.

**Dependencies** follow the same rule with two additions. A package is leftover when
nothing imports it *and* nothing invokes its CLI in a script, hook, or CI job. And a
package you use only transitively — reaching it through another dependency that happens to
pull it in — is not proof you can drop it; it is an undeclared dependency, and the fix is
to declare it rather than to remove it and wait for the upstream to change.

## What The Scan Hands Back

The deliverable is a **ranked backlog plus a small, defensible diff**, never a wall of
observations and never a repository-wide rewrite.

Each item carries file and line, axis, what breaks or what it costs, the evidence, the
proposed fix, and a rough cost. Ordering follows the triage ladder in `SKILL.md` — active
harm, then blockers, then what was asked for, then proof, then defects inside that blast
radius by `impact ÷ cost`. Shape and severity honesty are `findings.md`; lint and style
preferences are not findings (`findings.md#not-findings`).

Then split the list explicitly, because this is the gate the whole route turns on:

| Bucket | Contents | Rule |
| --- | --- | --- |
| **Fixed** | inside the authorized scope, and proven | one commit per cause, with the proof named per commit |
| **Proposed** | ready to do, needs a yes | the diff described, not applied |
| **Reported** | real but out of scope, or unproven | stays in `Next:`, never in the diff |

Close with what was *not* scanned — paths excluded, languages skipped, anything decided at
runtime, and any check the runtime could not execute. An unstated blind spot is read as
coverage (`defect-sets.md#the-frontier`). A count of fixes is not a result; the result is
which classes are closed and how that was proved.

## Health-Scan Anti-Patterns

- **The mega-diff.** Three hundred files reformatted, one real fix buried inside, and a
  reviewer who now approves the whole thing on trust.
- **Fixing the list instead of the generator.** Fifty findings are usually five causes
  (`defect-sets.md#find-the-generator-not-the-instances`).
- **Refactoring what is not covered**, then meeting the behaviour change in production.
- **Deleting on grep evidence**, or deleting a public export because this repository does
  not call it.
- **Reconstructing a missing file** and reporting it as recovered.
- **Guards sprinkled everywhere the scanner pointed**, none of which name where the bad
  value came from.
- **Dependency bumps as cleanup** — majors included, changelog unread, bundled with
  unrelated changes.
- **Cleanup that quietly becomes a rewrite.** That is a design decision wearing cleanup's
  clothes, and it needs to be asked rather than assumed.
- **Closing with "the codebase is now clean and secure."** Neither is a claim any scan can
  make, and stating it destroys the credibility of everything true in the same report.
