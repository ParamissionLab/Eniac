# Id / Ego / Superego Decision Triad

Use for an L2+ decision where meaningful alternatives compete, especially
architecture, defect strategy, dependency choice, scope negotiation, risky
delivery, or a problem whose fastest answer may conflict with evidence or duty.
Do not load for a routine edit with one reversible, easily verified path.

This is an engineering metaphor inspired by Freud's structural model, not a
claim that an agent has a psyche and not a scientifically validated model of
software reasoning. Keep private reasoning private. Expose only the compact
decision record, evidence, conflict, and verification signal useful to the user.

## Roles

| Voice | Engineering function | Required contribution | Cannot authorize |
| --- | --- | --- | --- |
| Id | outcome drive | Surface the boldest, fastest, simplest, or highest-upside viable option | scope expansion, unsafe action, or an unsupported claim |
| Superego | duty and standards | Test options against user intent, authority, safety, security, quality, compatibility, maintainability, and downstream impact | perfectionism, moralizing, or requirements the task does not own |
| Ego | reality mediator | Reconcile drive and duty with inspected facts, constraints, reversibility, cost, and proof; choose or escalate | inventing consensus where evidence is tied or authority is missing |

The Id creates productive pressure, the Superego creates protective pressure,
and the Ego owns the decision. None is a separate agent unless delegation is
already justified by the workstream protocol.

## Compact Cycle

```text
1. Frame      -> decision, invariant, authority, deadline, and falsifier
2. Id         -> strongest upside option and the need it satisfies
3. Superego   -> non-negotiable duties and the harm or debt to prevent
4. Ego        -> evidence, constraints, options, reversibility, and verification
5. Synthesize -> choose, run the cheapest discriminating check, or request authority
6. Observe    -> accept, revise, or stop when the falsifier appears
```

Do not let the labels replace analysis. Each role must add a distinct constraint
or option. If all three say the same thing, collapse to the normal direct path.

## Decision Record

Keep this to one line per field unless the decision is hard to reverse:

```text
Decision:
Id / drive: <desired upside or fastest useful path>
Superego / duty: <protected obligation or unacceptable harm>
Ego / reality: <decisive evidence, constraint, and tradeoff>
Choice: <selected option or approval request>
Falsifier: <signal and checkpoint that would reverse the choice>
```

For a reversible choice with a cheap check, use only `Choice`, `Because`, and
`Falsifier`. For a contract-changing, destructive, external, or otherwise
hard-to-reverse choice, preserve the full record in the execution context.

## Conflict Rules

- **Drive exceeds authority:** keep the option as a proposal; ask before acting.
- **Duty exceeds evidence:** identify the specific contract, risk, or instruction;
  discard generic perfection standards.
- **Reality is uncertain:** run the single cheapest check that can separate the
  leading options. Do not resolve a tie by familiarity.
- **Fast path is only containment:** label it as containment and keep diagnosis
  or permanent correction separate.
- **Safe path cannot meet the requested outcome:** state the conflict and ask for
  the decision instead of silently weakening the goal.
- **New evidence contradicts the choice:** re-run synthesis; do not defend the old
  decision with compensating patches.

## Dominance Failure Modes

| Dominant voice | Typical failure | Correction |
| --- | --- | --- |
| Id | speculative features, reckless speed, broad rewrite, premature completion | restore scope, authority, and falsifiable proof |
| Superego | paralysis, gold-plating, excessive gates, impossible quality bar | retain only task-owned obligations and risk-matched proof |
| Ego | timid compromise, local optimization, treating current constraints as permanent | re-surface the highest-value viable option and its reversible experiment |

The healthy result is not always compromise. Evidence may support the bold
option, duty may veto every unsafe option, or missing authority may require a
question. The goal is a reality-tested decision with an observable failure
signal, not agreement among labels.

## Problem-Solving Placement

Apply the triad at the few points where it can change the outcome:

- after framing an ambiguous or high-impact problem;
- before selecting among materially different solution paths;
- when containment, root-cause correction, and systemic prevention compete;
- when review feedback conflicts with repository evidence or user intent;
- before widening scope, introducing a dependency, breaking a contract, or
  taking an external/irreversible action;
- after a failed checkpoint changes the evidence.

Then return to Eniac's normal `Frame -> Weight -> Map -> Diagnose -> Change ->
Prove` workflow. The triad selects and constrains an action; it does not replace
implementation, tests, or observed proof.
