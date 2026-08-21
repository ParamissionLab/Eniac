# Test-First Delivery

Use when adding or changing observable behavior, fixing a reproducible defect,
or refactoring behind a behavior contract and a meaningful automated test can
be run before implementation. Pair with `references/debugging-protocol.md` for
non-trivial defects and `references/specialists/test-quality-flakiness.md` when
the signal is weak or nondeterministic.

Do not force this workflow onto generated output, documentation-only edits,
configuration with no executable harness, exploratory spikes that will be
discarded, hardware/external behavior that cannot be isolated, or a legacy
surface where adding a harness would exceed scope. In those cases, name the
closest falsifiable alternative before changing the implementation.

## Contract

The test must be capable of disproving the claim. A green test that was never
seen failing for the intended reason may be useful regression coverage, but it
is not evidence that the test detects the new defect or missing behavior.

```text
Claim: <behavior that should exist>
Falsifier: <production change or missing behavior that must make the check fail>
Level: unit | integration | contract | end-to-end | other
Command: <focused project-native check>
```

## Red -> Green -> Refactor -> Integrate

1. **Red:** Write the smallest behavior-focused case. Run it and confirm it
   fails, not errors, for the expected missing behavior or defect.
2. **Green:** Make the smallest production change that satisfies that case.
   Run the focused check and preserve the output.
3. **Refactor:** Improve structure only while the focused case remains green;
   do not add new behavior in this step.
4. **Integrate:** Run the regression signal required by the impact radius. A
   focused unit test does not prove consumers, contracts, or the main flow.

For a defect that already has a failing test, preserve it as the Red signal.
For a refactor, capture the current behavior with characterization tests before
changing structure when the contract is not already protected.

## Honest Red

Before trusting a new test, confirm:

- its name describes one observable behavior;
- its assertion reaches production behavior rather than only a mock;
- the failure message matches the intended missing behavior;
- setup, fixtures, and dependencies are not the reason it fails;
- it would fail under a plausible regression;
- it owns its state and is deterministic.

If the test passes immediately, determine whether the behavior already exists,
the test misses the path, or the requirement is wrong. Do not manufacture a Red
state by weakening production code.

## Proportional Exceptions

When Red cannot be observed safely or within scope, record:

```text
Why test-first is not viable:
Replacement signal: static check | contract fixture | smoke path | visual proof |
  controlled experiment | staged health signal | manual reproduction
Residual gap:
Next owner/check:
```

Exceptions are evidence decisions, not convenience. A test-first unit check may
also be the wrong tool when the risk lives in deployment, concurrency, data
migration, accessibility, or a third-party integration; choose the proof level
that can actually falsify the highest-risk claim.

## Stop Conditions

- The Red failure is unrelated to the target behavior.
- Passing requires changing the test to mirror the implementation.
- The test needs production-only hooks or public surface solely for testing.
- Mocks reproduce an imagined dependency instead of the real contract.
- The minimal Green change expands into unrelated refactoring or features.
- Focused tests pass but the relevant consumer or integration signal fails.

At a stop condition, revise the test seam, requirement, or architecture. Do not
accumulate code and test patches until something happens to pass.
