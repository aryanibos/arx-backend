# API Standard

Use this reference for HTTP endpoints, REST contracts, validation, error mapping, pagination, and idempotency.

## Contract

Follow existing project conventions first. When no contract is established, prefer consistent envelopes.

Success:

```json
{
  "success": true,
  "data": {}
}
```

Error:

```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "User-friendly message"
  }
}
```

Keep technical error codes stable and avoid leaking internal details.

## Status codes

Use semantics consistently:

- 200 successful read/update where appropriate
- 201 resource created
- 202 asynchronous work accepted
- 204 successful no-content operation
- 400 malformed or invalid request according to project convention
- 401 unauthenticated
- 403 forbidden
- 404 not found
- 409 conflict
- 413 payload too large
- 415 unsupported media type
- 422 semantic validation only when the project distinguishes it from 400
- 429 rate/resource limit
- 500 sanitized unexpected error
- 503 required dependency unavailable

## Validation

Treat request bodies, query parameters, route parameters, headers used as data, webhook payloads, and third-party responses as untrusted at their respective system boundaries.

Prefer Zod in Zod-based projects. Derive types from schemas when it reduces duplication.

Validation is not authorization; perform both independently.

## Authorization

For protected resources, consider role/permission, ownership, tenant/team scope, category/project scope, and indirect-object-reference risks.

Do not rely on frontend visibility or role checks alone when object-level authorization is required.

## Pagination

Use bounded pagination for list endpoints. Follow existing cursor/offset conventions and keep response shape stable. Avoid unbounded collections by default.

## Idempotency

Consider idempotency when requests may be retried or trigger external side effects. Keep idempotency keys scoped, validated, and stored according to project requirements.

## Error handling

Do not expose stack traces, raw SQL errors, storage/Redis/provider details, credential material, internal paths, or authorization headers.

Map application errors through a centralized HTTP boundary when the project architecture supports it.

## Request correlation

Use request/correlation IDs where available. Propagate and return them according to project convention without treating them as authorization credentials.

## Versioning

Follow the project's API versioning strategy. Do not introduce a new versioning mechanism without a compatibility requirement.
