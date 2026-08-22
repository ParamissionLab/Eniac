# System Types

Most engineering guidance quietly assumes one kind of system: a service you deploy, watch,
and redeploy in minutes. Under that assumption, "ship a small increment and watch a real
signal" is obvious advice. On a mobile app it takes a week and cannot be undone. On a
customer-installed product it happens whenever they feel like it. On a device in a field,
it may never happen at all.

The kind of system does not change what good work is. It changes **what a step costs, what
proof is available, and which mistakes are recoverable** — which is most of the working
method. Six questions settle it, and they are worth asking on any system, including one
that fits no category.

Load it when the thing being built is not a service you can deploy and watch: an app behind
a store review, software a customer installs on their own schedule, firmware, a data
pipeline, a game, a compiler, a library other people pin. Load it also at the start of
anything greenfield, where these answers decide the architecture. Do not load it for a
change inside a system whose delivery and feedback you already understand.

> **Owns** — how the kind of system changes the method: delivery cost, reversibility, feedback latency, state ownership, what "works" means, and what cannot be observed.
> **Defers** — running services under real traffic → `production.md`; the organization's constraints → `enterprise.md`; release sequencing → `workflows.md#ship`; multi-release change → `campaigns.md`; per-stack proof commands → `stack-signals.md`.

## Contents

- [The Six Questions](#the-six-questions)
- [What Each Answer Changes](#what-each-answer-changes)
- [Common Shapes](#common-shapes)
- [When A System Is Several Kinds At Once](#when-a-system-is-several-kinds-at-once)

## The Six Questions

Ask these once, early, and the rest of the method follows from the answers. They take a
minute and they change more decisions than the choice of language does.

```text
1. Reach       how does a change get in front of a user, and how long does that take
2. Reverse     can it be undone, by whom, and how fast
3. Feedback    when something is wrong, how do you find out — and how long after
4. State       where does the data live, and who owns the copy that matters
5. Works       what does "correct" mean here, beyond "it returned"
6. Blind       what can you never observe from where you are
```

The one that is skipped most often is **6**, and it is the one that decides how much of
your verification is real. If a whole class of failure is invisible to you, no amount of
local testing closes it — the answer is either to make it observable or to say plainly
that it is not covered.

## What Each Answer Changes

### Reach — the cost of one delivery

When delivery is cheap and fast, the correct strategy is small increments watched in
production. When it is slow or gated by someone else, that strategy inverts: batch more per
release, invest much more in pre-release verification, and treat every release as a
milestone rather than a step.

The failure is applying the wrong one. Shipping a half-finished slice to a store-reviewed
app means living with it for a week. Batching a month of changes into one deploy of a
service you could have released daily means a rollback that reverts everything and a
bisection surface nobody can search.

**When delivery is expensive, feature flags stop being optional.** They are how you get
small increments back: ship the code dark, enable it separately, and keep the enable/disable
path faster than the release path.

### Reverse — who can undo it, and how fast

| Reversibility | What the method becomes |
| --- | --- |
| You can roll back in minutes | proceed in small steps, watch a real signal after each |
| You can roll forward only | every change needs a fix-forward plan, and the fix ships as fast as the break |
| The user decides when to update | the old version runs forever — every change is a compatibility problem |
| It cannot be undone at all | the pre-mortem in `judgment.md` is mandatory, and this is `L4` |

**Anything the user chooses to update means old and new coexist indefinitely.** That single
fact drives more design than anything else on this list: your protocol, your schema, your
file formats, and your APIs all need a version field and a rule for what an old peer does
with a new message. Retrofitting that is far more expensive than adding it up front.

### Feedback — the latency between breaking and knowing

Feedback latency is loop latency (`loops.md`) at the scale of the product, and it has the
same consequence: it multiplies. Where it is measured in seconds, a defect is caught by the
next deploy. Where it is measured in weeks — crash reports, support tickets, a customer's
scheduled audit — the defect is in the field the whole time, and the number of affected
users is decided by how long you take to notice, not by how bad the bug is.

Long feedback changes what you build alongside the feature: error reporting that survives a
crash, logs the user can send you, a version stamp in every report, and a way to tell which
build a report came from. On systems where you cannot observe anything at all, the
substitute is a record-and-compare harness built from real inputs, and saying so explicitly
in the report.

### State — who owns the copy that matters

Where the authoritative data lives decides what a mistake costs and what a migration means:

- **You own it** — a bad migration is your incident, and it is recoverable if you took a
  backup. Expand → migrate → contract, always (`campaigns.md`).
- **The user's device owns it** — you cannot inspect it, you cannot fix it, and every
  schema change must be migrated *by code shipped earlier*. Migrations must run offline,
  survive being interrupted, and handle a device that skipped six versions.
- **A customer's installation owns it** — you get one chance per upgrade window, often
  unattended, sometimes on data you have never seen. Idempotence is not a nicety here.
- **It is append-only or externally anchored** — a ledger, an audit log, a published
  artifact, a paid transaction. There is no migration; there is only a new record that
  supersedes.

### Works — what correct means beyond "it returned"

"The request succeeded" is the definition for exactly one family of systems. Elsewhere the
real acceptance criterion is something else entirely, and a test suite that only checks
return values will pass while the product is unusable:

- a frame budget, and the *worst* frame rather than the average
- determinism — the same inputs producing byte-identical output, across machines
- numerical accuracy within a stated tolerance
- staying inside a memory, power, or thermal envelope over days of running
- no growth over a long run: the failure appears on day nine, not in any test
- an ordering or consistency guarantee that only breaks under concurrency
- a legal or regulatory property that no test can establish (`enterprise.md`)

Name this before building, because it decides what a test even looks like. When the
criterion is a distribution rather than a value, one run proves nothing —
`performance.md#verify-keep-or-revert` applies to correctness too.

### Blind — what you cannot see from here

List it explicitly. The device that is offline, the customer network you cannot reach, the
data you are not permitted to look at, the hardware you do not have, the scale you cannot
reproduce, the timing that only occurs on the real target.

Three honest responses, in order of preference: make it observable (a metric, a report, a
crash handler, a diagnostic mode); reproduce it approximately and state the gap; or declare
it uncovered. The dishonest response is testing what you *can* see and reporting that as
though it covered the rest.

## Common Shapes

The answers cluster. This table is orientation, not a taxonomy — a system that fits none of
these rows still answers the six questions.

| Shape | Reach | Reverse | Feedback | Sharpest constraint |
| --- | --- | --- | --- | --- |
| Web service / API | minutes | roll back | seconds | real traffic, partial failure — `production.md` |
| Internal tool | minutes | roll back | ask the user | do not over-build; density beats polish |
| Mobile app | days, gated by review | users update when they like | crash reports, days | every old version runs forever; offline state you cannot inspect |
| Desktop app | user-initiated | user must update | rarely reported | auto-update is a feature you must build and secure |
| CLI or library | package release | consumers pin | issue tracker | the public surface is the whole product — `stack-signals.md#what-breaks-a-contract-in-any-language` |
| Embedded / firmware | OTA or physical | often impossible | none unless built in | resource envelope, field recovery, a bricked unit is permanent |
| Data pipeline | deploy | reprocess if inputs kept | next run, or a wrong number nobody notices | idempotence, backfill, late and duplicate data |
| ML training | a run | retrain | an offline metric that may not predict the real one | reproducibility, data lineage, the metric is a proxy |
| Game / realtime | build or patch | patch | player reports | the worst frame, not the mean; determinism for replay and netcode |
| Distributed / stateful | rolling deploy | version-by-version | metrics plus a long tail | old and new run simultaneously by design |
| Compiler / dev tooling | release | users pin | issue tracker | output correctness across every input; a miscompile is silent |
| Customer-installed | their schedule | their decision | a support ticket, eventually | many live versions, unattended upgrade, unseen data |
| Batch / legacy enterprise | a change window | usually not | the next window, or a reconciliation | fixed formats, a batch window that must not overrun |

## When A System Is Several Kinds At Once

Most real products are. A mobile app has a backend; a data pipeline feeds a dashboard; a
firmware device has a cloud service and a phone app. **Answer the six questions per
component, not per product**, because the answers differ sharply across the boundary — and
the boundary between two different answers is where the hard problems live.

The recurring one: a fast-moving component and a slow-moving one that must keep talking to
each other. The rule is the same every time — **the side that can change quickly absorbs the
compatibility burden**, because the other side cannot. A backend keeps serving the app
version from two years ago; a new protocol is introduced additively and the old one
retired only when telemetry says nobody is on it; a schema change is deployed before the
code that needs it and cleaned up long after.

Write that expectation down where both sides can read it. Nothing in either codebase makes
it visible, and it is the first thing a new team member breaks.
