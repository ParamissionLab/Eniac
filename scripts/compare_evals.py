#!/usr/bin/env python3
"""Run the eval suite twice — with the skill and without — and compare.

A single score measures the model, not the skill. The comparison is the whole point, and
until now getting one meant uninstalling by hand between runs, which nobody does twice.
This automates the awkward half.

    python scripts/compare_evals.py \\
        --agent-cmd 'claude -p {prompt}' \\
        --skill-path ~/.claude/skills/Eniac

It renames the installed skill directory aside, runs the suite as **baseline**, restores
it, runs again as **with-skill**, and writes a comparison. The restore is in a `finally`,
and the script refuses to start if the aside path already exists — an interrupted earlier
run must be cleaned up deliberately rather than silently overwritten.

`--skill-path` is required and never guessed. This mutates a directory outside the
repository, so it names the exact target and prints it before touching anything.

Standard library only. Read evals/README.md before trusting a number from this.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "evals" / "results"


def run_suite(agent_cmd: str, label: str, timeout: int) -> dict | None:
    cmd = [sys.executable, str(ROOT / "scripts" / "run_evals.py"),
           "--agent-cmd", agent_cmd, "--label", label, "--timeout", str(timeout)]
    proc = subprocess.run(cmd, cwd=ROOT)
    if proc.returncode == 2:          # the harness aborted at its own probe
        return None
    path = RESULTS / f"{label}.json"
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else None


def compare(base: dict, skill: dict) -> str:
    def index(d):
        return {r["id"]: r for r in d["results"]}

    b, s = index(base), index(skill)
    ids = [r["id"] for r in skill["results"]]

    rows, gained, lost, both, neither = [], [], [], [], []
    for i in ids:
        bp = b.get(i, {}).get("passed")
        sp = s.get(i, {}).get("passed")
        gate = s.get(i, {}).get("gate")
        mark = {(True, True): "both", (False, True): "**skill only**",
                (True, False): "**baseline only**", (False, False): "neither"}[(bool(bp), bool(sp))]
        rows.append(f"| `{i}`{' *(gate)*' if gate else ''} | "
                    f"{s.get(i, {}).get('weight', 0) if not gate else '-'} | "
                    f"{'pass' if bp else 'fail'} | {'pass' if sp else 'fail'} | {mark} |")
        if gate:
            continue
        (gained if (sp and not bp) else lost if (bp and not sp)
         else both if sp else neither).append(i)

    def weight(ids_):
        return sum(s[i]["weight"] for i in ids_)

    scored = [r for r in skill["results"] if not r.get("gate")]
    total = sum(r["weight"] for r in scored)
    b_score = sum(b[r["id"]]["weight"] for r in scored if b.get(r["id"], {}).get("passed"))
    s_score = sum(r["weight"] for r in scored if r["passed"])

    gate_ok = all(r["passed"] for r in skill["results"] if r.get("gate"))

    out = [f"# Eniac evals - baseline vs with-skill", ""]
    if not gate_ok:
        out += ["> **The with-skill run did not report the skill as loaded.** The delta "
                "below is",
                "> almost certainly measuring nothing. Fix the install first — "
                "INSTALL.md,",
                "> *Verifying the install*.", ""]
    out += [
        f"- Agent command: `{skill['meta'].get('agent_cmd')}`",
        f"- Baseline: **{b_score} / {total}**",
        f"- With skill: **{s_score} / {total}**",
        f"- Delta: **{s_score - b_score:+d}**",
        "",
        "| Case | Weight | Baseline | With skill | |",
        "| --- | --- | --- | --- | --- |",
        *rows,
        "",
        "## Reading this",
        "",
        f"**Skill earned it ({weight(gained)} pts, {len(gained)} cases)** — the model did "
        f"not do this on its own. This is the only column that argues the guidance is "
        f"worth its tokens.",
        "",
        f"**Model already did it ({weight(both)} pts, {len(both)} cases)** — passing, but "
        f"not evidence for the skill. If a rule exists only to produce behaviour the model "
        f"defaults to, it is costing tokens for nothing.",
        "",
        f"**Skill lost it ({weight(lost)} pts, {len(lost)} cases)** — the most important "
        f"column and the easiest to skip. The guidance made something worse; read those "
        f"outputs before anything else.",
        "",
        f"**Neither passed ({weight(neither)} pts, {len(neither)} cases)** — either a gap "
        f"in the skill or a badly written case. Read the output before deciding which; "
        f"assuming the first is how a suite drifts into testing its own vocabulary.",
        "",
        "Assertions ran against final output text only. See `evals/README.md` for what "
        "that does and does not prove.",
        "",
    ]
    return "\n".join(out)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--agent-cmd", required=True)
    ap.add_argument("--skill-path", required=True,
                    help="the INSTALLED skill directory to move aside for the baseline")
    ap.add_argument("--timeout", type=int, default=600)
    args = ap.parse_args()

    skill = Path(args.skill_path).expanduser().resolve()
    aside = skill.with_name(skill.name + ".eval-aside")

    if not skill.is_dir():
        print(f"not a directory: {skill}\n"
              f"  Point --skill-path at the installed copy, not the repository.",
              file=sys.stderr)
        return 1
    if aside.exists():
        print(f"{aside} already exists — an earlier run did not clean up.\n"
              f"  Move it back by hand before running again; this script will not "
              f"guess which copy is real.", file=sys.stderr)
        return 1

    print(f"skill:    {skill}")
    print(f"aside as: {aside}  (restored in a finally block)\n")

    try:
        print("=== BASELINE: skill moved aside ===")
        skill.rename(aside)
        base = run_suite(args.agent_cmd, "baseline", args.timeout)
    finally:
        if aside.exists():
            aside.rename(skill)
            print(f"\nrestored {skill}")

    if base is None:
        print("baseline run produced nothing — aborting before the second run",
              file=sys.stderr)
        return 2

    print("\n=== WITH SKILL ===")
    with_skill = run_suite(args.agent_cmd, "with-skill", args.timeout)
    if with_skill is None:
        print("with-skill run produced nothing", file=sys.stderr)
        return 2

    report = compare(base, with_skill)
    (RESULTS / "comparison.md").write_text(report, encoding="utf-8", newline="\n")
    print("\n" + report)
    print(f"written to {RESULTS / 'comparison.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
