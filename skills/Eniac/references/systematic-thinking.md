# Systematic Thinking Reference

Use when a direct fix may miss dependencies, hidden assumptions, tradeoffs, or feedback effects.

## Frame

Keep only facts that affect decisions:

```text
Objective:
Boundary:
Actors/components:
Inputs/outputs:
State owner:
Constraints:
Dependencies:
Invariants:
Assumptions:
Failure modes:
Signal:
```

## Decompose

Break work by stable boundaries:

- user-visible behavior
- data flow
- control flow
- interfaces/contracts
- state ownership
- side effects
- verification path

Each unit needs an output and verification signal. Do not decompose by file count or every possible concern.

## Pattern

Pick one active pattern:

| Situation | Pattern | Proof |
| --- | --- | --- |
| small surface | direct path | one command/file/result |
| unknown cause | hypothesis tree | branch ruled in/out |
| many components | dependency path | upstream/downstream verified |
| public contract | contract map | caller/schema/API preserved |
| many options | decision matrix | value/risk/cost compared |

Switch patterns only when evidence stops fitting.

## Decision

```text
Option:
Expected value:
Risk:
Reversibility:
Token/context cost:
Verification cost:
Decision:
```

Prefer reversible, locally verifiable options that match existing patterns. Drop options needing broad rewrites, new dependencies, unverifiable assumptions, or unrequested scope expansion.

## Assumptions And Drift

- Verify cheap assumptions immediately.
- Convert expensive assumptions into explicit risks.
- Ask only when an assumption is high-impact and cannot be verified locally.
- Before acting, check: objective, boundary, invariant, verification, smaller reversible step.
- Compress long reasoning to: decision, because, risk, verify.
