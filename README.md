# ARX Backend

[![Version](https://img.shields.io/badge/version-2.0.0-111827)](https://github.com/aryanibos/arx-backend/releases)
[![License: MIT](https://img.shields.io/badge/license-MIT-16a34a.svg)](LICENSE)
[![Codex Plugin](https://img.shields.io/badge/Codex-plugin-111827)](https://developers.openai.com/plugins/)
[![Agent Skill](https://img.shields.io/badge/Agent%20Skill-cross--agent-7c3aed)](https://skills.sh/)

**ARX Backend** is a reusable backend engineering skill for AI coding agents. The skill is named **`arx-be`** and supports backend implementation, debugging, refactoring, and code review while preserving the architecture and conventions of the project it is working in.

> Project-specific architecture always wins. `arx-be` provides strong defaults and review discipline, but it never silently replaces an approved HLD, ADR, repository convention, or explicit task instruction.

## Version 2.0

Version 2.0 restructures the skill around progressive loading:

- `SKILL.md` is the control plane for precedence, workflow, verification, and output contracts.
- Domain standards are loaded from `references/` only when needed.
- `agents/openai.yaml` provides ChatGPT skill UI metadata.
- `skills/arx-be/` is the canonical source of truth.
- The Codex plugin copy is synchronized with repository scripts to prevent drift.

## Install

### Cross-agent

```bash
npx skills add aryanibos/arx-backend
```

### Codex plugin marketplace

```bash
codex plugin marketplace add aryanibos/arx-backend
```

## Coverage

| Area | Focus |
| --- | --- |
| Architecture | Project-first boundaries and layered REST when appropriate |
| TypeScript | Strict typing, safe narrowing, dependency discipline |
| API | REST contracts, validation, errors, pagination, idempotency |
| Database | PostgreSQL, Drizzle, migrations, transactions, constraints |
| Async | Redis, BullMQ, retries, idempotency, graceful shutdown |
| Storage | S3-compatible storage, uploads, signed URL safety |
| Security | AuthN/AuthZ, object access, secrets, SSRF/path/file risks |
| Testing | Unit, integration, contract tests, deterministic verification |
| Reliability | Partial failures, transaction boundaries, retry semantics |
| Review | Correctness, security, data integrity, maintainability |

## Default preferences

Only when the project has not selected alternatives: TypeScript, Bun, Hono, PostgreSQL, Drizzle ORM, Zod, Redis/BullMQ, S3-compatible storage, Docker, `bun:test`, and Pino.

## Usage

```text
Use arx-be to implement this backend task while following the project's architecture and coding standards.
```

```text
Use arx-be to trace this backend failure to its root cause, make the smallest safe fix, and add regression coverage.
```

```text
Use arx-be to review this backend change for correctness, security, data integrity, transaction boundaries, failure behavior, tests, and maintainability.
```

## Progressive references

- `backend-standard.md` — architecture and module boundaries
- `typescript-standard.md` — TypeScript and dependencies
- `api-standard.md` — HTTP/REST contracts
- `database-standard.md` — PostgreSQL/Drizzle/schema/migrations
- `security-standard.md` — auth, secrets, and security risks
- `async-workers.md` — Redis/BullMQ/background processing
- `storage-standard.md` — S3-compatible storage and uploads
- `testing-verification.md` — tests and quality gates
- `review-checklist.md` — backend/PR review

## Repository structure

```text
skills/arx-be/                         # canonical source
  SKILL.md
  agents/openai.yaml
  references/

scripts/
  sync-skill.sh
  check-skill-sync.sh

plugins/arx-be/
  .codex-plugin/plugin.json
  skills/arx-be/                       # synchronized copy
```

## Synchronization

After changing `skills/arx-be/`, run:

```bash
./scripts/sync-skill.sh
./scripts/check-skill-sync.sh
```

## Security

Never commit production credentials, API keys, access tokens, passwords, private keys, secret `.env` files, or sensitive signed URLs.

## Versioning

Current version: **`2.0.0`**. See `CHANGELOG.md` for release changes.
