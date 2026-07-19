# Algorithm Workflow Reference

Use for L2+ implementation, debugging, review, batch work, or complex planning when coverage, cause, prioritization, and documentation must remain reliable across loops. Use it with `workstream-orchestration.md` for L3 parallel/dependency work and with `architecture-evidence.md` when an existing-system boundary is involved.

Do not add this ceremony to an L0-L1 answer unless a concrete failure risk requires it.

## Contents

- [Core algorithm](#core-algorithm)
- [Weight the work](#weight-the-work)
- [Diagnose causes, not only symptoms](#diagnose-causes-not-only-symptoms)
- [Coverage matrix](#coverage-matrix)
- [Documentation and context per loop](#documentation-and-context-per-loop)
- [Closure gate](#closure-gate)

## Core Algorithm

Run this at the level of the current task, workstream, or defect. Repeat only the steps whose inputs changed:

```text
1. Frame       -> goal, scope, authority, invariant, done criteria
2. Weight      -> choose the next work by impact, urgency, dependency, uncertainty, and reversibility
3. Map         -> affected flow, contracts, callers, state, and verification surface
4. Diagnose    -> separate symptom, immediate cause, contributors, and root cause
5. Contain     -> apply a reversible safety measure when needed; label it as containment
6. Change      -> make the smallest correction that addresses the deepest in-scope cause
7. Prove       -> run the planned focused and integrated signals; check coverage gaps
8. Contextualize -> update decision-relevant plan state and documentation impact
9. Decide      -> close, continue, re-plan, or escalate
```

Containment may happen before diagnosis for a live safety, security, data-loss, or customer-impacting incident. It never substitutes for diagnosis: do not call a defect resolved until the causal claim is proven or explicitly labeled `Unverified` with a follow-up owner.

## Weight The Work

Score each candidate action from `0` to `3` for the dimensions that apply:

| Dimension | 0 | 3 |
| --- | --- | --- |
| Impact | cosmetic/local | correctness, data, security, or major user flow |
| Urgency | no time sensitivity | active incident, release blocker, or irreversible window |
| Dependency leverage | unlocks nothing | unlocks several blocked workstreams or a critical path |
| Uncertainty | direct proof available | core premise unverified |
| Irreversibility | easy local revert | public contract, data, production, or external effect |
| Verification gap | focused proof exists | no meaningful proof yet |

Use the profile, not false numeric precision:

- High impact/urgency: contain safely, then diagnose and prove before broad rollout.
- High dependency leverage: prioritize a design or contract gate that unblocks reliable parallel work.
- High uncertainty or verification gap: inspect or experiment before implementation.
- High irreversibility: require authorization, rollback, and staged proof.
- Low values across the profile: use the Lean direct path.

Record the chosen action, the strongest factors, the expected signal, and the stop condition. Reweight after every material signal rather than following a stale priority order.

## Diagnose Causes, Not Only Symptoms

For every defect, unexpected test result, regression, or repeated manual workaround, create a compact causal record before final closure:

```text
Symptom: <observable failure>
Scope: <affected user, flow, contract, or environment>
Immediate cause: <direct trigger, with evidence>
Contributors: <conditions that allowed it>
Root cause: <system condition that made recurrence likely>
Containment: none | <temporary protection>
Correction: <smallest in-scope fix>
Prevention/proof: <test, guard, monitor, contract, or documented limitation>
Confidence: Direct | Inferred | Unverified
```

Use a hypothesis tree when the cause is not direct. Pick the cheapest discriminating check first; rule in or out a branch with evidence. Do not repeat variants of the same guess. When the root cause lies outside authorized scope, fix only safe containment, preserve the evidence, and hand off the systemic correction.

## Coverage Matrix

Coverage means every decision-relevant surface is either proved, explicitly deferred, or shown not to apply. It is broader than a code-coverage percentage.

| Surface | Ask | Minimum record |
| --- | --- | --- |
| Requirement | Which requested outcomes exist? | done criterion and status |
| Main flow | Can the intended user/system path complete? | focused behavior proof |
| Edge/failure | What invalid, empty, retry, concurrency, or error path matters? | case or explicit non-applicability |
| Contract/data | Which API, schema, event, config, or compatibility promises move? | consumer/migration proof |
| Dependency | Which callers, downstream consumers, or workstreams are affected? | impact map or safe boundary |
| Operations | What security, rollout, observability, or rollback concern applies? | gate, owner, or non-applicability |
| Documentation | Did behavior, usage, contract, decision, risk, or handoff context change? | updated artifact or `Doc impact: none` |

For L0-L1, collapse the matrix to the applicable main flow, failure risk, and documentation impact. For L3, keep the relevant matrix rows in the execution context and do not mark the workstream accepted until its planned rows are addressed.

## Documentation And Context Per Loop

At every `Observe` step, assess documentation impact before choosing the next action:

```text
Observed signal changed a fact, decision, contract, risk, workflow, or handoff?
  Yes -> update the affected plan/context section and the smallest durable project doc that users or future agents rely on.
  No  -> record `Doc impact: none` only when the task is L2+ or the absence matters; do not create churn.
```

Update the execution context in place after each material loop: current workstream/wave, accepted proof, changed path, causal record, next action, risk/blocker, and documentation impact. Keep durable documents accurate when behavior, configuration, public contract, operation, architecture decision, or handoff guidance changes. Do not update docs merely to narrate activity.

## Closure Gate

Close a task or workstream only when:

- the requested outcome and applicable coverage rows have evidence;
- the cause is addressed or its uncertainty/owner is explicit;
- containment is not mislabeled as a permanent fix;
- required documentation/context is updated or intentionally not applicable;
- the next safe action, residual risk, and rollback state are clear.

If any condition fails, continue, re-plan, or escalate. Never convert an unverified root-cause hypothesis into a confident completion claim.
