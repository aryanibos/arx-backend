# ARX Backend

[![Version](https://img.shields.io/badge/version-0.1.0-111827)](https://github.com/aryanibos/arx-backend/releases)
[![License: MIT](https://img.shields.io/badge/license-MIT-16a34a.svg)](LICENSE)
[![Codex Plugin](https://img.shields.io/badge/Codex-plugin-111827)](https://developers.openai.com/plugins/)
[![Backend Engineering](https://img.shields.io/badge/focus-backend%20engineering-2563eb)](#what-arx-be-covers)

**ARX Backend** is a reusable backend engineering skill for Codex focused on building and reviewing backend systems that are **maintainable, secure, type-safe, testable, and production-oriented**.

The bundled skill is named **`arx-be`**.

> Project-specific architecture always wins. `arx-be` provides strong defaults and review discipline, but it never silently replaces an approved HLD, ADR, repository convention, or explicit task instruction.

---

## What `arx-be` covers

| Area | Focus |
| --- | --- |
| Architecture | Route → Handler → Service → Repository, module boundaries, low coupling |
| API | REST contracts, validation, error envelopes, pagination, idempotency |
| Type safety | Strict TypeScript, Zod, safe narrowing, no `any` by default |
| Database | PostgreSQL, Drizzle, migrations, transactions, constraints, indexing |
| Async processing | Redis, BullMQ, retries, idempotency, graceful shutdown |
| Storage | S3-compatible storage, MinIO, AWS S3, signed URL safety |
| Security | AuthN/AuthZ, object-level access, secrets, logging redaction, input safety |
| Testing | Unit, integration, contract tests, deterministic verification |
| Reliability | Partial failures, transaction boundaries, queue/storage consistency |
| Review | Correctness, security, data integrity, maintainability, performance |

## Default preferences

When a project has **not** already selected alternatives, `arx-be` prefers:

- TypeScript
- Bun
- Hono
- PostgreSQL
- Drizzle ORM
- Zod
- Redis / BullMQ
- S3-compatible object storage
- Docker
- `bun:test`
- Pino structured logging

These are preferences—not forced replacements for an existing project stack.

---

## Install

Add this repository as a Codex plugin marketplace source:

```bash
codex plugin marketplace add aryanibos/arx-backend
```

Then restart the supported ChatGPT/Codex host if required and install **ARX BE** from the added marketplace source.

Verify configured marketplaces:

```bash
codex plugin marketplace list
```

Refresh marketplace updates later with:

```bash
codex plugin marketplace upgrade
```

Codex supports GitHub marketplace sources using `owner/repo` syntax.

---

## Usage

### Implement backend work

```text
Use arx-be to implement this backend task while following the project's architecture and coding standards.
```

### Review backend code

```text
Use arx-be to review this backend change for correctness, security, data integrity, transaction boundaries, tests, and maintainability.
```

### Review a pull request

```text
Use arx-be in review mode. Prioritize blocker/high-severity findings and separate merge blockers from optional improvements.
```

---

## Engineering philosophy

`arx-be` optimizes for:

1. Correctness
2. Security
3. Data integrity
4. Maintainability
5. Explicit architecture
6. Testability
7. Reliability
8. Observability
9. Evidence-based performance work
10. Simple implementation over unnecessary abstraction

The goal is **boring, explicit, reviewable backend code**.

It intentionally discourages:

- speculative abstractions
- framework churn
- hidden side effects
- business logic in HTTP handlers
- database access from presentation layers
- over-engineered dependency injection
- unbounded retries
- secret leakage
- claiming tests passed without running them

---

## Backend boundary

The default layered direction is:

```text
Route
  ↓
Handler
  ↓
Service
  ↓
Repository
  ↓
Database / Infrastructure
```

### Route

Owns route registration, HTTP method/path, and middleware composition.

### Handler

Owns HTTP translation, request parsing, validation, service invocation, and response mapping.

### Service

Owns business rules, orchestration, transaction boundaries, and coordination with repositories/infrastructure ports.

### Repository

Owns persistence and database queries—not HTTP or business policy.

This model is a default. Existing approved project architecture takes precedence.

---

## Review priorities

When reviewing backend changes, `arx-be` checks in this order:

1. Correctness
2. Security
3. Data integrity
4. Transaction boundaries
5. Authorization
6. Failure and retry behavior
7. Architecture boundaries
8. Tests
9. Maintainability
10. Performance
11. Style

Findings are classified as:

- **Blocker**
- **High**
- **Medium**
- **Low**

Each finding should explain the location, problem, impact, and recommended fix.

---

## Repository structure

```text
.
├── .agents/
│   └── plugins/
│       └── marketplace.json
├── plugins/
│   └── arx-be/
│       ├── .codex-plugin/
│       │   └── plugin.json
│       └── skills/
│           └── arx-be/
│               ├── SKILL.md
│               └── references/
│                   ├── api-standard.md
│                   ├── backend-standard.md
│                   ├── database-standard.md
│                   └── review-checklist.md
├── CHANGELOG.md
├── CONTRIBUTING.md
├── LICENSE
└── README.md
```

The skill's main behavior lives in [`SKILL.md`](plugins/arx-be/skills/arx-be/SKILL.md). More focused rules live under [`references/`](plugins/arx-be/skills/arx-be/references/).

---

## Security

This repository must never contain:

- `.env` files
- cloud credentials
- API keys
- access tokens
- passwords
- private keys
- production secrets
- signed URLs containing sensitive access

`arx-be` favors least privilege, server-side authorization, sanitized errors, structured logging, and secret redaction.

---

## Versioning

Current version: **`0.1.0`**

The project follows semantic versioning:

```text
v0.1.0  Initial public skill
v0.1.1  Backward-compatible fixes / rule improvements
v0.2.0  Meaningful workflow or behavior additions
v1.0.0  Stable public contract
```

See [`CHANGELOG.md`](CHANGELOG.md) for published changes.

---

## Contributing

Contributions and improvements are welcome. Please read [`CONTRIBUTING.md`](CONTRIBUTING.md) before opening a pull request.

A contribution should keep the skill project-agnostic, avoid weakening security/type-safety rules without justification, and preserve the rule that **project-specific standards override personal defaults**.
