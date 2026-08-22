# Contributing

Thank you for contributing to Eniac.

## Project Goals

Eniac should remain:

- Provider-neutral and agent-agnostic.
- Token-aware — cheap on simple work, thorough only where risk justifies it.
- Practical for real full-cycle engineering rather than aspirational.
- Explicit about scope, authority, stop conditions, and what counts as proof.
- Coherent with its own cognitive model: Id proposes, Superego constrains, Ego decides and acts.

## Repository Layout

```text
skills/Eniac/
  SKILL.md                     — always-loaded control plane
  references/
    operating-manual.md        — arbitration, fast/slow, ambiguity, stuck, reporting
    lifecycle.md               — specify, design, traceability, phase gates
    workflows.md               — step chains per route + risk overlays
    craft.md                   — code judgment: abstraction, errors, concurrency, tests
    loops.md                   — loop design, shortening, convergence, stops, outer loop
    reasoning.md               — the method slow mode runs: frame, decompose, prove
    judgment.md                — deciding well when being wrong is expensive
    findings.md                — claim labels, finding shape, questions, handoff
    documentation.md           — one owner per fact, placement, status labels, doc audit
    interface-design.md        — design plan before code, escaping default looks, UI copy
    performance.md             — measure, identify, fix, verify, guard, anchor thresholds
    security.md                — trust boundaries, authz paths, injection, secrets
    llm-systems.md             — building on models: injection, evals, cost, versions
    production.md              — resilience, observability, load, data ops, runbooks
    enterprise.md              — regulated data, tenancy, change control, legacy
    comprehension.md          — intent that is lost: history, anomalies, Chesterton's fence
    scale.md                   — systems too large to read
    campaigns.md               — multi-session work, migrations, rollout, delegation
    debt.md                    — interest-rate ranking, in-path vs nearby, when not to pay
    triage.md                  — dependency order, lanes, plan files, handoff
    reality-testing.md         — verification ladder, baseline, honest reporting
    defenses.md                — agent failure modes under pressure
    token-economy.md           — context budgeting and progressive loading
    learning-loop.md           — insight capture and durable placement
    defect-sets.md             — many defects at once: generators, classes, fix order
    collaboration.md           — engagement modes, reading a preference, movable defaults
    safety.md                  — authorization, secrets, rollback, release
    autonomy.md                — unattended runs, envelopes, verdicts, fleets
    stack-signals.md           — any stack: deriving proofs, silent failures, contracts
    system-types.md            — how the kind of system changes delivery, proof, and risk
    architecture.md            — assessment dimensions, flow tracing, diagrams
  adapters/                    — not loaded by the skill; per-runtime install surfaces
    _source/core.md            — SOURCE OF TRUTH for every generated rule adapter
    eniac-compact.md           — hand-written; the whole mind in one self-contained file
    codex/openai.yaml          — hand-written; Codex interface metadata only
    agents-md/ cursor/ copilot/ windsurf/ cline/ zed/ gemini/
    continue/ aider/ junie/ generic/    — GENERATED, do not edit by hand
scripts/
  install.py                   — the installer: skill folders and adapters, one table
  check_skill.py               — structural checks, budget, compact coverage
  build_adapters.py            — regenerates the rule adapters from _source/core.md
  run_evals.py                 — runtime-neutral behavioural eval harness
  compare_evals.py             — runs both arms and attributes the difference
evals/
  cases.json                   — behavioural cases with discriminating assertions
  trigger.json                 — should-fire / should-not-fire queries for the description
  README.md                    — how to run them and how to write one
templates/
  house-rules.template.md      — an organization's own rules, at precedence level 3
install.sh install.ps1         — wrappers that find a Python and run scripts/install.py
INSTALL.md                     — per-runtime installation
ADOPTION.md                    — team and fleet rollout, versioning, customization
```

Edit `SKILL.md` only for core behavior — the agencies, the loop, investment levels, the triage ladder, routing, and reference discovery. Everything task-specific belongs in a reference file.

## Contribution Guidelines

**Progressive disclosure is the architecture, not a preference.** `SKILL.md` is loaded on every invocation, so anything added there is paid for by every task including trivial ones. New guidance belongs in `references/` unless it changes routing or applies to nearly all work.

- Keep changes narrow and tied to a specific failure the current text allows.
- Do not add reference content that would be loaded for simple tasks unless it prevents a concrete, describable mistake.
- Explain *why* a rule exists. Rules the model understands survive paraphrase and novel situations; bare imperatives do not. Prefer a reason over an emphatic `MUST`.
- Preserve provider-neutral and stack-neutral language, except where a section is explicitly about a named platform or ecosystem. Naming one vendor's instruction file, tool, or model where a capability was meant makes the skill wrong on every other runtime — write the capability and give the vendor names as examples.
- **Adapters are generated, not written.** Editing a file under `adapters/agents-md/`, `cursor/`, `copilot/`, `windsurf/`, `cline/`, `zed/`, `gemini/`, `continue/`, `aider/`, `junie/`, or `generic/` forks that runtime from every other one. Edit `adapters/_source/core.md` and run `python scripts/build_adapters.py`; CI rejects the mismatch otherwise. Supporting a new runtime is one entry in that script's `TARGETS` table, not a new hand-written file.
- **`eniac-compact.md` is the one deliberate restatement.** It is a distillation rather than a reformat, so it cannot be generated — which means it is the file that drifts. When a load-bearing rule in `SKILL.md` changes, that file needs the same edit in the same commit.
- Keep the Freudian model doing real work. Each borrowed concept should map onto a mechanism that changes behavior — an agency that produces something, a principle that gates something. Decorative psychoanalytic vocabulary costs tokens and earns nothing.
- Never introduce three-voice narration as visible output. Arbitration is internal and costs at most one line.
- Preserve the distinction between reporting and doing. Guidance that lets an agent silently widen scope is a regression regardless of how useful the extra work is.
- Do not include secrets, credentials, private URLs, or sensitive user data — including in examples.
- Use Markdown that renders cleanly on GitHub.

## Adding A Reference File

The default answer is no. Twenty-six files is already a lot to keep coherent, and the usual right move is a new section inside the file that already owns the territory. Before adding one, answer three questions in the pull request:

1. **Which decision does this change that the existing files do not?**
2. **What triggers loading it, and how would the agent know that trigger has fired?** If the trigger cannot be stated, the file will not be loaded at the right time and the content belongs inside an existing reference instead.
3. **What does it own, and what does it hand off?** If the answer overlaps an existing file, the boundary has to move — one of the two defers, explicitly and in writing.

Then wire it in, all four of which the checker enforces:

- An `> **Owns** — … / > **Defers** — …` block near the top, before `## Contents`. This is the package applying its own one-owner-per-fact rule to itself: it tells a reader deciding whether to keep reading exactly where the boundary is, and it makes a future overlap a build failure rather than a slow drift. The checker rejects a missing block, a hand-off to a file that does not exist, a file that defers to itself, and two files claiming the same owned phrase.
- A place in **exactly one group** of the reference map in `SKILL.md`. Groups say what *kind* of question a file answers; a file in two groups means the grouping has stopped meaning anything.
- A row in the README reference table and a line in the layout above.
- A load condition stated in the file's own opening lines.

Neighbouring files usually need an edit too. If the new file takes over territory another one covered in passing, that other file gets the topic removed and a hand-off added — otherwise the package ends up with the duplication it tells its users to avoid.

## Adding A Stack

`stack-signals.md` is the only stack-aware file. Adding an ecosystem means adding its detection evidence, the commands that actually prove something, and its silent failure modes — the third being the part that carries the value. Commands that merely exit zero without exercising behavior are not worth listing.

## Documentation Style

- Direct instructions over long explanations.
- Short headings, compact lists, tables where a table genuinely compresses.
- Examples portable across agent runtimes.
- Preserve exact file paths, command names, and technical terms; never paraphrase them.
- Include installation or update commands only when they are copy-pasteable and safe as written.

## Verifying A Change

This repository is prose that steers behavior, so most of its quality is judgment. What is *not* judgment drifts silently, and that part is checked by a script — standard library only, no arguments:

```bash
python scripts/check_skill.py
python scripts/build_adapters.py --check
python scripts/run_evals.py --self-test
```

Between them these verify the front matter; that every reference path and `file.md#anchor` resolves; that no reference is orphaned or unregistered across `SKILL.md` / README / this file; that each reference states its own load condition; that Markdown tables are well-formed; that no file assumes one vendor's instruction file where a capability was meant; that `SKILL.md` is inside its size budget; that every `SKILL.md` section is either carried by `adapters/eniac-compact.md` or recorded as deliberately absent; that the generated adapters match their source; and that every eval case rejects a deliberately bad answer. Run all three before opening a pull request; CI runs the same three.

**The size budget makes growth deliberate; it is not a target to shrink toward.** `SKILL.md` is loaded on every invocation, so its length is a real cost — but the opposite failure is worse and less visible. A control plane too thin to settle the next action pushes that work into a reference, and a reference is 150–200 lines loaded at full price on exactly the tasks that were supposed to be cheap. Twenty lines saved in `SKILL.md` can cost two hundred in a reference load, and nobody attributes it.

So: raise `SKILL_MAX_LINES` when the content earns it, in a commit that says why. Do not compress a rule until it stops explaining itself — a rule the model does not understand survives neither paraphrase nor a situation nobody wrote down, which is the whole reason this skill explains *why* instead of issuing bare imperatives.

The judgment half stays manual, and it is the half that matters:

- Markdown renders cleanly on GitHub.
- New guidance does not contradict the existing scope, authority, or token-discipline rules.
- A trivial task still loads no reference files.
- The rule explains *why*, so it survives paraphrase into a situation nobody wrote down.

Behavioural changes are best supported by the eval suite in `evals/`. If a change is meant to alter what an agent does, add or update a case in `evals/cases.json` so the claim is checkable by someone else, and run it against your runtime both with and without the skill:

```bash
python scripts/run_evals.py --agent-cmd '<your agent>' --label with-skill
python scripts/run_evals.py --agent-cmd '<your agent>' --label baseline
```

A case both runs pass is telling you the model already did that, and the guidance is not earning its tokens. Full instructions and the rules for writing a case that discriminates are in `evals/README.md`.

**Verifying an adapter path** is a small, high-value contribution. Every runtime path in `scripts/build_adapters.py` is currently marked unverified, because a wrong filename or front-matter key fails silently — nothing errors, the file is simply never loaded. If you install one and confirm it loads, set that target's `verified` field, re-run the generator, and send the change.

## Pull Requests

Pull requests should include:

- A short summary of the change.
- The specific failure it prevents.
- Any verification performed.
- Any known risks or follow-up work.

## Credits

Eniac is credited to [ParamissionLab](https://github.com/ParamissionLab).
