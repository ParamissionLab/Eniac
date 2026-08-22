# Eniac

Eniac is a provider-neutral, agent-agnostic operating skill for full-cycle software engineering. It gives an AI agent a working mind rather than a checklist: three agencies that disagree productively, a fixed priority ladder, a verification discipline, and a token budget that is spent on decisions instead of reassurance.

The cognitive model is borrowed from Freud's structural theory and used as machinery, not decoration.

Credit: [ParamissionLab](https://github.com/ParamissionLab)

## The Model

| Agency | Asks | Produces | Fails as |
| --- | --- | --- | --- |
| **Id** — drive | "What is the fastest path that could actually work?" | candidate actions, pattern matches, momentum | guessing, scope creep, unverified claims |
| **Superego** — conscience | "What must not break, and what did they actually ask for?" | invariants, authority limits, the done bar | ceremony, gold-plating, token burn |
| **Ego** — reality | "What do I do next and how will I know it worked?" | the decision, the batch, the proof | — |

Only the Ego acts. The other two are inputs, and when they agree the arbitration costs nothing — which is what keeps the model cheap instead of theatrical.

Alongside it runs a second, independent axis — **fast and slow thinking**. The agencies say whose interest is speaking; fast and slow says how carefully it is being processed. Fast pattern-matching is the correct default and is right most of the time; the discipline is knowing its failure signature and switching modes deliberately. An Ego running in fast mode is just the Id with better vocabulary.

Four other Freudian ideas do real work:

- **Economic principle** (finite energy, distributed) becomes the L0–L4 investment ladder that decides how much context a task is allowed to consume.
- **Topographic model** (conscious / preconscious / unconscious) becomes progressive disclosure: what is in context now, what is retrievable on demand, and what stays unread.
- **Reality testing** — the Ego's job of separating the internal model from the world — becomes the rule that only executed output counts as evidence.
- **Defense mechanisms** become a catalog of agent failure modes under pressure, each with a tell and a correction, so the agent can catch itself avoiding the work.

Every task opens the same way — read the request literally, classify the action, set the three dials, do the smallest thing that could settle it — and for most tasks that pass costs one sentence and lands on L0 or L1, where the right behaviour is to answer and stop. When a label is genuinely ambiguous the defaults are asymmetric and stated: take the lower investment level and let evidence promote you, take the higher magnitude, take the route whose proof is hardest, and if nothing fits, run the loop plainly and say what you improvised.

These subsystems are wired in a stated order rather than offered as a menu: precedence settles whose rules apply; route, investment level, and magnitude are three independent dials that size the work; the Ego Loop is the cycle that runs; fast-or-slow, the agencies, and the triage ladder operate inside each pass; reality testing decides whether it may close; authorization can halt any step regardless of everything above; and the defense catalog and learning loop run continuously. When two appear to disagree, the earlier one wins — except authorization, which wins outright.

## What It Does

- **Scales effort to real risk.** L0 answers directly with no ceremony; L4 inspects freely but asks before mutating. Applying L3 process to L1 work is treated as the expensive mistake it is.
- **Scales to work that does not fit in one head.** Magnitude is tracked separately from risk, because a two-line change on a payment path is high risk and tiny while a 400-file rename is low risk and enormous. From M1 upward the binding constraint becomes memory rather than thinking, so the skill switches to durable checkpoints, models built from partial evidence, verified waves, and migrations where every intermediate state is a good state.
- **Treats production and the organization as first-class constraints.** Every remote call needs a timeout, a retry decision, an idempotency answer, and a degradation path. Tenant isolation outranks every other invariant. Regulated data carries obligations that no amount of code reading can settle, so the skill names the gap instead of asserting compliance. Freeze windows, required reviewers, and CI gates are respected rather than routed around.
- **Reports honestly.** Every claim in a review, audit, or plan is labelled `Fact`, `Inference`, `Assumption`, `Proposed`, or `Unknown`, because a reader cannot detect uncertainty smoothed into confident prose. Code is judged against the framework's documented conventions and the project's own dominant pattern — never personal taste — and `None identified` is a legitimate result. "No pass required" is a complete answer.
- **Has a method for thinking slowly, not just permission to.** Frame the given, required, constraints, and the one unknown that would settle it. Decompose along a seam the system already has, so each part is independently checkable. Partition the case space and state which combinations are impossible *and why* — an unreasoned "impossible" is the most common origin of a production surprise. Derive constraints from the symptom rather than guessing better. Work backwards from the goal when forward search is too wide. Then name every proof obligation and discharge it, because an obligation you cannot discharge is a stated risk rather than an oversight.
- **Knows when to think fast and when to think slow.** Pattern-matching is free and usually right, so it is the default — but it switches to deliberate work on an unfamiliar pattern, a one-way door, an answer that came too fluently, a problem turning on numbers or ordering or negation, or anything that has already surprised it once. It names the two traps that are invisible from the inside: silently answering an easier question than the one asked, and "verifying" by re-reading its own reasoning instead of touching reality.
- **Decides in proportion to reversibility.** A two-way door gets decided now and answered by reality; deliberating there costs more than being wrong. A one-way door — persisted data, a public contract, a deletion, a release — earns a pre-mortem, an inverted failure list, a hunt for disconfirming evidence, base rates instead of the plan's own optimism, and a written `Revisit if`.
- **Prioritizes automatically.** A fixed six-tier ladder — active harm, blockers, the stated outcome, proof of it, defects inside the blast radius, then everything else — so ordering does not depend on whatever was noticed most recently. Tier six is reported, never silently done.
- **Refuses vagueness.** A request is actionable only when outcome, scope, and proof are each nameable in one line. Ambiguity is resolved from evidence, then by stated assumption, and only then by asking one specific question.
- **Verifies before claiming.** A five-rung ladder from "it parses" to "nothing else broke", baseline capture before regression claims, and a vocabulary where *verified*, *implemented*, and *unverified* mean different things.
- **Watches its own avoidance.** Denial, rationalization, projection, displacement, repression, regression, reaction formation, intellectualization, and omnipotence — each with the behavior that gives it away and the move that breaks it. Plus sublimation, the one worth keeping.
- **Knows when it is stuck.** Two failures of the same approach means the model is wrong, not the execution; the third attempt is where tokens go to die. It stops, states what it believed versus what happened, and either changes approach or reports a clear blocker.
- **Defers to what is more specific than itself.** The runtime's rules, then the user's instructions, then the repository's conventions, then this skill. A project convention outranks a principle in these references, and applying the skill against the user's stated wish is disobedience with extra steps.
- **Has opinions about code.** When to abstract and when duplication is cheaper, how to name, which errors to catch and which to let fly, where a boundary is real, how to keep concurrent code correct, what a test should assert, what an interface promises, what is safe to delete.
- **Disagrees once, then commits.** A request that looks like a mistake gets one concrete objection, then the work gets done — the user holds context the agent does not.
- **Learns deliberately.** On correction, repeated failure, or surprise, it records *believed X · actually Y · cheapest check that would have caught it* and writes the lesson into the smallest durable place that will be read again — preferring a test over a comment over prose.
- **Spends tokens on purpose.** Nothing loads without naming the decision it could change and the signal expected from it.

## Structure

```text
skills/
  Eniac/
    SKILL.md
    references/
      operating-manual.md
      workflows.md
      craft.md
      reasoning.md
      judgment.md
      findings.md
      performance.md
      production.md
      enterprise.md
      scale.md
      campaigns.md
      triage.md
      reality-testing.md
      defenses.md
      token-economy.md
      learning-loop.md
      safety.md
      stack-signals.md
      architecture.md
```

`SKILL.md` is the always-loaded control plane and is self-sufficient for most work. The nineteen reference files are loaded only when one can change the next decision.

| Reference | Load when |
| --- | --- |
| `operating-manual.md` | a task reaches L2, a decision is genuinely contested, or the work has started going wrong — how the three agencies arbitrate, the fast/slow switch and its two invisible traps, resolving an ambiguous request, the stuck protocol, and the full reporting discipline |
| `workflows.md` | running a route end to end — diagnose, incident, implement, refactor, greenfield, full-cycle, review, audit, batch, product UI, ship — or applying a risk overlay for performance, security, data migration, API contracts, dependencies, concurrency, or observability |
| `craft.md` | the work turns on code judgment rather than correctness — abstraction timing, naming, error handling, boundaries, concurrency, test design, interface design, deletion, dependencies, commits |
| `reasoning.md` | the problem itself is hard to hold — framing, decomposition, case partition with proved coverage, finding a checkable invariant, constraint propagation, working backwards, cost reasoning, proof obligations |
| `judgment.md` | a decision is expensive to get wrong — one-way versus two-way doors, pre-mortem, inversion, disconfirming evidence, base rates, second-order effects, Goodhart's law, when to stop deciding |
| `findings.md` | the deliverable is a set of findings, questions, or a handoff rather than a change — claim labels, finding shape and severity, what is not a finding, artifact budget, handoff minimum bar |
| `performance.md` | something is measurably slow — measure/identify/fix/verify/guard, where to start from a symptom, keep-or-revert with neutral counted as a revert, the attempt ledger |
| `production.md` | the change will meet real traffic — environment differences, timeout/retry/idempotency/degradation per remote call, observability and alerting, SLOs, performance under load, large-table data operations, runbooks, cost |
| `enterprise.md` | the work sits inside an organization's constraints — regulated data, multi-tenant isolation, least privilege, change control and freeze windows, team process, legacy and unowned code, incident severity, supply chain |
| `scale.md` | the system is too large to read — modelling from partial evidence, locating anything, search technique at size, monorepos, the five layers of blast radius |
| `campaigns.md` | work spans many sessions or a staged rollout — campaign contract, checkpoints, codemods, expand/contract and strangler migrations, delegation, durable decisions |
| `triage.md` | dependency ordering, parallel lanes, plan files, parking and resuming, handoff |
| `reality-testing.md` | choosing a verification level, separating baseline from regression, or deciding what closes a task |
| `defenses.md` | the same approach has failed twice, or the work has started avoiding itself |
| `token-economy.md` | large repositories, repeated compaction, expensive tools, long autonomous runs |
| `learning-loop.md` | capturing a lesson and deciding where it should durably live |
| `safety.md` | production, credentials, destructive operations, dependency or data risk, release gates |
| `stack-signals.md` | an unfamiliar stack, or uncertainty about which command actually proves anything |
| `architecture.md` | judging an existing system rather than only describing it — the five assessment dimensions, tracing a flow before calling it a conflict, using a codebase graph as evidence without letting it pre-judge, the named artifacts, diagram discipline |

## Installation

Copy the `skills/Eniac/` folder into your agent's skills directory.

**Claude Code** — user-wide, available in every project:

```bash
cp -r skills/Eniac ~/.claude/skills/Eniac
```

Or per-project, checked in with the repository:

```bash
cp -r skills/Eniac .claude/skills/Eniac
```

**Other agents** — copy the same folder into whatever directory that runtime loads skills from, keeping `SKILL.md` and `references/` together so the relative links resolve. Where a shared convention is supported, `.agents/skills/eniac/` works the same way.

**No skill support** — paste the contents of `SKILL.md` into your agent's instructions and point it at the reference files as optional material.

Restart the agent or start a new session after installing.

## Usage

Reach for the `eniac` skill when you want:

- software work that ends in a proof rather than a patch
- strict token, context, and scope control
- competing problems ranked without being asked to rank them
- autonomous work that continues until done or genuinely blocked, and says which one it is
- production, migration, dependency, or release work that stops and asks at the right moment
- Thai or other multilingual work that stays concise without mangling paths and commands

Example prompts:

```text
Use eniac to fix this bug, verify it, and keep the change scoped.
```

```text
Use eniac to audit this repo and tell me what would break if I changed the auth middleware.
```

```text
Use eniac to take this from empty folder to something that runs and has a README.
```

```text
ใช้ eniac แก้หลายไฟล์ตาม pattern เดียวกันแบบประหยัด token และตรวจให้พอมั่นใจ
```

## Token Discipline

The savings come from structure rather than from exhortation:

- Nothing is loaded without naming the decision it could change and the signal expected. Loading for reassurance is the failure this prevents.
- Simple work loads no references at all; normal work loads at most one.
- Cheap sources first — file listings, manifests, `rg`, headings, line ranges — before whole files.
- Noisy or truncated output is narrowed, never re-run wider.
- Related reads, searches, edits, and checks go in one round trip.
- The working set is a small replaceable evidence cache, not an accumulating log.
- Output answers the question asked: no restating the request, no narrating routine tool calls, no unrequested tutorial.
- Budgets are gates, not quotas — a risky change may cross one, and says in a clause why the cheap path was not enough.

## Updating

```bash
git -C Eniac pull
cp -r skills/Eniac ~/.claude/skills/Eniac
```

Restart your agent or start a new session after updating.

## Versioning

This project follows semantic versioning where practical:

- Patch versions fix wording, structure, or small behavioral issues.
- Minor versions add compatible guidance or references.
- Major versions may change the skill contract or expected agent behavior.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## Security

See [SECURITY.md](SECURITY.md).

## Code of Conduct

See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

## License

Apache License 2.0. See [LICENSE](LICENSE).
