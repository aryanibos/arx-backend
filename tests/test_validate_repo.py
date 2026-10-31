from __future__ import annotations

import json
import os
import unittest

from support import PLUGIN_SKILL, SKILL, RepoCopyTestCase, git

# Built at runtime so this file never contains a string the secret scanner flags.
FAKE_STRIPE_KEY = "sk_" + "live_" + "A1b2C3d4E5f6G7h8I9j0"


class ValidateRepoTest(RepoCopyTestCase):
    def test_clean_copy_passes(self) -> None:
        self.assertEqual(self.errors(), [])

    def test_crlf_in_skill_is_rejected(self) -> None:
        text = (self.repo / SKILL / "SKILL.md").read_text(encoding="utf-8")
        self.write_skill("SKILL.md", text.replace("\n", "\r\n").encode("utf-8"))
        self.assertErrorContaining("skills/arx-be/SKILL.md must use LF line endings")

    def test_executable_bit_is_read_from_git_index(self) -> None:
        git(self.repo, "update-index", "--chmod=-x", "scripts/sync-skill.sh")
        self.assertErrorContaining("scripts/sync-skill.sh must be executable")

    def test_secret_in_env_example_is_detected(self) -> None:
        self.write(".env.example", f"STRIPE_SECRET_KEY={FAKE_STRIPE_KEY}\n")
        self.assertErrorContaining("possible secret detected in .env.example: Stripe live key")

    def test_gitignored_local_files_are_not_scanned(self) -> None:
        self.write(".env", f"STRIPE_SECRET_KEY={FAKE_STRIPE_KEY}\n")
        self.assertEqual(self.errors(), [])

    def test_plugin_copy_drift_is_rejected(self) -> None:
        self.write(PLUGIN_SKILL / "references" / "api-standard.md", "# drifted\n")
        self.assertErrorContaining("skill distribution differs: references/api-standard.md")

    def test_untracked_file_missing_from_plugin_copy_is_rejected(self) -> None:
        self.write(SKILL / "references" / "extra.md", "# extra\n")
        self.assertErrorContaining("plugin skill missing files: references/extra.md")

    def test_version_mismatch_is_rejected(self) -> None:
        path = self.repo / "plugins/arx-be/.codex-plugin/plugin.json"
        plugin = json.loads(path.read_text(encoding="utf-8"))
        plugin["version"] = "9.9.9"
        self.write(path.relative_to(self.repo), json.dumps(plugin, indent=2) + "\n")
        self.assertErrorContaining("version mismatch")

    def test_marketplace_must_point_at_plugin(self) -> None:
        path = self.repo / ".agents/plugins/marketplace.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        data["plugins"][0]["source"]["path"] = "./plugins/other"
        self.write(path.relative_to(self.repo), json.dumps(data, indent=2) + "\n")
        self.assertErrorContaining("marketplace.json arx-be source path must point to plugins/arx-be")

    def test_unlinked_reference_is_rejected(self) -> None:
        self.write_skill("references/orphan.md", "# orphan\n")
        self.assertErrorContaining("reference files not linked directly from SKILL.md: references/orphan.md")


class ValidateWithoutGitTest(RepoCopyTestCase):
    init_git = False

    def test_extracted_archive_without_git_passes(self) -> None:
        if os.name != "nt":
            for name in ("sync-skill.sh", "check-skill-sync.sh"):
                (self.repo / "scripts" / name).chmod(0o755)
        self.assertEqual(self.errors(), [])


if __name__ == "__main__":
    unittest.main()
