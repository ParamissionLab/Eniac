# Contributing

Thank you for contributing to Eniac.

## Project Goals

Eniac should remain:

- Provider-neutral.
- Agent-agnostic.
- Token-aware.
- Cost-conscious for tokens, credits, tool calls, and context.
- Practical for real full-cycle engineering and UI/UX work.
- Clear about scope, stop conditions, and verification.

## Repository Layout

```text
skills/Eniac/SKILL.md
skills/Eniac/scripts/
  finalize_plan.py                 — verified plan finalization/deletion
skills/Eniac/tests/
  test_finalize_plan.py            — finalizer regression tests
skills/Eniac/references/
  architecture-evidence.md        — evidence-first architecture passes and handoff
  algorithm-workflow.md           — cause, coverage, weighting, and documentation loop
  ci-templates-by-stack.md        — CI YAML templates (8 stacks + release)
  commands-by-stack.md            — discovery, test, lint, format commands
  delivery-proof-pipelines.md     — CI as proof graph + principles
  execution-ledger.md             — restartable milestone tracking
  greenfield-launch-sequence.md   — new project staged launch
  loop-engineering.md             — autonomy, delegation, stop rules
  multilingual-token-discipline.md — Thai/multilingual token handling
  plan-template-extended.md       — rich plan for L2-L3 broad work
  platform-portability.md         — installation across platforms
  product-ux.md                   — UI/UX quality and verification
  project-interface-contract.md   — evidence-based README contract
  readme-template.md              — formatted README skeleton
  safety-and-delivery.md          — authority gates, secrets, verification
  software-engineering.md         — full-cycle engineering playbook
  stack-patterns-and-pitfalls.md  — code examples (11 stacks)
  stack-risk-matrix.md            — invariants, failure radar, proof
  systematic-thinking.md          — decomposition and options
  workstream-orchestration.md     — dependency-aware workflow and durable context
```

Edit `SKILL.md` only for core behavior, routing, and reference discovery. Edit files in `references/` for deeper task-specific guidance such as loop engineering, software engineering, product UI/UX, systematic thinking, CI templates, stack patterns, or multilingual token discipline.

## Contribution Guidelines

- Keep changes narrow and directly related to the issue or improvement.
- Preserve provider-neutral language unless a section explicitly discusses a named platform.
- Avoid adding new dependencies, tools, or workflows unless they are necessary.
- Keep instructions concise and operational.
- Prefer progressive disclosure: keep `SKILL.md` lean and move optional detail into a reference file.
- Keep complex-workflow guidance provider-neutral: use dependency gates, owned mutable scope, integration proof, and an explicit primary owner rather than assuming a specific sub-agent runtime.
- Treat L3 plan files as durable execution context during execution: keep only decision-relevant system facts, contracts, proofs, and resume state; delete them on completion by default, and retain only on explicit request or repository policy. Do not append activity logs or hidden reasoning.
- For defects and unexpected results, record an evidenced causal chain or an explicit unverified follow-up. A temporary containment is never a completed fix by itself.
- Update plans and durable docs after material signals that change facts, behavior, contracts, risks, decisions, or handoff; use `Doc impact: none` where relevant instead of creating activity-log churn.
- Do not add reference content that will be loaded for simple tasks unless it prevents a concrete failure.
- Keep UI/UX guidance practical: interface structure, states, responsive behavior, accessibility, and verification should matter more than decorative preference.
- Template files (`ci-templates-by-stack.md`, `readme-template.md`, `plan-template-extended.md`, `stack-patterns-and-pitfalls.md`) should always note "adapt to actual project" — they are starting points, not drop-in replacements.
- When adding a new language/stack, update all stack-aware files: `commands-by-stack.md`, `stack-risk-matrix.md`, `stack-patterns-and-pitfalls.md`, `ci-templates-by-stack.md`, and `delivery-proof-pipelines.md`.
- Do not include secrets, credentials, private URLs, or sensitive user data.
- Use Markdown that renders cleanly on GitHub.

## Documentation Style

- Prefer direct instructions over long explanations.
- Use short headings and compact lists.
- Keep examples portable across agent runtimes.
- Preserve exact file paths, command names, and technical terms when they matter.
- Include installation or update commands only when they are copy-pasteable and platform-specific enough to be safe.

## Testing Changes

Before submitting, check:

- Markdown files render cleanly.
- Links point to existing files or valid external pages.
- `skills/Eniac/SKILL.md` still has valid front matter.
- New guidance does not conflict with the existing scope and token discipline rules.
- Simple tasks still avoid unnecessary reference loading.
- `python skills/Eniac/tests/test_finalize_plan.py` passes after changing plan-finalization behavior.

## Pull Requests

Pull requests should include:

- A short summary of the change.
- The reason for the change.
- Any verification performed.
- Any known risks or follow-up work.

## Credits

Eniac is credited to [ParamissionLab](https://github.com/ParamissionLab).
