# Systematic Thinking Reference

Use when a direct fix may miss dependencies, hidden assumptions, tradeoffs, or feedback effects.

## Frame

```text
Objective:
Boundary:
Actors/components:
Inputs:
Outputs:
State:
Constraints:
Dependencies:
Invariants:
Assumptions:
Failure modes:
Signal:
```

Keep only facts that affect decisions.

## Decompose

Break work by stable boundaries:

- user-visible behavior
- data flow
- control flow
- interfaces/contracts
- state ownership
- side effects
- verification path

Each unit needs an output and verification signal.

## Pattern

| Difficulty | Pattern | Use |
| --- | --- | --- |
| Small surface | direct path | one command, one file, obvious answer |
| Unknown cause | hypothesis tree | bug, regression, flaky behavior |
| Many components | dependency path | integration, data flow, architecture |
| Many stakeholders | contract map | API, schema, public behavior |
| Many options | decision matrix | design, planning, tool choice |

Use one active pattern. Switch only when evidence stops fitting.

## Hypothesis Tree

```text
Symptom:
Likely causes:
Fastest test:
Ruled out:
Current best:
Next proof:
```

Prefer tests that eliminate branches before editing.

## Dependency Scan

List only dependencies that can change the decision:

```text
Upstream:
Downstream:
State owner:
External:
Contract:
Verifier:
```

## Decision

```text
Option:
Value:
Risk:
Reversibility:
Context cost:
Verification cost:
Decision:
```

Prefer reversible, locally verifiable options that match existing patterns. Kill options needing broad rewrites, new dependencies, unverifiable assumptions, or unrequested scope expansion.

## Assumptions And Drift

- Verify cheap assumptions immediately.
- Convert expensive assumptions into explicit risks.
- Ask only when an assumption is high-impact and cannot be verified locally.
- Before action, check: objective, boundary, invariant, verification, smaller reversible step.
- Compress long reasoning to: decision, because, risk, verify.
