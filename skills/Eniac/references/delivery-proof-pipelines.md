# Delivery Proof Pipelines

Use only when adding, repairing, or reviewing CI. Model CI as an executable proof graph derived from repository contracts, not as a copied workflow template.

## Derive The Pipeline

1. Inspect existing workflows, manifests, lockfiles, runtime declarations, scripts, test layout, and deployment boundaries.
2. Define required proofs before choosing provider syntax.
3. Order cheap deterministic gates before expensive or external gates.
4. Reuse repository commands locally where practical.
5. Pin permissions, runtime versions, and cache inputs intentionally.

```text
Checkout -> Runtime -> Deterministic install -> Static gates -> Tests -> Build -> Artifact/Smoke
```

Omit gates unsupported by the repository. Do not add a new linter, test framework, deployment, or release process merely to fill the graph.

## Proof Contract

| Gate | Evidence | Typical failure caught |
| --- | --- | --- |
| Install | lockfile-respecting clean install | undeclared or drifting dependencies |
| Format/lint | configured non-mutating check | style and basic defect regressions |
| Type/static | repository-native analyzer | contract and unsafe-flow regressions |
| Test | focused or full project suite | behavior regressions |
| Build | production-equivalent build | bundling, compile, packaging failures |
| Smoke/artifact | runnable path or inspected artifact | integration and delivery failures |

## Ecosystem Derivation

| Signal | Install | Core proof |
| --- | --- | --- |
| `package-lock.json` | `npm ci` | repository lint/type/test/build scripts |
| `pnpm-lock.yaml` | `pnpm install --frozen-lockfile` | repository pnpm scripts |
| `yarn.lock` | project-version frozen install | repository yarn scripts |
| `pyproject.toml` / requirements | project-declared environment install | configured test/type/lint commands |
| `go.mod` | `go mod download` when needed | `go test ./...`, configured vet/static checks |
| `Cargo.lock` | cargo resolves locked graph | format check, clippy when configured, tests |
| `build.zig` / `build.zig.zon` | `zig build` resolves dependencies | `zig build test`, `zig fmt --check` |
| Maven/Gradle/.NET/Ruby | wrapper or locked project tool | repository-native build and test tasks |

Repository scripts override these fallbacks.

## Safety And Reliability

- Grant the minimum workflow and token permissions.
- Never print secrets; pass named secret handles only to the step that needs them.
- Keep pull-request validation free of production mutation.
- Treat forked pull requests and untrusted code as hostile to secrets.
- Key caches from runtime, lockfile, architecture, and relevant build inputs; never rely on cache correctness.
- Add matrices only for supported compatibility claims, not for decorative coverage.
- Constrain path filters only when skipped jobs cannot hide a required proof.
- Separate release/deploy jobs from validation and require explicit authorization before adding them.

## Repair Method

Capture the first meaningful failing step, reproduce its repository command locally when possible, and classify the failure as workflow syntax, environment, dependency, code regression, flaky test, permission, or external service. Fix the cause, not the symptom. A retry without a changed hypothesis is not a repair.

Before handoff, validate workflow syntax, event filters, working directories, runtime versions, lockfile/cache paths, secret names, artifact paths, and the exact repository commands each gate invokes.

## Stack-Specific Starting Templates

For ready-to-adapt GitHub Actions YAML for common stacks (Node.js, Python, Go, Rust, Ruby, Java, .NET, and release workflows), load `references/ci-templates-by-stack.md`. Use these as starting points to adapt, not drop-in replacements. Repository scripts and existing workflows always take priority.
