#!/usr/bin/env python3
"""Guard for compiling a runtime /goal from approved control artifacts.

This script checks phase-gate conditions. It does not decide product semantics.
"""
from __future__ import annotations

import argparse
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


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--clarification", required=True)
    ap.add_argument("--goal", required=True)
    ap.add_argument("--plan", required=True)
    ap.add_argument("--review", required=True)
    args = ap.parse_args()

    errors: list[str] = []
    try:
        clarification = read(args.clarification)
        goal = read(args.goal)
        plan = read(args.plan)
        review = read(args.review)
    except FileNotFoundError as e:
        errors.append(str(e))
        clarification = goal = plan = review = ""

    if clarification:
        clarification_status = section_status(clarification, "Clarification Status")
        if clarification_status != "Complete":
            errors.append(f"clarification status under ## Clarification Status is not Complete: {clarification_status!r}")

    if plan:
        plan_status = section_status(plan, "Execution Policy Status")
        if plan_status != "Candidate":
            errors.append(f"execution policy status under ## Execution Policy Status must be Candidate: {plan_status!r}")

    if review:
        review_status = section_status(review, "Review Status")
        if review_status != "Approved":
            errors.append(f"control review status under ## Review Status is not Approved: {review_status!r}")

    for path, text, label in [
        (args.clarification, goal, "goal"),
        (args.clarification, plan, "plan"),
        (args.goal, plan, "plan"),
        (args.clarification, review, "review"),
        (args.goal, review, "review"),
        (args.plan, review, "review"),
    ]:
        if text and path not in text:
            errors.append(f"{label} does not reference required path: {path}")

    forbidden = [
        "first write a plan",
        "first create a plan",
        "Start with $superpowers:writing-plans",
        "Start with `$superpowers:writing-plans`",
        "write an implementation plan and then execute",
    ]
    for phrase in forbidden:
        if phrase.lower() in goal.lower():
            errors.append(f"goal contains runtime control-structure synthesis phrase: {phrase}")

    if errors:
        print("FAIL")
        for e in errors:
            print(f"ERROR: {e}")
        return 2
    print("PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
