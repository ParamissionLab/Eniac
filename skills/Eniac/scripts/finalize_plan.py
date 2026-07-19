#!/usr/bin/env python3
"""Safely finalize an Eniac execution plan.

Default behavior is delete-on-complete. Pass --retain only when the user or
repository policy explicitly requires keeping the completed context plan.
The command is idempotent when the target plan is already absent.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


PLAN_NAME = re.compile(r"^\.eniac-plan(?:-\d+)?\.md$")
DONE_STATUS = re.compile(r"^\s*>\s*Status:\s*done\s*$", re.MULTILINE)
RETENTION = re.compile(
    r"^\s*>\s*Retention:\s*(delete-on-complete|retain-by-explicit-request)\s*$",
    re.MULTILINE,
)
OWNER = re.compile(r"^\s*>\s*Owner:\s*(\S(?:.*\S)?)\s*$", re.MULTILINE)


def fail(message: str) -> int:
    print(f"ERROR: {message}", file=sys.stderr)
    return 1


def finalize(plan: Path, retain: bool, workspace_root: Path, owner: str) -> int:
    expanded = plan.expanduser()
    if expanded.is_symlink():
        return fail("refusing to operate on a symlink")
    resolved = expanded.resolve()
    workspace = workspace_root.expanduser().resolve()
    if not workspace.is_dir():
        return fail(f"workspace root is not a directory: {workspace}")
    try:
        resolved.relative_to(workspace)
    except ValueError:
        return fail(f"refusing a plan outside workspace root {workspace}")
    if not PLAN_NAME.fullmatch(resolved.name):
        return fail("refusing a path that is not an Eniac plan filename")
    if not resolved.exists():
        print("OK: plan already absent")
        return 0
    if not resolved.is_file():
        return fail("refusing a non-file plan path")

    try:
        content = resolved.read_text(encoding="utf-8")
    except OSError as error:
        return fail(f"cannot read {resolved}: {error}")

    if not DONE_STATUS.search(content):
        return fail("plan must have Status: done before finalization")

    owner_match = OWNER.search(content)
    if not owner_match:
        return fail("plan must declare a non-empty Owner before finalization")
    if owner_match.group(1) != owner:
        return fail("plan Owner does not match the expected task owner")

    retention_match = RETENTION.search(content)
    retention = retention_match.group(1) if retention_match else "delete-on-complete"
    if retain:
        if retention != "retain-by-explicit-request":
            return fail("--retain requires Retention: retain-by-explicit-request")
        print(f"OK: retained completed plan at {resolved}")
        return 0
    if retention == "retain-by-explicit-request":
        return fail("plan requests retention; pass --retain only with explicit authorization")

    try:
        resolved.unlink()
    except OSError as error:
        return fail(f"could not delete {resolved}: {error}")

    if resolved.exists():
        return fail(f"deletion was reported but the plan still exists at {resolved}")
    print(f"OK: deleted {resolved}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plan", type=Path, help="exact .eniac-plan*.md path")
    parser.add_argument(
        "--workspace-root",
        type=Path,
        required=True,
        help="workspace boundary; the plan must be inside it",
    )
    parser.add_argument(
        "--owner",
        required=True,
        help="exact non-empty task owner recorded in the plan",
    )
    parser.add_argument(
        "--retain",
        action="store_true",
        help="retain only when the plan explicitly opts into retention",
    )
    args = parser.parse_args()
    return finalize(args.plan, args.retain, args.workspace_root, args.owner)


if __name__ == "__main__":
    raise SystemExit(main())
