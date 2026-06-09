#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from control_json_runtime import (
    result_payload,
    read_progress_events,
    step_ids,
    validate_control_chain,
    verify_approved_hashes,
)


def mainline_completed_steps(events: list[dict]) -> set[str]:
    completed: set[str] = set()
    for event in events:
        role = event.get("progress_role", "mainline")
        counts = event.get("counts_as_goal_progress", role == "mainline")
        if (
            event.get("event_type") == "step.completed"
            and event.get("status") == "pass"
            and role == "mainline"
            and counts is True
            and event.get("evidence")
        ):
            completed.add(event["required_step"])
    return completed


def final_report_errors(final_report: dict) -> list[str]:
    errors: list[str] = []
    if final_report.get("goal_achieved") is not True:
        errors.append("not-done final report cannot be treated as success")
    if final_report.get("what_counts_as_done_met") is not True:
        errors.append("what_counts_as_done_met must be true")
    verification = final_report.get("verification")
    if not isinstance(verification, dict):
        errors.append("final-report.json missing verification object")
    else:
        if verification.get("verifier_result") != "pass" or verification.get("verifier_permits_goal_achieved") is not True:
            errors.append("verifier does not permit goal_achieved true")
    work_coverage = final_report.get("work_coverage")
    if not isinstance(work_coverage, dict) or work_coverage.get("status") != "complete":
        errors.append("work coverage must be complete before goal_achieved true")
    if final_report.get("remaining_gaps"):
        errors.append("remaining_gaps must be empty before goal_achieved true")
    if not final_report.get("evidence"):
        errors.append("final-report.json must include evidence")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Judge whether runtime progress permits goal_achieved true.")
    parser.add_argument("run_dir", help="Directory containing runtime.control.json, progress.jsonl, and final-report.json.")
    parser.add_argument("--approved-hashes", help="JSON mapping of read-only control files to pre-runtime sha256 hashes.")
    args = parser.parse_args()

    run_dir = Path(args.run_dir)
    artifacts, errors = validate_control_chain(run_dir)
    if artifacts is None:
        print(json.dumps(result_payload(False, errors, goal_achieved_permitted=False), indent=2))
        return 1

    if args.approved_hashes:
        errors.extend(verify_approved_hashes(run_dir, Path(args.approved_hashes)))

    events, event_errors = read_progress_events(run_dir / "progress.jsonl")
    errors.extend(event_errors)

    required_steps = step_ids(artifacts["runtime"])
    completed_steps = mainline_completed_steps(events)
    missing_steps = sorted(required_steps - completed_steps)
    if missing_steps:
        errors.append(
            "missing mainline evidence-backed progress for required steps: "
            + ", ".join(missing_steps)
        )

    final_report_path = run_dir / "final-report.json"
    try:
        final_report = json.loads(final_report_path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        final_report = {}
        errors.append("missing runtime final report: final-report.json")
    except json.JSONDecodeError as exc:
        final_report = {}
        errors.append(f"invalid JSON in final-report.json: {exc}")
    if isinstance(final_report, dict):
        errors.extend(final_report_errors(final_report))
    else:
        errors.append("final-report.json must contain a JSON object")

    ok = not errors
    print(
        json.dumps(
            result_payload(
                ok,
                errors,
                goal_achieved_permitted=ok,
                completed_required_steps=sorted(completed_steps),
                required_steps=sorted(required_steps),
            ),
            indent=2,
        )
    )
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
