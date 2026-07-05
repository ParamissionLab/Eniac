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
skills/Eniac/references/
```

Edit `SKILL.md` only for core behavior, routing, and reference discovery. Edit files in `references/` for deeper task-specific guidance such as loop engineering, software engineering, product UI/UX, systematic thinking, or multilingual token discipline.

## Contribution Guidelines

- Keep changes narrow and directly related to the issue or improvement.
- Preserve provider-neutral language unless a section explicitly discusses a named platform.
- Avoid adding new dependencies, tools, or workflows unless they are necessary.
- Keep instructions concise and operational.
- Prefer progressive disclosure: keep `SKILL.md` lean and move optional detail into a reference file.
- Do not add reference content that will be loaded for simple tasks unless it prevents a concrete failure.
- Keep UI/UX guidance practical: interface structure, states, responsive behavior, accessibility, and verification should matter more than decorative preference.
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

## Pull Requests

Pull requests should include:

- A short summary of the change.
- The reason for the change.
- Any verification performed.
- Any known risks or follow-up work.

## Credits

Eniac is credited to [ParamissionLab](https://github.com/ParamissionLab).
