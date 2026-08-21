# Performance

Performance work without measurement is guessing, and guessing produces complexity that
never pays for itself. The discipline is a loop, and the step teams skip is the fourth.

```text
MEASURE  → establish a baseline on representative data
IDENTIFY → find the actual bottleneck, not the assumed one
FIX      → address that specific bottleneck, one change
VERIFY   → measure again, the same way; keep or revert
GUARD    → add the check that stops the regression coming back
```

Load this when performance is the work — a stated budget or SLA, a measured complaint, a
suspected regression, or a feature meeting large data or high traffic. Do not load it to
make code "faster" with no evidence anything is slow.

## Measure First

- **Baseline before touching anything.** Without it there is no way to tell improvement
  from noise, and no way to tell a regression you caused from one that was there.
- **On production-shaped data.** A profile over 100 rows describes a different program
  than the one running over 100 million. Data volume, distribution, cardinality, and
  cache warmth all change which line is hot.
- **Synthetic and real user data answer different questions.** Synthetic (a profiler, a
  benchmark, a controlled run) is reproducible and good for isolating a cause and for CI.
  Real user or production measurement is the only thing that proves users benefited.
- **Record the exact command and conditions.** You will need to reproduce them precisely
  at the VERIFY step, and a baseline you cannot reproduce is not a baseline.

## Start Measuring From The Symptom

The symptom narrows what to measure first. Measuring everything is how a day disappears.

```text
What is slow?
├── First load of a page or app
│   ├── slow server response      → time to first byte; then profile the handler
│   ├── large payload or bundle   → transfer size; splitting and lazy loading
│   └── blocking resources        → the network waterfall, what blocks render
├── Interaction feels sluggish
│   ├── freezes on action         → main-thread long tasks
│   ├── input lag                 → redundant re-renders, work on every keystroke
│   └── visual jank               → layout thrash, forced synchronous reflow
├── One API or endpoint
│   ├── consistently slow         → query log first: N+1, missing index, full scan
│   ├── slow only sometimes       → lock contention, GC pauses, a slow dependency
│   └── slow under load only      → connection pool, queue depth, saturation
└── Everything is slow
    └── shared resource           → CPU, memory, connection pool, disk, replica lag
```

The single highest-yield check in most systems is the query log. N+1 access patterns and
a missing index dominate real-world slowness, and both are visible in seconds.

## Optimize In This Order

The ranking is almost always the same, and jumping to the bottom is the classic waste.

1. **Do less work** — a better algorithm, less data fetched, work moved off the request
   path, a cache with a correct invalidation story.
2. **Fewer round trips** — one query returning 500 rows beats 500 queries returning one.
   The same applies to remote calls, file reads, and per-item work of any kind.
3. **Better IO** — the missing index, the full scan, the unbounded result set, the query
   that was fine at 10k rows and is not at 10M.
4. **Then** allocation, serialization, and micro-optimization.

Caching buys latency by taking on a correctness problem. Before adding one, know the
invalidation story and how stale the product can tolerate being.

## Verify: Keep Or Revert

A fix is a hypothesis until re-measured. This step is where the discipline actually lives.

- **Re-measure the same way** — same command, same conditions, same fixed budget. A cold
  baseline against a warm result measures the cache, not the change.
- **One change at a time.** Three optimizations landed together produce one number that
  cannot be attributed to any of them.
- **Beat the noise, not the mean.** Repeat the run and compare the delta against
  run-to-run variance. A 3% gain inside ±5% variance is a different sample, not a gain.
- **Correctness gates the metric.** A "win" that skipped a validation, cached something
  that had to be fresh, or removed a load-bearing `await` is a regression wearing a win's
  clothing. If a test had to be changed, skipped, or deleted to make the number move,
  the number does not count.

| Result | Action |
| --- | --- |
| Past the threshold, tests green | **Keep** — commit with the before and after numbers |
| Inside the noise | **Revert** |
| Worse | **Revert** |
| Better, but a test went red | **Revert** |

**Neutral is a revert, not a keep.** This is the rule that gets broken, and always for the
same reason: the change is already written, discarding it feels wasteful, so it lands
unmeasured. The measurement does not care how long it took to write. Code you keep, you
maintain forever — make it pay for itself.

## Log The Attempts, Especially The Reverted Ones

Reverted work leaves no trace in history, which is exactly why the same dead idea gets
tried again next quarter by someone who was not there.

| Idea | Baseline → Result | Verdict | Why |
| --- | --- | --- | --- |
| Memoize the row component | 240ms → 235ms | reverted | inside noise; rows were not the bottleneck |
| Virtualize the list | 240ms → 90ms | kept | long tasks gone from the trace |
| Preconnect to the API origin | 2.8s → 2.8s | reverted | already same-origin |

A section in the pull request or a short file in the repository both work. What matters is
that the next person reads it before proposing an experiment that already failed.

## Guard The Win

An optimization with no guard is temporary. Whatever made the code slow will be
reintroduced by someone who does not know the history.

- A budget enforced in CI — bundle size, query count, response time, benchmark threshold.
- A test that fails on the anti-pattern returning, such as an assertion on query count.
- A production metric with an alert, when the regression would only appear under real load.
- A comment at the non-obvious line explaining why it is written that way, so the next
  reader does not "clean it up".

Budgets are only useful if something fails when they are exceeded. A documented budget
nobody enforces is a wish.

## Rationalizations

Each of these is a defense mechanism from `defenses.md` wearing performance vocabulary.

| Said | Reality |
| --- | --- |
| "We will optimize later" | Anti-patterns compound. Fix the obvious ones now; defer micro-optimization, not N+1s. |
| "It is fast on my machine" | Your machine is not the user's, and your dataset is not production's. |
| "This optimization is obvious" | If you did not measure, you do not know. Obvious ones are cheap to prove. |
| "It did not help much, but it does not hurt" | It costs maintenance forever and bought nothing. Revert. |
| "We already wrote it, may as well keep it" | Sunk cost. The measurement does not care what it cost to write. |
| "The improvement is obvious, no need to re-measure" | Then re-measuring is cheap and settles it. |
| "The framework handles performance" | Frameworks prevent some classes of problem. They do not fix your query patterns. |

## Red Flags

- Optimization with no profiling data behind it.
- N+1 access patterns; list endpoints with no pagination.
- Unbounded queries, unbounded caches, unbounded result sets.
- Several changes bundled into one measurement.
- A win that required a test to be changed, skipped, or deleted.
- Memoization applied everywhere — overuse costs as much as underuse and hides the real cause.
- The same failed optimization attempted twice because nobody recorded the first.
- No monitoring in production, so the first report of a regression comes from a user.
