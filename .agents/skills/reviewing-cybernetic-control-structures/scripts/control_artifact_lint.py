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
    "reviewed": "Reviewed",
    "已审查": "Reviewed",
}


def read(path: str) -> str:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"missing file: {path}")
    return p.read_text(encoding="utf-8")


def has_section(text: str, section: str) -> bool:
    pat = re.compile(rf"^##\s+{re.escape(section)}\s*$", re.MULTILINE)
    return bool(pat.search(text))


def has_any_section(text: str, sections: list[str]) -> bool:
    return any(has_section(text, section) for section in sections)


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


def first_section_status(text: str, *headings: str) -> str | None:
    for heading in headings:
        status = section_status(text, heading)
        if status is not None:
            return status
    return None


def design_gate_required(*texts: str) -> bool:
    combined = "\n".join(texts)
    for line in combined.splitlines():
        lowered = line.casefold()
        if "design gate" not in lowered:
            continue
        if re.search(r"not\s+required|not\s+applicable|satisfied", lowered):
            continue
        if "required" in lowered:
            return True
    return False


def check_required_sections(name: str, text: str, sections: list[str], errors: list[str]) -> None:
    for sec in sections:
        if not has_section(text, sec):
            errors.append(f"{name}: missing section ## {sec}")


def check_required_section_groups(name: str, text: str, groups: list[tuple[str, list[str]]], errors: list[str]) -> None:
    for label, sections in groups:
        if not has_any_section(text, sections):
            errors.append(f"{name}: missing section ## {label}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--requirements", dest="requirements")
    ap.add_argument("--clarification", dest="requirements", help="Deprecated alias for --requirements")
    ap.add_argument("--design", required=False)
    ap.add_argument("--goal", required=True)
    ap.add_argument("--plan", required=True)
    ap.add_argument("--review", required=False)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    if not args.requirements:
        ap.error("--requirements is required")

    errors: list[str] = []
    warnings: list[str] = []

    try:
        requirements = read(args.requirements)
        design = read(args.design) if args.design else None
        goal = read(args.goal)
        plan = read(args.plan)
        review = read(args.review) if args.review else None
    except FileNotFoundError as e:
        errors.append(str(e))
        requirements = goal = plan = ""
        design = None
        review = None

    if requirements:
        check_required_section_groups("requirements", requirements, [
            ("Requirements Analysis Status", ["Requirements Analysis Status", "Clarification Status"]),
            ("Human Purpose", ["Human Purpose"]),
            ("Current Understanding", ["Current Understanding"]),
            ("Confirmed Requirement Decisions", ["Confirmed Requirement Decisions", "Confirmed Decisions From Human"]),
            ("Non-Goals", ["Non-Goals"]),
            ("Draft Verification Strategy", ["Draft Verification Strategy"]),
        ], errors)
        st = first_section_status(requirements, "Requirements Analysis Status", "Clarification Status")
        if st != "Complete":
            errors.append(f"requirements: status must be Complete, got {st!r}")

    if design:
        check_required_sections("design", design, [
            "Design Status", "Source Contracts", "Human Purpose", "Confirmed Semantics",
            "Design Substrate", "Conceptual Design", "Detailed Design",
            "Design-to-Goal Mapping", "Design-to-Execution Mapping",
            "Open Design Questions", "Design Review Requirements", "Next Step"
        ], errors)
        st = section_status(design, "Design Status")
        if st not in {"Candidate", "Reviewed", "Approved"}:
            warnings.append(f"design: expected Status under ## Design Status to be Candidate, Reviewed, or Approved, got {st!r}")
        if args.requirements not in design:
            warnings.append("design: does not reference requirements path literally")
    elif design_gate_required(requirements, goal, plan, review or ""):
        errors.append("design: Design Gate required but --design was not provided")

    if goal:
        check_required_sections("goal", goal, [
            "Human Purpose", "Objective", "Success Condition", "Source of Truth",
            "Scope and Boundaries", "Invariants", "Verification Surface",
            "Stop Conditions", "Blocked Report Format", "Final Report Format"
        ], errors)
        if args.requirements not in goal:
            warnings.append("goal: does not reference requirements path literally")
        if args.design and args.design not in goal:
            warnings.append("goal: does not reference design path literally")
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
        if args.requirements not in plan:
            warnings.append("plan: does not reference requirements path literally")
        if args.goal not in plan:
            warnings.append("plan: does not reference goal path literally")
        if args.design and args.design not in plan:
            warnings.append("plan: does not reference design path literally")

    if review:
        check_required_sections("review", review, [
            "Review Status", "Inputs Reviewed", "Review Independence", "Final Observer Check",
            "Requirement Traceability", "Goal Fidelity", "Design Fidelity", "Control Law Quality", "Sensor / Test Governance",
            "Batch Rhythm", "Runtime Suitability", "Final Decision"
        ], errors)
        st = section_status(review, "Review Status")
        if st != "Approved":
            errors.append(f"review: Status under ## Review Status must be Approved for runtime compilation, got {st!r}")
        for path, label in [(args.requirements, "requirements"), (args.design, "design"), (args.goal, "goal"), (args.plan, "plan")]:
            if not path:
                continue
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
