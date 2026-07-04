# Loop Engineering Reference

Use when the task needs autonomous repeated execution, recovery after failure, delegation, handoff, or an expensive action decision.

## Loop State

Keep only decision-relevant facts:

```text
Goal:
Scope:
Facts:
Assumptions:
Next:
Stop:
Signal:
Risk:
```

Replace state after each Observe step. Do not preserve old reasoning branches unless they affect the next action.

## Budget Modes

| Mode | Use | Context | Verify |
| --- | --- | --- | --- |
| Lean | simple or targeted work | exact files/errors needed now | cheapest meaningful check |
| Standard | uncertain bug or multi-file change | direct dependencies and nearby tests | behavior plus regression signal |
| Deep | architecture, repeated failure, high risk | relevant references and options | prove or report uncertainty |

Compress state before expanding context.

## Cost Checkpoint

Before an expensive read, broad tool run, web lookup, full test suite, browser pass, or subagent:

```text
Need:
Cheaper signal:
Expected decision:
Stop if:
```

Proceed only if the result can change the next action, verification, or risk report.

## Loop Forms

Tiny:

```text
Need:
Action:
Check:
Report:
```

Milestone:

```text
Milestone:
Risk reduced:
Action batch:
Signal:
Next:
```

Batch:

```text
Pattern:
Candidates:
Sample:
Apply:
Exceptions:
Verify:
```

Batch only when the same rule applies. Split batches when the sample diff reveals different intent.

## PRAO Checks

- Perceive: gather enough context for the next decision, not every possible source.
- Reason: choose the smallest reversible action that reduces uncertainty or moves toward done.
- Act: produce an observable signal: diff, test result, log line, rendered output, or decision.
- Observe: compare signal to done criteria and continue only if the next action is materially different.

## Recovery

After failure:

```text
Failure:
Evidence:
Class:
Changed assumption:
Next different action:
Stop if:
```

Use at most three materially different attempts before reporting the blocker and needed decision.

## Delegation

Delegate only bounded, independently verifiable work:

```text
TASK:
CONTEXT:
SCOPE:
DONE WHEN:
CONSTRAINTS:
REPORT:
```

Do not delegate core synthesis, final risk judgment, or user-facing decisions.

## Handoff

For compaction or continuation, preserve only:

```text
Goal:
State:
Files touched:
Facts verified:
Decisions:
Commands:
Risks:
Next:
Stop:
```

Avoid copying logs, diffs, or file contents unless exact text is needed next.

## Stop

Stop when done and verified, a risky assumption needs user input, three different attempts hit the same blocker, context cost has no clear gain, next work is out of scope, or remaining work is optional polish.
