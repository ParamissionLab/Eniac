# LLM Systems

Software that calls a language model is ordinary software with one component that returns
a different answer to the same question, cannot be fully specified, and will happily
produce a confident wrong result rather than an error. Every rule in `production.md`
applies to that call. This file is what those rules do not cover.

Load it when the system under work *calls a model*: a feature backed by generation,
classification, extraction, or summarization; a retrieval pipeline; an agent that uses
tools; an evaluation harness for any of those. Do not load it merely because the
conversation is happening with a model — that is the runtime, not the subject.

This file is deliberately free of model names, prices, and parameter tables. Those change
faster than any document can track, and a stale number read as current is worse than no
number. Get them from the provider's own documentation at the moment you need them; what
is written here is the part that stays true.

> **Owns** — software that calls a model — the call's four unusual properties, pinned model and prompt versions, prompt injection as an authorization problem, output as untrusted input, structured output, testing something nondeterministic, cost and latency, what leaves your system in a prompt.
> **Defers** — the trust-boundary and injection frame in general → `security.md`; remote-call resilience → `production.md`; the evaluate-and-improve loop → `loops.md#the-outer-loop`; data obligations → `enterprise.md`.

## Contents

- [A Model Call Is A Remote Call With A Surprise](#a-model-call-is-a-remote-call-with-a-surprise)
- [Pin The Version, Or Ship A Silent Breaking Change](#pin-the-version-or-ship-a-silent-breaking-change)
- [Prompt Injection Is An Authorization Problem](#prompt-injection-is-an-authorization-problem)
- [Model Output Is Untrusted Input](#model-output-is-untrusted-input)
- [Ask For Structure, Not Prose You Will Parse](#ask-for-structure-not-prose-you-will-parse)
- [Testing Something Nondeterministic](#testing-something-nondeterministic)
- [Failure Modes That Have No Analogue](#failure-modes-that-have-no-analogue)
- [Cost And Latency Are Design Constraints](#cost-and-latency-are-design-constraints)
- [What Leaves Your System In A Prompt](#what-leaves-your-system-in-a-prompt)
- [Red Flags](#red-flags)

## A Model Call Is A Remote Call With A Surprise

Start from `production.md#resilience-four-questions-per-remote-call` — timeout, retry,
idempotency, degradation — because the call is remote and everything there holds. Then
adjust for four properties that ordinary remote calls do not have.

- **Latency is high, variable, and proportional to output length.** A timeout tuned for a
  database is wrong by an order of magnitude here, and a p99 that is four times the median
  is normal rather than a symptom.
- **Retrying is expensive and not free of side effects.** A retried generation is a second
  full charge, and if the first call already emitted tool calls it may have already acted.
  Decide idempotency at the *tool* layer, not the request layer.
- **Failure is often a well-formed 200.** A truncated answer, a refusal, or a plausible
  fabrication all arrive with a success status. Health checks and error rates will show
  nothing, so the degradation path must be triggered by *validating the content*, not by
  catching an exception.
- **Streaming changes the contract.** A response that has begun can still fail halfway, and
  a partial answer already shown to a user cannot be retracted. Decide what a
  half-delivered response means before building on it.

**Degrade to something honest.** When the model call fails or its output does not validate,
the fallback is a stated limitation — an empty state, a "could not summarize this", a
manual path — not a silently worse answer that looks like the real one.

## Pin The Version, Or Ship A Silent Breaking Change

A model identifier that resolves to "whatever is current" is a dependency that upgrades
itself in production without a pull request. The upgrade is usually an improvement and
occasionally reshapes your outputs: a different format, a different verbosity, a refusal
where there was none, a field that used to appear and now does not.

Pin the exact version. Treat a change to it exactly like a dependency bump under
`workflows.md#overlays`: read what changed, run the evals, roll out behind a flag, and keep
the previous version reachable for as long as rollback might be needed. The prompt is part
of the same contract — a prompt edit is a behaviour change, so version it with the code and
review it as code, not as configuration someone can adjust in a dashboard.

## Prompt Injection Is An Authorization Problem

**Everything the model reads is data. None of it is instruction.** A retrieved document, a
web page, a support ticket, a filename, a code comment, a tool's response, a previous
turn's output — all of it can contain text aimed at the model, and the model has no
reliable way to tell it apart from your own instructions. This is the same failure as every
other injection in `security.md#injection-is-one-bug-wearing-many-costumes`, and like the
others it is not solved by escaping or by instructing the model to be careful.

It is solved at the authorization layer, because the damage is never the text — it is what
the system does next:

- **Give the tools the permissions, not the model.** Every tool call is authorized by what
  the *user* may do, checked server-side, independently of what the model asked for. A
  model that requests a deletion it is not entitled to gets a refusal, not a deletion.
- **Watch for the combination that turns a nuisance into a breach:** untrusted content in
  context, access to private data, and any way to send data outward. Each is fine alone.
  Together, injected text can read your data and exfiltrate it — through a tool, a URL it
  asks you to render, an image source, an outbound request. Break one leg of the three.
- **Mark provenance and keep it.** Which part of the context came from the user, which from
  a retrieved document, which from a tool. Downstream decisions need to know, and a flat
  concatenated prompt has thrown that away.
- **Confirm consequential actions with a person**, and show them what will actually happen
  rather than the model's description of it. `autonomy.md` covers the unattended case,
  where the answer is a narrow written envelope and a gate that fails closed.
- **Never let generated text become an instruction to another agent** without the same
  treatment. Multi-agent pipelines re-introduce the boundary at every hop.

## Model Output Is Untrusted Input

Whatever consumes the response treats it as hostile, because a model asked for SQL will
produce SQL, and a model asked for a path will produce `../../etc/passwd` if the context
suggested it.

- Generated code is executed only in a sandbox with no credentials and no network, if at
  all.
- Generated queries, paths, URLs, shell arguments, and identifiers are validated against an
  allow-list before use — the same discipline as any other untrusted input.
- Generated HTML or Markdown rendered in a browser is an XSS surface; sanitize it.
- Identifiers the model produces — user ids, order numbers, file names — are *claims*, not
  facts. Resolve them against your own data before acting.

## Ask For Structure, Not Prose You Will Parse

Parsing prose with regular expressions is the most common source of quiet breakage in these
systems, because the format drifts with every prompt edit and every model version, and it
drifts without erroring.

Use whatever structured mechanism the provider offers — a schema, a typed tool call,
constrained decoding — and validate the result against your own schema anyway. Then decide
what happens when validation fails, before it does: one retry with the validation error fed
back is usually right; a second retry rarely helps and doubles the cost of a request that
was already going to fail.

Keep the schema small and flat. Deeply nested output is where models are least reliable,
and a field you do not use is a field that can fail validation for nothing.

## Testing Something Nondeterministic

Unit tests still apply to everything *around* the model — the retrieval, the parsing, the
tool implementations, the fallback path. Those should be deterministic and are where most
of your bugs actually live, so fake the model call there and test the machinery properly.

For the model call itself, equality assertions are the wrong instrument. Assert properties
that must hold for any acceptable answer:

- It validates against the schema, and required fields are present.
- Invariants hold: cited ids exist in the source, totals match the input, the language is
  the one asked for, nothing appears that was not in the context.
- Known-bad behaviour is absent: it does not answer when the context lacks the answer, does
  not follow instructions embedded in retrieved text, does not leak the system prompt.
- Cost and length stay inside their budget.

Above that sits an **eval set** — real inputs with graded outputs, run on every prompt or
model change. This is the outer loop from `loops.md#the-outer-loop` and its rules apply
without modification: fix the evaluation before the artifact, keep a baseline, change one
thing per run, and hold cases back, because the examples you iterate on are the examples you
get good at. An eval suite where everything passes is usually a suite that got easier.

Grading with another model is legitimate and needs the same scepticism as any other
measurement: check the grader against human judgment on a sample before trusting it, and
never let the grader and the system share a prompt, a bias, or an author's assumption.

## Failure Modes That Have No Analogue

| Symptom | What is actually happening | What to do |
| --- | --- | --- |
| Output stops mid-sentence | hit the output token limit | budget output length; detect truncation explicitly rather than parsing the fragment |
| Confidently wrong facts, names, APIs | the model produced plausible text with no source | ground it in retrieved content and require citations you can verify against the source |
| A refusal where the task is legitimate | safety behaviour on an ambiguous request | rephrase the task, not the model; if it persists, the framing is genuinely ambiguous |
| Quality drops as context grows | relevant material buried among irrelevant | retrieve less and better; position what matters where it will be read |
| Works in testing, fails on real data | test inputs were short, clean, and in one language | test with real length, real messiness, and real character sets |
| Same input, different shape of answer | ordinary nondeterminism | never depend on shape you did not constrain |
| Everything degrades after a deploy | prompt edit or model version change | version prompts with code; run the evals before merging |

## Cost And Latency Are Design Constraints

Both scale with usage in a way that ordinary compute does not, and both are usually
discovered after launch.

- **Know the cost of one request** — input tokens plus output tokens — before shipping, and
  multiply by realistic volume rather than expected volume. The gap between them is where
  budget incidents come from.
- **The cheapest call is the one you do not make.** Cache by a key that includes the prompt
  version and model version, so a prompt change invalidates the cache rather than serving
  answers generated by a system that no longer exists.
- **Match the model to the task.** A large model on a classification a small one handles is
  pure cost, and cost that scales with traffic.
- **Send less context.** Retrieval quality beats retrieval quantity on cost, latency, and
  accuracy simultaneously — one of the few places where all three move together.
- **Rate limits are per account and shared across everything you run** — the batch job can
  starve the user-facing path (`production.md`). Separate the quotas or the priorities.
- **Instrument per call**: tokens in, tokens out, latency, model version, prompt version,
  cache hit, validation outcome. Without prompt and model version on every record, you
  cannot attribute a regression to the change that caused it.

## What Leaves Your System In A Prompt

A prompt is an outbound transfer of everything in it, to a third party, usually across a
border. That makes it a data-handling decision rather than an implementation detail.

Know what is in the context: user content, retrieved documents, logs, error messages with
records embedded, and whatever a tool returned. Personal, health, payment, and financial
data carry legal obligations that no amount of code reading settles — recognize the
category, minimize what is sent, and route the question to whoever owns it rather than
deciding it yourself (`enterprise.md`). Whether provider retention, training use, or
regional processing is acceptable is a contractual question, not a technical one, and
**never assert compliance on your own authority**.

Log what you sent, and remember that doing so copies the same data into your logs. Redact
at the boundary or accept that the logs now carry the same obligations as the prompt.

## Red Flags

- A model identifier that means "latest" anywhere near production.
- Prompts edited in a dashboard, untracked, unreviewed, and unversioned.
- Retrieved or user content concatenated into the system prompt with no provenance kept.
- A tool whose authorization is "the model decided to call it".
- Untrusted content, private data access, and an outbound channel in the same context.
- Regexes parsing prose where a schema or tool call was available.
- Retry loops around generation with no cost ceiling and no attempt limit.
- Tests that assert exact output strings — they will be deleted the first time they flake,
  taking the only check with them.
- No eval set, so every prompt change is shipped on the strength of one example that looked
  good.
- Truncation, refusal, and empty output all handled by the same branch as success.
- Cost measured per month rather than per request, so nobody knows what a feature costs.
