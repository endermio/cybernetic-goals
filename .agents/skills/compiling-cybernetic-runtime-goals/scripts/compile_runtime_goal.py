#!/usr/bin/env python3
"""Compile runtime.control.json and a short /goal pointer from a JSON run directory."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from control_chain_guard import (
    ControlJsonValidationError,
    control_file_hash,
    generation_entry,
    generation_runtime_readonly_files,
    require_generation_review_checks,
    synthetic_steps_from_requirements,
    read_json_object,
    reject_markdown_control_artifacts,
    require_approved_control_inputs,
    validate_json_control_run,
)


APPROVED_CONTROL_FILES = [
    "requirements.control.json",
    "design.control.json",
    "goal.control.json",
    "plan.control.json",
    "review.control.json",
    "runtime.control.json",
]
WRITABLE_FILES = ["progress.jsonl", "runtime-status.json", "final-report.json"]
WRITABLE_EVIDENCE_PATHS = ["evidence/"]
RUN_STRATEGY_FIELDS = [
    "control_level",
    "target_model",
    "strategy_policy",
    "gate_mode",
    "phase_structure",
]


def runtime_control_pointer(runtime_control_path: Path) -> str:
    return (
        f"/goal Execute the runtime control JSON at {runtime_control_path} "
        "using .agents/skills/using-control-json. Read it first; if required JSON is missing, "
        "invalid, or inconsistent, stop and report the smallest required human decision."
    )


def blocking_required_outcome_ids(requirements: dict) -> list[str]:
    outcomes = requirements.get("approved_control", {}).get("required_outcomes", [])
    if not isinstance(outcomes, list):
        return []
    return [
        outcome["id"]
        for outcome in outcomes
        if isinstance(outcome, dict)
        and isinstance(outcome.get("id"), str)
        and outcome.get("blocks_goal_achieved_if_missing") is True
    ]


def require_review_before_runtime_write(run_dir: Path, generation: dict, strategy_kind: object) -> None:
    if strategy_kind not in {"execution", "amendment"}:
        return
    review_rel = generation.get("review")
    if not isinstance(review_rel, str) or not review_rel:
        raise ControlJsonValidationError(f"run.control.json: {strategy_kind} generations must declare review")
    review = read_json_object(run_dir / review_rel)
    if review.get("artifact_type") != "review.control":
        raise ControlJsonValidationError(f"{review_rel}: expected artifact_type review.control")
    if review.get("status") != "approved":
        raise ControlJsonValidationError(f"{review_rel}: generation review must be approved")
    require_generation_review_checks(review, context=f"{strategy_kind} generation")


def compile_generation_runtime_control(run_dir: Path) -> Path:
    requirements = read_json_object(run_dir / "requirements.control.json")
    run_control = read_json_object(run_dir / "run.control.json")
    current_generation = run_control.get("current_generation")
    if not isinstance(current_generation, str) or not current_generation:
        raise ControlJsonValidationError("run.control.json: current_generation must be a non-empty string")
    generation = generation_entry(run_control, current_generation)
    if not generation:
        raise ControlJsonValidationError("run.control.json: current_generation is not declared in generations")
    runtime_rel = generation.get("runtime")
    if not isinstance(runtime_rel, str) or not runtime_rel:
        raise ControlJsonValidationError("run.control.json: current_generation must name runtime")

    runtime_path = run_dir / runtime_rel
    if not runtime_path.exists():
        strategy_kind = generation.get("strategy_kind")
        require_review_before_runtime_write(run_dir, generation, strategy_kind)
        runtime_path.parent.mkdir(parents=True, exist_ok=True)
        required_steps = generation.get("required_steps")
        if not isinstance(required_steps, list) or not required_steps:
            if generation.get("strategy_kind") != "discovery":
                raise ControlJsonValidationError(
                    "run.control.json: only discovery generations may use synthetic required_steps"
                )
            required_steps = synthetic_steps_from_requirements(requirements)
        verifier = generation.get("verifier")
        if not isinstance(verifier, dict):
            verifier = {
                "required_before_goal_achieved": True,
                "command": "python3 .agents/skills/using-control-json/scripts/verify_runtime_progress.py",
                "required_outcomes": blocking_required_outcome_ids(requirements),
                "output_schema": "final-report.schema.json",
            }
        writable_evidence_paths = generation.get("writable_evidence_paths")
        if not isinstance(writable_evidence_paths, list) or not writable_evidence_paths:
            writable_evidence_paths = WRITABLE_EVIDENCE_PATHS
        imported_evidence = generation.get("imported_evidence")
        if not isinstance(imported_evidence, list):
            imported_evidence = []
        invalidated_evidence = generation.get("invalidated_evidence")
        if not isinstance(invalidated_evidence, list):
            invalidated_evidence = []
        runtime = {
            "artifact_type": "runtime.control",
            "schema_version": run_control.get("schema_version", "1.0.0"),
            "status": "compiled",
            "generation": {
                "id": current_generation,
            },
            "semantic_base_ref": run_control.get("semantic_base_ref"),
            "approved_control": {
                "objective": requirements.get("approved_control", {}).get("requested_transformation", "Execute the current approved generation."),
                "what_counts_as_done": requirements.get("approved_control", {}).get("what_counts_as_done", "Verifier permits the final report."),
            },
            "approved_control_hashes": {},
            "runtime": {
                "readonly_files": generation_runtime_readonly_files(generation),
                "writable_files": WRITABLE_FILES,
                "writable_evidence_paths": writable_evidence_paths,
            },
            "required_steps": required_steps,
            "progress": {"event_schema": "progress-event.schema.json", "append_only": True},
            "verifier": verifier,
            "imported_evidence": imported_evidence,
            "invalidated_evidence": invalidated_evidence,
        }
        for field in RUN_STRATEGY_FIELDS:
            runtime[field] = run_control.get(field)
        review_rel = generation.get("review")
        if isinstance(review_rel, str) and review_rel:
            review = read_json_object(run_dir / review_rel)
            runtime["approved_control_hashes"][review_rel] = control_file_hash(review_rel, review)
        runtime["approved_control_hashes"].update(
            {
                "requirements.control.json": control_file_hash("requirements.control.json", requirements),
                "run.control.json": control_file_hash("run.control.json", run_control),
                runtime_rel: control_file_hash(runtime_rel, runtime),
            }
        )
        runtime_path.write_text(json.dumps(runtime, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    validate_json_control_run(run_dir)
    return runtime_path


def compile_runtime_control(run_dir: Path) -> Path:
    if not run_dir.exists() or not run_dir.is_dir():
        raise ControlJsonValidationError(f"run directory does not exist: {run_dir}")
    reject_markdown_control_artifacts(run_dir)
    if not (run_dir / "run.control.json").exists():
        raise ControlJsonValidationError("missing run.control.json; official JSON control runs must use run.control.json")
    return compile_generation_runtime_control(run_dir)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", help="Official JSON control run directory containing *.control.json files.")
    parser.add_argument("--requirements", help=argparse.SUPPRESS)
    parser.add_argument("--clarification", help=argparse.SUPPRESS)
    parser.add_argument("--design", help=argparse.SUPPRESS)
    parser.add_argument("--goal", help=argparse.SUPPRESS)
    parser.add_argument("--plan", help=argparse.SUPPRESS)
    parser.add_argument("--review", help=argparse.SUPPRESS)
    parser.add_argument("--out", help=argparse.SUPPRESS)
    parser.add_argument("--expect-work-assignment", help=argparse.SUPPRESS)
    parser.add_argument("--expect-subagent-mode", help=argparse.SUPPRESS)
    parser.add_argument("--skip-guard", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("--i-understand-this-bypasses-phase-checks", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args()

    if not args.run_dir:
        print(
            "ERROR: official control input is JSON-only; use --run-dir with docs/cybernetics/runs/<slug>/",
            file=sys.stderr,
        )
        return 2
    if any(
        (
            args.requirements,
            args.clarification,
            args.design,
            args.goal,
            args.plan,
            args.review,
            args.out,
            args.expect_work_assignment,
            args.expect_subagent_mode,
            args.skip_guard,
            args.i_understand_this_bypasses_phase_checks,
        )
    ):
        print(
            "ERROR: --run-dir is the official JSON control input; do not combine it with Markdown artifact inputs, .goal.md output, or legacy assertions",
            file=sys.stderr,
        )
        return 2

    try:
        runtime_path = compile_runtime_control(Path(args.run_dir))
    except ControlJsonValidationError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    print("Runtime control JSON ready:")
    print(runtime_path)
    print()
    print("Use this /goal:")
    print(runtime_control_pointer(runtime_path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
