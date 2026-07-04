# Product UX Reference

Use when the task affects a user-facing interface, workflow, website, app, dashboard, editor, form, game, or design system.

## Domain Fit

| Domain | Priority | Avoid |
| --- | --- | --- |
| SaaS, CRM, admin, analytics | scanning, comparison, repeated actions | marketing layouts, low density |
| Developer or ops | diagnosis, logs, filters, keyboard flow | decoration hiding state/errors |
| Commerce or booking | trust, visible options/price/state | vague CTAs, hidden costs |
| Content, portfolio, brand | strong first signal, readable narrative, media | generic stock feel |
| Game/playful app | feedback, readable state, satisfying motion | unclear rules, slow restarts |
| Data entry/workflow | low error rate, validation, recovery, tab order | surprise navigation |

Follow the existing design system first. Improve only what blocks the requested outcome.

## Workflow Frame

```text
User:
Task:
Frequency:
Decision:
Info:
Action:
Failure:
Success:
```

Use the frame to choose density, layout, controls, and copy. Prefer clearer controls, labels, states, or flow over instructional text.

## Quality Gate

Check only what the change can affect:

- First screen and primary action are clear.
- Hierarchy separates primary action, secondary actions, and status.
- Density fits the domain.
- Controls match semantics: button, tab, filter, menu, slider, toggle, input.
- Relevant loading, empty, error, disabled, selected, hover/focus, and success states exist.
- Mobile and desktop keep text readable and controls usable when layout changes.
- Labels, contrast, focus, hit targets, and keyboard flow are reasonable.
- Long labels, empty data, large numbers, and validation errors do not break layout.

## Visual Direction

- Operational tools: restrained color, alignment, compact spacing, clear lists/tables, stable toolbars.
- Brand/content: distinctive media, typography, and motion that reinforce the subject.
- Editors/builders: persistent tools, selection state, reversible actions, stable canvas.
- Mobile flows: reachable primary actions, short copy, visible progress, resilient back navigation.

Avoid one-note palettes, decorative effects that reduce readability, and nested cards that hurt scanning.

## Verification

```text
Viewport:
Flow:
Edge data:
Interaction:
Issue:
Fix/risk:
```

Use one affected viewport for copy, spacing, or state-only changes. Use desktop and mobile when layout, navigation, responsiveness, or primary flows changed. Report visual checks left unrun.
