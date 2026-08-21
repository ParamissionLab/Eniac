# Concurrency And Distributed Work

Use for threads, async ownership, queues, retries, ordering, duplicate delivery,
timeouts, cancellation, partitions, or distributed state. Make time, ownership,
ordering, duplication, and partial failure explicit.

1. Map state owner, mutation boundary, atomicity, consistency model, ordering,
   delivery guarantee, clock assumptions, and lifecycle/cancellation owner.
2. Define duplicate, retry, timeout, late result, reordering, partition,
   disconnect, worker crash, and shutdown behavior where applicable.
3. Bound queues, retries, backoff/jitter, timeouts, concurrency, memory, leases,
   caches, and fan-out.
4. Make externally retried effects idempotent or deduplicated at a durable
   boundary. Do not assume exactly-once delivery from a retrying network path.
5. Preserve causality/errors across async boundaries. Release locks, handles,
   subscriptions, tasks, and transactions on all exit paths.
6. Prefer deterministic transition tests, fake clocks, controlled schedulers,
   race detectors, and bounded load/fault tests. Flaky stress success alone does
   not prove the targeted interleaving.
7. Verify overload behavior and recovery, not only nominal throughput.

Protected invariant: no lost/duplicated committed effect beyond the declared
delivery model; no deadlock, starvation, unbounded backlog, or orphaned work in
the supported failure model.

Proof for mutation: transition/invariant tests, race/static tooling when
available, controlled retry/timeout/cancellation, and representative load or
integration evidence. For review/design, provide the state machine, failure
model, unknowns, and proof strategy without a correctness claim.
