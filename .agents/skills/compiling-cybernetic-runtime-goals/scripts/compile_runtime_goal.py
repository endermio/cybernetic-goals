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


def runtime_control_pointer(runtime_control_path: Path) -> str:
    return (
        f"/goal Execute the runtime control JSON at {runtime_control_path} "
        "using .agents/skills/using-control-json. Read it first; if required JSON is missing, "
        "invalid, or inconsistent, stop and report the smallest required human decision."
    )


def compile_runtime_control(run_dir: Path) -> Path:
    if not run_dir.exists() or not run_dir.is_dir():
        raise ControlJsonValidationError(f"run directory does not exist: {run_dir}")
    reject_markdown_control_artifacts(run_dir)

    runtime_path = run_dir / "runtime.control.json"
    if not runtime_path.exists():
        requirements = read_json_object(run_dir / "requirements.control.json")
        design = read_json_object(run_dir / "design.control.json")
        goal = read_json_object(run_dir / "goal.control.json")
        plan = read_json_object(run_dir / "plan.control.json")
        review = read_json_object(run_dir / "review.control.json")
        require_approved_control_inputs(
            {
                "requirements.control.json": requirements,
                "design.control.json": design,
                "goal.control.json": goal,
                "plan.control.json": plan,
                "review.control.json": review,
            }
        )

        plan_bindings = plan.get("registry_bindings", {})
        required_outcomes = plan.get("verifier", {}).get("required_outcomes")
        if not required_outcomes:
            required_outcomes = [
                outcome.get("id")
                for outcome in requirements.get("approved_control", {}).get("required_outcomes", [])
                if isinstance(outcome, dict)
                and isinstance(outcome.get("id"), str)
                and outcome.get("blocks_goal_achieved_if_missing") is True
            ]
        runtime = {
            "artifact_type": "runtime.control",
            "schema_version": goal.get("schema_version", "1"),
            "status": "compiled",
            "control_chain": {
                "requirements": "requirements.control.json",
                "design": "design.control.json",
                "goal": "goal.control.json",
                "plan": "plan.control.json",
                "review": "review.control.json",
            },
            "semantic_base_ref": plan.get("semantic_base_ref") or goal.get("semantic_base_ref"),
            "approved_control": {
                "objective": goal.get("approved_control", {}).get("objective", "Execute the approved JSON control chain."),
                "what_counts_as_done": goal.get("approved_control", {}).get("what_counts_as_done", "Verifier permits the final report."),
            },
            "registry_bindings": {
                "selected_agent_workflow": plan_bindings.get("selected_agent_workflow") or review.get("registry_bindings", {}).get("selected_agent_workflow"),
            },
            "approved_control_hashes": {},
            "runtime": {
                "readonly_files": APPROVED_CONTROL_FILES,
                "writable_files": WRITABLE_FILES,
                "writable_evidence_paths": plan.get("runtime", {}).get("writable_evidence_paths", WRITABLE_EVIDENCE_PATHS),
            },
            "required_steps": plan.get("required_steps", []),
            "progress": plan.get("progress", {"event_schema": "progress-event.schema.json", "append_only": True}),
            "verifier": {
                "required_before_goal_achieved": True,
                "command": "python3 .agents/skills/using-control-json/scripts/verify_runtime_progress.py",
                "required_outcomes": required_outcomes,
                "output_schema": plan.get("verifier", {}).get("output_schema", "final-report.schema.json"),
            },
        }
        runtime["approved_control_hashes"] = {
            "requirements.control.json": control_file_hash("requirements.control.json", requirements),
            "design.control.json": control_file_hash("design.control.json", design),
            "goal.control.json": control_file_hash("goal.control.json", goal),
            "plan.control.json": control_file_hash("plan.control.json", plan),
            "review.control.json": control_file_hash("review.control.json", review),
            "runtime.control.json": control_file_hash("runtime.control.json", runtime),
        }
        runtime_path.write_text(json.dumps(runtime, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    validate_json_control_run(run_dir)
    return runtime_path


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
