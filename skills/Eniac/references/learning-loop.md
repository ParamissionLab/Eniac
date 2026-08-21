# Learning Loop

Freud distinguished *insight* — noticing the pattern once — from *working through* —
the repeated effort that actually changes behavior. An agent that notices a mistake,
apologizes, and repeats it next session has only ever had insight.

The goal is narrow and practical: make the next task cheaper than this one by leaving
something behind that a future session will actually encounter.

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
| A repository-wide convention or gotcha | `CLAUDE.md`, or the contributing doc |
| How to run, build, or debug this project | the README, in the section someone reads first |
| A durable user preference or working style | memory |
| Something true only for this task | the plan file, deleted when the task closes |

A test outranks a comment, and a comment outranks prose, because a test is the only one
that enforces itself.

**Do not** write a lesson into a place nobody reads: a new `NOTES.md`, a long commit
message, or a section of the final report the user will skim once. And do not create
documentation the user did not ask for — one line in an existing file beats a new file
every time.

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
is no longer a task fact; it is a durable preference, and it belongs in memory or in
`CLAUDE.md` rather than being absorbed again next time.

The measure of this loop is not how much was noticed. It is whether the same mistake
costs anything the second time.
