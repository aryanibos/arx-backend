# Security Standard

Use this reference for authentication, authorization, secret handling, logging, external URLs, file paths, abuse controls, and sensitive data.

## Authentication and authorization

Authentication establishes who the caller is. Authorization decides whether that caller may perform the action on the specific resource.

For protected operations consider:

- role or permission
- resource ownership
- tenant/team boundary
- project/category scope
- indirect object references
- privilege escalation through nested resources

Keep authorization server-side. Do not treat frontend restrictions as a security boundary.

## Input and injection

Validate all external input. Use parameterized queries and safe library APIs. Review dynamic SQL, shell execution, template injection, unsafe parsing/deserialization, and user-controlled path or URL construction.

## SSRF and outbound requests

When accepting URLs or hosts from users or external systems, consider SSRF. Restrict protocols and destinations according to the use case, and protect internal/link-local/cloud-metadata ranges when relevant.

## Files and paths

For file/path operations consider:

- path traversal
- filename normalization
- extension/MIME mismatch
- decompression bombs and oversized input
- malware scanning requirements
- temporary-file cleanup

Do not trust filename or `Content-Type` alone when stronger validation is required.

## Secrets

Never hardcode, commit, return, or log:

- production credentials
- API keys
- tokens
- passwords
- authorization headers
- private keys
- signed URLs
- cloud/storage secrets

Keep `.env` files out of version control unless the project intentionally commits a sanitized example file.

## Logging and observability

Prefer structured logging with safe metadata such as request ID, job ID, operation, service, environment, duration, and non-sensitive resource identifiers.

Prefer allowlisting safe fields over dumping whole request bodies.

Redact credentials, cookies, tokens, signed URLs, secrets, and sensitive document/request content.

## Abuse and resource limits

Consider rate limits, payload limits, batch limits, concurrency, expensive parsing, archive expansion, queue amplification, and repeated external side effects.

Use controls proportional to the real risk; do not add arbitrary restrictions without a requirement or threat model.
