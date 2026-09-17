# Database Standard

## PostgreSQL
Prefer PostgreSQL for relational application state when not otherwise specified.

## Naming
Default:
- tables: plural snake_case
- columns: snake_case
- indexes: descriptive snake_case
- UUID primary keys where appropriate
- timestamptz for timestamps

## Constraints
Use the database to enforce real invariants:
- NOT NULL
- UNIQUE
- FOREIGN KEY
- CHECK where appropriate

Do not rely only on application checks for invariants that must survive concurrency.

## Indexing
Add indexes for:
- demonstrated query patterns
- uniqueness
- common foreign-key access
- measured performance requirements

Avoid speculative indexing.

## Transactions
Transaction boundaries belong to the use case/service layer.

Repositories should support injected transaction handles where coordinated writes are required.

## Migrations
- use the approved migration tool
- never rewrite migrations already applied in shared environments
- keep logical changes focused
- rebase before generating migrations if branch conflicts are possible
- review locking/backfill risks
- verify clean-database application

## Query Review
Check:
- N+1
- unbounded scans
- missing filters
- unsafe dynamic SQL
- pagination
- lock behavior
- connection usage

## Integration Testing
Use disposable/local/CI database state. Never use production or a developer's normal persistent database for automated integration tests.
