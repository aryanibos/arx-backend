# Backend Architecture Standard

Use this reference for module design, boundary changes, and architecture review.

## Project architecture wins

Follow the repository's approved architecture. Do not mechanically introduce a layered REST structure into a project that already uses another coherent model.

When the project uses layered REST modules, prefer:

`Route -> Handler -> Service -> Repository`

## Route

Own:
- HTTP method and path
- route registration
- middleware composition
- route-level authorization middleware when appropriate

Do not own database queries, transactions, business decisions, or substantial request processing.

## Handler

Own:
- path/query/body extraction
- HTTP-facing validation
- service/use-case invocation
- application-result to HTTP-response mapping

Do not query the database directly, own transaction boundaries, or contain core business rules.

## Service / application layer

Own:
- business rules
- use-case orchestration
- transaction boundaries
- repository and infrastructure coordination
- application/domain errors

Do not depend on Hono `Context`, construct raw HTTP responses, or depend on frontend concerns.

## Repository / persistence layer

Own:
- persistence operations
- Drizzle/SQL queries
- persistence-oriented mapping

Do not know HTTP, decide authorization policy, produce user-facing messages, or own workflow decisions.

## Cross-module boundaries

Do not import another module's private handler or repository to bypass its public boundary.

Prefer:
- exported application/service functions
- explicit ports where decoupling is required
- genuinely shared schemas/contracts

Avoid circular dependencies. Do not move domain-specific code into `shared` merely to hide a dependency problem.

## Maintainability

Prefer one clear responsibility per module and explicit data flow.

Treat unusually large or multi-purpose files as a review signal, not an automatic line-count violation. Split when responsibilities, change reasons, or testing boundaries become unclear.

Comments should explain why, invariants, compatibility constraints, or non-obvious failure behavior rather than narrating obvious code.

Avoid speculative abstractions, hidden side effects, and design patterns added only for appearance.

## Performance boundary review

Before changing architecture for performance:

1. identify the bottleneck
2. measure it
3. inspect query/request behavior
4. change the smallest relevant layer
5. verify the improvement

Watch for N+1 queries, unbounded lists, large payloads, synchronous CPU-heavy work, excessive external calls, and poorly bounded concurrency.
