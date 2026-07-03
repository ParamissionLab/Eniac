# Contributing

Thank you for contributing to Eniac.

Current version: `1.0.0`

## Project Goals

Eniac should remain:

- Provider-neutral.
- Agent-agnostic.
- Token-aware.
- Practical for real engineering work.
- Clear about scope, stop conditions, and verification.

## Repository Layout

```text
skills/Eniac/SKILL.md
skills/Eniac/references/
```

Edit `SKILL.md` for core behavior. Edit files in `references/` only when the deeper guidance needs to change.

## Contribution Guidelines

- Keep changes narrow and directly related to the issue or improvement.
- Preserve provider-neutral language unless a section explicitly discusses a named platform.
- Avoid adding new dependencies, tools, or workflows unless they are necessary.
- Keep instructions concise and operational.
- Do not include secrets, credentials, private URLs, or sensitive user data.
- Use Markdown that renders cleanly on GitHub.

## Documentation Style

- Prefer direct instructions over long explanations.
- Use short headings and compact lists.
- Keep examples portable across agent runtimes.
- Preserve exact file paths, command names, and technical terms when they matter.

## Testing Changes

Before submitting, check:

- Markdown files render cleanly.
- Links point to existing files or valid external pages.
- `skills/Eniac/SKILL.md` still has valid front matter.
- New guidance does not conflict with the existing scope and token discipline rules.

## Pull Requests

Pull requests should include:

- A short summary of the change.
- The reason for the change.
- Any verification performed.
- Any known risks or follow-up work.

## Credits

Eniac is credited to [ParamissionLab](https://github.com/ParamissionLab).
