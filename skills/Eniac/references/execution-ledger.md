# Execution Ledger

Use for greenfield, broad, or L2-L4 implementation work that needs durable state. The ledger is a restartable control surface, not a narrative plan.

## Ledger Rules

- Record only facts and decisions that constrain the next action.
- Tie every milestone to an observable proof signal.
- Replace current state instead of appending progress logs.
- Separate requested scope, preserved contracts, and explicit non-goals.
- Keep one semantic item per line; never compress milestones or checks into semicolon-separated text.
- Wrap long values as indented continuation lines so labels and checklist markers remain scannable.
- Record a blocker only after evidence rules out the next safe action.
- Never store secrets, full logs, hidden reasoning, or copied source files.

## Shape

```markdown
# Eniac Execution: <short outcome>

> Owner: <task id or short label>
> Status: active | blocked | done

## Contract

- **Goal:** <requested result>
- **Done when:** <observable completion criteria>
- **Scope:** <authorized files, behavior, or systems>
- **Preserve:** <public behavior, data, compatibility, user changes>
- **Exclude:** <adjacent work not authorized>

## System

- **State:** greenfield | in-progress | mature | targeted
- **Stack:** <runtime, framework, package/build tool>
- **Entry:** <entry points and direct callers>
- **Primary risk:** <highest plausible failure>

## Milestones

- [ ] **M1 - <outcome>**
  - Proof: `<command>` or <observed signal>
- [ ] **M2 - <outcome>**
  - Proof: `<command>` or <observed signal>

## Active State

- **Current:** <one active milestone or action>
- **Invariant:** <must remain true>
- **Decision:** <chosen approach and binding reason>
- **Last signal:** <latest useful evidence>
- **Next:** <one concrete action>
- **Verify:** `<next command>` or <next observation>
- **Blocker:** none | <exact missing input or state>
- **Risk:** <highest remaining risk>
```

## Depth

| Work | Keep |
| --- | --- |
| Targeted change | contract, one invariant, one milestone, narrow proof |
| Multi-file feature | affected boundaries, ordered milestones, regression proof |
| Greenfield | product contract, stack rationale, walking skeleton, runnable slices, release proof |
| High-risk change | authorization state, rollback, data/contract compatibility, staged proof |

## Completion Gate

Set `Status: done` only when every required milestone has its stated proof, the worktree has been checked for unintended changes, and remaining risks are disclosed. Delete only the task-owned ledger after the handoff is ready. Keep it when interrupted or genuinely blocked.
