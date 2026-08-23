# Token Economy

Freud's economic viewpoint: a finite quantity of energy, distributed across competing
demands. Context is exactly that. Everything loaded displaces something else, and the
displaced thing is usually the detail that mattered.

Load this file only for genuinely large work — big repositories, repeated compaction,
expensive tools, or long autonomous runs. For an ordinary task the rules in SKILL.md
are enough, and reading this instead of the code would be its own irony.

> **Owns** — the cost of context — the loading gate, cheap sources before expensive, naming the anchors and expanding one hop at a time, batching round trips, the evidence cache, surviving compaction, output shaping, pricing an expensive operation before running it, multilingual cost, budgets as gates.
> **Defers** — which reference a task should load → `SKILL.md#routes`; the runtime token cost of a product's own model calls → `llm-systems.md#cost-and-latency-are-design-constraints`.

## The Loading Gate

Before pulling anything into context — a file, a reference, a command's output, a web
page — answer two questions:

1. **Which decision could this change?**
2. **What signal am I expecting to see?**

If either has no answer, do not load it. This single gate accounts for most of the
savings available; everything below is refinement.

The common failure is loading for reassurance rather than for a decision: reading a file
to feel prepared, re-reading something to confirm what you already read, or opening
three references because the topic sounds serious. None of those change an action.

## Cheap Before Expensive

Ordered by cost, use the cheapest that can answer the question:

1. File and directory listings — structure, naming, size, count.
2. Manifests and lockfiles — the stack, the dependencies, the scripts already defined.
3. `rg` with a tight pattern — where a symbol is defined and who uses it.
4. Headings, signatures, or a `--` outline of a file.
5. A line range around the match.
6. The whole file — when you will edit it or its logic genuinely must be understood end
   to end.

When output is noisy or truncated, **narrow it**: a tighter pattern, a smaller range, a
lower limit, a specific path. Re-running the same broad query is the single most common
way an agent burns a context window without learning anything new.

In a repository large enough that even targeted search returns noise, the technique
changes rather than the discipline — locate the owning region first, then search inside
it. See `scale.md` for navigating a system too large to read.

## Name The Anchors, Then Expand One Hop

Searching and reading have opposite economics, and treating them as one thing is why
context fills with files nobody needed. A search is cheap and precise: `rg` across a
million lines costs a few hundred tokens and *narrows* the question. Reading is the
expensive act, and it is the one to budget.

So before opening anything:

1. **Name at most three anchors** — the file, module, or symbol most likely to carry the
   answer — each with the reason it could. If you cannot name three with reasons, the
   question is not sharp enough yet, and sharpening it is cheaper than reading around it.
2. **Expand one hop at a time, along a real edge.** The caller, the import, the route
   that reaches it, the schema it writes, the config key it reads. A hop along an edge is
   an inference; a file opened because its name sounded relevant is a guess, and a
   context filled with guesses is worse than an empty one — every irrelevant file is
   something for a later step to reason from.
3. **Re-ask the loading gate at each hop.** Which decision does this change, what signal
   do I expect. The answers get *more* specific as you get closer, not less; when they
   start getting vaguer, the trail is cold.

**Three hops with nothing found means the model is wrong, not the radius.** Widening from
there is the reading equivalent of retry-until-green. Stop and get an observation instead
— run it, trace it, print the value, bisect the history — because a wrong model is
corrected by evidence and never by more of the same material.

Two habits this rule exists to kill: pulling a directory in "for context" before knowing
what is being decided, and re-reading a file already in context to feel prepared. Neither
has ever changed an action.

## Batch Round Trips

Independent reads, searches, edits, and checks belong in one round trip. Serial calls
that could have been parallel cost latency and repeated framing overhead for no
information gain.

Sequential is required only when the next call's arguments depend on this call's result.

## The Evidence Cache

Keep one compact, replaceable working set. Replace it at phase boundaries; never let it
accumulate.

```text
Facts:      confirmed fact + where it came from
Decisions:  choice + what would falsify it
Changed:    paths touched so far
Signal:     the last observed verification result
Risk:       open risk and its owner
Next:       the single next action
```

What does *not* belong: narrative of what you did, superseded hypotheses, full logs,
full file contents, anything you have not verified, and anything already written to a
plan file. Re-read a source only when it may have changed or when exact text is needed.

## Surviving Compaction

Long work loses context. Design for that instead of being surprised by it.

- Anything that must survive goes into a durable place — a plan file, a test, a comment
  — not into conversation history.
- Prefer many small verified steps over one long unverified stretch. A compaction in the
  middle of an unverified stretch loses both the work and the reason for it.
- After a compaction, verify the world rather than trusting the summary: the branch, the
  test state, what is actually on disk.
- Carry forward only confirmed facts, the current milestone, and its proof.

## Output Shaping

Output tokens are the user's money and the user's attention, and the second is scarcer.

- Answer the question asked. Do not restate their request back to them.
- No narration of routine tool calls. Announce a phase only when it carries a decision
  or a signal.
- No unrequested tutorial, no generic best-practice lecture, no summary of a summary.
- Keep exact text only for errors, commands, paths, identifiers, and contracts —
  paraphrase everything else.
- Code blocks show the change, not the file around it.
- For L0–L1, the answer is the whole output. Section headers on a one-sentence reply are
  ceremony charged to the user.
- When something is genuinely complex, length is justified. When it is not, length reads
  as padding and buries the part that mattered.

## Expensive Operations

Full test suites, browser passes, web lookups, subagents, and repository-wide scans are
worth their cost only when the result can change the next action. Before running one,
name the branch of your plan it would eliminate.

Prefer the narrowest meaningful verification first, and widen only if it passes and the
blast radius demands more.

**Price it in one line before starting it.** For anything in that class — plus reading
past a handful of files, or restructuring a whole module — say what it costs, which
decision it settles, and the cheaper thing that would settle the same decision:

```text
Running the full suite (~4 min, wide context) to see whether the serializer change
touched the export path. Cheaper: the two export tests alone — doing that first.
```

The test that makes this real is **branching outcomes**: name what you do if it comes
back one way and what you do if it comes back the other. If both answers are the same
action, the operation is not evidence-gathering, it is reassurance, and it can be
skipped. If only one outcome is imaginable, you already believe the answer — the cheaper
move is to state the belief and let the next step falsify it.

**Do not invent precision.** "This reduces uncertainty by forty percent" is a number
nobody measured and it converts a judgment call into a fake measurement. Say which
branches survive instead.

**The loop guard.** The same expensive operation run a third time with adjusted
parameters is not a strategy — it is regression under pressure (`defenses.md`), and the
correction is to spend the next tokens on a different *kind* of evidence rather than more
of the same kind.

## Multilingual Cost

Some languages cost several times more tokens per word than English. Thai is one of them.

Reason compactly in English internally; reply naturally in the user's language. Never
translate identifiers, file paths, commands, error messages, configuration keys, or
quoted text — those must round-trip exactly, and a translated command is a broken one.
For a long non-English document, work from a compact English outline rather than
re-quoting the source repeatedly.

## Budgets Are Gates, Not Quotas

Every rule here yields to correctness. When a risky change genuinely needs a wide read or
a full suite, take it — and say in a clause why the cheap path was not enough. The
failure mode this file prevents is spending without a decision behind it, not spending.
