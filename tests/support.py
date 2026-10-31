"""Shared helpers for testing the repository scripts against disposable copies."""

from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import validate_repo  # noqa: E402

SKILL = Path("skills/arx-be")
PLUGIN_SKILL = Path("plugins/arx-be/skills/arx-be")


def git(cwd: Path, *args: str) -> None:
    subprocess.run(["git", "-C", str(cwd), *args], check=True, capture_output=True)


class RepoCopyTestCase(unittest.TestCase):
    """Each test gets a fresh copy of the repository as its own git repository."""

    init_git = True

    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.repo = Path(self._tmp.name).resolve() / "repo"
        for source in validate_repo.list_files(ROOT, ROOT):
            target = self.repo / source.relative_to(ROOT)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
        if self.init_git:
            git(self.repo, "init", "-q")
            git(self.repo, "config", "core.autocrlf", "false")
            git(self.repo, "add", "-A")
            # Windows checkouts have no executable bit, so set the shipped mode explicitly.
            git(self.repo, "update-index", "--chmod=+x", "scripts/sync-skill.sh", "scripts/check-skill-sync.sh")

    def write(self, rel: str | Path, content: str | bytes) -> Path:
        path = self.repo / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(content, bytes):
            path.write_bytes(content)
        else:
            path.write_text(content, encoding="utf-8", newline="\n")
        return path

    def write_skill(self, rel: str, content: str | bytes) -> None:
        """Write the same file to the canonical skill and its plugin copy."""
        self.write(SKILL / rel, content)
        self.write(PLUGIN_SKILL / rel, content)

    def errors(self) -> list[str]:
        return validate_repo.validate_repo(self.repo)

    def assertErrorContaining(self, fragment: str) -> None:
        errors = self.errors()
        self.assertTrue(any(fragment in error for error in errors), f"{fragment!r} not in {errors}")
