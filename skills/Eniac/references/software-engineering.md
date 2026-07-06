# Software Engineering Reference

Use when creating, reading, modifying, testing, reviewing, documenting, or shipping code.

## Contents

- [Full-cycle and mode](#full-cycle-shape)
- [Task playbook](#playbook)
- [Discovery and planning](#discovery)
- [Build and batch edits](#build)
- [Test, bug hunt, and polish](#test)
- [Documentation and shipping](#docs-and-ship)
- [Failure recovery](#failure-recovery)

## Full-Cycle Shape

Own the path to a verified handoff:

```text
Discover -> Plan -> Build -> Test -> Bug hunt -> Polish -> Document -> Ship
```

Use every phase for greenfield or broad work. For targeted work, abbreviate the phases but do not edit existing code blind.

Announce only phase changes that help the user track risk or progress. Close a phase with its concrete signal, for example: `Test complete — 31 passing, 0 failing`.

## Engineering Contract

Treat code work as engineering delivery, not text editing:

- Own the requested outcome from discovery through verification and handoff.
- Determine project state first: greenfield, in-progress, mature, targeted, review-only, or explain-only.
- In existing projects, read the relevant code, tests, configs, and nearby patterns before changing anything.
- Build on what exists: same framework, package manager, test style, architecture, naming, errors, and docs style.
- Keep the change scoped, but do not stop after writing code if tests, lint, type checks, docs, or a smoke path are needed to prove the result.
- Prefer small, reviewable patches with clear contracts over broad rewrites.
- Report broader problems as risks unless they block the requested outcome.
- Ship only when the requested behavior exists and the best relevant verification has run or a blocker is named.

## Mode

| Signal | Mode | Entry | Proof |
| --- | --- | --- | --- |
| Empty/new project | Greenfield | product contract, stack decision, walking skeleton | acceptance flow runs |
| Existing source, weak tests/docs | In-progress | audit requested area | focused checks pass |
| Stable tests/docs/CI | Mature | abbreviated audit | regression signal passes |
| Bug, review, refactor, small feature | Targeted | relevant files/callers | failing case or flow works |
| User asks "review" | Review-only | findings first | file/line evidence |
| User asks only a question | Explain-only | inspect as needed | no edits unless asked |

## Playbook

| Task | First action | Main risk | Proof |
| --- | --- | --- | --- |
| Bug fix | reproduce or inspect failing path | symptom patch | failing case passes |
| Feature | find local analogs | pattern drift | behavior test/manual flow |
| Refactor | list preserved contracts | behavior drift | tests or equivalence |
| Build failure | capture first meaningful error | chasing noise | build reaches next state |
| Review | inspect diff and direct callers | missed regression | severity + evidence |
| Many small edits | define one repeated rule | partial inconsistency | sample diff + broad check |
| UI/frontend | inspect design system and states | pretty but unusable | affected flow renders/works |

Report broader problems as risks unless they block the requested outcome.

## Project State Detection

Start every code task by classifying the repository:

```text
State:
Stack:
Entry points:
Package manager/build tool:
Tests:
Tooling:
Docs:
Git state:
Immediate scope:
```

Use the classification to choose entry point:

- Greenfield: load `greenfield-launch-sequence.md`; establish the product contract before stack selection, then build and prove a production-shaped walking skeleton before expanding capability slices.
- In-progress: audit structure, manifests, direct modules, tests/tooling, then implement against existing patterns.
- Mature: identify the narrow touched surface, capture baseline when cheap, preserve public contracts, run regression signal.
- Targeted: inspect exact file/symbol, local analogs, direct callers, and relevant tests; skip broad audit unless evidence requires it.
- Review-only: do not edit; findings first with file/line evidence, severity, user impact, and test gaps.
- Explain-only: inspect enough to answer; do not mutate.

## Discovery

Inspect only what can affect the change:

```text
Structure:
Stack/manifests:
Local instructions:
Tests/tooling:
Conventions:
Relevant files/callers:
Git state:
Risk:
Verify:
```

Prefer `rg --files`, manifests, scripts, configs, tests, nearby examples, and call sites before whole-file or whole-repo reads. For tiny fixes, compress discovery to exact file, pattern, command, and risk.

For L2+ existing-code work, publish this compact audit before mutation:

```text
Stack:
Relevant surface:
Tests/tooling:
Conventions:
Risk:
Verification:
Open question: (only if blocking or high-impact)
```

Use `commands-by-stack.md` when concrete discovery commands will reduce uncertainty. Run only the sections that can affect the next decision; do not execute a full audit mechanically.

## Codebase Reading Depth

Choose the reading depth deliberately:

| Depth | Use | Required signal |
| --- | --- | --- |
| Targeted | exact bug/file/symbol known | requested path, local analogs, direct callers |
| Surface audit | unfamiliar existing project or multi-file change | inventory, manifests, tests/tooling, relevant modules |
| Deep code audit | architecture, broad refactor, repeated failure, security-sensitive change, or user asks to read all code/repo | full source inventory, module map, entry points, data/control flow, tests/tooling, risks |

For a Deep code audit:

1. Build a complete inventory before reading content. Include tracked and untracked files. Include ignored workspace files only when they are project artifacts or the user asked for all repo/code; still exclude `.git`, dependencies, caches, build outputs, binaries, minified bundles, lockfile blobs unless dependency state matters, and likely secret files.
2. Classify files by role: app source, tests, config/tooling, docs, generated/output, demos/examples, assets, scripts, data, unknown.
3. Read all human-authored source and test files that are small enough to fit safely. For large files, first read headings, symbols, imports/exports, and key ranges; then read the full file only if it can affect the implementation, review, or architecture answer.
4. Map entry points, shared types/contracts, state owners, side effects, external boundaries, and direct callers before editing.
5. Report any skipped file class explicitly with reason, for example binary asset, dependency cache, generated bundle, or possible secret.
6. Convert the audit into action: exact files to touch, behavior to preserve, tests to run, and risks. Do not keep auditing after the next decision is clear unless the user asked for a complete read report.

Deep code audit output:

```text
Inventory:
Stack:
Entry points:
Source map:
Tests/tooling:
Conventions:
Invariants/contracts:
Risks:
Skipped:
Next edit/verify:
```

When the user explicitly says "read all code", "อ่านโค้ดทั้งหมด", "whole repo", or equivalent, do not stop at manifests or snippets. Read every relevant human-authored source file or state precisely why a file was not read.

## Plan

Keep plans proportional:

| Size | Plan | Avoid |
| --- | --- | --- |
| Tiny | exact edit + narrow check | repo audit |
| Small | local analogs + direct caller | new abstraction |
| Medium | affected files + interfaces + tests | unrelated modules |
| Large | milestones with verification | one giant patch |
| Unclear | reproduce/logs/hypothesis | guessing first |

For code changes, set a private boundary:

```text
Change:
Read only:
Preserve:
Not changing:
Verification:
Rollback:
```

For L2-L4 mutation work, persist this boundary and milestone checklist in the disposable plan file defined in `SKILL.md`. Update the file in place as state changes; do not turn chat or the file into an execution diary.

Load `execution-ledger.md` when creating durable, restartable state for greenfield, broad, or multi-milestone software delivery. Tie each milestone to an observed proof signal.

For software delivery, the plan must name:

```text
Reuse:
Create/change:
Preserve:
Contracts:
Tests:
Static checks:
Docs:
Ship signal:
```

Ask only when a high-impact product, API, data, dependency, security, or deployment choice cannot be verified locally. Otherwise make a conservative choice that matches the repo.

## Build

- Match local architecture, style, names, imports, errors, and tests.
- Read nearby examples before adding a pattern.
- Validate external inputs and handle errors with actionable messages.
- Keep changes scoped to the request and touched files.
- Avoid new frameworks, formatters, runners, state managers, or dependencies without concrete need.
- Preserve public interfaces and serialized shapes unless explicitly changed.
- For greenfield work, follow `greenfield-launch-sequence.md`; keep the system runnable after every vertical slice and prove the acceptance flow through the real entry point.

Production code bar:

- Names reveal intent; avoid vague names, magic values, and hidden global coupling.
- Functions and modules do one coherent job; extract only when it removes real duplication or complexity.
- Error paths are handled deliberately; user-facing errors are actionable and internal errors preserve debugging context.
- External input is validated at boundaries; data contracts are explicit.
- Async, concurrency, lifecycle, cancellation, and cleanup paths are handled where the stack requires them.
- No hardcoded secrets, debug prints, commented-out dead code, or unrequested dependency churn.
- Public APIs, schemas, events, config keys, CLI flags, URLs, and persisted shapes remain compatible unless the user requested a breaking change.
- New code has tests when behavior, contracts, or regression risk justify them.

Load `stack-risk-matrix.md` when stack-specific behavior can affect correctness. Select only the detected runtime and touched boundary; convert the highest relevant failure mode into an invariant and proof.

## Batch Edits

For many small edits:

```text
Goal:
Pattern:
Rule:
Include:
Exclude:
Exceptions:
Verify:
```

Use structured tooling when the rule is exact: formatter, codemod, parser, project script, or reviewed search/replace. Edit one sample, inspect the diff, apply the group, handle exceptions, then run a broad check. Re-plan when matches need unique judgment.

## Test

- Use the existing framework and project scripts.
- Run the narrowest useful check first, then broaden if risk justifies it.
- Capture a comparable baseline first when the suite is cheap, the repository is already failing, or attribution would otherwise be ambiguous.
- Test behavior, not implementation details.
- Cover happy, boundary, and meaningful failure cases when risk justifies it.
- Keep tests isolated; avoid shared mutable state.
- Report pre-existing failures separately.
- Do not delete, skip, or weaken failing tests to pass.
- Add tests in the same framework/style as existing tests; do not introduce a new test runner without concrete need.

Common signals: `package.json`, `pyproject.toml`, `go test ./...`, `cargo test`, `dotnet test`, `mvn test`, `gradle test`, `bundle exec rspec`.

Use the project-native scripts first. If the repository does not expose the needed command, select a compatible command from `commands-by-stack.md`. Report the observed counts when available: `X passing, Y failing, Z% coverage`.

Use the verification ladder in `safety-and-delivery.md` for public contracts, dependencies, data, infrastructure, generated files, external effects, or any L4 task.

For UI/frontend changes, use `references/product-ux.md` when layout, visual hierarchy, controls, responsive behavior, or primary flow changed.

## Bug Hunt

Check changed files and direct dependencies for:

- invalid or untrusted inputs
- swallowed errors or unhandled async paths
- secrets, debug logs, or accidental telemetry
- lifecycle, cancellation, race, or cleanup issues
- hot-loop cost, N+1 queries, or avoidable broad work
- null, empty, duplicate, large, unicode, timezone, and locale cases
- compatibility drift in public APIs, schemas, URLs, events, or persisted data
- UI state regressions: loading, empty, error, disabled, focus, selected, hover

For review-only work, make findings only with concrete evidence and user impact.

Bug report shape when issues are found during delivery:

```text
Severity:
Location:
Problem:
Impact:
Fix or decision:
Verification:
```

## Polish

- Run configured formatter/linter/type/build checks relevant to touched files.
- Use `commands-by-stack.md` only after checking the repository's existing config and scripts.
- Remove unused imports, dead code introduced by the change, commented-out code, and debug prints.
- Update generated files only when they are source-controlled outputs for touched inputs.
- Do not add global formatting churn unless requested.
- Keep formatting diffs narrow. If a tool rewrites unrelated files, stop, inspect, and avoid absorbing the churn unless the user asked for it.

## Docs And Ship

Update docs only where behavior or usage changed. Do not write broad tutorials unless requested.

Load `project-interface-contract.md` when creating a new README or doing a major README rewrite. Load `delivery-proof-pipelines.md` only when adding, repairing, or reviewing CI.

Before handoff:

- [ ] Requested behavior exists.
- [ ] Existing and new relevant tests pass, or blockers are named.
- [ ] Relevant lint, type, build, and static checks pass.
- [ ] No known high-confidence or high/critical regressions remain.
- [ ] Affected README, docs, and examples are accurate.
- [ ] No debug logs, hardcoded secrets, or accidental telemetry were introduced.
- [ ] `.gitignore` covers newly introduced secrets, caches, and build artifacts.
- [ ] `.env.example` reflects required environment variables without values, when applicable.
- [ ] A clean-start or representative smoke path works when risk justifies it.
- [ ] The current task's disposable plan file is deleted after verification succeeds.

Apply checklist items only when relevant. `Not applicable` is valid when the task did not touch that surface; do not create CI, coverage, docs, `.env.example`, or clean-checkout work solely to satisfy ceremony.

Final report:

```text
Mode:
Changed:
Verified:
Risks:
Next:
```

If verification could not run, say why and name the best next command.

Do not claim "done" from code edits alone. Claim done only from implemented behavior plus a relevant signal: test, type/lint/build, smoke path, visual check, or review evidence for read-only work.

## Failure Recovery

Count materially different attempts against the same blocker, not every command failure.

- **Strike 1:** Fix the direct cause, then rerun the narrow check.
- **Strike 2:** Re-read the relevant path, revise the root-cause hypothesis, and try a different approach.
- **Strike 3:** Stop mutating. Preserve evidence and report the blocker.

After each failed attempt:

```text
Failure:
Evidence:
Class:
Changed assumption:
Next different action:
Stop if:
```

After strike 3, report:

```text
What I tried:
What failed:
Likely cause:
Ruled out:
Last known working state:
Needed decision or input:
```

Do not delete or weaken failing tests to pass. Do not keep making speculative edits. Revert only changes owned by the current task, and only when the exact safe boundary is known; never discard or stash unrelated user work. Keep the disposable plan file so the task can resume.
