#!/usr/bin/env python3
"""Report provider-neutral context-cost proxies for the Eniac package.

Exact token counts depend on the model and tokenizer. This audit uses stable
line, Unicode-character, and UTF-8-byte counts so package growth and reductions
can be compared without adding a tokenizer dependency.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path


REFERENCE_TOKEN = re.compile(r"(?<![\w/])references/[A-Za-z0-9._/-]+\.md")


@dataclass(frozen=True)
class FileMetrics:
    path: str
    lines: int
    characters: int
    utf8_bytes: int


@dataclass(frozen=True)
class ContextMetrics:
    entry: FileMetrics
    reference_files: int
    reference_characters: int
    reference_utf8_bytes: int
    direct_reference_routes: int
    largest_references: tuple[FileMetrics, ...]


def _measure_file(path: Path, root: Path) -> FileMetrics:
    text = path.read_text(encoding="utf-8")
    return FileMetrics(
        path=path.relative_to(root).as_posix(),
        lines=len(text.splitlines()),
        characters=len(text),
        utf8_bytes=len(text.encode("utf-8")),
    )


def audit_context(skill_dir: Path, largest: int = 8) -> ContextMetrics:
    """Measure the always-loaded entry and load-on-demand reference corpus."""

    skill_dir = skill_dir.resolve()
    if largest < 0:
        raise ValueError("largest must be zero or greater")

    skill_file = skill_dir / "SKILL.md"
    if not skill_file.is_file():
        raise FileNotFoundError(f"missing skill entrypoint: {skill_file}")

    entry = _measure_file(skill_file, skill_dir)
    skill_text = skill_file.read_text(encoding="utf-8")
    reference_paths = sorted((skill_dir / "references").rglob("*.md"))
    reference_metrics = [
        _measure_file(path, skill_dir) for path in reference_paths
    ]
    ranked = sorted(
        reference_metrics,
        key=lambda item: (-item.characters, item.path),
    )
    direct_routes = {
        match.group(0) for match in REFERENCE_TOKEN.finditer(skill_text)
    }

    return ContextMetrics(
        entry=entry,
        reference_files=len(reference_metrics),
        reference_characters=sum(item.characters for item in reference_metrics),
        reference_utf8_bytes=sum(item.utf8_bytes for item in reference_metrics),
        direct_reference_routes=len(direct_routes),
        largest_references=tuple(ranked[:largest]),
    )


def budget_errors(
    metrics: ContextMetrics,
    max_entry_characters: int | None,
) -> list[str]:
    errors: list[str] = []
    if max_entry_characters is not None and max_entry_characters < 1:
        errors.append("--max-entry-characters must be positive")
    elif (
        max_entry_characters is not None
        and metrics.entry.characters > max_entry_characters
    ):
        errors.append(
            "SKILL.md context budget exceeded: "
            f"{metrics.entry.characters} > {max_entry_characters} characters"
        )
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "skill_dir",
        nargs="?",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="Eniac skill directory (defaults to the parent of this script)",
    )
    parser.add_argument(
        "--largest",
        type=int,
        default=8,
        help="number of largest references to report (default: 8)",
    )
    parser.add_argument(
        "--max-entry-characters",
        type=int,
        help="fail when always-loaded SKILL.md exceeds this measured size",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="emit machine-readable JSON",
    )
    args = parser.parse_args()

    try:
        metrics = audit_context(args.skill_dir, args.largest)
    except (FileNotFoundError, OSError, UnicodeError, ValueError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1

    errors = budget_errors(metrics, args.max_entry_characters)
    if args.json:
        payload = asdict(metrics)
        payload["budget_errors"] = errors
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(
            "Entry: "
            f"{metrics.entry.lines} lines, "
            f"{metrics.entry.characters} characters, "
            f"{metrics.entry.utf8_bytes} UTF-8 bytes"
        )
        print(
            "References: "
            f"{metrics.reference_files} files, "
            f"{metrics.reference_characters} characters, "
            f"{metrics.reference_utf8_bytes} UTF-8 bytes (load on demand)"
        )
        print(f"Direct reference routes: {metrics.direct_reference_routes}")
        if metrics.largest_references:
            print("Largest references:")
            for item in metrics.largest_references:
                print(f"  {item.characters:>7}  {item.path}")
        print("Note: exact tokens vary by model/tokenizer; compare measured proxies.")

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
