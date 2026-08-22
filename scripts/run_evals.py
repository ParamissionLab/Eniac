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

PROBE_PROMPT = "Reply with exactly this token and nothing else: HARNESS_PROBE_OK_7Q2X"
PROBE_TOKEN = "HARNESS_PROBE_OK_7Q2X"


def probe(cmd_template: str, timeout: int) -> str | None:
    """Prove the agent command reaches a working agent before grading anything.

    A CLI that is unauthenticated, missing, or misconfigured normally exits 0 and prints a
    short notice to stdout. Graded against that, any case whose assertions are all negative
    passes - which is exactly how a run where no agent ever executed reports a score. A run
    that cannot be trusted must refuse to produce a number at all.
    """
    output, error = run_agent(cmd_template, PROBE_PROMPT, timeout)
    if error:
        return f"agent command failed: {error}"
    if PROBE_TOKEN not in output:
        head = " ".join(output.split())[:200] or "(no output at all)"
        return (f"agent did not answer the probe. It returned: {head!r}\n"
                f"    That is not an agent response, so nothing below would be measuring "
                f"the skill.\n"
                f"    Check the CLI is installed, authenticated, and that --agent-cmd is "
                f"right.")
    return None


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
    scored = [r for r in results if not r.get("gate")]
    gates = [r for r in results if r.get("gate")]
    gate_failed = [g for g in gates if not g["passed"]]
    earned = sum(r["weight"] for r in scored if r["passed"])
    total = sum(r["weight"] for r in scored)
    errored = [r for r in results if r.get("error")]

    lines = [f"# Eniac behavioural evals - {label}", ""]
    if gate_failed:
        lines += [
            "> **The skill did not report itself as loaded.** Everything below is measuring",
            "> the model on its own. Confirm the install before reading further: the agent",
            "> should answer a bare \"what rules are you following?\" by naming the skill.",
            "> See INSTALL.md, *Verifying the install*.",
            "",
        ]
    elif gates:
        lines += ["> Skill confirmed loaded - the agent named it when asked.", ""]
    lines += [
        f"- Suite version: `{meta.get('version', 'unknown')}`",
        f"- Agent command: `{meta.get('agent_cmd', 'n/a')}`",
        f"- Weighted score: **{earned} / {total}**"
        + ("  *(not attributable - see the gate above)*" if gate_failed else ""),
        f"- Cases passed: {sum(1 for r in scored if r['passed'])} / {len(scored)}",
    ]
    if errored:
        lines.append(f"- **Cases that never produced an answer: {len(errored)}** - the "
                     f"score is not measuring the skill for these")
    lines += ["", "| Case | Weight | Result | Failing check |", "| --- | --- | --- | --- |"]
    for r in results:
        if r.get("error"):
            detail = f"could not run — {r['error']}"
            mark = "ERROR"
        else:
            bad = [c for c in r["checks"] if not c["passed"]]
            detail = bad[0]["reason"] if bad else ""
            mark = "pass" if r["passed"] else "FAIL"
        name = f"`{r['id']}`" + (" *(gate)*" if r.get("gate") else "")
        weight = "-" if r.get("gate") else r["weight"]
        lines.append(f"| {name} | {weight} | {mark} | {detail} |")

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

def dead_assertion(case_id: str, a: dict) -> list[str]:
    """Catch an assertion that cannot fail, in either direction.

    The case-level tests below grade whole answers, so they only see the assertion set
    as a group. An individual assertion can be inert inside a set that still passes its
    junk test, and nothing announces it - the case simply gets quietly weaker. Both
    directions are silent in the same way and both are checked here:

      * A negative that matches nothing passes every answer forever.
      * A positive that matches everything passes every answer forever.

    A real one got shipped: `^(?:(?!word).)*$` looks like "contains none of these" and is
    dead against any multi-line output, because `.` does not cross a newline and agent
    output always has one. It was caught by reading, not by this harness. Hence
    `tripped_by`: a negative assertion carries an example of the output it exists to
    reject, the example is checked against the pattern here, and deadness stops being
    expressible rather than merely discouraged.
    """
    out, kind, val = [], a["kind"], a.get("value")

    if kind in ("matches", "not_matches") and isinstance(val, str):
        try:
            body = re.sub(r"^\(\?[aiLmsux]+\)", "", val)
            flags = re.match(r"^\(\?([aiLmsux]+)\)", val)
            if (body.startswith("^") and body.endswith("$")
                    and "s" not in (flags.group(1) if flags else "")):
                out.append(f"{case_id}: {val[:40]!r}... anchors the whole string with "
                           f"^...$ but `.` does not cross a newline and no (?s) flag is "
                           f"set. Agent output is multi-line, so this can never match")
        except re.error:
            return out

    if kind == "matches" and isinstance(val, str):
        try:
            if re.search(val, ""):
                out.append(f"{case_id}: positive pattern {val[:40]!r}... matches the "
                           f"empty string, so it passes every possible answer")
        except re.error:
            pass
    if kind == "contains" and val == "":
        out.append(f"{case_id}: `contains` an empty string passes everything")

    if kind in ("not_matches", "not_contains"):
        w = a.get("tripped_by")
        if not w:
            out.append(f"{case_id}: `{kind}` has no `tripped_by`. A negative assertion "
                       f"that matches nothing passes every answer, and nothing else here "
                       f"can see that - give it one example of the output it rejects")
        elif kind == "not_matches":
            try:
                if not re.search(val, w):
                    out.append(f"{case_id}: `tripped_by` {w[:40]!r} does not match its "
                               f"own pattern, so this assertion is dead and every answer "
                               f"passes it")
            except re.error:
                pass
        elif val not in w:
            out.append(f"{case_id}: `tripped_by` {w[:40]!r} does not contain "
                       f"{val!r}, so this assertion is dead")
    return out


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
            problems += dead_assertion(case["id"], a)

    # An assertion set that nothing can fail is not an assertion set. Every case must
    # reject at least one plausible bad answer, so we grade each case against a
    # deliberately terrible output and require it to fail.
    junk = ("Done:\nChanged: everything\nVerified: fixed, works now.\n"
            "I also cleaned up the quotes while I was there. "
            "Creating a new file docs/api/password-reset.md. "
            "Deleted 4,201 rows. references/craft.md " + "x" * 2000)
    # A case whose assertions are all negative passes an EMPTY output, which means a run
    # where the agent never executed reports a green case. That is the worst failure this
    # harness can have, so it is checked structurally as well as by example.
    non_answers = ["", "   ", "Not logged in - please run /login", "command not found"]

    for case in data["cases"]:
        positives = [a for a in case.get("pass_if", [])
                     if a["kind"] in ("contains", "matches", "min_chars")]
        if not positives:
            problems.append(f"{case['id']}: every assertion is negative, so an empty "
                            f"output would pass. Add one matches/contains/min_chars that "
                            f"a real answer must satisfy")
        model = case.get("passes_like")
        if not model:
            problems.append(f"{case['id']}: no `passes_like`. A case nobody has written a "
                            f"passing answer for may be over-strict or self-contradictory, "
                            f"and neither is visible until a real run wastes a suite on it")
        else:
            try:
                verdict = grade(case, model)
                if not verdict["passed"]:
                    why = "; ".join(f"{c['kind']} {str(c['value'])[:50]!r}"
                                    for c in verdict["checks"] if not c["passed"])
                    problems.append(f"{case['id']}: its own model answer is rejected by "
                                    f"{why}. Either the assertion is stricter than the "
                                    f"behaviour it means to test, or the model answer is "
                                    f"not actually a good one - read both before loosening "
                                    f"anything")
            except ValueError as exc:
                problems.append(f"{case['id']}: grading `passes_like` raised {exc}")

        try:
            if grade(case, junk)["passed"]:
                problems.append(f"{case['id']}: passes a deliberately bad answer - "
                                f"the assertions do not discriminate")
            for bad in non_answers:
                if grade(case, bad)["passed"]:
                    problems.append(f"{case['id']}: passes a non-answer ({bad[:30]!r}) - "
                                    f"this case would report green on a run where no "
                                    f"agent executed")
                    break
        except ValueError as exc:
            problems.append(f"{case['id']}: {exc}")

    if problems:
        for p in problems:
            print(p)
        print(f"\n{len(problems)} problem(s).")
        return 1
    weights = sum(c.get("weight", 1) for c in data["cases"])
    gates = sum(1 for c in data["cases"] if c.get("gate"))
    print(f"ok - {len(data['cases'])} cases ({gates} gate, {weights} weighted points); "
          f"assertions compile, none can pass unconditionally, every negative carries "
          f"an example it demonstrably rejects, every case accepts its own model answer "
          f"and rejects a known-bad answer and a non-answer")
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
    cases.sort(key=lambda c: not c.get("gate"))  # the install check runs first
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

    print("probing the agent command ...", flush=True)
    blocked = probe(args.agent_cmd, args.timeout)
    if blocked:
        print(f"\n  ABORTED - {blocked}", file=sys.stderr)
        print("\n  No results were written. A score from a run where the agent never "
              "answered\n  is worse than no score, because it looks like evidence.",
              file=sys.stderr)
        return 2
    print("  probe ok\n", flush=True)

    results = []
    for c in cases:
        print(f"running {c['id']} ...", flush=True)
        output, error = run_agent(args.agent_cmd, c["prompt"], args.timeout)
        if not error and len(output.strip()) < 40:
            error = (f"agent returned {len(output.strip())} characters, which is not an "
                     f"answer: {output.strip()[:120]!r}")
        r = grade(c, output) if not error else {
            "id": c["id"], "weight": c.get("weight", 1), "passed": False,
            "checks": [], "output_chars": len(output), "error": error,
        }
        r["gate"] = bool(c.get("gate"))
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

    scored = [r for r in results if not r.get("gate")]
    earned = sum(r["weight"] for r in scored if r["passed"])
    total = sum(r["weight"] for r in scored)
    return 0 if earned == total else 1


if __name__ == "__main__":
    raise SystemExit(main())
