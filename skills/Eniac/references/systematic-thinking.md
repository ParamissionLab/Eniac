# Systematic Thinking Reference

Use when a direct fix may miss dependencies, hidden assumptions, tradeoffs, or feedback effects. Also use for any task requiring deep reasoning: complex architecture decisions, multi-system interactions, unfamiliar domains, or when the first two attempts failed and you need to think differently.

## Contents

- [Frame](#frame)
- [Decompose](#decompose)
- [Deep reasoning protocol](#deep-reasoning-protocol)
- [Dependency and impact mapping](#dependency-and-impact-mapping)
- [Pattern selection](#pattern)
- [Decision framework](#decision)
- [Assumptions and drift](#assumptions-and-drift)
- [Complex refactoring thinking](#complex-refactoring-thinking)

## Frame

Keep only facts that affect decisions:

```text
Objective:
Boundary:
Actors/components:
Inputs/outputs:
State owner:
Constraints:
Dependencies:
Invariants:
Assumptions:
Failure modes:
Signal:
```

## Decompose

Break work by stable boundaries:

- user-visible behavior
- data flow
- control flow
- interfaces/contracts
- state ownership
- side effects
- verification path

Each unit needs an output and verification signal. Do not decompose by file count or every possible concern.

### Decomposition depth

Choose depth deliberately:

| Complexity | Decomposition | Verification |
|-----------|---------------|--------------|
| Simple (1-2 files, clear path) | One level: task → subtasks | One check at the end |
| Medium (3-10 files, some unknowns) | Two levels: task → groups → subtasks | Check per group |
| Complex (>10 files, cross-cutting, unknowns) | Three levels: task → phases → groups → subtasks | Check per group, integration check per phase |
| Deeply complex (architecture, multi-system, novel) | Use deep reasoning protocol below first | Check per decision boundary |

## Deep Reasoning Protocol

Use this when the problem resists straightforward decomposition — when you find yourself uncertain about the right approach, when the system interactions are non-obvious, or when previous attempts failed.

### Step 1: Slow down and frame the actual problem

Before solving, ensure you understand what you're actually solving:

```text
What is being asked (literal):
What is actually needed (intent):
Why is this hard (the real difficulty):
What would a wrong solution look like:
What would a right solution look like:
```

The gap between "literal ask" and "actual need" is where most failures happen. A request to "refactor the auth module" might actually need "make auth testable without breaking the session contract."

### Step 2: Map the forces

Every complex problem has competing forces. Name them:

```text
Forces in tension:
  - <force A> vs <force B> (e.g., performance vs readability)
  - <force C> vs <force D> (e.g., backward compatibility vs clean design)

Which force wins and why:
  - <reasoning based on context, constraints, and user intent>

Non-negotiable constraints:
  - <things that cannot be traded away>
```

### Step 3: Think in layers, not steps

Complex problems have layers of concern. Work from the inside out:

```text
Core invariant (what must never break):
Inner layer (data/state that the invariant protects):
Middle layer (logic that operates on the inner layer):
Outer layer (interfaces/entry points that expose the middle layer):
Environment layer (deployment, configuration, external systems):
```

Changes propagate outward. Start by understanding the core invariant, then trace outward to find what your change actually touches.

### Step 4: Generate alternatives

Do not commit to the first approach. Generate at least 2-3 meaningfully different approaches:

```text
Approach A: <description>
  - Works because: <reasoning>
  - Fails when: <conditions>
  - Cost: <effort, risk, reversibility>

Approach B: <description>
  - Works because: <reasoning>
  - Fails when: <conditions>
  - Cost: <effort, risk, reversibility>

Approach C: <description>
  - Works because: <reasoning>
  - Fails when: <conditions>
  - Cost: <effort, risk, reversibility>
```

If all approaches look similar, you haven't explored the space. Ask: "What would someone who disagrees with all of these suggest?"

### Step 5: Pre-mortem

Before implementing the chosen approach, imagine it failed:

```text
If this approach fails, the most likely reason is:
The second most likely reason is:
The failure I'd be most embarrassed by is:
To detect failure early, I should check:
The cheapest way to de-risk is:
```

### Step 6: Commit with checkpoints

Choose the approach, but set explicit checkpoints where you'll re-evaluate:

```text
Chosen approach:
Reason:
Checkpoint 1: After <milestone>, verify <signal>. If <bad signal>, switch to <fallback>.
Checkpoint 2: After <milestone>, verify <signal>. If <bad signal>, stop and report.
```

## Dependency And Impact Mapping

Use when a change can propagate in non-obvious ways:

### Direct dependency map

```text
Changed: <file/module/function>
Direct callers: <what calls this>
Direct dependencies: <what this calls>
Shared state: <what mutable state this reads/writes>
Shared contracts: <APIs, schemas, events, config keys this defines>
```

### Ripple analysis

For each item in "Direct callers" and "Shared contracts":

```text
If I change <X>, then:
  → <Y> will break because <reason>
  → <Z> might break if <condition>
  → <W> is safe because <reason>
```

### Impact radius classification

| Radius | Description | Verification needed |
|--------|-------------|-------------------|
| Local | Only the changed file/function | Unit test or type check |
| Module | Same package/module boundary | Module tests + type check |
| Interface | Crosses a public contract | Integration test + consumer check |
| System | Crosses service/process boundary | End-to-end or deployment check |
| External | Affects users, other teams, or data | Approval + staged rollout |

Stop expanding the radius when you reach code that does not depend on what you changed.

## Pattern

Pick one active pattern:

| Situation | Pattern | Proof |
| --- | --- | --- |
| Small surface | Direct path | One command/file/result |
| Unknown cause | Hypothesis tree | Branch ruled in/out |
| Many components | Dependency path | Upstream/downstream verified |
| Public contract | Contract map | Caller/schema/API preserved |
| Many options | Decision matrix | Value/risk/cost compared |
| Cross-cutting concern | Layer analysis | Each layer verified independently |
| Novel/unfamiliar domain | First principles + research | Concepts verified against sources |
| Repeated failure | Root cause analysis | Cause addressed, not symptoms |

Switch patterns only when evidence stops fitting.

### Root cause analysis (for repeated failures)

When the same problem keeps recurring or fixes don't stick:

```text
Symptom (what you observe):
Immediate cause (what directly triggers it):
Contributing causes (what makes it possible):
Root cause (why it keeps happening):
Systemic fix (what prevents recurrence):
```

Ask "why?" at least 3 times:
- Why did the build fail? → Because the import path is wrong.
- Why is the import path wrong? → Because the module was moved but references weren't updated.
- Why weren't references updated? → Because there's no automated check for stale imports.

Fix at the deepest level that's within scope.

## Decision

```text
Option:
Expected value:
Risk:
Reversibility:
Token/context cost:
Verification cost:
Decision:
```

Prefer reversible, locally verifiable options that match existing patterns. Drop options needing broad rewrites, new dependencies, unverifiable assumptions, or unrequested scope expansion.

### Decision quality checks

Before committing to a decision on complex work:

- [ ] Can I explain this decision to someone unfamiliar with the context in 2 sentences?
- [ ] If I'm wrong, how will I find out? (What signal will I see?)
- [ ] What's the cheapest way to test this assumption before going all-in?
- [ ] Am I choosing this because it's correct, or because it's familiar?
- [ ] Does this decision close off future options that might be needed?

## Assumptions And Drift

- Verify cheap assumptions immediately.
- Convert expensive assumptions into explicit risks.
- Ask only when an assumption is high-impact and cannot be verified locally.
- Before acting, check: objective, boundary, invariant, verification, smaller reversible step.
- Compress long reasoning to: decision, because, risk, verify.

### Assumption tracking for complex work

```text
Assumption: <what you believe to be true>
Basis: <why you believe it — evidence, inference, or guess>
Impact if wrong: <what breaks>
Verification: <how to check> or <cannot verify — treating as risk>
Status: verified | falsified | unverified-risk
```

Keep this list only for assumptions that would change your approach if wrong. Do not track obvious facts.

## Complex Refactoring Thinking

Use when refactoring involves more than mechanical code moves — when the structure change requires understanding why the code is shaped the way it is.

### Before refactoring, answer:

```text
Why is the code shaped this way?
  - Historical reason: <what constraint existed when this was written>
  - Current reason: <what constraint still exists>
  - Accidental: <no good reason, safe to change>

What behavior does this structure encode?
  - Explicit: <what the code obviously does>
  - Implicit: <what side effects or ordering guarantees exist>
  - Relied upon: <what callers/tests depend on, even if undocumented>

What is the target structure?
  - Shape: <how it should look after>
  - Preserves: <which behaviors and contracts carry over>
  - Breaks: <what intentionally changes — must be zero for pure refactor>
```

### Refactoring progression for complex cases

1. **Understand** — Map current behavior and its consumers
2. **Introduce** — Add the new structure alongside the old (parallel implementation)
3. **Migrate** — Move consumers one at a time to the new structure
4. **Verify** — Full verification at each migration step
5. **Remove** — Delete the old structure only after all consumers migrated and verified

This strangler-fig pattern prevents the "big bang" refactor failure where everything breaks at once and you can't tell what caused it.

### Signs you need to stop and rethink

- You're touching files outside your stated boundary
- The refactor keeps revealing "one more thing" that needs changing
- Tests are failing for reasons you didn't predict
- You've been working for 3+ waves without verification passing
- The change is growing beyond the original scope estimate

When these appear: stop editing, verify current state, update the plan boundary, and ask whether the scope should expand (with user) or the approach should change.
