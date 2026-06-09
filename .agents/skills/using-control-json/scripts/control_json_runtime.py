from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[4]
ANSWER_METHOD_REGISTRY = REPO_ROOT / ".agents/skills/references/answer-method-registry.json"
DELEGATION_WORKFLOW_REGISTRY = REPO_ROOT / ".agents/skills/references/delegation-workflow-registry.json"

CONTROL_FILES = {
    "requirements": "requirements.control.json",
    "design": "design.control.json",
    "goal": "goal.control.json",
    "plan": "plan.control.json",
    "review": "review.control.json",
    "runtime": "runtime.control.json",
}
READONLY_FILES = tuple(CONTROL_FILES.values())
WRITABLE_FILES = ("progress.jsonl", "runtime-status.json", "final-report.json")
REQUIRED_REVIEW_CHECKS = {
    "design-answer-method",
    "required-answer-path",
    "intent-preservation",
    "obligation-preservation",
    "required-outcome-coverage",
    "work-assignment",
    "horizon-authority",
    "final-observer",
}
REVIEW_HASH_FILES = (
    "requirements.control.json",
    "design.control.json",
    "goal.control.json",
    "plan.control.json",
)

EVENT_TYPES = {
    "step.started",
    "step.completed",
    "step.blocked",
    "verification.completed",
    "final_report.written",
}
EVENT_STATUSES = {"pass", "fail", "blocked", "partial"}
PROGRESS_ROLES = {"mainline", "supporting_only"}
REQUIRED_EVIDENCE_KINDS = {"progress_event", "file_exists", "json_file", "command_result"}


class ControlJsonError(Exception):
    pass


def canonical_json_hash(value: dict[str, Any], *, omit_top_level: set[str] | None = None) -> str:
    canonical_value = copy.deepcopy(value)
    for key in omit_top_level or set():
        canonical_value.pop(key, None)
    encoded = json.dumps(canonical_value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return "sha256:" + hashlib.sha256(encoded).hexdigest()


def semantic_base_hash(requirements: dict[str, Any]) -> str:
    approved = requirements.get("approved_control")
    if not isinstance(approved, dict):
        return ""
    semantic_value = copy.deepcopy(approved)
    semantic_value.pop("semantic_base", None)
    return canonical_json_hash(semantic_value)


def control_file_hash(filename: str, artifact: dict[str, Any]) -> str:
    omit = {"approved_control_hashes"} if filename == "runtime.control.json" else set()
    return canonical_json_hash(artifact, omit_top_level=omit)


def expected_hashes(artifacts: dict[str, dict[str, Any]], filenames: tuple[str, ...]) -> dict[str, str]:
    key_by_filename = {filename: key for key, filename in CONTROL_FILES.items()}
    return {filename: control_file_hash(filename, artifacts[key_by_filename[filename]]) for filename in filenames}


def check_hashes(label: str, actual: Any, expected: dict[str, str]) -> list[str]:
    if not isinstance(actual, dict):
        return [f"{label} approved_control_hashes must be an object"]
    errors: list[str] = []
    for filename, expected_hash in expected.items():
        if actual.get(filename) != expected_hash:
            errors.append(f"{label} approved_control_hashes mismatch for {filename}")
    return errors


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ControlJsonError(f"missing JSON file: {path.name}") from exc
    except json.JSONDecodeError as exc:
        raise ControlJsonError(f"invalid JSON in {path.name}: {exc}") from exc
    if not isinstance(value, dict):
        raise ControlJsonError(f"{path.name} must contain a JSON object")
    return value


def load_control_files(run_dir: Path) -> dict[str, dict[str, Any]]:
    artifacts = {}
    for key, filename in CONTROL_FILES.items():
        artifacts[key] = load_json(run_dir / filename)
    return artifacts


def require_keys(name: str, value: dict[str, Any], keys: tuple[str, ...], errors: list[str]) -> None:
    missing = [key for key in keys if key not in value]
    if missing:
        errors.append(f"{name} missing required fields: {', '.join(missing)}")


def string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, str)]


def registry_bindings(artifact: dict[str, Any]) -> dict[str, Any]:
    bindings = artifact.get("registry_bindings")
    return bindings if isinstance(bindings, dict) else {}


def step_ids(artifact: dict[str, Any]) -> set[str]:
    steps = artifact.get("required_steps")
    if not isinstance(steps, list):
        return set()
    return {
        step.get("step_id")
        for step in steps
        if isinstance(step, dict) and isinstance(step.get("step_id"), str)
    }


def required_outcome_sets(requirements: dict[str, Any]) -> tuple[set[str], set[str], list[str]]:
    outcomes = requirements.get("approved_control", {}).get("required_outcomes")
    if outcomes is None:
        return set(), set(), []
    if not isinstance(outcomes, list):
        return set(), set(), ["requirements.control.json approved_control.required_outcomes must be a list"]

    all_outcomes: set[str] = set()
    blocking_outcomes: set[str] = set()
    errors: list[str] = []
    for index, outcome in enumerate(outcomes):
        if not isinstance(outcome, dict):
            errors.append(f"requirements.control.json required_outcomes[{index}] must be an object")
            continue

        outcome_id = outcome.get("id")
        if not isinstance(outcome_id, str) or not outcome_id:
            errors.append(f"requirements.control.json required_outcomes[{index}].id must be a non-empty string")
            continue
        if outcome_id in all_outcomes:
            errors.append(f"requirements.control.json duplicate required_outcomes id: {outcome_id}")
            continue
        all_outcomes.add(outcome_id)

        blocks = outcome.get("blocks_goal_achieved_if_missing")
        if not isinstance(blocks, bool):
            errors.append(
                f"requirements.control.json required_outcomes[{index}].blocks_goal_achieved_if_missing must be boolean"
            )
            continue
        required_evidence = outcome.get("required_evidence")
        if not isinstance(required_evidence, list) or not required_evidence:
            errors.append(f"requirements.control.json required_outcomes[{index}].required_evidence must be a non-empty list")
            continue
        seen_evidence: set[str] = set()
        for evidence_index, evidence in enumerate(required_evidence):
            if not isinstance(evidence, dict):
                errors.append(
                    f"requirements.control.json required_outcomes[{index}].required_evidence[{evidence_index}] must be an object"
                )
                continue
            evidence_id = evidence.get("evidence_id")
            if not isinstance(evidence_id, str) or not evidence_id:
                errors.append(
                    f"requirements.control.json required_outcomes[{index}].required_evidence[{evidence_index}].evidence_id must be a non-empty string"
                )
                continue
            if evidence_id in seen_evidence:
                errors.append(
                    f"requirements.control.json required_outcomes[{index}] duplicate required_evidence id: {evidence_id}"
                )
                continue
            seen_evidence.add(evidence_id)
            kind = evidence.get("kind")
            if kind not in REQUIRED_EVIDENCE_KINDS:
                errors.append(
                    f"requirements.control.json required_outcomes[{index}].required_evidence[{evidence_index}].kind is not recognized"
                )
            description = evidence.get("description")
            if not isinstance(description, str) or not description:
                errors.append(
                    f"requirements.control.json required_outcomes[{index}].required_evidence[{evidence_index}].description must be a non-empty string"
                )
        if blocks:
            blocking_outcomes.add(outcome_id)
    return all_outcomes, blocking_outcomes, errors


def required_evidence_by_outcome(requirements: dict[str, Any]) -> dict[str, set[str]]:
    outcomes = requirements.get("approved_control", {}).get("required_outcomes")
    if not isinstance(outcomes, list):
        return {}
    evidence_by_outcome: dict[str, set[str]] = {}
    for outcome in outcomes:
        if not isinstance(outcome, dict) or not isinstance(outcome.get("id"), str):
            continue
        required_evidence = outcome.get("required_evidence")
        if not isinstance(required_evidence, list):
            continue
        evidence_ids = {
            evidence.get("evidence_id")
            for evidence in required_evidence
            if isinstance(evidence, dict) and isinstance(evidence.get("evidence_id"), str) and evidence.get("evidence_id")
        }
        evidence_by_outcome[outcome["id"]] = evidence_ids
    return evidence_by_outcome


def blocking_required_outcomes(requirements: dict[str, Any]) -> set[str]:
    _, blocking_outcomes, _ = required_outcome_sets(requirements)
    return blocking_outcomes


def step_outcome_map(
    artifact: dict[str, Any],
    *,
    known_outcomes: set[str] | None = None,
    errors: list[str] | None = None,
    label: str = "control artifact",
) -> dict[str, set[str]]:
    steps = artifact.get("required_steps")
    if not isinstance(steps, list):
        return {}
    mapped: dict[str, set[str]] = {}
    for index, step in enumerate(steps):
        if not isinstance(step, dict) or not isinstance(step.get("step_id"), str):
            continue
        step_id = step["step_id"]
        raw_outcomes = step.get("satisfies_outcomes", [])
        if not isinstance(raw_outcomes, list) or not all(isinstance(outcome, str) and outcome for outcome in raw_outcomes):
            if errors is not None:
                errors.append(f"{label} required_steps[{index}].satisfies_outcomes must be a list of non-empty strings")
            mapped[step_id] = set()
            continue
        outcome_ids = set(raw_outcomes)
        if known_outcomes is not None:
            unknown = sorted(outcome_ids - known_outcomes)
            if unknown and errors is not None:
                errors.append(
                    f"{label} required_steps.{step_id}.satisfies_outcomes references unknown required outcomes: "
                    + ", ".join(unknown)
                )
        mapped[step_id] = outcome_ids
    return mapped


def covered_outcomes_by_steps(step_map: dict[str, set[str]], steps: set[str] | None = None) -> set[str]:
    selected = steps if steps is not None else set(step_map)
    covered: set[str] = set()
    for step_id in selected:
        covered.update(step_map.get(step_id, set()))
    return covered


def validate_event(event: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for field in (
        "event_type",
        "schema_version",
        "occurred_at",
        "work_package_id",
        "required_step",
        "status",
        "evidence",
    ):
        if field not in event:
            errors.append(f"event missing required field: {field}")

    if event.get("event_type") not in EVENT_TYPES:
        errors.append("event_type is not recognized")
    if event.get("status") not in EVENT_STATUSES:
        errors.append("status is not recognized")
    if not isinstance(event.get("required_step"), str) or not event.get("required_step"):
        errors.append("required_step must be a non-empty string")
    evidence = event.get("evidence")
    if not isinstance(evidence, list) or not evidence or not all(isinstance(item, str) and item for item in evidence):
        errors.append("evidence must be a non-empty list")

    role = event.get("progress_role", "mainline")
    if role not in PROGRESS_ROLES:
        errors.append("progress_role is not recognized")
    counts = event.get("counts_as_goal_progress", role == "mainline")
    if not isinstance(counts, bool):
        errors.append("counts_as_goal_progress must be boolean when present")
    if role == "supporting_only" and counts:
        errors.append("supporting-only progress cannot count as goal progress")
    return errors


def read_progress_events(path: Path) -> tuple[list[dict[str, Any]], list[str]]:
    if not path.exists():
        return [], [f"missing runtime progress file: {path.name}"]
    events: list[dict[str, Any]] = []
    errors: list[str] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError as exc:
            errors.append(f"progress.jsonl line {line_number} is invalid JSON: {exc}")
            continue
        if not isinstance(event, dict):
            errors.append(f"progress.jsonl line {line_number} must be a JSON object")
            continue
        event_errors = validate_event(event)
        errors.extend(f"progress.jsonl line {line_number}: {error}" for error in event_errors)
        events.append(event)
    return events, errors


def validate_control_chain(run_dir: Path) -> tuple[dict[str, dict[str, Any]] | None, list[str]]:
    errors: list[str] = []
    try:
        artifacts = load_control_files(run_dir)
    except ControlJsonError as exc:
        return None, [str(exc)]

    for key, artifact in artifacts.items():
        require_keys(
            CONTROL_FILES[key],
            artifact,
            ("artifact_type", "schema_version", "status"),
            errors,
        )

    expected_artifact_types = {
        "requirements": "requirements.control",
        "design": "design.control",
        "goal": "goal.control",
        "plan": "plan.control",
        "review": "review.control",
        "runtime": "runtime.control",
    }
    expected_statuses = {
        "requirements": "approved",
        "design": "approved",
        "goal": "approved",
        "plan": "approved",
        "review": "approved",
        "runtime": "compiled",
    }
    for key, expected in expected_artifact_types.items():
        if artifacts[key].get("artifact_type") != expected:
            errors.append(f"{CONTROL_FILES[key]} artifact_type must be {expected}")
    for key, expected in expected_statuses.items():
        if artifacts[key].get("status") != expected:
            errors.append(f"{CONTROL_FILES[key]} status must be {expected}")

    runtime_chain = artifacts["runtime"].get("control_chain")
    if runtime_chain != {key: filename for key, filename in CONTROL_FILES.items() if key != "runtime"}:
        errors.append("runtime.control.json has inconsistent control chain references")

    semantic_base = artifacts["requirements"].get("approved_control", {}).get("semantic_base")
    if not isinstance(semantic_base, dict) or semantic_base.get("hash") != semantic_base_hash(artifacts["requirements"]):
        errors.append("requirements.control.json semantic_base hash must match approved_control")
    for key in ("design", "goal", "plan", "review", "runtime"):
        if artifacts[key].get("semantic_base_ref") != semantic_base:
            errors.append(f"{CONTROL_FILES[key]} semantic_base_ref must match requirements approved semantic_base")

    errors.extend(
        check_hashes(
            "review.control.json",
            artifacts["review"].get("approved_control_hashes"),
            expected_hashes(artifacts, REVIEW_HASH_FILES),
        )
    )
    errors.extend(
        check_hashes(
            "runtime.control.json",
            artifacts["runtime"].get("approved_control_hashes"),
            expected_hashes(artifacts, READONLY_FILES),
        )
    )

    expected_sources = {
        "design": {"requirements": "requirements.control.json"},
        "goal": {"requirements": "requirements.control.json", "design": "design.control.json"},
        "plan": {
            "requirements": "requirements.control.json",
            "design": "design.control.json",
            "goal": "goal.control.json",
        },
        "review": {
            "requirements": "requirements.control.json",
            "design": "design.control.json",
            "goal": "goal.control.json",
            "plan": "plan.control.json",
        },
    }
    for key, expected in expected_sources.items():
        source_contracts = artifacts[key].get("source_contracts")
        if not isinstance(source_contracts, dict):
            errors.append(f"{CONTROL_FILES[key]} missing source_contracts")
            continue
        for source_key, source_file in expected.items():
            if source_contracts.get(source_key) != source_file:
                errors.append(f"{CONTROL_FILES[key]} has inconsistent {source_key} source contract")

    readonly = artifacts["runtime"].get("runtime", {}).get("readonly_files")
    writable = artifacts["runtime"].get("runtime", {}).get("writable_files")
    if readonly != list(READONLY_FILES):
        errors.append("runtime.control.json readonly_files must declare approved control JSON as read-only")
    if writable != list(WRITABLE_FILES):
        errors.append("runtime.control.json writable_files must be progress.jsonl, runtime-status.json, final-report.json")
    plan_runtime = artifacts["plan"].get("runtime", {})
    if plan_runtime.get("readonly_files") != list(READONLY_FILES):
        errors.append("plan.control.json readonly_files must match runtime.control.json")
    if plan_runtime.get("writable_files") != list(WRITABLE_FILES):
        errors.append("plan.control.json writable_files must match runtime.control.json")

    if artifacts["plan"].get("progress", {}).get("append_only") is not True:
        errors.append("plan.control.json progress.append_only must be true")
    if artifacts["runtime"].get("progress", {}).get("append_only") is not True:
        errors.append("runtime.control.json progress.append_only must be true")
    if artifacts["plan"].get("verifier", {}).get("required_before_goal_achieved") is not True:
        errors.append("plan.control.json verifier must be required before goal_achieved")
    if artifacts["runtime"].get("verifier", {}).get("required_before_goal_achieved") is not True:
        errors.append("runtime.control.json verifier must be required before goal_achieved")
    if not artifacts["runtime"].get("verifier", {}).get("command"):
        errors.append("runtime.control.json verifier.command is required")

    review_checks = artifacts["review"].get("review_checks")
    if not isinstance(review_checks, list):
        errors.append("review.control.json missing review_checks")
    else:
        checks_by_id = {check.get("check_id"): check for check in review_checks if isinstance(check, dict)}
        missing = sorted(REQUIRED_REVIEW_CHECKS - set(checks_by_id))
        if missing:
            errors.append(f"missing required review checks: {', '.join(missing)}")
        for check_id in REQUIRED_REVIEW_CHECKS & set(checks_by_id):
            check = checks_by_id[check_id]
            if (
                check.get("status") != "pass"
                or check.get("verdict") != "approved"
                or check.get("return_to_stage") is not None
                or not string_list(check.get("evidence"))
            ):
                errors.append(f"required review check did not pass with evidence: {check_id}")

    try:
        answer_registry = load_json(ANSWER_METHOD_REGISTRY)
        workflow_registry = load_json(DELEGATION_WORKFLOW_REGISTRY)
    except ControlJsonError as exc:
        errors.append(str(exc))
        answer_registry = {}
        workflow_registry = {}

    answer_keys = [
        registry_bindings(artifacts[key]).get("answer_method_key")
        for key in ("requirements", "design", "goal", "plan", "runtime", "review")
        if registry_bindings(artifacts[key]).get("answer_method_key")
    ]
    selected_answer_key = registry_bindings(artifacts["runtime"]).get("answer_method_key")
    forbidden_keys = [
        registry_bindings(artifacts[key]).get("forbidden_substitute_key")
        for key in ("requirements", "design", "goal")
        if registry_bindings(artifacts[key]).get("forbidden_substitute_key")
    ]
    if not selected_answer_key or selected_answer_key not in answer_registry or selected_answer_key in forbidden_keys:
        errors.append("forbidden or unknown answer method")
    if any(key != selected_answer_key for key in answer_keys):
        errors.append("answer_method_key must be consistent across the control chain")

    if selected_answer_key in answer_registry:
        done_rule = answer_registry[selected_answer_key].get("done_rule", {})
        if not isinstance(done_rule, dict) or done_rule.get("all_mandatory_nodes_required") is not True:
            errors.append("answer method registry missing done_rule.all_mandatory_nodes_required")
        forbidden_substitutions = set(string_list(answer_registry[selected_answer_key].get("forbidden_substitutions")))
        if forbidden_substitutions & set(answer_keys):
            errors.append("forbidden or unknown answer method")
        approved_path = [
            item.casefold()
            for item in string_list(artifacts["design"].get("approved_control", {}).get("required_answer_path"))
        ]
        missing_nodes = [
            node
            for node in string_list(answer_registry[selected_answer_key].get("mandatory_nodes"))
            if node.casefold() not in approved_path
        ]
        if missing_nodes:
            errors.append(f"missing mandatory answer path nodes: {', '.join(missing_nodes)}")

    selected_workflow = registry_bindings(artifacts["runtime"]).get("selected_agent_workflow")
    plan_workflow = registry_bindings(artifacts["plan"]).get("selected_agent_workflow")
    assignment = registry_bindings(artifacts["plan"]).get("allowed_work_assignment")
    if not selected_workflow or selected_workflow not in workflow_registry:
        errors.append("unknown selected agent workflow")
    if selected_workflow != plan_workflow:
        errors.append("selected_agent_workflow must be consistent across plan and runtime")
    if selected_workflow in workflow_registry:
        allowed_assignments = workflow_registry[selected_workflow].get("allowed_work_assignment", [])
        if assignment not in allowed_assignments:
            errors.append("allowed_work_assignment is not permitted by workflow registry")

    plan_steps = step_ids(artifacts["plan"])
    goal_steps = step_ids(artifacts["goal"])
    runtime_steps = step_ids(artifacts["runtime"])
    if not runtime_steps:
        errors.append("runtime.control.json must declare required_steps")
    if not runtime_steps <= plan_steps:
        errors.append("runtime required_steps must be present in plan.control.json")
    if not runtime_steps <= goal_steps:
        errors.append("runtime required_steps must be present in goal.control.json")

    all_required_outcomes, required_outcomes, outcome_errors = required_outcome_sets(artifacts["requirements"])
    errors.extend(outcome_errors)
    step_outcomes_by_key: dict[str, dict[str, set[str]]] = {}
    if all_required_outcomes:
        for key in ("design", "goal", "plan", "runtime"):
            step_outcomes_by_key[key] = step_outcome_map(
                artifacts[key],
                known_outcomes=all_required_outcomes,
                errors=errors,
                label=CONTROL_FILES[key],
            )
    if required_outcomes:
        for key in ("design", "goal", "plan", "runtime"):
            covered = covered_outcomes_by_steps(step_outcomes_by_key.get(key, {}))
            missing = sorted(required_outcomes - covered)
            if missing:
                errors.append(
                    f"{CONTROL_FILES[key]} required_steps do not satisfy blocking required outcomes: "
                    + ", ".join(missing)
                )

        raw_verifier_outcomes = artifacts["runtime"].get("verifier", {}).get("required_outcomes")
        if not isinstance(raw_verifier_outcomes, list) or not all(
            isinstance(outcome, str) and outcome for outcome in raw_verifier_outcomes
        ):
            verifier_outcomes: set[str] = set()
            errors.append("runtime.control.json verifier.required_outcomes must be a list of non-empty strings")
        else:
            verifier_outcomes = set(raw_verifier_outcomes)
            unknown_verifier_outcomes = sorted(verifier_outcomes - all_required_outcomes)
            if unknown_verifier_outcomes:
                errors.append(
                    "runtime.control.json verifier.required_outcomes references unknown required outcomes: "
                    + ", ".join(unknown_verifier_outcomes)
                )
        missing_verifier = sorted(required_outcomes - verifier_outcomes)
        if missing_verifier:
            errors.append(
                "runtime.control.json verifier.required_outcomes missing blocking required outcomes: "
                + ", ".join(missing_verifier)
            )

    work_packages = artifacts["plan"].get("work_packages")
    if not isinstance(work_packages, list) or not work_packages:
        errors.append("plan.control.json must declare work_packages")
    else:
        covered_steps: set[str] = set()
        for package in work_packages:
            if not isinstance(package, dict):
                errors.append("plan.control.json work_packages entries must be objects")
                continue
            if not string_list(package.get("required_tests")):
                errors.append("work package missing required checks")
            covered_steps.update(string_list(package.get("required_steps")))
        if not runtime_steps <= covered_steps:
            errors.append("runtime required_steps must be covered by work packages")
        if required_outcomes:
            covered_outcomes = covered_outcomes_by_steps(step_outcomes_by_key.get("plan", {}), covered_steps)
            missing_outcomes = sorted(required_outcomes - covered_outcomes)
            if missing_outcomes:
                errors.append(
                    "plan.control.json work_packages do not cover blocking required outcomes: "
                    + ", ".join(missing_outcomes)
                )

    return artifacts, errors


def verify_approved_hashes(run_dir: Path, hash_file: Path, readonly_files: tuple[str, ...] = READONLY_FILES) -> list[str]:
    try:
        expected = load_json(hash_file)
    except ControlJsonError as exc:
        return [str(exc)]
    errors: list[str] = []
    for filename in readonly_files:
        if filename not in expected:
            errors.append(f"approved hash missing for {filename}")
            continue
        actual = hashlib.sha256((run_dir / filename).read_bytes()).hexdigest()
        if actual != expected[filename]:
            errors.append(f"approved control JSON changed after runtime start: {filename}")
    return errors


def result_payload(ok: bool, errors: list[str], **extra: Any) -> dict[str, Any]:
    payload: dict[str, Any] = {"ok": ok, "errors": errors}
    payload.update(extra)
    return payload
