# Database Standard

Use this reference for relational schema, PostgreSQL, Drizzle, transactions, migrations, indexing, and query review.

## Database choice and naming

Prefer PostgreSQL only when the project has not already selected another data store.

When no project convention exists, default to:

- plural `snake_case` tables
- `snake_case` columns
- descriptive `snake_case` indexes and constraints
- UUID primary keys where appropriate
- `timestamptz` timestamps
- `created_at` and `updated_at` for mutable records where useful

## Constraints and invariants

Use the database to enforce invariants that must survive concurrency:

- `NOT NULL`
- `UNIQUE`
- `FOREIGN KEY`
- `CHECK` where appropriate

Do not rely only on application pre-checks for concurrency-sensitive uniqueness or referential integrity.

## Transactions

A transaction should protect one logical atomic database operation.

Keep transaction orchestration in the application/service layer when the architecture supports it. Allow repositories to use an injected transaction handle when coordinated writes are required.

Think about isolation, locking, retries, and deadlocks for concurrent operations.

A database transaction cannot atomically commit S3, Redis, queue, or external-API side effects. Model those failure windows separately using idempotency, outbox/state-machine patterns, or compensating actions only when requirements justify them.

## Migrations

- use the project's approved migration tool
- never rewrite migrations already applied in shared environments
- keep migrations focused and reviewable
- review lock duration, backfill cost, defaults, and nullability transitions
- preserve backward compatibility during rolling deploys when required
- verify clean-database application when practical
- keep generated migration state synchronized with schema definitions

## Indexing

Add indexes for demonstrated access patterns, uniqueness, common foreign-key access, or measured performance requirements.

Avoid speculative indexing. Review write amplification and index size where relevant.

## Query review

Check for:

- N+1 access patterns
- unbounded scans or lists
- missing tenant/resource filters
- unsafe dynamic SQL
- pagination correctness
- unexpected lock behavior
- transaction scope
- connection usage and pool pressure
- unnecessary round trips

Inspect query plans for performance-sensitive work instead of guessing.

## Integration testing

Use disposable/local/CI database state for automated integration tests. Never point automated tests at production or a developer's normal persistent database.
