#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from bounded_control_runtime import (
    completed_step_evidence,
    load_json,
    normalize_run_dir,
    read_progress_events,
    required_step_map,
    result_payload,
    validate_bounded_runtime,
)


def final_report_errors(final_report: dict) -> list[str]:
    errors: list[str] = []
    if final_report.get("goal_achieved") is not True:
        errors.append("final-report.json goal_achieved must be true")
    if final_report.get("what_counts_as_done_met") is not True:
        errors.append("final-report.json what_counts_as_done_met must be true")
    if final_report.get("remaining_gaps") not in ([], None):
        errors.append("final-report.json remaining_gaps must be empty for goal_achieved")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify a bounded_runtime progress log and final report.")
    parser.add_argument("runtime_or_run_dir", help="Run directory or path to runtime.control.json.")
    args = parser.parse_args()

    run_dir = normalize_run_dir(Path(args.runtime_or_run_dir))
    _goal, runtime, errors = validate_bounded_runtime(run_dir)
    if runtime is None:
        print(json.dumps(result_payload(False, errors, goal_achieved_permitted=False, run_dir=str(run_dir)), indent=2))
        return 1

    events, event_errors = read_progress_events(run_dir)
    errors.extend(event_errors)
    step_requirements = required_step_map(runtime)
    evidence_by_step = completed_step_evidence(events)

    missing_steps = sorted(set(step_requirements) - set(evidence_by_step))
    if missing_steps:
        errors.append("missing mainline evidence-backed progress for required steps: " + ", ".join(missing_steps))

    missing_evidence_messages = []
    for step_id, required_evidence in sorted(step_requirements.items()):
        missing_evidence = sorted(required_evidence - evidence_by_step.get(step_id, set()))
        if missing_evidence:
            missing_evidence_messages.append(f"{step_id}: " + ", ".join(missing_evidence))
    if missing_evidence_messages:
        errors.append("missing required evidence for required steps: " + "; ".join(missing_evidence_messages))

    try:
        final_report = load_json(run_dir / "final-report.json")
    except Exception as exc:
        final_report = None
        errors.append(str(exc))
    if final_report is not None:
        errors.extend(final_report_errors(final_report))

    ok = not errors
    print(
        json.dumps(
            result_payload(
                ok,
                errors,
                goal_achieved_permitted=ok,
                completed_required_steps=sorted(evidence_by_step),
                required_steps=sorted(step_requirements),
                run_dir=str(run_dir),
            ),
            indent=2,
        )
    )
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
