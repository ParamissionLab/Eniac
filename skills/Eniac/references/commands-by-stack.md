# Commands by Stack

Use only the sections needed for the next decision. Prefer repository scripts and configured tools over these fallbacks. Detect the active shell; examples use portable command names, but globbing, redirection, and path syntax may require PowerShell or POSIX adaptation.

## Discovery Toolkit

Start with fast, read-only signals:

```text
rg --files
rg --files -g package.json -g pyproject.toml -g go.mod -g Cargo.toml -g Gemfile -g pom.xml -g "*.csproj"
rg --files -g "*.test.*" -g "*.spec.*" -g "test_*.py" -g "*_test.go" -g "*_test.rs" -g "*Test.java" -g "*Tests.cs"
git status --short
git log -20 --oneline
```

Then read only the detected manifest, project-local instructions, relevant config, and direct call sites. Exclude dependency, VCS, cache, and build-output directories from broader searches.

Mode signals:

| Signal | Mode | Start |
| --- | --- | --- |
| Empty directory or no source | Greenfield | requirements and stack |
| Source without strong tests/docs | In-progress | scoped audit |
| Source, tests, docs, and CI | Mature | targeted improvement |
| Explicit bug, feature, refactor, or review | Targeted | requested path and abbreviated audit |

## Test and Coverage

```text
Node.js: npm test; configured coverage script, or npx jest --coverage
Python: pytest -v --cov=src --cov-report=term-missing
Go: go test ./... -v -cover
Rust: cargo test -- --nocapture
Ruby: bundle exec rspec
Java/Maven: mvn test
Java/Gradle: ./gradlew test
.NET: dotnet test --collect:"XPlat Code Coverage"
```

Do not install a coverage tool solely to obtain a percentage unless coverage is required. Report actual observed counts and distinguish pre-existing failures.

## Static Analysis

Run only tools already configured or clearly available:

```text
TypeScript/JavaScript: npx tsc --noEmit; npx eslint .
Python: python -m mypy src/ --ignore-missing-imports; python -m bandit -r src/
Go: go vet ./...; staticcheck ./...
Rust: cargo clippy -- -D warnings
Ruby: bundle exec rubocop
Java/Maven: mvn spotbugs:check
Java/Gradle: ./gradlew spotbugsMain
.NET: dotnet build
```

Treat a missing unconfigured tool as unavailable, not as a reason to add a dependency.

## Format and Lint

Check project config and narrow the target before writing changes:

```text
JavaScript/TypeScript: npx prettier --write <touched paths>; npx eslint <touched paths> --fix
Python: black <touched paths>; isort <touched paths>; ruff check --fix <touched paths>
Go: gofmt -w <touched files>
Rust: cargo fmt
Ruby: bundle exec rubocop -A <touched paths>
Java/Kotlin: ./gradlew spotlessApply; mvn spotless:apply
.NET: dotnet format
```

Avoid repository-wide formatting when only a few files changed unless the user requested it.

## Dependency Audit

Run only for ecosystems present in the repository and only when security or shipping risk justifies it:

```text
Node.js: npm audit (or the repository's package-manager equivalent)
Python: pip-audit
Rust: cargo audit
Ruby: bundle audit check --update
.NET: dotnet list package --vulnerable
```

Do not chain alternatives with `||`; one failing ecosystem command must not trigger unrelated commands.
