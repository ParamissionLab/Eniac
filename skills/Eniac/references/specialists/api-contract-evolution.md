# API And Contract Evolution

Use for APIs, schemas, events, CLI flags/exit codes, configuration keys, file
formats, serialized values, plugin interfaces, or library exports.

1. Inventory producers, consumers, compatibility promise, versioning policy,
   defaults, errors, ordering, optionality, and unknown-field/event tolerance.
2. Identify the semantic change. Type-compatible edits can still break defaults,
   timing, pagination, error codes, ordering, or retry behavior.
3. Prefer additive evolution. For removal/breakage, declare version/deprecation
   window, migration path, telemetry, and owner.
4. Update the source of truth first: schema, interface, protocol, or config
   contract. Regenerate derived artifacts with project tooling.
5. Verify producers and representative consumers with contract, compatibility,
   serialization round-trip, or mixed-version tests as applicable.
6. Document the consumer-relevant change, migration, examples, and removal
   timeline. Never present proposed compatibility as deployed behavior.

Protected invariant: supported consumers interpret success, failure, data,
defaults, and ordering as promised.

Proof for mutation: consumer inventory, compatibility decision, and contract/
consumer tests. For review/design, trace the impact and test/migration plan; an
unrun consumer test remains planned evidence. Load `references/safety-and-delivery.md`
and apply the Architecture-First Gate when the boundary changes.
