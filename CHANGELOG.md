# Changelog

All notable changes to ARX Backend are documented in this file.

The project follows Semantic Versioning.

## [2.0.0] - Unreleased

### Changed

- Refactored `SKILL.md` into a smaller control plane focused on precedence, workflows, progressive reference loading, verification, and output contracts.
- Expanded the trigger description to cover implementation, modification, debugging, refactoring, security review, and backend pull-request review use cases.
- Added explicit negative trigger boundaries for frontend-only UI, client-side styling, general DevOps administration, data-analysis-only work, and other non-backend tasks.
- Replaced rigid line-count guidance with responsibility-based maintainability review signals.
- Relaxed absolute `any` guidance into a narrow interoperability exception while keeping strict typing as the default.
- Standardized HTTP terminology to `401 unauthenticated` and `403 forbidden`.

### Added

- ChatGPT skill UI metadata at `agents/openai.yaml` in both distribution paths.
- Dedicated progressive references for TypeScript, security, async workers, object storage/uploads, and testing/verification.
- `scripts/sync-skill.sh` and `scripts/check-skill-sync.sh` for canonical/plugin distribution consistency.
- `scripts/validate_repo.py` for deterministic frontmatter, metadata, reference, version, secret, link, executable-bit, and distribution validation.
- `scripts/package_skill.py` for deterministic, integrity-checked `skill.zip` packaging.
- `scripts/run_evals.py` plus `evals/cases.json` for deterministic contract-eval validation.
- Positive, negative-trigger, and adversarial behavioral fixtures covering critical backend failure modes.
- GitHub Actions CI that validates, evaluates, sync-checks, reproducibly packages, and uploads the validated skill artifact.

### Release policy

- `2.0.0` remains untagged while it is a release candidate.
- A public v2 tag requires all deterministic CI gates plus target-agent behavioral scoring defined in `evals/README.md`.

### Distribution

- `skills/arx-be/` is the canonical source of truth.
- `plugins/arx-be/skills/arx-be/` remains the synchronized Codex plugin copy.

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
