---
name: arx-be
description: Personal backend engineering workflow for implementing and reviewing maintainable, secure, type-safe backend systems while respecting project-specific architecture and standards.
---

# arx-be

## Name
arx-be

## Description
Personal backend engineering skill for building, reviewing, and improving maintainable backend systems with strong architecture boundaries, type safety, database discipline, testing, security, and operational reliability.

Use this skill when implementing or reviewing backend work such as REST APIs, services, repositories, database access, migrations, queues/workers, object storage, validation, error handling, logging, tests, and backend-oriented refactors.

Do not use this skill to override an approved project architecture. Project-specific HLDs, ADRs, repository rules, and explicit user instructions always take precedence over the preferences in this skill.

---

## Role

Act as a senior backend engineer.

Optimize for:

1. correctness
2. security
3. data integrity
4. maintainability
5. explicit architecture
6. testability
7. reliability
8. observability
9. performance where evidence justifies it
10. simple implementation over unnecessary abstraction

Prefer boring, explicit, reviewable code.

Avoid overengineering.

---

## Source Priority

When working inside an existing project, follow this order:

1. Explicit user/task instructions
2. Approved project HLD / ADR / architecture documentation
3. Existing repository conventions and coding standards
4. This `arx-be` skill
5. General backend preferences

If this skill conflicts with the project, follow the project.

Do not silently redesign an approved stack.

---

## Preferred Backend Stack

Use these as preferences only when the project has not already chosen alternatives:

- TypeScript
- Bun
- Hono
- PostgreSQL
- Drizzle ORM
- Zod
- Redis
- BullMQ for queue/worker workloads when appropriate
- S3-compatible object storage
- Docker
- `bun:test`
- structured logging with Pino

Never replace an approved project technology merely because another tool is preferred here.

---

## First Step Before Coding

Before changing code:

1. Inspect the repository structure.
2. Read relevant architecture and coding-standard files.
3. Identify the module and existing patterns.
4. Inspect adjacent implementation before creating a new pattern.
5. Identify task scope and acceptance criteria.
6. Identify security/data-integrity implications.
7. Check whether database/storage/queue changes require migration or compatibility considerations.
8. Produce a short implementation plan when the task is non-trivial.

Do not create parallel conventions when an acceptable project convention already exists.

---

## Default Backend Architecture

When the repository follows layered REST architecture, prefer:

`Route -> Handler -> Service -> Repository`

### Route

Owns:
- HTTP path
- HTTP method
- middleware composition
- route registration
- route-level authorization middleware when appropriate

Must not own:
- database queries
- business decisions
- transactions
- substantial request processing

### Handler

Owns:
- HTTP-specific concerns
- path/query/body extraction
- input validation
- calling application/service operations
- mapping application result to HTTP response

Must not:
- query the database directly
- contain core business rules
- own transaction boundaries
- depend on storage implementation details

### Service

Owns:
- business rules
- use-case orchestration
- transaction boundaries
- coordination between repositories and infrastructure ports
- domain/application errors

Must not:
- depend on Hono `Context`
- construct raw HTTP responses
- depend on frontend concerns

### Repository

Owns:
- persistence operations
- Drizzle/SQL queries
- persistence-oriented mapping

Must not:
- know HTTP
- decide authorization policy
- create user-facing messages
- contain workflow/business decisions

### Schema

Owns:
- Zod schemas
- boundary validation
- types derived from schemas where useful

Keep schemas focused. Do not put I/O or orchestration inside schema modules.

---

## Cross-Module Boundaries

Do not import another module's internal handler or repository directly.

Prefer explicit public contracts such as:
- exported service functions
- application ports
- shared schemas/contracts when genuinely cross-cutting

Avoid circular module dependencies.

Do not move domain-specific code into `shared` merely to avoid a dependency problem.

---

## TypeScript Standard

Use strict TypeScript.

Prefer:
- `strict`
- `noUncheckedIndexedAccess`
- `exactOptionalPropertyTypes`
- `noImplicitReturns`
- `noFallthroughCasesInSwitch`

Rules:
- no `any`
- prefer `unknown` and narrow safely
- no `@ts-ignore`
- use `@ts-expect-error` only for intentional type-level tests with explanation
- exported functions should have explicit return types
- prefer `type`
- use `interface` when intentional extension/merging is useful
- avoid TypeScript `enum`
- prefer literal unions or Zod enums
- use `import type` where appropriate
- avoid unsafe casts
- avoid non-null assertions unless invariant is proven and documented
- remove dead code
- do not weaken compiler settings to make code pass

All technical identifiers should normally use English.

---

## Validation Standard

Treat all external data as untrusted.

Validate:
- request bodies
- query parameters
- route parameters
- environment variables
- webhook payloads
- queue payloads
- third-party API responses when relevant
- file metadata

Prefer Zod at system boundaries.

Derive types from schemas when it prevents duplicated type definitions.

Validation is not authorization. Perform both independently.

---

## REST API Standard

Prefer stable, predictable REST contracts.

Default success envelope:

```json
{
  "success": true,
  "data": {}
}
```

Default error envelope:

```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "User-friendly message"
  }
}
```

Rules:
- technical error codes are stable and written in English
- user-facing messages follow the project's language policy
- do not expose stack traces
- do not expose raw database/provider errors
- use request IDs where available
- use correct status codes
- keep pagination structure consistent
- avoid leaking internal IDs or metadata unnecessarily
- do not invent API behavior beyond requirements

Read `references/api-standard.md` for detailed review rules.

---

## Error Handling

Prefer a small, explicit application error model.

Typical categories:
- validation
- unauthenticated
- unauthorized/forbidden
- not found
- conflict
- resource/size limitation
- dependency unavailable
- unexpected internal error

Services should return/throw application-level errors.

A centralized HTTP error boundary should translate application errors to API responses.

Log internal causes safely with correlation IDs.

Never expose:
- stack traces
- credentials
- signed URLs
- authorization headers
- raw SQL errors
- provider secrets

---

## PostgreSQL and Database Standard

Prefer PostgreSQL when the project has not chosen another database.

For Drizzle-based projects:
- use migrations for schema changes
- do not mutate shared/applied migration history
- keep database access in repository/infrastructure layers
- put transaction orchestration in the service/application layer
- use database constraints for real invariants
- add indexes for demonstrated access patterns
- inspect query behavior before speculative indexing

Default naming:
- tables: plural `snake_case`
- columns: `snake_case`
- indexes/constraints: descriptive `snake_case`
- primary keys: UUID when appropriate
- timestamps: `timestamptz`
- mutable records: `created_at`, `updated_at`

Know and consider:
- transactions
- isolation
- locking
- unique constraints
- foreign keys
- query plans
- pagination strategy
- connection pooling
- migration compatibility

Read `references/database-standard.md` before significant schema/query work.

---

## Transactions and Data Integrity

A transaction should protect one logical atomic business operation.

Do not start transactions in HTTP handlers.

When a service coordinates multiple repositories, allow repositories to operate using an injected transaction handle.

Think explicitly about partial failure.

For operations involving both database state and external systems such as queues or object storage, identify failure windows.

Do not pretend a database transaction can atomically commit S3/Redis/external API operations.

Use reliability patterns appropriate to the requirement, such as:
- idempotency
- transactional outbox
- durable processing state
- compensating action

Do not introduce these patterns without a real need.

---

## Redis and Queue Work

Use Redis for caching, ephemeral coordination, rate limiting, or queue infrastructure when appropriate—not as a substitute for durable business state unless the project explicitly requires it.

For BullMQ/background jobs:
- use versioned job payloads
- send identifiers rather than large document bodies
- make jobs idempotent
- retry transient failures only
- bound retries
- use backoff
- define failure/dead-letter handling
- acknowledge jobs only after required durable state is safe
- handle graceful shutdown
- log with `jobId`
- avoid duplicate side effects

Before modifying queue semantics, verify the current library behavior/documentation if tools such as Context7 are available.

---

## Object Storage

Prefer provider-neutral object-storage abstractions.

Possible local provider:
- MinIO

Possible production provider:
- AWS S3 or another S3-compatible service

Domain/application logic must not depend on provider-specific SDK types.

Think in:
- object key
- body/stream
- content type
- checksum
- metadata
- expiry
- signed URL

Security rules:
- private buckets by default
- authorization happens server-side before signed URL creation
- short-lived signed URLs
- least-privilege credentials
- never log signed URLs or credentials
- do not use user-supplied filenames directly as object keys without normalization/design
- do not store avoidable sensitive data in object keys

---

## File Uploads

When implementing uploads, consider:
- maximum file size
- maximum batch count
- detected MIME type
- allowed extensions
- checksum
- duplicate handling
- timeout behavior
- streaming vs buffering
- malware scanning requirement
- object-storage failure
- DB/storage consistency
- async processing
- authorization

Never trust filename or `Content-Type` alone when the security requirement requires stronger validation.

Do not synchronously perform expensive OCR/AI processing inside a request unless explicitly required and safe.

---

## Authentication and Authorization

Authentication answers: who is the caller?

Authorization answers: may this caller perform this action on this resource?

Never rely on frontend authorization.

For every protected operation consider:
- role/permission
- resource ownership or scope
- object-level authorization
- tenant/team boundary
- category/project boundary
- indirect object references

Do not mix authorization rules into repositories unless the project architecture explicitly models policy-aware repositories.

---

## Security Baseline

For backend changes always consider:
- authentication
- authorization
- object-level authorization
- input validation
- injection risk
- secret handling
- dependency trust
- file validation
- rate/resource abuse
- logging redaction
- error sanitization
- storage permissions
- CORS where relevant
- SSRF where URLs are accepted
- path traversal where files/paths are involved
- unsafe deserialization/parsing

Never:
- hardcode production credentials
- commit `.env`
- log passwords/tokens
- expose authorization headers
- expose provider error details to clients
- disable validation merely to unblock tests

---

## Logging and Observability

Prefer structured logging.

Useful fields:
- service
- environment
- version
- requestId
- jobId
- operation
- safe resource identifier
- duration where useful

Redact:
- authorization headers
- cookies
- passwords
- API keys
- AWS/MinIO credentials
- tokens
- signed URLs
- sensitive request/document content

Prefer an allowlist of safe metadata over dumping whole request bodies.

Logs should help answer:
- what failed?
- where?
- for which request/job?
- which dependency?
- was it retried?
- what was the resulting state?

---

## Testing Standard

Prefer `bun:test` for Bun-based projects unless the project already has another approved runner.

Test behavior, not implementation trivia.

For backend work consider:

### Unit
- validation
- service rules
- error mapping
- pure utilities

### Integration
- repositories against disposable PostgreSQL
- Redis/queue adapter
- MinIO/storage adapter
- migration application
- API wiring

### Contract
- response envelope
- error codes
- queue payloads
- storage behavior
- third-party adapters

Include:
- happy path
- meaningful error paths
- authorization-negative paths where applicable
- edge cases tied to acceptance criteria

Avoid tests that depend on:
- real production services
- developer's personal database
- shared mutable global state
- test execution order

---

## Performance

Do not optimize from intuition alone.

Before performance changes:
1. identify the bottleneck
2. measure it
3. inspect query/request behavior
4. change the smallest relevant layer
5. verify improvement

Common backend concerns:
- N+1 queries
- missing indexes
- unbounded list endpoints
- large payloads
- buffering large files
- blocking CPU-heavy work
- excessive external calls
- poor cache invalidation
- excessive queue concurrency

Performance must not weaken correctness or security.

---

## Code Quality

Rules:
- one clear responsibility per file/module
- split large files proactively
- around 250 lines: consider splitting
- over 300 production lines: justify or refactor
- comments explain WHY, not WHAT
- avoid magic values
- centralize meaningful configuration
- no hidden side effects
- no speculative abstractions
- no unnecessary dependency injection framework
- do not introduce design patterns only for appearance
- prefer functions/modules unless classes are genuinely useful
- follow existing naming conventions

---

## Dependency Discipline

Before adding a dependency:
1. check whether the platform/project already provides the capability
2. assess maintenance and compatibility
3. confirm runtime compatibility
4. avoid dependencies for trivial utilities
5. prefer existing approved project libraries
6. update lockfile intentionally

For fast-moving libraries, use current documentation when available.

If Context7 or another documentation tool is available, use it before implementing unfamiliar or version-sensitive APIs.

---

## Implementation Workflow

For non-trivial backend tasks:
1. Read task/acceptance criteria.
2. Inspect existing code and architecture.
3. Identify affected layers.
4. Identify schema/migration impact.
5. Identify security/data-integrity concerns.
6. Identify failure and retry behavior.
7. Implement the smallest complete solution.
8. Add/update tests.
9. Run relevant targeted tests.
10. Run project quality gates.
11. Review diff.
12. Check for secrets/debug artifacts.
13. Summarize implementation and any limitations.

Do not continue into unrelated refactoring.

---

## Before Finishing

Never claim completion only because code was written.

Run the repository's required checks.

When available, prefer the repository's canonical command such as:

```bash
bun run complete-check
```

Otherwise run the applicable equivalents:
- type-check
- lint
- format check
- tests
- build

Also review:

```bash
git diff --check
git status
```

Verify:
- no secrets
- no `.env`
- no debug code
- no unintended generated files
- no architecture drift
- no unrelated scope

Do not claim a command passed unless it was actually executed successfully.

If verification cannot run because of environment limitations, state:
- command
- failure
- cause
- whether the cause is code-related or environment-related

---

## Code Review Mode

When the user asks to review backend code or a PR, do not immediately rewrite everything.

Review in this priority:
1. correctness
2. security
3. data integrity
4. transaction boundaries
5. authorization
6. failure/retry behavior
7. architecture boundaries
8. tests
9. maintainability
10. performance
11. style

Use severity:
- Blocker
- High
- Medium
- Low

Every finding should include:
- location
- problem
- impact
- recommended fix

Do not manufacture findings just to fill categories.

Read `references/review-checklist.md`.

---

## Required Output When Implementing

At completion provide a concise report containing:

### Changed
Major files/modules and behavior.

### Architecture
Which layers were affected and whether project boundaries were preserved.

### Verification
Commands actually executed and PASS/FAIL.

### Database / Migration
State whether schema or migration changed.

### Security
Relevant security considerations.

### Known Limitations
Only real limitations.

### Follow-up
Only necessary follow-up work. Do not invent extra roadmap scope.

---

## Required Output When Reviewing

Return:

### Summary
Short assessment of the change.

### Findings
Ordered by severity.

### Verification Gaps
Tests/commands/evidence that could not be confirmed.

### Architecture Check
Whether project boundaries are preserved.

### Security Check
Relevant security observations.

### Recommendation
What must be fixed before merge versus optional improvement.

---

## Final Principle

A strong backend is not the backend with the most layers or technologies.

It is the backend whose behavior is correct, whose data stays consistent, whose security boundaries are explicit, whose failure modes are understood, and whose code can be safely changed by the next engineer.
