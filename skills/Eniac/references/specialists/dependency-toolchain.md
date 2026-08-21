# Dependency And Toolchain Change

Use for dependency, runtime, compiler, framework, plugin, package-manager, or
lockfile changes. A concrete capability, defect, vulnerability, support window,
or compatibility need must drive the change; “latest” is not an outcome.

1. Read manifests, lockfiles, runtime constraints, build images, plugins,
   generated files, and automation. Keep the established package manager and
   pinning policy.
2. Verify target version, upgrade notes, supported runtime matrix, breaking
   changes, migration steps, and vulnerability claims from current authoritative
   sources when material.
3. Map direct and important transitive impact: imported APIs, peer/plugin/native
   compatibility, licenses, artifact size, and deployment/runtime support.
4. Keep the change minimal. Separate unrelated upgrades; group packages only
   when they must move atomically.
5. Inspect manifest/lock diffs for removals, unexpected churn, source/registry
   changes, scripts, and platform artifacts.
6. Run clean resolution/install when feasible, then build, static checks,
   focused tests, integrations, and representative startup.
7. Record downgrade/revert limits and data/generated-format changes that source
   rollback cannot undo.

Protected invariant: supported builds, runtimes, public behavior, and supply-
chain policy remain valid.

Proof for mutation: reviewed dependency diff, clean-environment signal, affected
tests, and compatibility evidence. For plan/review, provide verified target
facts, impact, proof plan, and unresolved compatibility risk. Load
`references/safety-and-delivery.md`.
