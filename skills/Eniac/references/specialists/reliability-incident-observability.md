# Reliability Incident And Observability

Use for outages, degradation, SLOs, alerts, telemetry, recovery, or operability.
During an active incident, prioritize safety, data integrity, and containment;
recovery and resolution are distinct states.

1. Establish timestamped facts: affected flows, start time, severity, current
   health, recent changes, environment, and evidence gaps. Preserve logs, traces,
   metrics, events, and artifact identifiers without exposing secrets.
2. Contain with the smallest reversible authorized action. State customer/data
   tradeoffs. Never assume permission to deploy, fail over, or change production.
3. Confirm recovery through user/system health, not process liveness. Continue
   root-cause work after restoration or hand it off as `Unverified` with owner.
4. Trace symptom, trigger, contributors, root cause, detection gap, and recovery
   gap from evidence rather than the first narrative.
5. For observability, define the decision each signal enables. Include stable
   names, units, cardinality limits, sampling, privacy, and flow correlation.
6. Alerts need actionable risk, owner, evaluation window, and recovery/runbook
   action. A dashboard nobody can act on is not a control.
7. Prove remediation with the original failure signal, a safe regression/fault
   check, health/SLO observation, and recovery readiness.

Protected invariant: containment does not enlarge impact, corrupt data, destroy
evidence, or weaken security silently.

Proof for mutation: recovery signal, causal confidence, durable guardrail,
observability coverage, and residual risk. For incident review/plan, deliver the
evidence timeline, current state, safe options, required authority, and next
checks without claiming recovery or resolution. Load `references/safety-and-delivery.md`
for production or external effects.
