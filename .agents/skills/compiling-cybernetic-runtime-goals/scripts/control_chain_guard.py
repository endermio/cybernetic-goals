#!/usr/bin/env python3
"""JSON-only guard for compiled cybernetic control runs."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[4]
SCHEMA_DIR = REPO_ROOT / "schemas/control-json"
DELEGATION_WORKFLOW_REGISTRY = REPO_ROOT / ".agents/skills/references/delegation-workflow-registry.json"

CONTROL_SCHEMAS = {
    "requirements.control.json": "requirements.control.schema.json",
    "design.control.json": "design.control.schema.json",
    "goal.control.json": "goal.control.schema.json",
    "plan.control.json": "plan.control.schema.json",
    "review.control.json": "review.control.schema.json",
    "runtime.control.json": "runtime.control.schema.json",
}
MARKDOWN_CONTROL_FILENAMES = {
    "requirements.md",
    "design.md",
    "goal.md",
    "plan.md",
    "review.md",
    "runtime-goal.md",
    "runtime.goal.md",
}
READONLY_FILES = list(CONTROL_SCHEMAS)
WRITABLE_FILES = ["progress.jsonl", "runtime-status.json", "final-report.json"]
DEFAULT_WRITABLE_EVIDENCE_PATHS = ["evidence/"]
RUN_CONTROL_SCHEMA = "run.control.schema.json"
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
REQUIRED_REVIEW_CHECKS = {
    "required-answer-path",
    "intent-preservation",
    "obligation-preservation",
    "required-outcome-coverage",
    SOURCE_REQUIREMENT_REVIEW_CHECK,
    "producing-action-alignment",
    "work-assignment",
    "horizon-authority",
    "final-observer",
}
GENERATION_REVIEW_CHECKS = {
    "intent-preservation",
    "obligation-preservation",
    "required-outcome-coverage",
    SOURCE_REQUIREMENT_REVIEW_CHECK,
    "horizon-authority",
}
REVIEW_HASH_FILES = [
    "requirements.control.json",
    "design.control.json",
    "goal.control.json",
    "plan.control.json",
]
APPROVED_INPUT_STATUSES = {
    "requirements.control.json": "approved",
    "design.control.json": "approved",
    "goal.control.json": "approved",
    "plan.control.json": "approved",
    "review.control.json": "approved",
}
COMPILED_RUN_STATUSES = {
    **APPROVED_INPUT_STATUSES,
    "runtime.control.json": "compiled",
}


class ControlJsonValidationError(Exception):
    pass


def canonical_json_hash(value: dict[str, Any], *, omit_top_level: set[str] | None = None) -> str:
    canonical_value = copy.deepcopy(value)
    for key in omit_top_level or set():
        canonical_value.pop(key, None)
    encoded = json.dumps(canonical_value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return "sha256:" + hashlib.sha256(encoded).hexdigest()


def semantic_base_hash(requirements: dict[str, Any]) -> str:
    approved = requirements.get("approved_control", {})
    if not isinstance(approved, dict):
        return ""
    semantic_value = copy.deepcopy(approved)
    semantic_value.pop("semantic_base", None)
    return canonical_json_hash(semantic_value)


def control_file_hash(filename: str, artifact: dict[str, Any]) -> str:
    omit = {"approved_control_hashes"} if filename.endswith("runtime.control.json") else set()
    return canonical_json_hash(artifact, omit_top_level=omit)


def expected_hashes(artifacts: dict[str, dict[str, Any]], filenames: list[str]) -> dict[str, str]:
    return {filename: control_file_hash(filename, artifacts[filename]) for filename in filenames}


def require_hashes(label: str, actual: Any, expected: dict[str, str]) -> None:
    if not isinstance(actual, dict):
        raise ControlJsonValidationError(f"{label}: approved_control_hashes must be an object")
    for filename, expected_hash in expected.items():
        if actual.get(filename) != expected_hash:
            raise ControlJsonValidationError(f"{label}: approved_control_hashes mismatch for {filename}")


def require_control_statuses(artifacts: dict[str, dict[str, Any]], expected_statuses: dict[str, str]) -> None:
    errors = [
        f"{filename} status must be {expected}"
        for filename, expected in expected_statuses.items()
        if artifacts.get(filename, {}).get("status") != expected
    ]
    if errors:
        raise ControlJsonValidationError("; ".join(errors))


def require_approved_control_inputs(artifacts: dict[str, dict[str, Any]]) -> None:
    require_control_statuses(artifacts, APPROVED_INPUT_STATUSES)


def read_json_object(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ControlJsonValidationError(f"missing JSON file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ControlJsonValidationError(f"invalid JSON in {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ControlJsonValidationError(f"{path} must contain a JSON object")
    return value


def validate_json_schema(instance: Any, schema: dict[str, Any], path: str = "$") -> None:
    if "const" in schema and instance != schema["const"]:
        raise ControlJsonValidationError(f"{path}: expected {schema['const']!r}, got {instance!r}")
    if "enum" in schema and instance not in schema["enum"]:
        raise ControlJsonValidationError(f"{path}: expected one of {schema['enum']!r}, got {instance!r}")

    expected_type = schema.get("type")
    if expected_type == "object":
        if not isinstance(instance, dict):
            raise ControlJsonValidationError(f"{path}: expected object")
        required = schema.get("required", [])
        for key in required:
            if key not in instance:
                raise ControlJsonValidationError(f"{path}: missing required field {key!r}")
        properties = schema.get("properties", {})
        if schema.get("additionalProperties") is False:
            extra = sorted(set(instance) - set(properties))
            if extra:
                raise ControlJsonValidationError(f"{path}: unknown fields {extra!r}")
        for key, subschema in properties.items():
            if key in instance:
                validate_json_schema(instance[key], subschema, f"{path}.{key}")
    elif expected_type == "array":
        if not isinstance(instance, list):
            raise ControlJsonValidationError(f"{path}: expected array")
        if len(instance) < schema.get("minItems", 0):
            raise ControlJsonValidationError(f"{path}: expected at least {schema['minItems']} items")
        for index, item in enumerate(instance):
            validate_json_schema(item, schema.get("items", {}), f"{path}[{index}]")
    elif expected_type == "string":
        if not isinstance(instance, str):
            raise ControlJsonValidationError(f"{path}: expected string")
        if len(instance) < schema.get("minLength", 0):
            raise ControlJsonValidationError(f"{path}: expected non-empty string")
    elif expected_type == "boolean":
        if not isinstance(instance, bool):
            raise ControlJsonValidationError(f"{path}: expected boolean")
    elif expected_type == "integer":
        if not isinstance(instance, int) or isinstance(instance, bool):
            raise ControlJsonValidationError(f"{path}: expected integer")
    elif expected_type == "number":
        if not isinstance(instance, (int, float)) or isinstance(instance, bool):
            raise ControlJsonValidationError(f"{path}: expected number")


def string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, str)]


def path_is_under(path: str, allowed_paths: list[str]) -> bool:
    normalized = path.lstrip("./")
    for allowed in allowed_paths:
        allowed_normalized = allowed.lstrip("./")
        if allowed_normalized.endswith("/"):
            if normalized.startswith(allowed_normalized):
                return True
        elif normalized == allowed_normalized:
            return True
    return False


def required_evidence_paths(requirements: dict[str, Any]) -> list[str]:
    outcomes = requirements.get("approved_control", {}).get("required_outcomes")
    if not isinstance(outcomes, list):
        return []
    paths: list[str] = []
    for outcome in outcomes:
        if not isinstance(outcome, dict):
            continue
        required_evidence = outcome.get("required_evidence")
        if not isinstance(required_evidence, list):
            continue
        for evidence in required_evidence:
            if isinstance(evidence, dict) and isinstance(evidence.get("path"), str) and evidence.get("path"):
                paths.append(evidence["path"])
    return paths


def registry_bindings(artifact: dict[str, Any]) -> dict[str, Any]:
    bindings = artifact.get("registry_bindings")
    return bindings if isinstance(bindings, dict) else {}


def step_ids(artifact: dict[str, Any]) -> set[str]:
    steps = artifact.get("required_steps")
    if not isinstance(steps, list):
        return set()
    return {step.get("step_id") for step in steps if isinstance(step, dict) and isinstance(step.get("step_id"), str)}


def blocking_required_outcomes(requirements: dict[str, Any]) -> set[str]:
    outcomes = requirements.get("approved_control", {}).get("required_outcomes", [])
    if not isinstance(outcomes, list):
        return set()
    return {
        outcome.get("id")
        for outcome in outcomes
        if isinstance(outcome, dict)
        and isinstance(outcome.get("id"), str)
        and outcome.get("blocks_goal_achieved_if_missing") is True
    }


def source_requirement_map(requirements: dict[str, Any]) -> tuple[dict[str, dict[str, Any]], set[str], list[str]]:
    approved = requirements.get("approved_control", {})
    raw = approved.get("source_requirements") if isinstance(approved, dict) else None
    schema_version = str(requirements.get("schema_version", ""))
    if raw is None:
        if schema_version >= "1.1.0":
            return {}, set(), [
                "requirements.control.json approved_control.source_requirements is required for schema_version >= 1.1.0"
            ]
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
            errors.append(
                f"requirements.control.json required_outcomes[{index}].source_requirements must be a list of non-empty strings"
            )
            mapped[outcome["id"]] = set()
            continue
        if not isinstance(outcome.get("completion_claim"), str) or not outcome.get("completion_claim"):
            errors.append(f"requirements.control.json required_outcomes[{index}].completion_claim must be a non-empty string")
        mapped[outcome["id"]] = set(raw_sources)
    return mapped


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


def validate_source_requirement_coverage(
    requirements: dict[str, Any],
) -> tuple[set[str], dict[str, set[str]], dict[str, dict[str, Any]], list[str]]:
    source_map, blocking_sources, errors = source_requirement_map(requirements)
    has_source_requirements = bool(source_map) or bool(errors)
    if not has_source_requirements and str(requirements.get("schema_version", "")) < "1.1.0":
        return blocking_sources, {}, {}, errors

    outcome_sources = required_outcome_source_map(requirements, errors)
    evidence_sources = required_evidence_source_map(requirements, errors)
    known_sources = set(source_map)
    outcome_covered_sources: set[str] = set()
    evidence_covered_sources: set[str] = set()
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
            outcome_blocks = outcome.get("blocks_goal_achieved_if_missing") is True
            if outcome_blocks:
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
                unknown_evidence_sources = sorted(evidence_source_ids - known_sources)
                if unknown_evidence_sources:
                    errors.append(
                        "required evidence references unknown source requirements: "
                        + ", ".join(unknown_evidence_sources)
                    )
                if outcome_blocks:
                    evidence_covered_sources.update(evidence_source_ids & known_sources)
                for source_id in sorted(evidence_source_ids & known_sources):
                    source = source_map[source_id]
                    requirement_type = source.get("requirement_type")
                    allowed = ACCEPTABLE_EVIDENCE_STRENGTHS.get(requirement_type, set())
                    if evidence_strength not in allowed:
                        errors.append(
                            f"evidence strength {evidence_strength} is too weak for source requirement {source_id}"
                        )
                    required_strength = source.get("required_evidence_strength")
                    if evidence_strength != required_strength:
                        errors.append(
                            f"evidence strength {evidence_strength} does not meet required evidence strength "
                            f"{required_strength} for source requirement {source_id}"
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
    missing_evidence = sorted((blocking_sources & outcome_covered_sources) - evidence_covered_sources)
    if missing_evidence:
        errors.append("source requirements not covered by required evidence: " + ", ".join(missing_evidence))
    return blocking_sources, outcome_sources, evidence_sources, errors


def generation_entry(run_control: dict[str, Any], generation_id: str) -> dict[str, Any] | None:
    generations = run_control.get("generations")
    if not isinstance(generations, list):
        return None
    for generation in generations:
        if isinstance(generation, dict) and generation.get("id") == generation_id:
            return generation
    return None


def active_generation_ids(run_control: dict[str, Any]) -> list[str]:
    generations = run_control.get("generations")
    if not isinstance(generations, list):
        return []
    return [
        generation["id"]
        for generation in generations
        if isinstance(generation, dict)
        and generation.get("status") == "active"
        and isinstance(generation.get("id"), str)
    ]


def generation_runtime_readonly_files(generation: dict[str, Any]) -> list[str]:
    files = ["requirements.control.json", "run.control.json", generation["runtime"]]
    review = generation.get("review")
    if isinstance(review, str) and review:
        files.insert(2, review)
    return files


def synthetic_steps_from_requirements(requirements: dict[str, Any]) -> list[dict[str, Any]]:
    steps: list[dict[str, Any]] = []
    outcomes = requirements.get("approved_control", {}).get("required_outcomes", [])
    if not isinstance(outcomes, list):
        return steps
    for index, outcome in enumerate(outcomes, start=1):
        if not isinstance(outcome, dict) or outcome.get("blocks_goal_achieved_if_missing") is not True:
            continue
        outcome_id = outcome.get("id")
        if not isinstance(outcome_id, str) or not outcome_id:
            continue
        steps.append(
            {
                "step_id": f"S{index}-{outcome_id}",
                "transition": outcome.get("statement", outcome_id),
                "evidence": [
                    evidence.get("evidence_id", "required evidence")
                    for evidence in outcome.get("required_evidence", [])
                    if isinstance(evidence, dict)
                ]
                or ["required evidence"],
                "satisfies_outcomes": [outcome_id],
                "synthetic": True,
            }
        )
    return steps


def amendment_generation_count(run_control: dict[str, Any]) -> int:
    generations = run_control.get("generations")
    if not isinstance(generations, list):
        return 0
    return sum(1 for generation in generations if isinstance(generation, dict) and generation.get("parent"))


def require_generation_review_checks(review: dict[str, Any], *, context: str) -> None:
    review_checks = review.get("review_checks")
    if not isinstance(review_checks, list):
        raise ControlJsonValidationError(f"{context} review missing review_checks")
    checks_by_id = {check.get("check_id"): check for check in review_checks if isinstance(check, dict)}
    missing = sorted(GENERATION_REVIEW_CHECKS - set(checks_by_id))
    if missing:
        raise ControlJsonValidationError(f"{context} review missing required review checks: {', '.join(missing)}")
    for check_id in GENERATION_REVIEW_CHECKS:
        check = checks_by_id[check_id]
        if (
            check.get("status") != "pass"
            or check.get("verdict") != "approved"
            or check.get("return_to_stage") is not None
            or not string_list(check.get("evidence"))
        ):
            raise ControlJsonValidationError(f"{context} required review check did not pass with evidence: {check_id}")


def synthetic_step_ids(artifact: dict[str, Any]) -> set[str]:
    steps = artifact.get("required_steps")
    if not isinstance(steps, list):
        return set()
    return {
        step.get("step_id")
        for step in steps
        if isinstance(step, dict)
        and step.get("synthetic") is True
        and isinstance(step.get("step_id"), str)
    }


def step_outcome_map(artifact: dict[str, Any]) -> dict[str, set[str]]:
    steps = artifact.get("required_steps")
    if not isinstance(steps, list):
        return {}
    mapped: dict[str, set[str]] = {}
    for step in steps:
        if not isinstance(step, dict) or not isinstance(step.get("step_id"), str):
            continue
        mapped[step["step_id"]] = set(string_list(step.get("satisfies_outcomes")))
    return mapped


def covered_outcomes_by_steps(step_map: dict[str, set[str]], steps: set[str] | None = None) -> set[str]:
    selected = steps if steps is not None else set(step_map)
    covered: set[str] = set()
    for step_id in selected:
        covered.update(step_map.get(step_id, set()))
    return covered


def require_outcome_coverage(label: str, covered: set[str], required: set[str]) -> None:
    missing = sorted(required - covered)
    if missing:
        raise ControlJsonValidationError(f"{label}: " + ", ".join(missing))


def step_action_alignment_map(plan: dict[str, Any]) -> dict[str, dict[str, Any]]:
    alignments = plan.get("step_action_alignment")
    if not isinstance(alignments, list):
        raise ControlJsonValidationError("plan.control.json must declare step_action_alignment")
    mapped: dict[str, dict[str, Any]] = {}
    for alignment in alignments:
        if not isinstance(alignment, dict):
            raise ControlJsonValidationError("plan.control.json step_action_alignment entries must be objects")
        step_id = alignment.get("required_step_id")
        if not isinstance(step_id, str) or not step_id:
            raise ControlJsonValidationError("plan.control.json step_action_alignment entries must name required_step_id")
        if step_id in mapped:
            raise ControlJsonValidationError(f"plan.control.json duplicate step_action_alignment for {step_id}")
        mapped[step_id] = alignment
    return mapped


def alignment_write_paths(alignment: dict[str, Any]) -> list[str]:
    authority = alignment.get("allowed_authority_needed")
    if not isinstance(authority, dict):
        return []
    return string_list(authority.get("write_paths"))


def reject_markdown_control_artifacts(run_dir: Path) -> None:
    found = sorted(path.name for path in run_dir.iterdir() if path.name in MARKDOWN_CONTROL_FILENAMES or path.name.endswith(".goal.md"))
    if found:
        raise ControlJsonValidationError("Markdown control artifacts are not official JSON control input: " + ", ".join(found))


def validate_generation_control_run(run_dir: Path) -> dict[str, dict[str, Any]]:
    requirements = read_json_object(run_dir / "requirements.control.json")
    run_control = read_json_object(run_dir / "run.control.json")
    _, _, _, source_errors = validate_source_requirement_coverage(requirements)
    if source_errors:
        raise ControlJsonValidationError("; ".join(source_errors))
    validate_json_schema(requirements, read_json_object(SCHEMA_DIR / "requirements.control.schema.json"), "$requirements.control.json")
    validate_json_schema(run_control, read_json_object(SCHEMA_DIR / RUN_CONTROL_SCHEMA), "$run.control.json")

    if requirements.get("status") != "approved":
        raise ControlJsonValidationError("requirements.control.json status must be approved")
    if run_control.get("status") != "active":
        raise ControlJsonValidationError("run.control.json status must be active for runtime execution")

    semantic_base = requirements.get("approved_control", {}).get("semantic_base")
    if not isinstance(semantic_base, dict) or semantic_base.get("hash") != semantic_base_hash(requirements):
        raise ControlJsonValidationError("requirements.control.json: semantic_base hash must match approved_control")
    if run_control.get("semantic_base_ref") != semantic_base:
        raise ControlJsonValidationError("run.control.json: semantic_base_ref must match requirements approved semantic_base")

    current_generation = run_control.get("current_generation")
    if not isinstance(current_generation, str) or not current_generation:
        raise ControlJsonValidationError("run.control.json: current_generation must be a non-empty string")
    active_ids = active_generation_ids(run_control)
    if active_ids != [current_generation]:
        raise ControlJsonValidationError("run.control.json: exactly current_generation must be active")
    max_auto_amendment_rounds = run_control.get("max_auto_amendment_rounds")
    if not isinstance(max_auto_amendment_rounds, int) or isinstance(max_auto_amendment_rounds, bool) or max_auto_amendment_rounds < 0:
        raise ControlJsonValidationError("run.control.json: max_auto_amendment_rounds must be a non-negative integer")
    if amendment_generation_count(run_control) > max_auto_amendment_rounds:
        raise ControlJsonValidationError("run.control.json: auto amendment rounds exceed max_auto_amendment_rounds")
    generation = generation_entry(run_control, current_generation)
    if not generation:
        raise ControlJsonValidationError("run.control.json: current_generation is not declared in generations")
    if not isinstance(generation.get("runtime"), str):
        raise ControlJsonValidationError("run.control.json: current_generation must name runtime")
    strategy_kind = generation.get("strategy_kind")
    if strategy_kind not in {"discovery", "execution", "amendment"}:
        raise ControlJsonValidationError("run.control.json: current generation strategy_kind must be discovery, execution, or amendment")
    if strategy_kind == "amendment" and not generation.get("parent"):
        raise ControlJsonValidationError("run.control.json: amendment generations must declare parent")

    runtime_rel = generation["runtime"]
    runtime = read_json_object(run_dir / runtime_rel)
    validate_json_schema(runtime, read_json_object(SCHEMA_DIR / "runtime.control.schema.json"), f"${runtime_rel}")
    if runtime.get("artifact_type") != "runtime.control" or runtime.get("status") != "compiled":
        raise ControlJsonValidationError(f"{runtime_rel}: artifact_type/status must be runtime.control/compiled")
    if runtime.get("control_mode") != run_control.get("control_mode"):
        raise ControlJsonValidationError(f"{runtime_rel}: control_mode must match run.control.json")
    if runtime.get("semantic_base_ref") != semantic_base:
        raise ControlJsonValidationError(f"{runtime_rel}: semantic_base_ref must match requirements approved semantic_base")
    runtime_generation = runtime.get("generation")
    if not isinstance(runtime_generation, dict) or runtime_generation.get("id") != current_generation:
        raise ControlJsonValidationError(f"{runtime_rel}: generation.id must match run.control.json current_generation")

    review_rel = generation.get("review")
    review: dict[str, Any] | None = None
    if isinstance(review_rel, str) and review_rel:
        review = read_json_object(run_dir / review_rel)
        if review.get("artifact_type") != "review.control" or review.get("status") != "approved":
            raise ControlJsonValidationError(f"{review_rel}: amendment generation review must be approved")
        if strategy_kind == "amendment":
            require_generation_review_checks(review, context="amendment generation")
    if strategy_kind in {"execution", "amendment"} and not review_rel:
        raise ControlJsonValidationError(f"run.control.json: {strategy_kind} generations must declare review")
    if generation.get("parent") and (not review_rel or not generation.get("amendment_source")):
        raise ControlJsonValidationError("run.control.json: amendment generations must declare review and amendment_source")
    if generation.get("parent") and strategy_kind != "amendment":
        raise ControlJsonValidationError("run.control.json: generations with parent must use strategy_kind amendment")

    readonly_files = generation_runtime_readonly_files(generation)
    runtime_files = runtime.get("runtime", {})
    if runtime_files.get("readonly_files") != readonly_files:
        raise ControlJsonValidationError(f"{runtime_rel}: readonly_files must match current generation files")
    if runtime_files.get("writable_files") != WRITABLE_FILES:
        raise ControlJsonValidationError(f"{runtime_rel}: writable files must be progress.jsonl, runtime-status.json, final-report.json")
    writable_evidence_paths = string_list(runtime_files.get("writable_evidence_paths"))
    if not writable_evidence_paths:
        raise ControlJsonValidationError(f"{runtime_rel}: writable_evidence_paths must authorize non-control evidence artifacts")
    for path in required_evidence_paths(requirements):
        if not path_is_under(path, writable_evidence_paths):
            raise ControlJsonValidationError(
                "requirements.control.json required evidence path is not authorized by runtime writable_evidence_paths: "
                + path
            )

    expected_runtime_hashes: dict[str, str] = {
        "requirements.control.json": control_file_hash("requirements.control.json", requirements),
        "run.control.json": control_file_hash("run.control.json", run_control),
        runtime_rel: control_file_hash(runtime_rel, runtime),
    }
    if review is not None and isinstance(review_rel, str):
        expected_runtime_hashes[review_rel] = control_file_hash(review_rel, review)
    require_hashes(f"{runtime_rel}", runtime.get("approved_control_hashes"), expected_runtime_hashes)

    required_outcomes = blocking_required_outcomes(requirements)
    runtime_step_map = step_outcome_map(runtime)
    if strategy_kind != "discovery" and synthetic_step_ids(runtime):
        raise ControlJsonValidationError(f"{runtime_rel}: synthetic required_steps are only allowed in discovery generations")
    if required_outcomes:
        require_outcome_coverage(
            f"{runtime_rel} required_steps do not satisfy blocking required outcomes",
            covered_outcomes_by_steps(runtime_step_map),
            required_outcomes,
        )
        verifier_outcomes = set(string_list(runtime.get("verifier", {}).get("required_outcomes")))
        require_outcome_coverage(
            f"{runtime_rel} verifier.required_outcomes missing blocking required outcomes",
            verifier_outcomes,
            required_outcomes,
        )

    artifacts = {
        "requirements.control.json": requirements,
        "run.control.json": run_control,
        runtime_rel: runtime,
    }
    if review is not None and isinstance(review_rel, str):
        artifacts[review_rel] = review
    return artifacts


def validate_json_control_run(run_dir: Path) -> dict[str, dict[str, Any]]:
    if not run_dir.exists() or not run_dir.is_dir():
        raise ControlJsonValidationError(f"run directory does not exist: {run_dir}")
    reject_markdown_control_artifacts(run_dir)
    if not (run_dir / "run.control.json").exists():
        raise ControlJsonValidationError("missing run.control.json; official JSON control runs must use run.control.json")
    return validate_generation_control_run(run_dir)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", help="Official JSON control run directory containing *.control.json files.")
    parser.add_argument("--requirements", help=argparse.SUPPRESS)
    parser.add_argument("--clarification", help=argparse.SUPPRESS)
    parser.add_argument("--design", help=argparse.SUPPRESS)
    parser.add_argument("--goal", help=argparse.SUPPRESS)
    parser.add_argument("--plan", help=argparse.SUPPRESS)
    parser.add_argument("--review", help=argparse.SUPPRESS)
    args = parser.parse_args()

    if not args.run_dir:
        print(
            "ERROR: official control input is JSON-only; use --run-dir with docs/cybernetics/runs/<slug>/",
            file=sys.stderr,
        )
        return 2
    if any((args.requirements, args.clarification, args.design, args.goal, args.plan, args.review)):
        print(
            "ERROR: --run-dir is the official JSON control input; do not combine it with Markdown artifact inputs",
            file=sys.stderr,
        )
        return 2
    try:
        validate_json_control_run(Path(args.run_dir))
    except ControlJsonValidationError as exc:
        print("FAIL")
        print("NEXT: FixJsonControlRun")
        print(f"ERROR: {exc}")
        return 2

    print("PASS")
    print("NEXT: CompileRuntimeGoal")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
