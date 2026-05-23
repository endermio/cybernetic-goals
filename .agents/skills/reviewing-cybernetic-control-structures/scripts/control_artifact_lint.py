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


HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$", re.MULTILINE)
STATUS_LINE_RE = re.compile(r"(?im)^\s*Status\s*:\s*`?([^`\n]+?)`?\s*$")

STATUS_ALIASES = {
    "complete": "Complete",
    "completed": "Complete",
    "完成": "Complete",
    "已完成": "Complete",
    "approved": "Approved",
    "批准": "Approved",
    "已批准": "Approved",
    "candidate": "Candidate",
    "候选": "Candidate",
    "候选状态": "Candidate",
}


def read(path: str) -> str:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"missing file: {path}")
    return p.read_text(encoding="utf-8")


def has_section(text: str, section: str) -> bool:
    pat = re.compile(rf"^##\s+{re.escape(section)}\s*$", re.MULTILINE)
    return bool(pat.search(text))


def canonical_status(value: str) -> str:
    status = value.strip().strip("`").strip()
    return STATUS_ALIASES.get(status.casefold(), status)


def section_body(text: str, heading: str) -> str | None:
    target = heading.casefold()
    for match in HEADING_RE.finditer(text):
        title = match.group(2).strip().rstrip("#").strip()
        if title.casefold() != target:
            continue

        level = len(match.group(1))
        start = match.end()
        end = len(text)
        for next_match in HEADING_RE.finditer(text, start):
            if len(next_match.group(1)) <= level:
                end = next_match.start()
                break
        return text[start:end]
    return None


def section_status(text: str, heading: str) -> str | None:
    body = section_body(text, heading)
    if body is None:
        return None
    m = STATUS_LINE_RE.search(body)
    return canonical_status(m.group(1)) if m else None


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
        st = section_status(clarification, "Clarification Status")
        if st != "Complete":
            errors.append(f"clarification: Status under ## Clarification Status must be Complete, got {st!r}")

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
            "Execution Policy Status", "Source Contracts", "Superpowers Planning Substrate",
            "Confirmed Semantic Invariants", "Tactical Degrees of Freedom", "Dependency Matrix", "Batch Cadence",
            "Destructive Intermediate-State Policy", "Sensor / Test Governance",
            "Old Test Retirement and Rewrite Policy", "Phase Gates", "Execution Rhythm",
            "Stop Conditions", "Progress Log Rules"
        ], errors)
        st = section_status(plan, "Execution Policy Status")
        if st not in {"Candidate", "Approved"}:
            warnings.append(f"plan: expected Status under ## Execution Policy Status to be Candidate or Approved, got {st!r}")
        if args.clarification not in plan:
            warnings.append("plan: does not reference clarification path literally")
        if args.goal not in plan:
            warnings.append("plan: does not reference goal path literally")

    if review:
        check_required_sections("review", review, [
            "Review Status", "Inputs Reviewed", "Review Independence", "Requirement Traceability",
            "Goal Fidelity", "Control Law Quality", "Sensor / Test Governance",
            "Batch Rhythm", "Runtime Suitability", "Final Decision"
        ], errors)
        st = section_status(review, "Review Status")
        if st != "Approved":
            errors.append(f"review: Status under ## Review Status must be Approved for runtime compilation, got {st!r}")
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
