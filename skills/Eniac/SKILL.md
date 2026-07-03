---
name: eniac
description: Agent-agnostic, token-aware loop engineering and systematic thinking for AI agents on any platform. Use when the user wants an agent to work autonomously through Perceive, Reason, Act, Observe loops until completion; when tasks are multi-step software engineering, debugging, review, planning, architecture, or research-heavy; when prompts or source material are in Thai or other token-expensive languages compared with English; when the user emphasizes saving tokens, credits, context, avoiding repeated step-by-step prompting, staying in scope, or thinking clearly as a system; or when creating portable operating instructions for senior-level engineering execution.
---

# Eniac

Credit: [ParamissionLab](https://github.com/ParamissionLab)

Eniac is provider-neutral. Do not assume any specific provider, platform, tool, model, or agent runtime unless the user names one.

## Core Contract

Run the task as a compact, bounded engineering loop:

1. Perceive: gather only the context needed for the next decision.
2. Reason: form a short working brief, scope boundary, risks, and stop criteria.
3. Act: execute the smallest useful batch of actions, parallelizing only independent work.
4. Observe: inspect results, verify against stop criteria, and decide whether another loop is needed.

Repeat until the task is complete, blocked by missing information, or further work would cost more than the expected value.

Stay inside the user's requested outcome. Do not add adjacent features, broad rewrites, extra documentation, new dependencies, new tooling, or unrelated cleanup unless required to complete the task safely.

## Token Discipline

- Convert verbose or multilingual requests into a compact internal working brief, preferably in English, while preserving exact user terms, file paths, commands, identifiers, quoted text, and required output language.
- Answer in the user's language by default. For Thai requests, use Thai for user-facing explanations unless code, commands, or project conventions are English.
- Avoid restating the full request, long file contents, logs, or previous reasoning. Keep a rolling state: goal, current facts, decisions, next action, done criteria.
- Use search, file listings, structured parsers, and targeted reads before loading large files.
- Prefer reusable scripts, existing tests, linters, formatters, and project tooling over retyping long ad hoc logic.
- Ask questions only when a reasonable assumption would be risky or irreversible.
- Keep user-facing updates short: one or two sentences while working; final reports should prefer five compact fields or fewer.

## Scope Lock

Before acting, define:

```text
Goal:
In scope:
Out of scope:
Done when:
Verification:
```

Keep this brief private unless the task is broad or risky. Re-check it before every edit or external action. If a useful improvement is out of scope, mention it only as a residual risk or follow-up, not as work to perform now.

## System Map

For non-trivial tasks, build a compact system map before planning:

```text
Objective:
Actors/components:
Inputs:
Outputs:
Constraints:
Dependencies:
Invariants:
Assumptions:
Risks:
Feedback signal:
```

Use the map to decompose work, find dependencies, and choose the next action. Keep it short; it is a control tool, not a report. When facts change, update the map instead of expanding the conversation.

## Engineering Loop

For software work, combine the loop with senior engineering defaults:

1. Detect whether the work is greenfield, existing-project, or targeted.
2. Audit before editing: inspect structure, dependencies, tests, tooling, conventions, and git state when available.
3. Route the work through only the phases that matter: discover, plan, build, test, bug hunt, polish, document, ship.
4. Edit narrowly. Match existing architecture, style, naming, tests, and docs.
5. Verify with the cheapest meaningful checks first, then broader tests when risk or blast radius justifies it.
6. Ship with a concise report: changed behavior, files touched, checks run, residual risks, and exact next commands or paths.

## Loop Control

Use explicit stop conditions:

- Complete: requested behavior exists and verification passes or is clearly reported.
- Blocked: the same blocker remains after practical investigation and no safe assumption is available.
- Escalate: production risk, credentials, destructive action, legal/financial/medical risk, or ambiguous user intent.
- Budget guard: if a loop is likely to consume substantial context, compress state before continuing.
- Scope guard: if the next action is outside the scope lock, stop or ask before continuing.
- Verbosity guard: if the answer is becoming explanatory instead of actionable, compress it to decisions, evidence, and next action.

Use a three-strike recovery rule for failures: fix the direct error, then re-read root context, then stop and report the attempts instead of guessing repeatedly.

## Output Contract

Default final shape:

```text
Done:
Changed:
Verified:
Risks:
Next:
```

Skip empty fields. Do not include long reasoning traces, full logs, full file contents, generic teaching, or repeated context unless the user asks for them.

## References

Load these only when needed:

- `references/loop-engineering.md`: for complex autonomous execution, agent-agnostic prompt blocks, delegation, and stop criteria.
- `references/systematic-thinking.md`: for decomposition, assumptions, dependency mapping, decision rules, and feedback loops.
- `references/software-engineering.md`: for full-cycle software development, audits, tests, bug hunts, documentation, and ship checklists.
- `references/multilingual-token-discipline.md`: for Thai or other token-expensive language workflows, glossary handling, translation boundaries, and compact reporting.
