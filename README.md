# ARX Backend

[![Version](https://img.shields.io/badge/version-0.1.0-111827)](https://github.com/aryanibos/arx-backend/releases)
[![License: MIT](https://img.shields.io/badge/license-MIT-16a34a.svg)](LICENSE)
[![Codex Plugin](https://img.shields.io/badge/Codex-plugin-111827)](https://developers.openai.com/plugins/)
[![Agent Skill](https://img.shields.io/badge/Agent%20Skill-cross--agent-7c3aed)](https://skills.sh/)
[![Backend Engineering](https://img.shields.io/badge/focus-backend%20engineering-2563eb)](#what-arx-be-covers)

**ARX Backend** is a reusable backend engineering skill for AI coding agents. It helps agents build and review backend systems that are **maintainable, secure, type-safe, testable, and production-oriented**.

The skill is named **`arx-be`**.

> Project-specific architecture always wins. `arx-be` provides strong defaults and review discipline, but it never silently replaces an approved HLD, ADR, repository convention, or explicit task instruction.

---

## Install

### Cross-agent install with `skills`

Install `arx-be` from GitHub with the cross-agent Skills CLI:

```bash
npx skills add aryanibos/arx-backend
```

The repository includes the conventional root skill path:

```text
skills/arx-be/SKILL.md
```

This makes the skill discoverable by tools that support the Agent Skills ecosystem. Depending on the CLI/agent, you can choose the target agent and whether the skill is installed locally or globally during installation.

Typical supported agent environments include tools such as **Codex, Claude Code, Cursor, OpenCode**, and other clients that understand Agent Skills.

### Codex plugin marketplace

For the richer Codex plugin packaging, add this repository as a marketplace source:

```bash
codex plugin marketplace add aryanibos/arx-backend
```

Then install **ARX BE** from the added marketplace source.

Verify configured marketplaces:

```bash
codex plugin marketplace list
```

Refresh marketplace updates later with:

```bash
codex plugin marketplace upgrade
```

### Which install should I use?

| Goal | Recommended command |
| --- | --- |
| Use `arx-be` across compatible AI coding agents | `npx skills add aryanibos/arx-backend` |
| Use the packaged Codex plugin/marketplace experience | `codex plugin marketplace add aryanibos/arx-backend` |

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
├── skills/                         # Cross-agent Agent Skills entrypoint
│   └── arx-be/
│       ├── SKILL.md
│       └── references/
│
├── .agents/
│   └── plugins/
│       └── marketplace.json
│
├── plugins/                        # Codex plugin packaging
│   └── arx-be/
│       ├── .codex-plugin/
│       │   └── plugin.json
│       └── skills/
│           └── arx-be/
│               ├── SKILL.md
│               └── references/
│
├── CHANGELOG.md
├── CONTRIBUTING.md
├── LICENSE
└── README.md
```

### Why are there two skill paths?

The root [`skills/arx-be/`](skills/arx-be/) path is the **cross-agent distribution entrypoint** used by Agent Skills tooling.

The [`plugins/arx-be/`](plugins/arx-be/) path packages the same behavior as a **Codex plugin** with marketplace metadata.

They intentionally represent the same `arx-be` skill so users can choose the installation experience that matches their agent.

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
