# Architecture Work

Understanding an existing system well enough to judge it, and saying what is wrong with
evidence behind it. Load this on the Audit route, on a Review whose subject is structure
rather than a diff, and whenever a change is about to cross a boundary you have not
mapped.

`findings.md` owns the *shape* of what you write — claim labels, severity, the six-part
finding, the artifact budget, the handoff bar. This file owns what you *look at* and in
what order. Where the two touch, `findings.md` decides how it is reported.

The failure this file exists to prevent is the polished map with nothing judged: a clean
diagram, an accurate module list, and no mention of the duplicated source of truth that
was visible in the evidence the whole time. Describing is half the work. A senior read
also says what will hurt the next change.

## Contents

- [Reuse Before Re-Mapping](#reuse-before-re-mapping)
- [Classify Before Mapping](#classify-before-mapping)
- [Where To Look](#where-to-look) — the five assessment dimensions
- [Trace Before Judging A Flow](#trace-before-judging-a-flow)
- [Graph Tools Are Evidence, Not Architecture](#graph-tools-are-evidence-not-architecture)
- [The Artifacts](#the-artifacts)
- [Diagrams](#diagrams)
- [Before You Report](#before-you-report)

## Reuse Before Re-Mapping

Look for the map before drawing one. Existing architecture overviews, ADRs, handoff
notes, current-state docs, and Mermaid sources are evidence someone already paid for.

Do not re-map a stable area unless one of three things is true: the evidence you are
seeing conflicts with what the doc claims, the current scope actually touches that
boundary, or the user asked for a full re-check. Re-deriving a correct map costs the user
real money and produces the same picture.

When a doc and the code disagree, the code wins and **the disagreement is itself a
finding** — a stale architecture doc is actively misleading the next person, which is
worse than having no doc at all.

## Classify Before Mapping

Before drawing relationships, name which areas the system actually has:

frontend · backend · database and persistence · background jobs or AI processing ·
external services · infrastructure and deployment · shared modules · tests and quality
gates · anything you cannot place

**Mark absent categories `Not observed`, not absent.** There is a real difference between
"this system has no database" and "I did not find a database", and only the second one is
usually true. Inventing a backend, a datastore, or a queue because the shape of the
project suggests one should exist is the most common way an architecture report becomes
fiction.

Anything you cannot place is a legitimate category, and worth keeping visible. An
unplaceable module is often the most interesting thing in the system.

## Where To Look

`findings.md` tells you what a finding must contain. This is where they are found. Five
dimensions, each with a different question and a different smell:

**Architecture debt** — what works today and taxes every change tomorrow. Duplicated
responsibilities, hidden coupling, a workaround that became permanent, a missing quality
gate. *Ask: what will the next person have to work around?*

**Separation of concerns** — responsibilities mixed inside something whose structure
claims to separate them. UI reading storage directly, business rules living in a request
handler, shared mutable state across a boundary. *Ask: does the code respect the layers
the directory names promise?*

**Framework convention drift** — code fighting the framework's documented mechanisms.
Bypassed routing, hand-rolled state where the framework provides it, a lifecycle used
against its contract, a reimplemented feature that already exists. *Ask: is this working
with the framework or against it?* Judge against the framework's documentation, not your
memory of it.

**Project convention drift** — code breaking the codebase's own dominant pattern in
naming, layout, error handling, or data access. *Ask: what do most files here do, and
what does this one do instead?* Establish the dominant pattern first — `findings.md`
carries the rule that decides when a difference is drift and when it is an open question
about which convention the owner wants.

**Flow conflicts** — the dimension that finds real bugs, and the one that requires actual
tracing. Two sources of truth for the same state. A circular dependency. A path nothing
can reach. A side effect crossing a module boundary silently. A flow that bypasses a
layer the system declares. *Ask: if I follow this from the entry point to the data and
back, does the story stay consistent?*

Most systems will have `None identified` in at least one dimension. Write it. An empty
dimension is information; a padded one is noise.

## Trace Before Judging A Flow

A flow conflict claimed from file names is a guess wearing a severity label. Follow the
actual path — entry point, through each hop, to the data and back — before writing it up.

Tracing one real request or job end to end teaches more than reading ten files, because
it crosses exactly the boundaries where the interesting failures live: where the layer
changes, where the error handling changes, where the data shape changes, where something
becomes asynchronous.

If you cannot complete the trace, that is the finding. Say where the path went dark and
what would light it up.

## Graph Tools Are Evidence, Not Architecture

When a codebase-intelligence tool can answer dependency and caller questions, use it — it
finds in seconds what file reading finds in an hour. Two rules keep it honest:

**When graph output and a file read disagree, the file read wins.** Graph data goes
stale, misses dynamic wiring, and resolves what it can rather than what is true.

**Graph output enters the same taxonomy as everything else.** A statically resolved
relationship is `Direct`, with the tool named as its source. A heuristic or estimated one
is `Inferred` and usually `Verify first: yes`. Nothing arrives pre-judged.

Four queries earn their cost, and each maps to a dimension rather than to a verdict:

| Query | Feeds | The trap |
| --- | --- | --- |
| dependency chain, entry point to persistence | flow conflicts, separation | a resolved edge is not a used edge |
| caller list for a module you are about to change | blast radius | dynamic callers do not appear |
| edges that bypass a declared layer | separation of concerns | confirm by reading before filing |
| fan-in outliers | *inspection targets only* | shared utilities are **supposed** to have many consumers |

Two of these are routinely misread as findings. **High fan-in is a signal to look, never
a finding by itself.** **Zero consumers is not dead code** — reflection, dependency
injection, template strings, config-declared routes, and public API surface are all
invisible to a graph. Mark it `Inferred` + `Verify first: yes` and confirm by search
before anyone deletes anything.

Divergence between your hand-built map and the graph is useful in both directions: it
means one of them is wrong, and finding out which is cheap.

## The Artifacts

`findings.md` sets how many of these you may write. This is what each one is for. Each
answers one question, and an artifact that does not answer its question is decoration.

| Artifact | Answers |
| --- | --- |
| architecture overview | what is this system, in one page |
| system boundary | what is inside, what is outside, what crosses |
| module map | what the parts are and what each owns |
| data flow | where data enters, changes shape, and lands |
| workflow map | how one real user or system flow runs end to end |
| file responsibility map | which file owns what, for navigation |
| debt register | what is wrong, with evidence and severity |
| risk register | what could go wrong, and what it would cost |
| open questions | what is unresolved, blocking or not |
| decision record | what was decided, why, and what would reverse it |
| handoff notes | what the next session needs — the bar is in `findings.md` |

Prefer updating an existing artifact over adding a new one. A second document covering
the same ground splits the truth, and the next reader finds the wrong half.

Use the project's own vocabulary throughout. Renaming its concepts to ones you prefer
makes every document you write untranslatable to the people who actually work there.

## Diagrams

A diagram earns its place when a relationship is genuinely hard to hold in prose —
cross-module dependencies, a multi-hop flow, an ordering across services. When text is
clearer, write text.

- **Mermaid is the source of truth.** An SVG is a rendering for presentation or review;
  keep the editable source, or the diagram dies at the first change.
- **One diagram, one question.** A single picture holding boundary, modules, workflow,
  and data is unreadable, which means it is not a diagram, it is a texture. Split by
  question instead: boundary, module relationships, workflow, data flow.
- **Every node must be traceable** to inspected evidence, a user-provided fact, or an
  explicit label. A component you assume exists gets marked `Assumed` or `Proposed` in
  the diagram itself — an unlabelled node reads as confirmed, and diagrams are believed
  more readily than prose.
- **Say what the diagram is for**, in one line above it. If you cannot state the question
  it answers, it does not have one.
- `flowchart` for structure and data movement, `sequenceDiagram` for order and timing,
  `classDiagram` only when relationships between domain types are the actual subject.

## Before You Report

Three questions, answered honestly, before anything goes out:

1. **Does every important claim have a source?** If not, mark it `Unverified`, mark it
   `Assumption`, or cut it. Something in between is how a guess becomes a requirement.
2. **Does the final scope match the scope you started with?** If it grew, say what was
   added and why. Undisclosed scope expansion is how an audit becomes a redesign nobody
   approved.
3. **Can the next person act without asking you anything?** Unknowns, risks, safe next
   actions, and what to avoid until the questions are answered.

**A loopback is normal, not a failure.** If mapping or validation surfaces an unknown
that would change the architecture, go back and either ask it or label the assumption
before concluding. Carrying a discovered unknown silently into a conclusion is worse than
the extra round trip.

**Mapping never authorizes redesign.** Every correction you propose is `Proposed`, sized
to the smallest safe change, and waiting for approval — no matter how obviously right it
looks from inside the map you just drew.
