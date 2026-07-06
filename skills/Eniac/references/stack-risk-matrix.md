# Stack Risk Matrix

Use when stack-specific behavior can change implementation correctness. Read only detected rows. Repository contracts and configured tools override these defaults.

## Boundary First

For the touched path, identify:

```text
Input boundary -> normalization/validation -> domain operation -> side effect -> output contract
```

Then select the stack risks that can violate that path. Do not turn this matrix into a generic checklist.

## Runtime And Language Risks

| Stack signal | High-value invariants | Silent failure radar | Best proof |
| --- | --- | --- | --- |
| TypeScript / Node | runtime validation at external boundaries; consistent ESM/CJS and path resolution; awaited async ownership | `any` hiding contract drift, floating promises, unvalidated env, process-lifetime leaks | typecheck plus behavior test at boundary |
| Python | explicit package imports; specific exception contracts; isolated mutable state; public type boundaries | mutable defaults, broad catches, import-path-only success, fixture leakage | project test command from package root plus type/lint when configured |
| Go | every error handled with operation context; cancellation propagated; goroutine ownership defined | leaked goroutines, dropped errors, nil interface surprises, partial writes | table/race tests where relevant, `go test`, configured vet/static checks |
| Rust | typed error paths; ownership cost intentional; feature behavior explicit | production `unwrap`, clone masking design, feature-only compile failure, blocking in async path | fmt/clippy plus tests for enabled feature set |
| Java / Kotlin | nullability explicit; resources scoped; DTO/entity/API boundaries preserved | hidden nulls, blocking async pools, raw generic drift, transaction leakage | wrapper-native test/build and contract tests |
| .NET | async and cancellation propagated; enumeration/materialization intentional; comparison semantics explicit | `async void`, sync-over-async, repeated queries, culture-sensitive bugs | solution/project test plus analyzer/build signal |
| Ruby / Rails | validation and transaction ownership clear; query shape bounded; boundary objects explicit | callback side effects, N+1 queries, nil masking, global monkey patches | focused specs plus query/job/request proof |

## Framework And Data Risks

| Surface | Preserve | Failure radar | Proof |
| --- | --- | --- | --- |
| React / Next.js | render purity, server/client boundary, stable identity, lifecycle cleanup | stale closures, hydration mismatch, index keys, duplicate requests, secret leakage to client | component/route test and affected browser flow |
| HTTP / RPC API | auth before mutation, validated input, stable statuses/error shape, idempotency where required | mass assignment, stack trace leakage, retry duplication, incompatible schema drift | success plus invalid, unauthorized, not-found/conflict cases |
| Database | transaction boundary, migration ordering, old/new version coexistence, query cardinality | N+1, lock amplification, irreversible migration, partial write, missing index | migration dry run/rollback plan, integration test, query inspection |
| Queue / job | delivery semantics, deduplication, retry budget, poison-message handling | duplicate side effects, infinite retries, lost acknowledgements, unbounded concurrency | deterministic retry/idempotency test and observable failure path |
| Cache | source-of-truth ownership, invalidation, key versioning, stale tolerance | cross-tenant keys, cache-as-database, stampede, incompatible serialized values | miss/hit/stale/invalidation behavior tests |
| Files / object storage | path and content validation, atomicity, cleanup, access control | traversal, partial files, orphaned objects, public exposure | invalid input, interrupted write, authorization, cleanup proof |

## Cross-Stack Completion Gate

- Inputs are validated at the first trusted boundary.
- Errors preserve useful context without leaking secrets.
- Concurrency, cancellation, retry, and cleanup ownership are explicit where present.
- Public contracts and persisted data remain compatible unless change is authorized.
- Tests cover the highest-risk failure mode, not only the success path.
- Verification uses the repository's actual runtime and configured commands.
