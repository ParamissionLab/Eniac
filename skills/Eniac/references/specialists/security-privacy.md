# Security And Privacy

Use for authentication, authorization, trust boundaries, abuse, secrets,
untrusted input, sensitive data, privacy, or supply-chain exposure. A generic
checklist cannot prove a system secure.

1. Identify protected assets, sensitive data, identities/roles, entry points,
   trust boundaries, privileged operations, and external dependencies.
2. State the threat/review question. Trace untrusted input from entry to sink,
   authorization from identity to action, and secrets from storage to use/logs.
3. Distinguish authentication, authorization, validation, encoding, encryption,
   auditability, privacy retention, and availability.
4. Prefer controls at the narrowest enforceable boundary: deny by default,
   least privilege, allowlisted parsing, parameterized access, safe output
   encoding, resource limits, and secret handles instead of values.
5. Test relevant negative paths: unauthenticated, unauthorized, malformed,
   replayed, oversized, cross-tenant, or expired. Never run intrusive or
   destructive tests outside an explicitly authorized environment.
6. Inspect changed dependencies, logs, errors, configuration, and generated
   artifacts for credential, personal-data, or supply-chain exposure.
7. Report threat scope, evidence, remediation/proposal, verification limits,
   residual risk, and unreviewed surfaces. Say `no finding in inspected scope`,
   never an unsupported `secure`.

Protected invariant: relevant confidentiality, integrity, availability,
tenant/role isolation, and privacy obligations.

Proof for mutation: scoped abuse/negative tests and boundary-level integration
evidence. For review/design, trace every finding to evidence, distinguish
confirmed from inferred risk, and make no remediation claim. Load
`references/safety-and-delivery.md` for credentials, dependencies, production,
public contracts, or external effects.
