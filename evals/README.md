# ARX Backend Eval Suite

This directory defines the behavioral release criteria for ARX Backend v2.

## Two layers of evaluation

### 1. Deterministic contract evals

Run:

```bash
python scripts/run_evals.py
```

CI validates that:

- every fixture has an explicit expected trigger decision
- positive, negative, and adversarial cases are represented
- critical backend domains are covered
- every behavioral expectation is anchored to canonical skill policy
- no eval silently depends on a rule that disappeared during refactoring

This layer is deterministic and suitable for every pull request.

### 2. Target-agent behavioral runs

The fixtures are also prompts for real agent testing. Install or load `arx-be`, run each prompt against the target agent, and score the response against every rubric item.

For a v2.0.0 release tag, use this gate:

- 100% of critical cases pass all rubric items
- 100% of negative trigger cases do not invoke ARX Backend when backend behavior is absent
- at least 95% of all non-critical rubric items pass
- no security, data-integrity, migration, or verification critical failure is waived

Do not treat the deterministic contract eval as proof that a specific model or agent will behave perfectly. It proves that the skill contains the policy needed by the behavioral fixtures and protects the fixtures from becoming stale.

## Adding cases

Add a case when a real failure mode, regression, ambiguity, or important non-trigger boundary is discovered. Prefer cases that distinguish good backend engineering behavior from plausible but unsafe shortcuts.
