# Greenfield Launch Sequence

Use only for a genuinely new project, service, package, application, or substantial standalone module. Turn an idea into the smallest production-shaped system that can be run, tested, understood, and extended.

## Contents

- [Operating rules](#operating-rules)
- [Launch stages](#launch-stages)
- [Product contract](#product-contract)
- [Stack decision](#stack-decision)
- [Foundation gate](#foundation-gate)
- [Walking skeleton](#walking-skeleton)
- [Capability slices](#capability-slices)
- [Release proof](#release-proof)

## Operating Rules

- Confirm the target is greenfield; an empty-looking subdirectory may belong to an existing workspace or monorepo.
- Resolve only decisions that affect architecture, irreversible cost, public contracts, security, or user experience before building.
- Choose conservative defaults for reversible details and record them in the execution ledger.
- Build a walking skeleton through the real entry point before filling horizontal layers.
- End every stage with evidence. A directory full of generated files is not a working project.
- Do not require plan approval unless the user requests it or a high-impact ambiguity cannot be reversed safely.

## Launch Stages

| Stage | Produce | Gate |
| --- | --- | --- |
| 0. Ground truth | workspace and constraint inventory | target path and ownership are safe |
| 1. Product contract | user, job, primary flow, acceptance, non-goals | one testable outcome is explicit |
| 2. Stack decision | runtime, framework, storage, delivery rationale | every major choice serves a constraint |
| 3. Foundation | native scaffold, structure, scripts, config boundaries | install and minimal run succeed |
| 4. Walking skeleton | thinnest real end-to-end path | primary path crosses real boundaries |
| 5. Capability slices | behavior in dependency order | each slice has acceptance proof |
| 6. Hardening | failure states, security, tests, operability | highest-risk failure is covered |
| 7. Release proof | clean-start, checks, docs, worktree review | another operator can run and verify it |

Do not advance a failed gate by adding more code. Fix the foundation or revise the decision that caused it.

## Product Contract

Capture this before selecting a stack:

```text
Primary user:
Job to be done:
Primary flow:
Inputs and outputs:
Must-have behavior:
Quality constraints:
Acceptance signal:
Non-goals:
Unknowns that can change architecture:
```

Keep the first release narrow. Separate required behavior from plausible future features; future possibilities do not justify present abstractions.

## Stack Decision

Inspect local tool availability and user constraints first. Prefer the smallest established stack that supports the acceptance signal.

| Decision | Evaluate |
| --- | --- |
| Runtime/framework | team familiarity, target platform, ecosystem maturity, startup/build cost |
| Data/storage | consistency, query shape, volume, portability, migration and backup needs |
| Interface | actual client workflow, accessibility, latency, offline or realtime needs |
| Delivery | supported host/runtime, secrets, observability, rollback, operating cost |
| Testing | behavior risk, boundary coverage, execution speed, deterministic isolation |

Reuse one coherent toolchain. Do not add frameworks, state layers, service boundaries, queues, caches, or databases for hypothetical scale. Record the chosen option, rejected serious alternative, reason, and reversal cost when the choice constrains future work.

## Foundation Gate

Create only what makes the first slice repeatable:

- repository-native manifest and lockfile
- explicit runtime version when the ecosystem supports it
- deterministic install plus `dev`/`run`, `test`, and `build` or equivalent scripts
- source and test boundaries that match the product shape
- validated configuration with `.env.example` names but no secret values
- `.gitignore` for secrets, dependencies, caches, and generated output
- minimal error boundary and logging path appropriate to the runtime

Use official or already-installed scaffolding when it reduces configuration risk. Inspect generated output, remove unused sample code, and avoid retaining dependencies the first slice does not need.

## Walking Skeleton

Implement one production-shaped vertical slice through the real path:

```text
User or caller -> entry point -> domain behavior -> external boundary -> visible result
```

Use a real boundary where practical, or a contract-faithful substitute when credentials or infrastructure are unavailable. Include one success case and the most important failure case. Prove the application starts and the slice works before expanding features.

For user interfaces, load `product-ux.md` and establish the actual primary screen, responsive constraints, loading/empty/error states, keyboard path, and visual evidence. Do not substitute a marketing page for the requested product experience.

## Capability Slices

Order remaining work by dependency and user value. For each slice:

```text
Behavior:
Contract:
Failure mode:
Files/boundaries:
Acceptance proof:
Regression proof:
```

Keep the system runnable after every slice. Add abstractions only after a stable boundary or meaningful duplication appears.

## Release Proof

- Recreate or approximate a clean checkout without destroying user state.
- Run deterministic install, focused tests, full relevant tests, static checks, and production build.
- Exercise the primary flow and highest-risk failure path through the real entry point.
- Verify configuration failure is actionable and secrets are absent from source, logs, and examples.
- Load `project-interface-contract.md` and document only observed setup, run, test, build, and configuration behavior.
- Load `delivery-proof-pipelines.md` only when CI is requested or required by the delivery contract.
- Inspect the final file inventory and diff for generated debris, placeholders, debug output, dead sample code, and unrelated files.

Declare completion only when the acceptance signal is observed. Otherwise ship a runnable partial state with the exact missing proof and next command.
