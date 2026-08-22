# Interface Design

`workflows.md#product-ui` carries the chain that makes an interface *correct* — real
states, hierarchy, responsiveness, accessibility, walking the actual flow. This file
carries what that chain cannot: whether the thing looks like anyone decided anything, and
whether its words help.

Load it when the appearance is part of the deliverable — a marketing page, a landing page,
a product surface someone will judge in three seconds, a redesign, or any brief containing
the words *design*, *look*, *feel*, *brand*, or *modern*. Do not load it to add a column to
an existing admin table; there the surrounding conventions already decided everything, and
matching them is the whole job.

## Contents

- [Fit The Bar To The Product](#fit-the-bar-to-the-product)
- [Ground It In The Subject](#ground-it-in-the-subject)
- [The Design Plan Comes Before The Code](#the-design-plan-comes-before-the-code)
- [The Default Look, And Why To Avoid It](#the-default-look-and-why-to-avoid-it)
- [Spend Boldness In One Place](#spend-boldness-in-one-place)
- [Motion](#motion)
- [Words Are Design Material](#words-are-design-material)
- [The Quality Floor](#the-quality-floor)
- [Critique Before Handing It Over](#critique-before-handing-it-over)
- [Implementation Traps](#implementation-traps)

## Fit The Bar To The Product

Aesthetic ambition is not a constant. An internal operations tool someone stares at for
eight hours wants density, speed, and zero surprise; a landing page seen once for nine
seconds wants a point of view. Applying the second bar to the first produces a hero section
on an admin panel, which reads as a misunderstanding of the job.

Decide which you are building before choosing anything else, and say which you decided. If
the brief pins down a direction, follow it exactly — including when it asks for something
you would not have chosen. The brief's own words outrank everything in this file.

## Ground It In The Subject

Distinctive choices come from the subject's own world — its materials, instruments,
artifacts, and vocabulary — not from a general sense of what looks good. A design for a
sailmaker and a design for a payroll API should not be interchangeable, and if they are,
neither was designed.

If the brief does not pin down what the thing actually is, pin it yourself before designing:
name one concrete subject, its audience, and the single job this page has to do, then state
your choice in one line so the user can correct it cheaply. Building against an unstated
guess is how a whole direction gets thrown away.

Build with the real content throughout. Lorem ipsum and placeholder headings hide exactly
the problems that surface later: long names, empty fields, a title that wraps to three
lines. Where copy does not exist yet, write real copy — see
[Words Are Design Material](#words-are-design-material).

## The Design Plan Comes Before The Code

Write a compact plan first, in four parts. It costs a few lines, it is cheap to change,
and it prevents the far more expensive outcome of discovering the direction is generic
after the CSS exists.

| Part | What to decide | Shape |
| --- | --- | --- |
| **Color** | the palette, chosen for this subject | 4–6 named hex values with roles |
| **Type** | a display face used with restraint, a body face, and a utility face if data or captions need one | named faces, a scale, and intentional weights and spacing |
| **Layout** | the structural idea | one sentence of prose plus an ASCII wireframe |
| **Signature** | the one element this page is remembered by | one sentence naming it and what it encodes |

Typography carries most of the personality. A page whose type is a neutral delivery vehicle
for the content will read as templated no matter how the color is chosen.

Structure should encode something true. Numbered markers, eyebrows, dividers, and section
labels are information devices — use them when the content genuinely is a sequence, a
taxonomy, or a timeline, and drop them when they are decoration wearing the costume of
structure. `01 / 02 / 03` on three things that have no order is the tell.

Then review the plan against the brief *before* writing code. For each part, ask whether
you would have produced roughly the same answer for any other brief in this category. If
yes, that part is a default rather than a decision — revise it, and say what changed and
why. Only then write the code, deriving every color and type value from the revised plan
rather than improvising at the point of use.

## The Default Look, And Why To Avoid It

Machine-generated design currently converges on a small number of looks, and they appear
regardless of subject, which is precisely what makes them read as unconsidered:

- warm cream background, high-contrast serif display, terracotta accent
- near-black background with a single acid-green or vermilion accent
- broadsheet layout with hairline rules, zero border-radius, dense columns

Each is legitimate for some brief. None is a choice when it arrives by default. Where the
brief leaves an axis free, spend that freedom on something the subject earned.

The same convergence shows up in details, and these are the ones that undermine trust in
otherwise competent work: gratuitous gradients and glows, emoji standing in for icons,
everything centered, three typefaces, decorative color that encodes nothing, animation that
delays the task, and a testimonial section for a product with no users. Restraint reads as
competence.

## Spend Boldness In One Place

Let the signature element be the one memorable thing and keep everything around it quiet.
A page with five bold ideas has none, because the eye cannot rank them and the reader has
to do the work you were supposed to do.

Match complexity to the direction: maximalist directions need elaborate execution to hold
together, minimal directions need precision in spacing, type, and detail to avoid reading
as unfinished. Elegance is executing the chosen direction well, not choosing a safe one.

Not taking a risk is itself a risk — a design nobody objects to is usually a design nobody
remembers. Take one real aesthetic risk you can justify in a sentence, and cut everything
that does not serve the brief. Before showing the work, remove one thing.

## Motion

Ask what animation does for this subject before adding any. An orchestrated moment — a
page-load sequence, one scroll-triggered reveal that lands, a hover state that confirms
what is interactive — reads as intent. Effects scattered across every element read as a
machine that had access to a transition property.

Motion has a correctness component too: honour reduced-motion preferences, never gate
information behind an animation that may not run, and never make the user wait on
decoration before they can act.

## Words Are Design Material

Copy makes a design feel templated as fast as the layout does. Bring the same intent to it
as to spacing and color.

- **Write from the user's side of the screen.** Name things by what a person controls and
  recognizes, not by how the system is built. Someone manages notifications; they do not
  manage webhook configuration.
- **Active voice, and say what happens.** "Save changes", not "Submit". Be specific rather
  than clever — specific survives translation, clever does not.
- **Keep an action's name constant through the flow.** The button that says *Publish*
  produces a toast that says *Published*. An interface's vocabulary is its signposting, and
  consistency is how people learn their way around a product.
- **Errors say what happened and what to do next**, in the interface's voice. They do not
  apologize and they are never vague. An empty state is an invitation to act, not a mood.
- **One job per element.** A label labels, an example demonstrates, and nothing quietly
  does double duty.
- **Sentence case, plain verbs, no filler**, with the register tuned to the audience.

## The Quality Floor

Build to it without announcing it. These are correctness, not polish, and they are the
first things a real user hits:

- responsive down to mobile, checked with real content lengths at real breakpoints
- visible keyboard focus and a reachable tab order
- sufficient contrast, and never color alone carrying meaning
- reduced motion respected
- every state designed: empty, loading, partial, error, too-much-data, no-permission

A screen designed only for perfect data breaks on first contact with real data, and that
break is what the user remembers about the design.

## Critique Before Handing It Over

Do the iteration in your own thinking and show the user something you have already argued
with. A half-formed direction presented for feedback transfers your work to them.

If the runtime can render and screenshot the page, look at it — a picture settles in one
step what paragraphs of reasoning cannot. If it cannot, say the visual result is
`Unverified` and name what would confirm it, rather than describing the design as though
you had seen it.

If you have somewhere durable to keep notes, record the direction you took and why. The
value compounds across passes: knowing what was already tried is the difference between
iterating and re-rolling.

## Implementation Traps

- **Selector specificity that cancels itself.** A type-based selector and an element-based
  one competing over the same padding is the most common source of "the spacing is wrong
  and nothing I change fixes it". Decide which layer owns spacing between sections and keep
  it there.
- **Values improvised at the point of use.** Ad-hoc spacing and one-off hex values chosen
  per component are what make an interface feel amateur even when each screen looks fine in
  isolation. The plan's tokens exist so this does not happen.
- **A design system adopted for one page.** Pulling in a component library to style a
  single surface imports its opinions permanently — that is a dependency decision under
  `craft.md`, not a styling one.
- **Verifying component by component.** Walk the flow the user actually came to complete,
  start to finish. Component-level checking misses precisely the problems that matter.
