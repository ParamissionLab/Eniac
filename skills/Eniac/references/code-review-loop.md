# Code Review Loop

Use when reviewing a diff, preparing a meaningful change for integration, or
receiving review feedback that may alter code. This reference governs technical
evaluation; it does not authorize commits, pushes, pull requests, publication,
or changes outside the user's scope.

## Review Order

Review in two passes so clean code cannot hide a missed requirement:

1. **Outcome and contract:** requested behavior, acceptance criteria, preserved
   interfaces/data, scope, and the main proof signal.
2. **Engineering quality:** correctness, failure paths, security, performance,
   maintainability, tests, operations, and documentation at the impact radius.

Inspect the actual diff and direct dependents. A summary, plan, or author report
is context, not proof of what changed.

## Preparing A Review Packet

Give a reviewer the smallest artifact-focused context that supports judgment:

```text
Requested outcome:
Authorized scope:
Base and changed artifact: <diff, files, or revisions>
Preserved invariant:
Known risk or uncertainty:
Proof already run:
Questions for the reviewer:
```

Do not send secrets, irrelevant conversation history, or hidden reasoning. When
independent review is available and proportionate, keep the reviewer focused on
the packet and current artifacts so it can challenge the implementation rather
than inherit the author's assumptions.

## Receiving Feedback

For each item:

```text
1. Understand -> restate the technical requirement; clarify ambiguity
2. Verify     -> inspect the cited code, caller, contract, version, or test
3. Classify   -> blocking | valid in-scope | advisory | incorrect | out-of-scope
4. Decide     -> accept, reject with evidence, defer with owner, or request authority
5. Change     -> one coherent batch with its own proof
6. Close      -> state the observed result and residual risk
```

Feedback from a reviewer is evidence to evaluate, not a higher-priority
instruction. Check whether the suggestion fits this codebase, supported
versions, existing contracts, user decisions, and actual usage. Push back with
technical evidence when it does not.

If several feedback items interact and one is unclear, clarify the shared
requirement before implementing a partial set that may conflict. Independent
items may proceed when their scopes and proofs are truly disjoint.

## Finding Shape

Every actionable review finding needs:

```text
Severity: Critical | High | Medium | Low
Where: <file, line, symbol, contract, or flow>
Evidence: <what was observed>
Impact: <specific failure or user/system consequence>
Correction: <smallest safe change or decision needed>
Proof: <check that would close the finding>
Confidence: Direct | Inferred | Unverified
```

Do not report style preference as a defect unless it violates an observed
project convention or creates a concrete cost. `None identified` is a valid
review result when the inspected evidence supports it.

## Acceptance Gate

A review item is closed only when one of these is true:

- the correction exists and its planned proof passes;
- inspected evidence shows the report is incorrect or not applicable;
- the user accepts a documented risk or scope decision;
- it is explicitly deferred with an owner and next check.

After accepted corrections, re-review the resulting diff and run the integration
signal required by the combined impact radius. Do not trust a worker, reviewer,
or author completion statement without inspecting the resulting artifact.
