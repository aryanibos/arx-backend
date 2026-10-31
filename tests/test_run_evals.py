from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path
from typing import Any
from unittest import mock

import support  # noqa: F401  (puts scripts/ on sys.path)

import run_evals

CASES: list[dict[str, Any]] = json.loads(run_evals.CASES.read_text(encoding="utf-8"))["cases"]
VERSION = json.loads(run_evals.PLUGIN_JSON.read_text(encoding="utf-8"))["version"]


def case_with(predicate: Any) -> dict[str, Any]:
    return next(case for case in CASES if predicate(case))


def perfect_run(version: str = VERSION) -> dict[str, Any]:
    return {
        "skill_version": version,
        "agent": "test-agent",
        "model": "test-model",
        "run_date": "2026-10-31",
        "cases": {
            case["id"]: {"triggered": case["expected_trigger"], "rubric": [True] * len(case["rubric"])}
            for case in CASES
        },
    }


class ValidateCasesTest(unittest.TestCase):
    def errors_after(self, mutate: Any) -> list[str]:
        cases = copy.deepcopy(CASES)
        mutate(cases)
        errors, _ = run_evals.validate_cases(cases)
        return errors

    def assertRejected(self, mutate: Any, fragment: str) -> None:
        errors = self.errors_after(mutate)
        self.assertTrue(any(fragment in error for error in errors), f"{fragment!r} not in {errors}")

    def test_current_cases_pass(self) -> None:
        self.assertEqual(self.errors_after(lambda cases: None), [])

    def test_short_anchor_is_rejected(self) -> None:
        def mutate(cases: list[dict[str, Any]]) -> None:
            cases[0]["rubric"][0]["anchor"] = "the"

        self.assertRejected(mutate, "anchor shorter than 25 characters")

    def test_source_outside_skill_is_rejected(self) -> None:
        def mutate(cases: list[dict[str, Any]]) -> None:
            cases[0]["rubric"][0]["source"] = "../../README.md"

        self.assertRejected(mutate, "source must stay inside skills/arx-be")

    def test_unknown_category_is_rejected(self) -> None:
        def mutate(cases: list[dict[str, Any]]) -> None:
            cases[0]["category"] = "databse"

        self.assertRejected(mutate, "unknown category 'databse'")

    def test_anchor_missing_from_policy_is_rejected(self) -> None:
        def mutate(cases: list[dict[str, Any]]) -> None:
            cases[0]["rubric"][0]["anchor"] = "This sentence does not exist in the skill policy."

        self.assertRejected(mutate, "policy anchor not found")

    def test_negative_case_must_not_expect_trigger(self) -> None:
        def mutate(cases: list[dict[str, Any]]) -> None:
            next(case for case in cases if case["kind"] == "negative")["expected_trigger"] = True

        self.assertRejected(mutate, "negative case must set expected_trigger=false")


class ScoreResultsTest(unittest.TestCase):
    def setUp(self) -> None:
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.dir = Path(tmp.name)

    def score(self, run: dict[str, Any]) -> list[str]:
        path = self.dir / "run.json"
        path.write_text(json.dumps(run), encoding="utf-8")
        return run_evals.score_results(path, CASES, VERSION)

    def assertScoreError(self, run: dict[str, Any], fragment: str) -> None:
        errors = self.score(run)
        self.assertTrue(any(fragment in error for error in errors), f"{fragment!r} not in {errors}")

    def test_perfect_run_passes(self) -> None:
        self.assertEqual(self.score(perfect_run()), [])

    def test_failed_critical_rubric_item_blocks(self) -> None:
        run = perfect_run()
        critical = case_with(lambda case: case["critical"])
        run["cases"][critical["id"]]["rubric"][0] = False
        self.assertScoreError(run, f"critical case {critical['id']} failed rubric item(s) 1")

    def test_triggered_negative_case_blocks(self) -> None:
        run = perfect_run()
        negative = case_with(lambda case: case["kind"] == "negative" and not case["critical"])
        run["cases"][negative["id"]]["triggered"] = True
        self.assertScoreError(run, f"negative case {negative['id']} invoked the skill")

    def test_non_critical_threshold(self) -> None:
        run = perfect_run()
        non_critical = [case for case in CASES if not case["critical"]]
        total = sum(len(case["rubric"]) for case in non_critical)
        # Fail just enough non-critical items to drop below 95%.
        to_fail = total - int(total * run_evals.NON_CRITICAL_PASS_THRESHOLD) + 1
        for case in non_critical:
            for index in range(len(case["rubric"])):
                if to_fail == 0:
                    break
                run["cases"][case["id"]]["rubric"][index] = False
                to_fail -= 1
        self.assertScoreError(run, "non-critical rubric pass rate")

    def test_missing_case_and_wrong_shape_block(self) -> None:
        run = perfect_run()
        first = CASES[0]["id"]
        multi = case_with(lambda case: case["id"] != first and len(case["rubric"]) > 1)
        del run["cases"][first]
        run["cases"][multi["id"]]["rubric"] = [True]
        errors = self.score(run)
        self.assertIn(f"run.json: missing result for {first}", errors)
        self.assertIn(f"run.json: {multi['id']}.rubric must be {len(multi['rubric'])} booleans", errors)

    def test_version_mismatch_blocks(self) -> None:
        self.assertScoreError(perfect_run(version="0.0.1"), "does not match release version")


class ReleaseGateTest(unittest.TestCase):
    def setUp(self) -> None:
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.results = Path(tmp.name)
        patcher = mock.patch.object(run_evals, "RESULTS_DIR", self.results)
        patcher.start()
        self.addCleanup(patcher.stop)

    def write(self, name: str, run: dict[str, Any]) -> None:
        (self.results / name).write_text(json.dumps(run), encoding="utf-8")

    def test_no_results_blocks(self) -> None:
        errors = run_evals.release_gate(CASES)
        self.assertEqual(len(errors), 1)
        self.assertIn("no target-agent results", errors[0])

    def test_results_for_other_versions_are_history_only(self) -> None:
        self.write("old.json", perfect_run(version="0.1.0"))
        self.assertEqual(run_evals.release_gate(CASES), [f"no target-agent results recorded for skill_version {VERSION}"])

    def test_every_current_run_must_pass(self) -> None:
        self.write("good.json", perfect_run())
        bad = perfect_run()
        bad["cases"][CASES[0]["id"]]["triggered"] = not CASES[0]["expected_trigger"]
        self.write("bad.json", bad)
        errors = run_evals.release_gate(CASES)
        self.assertTrue(errors)
        self.assertTrue(all(error.startswith("bad.json") for error in errors), errors)

    def test_passing_runs_pass(self) -> None:
        self.write("good.json", perfect_run())
        self.write("old.json", perfect_run(version="0.1.0"))
        self.assertEqual(run_evals.release_gate(CASES), [])


if __name__ == "__main__":
    unittest.main()
