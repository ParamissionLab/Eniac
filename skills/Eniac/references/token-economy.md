# Token Economy

Freud's economic viewpoint: a finite quantity of energy, distributed across competing
demands. Context is exactly that. Everything loaded displaces something else, and the
displaced thing is usually the detail that mattered.

Load this file only for genuinely large work — big repositories, repeated compaction,
expensive tools, or long autonomous runs. For an ordinary task the rules in SKILL.md
are enough, and reading this instead of the code would be its own irony.

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
