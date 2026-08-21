# Skill Evaluation And Improvement

Use when creating, changing, benchmarking, or tuning an agent skill, reusable
prompt, or engineering workflow. Structural validation proves packaging; only
behavioral scenarios show whether instructions improve decisions and outcomes.

## Evaluation Contract

Start from a real failure, accepted work sample, or recurring workflow. Define
the intended behavior before editing the skill:

```text
Capability:
Trigger: when it should load
Counter-trigger: when it should stay out
Artifact: one observable output or repository state
Verifier: deterministic check or explicit evidence rubric
Pressure: ambiguity, time, sunk cost, conflicting feedback, or missing context
Cost: runtime, tool calls, context, and unnecessary artifacts
```

Avoid trivia prompts that a general agent completes without the skill. Include
ordinary cases, edge cases, and counterexamples that reveal over-triggering or
overconstraint.

## Comparison Loop

1. Run the same bounded scenario without the skill when the runtime permits it.
2. Run it with the candidate skill under the same inputs and authority.
3. Compare verifier pass/fail before subjective quality, speed, or token cost.
4. Inspect action/observation traces or artifacts to locate the behavioral cause.
5. Classify the result: capability gain, reliability gain, neutral, mixed, or
   regression.
6. Change the smallest instruction, route, example, or reusable script that
   addresses the observed cause.
7. Re-run both the failing scenario and counterexamples.

One successful run is a smoke signal, not a stable benchmark. Use repeated runs,
different capable evaluators, or a blind comparison when variance or importance
justifies the cost. Record the runtime/model/backend because skill effects may
not transfer unchanged.

## Scenario Types

| Type | Tests | Typical failure |
| --- | --- | --- |
| Trigger | description selects the skill for substantive matching work | under-triggering |
| Counter-trigger | unrelated or simple work does not acquire the workflow | context tax or overreach |
| Technique | agent applies a method to a novel case | memorized checklist without transfer |
| Pressure | agent preserves the invariant under urgency or sunk cost | rationalized shortcut |
| Recovery | failed signal causes a different diagnosis or safe stop | repeated guessing |
| Portability | outcome survives a supported runtime or stack change | provider-specific assumptions |

Store portable scenarios in `evals/scenarios.json`. The package validator checks
their shape and uniqueness, not their behavioral result.

## Verifier Design

Prefer a deterministic verifier tied to the artifact: tests, schema validation,
exact file constraints, a build, a static rule, or a reproducible smoke path.
When judgment is unavoidable, use a short rubric with independent criteria and
evidence citations. Do not grade style by keyword matching or reward the skill
for repeating its own terminology.

A strong verifier can fail. Prove that the verifier detects at least one known
bad artifact or scenario before trusting a pass.

## Diagnosis

Trace a failed or slower scenario to one primary class:

- **routing:** description did not load, loaded too broadly, or selected the
  wrong reference;
- **instruction gap:** the required decision or invariant is absent;
- **ambiguity:** two rules conflict or lack priority;
- **overconstraint:** the skill forces a brittle path or unnecessary ceremony;
- **missing reusable tool:** runs repeatedly rebuild the same deterministic
  transformation or checker;
- **environment:** runtime, tool, permission, or dependency differs from the
  scenario contract;
- **verifier defect:** the check does not measure the claimed outcome.

Fix the deepest evidenced class. Do not add warnings for every hypothetical
mistake or grow the entry file when a routed reference, script, example, or
description adjustment is more precise.

## Promotion Gate

Promote a skill change only when:

- target scenarios improve or a clearly documented tradeoff is accepted;
- counter-trigger and lean-path scenarios do not regress materially;
- the package graph, links, scripts, and scenario manifest validate;
- an independent forward test challenges the changed behavior when available;
- the installed copy matches the validated source;
- residual model/runtime variance is stated rather than hidden.

Delete scenarios that no longer represent a real contract. Add a scenario when
a production failure reveals a reusable gap. Evaluation is a maintenance loop,
not a one-time score.
