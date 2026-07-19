# Workstream Orchestration Reference

Use for L3+ work with several difficult, interacting outcomes: multiple modules or layers, a broad feature, a migration, a hard incident, a multi-step audit, or a task that can benefit from parallel effort. Use it for one primary agent coordinating multiple workers or for one agent executing the same workflow sequentially.

Do not load for a small edit. Parallelism is optional; a correct sequential workflow beats concurrent conflicting work.

When the work changes an existing-system boundary, data flow, shared contract, security posture, deployment path, or several interacting modules, load `architecture-evidence.md` first to establish the evidence and impact map that this workflow will execute. For L2+ loops, load `algorithm-workflow.md` so each workstream reweights work, preserves causal/coverage status, and records documentation impact.

## Contents

- [Operating model](#operating-model)
- [Select a workflow](#select-a-workflow)
- [Build the dependency map](#build-the-dependency-map)
- [Workstream card](#workstream-card)
- [Gates and waves](#gates-and-waves)
- [Durable execution context](#durable-execution-context)
- [Failure and conflict protocol](#failure-and-conflict-protocol)
- [Handoff](#handoff)

## Operating Model

Treat the work as a dependency graph, not a flat checklist:

```text
Context -> Design gates -> independent workstreams -> integration -> proof -> handoff
```

Each workstream owns one verifiable outcome. It declares its inputs, output contract, allowed change surface, dependencies, proof, and rollback. The primary agent owns the execution-context plan, cross-workstream decisions, integration, broad verification, and final handoff.

Never give two workers authority over the same file, unresolved interface, shared mutable state, migration, deployment, or release decision. Solve the shared contract first, then split downstream work.

## Select A Workflow

| Workflow | Use when | Shape |
| --- | --- | --- |
| Sequential | one path, shared files, or unresolved design | inspect -> change -> verify |
| Parallel lanes | independent surfaces with stable contracts | design gate -> concurrent lanes -> integration |
| Dependency waves | some work unlocks later work | wave 0 contract -> wave 1 lanes -> wave 2 consumers -> proof |
| Pipeline | repeated units share a safe rule | sample -> batch -> exceptions -> broad check |
| Recovery | verification fails, scope drifts, or assumptions break | freeze -> classify -> repair or re-plan -> re-verify |

Choose the smallest workflow that lowers total risk or elapsed time. State the choice, why concurrency is safe or unsafe, and the integration proof before starting.

## Build The Dependency Map

Before assigning workstreams, create a compact map:

```text
Outcome:
Invariant:
Shared contracts:
Integration owner:
Final proof:

W0 - <design/contract gate>
  Needs: <evidence or decision>
  Produces: <approved interface, migration shape, or test contract>
  Unlocks: W1, W2

W1 - <independent outcome>
  Needs: W0
  Owns: <files/modules>
  Produces: <artifact/behavior>
  Proof: <focused signal>

W2 - <independent outcome>
  Needs: W0
  Owns: <different files/modules>
  Produces: <artifact/behavior>
  Proof: <focused signal>

I1 - <integration>
  Needs: W1, W2
  Proof: <consumer, integration, or end-to-end signal>
```

Dependencies are real only when a workstream needs an unfinished artifact, decision, shared state, contract, or change surface from another. Do not add ceremonial dependencies. Mark an unresolved dependency as a blocker, not as a hidden assumption.

## Workstream Card

Give every active workstream this contract. Keep it in the execution-context plan; give a worker only its own card plus the minimum relevant context.

```text
ID and outcome:
Owner:
Mode: inspect | implement | test | review | document
Needs: <completed workstreams, inputs, decisions>
May change: <explicit paths or systems>
Must not change: <shared/user-owned paths and contracts>
Input contract: <facts, types, APIs, invariants>
Output contract: <observable artifact or behavior>
Acceptance proof: <command, test, review signal, or artifact check>
Rollback: <reversible action or escalation point>
Status: queued | active | blocked | ready-for-integration | accepted
```

A worker may inspect broadly only enough to meet its card; it must not silently expand its change surface. It reports the changed paths, observed proof, assumptions, conflicts, residual risks, applicable coverage rows, causal record for defects, and documentation impact. A workstream is `accepted` only after the primary agent checks its output contract, scope, coverage, documentation/context state, and integration effect.

## Gates And Waves

Use these gates in order. Skip only a gate whose purpose is already satisfied by direct evidence.

1. **Intake gate:** goal, done criteria, scope, authority, and workflow are recorded.
2. **Context gate:** project facts, important paths, contracts, constraints, open questions, and risks are current enough for the next wave.
3. **Design gate:** shared interfaces, ownership, migration shape, and invariants are resolved or explicitly blocked. Do not start dependent work before this gate.
4. **Dispatch gate:** each parallel card has disjoint mutable scope and a focused acceptance proof.
5. **Integration gate:** all prerequisite cards are accepted; reconcile contracts and run the first cross-boundary signal before starting unrelated polish.
6. **Completion gate:** final proof, scope check, coverage, causal status, documentation/context impact, residual risk, rollback state, and handoff are recorded.

For a dependency wave, update the context plan after each gate. If a wave changes a shared contract, invalidate dependent cards and re-plan them before dispatch.

## Durable Execution Context

For L3, multi-workstream, interrupted, or handoff-heavy work, the task-owned `.eniac-plan.md` is a durable execution context during execution, not a disposable TODO list. Record its owner and exact path before dispatching work. Keep it compact, but preserve the facts a new session needs to act safely:

```markdown
## System Context

- **System state:** <greenfield | in-progress | mature | targeted>
- **Important paths:** <entry points, contracts, tests, config>
- **Confirmed facts:** <decision-relevant evidence>
- **Inferences and assumptions:** <labeled; verification path>
- **Constraints and invariants:** <must remain true>
- **Open questions and risks:** <owner or next check>

## Workflow

- **Workflow:** <sequential | parallel lanes | dependency waves | pipeline | recovery>
- **Integration owner:** <primary agent or named role>
- **Final proof:** <required integrated signal>
- **Current wave:** <identifier and exit condition>

## Workstreams

| ID | Outcome | Needs | Mutable scope | Proof | Status |
| --- | --- | --- | --- | --- | --- |
| W0 | <contract> | none | <paths> | <signal> | complete |

## Evidence And Decisions

- **E1:** <fact/signal and source>
- **D1:** <binding decision, reason, reversal or review trigger>

## Coverage And Cause

- **Coverage gap:** none | <surface and next proof>
- **Causal record:** not applicable | <symptom -> immediate cause -> root cause -> proof>
- **Doc impact:** none | <artifact and update>

## Resume State

- **Last integrated signal:** <observed result>
- **Next safe action:** <one action>
- **Blocked by:** none | <exact missing state>
- **Do not do yet:** <unsafe action until a gate passes>
```

Update `Resume State` in place. After every material gate, reweight queued work and update applicable coverage, causal, and documentation state. Add evidence or decisions only when they constrain later work; replace stale items and explicitly mark a superseded decision. Never append activity logs, raw tool output, secrets, or hidden reasoning.

For L2, use the smaller plan shape unless the task develops a future-handoff or multi-workstream need. On completion, delete the task-owned plan by default at every level using its exact path, workspace root, and owner. Retain a completed plan with `Status: done` only when the user explicitly requested retention or an active repository policy requires it; report its path. Never infer retention from complexity or handoff value, and never overwrite or finalize a plan you do not own.

On resume, read the context plan once, inspect the worktree and the stated proof sources, invalidate stale claims, and continue from the first incomplete or unaccepted gate. Current files and direct signals always outrank the plan.

## Failure And Conflict Protocol

Freeze the affected workstream when a proof fails, a worker conflicts with scope, or a shared contract changes. Do not let other dependent work continue on stale assumptions.

```text
Failure:
Expected signal:
Observed signal:
Classification: implementation | contract | assumption | environment | baseline
Containment: <which cards/wave are paused>
Next discriminating check:
Decision: repair | re-plan | escalate
```

Repair a local defect in the same card. Re-plan when the change crosses the card boundary, invalidates a contract, or changes the impact radius. Escalate when a high-impact decision needs owner approval. Do not merge several uncertain outputs and debug the combined system blindly.

## Handoff

Record the completed and accepted workstreams, pending/blocked cards, final proof, key paths, confirmed facts, assumptions, decisions, risks, rollback state, and the next safe action. State which gates passed and which were intentionally not run.
