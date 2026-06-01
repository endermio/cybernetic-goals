#!/usr/bin/env python3
"""Guard pre-goal orchestration stage transitions.

This script checks artifact existence, statuses, source-contract references, and
stage ordering. It does not decide requirement semantics or synthesize artifacts.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$", re.MULTILINE)
STATUS_LINE_RE = re.compile(r"(?im)^\s*Status\s*:\s*`?([^`\n]+?)`?\s*$")
YES_NO_LINE_RE = re.compile(r"(?im)^\s*-\s*{label}\s*:\s*`?([^`\n]+?)`?\s*$")

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

NEXT_ACTION = {
    "before-design": "RunDesign",
    "before-goal": "RunGoalWriting",
    "before-policy": "RunExecutionPolicy",
    "before-review": "RunReview",
    "before-runtime-compile": "RunRuntimeCompile",
}


def blocked_next_action(errors: list[str]) -> str:
    """Return the next corrective orchestration action for a blocked transition."""
    joined = "\n".join(errors).casefold()
    if "$designing-cybernetic-solutions is unavailable" in joined:
        return "Blocked"
    if "design artifact is missing" in joined:
        return "RunDesign"
    if "design status" in joined or "design does not reference" in joined or "design has blocking" in joined:
        return "RunDesign"
    if "output contract gate" in joined and "design lacks" in joined:
        return "RunDesign"
    if "output contract gate" in joined and "goal lacks" in joined:
        return "RunGoalWriting"
    if "output contract is required" in joined and "goal lacks" in joined:
        return "RunGoalWriting"
    if "goal contract is required" in joined or "goal does not reference" in joined:
        return "RunGoalWriting"
    if "execution policy is required" in joined or "execution policy status" in joined or "execution topology" in joined or "plan does not reference" in joined:
        return "RunExecutionPolicy"
    if (
        "control review" in joined
        or "final observer" in joined
        or "review does not reference" in joined
        or "post-review" in joined
    ):
        return "RunReview"
    return "Blocked"


def ok_next_action(state: str, requirements: str | None, design_path: str | None) -> str:
    if state == "before-design":
        if design_gate_required(requirements) and not design_path:
            return "RunDesign"
        return "RunGoalWriting"
    return NEXT_ACTION[state]


def read(path: str | None) -> str | None:
    if not path:
        return None
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
    match = STATUS_LINE_RE.search(body)
    return canonical_status(match.group(1)) if match else None


def first_section_status(text: str, *headings: str) -> str | None:
    for heading in headings:
        status = section_status(text, heading)
        if status is not None:
            return status
    return None


def design_gate_required(*texts: str | None) -> bool:
    combined = "\n".join(text for text in texts if text)
    for line in combined.splitlines():
        lowered = line.casefold()
        if "design gate" not in lowered:
            continue
        if re.search(r"not\s+required|not\s+applicable|satisfied", lowered):
            continue
        if "required" in lowered:
            return True
    return False


def output_contract_gate_required(*texts: str | None) -> bool:
    combined = "\n".join(text for text in texts if text)
    for line in combined.splitlines():
        lowered = line.casefold()
        if "output contract gate" not in lowered:
            continue
        if re.search(r"not\s+required|not\s+applicable|satisfied", lowered):
            continue
        if "required" in lowered:
            return True
    return False


def meaningful_line(line: str) -> bool:
    text = line.strip().strip("`")
    if not text:
        return False
    if text.startswith("-"):
        text = text[1:].strip()
    lowered = text.casefold()
    if lowered.startswith(("use when ", "otherwise record", "runtime must not substitute", "if this contract is insufficient")):
        return False
    if re.fullmatch(r"\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)+\|?", text):
        return False
    if "|" in text and "element" in lowered and ("requirement" in lowered or "design" in lowered):
        return False
    if text.startswith("[") and text.endswith("]"):
        return False
    if "[" in text and "]" in text:
        return False
    if lowered in {"none", "no open questions", "no open design questions", "n/a", "not applicable", "无", "无。", "none."}:
        return False
    return True


def has_section(text: str | None, heading: str) -> bool:
    return bool(text and section_body(text, heading) is not None)


def section_has_meaningful_content(text: str | None, heading: str) -> bool:
    if not text:
        return False
    body = section_body(text, heading)
    if body is None:
        return False
    return any(meaningful_line(line) for line in body.splitlines())


def output_contract_present_upstream(requirements: str | None = None, design: str | None = None, goal: str | None = None) -> bool:
    return (
        section_has_meaningful_content(requirements, "Output Contract")
        or section_has_meaningful_content(design, "Output Contract Design")
        or section_has_meaningful_content(goal, "Final Output Contract")
    )


def output_contract_required(requirements: str | None, design: str | None, goal: str | None) -> bool:
    return output_contract_gate_required(requirements, design, goal) or output_contract_present_upstream(requirements, design, goal)


def selected_execution_topology(plan: str | None) -> str | None:
    if not plan:
        return None
    body = section_body(plan, "Context Management / Execution Topology")
    if body is None:
        return None
    match = re.search(r"(?im)^\s*Selected topology\s*:\s*`?([^`\n]+?)`?\s*$", body)
    if not match:
        return None
    value = match.group(1).strip().strip("`")
    lowered = value.casefold()
    if "/" in value:
        return None
    if "main-only" in lowered or "main only" in lowered:
        return "Main-only"
    if "serial" in lowered and "subagent" in lowered:
        return "Serial subagent-driven"
    if "parallel" in lowered and "subagent" in lowered:
        return "Parallel subagent-driven"
    return None


def labeled_block_has_content(text: str, label: str) -> bool:
    lines = text.splitlines()
    pattern = re.compile(rf"^\s*{re.escape(label)}\s*:\s*(.*?)\s*$", re.IGNORECASE)
    for index, line in enumerate(lines):
        match = pattern.match(line)
        if not match:
            continue
        if meaningful_line(match.group(1)):
            return True
        for following in lines[index + 1 :]:
            stripped = following.strip()
            if not stripped:
                continue
            if re.match(r"^[A-Za-z][A-Za-z0-9 /-]+:\s*$", stripped):
                break
            if meaningful_line(stripped):
                return True
        return False
    return False


def has_meaningful_delegation_matrix(body: str) -> bool:
    lowered = body.casefold()
    required_columns = [
        "work package",
        "executor",
        "context pack",
        "allowed actions",
        "return format",
        "integration gate",
    ]
    if not all(column in lowered for column in required_columns):
        return False

    for line in body.splitlines():
        stripped = line.strip()
        if "|" not in stripped:
            continue
        if re.fullmatch(r"\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)+\|?", stripped):
            continue
        row_lowered = stripped.casefold()
        if all(column in row_lowered for column in required_columns):
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if len(cells) >= len(required_columns) and all(meaningful_line(cell) for cell in cells):
            return True
    return False


def check_execution_topology(plan: str | None, errors: list[str]) -> None:
    body = section_body(plan or "", "Context Management / Execution Topology")
    if body is None:
        errors.append("execution policy missing ## Context Management / Execution Topology")
        return

    topology = selected_execution_topology(plan)
    if topology is None:
        errors.append("execution policy is required to define a selected Context Management / Execution Topology")
        return

    if not labeled_block_has_content(body, "Topology rationale"):
        errors.append("execution topology missing Topology rationale")
    if not labeled_block_has_content(body, "Main agent owns"):
        errors.append("execution topology missing main-agent ownership")

    if topology in {"Serial subagent-driven", "Parallel subagent-driven"}:
        if not has_meaningful_delegation_matrix(body):
            errors.append("execution topology missing meaningful delegation matrix with Context pack, Allowed actions, Return format, and Integration gate")
        if "subagent-driven-development" not in body.casefold() and "runtime target-work delegation" not in body.casefold():
            errors.append("subagent-driven topology missing $superpowers:subagent-driven-development or equivalent delegation substrate")

    if topology == "Parallel subagent-driven":
        for label in ("Human approval", "Dependency independence", "Control-review approval"):
            if not labeled_block_has_content(body, label):
                errors.append(f"parallel execution topology missing {label}")


def has_blocking_design_questions(design: str) -> bool:
    body = section_body(design, "Open Design Questions")
    if body is None:
        return True
    return any(meaningful_line(line) for line in body.splitlines())


def require_reference(text: str | None, path: str | None, label: str, errors: list[str]) -> None:
    if not path or not text:
        return
    if path not in text:
        errors.append(f"{label} does not reference required path: {path}")


def yes_no_value(text: str, label: str) -> str | None:
    pattern = re.compile(YES_NO_LINE_RE.pattern.format(label=re.escape(label)), YES_NO_LINE_RE.flags)
    match = pattern.search(text)
    if not match:
        return None
    value = match.group(1).strip().casefold()
    if value in {"yes", "y", "true", "是"}:
        return "yes"
    if value in {"no", "n", "false", "否"}:
        return "no"
    return value


def bullet_has_content(text: str, label: str) -> bool:
    pattern = re.compile(rf"(?im)^\s*-\s*{re.escape(label)}\s*:\s*(.+?)\s*$")
    match = pattern.search(text)
    if match and meaningful_line(match.group(1)):
        return True

    block_pattern = re.compile(rf"(?ims)^\s*-\s*{re.escape(label)}\s*:\s*$\n(?P<body>.*?)(?=^-\s*\S|\Z)")
    block = block_pattern.search(text)
    if not block:
        return False
    return any(meaningful_line(line) for line in block.group("body").splitlines())


def check_final_observer(review: str, errors: list[str]) -> None:
    body = section_body(review, "Final Observer Check")
    if body is None:
        errors.append("control review missing ## Final Observer Check")
        return

    approval_allowed = yes_no_value(body, "Approval allowed after final observer check")
    if approval_allowed != "yes":
        errors.append(f"final observer check does not allow approval: {approval_allowed!r}")

    substantive_changes = yes_no_value(body, "Substantive artifact changes after last independent review")
    final_re_review = yes_no_value(body, "If yes, final re-review performed")
    if substantive_changes == "yes":
        if final_re_review != "yes":
            errors.append("substantive post-review changes require final re-review")
        if not bullet_has_content(body, "Final reviewers confirming no Blocking/Major findings"):
            errors.append("final observer check lacks reviewers confirming no Blocking/Major findings")

    deterministic_exception = yes_no_value(body, "Deterministic-only exception used")
    if deterministic_exception == "yes" and not bullet_has_content(body, "Deterministic guard covering exception"):
        errors.append("deterministic-only exception lacks guard evidence")


def check_requirements(requirements: str | None, errors: list[str]) -> None:
    if not requirements:
        errors.append("requirements analysis is required")
        return
    status = first_section_status(requirements, "Requirements Analysis Status", "Clarification Status")
    if status != "Complete":
        errors.append(f"requirements analysis status is not Complete: {status!r}")


def check_design_ready(
    requirements_path: str,
    requirements: str | None,
    design_path: str | None,
    design: str | None,
    design_skill_path: str,
    errors: list[str],
) -> None:
    if not design_path or not design:
        if design_gate_required(requirements):
            if not Path(design_skill_path).exists():
                errors.append(f"Design Gate required but $designing-cybernetic-solutions is unavailable at {design_skill_path}")
            else:
                errors.append("Design Gate required but design artifact is missing; next allowed action is RunDesign")
        return

    status = section_status(design, "Design Status")
    if status not in {"Candidate", "Reviewed", "Approved"}:
        errors.append(f"design status must be Candidate, Reviewed, or Approved: {status!r}")
    require_reference(design, requirements_path, "design", errors)
    if output_contract_gate_required(requirements, design) and not output_contract_present_upstream(requirements, design):
        errors.append("Output Contract Gate is required but no upstream output contract is present")
    if has_blocking_design_questions(design):
        errors.append("design has blocking open design questions")


def check_goal_ready(
    requirements_path: str,
    requirements: str | None,
    design: str | None,
    design_path: str | None,
    goal_path: str | None,
    goal: str | None,
    errors: list[str],
) -> None:
    if not goal_path or not goal:
        errors.append("goal contract is required")
        return
    require_reference(goal, requirements_path, "goal", errors)
    require_reference(goal, design_path, "goal", errors)
    if output_contract_required(requirements, design, goal) and not section_has_meaningful_content(goal, "Final Output Contract"):
        errors.append("Output contract is required by gate or upstream artifact, but goal lacks meaningful ## Final Output Contract")


def check_plan_ready(
    requirements_path: str,
    design_path: str | None,
    goal_path: str | None,
    plan_path: str | None,
    plan: str | None,
    errors: list[str],
) -> None:
    if not plan_path or not plan:
        errors.append("execution policy is required")
        return
    status = section_status(plan, "Execution Policy Status")
    if status not in {"Candidate", "Approved"}:
        errors.append(f"execution policy status must be Candidate or Approved: {status!r}")
    require_reference(plan, requirements_path, "plan", errors)
    require_reference(plan, design_path, "plan", errors)
    require_reference(plan, goal_path, "plan", errors)
    check_execution_topology(plan, errors)


def check_review_ready(
    requirements_path: str,
    design_path: str | None,
    goal_path: str | None,
    plan_path: str | None,
    review_path: str | None,
    review: str | None,
    errors: list[str],
) -> None:
    if not review_path or not review:
        errors.append("control review is required")
        return
    require_reference(review, requirements_path, "review", errors)
    require_reference(review, design_path, "review", errors)
    require_reference(review, goal_path, "review", errors)
    require_reference(review, plan_path, "review", errors)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--state", required=True, choices=sorted(NEXT_ACTION))
    parser.add_argument("--requirements", dest="requirements")
    parser.add_argument("--clarification", dest="requirements", help="Deprecated alias for --requirements")
    parser.add_argument("--design")
    parser.add_argument("--goal")
    parser.add_argument("--plan")
    parser.add_argument("--review")
    parser.add_argument("--design-skill-path", default=".agents/skills/designing-cybernetic-solutions/SKILL.md")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    if not args.requirements:
        parser.error("--requirements is required")

    errors: list[str] = []
    warnings: list[str] = []
    try:
        requirements = read(args.requirements)
        design = read(args.design)
        goal = read(args.goal)
        plan = read(args.plan)
        review = read(args.review)
    except FileNotFoundError as exc:
        errors.append(str(exc))
        requirements = design = goal = plan = review = None

    check_requirements(requirements, errors)

    if args.state in {"before-design", "before-goal", "before-policy", "before-review", "before-runtime-compile"}:
        if args.state == "before-design" and design_gate_required(requirements) and not Path(args.design_skill_path).exists():
            errors.append(f"Design Gate required but $designing-cybernetic-solutions is unavailable at {args.design_skill_path}")

    if args.state in {"before-goal", "before-policy", "before-review", "before-runtime-compile"}:
        check_design_ready(args.requirements, requirements, args.design, design, args.design_skill_path, errors)

    if args.state in {"before-policy", "before-review", "before-runtime-compile"}:
        check_goal_ready(args.requirements, requirements, design, args.design, args.goal, goal, errors)

    if args.state in {"before-review", "before-runtime-compile"}:
        check_plan_ready(args.requirements, args.design, args.goal, args.plan, plan, errors)

    if args.state == "before-runtime-compile":
        check_review_ready(args.requirements, args.design, args.goal, args.plan, args.review, review, errors)
        if review:
            status = section_status(review, "Review Status")
            if status != "Approved":
                errors.append(f"control review status under ## Review Status is not Approved: {status!r}")
            check_final_observer(review, errors)

    ok = not errors
    result: dict[str, Any] = {
        "ok": ok,
        "state": args.state,
        "next_allowed_action": ok_next_action(args.state, requirements, args.design) if ok else blocked_next_action(errors),
        "errors": errors,
        "warnings": warnings,
    }

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("PASS" if ok else "FAIL")
        print(f"NEXT: {result['next_allowed_action']}")
        for error in errors:
            print(f"ERROR: {error}")
        for warning in warnings:
            print(f"WARN: {warning}")
    return 0 if ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
