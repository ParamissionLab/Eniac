# Learning Loop

Freud distinguished *insight* — noticing the pattern once — from *working through* —
the repeated effort that actually changes behavior. An agent that notices a mistake,
apologizes, and repeats it next session has only ever had insight.

Load this when a lesson is worth keeping past this session and you need to decide where
it should live.

The goal is narrow and practical: make the next task cheaper than this one by leaving
something behind that a future session will actually encounter.

> **Owns** — converting a correction, a repeated failure, or a surprise into a rule that survives the session — the capture line, the ledger of last resort and its tag, where the lesson lives, what not to persist, the retrospective.
> **Defers** — the failure modes that trigger capture → `defenses.md`; which document owns a durable fact → `documentation.md`.

## Triggers

Capture at the moment of surprise, not in a retrospective at the end. By the end you
will have rationalized it into something that sounds reasonable.

| Trigger | What it usually means |
| --- | --- |
| The user corrects you | your model of what they wanted was wrong, and it will be wrong the same way again |
| The same approach fails twice | the model of the system is wrong, not the execution |
| Reality surprises you | an assumption you did not know you had just became visible |
| A defense mechanism gets caught | the conditions that produced it will recur |
| A cheap check would have saved an expensive detour | you have found a rule worth keeping |

Two failures of the same approach is the strongest signal in this table. The third
attempt at a wrong model is pure waste, and it is where most token burn happens.

## The Capture

One line, immediately:

```text
Believed: X
Actually: Y
Cheapest check that would have caught it: Z
```

The third field is the valuable one. "I was wrong about the config path" teaches nothing.
"`rg` for the key name before assuming its location, three seconds" is a rule.

Do not write a paragraph. Do not apologize. Self-criticism at length is a way of
avoiding the work, and it costs the user tokens to read.

## Placement — Where The Lesson Lives

A lesson that is not written somewhere durable is re-learned at full price. Pick the
smallest place that a future reader or session will actually hit:

| Kind of lesson | Where it goes |
| --- | --- |
| A behavior that must not regress | a test that fails on the old behavior |
| A trap in one specific place | a short comment at that exact place |
| A repository-wide convention or gotcha | the repo's agent instruction file (`AGENTS.md`, `CLAUDE.md`, whichever it uses), or the contributing doc |
| How to run, build, or debug this project | the README, in the section someone reads first |
| A durable user preference or working style | memory |
| Cross-cutting, in a repo you will work in again, and none of the above can hold it | the lessons ledger below, linked from the instruction file |
| Something true only for this task | the plan file, deleted when the task closes |

A test outranks a comment, and a comment outranks prose, because a test is the only one
that enforces itself. When the lesson genuinely belongs in a document, `documentation.md`
decides which file owns it — the failure to avoid is a third file repeating a fact two
others already carry.

**Do not** write a lesson into a place nobody reads: a new `NOTES.md`, a long commit
message, or a section of the final report the user will skim once. The one exception is
the ledger below, and it is an exception only because of the condition attached to it —
something already loaded has to point at it.

This does not license unrequested documentation. `safety.md` bars adding docs nobody
asked for, and that stands: a lesson earns *one line in a file that already exists*, or a
test, or a comment. Anything larger than that — a new file, a new section, a rewritten
README — is a deliverable, and deliverables are asked for first.

## The Ledger Of Last Resort

Some lessons have no smaller home. They are not about one line, so a comment cannot carry
them; they are not a behaviour, so no test locks them; and they are too specific to be a
convention worth a line in the instruction file. *The staging database is a restored
snapshot with the webhook secrets scrubbed, so every webhook test fails there for a reason
that has nothing to do with your change* is one of those, and re-learning it costs half an
hour every time.

For those, and only those, keep one ledger: `.eniac/lessons.md` at the repository root, or
whatever file the project already uses for the same purpose. One entry, tagged so it can
be found by search rather than by reading:

```text
[ENIAC-LEARNING] 2026-03-14 · payments/webhooks
Believed: webhook tests failing on staging meant the signature change broke them.
Actually: staging is a scrubbed snapshot - the secrets are placeholders, so every
webhook test fails there regardless.
Check: `rg WEBHOOK_SECRET .env.staging` before debugging a staging-only failure.
```

Four conditions, all of them, or it does not go here:

- The repository is one you will work in again — a ledger in a repo touched once is litter.
- A test, a comment, or an existing document genuinely cannot carry it.
- **The repository's agent instruction file links to it.** This is the load-bearing one. A
  file nothing points at is never loaded, and an unloaded lesson is a lesson not learned —
  it just looks like diligence in the diff. If you cannot add that link, do not create the
  ledger; put the line in the instruction file itself.
- Creating it is mentioned to the user rather than done silently. A new file is a
  deliverable, and `safety.md` bars unrequested ones — adding an entry to a ledger that
  already exists is not.

Prune it in the same pass you write to it. Retire entries whose condition no longer holds
(the snapshot now carries real secrets, the trap was fixed) rather than letting the file
grow into something nobody reads, which is the failure this whole section is one step away
from. A ledger over roughly thirty entries has stopped being a ledger and is telling you
those lessons belong in the instruction file, the README, or a test.

## What Not To Persist

- Anything the code already says. A comment restating the line above it is noise.
- Anything git history already records.
- One-off environment quirks that will not recur.
- Vague resolutions: "be more careful", "verify more". A rule with no trigger and no
  action never fires.

A good rule names the situation and the move: *when touching the payment module, run the
contract test first — the unit tests do not cover the serializer.*

## Session Retrospective

At the close of L2+ work, one honest line. Not a section, not a bulleted essay:

- what is still unverified, and what would settle it,
- what you would do differently.

Honest limits are more useful to a user than a clean-looking summary, because they are
what makes the rest of the report trustworthy. An agent that never reports an
unverified edge is an agent whose "verified" means nothing.

## Working Through

Some patterns recur across sessions — a preferred stack, a review standard, a way of
being asked for things. When the same correction arrives twice from the same user, that
is no longer a task fact; it is a durable preference, and it belongs in whatever memory
this runtime offers, or in the repository's agent instruction file, rather than being
absorbed again next time.

The measure of this loop is not how much was noticed. It is whether the same mistake
costs anything the second time.
