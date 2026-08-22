# House rules

Copy this into your repository as the agent instruction file your runtime reads
(`AGENTS.md`, `CLAUDE.md`, `.cursor/rules/`, `.github/copilot-instructions.md`, or whatever
it is), or as a section inside the one that already exists.

This file sits at **precedence level 3** in `SKILL.md#precedence` — above the skill, below
the user. That is the whole mechanism: your rules win on contact, and Eniac stays a clean
vendored copy you can update without merging.

Delete every heading you have nothing true to put under. An empty section teaches readers
to skim, and a skimmed instruction file is an unread one. Aim for one page — this text is
loaded on every task, so every line is paid for continuously.

---

## Engineering behaviour

Follow Eniac for software work in this repository: `path/to/skills/Eniac/SKILL.md`.
<!-- Or, on a runtime with no skill loader: path/to/skills/Eniac/adapters/eniac-compact.md -->

The rules below are specific to this repository and **override** the skill where they
disagree.

## Commands that actually prove something

<!-- The ones that exist here, not the ones the ecosystem usually uses. If a command is
     slow, say how slow, so the agent can decide when to run it. -->

- Build:
- Test (fast):
- Test (full, ~N minutes):
- Lint / format:
- Type check:
- Run locally:

## Conventions the code follows but does not state

<!-- The things a new engineer gets wrong in their first week. -->

-

## Do not touch without an owner

<!-- Generated directories, vendored code, frozen surfaces, anything under change control.
     Name the owner or the process, not just the path. -->

| Path or surface | Why | Who to ask |
| --- | --- | --- |
|  |  |  |

## Deploy and rollback

<!-- The real sequence, including who approves what. Eniac treats production as L4 and
     will ask; this tells it who to ask and what the ask should contain. -->

- Environments:
- Deploy:
- Rollback:
- Approval required from:

## Definition of done here

<!-- Overrides the skill's default closing bar. Be concrete: what must be green, what must
     be updated, what must be linked. -->

-

## Known traps

<!-- Things that have already bitten someone. This section is the highest-value part of the
     file and the one most often left empty. -->

-

## Unattended runs

<!-- Only if agents run here on a schedule or in CI. See references/autonomy.md. Anything
     not listed under Allowed is forbidden. -->

```text
Scope:
Allowed:
Forbidden:
Budget:
On-gate:
```
