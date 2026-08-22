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
    reasoning.md               — the method slow mode runs: frame, decompose, prove
    judgment.md                — deciding well when being wrong is expensive
    findings.md                — claim labels, finding shape, questions, handoff
    documentation.md           — one owner per fact, placement, status labels, doc audit
    interface-design.md        — design plan before code, escaping default looks, UI copy
    performance.md             — measure, identify, fix, verify, guard, anchor thresholds
    production.md              — resilience, observability, load, data ops, runbooks
    enterprise.md              — regulated data, tenancy, change control, legacy
    scale.md                   — systems too large to read
    campaigns.md               — multi-session work, migrations, rollout, delegation
    triage.md                  — dependency order, lanes, plan files, handoff
    reality-testing.md         — verification ladder, baseline, honest reporting
    defenses.md                — agent failure modes under pressure
    token-economy.md           — context budgeting and progressive loading
    learning-loop.md           — insight capture and durable placement
    safety.md                  — authorization, secrets, rollback, release
    autonomy.md                — unattended runs, envelopes, verdicts, fleets
    stack-signals.md           — stack detection, real proof commands, pitfalls
    architecture.md            — assessment dimensions, flow tracing, diagrams
  adapters/                    — not loaded by the skill; per-runtime install surfaces
    _source/core.md            — SOURCE OF TRUTH for every generated rule adapter
    eniac-compact.md           — hand-written; the whole mind in one self-contained file
    codex/openai.yaml          — hand-written; Codex interface metadata only
    agents-md/ cursor/ copilot/ windsurf/ cline/ zed/ gemini/
    continue/ aider/ junie/ generic/    — GENERATED, do not edit by hand
scripts/
  check_skill.py               — structural checks; standard library only
  build_adapters.py            — regenerates the rule adapters from _source/core.md
templates/
  house-rules.template.md      — an organization's own rules, at precedence level 3
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

Before adding one, answer two questions in the pull request:

1. Which decision does this change that the existing files do not?
2. What triggers loading it, and how would the agent know that trigger has fired?

If the trigger cannot be stated, the file will not be loaded at the right time and the content belongs inside an existing reference instead. Every new reference must also be registered in the `## References` list in `SKILL.md`, in the README table, and in the layout above.

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
```

It verifies the front matter, that every reference path and `file.md#anchor` resolves, that no reference is orphaned or unregistered across `SKILL.md` / README / this file, that each reference states its own load condition, that Markdown tables are well-formed, that no file assumes one vendor's instruction file where a capability was meant, and that `adapters/eniac-compact.md` still carries the load-bearing rules it restates. Run it before opening a pull request; CI runs the same command.

The judgment half stays manual, and it is the half that matters:

- Markdown renders cleanly on GitHub.
- New guidance does not contradict the existing scope, authority, or token-discipline rules.
- A trivial task still loads no reference files.
- The rule explains *why*, so it survives paraphrase into a situation nobody wrote down.

Behavioral changes are best supported with a before/after example: a prompt where the current text produces the wrong behavior and the proposed text produces the right one.

## Pull Requests

Pull requests should include:

- A short summary of the change.
- The specific failure it prevents.
- Any verification performed.
- Any known risks or follow-up work.

## Credits

Eniac is credited to [ParamissionLab](https://github.com/ParamissionLab).
