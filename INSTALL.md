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

One script installs both — `scripts/install.py` — because the two routes fail in exactly
the same way and only the destination table differs. `--runtime` names either kind,
`--list` prints both tables, and every destination is stated once so nobody retypes a path.

## Straight from the repository URL, with no clone

```bash
curl -fsSL https://raw.githubusercontent.com/ParamissionLab/Eniac/main/scripts/install.py | python3 -
```

```powershell
irm https://raw.githubusercontent.com/ParamissionLab/Eniac/main/scripts/install.py | python -
```

Piped into an interpreter the script has no `skills/Eniac` beside it, so it downloads the
repository archive over HTTPS and installs from that. Arguments work as usual — everything
after `python3 -` is passed through:

```bash
curl -fsSL https://raw.githubusercontent.com/ParamissionLab/Eniac/main/scripts/install.py \
  | python3 - --ref v1.1.0 --dry-run
```

**Pin `--ref` for anything you rely on.** The default is `main`, which is whatever was
pushed a minute ago; an install that silently follows a moving branch is a dependency that
upgrades itself with no review. A tag or a full commit SHA both work.

Two things this does not do, because they are what makes `curl | interpreter` worth being
careful about: nothing from the download is *executed* — the archive is unpacked and files
are copied — and archive members that escape the extraction directory, or that are not
plain files or directories, are dropped before extraction rather than trusted. If you
would rather read the script before running it, download it first and run it as a file;
it is one file with no imports outside the standard library.

Cloning does the same thing with the files already local, which is the better choice when
you want to read the diff of an update before installing it:

```bash
git clone https://github.com/ParamissionLab/Eniac.git && cd Eniac
python scripts/install.py
```

## Runtimes with a skills directory

From a clone, one command installs into every runtime it finds on the machine:

```bash
python scripts/install.py
```

`.\install.ps1` and `./install.sh` do the same and find a Python first, which matters more
on Windows than it looks: the `python3` on `PATH` there is usually the Microsoft Store
stub, which exists, prints an advert, and installs nothing. Python 3.8+ is the only
requirement, and it is used to *copy files* — the skill itself has no runtime.

```bash
python scripts/install.py --list                # destinations, and what is already installed
python scripts/install.py --runtime claude      # one runtime, user-wide
python scripts/install.py --project ../my-app   # into that repository, checked in with it
python scripts/install.py --dry-run             # print the plan, change nothing
python scripts/install.py --backup              # keep the previous install under eniac-backups/
python scripts/install.py --uninstall
```

What it does that a copy does not: it removes reference files an older version left behind
— a stale reference keeps loading beside the file that replaced it, and contradicts it —
and it refuses a destination that is not an install of this skill, so a folder of somebody
else's work named `Eniac` is never overwritten silently. It writes nothing else, and
`--dry-run` will show you exactly what it would touch.

| Runtime | User-wide | Per-project |
| --- | --- | --- |
| Claude Code | `~/.claude/skills/Eniac` | `.claude/skills/Eniac` |
| Codex | `~/.codex/skills/Eniac` | `.codex/skills/Eniac` |
| The shared convention | `~/.agents/skills/eniac` | `.agents/skills/eniac` |

On Windows those are under `%USERPROFILE%`, which the script resolves for you.
`adapters/codex/openai.yaml` carries interface metadata only; the behaviour still comes
from `SKILL.md`.

Copying the folder in by hand works exactly as well — keep the name `Eniac`, keep
`SKILL.md` and `references/` together so the relative links resolve:

```bash
cp -r skills/Eniac ~/.claude/skills/Eniac
```

**Any other runtime with a skills directory** — `--into` takes the path directly:

```bash
python scripts/install.py --into ~/.config/some-agent/skills
```

Either way, restart the agent or start a new session afterwards so the skill list
refreshes; a running session keeps whatever it loaded at start.

> Skill directory paths are set by each runtime and do change between versions. If the
> skill does not appear after a restart, check that runtime's current documentation for
> the path rather than assuming the one above is still right.

## Runtimes that read standing instruction files

Copy the adapter to the path that runtime reads — the same installer, naming the runtime
and the repository that receives the file. The path is stated once and never retyped,
which matters more here than it looks, because a typo'd path produces no error anywhere:

```bash
python scripts/install.py --list                              # both tables
python scripts/install.py --runtime cursor --project ../my-project
python scripts/install.py --runtime cursor --project ../my-project --uninstall
```

It refuses to overwrite an existing file, because a project's own rules outrank this skill.
Keep `skills/Eniac/` in the repository so the pointer inside the adapter resolves.

Three of these runtimes document a **user-wide** path as well, so `--project` is optional
for them and the file applies to every repository you open:

| Runtime | User-wide destination |
| --- | --- |
| Kiro | `~/.kiro/steering/eniac.md` |
| Gemini CLI | `~/.gemini/GEMINI.md` |
| Codex, via the AGENTS.md adapter | `~/.codex/AGENTS.md` |

```bash
python scripts/install.py --runtime kiro        # no --project needed
```

The rest are project files on purpose — a team's rules belong in the repository where
everyone gets them — so the installer asks which repository rather than inventing a
home-directory path that runtime would never read.

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
| Kiro | `adapters/kiro/eniac.md` | `.kiro/steering/eniac.md`, or `~/.kiro/steering/eniac.md` for every workspace. Kiro also reads `AGENTS.md`, so a project that already has one can merge the `agents-md` adapter into it instead of carrying both |
| Claude Code | — | usually unnecessary; install the skill instead |

Paths are relative to `skills/Eniac/`. Every one of those files is generated from
`adapters/_source/core.md`, so the rules are identical across runtimes and cannot drift
apart — which is what makes a mixed-runtime team workable. Adjust the path *inside* the
adapter to wherever `skills/Eniac/` actually lives in your repository.

Adding a runtime that is not listed is one entry in `TARGETS` in
`scripts/build_adapters.py`, then `python scripts/build_adapters.py`, plus its destination
in `ADAPTER_RUNTIMES` in `scripts/install.py` — what to generate and where it goes are
two different facts.

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
python scripts/install.py
```

An update is the same command as the install: it writes to wherever it already finds a
copy, replaces only the files that changed, and deletes the ones this version no longer
ships. That last part is the reason to prefer it over re-copying — a reference removed in
a later version keeps loading from the old install, and it will contradict the file that
replaced it. Restart the agent afterwards.

Adapters are separate and change less often than the references; re-install one only when
`skills/Eniac/adapters/` shows changes in the diff.

## Beyond one machine

Rolling this out to a team or a fleet — pinning a version, adding your own rules without
forking the skill, distributing it across repositories, and running it unattended — is
[ADOPTION.md](ADOPTION.md).
