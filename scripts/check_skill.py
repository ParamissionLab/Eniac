#!/usr/bin/env python3
"""Structural checks for the Eniac skill package.

This repository is prose that steers behaviour, so most of its quality is judgment and
stays manual. What is *not* judgment — whether a path resolves, whether an anchor exists,
whether the four places that list the reference files still agree — drifts silently and is
exactly what a script should own.

Standard library only, no arguments, run from anywhere:

    python scripts/check_skill.py

Exits 0 when everything holds, 1 with one line per problem when it does not.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL_DIR = ROOT / "skills" / "Eniac"
SKILL = SKILL_DIR / "SKILL.md"
REFS = SKILL_DIR / "references"
ADAPTERS = SKILL_DIR / "adapters"

# Files that name a vendor's instruction file legitimately, because the surrounding text
# is an enumeration of the runtimes this skill supports rather than an assumption.
VENDOR_FILE_ALLOWED = {
    "SKILL.md",
    "build_adapters.py",
    "check_skill.py",
    "documentation.md",
    "learning-loop.md",
    "INSTALL.md",
    "README.md",
    "CONTRIBUTING.md",
    "CHANGELOG.md",
    "AGENTS.example.md",
    "eniac-compact.md",
    "ADOPTION.md",
}

problems: list[str] = []


def fail(msg: str) -> None:
    problems.append(msg)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def slug(heading: str) -> str:
    """GitHub's heading-to-anchor rule, close enough for our headings."""
    s = heading.strip().lower()
    s = re.sub(r"[`*_]", "", s)
    s = re.sub(r"[^\w\s-]", "", s)
    return re.sub(r"\s+", "-", s).strip("-")


def check_frontmatter() -> None:
    text = read(SKILL)
    if not text.startswith("---\n"):
        fail("SKILL.md: missing YAML front matter")
        return
    end = text.find("\n---\n", 4)
    if end == -1:
        fail("SKILL.md: front matter is not terminated")
        return
    fm = text[4:end]
    for key in ("name", "description"):
        if not re.search(rf"^{key}:", fm, re.M):
            fail(f"SKILL.md: front matter has no `{key}`")
    name = re.search(r"^name:\s*(\S+)", fm, re.M)
    if name and name.group(1).strip("\"'") != "eniac":
        fail(f"SKILL.md: front matter name is {name.group(1)!r}, expected 'eniac'")


def markdown_files() -> list[Path]:
    files = [SKILL, *sorted(REFS.glob("*.md"))]
    files += sorted(ADAPTERS.rglob("*.md"))
    files += [ROOT / n for n in ("README.md", "CONTRIBUTING.md", "INSTALL.md")]
    return [f for f in files if f.exists()]


def check_reference_links() -> None:
    """Every `something.md` and `something.md#anchor` mentioned must resolve."""
    known = {p.name for p in REFS.glob("*.md")}
    headings: dict[str, set[str]] = {}
    for p in REFS.glob("*.md"):
        headings[p.name] = {slug(m) for m in re.findall(r"^#{1,6}\s+(.+)$", read(p), re.M)}
    headings["SKILL.md"] = {
        slug(m) for m in re.findall(r"^#{1,6}\s+(.+)$", read(SKILL), re.M)
    }

    pattern = re.compile(r"`(?:references/)?([a-z][a-z\-]*\.md)(#[a-z0-9\-]+)?`")
    for path in markdown_files():
        for m in pattern.finditer(read(path)):
            target, anchor = m.group(1), m.group(2)
            if target not in known and target != "SKILL.md":
                continue  # a doc filename being described, not a link into this package
            if anchor:
                a = anchor[1:]
                if a not in headings.get(target, set()):
                    rel = path.relative_to(ROOT)
                    fail(f"{rel}: `{target}{anchor}` does not match a heading in {target}")


def check_registration() -> None:
    """The four places listing the reference files must agree with the directory."""
    actual = {p.name for p in REFS.glob("*.md")}
    listings = {
        "SKILL.md ## References": read(SKILL).split("## References", 1)[-1],
        "README.md": read(ROOT / "README.md"),
        "CONTRIBUTING.md": read(ROOT / "CONTRIBUTING.md"),
    }
    for where, text in listings.items():
        for name in sorted(actual):
            if name not in text:
                fail(f"{where}: does not register `{name}`")

    body = read(SKILL) + "".join(read(p) for p in REFS.glob("*.md"))
    for name in sorted(actual):
        others = body.replace(read(REFS / name), "")
        if name not in others:
            fail(f"references/{name}: nothing points at it, so it will never load")


def check_load_condition() -> None:
    """A reference nobody knows when to load is a reference that loads at the wrong time."""
    cues = ("load ", "loaded ", "load it", "use this", "reached by", "carries")
    for p in sorted(REFS.glob("*.md")):
        opening = "\n".join(read(p).split("\n")[:22]).lower()
        if not any(c in opening for c in cues):
            fail(f"references/{p.name}: opening lines do not state when to load it")


def check_tables() -> None:
    for path in markdown_files():
        lines = read(path).split("\n")
        i = 0
        while i < len(lines):
            if lines[i].startswith("|") and i + 1 < len(lines) and re.match(
                r"^\|[\s\-:|]+\|$", lines[i + 1]
            ):
                width = lines[i].count("|")
                j = i
                while j < len(lines) and lines[j].startswith("|"):
                    if lines[j].count("|") != width:
                        rel = path.relative_to(ROOT)
                        fail(f"{rel}:{j + 1}: table row has the wrong number of columns")
                    j += 1
                i = j
            else:
                i += 1


def check_vendor_neutrality() -> None:
    """Naming one vendor's file where a capability was meant breaks every other runtime."""
    for path in markdown_files():
        if path.name in VENDOR_FILE_ALLOWED:
            continue
        text = read(path)
        for token in ("CLAUDE.md", "Claude Code", "Anthropic"):
            if token in text:
                rel = path.relative_to(ROOT)
                fail(
                    f"{rel}: mentions {token}; name the capability instead "
                    f"(the repository's agent instruction file) or add the file to "
                    f"VENDOR_FILE_ALLOWED with a reason"
                )


def check_adapters() -> None:
    expected = [
        ADAPTERS / "README.md",
        ADAPTERS / "eniac-compact.md",
        ADAPTERS / "_source" / "core.md",
        ADAPTERS / "codex" / "openai.yaml",
        ROOT / "INSTALL.md",
    ]
    for p in expected:
        if not p.exists():
            fail(f"{p.relative_to(ROOT)}: missing")

    # The generated adapters must match what the generator would produce right now.
    # Without this, editing an adapter by hand silently forks it from every other runtime.
    sys.path.insert(0, str(ROOT / "scripts"))
    try:
        import build_adapters
    except Exception as exc:  # pragma: no cover - only when the generator is broken
        fail(f"scripts/build_adapters.py: cannot be imported ({exc})")
    else:
        for target in build_adapters.TARGETS:
            out = ADAPTERS / target["out"]
            if not out.exists():
                fail(f"adapters/{target['out']}: missing - run scripts/build_adapters.py")
            elif read(out) != build_adapters.render(target, read(build_adapters.SOURCE)):
                fail(
                    f"adapters/{target['out']}: does not match _source/core.md - "
                    f"edit the source and run scripts/build_adapters.py"
                )

    compact = ADAPTERS / "eniac-compact.md"
    if compact.exists():
        text = read(compact)
        # The compact file is the one deliberate restatement, so it is the one that
        # drifts. These are the load-bearing rules; their absence means it fell behind.
        for phrase, why in [
            ("Unverified", "the verification escape hatch"),
            ("irreversible", "the authorization gate"),
            ("WIP = 1", "the triage discipline"),
            ("One owner per fact", "the documentation rule"),
            ("capabilities, not tools", "the portability contract"),
            ("Silence is never consent", "the unattended-gate rule"),
        ]:
            if phrase not in text:
                fail(f"adapters/eniac-compact.md: missing {why} (`{phrase}`)")


def main() -> int:
    if not SKILL.exists():
        print(f"cannot find {SKILL}", file=sys.stderr)
        return 1
    check_frontmatter()
    check_reference_links()
    check_registration()
    check_load_condition()
    check_tables()
    check_vendor_neutrality()
    check_adapters()

    if problems:
        for p in problems:
            print(p)
        print(f"\n{len(problems)} problem(s).")
        return 1
    refs = len(list(REFS.glob("*.md")))
    print(f"ok - SKILL.md + {refs} references, links, registration, and adapters agree.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
