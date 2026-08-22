# Adoption

[INSTALL.md](INSTALL.md) covers putting one copy on one machine. This file covers the rest:
running Eniac across a team, a company, or a fleet of unattended agents, and keeping it
current without anyone forking it.

The short version — pin a version, put your own rules in a separate file rather than
editing the skill, leave the authorization gates alone, and pilot on real work before
mandating anything.

## Contents

- [Choose the tier before the tool](#choose-the-tier-before-the-tool)
- [Pin a version](#pin-a-version)
- [Customize without forking](#customize-without-forking)
- [What is not tunable](#what-is-not-tunable)
- [Distributing it](#distributing-it)
- [Rolling out to a team](#rolling-out-to-a-team)
- [Unattended fleets](#unattended-fleets)
- [Measuring whether it worked](#measuring-whether-it-worked)
- [How adoption actually fails](#how-adoption-actually-fails)

## Choose the tier before the tool

The same behaviour ships in three shapes, and picking the wrong one costs either capability
or tokens on every task forever.

| Tier | What loads | Use when |
| --- | --- | --- |
| **Full skill** — `skills/Eniac/` | a control plane on every invocation, references only when a task earns one | the runtime has a skills directory. Always prefer this |
| **Project rule** — a generated adapter | one page of rules on every task | the runtime reads standing instruction files but has no skill loader |
| **Single field** — `adapters/eniac-compact.md` | everything, always | the runtime has one instruction box and no file system |

Mixing tiers across a company is normal and fine — the rules agree, because the adapters
are generated from one source. What is not fine is installing the compact file *and* the
full skill in the same session: the same rules arrive twice, and the second copy is paid
for on every task.

## Pin a version

`skills/Eniac/SKILL.md` carries a version in its front matter, and [CHANGELOG.md](CHANGELOG.md)
says what each release changed. Vendor a specific tag rather than tracking the default
branch, so that behaviour changes arrive when someone chose them.

The version matters most when something goes wrong. "The agent stopped asking before
deploys" is answerable if you know which version each team runs, and nearly unanswerable if
everyone pulled at a different time.

Review the changelog before bumping. Guidance changes are behaviour changes even though
nothing compiles differently, and a rule that is right for one organization can be wrong
for another.

## Customize without forking

Every organization has rules Eniac cannot know: your deploy is `make ship`, your database
migrations go through a review board, your monorepo has three build systems, this service
is frozen until the audit closes.

Those belong in **your own file at precedence level 3**, not inside the skill.
`SKILL.md#precedence` puts the repository's standing instructions above the skill, so a
house rule wins on contact without anyone editing a vendored file. Start from
[`templates/house-rules.template.md`](templates/house-rules.template.md).

Two properties make this work, and both are lost the moment someone edits the skill
directly. Updates stay a clean fast-forward, because your rules are not entangled with the
upstream text. And the difference between "what Eniac says" and "what we decided" stays
visible, which is what makes a rule reviewable a year later.

Good house rules are specific and local: the commands that actually prove something here,
the paths nobody may touch without an owner, the deploy sequence, the review requirements,
the ticket format, the frozen surfaces. Bad house rules restate the skill in your own
words — that is a second copy of a fact, and `references/documentation.md` explains what it
costs.

If a house rule turns out to be right for everyone, that is a pull request upstream, not a
permanent local patch.

## What is not tunable

Almost everything in the skill is a default an organization may override. The
authorization gates in `SKILL.md#authority-and-safety` are the exception, and they are
worth defending in a way the rest is not.

They exist so that an irreversible mistake needs two people. Tuning them down is
attractive for exactly the reason it is dangerous: the gates fire on the actions where
being wrong is unrecoverable, and those are the same actions where a confirmation feels
like friction. An organization that removes them gets a faster agent and, eventually, one
incident that no amount of speed pays for.

If a gate fires too often, the fix is a **narrower authorization envelope** — naming what
this agent may do in which scope — rather than a weaker gate. That mechanism is in
`references/autonomy.md` and it is designed for exactly this pressure.

Also leave alone: the rule that only executed output counts as evidence, and the rule that
tier-six work is reported rather than silently done. Both look like process and are
actually the two things that make an agent's output trustworthy enough to act on.

## Distributing it

Pick one and make it boring:

- **Vendored copy per repository.** Simplest, works everywhere, checked in with the code
  so a change is reviewable. Costs a copy per repository and a sync job.
- **Submodule or subtree.** One upstream, explicit version per consumer. Good when teams
  update on their own schedule.
- **Internal package or template repository.** Best when new repositories are created from
  a template — new work gets it automatically and nobody has to remember.
- **Machine-level install** for the runtimes with a user-wide skills directory. Fastest to
  try, worst to audit: nobody can tell from the repository what the agent was told.

Whatever you pick, one team owns the upstream copy and one file says which version is
current. Two half-owned copies is the state that produces "it behaves differently on my
machine", and by the time anyone notices, both have diverged.

## Rolling out to a team

1. **Pilot on real work, not demos.** Three or four genuine tasks, done by people who will
   say if it got in the way.
2. **Start with one tier and one runtime.** Adding Eniac and changing tools at the same
   time makes it impossible to attribute either result.
3. **Read the objections carefully.** "It asks too much" usually means the envelope is
   missing, not that the gates are wrong. "It is too verbose" usually means people are
   getting the closing report on trivial tasks — the skill says to skip it there, so
   something is overriding that, and it is worth finding out what.
4. **Write the house rules from what the pilot revealed**, not in advance. Rules written
   before contact tend to encode what someone assumed rather than what actually tripped.
5. **Then make it default** for new repositories, and let existing ones adopt on their own
   schedule.

A mandate before a pilot produces compliance without belief, and the first time the skill
is inconvenient it gets silently deleted from one repository, then another.

## Unattended fleets

Scheduled jobs, CI runs, queue workers, and agent fleets are a different operating regime,
and `references/autonomy.md` is the reference that covers it. Three things belong in the
job definition rather than the prompt, because changing them should be a reviewable act:

- **The authorization envelope** — scope, allowed action classes, explicit prohibitions,
  budget, and what to do when something needs authorization. Anything not listed is
  forbidden; an envelope written as a list of prohibitions leaks.
- **The stop.** One switch that halts every worker, and a bound on damage before a person
  can reach it. Rate limits and quotas are shared with production.
- **Where the verdict goes.** A run that produces only a log is a run nobody acts on, and
  *blocked* must be distinguishable from *failed* or operators learn to ignore both.

Pilot two or three targets by hand before the fleet. A rule that is subtly wrong costs
three runs in a pilot and four hundred in a fleet, and the four hundred all look successful.

## Measuring whether it worked

Be honest about what is measurable. Some of this shows up in numbers and some does not.

Visible in the data: how often a change had to be reverted, how often a fix needed a second
attempt, how much of a pull request was outside what the ticket asked for, how many
unattended runs stopped at a gate versus failed. Those move, and they move in the direction
you want, and they are worth tracking before and after.

Not visible in the data, and usually the bigger effect: whether a reviewer trusts the
summary enough to skim rather than re-derive, whether an unfamiliar service is safe to hand
to someone new, whether "verified" means the same thing to everyone. Ask, rather than
inventing a metric — a proxy for trust becomes a target and stops measuring trust
(`references/judgment.md`).

Whatever you track, capture the baseline before rolling out. Otherwise the first thing
anyone asks has no answer.

## How adoption actually fails

- **Someone edits the vendored skill** to fix one thing, and updates become merges nobody
  wants to do. Six months later the copy is unmaintained and diverged.
- **The house rules grow into a second skill** — a thousand lines restating the upstream
  text in local vocabulary, paid for on every task, and slowly contradicting it.
- **The gates get relaxed after a busy week**, and the incident that follows is attributed
  to the agent rather than to the change.
- **It is installed and never piloted**, so nobody has an opinion, so nobody defends it
  when it is inconvenient.
- **Everyone runs a different version** and every behavioural question becomes
  unanswerable.
- **The compact file and the full skill are both loaded**, and the same rules are paid for
  twice on every task while everyone concludes the skill is expensive.
