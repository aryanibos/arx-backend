#!/usr/bin/env python3
"""Deterministic repository validator for ARX Backend."""

from __future__ import annotations

import json
import os
import re
import stat
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

ALLOWED_FRONTMATTER = {"name", "description"}
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
REFERENCE_RE = re.compile(r"references/[A-Za-z0-9._/-]+\.md")
MARKDOWN_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
VERSION_RE = re.compile(r"^\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?$")
SECRET_PATTERNS = [
    ("AWS access key", re.compile(r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b")),
    ("private key", re.compile(r"-----BEGIN (?:[A-Z]+ )?PRIVATE KEY-----")),
    ("GitHub token", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{36,}\b")),
    ("GitHub fine-grained token", re.compile(r"\bgithub_pat_[A-Za-z0-9_]{22,}\b")),
    ("sk- API key", re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b")),
    ("Stripe live key", re.compile(r"\b(?:sk|rk)_live_[A-Za-z0-9]{16,}\b")),
    ("Slack token", re.compile(r"\bxox[abposr]-[A-Za-z0-9-]{10,}\b")),
    ("Google API key", re.compile(r"\bAIza[0-9A-Za-z_-]{35}\b")),
]
# Used only when git cannot list files (for example an extracted source archive).
FALLBACK_EXCLUDED_PARTS = {".git", "dist", "__pycache__"}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def git(root: Path, *args: str) -> subprocess.CompletedProcess[bytes] | None:
    try:
        return subprocess.run(["git", "-C", str(root), *args], capture_output=True, check=False)
    except OSError:
        return None


def is_git_root(root: Path) -> bool:
    # git walks up parent directories, so only trust it when root is the repository itself.
    result = git(root, "rev-parse", "--show-toplevel")
    if result is None or result.returncode != 0:
        return False
    return Path(result.stdout.decode("utf-8").strip()).resolve() == root.resolve()


def list_files(base: Path, root: Path) -> list[Path]:
    """Files under base that git tracks or would track, ignoring gitignored local files."""
    files: set[Path] | None = None
    if is_git_root(root):
        pathspec = base.resolve().relative_to(root.resolve()).as_posix()
        result = git(root, "ls-files", "-z", "--cached", "--others", "--exclude-standard", "--", pathspec)
        if result is not None and result.returncode == 0:
            names = [name for name in result.stdout.decode("utf-8").split("\0") if name]
            files = {p for p in (root / name for name in names) if p.is_file()}
    if files is None:
        files = {
            p
            for p in base.rglob("*")
            if p.is_file() and not FALLBACK_EXCLUDED_PARTS.intersection(p.relative_to(base).parts)
        }
    # Sort by POSIX string so ordering is identical on case-insensitive Windows paths.
    return sorted(files, key=lambda p: p.as_posix())


def is_executable(path: Path, root: Path) -> bool | None:
    """Return the shipped executable bit, or None when it cannot be determined."""
    # The git index is authoritative for the mode that ships; Windows filesystems
    # do not carry an executable bit at all.
    if is_git_root(root):
        result = git(root, "ls-files", "-s", "--", path.relative_to(root).as_posix())
        if result is not None and result.returncode == 0 and result.stdout.strip():
            return result.stdout.decode("utf-8").split(maxsplit=1)[0] == "100755"
    if os.name == "nt":
        return None
    return bool(path.stat().st_mode & stat.S_IXUSR)


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---\n"):
        raise ValueError("SKILL.md must start with YAML frontmatter")
    end = text.find("\n---\n", 4)
    if end < 0:
        raise ValueError("SKILL.md frontmatter closing delimiter not found")

    raw = text[4:end]
    data: dict[str, str] = {}
    for lineno, line in enumerate(raw.splitlines(), start=2):
        if not line.strip():
            continue
        if line[:1].isspace():
            raise ValueError(f"frontmatter line {lineno} must be a top-level key")
        if ":" not in line:
            raise ValueError(f"frontmatter line {lineno} is not key: value")
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if key in data:
            raise ValueError(f"duplicate frontmatter key: {key}")
        data[key] = value.strip('"\'')
    return data, text[end + 5 :]


def compare_trees(a: Path, b: Path, root: Path) -> list[str]:
    errors: list[str] = []
    a_files = {p.relative_to(a).as_posix(): p for p in list_files(a, root)}
    b_files = {p.relative_to(b).as_posix(): p for p in list_files(b, root)}
    if set(a_files) != set(b_files):
        missing_b = sorted(set(a_files) - set(b_files))
        missing_a = sorted(set(b_files) - set(a_files))
        if missing_b:
            errors.append(f"plugin skill missing files: {', '.join(missing_b)}")
        if missing_a:
            errors.append(f"canonical skill missing files present in plugin copy: {', '.join(missing_a)}")
    for rel in sorted(set(a_files) & set(b_files)):
        if a_files[rel].read_bytes() != b_files[rel].read_bytes():
            errors.append(f"skill distribution differs: {rel}")
    return errors


def validate_local_markdown_links(path: Path, text: str, root: Path) -> list[str]:
    errors: list[str] = []
    for target in MARKDOWN_LINK_RE.findall(text):
        target = target.split("#", 1)[0].strip()
        if not target or "://" in target or target.startswith("mailto:") or target.startswith("#"):
            continue
        candidate = (path.parent / target).resolve()
        try:
            candidate.relative_to(root)
        except ValueError:
            errors.append(f"{path.relative_to(root)} links outside repository: {target}")
            continue
        if not candidate.exists():
            errors.append(f"broken markdown link in {path.relative_to(root)}: {target}")
    return errors


def validate_marketplace(root: Path, marketplace_json: Path, plugin_dir: Path, plugin: dict[str, object]) -> list[str]:
    errors: list[str] = []
    try:
        marketplace = json.loads(read_text(marketplace_json))
    except json.JSONDecodeError as exc:
        return [f"marketplace.json is invalid JSON: {exc}"]
    plugins = marketplace.get("plugins") if isinstance(marketplace, dict) else None
    entries = [p for p in plugins if isinstance(p, dict) and p.get("name") == "arx-be"] if isinstance(plugins, list) else []
    if len(entries) != 1:
        errors.append("marketplace.json must list the arx-be plugin exactly once")
    else:
        source = entries[0].get("source")
        source_path = source.get("path") if isinstance(source, dict) else None
        if not isinstance(source_path, str) or (root / source_path).resolve() != plugin_dir.resolve():
            errors.append(f"marketplace.json arx-be source path must point to {plugin_dir.relative_to(root).as_posix()}")

    skills_path = plugin.get("skills")
    if not isinstance(skills_path, str) or not (plugin_dir / skills_path / "arx-be" / "SKILL.md").is_file():
        errors.append("plugin.json skills path must contain arx-be/SKILL.md")
    return errors


def validate_repo(root: Path = ROOT) -> list[str]:
    root = root.resolve()
    skill_root = root / "skills" / "arx-be"
    plugin_dir = root / "plugins" / "arx-be"
    plugin_skill_root = plugin_dir / "skills" / "arx-be"
    plugin_json = plugin_dir / ".codex-plugin" / "plugin.json"
    marketplace_json = root / ".agents" / "plugins" / "marketplace.json"
    readme = root / "README.md"
    changelog = root / "CHANGELOG.md"
    openai_yaml = skill_root / "agents" / "openai.yaml"

    errors: list[str] = []
    required = [
        skill_root / "SKILL.md",
        openai_yaml,
        plugin_json,
        marketplace_json,
        readme,
        changelog,
        root / "evals" / "cases.json",
        root / "scripts" / "run_evals.py",
        root / "scripts" / "package_skill.py",
        root / "scripts" / "check-skill-sync.sh",
        root / "scripts" / "sync-skill.sh",
        root / ".github" / "workflows" / "validate.yml",
    ]
    for path in required:
        if not path.exists():
            errors.append(f"required path missing: {path.relative_to(root).as_posix()}")
    if errors:
        return errors

    skill_text = read_text(skill_root / "SKILL.md")
    try:
        frontmatter, _ = parse_frontmatter(skill_text)
    except ValueError as exc:
        errors.append(str(exc))
        frontmatter = {}

    unexpected = set(frontmatter) - ALLOWED_FRONTMATTER
    missing = ALLOWED_FRONTMATTER - set(frontmatter)
    if unexpected:
        errors.append(f"unexpected SKILL.md frontmatter keys: {', '.join(sorted(unexpected))}")
    if missing:
        errors.append(f"missing SKILL.md frontmatter keys: {', '.join(sorted(missing))}")

    name = frontmatter.get("name", "")
    description = frontmatter.get("description", "")
    if name != "arx-be":
        errors.append("skill name must be exactly arx-be")
    if name and not NAME_RE.fullmatch(name):
        errors.append("skill name must be lowercase hyphen-case")
    if not description:
        errors.append("skill description must not be empty")
    if len(description) > 1024:
        errors.append(f"skill description exceeds 1024 characters: {len(description)}")
    if "<" in description or ">" in description:
        errors.append("skill description may not contain angle brackets")
    for phrase in ("frontend-only UI", "client-side styling", "general DevOps administration", "non-backend application tasks"):
        if phrase.lower() not in description.lower():
            errors.append(f"skill description missing negative trigger boundary: {phrase}")

    skill_lines = skill_text.count("\n") + 1
    if skill_lines >= 500:
        errors.append(f"SKILL.md must stay below 500 lines; found {skill_lines}")

    references_dir = skill_root / "references"
    refs_on_disk = {p.relative_to(skill_root).as_posix() for p in references_dir.glob("*.md")}
    refs_declared = set(REFERENCE_RE.findall(skill_text))
    missing_refs = sorted(refs_declared - refs_on_disk)
    orphan_refs = sorted(refs_on_disk - refs_declared)
    if missing_refs:
        errors.append(f"SKILL.md references missing files: {', '.join(missing_refs)}")
    if orphan_refs:
        errors.append(f"reference files not linked directly from SKILL.md: {', '.join(orphan_refs)}")
    if any(p.is_dir() for p in references_dir.iterdir()):
        errors.append("references must remain one level deep from SKILL.md")

    for ref in sorted(references_dir.glob("*.md")):
        text = read_text(ref)
        line_count = text.count("\n") + 1
        if line_count > 100 and not re.search(r"^## (?:Contents|Table of contents)\s*$", text, re.MULTILINE | re.IGNORECASE):
            errors.append(f"{ref.relative_to(root).as_posix()} exceeds 100 lines without a table of contents")
        errors.extend(validate_local_markdown_links(ref, text, root))
    errors.extend(validate_local_markdown_links(skill_root / "SKILL.md", skill_text, root))

    openai_text = read_text(openai_yaml)
    if "\t" in openai_text:
        errors.append("agents/openai.yaml may not contain tabs")
    if not re.search(r"^interface:\s*$", openai_text, re.MULTILINE):
        errors.append("agents/openai.yaml missing interface mapping")
    if not re.search(r"^\s{2}display_name:\s*.+$", openai_text, re.MULTILINE):
        errors.append("agents/openai.yaml missing interface.display_name")
    if not re.search(r"^\s{2}short_description:\s*.+$", openai_text, re.MULTILINE):
        errors.append("agents/openai.yaml missing interface.short_description")

    try:
        plugin = json.loads(read_text(plugin_json))
    except json.JSONDecodeError as exc:
        errors.append(f"plugin.json is invalid JSON: {exc}")
        plugin = {}
    if not isinstance(plugin, dict):
        errors.append("plugin.json must be an object")
        plugin = {}
    version = str(plugin.get("version", ""))
    if not VERSION_RE.fullmatch(version):
        errors.append(f"plugin.json version is invalid semver: {version!r}")
    if plugin.get("name") != "arx-be":
        errors.append("plugin.json name must be arx-be")
    errors.extend(validate_marketplace(root, marketplace_json, plugin_dir, plugin))

    readme_text = read_text(readme)
    changelog_text = read_text(changelog)
    badge_match = re.search(r"version-([0-9]+\.[0-9]+\.[0-9]+(?:-[0-9A-Za-z.-]+)?)-", readme_text)
    current_match = re.search(r"Current development version:\s*\*\*`([^`]+)`\*\*", readme_text)
    changelog_match = re.search(r"^## \[([^\]]+)\] - (?:Unreleased|\d{4}-\d{2}-\d{2})\s*$", changelog_text, re.MULTILINE)
    versions = {
        "plugin.json": version,
        # shields.io escapes a literal dash as "--" inside badge text.
        "README badge": badge_match.group(1).replace("--", "-") if badge_match else "",
        "README current development version": current_match.group(1) if current_match else "",
        "CHANGELOG top version": changelog_match.group(1) if changelog_match else "",
    }
    if any(not value for value in versions.values()):
        errors.append("unable to determine version from all release metadata: " + json.dumps(versions, sort_keys=True))
    elif len(set(versions.values())) != 1:
        errors.append("version mismatch: " + json.dumps(versions, sort_keys=True))

    errors.extend(compare_trees(skill_root, plugin_skill_root, root))

    # CRLF checkouts would change the packaged bytes and break reproducible builds.
    for path in list_files(skill_root, root):
        if b"\r\n" in path.read_bytes():
            errors.append(f"{path.relative_to(root).as_posix()} must use LF line endings")

    for script_name in ("sync-skill.sh", "check-skill-sync.sh"):
        path = root / "scripts" / script_name
        if is_executable(path, root) is False:
            errors.append(f"{path.relative_to(root).as_posix()} must be executable")

    gitignore = read_text(root / ".gitignore") if (root / ".gitignore").exists() else ""
    for item in ("dist/", "__pycache__/"):
        if item not in gitignore:
            errors.append(f".gitignore should include {item}")

    gitattributes = read_text(root / ".gitattributes") if (root / ".gitattributes").exists() else ""
    if not re.search(r"^\*\s+.*\beol=lf\b", gitattributes, re.MULTILINE):
        errors.append(".gitattributes must normalize text files with eol=lf")

    # Scan every file git would commit, whatever its extension (.env.example included).
    for path in list_files(root, root):
        try:
            text = read_text(path)
        except UnicodeDecodeError:
            continue
        for label, pattern in SECRET_PATTERNS:
            if pattern.search(text):
                errors.append(f"possible secret detected in {path.relative_to(root).as_posix()}: {label}")

    return errors


def main() -> int:
    errors = validate_repo(ROOT)
    if errors:
        print(f"ARX repository validation FAILED ({len(errors)} issue(s))")
        for error in errors:
            print(f"- {error}")
        return 1
    print("ARX repository validation PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
