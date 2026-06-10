from __future__ import annotations

import copy
import hashlib
import json
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
AMENDMENT_ANCHOR_FIELDS = ("semantic_base_change", "required_outcomes_changed", "authority_expanded")
AMENDMENT_PROPOSAL_REQUIRED_FIELDS = (
    "reason",
    "triggering_observation",
    "affected_stages",
    *AMENDMENT_ANCHOR_FIELDS,
    "proposed_changes",
    "review_required",
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
            for field in ("proposed_changes", "review_required"):
                if field in event and (
                    not isinstance(event.get(field), list)
                    or not event.get(field)
                    or not all(isinstance(item, str) and item for item in event.get(field, []))
                ):
                    errors.append(f"control.amendment.proposed {field} must be a non-empty list")
    elif event_type in GENERATION_EVENT_TYPES:
        if event_type == "runtime.generation.superseded" and (
            not isinstance(event.get("reason"), str) or not event.get("reason")
        ):
            errors.append("runtime.generation.superseded events must include reason")
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
    if runtime.get("control_mode") != run_control.get("control_mode"):
        errors.append("runtime.control.json control_mode must match run.control.json")
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
    errors: list[str] = []
    if (run_dir / "run.control.json").exists():
        return validate_generation_control_chain(run_dir)
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
    writable_evidence_paths = string_list(artifacts["runtime"].get("runtime", {}).get("writable_evidence_paths"))
    if not writable_evidence_paths:
        errors.append("runtime.control.json writable_evidence_paths must authorize non-control evidence artifacts")
    plan_runtime = artifacts["plan"].get("runtime", {})
    if plan_runtime.get("readonly_files") != list(READONLY_FILES):
        errors.append("plan.control.json readonly_files must match runtime.control.json")
    if plan_runtime.get("writable_files") != list(WRITABLE_FILES):
        errors.append("plan.control.json writable_files must match runtime.control.json")
    if string_list(plan_runtime.get("writable_evidence_paths")) != writable_evidence_paths:
        errors.append("plan.control.json writable_evidence_paths must match runtime.control.json")
    for path in required_evidence_paths(artifacts["requirements"]):
        if not path_is_under(path, writable_evidence_paths):
            errors.append(
                "requirements.control.json required evidence path is not authorized by runtime writable_evidence_paths: "
                + path
            )

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
        workflow_registry = load_json(DELEGATION_WORKFLOW_REGISTRY)
    except ControlJsonError as exc:
        errors.append(str(exc))
        workflow_registry = {}

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
    plan_alignment = step_action_alignment_map(artifacts["plan"], errors)
    missing_runtime_alignment = sorted(runtime_steps - set(plan_alignment))
    if missing_runtime_alignment:
        errors.append(
            "plan.control.json step_action_alignment missing runtime required steps: "
            + ", ".join(missing_runtime_alignment)
        )

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
        mainline_producing_steps: set[str] = set()
        for package in work_packages:
            if not isinstance(package, dict):
                errors.append("plan.control.json work_packages entries must be objects")
                continue
            if not string_list(package.get("required_tests")):
                errors.append("work package missing required checks")
            package_steps = set(string_list(package.get("required_steps")))
            covered_steps.update(package_steps)
            used_alignment = set(string_list(package.get("uses_step_action_alignment")))
            if not package_steps <= used_alignment:
                errors.append("plan.control.json work package missing producing action alignment for required steps")
            unknown_alignment = sorted(used_alignment - set(plan_alignment))
            if unknown_alignment:
                errors.append(
                    "plan.control.json work package references unknown producing action alignment: "
                    + ", ".join(unknown_alignment)
                )
            for step_id in used_alignment:
                alignment = plan_alignment.get(step_id)
                if not alignment:
                    continue
                for write_path in alignment_write_paths(alignment):
                    if not path_is_under(write_path, string_list(package.get("allowed_write_paths"))):
                        errors.append(
                            "plan.control.json producing action write authority is not covered by work package allowed_write_paths"
                        )
            package_outcomes = covered_outcomes_by_steps(step_outcomes_by_key.get("plan", {}), package_steps)
            if package_outcomes & required_outcomes:
                if (
                    package.get("role") != "mainline"
                    or package.get("counts_as_goal_progress") is not True
                    or package.get("not_merely_verification") is not True
                ):
                    errors.append(
                        "plan.control.json mainline work package required for blocking outcomes must use a producing action"
                    )
                else:
                    mainline_producing_steps.update(package_steps)
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
            producing_outcomes = covered_outcomes_by_steps(
                step_outcomes_by_key.get("plan", {}),
                mainline_producing_steps,
            )
            missing_producing_outcomes = sorted(required_outcomes - producing_outcomes)
            if missing_producing_outcomes:
                errors.append(
                    "plan.control.json mainline producing work packages do not cover blocking required outcomes: "
                    + ", ".join(missing_producing_outcomes)
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
