# Execution Ledger

Use for greenfield, broad, or L2-L4 implementation work that needs restartable state. For L3, multi-workstream, interrupted, or handoff-heavy work, the ledger is also a durable execution context during execution, not a narrative plan.

## Ledger Rules

- Record only facts and decisions that constrain the next action.
- Tie every milestone to an observable proof signal.
- Replace current state instead of appending progress logs.
- Separate requested scope, preserved contracts, and explicit non-goals.
- Keep one semantic item per line; never compress milestones or checks into semicolon-separated text.
- Wrap long values as indented continuation lines so labels and checklist markers remain scannable.
- Record a blocker only after evidence rules out the next safe action.
- Never store secrets, full logs, hidden reasoning, or copied source files.
- For durable context, retain only reusable system facts, key paths, contracts, decisions, proof signals, and safe resume state. Current files and direct checks outrank the ledger.

## Shape

```markdown
# Eniac Execution: <short outcome>

> Owner: <task id or short label>
> Status: active | blocked | done
> Retention: delete-on-complete | retain-by-explicit-request

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

## Workflow

- **Workflow:** sequential | parallel lanes | dependency waves | pipeline | recovery
- **Integration owner:** <primary agent or role>
- **Final proof:** `<command>` or <integrated signal>
- **Current wave:** <identifier and exit condition>

## Workstreams

| ID | Outcome | Needs | Mutable scope | Proof | Status |
| --- | --- | --- | --- | --- |
| W0 | <contract or outcome> | none | <paths> | <signal> | queued |

## Evidence And Decisions

- **E1:** <fact/signal and source>
- **D1:** <binding decision, reason, review trigger>

## Coverage And Cause

- **Coverage gap:** none | <surface and next proof>
- **Causal record:** not applicable | <symptom -> immediate cause -> root cause -> proof>
- **Doc impact:** none | <artifact and update>

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
| Complex multi-workstream | dependency map, owned mutable scope, integration owner, accepted workstreams, coverage/cause/doc state, integrated proof |
| Greenfield | product contract, stack rationale, walking skeleton, runnable slices, release proof |
| High-risk change | authorization state, rollback, data/contract compatibility, staged proof |

## Completion Gate

Set `Status: done` only when every required milestone has its stated proof, the worktree has been checked for unintended changes, and remaining risks are disclosed. Delete the exact task-owned ledger by default at every level, then verify the path is absent. When the skill-local finalizer is available, pass the explicit workspace root and matching ledger owner to it. Retain it only when the user explicitly requested retention or an active repository policy requires it; report its path. If deletion fails, mark the task blocked and report the exact path and reason. Keep it when interrupted or genuinely blocked.
