#!/usr/bin/env python3
"""Validate ARX behavioral eval fixtures, their policy anchors, and release scoring."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = ROOT / "skills" / "arx-be"
CASES = ROOT / "evals" / "cases.json"
RESULTS_DIR = ROOT / "evals" / "results"
PLUGIN_JSON = ROOT / "plugins" / "arx-be" / ".codex-plugin" / "plugin.json"
REQUIRED_CATEGORIES = {
    "architecture",
    "api",
    "database",
    "security",
    "async",
    "storage",
    "reliability",
    "testing",
    "debugging",
    "review",
    "trigger-precision",
}
ALLOWED_CATEGORIES = REQUIRED_CATEGORIES | {"typescript"}
REQUIRED_KINDS = {"positive", "negative", "adversarial"}
# Short anchors such as "the" match almost any text and silently stop protecting policy.
MIN_ANCHOR_LENGTH = 25
NON_CRITICAL_PASS_THRESHOLD = 0.95


def load_source(source: str) -> str:
    path = (SKILL_ROOT / source).resolve()
    try:
        path.relative_to(SKILL_ROOT.resolve())
    except ValueError as exc:
        raise PermissionError(source) from exc
    if not path.is_file():
        raise FileNotFoundError(source)
    return path.read_text(encoding="utf-8")


def validate_cases(cases: list[Any]) -> tuple[list[str], dict[str, Any]]:
    errors: list[str] = []
    if len(cases) < 20:
        errors.append(f"eval suite must contain at least 20 cases; found {len(cases)}")

    ids: set[str] = set()
    categories: set[str] = set()
    kinds: Counter[str] = Counter()
    critical_count = 0
    total_rubric = 0

    for index, case in enumerate(cases, start=1):
        prefix = f"case #{index}"
        if not isinstance(case, dict):
            errors.append(f"{prefix} must be an object")
            continue
        case_id = case.get("id")
        if not isinstance(case_id, str) or not case_id:
            errors.append(f"{prefix} missing id")
            continue
        prefix = case_id
        if case_id in ids:
            errors.append(f"duplicate eval id: {case_id}")
        ids.add(case_id)

        kind = case.get("kind")
        if kind not in REQUIRED_KINDS:
            errors.append(f"{prefix}: invalid kind {kind!r}")
        else:
            kinds[kind] += 1

        category = case.get("category")
        if not isinstance(category, str) or not category:
            errors.append(f"{prefix}: missing category")
        elif category not in ALLOWED_CATEGORIES:
            errors.append(f"{prefix}: unknown category {category!r}")
        else:
            categories.add(category)

        prompt = case.get("prompt")
        if not isinstance(prompt, str) or len(prompt.strip()) < 20:
            errors.append(f"{prefix}: prompt is too short")

        expected_trigger = case.get("expected_trigger")
        if not isinstance(expected_trigger, bool):
            errors.append(f"{prefix}: expected_trigger must be boolean")
        if kind == "negative" and expected_trigger is not False:
            errors.append(f"{prefix}: negative case must set expected_trigger=false")
        if kind in {"positive", "adversarial"} and expected_trigger is not True:
            errors.append(f"{prefix}: {kind} case must set expected_trigger=true")

        critical = case.get("critical")
        if not isinstance(critical, bool):
            errors.append(f"{prefix}: critical must be boolean")
        elif critical:
            critical_count += 1

        rubric = case.get("rubric")
        if not isinstance(rubric, list) or not rubric:
            errors.append(f"{prefix}: rubric must be a non-empty array")
            continue

        for rindex, item in enumerate(rubric, start=1):
            total_rubric += 1
            rprefix = f"{prefix} rubric #{rindex}"
            if not isinstance(item, dict):
                errors.append(f"{rprefix}: rubric item must be an object")
                continue
            expectation = item.get("expect")
            source = item.get("source")
            anchor = item.get("anchor")
            if not all(isinstance(value, str) and value.strip() for value in (expectation, source, anchor)):
                errors.append(f"{rprefix}: expect/source/anchor are required strings")
                continue
            if len(anchor.strip()) < MIN_ANCHOR_LENGTH:
                errors.append(f"{rprefix}: anchor shorter than {MIN_ANCHOR_LENGTH} characters: {anchor!r}")
            try:
                source_text = load_source(source)
            except PermissionError:
                errors.append(f"{rprefix}: source must stay inside skills/arx-be: {source}")
                continue
            except FileNotFoundError:
                errors.append(f"{rprefix}: source not found: {source}")
                continue
            if anchor.lower() not in source_text.lower():
                errors.append(f"{rprefix}: policy anchor not found in {source}: {anchor!r}")

    missing_categories = REQUIRED_CATEGORIES - categories
    if missing_categories:
        errors.append("missing required eval categories: " + ", ".join(sorted(missing_categories)))
    missing_kinds = REQUIRED_KINDS - set(kinds)
    if missing_kinds:
        errors.append("missing required eval kinds: " + ", ".join(sorted(missing_kinds)))
    if kinds["negative"] < 4:
        errors.append(f"need at least 4 negative trigger cases; found {kinds['negative']}")
    if kinds["adversarial"] < 5:
        errors.append(f"need at least 5 adversarial cases; found {kinds['adversarial']}")
    if critical_count < 10:
        errors.append(f"need at least 10 critical cases; found {critical_count}")

    stats = {
        "cases": len(cases),
        "rubric": total_rubric,
        "critical": critical_count,
        "kinds": kinds,
        "categories": categories,
    }
    return errors, stats


def score_results(path: Path, cases: list[dict[str, Any]], version: str) -> list[str]:
    """Score one target-agent run against the release gate in evals/README.md."""
    name = path.relative_to(ROOT).as_posix()
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"{name}: cannot be loaded: {exc}"]
    if not isinstance(data, dict):
        return [f"{name}: must be an object"]

    errors: list[str] = []
    for key in ("agent", "model", "run_date"):
        if not isinstance(data.get(key), str) or not data[key].strip():
            errors.append(f"{name}: {key} is required")
    if data.get("skill_version") != version:
        errors.append(f"{name}: skill_version {data.get('skill_version')!r} does not match release version {version!r}")
    results = data.get("cases")
    if not isinstance(results, dict):
        return errors + [f"{name}: cases must be an object keyed by case id"]

    unknown = sorted(set(results) - {case["id"] for case in cases})
    if unknown:
        errors.append(f"{name}: results for unknown cases: {', '.join(unknown)}")

    non_critical_total = 0
    non_critical_passed = 0
    for case in cases:
        case_id = case["id"]
        result = results.get(case_id)
        if not isinstance(result, dict):
            errors.append(f"{name}: missing result for {case_id}")
            continue
        triggered = result.get("triggered")
        rubric = result.get("rubric")
        if not isinstance(triggered, bool):
            errors.append(f"{name}: {case_id}.triggered must be boolean")
            continue
        if not isinstance(rubric, list) or len(rubric) != len(case["rubric"]) or not all(isinstance(v, bool) for v in rubric):
            errors.append(f"{name}: {case_id}.rubric must be {len(case['rubric'])} booleans")
            continue

        trigger_ok = triggered == case["expected_trigger"]
        if case["kind"] == "negative" and not trigger_ok:
            errors.append(f"{name}: negative case {case_id} invoked the skill")
        if case["critical"]:
            if not trigger_ok:
                errors.append(f"{name}: critical case {case_id} trigger mismatch")
            failed = [str(i) for i, ok in enumerate(rubric, start=1) if not ok]
            if failed:
                errors.append(f"{name}: critical case {case_id} failed rubric item(s) {', '.join(failed)}")
        else:
            non_critical_total += len(rubric)
            # A wrong trigger decision means none of the case's expectations were exercised.
            non_critical_passed += sum(rubric) if trigger_ok else 0

    if non_critical_total:
        rate = non_critical_passed / non_critical_total
        if rate < NON_CRITICAL_PASS_THRESHOLD:
            errors.append(f"{name}: non-critical rubric pass rate {rate:.1%} is below {NON_CRITICAL_PASS_THRESHOLD:.0%}")
    return errors


def release_gate(cases: list[dict[str, Any]]) -> list[str]:
    try:
        version = str(json.loads(PLUGIN_JSON.read_text(encoding="utf-8"))["version"])
    except (OSError, json.JSONDecodeError, KeyError) as exc:
        return [f"cannot determine release version from plugin.json: {exc}"]
    result_files = sorted(RESULTS_DIR.glob("*.json")) if RESULTS_DIR.is_dir() else []
    if not result_files:
        return [f"no target-agent results in {RESULTS_DIR.relative_to(ROOT).as_posix()}/; see evals/README.md"]

    errors: list[str] = []
    scored = 0
    for path in result_files:
        try:
            run_version = json.loads(path.read_text(encoding="utf-8")).get("skill_version")
        except (OSError, json.JSONDecodeError, AttributeError):
            run_version = None
        # Results from earlier versions stay as history; only runs for this version gate the release.
        if isinstance(run_version, str) and run_version != version:
            continue
        scored += 1
        errors.extend(score_results(path, cases, version))
    if not scored:
        errors.append(f"no target-agent results recorded for skill_version {version}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--release",
        action="store_true",
        help="also require recorded target-agent results that meet the release scoring gate",
    )
    args = parser.parse_args()

    try:
        data = json.loads(CASES.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"Eval manifest cannot be loaded: {exc}")
        return 1

    cases = data.get("cases") if isinstance(data, dict) else None
    if not isinstance(cases, list):
        print("evals/cases.json must contain a cases array")
        return 1

    errors, stats = validate_cases(cases)
    if errors:
        print(f"ARX contract eval FAILED ({len(errors)} issue(s))")
        for error in errors:
            print(f"- {error}")
        return 1

    print("ARX contract eval PASS")
    print(f"cases={stats['cases']} rubric_assertions={stats['rubric']} critical_cases={stats['critical']}")
    print("kinds=" + ", ".join(f"{name}:{stats['kinds'][name]}" for name in sorted(stats["kinds"])))
    print("categories=" + ", ".join(sorted(stats["categories"])))

    if not args.release:
        print("Note: this deterministic suite verifies policy coverage and eval fixtures; run with --release to enforce recorded target-agent results.")
        return 0

    release_errors = release_gate(cases)
    if release_errors:
        print(f"ARX release eval gate FAILED ({len(release_errors)} issue(s))")
        for error in release_errors:
            print(f"- {error}")
        return 1
    print("ARX release eval gate PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
