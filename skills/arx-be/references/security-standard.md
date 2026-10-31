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

## Sessions, tokens, and passwords

- Prefer the project's established authentication library or provider over hand-rolled schemes.
- Verify JWT signature with an explicit allowed algorithm list, and check expiry, issuer, and audience. Never accept `alg: none`.
- Do not put secrets or unnecessary personal data in JWT claims; they are readable by the client.
- Keep access tokens short-lived and define how sessions or refresh tokens are revoked.
- Set session cookies with `HttpOnly`, `Secure`, and an appropriate `SameSite` value.
- Hash passwords with a vetted slow algorithm such as Argon2id, scrypt, or bcrypt through a maintained library. Never store plaintext, reversible encryption, or fast hashes such as SHA-256 alone.
- Compare secrets and tokens with constant-time comparison.

## Browser-facing APIs

- Configure CORS with an explicit origin allowlist. Never combine a wildcard origin with credentials or reflect arbitrary `Origin` values.
- Protect state-changing endpoints that rely on cookie authentication against CSRF (`SameSite` plus a CSRF token or origin verification).
- Serve user-uploaded content with a safe `Content-Type` and `Content-Disposition: attachment`, or from a separate origin, so it cannot execute as same-origin HTML.

## Webhooks

- Verify the provider signature against the raw request body before parsing or acting on it.
- Reject stale timestamps and replayed event IDs within the provider's tolerance window.
- Process webhook events idempotently; providers deliver at least once.
- Respond quickly and move slow work to a background job.

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
