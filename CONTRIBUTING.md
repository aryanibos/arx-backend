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
./scripts/check-skill-sync.sh
```

The packaged copy at `plugins/arx-be/skills/arx-be/` must remain synchronized with the canonical source.

## Rules

- Keep the skill project-agnostic.
- Preserve the rule that explicit project architecture and repository conventions take precedence over skill defaults.
- Keep `SKILL.md` focused on workflow/control-plane guidance and move domain detail into directly linked references.
- Add a reference only when it materially improves reliability or avoids bloating `SKILL.md`.
- Do not add secrets or credential examples.
- Keep changes focused and reviewable.
- Update `plugins/arx-be/.codex-plugin/plugin.json` and `CHANGELOG.md` for published behavioral changes.

## Pull requests

Explain:

- what changed
- why it improves backend implementation/review behavior
- whether the change is backward-compatible
- any new references, scripts, or rules
- how skill-distribution synchronization was verified
