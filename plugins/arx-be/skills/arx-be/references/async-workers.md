# Async Workers and Redis Standard

Use this reference for Redis, BullMQ, background jobs, retries, and asynchronous processing.

## Redis

Use Redis for caching, ephemeral coordination, rate limiting, or queue infrastructure when appropriate. Do not use it as the only durable source of important business state unless the project explicitly requires that design.

## Job payloads

Prefer payloads that contain identifiers and minimal execution context rather than large documents or sensitive bodies.

Version long-lived job payloads when producers and consumers may deploy independently or old jobs may remain queued across releases.

## Idempotency and side effects

Make jobs idempotent when retries or duplicate delivery are possible. Protect external side effects from accidental duplication.

Persist enough durable state to distinguish not-started, in-progress, completed, and failed work when the business process needs recovery visibility.

## Retry policy

- retry transient failures only
- bound retries
- use backoff and jitter where appropriate
- distinguish permanent validation/business failures from dependency failures
- define failed/dead-letter handling according to operational requirements

Do not create infinite retry loops.

## Acknowledgement and consistency

Acknowledge completion only after the required durable state and side effects are safe according to the job's delivery semantics.

For DB + queue coordination, explicitly consider the window between committing database state and publishing/acknowledging a job. Use an outbox or other reliability pattern only when delivery guarantees justify it.

## Worker lifecycle

Handle graceful shutdown:

- stop accepting new work
- allow in-flight jobs to finish or return safely according to library semantics
- close Redis/database/storage clients
- preserve visibility into interrupted work

## Observability

Log structured fields such as `jobId`, job name/version, attempt number, operation, duration, dependency, and final state. Never log secret or unnecessarily sensitive job payloads.

For library behavior that is version-sensitive, verify current official BullMQ/Redis documentation when available.
