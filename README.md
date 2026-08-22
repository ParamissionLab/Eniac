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
- **Treats documentation as a deliverable with an owner.** Each durable fact lives in exactly one file and everything else links to it, because two copies drift and once they disagree both have negative value. Uncertainty is marked `UNKNOWN` with the check that settles it rather than smoothed into confident prose, every command written into a doc has been run, and an audit usually ends with *fewer* files.
- **Designs interfaces rather than defaulting them.** When how a surface looks is part of the deliverable, the palette, type, layout, and one signature element are settled before any CSS exists, then each part is tested against a specific question: would this same answer have come out for any other brief in this category? If yes it is a default rather than a choice. Interface copy is treated as design material, and the handful of looks generated design converges on are named so they can be avoided on purpose.
- **Runs on any agent runtime.** The skill names capabilities — read, search, edit, execute — never a vendor's tool or instruction file, and it says what a missing capability costs instead of routing around it silently. Levels, routes, gates, and triage are decisions rather than features, so they behave identically everywhere; what varies is proof, and on a weaker runtime the honest report gets longer rather than shorter. Adapters ship for skill directories, `AGENTS.md`, Cursor rules, and single-instruction-field assistants.
- **Can tell you whether it is actually loaded.** Installing an agent instruction file fails *silently* on every runtime there is — a wrong path or an unrecognized front-matter key produces no error, the file is simply never read, and the agent behaves exactly as though nothing were installed. So the skill answers a bare "what rules are you following?" by naming itself, the eval suite runs that question as a gate before scoring anything, and `install_adapter.py` takes the destination path from the same table that generates the adapters instead of asking anyone to retype it. Without that gate, a failed install reports as *the skill did not help* — and you go rewrite guidance that was never loaded.
- **Carries no version number inside the skill folder.** The version lives in the changelog and the git tag that carries it, so a vendored copy produces no diff when a release happens and nobody edits fourteen files to cut one. The checker enforces it in both directions: the marker is present everywhere, and it is bare.
- **Is a system rather than a folder of files.** Each of the twenty-six references opens by declaring what it *owns* and what it *hands off* to a named neighbour, so when two look plausible the boundary is already written down instead of guessed at — and a future overlap fails the build rather than drifting for a year. `SKILL.md` groups them by the kind of question they answer, so choosing one is a step rather than a scan. The rule the package applies to other people's documentation, it applies to itself.
- **Treats security as a property of the design, not a review at the end.** A trust boundary is anywhere data crosses from somewhere you do not control into somewhere you do — including the ones that do not look like boundaries: an internal queue, a row a user wrote three months ago, a webhook nobody verifies, a third-party API's response. Authorization is checked per path *and per object*, because the most common serious vulnerability in real software is an endpoint nobody guarded behind a button the interface does not show. Injection is recognized as one bug in many costumes — SQL, shell, template, path, XSS, deserialization, prompt — whose only real fix is structural separation. And it never asserts that something is secure or compliant, because that is a claim about the world no code reading supports.
- **Knows that a model call is not an ordinary function call.** Software built on a model has one component that answers differently each time and fails with a well-formed success — truncation, refusal, confident fabrication. So versions get pinned because "latest" is a breaking change nobody reviewed, prompt injection is handled at the authorization layer rather than by instructing the model to be careful, model output is treated as untrusted input to whatever consumes it, and correctness is established by property assertions and an eval set rather than by equality on a string that will drift.
- **Engineers the loop, not just the fix.** Almost all non-trivial work is iteration, so the loop is what gets designed: its latency, which multiplies by every turn you have not had yet and is why *shortening a slow loop beats running it*; its signal, because a turn that cannot change the next decision is a retry rather than an iteration; and its stop, named before the first turn instead of discovered at the tenth. A loop ends *converged*, *exhausted*, or *diverged*, and saying which is part of the report — collapsing them into "done" is how a loop that learned nothing gets reported as one that succeeded.
- **Is checked, not just written.** Structure, size budget, cross-references, adapter sync, and compact-file coverage are enforced by a script and by CI rather than by a checklist someone reads. Behaviour has its own suite in `evals/`, runtime-neutral so a result from one agent is comparable to another, and every case is required to reject a deliberately bad answer — an assertion that always passes makes a suite look green while measuring nothing.
- **Spends tokens on purpose.** Nothing loads without naming the decision it could change and the signal expected from it.

## Structure

```text
skills/
  Eniac/
    SKILL.md
    references/
      operating-manual.md
      lifecycle.md
      workflows.md
      craft.md
      reasoning.md
      judgment.md
      findings.md
      documentation.md
      interface-design.md
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
      collaboration.md
      safety.md
      stack-signals.md
      architecture.md
    adapters/
      _source/core.md            — the one source every rule adapter is generated from
      eniac-compact.md           — hand-written full distillation, one file
      agents-md/ cursor/ copilot/ windsurf/ cline/ zed/
      gemini/ continue/ aider/ junie/ generic/ codex/
scripts/
  check_skill.py                 — structural checks, size budget, compact coverage
  build_adapters.py              — regenerate the rule adapters
  run_evals.py                   — runtime-neutral behavioural eval harness
  compare_evals.py               — baseline vs with-skill, attributed
  install_adapter.py             — install an adapter without retyping a path
evals/
  cases.json trigger.json        — behavioural cases, and description-triggering queries
templates/
  house-rules.template.md        — your own rules, at precedence level 3
```

`SKILL.md` is the always-loaded control plane and is self-sufficient for most work. The twenty-two reference files are loaded only when one can change the next decision. `adapters/` is not loaded by the skill at all — it exists so the same mind installs into runtimes that have no skill system; see [INSTALL.md](INSTALL.md).

| Reference | Load when |
| --- | --- |
| `operating-manual.md` | a task reaches L2, a decision is genuinely contested, or the work has started going wrong — how the three agencies arbitrate, the fast/slow switch and its two invisible traps, resolving an ambiguous request, the stuck protocol, and the full reporting discipline |
| `lifecycle.md` | the work is big enough that phase order matters — the map from specify to evolve, turning a vague ask into checkable acceptance criteria, choosing a shape before building, and tracing each criterion to the proof that ran |
| `workflows.md` | running a route end to end — diagnose, incident, implement, refactor, greenfield, full-cycle, review, audit, batch, product UI, ship — or applying a risk overlay for performance, security, data migration, API contracts, dependencies, concurrency, or observability |
| `craft.md` | the work turns on code judgment rather than correctness — abstraction timing, naming, error handling, boundaries, concurrency, test design, interface design, deletion, dependencies, commits |
| `loops.md` | the work is genuinely iterative and the iteration is expensive or open-ended — designing the turn/cost/signal/stop before the first run, the technique for shortening a loop rather than running it more, reading whether it is converging, the three ways a loop ends and why saying which one matters, the outer loop that improves the thing doing the work, and recurring or self-paced runs |
| `reasoning.md` | the problem itself is hard to hold — framing, decomposition, case partition with proved coverage, finding a checkable invariant, constraint propagation, working backwards, cost reasoning, proof obligations |
| `judgment.md` | a decision is expensive to get wrong — one-way versus two-way doors, pre-mortem, inversion, disconfirming evidence, base rates, second-order effects, Goodhart's law, when to stop deciding |
| `findings.md` | the deliverable is a set of findings, questions, or a handoff rather than a change — claim labels, finding shape and severity, what is not a finding, artifact budget, handoff minimum bar |
| `documentation.md` | documentation is the deliverable — one owner per fact, where a fact belongs, status labels that make a handoff safe, auditing an existing set down to fewer files, and what never to write |
| `interface-design.md` | how the thing *looks* is part of the deliverable — the palette/type/layout/signature plan settled before any CSS, escaping the handful of looks every generated design converges on, spending boldness in one place, interface copy as design material |
| `performance.md` | something is measurably slow — measure/identify/fix/verify/guard, the default thresholds to anchor against when the project states none, where to start from a symptom, keep-or-revert with neutral counted as a revert, the attempt ledger |
| `security.md` | the change crosses a trust boundary — auth, input from outside, secrets, uploads, serialization, query or template construction, anything one tenant could aim at another. Covers where the boundaries actually are (including the ones that do not look like boundaries), why authorization belongs on the object rather than the route, injection recognized as one bug in many costumes with structural separation as the only real fix, secrets as handles, default deny, threat modelling proportional to the risk, the comforts that are not controls, and what to do when you find something real |
| `llm-systems.md` | the system calls a model — generation, extraction, retrieval, a tool-using agent. Covers the model call as a remote call that fails with a well-formed success, pinning versions so an upgrade is not a silent breaking change, prompt injection handled at the authorization layer rather than by instructing the model, output treated as untrusted input, testing by property and eval rather than equality, the failure modes with no analogue, and cost and latency as design constraints |
| `production.md` | the change will meet real traffic — environment differences, timeout/retry/idempotency/degradation per remote call, observability and alerting, SLOs, performance under load, large-table data operations, runbooks, cost |
| `enterprise.md` | the work sits inside an organization's constraints — regulated data, multi-tenant isolation, least privilege, change control and freeze windows, team process, legacy and unowned code, incident severity, supply chain |
| `scale.md` | the system is too large to read — modelling from partial evidence, locating anything, search technique at size, monorepos, the five layers of blast radius |
| `campaigns.md` | work spans many sessions or a staged rollout — campaign contract, checkpoints, codemods, expand/contract and strangler migrations, delegation, durable decisions |
| `triage.md` | dependency ordering, parallel lanes, plan files, parking and resuming, handoff |
| `reality-testing.md` | choosing a verification level, separating baseline from regression, or deciding what closes a task |
| `defenses.md` | the same approach has failed twice, or the work has started avoiding itself |
| `token-economy.md` | large repositories, repeated compaction, expensive tools, long autonomous runs |
| `learning-loop.md` | capturing a lesson and deciding where it should durably live |
| `collaboration.md` | the response is not landing — corrections about tone or depth, a run of output the user did not want, or a request whose verb is not *do*. Covers what is being asked *of* you rather than *for*: the five engagement modes and what each hands over, how a mode switches mid-conversation without anyone announcing it, reading a preference from four signals without over-fitting to two data points, which of this skill's own defaults a person may move, and the four that never move for anyone |
| `safety.md` | production, credentials, destructive operations, dependency or data risk, release gates |
| `autonomy.md` | the run is unattended — a schedule, a CI job, a queue worker, a fleet — so "ask first" has nobody to ask: the authorization envelope decided in advance, gates that fail closed into a recorded request rather than a guess, the machine-readable verdict every run emits, budget reservation, idempotence and resumability, and the failure modes that only appear at fleet scale |
| `stack-signals.md` | an unfamiliar stack, or uncertainty about which command actually proves anything. Built as a method rather than a catalogue, so it works on a language nobody has written a guide for: deriving the proof commands from the project itself, the four questions that surface what fails *without* failing a build, the changes that break a published contract in any language, and how to write code a maintainer would recognize in an ecosystem you met an hour ago |
| `system-types.md` | the thing being built is not a deploy-and-watch service — a mobile or desktop app, a customer-installed product, firmware, a data pipeline, a game, a compiler, a distributed store. Six questions decide how the method changes: how a change reaches a user, whether it can be undone and by whom, how late the feedback is, who owns the state that matters, what "correct" means beyond a successful return, and what you can never observe from where you are |
| `architecture.md` | judging an existing system rather than only describing it — the five assessment dimensions, tracing a flow before calling it a conflict, using a codebase graph as evidence without letting it pre-judge, the named artifacts, diagram discipline |

## Installation

Eniac is plain Markdown with no build step and no dependency, so it installs into anything that reads instructions.

**A runtime with a skills directory** — copy the folder in and restart:

```bash
cp -r skills/Eniac ~/.claude/skills/Eniac    # Claude Code, user-wide
cp -r skills/Eniac ~/.codex/skills/Eniac     # Codex, user-wide
cp -r skills/Eniac .claude/skills/Eniac      # per-project, checked in
```

**A runtime that reads standing instruction files** — Codex, Cursor, Copilot, Windsurf, Cline, Roo Code, Zed, Gemini CLI, Continue, Aider, Junie, Antigravity, Jules, Amp — copy the matching adapter from `skills/Eniac/adapters/`. All eleven are generated from one source, so the rules are identical across runtimes and cannot drift apart.

**A runtime with one instruction field** — custom GPTs, assistant configurations, chat system prompts — paste `skills/Eniac/adapters/eniac-compact.md`. It is self-contained: a distillation of every rule, without the depth the references carry.

Per-runtime paths, merge guidance, and how to tell whether it actually loaded: **[INSTALL.md](INSTALL.md)**. Rolling it out to a team or a fleet — pinning a version, adding your own rules without forking, distribution, unattended runs: **[ADOPTION.md](ADOPTION.md)**.

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
git pull
cp -r skills/Eniac ~/.claude/skills/Eniac
```

Replace the destination with wherever you installed it, then restart your agent or start a new session.

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
