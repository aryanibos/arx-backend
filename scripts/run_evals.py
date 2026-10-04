#!/usr/bin/env python3
"""Validate ARX behavioral eval fixtures and their policy anchors."""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = ROOT / "skills" / "arx-be"
CASES = ROOT / "evals" / "cases.json"
REQUIRED_CATEGORIES = {
    "architecture",
    "api",
    "database",
    "security",
    "async",
    "storage",
    "testing",
    "debugging",
    "review",
    "trigger-precision",
}
REQUIRED_KINDS = {"positive", "negative", "adversarial"}


def load_source(source: str) -> str:
    path = SKILL_ROOT / source
    if not path.exists() or not path.is_file():
        raise FileNotFoundError(source)
    return path.read_text(encoding="utf-8")


def main() -> int:
    errors: list[str] = []
    try:
        data = json.loads(CASES.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"Eval manifest cannot be loaded: {exc}")
        return 1

    cases = data.get("cases") if isinstance(data, dict) else None
    if not isinstance(cases, list):
        print("evals/cases.json must contain a cases array")
        return 1

    if len(cases) < 20:
        errors.append(f"eval suite must contain at least 20 cases; found {len(cases)}")

    ids: set[str] = set()
    categories: set[str] = set()
    kinds = Counter()
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
            try:
                source_text = load_source(source)
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

    if errors:
        print(f"ARX contract eval FAILED ({len(errors)} issue(s))")
        for error in errors:
            print(f"- {error}")
        return 1

    print("ARX contract eval PASS")
    print(f"cases={len(cases)} rubric_assertions={total_rubric} critical_cases={critical_count}")
    print("kinds=" + ", ".join(f"{name}:{kinds[name]}" for name in sorted(kinds)))
    print("categories=" + ", ".join(sorted(categories)))
    print("Note: this deterministic suite verifies policy coverage and eval fixtures; target-agent behavioral runs still require executing the prompts against the agent and scoring the rubric.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
