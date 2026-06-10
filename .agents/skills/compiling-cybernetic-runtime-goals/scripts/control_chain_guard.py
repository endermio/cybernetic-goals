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
REQUIRED_REVIEW_CHECKS = {
    "required-answer-path",
    "intent-preservation",
    "obligation-preservation",
    "required-outcome-coverage",
    "producing-action-alignment",
    "work-assignment",
    "horizon-authority",
    "final-observer",
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
            }
        )
    return steps


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
    generation = generation_entry(run_control, current_generation)
    if not generation:
        raise ControlJsonValidationError("run.control.json: current_generation is not declared in generations")
    if not isinstance(generation.get("runtime"), str):
        raise ControlJsonValidationError("run.control.json: current_generation must name runtime")

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
    if generation.get("parent") and (not review_rel or not generation.get("amendment_source")):
        raise ControlJsonValidationError("run.control.json: amendment generations must declare review and amendment_source")

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
    if (run_dir / "run.control.json").exists():
        return validate_generation_control_run(run_dir)

    artifacts: dict[str, dict[str, Any]] = {}
    for filename, schema_name in CONTROL_SCHEMAS.items():
        artifact = read_json_object(run_dir / filename)
        schema = read_json_object(SCHEMA_DIR / schema_name)
        validate_json_schema(artifact, schema, f"${filename}")
        artifacts[filename] = artifact

    require_control_statuses(artifacts, COMPILED_RUN_STATUSES)

    runtime = artifacts["runtime.control.json"]
    semantic_base = artifacts["requirements.control.json"].get("approved_control", {}).get("semantic_base")
    if not isinstance(semantic_base, dict) or semantic_base.get("hash") != semantic_base_hash(artifacts["requirements.control.json"]):
        raise ControlJsonValidationError("requirements.control.json: semantic_base hash must match approved_control")
    for filename in ("design.control.json", "goal.control.json", "plan.control.json", "review.control.json", "runtime.control.json"):
        if artifacts[filename].get("semantic_base_ref") != semantic_base:
            raise ControlJsonValidationError(f"{filename}: semantic_base_ref must match requirements approved semantic_base")

    require_hashes(
        "review.control.json",
        artifacts["review.control.json"].get("approved_control_hashes"),
        expected_hashes(artifacts, REVIEW_HASH_FILES),
    )
    require_hashes(
        "runtime.control.json",
        runtime.get("approved_control_hashes"),
        expected_hashes(artifacts, READONLY_FILES),
    )

    expected_chain = {
        "requirements": "requirements.control.json",
        "design": "design.control.json",
        "goal": "goal.control.json",
        "plan": "plan.control.json",
        "review": "review.control.json",
    }
    if runtime.get("control_chain") != expected_chain:
        raise ControlJsonValidationError("runtime.control.json: control_chain must reference the approved JSON files")

    expected_sources = {
        "design.control.json": {"requirements": "requirements.control.json"},
        "goal.control.json": {"requirements": "requirements.control.json", "design": "design.control.json"},
        "plan.control.json": {"requirements": "requirements.control.json", "design": "design.control.json", "goal": "goal.control.json"},
        "review.control.json": {
            "requirements": "requirements.control.json",
            "design": "design.control.json",
            "goal": "goal.control.json",
            "plan": "plan.control.json",
        },
    }
    for filename, expected in expected_sources.items():
        sources = artifacts[filename].get("source_contracts", {})
        for key, value in expected.items():
            if sources.get(key) != value:
                raise ControlJsonValidationError(f"{filename}: source_contracts.{key} must reference {value}")

    runtime_files = runtime.get("runtime", {})
    if runtime_files.get("readonly_files") != READONLY_FILES:
        raise ControlJsonValidationError("runtime.control.json: approved control JSON must be read-only")
    if runtime_files.get("writable_files") != WRITABLE_FILES:
        raise ControlJsonValidationError("runtime.control.json: writable files must be progress.jsonl, runtime-status.json, final-report.json")
    writable_evidence_paths = string_list(runtime_files.get("writable_evidence_paths"))
    if not writable_evidence_paths:
        raise ControlJsonValidationError("runtime.control.json: writable_evidence_paths must authorize non-control evidence artifacts")
    plan_runtime = artifacts["plan.control.json"].get("runtime", {})
    if plan_runtime.get("readonly_files") != READONLY_FILES or plan_runtime.get("writable_files") != WRITABLE_FILES:
        raise ControlJsonValidationError("plan.control.json: runtime read/write files must match runtime.control.json")
    if string_list(plan_runtime.get("writable_evidence_paths")) != writable_evidence_paths:
        raise ControlJsonValidationError("plan.control.json: writable_evidence_paths must match runtime.control.json")
    for path in required_evidence_paths(artifacts["requirements.control.json"]):
        if not path_is_under(path, writable_evidence_paths):
            raise ControlJsonValidationError(
                "requirements.control.json required evidence path is not authorized by runtime writable_evidence_paths: "
                + path
            )

    if artifacts["plan.control.json"].get("progress", {}).get("append_only") is not True:
        raise ControlJsonValidationError("plan.control.json: progress.append_only must be true")
    if runtime.get("progress", {}).get("append_only") is not True:
        raise ControlJsonValidationError("runtime.control.json: progress.append_only must be true")
    if artifacts["plan.control.json"].get("verifier", {}).get("required_before_goal_achieved") is not True:
        raise ControlJsonValidationError("plan.control.json: verifier must be required before goal_achieved")
    if runtime.get("verifier", {}).get("required_before_goal_achieved") is not True or not runtime.get("verifier", {}).get("command"):
        raise ControlJsonValidationError("runtime.control.json: verifier command is required before goal_achieved")

    review_checks = artifacts["review.control.json"].get("review_checks", [])
    checks_by_id = {check.get("check_id"): check for check in review_checks if isinstance(check, dict)}
    missing_checks = sorted(REQUIRED_REVIEW_CHECKS - set(checks_by_id))
    if missing_checks:
        raise ControlJsonValidationError("review.control.json: missing required review checks: " + ", ".join(missing_checks))
    failed_checks = sorted(
        check_id
        for check_id in REQUIRED_REVIEW_CHECKS
        if checks_by_id[check_id].get("status") != "pass"
        or checks_by_id[check_id].get("verdict") != "approved"
        or checks_by_id[check_id].get("return_to_stage") is not None
        or not string_list(checks_by_id[check_id].get("evidence"))
    )
    if failed_checks:
        raise ControlJsonValidationError("review.control.json: required review checks did not pass: " + ", ".join(failed_checks))

    workflow_registry = read_json_object(DELEGATION_WORKFLOW_REGISTRY)

    selected_workflow = registry_bindings(runtime).get("selected_agent_workflow")
    plan_workflow = registry_bindings(artifacts["plan.control.json"]).get("selected_agent_workflow")
    work_assignment = registry_bindings(artifacts["plan.control.json"]).get("allowed_work_assignment")
    if not selected_workflow or selected_workflow not in workflow_registry:
        raise ControlJsonValidationError("unknown selected agent workflow")
    if selected_workflow != plan_workflow:
        raise ControlJsonValidationError("selected_agent_workflow must be consistent across plan and runtime")
    if work_assignment not in workflow_registry[selected_workflow].get("allowed_work_assignment", []):
        raise ControlJsonValidationError("allowed_work_assignment is not permitted by workflow registry")

    runtime_steps = step_ids(runtime)
    plan_steps = step_ids(artifacts["plan.control.json"])
    goal_steps = step_ids(artifacts["goal.control.json"])
    plan_step_outcomes = step_outcome_map(artifacts["plan.control.json"])
    plan_alignment = step_action_alignment_map(artifacts["plan.control.json"])
    if not runtime_steps:
        raise ControlJsonValidationError("runtime.control.json must declare required_steps")
    if not runtime_steps <= plan_steps:
        raise ControlJsonValidationError("runtime required_steps must be present in plan.control.json")
    if not runtime_steps <= goal_steps:
        raise ControlJsonValidationError("runtime required_steps must be present in goal.control.json")
    missing_runtime_alignment = sorted(runtime_steps - set(plan_alignment))
    if missing_runtime_alignment:
        raise ControlJsonValidationError(
            "plan.control.json step_action_alignment missing runtime required steps: "
            + ", ".join(missing_runtime_alignment)
        )

    required_outcomes = blocking_required_outcomes(artifacts["requirements.control.json"])
    if required_outcomes:
        for filename in ("design.control.json", "goal.control.json", "plan.control.json", "runtime.control.json"):
            require_outcome_coverage(
                f"{filename} required_steps do not satisfy blocking required outcomes",
                covered_outcomes_by_steps(step_outcome_map(artifacts[filename])),
                required_outcomes,
            )

        verifier_outcomes = set(string_list(runtime.get("verifier", {}).get("required_outcomes")))
        require_outcome_coverage(
            "runtime.control.json verifier.required_outcomes missing blocking required outcomes",
            verifier_outcomes,
            required_outcomes,
        )

    covered_steps: set[str] = set()
    mainline_producing_steps: set[str] = set()
    for package in artifacts["plan.control.json"].get("work_packages", []):
        package_steps = set(string_list(package.get("required_steps")))
        covered_steps.update(package_steps)
        if not string_list(package.get("required_tests")):
            raise ControlJsonValidationError("plan.control.json: work package missing required tests")
        used_alignment = set(string_list(package.get("uses_step_action_alignment")))
        if not package_steps <= used_alignment:
            raise ControlJsonValidationError("plan.control.json work package missing producing action alignment for required steps")
        unknown_alignment = sorted(used_alignment - set(plan_alignment))
        if unknown_alignment:
            raise ControlJsonValidationError(
                "plan.control.json work package references unknown producing action alignment: "
                + ", ".join(unknown_alignment)
            )
        for step_id in used_alignment:
            alignment = plan_alignment[step_id]
            for write_path in alignment_write_paths(alignment):
                if not path_is_under(write_path, string_list(package.get("allowed_write_paths"))):
                    raise ControlJsonValidationError(
                        "plan.control.json producing action write authority is not covered by work package allowed_write_paths"
                    )
        package_outcomes = covered_outcomes_by_steps(plan_step_outcomes, package_steps)
        if package_outcomes & required_outcomes:
            if (
                package.get("role") != "mainline"
                or package.get("counts_as_goal_progress") is not True
                or package.get("not_merely_verification") is not True
            ):
                raise ControlJsonValidationError(
                    "plan.control.json mainline work package required for blocking outcomes must use a producing action"
                )
            mainline_producing_steps.update(package_steps)
    if required_outcomes:
        require_outcome_coverage(
            "plan.control.json work_packages do not cover blocking required outcomes",
            covered_outcomes_by_steps(plan_step_outcomes, covered_steps),
            required_outcomes,
        )
        require_outcome_coverage(
            "plan.control.json mainline producing work packages do not cover blocking required outcomes",
            covered_outcomes_by_steps(plan_step_outcomes, mainline_producing_steps),
            required_outcomes,
        )
    if not runtime_steps <= covered_steps:
        raise ControlJsonValidationError("runtime required_steps must be covered by work packages")

    return artifacts


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
