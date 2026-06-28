"""Shared requirements information-sufficiency validation."""
from __future__ import annotations

from pathlib import Path
from typing import Any


INFORMATION_SUFFICIENCY_GATE_POINTS = {
    "source_requirements->information_sufficiency_facts",
    "required_outcomes->information_sufficiency_facts",
    "information_sufficiency_facts->design_plan_entry",
}

FACT_STATUSES = {
    "satisfied",
    "missing",
    "needs_information_gathering",
    "needs_user_input",
    "needs_requirements_revision",
    "blocked",
    "not_required",
}

ACCEPTABLE_EVIDENCE_KINDS = {
    "direct_observation",
    "command_result",
    "source_code",
    "test_result",
    "documentation",
    "human_decision",
    "external_blocker",
}

REVIEWER_KINDS = {"subagent", "human", "external"}


def schema_version_at_least(requirements: dict[str, Any], minimum: str) -> bool:
    version = requirements.get("schema_version")
    if not isinstance(version, str):
        return False
    try:
        current_parts = tuple(int(part) for part in version.split("."))
        minimum_parts = tuple(int(part) for part in minimum.split("."))
    except ValueError:
        return False
    return current_parts >= minimum_parts


def string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, str) and item]


def evidence_ref_errors(run_dir: Path, label: str, evidence_ref: Any) -> list[str]:
    return evidence_ref_path_errors(run_dir, label, evidence_ref, require_exists=True)


def evidence_ref_path_errors(
    run_dir: Path,
    label: str,
    evidence_ref: Any,
    *,
    require_exists: bool,
) -> list[str]:
    if not isinstance(evidence_ref, str) or not evidence_ref.strip():
        return [f"{label} evidence_ref must be non-empty"]
    path_part = evidence_ref.split("#", 1)[0]
    if not path_part:
        return [f"{label} evidence_ref must name a file before any JSON pointer fragment"]
    ref_path = Path(path_part)
    if ref_path.is_absolute():
        return [f"{label} evidence_ref must be relative to the run directory"]
    resolved_run_dir = run_dir.resolve()
    resolved_ref = (run_dir / ref_path).resolve()
    try:
        resolved_ref.relative_to(resolved_run_dir)
    except ValueError:
        return [f"{label} evidence_ref must stay inside the run directory"]
    if require_exists and not resolved_ref.exists():
        return [f"{label} evidence_ref does not exist: {evidence_ref}"]
    if require_exists and not resolved_ref.is_file():
        return [f"{label} evidence_ref must point to a file: {evidence_ref}"]
    return []


def acceptable_evidence_errors(label: str, value: Any) -> list[str]:
    if not isinstance(value, list) or not value:
        return [f"{label} acceptable_evidence must be a non-empty list"]
    errors: list[str] = []
    for index, evidence in enumerate(value):
        item_label = f"{label} acceptable_evidence[{index}]"
        if not isinstance(evidence, dict):
            errors.append(f"{item_label} must be an object")
            continue
        if evidence.get("kind") not in ACCEPTABLE_EVIDENCE_KINDS:
            errors.append(f"{item_label} kind is not recognized")
        if not isinstance(evidence.get("description"), str) or not evidence["description"].strip():
            errors.append(f"{item_label} description must be non-empty")
    return errors


def information_sufficiency_errors(requirements: dict[str, Any], run_dir: Path) -> list[str]:
    approved = requirements.get("approved_control")
    if not isinstance(approved, dict):
        return ["requirements.control.json approved_control must be an object"]
    check = approved.get("information_sufficiency_check")
    if not schema_version_at_least(requirements, "1.2.0"):
        if isinstance(check, dict):
            return [
                "requirements.control.json approved_control.information_sufficiency_check "
                "requires schema_version >= 1.2.0"
            ]
        return []
    if not isinstance(check, dict):
        return [
            "requirements.control.json approved_control.information_sufficiency_check "
            "is required for schema_version >= 1.2.0"
        ]

    errors: list[str] = []
    if check.get("status") not in {"satisfied", "not_required"}:
        errors.append(
            f"information_sufficiency_check status must be satisfied before handoff, got {check.get('status')!r}"
        )

    approved_sources = {
        item.get("id")
        for item in approved.get("source_requirements", [])
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }
    approved_outcomes = {
        item.get("id")
        for item in approved.get("required_outcomes", [])
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }
    facts = check.get("facts")
    if not isinstance(facts, list) or not facts:
        errors.append("information_sufficiency_check facts must be a non-empty list")
        facts = []

    blocking_fact_ids: set[str] = set()
    all_fact_ids: set[str] = set()
    for index, fact in enumerate(facts):
        if not isinstance(fact, dict):
            errors.append(f"information_sufficiency_check facts[{index}] must be an object")
            continue
        fact_id = fact.get("fact_id")
        label = f"information_sufficiency_check fact {fact_id or index}"
        if not isinstance(fact_id, str) or not fact_id:
            errors.append(f"{label} must have fact_id")
            continue
        all_fact_ids.add(fact_id)
        if not isinstance(fact.get("statement"), str) or not fact["statement"].strip():
            errors.append(f"{label} statement must be non-empty")
        derived_from = fact.get("derived_from")
        if not isinstance(derived_from, dict):
            errors.append(f"{label} derived_from must be an object")
            continue
        if not isinstance(derived_from.get("source_requirements"), list):
            errors.append(f"{label} derived_from.source_requirements must be a list")
        if not isinstance(derived_from.get("required_outcomes"), list):
            errors.append(f"{label} derived_from.required_outcomes must be a list")
        fact_sources = set(string_list(derived_from.get("source_requirements")))
        fact_outcomes = set(string_list(derived_from.get("required_outcomes")))
        if not fact_sources and not fact_outcomes:
            errors.append(f"{label} derived_from must reference source_requirements or required_outcomes")
        unknown_sources = sorted(fact_sources - approved_sources)
        if unknown_sources:
            errors.append(f"{label} references unknown source_requirements: {', '.join(unknown_sources)}")
        unknown_outcomes = sorted(fact_outcomes - approved_outcomes)
        if unknown_outcomes:
            errors.append(f"{label} references unknown required_outcomes: {', '.join(unknown_outcomes)}")
        if fact.get("current_status") not in FACT_STATUSES:
            errors.append(f"{label} current_status is not recognized")
        blocks_design = fact.get("blocks_design_or_plan_if_missing")
        if not isinstance(blocks_design, bool):
            errors.append(f"{label} blocks_design_or_plan_if_missing must be boolean")
        if blocks_design is True:
            blocking_fact_ids.add(fact_id)
            if fact.get("current_status") != "satisfied":
                errors.append(f"{label} is not satisfied and blocks handoff")
        if not isinstance(fact.get("why_needed"), str) or not fact["why_needed"].strip():
            errors.append(f"{label} why_needed must explain why design/plan needs this fact")
        errors.extend(acceptable_evidence_errors(label, fact.get("acceptable_evidence")))
        errors.extend(evidence_ref_errors(run_dir, label, fact.get("evidence_ref")))

    review = check.get("counterexample_review")
    if not isinstance(review, dict):
        errors.append("information_sufficiency_check counterexample_review must be an object")
        return errors
    if review.get("status") != "pass" or review.get("verdict") != "approved":
        errors.append("information_sufficiency_check counterexample_review must pass with verdict approved")
    reviewer = review.get("reviewer")
    if not isinstance(reviewer, dict):
        errors.append("information_sufficiency_check counterexample_review reviewer must be an object")
    elif reviewer.get("kind") not in REVIEWER_KINDS:
        errors.append("information_sufficiency_check counterexample_review reviewer kind is not recognized")
    elif not isinstance(reviewer.get("id"), str) or not reviewer["id"].strip():
        errors.append("information_sufficiency_check counterexample_review reviewer must have kind, id, and evidence_ref")
    elif not isinstance(reviewer.get("evidence_ref"), str) or not reviewer["evidence_ref"].strip():
        errors.append("information_sufficiency_check counterexample_review reviewer must have kind, id, and evidence_ref")
    else:
        errors.extend(
            evidence_ref_errors(
                run_dir,
                "information_sufficiency_check counterexample_review reviewer",
                reviewer.get("evidence_ref"),
            )
        )
    checked_facts = set(string_list(review.get("checked_facts")))
    if not isinstance(review.get("checked_facts"), list) or not checked_facts:
        errors.append("information_sufficiency_check counterexample_review checked_facts must be a non-empty list")
    missing_checked_facts = sorted(blocking_fact_ids - checked_facts)
    if missing_checked_facts:
        errors.append(
            "information_sufficiency_check counterexample_review missing checked_facts: "
            + ", ".join(missing_checked_facts)
        )
    checked_transformations = set(string_list(review.get("checked_transformations")))
    if not isinstance(review.get("checked_transformations"), list) or not checked_transformations:
        errors.append("information_sufficiency_check counterexample_review checked_transformations must be a non-empty list")
    missing_points = sorted(INFORMATION_SUFFICIENCY_GATE_POINTS - checked_transformations)
    if missing_points:
        errors.append(
            "information_sufficiency_check counterexample_review missing checked_transformations: "
            + ", ".join(missing_points)
        )
    unknown_checked_facts = sorted(checked_facts - all_fact_ids)
    if unknown_checked_facts:
        errors.append(
            "information_sufficiency_check counterexample_review references unknown facts: "
            + ", ".join(unknown_checked_facts)
        )
    findings = review.get("findings")
    if not isinstance(findings, list):
        errors.append("information_sufficiency_check counterexample_review findings must be a list")
    elif any(not isinstance(finding, str) for finding in findings):
        errors.append("information_sufficiency_check counterexample_review findings must contain only strings")
    return errors
