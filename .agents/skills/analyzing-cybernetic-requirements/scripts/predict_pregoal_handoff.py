#!/usr/bin/env python3
"""Predict queue-friendly handoff text from JSON requirements control."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(REPO_ROOT / ".agents/skills/_shared"))

from information_sufficiency import information_sufficiency_errors  # noqa: E402


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
