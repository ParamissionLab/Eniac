# Findings, Questions, And Handoff

The output discipline of read-only work — review, audit, architecture assessment,
planning. These deliverables have no compiler and no test suite, so the only thing
protecting the reader is whether the claims are labelled honestly.

Load this whenever the deliverable is findings, questions, or a handoff rather than a
change.

Two opposite failures live here. One is describing a system politely and stopping,
leaving real debt unnamed. The other is flooding the output with taste-based nitpicks
to look thorough. Both waste the reader's time; the second also destroys their trust in
the first real finding.

> **Owns** — read-only deliverables — claim labels, `None identified`, the two legitimate baselines, finding shape and severity, what is not a finding, questions, artifact budget, the handoff bar.
> **Defers** — how to conduct the review → `workflows.md#review`; what to look *for* in a structure → `architecture.md`; the closing report on work you did yourself → `operating-manual.md#communication`.

## Label Every Claim

A reader must be able to tell what they can build on. Blurring these categories is what
makes a confident-sounding report unusable.

| Label | Means | Requires |
| --- | --- | --- |
| `Fact` | observed directly | the file, line, command, or output it came from |
| `Inference` | reasoned from evidence | the evidence, and what would falsify it |
| `Assumption` | unverified, stated so it can be challenged | naming it as one, before it is relied on |
| `Proposed` | does not exist yet | explicit approval before it becomes real |
| `Unknown` | not established | either a question or an explicit non-blocking note |

**Never hide uncertainty inside confident prose.** Smoothing a shaky inference into a
declarative sentence is the single most damaging habit in assessment work, because the
reader has no way to detect it and will build on it.

**Never present a proposal as an existing implementation.** "The service validates the
token" and "the service should validate the token" are different reports, and only one
of them is true.

## Write `None identified`

An omitted section reads as "nothing there" and as "not checked" at the same time, and
the reader cannot tell which. Say which.

`None identified` is a legitimate, complete result for risks, open questions, debt, or
findings. Inventing something to fill a section is worse than an empty one, because it
spends the reader's attention on nothing and dilutes whatever was real.

## Say When No Work Is Needed

A complete, valuable answer: *"No architecture pass required — this is a local change
inside one module with no boundary, data, or contract impact. That conclusion changes if
the caller list turns out to cross packages."*

Three parts: the verdict, why, and what would change it. Manufacturing a process for a
task that does not need one is the most expensive form of politeness, and it trains the
user to skim everything you produce.

## Judge Against Two Baselines Only

A finding needs a standard behind it, and only two count:

1. **The framework's documented conventions** — its lifecycle, routing, state, and data
   mechanisms, as documented, not as remembered.
2. **The project's own dominant pattern** — what this codebase actually does in most places.

Personal preference is not a baseline. Neither is a practice that is common elsewhere.

**Establish the dominant pattern before calling anything drift.** One file doing X while
nine do Y is drift. Five doing X and five doing Y is not drift — it is an open question
about which convention the owner wants, and reporting it as a defect is wrong.

## Finding Shape

Every finding carries six things. A finding missing the third or fourth is an opinion.

```text
Observed:    what is actually there
Evidence:    file:line, command output, or the traced path
Impact:      what breaks, what becomes unsafe to change, what the next
             person will get wrong — in terms of THIS system
Severity:    Critical | High | Medium | Low
Confidence:  Direct (read the source) | Inferred (from structure or naming)
Correction:  the smallest safe fix, marked Proposed
```

- **"Not best practice" is not an impact.** If you cannot say what breaks or what
  becomes harder, there is no finding.
- **Severity honestly.** Reserve `Critical` for correctness breaks, data or security
  exposure, and flows that contradict themselves. Most real debt is `Medium`. Severity
  inflation is how a report gets ignored entirely.
- **`Inferred` usually means `Verify first: yes`.** A conclusion from file names and
  directory structure is a hypothesis about the code, not a reading of it.
- **Point the correction at what stops recurrence** — a clear boundary, a single source
  of truth, the framework's own mechanism — not only at deleting the symptom. But keep
  it small: a finding is not the place to design the full fix.

## Not Findings

Leaving these out is what makes the real findings readable:

- Style or naming preference with no convention behind it.
- Working code that is merely unfamiliar to you.
- Hypothetical scale problems with no evidence of present impact.
- Generic best-practice advice detached from the inspected files.
- A pattern the codebase uses consistently and deliberately, reported as a mistake.

And the inverse rule: **never soften a supported finding to be agreeable.** Evidence is
evidence, and a finding withheld for tone is a finding the user paid for and did not get.

**Record what you considered and rejected, in one line each.** A reader cannot tell the
difference between a candidate you examined and dismissed and one you never noticed, and
they will assume the second. Three or four lines at the end — *"considered and not filed:
no `__init__.py` (works as a namespace package here); no type hints (consistent with the
rest of the repo); 'should be Postgres' (no evidence of present harm)"* — costs almost
nothing and turns silence into a decision. It also protects you from re-examining the
same candidates on the next pass.

## Questions

Separate two kinds explicitly, because they demand different things from the reader:

- **Blocking** — proceeding under any assumption would be unsafe or would waste the
  work. State the question, why it matters, and what you will do while waiting.
- **Open** — worth knowing, not worth stopping for. Record it, proceed under a labelled
  assumption.

- Ask only what actually changes something: a boundary, a responsibility, a data flow,
  an integration, a deployment or security posture, or the scope of the work.
- **Never ask the user for something the repository answers.** It is slower for both of
  you and it signals the work was not done.
- Do not convert every uncertainty into a blocking question. Most uncertainty is
  survivable if it is labelled.

## Artifact Budget

Match the output size to the system's complexity, not to how thorough you want to appear.
These are the same three depths used by the Audit route in `workflows.md#audit`: that file
decides how much to inspect, this one decides how much to write.

| Depth | Output |
| --- | --- |
| Scan | one compact note: scope, what was checked, what was skipped, facts, inferences, open questions, risks, safe next actions |
| Focus | one to three artifacts covering the scoped module, workflow, or boundary |
| Full | the complete package — justified by whole-system scope, unclear ownership, three or more interacting modules, or a genuine handoff |

Promotion needs a real trigger, evidence or an explicit request, and a statement of the
risk of staying smaller. Do not promote because the system merely looks complicated, and
never promote in order to find more findings.

## Handoff

A handoff is only useful if the next person or session can act without asking you
anything. Minimum bar:

```text
Inspected:      what was actually looked at, and what was skipped
Scope:          what this work covers
Facts:          confirmed, with sources
Inferences:     reasoned, with what would falsify them
Assumptions:    unverified, stated
Unknowns:       or None identified
Risks:          or None identified
Next:           safe next actions
Avoid:          what the next agent should NOT do until the questions are answered
```

`Avoid` is the field people leave out and the one that prevents the most damage. Knowing
that the payment retry path must not be touched until someone confirms idempotency saves
more than any amount of description.

Keep it short enough to be read at the start of a session. A handoff nobody reads has
the same value as no handoff, at higher cost.
