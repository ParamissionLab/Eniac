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

## The gate runs first

`skill-reports-itself-loaded` is not a behaviour test — it is an install test, and it is
scored separately from everything else. It asks the agent what rules it follows and checks
that the skill names itself.

Without it, an install that silently failed reports as *the skill did not help*, which is
the most expensive misreading available: you would go and rewrite guidance that was never
loaded. When the gate fails, the report says so at the top and marks the score
unattributable rather than printing a number that looks like a finding.

## The comparison that matters

**A single score measures the model, not the skill.** One command runs both arms — it moves
the installed skill aside, runs the baseline, restores it in a `finally`, runs again, and
writes an attributed comparison:

```bash
python scripts/compare_evals.py \
    --agent-cmd 'claude -p {prompt}' \
    --skill-path ~/.claude/skills/Eniac
```

`--skill-path` is required and never guessed, because this moves a directory outside the
repository.

The comparison splits every case four ways, and the columns are not equally interesting:

- **Skill earned it** — only the with-skill run passed. The only column that argues the
  guidance is worth its tokens.
- **Model already did it** — both passed. Not evidence for the skill; a rule that only
  produces behaviour the model defaults to is costing tokens for nothing.
- **Skill lost it** — only the baseline passed. The most important column and the easiest
  to skip. Read those outputs before anything else.
- **Neither passed** — a gap in the skill, or a badly written case. Read the output before
  deciding which; assuming the first is how a suite drifts into testing its own vocabulary.

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

- **`tripped_by` on every `not_matches` and `not_contains`** — one short example of the
  output the assertion exists to reject. The self-test checks the example against the
  pattern, so a negative assertion that matches nothing cannot be written.

- **`passes_like` on every case** — one realistic good answer, which the self-test grades
  and requires to pass. It is the other half of `tripped_by`: that one proves an assertion
  can fail, this one proves the case can be passed.

### Why `tripped_by` is required

The case-level tests grade whole answers, so they only ever see the assertion set as a
group. A single inert assertion inside a set that still fails the junk test is invisible:
the case just gets quietly weaker, and the suite keeps printing green.

Both directions of deadness are silent in exactly the same way. A negative that matches
nothing passes every answer forever; a positive that matches everything does too. So the
self-test now rejects a positive pattern that matches the empty string, rejects a
whole-string `^...$` pattern with no `(?s)` flag — `.` does not cross a newline and agent
output always has one — and requires every negative to carry an example it demonstrably
rejects.

That last rule exists because a dead assertion was shipped here: `^(?:(?!word).)*$`, which
reads as "contains none of these" and can never match multi-line output. It was caught by
reading the regex, not by the harness. `tripped_by` makes it unwriteable rather than merely
discouraged, and it doubles as documentation — the example *is* the failure the case is
about.

### Why `passes_like` is required

`tripped_by` closes assertions that can never fail. `passes_like` closes the opposite
failure, which is quieter than it sounds: an assertion stricter than the behaviour it means
to test, so that a genuinely good answer is marked wrong.

That one does not announce itself either. It looks exactly like a finding — the case goes
red, and the natural reading is *the skill did not do this*, which sends you to rewrite
guidance that was working. Worse is the self-contradictory case, where two assertions
cannot both hold and no answer can ever pass; it will sit in the suite going red forever
while looking like a persistent gap.

Grading one hand-written good answer catches all of it: a positive narrowed to jargon the
answer never uses, a negative broad enough to catch correct output, a `max_chars` set below
what the answer needs, and any pair of assertions that contradict.

**Write the model answer first, then check it against the assertions.** Writing it *to* the
assertions inverts the test and proves almost nothing — a minimal string assembled to
satisfy each pattern in turn is not evidence that any real answer would. If the honest good
answer fails, read both before loosening anything: sometimes the assertion is wrong, and
sometimes the answer is not as good as it looked.

What this does **not** prove is that a real agent would produce something passing. It proves
the case is satisfiable and not over-strict, which is the failure that was invisible before.

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
