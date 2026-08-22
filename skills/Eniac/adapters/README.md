# Adapters

<!-- Generated from skills/Eniac/adapters/_source/core.md by scripts/build_adapters.py. Edit the source, not this file. -->

Eniac's behaviour lives in `../SKILL.md` and `../references/`. That pair is the source of
truth. These files exist because not every runtime loads skills the same way.

## Hand-written

| File | For | What it is |
| --- | --- | --- |
| `eniac-compact.md` | any runtime with one instruction field, or a small context budget | the whole mind distilled into one self-contained file — a system prompt, a custom assistant's instruction field, a pasted preamble |
| `codex/openai.yaml` | Codex | interface metadata only; the behaviour still comes from `SKILL.md` |

## Generated

Every file below is produced from `_source/core.md` by `scripts/build_adapters.py`, so the
rules cannot drift between runtimes. **Edit the source, not these files**, then re-run the
script. Adding a runtime is one entry in that script's `TARGETS` table.

| File | For | Install | Path confirmed |
| --- | --- | --- | --- |
| `agents-md/AGENTS.example.md` | Codex, Gemini CLI, Windsurf, Antigravity, Jules, Amp, and anything else on the AGENTS.md convention | merge into the project's AGENTS.md | not confirmed by an install |
| `cursor/eniac.mdc` | Cursor | copy to .cursor/rules/eniac.mdc | not confirmed by an install |
| `copilot/copilot-instructions.md` | GitHub Copilot (chat, agent mode, and coding agent) | copy to .github/copilot-instructions.md | not confirmed by an install |
| `windsurf/eniac.md` | Windsurf | copy to .windsurf/rules/eniac.md | not confirmed by an install |
| `cline/.clinerules` | Cline and Roo Code | copy to .clinerules in the project root | not confirmed by an install |
| `zed/rules.md` | Zed | copy to .rules in the project root | not confirmed by an install |
| `gemini/GEMINI.md` | Gemini CLI and Gemini Code Assist | copy to GEMINI.md in the project root | not confirmed by an install |
| `continue/eniac.md` | Continue | copy to .continue/rules/eniac.md | not confirmed by an install |
| `aider/CONVENTIONS.md` | Aider | add with `aider --read CONVENTIONS.md` | not confirmed by an install |
| `kiro/eniac.md` | Kiro | copy to .kiro/steering/eniac.md, or ~/.kiro/steering/eniac.md for every workspace | not confirmed by an install |
| `junie/guidelines.md` | JetBrains Junie | copy to .junie/guidelines.md | not confirmed by an install |
| `generic/system-prompt.md` | any assistant with a single instruction field, and any API integration | paste as the system prompt, or prepend to it | not confirmed by an install |

**12 of 12 paths are unconfirmed.** The rules in every adapter are
generated and therefore correct; what is not independently verified is each runtime's
*filename and front-matter contract*, which comes from that runtime's documentation rather
than from an install performed here. This distinction matters because the failure is
silent: a wrong key or path produces no error, the file is simply never loaded, and the
agent behaves exactly as though the adapter were absent.

If you install one and confirm it loads — the quickest signal is in `../../../INSTALL.md`
under "Verifying the install" — set `verified` for that entry in
`scripts/build_adapters.py` to a short `YYYY-MM-DD, who, what you saw`, re-run the
generator, and send the change. That is one line and it retires an assumption for everyone.

## Which one to use

- **The runtime loads skills** (Claude Code, Codex, and others with a skills directory) —
  install the whole `skills/Eniac/` folder and ignore this directory. Progressive
  disclosure is the point: the control plane loads, and a reference is read only when a
  task earns it.
- **The runtime reads standing instruction files** — copy the matching row above, and keep
  the full folder in the repository so the pointer inside it resolves.
- **The runtime offers only one instruction field** — paste `eniac-compact.md`.

The compact file is a distillation, not a summary: every rule in it is one the full skill
would apply. What it drops is the depth behind each rule, which is exactly what the
references carry. Where both fit, the full package is better.

Installation per runtime, including paths and merge guidance: `../../../INSTALL.md`.
