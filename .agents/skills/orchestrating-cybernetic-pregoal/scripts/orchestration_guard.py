#!/usr/bin/env python3
"""JSON-only pre-goal orchestration guard.

Official orchestration input is a run directory containing control JSON files.
Markdown control artifacts are not accepted as a guard/compiler/runtime source.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[4]
CONTROL_CHAIN_GUARD = REPO_ROOT / ".agents/skills/compiling-cybernetic-runtime-goals/scripts/control_chain_guard.py"

NEXT_ACTION = {
    "before-design": "RunDesign",
    "before-goal": "RunGoalWriting",
    "before-policy": "RunExecutionPolicy",
    "before-review": "RunReview",
    "before-runtime-compile": "RunRuntimeCompile",
}
RETURN_STAGE_ACTION = {
    "requirements": "ReturnToRequirementsAnalysis",
    "design": "RunDesign",
    "goal": "RunGoalWriting",
    "plan": "RunExecutionPolicy",
    "review": "RunReview",
}
RETURN_STAGE_ORDER = {
    "requirements": 0,
    "design": 1,
    "goal": 2,
    "plan": 3,
    "review": 4,
}
INFORMATION_SUFFICIENCY_STATES = {"before-design", "before-policy"}
INFORMATION_SUFFICIENCY_GATE_POINTS = {
    "source_requirements->information_sufficiency_facts",
    "required_outcomes->information_sufficiency_facts",
    "information_sufficiency_facts->design_plan_entry",
}


def payload(ok: bool, state: str, next_action: str, errors: list[str]) -> dict[str, object]:
    return {
        "ok": ok,
        "state": state,
        "next_allowed_action": next_action,
        "errors": errors,
        "warnings": [],
    }


def print_result(data: dict[str, object], as_json: bool) -> None:
    if as_json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return
    print("PASS" if data["ok"] else "FAIL")
    print(f"NEXT: {data['next_allowed_action']}")
    for error in data["errors"]:  # type: ignore[index]
        print(f"ERROR: {error}")


def legacy_args_present(args: argparse.Namespace) -> bool:
    return any(
        (
            args.requirements,
            args.clarification,
            args.design,
            args.goal,
            args.plan,
            args.review,
        )
    )


def read_json_object(path: Path) -> dict[str, object] | None:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return None
    return value if isinstance(value, dict) else None


def string_list(value: object) -> list[str]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, str)]


def schema_version_at_least(requirements: dict[str, object], minimum: str) -> bool:
    def parse(value: str) -> tuple[int, ...]:
        try:
            return tuple(int(part) for part in value.split("."))
        except ValueError:
            return (0,)

    return parse(str(requirements.get("schema_version", ""))) >= parse(minimum)


def evidence_ref_errors(run_dir: Path, label: str, evidence_ref: object) -> list[str]:
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


def information_sufficiency_errors(run_dir: Path) -> list[str]:
    requirements = read_json_object(run_dir / "requirements.control.json")
    if not requirements:
        return []
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
            "is required before design/plan"
        ]
    errors: list[str] = []
    if check.get("status") not in {"satisfied", "not_required"}:
        errors.append(
            f"information_sufficiency_check status must be satisfied before design/plan, got {check.get('status')!r}"
        )
    sources = {
        item.get("id")
        for item in approved.get("source_requirements", [])
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }
    outcomes = {
        item.get("id")
        for item in approved.get("required_outcomes", [])
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }
    facts = check.get("facts")
    if not isinstance(facts, list) or not facts:
        errors.append("information_sufficiency_check facts must be a non-empty list")
        facts = []
    blocking_fact_ids: set[str] = set()
    for index, fact in enumerate(facts):
        if not isinstance(fact, dict):
            errors.append(f"information_sufficiency_check facts[{index}] must be an object")
            continue
        fact_id = fact.get("fact_id")
        label = f"information_sufficiency_check fact {fact_id or index}"
        derived_from = fact.get("derived_from")
        if not isinstance(derived_from, dict):
            errors.append(f"{label} derived_from must be an object")
            continue
        fact_sources = set(string_list(derived_from.get("source_requirements")))
        fact_outcomes = set(string_list(derived_from.get("required_outcomes")))
        if not fact_sources and not fact_outcomes:
            errors.append(f"{label} derived_from must reference source_requirements or required_outcomes")
        unknown_sources = sorted(fact_sources - sources)
        if unknown_sources:
            errors.append(f"{label} references unknown source_requirements: {', '.join(unknown_sources)}")
        unknown_outcomes = sorted(fact_outcomes - outcomes)
        if unknown_outcomes:
            errors.append(f"{label} references unknown required_outcomes: {', '.join(unknown_outcomes)}")
        if fact.get("blocks_design_or_plan_if_missing") is True:
            if isinstance(fact_id, str):
                blocking_fact_ids.add(fact_id)
            if fact.get("current_status") != "satisfied":
                errors.append(f"{label} is not satisfied and blocks design/plan")
        if not isinstance(fact.get("why_needed"), str) or not fact["why_needed"].strip():
            errors.append(f"{label} why_needed must be non-empty")
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
    elif (
        not isinstance(reviewer.get("kind"), str)
        or not reviewer["kind"].strip()
        or not isinstance(reviewer.get("id"), str)
        or not reviewer["id"].strip()
        or not isinstance(reviewer.get("evidence_ref"), str)
        or not reviewer["evidence_ref"].strip()
    ):
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
    missing_facts = sorted(blocking_fact_ids - checked_facts)
    if missing_facts:
        errors.append(
            "information_sufficiency_check counterexample_review missing checked_facts: "
            + ", ".join(missing_facts)
        )
    checked_transformations = set(string_list(review.get("checked_transformations")))
    missing_points = sorted(INFORMATION_SUFFICIENCY_GATE_POINTS - checked_transformations)
    if missing_points:
        errors.append(
            "information_sufficiency_check counterexample_review missing checked_transformations: "
            + ", ".join(missing_points)
        )
    return errors


def current_generation_review_path(run_dir: Path) -> Path | None:
    run_control = read_json_object(run_dir / "run.control.json")
    if not run_control:
        legacy_review = run_dir / "review.control.json"
        return legacy_review if legacy_review.exists() else None

    current_generation = run_control.get("current_generation")
    generations = run_control.get("generations")
    if not isinstance(current_generation, str) or not isinstance(generations, list):
        return None
    for generation in generations:
        if not isinstance(generation, dict) or generation.get("id") != current_generation:
            continue
        review_rel = generation.get("review")
        if isinstance(review_rel, str) and review_rel:
            return run_dir / review_rel
        return None
    return None


def review_revision_route(run_dir: Path) -> tuple[str, list[str]] | None:
    review_path = current_generation_review_path(run_dir)
    if review_path is None:
        return None
    review = read_json_object(review_path)
    if not review:
        return None

    checks = review.get("review_checks")
    if not isinstance(checks, list):
        return None

    revision_checks: list[dict[str, object]] = []
    blocked_checks: list[dict[str, object]] = []
    for check in checks:
        if not isinstance(check, dict):
            continue
        verdict = check.get("verdict")
        status = check.get("status")
        if verdict == "blocked":
            blocked_checks.append(check)
        elif verdict == "needs_revision" or status == "needs_revision":
            revision_checks.append(check)

    if blocked_checks:
        errors = []
        for check in blocked_checks:
            check_id = check.get("check_id", "unknown-check")
            errors.append(f"{check_id}: blocked")
            for finding in check.get("findings", []) if isinstance(check.get("findings"), list) else []:
                if isinstance(finding, str):
                    errors.append(f"{check_id}: {finding}")
        return "Blocked", errors or ["review is blocked"]

    if not revision_checks:
        return None

    def stage_rank(check: dict[str, object]) -> int:
        stage = check.get("return_to_stage")
        return RETURN_STAGE_ORDER.get(stage, RETURN_STAGE_ORDER["review"]) if isinstance(stage, str) else RETURN_STAGE_ORDER["review"]

    selected = min(revision_checks, key=stage_rank)
    stage = selected.get("return_to_stage")
    next_action = RETURN_STAGE_ACTION.get(stage, "RunReview") if isinstance(stage, str) else "RunReview"
    check_id = selected.get("check_id", "unknown-check")
    errors = [f"{check_id}: needs_revision -> {next_action}"]
    for key in ("findings", "required_changes"):
        values = selected.get(key)
        if isinstance(values, list):
            for value in values:
                if isinstance(value, str):
                    errors.append(f"{check_id}: {value}")
    return next_action, errors


def review_structure_route(errors: list[str]) -> tuple[str, list[str]] | None:
    combined = "\n".join(errors)
    if "counterexample-gate" in combined or "required review check" in combined:
        return "RunReview", ["review gate is incomplete -> RunReview"]
    return None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--state", required=True, choices=sorted(NEXT_ACTION))
    parser.add_argument("--run-dir", help="Official JSON control run directory containing *.control.json files.")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--requirements", help=argparse.SUPPRESS)
    parser.add_argument("--clarification", help=argparse.SUPPRESS)
    parser.add_argument("--design", help=argparse.SUPPRESS)
    parser.add_argument("--goal", help=argparse.SUPPRESS)
    parser.add_argument("--plan", help=argparse.SUPPRESS)
    parser.add_argument("--review", help=argparse.SUPPRESS)
    args = parser.parse_args()

    if not args.run_dir:
        data = payload(
            False,
            args.state,
            "FixJsonControlRun",
            ["official control input is JSON-only; use --run-dir with docs/cybernetics/runs/<slug>/"],
        )
        print_result(data, args.json)
        return 2
    if legacy_args_present(args):
        data = payload(
            False,
            args.state,
            "FixJsonControlRun",
            ["--run-dir is the official JSON control input; do not combine it with Markdown artifact inputs"],
        )
        print_result(data, args.json)
        return 2

    if args.state in INFORMATION_SUFFICIENCY_STATES:
        sufficiency_errors = information_sufficiency_errors(Path(args.run_dir))
        if sufficiency_errors:
            data = payload(False, args.state, "RunInformationSufficiencyCheck", sufficiency_errors)
            print_result(data, args.json)
            return 2

    guard = subprocess.run(
        [sys.executable, str(CONTROL_CHAIN_GUARD), "--run-dir", args.run_dir],
        text=True,
        capture_output=True,
    )
    if guard.returncode != 0:
        errors = [line for line in (guard.stdout + guard.stderr).splitlines() if line.strip()]
        route = review_revision_route(Path(args.run_dir))
        if route:
            next_action, route_errors = route
            errors = route_errors + errors
        else:
            structure_route = review_structure_route(errors)
            if structure_route:
                next_action, route_errors = structure_route
                errors = route_errors + errors
            else:
                next_action = "FixJsonControlRun"
        data = payload(False, args.state, next_action, errors)
        print_result(data, args.json)
        return 2

    data = payload(True, args.state, NEXT_ACTION[args.state], [])
    print_result(data, args.json)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
