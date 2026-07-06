# CI Templates by Stack

Ready-to-adapt CI configurations. Use repository scripts and existing workflows first. These are starting points derived from ecosystem conventions, not drop-in replacements. Adapt versions, paths, scripts, and gates to the actual project.

## Contents

- [Node.js / TypeScript](#nodejs--typescript)
- [Python](#python)
- [Go](#go)
- [Rust](#rust)
- [Zig](#zig)
- [Ruby](#ruby)
- [Java / Kotlin (Gradle)](#java--kotlin-gradle)
- [.NET](#net)
- [Release: npm](#release-npm)
- [Release: PyPI](#release-pypi)
- [Setup checklist](#setup-checklist)

## Node.js / TypeScript

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        node-version: [18, 20, 22]

    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js ${{ matrix.node-version }}
        uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
          cache: 'npm'

      - run: npm ci
      - run: npm run lint --if-present
      - run: npm run typecheck --if-present
      - run: npm test
      - run: npm run build --if-present

      - name: Upload coverage
        if: matrix.node-version == 22
        uses: codecov/codecov-action@v4
        with:
          token: ${{ secrets.CODECOV_TOKEN }}
```

Adapt: replace `npm` with `pnpm` or `yarn` if the project uses them; match scripts to `package.json`.

## Python

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.10', '3.11', '3.12']

    steps:
      - uses: actions/checkout@v4

      - name: Setup Python ${{ matrix.python-version }}
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
          cache: 'pip'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install pytest pytest-cov mypy ruff

      - name: Lint
        run: ruff check .

      - name: Type check
        run: python -m mypy src/ --ignore-missing-imports

      - name: Test
        run: pytest --cov=src --cov-report=xml --cov-report=term-missing -v

      - name: Upload coverage
        if: matrix.python-version == '3.12'
        uses: codecov/codecov-action@v4
        with:
          token: ${{ secrets.CODECOV_TOKEN }}
```

Adapt: use `uv` or `poetry` install if the project uses them; match `src/` to actual source layout.

## Go

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Setup Go
        uses: actions/setup-go@v5
        with:
          go-version-file: 'go.mod'

      - name: Vet
        run: go vet ./...

      - name: Static check
        run: |
          go install honnef.co/go/tools/cmd/staticcheck@latest
          staticcheck ./...

      - name: Test
        run: go test ./... -v -race -coverprofile=coverage.out

      - name: Upload coverage
        uses: codecov/codecov-action@v4
        with:
          token: ${{ secrets.CODECOV_TOKEN }}
          files: ./coverage.out
```

Adapt: pin `go-version` explicitly if no `go.mod` version directive; add `golangci-lint` if configured.

## Rust

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

env:
  CARGO_TERM_COLOR: always

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Format check
        run: cargo fmt -- --check

      - name: Clippy
        run: cargo clippy -- -D warnings

      - name: Test
        run: cargo test --verbose

      - name: Build release
        run: cargo build --release --verbose
```

Adapt: add feature flags to test/clippy if the project uses them; add `cargo audit` for security.

## Zig

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4
        with:
          submodules: recursive

      - name: Setup Zig
        uses: goto-bus-stop/setup-zig@v2
        with:
          version: 0.13.0

      - name: Build
        run: zig build

      - name: Test
        run: zig build test

      - name: Format check
        run: zig fmt --check src/
```

Adapt: pin `version` to the project's `build.zig.zon` minimum version; add `--summary all` to test for verbose output; include `submodules: recursive` if using Zig package manager with git dependencies.

## Ruby

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        ruby-version: ['3.2', '3.3']

    steps:
      - uses: actions/checkout@v4

      - name: Setup Ruby ${{ matrix.ruby-version }}
        uses: ruby/setup-ruby@v1
        with:
          ruby-version: ${{ matrix.ruby-version }}
          bundler-cache: true

      - name: Lint
        run: bundle exec rubocop

      - name: Test
        run: bundle exec rspec
```

Adapt: add database services for Rails apps; match test command to `Rakefile` or `Gemfile` scripts.

## Java / Kotlin (Gradle)

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        java-version: [17, 21]

    steps:
      - uses: actions/checkout@v4

      - name: Setup Java ${{ matrix.java-version }}
        uses: actions/setup-java@v4
        with:
          distribution: 'temurin'
          java-version: ${{ matrix.java-version }}

      - name: Setup Gradle
        uses: gradle/actions/setup-gradle@v4

      - name: Lint
        run: ./gradlew spotlessCheck

      - name: Test
        run: ./gradlew test

      - name: Build
        run: ./gradlew build
```

Adapt: replace Gradle with Maven (`mvn verify`) if applicable; remove `spotlessCheck` if not configured.

## .NET

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        dotnet-version: ['8.0', '9.0']

    steps:
      - uses: actions/checkout@v4

      - name: Setup .NET ${{ matrix.dotnet-version }}
        uses: actions/setup-dotnet@v4
        with:
          dotnet-version: ${{ matrix.dotnet-version }}

      - name: Restore
        run: dotnet restore

      - name: Build
        run: dotnet build --no-restore

      - name: Test
        run: dotnet test --no-build --collect:"XPlat Code Coverage"
```

Adapt: add `dotnet format --verify-no-changes` if formatting is enforced.

## Release: npm

```yaml
name: Release

on:
  push:
    tags: ['v*']

jobs:
  publish:
    runs-on: ubuntu-latest
    permissions:
      contents: write
      id-token: write

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: 22
          registry-url: 'https://registry.npmjs.org'

      - run: npm ci
      - run: npm run build --if-present
      - run: npm test
      - run: npm publish --provenance --access public
        env:
          NODE_AUTH_TOKEN: ${{ secrets.NPM_TOKEN }}
```

## Release: PyPI

```yaml
name: Release

on:
  push:
    tags: ['v*']

jobs:
  publish:
    runs-on: ubuntu-latest
    permissions:
      id-token: write

    steps:
      - uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Build
        run: |
          pip install build
          python -m build

      - name: Publish to PyPI
        uses: pypa/gh-action-pypi-publish@release/v1
```

## Setup Checklist

After adding CI, verify:

- [ ] Workflow file at `.github/workflows/ci.yml` runs on push and PR to main
- [ ] Badge added to README: `![CI](https://github.com/USER/REPO/actions/workflows/ci.yml/badge.svg)`
- [ ] Required secrets configured in repo settings (tokens for coverage, publishing)
- [ ] CI runs green on first push — fix before shipping
- [ ] Matrix covers only versions the project actually supports
- [ ] Release workflow tested with a dry-run tag if applicable
- [ ] Path filters added only when skipped gates cannot hide a required proof
