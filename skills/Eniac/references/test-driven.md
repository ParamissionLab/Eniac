# Test-Driven Work

The Ego Loop asks for a commit — goal, scope, done criteria, proof — before execution.
Test-driven work is that commit made executable: the proof is written *before* the code,
run, and seen to fail, so that the code which follows has something outside your own head
to satisfy. It is the innermost loop this skill runs, and the one with the shortest turn.

Load this when a change has behaviour a check can fail on — a new function, a bug, a
parser, a rule, a calculation — and you are about to write it; when a test passed on its
first run and you are not sure why; when a test is turning out hard to write; and before
building anything you do not yet know how to build. Do not load it for a change with no
behaviour: a colour, a copy string, a configuration value. Those are checked through the
entry point, not test-driven, and the last section says how to tell the difference.

> **Owns** — the order of check and code — the check written first and seen to fail for the right reason, the red–green–refactor cycle as the innermost loop, the test list, what a first-run green means, red for the wrong reason, testability as design feedback and the smallest seam, spikes as throwaway exploration, property and generative checks, when test-first does not apply, and how the order is reported.
> **Defers** — what a test asserts and how it is named → `craft.md#tests`; the verification ladder, proof by change type, and what closes a task → `reality-testing.md`; pinning the behaviour of code whose intent is lost → `comprehension.md#characterization-tests-are-a-comprehension-tool`; the debugging chain the failing test slots into → `workflows.md#diagnose`; making a slow loop fast → `loops.md#shortening-beats-running`; proving nondeterministic output → `llm-systems.md#testing-something-nondeterministic`; which command runs tests in this stack → `stack-signals.md`.

## Contents

- [Why The Order Matters](#why-the-order-matters)
- [The Cycle](#the-cycle)
- [The Test List](#the-test-list)
- [Green On The First Run](#green-on-the-first-run)
- [Red For The Wrong Reason](#red-for-the-wrong-reason)
- [Bug Fixes](#bug-fixes)
- [Testability Is Design Feedback](#testability-is-design-feedback)
- [Spikes](#spikes)
- [Properties, Not Only Examples](#properties-not-only-examples)
- [When Test-First Does Not Apply](#when-test-first-does-not-apply)
- [Reporting The Order](#reporting-the-order)
- [Anti-Patterns](#anti-patterns)

## Why The Order Matters

A test written after the code is written *to* the code. You have the implementation in
front of you, so the assertions follow its shape, its branches, its happy path — and the
test proves that the code agrees with itself. It can pass while the behaviour is wrong,
because it was never asked to describe the behaviour, only to ratify it.

A test written first is a prediction. It says what the code must do before the code
exists to be looked at, and the moment it fails is the only moment you learn that the
test is wired to reality at all — that it imports the right module, reaches the right
function, and would notice if the behaviour were absent. `craft.md#tests` says to verify
a test can fail by breaking the code once; writing it first is that same check made
structural, because you have already watched it fail.

The order also moves the design decision to where it is cheapest. Naming the function,
choosing its inputs, deciding what it returns on the bad case — the test forces each of
those before there is an implementation to defend. Discovering the interface is awkward
*after* writing it costs a rewrite; discovering it in the test costs a line.

## The Cycle

One behaviour per turn, minutes per turn. If a turn is taking longer than that, the step
was too large — back up and take a smaller one, because a long red is a loop with no
signal.

**Red.** Write the smallest test that expresses the next behaviour on the list, and run
it. It must fail, and it must fail *for the reason you expect*: the assertion, with the
value the current code actually produces. Read the failure output rather than the colour
— the message is the evidence that the test tests this.

**Green.** Write the simplest code that makes it pass. Simplest genuinely means simplest:
if one test demands one value, returning that value is a legitimate step, and the second
test is what earns the general case. Code that no test demanded is where untested branches
come from, and every branch you add on speculation is a branch you have to remember to
cover later. The step is legitimate because the cycle does not end at green — it ends
when the test list is empty, and a stub that satisfies one test is a stub until the next
test replaces it.

**Refactor.** Now, with green as the net, restore the design: remove the duplication the
last step introduced, name what became nameable, move what landed in the wrong place —
in the test as well as in the code. Behaviour unchanged, suite run after each move. This
is the step that gets skipped when the code works, and skipping it is how test-driven work
produces correct code nobody wants to read. The cycle is not done at green.

Then the next item on the list. Turn length is what makes this a method rather than a
ritual: a test-run that takes a minute makes every step a decision, while one that takes
ten makes you batch — and a batch of tests written before any code is a specification,
not a cycle, and loses the design feedback each red would have given you
(`loops.md#shortening-beats-running`).

## The Test List

Before the first red, write the behaviours down as one-liners — the happy path, each
boundary, each error case, the invariant that must hold — drawn from the contract the
Implement chain asks for at step 3. Then take them one at a time, choosing next whichever
teaches you the most for the least code, which is usually the simplest one still failing.

The list is the done criterion made checkable. Without it, "widen to the edge cases" is a
feeling about completeness; with it, widening is crossing items off and adding the ones
you discovered on the way. It also answers *when to stop* — the loop's stop condition —
which is otherwise decided by fatigue. When a case space is large enough that a list
cannot hold it, enumerate rather than sample (`reasoning.md#enumerate-the-cases-then-prove-coverage`),
and consider a property instead of a row.

## Green On The First Run

A test that passes before any production code changed is not a result. It is one of
three findings, and you do not know which until you look:

| Finding | Tell | Right move |
| --- | --- | --- |
| The behaviour already exists | the current code visibly does it | no production change; say so; keep the test if it pins something the suite did not |
| The test asserts nothing, or the wrong thing | it would pass against an empty function | fix the test until it goes red |
| The wrong code is under test | a stale import, a cached build, a fixture that shadows the real thing | fix the wiring, then re-run |

The costly response is the natural one: write the code anyway. That produces an
implementation of something that already works, a diff nobody needed, and a test that
"proves" a change that never happened. First-run green is a stop, not a green light.

One look usually settles it. When the current code visibly does the thing — the line is
right there — that is the finding, and it is reported in a sentence; the other two rows
are for when you cannot see why it passed. Proving the test can go red against a stub is
worth doing when the assertion is not obviously about the behaviour, not as a ritual
after every green.

## Red For The Wrong Reason

An import error, a typo in the fixture, a missing dependency, a wrong argument count —
each is a failure that has not reached the assertion yet. Treat it as *not red*: the test
has not said anything about the behaviour, only about the plumbing. Fix the plumbing,
re-run, and only count the red when the failure message names the value the current code
produces.

For the very first test on a new function an import or name error is a legitimate first
signal — it proves the test is looking in the right place — but you still have not seen
the assertion fail. Add the stub, run again, watch the assertion go red, then implement.

## Bug Fixes

A bug reproduced as a failing test is two steps of the Diagnose chain in one artifact: the
reproduction, and the lock that stops it coming back. Write the test with the input from
the report, assert the behaviour that should have happened, and run it against the
unchanged code. It should fail with the exact wrong value from the report — `5400`, not
some other wrong value — because that is what confirms you have reproduced *this* bug
rather than a neighbour.

Then fix at the cause (`workflows.md#diagnose`), watch the test go green, and before
closing ask what else the same cause would have broken: the input from the report is
almost never the only member of its class. Add the sibling case while the cause is in
front of you — that is the class closing, and it costs one line now and a second ticket
later.

Reproducing by hand and promising a test "at the end" usually ships without one, because
by the end the fix works and the test feels like paperwork. The order is what makes it
happen.

## Testability Is Design Feedback

When the test is hard to write, the code is telling you where a seam is missing. The usual
reasons: the function reads the clock, the environment, a global, a file by fixed name,
the network, or a database it opens itself; or it does five things in one body, so nothing
can be reached without doing all of them. Difficulty here is not a reason to reach for a
mocking framework. It is the design review you did not get.

The moves, cheapest and most durable first:

1. **Extract the pure part** and test it directly, with no doubles at all. Formatting,
   calculation, decision logic — most of what a function does is usually pure once the
   I/O around it is peeled off.
2. **Pass the collaborator in.** A parameter with a default that is the real thing
   (`today=None`, `sender=None`) leaves every existing caller untouched and lets the test
   hand in a value or a fake. This is the smallest seam that exists.
3. **Patch at the boundary, last.** One thing, at the edge of the code you own, and say
   why the seam was not worth making.

Patching six globals to reach one assertion is the anti-pattern. The test that results
pins the internals — every call, every module path — so it breaks on any honest refactor
while proving little about behaviour, and the design that made it necessary is unchanged.
The rule from `craft.md#tests` holds here: real dependencies at the seam, fakes at the
leaf, and a mock of your own code tests your mock.

Prefer the simplest double that works: a value, a stub that returns one thing, a fake that
records what it was given (a list is enough). A mock framework asserting call order is
almost always testing the implementation, and it will say so at the first refactor.

## Spikes

When you do not know whether something works — an unfamiliar API, a library's real
behaviour, whether an approach is fast enough — the honest move is not to test-drive it
and not to guess. It is a spike: a time-boxed, throwaway experiment with one question,
written with no tests and no care, whose only output is the answer.

Three rules keep a spike from becoming production code with no history:

- **One question, written down first.** "Does the batch endpoint accept 500 ids or does it
  cap at 100?" — not "explore the API".
- **Record the answer, then delete the code.** The numbers, the shape that worked, the
  trap you hit — those survive, in the report or the plan. The code does not.
- **Then build it test-first**, from what you now know. Spike code that "works, so let me
  just add tests" gets tests written to it, which is the failure the whole order exists
  to prevent; and a spike that survives is untested code whose only documentation is that
  it was once an experiment.

## Properties, Not Only Examples

Example tests sample the input space, and for a parser, a serializer, a calculation, or
anything with a round-trip, the space is far larger than any list. A property states what
must hold for *every* input and lets a generator search for the counterexample:

- **Round-trip** — `decode(encode(x)) == x`
- **Invariant** — the output of `sort` is ordered *and* a permutation of the input
- **Idempotence** — applying it twice equals applying it once
- **Oracle** — it agrees with a slow, obviously-correct reference implementation
- **Monotonicity, bounds, symmetry** — whatever the domain promises

Most ecosystems have a property tool (Hypothesis, fast-check, QuickCheck, proptest are
examples); a loop over generated inputs with a seed does the job where none exists. A
property that finds a failing example has handed you the next red — shrink it to the
smallest input, add it as an example test, and fix. And when the suite looks suspiciously
green, break the code deliberately once and confirm something goes red: a suite that
cannot fail is the most expensive kind of reassurance.

## When Test-First Does Not Apply

Test-first is for behaviour that a check can fail on. Applied where there is none, it is
ceremony — and ceremony teaches everyone to skip the ritual exactly where it would have
caught something. Skipped where there *is* behaviour "because it is obvious", it is
omnipotence (`defenses.md#omnipotence`). Both failures cost; the second costs more.

| Change | Instead of test-first |
| --- | --- |
| A value with no behaviour — a colour, a string, a config key, a version bump | change it, check it through the entry point |
| Visual layout, a screen, how something looks | look at it through the real entry point (`reality-testing.md#the-verification-ladder`, rung four); a snapshot only once the shape is stable |
| Glue and wiring with no logic of its own | the integration rung — the seam, exercised once |
| Something you do not know how to build yet | a spike, then test-first |
| Legacy code with no seam to test through | pin current behaviour first (`comprehension.md#characterization-tests-are-a-comprehension-tool`), make the smallest seam, then test-drive the change |
| A throwaway script the user will run once | run it on the real input and read the output |
| The user said no tests | no tests, plus one sentence naming the risk — precedence settles this |
| The user declined a *suite* — "no time for tests right now", "just get it in" | the ceremony is declined, not the check: the cases you ran to verify the change are kept as the smallest test file that runs in CI. Three asserts in one file cost less than the paragraph reporting them, and without that file the next edit to the function reverts the change with nobody noticing |

When the change is small enough to be obvious *and* has behaviour, the check is still
written first: it is one assertion and thirty seconds, and it is the thirty seconds that
turns "obviously right" into "observed".

## Reporting The Order

Say what was written first, the failing line you observed, the pass count after, and
where the check now lives.
`"Wrote the test; ImportError: cannot import name 'slugify'; implemented; 8 passed."` is
one line and it is the whole proof. "Tests pass" on its own is indistinguishable from a
test written afterwards, and a reader who cannot tell the difference has to assume the
weaker one. A check that was run and then deleted is reported as *discarded* — which is a
statement that the change has no lock, and usually the moment you decide to keep it.

## Anti-Patterns

- **Test-after described as test-first.** The tell: no failing output anywhere in the
  report.
- **The batch.** Every test for a non-trivial piece written before any code. That is a
  specification with a suite attached; the design feedback of each red is gone, and the
  first green usually requires rewriting half the tests. A few one-line cases for a
  four-line function are a test list, not a batch — the line is whether the next test
  could still change the design.
- **Testing the implementation.** Asserting which private function was called, or in what
  order. Passes today, breaks on the first refactor, proves nothing about behaviour.
- **The mirror.** The test computes the expected value with the same logic as the code —
  the same regex, the same formula. It proves the code equals itself. Expected values are
  literals.
- **Green by editing the assertion.** The test disagreed with the code, and the test lost.
  Sometimes correct; never silent.
- **The scratch check.** Verifying with a throwaway script, reporting its numbers, and
  deleting it. The change is verified and unlocked, and the next edit to that file
  reverts it with nobody noticing. If the script ran, it is the test — keep it, in the
  suite's shape, however small.
- **Coverage as the goal.** A number that goes up when tests get worse
  (`judgment.md#goodharts-law`). The goal is a check that fails when the behaviour breaks.
- **Skipping refactor.** Green and stop. The code works and reads like the order it was
  written in.
- **The giant red.** A test so large that making it pass takes an hour of blind coding.
  Split it; the loop has no signal until it is green.
