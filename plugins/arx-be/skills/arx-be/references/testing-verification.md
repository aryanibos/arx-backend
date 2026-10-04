# Testing and Verification Standard

Use this reference when adding tests, changing behavior, reviewing quality gates, or preparing a final completion report.

## Test behavior, not implementation trivia

For Bun projects prefer `bun:test` unless the project already uses another approved runner.

Choose the lowest-cost test level that proves the important behavior, then add integration/contract coverage where boundaries matter.

## Unit tests

Use for:

- validation
- business/service rules
- error mapping
- pure utilities
- deterministic policy logic

## Integration tests

Use for:

- repositories against disposable PostgreSQL
- Redis/queue adapters
- object-storage adapters
- migrations
- API wiring where framework/database behavior matters

Avoid real production dependencies and developer-personal persistent services.

## Contract tests

Use where compatibility matters, including:

- API response envelopes and stable error codes
- queue payloads
- storage adapter behavior
- third-party adapter mapping

## Coverage priorities

Include applicable cases:

- happy path
- meaningful error path
- authorization-negative path
- concurrency/idempotency edge cases
- migration or compatibility behavior
- acceptance-criteria edge cases

Do not add meaningless assertions solely to increase coverage numbers.

## Verification order

1. run focused tests/checks for the changed area
2. run the repository's canonical quality command when available
3. otherwise run applicable type-check, lint, format check, tests, and build
4. inspect final diff/status
5. check for secrets, `.env`, debug code, generated artifacts, and unrelated changes

Useful repository checks when available:

```bash
git diff --check
git status --short
```

## Reporting

Record commands actually executed and their result. Do not report PASS for skipped, unavailable, or inferred checks.

If a command cannot run, state the command, the failure, the cause, and whether it appears to be an environment limitation or a code failure.
