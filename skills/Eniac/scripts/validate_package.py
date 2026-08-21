#!/usr/bin/env python3
"""Validate the Eniac skill package with standard-library-only checks."""

from __future__ import annotations

import argparse
import ast
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote


FRONTMATTER = re.compile(r"\A---\s*\n(?P<body>.*?)\n---\s*\n", re.DOTALL)
REFERENCE_TOKEN = re.compile(r"(?<![\w/])references/[A-Za-z0-9._/-]+\.md")
MARKDOWN_LINK = re.compile(r"\[[^\]]*\]\((?P<target>[^)]+)\)")
REPO_PATH = re.compile(r"`(?P<path>skills/Eniac/(?:[^`\r\n]*))`")
FENCED_CODE = re.compile(r"^```[^\n]*\n.*?^```\s*$", re.MULTILINE | re.DOTALL)
COUNT_PATTERNS = (
    re.compile(r"\b(?P<count>\d+)\s+reference files\b", re.IGNORECASE),
    re.compile(
        r"\bThe\s+(?P<count>\d+)\s+files\s+in\s+`?references/`?",
        re.IGNORECASE,
    ),
)
EVAL_KINDS = {
    "trigger",
    "counter-trigger",
    "technique",
    "pressure",
    "recovery",
    "portability",
}
EVAL_ID = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def _read_text(path: Path, errors: list[str]) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        errors.append(f"cannot read {path}: {error}")
        return ""


def _resolve_doc_target(
    source: Path,
    raw_target: str,
    skill_dir: Path,
    repo_root: Path | None,
) -> Path | None:
    target = raw_target.strip().strip("<>")
    if not target:
        return None
    if re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:", target):
        return None

    path_text = unquote(target.split("#", 1)[0]).strip()
    if not path_text:
        return source
    if any(marker in path_text for marker in ("<", ">", "*", "{")):
        return None
    if path_text.startswith("references/"):
        return skill_dir / Path(path_text)
    if path_text.startswith("skills/Eniac/") and repo_root is not None:
        return repo_root / Path(path_text)
    return source.parent / Path(path_text)


def _markdown_anchors(text: str) -> set[str]:
    anchors: set[str] = set()
    duplicates: dict[str, int] = {}
    prose = FENCED_CODE.sub("", text)
    for match in re.finditer(r"^#{1,6}\s+(.+?)\s*#*\s*$", prose, re.MULTILINE):
        heading = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", match.group(1))
        heading = re.sub(r"<[^>]+>", "", heading)
        heading = re.sub(r"[`*_~]", "", heading).strip().lower()
        base = re.sub(r"[^\w\- ]", "", heading, flags=re.UNICODE)
        base = re.sub(r"\s", "-", base)
        duplicate = duplicates.get(base, 0)
        anchor = base if duplicate == 0 else f"{base}-{duplicate}"
        duplicates[base] = duplicate + 1
        anchors.add(anchor)
    return anchors


def _validate_frontmatter(skill_file: Path, text: str, errors: list[str]) -> None:
    match = FRONTMATTER.match(text)
    if not match:
        errors.append(f"{skill_file}: missing or malformed YAML frontmatter")
        return

    body = match.group("body")
    name = re.search(r"^name:\s*(\S+)\s*$", body, re.MULTILINE)
    description = re.search(r"^description:\s*(.+)$", body, re.MULTILINE)
    if name is None or name.group(1).strip('"\'') != "eniac":
        errors.append(f"{skill_file}: frontmatter name must be eniac")
    if description is None or not description.group(1).strip().strip('"\''):
        errors.append(f"{skill_file}: frontmatter description must be non-empty")


def _validate_reference_catalog(
    skill_dir: Path,
    skill_text: str,
    errors: list[str],
) -> list[Path]:
    references_dir = skill_dir / "references"
    if not references_dir.is_dir():
        errors.append(f"missing references directory: {references_dir}")
        return []

    actual = sorted(references_dir.rglob("*.md"))
    by_token = {
        f"references/{path.relative_to(references_dir).as_posix()}": path
        for path in actual
    }
    by_resolved_path = {path.resolve(): token for token, path in by_token.items()}
    pending = list(
        dict.fromkeys(match.group(0) for match in REFERENCE_TOKEN.finditer(skill_text))
    )
    reachable: set[str] = set()

    while pending:
        token = pending.pop(0)
        if token in reachable:
            continue
        target = by_token.get(token)
        if target is None:
            errors.append(f"skill graph routes a missing reference: {token}")
            continue
        reachable.add(token)
        target_text = _read_text(target, errors)
        for match in REFERENCE_TOKEN.finditer(target_text):
            child = match.group(0)
            if child not in reachable and child not in pending:
                pending.append(child)
        prose = FENCED_CODE.sub("", target_text)
        for match in MARKDOWN_LINK.finditer(prose):
            linked = _resolve_doc_target(
                target,
                match.group("target"),
                skill_dir,
                None,
            )
            if linked is None:
                continue
            child = by_resolved_path.get(linked.resolve())
            if child is not None and child not in reachable and child not in pending:
                pending.append(child)

    for token in sorted(set(by_token) - reachable):
        errors.append(f"reference is unreachable from SKILL.md: {token}")
    return actual


def _validate_document_links(
    documents: list[Path],
    skill_dir: Path,
    repo_root: Path | None,
    errors: list[str],
) -> None:
    for source in documents:
        text = _read_text(source, errors)
        if not text:
            continue

        prose = FENCED_CODE.sub("", text)
        targets = [match.group("target") for match in MARKDOWN_LINK.finditer(prose)]
        targets.extend(match.group(0) for match in REFERENCE_TOKEN.finditer(prose))
        for raw_target in targets:
            target = _resolve_doc_target(source, raw_target, skill_dir, repo_root)
            if target is not None and not target.exists():
                errors.append(f"{source}: missing local target {raw_target}")
                continue
            if target is None or "#" not in raw_target or target.suffix.lower() != ".md":
                continue
            anchor = unquote(raw_target.rsplit("#", 1)[1]).strip().lower()
            if not anchor or any(marker in anchor for marker in ("<", ">", "{")):
                continue
            target_text = _read_text(target, errors)
            if anchor not in _markdown_anchors(target_text):
                errors.append(f"{source}: missing local anchor {raw_target}")


def _validate_python(skill_dir: Path, errors: list[str]) -> list[Path]:
    python_files = sorted(
        path
        for directory in (skill_dir / "scripts", skill_dir / "tests")
        if directory.is_dir()
        for path in directory.rglob("*.py")
    )
    for path in python_files:
        text = _read_text(path, errors)
        if not text:
            continue
        try:
            ast.parse(text, filename=str(path))
        except SyntaxError as error:
            errors.append(f"{path}:{error.lineno}: Python syntax error: {error.msg}")
    return python_files


def _non_empty_string_list(value: object) -> bool:
    return (
        isinstance(value, list)
        and bool(value)
        and all(isinstance(item, str) and bool(item.strip()) for item in value)
    )


def _validate_evals(skill_dir: Path, errors: list[str]) -> list[Path]:
    evals_dir = skill_dir / "evals"
    if not evals_dir.exists():
        return []
    if not evals_dir.is_dir():
        errors.append(f"evals path is not a directory: {evals_dir}")
        return []

    manifest = evals_dir / "scenarios.json"
    if not manifest.is_file():
        errors.append(f"missing evaluation scenario manifest: {manifest}")
        return []

    text = _read_text(manifest, errors)
    if not text:
        return [manifest]
    try:
        payload = json.loads(text)
    except json.JSONDecodeError as error:
        errors.append(
            f"{manifest}:{error.lineno}: invalid JSON: {error.msg}"
        )
        return [manifest]

    if not isinstance(payload, dict):
        errors.append(f"{manifest}: root must be an object")
        return [manifest]
    if payload.get("schema_version") != 1:
        errors.append(f"{manifest}: schema_version must be 1")

    scenarios = payload.get("scenarios")
    if not isinstance(scenarios, list) or not scenarios:
        errors.append(f"{manifest}: scenarios must be a non-empty list")
        return [manifest]

    seen_ids: set[str] = set()
    for index, scenario in enumerate(scenarios):
        label = f"{manifest}: scenarios[{index}]"
        if not isinstance(scenario, dict):
            errors.append(f"{label} must be an object")
            continue

        scenario_id = scenario.get("id")
        if not isinstance(scenario_id, str) or not EVAL_ID.fullmatch(scenario_id):
            errors.append(f"{label}.id must be unique lower-kebab-case")
        elif scenario_id in seen_ids:
            errors.append(f"{label}.id is duplicated: {scenario_id}")
        else:
            seen_ids.add(scenario_id)

        kind = scenario.get("kind")
        if kind not in EVAL_KINDS:
            errors.append(
                f"{label}.kind must be one of {', '.join(sorted(EVAL_KINDS))}"
            )
        prompt = scenario.get("prompt")
        if not isinstance(prompt, str) or not prompt.strip():
            errors.append(f"{label}.prompt must be a non-empty string")
        for field in ("expected", "anti_patterns"):
            if not _non_empty_string_list(scenario.get(field)):
                errors.append(f"{label}.{field} must be a non-empty string list")

    return [manifest]


def _validate_readme(
    repo_root: Path,
    reference_count: int,
    errors: list[str],
) -> list[Path]:
    readme = repo_root / "README.md"
    if not readme.is_file():
        errors.append(f"missing repository README: {readme}")
        return []

    text = _read_text(readme, errors)
    declared_counts = [
        int(match.group("count"))
        for pattern in COUNT_PATTERNS
        for match in pattern.finditer(text)
    ]
    if not declared_counts:
        errors.append("README.md must declare the number of reference files")
    for declared in declared_counts:
        if declared != reference_count:
            errors.append(
                "README.md reference count is stale: "
                f"declares {declared}, package contains {reference_count}"
            )

    for match in REPO_PATH.finditer(text):
        relative = match.group("path").strip()
        if any(marker in relative for marker in ("<", ">", "*", "{")):
            continue
        if not (repo_root / Path(relative)).exists():
            errors.append(f"README.md documents a missing path: {relative}")
    return [readme]


def validate_package(skill_dir: Path, repo_root: Path | None = None) -> list[str]:
    """Return package validation errors; an empty list means success."""

    skill_dir = skill_dir.resolve()
    repo_root = repo_root.resolve() if repo_root is not None else None
    errors: list[str] = []

    skill_file = skill_dir / "SKILL.md"
    if not skill_file.is_file():
        return [f"missing skill entrypoint: {skill_file}"]

    skill_text = _read_text(skill_file, errors)
    _validate_frontmatter(skill_file, skill_text, errors)
    references = _validate_reference_catalog(skill_dir, skill_text, errors)
    _validate_python(skill_dir, errors)
    _validate_evals(skill_dir, errors)

    documents = [skill_file, *references]
    if repo_root is not None:
        documents.extend(_validate_readme(repo_root, len(references), errors))
    _validate_document_links(documents, skill_dir, repo_root, errors)

    # De-duplicate identical failures from inline reference tokens and Markdown links.
    return list(dict.fromkeys(errors))


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
        "--repo-root",
        type=Path,
        help="optional repository root for README and documented-path checks",
    )
    args = parser.parse_args()

    errors = validate_package(args.skill_dir, args.repo_root)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(f"FAILED: {len(errors)} package validation error(s)", file=sys.stderr)
        return 1

    reference_count = len(list((args.skill_dir / "references").rglob("*.md")))
    python_count = sum(
        1
        for directory in (args.skill_dir / "scripts", args.skill_dir / "tests")
        if directory.is_dir()
        for _ in directory.rglob("*.py")
    )
    eval_count = 0
    eval_manifest = args.skill_dir / "evals" / "scenarios.json"
    if eval_manifest.is_file():
        try:
            payload = json.loads(eval_manifest.read_text(encoding="utf-8"))
            scenarios = payload.get("scenarios", [])
            eval_count = len(scenarios) if isinstance(scenarios, list) else 0
        except (OSError, UnicodeError, json.JSONDecodeError, AttributeError):
            eval_count = 0
    print(
        f"OK: validated Eniac package "
        f"({reference_count} references, {python_count} Python files, "
        f"{eval_count} evaluation scenarios)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
