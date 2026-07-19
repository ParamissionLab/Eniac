# Extended Plan Template

Use for L2-L3 greenfield or broad feature work where the minimal `.eniac-plan.md` format lacks sufficient context for decision-making. For L3 work, make it a durable execution context during the task so a new session can safely resume. For L1 targeted work, the minimal plan format in SKILL.md is sufficient.

## Template

```markdown
# Plan: <Project or Feature Name>

> Status: active | blocked | done
> Owner: <runtime task id or unique task label>
> Retention: delete-on-complete | retain-by-explicit-request
> Created: <date>

## Goal

<One paragraph: what problem does this solve, who benefits, what does success look like concretely.>

## Users and Use Cases

- **Primary user:** <who>
- **Core use case:** <what they accomplish>
- **Secondary:** <optional additional users/cases>

## Architecture

**Stack:** <language, framework, database, hosting>

**Key decisions:**

| Decision | Chosen | Rejected | Reason | Reversal cost |
|----------|--------|----------|--------|---------------|
| <e.g., framework> | <choice> | <alternative> | <why> | low/medium/high |

**Structure:**
<Brief description of module/directory layout if not obvious>

## System Context

- **Important paths:** <entry points, contracts, tests, config>
- **Confirmed facts:** <decision-relevant evidence>
- **Assumptions:** <labeled premise and verification path>
- **Invariants:** <behavior, data, and compatibility that must hold>

## Workflow

- **Workflow:** sequential | parallel lanes | dependency waves | pipeline | recovery
- **Integration owner:** <primary agent or role>
- **Final proof:** <required cross-boundary signal>
- **Current wave:** <identifier and exit condition>

## Workstreams

| ID | Outcome | Needs | Mutable scope | Proof | Status |
|----|---------|-------|---------------|-------|--------|
| W0 | <design gate> | none | <paths> | <signal> | queued |

**Dispatch rule:** Run workstreams concurrently only when their mutable scopes and unfinished contracts do not overlap. The primary agent accepts each output and runs integration proof.

## Evidence And Decisions

- **E1:** <fact/signal and source>
- **D1:** <binding decision, reason, reversal/review trigger>

## Coverage And Cause

- **Coverage gap:** none | <requirement, flow, contract, operation, or documentation surface>
- **Causal record:** not applicable | <symptom -> immediate cause -> root cause -> proof>
- **Doc impact:** none | <artifact and update>

## Task Breakdown

### Layer 1 — Foundation / Setup
- [ ] 🟢 <task> — Done when: <criteria>
- [ ] 🟡 <task> — Done when: <criteria>

### Layer 2 — Core Logic
- [ ] 🟡 <task> — Done when: <criteria>
- [ ] 🔴 <task> — Done when: <criteria>

### Layer 3 — Interface / API / UI
- [ ] 🟡 <task> — Done when: <criteria>

### Layer 4 — Tests and Verification
- [ ] 🟢 <task> — Done when: <criteria>

### Layer 5 — Documentation and Ship
- [ ] 🟢 <task> — Done when: <criteria>

**Complexity:** 🟢 easy (< 1hr) / 🟡 medium (1-4hr) / 🔴 hard (> 4hr or uncertain)

**Parallelizable:** <which tasks can run independently>

## Scope Boundary

- **Reuse:** <existing code, patterns, or infrastructure to build on>
- **Create:** <new files, modules, or systems>
- **Preserve:** <interfaces, data, behavior that must not change>
- **Exclude:** <explicit non-goals, future features not included>

## Risks and Unknowns

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| <risk> | 🟢/🟡/🔴 | 🟢/🟡/🔴 | <action> |

## Constraints

- <e.g., must work offline, no paid APIs, target Node 18+>
- <e.g., must not break existing API consumers>

## Open Questions

- [ ] <question that needs answer before or during build>

## Active State

- **Current:** <active milestone or task>
- **Last signal:** <latest verification evidence>
- **Next:** <one concrete action>
- **Blocker:** none | <what's blocking>

## Progress

| Phase | Status | Signal |
|-------|--------|--------|
| Discover | ✅/⏳/⏸️ | <evidence> |
| Plan | ✅/⏳/⏸️ | <evidence> |
| Build | ✅/⏳/⏸️ | <evidence> |
| Test | ✅/⏳/⏸️ | <evidence> |
| Bug hunt | ✅/⏳/⏸️ | <evidence> |
| Polish | ✅/⏳/⏸️ | <evidence> |
| Document | ✅/⏳/⏸️ | <evidence> |
| Ship | ✅/⏳/⏸️ | <evidence> |
```

## Usage Rules

- Fill only sections relevant to the task. Remove empty sections.
- Update `Active State` in place; do not append history.
- For L3 or multi-workstream work, also keep System Context, Workflow, Workstreams, Evidence, and Decisions current. Add only durable facts that affect later work; replace stale content and mark a superseded decision explicitly.
- At every material loop, reweight the next action and update applicable coverage, causal, and documentation state. A containment patch must remain labeled until the causal correction has proof or an explicit owner.
- Update `Progress` table as phases complete with the observed signal.
- Task Breakdown layers can be renamed to match the actual decomposition (e.g., "Backend", "Frontend", "Data layer").
- Share the plan with the user before first mutation on L3 work or when architecture decisions need confirmation.
- Delete the task-owned plan after `Status: done` and verification passes by default at every level. Use its exact path, explicit workspace root, and matching owner for finalization. Retain it only when the user explicitly requested retention or an active repository policy requires it, and state its path in the final handoff. If deletion fails, mark the task blocked and report the exact path and reason.
- For L2 work, the minimal plan in SKILL.md is often sufficient; use this template only when the task has multiple unknowns, risks, or architecture decisions.
