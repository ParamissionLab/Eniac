# Systematic Thinking Reference

Use this reference when the task is complex enough that a direct fix may miss dependencies, hidden assumptions, or feedback effects.

## System Frame

Model the task as a system, not a list of wishes:

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
Feedback signal:
```

Keep the frame compact. Preserve only facts that affect decisions.

## Decomposition

Break work along stable boundaries:

- user-visible behavior
- data flow
- control flow
- interfaces/contracts
- state ownership
- side effects
- verification path

Do not decompose by arbitrary file count or by every possible concern. Each unit should have a clear output and verification signal.

## Reasoning Order

Use this order before acting:

1. Define the objective and non-goals.
2. Identify constraints and invariants that must not break.
3. List assumptions and mark which are verified, likely, or risky.
4. Map dependencies and blockers.
5. Choose the smallest action that reduces uncertainty or moves toward done.
6. Define the observation that will prove whether the action worked.

## Decision Rule

When there are multiple paths, score them quickly:

```text
Option:
Expected value:
Risk:
Reversibility:
Token/context cost:
Verification cost:
Decision:
```

Prefer the option that is reversible, locally verifiable, and consistent with existing patterns. Do not optimize for elegance before correctness.

## Assumption Handling

- Verify cheap assumptions immediately.
- Convert expensive assumptions into explicit risks.
- Ask the user only when an assumption is high-impact and cannot be verified locally.
- If an assumption changes, update the system frame and re-check the plan.

## Feedback Loops

Every loop must produce a signal:

```text
Action:
Expected signal:
Observed signal:
Interpretation:
Next action:
```

If the signal is ambiguous, gather sharper evidence before making larger changes.

## Anti-Drift Checks

Before each action, ask:

- Does this directly serve the objective?
- Is it inside the boundary?
- What invariant could it break?
- How will I verify it?
- Is there a smaller reversible action?

Stop or ask before crossing the boundary.
