# Backend Review Checklist

Use only applicable items.

## Correctness
- [ ] Acceptance criteria are actually implemented.
- [ ] Edge cases and failure paths are handled.
- [ ] No unrelated scope was introduced.

## Architecture
- [ ] Route only registers HTTP/middleware.
- [ ] Handler has no direct database queries.
- [ ] Service owns business orchestration.
- [ ] Repository owns persistence only.
- [ ] Service does not depend on HTTP framework context.
- [ ] Cross-module boundaries are explicit.
- [ ] No architecture drift from HLD/ADR.

## Data
- [ ] Constraints protect real invariants.
- [ ] Transaction boundary is correct.
- [ ] Partial failure across DB/queue/storage is considered.
- [ ] Migration is forward-safe.
- [ ] Indexes have a real reason.
- [ ] Query patterns are bounded.

## Security
- [ ] Authentication requirement is correct.
- [ ] Authorization is server-side.
- [ ] Object-level authorization exists where required.
- [ ] Input is validated.
- [ ] Secrets are not committed/logged.
- [ ] Errors are sanitized.
- [ ] Storage access is private/authorized.
- [ ] Resource abuse/file size/rate concerns are considered.

## Queue / Worker
- [ ] Job is idempotent where retries are possible.
- [ ] Retry policy distinguishes transient/permanent failures.
- [ ] Job payload is versioned if long-lived.
- [ ] Large/sensitive content is not placed in queue unnecessarily.
- [ ] Graceful shutdown is safe.

## Storage
- [ ] Business logic is provider-neutral.
- [ ] No credentials or signed URLs in logs.
- [ ] Object keys avoid unnecessary sensitive data.
- [ ] Signed URL expiry is bounded.

## Testing
- [ ] Happy path tested.
- [ ] Important error paths tested.
- [ ] Authorization-negative case tested when applicable.
- [ ] Migration/integration behavior tested when relevant.
- [ ] Tests do not depend on production services.

## Maintainability
- [ ] Types are strict.
- [ ] No `any`.
- [ ] No `@ts-ignore`.
- [ ] No god file/module.
- [ ] No speculative abstraction.
- [ ] Comments explain why.
- [ ] Dependencies are justified.

## Verification
- [ ] Type-check passes.
- [ ] Lint passes.
- [ ] Format check passes.
- [ ] Tests pass.
- [ ] Build passes.
- [ ] Diff reviewed.
- [ ] Secret/debug artifact check completed.
