# Software Engineering Reference

Use when creating, reading, modifying, testing, reviewing, documenting, or shipping code.

## Full-Cycle Shape

Own the path to a verified handoff:

```text
Discover -> Plan -> Build -> Test -> Bug hunt -> Polish -> Document -> Ship
```

Use every phase for greenfield or broad work. For targeted work, abbreviate the phases but do not edit existing code blind.

Announce only phase changes that help the user track risk or progress. Close a phase with its concrete signal, for example: `Test complete — 31 passing, 0 failing`.

## Mode

| Signal | Mode | Entry | Proof |
| --- | --- | --- | --- |
| Empty/new project | Greenfield | requirements, stack, plan | app/library runs |
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

## Build

- Match local architecture, style, names, imports, errors, and tests.
- Read nearby examples before adding a pattern.
- Validate external inputs and handle errors with actionable messages.
- Keep changes scoped to the request and touched files.
- Avoid new frameworks, formatters, runners, state managers, or dependencies without concrete need.
- Preserve public interfaces and serialized shapes unless explicitly changed.
- For greenfield work, include run/test scripts, minimal README, `.gitignore`, and a smoke check.

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
- Test behavior, not implementation details.
- Cover happy, boundary, and meaningful failure cases when risk justifies it.
- Keep tests isolated; avoid shared mutable state.
- Report pre-existing failures separately.

Common signals: `package.json`, `pyproject.toml`, `go test ./...`, `cargo test`, `dotnet test`, `mvn test`, `gradle test`, `bundle exec rspec`.

Use the project-native scripts first. If the repository does not expose the needed command, select a compatible command from `commands-by-stack.md`. Report the observed counts when available: `X passing, Y failing, Z% coverage`.

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

## Polish

- Run configured formatter/linter/type/build checks relevant to touched files.
- Use `commands-by-stack.md` only after checking the repository's existing config and scripts.
- Remove unused imports, dead code introduced by the change, commented-out code, and debug prints.
- Update generated files only when they are source-controlled outputs for touched inputs.
- Do not add global formatting churn unless requested.

## Docs And Ship

Update docs only where behavior or usage changed. Do not write broad tutorials unless requested.

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

Final report:

```text
Mode:
Changed:
Verified:
Risks:
Next:
```

If verification could not run, say why and name the best next command.

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
