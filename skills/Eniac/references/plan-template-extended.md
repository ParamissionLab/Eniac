# Extended Plan Template

Use for L2-L3 greenfield or broad feature work where the minimal `.eniac-plan.md` format lacks sufficient context for decision-making. For L1 targeted work, the minimal plan format in SKILL.md is sufficient.

## Template

```markdown
# Plan: <Project or Feature Name>

> Status: active | blocked | done
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
- Update `Progress` table as phases complete with the observed signal.
- Task Breakdown layers can be renamed to match the actual decomposition (e.g., "Backend", "Frontend", "Data layer").
- Share the plan with the user before first mutation on L3 work or when architecture decisions need confirmation.
- Delete the plan file after `Status: done` and verification passes.
- For L2 work, the minimal plan in SKILL.md is often sufficient; use this template only when the task has multiple unknowns, risks, or architecture decisions.
