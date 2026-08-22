# Security

`safety.md` governs what *you* are allowed to do — the authorization gates on your own
actions. This file is different: it is about building software that resists an attacker,
and it applies even when every action you take is perfectly authorized.

Load it when the change touches a trust boundary: authentication or authorization, input
that came from outside the system, secrets or credentials, file upload or download,
serialization and deserialization, templating or query construction, session and cookie
handling, cryptography, or anything a user of one tenant could aim at another. Load it
also when the task is a security review, or when the deliverable will be reachable from
the public internet for the first time.

Do not load it because the word *security* appeared. An ordinary task does not inherit
this specialty, and topic anxiety is not evidence — that rule from `SKILL.md#routes` holds
here more than anywhere, because security material is long and reads as important.

> **Owns** — software that resists an attacker — trust boundaries, per-path and per-object authorization, injection as one bug in many costumes, secrets in code and their rotation, default deny, proportional threat modelling, the comforts that are not controls, security review, disclosure.
> **Defers** — your own authorization gates and secret *handling* → `safety.md`; tenancy, compliance, and supply chain as obligations → `enterprise.md`; injection through a model's context → `llm-systems.md#prompt-injection-is-an-authorization-problem`.

## Contents

- [Everything Starts At A Trust Boundary](#everything-starts-at-a-trust-boundary)
- [Authorization Is Per Path, Not Per Screen](#authorization-is-per-path-not-per-screen)
- [Injection Is One Bug Wearing Many Costumes](#injection-is-one-bug-wearing-many-costumes)
- [Secrets In Code And Configuration](#secrets-in-code-and-configuration)
- [Default Deny](#default-deny)
- [Threat Modelling, Proportionally](#threat-modelling-proportionally)
- [The Comforts That Are Not Controls](#the-comforts-that-are-not-controls)
- [Reviewing For Security](#reviewing-for-security)
- [When You Find Something Real](#when-you-find-something-real)
- [Red Flags](#red-flags)

## Everything Starts At A Trust Boundary

A trust boundary is any place data or control crosses from somewhere you do not control
into somewhere you do. Almost every vulnerability worth the name lives on one, which makes
"where are the boundaries in this change" the first and most productive question.

The boundaries people find easily: the HTTP request, the login form, the file upload. The
boundaries that produce real incidents are the ones that do not look like boundaries:

- A message from an internal queue, written by a service someone else deployed.
- A row in your own database that a user put there three months ago.
- An environment variable, a config file, or a feature flag set through a UI.
- A webhook, whose only proof of origin is a signature nobody verifies.
- A filename, an image's metadata, a PDF's embedded script, a spreadsheet formula.
- The response from a third-party API you called — outbound is not the same as trusted.
- Text your own model generated from any of the above (`llm-systems.md#prompt-injection-is-an-authorization-problem`).

**Validate at the boundary, in the shape the destination needs.** Not "sanitize
everywhere", which produces double-escaped data and a false sense that it is handled
somewhere. Decide the type, the range, the length, and the allowed character set *once*,
at the point of entry, and let everything downstream rely on it.

Trust does not survive a hop. Data that was validated at the API edge and then written to
a queue arrives at the consumer as untrusted input again unless the consumer can verify
where it came from.

## Authorization Is Per Path, Not Per Screen

This is the single most common serious vulnerability in real applications, and it is
almost always the same shape: the interface does not show a button, so nobody checked the
endpoint behind it.

- **Authentication answers "who is this". Authorization answers "may this person do this
  to this object".** Confusing them produces a system where any logged-in user can act on
  any record by changing an id.
- **Check on the object, not on the route.** `GET /invoices/{id}` needs "does this caller
  own invoice {id}", not "is this caller logged in". The route-level check passes for
  everyone and reads as protection.
- **Every entry point, not just the main one.** The REST route, the GraphQL resolver, the
  gRPC method, the admin action, the background job that acts on a user's behalf, the
  export, the bulk endpoint, the websocket message, the CSV import. A single unguarded
  path is the whole vulnerability.
- **Enumerable identifiers are a disclosure even when authorization holds.** Sequential
  ids leak volume and growth; the fix is opaque identifiers, not a stronger check.
- **Deny by returning the same answer.** A 403 where a 404 belongs tells an attacker the
  record exists, which is often the thing they wanted.
- **In a multi-tenant system, the tenant scope is part of the query, not a filter applied
  after.** An unscoped query is a breach rather than a bug (`enterprise.md#multi-tenancy`).

When reviewing, the productive move is to enumerate the paths that reach a piece of data
and check each one, rather than to read the code that guards the one you were shown.

## Injection Is One Bug Wearing Many Costumes

SQL injection, command injection, template injection, path traversal, XSS, LDAP, XML
external entities, deserialization, log forging, CSV formula injection, and prompt
injection are all the same failure: **data was placed somewhere an interpreter reads
instructions.** Recognizing the shape matters more than memorizing the list, because the
list keeps growing and the shape does not.

The fix is structural separation, in this order:

1. **Do not build the instruction from the data.** A parameterized query, an argument
   array rather than a shell string, a real templating API rather than concatenation, an
   allow-list mapped to a fixed set of choices.
2. **If separation is impossible, use the platform's escaper for that exact context**, and
   know that context: HTML body, HTML attribute, JavaScript string, URL parameter, and CSS
   each need a different escape, and the right escape in the wrong place is no escape.
3. **Hand-written escaping is not a control.** Blocklists of dangerous characters have
   been bypassed for every interpreter that exists, usually by an encoding nobody
   considered.

Two specific traps worth naming. **Path handling** — user-supplied filenames must be
resolved and then confirmed to sit inside the intended directory, because `..`, symlinks,
absolute paths, URL encoding, and Unicode normalization all produce the same escape.
**Deserialization** of an untrusted payload into arbitrary types is remote code execution
in most ecosystems; parse into a known shape instead.

## Secrets In Code And Configuration

- **Secrets are handles, not content.** Never print, log, echo into an error message, put
  in a URL, or write into a fixture. A secret that has been in a log is a secret that has
  been rotated, not one that is fine because the log is private.
- **A secret in git history is compromised**, even after the commit is amended away.
  Rotate it, then remove it; the reverse order accomplishes nothing.
- **Configuration comes from the environment or a secret manager**, not from a file that
  is one `.gitignore` mistake from being public.
- **Compare secrets in constant time** where the comparison is attacker-observable — token
  and signature checks especially.
- **Webhook signatures exist to be verified.** An unverified webhook endpoint is an
  unauthenticated write endpoint that looks authenticated because a vendor's name is on it.
- **Rotation must be possible without downtime**, which means the system accepts two valid
  secrets during the overlap. Design that before you need it at 3am.

## Default Deny

The safe default is refusal, and every exception is a decision someone made on purpose.
Where a system defaults to permission, its security is the completeness of a list nobody
finished.

Applied concretely: routes require authorization unless explicitly marked public; CORS
names origins rather than reflecting the request's; new database columns are not exposed by
an API until someone adds them; uploads accept known types rather than rejecting known-bad
ones; an unknown enum value is an error rather than a fallback; a failed authorization
check fails closed even when the authorization service is down.

That last one is where systems quietly invert. A permission check wrapped in
`try/except: return True` is not resilience — it converts every outage into an open door.

## Threat Modelling, Proportionally

The formal exercise is worth its cost on a new externally-reachable system, an
authentication or payment flow, or anything holding regulated data. It is not worth it for
a form field on an internal admin page, and running it anyway trains everyone to skip it
when it matters.

The proportional version is four questions and takes minutes:

```text
What is worth taking here?          data, money, compute, reputation, access to something else
Who can reach it?                   anonymous internet, any logged-in user, another tenant,
                                    an employee, a compromised dependency
What is the cheapest way in?        attack the weakest boundary, not the most interesting one
What would we see if it happened?   if the answer is "nothing", that is the finding
```

The fourth question is the one that gets skipped and the one that most often produces a
concrete action. A control you cannot observe failing is a control you are hoping for.

## The Comforts That Are Not Controls

Each of these is true and none of them is the protection it gets treated as:

| Said | What it actually covers |
| --- | --- |
| "It is behind HTTPS" | data in transit — not authorization, not injection, not the payload |
| "The framework handles that" | the classes it knows about, in the way you used it; ORMs still have raw-SQL escape hatches, and templating engines still have `safe` |
| "It is internal only" | until a VPN, a proxy, a misconfigured ingress, or an SSRF makes it reachable — and internal callers include compromised ones |
| "We have a WAF" | known signatures; it is a delay, not a fix, and it fails open under load |
| "The endpoint is not documented" | nothing. Obscurity is not a control, and endpoints are enumerated by tooling in seconds |
| "Users would not do that" | users would not; attackers are not users, and neither are scripts |
| "We validate on the client" | user experience. The client is attacker-controlled and its checks are advisory |
| "It is a hash, so it is safe" | fast hashes are cracked at scale; passwords need a slow, salted, purpose-built one |

## Reviewing For Security

Read for the abuse case, not the happy path — the difference is the whole job.

1. **Follow the untrusted data.** From where it enters, through every transformation, to
   every place it is interpreted, stored, rendered, or forwarded. Most findings are on
   that path.
2. **Enumerate the reachable paths** to each sensitive operation and check authorization
   on each independently.
3. **Look at what happens on failure.** Errors that leak internals, checks that fail open,
   partial writes that leave a record half-created, retries that duplicate a charge.
4. **Check the new dependency**, if there is one: what it does at install time, what it
   reaches out to, whether it is maintained (`enterprise.md#supply-chain`).
5. **Look for the thing that was removed** — a check deleted to fix a bug, a validation
   loosened to accept a customer's data, a scope widened during an incident and never
   narrowed.

**Prove the finding.** A security claim without a concrete path from attacker to impact is
an opinion, and a confidently wrong security review costs more than none: it spends the
team's trust and buries the real findings underneath it. Write the abuse case as concretely
as a test — who, what they send, what they get.

**Never assert that something is secure or compliant.** You can say what you checked, what
you found, and what you did not look at. "No issues found in the authorization paths I
traced" is honest and useful; "this is secure" is a claim about the world that no code
reading supports (`enterprise.md#never-invent-a-compliance-claim`).

## When You Find Something Real

A live exploitable vulnerability in production is **tier one** on the triage ladder —
active harm — and it is `L4`. That combination has specific consequences:

- **Stop and report before exploring.** Confirming an authorization bypass on production
  data with a real account is itself an incident. Reproduce on a local or staging instance,
  or with your own record.
- **Report privately, in the channel that exists for it.** Not in a public issue, not in a
  commit message, and not in a pull request title that describes the exploit before the fix
  ships.
- **Do not write the exploit into the repository.** A regression test proves the fix
  without publishing a recipe: assert that the request is refused, not how to craft it.
- **Two corrections, not one** — fix the vulnerability, and separately fix whatever let it
  reach production. The second is what prevents the next one.
- **Assume it was found before you found it** when the exposure was long-lived or the data
  was valuable. Whether to treat it as a breach is a decision for people with legal
  obligations, not for you — surface it, name what you saw, and let them decide.

## Red Flags

- String concatenation anywhere near a query, a shell command, a path, or a template.
- An authorization check that reads a role but never the object being acted on.
- `try`/`except` around a permission check, a signature verification, or a token check.
- Any comparison of a secret, token, or signature with `==` in an attacker-observable path.
- A new endpoint that is public because nobody said it was not.
- User-controlled input reaching a deserializer, a file path, an HTTP client, or `eval`.
- Verbose errors, stack traces, or internal identifiers on a public surface.
- A dependency added mid-task to solve a security problem — cryptography especially, where
  the correct move is almost always the platform's standard library.
- A test that was changed or deleted to make a security-relevant change pass.
- Rate limiting on login but not on password reset, token exchange, or the API key path.
