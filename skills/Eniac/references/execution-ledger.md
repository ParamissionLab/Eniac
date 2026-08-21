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

## Lifecycle

1. Before the first L2-L4 mutation, choose the exact plan path and unique
   `Owner`, record both in private task state, and write the current contract and
   first active milestone.
2. Default to `.eniac-plan.md` in the workspace root. If that file exists and is
   not clearly owned by the task, use `.eniac-plan-2.md`, then increment only the
   numeric suffix. The filename must start with `.eniac-plan` and end with `.md`;
   do not invent descriptive suffixes.
3. Keep milestone checkboxes and `Active State` synchronized with observed work.
   Mark the active item before starting and complete it immediately after its
   proof. Reweight the next action after material evidence.
4. When the user adds or changes a request, reconcile `Goal`, `Done when`,
   `Scope`, `Preserve`, `Exclude`, milestones, and active state before the next
   mutation. The newest instruction controls conflicts; do not undo completed
   work unless requested.
5. Re-read the plan after context loss, interruption, or before a new milestone,
   then confirm repository state still matches it. A delegate may read relevant
   context but may not finalize the primary task's plan.
6. Keep an unproven hypothesis, containment, deferred coverage row, or missing
   authority visible. Do not convert it into a completion claim.

Before the final response, set `Status: done` only after every required proof
passes. Unless `Retention` is explicitly `retain-by-explicit-request`, use
delete-on-complete. When available, invoke `scripts/finalize_plan.py` with the
exact plan path, explicit `--workspace-root`, and matching `--owner`; pass
`--retain` only with explicit authorization. Verify the exact path is absent.
If finalization fails, set `Status: blocked`, preserve the plan, and report its
path and failure instead of claiming completion.

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
