#!/usr/bin/env python3
"""Emit queue-friendly pre-goal handoff text from a requirements artifact.

This script predicts the orchestration command and the runtime goal file
path. It does not compile the final runtime goal and does not approve
downstream artifacts.
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


def design_check_required(text: str) -> bool:
    for line in text.splitlines():
        lowered = line.casefold()
        if "design check" not in lowered:
            continue
        if re.search(r"not\s+required|not\s+applicable|satisfied", lowered):
            continue
        if "required" in lowered:
            return True
    return False


def table_field_value(section: str, field: str) -> str | None:
    for line in section.splitlines():
        stripped = line.strip()
        if "|" not in stripped:
            continue
        if re.fullmatch(r"\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)+\|?", stripped):
            continue
        cells = [cell.strip().strip("`") for cell in stripped.strip("|").split("|")]
        if len(cells) >= 2 and field.casefold() in cells[0].casefold() and cells[1]:
            return cells[1]
    return None


def answer_method_sidecar_required(text: str) -> bool:
    body = section_body(text, "What the User Approved")
    if body is None:
        return False
    return bool(table_field_value(body, "How this should be answered") or table_field_value(body, "What is not enough"))


def check_requirements_control_sidecar(requirements_path: Path, text: str) -> str | None:
    if not answer_method_sidecar_required(text):
        return None
    control_path = requirements_path.with_suffix(".control.json")
    try:
        value = json.loads(control_path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return f"requirements control sidecar missing: {control_path}"
    except json.JSONDecodeError as exc:
        return f"requirements control sidecar invalid JSON: {control_path}: {exc}"
    if not isinstance(value, dict):
        return f"requirements control sidecar must be a JSON object: {control_path}"
    if not isinstance(value.get("answer_method_key"), str) or not value["answer_method_key"].strip():
        return "requirements control sidecar missing answer_method_key"
    body = section_body(text, "What the User Approved") or ""
    if table_field_value(body, "What is not enough"):
        if not isinstance(value.get("forbidden_substitute_key"), str) or not value["forbidden_substitute_key"].strip():
            return "requirements control sidecar missing forbidden_substitute_key"
    return None


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

    hsa_status = section_status(text, "What the User Approved")
    if hsa_status != "Approved":
        return blocked(f"What the User Approved is not Approved: {hsa_status!r}")

    sidecar_error = check_requirements_control_sidecar(requirements_path, text)
    if sidecar_error:
        return blocked(sidecar_error)

    paths = derive_paths(requirements_path)
    if paths is None:
        return blocked(
            "requirements path must look like docs/cybernetics/requirements/YYYY-MM-DD-slug.md"
        )

    design_required = design_check_required(text)
    print("Response-only queue suggestions:")
    print()
    print("```text")
    print(f"$orchestrating-cybernetic-pregoal 根据 {paths['requirements']} 完成 pre-goal 编译，允许使用 subagents review。")
    print("```")
    print()
    if design_required:
        print("Design dispatch: when `design check: required`, `$orchestrating-cybernetic-pregoal` must invoke or request `$designing-cybernetic-solutions` before goal writing.")
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
    print(f"Review: {paths['review']}")
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
        f"/goal Execute the runtime goal file at {paths['runtime_contract']}. "
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
