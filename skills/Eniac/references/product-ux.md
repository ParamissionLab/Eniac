# Product UI/UX Reference

Use when the task affects a user-facing interface, workflow, website, app, dashboard, editor, form, game, or design system.

## Domain Fit

| Domain | Prioritize | Avoid |
| --- | --- | --- |
| SaaS, CRM, admin, analytics | scanning, comparison, repeated actions | marketing layouts, low density |
| Developer or ops | diagnosis, logs, filters, keyboard flow | decoration hiding state/errors |
| Commerce or booking | trust, visible price/options/state | vague CTAs, hidden costs |
| Content, portfolio, brand | first-viewport signal, readable narrative, real media | generic stock feel |
| Game/playful app | readable state, feedback, satisfying motion | unclear rules, slow restarts |
| Data entry/workflow | low error rate, validation, recovery, tab order | surprise navigation |

Follow the existing design system first. Improve only what blocks the requested outcome.

## Workflow Frame

Use this short frame before changing UI:

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

Prefer clearer structure, controls, labels, states, or flow over explanatory text.

## UI Surface Audit

Check only surfaces affected by the change:

- Layout: stable grid, spacing, alignment, responsive behavior, no overlap.
- Hierarchy: primary action, secondary actions, status, and destructive actions are visually distinct.
- Components: controls match semantics: button, tab, menu, filter, slider, toggle, input, link.
- State: loading, empty, error, disabled, selected, hover, focus, success, and validation states exist where relevant.
- Content: labels are concrete, numbers/units are clear, long text and empty data do not break layout.
- Accessibility: contrast, focus ring, keyboard flow, hit target, labels, and reduced-motion behavior are reasonable.
- System fit: icons, typography, colors, density, and motion match the product's purpose.

## Visual Direction

- Operational tools: restrained color, compact spacing, clear tables/lists, stable toolbars, visible filters.
- Dashboards: make comparisons easy; keep legends, units, date ranges, and empty states visible.
- Editors/builders: persistent tools, selection state, reversible actions, stable canvas.
- Forms: grouped fields, inline validation, clear required/optional state, recovery from errors.
- Mobile flows: reachable primary actions, short copy, visible progress, resilient back navigation.
- Brand/content: distinctive media and typography that reinforce the subject, not generic decoration.
- Games: readable rules/state, quick restart, feedback tied to action, performance-aware motion.

Avoid one-note palettes, nested cards that hurt scanning, decorative effects that reduce readability, and landing-page composition for operational apps.

## Implementation Bias

- Reuse existing components and design tokens before inventing new UI.
- Prefer icons for common tools and text labels for ambiguous actions.
- Keep fixed-format UI stable with explicit dimensions, aspect ratios, or grid tracks.
- Ensure button/card text fits at mobile and desktop widths.
- Do not scale font size directly with viewport width.
- Use real or generated bitmap/media assets when a visual product/site/game needs visual identity.
- For 3D or canvas work, verify nonblank render, framing, motion/interaction, and asset loading.

## Verification

Use the cheapest visual proof that can catch the risk:

```text
Viewport:
Flow:
Edge data:
Interaction:
Issue:
Fix/risk:
```

Use one affected viewport for copy, spacing, or state-only changes. Use desktop and mobile when layout, navigation, responsiveness, canvas, or primary flows changed. Report visual checks left unrun.
