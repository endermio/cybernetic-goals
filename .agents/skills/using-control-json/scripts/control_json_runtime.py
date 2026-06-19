from __future__ import annotations

import copy
import hashlib
import json
import re
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[4]
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
DEFAULT_WRITABLE_EVIDENCE_PATHS = ("evidence/",)
RUN_STRATEGY_FIELDS = (
    "control_level",
    "target_model",
    "strategy_policy",
    "gate_mode",
    "phase_structure",
)
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
COUNTEREXAMPLE_GATE_CHECK = "counterexample-gate"
COUNTEREXAMPLE_GATE_POINTS = {
    "source_requirements->required_outcomes",
    "required_outcomes->required_steps",
    "required_steps->work_packages",
    "required_steps->runtime_steps",
    "pre_runtime_compile",
    "blocked_or_goal_achieved",
}
COUNTEREXAMPLE_REVIEWER_KINDS = {"subagent", "human", "external"}
MEASUREMENT_ACTION_RE = re.compile(r"\b(?:measure|measuring|measured)\b", re.IGNORECASE)
MEASUREMENT_CURVE_LANGUAGE_RE = re.compile(r"\b(?:curve|curves|growth)\b", re.IGNORECASE)
API_V2_IMPLEMENT_ACTION_RE = re.compile(r"\b(?:implement|implementing)\b", re.IGNORECASE)
API_V2_FAMILY_RE = re.compile(
    r"(?<![A-Za-z])(?:download|extract|preview|route|routes|endpoint|endpoints|api\s+family)(?![A-Za-z])",
    re.IGNORECASE,
)
FRAMEWORK_WEAKENING_LANGUAGE_RE = re.compile(
    r"\b(?:define|document|draft|list|outline|plan|prepare|describe|catalog|enumerate)\b"
    r".*\b(?:framework|scan|variables?|rules?|plan|readiness|compatibility|compatible)\b"
    r"|"
    r"\b(?:framework|scan)\b"
    r".*\b(?:document|plan|readiness|compatibility|compatible|variables?|rules?|listing|list)\b",
    re.IGNORECASE,
)
READINESS_WEAKENING_LANGUAGE_RE = re.compile(
    r"\b(?:future|compat(?:ibility|ible)?|readiness|ready|framework)\b",
    re.IGNORECASE,
)
REQUIRED_REVIEW_CHECKS = {
    "required-answer-path",
    "intent-preservation",
    "obligation-preservation",
    "required-outcome-coverage",
    SOURCE_REQUIREMENT_REVIEW_CHECK,
    COUNTEREXAMPLE_GATE_CHECK,
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
    COUNTEREXAMPLE_GATE_CHECK,
    "horizon-authority",
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
    "step.failed",
    "observation.recorded",
    "runtime.generation.started",
    "runtime.generation.superseded",
    "control.amendment.proposed",
    "control.amendment.approved",
    "control.amendment.rejected",
    "control.amendment.blocked",
    "verification.completed",
    "final_report.written",
}
EVENT_STATUSES = {"pass", "fail", "blocked", "partial"}
PROGRESS_ROLES = {"mainline", "supporting_only"}
REQUIRED_EVIDENCE_KINDS = {"progress_event", "file_exists", "json_file", "command_result"}
STEP_EVENT_TYPES = {"step.started", "step.completed", "step.blocked", "step.failed"}
AMENDMENT_EVENT_TYPES = {
    "control.amendment.proposed",
    "control.amendment.approved",
    "control.amendment.rejected",
    "control.amendment.blocked",
}
GENERATION_EVENT_TYPES = {"runtime.generation.started", "runtime.generation.superseded"}
OBSERVATION_EVENT_TYPES = {"observation.recorded"}
OBSERVATION_STRING_FIELDS = (
    "corrects_event_ref",
    "classification",
    "summary",
    "evidence_id",
    "evidence_path",
)
AMENDMENT_ANCHOR_FIELDS = ("semantic_base_change", "required_outcomes_changed", "authority_expanded")
AMENDMENT_PROPOSAL_REQUIRED_FIELDS = (
    "reason",
    "triggering_observation",
    "affected_stages",
    "affected_source_requirements",
    *AMENDMENT_ANCHOR_FIELDS,
    "proposed_changes",
    "review_required",
    "patch_ref",
)


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
    omit = {"approved_control_hashes"} if filename.endswith("runtime.control.json") else set()
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


def amendment_generation_count(run_control: dict[str, Any]) -> int:
    generations = run_control.get("generations")
    if not isinstance(generations, list):
        return 0
    return sum(1 for generation in generations if isinstance(generation, dict) and generation.get("parent"))


def counterexample_gate_contract(requirements: dict[str, Any] | None) -> dict[str, Any]:
    if not isinstance(requirements, dict):
        return {}
    contract = requirements.get("approved_control", {}).get("counterexample_gate_contract")
    return contract if isinstance(contract, dict) else {}


def counterexample_contract_errors(requirements: dict[str, Any]) -> list[str]:
    schema_version = str(requirements.get("schema_version", ""))
    contract = counterexample_gate_contract(requirements)
    if schema_version < "1.1.0" and not contract:
        return []
    errors: list[str] = []
    if not contract:
        return ["requirements.control.json approved_control.counterexample_gate_contract is required for schema_version >= 1.1.0"]
    if not isinstance(contract.get("quality_standard"), str) or not contract.get("quality_standard"):
        errors.append("requirements.control.json counterexample_gate_contract.quality_standard must be a non-empty string")
    required_points = string_list(contract.get("required_checked_transformations"))
    if not required_points:
        errors.append(
            "requirements.control.json counterexample_gate_contract.required_checked_transformations must be a non-empty list"
        )
    minimum = contract.get("minimum_reviewer")
    if not isinstance(minimum, dict):
        errors.append("requirements.control.json counterexample_gate_contract.minimum_reviewer must be an object")
    else:
        allowed = set(string_list(minimum.get("allowed_kinds")))
        if not allowed:
            errors.append(
                "requirements.control.json counterexample_gate_contract.minimum_reviewer.allowed_kinds must be non-empty"
            )
        elif not allowed.issubset(COUNTEREXAMPLE_REVIEWER_KINDS):
            errors.append(
                "requirements.control.json counterexample_gate_contract.minimum_reviewer.allowed_kinds contains unknown kinds"
            )
        if not isinstance(minimum.get("independence"), str) or not minimum.get("independence"):
            errors.append(
                "requirements.control.json counterexample_gate_contract.minimum_reviewer.independence must be a non-empty string"
            )
        if not isinstance(minimum.get("evidence_ref_required"), bool):
            errors.append(
                "requirements.control.json counterexample_gate_contract.minimum_reviewer.evidence_ref_required must be boolean"
            )
    reject_if = contract.get("reject_if")
    if not isinstance(reject_if, list) or not string_list(reject_if):
        errors.append("requirements.control.json counterexample_gate_contract.reject_if must be a non-empty list")
    return errors


def counterexample_contract_points(requirements: dict[str, Any] | None) -> set[str]:
    contract = counterexample_gate_contract(requirements)
    return set(string_list(contract.get("required_checked_transformations")))


def counterexample_allowed_reviewer_kinds(requirements: dict[str, Any] | None) -> set[str]:
    contract = counterexample_gate_contract(requirements)
    minimum = contract.get("minimum_reviewer")
    if not isinstance(minimum, dict):
        return set(COUNTEREXAMPLE_REVIEWER_KINDS)
    allowed = set(string_list(minimum.get("allowed_kinds")))
    return allowed or set(COUNTEREXAMPLE_REVIEWER_KINDS)


def generation_review_errors(
    review: dict[str, Any],
    *,
    context: str,
    requirements: dict[str, Any] | None = None,
) -> list[str]:
    review_checks = review.get("review_checks")
    if not isinstance(review_checks, list):
        return [f"{context} review missing review_checks"]
    checks_by_id = {check.get("check_id"): check for check in review_checks if isinstance(check, dict)}
    errors: list[str] = []
    missing = sorted(GENERATION_REVIEW_CHECKS - set(checks_by_id))
    if missing:
        errors.append(f"{context} review missing required review checks: {', '.join(missing)}")
    for check_id in GENERATION_REVIEW_CHECKS & set(checks_by_id):
        check = checks_by_id[check_id]
        if (
            check.get("status") != "pass"
            or check.get("verdict") != "approved"
            or check.get("return_to_stage") is not None
            or not string_list(check.get("evidence"))
        ):
            errors.append(f"{context} required review check did not pass with evidence: {check_id}")
    counterexample = checks_by_id.get(COUNTEREXAMPLE_GATE_CHECK)
    if isinstance(counterexample, dict):
        checked = set(string_list(counterexample.get("checked_transformations")))
        missing_points = sorted(COUNTEREXAMPLE_GATE_POINTS - checked)
        if missing_points:
            errors.append(
                f"{context} counterexample-gate missing required gate points: "
                + ", ".join(missing_points)
            )
        contract_missing_points = sorted(counterexample_contract_points(requirements) - checked)
        if contract_missing_points:
            errors.append(
                f"{context} counterexample-gate missing requirements-approved gate points: "
                + ", ".join(contract_missing_points)
            )
        reviewer = counterexample.get("reviewer")
        if not isinstance(reviewer, dict):
            errors.append(f"{context} counterexample-gate missing independent reviewer provenance")
        else:
            allowed_reviewer_kinds = counterexample_allowed_reviewer_kinds(requirements)
            if (
                reviewer.get("kind") not in allowed_reviewer_kinds
                or not isinstance(reviewer.get("id"), str)
                or not reviewer["id"].strip()
                or not isinstance(reviewer.get("evidence_ref"), str)
                or not reviewer["evidence_ref"].strip()
            ):
                errors.append(
                    f"{context} counterexample-gate reviewer provenance must be subagent, human, or external "
                    "with id and evidence_ref"
                )
    return errors


def generation_runtime_readonly_files(generation: dict[str, Any]) -> list[str]:
    files = ["requirements.control.json", "run.control.json", generation["runtime"]]
    review = generation.get("review")
    if isinstance(review, str) and review:
        files.insert(2, review)
    return files


def load_generation_control_files(run_dir: Path) -> tuple[dict[str, dict[str, Any]] | None, list[str]]:
    errors: list[str] = []
    try:
        requirements = load_json(run_dir / "requirements.control.json")
        run_control = load_json(run_dir / "run.control.json")
    except ControlJsonError as exc:
        return None, [str(exc)]
    current_generation = run_control.get("current_generation")
    if not isinstance(current_generation, str) or not current_generation:
        return None, ["run.control.json current_generation must be a non-empty string"]
    generation = generation_entry(run_control, current_generation)
    if not generation or not isinstance(generation.get("runtime"), str):
        return None, ["run.control.json current_generation must name a generation runtime"]
    try:
        runtime = load_json(run_dir / generation["runtime"])
    except ControlJsonError as exc:
        return None, [str(exc)]
    artifacts = {
        "requirements": requirements,
        "run": run_control,
        "runtime": runtime,
    }
    review_rel = generation.get("review")
    if isinstance(review_rel, str) and review_rel:
        try:
            artifacts["review"] = load_json(run_dir / review_rel)
        except ControlJsonError as exc:
            errors.append(str(exc))
    return artifacts, errors


def require_keys(name: str, value: dict[str, Any], keys: tuple[str, ...], errors: list[str]) -> None:
    missing = [key for key in keys if key not in value]
    if missing:
        errors.append(f"{name} missing required fields: {', '.join(missing)}")


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


def source_requirement_preservation_errors(source_requirement: dict[str, Any], label: str) -> list[str]:
    source = source_requirement.get("source")
    source_text = source_requirement_source_text(source)
    if not source_text:
        return []
    requirement_type = source_requirement.get("requirement_type")
    evidence_strength = source_requirement.get("required_evidence_strength")
    if source_text_is_measurement_curve_request(source_text) and source_requirement_is_weakened_to_framework(
        source_requirement, requirement_type, evidence_strength
    ):
        return [f"{label} source requirement appears weaker than source quote"]
    if source_text_is_api_v2_family_implementation(source_text) and source_requirement_is_weakened_to_readiness(
        source_requirement, requirement_type, evidence_strength
    ):
        return [f"{label} source requirement appears weaker than source quote"]
    return []


def source_requirement_source_text(source: Any) -> str:
    if not isinstance(source, dict):
        return ""
    parts = []
    for field in ("quote", "reference"):
        value = source.get(field)
        if isinstance(value, str):
            parts.append(value)
    return "\n".join(parts)


def source_requirement_requirement_text(source_requirement: dict[str, Any]) -> str:
    parts = []
    for field in ("required_action", "completion_checks", "target_objects"):
        value = source_requirement.get(field)
        if isinstance(value, str):
            parts.append(value)
        elif isinstance(value, list):
            parts.extend(item for item in value if isinstance(item, str))
    return "\n".join(parts).lower()


def source_text_is_measurement_curve_request(source_text: str) -> bool:
    english_measurement_curve = bool(MEASUREMENT_ACTION_RE.search(source_text)) and bool(
        MEASUREMENT_CURVE_LANGUAGE_RE.search(source_text)
    )
    chinese_measurement_curve = "测" in source_text and ("曲线" in source_text or "增长" in source_text)
    return english_measurement_curve or chinese_measurement_curve


def source_text_is_api_v2_family_implementation(source_text: str) -> bool:
    normalized = source_text.lower()
    asks_to_implement = bool(API_V2_IMPLEMENT_ACTION_RE.search(source_text)) or "实现" in source_text
    return asks_to_implement and "/api/v2" in normalized and bool(API_V2_FAMILY_RE.search(source_text))


def source_requirement_is_weakened_to_framework(
    source_requirement: dict[str, Any],
    requirement_type: Any,
    evidence_strength: Any,
) -> bool:
    requirement_text = source_requirement_requirement_text(source_requirement)
    return (
        requirement_type == "define_framework_or_plan"
        or evidence_strength == "framework_document"
        or bool(FRAMEWORK_WEAKENING_LANGUAGE_RE.search(requirement_text))
    )


def source_requirement_is_weakened_to_readiness(
    source_requirement: dict[str, Any],
    requirement_type: Any,
    evidence_strength: Any,
) -> bool:
    requirement_text = source_requirement_requirement_text(source_requirement)
    return (
        requirement_type == "define_framework_or_plan"
        or evidence_strength == "framework_document"
        or bool(READINESS_WEAKENING_LANGUAGE_RE.search(requirement_text))
    )


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


def source_requirements_completed_by_evidence(
    requirements: dict[str, Any],
    completed_evidence: set[str],
) -> set[str]:
    _, _, evidence_sources, validation_errors = validate_source_requirement_coverage(requirements)
    if validation_errors:
        return set()
    completed_sources: set[str] = set()
    for evidence_id in sorted(completed_evidence):
        evidence = evidence_sources.get(evidence_id)
        if isinstance(evidence, dict):
            completed_sources.update(string_list(evidence.get("satisfies_source_requirements")))
    return completed_sources


def validate_source_requirement_coverage(
    requirements: dict[str, Any],
) -> tuple[set[str], dict[str, set[str]], dict[str, dict[str, Any]], list[str]]:
    source_map, blocking_sources, errors = source_requirement_map(requirements)
    has_source_requirements = bool(source_map) or bool(errors)
    if not has_source_requirements and str(requirements.get("schema_version", "")) < "1.1.0":
        return blocking_sources, {}, {}, errors
    for source_id, source in sorted(source_map.items()):
        errors.extend(source_requirement_preservation_errors(source, f"source requirement {source_id}"))

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


def step_action_alignment_map(plan: dict[str, Any], errors: list[str]) -> dict[str, dict[str, Any]]:
    alignments = plan.get("step_action_alignment")
    if not isinstance(alignments, list):
        errors.append("plan.control.json must declare step_action_alignment")
        return {}
    mapped: dict[str, dict[str, Any]] = {}
    for alignment in alignments:
        if not isinstance(alignment, dict):
            errors.append("plan.control.json step_action_alignment entries must be objects")
            continue
        step_id = alignment.get("required_step_id")
        if not isinstance(step_id, str) or not step_id:
            errors.append("plan.control.json step_action_alignment entries must name required_step_id")
            continue
        if step_id in mapped:
            errors.append(f"plan.control.json duplicate step_action_alignment for {step_id}")
            continue
        mapped[step_id] = alignment
    return mapped


def alignment_write_paths(alignment: dict[str, Any]) -> list[str]:
    authority = alignment.get("allowed_authority_needed")
    if not isinstance(authority, dict):
        return []
    return string_list(authority.get("write_paths"))


def validate_event(event: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for field in (
        "event_type",
        "schema_version",
        "occurred_at",
        "runtime_generation",
    ):
        if field not in event:
            if field == "runtime_generation":
                errors.append("all progress events must include runtime_generation")
            else:
                errors.append(f"event missing required field: {field}")

    if event.get("event_type") not in EVENT_TYPES:
        errors.append("event_type is not recognized")
    event_type = event.get("event_type")
    if "runtime_generation" in event and (
        not isinstance(event.get("runtime_generation"), str) or not event.get("runtime_generation")
    ):
        errors.append("runtime_generation must be a non-empty string")

    if event_type in STEP_EVENT_TYPES:
        for field in ("work_package_id", "required_step", "status", "evidence"):
            if field not in event:
                errors.append(f"event missing required field: {field}")
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
    elif event_type in AMENDMENT_EVENT_TYPES:
        if not isinstance(event.get("amendment_id"), str) or not event.get("amendment_id"):
            errors.append("amendment events must include amendment_id")
        for field in AMENDMENT_ANCHOR_FIELDS:
            if field in event and not isinstance(event[field], bool):
                errors.append(f"{field} must be boolean when present")
        if event_type == "control.amendment.proposed":
            for field in AMENDMENT_PROPOSAL_REQUIRED_FIELDS:
                if field not in event:
                    errors.append(f"control.amendment.proposed events must include {field}")
            if "triggering_observation" in event and (
                not isinstance(event.get("triggering_observation"), str) or not event.get("triggering_observation")
            ):
                errors.append("control.amendment.proposed triggering_observation must be a non-empty string")
            if "reason" in event and (
                not isinstance(event.get("reason"), str) or not event.get("reason")
            ):
                errors.append("control.amendment.proposed reason must be a non-empty string")
            if "affected_stages" in event and (
                not isinstance(event.get("affected_stages"), list)
                or not event.get("affected_stages")
                or not all(isinstance(stage, str) and stage for stage in event.get("affected_stages", []))
            ):
                errors.append("control.amendment.proposed affected_stages must be a non-empty list")
            if "affected_source_requirements" in event and (
                not isinstance(event.get("affected_source_requirements"), list)
                or not event.get("affected_source_requirements")
                or not all(
                    isinstance(source_requirement, str) and source_requirement
                    for source_requirement in event.get("affected_source_requirements", [])
                )
            ):
                errors.append("control.amendment.proposed affected_source_requirements must be a non-empty list")
            for field in ("proposed_changes", "review_required"):
                if field in event and (
                    not isinstance(event.get(field), list)
                    or not event.get(field)
                    or not all(isinstance(item, str) and item for item in event.get(field, []))
                ):
                    errors.append(f"control.amendment.proposed {field} must be a non-empty list")
            if "patch_ref" in event and (not isinstance(event.get("patch_ref"), str) or not event.get("patch_ref")):
                errors.append("control.amendment.proposed patch_ref must be a non-empty string")
    elif event_type in GENERATION_EVENT_TYPES:
        if event_type == "runtime.generation.superseded" and (
            not isinstance(event.get("reason"), str) or not event.get("reason")
        ):
            errors.append("runtime.generation.superseded events must include reason")
    elif event_type in OBSERVATION_EVENT_TYPES:
        for field in OBSERVATION_STRING_FIELDS:
            if field in event and (not isinstance(event.get(field), str) or not event.get(field)):
                errors.append(f"{field} must be a non-empty string")
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


def validate_generation_control_chain(run_dir: Path) -> tuple[dict[str, dict[str, Any]] | None, list[str]]:
    artifacts, errors = load_generation_control_files(run_dir)
    if artifacts is None:
        return None, errors
    requirements = artifacts["requirements"]
    run_control = artifacts["run"]
    runtime = artifacts["runtime"]

    if requirements.get("artifact_type") != "requirements.control":
        errors.append("requirements.control.json artifact_type must be requirements.control")
    if requirements.get("status") != "approved":
        errors.append("requirements.control.json status must be approved")
    if run_control.get("artifact_type") != "run.control":
        errors.append("run.control.json artifact_type must be run.control")
    if run_control.get("status") != "active":
        errors.append("run.control.json status must be active")
    if runtime.get("artifact_type") != "runtime.control":
        errors.append("runtime.control.json artifact_type must be runtime.control")
    if runtime.get("status") != "compiled":
        errors.append("runtime.control.json status must be compiled")

    semantic_base = requirements.get("approved_control", {}).get("semantic_base")
    if not isinstance(semantic_base, dict) or semantic_base.get("hash") != semantic_base_hash(requirements):
        errors.append("requirements.control.json semantic_base hash must match approved_control")
    if run_control.get("semantic_base_ref") != semantic_base:
        errors.append("run.control.json semantic_base_ref must match requirements approved semantic_base")
    if runtime.get("semantic_base_ref") != semantic_base:
        errors.append("runtime.control.json semantic_base_ref must match requirements approved semantic_base")
    errors.extend(counterexample_contract_errors(requirements))

    current_generation = run_control.get("current_generation")
    active_ids = active_generation_ids(run_control)
    if not isinstance(current_generation, str) or not current_generation:
        errors.append("run.control.json current_generation must be a non-empty string")
        current_generation = ""
    if active_ids != [current_generation]:
        errors.append("run.control.json exactly current_generation must be active")
    max_auto_amendment_rounds = run_control.get("max_auto_amendment_rounds")
    if not isinstance(max_auto_amendment_rounds, int) or isinstance(max_auto_amendment_rounds, bool) or max_auto_amendment_rounds < 0:
        errors.append("run.control.json max_auto_amendment_rounds must be a non-negative integer")
        max_auto_amendment_rounds = 0
    if amendment_generation_count(run_control) > max_auto_amendment_rounds:
        errors.append("run.control.json auto amendment rounds exceed max_auto_amendment_rounds")
    generation = generation_entry(run_control, current_generation) if current_generation else None
    if not generation:
        errors.append("run.control.json current_generation is not declared in generations")
        generation = {}
    strategy_kind = generation.get("strategy_kind")
    if strategy_kind not in {"discovery", "execution", "amendment"}:
        errors.append("run.control.json current generation strategy_kind must be discovery, execution, or amendment")
    runtime_rel = generation.get("runtime")
    if not isinstance(runtime_rel, str) or not runtime_rel:
        errors.append("run.control.json current_generation must name runtime")
        runtime_rel = "runtime.control.json"
    runtime_generation = runtime.get("generation")
    if not isinstance(runtime_generation, dict) or runtime_generation.get("id") != current_generation:
        errors.append("runtime.control.json generation.id must match run.control.json current_generation")
    for field in RUN_STRATEGY_FIELDS:
        if runtime.get(field) != run_control.get(field):
            errors.append(f"runtime.control.json {field} must match run.control.json")
    strategy_policy = run_control.get("strategy_policy")
    if strategy_policy == "frozen_strategy" and (strategy_kind == "amendment" or generation.get("parent")):
        errors.append("run.control.json frozen_strategy cannot continue through amendment generations")
    if strategy_kind == "amendment" and not generation.get("parent"):
        errors.append("run.control.json amendment generations must declare parent")
    if generation.get("parent") and (not generation.get("review") or not generation.get("amendment_source")):
        errors.append("run.control.json amendment generations must declare review and amendment_source")
    if generation.get("parent") and strategy_kind != "amendment":
        errors.append("run.control.json generations with parent must use strategy_kind amendment")
    if strategy_kind in {"execution", "amendment"} and not generation.get("review"):
        errors.append(f"run.control.json {strategy_kind} generations must declare review")
    if generation.get("review"):
        review = artifacts.get("review")
        if not isinstance(review, dict) or review.get("artifact_type") != "review.control" or review.get("status") != "approved":
            errors.append("amendment generation review must be approved")
        elif strategy_kind in {"execution", "amendment"}:
            errors.extend(generation_review_errors(review, context=f"{strategy_kind} generation", requirements=requirements))

    readonly_files = generation_runtime_readonly_files(generation) if generation and runtime_rel else []
    runtime_files = runtime.get("runtime", {})
    if runtime_files.get("readonly_files") != readonly_files:
        errors.append("runtime.control.json readonly_files must match current generation files")
    if runtime_files.get("writable_files") != list(WRITABLE_FILES):
        errors.append("runtime.control.json writable_files must be progress.jsonl, runtime-status.json, final-report.json")
    writable_evidence_paths = string_list(runtime_files.get("writable_evidence_paths"))
    if not writable_evidence_paths:
        errors.append("runtime.control.json writable_evidence_paths must authorize non-control evidence artifacts")
    for path in required_evidence_paths(requirements):
        if not path_is_under(path, writable_evidence_paths):
            errors.append(
                "requirements.control.json required evidence path is not authorized by runtime writable_evidence_paths: "
                + path
            )

    expected = {
        "requirements.control.json": control_file_hash("requirements.control.json", requirements),
        "run.control.json": control_file_hash("run.control.json", run_control),
        runtime_rel: control_file_hash(runtime_rel, runtime),
    }
    if generation.get("review") and isinstance(artifacts.get("review"), dict):
        expected[generation["review"]] = control_file_hash(generation["review"], artifacts["review"])
    errors.extend(check_hashes("runtime.control.json", runtime.get("approved_control_hashes"), expected))

    all_required_outcomes, required_outcomes, outcome_errors = required_outcome_sets(requirements)
    errors.extend(outcome_errors)
    _, _, _, source_errors = validate_source_requirement_coverage(requirements)
    errors.extend(source_errors)
    runtime_step_outcomes = step_outcome_map(
        runtime,
        known_outcomes=all_required_outcomes if all_required_outcomes else None,
        errors=errors,
        label="runtime.control.json",
    )
    runtime_steps = step_ids(runtime)
    if not runtime_steps:
        errors.append("runtime.control.json must declare required_steps")
    synthetic_steps = {
        step.get("step_id")
        for step in runtime.get("required_steps", [])
        if isinstance(step, dict)
        and step.get("synthetic") is True
        and isinstance(step.get("step_id"), str)
    }
    if strategy_kind != "discovery" and synthetic_steps:
        errors.append("runtime.control.json synthetic required_steps are only allowed in discovery generations")
    if required_outcomes:
        missing_runtime = sorted(required_outcomes - covered_outcomes_by_steps(runtime_step_outcomes))
        if missing_runtime:
            errors.append(
                "runtime.control.json required_steps do not satisfy blocking required outcomes: "
                + ", ".join(missing_runtime)
            )
        raw_verifier_outcomes = runtime.get("verifier", {}).get("required_outcomes")
        verifier_outcomes = set(string_list(raw_verifier_outcomes))
        missing_verifier = sorted(required_outcomes - verifier_outcomes)
        if missing_verifier:
            errors.append(
                "runtime.control.json verifier.required_outcomes missing blocking required outcomes: "
                + ", ".join(missing_verifier)
            )
    if runtime.get("verifier", {}).get("required_before_goal_achieved") is not True:
        errors.append("runtime.control.json verifier must be required before goal_achieved")
    if not runtime.get("verifier", {}).get("command"):
        errors.append("runtime.control.json verifier.command is required")

    return artifacts, errors


def validate_control_chain(run_dir: Path) -> tuple[dict[str, dict[str, Any]] | None, list[str]]:
    if not (run_dir / "run.control.json").exists():
        return None, ["missing run.control.json; official JSON control runs must use run.control.json"]
    return validate_generation_control_chain(run_dir)


def verify_approved_hashes(run_dir: Path, hash_file: Path, readonly_files: tuple[str, ...] | None = None) -> list[str]:
    try:
        expected = load_json(hash_file)
    except ControlJsonError as exc:
        return [str(exc)]
    readonly_files = readonly_files or READONLY_FILES
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
