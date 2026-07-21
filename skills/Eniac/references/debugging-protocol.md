# Debugging Protocol Reference

Use when fixing a bug, investigating a failure, or when behavior does not match expectation. This is the hands-on companion to the causal-record shape in `algorithm-workflow.md`: that file defines what a closed defect record must contain; this file defines how to get there.

## Contents

- [Debugging contract](#debugging-contract)
- [Step 1: Reproduce](#step-1-reproduce)
- [Step 2: Localize](#step-2-localize)
- [Step 3: Hypothesize and discriminate](#step-3-hypothesize-and-discriminate)
- [Step 4: Instrument](#step-4-instrument)
- [Step 5: Fix minimally](#step-5-fix-minimally)
- [Step 6: Lock with regression proof](#step-6-lock-with-regression-proof)
- [Bug class playbook](#bug-class-playbook)
- [Hard bug tactics](#hard-bug-tactics)
- [Anti-patterns](#anti-patterns)

## Debugging Contract

- A bug is not understood until it can be reproduced or the failing path is fully traced with evidence.
- A bug is not fixed until the fix is explained by a proven cause and locked by a regression signal.
- Never stack speculative edits. One hypothesis, one discriminating check, one conclusion — then the next.
- Preserve the evidence: keep the failing input, the exact error text, and the reproduction command in task state until closure.
- If the fix works but you cannot explain why, the bug is not fixed. Label it `Unverified` and continue or hand off.

## Step 1: Reproduce

Before reading code, secure a reproduction:

```text
Trigger: <exact command, input, request, or user action>
Expected: <what should happen>
Actual: <what happens, exact error text or wrong output>
Frequency: always | intermittent | once
Environment: <runtime, version, OS, config that may matter>
```

- Prefer the narrowest reproduction: a single failing test, a curl request, a one-line script — not the full app flow.
- If reproduction is impossible (production-only, user report, race), trace the failing path from the evidence you have: stack trace, logs, input data. State explicitly that the diagnosis rests on trace evidence, not reproduction.
- For intermittent bugs, find the condition that makes it deterministic (fixed seed, forced timing, specific data) before proceeding. An intermittent reproduction cannot verify a fix.
- Write the reproduction as a failing test first when the test harness makes it cheap — it becomes the regression lock in Step 6 for free.

## Step 2: Localize

Shrink the search space before forming hypotheses:

| Technique | Use when | How |
| --- | --- | --- |
| Stack trace walk | crash or thrown error | Read the deepest in-project frame first; library frames are usually victims, not causes |
| Input bisection | large failing input | Halve the input until minimal failing case found |
| Code path bisection | unclear where in a flow | Check intermediate state at the midpoint; recurse into the failing half |
| Version bisection | it worked before | `git bisect` with the reproduction as the test; or diff the suspect range |
| Differential comparison | works in one env/config/case, fails in another | List the exact differences; test them one at a time |
| Data inspection | wrong output, no error | Dump the actual value at each transformation boundary until the first wrong value appears |

The first place the state goes wrong is the crime scene. Everything downstream is a consequence — do not fix downstream.

## Step 3: Hypothesize and Discriminate

```text
H1: <cause> — predicts <observable X if true, Y if false> — check: <cheapest test>
H2: <cause> — predicts <...> — check: <...>
```

- Every hypothesis must make a testable prediction. "Maybe it's the cache" is not a hypothesis; "if the cache is stale, a cold start will not reproduce" is.
- Run the cheapest discriminating check first — the one that eliminates the most hypotheses per unit cost.
- Record ruled-out branches. Re-testing a ruled-out hypothesis is the most common debugging waste.
- After two failed hypotheses, stop and re-read the evidence from scratch — the frame is usually wrong, not the hypotheses. Question the assumption you have not written down: is the code you are reading actually the code that runs? Is the config you assume loaded actually loaded? Is the error from the request you think it is?

## Step 4: Instrument

When reading is not enough, make the system tell you:

- Add targeted, temporary instrumentation at the suspected boundary: log the input, output, and relevant state with an unmistakable marker (e.g. `DEBUG-ENIAC:`), so cleanup is a grep away.
- Prefer structured observation over noise: one log line per boundary crossing with the discriminating value, not print-everything.
- Use the runtime's native tools when they beat prints: debugger breakpoints, `--inspect`, `pdb`, `dlv`, `lldb`, DB query logs, browser devtools network/console, framework debug modes.
- For state corruption, log a checksum or shape summary at each mutation site to find the first corrupting write.
- Remove all instrumentation before shipping. The defect radar in `software-engineering.md` includes residual debug output — do not trip it yourself.

## Step 5: Fix Minimally

- Fix at the first point where state goes wrong, or deeper if the root cause is in scope — never at the symptom site by compensating for bad upstream data.
- The fix must be explained by the proven cause in one sentence: "X failed because Y; this change makes Y impossible/handled."
- If the same root cause has siblings (the same wrong pattern copied elsewhere), search for them (`rg` the pattern) and report or fix per scope. A fixed instance with live siblings is a containment, not a resolution.
- Keep the fix diff separable from any refactor impulse. If the code deserves restructuring, note it in the handoff.
- If an urgent workaround ships first, label it containment in the causal record and keep the investigation open.

## Step 6: Lock With Regression Proof

- Convert the reproduction into a permanent test in the project's existing framework, named after the behavior: `"parses UTF-8 filenames with combining marks"` — not `"fix bug 123"`.
- Run the test against the pre-fix code when cheap (stash/branch) to prove it actually catches the bug — a test that passes both before and after locks nothing.
- Run the surrounding suite to prove the fix introduced no regression; report baseline failures separately.
- Complete the causal record from `algorithm-workflow.md` with `Confidence: Direct` only when the discriminating evidence supports it.

## Bug Class Playbook

| Class | Signature | First move | Frequent root cause |
| --- | --- | --- | --- |
| Off-by-one / boundary | fails at empty, first, last, max | test the exact boundary values | `<` vs `<=`, length vs index, inclusive vs exclusive range |
| Null/undefined/None | crash on missing value | trace where the value should have been set | optional path not handled, API shape changed, race on init |
| Type/shape mismatch | wrong output, silent coercion | dump actual runtime type at the boundary | string vs number, snake vs camel keys, date as string |
| State/lifecycle | works first time, fails on repeat | compare first vs second run state | stale cache, unreset singleton, leaked listener, module-level mutable state |
| Async/race | intermittent, timing-dependent | force the orderings (delays, single-thread, seeds) | missing await, shared state without sync, callback after unmount/dispose |
| Concurrency/deadlock | hang or corruption under load | capture thread/task dump at hang | lock ordering, blocking call in async context, unbounded queue |
| Config/environment | works on one machine only | diff resolved config between environments | env var absent, path separator, locale/timezone/encoding, version skew |
| Dependency behavior | broke without code change | check lockfile diff and changelog | transitive bump, breaking minor, removed default |
| Encoding/unicode | fails on specific text | test with multibyte, combining, RTL samples | byte length vs char length, wrong codec, normalization form |
| Time | fails at midnight/DST/month-end/leap | test the pathological instants | local vs UTC, DST transition, month arithmetic |
| Floating point | almost-equal comparisons fail | print full precision values | equality on floats, accumulation error, currency as float |
| Resource exhaustion | degrades over time, then dies | measure the resource curve | connection/file-handle leak, unbounded cache, missing cleanup |

## Hard Bug Tactics

When the standard loop stalls:

- **Minimal repro project**: extract the failing behavior into the smallest standalone case. The bug either survives extraction (now trivially inspectable) or dies (the removed context contains the cause — bisect it back in).
- **Working-backwards diff**: find the nearest configuration that works (older commit, simpler input, other environment) and morph it toward the failing one, one change at a time.
- **Read the actual source** of the library/framework behavior in question instead of guessing from docs — node_modules, site-packages, and vendored sources are readable.
- **Question the tools**: stale build artifacts, caches, and hot-reload can run code that no longer exists. Clean build, restart, verify the running version before trusting any observation.
- **Rubber-duck the evidence**: write the complete evidence list and what each item implies. Contradictions between implications expose the wrong assumption.
- **Second-opinion pass**: after three materially different failed attempts, follow the strike protocol in `software-engineering.md` — stop mutating, preserve evidence, report with hypotheses ruled out.

## Anti-Patterns

- Fixing the symptom site with a guard while the corrupt upstream state lives on.
- Changing several things at once, then not knowing which one mattered.
- "It passes now" after an unrelated-looking edit — without an explanation, the bug moved, not died.
- Deleting or weakening the failing test.
- Blaming the framework/compiler/OS before verifying your own boundary — those are occasionally guilty, but the prior is heavily against it.
- Debugging on top of an unclean state: uncommitted experiments, stale caches, or mixed versions poison every observation.
- Leaving instrumentation, commented-out attempts, or debug flags in the shipped diff.
