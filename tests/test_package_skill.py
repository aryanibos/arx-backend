from __future__ import annotations

import contextlib
import io
import unittest
import zipfile

from support import SKILL, RepoCopyTestCase

import package_skill


class PackageSkillTest(RepoCopyTestCase):
    def build(self) -> str:
        with contextlib.redirect_stdout(io.StringIO()):
            return package_skill.build(self.repo / "dist" / "skill.zip", self.repo)

    def test_build_is_reproducible(self) -> None:
        self.assertEqual(self.build(), self.build())

    def test_archive_order_is_case_sensitive_posix_order(self) -> None:
        self.build()
        with zipfile.ZipFile(self.repo / "dist" / "skill.zip") as zf:
            names = zf.namelist()
        self.assertEqual(names, sorted(names))
        self.assertEqual(names[0], "arx-be/SKILL.md")

    def test_ignored_local_files_are_not_packaged(self) -> None:
        self.write(SKILL / ".DS_Store", b"\x00\x01")
        self.build()
        with zipfile.ZipFile(self.repo / "dist" / "skill.zip") as zf:
            self.assertNotIn("arx-be/.DS_Store", zf.namelist())

    def test_invalid_repository_is_not_packaged(self) -> None:
        self.write(SKILL / "references" / "api-standard.md", "# drifted\n")
        with self.assertRaises(SystemExit):
            self.build()
        self.assertFalse((self.repo / "dist" / "skill.zip").exists())


if __name__ == "__main__":
    unittest.main()
