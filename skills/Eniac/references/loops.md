# Loops

`SKILL.md#the-ego-loop` states the three properties that decide what iterative work costs —
latency, signal, and stop. This file is how to act on them.

Load it when the work is genuinely iterative and the iteration is expensive or open-ended:
a debug loop that is not converging, a build-test cycle measured in minutes, an
optimization or tuning sweep, an agent improving an artifact against a metric, or a
recurring run that has to decide its own pace. Do not load it for a task that will be
finished in one pass — most work is one pass, and treating a single edit as a loop is the
ceremony this skill exists to avoid.

> **Owns** — iterative work as a designed thing — turn/cost/signal/stop, shortening a loop instead of running it, reading convergence, the three stops, the outer evaluate-and-improve loop, recurring and self-paced runs.
> **Defers** — the innermost loop, a failing check and the code that satisfies it → `test-driven.md`; the debugging chain → `workflows.md#diagnose`; measuring and re-measuring a system → `performance.md`; unattended recurrence and its envelope → `autonomy.md`.

## Contents

- [Design The Loop First](#design-the-loop-first)
- [Shortening Beats Running](#shortening-beats-running)
- [Is It Converging](#is-it-converging)
- [The Three Stops](#the-three-stops)
- [The Outer Loop](#the-outer-loop)
- [Recurring And Self-Paced Runs](#recurring-and-self-paced-runs)
- [Loop Anti-Patterns](#loop-anti-patterns)

## Design The Loop First

Before the first turn, name four things. It costs a sentence and it is the difference
between iterating and thrashing.

```text
Turn:     what one iteration does, end to end
Cost:     what it takes — seconds, tokens, an API call, a human's attention
Signal:   what comes back, and which decision it can change
Stop:     converged / exhausted — the condition, written before turn one
```

The one people skip is **Signal**, and skipping it is what produces a loop that runs
twenty times and learns once. If you cannot say what a turn would tell you that you do not
already know, you are not ready to run it — go find the observation that discriminates
instead (`workflows.md#diagnose`).

The one that gets written vaguely is **Stop**. "Until it works" is not a stop condition
when *works* has not been defined; it is a promise to keep going. A real stop is checkable
by someone else: the test passes, the number beats the baseline by more than the variance,
three consecutive turns found nothing new.

## Shortening Beats Running

Loop latency multiplies by every iteration you have not had yet, which is why it dominates
everything else about iterative work — and why it is systematically under-invested in. The
next iteration always feels closer than the work of making iterations cheap.

The arithmetic settles it. A ten-minute loop and thirty seconds of thinking per turn gives
you five turns an hour. A thirty-second loop gives you dozens. If the problem needs fifteen
turns, the first loop costs most of a day and the second costs twenty minutes — and the
fast loop also lets you be *wrong* cheaply, which is where most of the real gain is, because
you will try the bad hypothesis first either way.

Ways a loop gets shorter, cheapest first:

- **Run less of it.** One test rather than the suite; one file rather than the build; the
  failing case rather than the fixture set. Narrowing the loop is almost always available
  and almost always skipped.
- **Make the failure reproducible on demand.** A script that fails in one command turns
  "reproduce, then investigate" into "investigate". This is the highest-value artifact in
  any hard debugging session and it is worth building before the second manual reproduction.
- **Remove the human from the turn.** A loop that waits on a person runs at human latency
  no matter how fast the machine is. Batch the questions instead of interleaving them.
- **Cache the expensive prefix.** Setup, fixtures, compiled artifacts, a warm process, a
  seeded database. Re-deriving the same state every turn is the most common hidden cost.
- **Move the check earlier.** A type error caught by the editor never enters the loop at
  all. The cheapest iteration is the one that does not happen.

When the loop cannot be shortened — a twenty-minute CI run, a nightly job, a deploy —
change strategy rather than accepting the cost: batch several hypotheses into one turn,
each independently observable, so one expensive turn discriminates between four candidates
instead of one.

## Is It Converging

Every turn should reduce uncertainty. When it stops doing that, the loop is wrong and
running it again will not fix it.

| Signal | Reading |
| --- | --- |
| The failure moves, narrows, or changes shape | converging — keep going |
| The same output twice from different inputs | the input is not reaching the code you think it is |
| Each fix produces a new error further along | converging, but the design may be the real subject |
| Two turns, same information | not converging — change the loop, not the input |
| You cannot say what the last turn taught you | not converging, and the honest report is that |

**Two failures of the same approach mean the model is wrong, not the execution.** That rule
in `SKILL.md` is the convergence check applied to debugging: after the second failure the
cheapest available action is not another attempt, it is one observation that discriminates
between what you believe and what is happening.

Track what has already been tried, including what failed. In a long loop this is the
difference between converging and circling — and it is exactly the attempt ledger
`performance.md` asks for, generalized to any loop. An idea that failed silently gets
retried by the same person an hour later.

## The Three Stops

A loop ends one of three ways, and saying which one is part of the report:

- **Converged** — the stop condition written at design time is met. Report the result.
- **Exhausted** — budget, time, or context ran out first. Report the state: what is proven,
  what is left, and what the next turn would be. An exhausted loop is resumable; an
  exhausted loop reported as finished is not.
- **Diverged** — the turns stopped producing new information. This is a finding, not a
  failure: the loop was aimed at the wrong thing, and saying so is more useful than another
  ten turns.

Reserve enough budget to stop cleanly. Running out mid-turn destroys the summary along with
the work, which turns a resumable stop into an invisible one — the same rule
`autonomy.md` applies to unattended runs, and it holds anywhere the loop can be cut off.

## The Outer Loop

Above the loop that fixes a bug sits the loop that improves the thing doing the fixing: a
prompt, a rule, a check, a template, a skill. It has the same three properties and one
extra hazard.

1. **Fix the evaluation before the artifact.** Without a way to tell better from worse, the
   loop optimizes for whatever you noticed most recently. The evaluation is the loop's
   Signal, and a loop with no signal cannot converge no matter how good the changes are.
2. **Keep a baseline.** Compare against the version you started with, not against the
   previous turn — otherwise a slow drift downhill reads as improvement at every step.
3. **Change one thing per turn**, for the same reason `performance.md` demands it: several
   changes produce one number that cannot be attributed to any of them.
4. **Beware fitting the examples.** The hazard specific to this loop is that the cases you
   iterate on are the cases you get good at. Hold some back, and prefer a change that
   explains *why* over a change that patches the failing case — a rule that generalizes
   survives inputs nobody wrote down.
5. **Stop when the changes stop being defensible**, not when the examples all pass. Passing
   everything usually means the evaluation got easier, not the artifact better.

## Recurring And Self-Paced Runs

Some loops have no natural end: a watcher, a scheduled check, a poller, an agent asked to
keep going until something happens. Two questions decide whether they are useful or just
expensive.

**How often.** Match the interval to how fast the watched thing actually changes, not to
how much you want to know. A build that takes eight minutes deserves one check at eight
minutes, not eight checks at one minute — polling faster than the world changes produces
identical observations at full price. When something will *notify* you, do not poll at all;
set a long fallback in case the notification never arrives.

**What counts as a change.** A recurring run needs to distinguish *nothing happened* from
*something happened*, and report the first briefly and the second fully. A watcher that
produces a paragraph every interval trains its reader to ignore it, and it will be ignored
on the interval that mattered.

Every recurring loop also needs the things `autonomy.md` requires of any unattended run: a
budget it cannot exceed on its own authority, a stop that a person can reach, and gates
that fail closed. A loop is the shape most likely to turn a small mistake into a repeated
one.

## Loop Anti-Patterns

- **Retry-until-green.** Re-running with small variations and no hypothesis. The tell is
  that you cannot say what the last turn ruled out.
- **Widening on failure.** The check fails, so the next turn runs more of the suite, reads
  more files, or logs everywhere. Narrow instead — a noisy turn has less signal, not more.
- **Iterating on the artifact instead of the loop.** Twenty turns against a ten-minute
  cycle when one hour would have made it thirty seconds.
- **Loops nested by accident.** A retry inside a retry inside a timeout multiplies rather
  than adds, and the total is discovered in production.
- **No ledger.** Nothing records what was tried, so failed ideas return — within the
  session, and again next quarter.
- **A stop condition invented at the end** to match whatever happened, which makes every
  loop look converged and none of them checkable.
