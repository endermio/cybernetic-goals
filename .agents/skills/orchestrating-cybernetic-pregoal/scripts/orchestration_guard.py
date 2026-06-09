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
        data = payload(False, args.state, "FixJsonControlRun", errors)
        print_result(data, args.json)
        return 2

    data = payload(True, args.state, NEXT_ACTION[args.state], [])
    print_result(data, args.json)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
