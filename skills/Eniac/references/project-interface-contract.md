# Project Interface Contract

Use when creating a project README or materially rewriting one. Treat the README as the tested interface between the repository and its next operator, not as marketing copy.

## Contract

A useful README lets a new operator answer, without reading source:

1. What does this project do, and for whom?
2. What must exist before it can run?
3. What exact commands install, run, test, and build it?
4. What configuration is required, and where does it come from?
5. What success looks like and where failures surface?

Derive answers from manifests, scripts, configs, entry points, examples, and observed commands. Do not invent capabilities or copy stale package scripts.

## Adaptive Shape

Include only sections the project needs:

```markdown
# <Project Name>

<One factual sentence: purpose, primary user, and boundary.>

## Capabilities

- <Concrete behavior, not aspiration.>

## Quick Start

### Prerequisites

- <runtime/tool/service with supported version evidence>

### Run

```<shell>
<commands verified from a clean or equivalent state>
```

Expected: <observable success signal, URL, output, or artifact>

## Configuration

| Name | Required | Default | Purpose |
| --- | --- | --- | --- |
| `<NAME>` | yes/no | `<value>` | <effect, never secret content> |

## Usage

<Smallest real example or primary workflow.>

## Development

```<shell>
<test command>
<lint/type/build command>
```

## Architecture

<Only when the module map or data flow is not obvious.>

## Operations

<Only when deployment, migrations, jobs, observability, or recovery matter.>

## License

<Actual license or repository link.>
```

## Evidence Pass

- Resolve every local link and referenced path.
- Match commands to the active package manager and repository scripts.
- Verify at least the Quick Start path when execution is safe.
- Name configuration keys only; never include live values.
- Remove placeholders, impossible examples, and claims not supported by code.
- Preserve useful existing sections unless they are incorrect or superseded.
- If a command cannot be verified, label that limitation in the handoff instead of presenting it as proven.

For small behavior changes, patch only affected sections. Do not replace a mature README merely to impose this structure.

## Formatted Starting Template

For a full visual template with badges, centered header, section structure, and quality checklist, load `references/readme-template.md`. Use it as the skeleton and fill content from the evidence pass above.
