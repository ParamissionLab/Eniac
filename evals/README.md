# Evals

`scripts/check_skill.py` proves the package is well-formed. It cannot prove the package
makes an agent behave better, and a skill verified only structurally is a skill whose
central claim is untested. This directory is the other half.

It is also the **Signal** in the sense `skills/Eniac/references/loops.md` uses the word:
the outer loop that improves the skill cannot converge without a way to tell better from
worse, and every change to `SKILL.md` is a turn of that loop.

## What is here

| File | What it is |
| --- | --- |
| `cases.json` | behavioural cases — a prompt, why it matters, and assertions that a bad answer fails |
| `trigger.json` | queries for testing whether the `description` field makes the skill fire when it should and stay quiet when it should not |
| `results/` | run outputs, git-ignored — regenerate rather than commit |

## Running them

The harness is runtime-neutral for the same reason the adapters are: you supply the
command that runs your agent, so a result from one runtime is comparable to a result from
another.

```bash
python scripts/run_evals.py --self-test
```

Validates the case file and proves every case rejects a deliberately bad answer. Needs no
agent, runs in CI, and is the check that keeps a non-discriminating assertion — one that
passes no matter what the agent does — from quietly entering the suite.

```bash
python scripts/run_evals.py --dry-run
```

Prints each case, its rationale, and its assertion count.

```bash
python scripts/run_evals.py --agent-cmd 'claude -p {prompt}' --label with-skill
python scripts/run_evals.py --agent-cmd 'codex exec {prompt}'  --label with-skill-codex
```

`{prompt}` is substituted if present; otherwise the prompt is piped to stdin. Results land
in `results/<label>.json` and `results/<label>.md`.

## The comparison that matters

**A single score measures the model, not the skill.** Run the same cases twice — once with
the skill installed, once without — and compare:

```bash
# with skills/Eniac installed
python scripts/run_evals.py --agent-cmd '<your agent>' --label with-skill

# with it removed or disabled
python scripts/run_evals.py --agent-cmd '<your agent>' --label baseline
```

A case both runs pass is telling you the model already did that. A case only the with-skill
run passes is the skill earning its tokens. A case neither passes is a gap in the skill or
a badly written case — read the output before deciding which.

## What a pass does not prove

Assertions run against the agent's **final output text**, because that is the one artifact
every runtime produces. They catch what the agent *said* it did. Where saying and doing
could diverge — whether a reference was actually read, whether a file was actually
written — read the transcript before treating a pass as evidence. This limitation is
stated rather than designed around, because the alternative is a harness that only works on
one vendor's transcript format.

## Adding a case

A case earns its place by encoding a failure that has actually happened, or one the skill
explicitly claims to prevent. Each needs:

- **`why`** — the rule it tests and the failure it catches. A case whose rationale cannot
  be written in a sentence is usually testing prose rather than behaviour.
- **`reason` on every assertion** — it is what the report prints when the case fails, and a
  failure that does not say what went wrong costs a debugging session.
- **Assertions that a bad answer fails.** `--self-test` grades every case against a
  deliberately terrible output and rejects the case if it passes. An assertion that always
  passes is worse than no assertion: it makes the suite look green while measuring nothing.

Prefer `not_matches` on the specific bad behaviour over `matches` on the good one. There
are many right answers and comparatively few characteristic wrong ones, so the negative
form is both more robust and less likely to reward an agent for reciting the skill's own
vocabulary back.

## Triggering

`trigger.json` is a separate question: not *does the skill behave well* but *does it fire
at all*. Half the queries should trigger and half should not, and the valuable ones are the
near-misses — queries that share vocabulary with the skill but need something else. Feed it
to whichever description-optimization tooling your runtime offers; the file is plain JSON so
it is not tied to one.
