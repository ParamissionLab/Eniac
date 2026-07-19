# Eniac

Eniac is a provider-neutral, agent-agnostic operating skill for token-aware AI agents. It helps agents handle simple tasks without overthinking, scale up to complex autonomous work, stay scoped, verify results, and avoid wasting tokens or credits.

Credit: [ParamissionLab](https://github.com/ParamissionLab)

## What It Does

- Runs compact Perceive -> Reason -> Act -> Observe loops with cause, coverage, and documentation-impact checks on material signals.
- Scales effort from tiny edits (L0) to complex architecture (L3) and high-risk production work (L4).
- Keeps context use lean with cost guards, targeted reads, batching, and narrow verification first.
- Supports senior software engineering workflows: staged Greenfield launches, project-state detection, codebase audits, stack-risk analysis, restartable execution ledgers, evidence-backed project interfaces, CI proof graphs, full-cycle build/test/bug-hunt/polish/docs/ship, deep codebase audits, whole-repo code reads when requested, UI/UX/frontend quality, prompt or agent workflow design, and many-small-edit batches.
- Uses dependency-aware workstreams for difficult multi-surface work, while keeping one integration owner, explicit mutable scope, acceptance proof, and recovery gates.
- Requires a causal record before closing defects; emergency containment is clearly separated from the systemic correction.
- Provides ready-to-adapt CI templates for 8 stacks (Node.js, Python, Go, Rust, Zig, Ruby, Java, .NET) plus release workflows.
- Includes concrete code pitfalls and good patterns for 11 stacks with bad-to-good examples.
- Ships README and plan templates for consistent, high-quality documentation and planning.
- Handles Thai and other token-expensive languages with compact planning while preserving exact paths, commands, identifiers, and quotes.
- Loads deeper references only when needed (20 reference files, loaded on demand).

## Structure

```text
skills/
  Eniac/
    SKILL.md
    scripts/
      finalize_plan.py
    tests/
      test_finalize_plan.py
    references/
      ci-templates-by-stack.md
      architecture-evidence.md
      algorithm-workflow.md
      commands-by-stack.md
      delivery-proof-pipelines.md
      execution-ledger.md
      greenfield-launch-sequence.md
      loop-engineering.md
      multilingual-token-discipline.md
      plan-template-extended.md
      platform-portability.md
      product-ux.md
      project-interface-contract.md
      readme-template.md
      safety-and-delivery.md
      software-engineering.md
      stack-patterns-and-pitfalls.md
      stack-risk-matrix.md
      systematic-thinking.md
      workstream-orchestration.md
```

`SKILL.md` is the lightweight control plane. The 20 files in `references/` are loaded only when deeper task-specific guidance is needed:

| Category | Files | Loaded when |
|----------|-------|-------------|
| Core engineering | `software-engineering.md`, `commands-by-stack.md` | Non-trivial code work |
| Architecture | `architecture-evidence.md` | Existing-system architecture work, non-local changes, blast-radius analysis, or handoff |
| Complex workflow | `workstream-orchestration.md` | Difficult multi-workstream work, dependency waves, safe parallel execution, integration, or durable task context |
| Algorithmic quality | `algorithm-workflow.md` | L2+ execution loops requiring root-cause diagnosis, work weighting, coverage, or documentation-impact discipline |
| Actionable templates | `ci-templates-by-stack.md`, `readme-template.md`, `plan-template-extended.md` | Creating CI, README, or plans for broad work |
| Stack knowledge | `stack-risk-matrix.md`, `stack-patterns-and-pitfalls.md` | Stack-specific correctness risk |
| Greenfield | `greenfield-launch-sequence.md`, `execution-ledger.md` | New project or broad milestoned work |
| Safety | `safety-and-delivery.md`, `delivery-proof-pipelines.md` | L4, CI, dependencies, production |
| Specialized | `product-ux.md`, `loop-engineering.md`, `systematic-thinking.md`, `multilingual-token-discipline.md` | UI/UX, autonomy, complex decomposition, multilingual |
| Meta | `project-interface-contract.md`, `platform-portability.md` | README rewrites, platform installation |

## Installation

See `skills/Eniac/references/platform-portability.md` for current installation paths across supported platforms (OpenAI Codex, Anthropic Claude Code, Google Gemini CLI, GitHub Copilot, OpenCode, Cline, Windsurf, Zed, Augment, and others).

Quick approach: copy or link the entire `skills/Eniac/` folder into your agent's native skills directory, or use the shared `.agents/skills/eniac/` path where supported. If your runtime does not support skill loading, paste the core contract from `SKILL.md` into your agent instructions and point the agent at the reference files as optional material.

## Usage

Use the `eniac` skill when you want:

- autonomous work that should continue until done or genuinely blocked
- strict token, credit, context, or scope control
- software engineering, debugging, review, planning, architecture, or research
- UI/UX/frontend work that should fit the product type, visual system, and real user workflow
- many small edits that should be batched safely
- Thai or multilingual work that should stay concise

Example prompts:

```text
Use eniac to fix this bug, verify it, and keep changes scoped.
```

```text
Use eniac to improve this dashboard UX for real daily operations without making it look like a landing page.
```

```text
Use eniac to tighten this app UI: layout, controls, states, responsive behavior, and accessibility, without adding visual noise.
```

```text
ใช้ eniac แก้หลายไฟล์ตาม pattern เดียวกันแบบประหยัด token และตรวจให้พอมั่นใจ
```

## Token And Credit Discipline

Eniac is designed to reduce waste:

- simple work should not load extra references
- large files should be searched or read by targeted ranges first
- repeated edits should be batched by one safe rule
- concurrent work should begin only after contracts, mutable scopes, and integration proof are explicit
- L3 work should keep a compact durable execution context during execution so a later session can resume from verified facts; plans are deleted on completion by default unless retention is explicitly requested
- each material loop should reweight the next action and assess applicable flow, contract, failure, operations, and documentation coverage
- a green symptom check is not a final fix unless the causal record is proven or its uncertainty and owner are explicit
- installed references should stay specific so UI/UX, software, loop, and multilingual guidance load only when they can change the result
- broad tests, browser checks, web lookups, and subagents should run only when they can change the decision or risk report
- final reports should summarize changed behavior, verification, risks, and next steps without long reasoning traces

## Updating

```bash
git -C Eniac pull
# Then copy the skills/Eniac folder to your agent's skill directory
# See platform-portability.md for your target platform path
```

Restart your agent or start a new session after updating.

## Validation

```powershell
python skills/Eniac/tests/test_finalize_plan.py
```

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

MIT. See [LICENSE](LICENSE).
