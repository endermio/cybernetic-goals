#!/usr/bin/env python3
"""Emit queue-friendly pre-goal handoff text from a requirements artifact.

This script predicts the orchestration command and the runtime goal contract
path. It does not compile the final runtime goal and does not approve
downstream artifacts.
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
}


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
    match = STATUS_LINE_RE.search(body)
    return canonical_status(match.group(1)) if match else None


def design_gate_required(text: str) -> bool:
    for line in text.splitlines():
        lowered = line.casefold()
        if "design gate" not in lowered:
            continue
        if re.search(r"not\s+required|not\s+applicable|satisfied", lowered):
            continue
        if "required" in lowered:
            return True
    return False


def derive_paths(requirements: Path) -> dict[str, str] | None:
    parts = requirements.as_posix().split("/")
    if len(parts) < 4:
        return None
    if parts[-3:-1] != ["cybernetics", "requirements"]:
        return None
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}-.+\.md", parts[-1]):
        return None

    slug = parts[-1]
    prefix = "/".join(parts[:-2])
    return {
        "requirements": requirements.as_posix(),
        "design": f"{prefix}/designs/{slug}",
        "goal": f"{prefix}/goals/{slug}",
        "plan": f"{prefix}/plans/{slug}",
        "review": f"{prefix}/control-reviews/{slug}",
        "runtime_contract": f"{prefix}/runtime-goals/{Path(slug).stem}.goal.md",
    }


def blocked(message: str) -> int:
    print("Pre-goal handoff prediction blocked.")
    print()
    print(f"Reason: {message}")
    print()
    print("Next: approve or revise the compact control commitment in the requirements analysis.")
    return 2


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--requirements", required=True)
    args = parser.parse_args()

    requirements_path = Path(args.requirements)
    if not requirements_path.exists():
        print(f"Pre-goal handoff prediction blocked.\n\nReason: missing file: {requirements_path}", file=sys.stderr)
        return 2

    text = requirements_path.read_text(encoding="utf-8")
    requirements_status = section_status(text, "Requirements Analysis Status")
    if requirements_status != "Complete":
        return blocked(f"requirements analysis status is not Complete: {requirements_status!r}")

    hsa_status = section_status(text, "Human Setpoint Approval")
    if hsa_status != "Approved":
        return blocked(f"Human Setpoint Approval is not Approved: {hsa_status!r}")

    paths = derive_paths(requirements_path)
    if paths is None:
        return blocked(
            "requirements path must look like docs/cybernetics/requirements/YYYY-MM-DD-slug.md"
        )

    design_required = design_gate_required(text)
    print("Response-only queue suggestions:")
    print()
    print("```text")
    print(f"$orchestrating-cybernetic-pregoal 根据 {paths['requirements']} 完成 pre-goal 编译，允许使用 subagents review。")
    print("```")
    print()
    if design_required:
        print("Design dispatch: when `Design Gate: required`, `$orchestrating-cybernetic-pregoal` must invoke or request `$designing-cybernetic-solutions` before goal writing.")
        print()
    print("Predicted downstream artifact paths:")
    print()
    print("```text")
    print(f"Requirements: {paths['requirements']}")
    if design_required:
        print(f"Design: {paths['design']}")
    else:
        print("Design: not required")
    print(f"Goal: {paths['goal']}")
    print(f"Execution policy: {paths['plan']}")
    print(f"Control review: {paths['review']}")
    print("```")
    print()
    print("Predicted runtime contract path:")
    print()
    print("```text")
    print(paths["runtime_contract"])
    print("```")
    print()
    print("Predicted pointer-only runtime command shape:")
    print()
    print("```text")
    print(
        f"/goal Execute the runtime goal contract at {paths['runtime_contract']}. "
        "Read it first and follow it exactly. "
        "If any referenced artifact is missing, not approved, or inconsistent, "
        "stop and report the smallest required human decision."
    )
    print("```")
    print()
    print("Predicted only: compile_runtime_goal.py must generate the final runtime contract and pointer command after approved downstream artifacts exist.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
