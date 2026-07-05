# Safety and Delivery Reference

Use for L4 work or whenever a change can affect credentials, production, external systems, dependencies, public contracts, persisted data, generated artifacts, or irreversible state.

## Authority Gate

Classify the next action before execution:

| Action | Default | Gate |
| --- | --- | --- |
| Read local state | proceed | stay in scope; avoid exposing secrets |
| Reversible local edit | proceed when requested | preserve unrelated work; keep rollback boundary |
| Install or upgrade dependency | inspect first | require concrete need; report lockfile and compatibility impact |
| Stage, commit, push, publish, deploy | do only when requested or explicitly part of the workflow | confirm target, branch/environment, and included changes |
| Use credentials or contact an external service | minimize | confirm authorization and redact sensitive values |
| Delete, migrate, overwrite, rotate, or spend | pause | require explicit scope and a tested recovery path when possible |

Do not infer authority for a materially different action from permission to perform a nearby one.

## Change Boundary

Before a risky mutation, record:

```text
Target:
Authorized effect:
Unrelated state to preserve:
Expected signal:
Rollback or recovery:
Abort condition:
```

Use exact paths, environments, accounts, branches, and resource identifiers. Resolve computed destructive targets before acting. Prefer dry runs and previews when supported.

## Sensitive Data

- Read only the secret names or handles required to complete the task.
- Do not echo secret values, copy them into plan files, commit them, or include them in reports.
- Redact tokens, passwords, private keys, cookies, personal data, and signed URLs from logs or examples.
- Stop and report the location, not the value, when a secret is accidentally tracked or exposed.
- Do not rotate or revoke credentials unless explicitly authorized; containment can disrupt production.

## Risky Change Classes

### Dependencies

Use the existing package manager and lockfile. Explain why the dependency is needed, check runtime/toolchain compatibility, inspect transitive or licensing risk when material, and run the affected build/tests. Do not upgrade unrelated packages.

### Public Contracts

Map callers and consumers before changing APIs, schemas, CLI flags, events, URLs, configuration keys, or serialized data. Prefer additive compatibility. Name intentional breaking changes and migration steps.

### Persisted Data and Migrations

Check forward compatibility, rollback feasibility, idempotency, ordering, backups, partial-failure behavior, and old/new application coexistence. Never test destructive migrations against production data by default.

### Infrastructure and External Systems

Identify environment and blast radius. Preview changes, use least privilege, avoid embedding credentials, and verify health plus rollback. Do not assume local success proves production safety.

### Generated Artifacts

Edit the source of truth, then regenerate with project tooling. Inspect generated diffs for unexpected churn. Do not hand-edit generated output unless the repository explicitly requires it.

## Verification Ladder

Choose the lowest-cost set that proves the requested outcome and covers material risk:

1. Static signal: parse, schema, lint, type, or focused inspection.
2. Focused behavior: exact unit test, reproduction, or touched command.
3. Direct regression: nearby tests, callers, integration boundary, or rendered state.
4. Build/package: production build, artifact validation, or clean import/start.
5. End-to-end: representative user or system flow.
6. Operational: deployment health, logs, metrics, rollback, or data integrity.

Escalate upward only when a lower layer cannot prove the relevant risk. For read-only review, evidence and traceable reasoning may be the verification.

## Baseline and Regression

- Capture a baseline before mutation when checks are cheap or failures already exist.
- After mutation, run the same focused signal so results are comparable.
- Classify failures as introduced, pre-existing, environmental, flaky, or unverified.
- Do not claim a regression is fixed when the proving check did not run.
- Do not absorb unrelated baseline failures into scope unless they block the requested outcome.

## Completion Gate

Call work complete only when requested behavior exists, relevant verification passed, risky side effects were checked, documentation/contracts are accurate, and residual risks are stated. Use `partial` or `blocked` when any required outcome remains. Never convert an unrun check into an implied pass.

Before final handoff, confirm the diff/changed-state boundary, remove task-owned temporary artifacts, and delete the disposable plan only after its completion gate succeeds.
