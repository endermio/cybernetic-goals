#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from control_json_runtime import (
    blocking_required_outcomes,
    covered_outcomes_by_steps,
    required_evidence_by_outcome,
    result_payload,
    read_progress_events,
    source_requirement_map,
    source_requirements_completed_by_evidence,
    step_outcome_map,
    step_ids,
    validate_control_chain,
    verify_approved_hashes,
)


def event_matches_generation(
    event: dict,
    *,
    current_generation: str | None,
    imported_evidence: set[str],
    invalidated_evidence: set[str],
) -> bool:
    evidence = event.get("evidence")
    evidence_ids = set(evidence) if isinstance(evidence, list) else set()
    evidence_ids = {item for item in evidence_ids if isinstance(item, str)}
    if evidence_ids & invalidated_evidence:
        return False
    if current_generation is None:
        return True
    if event.get("runtime_generation") == current_generation:
        return True
    return bool(evidence_ids & imported_evidence)


def unresolved_amendment_ids(events: list[dict], current_generation: str | None) -> set[str]:
    proposed: set[str] = set()
    resolved: set[str] = set()
    for event in events:
        if current_generation is not None and event.get("runtime_generation") != current_generation:
            continue
        amendment_id = event.get("amendment_id")
        if not isinstance(amendment_id, str) or not amendment_id:
            continue
        event_type = event.get("event_type")
        if event_type == "control.amendment.proposed":
            proposed.add(amendment_id)
        elif event_type in {
            "control.amendment.approved",
            "control.amendment.rejected",
            "control.amendment.blocked",
        }:
            resolved.add(amendment_id)
    return proposed - resolved


def anchor_changing_amendment_ids(events: list[dict], current_generation: str | None) -> set[str]:
    anchor_changing: set[str] = set()
    for event in events:
        if current_generation is not None and event.get("runtime_generation") != current_generation:
            continue
        if event.get("event_type") != "control.amendment.proposed":
            continue
        amendment_id = event.get("amendment_id")
        if not isinstance(amendment_id, str) or not amendment_id:
            continue
        if (
            event.get("semantic_base_change") is True
            or event.get("required_outcomes_changed") is True
            or event.get("authority_expanded") is True
        ):
            anchor_changing.add(amendment_id)
    return anchor_changing


def synthetic_required_step_ids(runtime: dict) -> set[str]:
    steps = runtime.get("required_steps")
    if not isinstance(steps, list):
        return set()
    return {
        step["step_id"]
        for step in steps
        if isinstance(step, dict)
        and step.get("synthetic") is True
        and isinstance(step.get("step_id"), str)
    }


def mainline_completed_steps(
    events: list[dict],
    *,
    current_generation: str | None = None,
    imported_evidence: set[str] | None = None,
    invalidated_evidence: set[str] | None = None,
) -> set[str]:
    completed: set[str] = set()
    imported_evidence = imported_evidence or set()
    invalidated_evidence = invalidated_evidence or set()
    for event in events:
        role = event.get("progress_role", "mainline")
        counts = event.get("counts_as_goal_progress", role == "mainline")
        if (
            event.get("event_type") == "step.completed"
            and event.get("status") == "pass"
            and role == "mainline"
            and counts is True
            and event.get("evidence")
            and event_matches_generation(
                event,
                current_generation=current_generation,
                imported_evidence=imported_evidence,
                invalidated_evidence=invalidated_evidence,
            )
        ):
            completed.add(event["required_step"])
    return completed


def mainline_evidence_by_completed_step(
    events: list[dict],
    *,
    current_generation: str | None = None,
    imported_evidence: set[str] | None = None,
    invalidated_evidence: set[str] | None = None,
) -> dict[str, set[str]]:
    evidence_by_step: dict[str, set[str]] = {}
    imported_evidence = imported_evidence or set()
    invalidated_evidence = invalidated_evidence or set()
    for event in events:
        role = event.get("progress_role", "mainline")
        counts = event.get("counts_as_goal_progress", role == "mainline")
        evidence = event.get("evidence")
        if (
            event.get("event_type") == "step.completed"
            and event.get("status") == "pass"
            and role == "mainline"
            and counts is True
            and isinstance(evidence, list)
            and all(isinstance(item, str) and item for item in evidence)
            and event_matches_generation(
                event,
                current_generation=current_generation,
                imported_evidence=imported_evidence,
                invalidated_evidence=invalidated_evidence,
            )
        ):
            evidence_by_step.setdefault(event["required_step"], set()).update(evidence)
    return evidence_by_step


def final_report_errors(
    final_report: dict,
    *,
    current_generation: str | None = None,
    unresolved_amendments: set[str] | None = None,
    anchor_changing_amendments: set[str] | None = None,
    strategy_kind: str | None = None,
    synthetic_required_steps: set[str] | None = None,
) -> list[str]:
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
    if current_generation is not None and final_report.get("runtime_generation") != current_generation:
        errors.append("final-report.json runtime_generation must match current_generation")
    if strategy_kind == "discovery":
        errors.append("discovery generation cannot permit goal_achieved true")
    synthetic_required_steps = synthetic_required_steps or set()
    if synthetic_required_steps:
        errors.append("synthetic required_steps cannot permit goal_achieved true: " + ", ".join(sorted(synthetic_required_steps)))
    unresolved_amendments = unresolved_amendments or set()
    anchor_changing_amendments = anchor_changing_amendments or set()
    reported_unresolved = final_report.get("unresolved_amendments")
    if unresolved_amendments:
        errors.append("unresolved amendments block goal_achieved true: " + ", ".join(sorted(unresolved_amendments)))
    if anchor_changing_amendments:
        errors.append("anchor-changing amendments require human decision: " + ", ".join(sorted(anchor_changing_amendments)))
    if reported_unresolved:
        errors.append("final-report.json unresolved_amendments must be empty before goal_achieved true")
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
        readonly_files = artifacts["runtime"].get("runtime", {}).get("readonly_files")
        readonly = tuple(readonly_files) if isinstance(readonly_files, list) else None
        errors.extend(verify_approved_hashes(run_dir, Path(args.approved_hashes), readonly or None))

    events, event_errors = read_progress_events(run_dir / "progress.jsonl")
    errors.extend(event_errors)

    required_steps = step_ids(artifacts["runtime"])
    run_control = artifacts.get("run")
    current_generation = run_control.get("current_generation") if isinstance(run_control, dict) else None
    if not isinstance(current_generation, str):
        current_generation = None
    generation = None
    if isinstance(run_control, dict) and current_generation is not None:
        for candidate in run_control.get("generations", []):
            if isinstance(candidate, dict) and candidate.get("id") == current_generation:
                generation = candidate
                break
    strategy_kind = generation.get("strategy_kind") if isinstance(generation, dict) else None
    runtime = artifacts["runtime"]
    imported_evidence = set(
        item for item in runtime.get("imported_evidence", []) if isinstance(item, str)
    )
    invalidated_evidence = set(
        item for item in runtime.get("invalidated_evidence", []) if isinstance(item, str)
    )
    unresolved = unresolved_amendment_ids(events, current_generation)
    anchor_changing = anchor_changing_amendment_ids(events, current_generation)
    synthetic_steps = synthetic_required_step_ids(runtime)
    evidence_by_step = mainline_evidence_by_completed_step(
        events,
        current_generation=current_generation,
        imported_evidence=imported_evidence,
        invalidated_evidence=invalidated_evidence,
    )
    completed_steps = set(evidence_by_step)
    required_outcomes = blocking_required_outcomes(artifacts["requirements"])
    runtime_step_outcomes = step_outcome_map(artifacts["runtime"])
    completed_outcomes = covered_outcomes_by_steps(runtime_step_outcomes, completed_steps)
    completed_evidence_ids = set()
    for evidence_ids in evidence_by_step.values():
        completed_evidence_ids.update(evidence_ids)
    source_requirements, blocking_source_requirements, _ = source_requirement_map(artifacts["requirements"])
    completed_source_requirements = source_requirements_completed_by_evidence(
        artifacts["requirements"],
        completed_evidence_ids,
    )
    missing_steps = sorted(required_steps - completed_steps)
    if missing_steps:
        errors.append(
            "missing mainline evidence-backed progress for required steps: "
            + ", ".join(missing_steps)
        )
    missing_outcomes = sorted(required_outcomes - completed_outcomes)
    if missing_outcomes:
        errors.append(
            "missing mainline evidence-backed progress for blocking required outcomes: "
            + ", ".join(missing_outcomes)
        )
    required_evidence = required_evidence_by_outcome(artifacts["requirements"])
    evidence_by_outcome: dict[str, set[str]] = {}
    for step_id, evidence_ids in evidence_by_step.items():
        for outcome_id in runtime_step_outcomes.get(step_id, set()):
            evidence_by_outcome.setdefault(outcome_id, set()).update(evidence_ids)
    missing_evidence_messages = []
    for outcome_id in sorted(required_outcomes):
        missing_evidence = sorted(required_evidence.get(outcome_id, set()) - evidence_by_outcome.get(outcome_id, set()))
        if missing_evidence:
            missing_evidence_messages.append(f"{outcome_id}: " + ", ".join(missing_evidence))
    if missing_evidence_messages:
        errors.append(
            "missing required evidence for blocking required outcomes: "
            + "; ".join(missing_evidence_messages)
        )
    missing_source_requirements = sorted(blocking_source_requirements - completed_source_requirements)
    if missing_source_requirements:
        errors.append(
            "missing completed evidence for blocking source requirements: "
            + ", ".join(missing_source_requirements)
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
        errors.extend(
            final_report_errors(
                final_report,
                current_generation=current_generation,
                unresolved_amendments=unresolved,
                anchor_changing_amendments=anchor_changing,
                strategy_kind=strategy_kind if isinstance(strategy_kind, str) else None,
                synthetic_required_steps=synthetic_steps,
            )
        )
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
                completed_required_outcomes=sorted(completed_outcomes),
                required_outcomes=sorted(required_outcomes),
                completed_source_requirements=sorted(completed_source_requirements),
                source_requirements=sorted(source_requirements),
                current_generation=current_generation,
                unresolved_amendments=sorted(unresolved),
                anchor_changing_amendments=sorted(anchor_changing),
            ),
            indent=2,
        )
    )
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
