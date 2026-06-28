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


SAFE_ACTION_TYPES = {"read_source", "read_documentation", "run_no_side_effect_probe"}
USER_ACTION_TYPES = {"ask_user", "external_access_request", "human_decision"}


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
    if isinstance(value, str):
        return bool(value.strip())
    return has_string_list(value)


def action_detail_errors(action: dict[str, Any], action_type: Any, action_ref: Any) -> list[str]:
    if action_type in {"read_source", "read_documentation"} and not has_string_list(action.get("paths")):
        return [f"collection action {action_ref} with action_type {action_type!r} must include non-empty paths"]
    if action_type == "run_no_side_effect_probe" and not has_command(action.get("command")):
        return [f"collection action {action_ref} with action_type 'run_no_side_effect_probe' must include command"]
    if action_type in USER_ACTION_TYPES and not isinstance(action.get("question"), str):
        return [f"collection action {action_ref} with action_type {action_type!r} must include question"]
    if action_type in USER_ACTION_TYPES and not action["question"].strip():
        return [f"collection action {action_ref} with action_type {action_type!r} must include a non-empty question"]
    return []


def counterexample_review_passed(check: dict[str, Any]) -> bool:
    review = check.get("counterexample_review")
    return (
        isinstance(review, dict)
        and review.get("status") == "pass"
        and review.get("verdict") == "approved"
    )


def counterexample_review_errors(check: dict[str, Any]) -> list[str]:
    if counterexample_review_passed(check):
        return []
    return ["information_sufficiency_check counterexample_review must pass with verdict approved before approval or handoff"]


def classify_actions(check: dict[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[str]]:
    facts = fact_by_id(check)
    automatic: list[dict[str, Any]] = []
    user: list[dict[str, Any]] = []
    errors: list[str] = []
    actions = check.get("collection_actions")
    if not isinstance(actions, list) or not actions:
        return automatic, user, ["information_sufficiency_check needs collection_actions for unsatisfied facts"]
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
        if action.get("status") != "planned":
            errors.append(f"collection action {action_ref} must have status 'planned' to be used as the next action")
            continue
        detail_errors = action_detail_errors(action, action_type, action_ref)
        if detail_errors:
            errors.extend(detail_errors)
            continue
        summary = action_summary(action, facts)
        if action_type in SAFE_ACTION_TYPES:
            automatic.append(summary)
        elif action_type in USER_ACTION_TYPES:
            user.append(summary)
        else:
            errors.append(f"collection action {action.get('action_id') or index} has unsupported action_type {action_type!r}")
    return automatic, user, errors


def next_action(run_dir: Path, requirements: dict[str, Any]) -> dict[str, Any]:
    check = information_check(requirements)
    status = check.get("status")
    payload = base_payload(run_dir, requirements, check)

    if requirements.get("status") == "approved" and status in {"satisfied", "not_required"}:
        review_errors = counterexample_review_errors(check)
        if review_errors:
            payload["blocking_reasons"] = review_errors
            return gate_payload(
                payload,
                ok=False,
                next_action="RunInformationCounterexampleReview",
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
        review_errors = counterexample_review_errors(check)
        if review_errors:
            payload["blocking_reasons"] = review_errors
            return gate_payload(
                payload,
                ok=False,
                next_action="RunInformationCounterexampleReview",
                review_prompt=review_prompt(check),
            )
        return gate_payload(
            payload,
            ok=True,
            next_action="ReadyForUserApproval",
            message="Information sufficiency is complete; show the requirements approval commitment.",
        )

    automatic, user, errors = classify_actions(check)
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
        if payload.get("message"):
            print(payload["message"])
        for reason in payload.get("blocking_reasons", []):
            print(f"ERROR: {reason}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
