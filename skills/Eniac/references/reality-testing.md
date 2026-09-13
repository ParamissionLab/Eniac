# Reality Testing

Distinguishing the internal model from the world is the Ego's defining job. In
engineering it is the difference between a change and a result.

Load this when choosing how far to verify, when separating a regression you caused from
one you inherited, or when deciding what actually closes a task.

> **Owns** — what counts as evidence — the verification ladder, baseline before regression, proof by change type, the adversarial pass that runs before a done claim, truthful reporting vocabulary, what to do when you cannot run it, common false proofs, closing criteria.
> **Defers** — what a test should assert → `craft.md#tests`; the order of check and code, and what a first-run green means → `test-driven.md`; proving a performance change → `performance.md`; proving nondeterministic output → `llm-systems.md#testing-something-nondeterministic`; which command proves anything in this stack → `stack-signals.md`; attacking a *plan* rather than a finished change → `judgment.md#pre-mortem`; attacking a whole system on an attacker's terms → `security.md#reviewing-for-security`.

## What Counts As Evidence

| Strength | Source |
| --- | --- |
| Strongest | output you just observed from executing the actual code path |
| Strong | a test that fails on the old code and passes on the new |
| Medium | a read of the current source at a known revision |
| Weak | repository convention, documentation, a comment |
| Not evidence | inference, memory of a similar codebase, "it should", a plan |

A run proves exactly the behavior it exercised — no more. A green unit test says the
unit behaves; it says nothing about wiring, configuration, or the real entry point.
A successful build says it compiles.

When two sources disagree, the observed signal wins over the source, and the source
wins over the documentation. Documentation drifts; running code does not.

**Re-reading your own reasoning is not verification.** Deliberate checking tends to
ratify the first answer rather than test it, so a check that never leaves your own head
confirms nothing except that you are consistent. Every rung below touches something
outside it.

## The Verification Ladder

Climb from cheapest, and stop at the rung the risk actually requires. Climbing further
than the risk justifies is waste; stopping short of it is how regressions ship.

1. **It parses** — syntax, types, lint. Seconds. Catches typos, catches nothing else.
2. **The unit behaves** — targeted test on the changed logic. This is the rung most
   changes need.
3. **The seam holds** — integration across the boundary you touched: the real
   database, the real serializer, the real route.
4. **The real entry point works** — the way a user actually invokes it: the CLI
   command, the HTTP request, the button. Many bugs live only here, in wiring and
   configuration that no unit test sees.
5. **Nothing else broke** — the surrounding suite, scaled to blast radius.

Rung 4 is the one most often skipped and most often needed. A feature that works in
tests and not through its entry point is not delivered.

## Baseline Before Regression

Before touching a repository whose state you do not know, capture what already fails.
Without a baseline, every pre-existing failure looks like something you caused, and
every failure you caused can be dismissed as pre-existing.

Record the command, the counts, and the names of failing tests. When reporting later,
state both numbers: what failed before, what fails now. "Tests pass" is a much weaker
and more suspicious claim than "12 failed before, the same 12 fail now, plus the 3 I
added pass".

## Proof By Change Type

| Change | Proof that actually closes it |
| --- | --- |
| Bug fix | a check that fails on the old code and passes on the new |
| New behavior | exercised through the real entry point, plus its error path |
| Refactor | identical results from tests written before the change |
| Performance | before and after numbers on the same workload |
| Contract change | every known consumer still works, or is updated in the same change |
| Data change | run on a copy, counts before and after, reversal tested |
| Config or infra | applied in a real environment, effect observed, not assumed |
| Deletion | the callers are gone too, and the suite still passes |
| Documentation | the commands in it were actually run |

## Attack It Before You Claim It

Everything above asks *did the thing I intended work*. That question is asked by the
person who intended it, which is exactly the wrong person to ask it — you test the path
you had in mind, and the path you had in mind is the one you already got right. So before
writing `Done`, switch roles: stop defending the change and try to break it.

**The gate.** At L2 and above, and at any level when the change touches a trust boundary,
persisted data, concurrency, money, or a contract someone else depends on: name **at least
three concrete ways this specific change breaks**, then say what each one turned into.
Every mode ends in one of three states, and silence is not one of them.

| State | Means | What it must carry |
| --- | --- | --- |
| **Handled** | the code already survives it | the check that demonstrates it, run |
| **Accepted** | real, and deliberately not addressed | why, and who the decision belongs to |
| **Open** | real, and unaddressed | a line in `Risks:` — never omitted because it was inconvenient |

**Generating modes that are worth the two minutes.** The failure of this exercise is
reciting three generic ones — null input, network down, large payload — that could have
been written before reading the diff. If a mode does not name something from *this*
change, it is ceremony. Prompts that produce specific ones:

| Angle | The question to ask of this change |
| --- | --- |
| **Input** | what value passes every check and still produces nonsense — empty, zero, negative, duplicate, unicode, the maximum, the value from the bug report |
| **State** | what is true on the second call that was not true on the first — cached, already inserted, partially written, retried after a crash |
| **Ordering** | what if two of these run at once, or arrive out of order, or the slow one finishes last |
| **Dependency** | what if the thing it calls is slow, returns a well-formed wrong answer, or fails after having already acted |
| **Scale** | what happens at a thousand times the row count, and where the unbounded growth is |
| **Authority** | who can reach this that should not — another tenant, an expired session, a request that skips the interface |
| **Environment** | timezone, locale, encoding, filesystem case, clock skew, a different runtime version |
| **Reversal** | if this is wrong in production, what does undoing it cost, and what is already unrecoverable |

**A mode is only real if it can be written as a test.** "Bad input breaks it" is a
feeling. "An empty list reaches `mean()` after the filter drops every row, and the
handler returns 500 instead of an empty result" is a mode — it names the input, the path,
and the observable. Anything vaguer is either not understood yet or not there.

The cheapest three of these usually become the regression tests the change was missing
anyway, which is why this pays for itself rather than costing extra.

**Scale it down honestly.** A typo fix does not get an adversarial pass; its failure mode
is the typo. Running this ritual on L0 and L1 work is the same failure as skipping it on
L3 work — ceremony applied where it changes nothing, which teaches everyone to ignore it
where it would have.

## Truthful Reporting

Words carry claims. Use them precisely — a user who cannot trust the report has to
re-verify everything, which costs far more than an honest "I could not run this".

- **"Verified"** — you ran it and observed the result. Name the command, and where the
  check now lives. A check that was run and then deleted is `Verified (discarded)`: true,
  and a statement that the change has no lock.
- **"Implemented"** — the code exists and is complete, and you are saying nothing
  about whether it runs.
- **"Unverified"** — you could not execute it. Say why, and give the exact command
  that would settle it.
- Never write "should work", "now works", "fixed", or "this resolves it" about
  something you did not execute. If it needs a hedge, it needs a label instead.

Report a partial result as a partial result. "Three of four migrated; the fourth fails
on X" is a useful deliverable. "Migration complete" when it is not is a defect you
handed to someone else.

## When You Cannot Run It

Sometimes execution is genuinely unavailable: missing runtime or dependencies, no
credentials, a read-only environment, hardware you do not have, or behavior that only
appears under real production load. This is common and it is not a failure — silently
downgrading to "it looks right" is.

1. **Try to remove the barrier first.** Installing dependencies or starting the service
   is usually cheaper than reasoning carefully about code you cannot execute, and it
   converts every later claim from argument into evidence.
2. **If the barrier stands, say what it is.** "No database credentials in this
   environment" tells the user something actionable. Omitting it does not.
3. **Take the strongest check still available** — type checking, static analysis, a
   targeted read of the full call path, or a hand trace of the data through each
   transformation. Name which one you used.
4. **Label the result `Unverified`** and give the exact command someone with access
   should run, so the gap closes in one step rather than in another conversation.

**Never present an expected output as an observed one.** Inventing a plausible test
result or command output is the single most damaging thing an agent can do, because it
is undetectable at the time and it retroactively makes every other claim untrustworthy.

## Common False Proofs

- **The error changed, so it is fixed.** A different error is a different bug, possibly
  the same one wearing a coat.
- **The test passes, so the code is right.** Check that the test fails when you break
  the code — or write it first and watch it fail, which is the same check made
  structural (`test-driven.md`). A test that cannot fail proves nothing, and a test
  that passed on its first run before any code changed has not yet proven anything
  either.
- **It works locally.** Locale, timezone, filesystem case, environment variables, and
  installed versions are all part of the code path.
- **The deploy succeeded.** That proves an upload, not a behavior.
- **The retry passed.** Intermittent success on a flaky check is not evidence; it is
  the bug still being present.
- **I read the code and it looks right.** The most reliable way to be confidently wrong.

## Closing Criteria

**Mutations** close when the outcome exists through its intended entry point, the
highest-risk invariant is intact, focused proof covers the changed behavior, regression
proof matches the blast radius, and at L2+ the adversarial pass has run with every mode
landed as handled, accepted, or open.

**Reviews, explanations, designs, and plans** close on traceable evidence, internally
consistent decisions, and explicitly stated unknowns. Never phrase a proposal as if it
had already happened, and never present an unrun command's expected output as a result.
