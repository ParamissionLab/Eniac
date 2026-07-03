# Eniac

Eniac is a Codex-compatible skill for agent-agnostic, token-aware loop engineering and systematic thinking. It helps AI agents work through compact Perceive, Reason, Act, Observe loops while staying scoped, reducing unnecessary context use, and reporting results clearly.

Credit: [ParamissionLab](https://github.com/ParamissionLab)

## What It Does

- Guides agents through bounded engineering loops until work is complete or clearly blocked.
- Keeps tasks scoped to the user's requested outcome.
- Encourages targeted context gathering, concise working briefs, and meaningful verification.
- Supports software engineering, debugging, review, planning, architecture, and research-heavy work.
- Includes guidance for Thai and other token-expensive language workflows.

## Structure

```text
skills/
  Eniac/
    SKILL.md
    references/
      loop-engineering.md
      multilingual-token-discipline.md
      software-engineering.md
      systematic-thinking.md
```

## Installation

Copy `skills/Eniac` into your Codex skills directory, or keep this repository available in a skills path supported by your runtime.

## Usage

Use the `eniac` skill when a task needs autonomous progress, compact reasoning loops, scope control, or token-aware execution. The main entry point is:

```text
skills/Eniac/SKILL.md
```

The reference files are loaded only when needed for deeper guidance.

## Versioning

This project follows semantic versioning where practical:

- Patch versions fix wording, structure, or small behavioral issues.
- Minor versions add compatible guidance or references.
- Major versions may change the skill contract or expected agent behavior.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines.

## Security

See [SECURITY.md](SECURITY.md) for reporting security issues.

## Code of Conduct

See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) for community expectations.

## License

MIT. See [LICENSE](LICENSE).
