#!/usr/bin/env python3
"""Check whether a requirements analysis brief is ready for pre-goal compilation.

This script performs deterministic structural checks only. It does not judge requirement semantics.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(errors="replace")


def has_complete_status(text: str) -> bool:
    patterns = [
        r"Requirements\s+Analysis\s+Status[^\n]*(Complete|`Complete`)",
        r"Clarification\s+Status[^\n]*(Complete|`Complete`)",
        r"Status\s*:\s*`?Complete`?",
        r"Requirements\s+analysis\s+is\s+complete",
        r"Clarification\s+is\s+complete",
        r"No\s+open\s+blocking\s+questions",
        r"No\s+open\s+questions",
        r"All\s+blocking\s+human\s+decisions[^\n]*(resolved|complete)",
    ]
    return any(re.search(p, text, re.IGNORECASE) for p in patterns)


def has_confirmed_decisions(text: str) -> bool:
    return (
        bool(re.search(r"##\s+Confirmed\s+Requirement\s+Decisions", text, re.IGNORECASE))
        or bool(re.search(r"##\s+Confirmed\s+Decisions", text, re.IGNORECASE))
        or "已确认" in text
    )


def has_open_questions(text: str) -> bool:
    if re.search(r"No\s+open\s+(blocking\s+)?questions", text, re.IGNORECASE):
        return False
    m = re.search(r"##\s+Questions\s+for\s+Human(?P<body>.*?)(?:\n##\s+|\Z)", text, re.IGNORECASE | re.DOTALL)
    if not m:
        return False
    body = m.group("body").strip()
    if not body:
        return False
    if re.search(r"No\s+open", body, re.IGNORECASE):
        return False
    return bool(re.search(r"(^|\n)\s*(\d+\.|[-*])\s+\S", body))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--requirements", dest="requirements", help="Path to requirements analysis brief")
    parser.add_argument("--clarification", dest="requirements", help="Deprecated alias for --requirements")
    args = parser.parse_args()

    if not args.requirements:
        parser.error("--requirements is required")

    path = Path(args.requirements)
    result: dict[str, Any] = {
        "path": str(path),
        "exists": path.exists(),
        "ok": False,
        "checks": {},
        "errors": [],
    }

    if not path.exists():
        result["errors"].append("requirements analysis file does not exist")
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 2

    text = read_text(path)
    complete = has_complete_status(text)
    confirmed = has_confirmed_decisions(text)
    open_questions = has_open_questions(text)

    result["checks"] = {
        "complete_status": complete,
        "confirmed_decisions_section": confirmed,
        "open_questions_detected": open_questions,
    }

    if not complete:
        result["errors"].append("requirements analysis is not marked complete")
    if open_questions:
        result["errors"].append("open human questions detected")
    if not confirmed:
        result["errors"].append("confirmed decisions section not detected")

    result["ok"] = not result["errors"]
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
