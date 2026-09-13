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

# The control plane is loaded on every invocation, so its size is a cost paid by every
# task including trivial ones. A budget nobody enforces is a wish (references/performance.md),
# so this one fails the build.
#
# It is NOT a target to shrink toward. A control plane too thin to settle the next action
# pushes the work into a reference, and a reference is 150-200 lines loaded at full price
# on exactly the tasks that were supposed to be cheap - so twenty lines cut here can cost
# two hundred there. The budget exists to make growth deliberate, not to make the file
# small. Raise it when the content earns it, in a commit that says why.
# Raised from 560 when defect-sets.md landed. Three capability additions - system types,
# collaboration, defect sets - each earned a hook in the always-loaded plane, and a hook
# that only names a file does not fire on its own. The char budget is the real guard;
# this number exists to make growth a decision rather than a drift, so move it in a
# commit that says why.
#
# Raised again from 580/40k when code-health.md landed. A whole-codebase quality pass -
# "clean this up", "scan the project" - was the one common request with no route, so it
# arrived as an unbounded Sweep or an unrequested refactor. It earned four lines: a route
# row, a map entry, and a clause on the triage ladder saying that cleanup as the *request*
# is a route with its own scope gate rather than tier-6 work done anyway.
#
# Raised again from 590/41k for three gates that only work if they are always loaded: the
# adversarial pass before a done claim, the four-field request a stopped gate emits, and
# the read budget (three anchors, one hop at a time) with the price-it-first rule on
# expensive moves. Each of those fires on ordinary work rather than on a route, so a
# reference-only version would fire only after somebody already decided to look - which is
# the failure they exist to prevent. The depth stayed in the references; what landed here
# is the trigger.
#
# Raised again from 600/42k for two rules that fire on ordinary implementation work rather
# than on a route: the check written before the code (test-driven.md) and the ladder
# climbed before writing any code (craft.md#write-less-the-ladder). Both change what the
# agent does on an L1 edit, which is exactly the work that never loads a reference - so a
# reference-only version would apply only to the tasks that least need it.
SKILL_MAX_LINES = 620
SKILL_MAX_CHARS = 44_000

# `eniac-compact.md` is the one deliberate restatement in the package, which makes it the
# one file that drifts. Every H2 in SKILL.md maps to the compact section carrying it, or to
# None when it is intentionally absent. Adding a section to SKILL.md therefore fails this
# check until someone decides whether the standalone version needs it too.
COMPACT_COVERAGE: dict[str, str | None] = {
    "Precedence": "Precedence",
    "First Move": "First move, on every task",
    "The Ego Loop": "The loop",
    "Investment Levels": "Investment levels",
    "Magnitude": "Size",
    "Triage \u2014 Automatic Prioritization": "Triage \u2014 when more than one thing wants doing",
    "Routes": "Routes",
    "Reality Testing": "Reality testing",
    "Runtime Portability": "Runtime portability",
    "Authority And Safety": "Authority and safety",
    "Self-Awareness": "Self-awareness",
    "Token Economy": "Token discipline",
    "Language": "Communication",
    "Learning": "Learning",
    "Communication": "Communication",
    "References": None,
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


def check_ownership() -> None:
    """Every reference declares what it owns and what it hands off.

    The package tells its readers to keep one owner per fact (references/documentation.md).
    A set of 25+ files that does not do the same to itself accumulates the exact failure it
    warns about: two files half-covering `secrets`, three half-covering `delegation`, and a
    reader who cannot tell which is authoritative. These blocks make the boundary explicit
    at the top of each file, where an agent deciding whether to keep reading will see it.
    """
    owns_by_topic: dict[str, str] = {}
    for p in sorted(REFS.glob("*.md")):
        head = "\n".join(read(p).split("\n")[:40])
        owns = re.search(r"^> \*\*Owns\*\* — (.+)$", head, re.M)
        defers = re.search(r"^> \*\*Defers\*\* — (.+)$", head, re.M)
        if not owns:
            fail(f"references/{p.name}: no `> **Owns** —` line, so nothing says what this "
                 f"file is authoritative for")
        if not defers:
            fail(f"references/{p.name}: no `> **Defers** —` line; a reference with no "
                 f"declared hand-offs is one that will duplicate a neighbour")
            continue

        for target in re.findall(r"→ `([a-zA-Z][a-zA-Z\-]*\.md)(?:#[a-z0-9\-]+)?`", defers.group(1)):
            if target == p.name:
                fail(f"references/{p.name}: defers to itself")
            elif target != "SKILL.md" and not (REFS / target).exists():
                fail(f"references/{p.name}: defers to `{target}`, which does not exist")

        if owns:
            for topic in owns.group(1).rstrip(".").split(";"):
                key = re.sub(r"[^a-z ]", "", topic.strip().lower()).strip()
                if len(key) < 12:
                    continue
                if key in owns_by_topic and owns_by_topic[key] != p.name:
                    fail(f"references/{p.name} and references/{owns_by_topic[key]} both "
                         f"claim to own \"{topic.strip()}\" - one of them must defer")
                owns_by_topic[key] = p.name


def check_counts() -> None:
    """A count in prose that introduces a list, checked against the list.

    Found by a sweep: SKILL.md said "Four conditions" over a five-row table, and the
    reference map said "Twenty-six files" over twenty-seven. One generator - a number
    written in prose that nothing recomputes when somebody adds a row - so this closes
    the class rather than the two instances. Deliberately narrow: it fires only on a
    lead-in ending in a colon, which on the current corpus is a hundred percent precise.
    A looser version flagged thirteen places and was right about one, and a check that
    cries wolf gets switched off.
    """
    words = {"two": 2, "three": 3, "four": 4, "five": 5, "six": 6,
             "seven": 7, "eight": 8, "nine": 9, "ten": 10}
    noun = (r"(?:things?|questions?|conditions?|reasons?|sources?|relationships?|rows?|"
            r"stops?|dials?|modes?|steps?|signals?|properties|fields?|columns?|answers?|"
            r"checks?|failures?|modalities|generators?|levels?|groups?|sections?|items?|"
            r"parts?|cases?|kinds?|ways?|moves?|rules?)")
    pat = re.compile(r"\b(" + "|".join(words) + r")\s+" + noun + r"\b", re.I)
    skip = ("|", "> ", "#", "- ", "* ")

    for path in [SKILL] + sorted(REFS.glob("*.md")):
        lines = read(path).split("\n")
        rel = path.relative_to(ROOT).as_posix()
        i = 0
        while i < len(lines):
            if (not lines[i].strip() or lines[i].lstrip().startswith(skip)
                    or re.match(r"^\d+\.", lines[i])):
                i += 1
                continue
            start, para = i, []
            while (i < len(lines) and lines[i].strip()
                   and not lines[i].lstrip().startswith(("|", "- ", "* "))
                   and not re.match(r"^\d+\.", lines[i])):
                para.append(lines[i].strip())
                i += 1
            text = " ".join(para)
            if not text.endswith(":"):
                continue
            m = pat.search(text)
            if not m:
                continue
            want, j, got = words[m.group(1).lower()], i, 0
            while j < len(lines) and not lines[j].strip():
                j += 1
            if j < len(lines) and lines[j].strip().startswith("|"):
                k = j + 2
                while k < len(lines) and lines[k].strip().startswith("|"):
                    got += 1
                    k += 1
            else:
                k = j
                while k < len(lines) and lines[k].strip():
                    flush = len(lines[k]) == len(lines[k].lstrip())
                    if flush and (lines[k].startswith(("- ", "* "))
                                  or re.match(r"^\d+\.\s", lines[k])):
                        got += 1
                    elif flush and got:
                        break
                    k += 1
            if got and got != want:
                fail(f"{rel}:{start + 1}: says {m.group(0)!r} and the list below it has "
                     f"{got} - somebody added or removed one without rereading the "
                     f"sentence above")


def check_reference_map() -> None:
    """Every reference sits in exactly one group of SKILL.md's map, so none is floating."""
    section = read(SKILL).split("## References", 1)
    if len(section) < 2:
        fail("SKILL.md: no `## References` section")
        return
    body = section[1]
    intro = body.split("\n\n")[1] if "\n\n" in body else body
    if re.search(r"(?i)\b(twenty|thirty|forty|\d\d)[- ]?\w*\s+(files|references)", intro):
        fail("SKILL.md: the reference map states a count in prose. Nothing keeps that "
             "number true when a file is added, and this package's own rule is that "
             "the filesystem owns it - drop the number")
    for p in sorted(REFS.glob("*.md")):
        hits = body.count(f"`references/{p.name}`")
        if hits == 0:
            fail(f"SKILL.md: `{p.name}` is not placed in the reference map")
        elif hits > 1:
            fail(f"SKILL.md: `{p.name}` appears {hits} times in the map - it belongs to "
                 f"exactly one group, or the grouping is not telling the reader anything")


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


def check_loaded_marker() -> None:
    """The marker must exist everywhere, and must never carry a version number.

    It exists because installing an instruction file fails silently on almost every
    runtime — a wrong path or an unrecognized key produces no error, the file is simply
    never read — so asking the agent what it follows is the only cheap cross-runtime way
    to tell.

    The skill folder deliberately states no version anywhere. A vendored copy should
    produce no diff when a release happens, the version belongs to CHANGELOG.md and the
    git tag that carries it, and a literal repeated across fourteen generated files is the
    duplication `references/documentation.md` tells everyone else to avoid. So this check
    runs in both directions: the marker is present, and it is bare.
    """
    for path in (SKILL,
                 ADAPTERS / "_source" / "core.md",
                 ADAPTERS / "eniac-compact.md"):
        if not path.exists():
            continue
        rel = path.relative_to(ROOT)
        if not re.search(r"`eniac`", read(path)):
            fail(f"{rel}: no bare `eniac` loaded-marker; an install that fails silently "
                 f"would be undetectable here")

    for path in [SKILL, *sorted(REFS.glob("*.md")), *sorted(ADAPTERS.rglob("*.md"))]:
        rel = path.relative_to(ROOT)
        text = read(path)
        if re.search(r"^\s*version:\s*[\"']?\d", text, re.M):
            fail(f"{rel}: declares a version. The skill folder carries none - version "
                 f"lives in CHANGELOG.md and the git tag")
        for m in re.findall(r"`eniac[ @v]+([0-9][^`]*)`", text):
            fail(f"{rel}: loaded-marker pins version {m!r}. Keep it bare so a release "
                 f"produces no diff inside the skill")


def check_budget() -> None:
    """The control plane is paid for on every task, so its size is enforced, not hoped."""
    text = read(SKILL)
    lines, chars = len(text.split("\n")), len(text)
    if lines > SKILL_MAX_LINES:
        fail(f"SKILL.md: {lines} lines exceeds the {SKILL_MAX_LINES}-line budget - "
             f"remove something before adding, or raise the budget deliberately")
    if chars > SKILL_MAX_CHARS:
        fail(f"SKILL.md: {chars} chars exceeds the {SKILL_MAX_CHARS}-char budget")


def check_compact_coverage() -> None:
    """Every section of the control plane is either in the standalone file or listed as absent."""
    compact = ADAPTERS / "eniac-compact.md"
    if not compact.exists():
        return
    skill_h2 = [m[3:].strip() for m in read(SKILL).split("\n") if m.startswith("## ")]
    compact_h2 = {m[3:].strip() for m in read(compact).split("\n") if m.startswith("## ")}

    for h in skill_h2:
        if h not in COMPACT_COVERAGE:
            fail(f"SKILL.md: section `{h}` is not in COMPACT_COVERAGE - decide whether "
                 f"adapters/eniac-compact.md needs it, then record the decision there")
        elif COMPACT_COVERAGE[h] and COMPACT_COVERAGE[h] not in compact_h2:
            fail(f"adapters/eniac-compact.md: no section `{COMPACT_COVERAGE[h]}` to carry "
                 f"SKILL.md's `{h}`")
    for h in COMPACT_COVERAGE:
        if h not in skill_h2:
            fail(f"check_skill.py: COMPACT_COVERAGE lists `{h}`, which SKILL.md no longer has")


def check_evals() -> None:
    """A skill verified only structurally is a skill whose central claim is untested."""
    import json

    evals = ROOT / "evals"
    for name in ("cases.json", "trigger.json", "README.md"):
        if not (evals / name).exists():
            fail(f"evals/{name}: missing")
    cases = evals / "cases.json"
    if cases.exists():
        try:
            data = json.loads(read(cases))
        except json.JSONDecodeError as exc:
            fail(f"evals/cases.json: not valid JSON ({exc})")
            return
        if len(data.get("cases", [])) < 5:
            fail("evals/cases.json: fewer than five behavioural cases is not a suite")
        changelog = ROOT / "CHANGELOG.md"
        if changelog.exists():
            latest = re.search(r"^## \[([^\]]+)\]", read(changelog), re.M)
            if latest and data.get("version") != latest.group(1):
                fail(f"evals/cases.json: version {data.get('version')!r} does not match "
                     f"the newest CHANGELOG entry {latest.group(1)!r} - the suite is "
                     f"describing a different release")


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
    check_budget()
    check_counts()
    check_compact_coverage()
    check_evals()
    check_ownership()
    check_reference_map()
    check_loaded_marker()

    if problems:
        for p in problems:
            print(p)
        print(f"\n{len(problems)} problem(s).")
        return 1
    refs = len(list(REFS.glob("*.md")))
    skill_lines = len(read(SKILL).split("\n"))
    print(f"ok - SKILL.md ({skill_lines}/{SKILL_MAX_LINES} lines) + {refs} references; "
          f"links, registration, ownership, the map, adapters, compact coverage, and evals "
          f"all agree.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
