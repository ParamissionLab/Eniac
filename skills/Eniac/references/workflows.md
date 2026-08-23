# Workflows

Step chains for each route in SKILL.md. Every chain ends in a proof, because a route
that cannot close is not finished.

Load only the one section matching the route you selected — they are independent, and
reading the others costs you the budget the route was supposed to save.

> **Owns** — the step chain per route — diagnose, incident, implement, refactor, greenfield, full-cycle, review, audit, batch, product UI, ship — and the overlay triage table.
> **Defers** — specify and design → `lifecycle.md`; optimize → `performance.md`; document → `documentation.md`; a quality pass whose target is the whole repository rather than a change → `code-health.md`; and each overlay's depth to the file its row names.

## Contents

- [Diagnose](#diagnose) — something is broken, cause unknown
- [Incident](#incident) — production is broken right now
- [Implement](#implement) — build the requested thing
- [Refactor](#refactor) — restructure without changing behavior
- [Greenfield](#greenfield) — new project from nothing
- [Full-cycle](#full-cycle) — discover through ship
- [Review](#review) — judge a diff or existing code
- [Audit](#audit) — understand an unfamiliar system
- [Batch](#batch) — many small mechanical edits
- [Product UI](#product-ui) — a user-facing screen, page, or flow
- Optimize — something is measurably slow; the chain for it lives in `performance.md`
- Document — docs are the deliverable; the chain for it lives in `documentation.md`
- Health scan — the whole codebase is the target; the chain for it lives in `code-health.md`
- [Ship](#ship) — release, deploy, migrate
- [Overlays](#overlays) — performance, security, data, contracts, deps, concurrency, observability

---

## Diagnose

1. **Reproduce.** Get a command that fails on demand. If you cannot reproduce it,
   that is the first bug — say so instead of guessing at a fix.
2. **Freeze the signal.** Exact error text, exact input, exact commit and
   environment. A vague symptom produces a vague fix.
3. **Localize.** Halve the search space each step, not the line count: which layer,
   which commit (`git log -S`, `git bisect`), which input, which config. Binary
   search beats reading.
4. **Hypothesize.** Write two or three competing causes *before* investigating the
   first one — the first hypothesis anchors everything after it, and later evidence
   gets read as an adjustment to it rather than on its own terms. For each, name the
   observation that would rule it *out*. A hypothesis with no falsifier is a belief.
5. **Discriminate.** Run the cheapest experiment that kills the most hypotheses.
   Instrument at the boundary between suspects, not everywhere.
6. **Fix at the cause, minimally.** Ask *why* of each answer until you reach something
   you can change that would have prevented the links above it, keeping every "because"
   an observation rather than a belief (`reasoning.md#ask-why-until-it-is-actionable`).
   Before writing a guard, answer where the bad value came from — a purely additive change at the point of failure is a symptom fix until
   argued otherwise (`defenses.md#symptom-substitution`). If only a symptom fix is
   possible right now, say so explicitly, name the real cause with an owner, and make
   the mitigation visibly temporary in the code rather than a silent guard the next
   reader takes for design.
7. **Lock it.** Add a check that fails on the old code and passes on the new.
   Without this the bug comes back and nobody knows why.
8. **Sweep.** Does the same cause exist elsewhere? Report siblings; fix only those
   in scope. Once the answer is *yes, several* this stops being the last step of one
   diagnosis and becomes its own problem — `defect-sets.md`.

**Anti-patterns:** changing more than one thing per experiment; adding logging
everywhere instead of at the decisive boundary; "try this and see"; declaring
victory because the error message changed rather than disappeared.

**Hard bugs** — intermittent, heisenbug, works-on-my-machine — are almost always
state you are not looking at. Enumerate the candidates explicitly: time and
timezone, ordering, concurrency, caching, environment variables, locale, filesystem
case-sensitivity, network, RNG seed, uninitialized or leftover data. Then make the
suspect state explicit and control it.

---

## Incident

A live production failure inverts the normal order: **restore service first, understand
second.** Diagnosing before mitigating is the most common way a short outage becomes a
long one.

1. **Assess before cause.** What is broken, for whom, how badly, since when. Blast radius
   and start time are what decide everything next; the cause is not yet relevant.
   Severity decides who gets woken and how much process applies — see
   `enterprise.md#incident-severity-and-postmortem`.
2. **Mitigate.** Roll back, fail over, disable the feature, shed load, scale out. The
   fastest safe restoration wins even if it is inelegant and even if you still do not
   know why it broke.
3. **Preserve evidence first, if it costs seconds.** Logs, metrics, one failing request,
   the current configuration, the deploy that preceded it. Mitigation frequently destroys
   the evidence you will need — rotated logs and restarted processes take their state
   with them.
4. **Communicate state, not theories.** What is broken, what is being done, when the next
   update comes. Speculation broadcast during an incident becomes fact in someone's head.
5. **Then diagnose** with the [Diagnose](#diagnose) chain, using the evidence you kept.
6. **Two corrections, not one:** fix the cause, and separately fix whatever let it reach
   production. The second is the one that prevents the next incident.

Containment is never a fix. Label it explicitly as temporary with a named owner, or it
silently becomes the permanent architecture.

An incident is **L4 by default** — rollbacks, failovers, traffic changes, and flag flips
are external effects on a system other people depend on. Involve a human early, and act
unilaterally only within whatever authority has already been granted.

---

## Implement

1. **Restate the outcome** in one line, including what is out of scope.
2. **Find the seam.** Where does this belong in the existing design? Read one
   neighbor that already does something similar and match it. New code that ignores
   local convention is a permanent maintenance tax.
3. **Contract first.** Signature, inputs, outputs, error behavior, and the one
   invariant that must hold.
4. **Thin slice.** Make the smallest end-to-end path work through the real entry
   point before widening. One vertical slice that runs beats four horizontal layers
   that do not.
5. **Prove the behavior.** A check that fails before and passes after. When
   test-first is viable, use it — it is the cheapest way to know the test tests
   anything at all.
6. **Widen.** Edge cases, error paths, and the states the API or UI can actually
   reach.
7. **Integrate.** Run the surrounding suite. Check the callers whose shape you changed.
8. **Close** with Done / Changed / Verified / Risks / Next.

**Judgment calls that separate senior from average work:** match the repository's
existing patterns over your preferred ones; handle errors the way the neighbours do;
do not add a dependency to save twenty lines; do not build the general case before
the second caller exists; and delete the code you replaced rather than leaving both.

---

## Refactor

Refactoring means behavior does not change. If behavior changes, it is a rewrite and
it needs a different conversation with the user first.

The strongest reason to refactor is not tidiness — it is that a needed change is hard in
the current shape. Reshape first with behavior unchanged, then make the now-small change:
two steps, separately reviewable and separately revertible. See `craft.md`.

1. **Lock the contract** — write down exactly what behavior is preserved.
2. **Build the safety net first** — characterization tests that pass on the *current*
   code. Without a net this is not refactoring, it is redecorating in the dark.
3. **Draw the boundary** — which files may change. Everything else is read-only for
   the duration.
4. **Move in verified waves** — beyond about ten files, batch by one mechanical rule
   and verify each wave; past roughly twenty, write the transform as a script rather
   than editing by hand (`campaigns.md`). One giant edit offers no bisection point
   when it breaks.
5. **Never mix** behavior change with restructuring in the same step or commit.
   Mixing them makes review impossible and hides regressions inside noise.
6. **Report adjacent defects** instead of quietly fixing them.
7. **Prove** — same tests, same results, plus one spot check through the real entry
   point, because a test suite can share the same blind spot as the code.

---

## Greenfield

1. **Contract.** Who uses it, the one job it must do, what "working" looks like, and
   what is explicitly out of scope.
2. **Stack.** Choose from what the user already has and knows, and what the target
   environment supports. One line of defence each for language, framework, storage,
   deployment. Boring beats clever; the user maintains this after you leave.
3. **Skeleton.** The thinnest thing that runs end to end: entry point → one real path
   → one real output, committed. Do this before any feature.
4. **Slices.** One capability at a time, each ending with something the user can run.
5. **Harden.** Error paths, input validation, secrets handling, logging.
6. **Handover.** A README a stranger can follow: install, run, test, deploy, layout,
   and the decisions someone would otherwise re-litigate.

**Traps:** scaffolding a framework's full opinionated tree when four files would do;
choosing infrastructure before the first feature exists; building a configuration
system before there are two configurations; adding auth, Docker, and CI to a script.

---

## Full-cycle

Discover → Plan → Build → Test → Harden → Document → Ship. Each phase ends with a
signal, not a feeling. Report at phase boundaries, not inside them.

This chain starts once it is settled *what* is being built. When that is not settled — no
checkable done condition, or more than one shape would work — `lifecycle.md` carries the
two phases that come first, and the map of which route closes which phase.

- **Discover** — what exists, what runs today, what the conventions are.
- **Plan** — milestones each bound to observable proof. Write it to a file once there
  are more than two, or the work will outlive the context window.
- **Build** — the Implement chain per slice, WIP 1.
- **Test** — unit for logic, integration for seams, one real end-to-end path.
- **Harden** — failure paths, input handling, plus performance or security only where
  evidence says they matter.
- **Document** — only what changes a reader's action: how to run it, how to extend it,
  and what surprised you. Where each of those facts belongs, and how to avoid growing a
  second copy of one that already exists: `documentation.md`.
- **Ship** — see [Ship](#ship).

---

## Review

Outcome first, style last. Reviewing style before correctness is how real bugs ship.

1. **Intent.** What was this supposed to do? Read the tests and the entry point before
   the diff.
2. **Correctness.** Attack the failure case, not the happy path: boundaries, nulls and
   empties, error swallowing, resource leaks, concurrency, partial failure.
3. **Blast radius.** Who calls this, which contracts moved, what data shape changed,
   what is now silently different for an existing caller.
4. **Proof.** Do the tests actually exercise the change, or merely run near it?
5. **Then** simplification, duplication, and convention.

Finding shape, severity honesty, the two legitimate baselines for judging code, and
the list of things that are *not* findings are in `findings.md` — load it whenever the
output is a set of findings rather than a change. When the review is about structure rather
than a diff — boundaries, coupling, convention drift — `architecture.md` names the
dimensions to look along.

Every finding needs file:line, what breaks, a concrete failure scenario, and a
suggested fix. A finding with no failure scenario is an opinion — label it as one or
drop it. Verify a suggestion against the real code before offering it; a confidently
wrong review costs more than no review.

When receiving review feedback, check the claim against the system before agreeing or
defending. Agreeing with a wrong review is as expensive as ignoring a right one.

When the target is not a diff but the whole repository — *review the project*, *find
everything wrong with it* — this is not a bigger review. It has no bounded surface and no
scope gate, and both have to be set before reading: `code-health.md`.

---

## Audit

Scope before reading. Reading everything is almost never the cheapest way to
understand anything.

- **Scan** — bounded orientation, default.
- **Focus** — one module, flow, or boundary that the task actually touches.
- **Full** — whole system, only on explicit request or evidenced impact across three
  or more interacting modules.

1. **Inventory** — manifests, entry points, configuration, scripts, test layout.
   The cheapest orientation available.
2. **Map** — responsibilities, data flow, boundaries, external dependencies.
3. **Trace** — follow one real request or task end to end. One traced flow teaches
   more than ten skimmed files.
4. **Findings** — keep fact, inference, assumption, and recommendation visibly
   separate. A handoff built on blurred inference is worse than no handoff.
5. **Blast radius** for anything you propose.

Mapping never authorizes redesign, and a sensitive topic alone never forces Full. When an
audit turns into "and fix what you find", it has become a different route with a different
gate — `code-health.md`.

Steps 2 and 4 are where this route is usually weakest. `architecture.md` carries what to
look *for* — the five assessment dimensions, how to trace a flow before calling it a
conflict, using a codebase graph as evidence without letting it pre-judge, the named
artifacts, and diagram discipline. Load it whenever the deliverable is a map or an
assessment rather than a quick orientation.

For how to label claims, when to write `None identified`, how to declare that no pass
was needed at all, and the artifact budget per depth, use `findings.md`.

---

## Batch

1. **One rule** that decides every case. If each file needs judgment, this is not a
   batch — it is many small tasks.
2. **Enumerate** the full target set and state the count before starting.
3. **Pilot** two or three by hand, verify, and confirm the rule survives contact.
4. **Apply in groups**, verifying per group.
5. **Handle exceptions separately** and list them explicitly.
6. **Broad check** at the end.

A batch that quietly becomes a redesign is the most expensive failure in this route.

---

## Product UI

When the work touches a user-facing surface, correctness is necessary and not
sufficient — to the person using it, the interface *is* the product.

1. **Fit the product type.** An internal operations tool, a marketing page, and a data
   dashboard have different bars. Dense and fast beats beautiful for something someone
   stares at for eight hours; the reverse holds for a page seen once.
2. **Design the states, not just the ideal screen.** Empty, loading, partial, error,
   too-much-data, and no-permission are the states users actually hit. A screen designed
   only for perfect data breaks on first contact with real data.
3. **Systematize before styling.** A type scale, a spacing scale, and a small color set,
   applied consistently. Ad-hoc values chosen per component is what makes an interface
   feel amateur even when each screen looks fine in isolation.
4. **Hierarchy carries meaning.** The most important thing should be the most prominent.
   When everything is emphasized, nothing is, and the user has to do the ranking you
   were supposed to do.
5. **Engineer the responsiveness.** Check real breakpoints with real content lengths —
   long names, empty fields, ten items and a thousand — not placeholder text at one width.
6. **Accessibility is correctness, not polish.** Keyboard reachable, focus visible,
   labels present, contrast sufficient, and never colour alone to carry meaning.
7. **Verify by walking the actual flow** the user came to complete, start to finish.
   Component-by-component checking misses exactly the problems that matter.

**Anti-slop check** — these read as machine-generated and undermine trust in the work:
gratuitous gradients and glows, emoji standing in for icons, everything centered, a hero
section on an internal tool, animation that delays the task, three typefaces, and
decorative colour that encodes nothing. Restraint reads as competence.

This chain makes an interface correct. When the *appearance itself* is part of the
deliverable — a marketing or landing page, a redesign, a brief that says design, look,
feel, or brand — correctness is the floor rather than the goal, and
`interface-design.md` carries the rest: settling the palette, type, layout, and signature
element before any CSS exists, avoiding the handful of looks every generated design
converges on, and writing interface copy as design material rather than filler.

---

## Ship

**Preconditions:** tests green or a stated and accepted baseline; the change works
through its real entry point; rollback known; no secrets in the diff.

1. Confirm authorization for the target environment. Production is L4 — ask.
2. Dry run or preview wherever the tool offers one.
3. Smallest safe increment, watching a real signal after each.
4. State the rollback path *before*, not discovered after.
5. Post-check actual behavior in the target environment, not just the deploy exit code.

**Migrations** must be reversible and idempotent, tested on a copy, with row counts
before and after and a plan for failing halfway. Use expand → migrate → contract, and
never compress those into one release.

---

## Overlays

Load an overlay only when inspected evidence makes it material. An ordinary task does
not inherit every specialty, and topic anxiety is not evidence.

| Overlay | Triggered by | Check | Proof |
| --- | --- | --- | --- |
| **Performance** | a measured complaint, a profile, an SLA | measure before optimizing; find the actual hot path — `performance.md` | before/after number beating run-to-run variance |
| **Security** | auth, input from outside, secrets, uploads, serialization | trust boundaries, authz on every path not just the UI, injection surfaces, dependency CVEs — `security.md` | a check that exercises the abuse case |
| **Model calls** | generation, extraction, retrieval, a tool-using agent | pinned model and prompt versions, untrusted content kept out of the instruction position, output validated before use — `llm-systems.md` | an eval set that runs on every prompt or model change |
| **Data migration** | schema or persisted-shape change | reversibility, idempotence, partial-failure plan | run on a copy, row counts before and after |
| **API contract** | a public signature, response, or event changes | additive first; version or deprecate rather than break; every known consumer | contract test against the old shape |
| **Dependencies** | add, remove, or bump | changelog across the crossed range, lockfile diff, license, maintenance signals | full suite plus the feature that uses it |
| **Concurrency** | threads, async, queues, shared state | name the shared state, the ordering assumption, and the failure under interleaving — `craft.md#concurrency` | stress or deterministic scheduling, not hope |
| **Observability** | anything that can fail unseen in production | error surfaces, one metric, a log line with a correlating id | trigger the failure and confirm you can see it |

Blanket debug logging is not observability, and a `try/except` that hides the error is
the opposite of it.

These rows are triage, not depth. When an overlay is genuinely the work rather than a
side condition, go to the file that carries it: `security.md` for trust boundaries,
authorization paths, and injection; `llm-systems.md` for anything built on a model;
`production.md` for performance under real load, observability and alerting, resilience per
remote call, and large-table data operations; `enterprise.md` for regulated data, tenant
isolation, least privilege, and supply chain; `campaigns.md` for the migration and rollout
sequences themselves.
