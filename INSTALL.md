# Install Eniac

Eniac is plain Markdown. There is nothing to build, no runtime, and no dependency — which
is why it installs into anything that can read instructions.

## What to install

| You are installing | Copy |
| --- | --- |
| The full skill (preferred) | the whole `skills/Eniac/` folder, keeping `SKILL.md` and `references/` together so the relative links resolve |
| A project-wide rule | `skills/Eniac/adapters/` — see the table below |
| A single instruction field | the contents of `skills/Eniac/adapters/eniac-compact.md` |

Prefer the full folder wherever the runtime supports it. Its whole design is progressive
disclosure: a small control plane loads, and a reference file is read only when a task
earns it. Pasting everything into one prompt gives that up and costs tokens on every task.

## Runtimes with a skills directory

Copy the folder in, keeping the name `Eniac`, then restart the agent or start a new
session so the skill list refreshes.

**Claude Code** — user-wide:

```bash
cp -r skills/Eniac ~/.claude/skills/Eniac
```

Or per-project, checked in with the repository:

```bash
cp -r skills/Eniac .claude/skills/Eniac
```

**Codex** — user-wide:

```bash
cp -r skills/Eniac ~/.codex/skills/Eniac
```

On Windows the equivalent is `%USERPROFILE%\.codex\skills\Eniac`. `adapters/codex/openai.yaml`
carries interface metadata only; the behaviour still comes from `SKILL.md`.

**Any other runtime with a skills directory** — the same copy into whatever path it loads
skills from. Where a shared convention is supported, `.agents/skills/eniac/` works the
same way.

> Skill directory paths are set by each runtime and do change between versions. If the
> skill does not appear after a restart, check that runtime's current documentation for
> the path rather than assuming the one above is still right.

## Runtimes that read standing instruction files

Copy the adapter to the path that runtime reads. The script below takes the destination
from the same table the generator uses, so the path is stated once and never retyped —
which matters more here than it looks, because a typo'd path produces no error anywhere:

```bash
python scripts/install_adapter.py --list
python scripts/install_adapter.py --runtime cursor --into ../my-project
```

It refuses to overwrite an existing file, because a project's own rules outrank this skill.
Keep `skills/Eniac/` in the repository so the pointer inside the adapter resolves.

| Runtime | Copy this adapter | To |
| --- | --- | --- |
| Codex, Gemini CLI, Windsurf, Antigravity, Jules, Amp, and others on the convention | `adapters/agents-md/AGENTS.example.md` | `AGENTS.md` |
| Cursor | `adapters/cursor/eniac.mdc` | `.cursor/rules/eniac.mdc` |
| GitHub Copilot | `adapters/copilot/copilot-instructions.md` | `.github/copilot-instructions.md` |
| Windsurf | `adapters/windsurf/eniac.md` | `.windsurf/rules/eniac.md` |
| Cline, Roo Code | `adapters/cline/.clinerules` | `.clinerules` |
| Zed | `adapters/zed/rules.md` | `.rules` |
| Gemini CLI, Gemini Code Assist | `adapters/gemini/GEMINI.md` | `GEMINI.md` |
| Continue | `adapters/continue/eniac.md` | `.continue/rules/eniac.md` |
| Aider | `adapters/aider/CONVENTIONS.md` | `CONVENTIONS.md`, then `aider --read CONVENTIONS.md` |
| JetBrains Junie | `adapters/junie/guidelines.md` | `.junie/guidelines.md` |
| Claude Code | — | usually unnecessary; install the skill instead |

Paths are relative to `skills/Eniac/`. Every one of those files is generated from
`adapters/_source/core.md`, so the rules are identical across runtimes and cannot drift
apart — which is what makes a mixed-runtime team workable. Adjust the path *inside* the
adapter to wherever `skills/Eniac/` actually lives in your repository.

Adding a runtime that is not listed is one entry in `TARGETS` in
`scripts/build_adapters.py`, then `python scripts/build_adapters.py`.

If a project already has one of these files, **merge rather than replace**, and keep one
of them authoritative with the others pointing at it. Several instruction files that each
say something slightly different is the failure `references/documentation.md` describes:
every agent then reads a different version of the truth.

## Runtimes with only one instruction field

Custom GPTs, assistant configurations, chat system prompts, API integrations that set a
system prompt, IDE assistants with a single "custom instructions" box, and anything else
with no file system: paste the contents of

```txt
skills/Eniac/adapters/eniac-compact.md
```

It is self-contained and needs no other file. It is a distillation rather than a summary —
every rule in it is one the full skill would apply; what it drops is the depth behind each
rule.

## No installation at all

Clone the repository and point the agent at the file before the work:

```bash
git clone https://github.com/ParamissionLab/Eniac.git
```

Then:

```txt
Read Eniac/skills/Eniac/SKILL.md and follow it for this task.
```

This works on any agent that can read a local file, and it is the fastest way to try the
skill before deciding where to install it.

## Verifying the install

**Ask it.** This works identically on every runtime and takes one question:

```txt
What operating skill or rules are you currently following?
```

A loaded skill names itself. If the answer is a generic "I'm a helpful assistant with no
special rules", the file is not being read — and **nothing will have errored to tell you**.
That is the whole reason this check exists: an instruction file at the wrong path, or with
a front-matter key the runtime does not recognize, fails *silently* on every runtime there
is, and the agent behaves exactly as though nothing were installed.

The eval suite runs the same question as a gate before scoring anything, so a broken
install can never be misread as "the skill did not help":

```bash
python scripts/run_evals.py --agent-cmd '<your agent>' --only skill-reports-itself-loaded
```

Beyond that, the skill is working when behaviour changes in ways you can see:

- a trivial request gets a direct answer rather than a plan
- it says what it ran and what came back, instead of asserting a fix
- it stops and asks before anything destructive or irreversible
- adjacent cleanups show up under `Next:` rather than inside the diff

If none of that changes, the skill is probably not being loaded. Check the path, restart
the session, and — on runtimes with a skill list — confirm `eniac` appears in it.

This matters more for the adapter route than for the skill route, because an adapter fails
**silently**: a wrong filename or front-matter key produces no error, the file is simply
never read, and the agent behaves exactly as though nothing were installed. Every adapter
path in this repository is currently marked unconfirmed for that reason. If you check one
and it loads, recording it is one line — `skills/Eniac/adapters/README.md` says where.

For a sharper signal than reading behaviour by eye, the eval suite has cases for exactly
these claims:

```bash
python scripts/run_evals.py --agent-cmd '<your agent>' --label with-skill
```

## Updating

```bash
git pull
cp -r skills/Eniac ~/.claude/skills/Eniac
```

Replace the destination with wherever you installed it. Restart the agent afterwards.
Adapters change less often than the references; re-copy them only when
`skills/Eniac/adapters/` shows changes in the diff.

## Beyond one machine

Rolling this out to a team or a fleet — pinning a version, adding your own rules without
forking the skill, distributing it across repositories, and running it unattended — is
[ADOPTION.md](ADOPTION.md).
