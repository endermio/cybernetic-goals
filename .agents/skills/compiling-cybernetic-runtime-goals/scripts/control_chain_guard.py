#!/usr/bin/env python3
"""Guard for compiling a runtime /goal from approved control artifacts.

This script checks phase-gate conditions. It does not decide product semantics.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


def read(path: str) -> str:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"missing file: {path}")
    return p.read_text(encoding="utf-8")


def status(text: str) -> str | None:
    m = re.search(r"Status\s*:\s*`?([A-Za-z ]+)`?", text)
    return m.group(1).strip() if m else None


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

    if clarification and status(clarification) != "Complete":
        errors.append("clarification status is not Complete")
    if review and status(review) != "Approved":
        errors.append("control review status is not Approved")

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
