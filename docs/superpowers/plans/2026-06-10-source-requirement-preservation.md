# Source Requirement Preservation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add original-request preservation so a user request cannot be translated into a weaker requirements/runtime target while still passing review and verifier.

**Architecture:** Extend `requirements.control.json` with `source_requirements`, then thread those source requirements through required outcomes, required evidence, runtime validation, amendment events, review checks, and verifier completion. Structural checks live in schemas and `control_json_runtime.py`; completion gating lives in `verify_runtime_progress.py`; semantic review instructions live in the requirements/review skills.

**Tech Stack:** Python 3 standard library, `unittest`, JSON Schema files under `schemas/control-json`, cybernetic skill docs under `.agents/skills`.

---

## File Map

- `schemas/control-json/requirements.control.schema.json`: add `source_requirements` and source-linked outcome/evidence fields.
- `schemas/control-json/review.control.schema.json`: no schema-level check-id enum exists, but example fixtures must include the new check.
- `schemas/control-json/progress-event.schema.json`: add `affected_source_requirements` to amendment proposal events.
- `schemas/control-json/amendment-proposal.schema.json`: add `affected_source_requirements` for file-based amendment proposals.
- `.agents/skills/using-control-json/scripts/control_json_runtime.py`: central validation helpers for source requirements, evidence strength, target objects, amendment events, and review checks.
- `.agents/skills/using-control-json/scripts/verify_runtime_progress.py`: compute completed source requirements from completed evidence and reject final success when missing.
- `.agents/skills/compiling-cybernetic-runtime-goals/scripts/control_chain_guard.py`: standalone generation guard; copy the source requirement validation constants/helpers from `control_json_runtime.py` and call them during generation validation.
- `.agents/skills/analyzing-cybernetic-requirements/SKILL.md`: require original request extraction and compact approval display.
- `.agents/skills/analyzing-cybernetic-requirements/assets/requirements.control.example.json`: update example to schema version `1.1.0` with source requirements.
- `.agents/skills/reviewing-cybernetic-control-structures/SKILL.md`: add source-requirement preservation review instructions.
- `.agents/skills/reviewing-cybernetic-control-structures/assets/review.control.example.json`: include `source-requirement-preservation`.
- `.agents/skills/orchestrating-cybernetic-pregoal/scripts/amendment_orchestrator.py`: include new review check in generated amendment reviews and preserve `affected_source_requirements` in events.
- `tests/skills/test_control_json_schemas.py`: schema fixture and negative schema tests.
- `tests/skills/test_reviewed_replanning_control.py`: source requirement guard/amendment regression tests.
- `tests/skills/test_runtime_json_progress_verifier.py`: verifier source requirement completion tests.

## Task 1: Add schema coverage for source requirements

**Files:**
- Modify: `tests/skills/test_control_json_schemas.py`
- Modify: `schemas/control-json/requirements.control.schema.json`
- Modify: `schemas/control-json/progress-event.schema.json`
- Modify: `schemas/control-json/amendment-proposal.schema.json`

- [ ] **Step 1: Add a passing schema fixture for `source_requirements`**

In `tests/skills/test_control_json_schemas.py`, update `SCHEMA_FIXTURES["requirements.control.schema.json"]["approved_control"]` by inserting `source_requirements` before `required_outcomes`:

```python
"source_requirements": [
    {
        "id": "SR-schema-validation",
        "source": {
            "kind": "user_message",
            "quote": "replace Markdown authority with strict JSON control files",
        },
        "required_action": "replace Markdown authority with strict JSON control files",
        "requirement_type": "implement_behavior",
        "required_evidence_strength": "test_result",
        "target_objects": ["JSON control files", "Markdown control inputs"],
        "completion_checks": [
            "JSON control files validate through schema tests.",
            "Markdown control inputs are rejected by official guard/compiler/runtime paths.",
        ],
        "blocks_goal_achieved_if_missing": True,
    }
],
```

Then update the required outcome fixture to include source fields:

```python
"source_requirements": ["SR-schema-validation"],
"completion_claim": "Completes the request by making JSON control files pass and Markdown control inputs fail.",
"completed_target_objects": ["JSON control files", "Markdown control inputs"],
```

Then update its required evidence object:

```python
"evidence_strength": "test_result",
"satisfies_source_requirements": ["SR-schema-validation"],
"evidence_claim": "The schema validation tests prove JSON control files pass and Markdown control inputs fail.",
"completed_target_objects": ["JSON control files", "Markdown control inputs"],
```

- [ ] **Step 2: Add schema negative tests**

Append this test method to `ControlJsonSchemaTest` in `tests/skills/test_control_json_schemas.py`:

```python
def test_requirements_schema_rejects_missing_source_requirement_fields_for_v1_1(self):
    schema = json.loads((SCHEMA_DIR / "requirements.control.schema.json").read_text(encoding="utf-8"))
    fixture = copy.deepcopy(SCHEMA_FIXTURES["requirements.control.schema.json"])
    fixture["schema_version"] = "1.1.0"
    del fixture["approved_control"]["source_requirements"][0]["completion_checks"]

    with self.assertRaises(AssertionError):
        validate(fixture, schema)


def test_progress_event_schema_accepts_affected_source_requirements_on_amendment(self):
    schema = json.loads((SCHEMA_DIR / "progress-event.schema.json").read_text(encoding="utf-8"))
    event = {
        "event_type": "control.amendment.proposed",
        "schema_version": "1.1.0",
        "occurred_at": "2026-06-10T00:00:00Z",
        "runtime_generation": "gen-000",
        "amendment_id": "A1",
        "reason": "current strategy cannot complete source requirement",
        "triggering_observation": "only framework evidence exists for a measurement request",
        "affected_stages": ["plan", "runtime"],
        "affected_source_requirements": ["SR-measure-scale-curves"],
        "semantic_base_change": False,
        "required_outcomes_changed": False,
        "authority_expanded": False,
        "proposed_changes": ["add measured curve producing step"],
        "review_required": ["source-requirement-preservation", "obligation-preservation"],
    }

    validate(event, schema)
```

Run: `python3 -m unittest tests.skills.test_control_json_schemas -v`

Expected: FAIL because schema does not yet define source fields and `affected_source_requirements`.

- [ ] **Step 3: Update requirements schema**

In `schemas/control-json/requirements.control.schema.json`:

Do not add `source_requirements` to the unconditional `approved_control.required` list, because existing `schema_version: "1.0.0"` fixtures must remain readable. Add a schema conditional at the top level:

```json
"allOf": [
  {
    "if": {
      "properties": {
        "schema_version": { "const": "1.1.0" }
      }
    },
    "then": {
      "properties": {
        "approved_control": {
          "required": ["source_requirements"]
        }
      }
    }
  }
]
```

The Python validator in Task 2 enforces `schema_version >= "1.1.0"` for future versions; JSON Schema only needs to catch the current `1.1.0` format.

Add this property under `approved_control.properties`:

```json
"source_requirements": {
  "type": "array",
  "minItems": 1,
  "items": {
    "type": "object",
    "additionalProperties": false,
    "required": [
      "id",
      "source",
      "required_action",
      "requirement_type",
      "required_evidence_strength",
      "completion_checks",
      "blocks_goal_achieved_if_missing"
    ],
    "properties": {
      "id": { "type": "string", "minLength": 1 },
      "source": {
        "type": "object",
        "additionalProperties": false,
        "required": ["kind"],
        "properties": {
          "kind": { "enum": ["user_message", "approved_summary", "requirements_review"] },
          "quote": { "type": "string", "minLength": 1 },
          "reference": { "type": "string", "minLength": 1 }
        },
        "anyOf": [
          { "required": ["quote"] },
          { "required": ["reference"] }
        ]
      },
      "required_action": { "type": "string", "minLength": 1 },
      "requirement_type": {
        "enum": [
          "implement_behavior",
          "produce_empirical_measurement",
          "analyze_existing_evidence",
          "define_framework_or_plan",
          "write_documentation",
          "verify_or_review",
          "diagnose_root_cause",
          "decide_or_classify"
        ]
      },
      "required_evidence_strength": {
        "enum": [
          "behavior_exists",
          "measured_curve_data",
          "benchmark_result",
          "analysis_report",
          "framework_document",
          "review_report",
          "command_result",
          "code_change",
          "test_result"
        ]
      },
      "target_objects": {
        "type": "array",
        "items": { "type": "string", "minLength": 1 }
      },
      "completion_checks": {
        "type": "array",
        "minItems": 1,
        "items": { "type": "string", "minLength": 1 }
      },
      "blocks_goal_achieved_if_missing": { "type": "boolean" }
    }
  }
}
```

Extend `required_outcomes.items.required` with:

```json
"source_requirements",
"completion_claim"
```

Add optional `completed_target_objects`.

Extend `required_evidence.items.required` with:

```json
"evidence_strength",
"satisfies_source_requirements",
"evidence_claim"
```

Add optional `completed_target_objects`.

- [ ] **Step 4: Update amendment schemas**

In both `schemas/control-json/progress-event.schema.json` and `schemas/control-json/amendment-proposal.schema.json`, add property:

```json
"affected_source_requirements": {
  "type": "array",
  "minItems": 1,
  "items": { "type": "string", "minLength": 1 }
}
```

For `control.amendment.proposed` and file-based amendment proposals, add `affected_source_requirements` to required fields.

- [ ] **Step 5: Run schema tests**

Run: `python3 -m unittest tests.skills.test_control_json_schemas -v`

Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add schemas/control-json tests/skills/test_control_json_schemas.py
git commit -m "Add source requirement schema fields"
```

## Task 2: Add source requirement validation helpers

**Files:**
- Modify: `tests/skills/test_reviewed_replanning_control.py`
- Modify: `.agents/skills/using-control-json/scripts/control_json_runtime.py`
- Modify: `.agents/skills/compiling-cybernetic-runtime-goals/scripts/control_chain_guard.py`

- [ ] **Step 1: Update lean test fixture helper to schema v1.1**

In `tests/skills/test_reviewed_replanning_control.py`, update `requirements()` to set `schema_version` to `1.1.0` and add source requirement fields matching the schema from Task 1. Use the default outcome/evidence ids:

```python
"source_requirements": [
    {
        "id": "SR-lean-startup",
        "source": {"kind": "user_message", "quote": "run a lean current generation"},
        "required_action": "run a lean current generation to completion",
        "requirement_type": "implement_behavior",
        "required_evidence_strength": "test_result",
        "target_objects": ["lean current generation"],
        "completion_checks": ["current generation verifier permits completion"],
        "blocks_goal_achieved_if_missing": True,
    }
],
```

Update the default required outcome and required evidence to link to `SR-lean-startup`.

- [ ] **Step 2: Add validation regression tests**

Append these tests to `ReviewedReplanningControlTest`:

```python
def test_guard_rejects_blocking_source_requirement_without_outcome_coverage(self):
    with tempfile.TemporaryDirectory() as tmpdir:
        run_dir = Path(tmpdir)
        write_lean_run(run_dir)
        req = json.loads((run_dir / "requirements.control.json").read_text(encoding="utf-8"))
        req["approved_control"]["source_requirements"].append(
            {
                "id": "SR-api-v2",
                "source": {"kind": "user_message", "quote": "implement /api/v2 routes"},
                "required_action": "implement /api/v2 routes",
                "requirement_type": "implement_behavior",
                "required_evidence_strength": "behavior_exists",
                "target_objects": ["/api/v2 routes"],
                "completion_checks": ["/api/v2 routes return non-404 behavior under tests"],
                "blocks_goal_achieved_if_missing": True,
            }
        )
        run = json.loads((run_dir / "run.control.json").read_text(encoding="utf-8"))
        runtime = json.loads((run_dir / "gen-000/runtime.control.json").read_text(encoding="utf-8"))
        review = json.loads((run_dir / "gen-000/review.control.json").read_text(encoding="utf-8"))
        apply_hashes(req, run, runtime, "gen-000/runtime.control.json", review, "gen-000/review.control.json")
        (run_dir / "requirements.control.json").write_text(json.dumps(req, indent=2), encoding="utf-8")
        (run_dir / "gen-000/runtime.control.json").write_text(json.dumps(runtime, indent=2), encoding="utf-8")

        result = run_script(CONTROL_GUARD, "--run-dir", str(run_dir))

        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("source requirements not covered by blocking required outcomes: SR-api-v2", result.stdout + result.stderr)


def test_guard_rejects_framework_evidence_for_measurement_source_requirement(self):
    with tempfile.TemporaryDirectory() as tmpdir:
        run_dir = Path(tmpdir)
        write_lean_run(run_dir)
        req = json.loads((run_dir / "requirements.control.json").read_text(encoding="utf-8"))
        sr = req["approved_control"]["source_requirements"][0]
        sr["id"] = "SR-measure-curves"
        sr["source"] = {"kind": "user_message", "quote": "measure scale curves"}
        sr["required_action"] = "measure scale curves"
        sr["requirement_type"] = "produce_empirical_measurement"
        sr["required_evidence_strength"] = "measured_curve_data"
        sr["target_objects"] = ["E", "S"]
        sr["completion_checks"] = ["measured data exists for E", "measured data exists for S"]
        outcome = req["approved_control"]["required_outcomes"][0]
        outcome["source_requirements"] = ["SR-measure-curves"]
        outcome["completion_claim"] = "Defines a scan framework for E and S."
        outcome["completed_target_objects"] = ["E", "S"]
        evidence = outcome["required_evidence"][0]
        evidence["evidence_strength"] = "framework_document"
        evidence["satisfies_source_requirements"] = ["SR-measure-curves"]
        evidence["evidence_claim"] = "The file defines scan rules."
        evidence["completed_target_objects"] = ["E", "S"]
        run = json.loads((run_dir / "run.control.json").read_text(encoding="utf-8"))
        runtime = json.loads((run_dir / "gen-000/runtime.control.json").read_text(encoding="utf-8"))
        review = json.loads((run_dir / "gen-000/review.control.json").read_text(encoding="utf-8"))
        apply_hashes(req, run, runtime, "gen-000/runtime.control.json", review, "gen-000/review.control.json")
        (run_dir / "requirements.control.json").write_text(json.dumps(req, indent=2), encoding="utf-8")
        (run_dir / "gen-000/runtime.control.json").write_text(json.dumps(runtime, indent=2), encoding="utf-8")

        result = run_script(CONTROL_GUARD, "--run-dir", str(run_dir))

        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("evidence strength framework_document is too weak for source requirement SR-measure-curves", result.stdout + result.stderr)
```

Run: `python3 -m unittest tests.skills.test_reviewed_replanning_control -v`

Expected: FAIL because helpers and validation do not exist yet.

- [ ] **Step 3: Add constants and helpers in `control_json_runtime.py`**

Add near existing constants:

```python
SOURCE_REQUIREMENT_TYPES = {
    "implement_behavior",
    "produce_empirical_measurement",
    "analyze_existing_evidence",
    "define_framework_or_plan",
    "write_documentation",
    "verify_or_review",
    "diagnose_root_cause",
    "decide_or_classify",
}
EVIDENCE_STRENGTHS = {
    "behavior_exists",
    "measured_curve_data",
    "benchmark_result",
    "analysis_report",
    "framework_document",
    "review_report",
    "command_result",
    "code_change",
    "test_result",
}
ACCEPTABLE_EVIDENCE_STRENGTHS = {
    "implement_behavior": {"behavior_exists", "code_change", "test_result", "command_result"},
    "produce_empirical_measurement": {"measured_curve_data", "benchmark_result"},
    "analyze_existing_evidence": {"analysis_report"},
    "define_framework_or_plan": {"framework_document", "analysis_report"},
    "write_documentation": {"framework_document", "analysis_report"},
    "verify_or_review": {"review_report", "test_result", "command_result"},
    "diagnose_root_cause": {"analysis_report"},
    "decide_or_classify": {"analysis_report"},
}
SOURCE_REQUIREMENT_REVIEW_CHECK = "source-requirement-preservation"
```

Add `SOURCE_REQUIREMENT_REVIEW_CHECK` to both `REQUIRED_REVIEW_CHECKS` and `GENERATION_REVIEW_CHECKS`.

Add helper functions after `required_evidence_by_outcome()`:

```python
def source_requirement_map(requirements: dict[str, Any]) -> tuple[dict[str, dict[str, Any]], set[str], list[str]]:
    approved = requirements.get("approved_control", {})
    raw = approved.get("source_requirements")
    schema_version = str(requirements.get("schema_version", ""))
    if raw is None:
        if schema_version >= "1.1.0":
            return {}, set(), ["requirements.control.json approved_control.source_requirements is required for schema_version >= 1.1.0"]
        return {}, set(), []
    if not isinstance(raw, list) or not raw:
        return {}, set(), ["requirements.control.json approved_control.source_requirements must be a non-empty list"]
    mapped: dict[str, dict[str, Any]] = {}
    blocking: set[str] = set()
    errors: list[str] = []
    for index, item in enumerate(raw):
        label = f"requirements.control.json source_requirements[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{label} must be an object")
            continue
        source_id = item.get("id")
        if not isinstance(source_id, str) or not source_id:
            errors.append(f"{label}.id must be a non-empty string")
            continue
        if source_id in mapped:
            errors.append(f"requirements.control.json duplicate source_requirements id: {source_id}")
            continue
        source = item.get("source")
        if not isinstance(source, dict) or not (source.get("quote") or source.get("reference")):
            errors.append(f"{label}.source must include quote or reference")
        requirement_type = item.get("requirement_type")
        if requirement_type not in SOURCE_REQUIREMENT_TYPES:
            errors.append(f"{label}.requirement_type is not recognized")
        strength = item.get("required_evidence_strength")
        if strength not in EVIDENCE_STRENGTHS:
            errors.append(f"{label}.required_evidence_strength is not recognized")
        checks = item.get("completion_checks")
        if not isinstance(checks, list) or not checks or not all(isinstance(check, str) and check for check in checks):
            errors.append(f"{label}.completion_checks must be a non-empty list of strings")
        if not isinstance(item.get("required_action"), str) or not item.get("required_action"):
            errors.append(f"{label}.required_action must be a non-empty string")
        if not isinstance(item.get("blocks_goal_achieved_if_missing"), bool):
            errors.append(f"{label}.blocks_goal_achieved_if_missing must be boolean")
        mapped[source_id] = item
        if item.get("blocks_goal_achieved_if_missing") is True:
            blocking.add(source_id)
    return mapped, blocking, errors
```

Add helper:

```python
def required_outcome_source_map(requirements: dict[str, Any], errors: list[str]) -> dict[str, set[str]]:
    outcomes = requirements.get("approved_control", {}).get("required_outcomes")
    if not isinstance(outcomes, list):
        return {}
    mapped: dict[str, set[str]] = {}
    for index, outcome in enumerate(outcomes):
        if not isinstance(outcome, dict) or not isinstance(outcome.get("id"), str):
            continue
        raw_sources = outcome.get("source_requirements", [])
        if not isinstance(raw_sources, list) or not all(isinstance(item, str) and item for item in raw_sources):
            errors.append(f"requirements.control.json required_outcomes[{index}].source_requirements must be a list of non-empty strings")
            mapped[outcome["id"]] = set()
            continue
        if not isinstance(outcome.get("completion_claim"), str) or not outcome.get("completion_claim"):
            errors.append(f"requirements.control.json required_outcomes[{index}].completion_claim must be a non-empty string")
        mapped[outcome["id"]] = set(raw_sources)
    return mapped
```

Add helper:

```python
def required_evidence_source_map(requirements: dict[str, Any], errors: list[str]) -> dict[str, dict[str, Any]]:
    evidence_map: dict[str, dict[str, Any]] = {}
    outcomes = requirements.get("approved_control", {}).get("required_outcomes")
    if not isinstance(outcomes, list):
        return evidence_map
    for outcome_index, outcome in enumerate(outcomes):
        required_evidence = outcome.get("required_evidence") if isinstance(outcome, dict) else None
        if not isinstance(required_evidence, list):
            continue
        for evidence_index, evidence in enumerate(required_evidence):
            if not isinstance(evidence, dict) or not isinstance(evidence.get("evidence_id"), str):
                continue
            evidence_id = evidence["evidence_id"]
            label = f"requirements.control.json required_outcomes[{outcome_index}].required_evidence[{evidence_index}]"
            if evidence.get("evidence_strength") not in EVIDENCE_STRENGTHS:
                errors.append(f"{label}.evidence_strength is not recognized")
            raw_sources = evidence.get("satisfies_source_requirements", [])
            if not isinstance(raw_sources, list) or not all(isinstance(item, str) and item for item in raw_sources):
                errors.append(f"{label}.satisfies_source_requirements must be a list of non-empty strings")
            if not isinstance(evidence.get("evidence_claim"), str) or not evidence.get("evidence_claim"):
                errors.append(f"{label}.evidence_claim must be a non-empty string")
            evidence_map[evidence_id] = evidence
    return evidence_map
```

Add helper:

```python
def validate_source_requirement_coverage(requirements: dict[str, Any]) -> tuple[set[str], dict[str, set[str]], dict[str, dict[str, Any]], list[str]]:
    source_map, blocking_sources, errors = source_requirement_map(requirements)
    outcome_sources = required_outcome_source_map(requirements, errors)
    evidence_sources = required_evidence_source_map(requirements, errors)
    known_sources = set(source_map)
    outcome_covered_sources: set[str] = set()
    outcomes = requirements.get("approved_control", {}).get("required_outcomes")
    if isinstance(outcomes, list):
        for outcome in outcomes:
            if not isinstance(outcome, dict):
                continue
            outcome_id = outcome.get("id")
            sources = outcome_sources.get(outcome_id, set()) if isinstance(outcome_id, str) else set()
            unknown = sorted(sources - known_sources)
            if unknown:
                errors.append("required outcome references unknown source requirements: " + ", ".join(unknown))
            if outcome.get("blocks_goal_achieved_if_missing") is True:
                outcome_covered_sources.update(sources & known_sources)
            required_evidence = outcome.get("required_evidence")
            if not isinstance(required_evidence, list):
                continue
            for evidence in required_evidence:
                if not isinstance(evidence, dict):
                    continue
                evidence_id = evidence.get("evidence_id")
                evidence_strength = evidence.get("evidence_strength")
                evidence_source_ids = set(string_list(evidence.get("satisfies_source_requirements")))
                for source_id in sorted(evidence_source_ids & known_sources):
                    source = source_map[source_id]
                    requirement_type = source.get("requirement_type")
                    allowed = ACCEPTABLE_EVIDENCE_STRENGTHS.get(requirement_type, set())
                    if evidence_strength not in allowed:
                        errors.append(
                            f"evidence strength {evidence_strength} is too weak for source requirement {source_id}"
                        )
                    source_targets = set(string_list(source.get("target_objects")))
                    completed_targets = set(string_list(evidence.get("completed_target_objects")))
                    if source_targets and not source_targets.issubset(completed_targets):
                        errors.append(
                            f"evidence {evidence_id} completed_target_objects do not cover source requirement {source_id}"
                        )
    missing = sorted(blocking_sources - outcome_covered_sources)
    if missing:
        errors.append("source requirements not covered by blocking required outcomes: " + ", ".join(missing))
    return blocking_sources, outcome_sources, evidence_sources, errors
```

- [ ] **Step 4: Wire validation into `validate_generation_control_chain()`**

In `.agents/skills/using-control-json/scripts/control_json_runtime.py`, after `required_outcome_sets(requirements)` is called, add:

```python
blocking_source_requirements, outcome_source_map, evidence_source_map, source_errors = validate_source_requirement_coverage(requirements)
errors.extend(source_errors)
```

Do not use the returned maps yet in this task.

- [ ] **Step 5: Mirror validation into `control_chain_guard.py`**

`.agents/skills/compiling-cybernetic-runtime-goals/scripts/control_chain_guard.py` is a standalone script today, so copy the same constants and helper functions from Step 3 into that file. Place them near the existing required-outcome helper functions.

Inside `validate_generation_control_run()`, immediately after `required_outcomes = blocking_required_outcomes(requirements)`, add:

```python
_, _, _, source_errors = validate_source_requirement_coverage(requirements)
if source_errors:
    raise ControlJsonValidationError("; ".join(source_errors))
```

- [ ] **Step 6: Run focused tests**

Run:

```bash
python3 -m unittest tests.skills.test_reviewed_replanning_control -v
python3 -m unittest tests.skills.test_runtime_json_progress_verifier -v
```

Expected: PASS.

- [ ] **Step 7: Commit**

```bash
git add .agents/skills/using-control-json/scripts/control_json_runtime.py .agents/skills/compiling-cybernetic-runtime-goals/scripts/control_chain_guard.py tests/skills/test_reviewed_replanning_control.py
git commit -m "Validate source requirement coverage"
```

## Task 3: Enforce source requirement completion in verifier

**Files:**
- Modify: `tests/skills/test_runtime_json_progress_verifier.py`
- Modify: `.agents/skills/using-control-json/scripts/verify_runtime_progress.py`
- Modify: `.agents/skills/using-control-json/scripts/control_json_runtime.py`

- [ ] **Step 1: Add verifier regression test for missing source evidence**

Append to `RuntimeJsonProgressVerifierTest`:

```python
def test_verify_runtime_progress_rejects_completed_outcome_without_source_requirement_evidence(self):
    with tempfile.TemporaryDirectory() as tmpdir:
        run_dir = Path(tmpdir)
        write_lean_run(
            run_dir,
            progress_events=[progress_event("evidence.other")],
            report=final_report("gen-000", "evidence.other"),
        )

        result = run_script(VERIFY, str(run_dir))

        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("missing completed evidence for blocking source requirements: SR-lean-startup", result.stdout + result.stderr)
```

Run: `python3 -m unittest tests.skills.test_runtime_json_progress_verifier.RuntimeJsonProgressVerifierTest.test_verify_runtime_progress_rejects_completed_outcome_without_source_requirement_evidence -v`

Expected: FAIL until verifier computes source requirements.

- [ ] **Step 2: Add helper to compute source requirements completed by evidence**

In `.agents/skills/using-control-json/scripts/control_json_runtime.py`, add after `validate_source_requirement_coverage()`:

```python
def source_requirements_completed_by_evidence(requirements: dict[str, Any], completed_evidence: set[str]) -> set[str]:
    errors: list[str] = []
    _, _, evidence_map, _ = validate_source_requirement_coverage(requirements)
    completed_sources: set[str] = set()
    for evidence_id in completed_evidence:
        evidence = evidence_map.get(evidence_id)
        if not isinstance(evidence, dict):
            continue
        completed_sources.update(string_list(evidence.get("satisfies_source_requirements")))
    return completed_sources
```

- [ ] **Step 3: Use source completion in verifier**

In `.agents/skills/using-control-json/scripts/verify_runtime_progress.py`, update imports:

```python
from control_json_runtime import (
    blocking_required_outcomes,
    covered_outcomes_by_steps,
    required_evidence_by_outcome,
    result_payload,
    read_progress_events,
    source_requirement_map,
    source_requirements_completed_by_evidence,
    step_outcome_map,
    step_ids,
    validate_control_chain,
    verify_approved_hashes,
)
```

Implement this verifier completion algorithm: completed mainline progress events provide evidence ids; completed evidence ids map through `required_outcomes[*].required_evidence[*].satisfies_source_requirements`; blocking source requirements not reached by acceptable completed evidence reject `goal_achieved`.

After `missing_evidence_messages` handling, add:

```python
source_map, blocking_source_requirements, source_errors = source_requirement_map(artifacts["requirements"])
errors.extend(source_errors)
completed_evidence_ids: set[str] = set()
for evidence_ids in evidence_by_step.values():
    completed_evidence_ids.update(evidence_ids)
completed_source_requirements = source_requirements_completed_by_evidence(
    artifacts["requirements"],
    completed_evidence_ids,
)
missing_source_requirements = sorted(blocking_source_requirements - completed_source_requirements)
if missing_source_requirements:
    errors.append(
        "missing completed evidence for blocking source requirements: "
        + ", ".join(missing_source_requirements)
    )
```

In the final `result_payload`, include:

```python
completed_source_requirements=sorted(completed_source_requirements),
source_requirements=sorted(blocking_source_requirements),
```

Initialize those variables to empty sets before possible errors if needed.

- [ ] **Step 4: Run verifier tests**

Run:

```bash
python3 -m unittest tests.skills.test_runtime_json_progress_verifier -v
```

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add .agents/skills/using-control-json/scripts/control_json_runtime.py .agents/skills/using-control-json/scripts/verify_runtime_progress.py tests/skills/test_runtime_json_progress_verifier.py
git commit -m "Require source requirement evidence in verifier"
```

## Task 4: Add review and amendment check integration

**Files:**
- Modify: `.agents/skills/using-control-json/scripts/control_json_runtime.py`
- Modify: `.agents/skills/orchestrating-cybernetic-pregoal/scripts/amendment_orchestrator.py`
- Modify: `tests/skills/test_reviewed_replanning_control.py`

- [ ] **Step 1: Add tests for source review check and amendment source ids**

In `tests/skills/test_reviewed_replanning_control.py`, update `approved_generation_review()` to include `source-requirement-preservation` in the tuple of check ids.

Update `progress_event()` so amendment events include:

```python
"affected_source_requirements": ["SR-lean-startup"],
```

Add this test:

```python
def test_guard_rejects_generation_review_missing_source_requirement_preservation(self):
    with tempfile.TemporaryDirectory() as tmpdir:
        run_dir = Path(tmpdir)
        write_lean_run(run_dir)
        review_path = run_dir / "gen-000/review.control.json"
        review = json.loads(review_path.read_text(encoding="utf-8"))
        review["review_checks"] = [
            check for check in review["review_checks"]
            if check["check_id"] != "source-requirement-preservation"
        ]
        req = json.loads((run_dir / "requirements.control.json").read_text(encoding="utf-8"))
        run = json.loads((run_dir / "run.control.json").read_text(encoding="utf-8"))
        runtime = json.loads((run_dir / "gen-000/runtime.control.json").read_text(encoding="utf-8"))
        apply_hashes(req, run, runtime, "gen-000/runtime.control.json", review, "gen-000/review.control.json")
        review_path.write_text(json.dumps(review, indent=2), encoding="utf-8")
        (run_dir / "gen-000/runtime.control.json").write_text(json.dumps(runtime, indent=2), encoding="utf-8")

        result = run_script(CONTROL_GUARD, "--run-dir", str(run_dir))

        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("source-requirement-preservation", result.stdout + result.stderr)
```

Add this test:

```python
def test_runtime_validator_requires_affected_source_requirements_on_amendment_proposal(self):
    event = progress_event(
        "evidence.lean-startup",
        event_type="control.amendment.proposed",
        amendment_id="A1",
    )
    del event["affected_source_requirements"]
    with tempfile.TemporaryDirectory() as tmpdir:
        run_dir = Path(tmpdir)
        write_lean_run(run_dir, progress_events=[event], report=final_report("gen-000", "evidence.lean-startup"))

        result = run_script(VERIFY, str(run_dir))

        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("control.amendment.proposed events must include affected_source_requirements", result.stdout + result.stderr)
```

Run: `python3 -m unittest tests.skills.test_reviewed_replanning_control -v`

Expected: FAIL until implementation is updated.

- [ ] **Step 2: Update amendment required fields**

In `.agents/skills/using-control-json/scripts/control_json_runtime.py`, add `"affected_source_requirements"` to `AMENDMENT_PROPOSAL_REQUIRED_FIELDS`.

In `validate_event()`, add validation for the field in `control.amendment.proposed`:

```python
if "affected_source_requirements" in event and (
    not isinstance(event.get("affected_source_requirements"), list)
    or not event.get("affected_source_requirements")
    or not all(isinstance(item, str) and item for item in event.get("affected_source_requirements", []))
):
    errors.append("control.amendment.proposed affected_source_requirements must be a non-empty list")
```

- [ ] **Step 3: Update amendment orchestrator review checks**

In `.agents/skills/orchestrating-cybernetic-pregoal/scripts/amendment_orchestrator.py`, add `source-requirement-preservation` to required review checks. In the generated review evidence text, include the affected source requirements from the amendment event.

Use this pattern in the generated review check description:

```python
"source-requirement-preservation": (
    "amendment preserves source requirements affected by "
    + amendment_id
    + ": "
    + ", ".join(string_list(amendment.get("affected_source_requirements")))
),
```

If there is no `string_list` helper in this script, add:

```python
def string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, str) and item]
```

- [ ] **Step 4: Run reviewed replanning tests**

Run:

```bash
python3 -m unittest tests.skills.test_reviewed_replanning_control -v
```

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add .agents/skills/using-control-json/scripts/control_json_runtime.py .agents/skills/orchestrating-cybernetic-pregoal/scripts/amendment_orchestrator.py tests/skills/test_reviewed_replanning_control.py
git commit -m "Require source requirement review in amendments"
```

## Task 5: Update skill instructions and examples

**Files:**
- Modify: `.agents/skills/analyzing-cybernetic-requirements/SKILL.md`
- Modify: `.agents/skills/analyzing-cybernetic-requirements/assets/requirements.control.example.json`
- Modify: `.agents/skills/reviewing-cybernetic-control-structures/SKILL.md`
- Modify: `.agents/skills/reviewing-cybernetic-control-structures/assets/review.control.example.json`
- Modify: `.agents/skills/using-control-json/references/runtime-control-json-protocol.md`
- Modify: `.agents/skills/using-control-json/SKILL.md`

- [ ] **Step 1: Update requirements skill instructions**

In `.agents/skills/analyzing-cybernetic-requirements/SKILL.md`, under “Preserve Requested Scope”, add:

```markdown
## Preserve Original Request Items

For Level 3/4 JSON control work, extract `source_requirements` before writing `required_outcomes`. A source requirement is one must-do item from the approved user request. It must include the user's quote or source reference, required action, requirement type, required evidence strength, target objects when applicable, completion checks, and whether missing it blocks `goal_achieved`.

Do not weaken the user's request while extracting source requirements. If the user asks to measure, implement, decide, repair, or diagnose, the source requirement must preserve that action. A framework, plan, readiness result, compatibility result, or decision rule may support the work, but it cannot replace the requested action unless the user gives a new approval for the weaker target.

The compact approval summary must show each source requirement in plain language: original quote/reference, required action, evidence needed, and completion checks.
```

- [ ] **Step 2: Update requirements example JSON**

In `.agents/skills/analyzing-cybernetic-requirements/assets/requirements.control.example.json`, set `schema_version` to `1.1.0` and add source requirement fields that validate against Task 1 schema. Keep the example concise and aligned with its JSON-only control purpose.

- [ ] **Step 3: Update review skill instructions**

In `.agents/skills/reviewing-cybernetic-control-structures/SKILL.md`, add a section after “What The User Approved Check”:

```markdown
### Source Requirement Preservation Check

For JSON control runs with `source_requirements`, review must first compare the approved user request text or approved compact summary to `source_requirements`. Reject or return to requirements when a source requirement weakens the requested action, changes the target object, lowers the required evidence strength, omits completion checks, or converts current-run required work into future work.

Then review `source_requirements -> required_outcomes -> required_evidence -> runtime.required_steps -> verifier`. Each blocking source requirement must be covered by equal or stronger evidence. This is not keyword lint: judge whether the proposed outcome and evidence actually complete the original requested item.
```

- [ ] **Step 4: Update review example JSON**

In `.agents/skills/reviewing-cybernetic-control-structures/assets/review.control.example.json`, add a review check object:

```json
{
  "check_id": "source-requirement-preservation",
  "status": "pass",
  "evidence": [
    "source requirements preserve the approved request text and are covered by equal-or-stronger outcomes and evidence"
  ],
  "verdict": "approved",
  "return_to_stage": null,
  "findings": [],
  "required_changes": [],
  "checked_transformations": [
    "approved-request->source-requirements",
    "source-requirements->required-outcomes",
    "required-outcomes->runtime"
  ]
}
```

- [ ] **Step 5: Update runtime protocol**

In `.agents/skills/using-control-json/references/runtime-control-json-protocol.md`, add a paragraph in amendment protocol:

```markdown
When runtime observes that current strategy can only produce weaker evidence for a blocking source requirement, append `control.amendment.proposed` with `affected_source_requirements`. Do not claim completion from substitute evidence. Amendment may change derived strategy only; it may not weaken source requirements, required outcomes, approved authority, or semantic base.
```

In `.agents/skills/using-control-json/SKILL.md`, add one bullet to the runtime rules:

```markdown
- Source requirements are approved original-request items. Runtime may not treat weaker substitute evidence as completion. If strategy cannot complete a blocking source requirement, propose an amendment with `affected_source_requirements`.
```

- [ ] **Step 6: Run skill/docs checks**

Run:

```bash
python3 -m unittest tests.skills.test_skill_repository_integrity tests.skills.test_skill_hot_path_compression -v
```

Expected: PASS.

- [ ] **Step 7: Commit**

```bash
git add .agents/skills/analyzing-cybernetic-requirements .agents/skills/reviewing-cybernetic-control-structures .agents/skills/using-control-json
git commit -m "Document source requirement preservation workflow"
```

## Task 6: Add historical regression tests

**Files:**
- Modify: `tests/skills/test_semantic_review_needs_revision.py`
- Modify: `tests/skills/test_reviewed_replanning_control.py`
- Modify: `tests/fixtures/cybernetics/json_only_control_regression_inventory.json`

- [ ] **Step 1: Add semantic review eval cases**

Open `tests/skills/test_semantic_review_needs_revision.py` and append these tests to `SemanticReviewNeedsRevisionTest`. These tests match the file's current style: they inspect skill text and require the review skill to name the historical weak-source cases.

```python
def test_source_requirement_extraction_cannot_weaken_measurement_to_framework(self):
    review_text = read(REVIEW_SKILL)

    self.assertIn("source-requirement-preservation", review_text)
    self.assertIn("measure E, S, A, M, Q, K, Se, Nout, Cckpt growth curves", review_text)
    self.assertIn("define scan framework and dominance rules", review_text)
    self.assertIn("NeedsRevision", review_text)
    self.assertIn("ReturnToRequirementsAnalysis", review_text)


def test_source_requirement_extraction_cannot_weaken_api_v2_implementation_to_compatibility(self):
    review_text = read(REVIEW_SKILL)

    self.assertIn("source-requirement-preservation", review_text)
    self.assertIn("implement /api/v2 download/extract/preview API family", review_text)
    self.assertIn("compatible with future v2 exposure", review_text)
    self.assertIn("NeedsRevision", review_text)
    self.assertIn("ReturnToRequirementsAnalysis", review_text)
```

- [ ] **Step 2: Add machine regression for bad source requirement accepted before fix**

In `tests/skills/test_reviewed_replanning_control.py`, add a test that mutates the source quote to measurement but source requirement action/evidence to framework. It should expect guard failure:

```python
def test_guard_rejects_source_requirement_weakened_from_quote(self):
    with tempfile.TemporaryDirectory() as tmpdir:
        run_dir = Path(tmpdir)
        write_lean_run(run_dir)
        req = json.loads((run_dir / "requirements.control.json").read_text(encoding="utf-8"))
        sr = req["approved_control"]["source_requirements"][0]
        sr["source"] = {"kind": "user_message", "quote": "measure scale curves for E and S"}
        sr["required_action"] = "define scan framework for E and S"
        sr["requirement_type"] = "define_framework_or_plan"
        sr["required_evidence_strength"] = "framework_document"
        sr["completion_checks"] = ["scan variables are listed"]
        outcome = req["approved_control"]["required_outcomes"][0]
        outcome["completion_claim"] = "Completes the request by defining scan variables."
        evidence = outcome["required_evidence"][0]
        evidence["evidence_strength"] = "framework_document"
        evidence["evidence_claim"] = "The document lists scan variables."
        run = json.loads((run_dir / "run.control.json").read_text(encoding="utf-8"))
        runtime = json.loads((run_dir / "gen-000/runtime.control.json").read_text(encoding="utf-8"))
        review = json.loads((run_dir / "gen-000/review.control.json").read_text(encoding="utf-8"))
        apply_hashes(req, run, runtime, "gen-000/runtime.control.json", review, "gen-000/review.control.json")
        (run_dir / "requirements.control.json").write_text(json.dumps(req, indent=2), encoding="utf-8")
        (run_dir / "gen-000/runtime.control.json").write_text(json.dumps(runtime, indent=2), encoding="utf-8")

        result = run_script(CONTROL_GUARD, "--run-dir", str(run_dir))

        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("source requirement appears weaker than source quote", result.stdout + result.stderr)
```

Implementing this exact error requires a heuristic. Keep the heuristic narrow: if the source quote contains `measure` or `测` and the source requirement type is `define_framework_or_plan`, reject; if the source quote contains `implement` or `实现` and the source requirement type is `define_framework_or_plan` or evidence strength is `framework_document`, reject. This heuristic is only a guard for known regressions; semantic review remains the primary defense.

- [ ] **Step 3: Update regression inventory**

In `tests/fixtures/cybernetics/json_only_control_regression_inventory.json`, add entries:

```json
{
  "id": "source-requirement-measurement-to-framework",
  "class": "original-request-preservation",
  "description": "User asks to measure curves but source requirement records only framework definition.",
  "expected_guard": "reject"
},
{
  "id": "source-requirement-api-v2-to-readiness",
  "class": "original-request-preservation",
  "description": "User asks to implement /api/v2 but source requirement records future compatibility/readiness.",
  "expected_guard": "reject"
}
```

Follow the existing JSON structure exactly.

- [ ] **Step 4: Run regression tests**

Run:

```bash
python3 -m unittest tests.skills.test_semantic_review_needs_revision tests.skills.test_reviewed_replanning_control tests.skills.test_json_control_regression_inventory -v
```

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add tests/skills/test_semantic_review_needs_revision.py tests/skills/test_reviewed_replanning_control.py tests/fixtures/cybernetics/json_only_control_regression_inventory.json
git commit -m "Add original request preservation regressions"
```

## Task 7: Full verification and final cleanup

**Files:**
- Verify only unless tests reveal targeted fixes.

- [ ] **Step 1: Run full test suite**

Run:

```bash
python3 -m unittest discover -v
```

Expected: PASS.

- [ ] **Step 2: Run direct control validators on an example generated run**

Run:

```bash
python3 .agents/skills/compiling-cybernetic-runtime-goals/scripts/control_chain_guard.py --run-dir docs/cybernetics/runs/2026-06-10-reviewed-replanning-control
python3 .agents/skills/using-control-json/scripts/validate_control_chain.py docs/cybernetics/runs/2026-06-10-reviewed-replanning-control
```

Expected: Existing run either passes as legacy schema version or reports only expected pre-existing fixture issues. If it fails solely because `source_requirements` is absent, adjust the schema gate to require source requirements only for `schema_version >= 1.1.0` newly generated fixtures.

- [ ] **Step 3: Scan for old terminology in new spec-facing docs**

Run:

```bash
rg -n "source_obligation|source obligation|makes_true|proves_true|truth-making|making it true" .agents docs tests schemas
```

Expected: No matches in newly changed hot-path docs, schemas, or tests except historical references if any are intentionally retained.

- [ ] **Step 4: Inspect git diff**

Run:

```bash
git diff --stat HEAD~6..HEAD
git status --short
```

Expected: no uncommitted changes except any final cleanup intentionally staged.

- [ ] **Step 5: Commit cleanup if needed**

If Step 1-4 require cleanup:

```bash
git add <changed-files>
git commit -m "Finalize source requirement preservation"
```

If no cleanup is needed, do not create an empty commit.

- [ ] **Step 6: Final implementation report**

Report:

- files changed by category;
- test commands and results;
- whether negative regressions now reject bad control runs;
- any remaining gap, especially deployment drift to `/home/ender/.agents` if still out of scope.
