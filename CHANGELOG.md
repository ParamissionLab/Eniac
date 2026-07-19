# Changelog

All notable changes to this project will be documented in this file.

This project follows semantic versioning where practical.

## [Unreleased]

### Added

- Added `references/architecture-evidence.md`: a load-on-demand, evidence-first architecture pass for existing systems. It covers Scan/Focus/Full sizing, claim labels, narrow inspection, caller and blast-radius mapping, evidence-backed findings, change/documentation gates, validation, and handoff.
- Added the `Architecture-First Gate` to `SKILL.md`, so structural or non-local work is mapped before change while local work stays lean.
- Added `references/workstream-orchestration.md`: dependency-aware sequential/parallel/pipeline/recovery workflows, workstream contracts, design/dispatch/integration gates, acceptance rules, conflict containment, and durable execution context.
- Added `references/algorithm-workflow.md`: a reusable Frame/Weight/Map/Diagnose/Contain/Change/Prove/Contextualize/Decide algorithm with causal records, coverage matrix, and per-loop documentation-impact checks.

### Changed

- Strengthened Eniac's architecture and deep-audit route with explicit pass-promotion criteria, separation of facts from proposals, and traceable impact analysis.
- Upgraded L3 plan files from disposable checklists to reusable execution context when they carry system facts, decisions, workflow state, proof, and handoff value; task-only L2 plans remain disposable.
- Strengthened loop, ledger, and extended-plan references with workstream ownership, dependency waves, integration proof, and safe resume rules.
- Corrected plan cleanup semantics: plans remain stable context while active but default to delete-on-complete at every level, with explicit retention opt-in and a verified deletion gate.
- Added `scripts/finalize_plan.py` to make plan finalization deterministic, safe, idempotent, and verifiable.
- Added owner- and workspace-boundary validation plus regression tests for the plan finalizer.
- Made root-cause tracing mandatory before defect closure; emergency containment remains allowed but is labeled separately from a proven systemic correction.
- Added work weighting, coverage, causal status, and documentation impact to core delivery, architecture, workflow, ledger, and plan references.

## [1.2.1] - 2026-07-06

### Added

- Added Mode Announcement in `SKILL.md` Route section: agent states its project classification and chosen route in one line before acting, giving the user early correction opportunity.
- Added Test Coverage Guidance table in `software-engineering.md`: maps delivery shape (library, service, CLI, component, app, script) to appropriate test focus and minimum useful signal.
- Added Test Isolation rule in `software-engineering.md`: each test must own its state via fresh initialization; cross-test mutation is prohibited.
- Added Test Naming convention: describe the behavior under test as a readable assertion.
- Added Inline Documentation section in Docs And Ship: language-native doc-comment format table, module-level comment guidance, and TODO/FIXME for acknowledged limitations.
- Added Working In Existing Codebases section in Build: inspect local analogs first, scope edits to the task, adopt repository conventions, propose structural changes only when they unblock work or fix a defect.
- Added `To run:` field to final report so users get exact reproduction commands.

### Changed

- Rewrote Production Code Bar in `software-engineering.md` with original phrasing: intent-revealing identifiers, single-responsibility extraction rule, decision-justifying comments, actionable error messages, trust-boundary validation, no magic literals, and idiomatic naming per language.
- Rewrote Bug Hunt section in `software-engineering.md` as "Defect Radar" with original checklist structure (12 items organized by risk class), priority-ordered inspection path, and structured defect report format.
- Rewrote Ship Checklist in `software-engineering.md` with concise verification items, stack-generated directory exclusion guidance, and "ceremony for its own sake is waste" principle.
- Rewrote `references/systematic-thinking.md` with Deep Reasoning Protocol (6 steps), Dependency & Impact Mapping with ripple analysis and radius classification, Root Cause Analysis, Decision quality checks, Assumption tracking, and Complex Refactoring Thinking with strangler-fig progression.
- Added Refactor route in `SKILL.md` with explicit boundary lock, wave-based execution, invariant verification between waves, and prohibition on mixing refactoring with behavior changes.
- Enforced strict plan file naming: `.eniac-plan.md` with numeric-only suffixes (`-2`, `-3`). Descriptive or creative suffixes are forbidden.

## [1.2.0] - 2026-07-06

### Added

- Added `references/execution-ledger.md` for structured, restartable task state with milestone-level proof signals.
- Added `references/project-interface-contract.md` for evidence-backed README, onboarding, configuration, and operating guidance.
- Added `references/delivery-proof-pipelines.md` for deriving CI as a repository-specific proof graph instead of copying generic workflows.
- Added `references/stack-risk-matrix.md` for runtime, framework, data, concurrency, and boundary-specific failure analysis.
- Added `references/greenfield-launch-sequence.md` with staged product contracts, stack decisions, foundation gates, walking skeletons, capability slices, hardening, and clean-start release proof.
- Added `references/ci-templates-by-stack.md` with ready-to-adapt GitHub Actions YAML for Node.js, Python, Go, Rust, Zig, Ruby, Java/Gradle, .NET, and release workflows (npm, PyPI). Includes setup checklist.
- Added `references/stack-patterns-and-pitfalls.md` with concrete bad-to-good code examples for 11 stacks: TypeScript/Node.js, Python, Go, Rust, Zig, Ruby, Java/Kotlin, C#/.NET, React/Next.js, REST API patterns, and database patterns.
- Added `references/readme-template.md` with a full formatted README skeleton including centered hero, badges, feature bullets, quick start, configuration table, development setup, architecture section, and a quality checklist.
- Added `references/plan-template-extended.md` with a rich planning template for L2-L3 work: users/use cases, architecture rationale table, task breakdown with complexity tags, risk table with likelihood/impact/mitigation, constraints, open questions, and phase progress log.
- Added Zig language support across all stack-aware references: CI templates, patterns/pitfalls (5 pitfalls + good patterns), stack-risk-matrix row, commands-by-stack (discovery, test, static analysis, format), and delivery-proof-pipelines ecosystem derivation.
- Added Refactor route in `SKILL.md` with explicit boundary lock, wave-based execution for large refactors (>10 files), invariant verification after each wave, and strict rule against mixing refactoring with behavior changes.

### Changed

- Made Eniac the explicit default for code-file and software-delivery work, including simple requests.
- Strengthened software delivery with invariant selection, observable proof signals, and evidence-backed completion claims.
- Reworked disposable plans into aligned Markdown sections with separate contracts, milestones, proof, and active state fields.
- Expanded Greenfield routing across the control plane, execution ledger, engineering playbook, and README while keeping the detailed workflow conditionally loaded.
- Updated `references/software-engineering.md` discovery section: audit format now includes size estimate and tech debt fields; added explicit instruction to share audit with user before mutation for L2+ work; added pointer to extended plan template for broad work.
- Updated `references/delivery-proof-pipelines.md` with Zig ecosystem derivation row and pointer to `ci-templates-by-stack.md`.
- Updated `references/stack-risk-matrix.md` with Zig invariants/failure-radar row and pointer to `stack-patterns-and-pitfalls.md`.
- Updated `references/project-interface-contract.md` with pointer to `readme-template.md` for formatted starting skeleton.
- Updated `references/commands-by-stack.md` with Zig commands (build, test, fmt, discovery) and `build.zig`/`build.zig.zon` in manifest discovery.
- Updated `references/loop-engineering.md` with platform-specific execution model table (12 platforms), parallelizable vs sequential work rules, and sub-agent failure recovery protocol.
- Updated `SKILL.md` Communication section with structured phase announcement format for L2+ full-cycle work.
- Updated `SKILL.md` References section to list all 17 reference files with descriptions and load conditions.
- Enforced strict plan file naming: `.eniac-plan.md` with numeric-only suffixes (`.eniac-plan-2.md`, `.eniac-plan-3.md`) when collisions exist. Creative suffixes, descriptions, or task names in filenames are explicitly forbidden.
- Rewrote `references/systematic-thinking.md` from ~50 lines to ~250 lines: added Deep Reasoning Protocol (6-step framework for problems that resist straightforward decomposition), Dependency & Impact Mapping with ripple analysis and radius classification, Root Cause Analysis (5-whys for repeated failures), Decision quality checks, Assumption tracking with status, Complex Refactoring Thinking (strangler-fig pattern: understand → introduce → migrate → verify → remove), and explicit signs-you-need-to-stop checklist.

## [1.1.1] - 2026-07-05

### Changed

- Re-compressed `SKILL.md` back into a lean control plane while preserving full-cycle developer routing.
- Tightened token/credit cost guards with explicit Lean/Standard/Deep budget modes and cost checkpoints.
- Expanded `references/product-ux.md` from product UX guidance into concise Product UI/UX guidance for layout, visual hierarchy, components, states, responsive behavior, accessibility, and verification.
- Condensed `references/software-engineering.md` into a shorter full-cycle developer playbook with build, test, bug hunt, polish, docs, and ship gates.
- Updated README and contributing docs for version `1.1.1`.
- Strengthened Eniac's software engineering guidance with an explicit Deep code audit mode for whole-repo code reads, architecture mapping, and broad existing-code work.
- Added discovery commands for full repository inventories that can include ignored project files while excluding dependency, cache, build, binary, generated, and secret material.
- Raised the software engineering contract to behave more like a full-cycle senior engineer: detect project state, audit before mutation, preserve local conventions, build production-quality code, test, bug hunt, polish, document, and ship with verified handoff.

## [1.1.0] - 2026-07-04

### Added

- Added token/credit cost guards to keep simple work lean and avoid unnecessary reference loading.
- Added task scaling from trivial work to complex milestone-based execution.
- Added batch guidance for many small edits across files.
- Added Product UX reference for user-facing UI, dashboards, apps, websites, forms, and workflows.
- Added Codex installation, update, and usage examples to the README.

### Changed

- Optimized `SKILL.md` into a smaller control plane with task-specific references loaded only when needed.
- Condensed reference documents into shorter operational checklists.
- Updated documentation to include `references/product-ux.md`.

## [1.0.0] - 2026-07-03

### Added

- Initial Eniac skill release.
- Added compact Perceive, Reason, Act, Observe loop contract.
- Added token discipline guidance for concise, scoped agent work.
- Added scope lock, system map, engineering loop, loop control, and output contract sections.
- Added reference documents for loop engineering, systematic thinking, software engineering, and multilingual token discipline.
- Added project documentation: README, security policy, changelog, code of conduct, and contributing guide.

### Credits

- Created by [ParamissionLab](https://github.com/ParamissionLab).
