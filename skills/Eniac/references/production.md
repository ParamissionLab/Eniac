# Production

Code that is correct on a laptop and code that survives production are different
artifacts. The difference is not quality — it is that production has concurrency,
partial failure, real data volumes, hostile inputs, other people's outages, and no
one watching at 3am.

Load this when work touches a running system, or when a change will meet real traffic.

> **Owns** — systems meeting real traffic — environment differences, the four resilience questions per remote call, third-party dependencies, observability that works, SLOs and error budgets, load, data operations at scale, runbooks, infrastructure cost.
> **Defers** — finding and fixing a specific bottleneck → `performance.md`; the incident step chain → `workflows.md#incident`; organizational and regulatory constraints → `enterprise.md`.

## Environments Are Not Copies Of Each Other

"It works in staging" is evidence about staging. Staging almost always differs in data
volume and distribution, concurrency, network topology, cache warmth, third-party
sandbox behavior, and configuration — and every one of those has caused an outage.

- **Configuration is code with no type checker and no tests.** Most incidents attributed
  to a deploy are configuration differences, not logic. Diff the config, not just the diff.
- **Secrets differ per environment by design.** A change that works because a staging key
  has broader permissions will fail in production, which is the correct outcome.
- Name explicitly which environment a result came from. A verification that does not
  say where it ran is a claim about nowhere.

## Resilience: Four Questions Per Remote Call

Every call that leaves the process needs an answer to all four. Most production
fragility is one of these left unanswered.

1. **Timeout** — what is the deadline? A call with no timeout is an unbounded outage
   waiting for its dependency to hang. Default library timeouts are usually far too long
   or absent entirely.
2. **Retry** — is this safe to retry, and how? Retries need exponential backoff *with
   jitter* (synchronized retries are how a blip becomes a thundering herd) and a total
   budget. Retrying a non-idempotent write duplicates it.
3. **Idempotency** — if this runs twice, what happens? At-least-once delivery is the
   norm in queues, webhooks, and retried HTTP. An idempotency key, a natural unique
   constraint, or a conditional write turns a duplicate into a no-op.
4. **Degradation** — what does the caller do when this fails? Failing the whole request
   because a non-essential enrichment call timed out is a choice, and usually the wrong one.

**Circuit breakers** stop a failing dependency from consuming all your capacity in
timeouts. **Bulkheads** — separate pools, queues, or concurrency limits per dependency —
stop one slow dependency from starving everything else. Both are cheap and both are
missing until the first outage teaches otherwise.

## Third-Party Dependencies

**Their availability is your availability**, unless you designed otherwise. Before
depending on an external service, know its rate limits, its actual latency
distribution rather than its advertised one, and what your system does when it is down
for an hour.

- Rate limits are per-account and shared across your whole fleet. Local testing will
  never reveal the limit that production hits.
- Verify webhook signatures, and treat webhook delivery as at-least-once and
  out-of-order. Store the event id and ignore repeats.
- Never trust an external response shape without validation. Their non-breaking change
  is your outage.

## Observability That Works

The test of observability is a single question: **when this fails at 3am, can someone
who did not write it find out why without a debugger?**

- **Instrument the request, not the function.** Rate, errors, and duration per endpoint
  or job — plus saturation of every bounded resource: pool, queue, memory, disk,
  connection count.
- **Structured logs with a correlation id** that follows a request across services. An
  unstructured log at scale is a text file nobody can query.
- **Cardinality is the cost trap.** A label containing a user id, request id, or URL with
  parameters will multiply time series until the metrics bill or the metrics system
  breaks. Ids belong in logs and traces, never in metric labels.
- **Alert on symptoms, not causes.** "Checkout error rate above 2%" is actionable;
  "CPU above 80%" is usually not, and pages nobody can act on train everyone to ignore
  the pager — after which the real alert is also ignored.
- Every alert needs an owner and a runbook, or it should not exist.

Blanket debug logging is not observability, and a `catch` that logs and continues is
the opposite of it.

## SLOs And Error Budgets

An SLO makes reliability a number instead of an argument. It defines what "working"
means for users and how much failure is acceptable over a window.

The useful consequence is the **error budget**: if the budget is intact, ship faster; if
it is spent, reliability work outranks features until it recovers. This converts
"should we ship this risky change" from a personality contest into a measurement.

When a change would consume a meaningful share of the budget, that is a fact the user
needs before deciding, not after.

## Performance Under Real Load

The measurement discipline — where to start from a symptom, the optimization order, and
the keep-or-revert rule — is in `performance.md`. Three things are specific to production:

- **Systems fail at the tail, not at the mean.** Track p95 and p99. An average latency
  that looks healthy routinely hides a p99 that is timing out for a real subset of users.
- **Load-test the shape of real traffic** — bursts, hot keys, an uneven tenant
  distribution — not a uniform average. Uniform load is the one pattern production never
  produces.
- **Saturation is the leading indicator.** Latency degrades gently until a bounded
  resource fills — pool, queue, memory, file handles — and then it collapses. Watch
  utilization of every bounded resource, not just response time.

## Data Operations At Production Scale

Operations that are instant on a development database are outages on a large table.

- **Locking is the danger, not duration.** A migration that locks a hot table for thirty
  seconds is an outage. Use the online / concurrent path your database offers, and know
  which operations rewrite the table.
- **Batch and throttle every backfill.** Bounded batches, a pause between them, and a
  stop switch. Watch replica lag while it runs — saturating replication breaks reads
  everywhere else.
- **Make backfills resumable and idempotent.** They will be interrupted, and restarting
  from zero on a 500-million-row table is not an option.
- Adding a column with a default, adding an index, changing a type, and adding a
  constraint each behave differently per engine and per version. Check the specific
  behavior for the version actually running.
- Test on a production-sized copy. Row counts before and after. A reversal that was
  actually tried.

## Runbooks

Any change that introduces a new way to fail operationally deserves one. Six lines:

```text
Symptom:    what someone will see or be paged for
Impact:     who is affected and how badly
Check:      the command, query, or dashboard that confirms it
Mitigate:   the fastest safe restoration
Fix:        the real correction
Escalate:   who to wake, and when it is worth it
```

Write it while the knowledge is fresh. Nobody reconstructs this at 3am.

## Cost

Cloud cost is a production property with the same standing as latency. A query, a
retry policy, a log line, or a metric label can each multiply spend without changing
behavior. When a change materially affects cost — a new always-on resource, a
high-cardinality metric, an egress-heavy path, a retry storm — say so, because that
number belongs to someone and it will be noticed later rather than never.
