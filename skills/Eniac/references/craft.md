# Craft

The judgment calls that separate a senior engineer from a competent one. Load when
writing non-trivial code, or when a review turns on judgment rather than correctness.

Almost every decision here collapses to one question: **what will this cost the person
who touches it in six months?** That person is usually the user, sometimes you, and
they will not have the context you have right now.

> **Owns** — the code judgment calls — the write-less ladder climbed before writing any code and the same ladder as a review lens for excess, abstraction timing, naming, error handling, boundaries and coupling, what a test should assert, concurrency, deletion, illegal states, the posture every number it introduces has to declare, comments, designing an interface others use, taking a dependency, commits.
> **Defers** — what specifically breaks a *published* contract → `stack-signals.md#what-breaks-a-contract-in-any-language`; whether the change is proven → `reality-testing.md`; the order of check and code, and what to do when a test is hard to write → `test-driven.md`; whether it is fast enough → `performance.md`; whether it resists an attacker → `security.md`; the step chain for building it → `workflows.md#implement`; recording a shortcut taken on purpose → `debt.md#name-it-when-you-create-it`; proving a whole set of code dead during a cleanup sweep → `code-health.md`; designing the persisted shape itself and the states an entity moves through → `data-modelling.md`.

## Write Less: The Ladder

The best code is the code that was never written — not because short is pretty, but
because every line is a permanent cost to whoever reads, tests, and maintains it, and most
lines an agent writes are lines something already provided. So before writing any code,
climb this ladder and stop at the first rung that holds:

1. **Does this need to exist at all?** A feature nobody asked for, a case that cannot
   occur, flexibility for a future that has not arrived — do not build it.
2. **Does it already exist in this codebase?** The helper, the utility, the pattern two
   files over. Reuse it rather than writing a second one; two implementations of one idea
   is a permanent tax on every reader.
3. **Does the standard library do it?** It usually does, with the edge cases handled.
4. **Does the platform do it natively?** The browser, the database, the framework, the
   runtime — a capability that is already there costs nothing to depend on.
5. **Does an installed dependency do it?** Something the project already pays for.
6. **Can it be one line?** Then it is one line.
7. **Only then write the minimum that works** — and match the conventions around it.

The ladder runs *after* understanding the problem, never instead of it: read the task,
read the code it touches, trace the real flow, then climb. The shortest working diff wins
— but the smallest change in the wrong place is not economy, it is a second bug. And when
two options on the same rung are the same size, take the one that is correct at the
edges; less code was the goal, not a flimsier algorithm.

**What the ladder never cuts.** Input validation at a trust boundary, error handling that
prevents data loss, security, accessibility, the calibration real hardware needs, the one
check that proves the logic (`test-driven.md`), and anything the user explicitly asked
for. Lean means fewer lines of *speculation*, not fewer lines of correctness.

**When the request itself is the excess** — a framework for one config, an abstraction
for one caller — say so once, in one line, and name the leaner thing that would cover it.
Then build what was asked if they still want it; precedence is theirs. Explaining at
length why you did not build something is itself complexity: in the report, the code
comes first, then at most three short lines on what was skipped and what would make it
worth adding.

**A corner cut on purpose gets a record**, where the next reader will hit it, naming the
ceiling and the condition that retires it — `debt.md#name-it-when-you-create-it`. A
deliberate `O(n²)` scan with a note is a decision; the same scan without one is a bug
someone will find in production.

**The ladder as a review lens.** When the question about a diff is *what can be deleted*
rather than *what is wrong*, walk it with the same rungs and report one line per finding,
each carrying its class: **delete** (dead code, unused flexibility, a speculative feature —
nothing replaces it), **stdlib** (a hand-rolled thing the standard library provides — name
the function), **native** (a dependency or code replicating a platform capability — name
the feature), **yagni** (an abstraction with one implementation, a layer with one caller,
a configuration nobody sets), **shrink** (the same logic in fewer lines — show the form).
Close with the net lines the diff could lose, or with *lean already* when it is. The
minimum a review never flags as excess is the one check that proves the logic. This lens
finds excess and only excess — correctness, security, and performance are the ordinary
Review chain, and a lean bug is still a bug.

## Make The Change Easy, Then Make The Easy Change

When a change is hard to make in the current structure, that difficulty is information,
not an obstacle to push through. The move is two steps: first reshape the code — behavior
unchanged, tests green — so the change becomes small, then make the small change.

Whether that reshaping is in scope for *this* task is a separate question with its own
answer — `debt.md#in-the-path-or-merely-nearby`. Being in the file is not the test.

Forcing a change into a shape that resists it is what produces the special-case
parameter, the duplicated branch, and the flag nobody removes. And the reshaping step is
separately reviewable and separately revertible, which the combined version never is.

## Abstraction Timing

- **Duplicate twice, abstract on the third.** Two examples cannot show you which parts
  actually vary; the abstraction built from two is usually wrong in a way that only
  shows up at the fourth caller.
- **A wrong abstraction costs more than duplication.** Duplication is visible and local.
  A wrong abstraction is invisible and global, and every future caller pays to work
  around it.
- **Inline it back before abstracting differently.** Deleting a bad abstraction is
  ordinary maintenance, not an admission of failure.
- **A boolean flag that switches behavior means there were two functions.** Parameters
  added so one function can serve two callers is the smell, not the solution.
- Do not build the general case before the second caller exists. Speculative generality
  is a bet on a future you cannot see, paid for in present complexity.

## Naming

- Name for what it is in the domain, not how it is implemented. `retryDelayMs`, not `n`.
  `pendingInvoices`, not `list2`.
- Length scales with scope. A loop index can be `i`; a module-level export cannot.
- **If you cannot name it, you do not yet understand its responsibility.** That is the
  useful signal — renaming later is cheap, but a wrong boundary is not.
- Match the codebase's existing vocabulary even where you prefer different words. Two
  names for one concept is a permanent tax on every reader.
- Booleans read as assertions: `isExpired`, `hasAccess`. Negated names (`notDisabled`)
  produce double negatives at the call site.

## Error Handling

Most bad error handling is a failure to decide. For each error, pick one:

- **Expected and recoverable here** — handle it, at the level that has enough context
  to actually act.
- **Expected but not recoverable here** — propagate it, adding context on the way up.
- **Impossible / programmer error** — fail loudly and immediately. A "safe" default
  hides the bug and relocates the crash somewhere unrelated and harder to diagnose.

- **Never catch what you cannot act on.** A `catch` that logs and continues converts a
  loud failure into silent corruption — strictly the worse outcome.
- Add context, do not replace it. Wrapping an error in a new opaque message and
  discarding the original destroys the only evidence anyone had.
- **Choose fail-closed or fail-open deliberately.** When a check cannot complete — the
  auth service is down, the rate limiter is unreachable — refusing and allowing are both
  defensible, and the wrong default is the silent one. Anything guarding access, money, or
  safety fails closed. Availability of a non-sensitive read may fail open. Never let the
  answer be whatever the code happened to do.
- Error messages get read at 3am by someone who did not write the code: say what
  failed, what was expected, and what to do about it.

## Boundaries And Coupling

- **Depend on the narrowest thing that works:** a function over a module, an interface
  over a concrete type, data over behavior.
- **Two modules that must change together are one module wearing a costume.** Either
  merge them or fix the boundary; pretending otherwise makes every change a two-file
  change forever.
- Push side effects to the edges. Keep the core computable and testable without a
  database, a clock, a network, or a filesystem.
- A boundary is real only if you can state what crosses it. If everything crosses, there
  is no boundary — only a directory.
- **With enough users, every observable behavior becomes a contract** — not only the
  documented ones. Ordering that happens to be stable, an error string someone parses, a
  field that happens to be present, a timing that happens to be fast. "Internal" protects
  you until someone depends on it. Before changing observable behavior on a widely used
  path, find out who is watching instead of assuming the documentation defines the surface.

## Tests

- **Test the behavior you promise, at the boundary you promise it.** Tests bound to
  internals calcify the design and break on every honest refactor.
- One reason to fail per test. A test that can go red for five reasons tells you nothing
  when it does.
- The name states the scenario and the expectation: `rejects_expired_token`, not
  `test_auth_2`.
- **Verify the test can fail.** Break the code deliberately, once. A test that cannot
  fail is worse than no test, because it manufactures confidence. Writing the test
  before the code is this check made structural — the order, the cycle, and what a
  first-run green means are `test-driven.md`.
- Real dependencies at the seam, fakes at the leaf. A mock of your own code tests your
  mock. Prefer the simplest double that works — a value, a stub, a list that records —
  over a framework asserting call order, which tests the implementation rather than the
  behaviour.
- Expected values are literals. A test that computes the expectation with the same logic
  as the code proves the code equals itself.
- Flaky tests are defects wearing a different symptom. Quarantine with a named owner or
  fix them; re-running until green is how a real bug becomes permanent.

## Concurrency

Concurrency defects pass every test and fail in production, because tests run one thing
at a time and production does not.

- **Name the shared mutable state.** Every concurrency bug is two things touching the
  same state with no agreed order. If you cannot name the state, you are not reasoning
  about the bug — and most "random" failures are exactly this.
- **Prefer not sharing over sharing carefully.** Immutable data, a message, a copy, or
  confinement to a single owner removes the problem instead of managing it. A lock is
  the fallback, not the opening move.
- **Check-then-act is a bug.** `if not exists: create()` is two operations with a gap in
  the middle. Use the atomic form the platform already offers: a unique constraint, a
  conditional write, compare-and-swap, an upsert.
- **Locks need a written order.** Deadlock is two paths taking the same locks in
  different orders. Decide the order and record it, or discover it at 3am.
- **Async is not automatically safe.** A single-threaded event loop still interleaves at
  every `await`, so state read before one can be stale after it.
- **Cancellation propagates or it leaks.** A cancelled request whose work keeps running
  is a resource leak that only shows up under load.
- **Reproduce with pressure, not hope** — stress, forced interleaving, deterministic
  scheduling, or a race detector. "I could not reproduce it" is not evidence of absence
  for this bug class; it is the normal experience of it.

## Deletion

- **Delete the code you replaced.** Two implementations of one thing guarantees the next
  reader picks the wrong one.
- Commented-out code is deleted code with extra steps. Version control already remembers.
- Before deleting, search for dynamic callers, not only static ones: reflection,
  dependency injection, template strings, configuration files, serialized names, and
  routes defined by convention do not appear in a symbol search.
- **Find out why it is there before removing it.** Strange code in a long-lived system is
  usually a fix for something no longer visible; `git log -S` and `git blame` on the odd
  line will usually surface the bug it was written for in under a minute. Not knowing the
  reason is not evidence there is none.
- Code you *think* is unused needs evidence first. Code proven unreachable is worth
  removing — dead code is read, trusted, and maintained by people who do not know it is
  dead. Deleting a whole set of it at once — unused files, dependencies, and exports in one
  pass — needs the proof procedure in `code-health.md`, because grep finding nothing is one
  modality reporting nothing.

## Make Illegal States Unrepresentable

The cheapest bug is the one the type, schema, or constructor refuses to express.

- **Parse at the boundary; do not validate everywhere.** Convert untrusted input into a
  trusted shape once, at the edge, and let everything inward take that shape for granted.
  Validation scattered through the call stack means every caller has to remember, and one
  eventually will not.
- Prefer a shape that cannot be wrong over a check that catches it being wrong. Two
  optional fields where exactly one must be set is a bug generator; a two-case union is not.
- Encode the invariant where it is enforced — a constructor, a database constraint, a
  narrow type — not in a comment asking future readers to be careful.
- This is the opposite of defensive programming, not a version of it: defensive code
  repeats the same check everywhere, while this makes the check unnecessary past the edge.

## Every Number Carries Its Derivation

A timeout, a retry count, a page size, a pool size, a TTL, a batch size, a backoff, a
threshold, a rate limit, a memory budget. Each one you introduce becomes permanent and
unexplained unless it arrives with its reason, because nobody deletes a number they cannot
account for — they work around it.

The failure mode is not the guess. It is that **an unlabelled number reads as derived
whether it is or not**, so the next reader treats a value somebody invented in a hurry as
one somebody measured, and nobody can tell which of the two it is safe to change. That is
why the fix is a label rather than a better guess. Adapted from the numbers policy in the
`dm-game` design plugin, which states the rule for game-balance values and states it well.

So every number declares one of three postures:

| Posture | What it requires |
| --- | --- |
| **Derived** | the input it came from, written where the number is — a measured p99, a documented API limit, a row size, an SLA, a page budget |
| **Starting value** | an explicit label saying it is a guess, the signal that would move it, and which direction to move |
| **Measured here** | what was measured, on what sample, and when |

Not acceptable: *industry standard*, *best practice*, *typical*, *should be fine*, or a bare
literal at a call site with nothing attached to it.

Where the derivation lives matters as much as having one: a named constant with the reason
beside it, not a literal three frames down a call stack where the next reader meets it
without context (`#comments`). And a starting value that nobody revisits becomes a derived
one in everybody's mind within about a release, so the label is the part doing the work.

The exception is a number with no behaviour behind it — a colour, a column width, a version
string, a copy length. Deriving those is the ceremony rather than the discipline, and
`SKILL.md#investment-levels` is the reason to skip it.

## Comments

- Comment the **why**. The code already says the what, and says it more reliably.
- The highest-value comment marks a trap: a non-obvious ordering requirement, a
  workaround for an upstream bug (with the link), an ugliness that exists for a measured
  performance reason.
- A comment restating the line above it is noise the reader must still process.
- When a block needs a paragraph of explanation, check whether the naming or the
  structure is the actual problem before writing the paragraph.

## Designing An Interface Others Use

An interface is a promise, and a bad one is paid for by everyone who calls it.

- **Consistency beats cleverness.** An interface matching the conventions around it is
  learned once; a better-but-different one is learned every time.
- **Make the common case the short case** and the dangerous case explicit. If the
  easiest call is the wrong one, the wrong one ends up everywhere.
- **Least astonishment.** A function that also writes to disk, mutates its argument, or
  populates a cache has broken a promise its name made.
- **Errors are part of the signature** — what can fail, how the caller finds out, and
  what state things are in afterwards are contract, not implementation detail.
- **Defaults are decisions made for the caller.** Choose the safe one; most callers will
  never change it.
- Narrow now, widen later. Widening an interface is easy; narrowing one breaks everybody.

## Dependencies

A dependency is a permanent commitment to someone else's decisions, taken on behalf of
whoever maintains this next. Before adding one, weigh three things: how much code it
genuinely saves, how maintained it is, and how hard it would be to remove later.

Prefer the standard library, then the ecosystem's dominant option, then anything else.
Never add a dependency to save a small amount of code you already understand.

## Version Control

Only when asked to commit — committing unprompted removes the user's chance to review
before history is written.

- One logical change per commit. A commit that does two things cannot be reverted for
  one of them.
- The message says what changed and why, in the imperative. The diff already shows how.
- **Never mix a refactor with a behavior change** in one commit: review becomes
  impossible and `git bisect` becomes useless.
- Branch off the default branch before committing.
- Never rewrite published history, and never force-push a shared branch.
