# Performance And Capacity

Use for latency, throughput, memory, CPU, I/O, startup, bundle-size, capacity,
or cost work. Start with a representative workload and comparable baseline;
“feels faster,” one noisy timing, or an irrelevant microbenchmark is not proof.

1. Define the user/system outcome, workload shape, environment, data size,
   concurrency, warm/cold state, and constraining metric.
2. Capture baseline and variance before changing code. Keep fixtures,
   environment, build mode, sampling window, and cache state comparable.
3. Profile or instrument the real path. A suspected hot path is `Unverified`
   until measured.
4. Fix the dominant in-scope cause. Check complexity, repeated I/O, N+1 work,
   allocation/copying, contention, serialization, network round trips, caching
   correctness, and batching before micro-optimization.
5. Re-run the same workload and report absolute and relative results with
   variance. Verify correctness, memory, downstream latency, and material cost.
6. Add a regression budget only when the repository can run it reproducibly.
   Do not create a noisy performance gate.

Protected invariant: external semantics and correctness remain intact unless the
user explicitly approves a tradeoff.

Proof for mutation: comparable before/after measurement plus correctness and
regression checks for the changed radius. For review/design, provide traceable
bottleneck evidence, measurement limits, proposed experiments, and decision
criteria without claiming improvement.
