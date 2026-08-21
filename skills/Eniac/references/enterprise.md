# Enterprise Constraints

In a large organization the code is rarely the hard part. The hard part is that the
code sits inside a regime of regulation, process, shared ownership, and history — and
the constraints that regime imposes are usually invisible in the files you are reading.

The failure this file prevents is a technically excellent change that violates a rule
nobody wrote down in the repository.

Load this when the work touches regulated data, more than one tenant, another team's
code, a release process with approvals, or code nobody owns.

## Recognize The Regime

Before touching data, identify what kind it is. The category changes what is legal, not
merely what is wise.

| Signal in the code | Likely regime | What it changes |
| --- | --- | --- |
| names, emails, addresses, device or user ids, IP | personal data (GDPR-style) | lawful basis, retention limits, deletion and export rights, residency |
| diagnoses, treatment, health metrics | health data | stricter access control, audit logging of every access |
| card numbers, CVV, PAN fragments | payment data | never store or log; tokenize; the storing system is in scope for audit |
| balances, trades, ledgers | financial records | immutable audit trail, retention periods, separation of duties |
| government ids, biometrics | high-sensitivity identifiers | encryption at rest, minimal access, breach obligations |

Practical consequences that apply across most regimes:

- **Do not log it.** The most common real-world violation is sensitive data landing in
  application logs, error reports, or analytics events through a generic serializer.
  Check what your error handler actually serializes.
- **Deletion must be real.** If users can request erasure, a soft-delete flag is not
  deletion, and neither are backups, caches, search indexes, and downstream warehouses
  that nobody remembered.
- **Access is logged, minimal, and justified.** Adding a broad query capability to
  simplify a feature can quietly widen who can read what.
- **Residency constrains architecture.** Data required to stay in a region cannot be
  processed by a service in another one, including a logging or analytics vendor.

## Never Invent A Compliance Claim

You cannot determine from source code whether a system is compliant with anything. When
a regime is in play:

- Look for the actual policy — a compliance doc, a data classification, a DPA, an
  architecture decision record, a security review.
- If it does not exist or you cannot see it, **say the gap exists** rather than
  assuming either direction. "This handles what looks like health data and I could not
  find a data-handling policy" is a valuable finding.
- Never write reassurance into documentation or a report — "this is GDPR compliant",
  "this meets SOC2" — on your own authority. That sentence gets quoted later by someone
  making a decision, and it was never true.

## Multi-Tenancy

In a multi-tenant system, **tenant isolation is the highest invariant there is.** A
performance bug is an incident; a cross-tenant data leak is a breach, a disclosure
obligation, and sometimes the end of the contract.

- Every query, cache key, file path, queue message, and search index entry is scoped by
  tenant. A single unscoped query is a leak.
- The dangerous ones are the paths that feel exempt: admin tools, background jobs,
  exports, reports, migrations, and anything that iterates "all" records.
- **Test the denial, not only the permission.** A test proving tenant A sees their data
  proves nothing. The test that matters proves tenant A *cannot* see tenant B's.
- Caches are a classic leak: a key without the tenant serves one tenant's data to
  another, intermittently, which is also the hardest version to detect.

## Access And Least Privilege

- Grant the narrowest permission that works, at the narrowest scope, for the shortest
  time. Widened permissions are never narrowed again by anyone.
- **Never widen a permission to make a bug go away.** That converts a visible failure
  into an invisible exposure, and it is a common shortcut under time pressure.
- Service accounts are identities: one per service, distinct from human accounts, with
  their own limited scope.
- Secrets rotate. A design that makes rotation painful guarantees secrets that are years
  old. Read secrets from a manager at runtime rather than baking them into an image or a
  config file.
- A production credential in a development environment removes the boundary between them.

## Change Management

Large organizations constrain *when* and *how* change reaches production, and those
constraints are usually not visible in the repository.

- **Ask about freeze windows** before planning a release near a quarter end, a holiday
  period, or a major business event. Discovering a freeze after the work is staged is a
  wasted cycle.
- Approvals, tickets, and change records exist to make change reversible and
  attributable. Reference the ticket; do not route around the process because it is slow.
- **Separation of duties** is a control, not friction: in some environments the person
  who writes a change may not be the person who approves or deploys it.
- Maintenance windows exist because some operations cannot be done safely under load.
  A migration that needs one should say so early, when scheduling is still cheap.

An agent should surface these questions rather than assume the permissive answer.

## Normalization Of Deviance

A rule gets bent once under pressure, nothing bad happens, and the bent version becomes
normal. Repeat, and the safety margin is gone before anyone notices it was being spent.

In practice: a test skipped "temporarily" two years ago, an alert everyone mutes, a manual
step in a deploy that was going to be automated, a permission granted for one debugging
session, a containment labelled temporary that is now the architecture. The tell is a "we
always do it this way" that nobody can trace back to a decision.

- **Name it.** Say what the original rule protected against and what the practice actually
  is now. That gap is invisible precisely because it has become normal, so naming it is
  most of the work.
- **Do not join it silently.** One more skipped test, one more manual step, one more
  standing exception is exactly how the next person concludes it is fine.
- **Do not unilaterally remove it either.** The workaround usually exists because something
  else is broken; deleting it without the cause creates an incident. Report it with what
  fixing it would take.

This is a defense mechanism running at organizational scale — the same rationalization
described in `defenses.md`, spread across enough people that nobody owns it.

## Team Process Is A Contract

The repository's conventions encode decisions you were not present for.

- Match the branch naming, commit format, PR template, and ticket-linking convention
  already in use. Reading the last twenty commits establishes all of it in seconds.
- **Do not bypass a CI gate.** A failing required check is information. Disabling it,
  marking a test skipped, or force-merging converts a finding into a hidden problem and
  removes the protection for everyone afterwards.
- Respect required reviewers and `CODEOWNERS`. A change to code owned by another team is
  a conversation, not just a diff.
- If the process genuinely blocks correct work, say so once with the specific cost, then
  follow it.

## Legacy And Unowned Code

Much enterprise code cannot be run locally, has no tests, no documentation, and no
living author. Normal workflow assumes evidence you cannot get here, so the approach
changes:

1. **Read-only first, for longer than feels necessary.** In code you cannot execute,
   reading *is* the verification, and there is no cheaper substitute.
2. **Characterize before changing.** If any execution path exists — a staging
   environment, a replayable log, a captured request — capture the current behavior as
   the specification. Whatever it does today is what someone depends on, including the
   bugs.
3. **Assume every oddity is load-bearing** until proven otherwise. Strange code in a
   long-lived system is usually a fix for something that is no longer visible.
4. **Smallest reversible slice**, shipped and observed, before the next one. A large
   change to unowned code has no safe rollback story because nobody knows what depends
   on it.
5. **Find the real owner through history**, not the org chart: `git log` on the path
   shows who has actually touched it and when it last moved.
6. **Leave a trace.** A comment, a test, or a note about what you learned is worth more
   here than anywhere else, because the next person will start from exactly where you did.

Do not propose a rewrite as the answer to a legacy system unless the user asked for one.
The estimate is always wrong and the current system's behavior is the requirement.

## Incident Severity And Postmortem

Severity determines who is woken and how much process applies — assess it before acting,
because the answer changes the response:

| Level | Rough test |
| --- | --- |
| SEV1 | broad outage, data loss, security breach, money moving incorrectly |
| SEV2 | major feature broken, or one large customer fully blocked |
| SEV3 | degraded or partial, with a workaround |
| SEV4 | minor, no user-visible impact |

After the fact, the postmortem is **blameless** — not out of politeness, but because a
process that assigns blame stops receiving accurate information, and inaccurate incident
data is worse than none. Ask what made the failure possible and what made it hard to
detect, not who typed it.

The output is action items with owners. A postmortem that produces only a narrative has
changed nothing.

## Supply Chain

- Pin dependencies with a committed lockfile. An unpinned build is not reproducible and
  cannot be audited after the fact.
- A transitive dependency is a real dependency with real code execution rights, including
  at install time.
- Vulnerability findings need triage rather than either panic or dismissal: is the
  vulnerable path actually reachable from this application?
- Internal package registries, mirrors, and proxies exist for a reason. Do not route
  around them to install something faster.
