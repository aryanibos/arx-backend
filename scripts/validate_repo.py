#!/usr/bin/env python3
"""Deterministic repository validator for ARX Backend."""

from __future__ import annotations

import json
import re
import stat
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = ROOT / "skills" / "arx-be"
PLUGIN_SKILL_ROOT = ROOT / "plugins" / "arx-be" / "skills" / "arx-be"
PLUGIN_JSON = ROOT / "plugins" / "arx-be" / ".codex-plugin" / "plugin.json"
README = ROOT / "README.md"
CHANGELOG = ROOT / "CHANGELOG.md"
OPENAI_YAML = SKILL_ROOT / "agents" / "openai.yaml"

ALLOWED_FRONTMATTER = {"name", "description"}
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
REFERENCE_RE = re.compile(r"references/[A-Za-z0-9._/-]+\.md")
MARKDOWN_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
VERSION_RE = re.compile(r"^\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?$")
SECRET_PATTERNS = [
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"\bghp_[A-Za-z0-9]{30,}\b"),
    re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
]
TEXT_SUFFIXES = {".md", ".json", ".yaml", ".yml", ".py", ".sh", ".txt"}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


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


def compare_trees(a: Path, b: Path) -> list[str]:
    errors: list[str] = []
    a_files = {p.relative_to(a).as_posix(): p for p in a.rglob("*") if p.is_file()}
    b_files = {p.relative_to(b).as_posix(): p for p in b.rglob("*") if p.is_file()}
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


def validate_local_markdown_links(path: Path, text: str) -> list[str]:
    errors: list[str] = []
    for target in MARKDOWN_LINK_RE.findall(text):
        target = target.split("#", 1)[0].strip()
        if not target or "://" in target or target.startswith("mailto:") or target.startswith("#"):
            continue
        candidate = (path.parent / target).resolve()
        try:
            candidate.relative_to(ROOT.resolve())
        except ValueError:
            errors.append(f"{path.relative_to(ROOT)} links outside repository: {target}")
            continue
        if not candidate.exists():
            errors.append(f"broken markdown link in {path.relative_to(ROOT)}: {target}")
    return errors


def validate_repo(root: Path = ROOT) -> list[str]:
    global ROOT, SKILL_ROOT, PLUGIN_SKILL_ROOT, PLUGIN_JSON, README, CHANGELOG, OPENAI_YAML
    ROOT = root.resolve()
    SKILL_ROOT = ROOT / "skills" / "arx-be"
    PLUGIN_SKILL_ROOT = ROOT / "plugins" / "arx-be" / "skills" / "arx-be"
    PLUGIN_JSON = ROOT / "plugins" / "arx-be" / ".codex-plugin" / "plugin.json"
    README = ROOT / "README.md"
    CHANGELOG = ROOT / "CHANGELOG.md"
    OPENAI_YAML = SKILL_ROOT / "agents" / "openai.yaml"

    errors: list[str] = []
    required = [
        SKILL_ROOT / "SKILL.md",
        OPENAI_YAML,
        PLUGIN_JSON,
        README,
        CHANGELOG,
        ROOT / "evals" / "cases.json",
        ROOT / "scripts" / "run_evals.py",
        ROOT / "scripts" / "package_skill.py",
        ROOT / "scripts" / "check-skill-sync.sh",
        ROOT / "scripts" / "sync-skill.sh",
        ROOT / ".github" / "workflows" / "validate.yml",
    ]
    for path in required:
        if not path.exists():
            errors.append(f"required path missing: {path.relative_to(ROOT)}")
    if errors:
        return errors

    skill_text = read_text(SKILL_ROOT / "SKILL.md")
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

    references_dir = SKILL_ROOT / "references"
    refs_on_disk = {p.relative_to(SKILL_ROOT).as_posix() for p in references_dir.glob("*.md")}
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
            errors.append(f"{ref.relative_to(ROOT)} exceeds 100 lines without a table of contents")
        errors.extend(validate_local_markdown_links(ref, text))
    errors.extend(validate_local_markdown_links(SKILL_ROOT / "SKILL.md", skill_text))

    openai_text = read_text(OPENAI_YAML)
    if "\t" in openai_text:
        errors.append("agents/openai.yaml may not contain tabs")
    if not re.search(r"^interface:\s*$", openai_text, re.MULTILINE):
        errors.append("agents/openai.yaml missing interface mapping")
    if not re.search(r"^\s{2}display_name:\s*.+$", openai_text, re.MULTILINE):
        errors.append("agents/openai.yaml missing interface.display_name")
    if not re.search(r"^\s{2}short_description:\s*.+$", openai_text, re.MULTILINE):
        errors.append("agents/openai.yaml missing interface.short_description")

    try:
        plugin = json.loads(read_text(PLUGIN_JSON))
    except json.JSONDecodeError as exc:
        errors.append(f"plugin.json is invalid JSON: {exc}")
        plugin = {}
    version = str(plugin.get("version", ""))
    if not VERSION_RE.fullmatch(version):
        errors.append(f"plugin.json version is invalid semver: {version!r}")
    if plugin.get("name") != "arx-be":
        errors.append("plugin.json name must be arx-be")

    readme_text = read_text(README)
    changelog_text = read_text(CHANGELOG)
    badge_match = re.search(r"version-([0-9]+\.[0-9]+\.[0-9]+(?:-[0-9A-Za-z.-]+)?)-", readme_text)
    current_match = re.search(r"Current development version:\s*\*\*`([^`]+)`\*\*", readme_text)
    changelog_match = re.search(r"^## \[([^\]]+)\] - (?:Unreleased|\d{4}-\d{2}-\d{2})\s*$", changelog_text, re.MULTILINE)
    versions = {
        "plugin.json": version,
        "README badge": badge_match.group(1) if badge_match else "",
        "README current development version": current_match.group(1) if current_match else "",
        "CHANGELOG top version": changelog_match.group(1) if changelog_match else "",
    }
    if any(not value for value in versions.values()):
        errors.append("unable to determine version from all release metadata: " + json.dumps(versions, sort_keys=True))
    elif len(set(versions.values())) != 1:
        errors.append("version mismatch: " + json.dumps(versions, sort_keys=True))

    errors.extend(compare_trees(SKILL_ROOT, PLUGIN_SKILL_ROOT))

    for script_name in ("sync-skill.sh", "check-skill-sync.sh"):
        path = ROOT / "scripts" / script_name
        mode = path.stat().st_mode
        if not mode & stat.S_IXUSR:
            errors.append(f"{path.relative_to(ROOT)} must be executable")

    gitignore = read_text(ROOT / ".gitignore") if (ROOT / ".gitignore").exists() else ""
    for item in ("dist/", "__pycache__/"):
        if item not in gitignore:
            errors.append(f".gitignore should include {item}")

    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts or "dist" in path.parts:
            continue
        if path.suffix.lower() not in TEXT_SUFFIXES and path.name not in {"SKILL.md"}:
            continue
        try:
            text = read_text(path)
        except UnicodeDecodeError:
            continue
        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                errors.append(f"possible secret detected in {path.relative_to(ROOT)} by pattern {pattern.pattern}")

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
