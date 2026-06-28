#!/usr/bin/env python3
"""Drive the requirements-analysis information sufficiency loop.

This script does not compile pre-goal artifacts. It reports the next
requirements-analysis action before approval: independent counterexample
review, safe information gathering, user input, requirements revision, or
approval readiness.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(REPO_ROOT / ".agents/skills/_shared"))

from transition_gate import transition_gate_payload  # noqa: E402
from information_sufficiency import evidence_ref_path_errors, information_sufficiency_errors  # noqa: E402


SAFE_ACTION_TYPES = {"read_source", "read_documentation", "run_no_side_effect_probe"}
USER_ACTION_TYPES = {"ask_user", "external_access_request", "human_decision"}
UNFINISHED_FACT_STATUSES = {
    "missing",
    "needs_information_gathering",
    "needs_user_input",
    "needs_requirements_revision",
    "blocked",
}


def read_json_object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, str) and item]


def fact_by_id(check: dict[str, Any]) -> dict[str, dict[str, Any]]:
    facts = check.get("facts")
    if not isinstance(facts, list):
        return {}
    result: dict[str, dict[str, Any]] = {}
    for fact in facts:
        if isinstance(fact, dict) and isinstance(fact.get("fact_id"), str):
            result[fact["fact_id"]] = fact
    return result


def information_check(requirements: dict[str, Any]) -> dict[str, Any]:
    approved = requirements.get("approved_control")
    if not isinstance(approved, dict):
        raise ValueError("requirements.control.json approved_control must be an object")
    check = approved.get("information_sufficiency_check")
    if not isinstance(check, dict):
        raise ValueError("approved_control.information_sufficiency_check must be an object")
    return check


def base_payload(run_dir: Path, requirements: dict[str, Any], check: dict[str, Any]) -> dict[str, Any]:
    return {
        "run_dir": str(run_dir),
        "requirements_status": requirements.get("status"),
        "information_sufficiency_status": check.get("status"),
        "automatic_actions": [],
        "user_actions": [],
        "blocking_reasons": [],
    }


def gate_payload(
    payload: dict[str, Any],
    *,
    ok: bool,
    next_action: str,
    errors: list[str] | None = None,
    **fields: Any,
) -> dict[str, Any]:
    blocking_reasons = payload.get("blocking_reasons")
    result = transition_gate_payload(
        ok=ok,
        gate_id="requirements-information-sufficiency",
        next_action=next_action,
        errors=errors if errors is not None else blocking_reasons if isinstance(blocking_reasons, list) else [],
        **fields,
    )
    result.update(payload)
    result["next_action"] = next_action
    result["requires_user_authorization"] = result["may_ask_user"]
    return result


def review_prompt(check: dict[str, Any]) -> str:
    facts = fact_by_id(check)
    lines = [
        "Run an independent requirements information sufficiency counterexample review.",
        "Try to find missing facts that would make later design or plan invalid.",
        "Do not ask the user for permission to run this review; it is an internal requirements-analysis gate.",
        "",
        "Facts to challenge:",
    ]
    for fact_id, fact in sorted(facts.items()):
        lines.append(f"- {fact_id}: {fact.get('statement', '')}")
        lines.append(f"  why needed: {fact.get('why_needed', '')}")
    lines.extend(
        [
            "",
            "Required transformations to check:",
            "- source_requirements->information_sufficiency_facts",
            "- required_outcomes->information_sufficiency_facts",
            "- information_sufficiency_facts->design_plan_entry",
        ]
    )
    return "\n".join(lines)


def action_summary(action: dict[str, Any], facts: dict[str, dict[str, Any]]) -> dict[str, Any]:
    fact_id = action.get("fact_id")
    fact = facts.get(fact_id) if isinstance(fact_id, str) else None
    item = {
        "action_id": action.get("action_id"),
        "fact_id": fact_id,
        "fact": fact.get("statement") if fact else None,
        "action_type": action.get("action_type"),
        "status": action.get("status"),
        "why_safe_or_needed": action.get("why_safe_or_needed"),
        "evidence_ref": action.get("evidence_ref"),
    }
    for key in ("command", "working_dir", "paths", "question", "allow_automatic_execution"):
        if key in action:
            item[key] = action[key]
    return item


def has_string_list(value: Any) -> bool:
    return isinstance(value, list) and any(isinstance(item, str) and item for item in value)


def has_command(value: Any) -> bool:
    return has_string_list(value)


def action_detail_errors(run_dir: Path, action: dict[str, Any], action_type: Any, action_ref: Any) -> list[str]:
    errors = evidence_ref_path_errors(
        run_dir,
        f"collection action {action_ref}",
        action.get("evidence_ref"),
        require_exists=False,
    )
    if not isinstance(action.get("action_id"), str) or not action["action_id"].strip():
        errors.append(f"collection action {action_ref} must include non-empty action_id")
    if not isinstance(action.get("why_safe_or_needed"), str) or not action["why_safe_or_needed"].strip():
        errors.append(f"collection action {action_ref} must include non-empty why_safe_or_needed")
    if action.get("allow_automatic_execution") is False and action_type in SAFE_ACTION_TYPES:
        errors.append(f"collection action {action_ref} cannot be automatic when allow_automatic_execution is false")
    if action_type == "run_no_side_effect_probe" and action.get("allow_automatic_execution") is not True:
        errors.append(f"collection action {action_ref} must set allow_automatic_execution true for automatic probes")
    if action_type in {"read_source", "read_documentation"} and not has_string_list(action.get("paths")):
        errors.append(f"collection action {action_ref} with action_type {action_type!r} must include non-empty paths")
    if action_type == "run_no_side_effect_probe" and not has_command(action.get("command")):
        errors.append(f"collection action {action_ref} with action_type 'run_no_side_effect_probe' must include command")
    if action_type in USER_ACTION_TYPES and not isinstance(action.get("question"), str):
        errors.append(f"collection action {action_ref} with action_type {action_type!r} must include question")
    elif action_type in USER_ACTION_TYPES and not action["question"].strip():
        errors.append(f"collection action {action_ref} with action_type {action_type!r} must include a non-empty question")
    return errors


def approval_or_handoff_errors(requirements: dict[str, Any], run_dir: Path) -> list[str]:
    return information_sufficiency_errors(requirements, run_dir)


def requires_counterexample_review(errors: list[str]) -> bool:
    review_error_prefixes = (
        "information_sufficiency_check counterexample_review must pass with verdict approved",
        "information_sufficiency_check counterexample_review missing checked_facts:",
        "information_sufficiency_check counterexample_review missing checked_transformations:",
    )
    return bool(errors) and all(error.startswith(review_error_prefixes) for error in errors)


def classify_actions(run_dir: Path, check: dict[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[str]]:
    facts = fact_by_id(check)
    check_status = check.get("status")
    automatic: list[dict[str, Any]] = []
    user: list[dict[str, Any]] = []
    errors: list[str] = []
    current_blocking_fact_ids = {
        fact_id
        for fact_id, fact in facts.items()
        if fact.get("blocks_design_or_plan_if_missing") is True and fact.get("current_status") == check_status
    }
    mismatched_blocking_facts = [
        f"{fact_id} ({fact.get('current_status')!r})"
        for fact_id, fact in sorted(facts.items())
        if fact.get("blocks_design_or_plan_if_missing") is True
        and fact.get("current_status") in UNFINISHED_FACT_STATUSES
        and fact.get("current_status") != check_status
    ]
    if mismatched_blocking_facts:
        errors.append(
            "information_sufficiency_check has unfinished blocking facts outside current status: "
            + ", ".join(mismatched_blocking_facts)
        )
    actions = check.get("collection_actions")
    if not isinstance(actions, list) or not actions:
        return automatic, user, ["information_sufficiency_check needs collection_actions for unsatisfied facts"]
    covered_blocking_fact_ids: set[str] = set()
    for index, action in enumerate(actions):
        if not isinstance(action, dict):
            errors.append(f"collection_actions[{index}] must be an object")
            continue
        action_type = action.get("action_type")
        fact_id = action.get("fact_id")
        if not isinstance(fact_id, str) or fact_id not in facts:
            errors.append(f"collection action {action.get('action_id') or index} references unknown fact_id")
            continue
        action_ref = action.get("action_id") or index
        fact_status = facts[fact_id].get("current_status")
        if fact_status != check_status:
            errors.append(
                f"collection action {action_ref} targets fact {fact_id} with current_status {fact_status!r}, "
                f"but information_sufficiency_check status is {check_status!r}"
            )
            continue
        if action.get("status") != "planned":
            errors.append(f"collection action {action_ref} must have status 'planned' to be used as the next action")
            continue
        detail_errors = action_detail_errors(run_dir, action, action_type, action_ref)
        if detail_errors:
            errors.extend(detail_errors)
            continue
        summary = action_summary(action, facts)
        if action_type in SAFE_ACTION_TYPES:
            automatic.append(summary)
            if fact_id in current_blocking_fact_ids:
                covered_blocking_fact_ids.add(fact_id)
        elif action_type in USER_ACTION_TYPES:
            user.append(summary)
            if fact_id in current_blocking_fact_ids:
                covered_blocking_fact_ids.add(fact_id)
        else:
            errors.append(f"collection action {action.get('action_id') or index} has unsupported action_type {action_type!r}")
    missing_blocking_fact_ids = sorted(current_blocking_fact_ids - covered_blocking_fact_ids)
    if missing_blocking_fact_ids:
        errors.append(
            "information_sufficiency_check collection_actions missing current blocking facts: "
            + ", ".join(missing_blocking_fact_ids)
        )
    if errors:
        return [], [], errors
    return automatic, user, errors


def next_action(run_dir: Path, requirements: dict[str, Any]) -> dict[str, Any]:
    check = information_check(requirements)
    status = check.get("status")
    payload = base_payload(run_dir, requirements, check)

    if requirements.get("status") == "approved" and status in {"satisfied", "not_required"}:
        handoff_errors = approval_or_handoff_errors(requirements, run_dir)
        if handoff_errors:
            payload["blocking_reasons"] = handoff_errors
            next_gate_action = (
                "RunInformationCounterexampleReview"
                if requires_counterexample_review(handoff_errors)
                else "RepairRequirementsInformationState"
            )
            return gate_payload(
                payload,
                ok=False,
                next_action=next_gate_action,
                review_prompt=review_prompt(check),
            )
        return gate_payload(
            payload,
            ok=True,
            next_action="ReadyForPreGoalHandoff",
            message="Information sufficiency is complete; run predict_pregoal_handoff.py next.",
        )

    if status == "needs_counterexample_review" or requirements.get("status") == "pending_counterexample_review":
        return gate_payload(
            payload,
            ok=False,
            next_action="RunInformationCounterexampleReview",
            review_prompt=review_prompt(check),
        )

    if status == "needs_requirements_revision" or requirements.get("status") == "needs_requirements_revision":
        return gate_payload(
            payload,
            ok=False,
            next_action="ReviseRequirements",
            message=(
                "Newly gathered information changes the requested result, completion standard, "
                "authority, or forbidden actions. Revise requirements before asking for approval."
            ),
        )

    if status == "blocked" or requirements.get("status") == "blocked":
        return gate_payload(
            payload,
            ok=False,
            next_action="RequirementsInformationBlocked",
            message="A design-blocking fact cannot currently be collected.",
        )

    if status in {"satisfied", "not_required"}:
        if requirements.get("status") != "pending_approval":
            payload["blocking_reasons"] = [
                "requirements.control.json status must be pending_approval before asking for user approval"
            ]
            return gate_payload(payload, ok=False, next_action="RepairRequirementsInformationState")
        approval_errors = approval_or_handoff_errors(requirements, run_dir)
        if approval_errors:
            payload["blocking_reasons"] = approval_errors
            next_gate_action = (
                "RunInformationCounterexampleReview"
                if requires_counterexample_review(approval_errors)
                else "RepairRequirementsInformationState"
            )
            return gate_payload(
                payload,
                ok=False,
                next_action=next_gate_action,
                review_prompt=review_prompt(check),
            )
        return gate_payload(
            payload,
            ok=True,
            next_action="ReadyForUserApproval",
            message="Information sufficiency is complete; show the requirements approval commitment.",
        )

    automatic, user, errors = classify_actions(run_dir, check)
    payload["automatic_actions"] = automatic
    payload["user_actions"] = user
    payload["blocking_reasons"] = errors

    if errors:
        return gate_payload(payload, ok=False, next_action="RepairRequirementsInformationState")

    if status == "needs_user_input":
        if not user:
            payload["blocking_reasons"] = [
                "information_sufficiency_check status needs_user_input requires at least one user collection action"
            ]
            return gate_payload(payload, ok=False, next_action="RepairRequirementsInformationState")
        return gate_payload(payload, ok=False, next_action="AskUserForInformation")

    if status == "needs_information_gathering":
        if not automatic:
            payload["blocking_reasons"] = [
                "information_sufficiency_check status needs_information_gathering requires at least one safe automatic collection action"
            ]
            return gate_payload(payload, ok=False, next_action="RepairRequirementsInformationState")
        return gate_payload(payload, ok=False, next_action="RunInformationGathering")

    if user:
        return gate_payload(payload, ok=False, next_action="AskUserForInformation")

    if automatic:
        return gate_payload(payload, ok=False, next_action="RunInformationGathering")

    payload["blocking_reasons"] = errors or [f"unsupported information_sufficiency_check status {status!r}"]
    return gate_payload(payload, ok=False, next_action="RepairRequirementsInformationState")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=True, help="Path to docs/cybernetics/runs/<slug>.")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON.")
    args = parser.parse_args()

    run_dir = Path(args.run_dir)
    try:
        requirements = read_json_object(run_dir / "requirements.control.json")
        payload = next_action(run_dir, requirements)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        payload = transition_gate_payload(
            ok=False,
            gate_id="requirements-information-sufficiency",
            next_action="RepairRequirementsInformationState",
            errors=[str(exc)],
            run_dir=str(run_dir),
            blocking_reasons=[str(exc)],
        )
        payload["requires_user_authorization"] = payload["may_ask_user"]
        if args.json:
            print(json.dumps(payload, ensure_ascii=False, indent=2))
        else:
            print(f"NEXT: {payload['next_action']}")
            print(f"ERROR: {payload['blocking_reasons'][0]}")
        return 2

    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(f"NEXT: {payload['next_action']}")
        print(f"TERMINAL: {str(payload.get('terminal')).lower()}")
        print(f"RERUN_REQUIRED: {str(payload.get('rerun_required')).lower()}")
        print(f"USER_ACTION_REQUIRED: {str(payload.get('user_action_required')).lower()}")
        print(f"AGENT_MUST_CONTINUE: {str(payload.get('agent_must_continue')).lower()}")
        if payload.get("agent_must_continue") and not payload.get("may_ask_user"):
            print("DO_NOT_ASK_USER_AUTHORIZATION")
        if payload.get("message"):
            print(payload["message"])
        for reason in payload.get("blocking_reasons", []):
            print(f"ERROR: {reason}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
