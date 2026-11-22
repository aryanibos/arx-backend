# Stack Resolution

Use this reference when the backend stack is not yet decided, or when a task asks which stack to use.

## Resolution order

Resolve the backend stack in this order. Stop at the first step that decides it:

1. Foundation first. If the project was built with arx-foundation or arx-lead, read the foundation docs (technical spec, decision log, ADRs) and take the backend stack recorded there. Build with it; do not ask again.
2. Existing project. If the repository already has a backend stack, keep it.
3. Standalone ask-gate. If there is no foundation and no existing stack, STOP and ask the user which backend stack to use before writing code. Present curated recommendations from the table below plus a choose-your-own option. Do not proceed until the user answers.
4. Foundation silent on stack. If a foundation exists but does not name a backend stack, ask. Never fall back silently to the recommended stack.

A stack the user did not choose and the foundation did not record is not a decision; it is a guess.

## Recommendation table

The table below is the curated recommendation set for the ask-gate. Every row is a recommendation, never a mandate. Present at most two or three fitting options plus choose-your-own; do not dump the whole table on the user.

### Framework

| Option | Fit when | Trade-off |
| --- | --- | --- |
| Hono | Small to medium TypeScript service; Bun or Node; minimal footprint | Small ecosystem; fewer batteries included than NestJS |
| Elysia | Bun-first TypeScript service; end-to-end type safety matters | Bun-coupled; smaller community than Express or NestJS |
| FastAPI | Python service; typed APIs; data or ML-adjacent work | Python runtime; async ORM patterns need care |
| NestJS | Large TypeScript team; structured modules; long-lived service | Heavier ceremony; slower to start a small service |
| Express | Node service needing the widest middleware ecosystem | Unopinionated; the team must set its own structure |

### Runtime, data, and tooling

| Layer | Recommended | Fit when | Trade-off |
| --- | --- | --- | --- |
| Runtime | Bun | TypeScript service; fast startup and tests matter | Younger runtime; some Node packages need checks |
| Runtime | Node.js | Widest TypeScript ecosystem; team already knows it | Slower startup than Bun; test runner is separate |
| Runtime | Python | FastAPI service; data or ML libraries required | Async patterns differ from Node; packaging needs discipline |
| ORM | Drizzle | TypeScript with PostgreSQL; SQL-close control wanted | Less magic than Prisma; more manual mapping |
| ORM | Prisma | TypeScript team wanting schema-first speed | Abstraction hides SQL; migrations need care |
| ORM | SQLAlchemy | Python with PostgreSQL; explicit control wanted | Verbose for simple CRUD; async setup needs care |
| Database | PostgreSQL | Relational data; transactions and constraints matter | Needs managed hosting or ops for production |
| Queue | Redis with BullMQ | TypeScript jobs; retries and delayed jobs needed | Redis is extra infrastructure; not durable alone |
| Validation | Zod | TypeScript; schema and types from one definition | TypeScript only |
| Validation | Pydantic | Python; FastAPI-native validation wanted | Python only |
| Logging | Pino | TypeScript; structured JSON logs wanted | TypeScript only; pick the equivalent logger per language |
| Testing | `bun:test` | Bun project; colocated fast tests wanted | Bun only; use the project's approved runner otherwise |

## Ask-gate format

Present these five parts, then wait:

- Recommendation: one stack, with the reason grounded in the source doc (scale, team, timeline, features, constraints).
- Alternatives: one or two other fitting options, each with its trade-off.
- Challenge: one specific risk or alternative the user should weigh before deciding.
- Choose your own: the user may name any stack instead.
- Record: the decision, the reason, the rejected alternatives, and the decider go into the decision log.

Stop, ask, wait. Silence is not agreement. Do not scaffold, install dependencies, or write stack-specific code before the gate closes.

## No silent fallback

If the foundation exists but does not name a backend stack, ask. If the user picks a stack the agent does not know well, say so and still build with it; do not steer the user back to the recommended stack without a named, concrete reason.

## Which references apply

- `backend-standard.md`, `api-standard.md`, `security-standard.md`, `storage-standard.md`, `reliability-operations.md`, `testing-verification.md`, `review-checklist.md`: principles apply to any stack.
- `typescript-standard.md`: applies only when the resolved stack is TypeScript. For another language, apply the same discipline (strict typing, no unsafe casts, dependency hygiene) with that language's equivalent tooling.
- `database-standard.md`: documents the recommended PostgreSQL and Drizzle stack in depth. For another database or ORM, apply the same rules (transactions, constraints, migration safety) with the chosen stack's equivalent.
- `async-workers.md`: documents the recommended Redis and BullMQ stack in depth. For another queue, apply the same rules (idempotency, retries, delivery semantics) with the chosen stack's equivalent.

## Decision-log example (fictional)

File: `docs/decisions/2026-11-22-backend-stack.md`

- Decision: backend stack is FastAPI on Python with PostgreSQL and SQLAlchemy.
- Reason: the source doc requires a Python data pipeline the team already maintains, and the team has no TypeScript experience.
- Rejected: Hono on Bun (faster startup, but the team would need to learn a new runtime); NestJS (richer structure, but heavier than the service needs).
- Challenge weighed: FastAPI async ORM patterns are less familiar to the team, so the first card includes a spike to prove the transaction pattern.
- Decider: project owner, 2026-11-22.
