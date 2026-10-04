# Changelog

All notable changes to ARX Backend are documented in this file.

The project follows Semantic Versioning.

## [2.0.0] - 2026-10-04

### Changed

- Refactored `SKILL.md` into a smaller control plane focused on precedence, workflows, progressive reference loading, verification, and output contracts.
- Expanded the trigger description to cover implementation, modification, debugging, refactoring, security review, and backend pull-request review use cases.
- Replaced rigid line-count guidance with responsibility-based maintainability review signals.
- Relaxed absolute `any` guidance into a narrow interoperability exception while keeping strict typing as the default.
- Standardized HTTP terminology to `401 unauthenticated` and `403 forbidden`.
- Updated Codex plugin metadata and default prompts for the v2 workflow.

### Added

- ChatGPT skill UI metadata at `agents/openai.yaml` in both distribution paths.
- Dedicated progressive references for TypeScript, security, async workers, object storage/uploads, and testing/verification.
- `scripts/sync-skill.sh` to copy the source skill into the packaged plugin distribution.
- `scripts/check-skill-sync.sh` to detect distribution drift.

### Distribution

- `skills/arx-be/` is the canonical source of truth.
- `plugins/arx-be/skills/arx-be/` remains the Codex plugin copy and must stay synchronized through the provided scripts.

## [0.1.0] - 2026-09-17

### Added

- Initial public `arx-be` backend engineering skill.
- Backend architecture guidance and layer boundaries.
- REST API standards and response conventions.
- PostgreSQL and database engineering guidance.
- Queue/worker reliability guidance for Redis and BullMQ.
- S3-compatible object storage guidance.
- Backend security baseline.
- Testing and verification workflow.
- Backend review checklist with severity-based findings.
- Codex plugin manifest and repository marketplace metadata.
