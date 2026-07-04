# Software Engineering Reference

Use when creating, reading, modifying, testing, reviewing, documenting, or shipping code.

## Mode

| Signal | Mode | Entry |
| --- | --- | --- |
| Empty or new directory | Greenfield | requirements, stack, plan, build |
| Existing source, weak tests/docs | In-progress | audit, improve requested area |
| Stable tests/docs/CI | Mature | abbreviated audit, targeted change |
| Bug, review, refactor, small feature | Targeted | inspect relevant context, patch, verify |

Do not run ceremony for tiny work. Do not edit existing code blind.

## Playbook

| Task | First action | Risk | Proof |
| --- | --- | --- | --- |
| Bug fix | reproduce or inspect failing path | symptom fix | failing case passes |
| Review | inspect diff and direct callers | missed regression | file/line evidence |
| Refactor | identify preserved contracts | behavior drift | tests or equivalence |
| Feature | find local analogs | pattern drift | behavior test/manual flow |
| Build failure | capture first meaningful error | chasing secondary errors | build reaches next state |
| Many small edits | group repeated pattern | partial inconsistency | sample diff plus broad check |

Report broader problems as risks unless they block the requested outcome.

## Size

| Size | Do | Avoid |
| --- | --- | --- |
| Tiny | exact file/error, edit, narrow check | repo audit |
| Small | local analogs, direct caller, patch, test | new abstractions |
| Medium | affected files, interfaces, tests, rollback risk | unrelated modules |
| Large | milestones with verification | one giant patch |
| Unclear | reproduce, logs, hypothesis, then size | guessing first |

## Batch Edits

For small edits across many files:

```text
Goal:
Pattern:
Rule:
Include:
Exclude:
Exceptions:
Verify:
```

Use structured tooling when the rule is exact: formatter, codemod, parser, project script, reviewed search/replace. Use manual patches when cases require judgment.

Flow: find candidates, group same-rule matches, edit one sample, inspect diff, apply group, handle exceptions, run narrow broad-check (`lint`, `typecheck`, tests, build, or targeted grep). Re-plan when many matches need unique judgment.

## Audit

Before editing, inspect only what can affect the change:

```text
Structure:
Stack:
Tests:
Tooling:
Conventions:
Git state:
Risk:
```

Set an edit boundary:

```text
Change:
Read only:
Preserve:
Not changing:
```

For tiny fixes, compress this to: files, pattern, command, risk.

## Build Standards

- Match local architecture, style, names, and tests.
- Read nearby examples before adding a pattern.
- Validate external inputs and handle errors with actionable messages.
- Keep changes scoped to the request.
- Avoid new frameworks, formatters, runners, state managers, or dependencies without concrete need.
- Preserve public interfaces unless explicitly changed.

## Tests

- Use the existing test framework and project scripts.
- Test behavior, not implementation details.
- Cover happy, boundary, and meaningful failure cases when risk justifies it.
- Run the narrowest useful check first; name broader checks left unrun.
- Report pre-existing failures separately.

Common signals: `package.json`, `pyproject.toml`, `go test ./...`, `cargo test`, `dotnet test`, `mvn test`, `gradle test`, `bundle exec rspec`.

## Bug Hunt

Check changed files and direct dependencies for input validation, swallowed errors, secrets, debug logs, async/lifecycle issues, hot-loop cost, null/empty/large/unicode input, and compatibility drift.

For review-only work, make a finding only with concrete evidence and user impact.

## Docs And Ship

Update docs only where behavior or usage changed. Do not write broad tutorials unless requested.

Final report:

```text
Mode:
Changed:
Verified:
Risks:
Next:
```

If verification could not run, say why and name the best next command.
