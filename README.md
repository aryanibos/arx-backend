# ARX Backend

[![Version](https://img.shields.io/badge/version-2.0.0-111827)](https://github.com/aryanibos/arx-backend/releases)
[![License: MIT](https://img.shields.io/badge/license-MIT-16a34a.svg)](LICENSE)
[![Codex Plugin](https://img.shields.io/badge/Codex-plugin-111827)](https://developers.openai.com/plugins/)
[![Agent Skill](https://img.shields.io/badge/Agent%20Skill-cross--agent-7c3aed)](https://skills.sh/)

**ARX Backend** is a reusable backend engineering skill for AI coding agents. The skill is named **`arx-be`** and supports backend implementation, debugging, refactoring, and code review while preserving the architecture and conventions of the project it is working in.

> Project-specific architecture always wins. `arx-be` provides strong defaults and review discipline, but it never silently replaces an approved HLD, ADR, repository convention, or explicit task instruction.

## Version 2.0 release-candidate status

Version 2.0 is intentionally not tagged yet. The repository is being hardened before the public `v2.0.0` release.

Current development version: **`2.0.0`**.

Release gates now include:

- structural repository and skill validation
- canonical/plugin distribution synchronization
- deterministic contract evals
- positive, negative-trigger, and adversarial behavioral fixtures
- deterministic `skill.zip` packaging and integrity verification
- CI enforcement on pushes and pull requests

A release tag should only be created after critical behavioral fixtures have also been executed against the intended target agents and meet the scoring policy in `evals/README.md`.

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

## Quality gates

Run all deterministic release checks locally:

```bash
python scripts/validate_repo.py
python scripts/run_evals.py
./scripts/check-skill-sync.sh
python scripts/package_skill.py
```

The package command creates `dist/skill.zip` only after repository validation passes.

The eval suite intentionally separates deterministic policy/fixture validation from real target-agent behavior. See `evals/README.md` for the v2 release scoring threshold.

## Progressive references

- `backend-standard.md` - architecture and module boundaries
- `typescript-standard.md` - TypeScript and dependencies
- `api-standard.md` - HTTP/REST contracts
- `database-standard.md` - PostgreSQL/Drizzle/schema/migrations
- `security-standard.md` - auth, secrets, and security risks
- `async-workers.md` - Redis/BullMQ/background processing
- `storage-standard.md` - S3-compatible storage and uploads
- `testing-verification.md` - tests and quality gates
- `review-checklist.md` - backend/PR review

## Repository structure

```text
skills/arx-be/                         # canonical source
  SKILL.md
  agents/openai.yaml
  references/

evals/
  cases.json
  README.md

scripts/
  validate_repo.py
  run_evals.py
  package_skill.py
  sync-skill.sh
  check-skill-sync.sh

.github/workflows/
  validate.yml

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

Current development version: **`2.0.0`**. It remains untagged until the v2 release gates pass.
