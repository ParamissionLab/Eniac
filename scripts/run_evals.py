#!/usr/bin/env python3
"""Behavioural evaluation harness for the Eniac skill.

`check_skill.py` proves the package is well-formed. It cannot prove the package makes an
agent behave better, and a skill verified only structurally is a skill whose central claim
is untested. This is the missing half.

It is deliberately runtime-neutral, for the same reason the adapters are: you supply the
command that runs your agent, and the harness supplies the prompts and the grading. That
keeps a result from Codex comparable to a result from Claude Code or a raw API call.

    # validate the case file and the assertion engine, no agent needed
    python scripts/run_evals.py --self-test

    # see exactly what would run
    python scripts/run_evals.py --dry-run

    # run for real: {prompt} is substituted, or the prompt goes to stdin if absent
    python scripts/run_evals.py --agent-cmd 'claude -p {prompt}'
    python scripts/run_evals.py --agent-cmd 'codex exec {prompt}' --label codex

    # the comparison that actually matters
    python scripts/run_evals.py --agent-cmd '...' --label with-skill
    python scripts/run_evals.py --agent-cmd '...' --label baseline   # skill not installed

Assertions run against the agent's final output text, because that is the one artifact
every runtime produces. That is a real limitation and it is stated rather than hidden:
these cases catch what the agent *says* it did. Pair them with a reading of the transcript
for anything where saying and doing could diverge.

Results land in evals/results/ as JSON plus a Markdown report. Standard library only.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CASES = ROOT / "evals" / "cases.json"
RESULTS = ROOT / "evals" / "results"


# --- assertion engine -------------------------------------------------------------

def check(assertion: dict, output: str) -> bool:
    kind, value = assertion["kind"], assertion.get("value")
    if kind == "contains":
        return value in output
    if kind == "not_contains":
        return value not in output
    if kind == "matches":
        return re.search(value, output) is not None
    if kind == "not_matches":
        return re.search(value, output) is None
    if kind == "max_chars":
        return len(output) <= value
    if kind == "min_chars":
        return len(output) >= value
    raise ValueError(f"unknown assertion kind: {kind}")


KINDS = ("contains", "not_contains", "matches", "not_matches", "max_chars", "min_chars")


# --- running ----------------------------------------------------------------------

def run_agent(cmd_template: str, prompt: str, timeout: int) -> tuple[str, str | None]:
    """Return (output, error). Substitutes {prompt}, or pipes it in if absent."""
    try:
        if "{prompt}" in cmd_template:
            cmd = cmd_template.replace("{prompt}", prompt)
            proc = subprocess.run(
                cmd, shell=True, capture_output=True, text=True, timeout=timeout
            )
        else:
            proc = subprocess.run(
                cmd_template, shell=True, input=prompt,
                capture_output=True, text=True, timeout=timeout,
            )
    except subprocess.TimeoutExpired:
        return "", f"timed out after {timeout}s"
    except Exception as exc:  # pragma: no cover
        return "", str(exc)
    if proc.returncode != 0 and not proc.stdout.strip():
        return "", f"exit {proc.returncode}: {proc.stderr.strip()[:400]}"
    return proc.stdout, None


def grade(case: dict, output: str) -> dict:
    checks = []
    for a in case["pass_if"]:
        ok = check(a, output)
        checks.append({
            "kind": a["kind"],
            "value": a.get("value"),
            "reason": a.get("reason", ""),
            "passed": ok,
        })
    return {
        "id": case["id"],
        "weight": case.get("weight", 1),
        "passed": all(c["passed"] for c in checks),
        "checks": checks,
        "output_chars": len(output),
    }


# --- reporting --------------------------------------------------------------------

def report_markdown(label: str, results: list[dict], meta: dict) -> str:
    earned = sum(r["weight"] for r in results if r["passed"])
    total = sum(r["weight"] for r in results)
    errored = [r for r in results if r.get("error")]

    lines = [
        f"# Eniac behavioural evals — {label}",
        "",
        f"- Skill version: `{meta.get('version', 'unknown')}`",
        f"- Agent command: `{meta.get('agent_cmd', 'n/a')}`",
        f"- Weighted score: **{earned} / {total}**",
        f"- Cases passed: {sum(1 for r in results if r['passed'])} / {len(results)}",
    ]
    if errored:
        lines.append(f"- Cases that failed to run: {len(errored)} (not counted as passes)")
    lines += ["", "| Case | Weight | Result | Failing check |", "| --- | --- | --- | --- |"]
    for r in results:
        if r.get("error"):
            detail = f"could not run — {r['error']}"
            mark = "ERROR"
        else:
            bad = [c for c in r["checks"] if not c["passed"]]
            detail = bad[0]["reason"] if bad else ""
            mark = "pass" if r["passed"] else "FAIL"
        lines.append(f"| `{r['id']}` | {r['weight']} | {mark} | {detail} |")

    lines += [
        "",
        "## What this does and does not prove",
        "",
        "Assertions ran against each agent's final output text. That catches what the agent",
        "*said* it did. Where saying and doing could diverge — whether a reference was",
        "actually read, whether a file was actually written — read the transcript before",
        "treating a pass as evidence.",
        "",
        "A score here is only meaningful against a baseline run of the same cases with the",
        "skill not installed. One number alone measures the model, not the skill.",
        "",
    ]
    return "\n".join(lines)


# --- entry point ------------------------------------------------------------------

def self_test() -> int:
    """Prove the harness works before trusting a result from it."""
    problems = []
    data = json.loads(CASES.read_text(encoding="utf-8"))
    ids = [c["id"] for c in data["cases"]]
    if len(ids) != len(set(ids)):
        problems.append("duplicate case ids")
    for case in data["cases"]:
        for field in ("id", "prompt", "why", "pass_if"):
            if field not in case:
                problems.append(f"{case.get('id', '?')}: missing `{field}`")
        for a in case.get("pass_if", []):
            if a["kind"] not in KINDS:
                problems.append(f"{case['id']}: unknown assertion kind {a['kind']!r}")
            if a["kind"] in ("matches", "not_matches"):
                try:
                    re.compile(a["value"])
                except re.error as exc:
                    problems.append(f"{case['id']}: bad regex {a['value']!r} ({exc})")
            if not a.get("reason"):
                problems.append(f"{case['id']}: assertion has no `reason`, so a failure "
                                f"would not say what went wrong")

    # An assertion set that nothing can fail is not an assertion set. Every case must
    # reject at least one plausible bad answer, so we grade each case against a
    # deliberately terrible output and require it to fail.
    junk = ("Done:\nChanged: everything\nVerified: fixed, works now.\n"
            "I also cleaned up the quotes while I was there. "
            "Creating a new file docs/api/password-reset.md. "
            "Deleted 4,201 rows. references/craft.md " + "x" * 2000)
    for case in data["cases"]:
        try:
            if grade(case, junk)["passed"]:
                problems.append(f"{case['id']}: passes a deliberately bad answer — "
                                f"the assertions do not discriminate")
        except ValueError as exc:
            problems.append(f"{case['id']}: {exc}")

    if problems:
        for p in problems:
            print(p)
        print(f"\n{len(problems)} problem(s).")
        return 1
    weights = sum(c.get("weight", 1) for c in data["cases"])
    print(f"ok - {len(data['cases'])} cases ({weights} weighted points), assertions "
          f"compile and all reject a known-bad answer")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--agent-cmd", help="shell command; {prompt} is substituted if present")
    ap.add_argument("--label", default="run", help="name for this run, e.g. with-skill")
    ap.add_argument("--timeout", type=int, default=600)
    ap.add_argument("--only", help="run one case by id")
    ap.add_argument("--dry-run", action="store_true", help="print what would run")
    ap.add_argument("--self-test", action="store_true", help="validate cases, no agent")
    args = ap.parse_args()

    if args.self_test:
        return self_test()

    data = json.loads(CASES.read_text(encoding="utf-8"))
    cases = [c for c in data["cases"] if not args.only or c["id"] == args.only]
    if not cases:
        print(f"no case matching {args.only!r}", file=sys.stderr)
        return 1

    if args.dry_run or not args.agent_cmd:
        if not args.agent_cmd:
            print("no --agent-cmd given; showing what would run\n")
        for c in cases:
            print(f"--- {c['id']} (weight {c.get('weight', 1)}) ---")
            print(f"why: {c['why']}")
            print(f"prompt: {c['prompt'][:200]}")
            print(f"checks: {len(c['pass_if'])}\n")
        return 0

    results = []
    for c in cases:
        print(f"running {c['id']} ...", flush=True)
        output, error = run_agent(args.agent_cmd, c["prompt"], args.timeout)
        r = grade(c, output) if not error else {
            "id": c["id"], "weight": c.get("weight", 1), "passed": False,
            "checks": [], "output_chars": 0, "error": error,
        }
        r["output"] = output
        results.append(r)
        print(f"  {'pass' if r['passed'] else 'FAIL'}")

    meta = {"version": data.get("version"), "agent_cmd": args.agent_cmd, "label": args.label}
    RESULTS.mkdir(parents=True, exist_ok=True)
    (RESULTS / f"{args.label}.json").write_text(
        json.dumps({"meta": meta, "results": results}, indent=2), encoding="utf-8"
    )
    md = report_markdown(args.label, results, meta)
    (RESULTS / f"{args.label}.md").write_text(md, encoding="utf-8", newline="\n")
    print("\n" + md)

    earned = sum(r["weight"] for r in results if r["passed"])
    total = sum(r["weight"] for r in results)
    return 0 if earned == total else 1


if __name__ == "__main__":
    raise SystemExit(main())
