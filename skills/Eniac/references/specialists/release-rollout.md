# Release And Rollout

Use for packaging, publishing, artifact promotion, deployments, migrations in a
rollout, or recovery planning. A release is a controlled transition to an
identifiable artifact, not merely a green build.

1. Identify source revision, version, artifact digest/provenance, build inputs,
   config/schema expectations, supported platforms, and exact target.
2. Confirm the validation graph: tests, static checks, build/package, artifact
   inspection, security/dependencies, migration compatibility, and smoke path.
3. Define rollout unit/stages, health signals, observation windows, stop
   thresholds, owner, and communication path proportional to blast radius.
4. Define rollback and forward recovery separately. Verify old/new app, config,
   API, and data compatibility for the declared window.
5. Deploy/publish only with explicit authority. Avoid ambiguous artifacts or
   targets across environments.
6. After authorized rollout, verify user-visible health, errors, saturation,
   data integrity, and intended capability; record partial state and residual risk.

Protected invariant: running instances and persisted state remain in a supported
compatibility window, and the artifact traces to validated source.

Proof for mutation: artifact identity, applicable gates, staged health, smoke
path, and evidenced recovery. For plan/review, deliver stages, gates, signals,
authority requirements, and recovery limits without implying build/deploy. Load
`references/safety-and-delivery.md`; use `references/delivery-proof-pipelines.md`
when creating or repairing CI/release automation.
