# Data And State

The shape of what gets stored, and the states a thing is allowed to be in.

Load it when the work introduces or reshapes persisted data — a table, a column, a
document, an event, a queue payload, a file format — or when it adds a state something
moves through. Do not load it for data with no reader after today: a cache, a scratch
table, a fixture, a log you will drop next week. Those carry none of the cost this file is
about, and designing them like a schema is the ceremony `SKILL.md#investment-levels` warns
against.

> **Owns** — designing the data and the state it moves through: finding the entity and its identity, state as an explicit machine rather than a bag of flags, which facts are stored and which are derived, time and history, cardinality and optionality, deletion semantics, and pushing an invariant to the strongest enforcer that can hold it.
> **Defers** — making a bad *value* unrepresentable in a type, and parsing once at the boundary → `craft.md#make-illegal-states-unrepresentable`; the number chosen for a limit, a threshold, or a size → `craft.md#every-number-carries-its-derivation`; comparing two candidate shapes and recording the choice → `lifecycle.md#design-before-building`; changing a shape that already has rows in it → `campaigns.md` for expand and contract, `safety.md` before anything irreversible; index and query shape under load → `performance.md`; volume and large-table operations → `production.md`; retention, residency, and regulated categories → `enterprise.md`; judging the structure of a system that already exists → `architecture.md`.

## Contents

- [Why Data Is Not Code](#why-data-is-not-code)
- [Find The Entity And Its Identity](#find-the-entity-and-its-identity)
- [State Is A Machine, Not A Bag Of Flags](#state-is-a-machine-not-a-bag-of-flags)
- [One Owner Per Fact](#one-owner-per-fact)
- [Time And History](#time-and-history)
- [Cardinality And Optionality](#cardinality-and-optionality)
- [Deletion](#deletion)
- [Push The Invariant Down](#push-the-invariant-down)
- [The Tells](#the-tells)

## Why Data Is Not Code

`craft.md#write-less-the-ladder` says to write less code, because every line is one
somebody reads, tests, and maintains. Data runs the other way, and the asymmetry is the
reason this file exists: the cost is not in writing it, it is in **having written it**.

A wrong function is rewritten in an afternoon by one person who can see all of its callers.
A wrong column with four million rows and six readers needs a migration, a backfill, a
compatibility window, and the agreement of everyone who selects from it — so in practice it
does not get fixed. It gets worked around, and the workarounds become the system. The
second-worst outcome is a schema nobody dares change; the worst is one that quietly means
two different things in two different years.

So the ladder inverts here: **write less code, decide more data.** Thinking done before the
first row exists is the cheapest thinking available anywhere in software, and this is the
one place where spending longer is almost always right.

How much longer is set by two questions, not by how interesting the modelling is: how many
rows will exist before anyone notices it is wrong, and who is reading it by then. A table
with one writer and no consumers is nearly free to change. One with an external API over it
is not changeable at all, only versionable.

## Find The Entity And Its Identity

Before the columns, settle what one of these things *is*, and when two of them are the
same thing. Identity is the decision that travels furthest, because every reference to the
entity repeats it, and a reference cannot be more correct than the identity it points at.

- **Prefer a key nobody outside can change.** An email, a vendor's order number, a username,
  an ISBN are all keys someone else controls, and the day one of them changes, every table
  that referenced it is wrong. Keep the identity internal and the natural key as a unique
  attribute that is allowed to change.
- **A composite natural key is a design claim**, not a shortcut: it says those fields
  together can never both change and never repeat. That is usually true until the first
  acquisition, correction, or re-import.
- **The tell that identity is wrong** is a row that gets updated to mean a different thing —
  a user row reused for a new person, a "slot" that gets reassigned. Anything referencing
  the old meaning now silently references the new one.

## State Is A Machine, Not A Bag Of Flags

This is the most productive bug generator in ordinary software, and it arrives one
reasonable column at a time.

An order with `status` text, plus `is_paid`, plus `cancelled_at`, plus `refunded` can
represent far more combinations than are legal. `status='pending'` with `refunded=true`,
`cancelled_at` set with `status='shipped'` — nothing prevents those, they are merely
undocumented, and every query that forgets one is a defect that no test is looking for.
The combinations are not edge cases; they are the arithmetic of having four fields.

**The tell is code that reads two fields to decide one thing.** The moment a condition says
`status == 'paid' and not refunded`, the real state is a function of several columns, and
the columns are no longer the state.

So name the states, then name the transitions. Per state, this checklist is worth the
sentence it costs — adapted from the state-machine checklist in the `dm-game` design
plugin, which asks it of player abilities and asks the right things:

| Property | What to settle |
| --- | --- |
| **Entry** | which states may transition into this one, and what triggers it |
| **Exit** | what ends it — an event, a timer, a person, or nothing |
| **Illegal** | the combinations the shape should refuse, and where that refusal lives |
| **Concurrent** | what happens when two actors attempt the same transition at once |
| **Retry** | whether running the transition twice is safe, and what makes it so |
| **Record** | whether anyone will later need to know it happened, and when it did |

Then the shape follows: one field holding the state, transitions enforced in the one place
they can be — a constraint, a guarded update, a single function everything goes through —
and the old flags **deleted** rather than kept for compatibility. Two representations of
one fact is the next section's problem, and keeping both is how a state machine becomes a
bag of flags again.

`Concurrent` and `Retry` are the two most often skipped, and they are the two that fail in
production rather than in review: a transition with no guard runs twice the first time a
client retries a request (`production.md`), and the second run is usually not harmless.

## One Owner Per Fact

`documentation.md` makes one-owner-per-fact the rule for docs. Data has the same rule with
higher stakes, because two copies of a fact in a store do not merely disagree — they
disagree *per row*, silently, and nothing raises an error.

- **Derived or stored?** If it can be computed from what you already have, computing it is
  the default. A stored copy is a second source of truth, and it starts drifting the first
  time anything writes one without the other — a backfill, an admin tool, a failed
  transaction, a new service.
- **Denormalize deliberately.** That means the reason, the thing that reconciles the copy,
  and the record `debt.md#name-it-when-you-create-it` already specifies. "It was faster"
  with no measurement behind it is not a reason, and `performance.md` is where that
  measurement comes from.
- **The tell** is a total that needs a nightly job to stay correct. The job is not
  maintenance; it is the schema admitting the number has two owners.

## Time And History

Ask this before the first mutable column ships, because it has no cheap answer afterwards:
**will anyone need to know what this was before?**

Retrofitting history is among the most expensive migrations there is, and not because of
the code. The code is easy. The problem is that for every row already written, the honest
answer is *unknown and unrecoverable* — so the feature ships with a hole where the past
should be, and the hole never fills.

Ranked by cost, the options are: nothing, because the current value is genuinely all anyone
will ask for; a timestamp on the row, which answers *when* and never *what* or *who*; or an
append-only record of each change, where the current row becomes a projection of it.

Choosing the cheapest on purpose is correct most of the time. Choosing it by never asking
is how an audit or billing-dispute requirement arrives a year later with no data behind it
(`enterprise.md`).

## Cardinality And Optionality

- **Nullable conflates three different facts** — not known, not applicable, and not yet. If
  more than one of those can be true for a column, that column is answering more than one
  question, and every reader has to guess which. Either split it, or store which meaning
  applies.
- **"One" is usually "one for now."** One address, one payment method, one owner, one tax
  rate. The cost of a join table that turned out unnecessary is small and local; the cost of
  promoting a column to a table after there is data and code depending on it is a migration
  plus every caller.
- **Which side holds the reference is a real decision**, not a convention: put it on the
  wrong side and the query everyone actually runs becomes a scan (`performance.md`).

## Deletion

Settle what *deleted* means before anything can be deleted, because the choice leaks into
every query written afterwards by people who were not in this conversation.

- **Hard delete** removes the row, the referential question, and the history together. It is
  the honest choice when nobody will ask what used to be there.
- **Soft delete** keeps the row and moves the cost into every future query, including the
  ones someone else writes without knowing the convention. It also quietly breaks unique
  constraints: *one active email per user* stops being expressible the moment deleted rows
  remain in the table.
- **What points at it decides more than taste.** A row other rows reference cannot simply
  vanish, so the choice is cascade, restrict, or orphan — and all three are somebody's
  problem later, which is why it belongs in the design rather than in a default.
- **Obligations outrank preference.** Some data must be removable on request and some must
  be retained for years, and which is which is not a code-reading question —
  `enterprise.md`, never your own judgment.

## Push The Invariant Down

A rule can live in a comment, a convention, one function, a type, or the store itself. That
list is in increasing order of strength, so prefer the strongest enforcer the rule can
actually reach:

```text
store constraint  →  type or constructor  →  one guarded function  →  convention  →  comment
```

`craft.md#make-illegal-states-unrepresentable` carries the type-level version of this move.
The reason it matters more for data is reach: a database constraint still holds when someone
writes a new service in a different language and never reads your code, and a comment holds
for exactly as long as people read comments.

A rule that genuinely cannot be pushed down is a rule to write a check for instead
(`test-driven.md`) — not one to leave implicit and hope for.

## The Tells

Each of these is a shape that will generate defects rather than a style preference:

- a `type`, `kind`, or `flag` column whose legal values exist only in application code
- two columns that must agree, plus a job whose purpose is making them agree
- a boolean that acquired a third meaning, usually `NULL` standing for *pending*
- `status`, plus one nullable timestamp per possible status
- a unique constraint nobody can add because the existing data already violates it
- JSON holding fields that are queried, filtered, or joined on
- an id that also carries meaning — parsed prefixes, ranges reserved per tenant, dates
- a column whose name ends in `_new`, `_v2`, or `_tmp` and has been there for a year
