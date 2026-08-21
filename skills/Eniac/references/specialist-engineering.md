# Specialist Engineering Router

Use this router when an ordinary implementation, investigation, refactor,
review, design, or release materially touches one or more specialist risks.
Read this file, then read only the matched overlay references. Do not load every
overlay for an ordinary code task.

Overlays strengthen Eniac's primary route. They do not authorize wider scope,
production mutation, destructive testing, credential use, deployment,
publication, or another external side effect.

## Composition Contract

Select one primary route and only evidence-backed overlays. Keep shared facts,
maps, and proof once when several overlays apply.

```text
Primary route: Answer | Investigate | Implement | Refactor | Review | Design | other
Operation: read-only | local mutation | external mutation
Overlay trigger:
Requested deliverable or outcome:
Current state or baseline: <when comparison matters>
Protected invariant:
Authorized boundary:
Change strategy: none for read-only | <smallest safe change>
Proof: evidence traceability for read-only | <behavior signal for mutation>
Rollback/recovery: not applicable for read-only | <proportional recovery>
Abort signal:
```

For review, explanation, design, or planning, proof means traceable evidence,
internally consistent decisions, explicit unknowns, and a usable deliverable.
Never imply that a proposed change, benchmark, test, deployment, or operational
signal already ran.

For mutation, proof means an observed signal for the changed behavior plus
regression/integration evidence proportional to its impact radius. A plan,
plausible diff, or unrelated green check is not changed-state proof.

When a version, vulnerability, platform behavior, or dependency contract can
have changed, verify it from current authoritative sources before relying on
memory.

## Select Overlays

| Concern | Trigger | Read |
| --- | --- | --- |
| Performance and capacity | latency, throughput, memory, cost, hot path, load | [performance-capacity.md](specialists/performance-capacity.md) |
| Security and privacy | trust boundary, auth, secrets, untrusted input, abuse, sensitive data | [security-privacy.md](specialists/security-privacy.md) |
| Data and schema migration | persisted shape, backfill, destructive transform, mixed app versions | [data-schema-migration.md](specialists/data-schema-migration.md) |
| API and contract evolution | public API, event, CLI, config, schema, serialized format | [api-contract-evolution.md](specialists/api-contract-evolution.md) |
| Dependency and toolchain change | manifest, lockfile, runtime, compiler, framework upgrade | [dependency-toolchain.md](specialists/dependency-toolchain.md) |
| Infrastructure and configuration | IaC, environment config, topology, stateful resource, secret reference | [infrastructure-configuration.md](specialists/infrastructure-configuration.md) |
| Reliability, incident, and observability | outage, degradation, SLO, alert, telemetry, recovery | [reliability-incident-observability.md](specialists/reliability-incident-observability.md) |
| Concurrency and distributed work | threads, async ownership, retries, queues, ordering, duplicate delivery | [concurrency-distributed.md](specialists/concurrency-distributed.md) |
| Test quality and flakiness | weak signal, nondeterminism, missing regression coverage | [test-quality-flakiness.md](specialists/test-quality-flakiness.md) |
| Release and rollout | package, artifact, migration rollout, deployment, rollback | [release-rollout.md](specialists/release-rollout.md) |

Apply an overlay only when inspected evidence or the requested deliverable
actually crosses that concern. A keyword, filename, or hypothetical possibility
is not a trigger.

## Cross-Overlay Completion Gate

Before closing:

- the primary route, operation type, matched triggers, boundary, deliverable,
  invariant, and evidence limits are explicit;
- read-only work contains evidence-backed findings/options and makes no changed-
  state or executed-proof claim;
- mutation work compares the relevant before/after state, addresses the deepest
  authorized cause, and proves behavior through a meaningful boundary;
- each applicable compatibility, security, performance, data, reliability,
  infrastructure, concurrency, test, and release effect is proved or explicitly
  deferred with an owner and next check;
- rollback/recovery is truthful and proportional when mutation is reversible or
  recovery is possible; `not applicable` is explicit for read-only work;
- durable docs change only when users or future operators need a changed fact,
  contract, decision, risk, operation, or handoff;
- no production, destructive, credentialed, publishing, or external action was
  inferred from permission for local engineering work.

One integrated signal may prove several overlays. Record which invariant it
supports instead of multiplying ceremony or duplicate tests.
