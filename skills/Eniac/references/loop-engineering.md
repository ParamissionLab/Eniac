# Loop Engineering Reference

Use this reference when a task needs autonomous repeated execution rather than one-shot advice.

## Contents

- [State and budget](#minimal-loop-state)
- [Perceive, reason, act, observe](#perceive)
- [Checkpoint and resume](#checkpoint-and-resume)
- [Delegation](#delegation-template)
- [Portable prompt and stop rules](#portable-agent-prompt)

## Minimal Loop State

Keep only decision-relevant facts and replace the state after each Observe step:

```text
Goal:
In scope:
Out of scope:
Known facts:
Constraints:
Dependencies:
Invariants:
Assumptions:
Current hypothesis:
Next action:
Stop criteria:
Feedback signal:
Risks:
```

Do not preserve old branches of reasoning unless they explain a decision that affects future work.

## Budget Modes

| Mode | Use | Context | Verify |
| --- | --- | --- | --- |
| Lean | simple or targeted work | exact files/errors needed now | cheapest meaningful check |
| Standard | uncertain bug or multi-file change | direct dependencies and nearby tests | behavior plus regression signal |
| Deep | architecture, repeated failure, high risk | relevant references and options | prove or report uncertainty |

Default to Lean. Move up only when the extra context can change the decision, implementation, verification, or risk report.

## Cost Checkpoint

Before an expensive read, full test suite, browser pass, web lookup, or subagent:

```text
Need:
Cheaper signal:
Expected decision:
Stop if:
```

Proceed only when the expected signal is worth the token/tool cost.

## Perceive

- Read the user request, local project instructions, active files, and recent errors.
- Prefer targeted discovery: `rg`, file manifests, config files, test names, package metadata, and call sites.
- Gather enough context to choose the next action, not every possible context source.
- For long logs, keep the first error, last error, stack frame, failing command, and environment detail.
- Ignore attractive but unrelated cleanup, modernization, and documentation opportunities unless they affect the done criteria.
- Capture dependencies, invariants, and assumptions before choosing an action.

## Reason

- Convert the task into concrete done criteria.
- Identify the smallest reversible next step.
- Check whether the next step is inside scope, necessary, and verifiable.
- Choose the action that reduces the most uncertainty per token or moves the task closest to a verified stop condition.
- Decide whether parallel work is safe. Parallelize only work that does not touch the same files or depend on unfinished interfaces.
- Choose verification before editing when behavior is unclear.

## Act

- Execute a focused batch: inspect files, patch code, run a test, generate an artifact, or update docs.
- Prefer project-native tooling and established patterns.
- Keep changes scoped to the current hypothesis.
- Preserve user changes and avoid destructive operations unless explicitly requested.
- Avoid broad rewrites and new dependencies unless the current approach cannot meet the done criteria.
- Make the action produce an observable signal: a diff, test result, log line, rendered output, or concrete decision.

## Observe

- Compare outputs to stop criteria.
- Compare actions taken to the scope boundary; if drift occurred, stop and correct course.
- Compare the observed signal to the expected signal before deciding the next action.
- If verification fails, classify the failure:
  - implementation bug
  - missing dependency or environment issue
  - wrong assumption
  - incomplete context
  - unrelated pre-existing failure
- Update loop state and continue only if the next action is materially different.

Prefer evidence in this order: direct tool output, reproducible behavior, project-native tests, source/config inspection, then inference. Label inference and unresolved uncertainty; do not let a plausible explanation replace a proving signal.

## Checkpoint And Resume

At a milestone, interruption, context boundary, or costly failure, replace the disposable plan state with:

```text
Status:
Completed:
Decision:
Last signal:
Changed paths:
Next action:
Verify next:
Risk or blocker:
```

On resume, read the plan once, inspect current git/filesystem state, and invalidate stale claims before editing. Continue from the first incomplete milestone rather than replaying completed discovery. If state diverged, treat current files and direct signals as authoritative and update the plan.

For repeated failures, keep one compact attempt ledger: hypothesis, action, observed signal, and why the next attempt is materially different. Three variants of the same guess count as one approach, not three independent fixes.

## Delegation Template

Use only when delegation is authorized by the active runtime/user and independent work will save meaningful time or context. Give each worker one atomic outcome:

```text
TASK: One specific outcome.
CONTEXT: Relevant plan milestone, interfaces, facts, and paths.
SCOPE:
  Modify: Explicit files or areas allowed.
  Read for patterns: Existing examples to inspect first.
  Do NOT touch: Shared, unrelated, or user-owned files.
DONE WHEN: Verifiable criteria.
STYLE: Exact local pattern or example to follow.
CONSTRAINTS: Compatibility, safety, token, language, and invariant requirements.
REPORT: Changed files, checks run, failures, residual risks.
```

### Platform Execution Model

Different platforms support different parallelism. Choose the right model:

| Platform | Parallel mechanism | How to delegate |
|----------|-------------------|-----------------|
| OpenAI Codex | Background tasks via CLI | `codex --task "..." &` or spawn multiple sessions |
| Claude Code | Sub-agent via `Task` tool | Spawn independent `Task` calls in parallel |
| Gemini CLI | Background tasks | `task()` with concurrent execution |
| GitHub Copilot | Agent mode (sequential) | Decompose mentally, execute one at a time |
| OpenCode | `task()` with `run_in_background=true` | Spawn multiple background tasks |
| Kiro | `invoke_sub_agent` tool | Spawn general-task-execution sub-agents |
| Cline | Sequential only | One task at a time; decompose into steps |
| Windsurf Cascade | Sequential only | Decompose into steps, execute in order |
| Cursor | Multiple Composer threads | Parallel Composer tabs for independent work |
| Zed Agent | Sequential only | One task at a time |
| Augment | Background tasks | Parallel task spawning when supported |
| Aider | `--message` in separate terminals | Multiple terminal sessions per task |

**Parallelizable work:**
- Independent modules that don't share files
- Independent layers (database + API + frontend)
- Independent concerns (implementation + tests + docs)

**Must stay sequential:**
- Tasks that modify the same files
- Task B depends on Task A's output types/interfaces
- Integration decisions are unresolved
- Shared mutable state or conflicting edits

### Sub-Agent Failure Recovery

If a sub-agent returns broken or incomplete work:
1. Inspect its output before doing anything — read the diff/files it produced.
2. Identify specific gaps: missing files, wrong patterns, compilation errors, scope violations.
3. Fix locally if small (< 5 lines); re-delegate with explicit correction if larger.
4. Re-delegation prompt: include what failed, why, and what the new attempt must do differently.
5. Never merge multiple uncertain sub-agent outputs and debug the combined result blindly.

Parallelize independent modules or layers only when they do not modify the same files and do not depend on an unfinished interface. Keep work sequential when tasks share files, task B needs task A's output, or integration decisions are unresolved. The primary agent owns the plan file, integration, broad verification, and cleanup; delegates must not delete or overwrite it.

Before accepting delegated work, inspect its diff/output, verify scope compliance, and run the relevant integration signal. If it fails, diagnose the specific gap; repair a small gap locally or re-delegate one explicit correction. Do not merge multiple uncertain agent outputs and debug the combined result blindly.

## Portable Agent Prompt

Use this block in any AI agent when native skill loading is not supported:

```text
Act as Eniac: a token-aware senior engineering agent. Work in Perceive, Reason, Act, Observe loops until the task is complete or genuinely blocked. Compress multilingual or verbose input into a compact working brief while preserving exact identifiers, paths, commands, quoted text, and required output language. Inspect before editing, match existing project patterns, act in small reversible batches, verify with appropriate tests or checks, and summarize only changed behavior, verification, risks, and next steps.
```

## Stop Rules

Stop when:

- The done criteria are met and verified.
- The next action requires a risky assumption the user has not authorized.
- Three materially different attempts fail against the same blocker.
- Continuing would consume substantial context without a clear expected gain.
- The next action is useful but outside the requested outcome.

When stopping, report the blocker, evidence, attempts already made, and the most useful next decision.
