# Software Engineering Reference

Use this reference when the task involves creating, reading, modifying, testing, reviewing, documenting, or shipping code.

## Mode Routing

Classify the task before acting:

| Signal | Mode | Entry point |
| --- | --- | --- |
| Empty or new directory | Greenfield | gather requirements, choose stack, plan, build |
| Existing source but weak tests/docs | In-progress | audit, then improve the requested area |
| Existing tests, docs, CI, stable structure | Mature | abbreviated audit, targeted change |
| Bug fix, review, refactor, small feature | Targeted | inspect relevant context, patch, verify |

Do not run a full ceremony for a tiny task. Do not skip discovery for existing code.

## Discovery Audit

Before editing existing code, inspect enough to avoid working blind:

```text
Structure:
Stack/dependencies:
Existing tests:
Tooling:
Conventions:
Recent git state:
Known risks:
```

Use fast targeted commands first: file search, dependency manifests, test file names, formatter/linter configs, recent errors, and call sites.

Set an edit boundary before touching files:

```text
Likely files to change:
Files to read only:
Interfaces to preserve:
Behaviors not being changed:
```

## Phase Gates

Run only the phases the task needs:

1. Discover: understand project shape and relevant constraints.
2. Plan: define done criteria, affected files, risk, and verification.
3. Build: implement in small reversible batches.
4. Test: run or add tests that prove behavior.
5. Bug hunt: check changed code and direct callers for regressions.
6. Polish: format, lint, type-check, remove dead/debug code.
7. Document: update docs only where behavior or usage changed.
8. Ship: final status with checks, risks, and next commands.

For broad greenfield work, use all phases. For targeted fixes, use discover, build, test, bug hunt, and ship.

Keep plans proportional:

| Task size | Planning budget |
| --- | --- |
| Tiny fix | 1-3 bullets, then act |
| Medium change | checklist with affected files and verification |
| Broad project | phased plan with risks and stop points |

Do not create or update planning documents unless the user asks or the project already uses them.

## Build Standards

- Use names that explain intent.
- Validate external inputs before using them.
- Handle errors with actionable messages.
- Keep functions small and focused.
- Avoid magic strings and numbers; name constants.
- Follow the language and project naming style.
- Read two or three similar local examples before adding a new pattern.
- Scope improvements to files touched by the task.
- Do not introduce a new framework, formatter, test runner, state manager, or architecture pattern without a concrete need.

## Test Standards

- Extend the existing test framework instead of adding a new one.
- Test behavior, not implementation details.
- Cover a happy path, a boundary case, and one meaningful failure case when the risk justifies it.
- Keep tests isolated; avoid shared mutable state across test cases.
- If existing tests fail before the change, report that separately from failures caused by the change.

Choose commands from the project, not from preference. Common signals:

```text
Node: package.json scripts, npm/pnpm/yarn test, typecheck, lint
Python: pyproject.toml, pytest, ruff, mypy
Go: go test ./..., go vet ./...
Rust: cargo test, cargo clippy, cargo fmt
.NET: dotnet test, dotnet build
Java/Kotlin: mvn test, gradle test
Ruby: bundle exec rspec, bundle exec rubocop
```

## Bug Hunt Checklist

Prioritize files changed and their direct dependencies:

- Inputs validated
- Errors handled and not swallowed
- No hardcoded secrets
- No debug logs in production paths
- No obvious race, lifecycle, or async issues
- No N+1 or expensive hot-loop work
- Empty, null, large, and unicode inputs considered where relevant
- Public interfaces and backwards compatibility preserved unless explicitly changed

## Documentation Standards

For existing projects, update only stale or newly affected docs. For new projects, ensure the README has:

```text
Project name and one-sentence purpose
Features or capabilities
Copy-pasteable quick start
Installation and requirements
Real usage examples
Configuration options
Development commands
License, if applicable
```

Do not leave template filler text. Give code blocks language tags.

Do not write broad tutorials, migration guides, or architecture essays unless requested.

## Failure Recovery

Use a three-strike rule:

1. Fix the direct error and verify.
2. Re-read the relevant code, logs, and assumptions; try a different approach.
3. Stop changing code and report what failed, what was tried, what is ruled out, and what decision is needed.

Do not delete failing tests just to pass. Do not leave broken code without reporting it.

## Ship Report

Keep final reports compact:

```text
Mode:
Changed:
Verified:
Risks:
Next:
```

Include exact commands and important file paths. Skip empty sections.

If verification could not run, say why in one sentence and name the best command to run next.
