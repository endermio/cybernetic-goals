"""Shared transition-gate result helpers.

Transition gates do not execute the workflow. They describe whether the current
stage may advance, what action must happen next, and whether the agent must run
the gate again after that action.
"""
from __future__ import annotations

from typing import Any


PROTOCOL = "transition-gate/v1"

TERMINAL_ACTIONS = {
    "AwaitAmendmentProposal",
    "ReadyForUserApproval",
    "ReadyForPreGoalHandoff",
    "RequirementsInformationBlocked",
    "Blocked",
    "HumanApprovalRequired",
    "ContinueCurrentGeneration",
}

APPROVAL_ACTIONS = {"ReadyForUserApproval"}
HANDOFF_ACTIONS = {"ReadyForPreGoalHandoff", "ContinueCurrentGeneration"}
USER_ACTIONS = {"AskUserForInformation", "ReadyForUserApproval", "HumanApprovalRequired"}
INDEPENDENT_REVIEW_ACTIONS = {"RunReview", "RunInformationCounterexampleReview"}


def transition_gate_payload(
    *,
    ok: bool,
    gate_id: str,
    next_action: str,
    errors: list[str] | None = None,
    state: str | None = None,
    legacy_next_allowed_action: bool = False,
    **fields: Any,
) -> dict[str, Any]:
    terminal = bool(ok) or next_action in TERMINAL_ACTIONS
    user_action_required = next_action in USER_ACTIONS
    payload: dict[str, Any] = {
        "gate_protocol": PROTOCOL,
        "gate_id": gate_id,
        "ok": ok,
        "state": state,
        "next_action": next_action,
        "terminal": terminal,
        "rerun_required": not terminal,
        "approval_allowed": next_action in APPROVAL_ACTIONS,
        "handoff_allowed": next_action in HANDOFF_ACTIONS or (ok and next_action not in APPROVAL_ACTIONS),
        "may_ask_user": user_action_required,
        "user_action_required": user_action_required,
        "agent_must_continue": not terminal and not user_action_required,
        "requires_independent_review": next_action in INDEPENDENT_REVIEW_ACTIONS,
        "errors": errors or [],
        "warnings": [],
    }
    if legacy_next_allowed_action:
        payload["next_allowed_action"] = next_action
    payload.update(fields)
    if payload["state"] is None:
        payload.pop("state")
    return payload
