# Comprehension

The system exists. It works. Nobody can tell you why it is the way it is — the people who
decided are gone, the ticket system was migrated twice, and the documentation describes a
version that shipped four years ago.

This is a different problem from the two next to it. `scale.md` is about a system too large
to read; `enterprise.md#legacy-and-unowned-code` is about the organizational situation of
code nobody owns. A small system can be completely opaque, and the missing thing here is
neither size nor ownership. It is **intent** — and intent is the one thing source code
never records.

Load it when you have to change or judge code whose reasons are not available: an
unfamiliar or inherited system, a module everyone avoids, code with no tests and no
comments, or anything where the honest answer to "why does it do this?" is currently a
guess. Load it also before deleting something that looks pointless. Do not load it for code
you or the current team wrote and can still explain — asking someone is faster than
everything in this file.

> **Owns** — building understanding of a system whose intent is lost: what working code does and does not prove, version history as the primary source of intent, collecting anomalies before resolving them, when it is safe to remove something nobody can explain, characterization tests as a comprehension instrument rather than a safety net, and the test for whether you actually understand it.
> **Defers** — navigating a system too large to read → `scale.md`; assessing and mapping one → `architecture.md`; the organizational reality of unowned code → `enterprise.md#legacy-and-unowned-code`; the chain for a specific defect → `workflows.md#diagnose`; what a test should assert once you are writing them for real → `craft.md`.

## Contents

- [Working Code Is Evidence, Not Documentation](#working-code-is-evidence-not-documentation)
- [History Is The Primary Source](#history-is-the-primary-source)
- [Collect The Weirdness Before Explaining Any Of It](#collect-the-weirdness-before-explaining-any-of-it)
- [Removing What Nobody Can Explain](#removing-what-nobody-can-explain)
- [Characterization Tests Are A Comprehension Tool](#characterization-tests-are-a-comprehension-tool)
- [Knowing You Have Understood It](#knowing-you-have-understood-it)

## Working Code Is Evidence, Not Documentation

Running code tells you *what happens*. It never tells you *why*, and the gap between those
two produces both of the failures here, from the same missing information:

- **Assuming there was no reason.** The odd branch is treated as sloppiness and removed,
  and three weeks later the edge case it existed for comes back — usually in production,
  usually to someone who has no idea the branch ever existed.
- **Assuming the reason still applies.** The workaround for a bug fixed in 2019 is
  preserved, worked around, and eventually built upon, until the accident is load-bearing
  and the cost of the original bug is being paid forever.

Both are guesses presented as decisions. The work in this file is turning them into
findings — and where that fails, into *labelled* guesses, which is a legitimate outcome and
a much better one than either failure above.

## History Is The Primary Source

Version control is the most under-used tool available for this, and it is usually the only
surviving record of intent. The commit that introduced a strange line often explains it in
one sentence written by someone who understood it completely at the time.

```bash
git log -S'the_odd_constant' --oneline -- path/to/file   # when did this value appear
git log --follow -p -- path/to/file                      # how this file became this
git log -L 40,60:path/to/file                            # the history of one region
git blame -w -C -C path/to/file                          # ignoring whitespace and moves
```

`blame` alone is the shallow version and gives the *last* person to touch a line, which
after any reformatting is nobody useful. `-w -C -C` sees through whitespace changes and code
movement, and the point is not the name — it is the **commit message and whatever it links
to**. Follow it to the ticket, the pull request, the review discussion.

Rank the sources by how much they actually constrain:

| Source | What it gives you |
| --- | --- |
| The commit message and its linked ticket or PR | the reason, in the words of someone who had it |
| A test that pins the behaviour | proof somebody intended it, even without a why |
| A comment at the site | a reason, possibly stale — check it against the code around it |
| The shape of the code | a hypothesis, nothing more |
| Someone's recollection | a hypothesis, and one that will be stated confidently |

**The commit's character matters as much as its message.** A line introduced by a commit
called *"hotfix: payments failing for AU customers"* is load-bearing and you have just found
out why. The same line introduced inside a nine-hundred-file reformat is probably an
accident of the tooling. That distinction costs one command and changes what you do next.

Where history is unavailable — a squashed import, a vendored directory, a repository that
began as a copy — say so explicitly. "No history before the initial commit" is a real
constraint on every conclusion after it, and it changes the standard of proof for removal.

## Collect The Weirdness Before Explaining Any Of It

Read for anomalies first and resolve them second. Two passes, deliberately separated:

1. **List everything that looks wrong** — the redundant check, the magic number, the
   sleep, the field that is always null, the parameter nobody passes, the branch that
   appears unreachable, the comment contradicting the code beneath it.
2. **Then find out why each one is there**, one at a time, using history.

Doing this in one pass is the trap. The first anomaly you explain becomes the frame for
every other one, and a system with two unrelated historical scars gets described as having
one — the same anchoring failure `workflows.md#diagnose` guards against by demanding
competing hypotheses before investigating any of them.

**Weirdness is compressed information.** Ordinary code teaches you almost nothing; someone
paid for the weird line, usually with an incident. The list of anomalies and their reasons
*is* the understanding, and it is the part worth writing down, because it is exactly what
the next reader will otherwise re-derive at full price.

Expect a third category alongside "still needed" and "obsolete": the anomaly nobody can
explain and nothing depends on. Do not force it into one of the other two. Record it as
unresolved with what you tried.

## Removing What Nobody Can Explain

Chesterton's fence — do not remove what you do not understand the reason for. Taken
literally it is paralysing, because in an old system the reason is frequently unrecoverable
at any price, and "never touch anything unexplained" means the code can only ever grow.

The workable version turns on a distinction: **you do not have to agree with the reason,
you have to know what it was.** So the search is bounded, and it is the search from the
section above — history, tests, the ticket, one person who might remember. When it comes up
empty, that is not permission and it is not a veto. It changes the category of the change:

**Removal stops being cleanup and becomes a change that needs proof.**

The move that resolves most of these cheaply is to **make the fence testable**. Write a
check that asserts what you *believe* the suspicious code is doing. Then:

- The check fails — you were wrong about what it does, and you have just learned the thing
  you were missing. Do not remove it.
- The check passes and is non-trivial — you now have the behaviour pinned, and removal is a
  change you can actually verify rather than hope about.
- The check is impossible to write without asserting nothing — the code has no observable
  effect on anything you can reach, which is itself the strongest available evidence, and
  worth saying in exactly those terms rather than as "it looks dead".

If it must go out unexplained, ship it where it is reversible on its own: separate commit,
behind a flag if the system supports one, and named in the report as an unexplained removal
with what you looked at. That way the incident three weeks later takes ten minutes to
diagnose instead of three days.

## Characterization Tests Are A Comprehension Tool

They are usually described as a safety net for refactoring. That undersells them: writing
one is the most reliable way to find out how much you actually understand.

The mechanism is simple and slightly uncomfortable. Before running anything, **write down
what you predict the output will be**. Then run it. Every place your prediction was wrong is
a place your model of the system was wrong, located precisely, and cheaper than any amount
of further reading. **The failed prediction is the finding.**

- Pin what the code *currently does*, not what it should do. A characterization test
  asserting correct behaviour on code that behaves incorrectly will not go green, and now
  you have two problems.
- Where the output is too large or too tangled to predict — a rendered document, a report,
  a serialized structure — capture it as a golden master and diff against it. Understanding
  can come later; the safety comes now.
- **Bugs pinned by these tests stay pinned, and get labelled.** A characterization test is
  a description, not an endorsement. Say in the test name or a comment that the behaviour
  is being preserved rather than approved, or the next reader will treat it as a
  requirement.

This is also the cheapest way to make an unowned system safe to work in at all, which is
why `enterprise.md#legacy-and-unowned-code` reaches for it as the first move.

## Knowing You Have Understood It

Reading until it feels familiar is not a stopping condition — familiarity arrives well
before understanding and feels identical from the inside. Two tests, and both are cheap:

**Predict, then run.** Name a specific input and say what will happen, in enough detail to
be wrong. Then execute it. A model you have never tested against the running system is a
story, however coherent, and coherence is exactly what a wrong model has plenty of.

**Explain the why, not the what.** Can you say why the system is like this, to someone who
was not there — which parts are deliberate, which are historical scars, and which are
genuinely arbitrary? Describing what it does is the easy half and it is what everyone
produces. The why is the half that rots fastest, is most expensive to recover, and is the
whole reason this file exists.

Then write it down while you still have it. The anomaly list with reasons attached, the
invariants nobody stated, and the things that look wrong but are not — those go somewhere
durable (`scale.md#put-the-map-somewhere-durable`, `documentation.md`), because the next
person to arrive is quite likely to be you, with none of this in context.
