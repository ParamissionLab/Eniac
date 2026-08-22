#!/usr/bin/env python3
"""Install a generated adapter into the path its runtime actually reads.

The adapters are correct; copying them by hand is where installs break. A wrong directory
or a typo'd filename produces **no error on any runtime** — the file is simply never read
and the agent behaves exactly as though nothing were installed. This script removes that
class of mistake by taking the destination from the same table the generator uses, so the
path is stated once and never retyped.

    python scripts/install_adapter.py --list
    python scripts/install_adapter.py --runtime cursor --into ../my-project
    python scripts/install_adapter.py --runtime cursor --into ../my-project --force

Without --force an existing file is never overwritten: these are files people edit, and a
project's own rules outrank this skill (SKILL.md#precedence). You get a diff hint instead.

After installing, verify it actually loaded — ask the agent what rules it follows and see
whether it names the skill. INSTALL.md, *Verifying the install*. Standard library only.
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ADAPTERS = ROOT / "skills" / "Eniac" / "adapters"

sys.path.insert(0, str(ROOT / "scripts"))
import build_adapters  # noqa: E402

# runtime key -> (adapter file under adapters/, destination relative to the target repo)
DESTINATIONS: dict[str, tuple[str, str]] = {
    "agents-md": ("agents-md/AGENTS.example.md", "AGENTS.md"),
    "cursor": ("cursor/eniac.mdc", ".cursor/rules/eniac.mdc"),
    "copilot": ("copilot/copilot-instructions.md", ".github/copilot-instructions.md"),
    "windsurf": ("windsurf/eniac.md", ".windsurf/rules/eniac.md"),
    "cline": ("cline/.clinerules", ".clinerules"),
    "zed": ("zed/rules.md", ".rules"),
    "gemini": ("gemini/GEMINI.md", "GEMINI.md"),
    "continue": ("continue/eniac.md", ".continue/rules/eniac.md"),
    "aider": ("aider/CONVENTIONS.md", "CONVENTIONS.md"),
    "junie": ("junie/guidelines.md", ".junie/guidelines.md"),
    "generic": ("generic/system-prompt.md", "eniac-system-prompt.md"),
}


def runtime_note(key: str) -> str:
    for t in build_adapters.TARGETS:
        if t["out"] == DESTINATIONS[key][0]:
            confirmed = t.get("verified") or "path not confirmed by an install"
            return f"{t['runtime']}  [{confirmed}]"
    return "unknown"


def do_list() -> int:
    print("runtime      destination in the target repo        for")
    print("-" * 78)
    for key, (_, dest) in DESTINATIONS.items():
        print(f"{key:<12} {dest:<36} {runtime_note(key)}")
    print("\nEvery destination above comes from that runtime's own documentation rather")
    print("than from an install performed here. If you confirm one works, record it:")
    print("set `verified` for that target in scripts/build_adapters.py and re-run it.")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--runtime", choices=sorted(DESTINATIONS))
    ap.add_argument("--into", help="path to the repository that should get the adapter")
    ap.add_argument("--force", action="store_true", help="overwrite an existing file")
    ap.add_argument("--list", action="store_true", help="show runtimes and destinations")
    args = ap.parse_args()

    if args.list or not args.runtime:
        return do_list()
    if not args.into:
        print("--into is required: the repository that should receive the adapter",
              file=sys.stderr)
        return 1

    src_rel, dest_rel = DESTINATIONS[args.runtime]
    src = ADAPTERS / src_rel
    target_root = Path(args.into).expanduser().resolve()
    dest = target_root / dest_rel

    if not src.exists():
        print(f"missing adapter {src} — run scripts/build_adapters.py", file=sys.stderr)
        return 1
    if not target_root.is_dir():
        print(f"not a directory: {target_root}", file=sys.stderr)
        return 1

    if dest.exists() and not args.force:
        same = dest.read_text(encoding="utf-8") == src.read_text(encoding="utf-8")
        if same:
            print(f"already installed and identical: {dest}")
            return 0
        print(f"{dest} already exists and differs.\n"
              f"  A project's own rules outrank this skill, so nothing was overwritten.\n"
              f"  Merge by hand, or re-run with --force if the file is a stale copy of "
              f"this adapter.", file=sys.stderr)
        return 1

    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dest)
    print(f"installed {src_rel} -> {dest}")
    print(f"  runtime: {runtime_note(args.runtime)}")
    print("\nNow confirm it loaded. Start the agent in that repository and ask:")
    print('  "What operating skill or rules are you currently following?"')
    print("If it does not name the skill, the file is not being read — the path or the")
    print("front-matter key is wrong, and nothing will have errored to tell you.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
