#!/usr/bin/env python3
"""Install this skill into whatever the agent runtime actually reads.

Two things can be installed and they are one job: the **skill folder**, for runtimes with
a skills directory, and a generated **adapter file**, for runtimes that read standing
instructions instead. Both fail the same way, which is why they live in one script: a
wrong destination produces **no error on any runtime** - the file is simply never read and
the agent behaves exactly as though nothing were installed. So every destination is stated
once, here, and never retyped.

    python scripts/install.py                       # skill -> every runtime detected here
    python scripts/install.py --list                # destinations, and what is installed
    python scripts/install.py --runtime claude      # one runtime, user-wide
    python scripts/install.py --project ../my-app   # into that repository, checked in
    python scripts/install.py --runtime cursor --project ../my-app     # an adapter
    python scripts/install.py --runtime kiro        # adapter, user-wide where
                                                    # the runtime documents one
    python scripts/install.py --into ~/.config/some-agent/skills
    python scripts/install.py --dry-run             # print the plan, touch nothing
    python scripts/install.py --doctor              # is it working, and what is wrong
    python scripts/install.py --uninstall

Three things are checked that nothing errors on by itself, because this script's whole
premise - a wrong destination produces no error on any runtime - applies equally to its
own input and its own writes. The **source** has to be a complete skill before anything
is copied, so a truncated download cannot install. What **landed** is re-read and hashed
against the source, because a full disk, a sync client or an antivirus tool each leave a
file that exists and is wrong. And each install records what it wrote, so a later run can
tell a file somebody **edited** from one that is merely **out of date** - opposite
treatments, and guessing means discarding somebody's work silently.

It also runs with no clone at all. Downloaded on its own it has no `skills/Eniac` beside
it, so it fetches the repository archive over HTTPS and installs from that:

    curl -fsSL https://raw.githubusercontent.com/ParamissionLab/Eniac/main/scripts/install.py | python3 -
    irm https://raw.githubusercontent.com/ParamissionLab/Eniac/main/scripts/install.py | python -

`--ref` pins what it downloads to a tag or a commit, and is the honest default for
anything you rely on: `main` is whatever was pushed a minute ago, and an install that
silently follows a moving branch is a dependency that upgrades itself with no review.
Nothing from the download is executed - files are copied, and only under the skill folder.

Standard library only, no arguments required, runs from anywhere.
"""

from __future__ import annotations

import argparse
import filecmp
import hashlib
import io
import json
import os
import re
import shutil
import sys
import tarfile
import tempfile
import time
import urllib.error
import urllib.request
from pathlib import Path

# `__file__` is `<stdin>` when this file is piped into an interpreter, which is exactly
# the no-clone case - so a local checkout is something to test for rather than assume.
_here = Path(__file__).resolve() if __file__ not in ("<stdin>", "", None) else None
ROOT: Path | None = _here.parent.parent if _here else None

DEFAULT_REPO = "ParamissionLab/Eniac"
DEFAULT_REF = "main"

# Runtimes that load a skill folder. `home` is the runtime's configuration directory,
# resolved against the user's home directory for a user-wide install and against a
# repository root for a project one; `folder` is the name the skill must keep, because
# runtimes match the directory rather than anything inside it.
SKILL_RUNTIMES: dict[str, dict[str, str]] = {
    "claude": {"label": "Claude Code", "home": ".claude", "folder": "Eniac"},
    "codex": {"label": "Codex", "home": ".codex", "folder": "Eniac"},
    "agents": {"label": "runtimes on the shared .agents convention",
               "home": ".agents", "folder": "eniac"},
}

# Runtimes that read a standing instruction file: adapter under `skills/Eniac/adapters/`
# -> where that runtime reads it, relative to the repository receiving it. Generated from
# one source (scripts/build_adapters.py), so the rules cannot drift between runtimes.
#
# `user` is the same runtime's user-wide path, present only where that runtime documents
# one. Most do not: their rules file is a project artifact by design, checked in so a team
# shares it, and inventing a home-directory path for those would install a file nothing
# reads. `home` is the directory whose existence suggests the runtime is on this machine -
# a hint for what to offer, never a reason to write anything.
ADAPTER_RUNTIMES: dict[str, dict[str, str]] = {
    "agents-md": {"label": "AGENTS.md convention (Codex, Gemini CLI, Windsurf, Jules, Amp)",
                  "src": "agents-md/AGENTS.example.md", "dest": "AGENTS.md",
                  # Codex reads ~/.codex/AGENTS.md as personal defaults for every repo.
                  "user": ".codex/AGENTS.md", "home": ".codex"},
    "cursor": {"label": "Cursor", "src": "cursor/eniac.mdc",
               "dest": ".cursor/rules/eniac.mdc", "home": ".cursor"},
    "copilot": {"label": "GitHub Copilot", "src": "copilot/copilot-instructions.md",
                "dest": ".github/copilot-instructions.md"},
    "windsurf": {"label": "Windsurf", "src": "windsurf/eniac.md",
                 "dest": ".windsurf/rules/eniac.md", "home": ".windsurf"},
    "cline": {"label": "Cline, Roo Code", "src": "cline/.clinerules", "dest": ".clinerules"},
    "zed": {"label": "Zed", "src": "zed/rules.md", "dest": ".rules"},
    "gemini": {"label": "Gemini CLI, Gemini Code Assist", "src": "gemini/GEMINI.md",
               "dest": "GEMINI.md", "user": ".gemini/GEMINI.md", "home": ".gemini"},
    "continue": {"label": "Continue", "src": "continue/eniac.md",
                 "dest": ".continue/rules/eniac.md", "home": ".continue"},
    "aider": {"label": "Aider (then: aider --read CONVENTIONS.md)",
              "src": "aider/CONVENTIONS.md", "dest": "CONVENTIONS.md"},
    "junie": {"label": "JetBrains Junie", "src": "junie/guidelines.md",
              "dest": ".junie/guidelines.md"},
    "kiro": {"label": "Kiro", "src": "kiro/eniac.md",
             "dest": ".kiro/steering/eniac.md", "user": ".kiro/steering/eniac.md",
             "home": ".kiro"},
    "generic": {"label": "any single instruction field (API, custom assistant)",
                "src": "generic/system-prompt.md", "dest": "eniac-system-prompt.md"},
}

# The one question that works identically on every runtime, and the only cheap way to
# tell an install that took from one that failed silently. INSTALL.md explains why.
QUESTION = "What operating skill or rules are you currently following?"


# --------------------------------------------------------------------- presentation
#
# Colour carries meaning here rather than decoration: green is something changed, yellow
# is something removed or unconfirmed, red is a refusal, dim is context. Which means it
# has to degrade rather than corrupt - a script reading this output, a log file, a
# terminal that cannot encode `✓`, and a console with no escape-sequence support all get
# the same report in plain ASCII. Every fallback below is a failure this repository has
# actually seen, including an em dash arriving as `?` in a Windows console earlier today.

ANSI = {"bold": "1", "dim": "2", "red": "31", "green": "32", "yellow": "33", "cyan": "36"}
FANCY = {"ok": "✓", "same": "·", "add": "+", "gone": "−", "warn": "!", "no": "✗",
         "to": "→"}
PLAIN = {"ok": "+", "same": ".", "add": "+", "gone": "-", "warn": "!", "no": "x",
         "to": "->"}


def _enable_windows_vt() -> bool:
    """Windows 10+ consoles understand escape sequences, once asked."""
    try:
        import ctypes

        kernel32 = ctypes.windll.kernel32
        handle = kernel32.GetStdHandle(-11)
        mode = ctypes.c_uint32()
        if not kernel32.GetConsoleMode(handle, ctypes.byref(mode)):
            return False
        return bool(kernel32.SetConsoleMode(handle, mode.value | 0x0004))
    except Exception:
        return False


def _supports_color(stream) -> bool:
    if os.environ.get("NO_COLOR"):
        return False
    if os.environ.get("FORCE_COLOR"):
        return True
    if not hasattr(stream, "isatty") or not stream.isatty():
        return False
    if os.name == "nt":
        return _enable_windows_vt()
    return os.environ.get("TERM", "") not in ("", "dumb")


def _supports_glyphs(stream) -> bool:
    try:
        "".join(FANCY.values()).encode(getattr(stream, "encoding", None) or "ascii")
        return True
    except (UnicodeEncodeError, LookupError):
        return False


COLOR = _supports_color(sys.stdout)
COLOR_ERR = _supports_color(sys.stderr)
MARKS = FANCY if _supports_glyphs(sys.stdout) else PLAIN


def paint(text: str, *styles: str, err: bool = False) -> str:
    if not styles or not (COLOR_ERR if err else COLOR):
        return text
    return f"\033[{';'.join(ANSI[s] for s in styles)}m{text}\033[0m"


def under_home(path: Path) -> bool:
    """`Path.is_relative_to` arrived in 3.9, and the wrappers promise 3.8."""
    try:
        path.relative_to(Path.home())
        return True
    except ValueError:
        return False


def show_path(path: Path) -> str:
    """Home-relative where possible - the difference between a readable line and a wrap."""
    try:
        return "~/" + str(path.relative_to(Path.home())).replace("\\", "/")
    except ValueError:
        return str(path)


def title(text: str) -> None:
    print(f"\n  {paint(text, 'bold')}")


def item(mark: str, text: str, *styles: str, trail: str = "") -> None:
    """One status line, with the destination trailing it - or under it when it is long.

    A deep path wrapped mid-word turns a report into a wall, and paths are exactly the
    part a reader scans for.
    """
    print(f"    {paint(MARKS[mark], *styles)} {text}"
          + ("" if not trail or len(text) + len(trail) > 74
             else f"  {paint(MARKS['to'] + ' ' + trail, 'dim')}"))
    if trail and len(text) + len(trail) > 74:
        print(f"      {paint(MARKS['to'] + ' ' + trail, 'dim')}")


def detail(text: str) -> None:
    print(f"      {paint(text, 'dim')}")


def refuse(headline: str, *lines: str) -> int:
    """A refusal is the one message that must survive a redirected stdout, so: stderr.

    Flushing first is not decoration: stdout is block-buffered once it is not a terminal,
    so without this the refusal overtakes the heading it belongs under and the report
    reads as though a different runtime failed.
    """
    sys.stdout.flush()
    print(f"    {paint(MARKS['no'], 'red', err=True)} {paint(headline, 'red', err=True)}",
          file=sys.stderr)
    for line in lines:
        print(f"      {line}", file=sys.stderr)
    return 1


# --------------------------------------------------------------------------- source

def fetch_repo(repo: str, ref: str, keep: list) -> Path:
    """Download and unpack the repository archive; return the extracted root.

    `keep` holds the TemporaryDirectory alive for the caller's lifetime - dropping it
    deletes the tree mid-copy, which is the kind of bug that only shows up under a
    slow disk.
    """
    url = f"https://codeload.github.com/{repo}/tar.gz/{ref}"
    # The default ref is noise - it says nothing the reader did not already assume. A
    # pinned one is the opposite: it is the whole reason someone passed --ref, so it shows.
    what = repo if ref == DEFAULT_REF else f"{repo}@{ref}"
    print(f"  {paint('downloading', 'cyan')} {paint(what, 'bold')}")
    try:
        with urllib.request.urlopen(url, timeout=60) as response:
            payload = response.read()
    except urllib.error.HTTPError as exc:
        raise SystemExit(f"{url}\n  returned HTTP {exc.code}. Check the repository name "
                         f"and that --ref names a branch, tag, or commit that exists.")
    except (urllib.error.URLError, OSError) as exc:
        raise SystemExit(f"could not download {url}: {exc}")

    tmp = tempfile.TemporaryDirectory(prefix="eniac-install-")
    keep.append(tmp)
    out = Path(tmp.name)

    with tarfile.open(fileobj=io.BytesIO(payload), mode="r:gz") as tar:
        # An archive member is data, not an instruction about where to write. A path
        # escaping the extraction directory, or anything that is not a plain file or
        # directory, is dropped rather than trusted.
        members = []
        for member in tar.getmembers():
            if member.islnk() or member.issym() or not (member.isfile() or member.isdir()):
                continue
            target = (out / member.name).resolve()
            if out.resolve() not in target.parents and target != out.resolve():
                continue
            members.append(member)
        # `filter="data"` is the interpreter's own version of the check above, on 3.12+.
        # Both run: the filter is the one that stays correct as tar grows new tricks.
        extra = {"filter": "data"} if hasattr(tarfile, "data_filter") else {}
        tar.extractall(out, members=members, **extra)

    roots = [p for p in out.iterdir() if p.is_dir()]
    if len(roots) != 1:
        raise SystemExit(f"unexpected archive layout from {url}")
    return roots[0]


def resolve_repo_root(args, keep: list) -> Path:
    """Where the files come from: this clone, or a download when there is no clone."""
    if args.source:
        root = Path(args.source).expanduser().resolve()
        if not (root / "skills" / "Eniac" / "SKILL.md").is_file():
            raise SystemExit(f"{root} does not look like a checkout of this repository")
        return root
    local = ROOT if ROOT and (ROOT / "skills" / "Eniac" / "SKILL.md").is_file() else None
    if local and not args.from_github and args.ref == DEFAULT_REF and args.repo == DEFAULT_REPO:
        return local
    return fetch_repo(args.repo, args.ref, keep)


def skill_source(repo_root: Path) -> Path:
    return repo_root / "skills" / "Eniac"


def source_files(source: Path) -> list[Path]:
    if not source.is_dir():
        return []
    return sorted(
        p.relative_to(source)
        for p in source.rglob("*")
        if p.is_file() and "__pycache__" not in p.parts
    )


# ---------------------------------------------------------------------- destinations

def skills_root(key: str, project: Path | None) -> Path:
    base = project if project is not None else Path.home()
    return base / SKILL_RUNTIMES[key]["home"] / "skills"


def skill_destination(key: str, project: Path | None) -> Path:
    return skills_root(key, project) / SKILL_RUNTIMES[key]["folder"]


def detected(key: str, project: Path | None) -> bool:
    """The runtime's configuration directory exists, so this machine (or repo) uses it.

    Deliberately the configuration directory and not the skills directory: a runtime
    that has never had a skill installed has no `skills/` yet, and refusing to install
    there would be refusing the ordinary first install.
    """
    base = project if project is not None else Path.home()
    return (base / SKILL_RUNTIMES[key]["home"]).is_dir()


def installed_files(dest: Path) -> list[Path]:
    return sorted(
        p.relative_to(dest)
        for p in dest.rglob("*")
        if p.is_file() and "__pycache__" not in p.parts
    )


def looks_like_eniac(dest: Path) -> bool:
    """Is this directory a copy of this skill, or somebody else's folder of that name?

    Guessing wrong here deletes someone's work, so the test is a positive identification
    rather than the absence of a signal: the front-matter name the runtime itself keys on.
    """
    skill = dest / "SKILL.md"
    if not skill.is_file():
        return False
    return "name: eniac" in skill.read_text(encoding="utf-8", errors="replace")[:400]


def back_up(dest: Path, dry_run: bool) -> Path:
    """Copy the current install aside, *outside* the skills directory.

    Not `dest.with_name(dest.name + ".bak")`: a runtime indexes every folder under its
    skills directory, so a backup left beside the install loads as a second skill with
    the same description and the agent gets two copies of one mind - the duplication this
    package spends a reference warning other people about. Found by doing it.
    """
    stamp = time.strftime("%Y%m%d-%H%M%S")
    target = dest.parent.parent / "eniac-backups" / f"{dest.name}-{stamp}"
    if not dry_run:
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(dest, target)
    item("ok", "backed up the existing install", "cyan", trail=show_path(target))
    return target


# ------------------------------------------------------------------- the skill folder

def install_skill(source: Path, dest: Path, *, force: bool, prune: bool, dry_run: bool,
                  backup: bool) -> int:
    """Copy the skill folder into `dest`. Returns 0 on success, 1 on a refusal."""
    files = source_files(source)
    if not files:
        return refuse(f"nothing to install: {show_path(source)} is missing or empty")

    if dest.exists():
        if not dest.is_dir():
            return refuse(f"{show_path(dest)} exists and is not a directory",
                          "Nothing was touched.")
        if not looks_like_eniac(dest) and not force:
            return refuse(f"{show_path(dest)} is not an install of this skill",
                          "Nothing was overwritten. Move it aside, or re-run with",
                          "--force if it is a stale copy.")
        # Somebody's edit is work, not drift. This package tells everyone else never to
        # discard a user's changes as incidental cleanup, so it does not get to do it
        # here either - and without the manifest it could not even tell, which is most of
        # why the manifest exists. Both ways forward are deliberate acts.
        edited = local_edits(dest)
        if edited and not (force or backup):
            return refuse(
                f"{len(edited)} file(s) in {show_path(dest)} changed after they were "
                f"installed",
                *(f"    {p}" for p in edited[:6]),
                *(["    ..."] if len(edited) > 6 else []),
                "Installing over them would throw that work away silently. Keep it with",
                "--backup, which copies the folder aside first, or discard it on purpose",
                "with --force.")
        if edited and force and not backup:
            item("warn", f"discarding {len(edited)} local edit(s) as asked", "yellow")
            for p in edited[:6]:
                detail(p)
        if backup:
            back_up(dest, dry_run)

    written: list[Path] = []
    unchanged = 0
    for rel in files:
        src, target = source / rel, dest / rel
        if target.is_file() and filecmp.cmp(src, target, shallow=False):
            unchanged += 1
            continue
        written.append(rel)
        if not dry_run:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(src, target)

    # A reference dropped in a later version keeps loading from an old install until
    # something removes it, and it will contradict the version that replaced it. Pruning
    # is scoped to files this skill ships, so anything else in the folder is left alone.
    stale: list[Path] = []
    if prune and dest.is_dir():
        # The manifest is this installer's own bookkeeping rather than a file the skill
        # ships, so pruning must not treat it as stale and delete the record it needs.
        known = set(files) | {Path(MANIFEST)}
        stale = [rel for rel in installed_files(dest) if rel not in known]
        for rel in stale:
            if not dry_run:
                (dest / rel).unlink()
        if not dry_run:
            for d in sorted((p for p in dest.rglob("*") if p.is_dir()),
                            key=lambda p: len(p.parts), reverse=True):
                if not any(d.iterdir()):
                    d.rmdir()

    if not dry_run and written:
        bad = verify_written(source, dest, written)
        if bad:
            return refuse(
                f"{len(bad)} file(s) did not land correctly in {show_path(dest)}",
                *bad[:5],
                "The install is incomplete, and an incomplete skill loads and then",
                "under-delivers rather than failing visibly. Check free space and any",
                "sync or antivirus tool watching that folder, then re-run.")
    if not dry_run:
        write_manifest(source, dest, files)

    if not written and not stale:
        item("same", f"already up to date, {unchanged} files", "dim",
             trail=show_path(dest))
        return 0

    if written:
        verb = "would install" if dry_run else "installed"
        count = f"{verb} {len(written)} file{'s' if len(written) != 1 else ''}"
        if unchanged:
            count += paint(f"  {MARKS['same']} {unchanged} unchanged", "dim")
        item("ok", count, "green", trail=show_path(dest))
    else:
        item("same", f"{unchanged} files already current", "dim", trail=show_path(dest))
    for rel in stale:
        verb = "would remove stale" if dry_run else "removed stale"
        item("gone", f"{verb} {rel.as_posix()}", "yellow")
    return 0


def uninstall_skill(dest: Path, *, force: bool, dry_run: bool) -> int:
    if not dest.exists():
        item("same", "not installed", "dim", trail=show_path(dest))
        return 0
    if not looks_like_eniac(dest) and not force:
        return refuse(f"{show_path(dest)} is not an install of this skill",
                      "Nothing was removed. Re-run with --force only if you are sure.")
    if not dry_run:
        shutil.rmtree(dest)
    item("gone", "would remove" if dry_run else "removed", "yellow",
         trail=show_path(dest))
    return 0


# ------------------------------------------------------------------- adapter files

def adapter_destination(key: str, project: Path | None) -> Path | None:
    """Where this adapter goes: inside a repository, or the runtime's user-wide path.

    Returns None when asked for a user-wide install the runtime does not document one
    for - which is most of them, because a rules file that a team shares is a project
    artifact on purpose. Guessing a home-directory path there installs a file nothing
    ever reads, and nothing errors to say so.
    """
    meta = ADAPTER_RUNTIMES[key]
    if project is not None:
        return project / meta["dest"]
    return Path.home() / meta["user"] if meta.get("user") else None


def installed_elsewhere(project: Path | None) -> list[str]:
    """Adapter runtimes whose config directory exists here - a hint, not an install."""
    if project is not None:
        return []
    return [key for key, meta in ADAPTER_RUNTIMES.items()
            if meta.get("home") and (Path.home() / meta["home"]).is_dir()]


def install_adapter(repo_root: Path, key: str, dest: Path, *, force: bool,
                    dry_run: bool) -> int:
    meta = ADAPTER_RUNTIMES[key]
    src = repo_root / "skills" / "Eniac" / "adapters" / meta["src"]

    if not src.is_file():
        return refuse(f"missing adapter {meta['src']}",
                      "Run scripts/build_adapters.py to generate it.")

    if dest.exists():
        if dest.read_text(encoding="utf-8", errors="replace") == src.read_text(
                encoding="utf-8", errors="replace"):
            item("same", "already installed and identical", "dim",
                 trail=show_path(dest))
            return 0
        if not force:
            # These are files people edit, and a project's own rules outrank this skill
            # (SKILL.md#precedence), so merging is a decision rather than a copy.
            return refuse(f"{show_path(dest)} already exists and differs",
                          "Nothing was overwritten. Merge by hand, keeping one file",
                          "authoritative, or re-run with --force if it is a stale copy.")

    if not dry_run:
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dest)
    item("ok", f"{'would install' if dry_run else 'installed'} {meta['src']}", "green",
         trail=show_path(dest))
    # The rules are inline in every adapter; the pointer to the full text is depth on
    # demand. Worth saying only where it resolves - inside a repository that vendors the
    # skill - because a user-wide copy has no repository around it to point into.
    if meta.get("user") and under_home(dest):
        detail("the rules are inline; the pointer to the full text needs a checkout")
    else:
        detail("adjust the path inside it to wherever skills/Eniac lives in that repository")
    return 0


def uninstall_adapter(repo_root: Path, key: str, dest: Path, *, force: bool,
                      dry_run: bool) -> int:
    meta = ADAPTER_RUNTIMES[key]
    src = repo_root / "skills" / "Eniac" / "adapters" / meta["src"]
    if not dest.exists():
        item("same", "not installed", "dim", trail=show_path(dest))
        return 0
    same = src.is_file() and dest.read_text(encoding="utf-8", errors="replace") == \
        src.read_text(encoding="utf-8", errors="replace")
    if not same and not force:
        return refuse(f"{show_path(dest)} differs from the adapter",
                      "It has been edited, or it is somebody else's file. Nothing was",
                      "removed. Re-run with --force if you are sure.")
    if not dry_run:
        dest.unlink()
    item("gone", "would remove" if dry_run else "removed", "yellow",
         trail=show_path(dest))
    return 0


# ------------------------------------------------------------------------- listing

def adapter_confirmation() -> dict[str, str]:
    """Per-adapter: has anyone confirmed this destination actually loads?

    The generator owns that fact (`verified` in its TARGETS), so it is read rather than
    restated here. It is the most useful column in the table: an unconfirmed path is the
    one that will fail silently. Absent when running from a download with no clone, which
    is why every row still says something rather than going blank.
    """
    if not ROOT or not (ROOT / "scripts" / "build_adapters.py").is_file():
        return {}
    sys.path.insert(0, str(ROOT / "scripts"))
    try:
        import build_adapters
    except Exception:
        return {}
    by_out = {t["out"]: t.get("verified") for t in build_adapters.TARGETS}
    return {key: (by_out.get(meta["src"]) or "path not confirmed by an install")
            for key, meta in ADAPTER_RUNTIMES.items() if meta["src"] in by_out}


def table(rows: list[tuple[str, str, str, tuple[str, ...]]], headers: tuple[str, str, str]
          ) -> None:
    """Three columns sized to their contents.

    Fixed widths were the bug this replaces: a project path is as long as it happens to
    be, and a hard-coded 50 turns one long row into a wrapped mess for every other row.
    """
    widths = [max(len(h), *(len(row[i]) for row in rows)) for i, h in enumerate(headers)]
    header = "  ".join(h.ljust(w) for h, w in zip(headers, widths)).rstrip()
    print("    " + paint(header, "dim"))
    for key, dest, state, styles in rows:
        print(f"    {paint(key.ljust(widths[0]), 'bold')}  "
              f"{paint(dest.ljust(widths[1]), 'dim')}  {paint(state, *styles)}")


# ----------------------------------------------------------------------- integrity
#
# This script is organised around one fact: a wrong destination produces no error on any
# runtime. That fact applies in two more places nothing was checking - the source it
# copies *from*, and the bytes that actually land. Both fail the same silent way, and a
# half-installed skill is worse than an absent one, because it loads and then
# under-delivers on exactly the task that reached for the missing part.

MANIFEST = ".eniac-install.json"


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def verify_source(source: Path) -> list[str]:
    """Is this a coherent skill, or half of a download?

    A truncated archive, an interrupted extract, or a `--ref` pointing at a broken commit
    all produce a directory that copies without complaining. These checks are derived from
    the file itself rather than from a threshold somebody picked: the front matter the
    runtime keys on, and the references the control plane actually names.
    """
    problems: list[str] = []
    skill = source / "SKILL.md"
    if not skill.is_file():
        return [f"{show_path(source)} has no SKILL.md"]

    text = skill.read_text(encoding="utf-8", errors="replace")
    if not text.startswith("---\n") or text.find("\n---\n", 4) == -1:
        problems.append("SKILL.md front matter is missing or unterminated")
    if "name: eniac" not in text[:800]:
        problems.append("SKILL.md does not declare `name: eniac` in its front matter")

    named = sorted(set(re.findall(r"`references/([a-z][a-z0-9\-]*\.md)", text)))
    missing = [n for n in named if not (source / "references" / n).is_file()]
    if missing:
        shown = ", ".join(missing[:4]) + (", ..." if len(missing) > 4 else "")
        problems.append(f"SKILL.md names {len(missing)} reference file(s) that are not "
                        f"in this copy: {shown}")
    return problems


def verify_written(source: Path, dest: Path, files: list[Path]) -> list[str]:
    """Re-read what landed. The copy reported success; this asks the filesystem.

    `shutil.copyfile` raising is not the only way a write goes wrong. A full disk, a sync
    client rewriting the file underneath, an antivirus quarantine, or a permission quirk
    each leave a file that exists and is wrong, and counting bytes on the write side
    cannot see any of it.
    """
    bad: list[str] = []
    for rel in files:
        target = dest / rel
        if not target.is_file():
            bad.append(f"{rel.as_posix()} did not land")
        elif digest(source / rel) != digest(target):
            bad.append(f"{rel.as_posix()} differs from the source after copying")
    return bad


def write_manifest(source: Path, dest: Path, files: list[Path]) -> None:
    """Record what this install wrote, so a later run can tell an edit from an upgrade.

    Without it, a file differing from the current source is ambiguous - somebody changed
    it, or it is simply older - and those deserve opposite treatment: one is work to
    preserve, the other is a file to replace. Guessing means silently discarding
    somebody's edit, which this package tells everyone else never to do.
    """
    data = {
        "installed_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "files": {rel.as_posix(): digest(source / rel) for rel in files},
    }
    (dest / MANIFEST).write_text(json.dumps(data, indent=2, sort_keys=True) + "\n",
                                 encoding="utf-8")


def read_manifest(dest: Path) -> dict:
    path = dest / MANIFEST
    if not path.is_file():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def local_edits(dest: Path) -> list[str]:
    """Installed files whose bytes no longer match what the last install put there."""
    recorded = (read_manifest(dest).get("files") or {})
    return sorted(rel for rel, want in recorded.items()
                  if (dest / rel).is_file() and digest(dest / rel) != want)


def do_doctor(repo_root: Path | None, project: Path | None) -> int:
    """Judgement, where `--list` is inventory.

    The question people actually arrive with is "is it working?", and the package's own
    claim is that a failed install says nothing anywhere. Four states need separating
    because the fix differs for each: current, out of date, edited here, and loading
    twice. The last one is the quietest - two copies of this guidance both load, and
    neither reports the other.
    """
    source = skill_source(repo_root) if repo_root else None
    problems = 0

    title("Source")
    if source is None or not source.is_dir():
        item("warn", "no checkout beside this script, so nothing to compare against",
             "yellow")
        detail("run from a clone, or pass --source, for the currency and edit checks")
    else:
        bad = verify_source(source)
        if bad:
            problems += 1
            item("no", f"{show_path(source)} is not a complete skill", "red")
            for line in bad:
                detail(line)
        else:
            item("ok", "complete and self-consistent", "green", trail=show_path(source))

    title("Installs")
    live: list[str] = []
    for key in SKILL_RUNTIMES:
        dest = skill_destination(key, project)
        if not dest.is_dir():
            if detected(key, project):
                problems += 1
                item("warn", f"{key}: runtime is here, skill is not installed", "yellow")
                detail(f"install it: python scripts/install.py --runtime {key}")
            continue
        if not looks_like_eniac(dest):
            problems += 1
            item("no", f"{key}: {show_path(dest)} holds something else", "red")
            continue

        live.append(key)
        edited = local_edits(dest)
        if source is not None and source.is_dir():
            files = source_files(source)
            stale = [r.as_posix() for r in files
                     if not (dest / r).is_file()
                     or not filecmp.cmp(source / r, dest / r, shallow=False)]
            outdated = [p for p in stale if p not in edited]
        else:
            outdated = []

        if edited:
            problems += 1
            item("warn", f"{key}: {len(edited)} file(s) edited here since install",
                 "yellow", trail=show_path(dest))
            for p in edited[:5]:
                detail(p)
            detail("re-installing overwrites these - use --backup, or copy them aside")
        if outdated:
            problems += 1
            item("warn", f"{key}: {len(outdated)} file(s) out of date", "yellow",
                 trail=show_path(dest))
            detail(f"re-run: python scripts/install.py --runtime {key}")
        if not edited and not outdated:
            trail = show_path(dest)
            if not read_manifest(dest):
                item("ok", f"{key}: installed (no manifest, so no edit check)", "green",
                     trail=trail)
            else:
                item("ok", f"{key}: current", "green", trail=trail)

    # Two copies of the same guidance, each unaware of the other. The skill folder and an
    # adapter say the same things in different words, so an agent that reads both spends
    # the tokens twice and gets two slightly different phrasings of one rule.
    adapters_here = [k for k in ADAPTER_RUNTIMES
                     if (d := adapter_destination(k, project)) is not None and d.exists()]
    if live and adapters_here:
        title("Loading twice")
        item("warn", f"the skill folder is installed for {', '.join(live)} and an adapter "
                     f"file is present for {', '.join(adapters_here)}", "yellow")
        detail("an agent reading both gets this guidance twice, in two wordings")
        detail("keep whichever its runtime actually reads; --uninstall removes the other")
        problems += 1

    print()
    if problems:
        print(f"  {paint(MARKS['warn'] + ' ' + str(problems) + ' thing(s) to look at',
                         'yellow', 'bold')}")
    else:
        print(f"  {paint(MARKS['ok'] + ' nothing to fix here', 'green', 'bold')}")
    print(f"\n  {paint('Still ask the agent', 'cyan', 'bold')}  nothing above proves the "
          f"runtime reads it:")
    print(f"        {paint(QUESTION, 'bold')}")
    print()
    return 0


def do_list(project: Path | None) -> int:
    title("Skill folder" + paint("   runtimes with a skills directory", "dim"))
    rows = []
    for key in SKILL_RUNTIMES:
        dest = skill_destination(key, project)
        if dest.is_dir() and looks_like_eniac(dest):
            state, styles = "installed", ("green",)
        elif dest.is_dir():
            state, styles = "occupied by something else", ("yellow",)
        elif detected(key, project):
            state, styles = "runtime found, not installed", ()
        else:
            state, styles = "runtime not found", ("dim",)
        rows.append((key, show_path(dest), state, styles))
    scope = f"destination ({'project' if project else 'user-wide'})"
    table(rows, ("runtime", scope, "state"))

    title("Adapter file" + paint("   runtimes that read standing instructions", "dim"))
    confirmed = adapter_confirmation()
    rows = []
    for key, meta in ADAPTER_RUNTIMES.items():
        state = confirmed.get(key, "confirmation unknown without a checkout")
        styles: tuple[str, ...] = ("yellow",) if state.startswith("path not") else ()
        # Show the destination this invocation would actually use, so the table answers
        # "where does it go" rather than "where would it go in some other invocation".
        dest = adapter_destination(key, project)
        where = show_path(dest) if dest and project is None else meta["dest"]
        if dest is not None and dest.exists():
            state, styles = f"file present, {state}", ("green",)
        rows.append((key, where, state, styles))
    table(rows, ("runtime", "destination", "state"))
    print()
    detail("a destination shown as ~/... installs user-wide with no --project;")
    detail("the rest are project files, so name the repository with --project")
    detail("destinations come from each runtime's own docs, not from an install done here,")
    detail("and a wrong one fails silently. Confirm one and record it: set `verified`")
    detail("for that target in build_adapters.py.")
    return 0


# ---------------------------------------------------------------------------- main

def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__.split("\n")[0],
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("--runtime", action="append", metavar="NAME",
                    help=f"skill folder: {', '.join(SKILL_RUNTIMES)}, or all. "
                         f"Adapter file: {', '.join(ADAPTER_RUNTIMES)}. Repeatable. "
                         f"Default: every skill runtime detected here")
    ap.add_argument("--project", metavar="PATH",
                    help="the repository that receives this, instead of the user's home. "
                         "Required for adapters whose runtime documents no user-wide path")
    ap.add_argument("--into", metavar="PATH",
                    help="an explicit skills directory, for a runtime not in the table")
    ap.add_argument("--source", metavar="PATH",
                    help="install from this checkout instead of the one around this script")
    ap.add_argument("--repo", default=DEFAULT_REPO, metavar="OWNER/NAME",
                    help=f"download from this GitHub repository (default {DEFAULT_REPO})")
    ap.add_argument("--ref", default=DEFAULT_REF, metavar="REF",
                    help="branch, tag, or commit to download. Pin it for anything you "
                         "rely on")
    ap.add_argument("--from-github", action="store_true",
                    help="download even when there is a checkout around this script")
    ap.add_argument("--list", action="store_true",
                    help="show the destinations and what is already installed")
    ap.add_argument("--dry-run", action="store_true",
                    help="print the plan and change nothing")
    ap.add_argument("--force", action="store_true",
                    help="write over a destination that is not an install of this skill")
    ap.add_argument("--no-prune", action="store_true",
                    help="keep files an older version left behind")
    ap.add_argument("--backup", action="store_true",
                    help="copy an existing install to <runtime>/eniac-backups/ first")
    ap.add_argument("--doctor", action="store_true",
                    help="is it working? reports current / out of date / edited here / "
                         "loading twice, and what to do about each")
    ap.add_argument("--uninstall", action="store_true", help="remove what was installed")
    ap.add_argument("--no-color", action="store_true",
                    help="plain output (also honours NO_COLOR)")
    args = ap.parse_args()

    if args.no_color:
        global COLOR, COLOR_ERR
        COLOR = COLOR_ERR = False

    project = Path(args.project).expanduser().resolve() if args.project else None
    if project is not None and not project.is_dir():
        return refuse(f"not a directory: {project}")

    if args.list:
        return do_list(project)

    if args.doctor:
        root = None
        if args.source or args.from_github or ROOT is None:
            keep: list = []
            try:
                root = resolve_repo_root(args, keep)
            except SystemExit:
                raise
            except Exception:
                root = None
        else:
            root = ROOT
        return do_doctor(root, project)

    keys: list[str] = []
    for name in args.runtime or []:
        keys.extend(k.strip() for k in name.split(",") if k.strip())
    if "all" in keys:
        keys = list(SKILL_RUNTIMES)
    unknown = [k for k in keys if k not in SKILL_RUNTIMES and k not in ADAPTER_RUNTIMES]
    if unknown:
        return refuse(f"unknown runtime {unknown[0]!r}", "Run --list to see the names.")

    adapters = [k for k in keys if k in ADAPTER_RUNTIMES]
    homeless = [k for k in adapters if adapter_destination(k, project) is None]
    if homeless:
        return refuse(f"--project is required for {homeless[0]}",
                      "That runtime reads its rules from inside a repository and",
                      "documents no user-wide path, so name the repository it goes in.")

    skills = [k for k in keys if k in SKILL_RUNTIMES]
    if not keys and not args.into:
        skills = [k for k in SKILL_RUNTIMES if detected(k, project)]
        if not skills:
            where = f"in {show_path(project)}" if project else "on this machine"
            refuse(f"no known runtime found {where}",
                   "Name one explicitly with --runtime, or give a path with --into.")
            do_list(project)
            return 1

    keep: list = []
    repo_root = resolve_repo_root(args, keep)
    source = skill_source(repo_root)

    # Check the source before touching any destination. A partial download copies happily
    # and the result loads, which is the failure this whole script is built around -
    # applied here to its own input rather than only to where it writes.
    if not args.uninstall and (skills or args.into):
        bad = verify_source(source)
        if bad:
            return refuse(f"{show_path(source)} is not a complete copy of this skill",
                          *bad,
                          "Nothing was written. Re-download, or use --source to point at",
                          "a good checkout. --force deliberately does not override this:",
                          "a partial install loads and then under-delivers, which is",
                          "worse than no install at all.")

    failures = 0
    for key in skills:
        title(SKILL_RUNTIMES[key]["label"])
        dest = skill_destination(key, project)
        if args.uninstall:
            failures += uninstall_skill(dest, force=args.force, dry_run=args.dry_run)
        else:
            failures += install_skill(source, dest, force=args.force,
                                      prune=not args.no_prune, dry_run=args.dry_run,
                                      backup=args.backup)
    if args.into:
        dest = Path(args.into).expanduser().resolve() / "Eniac"
        title("Custom path")
        if args.uninstall:
            failures += uninstall_skill(dest, force=args.force, dry_run=args.dry_run)
        else:
            failures += install_skill(source, dest, force=args.force,
                                      prune=not args.no_prune, dry_run=args.dry_run,
                                      backup=args.backup)
    for key in adapters:
        title(ADAPTER_RUNTIMES[key]["label"])
        dest = adapter_destination(key, project)
        assert dest is not None  # `homeless` above rejected the ones with nowhere to go
        if args.uninstall:
            failures += uninstall_adapter(repo_root, key, dest, force=args.force,
                                          dry_run=args.dry_run)
        else:
            failures += install_adapter(repo_root, key, dest, force=args.force,
                                        dry_run=args.dry_run)

    if failures:
        print()
        return 1
    if args.dry_run:
        print(f"\n  {paint(MARKS['warn'] + ' dry run:', 'yellow')} "
              f"{paint('nothing above was written', 'dim')}")
    # A default run installs the skill folder and stops, which looks like "it missed my
    # other IDEs" when the truth is that those read a file inside a repository and the
    # installer will not write into one it was not pointed at. Saying so beats being
    # silently correct.
    if not args.uninstall and not adapters:
        others = [k for k in installed_elsewhere(project) if k not in skills]
        if others:
            print(f"\n  {paint('Also here', 'cyan', 'bold')}  these read a standing "
                  f"instruction file rather than a skill:")
            rows = []
            for key in others:
                dest = adapter_destination(key, None)
                command = f"--runtime {key}" if dest else f"--runtime {key} --project ."
                rows.append((key, command,
                             show_path(dest) if dest else ADAPTER_RUNTIMES[key]["dest"]))
            keyw = max(len(r[0]) for r in rows)
            cmdw = max(len(r[1]) for r in rows)
            for key, command, where in rows:
                print(f"        {paint(key.ljust(keyw), 'bold')}  "
                      f"{paint(command.ljust(cmdw), 'dim')}  {paint(where, 'dim')}")

    if not args.uninstall and not args.dry_run:
        print(f"\n  {paint('Next', 'cyan', 'bold')}  restart the agent, then ask it:")
        print(f"        {paint(QUESTION, 'bold')}")
        for line in ("A loaded skill names itself. A generic answer means the file is not",
                     "being read, and nothing will have errored to tell you - INSTALL.md"):
            print(f"        {paint(line, 'dim')}")
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
