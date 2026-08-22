# Stack Signals

Detect the stack from evidence, then use the commands that actually prove something.
Load only the section for the stack in front of you.

**Always check the repository's own scripts first.** A `package.json` scripts block, a
`Makefile`, `justfile`, `Taskfile`, `tox.ini`, or CI workflow tells you what this project
considers a real check. Running the project's own command beats running the ecosystem
default, because it is the one the maintainers keep green.

> **Owns** — recognizing an unfamiliar stack and knowing which command actually proves something in it, plus the silent failure modes per ecosystem.
> **Defers** — what the proof needs to establish → `reality-testing.md`; first orientation in an unfamiliar repository → `workflows.md#audit`.

## First Contact With A Repository

Before reasoning about code you have never executed, find out whether it runs. Each
step that fails is information about the project, not a detour — and reaching a running
state is almost always cheaper than arguing with code you cannot observe.

1. **Does it install?** Run the project's own install command and read the real error.
   A version mismatch is the most common cause — check `.nvmrc`, `.python-version`,
   `.tool-versions`, or an `engines` field before blaming the code.
2. **Does it build?**
3. **Does it test?** Record the baseline here: which tests already fail, and how many.
   This number is what separates a regression you caused from one you inherited.
4. **Does it run?** Find the entry point and start it once. Rung 4 of the verification
   ladder needs this, and wiring bugs live nowhere else.

**Do not modify project configuration to make a command pass.** Loosening a type
setting, pinning around a failing dependency, or skipping a failing test converts a
finding into a hidden problem. If the project does not build, that is something to
report, not something to route around.

## Detection

| Evidence | Stack |
| --- | --- |
| `package.json` | Node — check `packageManager`, then the lockfile: `package-lock.json` / `yarn.lock` / `pnpm-lock.yaml` / `bun.lockb` |
| `tsconfig.json` | TypeScript — type checking is a separate step from the build |
| `pyproject.toml`, `requirements.txt`, `setup.py` | Python — check for `uv.lock`, `poetry.lock`, `Pipfile.lock` |
| `go.mod` | Go |
| `Cargo.toml` | Rust |
| `pom.xml`, `build.gradle` | Java / Kotlin |
| `Gemfile` | Ruby |
| `*.csproj`, `*.sln` | .NET |
| `composer.json` | PHP |
| `Dockerfile`, `compose.yaml` | containerized — the real runtime may differ from the host |
| `.github/workflows/` | the authoritative definition of "passing" for this project |

Also read `.nvmrc`, `.python-version`, `.tool-versions`, or an `engines` field before
running anything — a version mismatch produces failures that look like code bugs.

## Node / TypeScript

```bash
npm ci                 # or: pnpm i --frozen-lockfile / yarn --immutable / bun install
npm test
npx tsc --noEmit       # types: the build often does not check these
npx eslint .
npm run build
npm audit --omit=dev
```

**Silent failure modes:** `tsc` passing while the runtime fails, because types are erased
and external data is unvalidated. `any` and non-null `!` hiding a real null. ESM/CJS
interop breaking only at runtime. Floating promises swallowing rejections — check for
`no-floating-promises`. `NODE_ENV` changing behavior between test and production. A
lockfile not committed, so CI resolves different versions than you did.

## Python

```bash
python -m pytest -q
python -m mypy .           # or: pyright
python -m ruff check .
python -m ruff format --check .
pip check
```

**Silent failure modes:** the wrong interpreter or virtualenv — confirm with
`python -c "import sys; print(sys.executable)"` before believing any result. Mutable
default arguments. Broad `except Exception` swallowing real errors. Import-time side
effects. Type hints that are not enforced at runtime. `__pycache__` from a previous
version masking a change.

## Go

```bash
go build ./...
go test ./...
go test -race ./...
go vet ./...
gofmt -l .
```

**Silent failure modes:** an ignored `err` return — this is the single most common Go
defect. Loop-variable capture in goroutines on older versions. A nil map write panicking
at runtime. A missing `-race` run on concurrent code. `context` deadlines not propagated.

## Rust

```bash
cargo build
cargo test
cargo clippy -- -D warnings
cargo fmt --check
```

**Silent failure modes:** `unwrap()` and `expect()` in a path that can actually fail.
Feature flags changing what compiles, so a green local build says nothing about another
feature set. `unsafe` blocks whose invariants are only in a comment.

## Java / Kotlin

```bash
./mvnw -q verify        # or: ./gradlew build
./mvnw -q test
```

**Silent failure modes:** dependency version conflicts resolved silently — check the
dependency tree. A checked exception caught and logged but not handled. Reflection and
dependency injection wiring that fails only at startup, not at compile time.

## Ruby

```bash
bundle install
bundle exec rspec       # or: bundle exec rake test
bundle exec rubocop
```

**Silent failure modes:** monkey patches applied by load order. `nil` propagating far
from its origin. Metaprogramming that makes static search miss real callers — search for
string forms of method names too.

## .NET

```bash
dotnet restore
dotnet build --no-restore
dotnet test
dotnet format --verify-no-changes
```

**Silent failure modes:** `async void`. Nullable reference warnings disabled at the
project level. Deadlocks from `.Result` or `.Wait()` on an async call.

## PHP

```bash
composer install
composer test           # or: ./vendor/bin/phpunit
./vendor/bin/phpstan analyse
```

**Silent failure modes:** loose comparison (`==`) surprises. Autoload cache staleness.
Errors suppressed with `@`.

## Cross-Stack Discovery

```bash
git status --short
git log --oneline -10
rg -n "TODO|FIXME|HACK" --stats
rg -l "<symbol>"                  # who uses this
git log -S "<symbol>" --oneline   # when it appeared or changed
```

For "what changed and what might it break", `git diff` plus a caller search on the
changed symbols is faster and more accurate than reading files.

## Containers

When a `Dockerfile` or compose file exists, the host is not the runtime. Tests that pass
locally can fail in the image over base-image versions, missing system libraries, file
permissions, or the absence of dev dependencies. If the project ships in a container, at
least one verification run belongs inside it.

## When The Stack Is Unfamiliar

1. Read the CI workflow — it defines what "passing" means here, authoritatively.
2. Read the README's build and test sections.
3. Run the smallest check first and confirm it fails when you break something on purpose.
   A check that cannot fail is not proof, and this is the cheapest possible way to find
   that out.
