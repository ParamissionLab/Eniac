# Defect Sets

`workflows.md#diagnose` is the chain for **one** bug: reproduce, localize, discriminate,
fix at the cause, lock it. Its last step — *does the same cause exist elsewhere* — opens a
different problem that nothing else here owns, and that problem is where bug-fixing work
usually goes wrong.

The mistake is treating a list of defects as a list of independent items. It almost never
is. A list of defects is a **projection of a smaller number of causes onto whatever surface
you happened to look at**, and the two failures everyone recognizes both follow from that
one misreading: the scan misses things, so the fix is incomplete; and the fixes interact,
so new defects appear where old ones were closed. Neither is a failure of effort. Both are
failures of *structure* — a list has no structure, and the work needs one.

Load it when you are looking at more than one defect at once: a bug bash, a review or audit
backlog, a static-analysis or scanner dump, a QA report, a list of failing tests, or a
single fix that turned out to have neighbours. Load it also before promising that a class
of bug is *gone* rather than that one instance is fixed. Do not load it for one bug with
one cause — that is the Diagnose chain, and running set logic over a set of one is ceremony.

> **Owns** — more than one defect at once: why a scan is structurally incomplete rather than insufficiently thorough, finding the generator behind the instances, enumerating a defect class instead of sampling it, the interaction graph that decides fix order, where new defects come from during a fix sweep, closing a class rather than a ticket, and the frontier that keeps residue from being silent.
> **Defers** — the chain for a single bug → `workflows.md#diagnose`; enumeration and case-coverage technique → `reasoning.md`; writing findings up for a reader → `findings.md`; proving any one fix → `reality-testing.md`; applying one known rule across many files → `workflows.md#batch`; the avoidance patterns that fire on attempt seven → `defenses.md`; deciding when the sweep has stopped learning → `loops.md#the-three-stops`; a scan of the whole repository that has to generate its own defect list first → `code-health.md`.

## Contents

- [Why A Scan Is Structurally Incomplete](#why-a-scan-is-structurally-incomplete)
- [Find The Generator, Not The Instances](#find-the-generator-not-the-instances)
- [Enumerate The Class, Do Not Sample It](#enumerate-the-class-do-not-sample-it)
- [Map Before Fixing](#map-before-fixing)
- [Where The New Bugs Come From](#where-the-new-bugs-come-from)
- [Close The Class, Not The Ticket](#close-the-class-not-the-ticket)
- [The Frontier](#the-frontier)
- [Sweep Anti-Patterns](#sweep-anti-patterns)

## Why A Scan Is Structurally Incomplete

A scan finds what it looked *with*. Its coverage is set by the modality, not by the effort
spent inside it — so reading the same code a second time, more carefully, adds almost
nothing, while spending a tenth of that time running it finds a whole class that reading
cannot reach. Careful reading finds what is visibly wrong. It is structurally blind to what
is *absent*, to anything that depends on runtime state, and to anything that is wrong in a
way that looks right.

This is why the completeness question is never *did I look hard enough*. It is **what did I
not look with**:

| Modality | Finds | Structurally blind to |
| --- | --- | --- |
| Read the code | wrong logic, missing cases in what is present, contradictions with the comments | what is absent entirely; anything decided by runtime state |
| Run it — real inputs, edge inputs, volume, concurrency | wrong behaviour, crashes, races, resource growth | every path the run did not exercise |
| Follow one piece of data end to end | encoding, truncation, lost updates, silent coercion, corruption at a boundary | pure-logic bugs that never touch stored data |
| Follow the trust boundary | authorization holes, injection, unvalidated input reaching a sink — `security.md` | ordinary correctness, which it will happily skip past |
| Diff against history — `git log -S`, blame, the last migration | regressions, half-finished changes, a rule applied to nine of ten sites | defects that have always been there |
| Check against the contract, spec, or schema | wrong-by-agreement: the code is self-consistent and disagrees with what was promised | anything the contract does not mention |
| Read what is being suppressed | swallowed exceptions, ignored return values, disabled or skipped tests, lint and type suppressions, `TODO` and `FIXME` | anything nobody thought worth silencing |
| Ask what the tooling is told to ignore | deliberate holes, excluded paths, pinned-back versions, weakened config | code the tooling covers and still gets wrong |

Two or three of these, chosen for the system in front of you, beat one done exhaustively —
and the choice is not arbitrary. Pick the modality that reaches where this system's defects
actually live (`system-types.md#blind-what-you-cannot-see-from-here`): a data pipeline
hides them in the data, a concurrent service hides them in the run, a library hides them in
the contract.

**Say which modalities you used and which you did not.** An unstated blind spot is read as
coverage by everyone downstream, including you next week.

## Find The Generator, Not The Instances

The moment there are **two** defects, stop collecting and ask one question: *what single
thing would produce both of these?*

This is the highest-value move in this file, and its value comes from what it converts. A
list of instances has unknown length, and no amount of looking tells you whether you are
near the end. A generator has a **class**, and a class can be enumerated — which turns "I
found some" into "there are fourteen, here they are". That conversion is the entire
difference between a fix that holds and a fix that leaves residue.

| Generator | The tell |
| --- | --- |
| A misunderstood API or library contract | the same wrong call shape in places that never copied from each other |
| A copy-pasted block | identical structure with drifted details — and the drift is where the interesting bugs are |
| A missing check at a boundary | every caller validates, each slightly differently, and one does not |
| An implicit contract nobody wrote down | it works for every existing caller and breaks on the next one |
| A leaky abstraction | callers reach past it, so each of them re-implements the same mistake |
| A wrong default | correct only in the places where somebody happened to override it |
| A primitive that is unsafe unless used carefully | every single use is a potential instance, so the count equals the call count |
| One wrong belief about the environment | timezone, encoding, ordering, case sensitivity, clock, locale — wrong everywhere at once and visible in almost none of them |

The chain that gets you there is the why-chain in
`reasoning.md#ask-why-until-it-is-actionable`, run one link past the point where this
particular bug is explained: the link that explains *this* instance is the fix, and the
link after it is usually the generator.

Two instances are enough to hypothesize a generator and not enough to confirm one. Confirm
it the way any hypothesis is confirmed: name what would rule it out, then look for that.
Sometimes there genuinely are two unrelated bugs, and forcing a shared cause onto them is
its own defect — but the cost is asymmetric, because a generator missed is a fix that ships
incomplete, and a generator wrongly proposed dies at the first counterexample.

**Generators nest.** Three copy-pasted blocks may share a cause with a fourth defect
somewhere else — the missing helper that would have made copying unnecessary. When the
first generator is found, ask the question once more of the generator itself.

## Enumerate The Class, Do Not Sample It

With a generator in hand the set becomes derivable rather than discoverable, and that is a
change in kind. Define the class precisely enough to search for, then get the complete list
**mechanically**.

**A text search is a hypothesis, not an enumeration.** It finds one spelling of the thing,
which means it silently omits the alias, the re-export, the dynamic call, the wrapper, and
the one written differently. Enumerate by whatever *cannot* be spelled another way and let
the tooling do it: the symbol's caller list, the type's implementors, the import graph, the
route table, the schema, the subclass list, the places a field is written. Where the
language or tooling cannot give you that, say so and treat the search as a sample —
labelled as one.

Then **state the size**, because the number is the finding:

```text
Class:    callers of parse_ts() that do not pass an explicit timezone
Found by: caller list from the language server, cross-checked against the import graph
Size:     17 call sites - 14 already correct, 3 wrong
Frontier: dynamic dispatch through the plugin registry is not in this list
```

"Found several places" is not a result. It is an admission that the class was never
enumerated, written in a tone that sounds like it was.

## Map Before Fixing

Before touching anything, relate the findings to each other. This costs a few minutes and
it is what turns a list into the single connected thing the work actually is. Four
relationships matter:

- **Shared cause.** Fix once at the cause; the rest should disappear. *Verify that they
  did* — a sibling that survives the cause fix was never a sibling, and finding that out
  now is much cheaper than finding it out after the sweep is reported as done.
- **Shared file or function.** One edit, one review, one proof. Splitting these into
  separate changes multiplies the review cost and gains nothing.
- **Shared state, invariant, or data structure.** This is where the new bugs come from.
  Two fixes that each look local are both editing the same assumption, in directions that
  do not compose.
- **Ordering.** B is only reachable once A is fixed, or A's fix changes what B even means.
  This edge is invisible in a flat list and decides the whole sequence.

**Fixing in discovery order is the most reliable way to create new defects**, because
discovery order is arbitrary with respect to every relationship above. Order by the graph
instead: causes before symptoms, shared state before anything that reads it, and the fix
that shrinks the remaining list before the fix that only closes one line of it.

At `M1` or above, or any set large enough that you will lose the thread, write the map
down — the plan file in `triage.md` is where it goes, and re-deriving it next session at
full price is the alternative.

## Where The New Bugs Come From

They are predictable, which means they are preventable. Six sources, in rough order of how
often they are the culprit:

- **Independent fixes to a shared thing.** Two edits each adjust the same validation,
  default, or piece of state to satisfy their own symptom, in incompatible directions. The
  result passes both original reproductions and breaks a third case neither looked at.
- **The symptom moved rather than went away.** A guard added where the bad value should
  never have arrived pushes the failure one layer outward, where it is harder to trace and
  no longer looks related to anything. `workflows.md#diagnose` step 6 is the rule: fix at
  the cause, or say explicitly that this is a symptom fix and name the real cause.
- **The fix widened a contract.** Accepting more input, returning a new shape, relaxing a
  constraint — each is a compatibility change wearing a bug fix's clothes
  (`stack-signals.md#what-breaks-a-contract-in-any-language`).
- **Stale findings.** A fix that changed shared state may have invalidated, altered, or
  created entries in the list you have not reached yet. The remaining findings were derived
  against a system that no longer exists.
- **An unproven batch.** Every fix in a sweep feels too small to verify individually, and
  the aggregate is a large unverified change. This is the most common way a bug-fix sweep
  ships a regression, and it feels like diligence the entire time.
- **Fix number seven at the end of a long session.** By then the approach is being repeated
  rather than chosen, which is `defenses.md` territory — the correction is one fresh
  observation and one investment level lower, not one more edit.

The operative discipline against the fourth: **after any fix that touches shared state,
re-derive the remaining list rather than re-scanning.** Re-deriving is cheap and specific —
walk the remaining findings and ask which the fix invalidated, changed, or created.
Re-scanning is expensive, and it starts from the same blind modality that produced the
incomplete list in the first place.

## Close The Class, Not The Ticket

A lock that fails only for the instance you found lets the class return through the next
call site, and it returns looking like a new bug. The closes, strongest first:

1. **Make the wrong state unrepresentable.** A type, a constructor that cannot produce an
   invalid value, a private field with no public setter. Nothing to remember and nothing to
   enforce.
2. **One validated entry point, and delete the others.** The class stops existing because
   the surface it lived on is gone.
3. **A mechanical check in CI** — a lint rule, a banned-pattern grep, a schema assertion.
   It catches the *next* instance, including the one a stranger writes next year.
4. **A property or table test over the enumerated set.** Locks every member at once, and
   fails loudly when the set grows.
5. **A test for each instance.** Honest, and it does not close the class.
6. **A comment where the trap is, with the reason.** The weakest close and the one chosen
   most often, because it is the fastest — and it depends entirely on a future reader
   noticing it.

Reach as high up that list as the cost allows, and when you settle for a lower rung, say
which rung and why. "Locked with a test on the three sites we found" is a complete and
honest statement. "Fixed" is not, when the class has fourteen members.

## The Frontier

The close of a sweep needs one thing a per-bug report does not: an explicit statement of
what was **not** covered. Without it the reader takes "I fixed nine of nine found" to mean
the system is clean, which is a claim nobody made and everybody heard.

State, at minimum:

- **Generators found**, and the enumerated size of each class.
- **Fixed, and how each was proven** — the sweep does not get to skip `reality-testing.md`
  because the individual changes were small.
- **Found and not fixed**, with the reason: out of scope, needs a decision that is not
  yours, or blocked. A defect reported and left is a result; a defect quietly dropped is
  the failure `defenses.md` calls repression.
- **Not scanned**: which modalities were not run and what would plausibly be found there.
- **What a fix changed** that other findings, or other people's work, depended on.

Then say which of the three stops ended it (`loops.md#the-three-stops`): *converged* — the
classes are enumerated and closed; *exhausted* — the budget ran out, and here is the
frontier; *diverged* — the last passes produced only restatements of findings already held,
so more scanning of this kind will not help and the modality has to change.

## Sweep Anti-Patterns

- **Fixing in discovery order.** Covered above, and worth repeating because it is the
  default behaviour of anyone working from a list.
- **Treating a scanner's output as the enumeration.** It is one modality with a known blind
  spot and a false-positive rate, not a census.
- **Counting findings as progress.** Twenty symptoms of one cause is one finding reported
  twenty times, and the count makes the work look thorough while it is being least so.
- **One commit for the whole sweep.** Unbisectable, unrevertable in part, and unreviewable —
  the reviewer cannot tell the mechanical fixes from the risky one hiding among them.
- **"While I'm here" widening.** A sweep is an invitation to unrelated cleanup and the
  answer is the same as everywhere else: report it under `Next:`, keep it out of the diff.
- **Declaring the class closed without enumerating it.** The specific sentence to distrust
  in your own output is *"I've fixed all the places where this happens"* written after a
  single text search.
