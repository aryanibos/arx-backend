# Changelog

All notable changes to ARX Backend are documented in this file.

The project follows Semantic Versioning.

## [2.0.0] - 2026-11-22

### Added

- Stack resolution: the backend stack is now resolved from the project foundation (arx-foundation or arx-lead) when one exists, or through a stack ask-gate with curated recommendations and a choose-your-own option when it does not. New `references/stack-resolution.md` documents the resolution order, the recommendation table, the ask-gate format, the no-silent-fallback rule, and a fictional decision-log example.
- Challenge step before finalizing a stack recommendation, and recording of the resolved stack in the decision log or completion report.

### Changed

- `SKILL.md` is now stack-agnostic: the frontmatter description no longer names a fixed stack, "Default technology preferences" became "Recommended technology preferences", and stack resolution is the first grounding step for every task. All other technical rules are unchanged.
- Framework-specific wording generalized in `references/backend-standard.md` (Hono `Context`, Drizzle queries) and `references/testing-verification.md` (test runner); scope notes added to `references/database-standard.md`, `references/async-workers.md`, and `references/typescript-standard.md`.

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
- Standard-library unit tests in `tests/` for `validate_repo.py`, `run_evals.py`, and `package_skill.py`, run in CI.
- Validation of `.agents/plugins/marketplace.json` and the `plugin.json` skills path.

### Fixed

- Package file order no longer depends on the operating system's path sorting (Windows sorted `SKILL.md` case-insensitively), so Linux and Windows builds are byte-identical.
- Packaging and validation list files through git, so gitignored local files such as `.DS_Store` are never packaged or compared.
- Secret scanning covers every file git would commit (including `.env.example`) and detects Stripe live keys, Slack tokens, GitHub fine-grained/OAuth tokens, Google API keys, and AWS temporary keys.
- `validate_repo.py` no longer mutates module globals when validating another root.
- CI actions are pinned to commit SHAs.

### Release policy

- `2.0.0` is tagged as the v2 release.
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
