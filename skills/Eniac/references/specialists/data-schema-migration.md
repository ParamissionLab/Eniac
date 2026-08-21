# Data And Schema Migration

Use for persisted shapes, backfills, semantic transforms, indexes/constraints,
data format changes, or mixed application versions. Treat the work as a
transition between live states, not one schema edit.

1. Inventory schema/format, readers, writers, constraints, volume, retention,
   backups, replication, and old/new versions that may coexist.
2. Classify the change: additive, backfill, rename, type/semantic transform,
   split/merge, index/constraint, or destructive removal.
3. Prefer `expand -> migrate/backfill -> verify -> switch readers/writers ->
   contract`; declare the compatibility window.
4. Make migration/backfill restartable or idempotent. Define batching,
   checkpoints, ordering, contention limits, and partial-failure behavior.
5. Define reconciliation before execution: counts, checksums, invariants,
   semantic samples, orphan/duplicate detection, and accepted error budget.
6. Separate code rollback from data rollback. Name the point requiring restore,
   forward fix, or compensating migration.
7. Rehearse on representative non-production data when risk warrants it. A
   backup claim is not recovery proof until restore feasibility is known.
8. Remove compatibility paths only after consumers move and reconciliation plus
   the observation window pass.

Protected invariant: no silent loss, corruption, duplication, cross-tenant leak,
or unreadable state for supported versions.

Proof for mutation: rehearsal/dry run, reconciliation, mixed-version evidence,
and rollback/forward-recovery plus post-change health. For plan/review, provide
the transition stages, unknowns, proof plan, and rollback limits without
implying execution. Load `references/safety-and-delivery.md`.
