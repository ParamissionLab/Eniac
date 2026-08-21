# Craft

The judgment calls that separate a senior engineer from a competent one. Load when
writing non-trivial code, or when a review turns on judgment rather than correctness.

Almost every decision here collapses to one question: **what will this cost the person
who touches it in six months?** That person is usually the user, sometimes you, and
they will not have the context you have right now.

## Make The Change Easy, Then Make The Easy Change

When a change is hard to make in the current structure, that difficulty is information,
not an obstacle to push through. The move is two steps: first reshape the code — behavior
unchanged, tests green — so the change becomes small, then make the small change.

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
  fail is worse than no test, because it manufactures confidence.
- Real dependencies at the seam, fakes at the leaf. A mock of your own code tests your
  mock.
- Flaky tests are defects wearing a different symptom. Quarantine with a named owner or
  fix them; re-running until green is how a real bug becomes permanent.

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
  dead.

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

## Comments

- Comment the **why**. The code already says the what, and says it more reliably.
- The highest-value comment marks a trap: a non-obvious ordering requirement, a
  workaround for an upstream bug (with the link), an ugliness that exists for a measured
  performance reason.
- A comment restating the line above it is noise the reader must still process.
- When a block needs a paragraph of explanation, check whether the naming or the
  structure is the actual problem before writing the paragraph.

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
