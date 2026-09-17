# API Standard

## Contract
Prefer consistent envelopes.

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

## Status Codes
Use semantics consistently:
- 200 successful read/update where appropriate
- 201 resource created
- 202 asynchronous work accepted
- 204 successful no-content operation
- 400 invalid request
- 401 unauthenticated
- 403 unauthorized
- 404 not found
- 409 conflict
- 413 payload too large
- 415 unsupported media type
- 422 only when project API convention uses semantic validation separately
- 429 rate/resource limit
- 500 sanitized unexpected error
- 503 required dependency unavailable

Follow existing project conventions when they differ.

## Validation
Validate all external input.

## Authorization
Perform object-level authorization, not role-only checks.

## Pagination
Prefer bounded pagination. Never return unbounded collections by default.

## Idempotency
Consider idempotency for operations that may be retried or create external side effects.

## Errors
Do not expose:
- stack traces
- SQL messages
- S3/Redis raw errors
- credential material
- internal paths

## Request Correlation
Use request IDs where available and return/propagate them according to project convention.

## Versioning
Follow the project's API versioning strategy. Do not introduce new versioning without need.
