# Platform Portability

Use this reference only when installing or adapting Eniac for another coding-agent platform. Keep `SKILL.md` as the canonical source; do not maintain divergent copies.

Verified against official documentation on 2026-07-05. This is a curated compatibility matrix, not a claim that every AI product exposes a public or stable instruction format.

## Support Levels

- **Native skill:** Loads `SKILL.md` on demand with progressive disclosure.
- **Compatible skill:** Loads the Agent Skills layout from a shared compatibility path.
- **Rule adapter:** Requires a concise rule/instruction file; bundled resources may not load automatically.
- **Read-only include:** Loads Eniac as cached context rather than a native skill.

## Current Platform Matrix

| Company / product | Support | Workspace or personal path | Invocation |
| --- | --- | --- | --- |
| OpenAI Codex | Native skill | `~/.codex/skills/Eniac/SKILL.md` | `$eniac` or automatic matching |
| Anthropic Claude Code | Native skill | `.claude/skills/eniac/SKILL.md` or `~/.claude/skills/eniac/SKILL.md` | `/eniac` or automatic matching |
| Google Gemini CLI | Native skill | `.gemini/skills/eniac/SKILL.md`, `.agents/skills/eniac/SKILL.md` | automatic; manage with `/skills` |
| GitHub Copilot | Native skill | `.github/skills/eniac/SKILL.md`, `.agents/skills/eniac/SKILL.md`, or `~/.copilot/skills/eniac/SKILL.md` | `/eniac` or automatic matching |
| OpenCode | Native skill | `.opencode/skills/eniac/SKILL.md`, `.agents/skills/eniac/SKILL.md`, or `~/.config/opencode/skills/eniac/SKILL.md` | native skill tool |
| Cline | Native skill | `.cline/skills/eniac/SKILL.md` or `~/.cline/skills/eniac/SKILL.md` | automatic `use_skill`; enable Skills |
| Windsurf Cascade | Native skill | `.windsurf/skills/eniac/SKILL.md`, `.agents/skills/eniac/SKILL.md`, or `~/.codeium/windsurf/skills/eniac/SKILL.md` | `@eniac` or automatic matching |
| AWS Kiro | Native skill | `.kiro/skills/eniac/SKILL.md` or `~/.kiro/skills/eniac/SKILL.md` | `/eniac` or automatic matching |
| Zed Agent | Native skill | `.agents/skills/eniac/SKILL.md` or `~/.agents/skills/eniac/SKILL.md` | `/eniac`, `@eniac`, or automatic matching |
| Augment Auggie | Native skill | `.augment/skills/eniac/SKILL.md`, `.agents/skills/eniac/SKILL.md`, or `~/.augment/skills/eniac/SKILL.md` | `/eniac` or automatic matching |
| Alibaba Qwen Code | Native skill | `.qwen/skills/eniac/SKILL.md` or `~/.qwen/skills/eniac/SKILL.md` | `/skills eniac` or automatic matching |
| OpenHands | Native skill | `.agents/skills/eniac/SKILL.md` or `~/.openhands/skills/eniac/SKILL.md` | agent invocation or `/add-skill` installation |
| Replit Agent | Compatible skill | `.agents/skills/eniac/SKILL.md` | on-demand discovery in supported projects/templates |
| Cursor | Rule adapter | `.cursor/rules/eniac.mdc` | Agent Requested rule or `@rule` |
| Continue | Rule adapter | `.continue/rules/eniac.md` | automatic rule application |
| Aider | Read-only include | `.aider.conf.yml` with `read: [skills/Eniac/SKILL.md]`, or `--read` | loaded as cached conventions |
| Amazon Q Developer | Rule adapter | `.amazonq/rules/eniac.md` | automatic project-rule context |
| JetBrains Junie | Rule adapter | `.junie/AGENTS.md`, root `AGENTS.md`, or legacy `.junie/guidelines.md` | loaded for every task |

## Adaptation Rules

1. Prefer `.agents/skills/eniac/SKILL.md` only for platforms that document support: Gemini CLI, GitHub Copilot, OpenCode, Windsurf, Zed, Augment, OpenHands, and supported Replit templates.
2. Otherwise use the provider-native path. Copy or link the complete Eniac directory when native skills support bundled references.
3. For rule adapters, keep only the core contract, scale, safety, and output behavior in the rule. Point to the canonical `SKILL.md` when workspace-file references are supported.
4. Do not add vendor-only frontmatter to the canonical `SKILL.md` unless every target parser safely accepts it.
5. Keep `agents/openai.yaml` OpenAI-specific; other vendors do not share its interface schema.
6. Add a platform only when official documentation names a stable discovery path or adapter format. Record model providers separately from agent products; changing the underlying LLM does not change skill installation.

## Official Sources

- [OpenAI skills](https://openai.com/academy/codex-plugins-and-skills/)
- [Claude Code skills](https://code.claude.com/docs/en/skills)
- [Gemini CLI Agent Skills](https://geminicli.com/docs/cli/using-agent-skills/)
- [GitHub Copilot Agent Skills](https://docs.github.com/en/copilot/concepts/agents/about-agent-skills)
- [OpenCode Agent Skills](https://opencode.ai/docs/skills)
- [Cline Skills](https://docs.cline.bot/customization/skills)
- [Windsurf Cascade Skills](https://docs.windsurf.com/windsurf/cascade/skills)
- [Kiro Agent Skills](https://kiro.dev/docs/skills/)
- [Zed Agent Skills](https://zed.dev/docs/ai/skills)
- [Augment Agent Skills](https://docs.augmentcode.com/cli/skills)
- [Qwen Code Agent Skills](https://qwenlm.github.io/qwen-code-docs/en/users/features/skills/)
- [OpenHands Skills](https://docs.openhands.dev/overview/skills)
- [Replit skills and project instructions](https://docs.replit.com/teams/custom-templates)
- [Cursor Rules](https://docs.cursor.com/context/rules)
- [Continue Rules](https://docs.continue.dev/customize/rules)
- [Aider conventions](https://aider.chat/docs/usage/conventions.html)
- [Amazon Q project rules](https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/context-project-rules.html)
- [JetBrains Junie guidelines](https://junie.jetbrains.com/docs/guidelines-and-memory.html)
