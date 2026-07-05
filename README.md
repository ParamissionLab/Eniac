# Eniac

Eniac is a provider-neutral, agent-agnostic operating skill for token-aware AI agents. It helps agents handle simple tasks without overthinking, scale up to complex autonomous work, stay scoped, verify results, and avoid wasting tokens or credits.

Credit: [ParamissionLab](https://github.com/ParamissionLab)

Current version: `1.1.1`

## What It Does

- Runs compact Perceive -> Reason -> Act -> Observe loops.
- Scales effort from tiny edits to complex architecture, debugging, research, and review work.
- Keeps context use lean with cost guards, targeted reads, batching, and narrow verification first.
- Supports full-cycle software engineering, UI/UX/frontend quality, prompt or agent workflow design, and many-small-edit batches.
- Handles Thai and other token-expensive languages with compact planning while preserving exact paths, commands, identifiers, and quotes.
- Loads deeper references only when needed.

## Structure

```text
skills/
  Eniac/
    SKILL.md
    references/
      loop-engineering.md
      multilingual-token-discipline.md
      product-ux.md
      software-engineering.md
      systematic-thinking.md
```

`SKILL.md` is the lightweight control plane. The files in `references/` are loaded only for deeper task-specific guidance.

## Install For Codex

Copy the skill folder into your Codex skills directory.

### Windows PowerShell

```powershell
git clone https://github.com/ParamissionLab/Eniac.git
New-Item -ItemType Directory -Force "$env:USERPROFILE\.codex\skills" | Out-Null
Copy-Item -Recurse -Force ".\Eniac\skills\Eniac" "$env:USERPROFILE\.codex\skills"
```

### macOS/Linux

```bash
git clone https://github.com/ParamissionLab/Eniac.git
mkdir -p ~/.codex/skills
cp -R Eniac/skills/Eniac ~/.codex/skills/
```

Restart Codex or start a new thread so the skill list refreshes.

## Install For Other Agents

Use `skills/Eniac/SKILL.md` as the main instruction file. Keep the `references/` folder next to it so the agent can load deeper guidance only when needed.

If your runtime does not support skill loading, paste the short contract from `SKILL.md` into your agent instructions and point the agent at the reference files as optional material.

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
- installed references should stay specific so UI/UX, software, loop, and multilingual guidance load only when they can change the result
- broad tests, browser checks, web lookups, and subagents should run only when they can change the decision or risk report
- final reports should summarize changed behavior, verification, risks, and next steps without long reasoning traces

## Updating

To update an installed copy:

```bash
git -C Eniac pull
cp -R Eniac/skills/Eniac ~/.codex/skills/
```

On Windows PowerShell:

```powershell
git -C .\Eniac pull
Copy-Item -Recurse -Force ".\Eniac\skills\Eniac" "$env:USERPROFILE\.codex\skills"
```

Restart Codex or open a new thread after updating.

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
