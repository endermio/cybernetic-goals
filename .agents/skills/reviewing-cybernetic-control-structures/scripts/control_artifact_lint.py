#!/usr/bin/env python3
"""Deterministic structural lint for cybernetic control artifacts.

This script checks file existence, required sections, statuses, and cross-references.
It does not decide product semantics.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


def read(path: str) -> str:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"missing file: {path}")
    return p.read_text(encoding="utf-8")


def has_section(text: str, section: str) -> bool:
    pat = re.compile(rf"^##\s+{re.escape(section)}\s*$", re.MULTILINE)
    return bool(pat.search(text))


def status_value(text: str, label: str) -> str | None:
    # Matches: Status: `Complete` or Status: Complete
    m = re.search(rf"{re.escape(label)}\s*:\s*`?([A-Za-z ]+)`?", text)
    return m.group(1).strip() if m else None


def check_required_sections(name: str, text: str, sections: list[str], errors: list[str]) -> None:
    for sec in sections:
        if not has_section(text, sec):
            errors.append(f"{name}: missing section ## {sec}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--clarification", required=True)
    ap.add_argument("--goal", required=True)
    ap.add_argument("--plan", required=True)
    ap.add_argument("--review", required=False)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    errors: list[str] = []
    warnings: list[str] = []

    try:
        clarification = read(args.clarification)
        goal = read(args.goal)
        plan = read(args.plan)
        review = read(args.review) if args.review else None
    except FileNotFoundError as e:
        errors.append(str(e))
        clarification = goal = plan = ""
        review = None

    if clarification:
        check_required_sections("clarification", clarification, [
            "Clarification Status", "Human Purpose", "Current Understanding",
            "Confirmed Decisions From Human", "Non-Goals", "Draft Verification Strategy"
        ], errors)
        st = status_value(clarification, "Status")
        if st != "Complete":
            errors.append(f"clarification: Status must be Complete, got {st!r}")

    if goal:
        check_required_sections("goal", goal, [
            "Human Purpose", "Objective", "Success Condition", "Source of Truth",
            "Scope and Boundaries", "Invariants", "Verification Surface",
            "Stop Conditions", "Blocked Report Format", "Final Report Format"
        ], errors)
        if args.clarification not in goal:
            warnings.append("goal: does not reference clarification path literally")
        forbidden_runtime_plan_phrases = [
            "first write a plan, then implement",
            "Start with `$superpowers:writing-plans`",
            "Start with $superpowers:writing-plans",
            "first write an implementation plan, then execute",
        ]
        for phrase in forbidden_runtime_plan_phrases:
            if phrase.lower() in goal.lower():
                errors.append(f"goal: contains runtime plan-synthesis phrase: {phrase}")

    if plan:
        check_required_sections("plan", plan, [
            "Execution Policy Status", "Source Contracts", "Confirmed Semantic Invariants",
            "Tactical Degrees of Freedom", "Dependency Matrix", "Batch Cadence",
            "Destructive Intermediate-State Policy", "Sensor / Test Governance",
            "Old Test Retirement and Rewrite Policy", "Phase Gates", "Execution Rhythm",
            "Stop Conditions", "Progress Log Rules"
        ], errors)
        st = status_value(plan, "Status")
        if st not in {"Candidate", "Approved"}:
            warnings.append(f"plan: expected Status Candidate or Approved, got {st!r}")
        if args.clarification not in plan:
            warnings.append("plan: does not reference clarification path literally")
        if args.goal not in plan:
            warnings.append("plan: does not reference goal path literally")

    if review:
        check_required_sections("review", review, [
            "Review Status", "Inputs Reviewed", "Requirement Traceability",
            "Goal Fidelity", "Control Law Quality", "Sensor / Test Governance",
            "Batch Rhythm", "Runtime Suitability", "Final Decision"
        ], errors)
        st = status_value(review, "Status")
        if st != "Approved":
            errors.append(f"review: Status must be Approved for runtime compilation, got {st!r}")
        for path, label in [(args.clarification, "clarification"), (args.goal, "goal"), (args.plan, "plan")]:
            if path not in review:
                warnings.append(f"review: does not reference {label} path literally")

    result = {"ok": not errors, "errors": errors, "warnings": warnings}
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        if errors:
            print("FAIL")
            for e in errors:
                print(f"ERROR: {e}")
        else:
            print("PASS")
        for w in warnings:
            print(f"WARN: {w}")
    return 0 if not errors else 2


if __name__ == "__main__":
    raise SystemExit(main())
