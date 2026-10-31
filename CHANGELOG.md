# Changelog

All notable changes to ARX Backend are documented in this file.

The project follows Semantic Versioning.

## [2.0.0-rc.1] - Unreleased

### Changed

- Refactored `SKILL.md` into a smaller control plane focused on precedence, workflows, progressive reference loading, verification, and output contracts.
- Expanded the trigger description to cover implementation, modification, debugging, refactoring, security review, and backend pull-request review use cases.
- Added explicit negative trigger boundaries for frontend-only UI, client-side styling, general DevOps administration, data-analysis-only work, and other non-backend tasks.
- Replaced rigid line-count guidance with responsibility-based maintainability review signals.
- Relaxed absolute `any` guidance into a narrow interoperability exception while keeping strict typing as the default.
- Standardized HTTP terminology to `401 unauthenticated` and `403 forbidden`.
- Added a conflicting-instructions rule: explicit instructions no longer silently override security, data-integrity, secret-handling, or verification-honesty safeguards.
- Replaced the Blocker/High/Medium/Low review scale with defined P0-P3 severities and deferred to an active review process's format when present.
- Implementation completion reports omit sections that do not apply.
- `run_evals.py` rejects anchors shorter than 25 characters, sources outside the skill, and unknown categories; `--release` scores recorded target-agent results.
- `validate_repo.py` reads executable bits from the git index (works on Windows) and requires LF line endings in the skill.
- Development version is now the prerelease `2.0.0-rc.1` so installs from `main` are distinguishable from the final release.

### Added

- ChatGPT skill UI metadata at `agents/openai.yaml` in both distribution paths.
- Dedicated progressive references for TypeScript, security, async workers, object storage/uploads, and testing/verification.
- `scripts/sync-skill.sh` and `scripts/check-skill-sync.sh` for canonical/plugin distribution consistency.
- `scripts/validate_repo.py` for deterministic frontmatter, metadata, reference, version, secret, link, executable-bit, and distribution validation.
- `scripts/package_skill.py` for deterministic, integrity-checked `skill.zip` packaging.
- `scripts/run_evals.py` plus `evals/cases.json` for deterministic contract-eval validation.
- Positive, negative-trigger, and adversarial behavioral fixtures covering critical backend failure modes.
- GitHub Actions CI that validates, evaluates, sync-checks, reproducibly packages, and uploads the validated skill artifact.
- `references/reliability-operations.md` for outbound call timeouts/retries, configuration validation, health checks, and HTTP server shutdown.
- Security guidance for sessions/JWT, password storage, CORS, CSRF, user-content serving, and webhook signature/replay handling.
- Transaction rule against holding database transactions open across network I/O.
- Eval cases for reliability, webhooks, password storage, CORS, severity, non-TypeScript stacks, and near-miss trigger boundaries.
- `.gitattributes` enforcing LF line endings, and a CI matrix that proves the package is byte-identical on Linux and Windows.

### Release policy

- `2.0.0-rc.1` remains untagged while it is a release candidate.
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
