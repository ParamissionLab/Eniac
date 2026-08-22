#!/usr/bin/env python3
"""Generate the per-runtime adapter files from one source.

Every runtime that reads standing instructions wants the same rules in a slightly
different wrapper: a filename it looks for, sometimes front matter, sometimes a heading.
Hand-writing one file per runtime means one copy per runtime, and copies drift — the exact
failure `references/documentation.md` describes, committed by the package that describes it.

So the rules live once, in `skills/Eniac/adapters/_source/core.md`, and this script wraps
them per target. Adding a runtime is one entry in TARGETS below.

    python scripts/build_adapters.py            # write the files
    python scripts/build_adapters.py --check     # fail if any file is out of date (CI)

Standard library only. `eniac-compact.md` and `codex/openai.yaml` are deliberately
hand-written and are not generated here — the compact file is a real distillation rather
than a reformat, and the yaml is interface metadata with no rules in it.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ADAPTERS = ROOT / "skills" / "Eniac" / "adapters"
SOURCE = ADAPTERS / "_source" / "core.md"

BANNER = (
    "<!-- Generated from skills/Eniac/adapters/_source/core.md by "
    "scripts/build_adapters.py. Edit the source, not this file. -->"
)

# path relative to adapters/, the file the runtime actually reads, and the wrapper.
#   header:  text placed above the rules (front matter, title, banner)
#   comment: how this format carries the "generated" banner, or None to omit it
TARGETS: list[dict] = [
    {
        "out": "agents-md/AGENTS.example.md",
        "runtime": "Codex, Gemini CLI, Windsurf, Antigravity, Jules, Amp, and anything "
                   "else on the AGENTS.md convention",
        "install": "merge into the project's AGENTS.md",
        "header": "# AGENTS.md — Eniac section\n\n"
                  "Merge this section into the project's `AGENTS.md`, or use it as the "
                  "file if none exists.\n\n## Engineering behaviour — Eniac\n",
    },
    {
        "out": "cursor/eniac.mdc",
        "runtime": "Cursor",
        "install": "copy to .cursor/rules/eniac.mdc",
        "header": "---\n"
                  "description: Eniac — scale effort to real risk, stay in scope, prove "
                  "before claiming.\n"
                  "alwaysApply: true\n"
                  "---\n\n# Eniac\n",
    },
    {
        "out": "copilot/copilot-instructions.md",
        "runtime": "GitHub Copilot (chat, agent mode, and coding agent)",
        "install": "copy to .github/copilot-instructions.md",
        "header": "# Copilot instructions — Eniac\n",
    },
    {
        "out": "windsurf/eniac.md",
        "runtime": "Windsurf",
        "install": "copy to .windsurf/rules/eniac.md",
        "header": "---\ntrigger: always_on\n---\n\n# Eniac\n",
    },
    {
        "out": "cline/.clinerules",
        "runtime": "Cline and Roo Code",
        "install": "copy to .clinerules in the project root",
        "header": "# Eniac\n",
    },
    {
        "out": "zed/rules.md",
        "runtime": "Zed",
        "install": "copy to .rules in the project root",
        "header": "# Eniac\n",
    },
    {
        "out": "gemini/GEMINI.md",
        "runtime": "Gemini CLI and Gemini Code Assist",
        "install": "copy to GEMINI.md in the project root",
        "header": "# GEMINI.md — Eniac\n",
    },
    {
        "out": "continue/eniac.md",
        "runtime": "Continue",
        "install": "copy to .continue/rules/eniac.md",
        "header": "---\nname: Eniac\nalwaysApply: true\n---\n\n# Eniac\n",
    },
    {
        "out": "aider/CONVENTIONS.md",
        "runtime": "Aider",
        "install": "add with `aider --read CONVENTIONS.md`",
        "header": "# Conventions — Eniac\n",
    },
    {
        "out": "junie/guidelines.md",
        "runtime": "JetBrains Junie",
        "install": "copy to .junie/guidelines.md",
        "header": "# Project guidelines — Eniac\n",
    },
    {
        "out": "generic/system-prompt.md",
        "runtime": "any assistant with a single instruction field, and any API integration",
        "install": "paste as the system prompt, or prepend to it",
        "header": "# Eniac\n",
    },
]


def banner_for(path: str) -> str | None:
    if path.endswith(".mdc") or path.endswith(".md"):
        return BANNER
    return "# " + BANNER.strip("<!->").strip()


def render(target: dict, rules: str) -> str:
    parts = [target["header"].rstrip("\n"), "", banner_for(target["out"]), "", rules.strip(), ""]
    return "\n".join(p for p in parts if p is not None).replace("\n\n\n", "\n\n")


def build(check_only: bool = False) -> int:
    if not SOURCE.exists():
        print(f"missing source: {SOURCE.relative_to(ROOT)}", file=sys.stderr)
        return 1
    rules = SOURCE.read_text(encoding="utf-8")

    stale: list[str] = []
    for target in TARGETS:
        out = ADAPTERS / target["out"]
        want = render(target, rules)
        have = out.read_text(encoding="utf-8") if out.exists() else None
        if have == want:
            continue
        if check_only:
            stale.append(target["out"])
        else:
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(want, encoding="utf-8", newline="\n")
            print(f"wrote adapters/{target['out']}")

    if check_only:
        if stale:
            for s in stale:
                print(f"adapters/{s}: out of date - run `python scripts/build_adapters.py`")
            return 1
        print(f"ok - {len(TARGETS)} generated adapters match adapters/_source/core.md")
        return 0

    write_index(rules)
    print(f"ok - {len(TARGETS)} adapters generated from adapters/_source/core.md")
    return 0


def write_index(rules: str) -> None:
    """The adapters README is a listing, so it is generated from the same table."""
    rows = "\n".join(
        f"| `{t['out']}` | {t['runtime']} | {t['install']} |" for t in TARGETS
    )
    text = f"""# Adapters

{BANNER}

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

| File | For | Install |
| --- | --- | --- |
{rows}

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
"""
    (ADAPTERS / "README.md").write_text(text, encoding="utf-8", newline="\n")
    print("wrote adapters/README.md")


if __name__ == "__main__":
    raise SystemExit(build(check_only="--check" in sys.argv))
