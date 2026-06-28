#!/usr/bin/env python3
"""Predict queue-friendly handoff text from JSON requirements control."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


def blocked(message: str) -> int:
    print("Pre-goal handoff prediction blocked.")
    print()
    print(f"Reason: {message}")
    print()
    print("Next: create or repair the JSON control run directory.")
    return 2


def read_json_object(path: Path) -> dict[str, Any] | None:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        blocked(f"missing file: {path}")
        return None
    except json.JSONDecodeError as exc:
        blocked(f"invalid requirements control JSON: {path}: {exc}")
        return None
    if not isinstance(value, dict):
        blocked(f"requirements control JSON must contain an object: {path}")
        return None
    return value


def read_optional_json_object(path: Path) -> dict[str, Any] | None:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return None
    return value if isinstance(value, dict) else None


def schema_version_at_least(requirements: dict[str, Any], minimum: str) -> bool:
    version = requirements.get("schema_version")
    if not isinstance(version, str):
        return False
    try:
        current_parts = tuple(int(part) for part in version.split("."))
        minimum_parts = tuple(int(part) for part in minimum.split("."))
    except ValueError:
        return False
    return current_parts >= minimum_parts


def string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, str) and item]


def evidence_ref_errors(run_dir: Path, label: str, evidence_ref: Any) -> list[str]:
    if not isinstance(evidence_ref, str) or not evidence_ref.strip():
        return [f"{label} evidence_ref must be non-empty"]
    path_part = evidence_ref.split("#", 1)[0]
    if not path_part:
        return [f"{label} evidence_ref must name a file before any JSON pointer fragment"]
    ref_path = Path(path_part)
    if ref_path.is_absolute():
        return [f"{label} evidence_ref must be relative to the run directory"]
    resolved_run_dir = run_dir.resolve()
    resolved_ref = (run_dir / ref_path).resolve()
    try:
        resolved_ref.relative_to(resolved_run_dir)
    except ValueError:
        return [f"{label} evidence_ref must stay inside the run directory"]
    if not resolved_ref.exists():
        return [f"{label} evidence_ref does not exist: {evidence_ref}"]
    if not resolved_ref.is_file():
        return [f"{label} evidence_ref must point to a file: {evidence_ref}"]
    return []


INFORMATION_SUFFICIENCY_GATE_POINTS = {
    "source_requirements->information_sufficiency_facts",
    "required_outcomes->information_sufficiency_facts",
    "information_sufficiency_facts->design_plan_entry",
}


def information_sufficiency_errors(requirements: dict[str, Any], run_dir: Path) -> list[str]:
    approved = requirements.get("approved_control")
    if not isinstance(approved, dict):
        return ["requirements.control.json approved_control must be an object"]
    check = approved.get("information_sufficiency_check")
    if not schema_version_at_least(requirements, "1.2.0"):
        if isinstance(check, dict):
            return [
                "requirements.control.json approved_control.information_sufficiency_check "
                "requires schema_version >= 1.2.0"
            ]
        return []
    if not isinstance(check, dict):
        return [
            "requirements.control.json approved_control.information_sufficiency_check "
            "is required for schema_version >= 1.2.0"
        ]

    errors: list[str] = []
    if check.get("status") not in {"satisfied", "not_required"}:
        errors.append(
            f"information_sufficiency_check status must be satisfied before handoff, got {check.get('status')!r}"
        )

    approved_sources = {
        item.get("id")
        for item in approved.get("source_requirements", [])
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }
    approved_outcomes = {
        item.get("id")
        for item in approved.get("required_outcomes", [])
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }
    facts = check.get("facts")
    if not isinstance(facts, list) or not facts:
        errors.append("information_sufficiency_check facts must be a non-empty list")
        facts = []

    blocking_fact_ids: set[str] = set()
    all_fact_ids: set[str] = set()
    for index, fact in enumerate(facts):
        if not isinstance(fact, dict):
            errors.append(f"information_sufficiency_check facts[{index}] must be an object")
            continue
        fact_id = fact.get("fact_id")
        label = f"information_sufficiency_check fact {fact_id or index}"
        if not isinstance(fact_id, str) or not fact_id:
            errors.append(f"{label} must have fact_id")
            continue
        all_fact_ids.add(fact_id)
        derived_from = fact.get("derived_from")
        if not isinstance(derived_from, dict):
            errors.append(f"{label} derived_from must be an object")
            continue
        fact_sources = set(string_list(derived_from.get("source_requirements")))
        fact_outcomes = set(string_list(derived_from.get("required_outcomes")))
        if not fact_sources and not fact_outcomes:
            errors.append(f"{label} derived_from must reference source_requirements or required_outcomes")
        unknown_sources = sorted(fact_sources - approved_sources)
        if unknown_sources:
            errors.append(f"{label} references unknown source_requirements: {', '.join(unknown_sources)}")
        unknown_outcomes = sorted(fact_outcomes - approved_outcomes)
        if unknown_outcomes:
            errors.append(f"{label} references unknown required_outcomes: {', '.join(unknown_outcomes)}")
        if fact.get("blocks_design_or_plan_if_missing") is True:
            blocking_fact_ids.add(fact_id)
            if fact.get("current_status") != "satisfied":
                errors.append(f"{label} is not satisfied and blocks handoff")
        if not isinstance(fact.get("why_needed"), str) or not fact["why_needed"].strip():
            errors.append(f"{label} why_needed must explain why design/plan needs this fact")
        errors.extend(evidence_ref_errors(run_dir, label, fact.get("evidence_ref")))

    review = check.get("counterexample_review")
    if not isinstance(review, dict):
        errors.append("information_sufficiency_check counterexample_review must be an object")
        return errors
    if review.get("status") != "pass" or review.get("verdict") != "approved":
        errors.append("information_sufficiency_check counterexample_review must pass with verdict approved")
    reviewer = review.get("reviewer")
    if not isinstance(reviewer, dict):
        errors.append("information_sufficiency_check counterexample_review reviewer must be an object")
    elif not isinstance(reviewer.get("id"), str) or not reviewer["id"].strip():
        errors.append("information_sufficiency_check counterexample_review reviewer must have kind, id, and evidence_ref")
    elif not isinstance(reviewer.get("evidence_ref"), str) or not reviewer["evidence_ref"].strip():
        errors.append("information_sufficiency_check counterexample_review reviewer must have kind, id, and evidence_ref")
    else:
        errors.extend(
            evidence_ref_errors(
                run_dir,
                "information_sufficiency_check counterexample_review reviewer",
                reviewer.get("evidence_ref"),
            )
        )
    checked_facts = set(string_list(review.get("checked_facts")))
    missing_checked_facts = sorted(blocking_fact_ids - checked_facts)
    if missing_checked_facts:
        errors.append(
            "information_sufficiency_check counterexample_review missing checked_facts: "
            + ", ".join(missing_checked_facts)
        )
    checked_transformations = set(string_list(review.get("checked_transformations")))
    missing_points = sorted(INFORMATION_SUFFICIENCY_GATE_POINTS - checked_transformations)
    if missing_points:
        errors.append(
            "information_sufficiency_check counterexample_review missing checked_transformations: "
            + ", ".join(missing_points)
        )
    unknown_checked_facts = sorted(checked_facts - all_fact_ids)
    if unknown_checked_facts:
        errors.append(
            "information_sufficiency_check counterexample_review references unknown facts: "
            + ", ".join(unknown_checked_facts)
        )
    return errors


def current_generation_runtime(run_dir: Path) -> Path:
    run_control = read_optional_json_object(run_dir / "run.control.json")
    if run_control is None:
        return run_dir / "gen-000/runtime.control.json"
    current_generation = run_control.get("current_generation")
    generations = run_control.get("generations")
    if not isinstance(current_generation, str) or not isinstance(generations, list):
        return run_dir / "gen-000/runtime.control.json"
    for generation in generations:
        if not isinstance(generation, dict) or generation.get("id") != current_generation:
            continue
        runtime = generation.get("runtime")
        if isinstance(runtime, str) and runtime:
            return run_dir / runtime
    return run_dir / "gen-000/runtime.control.json"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--requirements", help="Path to requirements.control.json.")
    parser.add_argument("--run-dir", help="Path to docs/cybernetics/runs/<slug> containing requirements.control.json.")
    args = parser.parse_args()

    if bool(args.requirements) == bool(args.run_dir):
        return blocked("pass exactly one JSON input: --run-dir or --requirements")

    requirements_path = Path(args.run_dir) / "requirements.control.json" if args.run_dir else Path(args.requirements)
    if requirements_path.name != "requirements.control.json":
        return blocked(
            "official pre-goal prediction input is JSON-only; pass docs/cybernetics/runs/<slug>/requirements.control.json"
        )

    requirements = read_json_object(requirements_path)
    if requirements is None:
        return 2
    if requirements.get("artifact_type") != "requirements.control":
        return blocked(f"requirements control JSON has wrong artifact_type: {requirements.get('artifact_type')!r}")
    if requirements.get("status") != "approved":
        return blocked(f"requirements control JSON status is not approved: {requirements.get('status')!r}")
    run_dir = requirements_path.parent
    information_errors = information_sufficiency_errors(requirements, run_dir)
    if information_errors:
        return blocked("; ".join(information_errors))
    runtime_control = current_generation_runtime(run_dir)
    print("Response-only queue suggestions:")
    print()
    print("```text")
    print(f"$orchestrating-cybernetic-pregoal 根据 JSON run directory {run_dir} 完成 pre-goal 编译，允许使用 subagents review。")
    print("```")
    print()
    print("Predicted downstream JSON control files:")
    print()
    print("```text")
    for filename in (
        "requirements.control.json",
        "run.control.json",
        str(runtime_control.relative_to(run_dir)),
    ):
        print(f"{filename}: {run_dir / filename}")
    print("```")
    print()
    print("Predicted runtime control JSON path:")
    print()
    print("```text")
    print(runtime_control)
    print("```")
    print()
    print("Predicted pointer-only runtime command shape:")
    print()
    print("```text")
    print(
        f"/goal Execute the runtime control JSON at {runtime_control} "
        "using .agents/skills/using-control-json. Read it first; validate the JSON control chain; "
        "treat approved control JSON as read-only; append progress only to progress.jsonl; "
        "do not claim goal_achieved true unless the verifier permits it."
    )
    print("```")
    print()
    print("Predicted only: compile_runtime_goal.py --run-dir must generate or validate the current generation runtime from run.control.json.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
