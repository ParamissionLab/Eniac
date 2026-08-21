# Test Quality And Flakiness

Use for weak signals, missing regression coverage, nondeterminism, flaky tests,
or a new test strategy. Optimize for discrimination, not test count or coverage
percentage alone.

1. Map outcomes and highest risks to the cheapest proving layer: unit, contract,
   integration, end-to-end, or operational.
2. Make tests own data, clock, randomness, ports, filesystem, environment, and
   external substitutes. Use deterministic seeds and report them on failure.
3. Assert behavior/invariants. Avoid implementation mirroring, broad snapshots,
   arbitrary sleeps, and mocks that bypass the contract.
4. For regressions, show fail-before/pass-after when feasible. A test always
   green does not lock the defect.
5. For flakes, preserve evidence and classify shared state, time, randomness,
   race, exhaustion, environment, external dependency, or brittle assertion.
   Instrument before adding retries.
6. Prefer a deterministic trigger or forced ordering. If impossible, a bounded
   repeated/stress run can reduce uncertainty but cannot alone prove root cause
   or permanent correction; report the run shape, prior frequency, monitoring,
   and residual confidence.
7. Quarantine only as explicit temporary containment with owner, impact, and
   removal condition. Never skip, weaken, or retry away a product defect.
8. Use property/fuzz/mutation/load/fault testing only when the input space or
   invariant warrants it and failures are reproducible from captured data.

Protected invariant: the suite remains deterministic enough to trust and fails
when protected behavior breaks.

Proof for mutation: deterministic fail-then-pass when possible, isolation
evidence, and broader checks. Non-deterministic repetition is supporting evidence,
not sole completion proof. For review/design, deliver the risk-to-test map,
evidence limits, and proposed proving signals without a pass claim.
