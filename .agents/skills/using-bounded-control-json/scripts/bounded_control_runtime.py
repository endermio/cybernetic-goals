from __future__ import annotations

import json
from pathlib import Path
from typing import Any


READONLY_FILES = ("goal.control.json", "runtime.control.json")
WRITABLE_FILES = ("progress.jsonl", "runtime-status.json", "final-report.json")


class BoundedControlError(Exception):
    pass


def result_payload(ok: bool, errors: list[str], **extra: Any) -> dict[str, Any]:
    payload: dict[str, Any] = {"ok": ok, "errors": errors}
    payload.update(extra)
    return payload


def normalize_run_dir(path: Path) -> Path:
    return path.parent if path.name == "runtime.control.json" else path


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise BoundedControlError(f"missing JSON file: {path.name}") from exc
    except json.JSONDecodeError as exc:
        raise BoundedControlError(f"invalid JSON in {path.name}: {exc}") from exc
    if not isinstance(value, dict):
        raise BoundedControlError(f"{path.name} must contain a JSON object")
    return value


def load_bounded_artifacts(run_dir: Path) -> tuple[dict[str, Any] | None, dict[str, Any] | None, list[str]]:
    errors: list[str] = []
    try:
        goal = load_json(run_dir / "goal.control.json")
    except BoundedControlError as exc:
        goal = None
        errors.append(str(exc))
    try:
        runtime = load_json(run_dir / "runtime.control.json")
    except BoundedControlError as exc:
        runtime = None
        errors.append(str(exc))
    return goal, runtime, errors


def string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, str) and item]


def required_step_map(runtime: dict[str, Any]) -> dict[str, set[str]]:
    steps = runtime.get("required_steps")
    if not isinstance(steps, list):
        return {}
    step_map: dict[str, set[str]] = {}
    for step in steps:
        if not isinstance(step, dict) or not isinstance(step.get("step_id"), str):
            continue
        step_map[step["step_id"]] = set(string_list(step.get("evidence_required")))
    return step_map


def validate_bounded_runtime(run_dir: Path) -> tuple[dict[str, Any] | None, dict[str, Any] | None, list[str]]:
    goal, runtime, errors = load_bounded_artifacts(run_dir)
    if goal is None or runtime is None:
        return goal, runtime, errors

    if runtime.get("artifact_type") != "bounded-runtime.control":
        errors.append("runtime.control.json artifact_type must be bounded-runtime.control")
    if runtime.get("control_kind") != "bounded_runtime":
        errors.append("runtime.control.json control_kind must be bounded_runtime")
    if runtime.get("status") != "compiled":
        errors.append("runtime.control.json status must be compiled")
    if runtime.get("goal") != "goal.control.json":
        errors.append("runtime.control.json goal must reference goal.control.json")

    runtime_io = runtime.get("runtime")
    if not isinstance(runtime_io, dict):
        errors.append("runtime.control.json runtime must be an object")
    else:
        if runtime_io.get("readonly_files") != list(READONLY_FILES):
            errors.append("runtime.control.json readonly_files must be goal.control.json and runtime.control.json")
        if runtime_io.get("writable_files") != list(WRITABLE_FILES):
            errors.append("runtime.control.json writable_files must be progress.jsonl, runtime-status.json, final-report.json")

    for field in ("approved_source", "objective", "scope", "what_counts_as_done", "progress", "verifier", "final_report"):
        if field not in runtime:
            errors.append(f"runtime.control.json missing required field: {field}")

    progress = runtime.get("progress")
    if not isinstance(progress, dict) or progress.get("path") != "progress.jsonl" or progress.get("append_only") is not True:
        errors.append("runtime.control.json progress must set path progress.jsonl and append_only true")

    verifier = runtime.get("verifier")
    if not isinstance(verifier, dict):
        errors.append("runtime.control.json verifier must be an object")
    else:
        if verifier.get("required_before_goal_achieved") is not True:
            errors.append("runtime.control.json verifier.required_before_goal_achieved must be true")
        if not isinstance(verifier.get("command"), str) or not verifier.get("command"):
            errors.append("runtime.control.json verifier.command must be a non-empty string")

    steps = runtime.get("required_steps")
    if not isinstance(steps, list) or not steps:
        errors.append("runtime.control.json required_steps must be a non-empty list")
    else:
        seen_steps: set[str] = set()
        for index, step in enumerate(steps):
            if not isinstance(step, dict):
                errors.append(f"runtime.control.json required_steps[{index}] must be an object")
                continue
            step_id = step.get("step_id")
            if not isinstance(step_id, str) or not step_id:
                errors.append(f"runtime.control.json required_steps[{index}].step_id must be a non-empty string")
                continue
            if step_id in seen_steps:
                errors.append(f"runtime.control.json duplicate required step: {step_id}")
            seen_steps.add(step_id)
            if not isinstance(step.get("description"), str) or not step.get("description"):
                errors.append(f"runtime.control.json required_steps[{index}].description must be a non-empty string")
            if not string_list(step.get("evidence_required")):
                errors.append(f"runtime.control.json required_steps[{index}].evidence_required must be a non-empty string list")
            if not isinstance(step.get("done_when"), str) or not step.get("done_when"):
                errors.append(f"runtime.control.json required_steps[{index}].done_when must be a non-empty string")

    if not string_list(runtime.get("stop_conditions")):
        errors.append("runtime.control.json stop_conditions must be a non-empty string list")

    return goal, runtime, errors


def read_progress_events(run_dir: Path) -> tuple[list[dict[str, Any]], list[str]]:
    path = run_dir / "progress.jsonl"
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except FileNotFoundError:
        return [], ["missing JSONL file: progress.jsonl"]

    events: list[dict[str, Any]] = []
    errors: list[str] = []
    for index, line in enumerate(lines, start=1):
        if not line.strip():
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError as exc:
            errors.append(f"progress.jsonl line {index} invalid JSON: {exc}")
            continue
        if not isinstance(event, dict):
            errors.append(f"progress.jsonl line {index} must be a JSON object")
            continue
        events.append(event)
    return events, errors


def completed_step_evidence(events: list[dict[str, Any]]) -> dict[str, set[str]]:
    evidence_by_step: dict[str, set[str]] = {}
    for event in events:
        role = event.get("progress_role", "mainline")
        counts = event.get("counts_as_goal_progress", role == "mainline")
        evidence = string_list(event.get("evidence"))
        required_step = event.get("required_step")
        if (
            event.get("event_type") == "step.completed"
            and event.get("status") == "pass"
            and isinstance(required_step, str)
            and role == "mainline"
            and counts is True
            and evidence
        ):
            evidence_by_step.setdefault(required_step, set()).update(evidence)
    return evidence_by_step
