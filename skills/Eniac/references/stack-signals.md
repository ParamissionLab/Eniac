# Stack Signals

Every stack asks the same four questions and answers them differently. Learn the questions
and the answers can be derived on the spot — including for a language nobody has written a
guide for, a house framework with three users, or something released after this file was
written.

```text
Detect    what tells you which stack this is
Prove     which commands, when they fail, mean something is actually wrong
Silent    what breaks here WITHOUT failing a build — where the real defects hide
Contract  what constitutes a breaking change for anything other people import
```

A list of ecosystems would always be missing the next one. The method is what generalizes,
and the shortcuts near the end are only shortcuts.

Load it when you do not yet know what proves anything here: an unfamiliar language, a house
framework, a repository you have not run, or any change to something other people import.
Do not load it for a stack whose commands you already know and have already run.

> **Owns** — deriving the proof commands, the silent failure modes, and the contract hazards for any stack, familiar or not; first contact with an unfamiliar repository; cross-stack discovery.
> **Defers** — what a proof must establish → `reality-testing.md`; whether an interface is well designed → `craft.md#designing-an-interface-others-use`; release sequencing → `workflows.md#ship`; what kind of *system* this is → `system-types.md`.

## Contents

- [First Contact With A Repository](#first-contact-with-a-repository)
- [Deriving The Proof Commands](#deriving-the-proof-commands)
- [Finding The Silent Failures](#finding-the-silent-failures)
- [What Breaks A Contract, In Any Language](#what-breaks-a-contract-in-any-language)
- [Writing Code In A Stack You Do Not Know](#writing-code-in-a-stack-you-do-not-know)
- [Detection Shortcuts](#detection-shortcuts)
- [Command Shortcuts](#command-shortcuts)
- [Cross-Stack Discovery](#cross-stack-discovery)
- [Containers](#containers)

## First Contact With A Repository

Before reasoning about code you have never executed, find out whether it runs. Each step
that fails is information about the project, not a detour — and reaching a running state is
almost always cheaper than arguing with code you cannot observe.

1. **Does it install?** Run the project's own install command and read the real error. A
   toolchain version mismatch is the most common cause — check whatever pins the version
   before blaming the code.
2. **Does it build?**
3. **Does it test?** Record the baseline here: which tests already fail, and how many. That
   number is what separates a regression you caused from one you inherited.
4. **Does it run?** Find the entry point and start it once. Rung four of the verification
   ladder needs this, and wiring bugs live nowhere else.

**Do not modify project configuration to make a command pass.** Loosening a type setting,
pinning around a failing dependency, or skipping a failing test converts a finding into a
hidden problem. If the project does not build, that is something to report, not something
to route around.

## Deriving The Proof Commands

**The project's own commands outrank the ecosystem's defaults, always.** They are the ones
the maintainers keep green, and they encode local knowledge no general guide has. Look in
this order and stop at the first that answers:

1. **The CI workflow.** This is the authoritative definition of "passing" for this project.
   Whatever it runs is what must pass, in that order, with those flags.
2. **The task runner** — a scripts block, `Makefile`, `justfile`, `Taskfile`, or equivalent.
   Read the target names; they tell you what the team considers a distinct check.
3. **Contributing docs and the README's build section.**
4. **The ecosystem default**, only when the first three are silent.

Then sort what you found into four kinds, because they fail for different reasons and
skipping one is how a defect ships:

| Kind | Answers | Skipping it means |
| --- | --- | --- |
| Build / compile | does it turn into an artifact | nothing runs |
| Type or static check | do the declared shapes hold | a whole class of bug reaches runtime — and in several ecosystems this is a **separate command from the build**, which is the single most common gap |
| Test | does it behave | you are guessing |
| Lint / format | does it match the local conventions | review noise, and sometimes a real bug the linter knew about |

**Confirm each command can fail.** Break something on purpose once — a deliberate type
error, a deliberately wrong assertion — and check that the command goes red. A check that
cannot fail is not proof, and this is the cheapest possible way to find that out. It is
also how you discover that the test command matched zero tests, that the linter had no
files in scope, or that the type checker was disabled in this directory.

## Finding The Silent Failures

Every ecosystem has a set of things that go wrong *without* failing a build. These are
where real defects live, because everything that fails loudly was already fixed. Four
questions surface them in any stack:

- **What does this language let you ignore?** An unchecked error return, a swallowed
  exception, a nullable value used as if it were not, a discarded promise or future, an
  unread status code. Grep for the local shape of "ignore this" and read each hit.
- **What is checked at runtime rather than at build time?** Reflection, dynamic dispatch,
  string-keyed lookups, serialization, dependency injection, configuration parsing. None of
  it is covered by a green build, and all of it fails in front of a user.
- **What differs between the environment you are in and the one that matters?** Toolchain
  version, feature flags or build tags, optimization level, target platform, locale and
  timezone, filesystem case sensitivity, available system libraries. A green build under
  one configuration says nothing about another — and in ecosystems with conditional
  compilation, that is a genuine second build you have not run.
- **What is only asserted in a comment?** Invariants, lifetimes, thread-safety, ownership,
  ordering. When correctness depends on something the compiler cannot see, the comment is
  the entire enforcement mechanism, and it is one refactor from being false.

When you find one, the cheapest durable fix is usually to make it loud: a lint rule, a
stricter compiler flag, a check in CI. Write it down at the seam either way
(`learning-loop.md`).

## What Breaks A Contract, In Any Language

Anything other people import — a library, an SDK, a framework, a service API, a schema, a
shared module, a script another job calls — has a public surface, and a public surface is a
one-way door (`judgment.md#sort-the-door-first`). These changes look additive and are not,
in every language that has the concept:

| Change | Why it breaks |
| --- | --- |
| Adding a member to an interface, trait, protocol, or abstract type | every outside implementer stops compiling — a default implementation or a separate interface avoids it |
| Adding a required parameter | every existing call site; a defaulted or keyword-only parameter does not |
| Narrowing what you accept, or widening what you return | callers passing the old shape, or handling only the old shape |
| Changing the error or exception raised | handlers matching the old one silently stop matching, and the failure surfaces somewhere else |
| Adding a variant to an enum or union | exhaustive matches in consumers — mark the type non-exhaustive from the first release, because retrofitting that *is* the breaking change |
| Changing a serialized shape — JSON, protobuf, database rows, files | old readers and new writers coexist during every single deploy |
| Renaming anything reachable by name | named arguments, reflection, serializers, ORMs, and configuration files that nothing type-checks |
| Changing memory layout or symbol shape, where compiled callers exist | source compatibility and binary compatibility are **different questions**, and the second is the one that bites |
| Raising a minimum language, runtime, or platform version | consumers who cannot move yet — it is a major version everywhere |
| Tightening a default, or changing what one means | every caller who never set it, which is most of them |

Four rules cover the rest:

- **Additive first.** A new function beside the old one costs a deprecation cycle and
  breaks nobody. Narrow now, widen later — widening is easy, narrowing breaks everybody.
- **The contract is what people actually depend on**, not what you documented. If a
  "private" symbol is imported by three teams, it is public, and discovering that after
  removing it is the expensive order.
- **Design for evolution before the first release**, because most of these hazards have a
  cheap answer that is only available up front: non-exhaustive types, keyword-only
  parameters, an opaque handle instead of an exposed layout, a sealed extension point, a
  version field in every serialized shape.
- **Check compatibility mechanically if the ecosystem has a tool for it.** Where one
  exists, it belongs in CI — source compatibility is what your build proves, and it is not
  the thing your users hit.

## Writing Code In A Stack You Do Not Know

The goal is not fluency. It is producing a change that a maintainer would have written, in
an ecosystem you met an hour ago.

1. **Read three neighbours before writing one line.** The file you are changing, the file
   most like it, and its test. That gives you the local answers to error handling, naming,
   file layout, and test structure — which matter more than anything general you know.
   Convention is inferred from the code, never from the ecosystem's blog posts.
2. **Copy the shape of the nearest working example**, then change what the task requires.
   New code that ignores local convention is a permanent maintenance tax, and in an
   unfamiliar stack your instinct for "better" is untrustworthy.
3. **Let the tools teach you.** Compiler errors, the strictest available lint, and the type
   checker are a free tutor. Turn them up rather than down, and read what they say instead
   of pattern-matching a fix.
4. **Write the smallest thing that runs, and run it**, before writing the rest. In an
   unfamiliar stack the gap between "looks right" and "works" is wider than usual, and
   feedback is the only way to close it (`loops.md#shortening-beats-running`).
5. **Do not introduce a dependency, a pattern, or a tool the project does not already use.**
   You do not yet know what it conflicts with here, and the maintainers do.
6. **Say what you are unsure about.** An idiom you guessed at, an API you did not verify,
   a convention you inferred from one example — label it (`Assumption`) rather than
   letting it read as knowledge. That single sentence is what makes the change safe to
   review.

## Detection Shortcuts

Evidence at the repository root usually settles the stack in seconds:

| Evidence | Stack |
| --- | --- |
| `package.json` | Node — check `packageManager`, then the lockfile |
| `tsconfig.json` | TypeScript — type checking is a separate step from the build |
| `pyproject.toml`, `requirements.txt`, `setup.py` | Python — look for the lockfile |
| `go.mod` | Go |
| `Cargo.toml` | Rust |
| `pom.xml`, `build.gradle` | Java / Kotlin |
| `Gemfile` | Ruby |
| `*.csproj`, `*.sln` | .NET |
| `composer.json` | PHP |
| `Package.swift`, `*.xcodeproj` | Swift |
| `mix.exs` | Elixir |
| `CMakeLists.txt`, `Makefile`, `meson.build` | C / C++ |
| `pubspec.yaml` | Dart / Flutter |
| `*.tf`, `Pulumi.yaml`, `helm/`, k8s manifests | infrastructure as code |
| `Dockerfile`, `compose.yaml` | containerized — the real runtime differs from the host |
| `.github/workflows/` or equivalent | the authoritative definition of "passing" here |

Read whatever pins the toolchain version before running anything. A version mismatch
produces failures that look exactly like code bugs.

Nothing recognizable is not a dead end: the language is in the file extensions, the build
is in whatever the CI step invokes, and the conventions are in the code. Run
[Deriving The Proof Commands](#deriving-the-proof-commands) and say which parts you had to
infer.

## Command Shortcuts

Common defaults, for when the project defines none. **These are shortcuts, not the method** —
when the stack is not here, or these do not fit, derive them instead.

```text
Node/TS   npm ci · npm test · npx tsc --noEmit · npx eslint . · npm run build
Python    pytest · mypy . (or pyright) · ruff check . · python -c "import <pkg>"
Go        go build ./... · go test ./... -race · go vet ./... · gofmt -l .
Rust      cargo build --all-features · cargo test · cargo clippy -- -D warnings · cargo fmt --check
Java/Kt   mvn -q verify   /   ./gradlew build --warning-mode all
.NET      dotnet build -warnaserror · dotnet test · dotnet format --verify-no-changes
Ruby      bundle exec rspec · bundle exec rubocop
PHP       vendor/bin/phpunit · vendor/bin/phpstan analyse
Swift     swift build · swift test   /   xcodebuild test -scheme <name>
Elixir    mix compile --warnings-as-errors · mix test · mix dialyzer
C/C++     cmake --build . && ctest · -Wall -Wextra -Werror · a sanitizer run
Dart      dart analyze --fatal-infos · flutter test
Shell     shellcheck · and run it once with set -euo pipefail and a failing step
SQL       run the migration on a copy, run it twice, run the down-migration, EXPLAIN
IaC       validate && plan — the plan IS the review artifact; read it for destroys first
```

Two of these carry more weight than the rest. In several ecosystems **the type check is a
separate command from the build**, so a green build proves less than it appears to. And
**sanitizers, race detectors, and dialyzer-style tools find defects no test does** — where
the ecosystem has one, it is a required check rather than a debugging aid.

## Cross-Stack Discovery

```bash
git status --short
git log --oneline -10
rg -n "TODO|FIXME|HACK" --stats
rg -l "<symbol>"                  # who uses this
git log -S "<symbol>" --oneline   # when it appeared or changed
```

For "what changed and what might it break", a diff plus a caller search on the changed
symbols is faster and more accurate than reading files.

## Containers

When a container definition exists, the host is not the runtime. Tests that pass locally
can fail in the image over base-image versions, missing system libraries, file permissions,
or the absence of dev dependencies. If the project ships in a container, at least one
verification run belongs inside it.
