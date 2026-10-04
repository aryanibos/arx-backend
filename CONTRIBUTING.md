# Contributing

Contributions are welcome.

## Source of truth

Edit the canonical skill only in:

```text
skills/arx-be/
```

Do not manually maintain a divergent copy under the Codex plugin path.

After changing the skill, run:

```bash
./scripts/sync-skill.sh
python scripts/validate_repo.py
python scripts/run_evals.py
./scripts/check-skill-sync.sh
python scripts/package_skill.py
```

The packaged copy at `plugins/arx-be/skills/arx-be/` must remain synchronized with the canonical source.

## Rules

- Keep the skill project-agnostic.
- Preserve the rule that explicit project architecture and repository conventions take precedence over skill defaults.
- Keep `SKILL.md` focused on workflow/control-plane guidance and move domain detail into directly linked references.
- Keep trigger scope precise; backend-adjacent wording must not cause frontend-only or general administration work to trigger the skill.
- Add a reference only when it materially improves reliability or avoids bloating `SKILL.md`.
- Add or update eval cases when changing behavior, trigger scope, security/data-integrity policy, or verification rules.
- Do not add secrets or credential examples.
- Keep changes focused and reviewable.
- Update `plugins/arx-be/.codex-plugin/plugin.json`, `README.md`, and `CHANGELOG.md` consistently for published version changes.

## Eval policy

`python scripts/run_evals.py` is a deterministic contract check. It verifies fixture quality and that each behavioral expectation remains anchored in canonical policy.

Before a major release tag, also execute the fixtures against intended target agents and score them using `evals/README.md`.

## Pull requests

Explain:

- what changed
- why it improves backend implementation/review behavior
- whether the change is backward-compatible
- any new references, scripts, or rules
- eval cases added or changed
- how validation, packaging, and skill-distribution synchronization were verified
