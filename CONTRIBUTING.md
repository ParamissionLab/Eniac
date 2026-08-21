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
    workflows.md               — step chains per route + risk overlays
    craft.md                   — code judgment: abstraction, naming, errors, tests
    findings.md                — claim labels, finding shape, questions, handoff
    performance.md             — measure, identify, fix, verify, guard
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
    stack-signals.md           — stack detection, real proof commands, pitfalls
```

Edit `SKILL.md` only for core behavior — the agencies, the loop, investment levels, the triage ladder, routing, and reference discovery. Everything task-specific belongs in a reference file.

## Contribution Guidelines

**Progressive disclosure is the architecture, not a preference.** `SKILL.md` is loaded on every invocation, so anything added there is paid for by every task including trivial ones. New guidance belongs in `references/` unless it changes routing or applies to nearly all work.

- Keep changes narrow and tied to a specific failure the current text allows.
- Do not add reference content that would be loaded for simple tasks unless it prevents a concrete, describable mistake.
- Explain *why* a rule exists. Rules the model understands survive paraphrase and novel situations; bare imperatives do not. Prefer a reason over an emphatic `MUST`.
- Preserve provider-neutral and stack-neutral language, except where a section is explicitly about a named platform or ecosystem.
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

There are no build steps or test scripts in this repository — it is prose that steers behavior. Verification is correspondingly manual:

- Markdown renders cleanly on GitHub.
- `skills/Eniac/SKILL.md` still has valid YAML front matter with `name` and `description`.
- Every `references/*.md` path mentioned anywhere resolves to a file that exists.
- Every `workflows.md#anchor` link matches a real heading.
- The README layout, the README reference table, the layout in this file, and the `## References` list in `SKILL.md` all agree with the actual contents of `references/`.
- New guidance does not contradict the existing scope, authority, or token-discipline rules.
- A trivial task still loads no reference files.

Behavioral changes are best supported with a before/after example: a prompt where the current text produces the wrong behavior and the proposed text produces the right one.

## Pull Requests

Pull requests should include:

- A short summary of the change.
- The specific failure it prevents.
- Any verification performed.
- Any known risks or follow-up work.

## Credits

Eniac is credited to [ParamissionLab](https://github.com/ParamissionLab).
