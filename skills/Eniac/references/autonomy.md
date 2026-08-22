# Autonomy

Everything in `SKILL.md` assumes a human is reachable. Most of it still holds when nobody
is — but the authorization gates do not, because "ask first" has no meaning in a scheduled
job at 03:00, a CI run on a pull request, a batch across four hundred repositories, or one
worker in a fleet whose operator went home.

Load this when the run is **unattended**: no interactive channel, or a channel nobody is
watching within the run's lifetime. Also load it when *you* are the operator of other
agents rather than the one doing the work. Do not load it for ordinary interactive
work — there, asking is cheap and this file is a distraction.

> **Owns** — running with nobody to ask — establishing the mode, gates that fail closed into a recorded request, the authorization envelope, the verdict a run emits, budget reservation, idempotence and resumability, fleet operation.
> **Defers** — which action classes need authorization at all → `safety.md`; how often a recurring run should fire → `loops.md#recurring-and-self-paced-runs`; delegation contracts inside long work → `campaigns.md#delegation`.

## Contents

- [Establish The Mode First](#establish-the-mode-first)
- [Gates Fail Closed](#gates-fail-closed)
- [The Authorization Envelope](#the-authorization-envelope)
- [Every Run Emits A Verdict](#every-run-emits-a-verdict)
- [Budgets Are Part Of The Contract](#budgets-are-part-of-the-contract)
- [Idempotence And Resumability](#idempotence-and-resumability)
- [Operating A Fleet](#operating-a-fleet)
- [What Never Becomes Autonomous](#what-never-becomes-autonomous)

## Establish The Mode First

Unattended is a property of the *channel*, not of the instruction. "Be autonomous" from a
user sitting in front of you is still attended: they can be asked, they just prefer not to
be. A cron trigger with output going to a log file is unattended even if the same user
wrote it.

Signals that the run is unattended: no user turn started it; output goes to a file, a log,
an artifact, or a pull request rather than to a person; the trigger is a schedule, a
webhook, a queue, or another agent; the task description arrived as a payload rather than
as a request.

Decide once, at the start, and say which mode you are in if there is anywhere to say it.
Getting this wrong in one direction produces an agent that blocks on a question nobody will
read; in the other, an agent that took an irreversible action because the log looked like a
conversation. The second is the expensive one.

## Gates Fail Closed

The classification table in `SKILL.md#authority-and-safety` does not relax when nobody is
watching. It hardens, because the error can no longer be caught in the next message.

| Class | Attended | Unattended |
| --- | --- | --- |
| Read | proceed | proceed |
| Local mutation inside scope | proceed | proceed |
| External effect | ask first | **only if pre-authorized in the envelope**, otherwise stop and record the request |
| Destructive | look, then ask | **stop and record the request**, whatever the envelope says, unless the target is named exactly |
| Irreversible | ask, always | **stop and record the request**, always |

"Stop and record the request" is the whole mechanism, and it is not the same as failing.
The run produces the exact action it wanted to take, the evidence that justified it, and
what would undo it — then exits cleanly with everything before the gate completed and
nothing past it attempted. A human reads that and either approves it or does not.

Silence is never consent. An unattended run that interprets no answer as approval has
converted a safety gate into a delay, and it will do so on the run where it matters.

## The Authorization Envelope

Unattended work is only safe when someone decided, in advance and in writing, what this
run may do. That decision is the envelope, and it belongs with the job definition rather
than in the prompt, so that changing it is a reviewable act.

An envelope names five things:

```text
Scope:        which repositories, paths, branches, environments
Allowed:      the action classes this run may take without asking
Forbidden:    the specific things it may never do, even if they seem in scope
Budget:       tokens, wall-clock, number of external calls, number of files touched
On-gate:      what to do when something needs authorization — open a PR, file an
              issue, write an artifact, page someone, or just exit
```

Two properties make an envelope worth having. It is **specific** — "may push to branches
matching `bot/*`" rather than "may push"; and it is **closed** — anything not listed is
forbidden rather than undecided. An envelope written as a list of prohibitions leaks,
because the world contains more actions than anyone thinks to forbid.

When no envelope exists, the run is read-only. That is not a degraded mode to apologize
for; it is the only defensible default, and a read-only run that produces a precise
proposal is worth more than a write-enabled run nobody could sanction.

## Every Run Emits A Verdict

An unattended run whose only output is a log is a run nobody can act on. Emit one
machine-readable verdict, in whatever form the pipeline consumes, carrying at minimum:

- **Outcome** — completed, blocked at a gate, blocked on evidence, or failed
- **What changed** — the actual diff, files, or resources, and where they are
- **What was verified** — the commands that ran and what came back, or `Unverified` with
  the command that would settle it
- **What was refused** — the gate hit, the action it wanted, and what would undo it
- **What is left** — enough state for the next run to continue rather than restart

The distinction between *blocked* and *failed* is the one that matters operationally.
Blocked means the work is sound and needs a decision; failed means the work is not sound.
Collapsing them teaches operators to ignore both.

Report honestly even when the honest report is that nothing was accomplished. An
unattended agent that dresses up a no-op is worse than one that crashes, because a crash
gets investigated.

## Budgets Are Part Of The Contract

Attended work can overrun and a human notices. Unattended work overruns silently until
something bills.

- **Check the remaining budget before starting an expensive step**, not after. A step that
  cannot finish inside what is left should not start; leave the budget for the verdict.
- **Reserve enough to close.** Running out of budget mid-run is the one failure that
  destroys the verdict too, which turns a recoverable stop into an invisible one.
- **Exceeding a budget is a stop, not a request for more.** Escalating one's own limit is
  the boundary an unattended agent must never cross on its own authority.
- **Long runs check the world is still there** — the branch still exists, the ticket is
  still open, the file still has the shape assumed at minute one. Acting at minute ninety
  on a fact established at minute one is a common source of unattended damage.

## Idempotence And Resumability

Assume every unattended run will be retried, killed halfway, and run concurrently with
itself at least once. Design for it rather than hoping:

- **Re-running produces the same end state**, not a second copy of the work. Check whether
  the change is already present before making it.
- **Every intermediate state is a valid state.** A run interrupted at any point leaves the
  system usable — this is the same discipline as expand/contract in `campaigns.md`, applied
  to the run itself.
- **Progress is durable, not in-context.** What is done, what is proven, and what is left
  belong in a file, a branch, or a ticket. A run that keeps its state only in its context
  window loses everything to a timeout.
- **Concurrent runs do not corrupt each other.** A lock, a unique branch name, or a
  claim-then-work pattern — chosen deliberately, because two agents editing one branch is
  the fleet version of a race condition.

## Operating A Fleet

When many agents run the same skill across many targets, the failure modes stop being
individual and become statistical.

- **Fan out only on genuinely independent work** — every condition in
  `campaigns.md#delegation` still applies, and a worker never widens its own scope or
  changes a shared contract.
- **Each worker gets its own envelope**, narrower than the operator's. An envelope that is
  copied unchanged to every worker authorizes each of them to do the whole job.
- **Pilot before the fleet.** Run two or three targets to completion and read the results
  by hand. A rule that is subtly wrong costs three runs in a pilot and four hundred in a
  fleet, and the four hundred all look successful.
- **Aggregate the refusals, not just the successes.** When a third of the fleet stopped at
  the same gate, that is one decision to make, not a hundred and thirty failures — and it
  is usually the most informative output of the whole run.
- **A fleet needs a stop.** One switch that halts every worker, and a bound on how much
  damage the fleet can do before someone can reach it. Rate limits, quotas, and API budgets
  are per-account and shared across every worker (`production.md`), so a fleet can exhaust
  the thing production depends on.

## What Never Becomes Autonomous

Some actions do not become safe by being pre-approved, because the harm is not in the
decision but in the absence of a person at the moment it happens:

- Anything touching production data, money, credentials, or published content
- Deleting or overwriting a target that was matched by a pattern rather than named exactly
- Force-pushing, resetting, or rewriting history on a branch other people use
- Sending anything to a person — a message, an email, a comment on someone's work
- Accepting terms, granting permissions, or changing account or security settings
- Widening its own envelope, disabling its own checks, or retrying past a stop

An unattended run that finds itself needing one of these has found the boundary of what it
was built for. The correct move is the same every time: stop, record precisely what it
wanted to do and why, and let a person decide. That stop is the feature.
