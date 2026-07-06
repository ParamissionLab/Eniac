# README Template

Use as a starting skeleton when creating a new README. Adapt sections to the project's actual scope. Remove sections that have no content. Fill all content from observed project behavior, not assumptions.

This complements `project-interface-contract.md` which defines the evidence rules. This file provides the visual structure and format.

## Template

```markdown
<div align="center">

# Project Name

[![CI](https://img.shields.io/github/actions/workflow/status/USER/REPO/ci.yml?branch=main)](https://github.com/USER/REPO/actions)
[![Coverage](https://img.shields.io/codecov/c/github/USER/REPO)](https://codecov.io/gh/USER/REPO)
[![License](https://img.shields.io/github/license/USER/REPO)](LICENSE)
[![Version](https://img.shields.io/npm/v/PACKAGE)](https://npmjs.com/package/PACKAGE)

**One sentence: what it does, who it's for, and the key constraint or differentiator.**

[Demo](https://...) · [Docs](https://...) · [Report Bug](https://github.com/USER/REPO/issues)

</div>

---

## Features

- **Feature 1** — concrete behavior, not aspiration
- **Feature 2** — concrete behavior
- **Feature 3** — concrete behavior

---

## Quick Start

Get running in under 60 seconds:

\```bash
npm install package-name
\```

\```typescript
import { thing } from 'package-name'

const result = thing({ input: 'hello' })
console.log(result) // => expected output
\```

---

## Installation

### Prerequisites

- Runtime version (e.g., Node.js 18+)
- Required system dependencies

### Install

\```bash
npm install package-name
\```

### From source

\```bash
git clone https://github.com/USER/REPO.git
cd REPO
npm install
npm run build
\```

---

## Usage

### Basic

\```typescript
// Real working example — not pseudocode
\```

### Common use case

\```typescript
// Another real example with expected output
\```

---

## Configuration

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `option1` | `string` | `"default"` | What it controls |
| `option2` | `number` | `100` | What it controls |
| `option3` | `boolean` | `false` | What it controls |

### Environment Variables

Copy `.env.example` to `.env` and configure:

| Variable | Required | Description |
|----------|----------|-------------|
| `DATABASE_URL` | yes | PostgreSQL connection string |
| `PORT` | no | Server port (default: 3000) |

---

## Development

### Setup

\```bash
git clone https://github.com/USER/REPO.git
cd REPO
npm install
cp .env.example .env
\```

### Run locally

\```bash
npm run dev
\```

### Run tests

\```bash
npm test
npm run test:coverage
\```

### Lint and format

\```bash
npm run lint
npm run format
\```

---

## Architecture

> Include only when module structure or data flow is not obvious from the file tree.

\```
src/
├── api/        # HTTP handlers
├── domain/     # Business logic (no framework deps)
├── infra/      # Database, external services
└── shared/     # Types, utilities
\```

---

## Contributing

1. Fork the repository
2. Create a branch: `git checkout -b feature/your-feature`
3. Make changes and add tests
4. Run `npm test && npm run lint`
5. Push and open a Pull Request

---

## License

[MIT](LICENSE) © Author Name
```

## Badge Reference

Common badge sources (replace USER, REPO, PACKAGE):

```markdown
<!-- GitHub Actions -->
[![CI](https://img.shields.io/github/actions/workflow/status/USER/REPO/ci.yml?branch=main)](https://github.com/USER/REPO/actions)

<!-- Coverage -->
[![Coverage](https://img.shields.io/codecov/c/github/USER/REPO)](https://codecov.io/gh/USER/REPO)

<!-- npm -->
[![npm](https://img.shields.io/npm/v/PACKAGE)](https://npmjs.com/package/PACKAGE)
[![Downloads](https://img.shields.io/npm/dm/PACKAGE)](https://npmjs.com/package/PACKAGE)

<!-- PyPI -->
[![PyPI](https://img.shields.io/pypi/v/PACKAGE)](https://pypi.org/project/PACKAGE/)

<!-- crates.io -->
[![Crates.io](https://img.shields.io/crates/v/PACKAGE)](https://crates.io/crates/PACKAGE)

<!-- License -->
[![License](https://img.shields.io/github/license/USER/REPO)](LICENSE)
```

## Quality Checklist

- [ ] Every code block has a language tag
- [ ] No placeholder text remains (no "TODO", "lorem ipsum", "your-thing-here")
- [ ] All links verified working
- [ ] Quick Start is copy-pasteable and works on first try
- [ ] Configuration table matches actual options (from source, not memory)
- [ ] Commands match the actual package manager (npm/pnpm/yarn/pip/cargo/etc.)
- [ ] Badges point to real CI/registry URLs
- [ ] Consistent heading hierarchy (H1 → H2 → H3)
- [ ] Sections without content removed (not left empty)
- [ ] `.env.example` section matches actual required env vars
