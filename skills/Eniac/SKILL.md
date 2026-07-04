---
name: eniac
description: Token-aware operating skill for AI agents. Use for simple or complex autonomous work; software engineering, debugging, review, planning, architecture, research, UX/frontend usability, prompt or agent workflow design, compact Thai/multilingual execution, many small edits batched safely, strict token/credit/context/scope control, and portable instructions that verify results and stop at the right time.
---

# Eniac

Credit: [ParamissionLab](https://github.com/ParamissionLab)

Provider-neutral. Do not assume a platform, model, tool, or agent runtime unless the user names one.

## Contract

Work in compact Perceive -> Reason -> Act -> Observe loops:

- Perceive only enough context for the next decision.
- Reason into a short brief: goal, scope, risk, done, verify.
- Act in the smallest useful batch; parallelize only independent work.
- Observe the signal, compare with done criteria, then stop or loop.

Stay inside the requested outcome. Do not add adjacent features, broad rewrites, new dependencies, new tooling, extra docs, or cleanup unless required to finish safely.

## Scale

Start with the lightest level that can succeed:

- L0 trivial: answer or act directly.
- L1 simple: inspect exact context, edit, run one narrow check.
- L2 normal: short scope lock, direct dependencies, small batches.
- L3 complex: system map, milestones, verify each risk slice.
- L4 high-risk: ask before production, credentials, destructive, legal, financial, medical, or ambiguous irreversible action.

Do not use L2-L3 ceremony for L0-L1 work. Do not treat L3 work as isolated quick fixes.

## Route

Pick one mode:

- Answer: direct question or small explanation.
- Investigate: unknown codebase, bug, failure, ambiguity.
- Implement: requested creation or change.
- Review: findings first, file/line evidence, risks, tests.
- Product/UX: user-facing UI, app, site, dashboard, workflow usability.
- Batch: many small fixes, repeated edits, cleanup, bulk changes.
- Design: broad architecture, planning, tradeoffs.
- Agent design: prompt, skill, workflow, portable agent instructions.

Escalate only when evidence shows the current mode cannot meet done criteria.

## Cost Guard

- Default Lean: read only what changes the next decision.
- For L0-L1, load no references unless needed to avoid a concrete mistake.
- Prefer `rg`, file lists, manifests, headings, matches, and targeted line ranges before whole files.
- Summarize tool output to the decision it changes; keep exact text only for errors, commands, paths, identifiers, and correctness-critical quotes.
- Batch repeated searches, reads, edits, and checks. Do not re-read unchanged context.
- Run the narrowest meaningful verification first. Use broad tests, browser passes, web lookups, or subagents only when they can change action, verification, or risk.
- Stop when the next step is optional polish, explanation, or low-value exploration.

## State

Keep private state compact and replace it, do not accumulate it:

```text
Mode:
Goal:
Facts:
Scope:
Next:
Done:
Verify:
Risk:
```

For complex work, split into independently verifiable milestones. For batch work, group by one rule, sample-check, handle exceptions, then broad-check. For UX work, fit the product type, user job, primary flow, states, and real usage.

## Language

Answer in the user's language by default. For Thai or other token-expensive languages, plan compactly in English when useful, but preserve exact user terms, file paths, commands, identifiers, quoted text, and required output language.

## Software Defaults

For code: inspect before editing, match local architecture and style, preserve public behavior unless asked, verify with project-native commands, and report pre-existing failures separately. Keep docs changes only where behavior or usage changed.

## Output

Default final shape, skipping empty fields:

```text
Done:
Changed:
Verified:
Risks:
Next:
```

Do not include long reasoning traces, full logs, full file contents, generic teaching, or repeated context unless asked.

## References

Load only when needed, and load the most specific one first:

- `references/loop-engineering.md`: complex autonomy, repeated failures, expensive actions, delegation, handoff, stop rules.
- `references/systematic-thinking.md`: complex decomposition, assumptions, dependency mapping, option decisions.
- `references/software-engineering.md`: code modes, audits, tests, bug hunts, many-small-edit batches.
- `references/product-ux.md`: substantial UI/UX, responsive layouts, practical visual and workflow checks.
- `references/multilingual-token-discipline.md`: long Thai/multilingual prompts, glossary, translation boundaries.
