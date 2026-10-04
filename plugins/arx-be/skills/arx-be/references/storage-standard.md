# Object Storage and Upload Standard

Use this reference for S3-compatible storage, MinIO/AWS S3 adapters, signed URLs, uploads, object keys, and DB/storage consistency.

## Provider boundary

Prefer provider-neutral application contracts. Domain/application logic should not depend on provider-specific SDK request/response types.

Think in stable concepts such as:

- object key
- body or stream
- content type
- checksum
- metadata
- expiry
- signed URL

## Access control

- private buckets by default
- authorize server-side before creating a signed URL
- use short-lived signed URLs appropriate to the workflow
- use least-privilege credentials
- never log credentials or signed URLs

## Object keys

Do not use raw user-supplied filenames directly as object keys without a deliberate normalization/key strategy.

Avoid putting unnecessary personal, secret, or authorization-sensitive data in object keys because keys often appear in logs, metrics, or provider consoles.

## Upload validation

Consider:

- maximum file size
- maximum batch count
- detected MIME type
- allowed extensions
- checksum
- duplicate handling
- timeout behavior
- streaming versus buffering
- malware scanning requirements
- authorization
- async processing needs

Do not trust filename or `Content-Type` alone when security requirements need stronger validation.

## Consistency and failure windows

Database and object-storage operations are not one atomic transaction.

For workflows that write both:

1. identify which operation happens first
2. identify each partial-failure state
3. define retry/idempotency behavior
4. decide whether orphan cleanup, durable processing state, or compensating action is required

Do not introduce complex consistency mechanisms unless the business requirement justifies them.

## Expensive processing

Avoid doing expensive OCR, media conversion, antivirus scanning, or AI processing synchronously inside a request unless explicitly required and safe for request timeouts and resource limits.
