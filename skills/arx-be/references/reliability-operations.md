# Reliability and Operations Standard

Use this reference for outbound HTTP/SDK calls, runtime configuration, health checks, and HTTP server lifecycle.

## Outbound calls

- Give every outbound network call an explicit timeout; never rely on an unbounded library default.
- Keep the total time budget of a request below the caller's own timeout, including retries.
- Retry only transient failures (timeouts, connection resets, 429, 502, 503, 504) and only when the operation is idempotent or protected by an idempotency key.
- Bound retries and use exponential backoff with jitter. Honor `Retry-After` when the dependency sends it.
- Bound concurrency toward slow or rate-limited dependencies.
- Add circuit breaking or bulkheads only when a measured dependency failure mode justifies them.
- Map dependency failures to stable application errors; do not leak provider responses to clients.

## Transactions and network I/O

Do not hold a database transaction open across network calls to external APIs, object storage, or queues. A slow dependency then holds row locks and pool connections, amplifying an outage.

Prefer: read and decide, commit, then perform the side effect with idempotency; or record intent in the transaction and perform the side effect afterwards (outbox/state machine) when delivery guarantees require it.

## Configuration

- Load configuration once at startup and validate it against a schema (for example Zod) with typed output.
- Fail fast with a clear message when required configuration is missing or invalid; do not start in a half-configured state.
- Never default secrets to placeholder values in code.
- Do not print secret values in validation errors or startup logs; name the missing key only.
- Keep environment-specific behavior in configuration, not in scattered `NODE_ENV` checks.

## Health checks

- Liveness reports only whether the process can make progress; do not check external dependencies in liveness, or a dependency outage restarts every instance.
- Readiness reports whether the instance can serve traffic now, including required dependencies such as the database.
- Keep health checks cheap, bounded by timeouts, and free of sensitive details.

## HTTP server lifecycle

On shutdown signals:

1. fail readiness so new traffic drains away
2. stop accepting new connections
3. let in-flight requests finish within a bounded grace period
4. close database, Redis, queue, and storage clients
5. exit with a meaningful status code

Apply the worker-specific rules in `async-workers.md` for background consumers.

## Observability

Emit structured logs, and metrics or traces where the project supports them, for dependency latency, timeouts, retries, and error rates. Correlate them with request or job IDs.
