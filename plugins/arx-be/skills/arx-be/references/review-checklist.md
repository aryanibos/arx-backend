# Backend Review Checklist

Use only applicable items. Prioritize real merge risk over stylistic preference.

## Correctness

- [ ] Acceptance criteria are implemented.
- [ ] State transitions and edge cases are correct.
- [ ] Failure paths do not leave unsafe or contradictory state.
- [ ] No unrelated behavior change was introduced.

## Architecture

- [ ] Project HLD/ADR/repository conventions are preserved.
- [ ] Transport, business, and persistence responsibilities are separated according to project architecture.
- [ ] Transaction boundaries live at the correct application boundary.
- [ ] Cross-module dependencies use intentional public contracts.
- [ ] No new pattern or abstraction was introduced without a real need.

## Data integrity

- [ ] Database constraints protect concurrency-sensitive invariants.
- [ ] Transaction scope is correct and not unnecessarily broad.
- [ ] Partial failure across DB/queue/storage/external APIs is considered.
- [ ] Migration is forward-safe and compatible with deployment strategy.
- [ ] Query patterns are bounded and correctly scoped.

## Security

- [ ] Authentication requirement is correct.
- [ ] Authorization is server-side and resource-scoped where required.
- [ ] External input is validated at the correct boundary.
- [ ] Injection, SSRF, path/file, and deserialization risks are considered where applicable.
- [ ] Secrets and sensitive values are not committed, returned, or logged.
- [ ] Errors are sanitized.
- [ ] Rate/resource abuse is considered for expensive endpoints or uploads.

## Queue / worker

- [ ] Job behavior is idempotent where retries/duplicates are possible.
- [ ] Retry policy distinguishes transient and permanent failures.
- [ ] Payload compatibility/versioning is adequate for queued lifetime.
- [ ] Large or sensitive data is not queued unnecessarily.
- [ ] Graceful shutdown and interrupted work are safe.

## Storage / uploads

- [ ] Storage access is private and authorized.
- [ ] Signed URL expiry is bounded.
- [ ] Credentials and signed URLs are not logged.
- [ ] Object keys avoid raw untrusted filenames and unnecessary sensitive data.
- [ ] DB/storage partial-failure behavior is understood.
- [ ] Upload limits and content validation are appropriate.

## Testing

- [ ] Happy path is tested.
- [ ] Important error paths are tested.
- [ ] Authorization-negative paths are tested where relevant.
- [ ] Regression coverage exists for fixed bugs when practical.
- [ ] Integration/migration behavior is tested where boundary behavior matters.
- [ ] Tests do not depend on production services or execution order.

## Maintainability

- [ ] Types remain strict and unsafe escapes are justified narrowly.
- [ ] No stale/dead/debug code remains.
- [ ] Responsibilities remain understandable.
- [ ] Comments explain non-obvious reasons or invariants.
- [ ] New dependencies are justified.

## Verification

- [ ] Relevant targeted checks pass.
- [ ] Repository quality gates pass or gaps are explicitly reported.
- [ ] Final diff was reviewed.
- [ ] Secret/debug/generated-artifact checks were completed.
