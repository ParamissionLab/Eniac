# Product UI/UX Reference

Use when the task affects a user-facing interface, workflow, website, app, dashboard, editor, form, game, or design system.

Target bar: the interface should look and feel like a deliberate product decision by a senior designer — not like generated filler. Every visual choice must be explainable by the product's purpose, audience, and content.

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

## Premium Design Standard

A premium interface is defined by system discipline, not by effects. Build these foundations before styling anything:

### Type system

- Choose one primary typeface with real weight range (or a deliberate display+body pair); never stack more than two families.
- Define a modular scale (e.g., 12/14/16/20/24/32/48) and use only those sizes. Ad-hoc font sizes are the fastest tell of generated UI.
- Tighten letter-spacing slightly on large headings (`-0.01em` to `-0.03em`); never letter-space body text.
- Body line-height 1.5-1.7; headings 1.1-1.3. Line length 45-75 characters — constrain with `max-width: 65ch`, not viewport percentages.
- Use `font-variant-numeric: tabular-nums` for any column of numbers, timers, or prices.

### Spacing and layout

- One spacing scale (4 or 8 px base) applied everywhere: padding, gaps, margins. Mixed arbitrary values read as sloppy immediately.
- Whitespace is hierarchy: group related items tightly, separate groups generously. Spacing between sections must exceed spacing within them.
- Align to a real grid. Optical alignment beats mechanical alignment for icons and mixed-size text.
- Establish a consistent container width and stick to it; don't let each section pick its own.

### Color discipline

- Build from a neutral scale (8-10 steps) plus one brand accent plus semantic colors (success/warn/danger). That is the whole palette.
- Neutrals should carry the interface; accent color appears only where attention is earned: primary actions, active states, key data.
- Derive dark mode from the same tokens; never invert colors mechanically. Elevated surfaces get lighter in dark mode, not shadowed.
- Text contrast: 4.5:1 minimum for body, 3:1 for large text — verify, don't eyeball.
- Tint grays toward the brand hue slightly for warmth; pure `#808080` grays look dead.

### Depth, borders, and radius

- Pick one elevation language: borders, shadows, or surface-color shifts — lead with one, support with another; don't stack all three at full strength.
- Shadows: low opacity (4-10%), correct light direction, larger blur than offset. Hard dark shadows and glows read cheap.
- One border-radius scale (e.g., 4/8/12/16) applied by component class. Mixed radii on sibling elements look accidental.

### Motion

- Motion explains state change; it never decorates. Animate the thing that changed, nothing else.
- Durations 120-250 ms for micro-interactions, 250-400 ms for layout/page transitions; standard easing (`ease-out` for entrances, `ease-in-out` for moves).
- Prefer transform/opacity animations (compositor-friendly); avoid animating layout properties in lists.
- Respect `prefers-reduced-motion` with a real fallback, not a broken state.

### Craft details that separate premium from generic

- Real focus-visible styles that match the design language, not the browser default outline nor `outline: none`.
- Interactive states designed, not defaulted: hover, active, focus, disabled each visibly distinct and consistent.
- Empty states designed with the same care as full states: what it is, why it's empty, what to do next.
- Skeletons or stable placeholders sized to real content so loading never causes layout shift.
- Text truncation and overflow handled: long names, long emails, RTL, and multibyte text tested.
- Icons from one set, one stroke weight, one optical size — never mixed libraries or emoji standing in for icons.

## Anti-Slop Checklist

These are the recognizable fingerprints of generated UI. Reject each one unless the product genuinely calls for it:

- [ ] Purple-to-blue (or teal-to-indigo) gradient on hero, buttons, or text — the single strongest slop signal.
- [ ] Emoji used as feature icons or section markers.
- [ ] Glassmorphism/backdrop-blur cards everywhere without a reason.
- [ ] Three-column "features" grid with icon, bold title, and two lines of filler copy.
- [ ] Every element rounded-2xl with a soft shadow, floating on a pastel background.
- [ ] Generic copy: "Unlock the power of...", "Seamlessly manage...", "Take your X to the next level".
- [ ] Centered everything; no deliberate asymmetry or typographic tension anywhere.
- [ ] Placeholder-feel imagery: abstract blobs, generic undraw-style illustrations unrelated to the product.
- [ ] Dark theme that is pure black with neon accents by default, unrelated to brand.
- [ ] Identical card treatment for every content type regardless of importance.
- [ ] Animations on scroll for every section (fade-up cascade) with no informational purpose.
- [ ] Default framework aesthetics shipped unmodified (stock Tailwind blue-500 buttons, default Bootstrap look) when the task asked for design.

Passing the checklist means the design derives from the product's content and audience. When unsure what "premium" means for this product, find 2-3 best-in-class references in the same domain and extract their system (type scale, density, color restraint) — do not transplant their brand.

## Responsive Engineering

Responsive is an engineering property, not a media-query afterthought:

- **Content-out, not device-in**: design the layout around where the content breaks, then set breakpoints there. Common working set: ~640 / 768 / 1024 / 1280 px — but let content decide.
- **Fluid by default**: use `flex`, `grid` with `minmax()` and `auto-fit/auto-fill`, `clamp()` for fluid type (`clamp(1rem, 0.9rem + 0.5vw, 1.25rem)`), and intrinsic sizing before writing any media query. A layout that needs a breakpoint for every width is over-constrained.
- **Container queries** for components reused in different-width contexts (card in sidebar vs main column) when the stack supports them.
- **Mobile is a different product posture, not a shrunk desktop**: navigation collapses into an intentional pattern (not just a hamburger dumping every link), tables become cards or scoped horizontal scrollers, hover-revealed actions get a visible alternative, multi-column forms become single-column.
- **Touch targets** minimum 44x44 px with adequate gaps; primary actions reachable in the thumb zone on tall screens.
- **Never disable zoom**; keep `user-scalable` on and text at least 16 px in inputs (prevents iOS auto-zoom).
- **Safe areas and viewport units**: use `dvh` over `vh` for full-height mobile layouts; respect `env(safe-area-inset-*)` on fixed bars.
- **Test the uncomfortable widths**: 320 px, the 768-1024 tablet band, and ultra-wide. Most breakage lives between the breakpoints you designed at, not on them.
- **No horizontal scroll on the page body at any width** — scrolling belongs to designated containers (tables, code blocks, carousels) with visible affordance.
- **Images/media**: `max-width: 100%`, explicit aspect ratios to prevent layout shift, `srcset`/responsive sources when payload matters.

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
