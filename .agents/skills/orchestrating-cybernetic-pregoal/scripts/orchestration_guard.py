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
            next_action = "FixJsonControlRun"
        data = payload(False, args.state, next_action, errors)
        print_result(data, args.json)
        return 2

    data = payload(True, args.state, NEXT_ACTION[args.state], [])
    print_result(data, args.json)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
