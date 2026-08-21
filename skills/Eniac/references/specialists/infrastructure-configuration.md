# Infrastructure And Configuration

Use for infrastructure-as-code, deployment configuration, policy, stateful
resources, network boundaries, secret references, or environment settings.
Local syntax success does not prove the correct target or a safe live change.

1. Identify exact account/project, environment, region, namespace, state
   backend, ownership boundary, and source of truth. Keep secrets as handles.
2. Read desired state, authorized live/drift evidence, tool/provider versions,
   dependencies, policies, and rollout/rollback convention.
3. Generate and inspect the narrowest plan/diff. Classify create, update,
   replace, delete, permission, network, data, and cost effects. A plan is
   evidence, not execution authority.
4. Protect state locking/concurrent-change rules. Do not hand-edit managed state
   or live resources outside an authorized documented recovery procedure.
5. Order dependent changes so supported app/config/data versions remain viable.
6. Define abort thresholds, rollback/forward recovery, and resources that cannot
   be recreated without loss or identity change.
7. Mutate live state only with explicit authority for the exact target. Verify
   desired/live convergence, policy, health, connectivity, integrity,
   observability, and unexpected cost/blast radius.

Protected invariant: environment identity, managed state, least privilege,
network reachability, data, and recoverability stay inside the boundary.

Proof for mutation: syntax/schema, reviewed desired-state plan, policy checks,
exact-target confirmation, and post-change health/drift. For plan/review, deliver
the inspected diff/effect map and proposed gates without an apply claim. Load
`references/safety-and-delivery.md`.
