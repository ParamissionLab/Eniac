# Documentation

Documentation is a deliverable, not a courtesy. It is written when someone asked for it,
or when the work changed how a person runs, extends, or trusts the thing — and not
otherwise. The most common failure here is not missing docs; it is a pile of overlapping
Markdown files that each half-own the same fact, none of which anyone believes.

Load this when documentation is the work: initializing docs for a project, auditing or
deduplicating an existing set, deciding where a fact belongs, writing a handoff someone
else continues from, or documenting an API, a feature, or an architecture. Do not load it
to add a comment or fix one line in a README.

**The permission gate comes first.** `safety.md` bars adding documentation nobody asked
for. A README a stranger can follow at handover is part of Greenfield's contract; a
`docs/` tree grown beside a bug fix is unrequested work that spends the user's review
attention. When in doubt, report the gap in `Next:` instead of filling it.

## Contents

- [Before Writing Anything](#before-writing-anything)
- [One Owner Per Fact](#one-owner-per-fact)
- [The Placement Flow](#the-placement-flow)
- [Status Labels](#status-labels)
- [The Minimal Document](#the-minimal-document)
- [Every Claim In A Doc Is A Claim](#every-claim-in-a-doc-is-a-claim)
- [Auditing An Existing Set](#auditing-an-existing-set)
- [Docs Written For Agents](#docs-written-for-agents)
- [What Not To Write](#what-not-to-write)

## Before Writing Anything

Read what exists first. Writing before reading is how a fourth authentication document
gets born, and each new copy makes the existing three less trustworthy rather than more.

1. List the docs that already exist — the root README, `docs/`, per-package READMEs, the
   agent instruction file, anything in a wiki the repository points at.
2. Read the source near the thing you are documenting. A doc that contradicts the code it
   describes is worse than no doc, because it gets believed.
3. Ask whether this information changes what a future reader or agent *does*. If it does
   not, leaving it undocumented is the correct outcome, not a lapse.

**Update before you create.** A new file is justified only when no existing file is
responsible for the fact and the fact needs an owner.

## One Owner Per Fact

Each durable fact lives in exactly one place. Everything else links to it. This is the
single rule that decides most documentation arguments, and it is worth more than any
template.

| Fact | Owner |
| --- | --- |
| Endpoint shape, request, response, error codes | the API doc |
| Schema, migrations, retention, indexes | the database doc |
| Screen behaviour, states, component contract | the frontend or feature doc |
| Environments, secrets handling, rollout, rollback | the deployment or runbook doc |
| How the pieces fit and where the boundaries are | the architecture doc |
| Why a shape was chosen and what would reverse it | an ADR or decision record |
| Install, run, test — the first ten minutes | the root README |
| Conventions an agent must follow in this repo | the agent instruction file |

Duplication is not a style problem. Two copies of the same fact drift, and once they
disagree a reader must go read the code to find out which one lied — at which point both
documents have negative value. When you find a duplicate, keep the best copy, replace the
others with a link, and say in the report which you removed.

The cost of a link is one hop. The cost of a copy is paid on every future change to that
fact, forever, by someone who does not know the copy exists.

## The Placement Flow

```text
Does a file already own this fact?
├── yes → update it in place; do not create a sibling
└── no
    ├── Is the same fact already stated across several files?
    │   └── yes → keep the best one, replace the rest with links, then update it
    ├── Will a future reader or agent act differently because of it?
    │   ├── no  → leave it undocumented, or one line in Next:
    │   └── yes → create the smallest file that has one clear responsibility
    └── Is any part uncertain?
        └── yes → write UNKNOWN and name the check that would settle it
```

Prefer few files with clear ownership over many with overlapping ones. A documentation
tree is navigated by guessing which file holds a thing, and every ambiguous file costs
every future reader a wrong guess.

## Status Labels

A handoff fails when the next person cannot tell what is finished from what merely
exists. These labels are cheap and they carry that difference:

- `Current State` — what exists right now, in observable terms
- `Implementation` — implemented, partial, planned, or unknown
- `Dependency` — the file, system, or decision this waits on
- `Done` / `Not Done` — confirmed complete versus known remaining
- `TODO` — an action someone must take, with enough detail to take it
- `UNKNOWN` — must be verified, plus how to verify it

```md
- Current State: Login form renders and posts to `/api/session`.
- Implementation: Partial — password reset is not wired.
- Dependency: `../api/auth-api.md`
- TODO: Verify the reset-token expiry against the mailer config.
- UNKNOWN: Whether sessions survive a deploy. Check `SESSION_STORE` in staging.
```

Never smooth over uncertainty to make a document read as finished. An honest `UNKNOWN`
costs one line; a confident wrong sentence costs whatever the next person builds on it.
This is the claim discipline from `findings.md`, applied to files that outlive the session.

## The Minimal Document

Start from this and delete every heading that would be empty. A section with nothing under
it teaches the reader to skim, and a skimmed document is an unread one.

```md
# Title

## Purpose
One or two sentences: what this covers and who needs it.

## Status
- Current State:
- Implementation:
- Dependency:

## <the actual content>
Whatever this file is responsible for. Short sections, concrete nouns.

## Not Done
- [ ] known remaining work

## Related
- `path/to/the/other/file.md`
```

Length is not thoroughness. Expand a section when the complexity is real — a protocol with
ten error states needs ten error states — and never to look complete.

## Every Claim In A Doc Is A Claim

Documentation inherits the reality-testing rule rather than escaping it, and it escapes
more often than code does because nothing fails when a document is wrong.

- **Every command written in a document has been run**, in the state the reader will be
  in. An install sequence that was reasoned about rather than executed is the single most
  commonly broken thing in any repository.
- **Describe what exists in the present tense, and what is planned as planned.** Writing a
  proposal in a tense that makes it sound shipped is the failure `findings.md` names, and
  a document is where that failure survives longest.
- **Do not invent details you did not verify** — default values, error codes, flag names,
  timeouts, ports. Read them, or mark them `UNKNOWN`.
- **Never write reassurance** — "this is secure", "fully tested", "production ready",
  "GDPR compliant". Those are claims about the world that a document cannot make on its
  own authority (`enterprise.md`).

## Auditing An Existing Set

The output of an audit is usually *fewer* files. Say that plainly rather than adding a
summary document on top of the pile, which is the tempting move and makes it worse.

1. **Inventory** — every doc, its apparent owner, its last meaningful change.
2. **Find the duplicates** — the same fact in more than one file. These are the expensive
   ones, so handle them first.
3. **Find the lies** — statements the code contradicts. Check the commands and the
   identifiers; that is where drift shows first.
4. **Find the orphans** — files nothing links to and nobody would think to open.
5. **Decide per file:** keep and update, merge into its owner, or delete. Deletion is a
   legitimate and badly under-used outcome — dead documentation gets read, believed, and
   acted on, which is strictly worse than absence.
6. **Report before deleting.** Removing files is a destructive action under
   `SKILL.md#authority-and-safety`: list what would go and why, then act on the answer.

## Docs Written For Agents

A repository's agent instruction file — `AGENTS.md`, `CLAUDE.md`, `.cursor/rules/`,
`.github/copilot-instructions.md`, or whatever this runtime reads — is documentation with
a different reader and a much tighter budget. It is loaded on every task, so every line in
it is paid for continuously.

Put in it only what an agent would otherwise get wrong: the build and test commands that
actually work, conventions the code follows but never states, directories that are
generated, and the traps that have already bitten someone. Architecture, tutorials, and
rationale stay in normal docs, linked rather than inlined.

When a repository carries more than one such file for different runtimes, keep one
authoritative and have the others point at it. The alternative is the duplication problem
above with an added property: each agent then reads a different version of the truth.

## What Not To Write

- Placeholder files with headings and no content. They claim ownership of a fact while
  holding none, which blocks the real document from ever being written.
- Prose that restates what the code says. The code is the source of truth for *how*; a
  document earns its place by carrying *why*, *where*, and *what breaks*.
- A changelog of your own session. What you did belongs in the commit and the report.
- Background context repeated in every file so each one can "stand alone". That is the
  duplication rule broken on purpose.
- Documentation added alongside an unrelated change because the tree looked thin.
