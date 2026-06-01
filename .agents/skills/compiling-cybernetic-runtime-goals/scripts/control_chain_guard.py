#!/usr/bin/env python3
"""Guard for compiling a runtime /goal from approved control artifacts.

This script checks phase-gate conditions. It does not decide requirement semantics.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


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


def output_contract_gate_required(*texts: str) -> bool:
    combined = "\n".join(texts)
    for line in combined.splitlines():
        lowered = line.casefold()
        if "output contract gate" not in lowered:
            continue
        if re.search(r"not\s+required|not\s+applicable|satisfied", lowered):
            continue
        if "required" in lowered:
            return True
    return False


def yes_no_value(text: str, label: str) -> str | None:
    pattern = re.compile(YES_NO_LINE_RE.pattern.format(label=re.escape(label)), YES_NO_LINE_RE.flags)
    m = pattern.search(text)
    if not m:
        return None
    value = m.group(1).strip().casefold()
    if value in {"yes", "y", "true", "是"}:
        return "yes"
    if value in {"no", "n", "false", "否"}:
        return "no"
    return value


def bullet_has_content(text: str, label: str) -> bool:
    pattern = re.compile(rf"(?im)^\s*-\s*{re.escape(label)}\s*:\s*(.+?)\s*$")
    m = pattern.search(text)
    if m and meaningful_line(m.group(1)):
        return True

    block_pattern = re.compile(rf"(?ims)^\s*-\s*{re.escape(label)}\s*:\s*$\n(?P<body>.*?)(?=^-\s*\S|\Z)")
    block = block_pattern.search(text)
    if not block:
        return False
    body = block.group("body")
    return any(meaningful_line(line) for line in body.splitlines())


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
    if text in {"yes/no", "yes / no"}:
        return False
    return True


def has_section(text: str, heading: str) -> bool:
    return section_body(text, heading) is not None


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


def output_contract_required(*texts: str | None) -> bool:
    return output_contract_gate_required(*(text or "" for text in texts)) or output_contract_present_upstream(
        requirements=texts[0] if len(texts) > 0 else None,
        design=texts[1] if len(texts) > 1 else None,
        goal=texts[2] if len(texts) > 2 else None,
    )


def selected_execution_topology(plan: str | None) -> str | None:
    if not plan:
        return None
    body = section_body(plan, "Context Management / Execution Topology")
    if body is None:
        return None
    m = re.search(r"(?im)^\s*Selected topology\s*:\s*`?([^`\n]+?)`?\s*$", body)
    if not m:
        return None
    value = m.group(1).strip().strip("`")
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


def suggest_next_action(errors: list[str]) -> str:
    joined = "\n".join(errors).casefold()

    if "requirements analysis status is not complete" in joined:
        return "ReturnToRequirementsAnalysis"
    if "design gate is required" in joined or "design status" in joined or "design does not reference" in joined:
        return "RunDesign"
    if "output contract" in joined or "goal lacks" in joined or "goal contains runtime control-structure" in joined:
        return "RunGoalWriting"
    if "execution policy status" in joined or "execution topology" in joined or "plan does not reference" in joined:
        return "RunExecutionPolicy"
    if (
        "control review status" in joined
        or "final observer" in joined
        or "post-review" in joined
        or "deterministic-only exception" in joined
        or "review does not reference" in joined
    ):
        return "RunReview"
    if "missing file" in joined:
        return "ProvideMissingArtifact"
    if "does not reference required path" in joined:
        return "FixSourceContracts"
    return "Blocked"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--requirements", dest="requirements")
    ap.add_argument("--clarification", dest="requirements", help="Deprecated alias for --requirements")
    ap.add_argument("--design", required=False)
    ap.add_argument("--goal", required=True)
    ap.add_argument("--plan", required=True)
    ap.add_argument("--review", required=True)
    args = ap.parse_args()
    if not args.requirements:
        ap.error("--requirements is required")

    errors: list[str] = []
    try:
        requirements = read(args.requirements)
        design = read(args.design) if args.design else None
        goal = read(args.goal)
        plan = read(args.plan)
        review = read(args.review)
    except FileNotFoundError as e:
        errors.append(str(e))
        requirements = goal = plan = review = ""
        design = None

    if requirements:
        requirements_status = first_section_status(requirements, "Requirements Analysis Status", "Clarification Status")
        if requirements_status != "Complete":
            errors.append(f"requirements analysis status is not Complete: {requirements_status!r}")

    if design:
        design_status = section_status(design, "Design Status")
        if design_status not in {"Candidate", "Reviewed", "Approved"}:
            errors.append(f"design status under ## Design Status must be Candidate, Reviewed, or Approved: {design_status!r}")
        if args.requirements not in design:
            errors.append(f"design does not reference required requirements path: {args.requirements}")
        if output_contract_gate_required(requirements, design) and not output_contract_present_upstream(requirements, design):
            errors.append("Output Contract Gate is required but no upstream output contract is present")
    elif design_gate_required(requirements, goal, plan, review):
        errors.append("Design Gate is required but --design was not provided")

    if goal and output_contract_required(requirements, design or "", goal) and not section_has_meaningful_content(goal, "Final Output Contract"):
        errors.append("Output contract is required by gate or upstream artifact, but goal lacks meaningful ## Final Output Contract")

    if plan:
        plan_status = section_status(plan, "Execution Policy Status")
        if plan_status != "Candidate":
            errors.append(f"execution policy status under ## Execution Policy Status must be Candidate: {plan_status!r}")
        if selected_execution_topology(plan) is None:
            errors.append("execution policy must define a selected Context Management / Execution Topology")

    if review:
        review_status = section_status(review, "Review Status")
        if review_status != "Approved":
            errors.append(f"control review status under ## Review Status is not Approved: {review_status!r}")
        check_final_observer(review, errors)

    for path, text, label in [
        (args.requirements, goal, "goal"),
        (args.design, goal, "goal"),
        (args.requirements, plan, "plan"),
        (args.design, plan, "plan"),
        (args.goal, plan, "plan"),
        (args.requirements, review, "review"),
        (args.design, review, "review"),
        (args.goal, review, "review"),
        (args.plan, review, "review"),
    ]:
        if not path:
            continue
        if text and path not in text:
            errors.append(f"{label} does not reference required path: {path}")

    forbidden = [
        "first write a plan",
        "first create a plan",
        "Start with $superpowers:writing-plans",
        "Start with `$superpowers:writing-plans`",
        "write an execution policy and then execute",
    ]
    for phrase in forbidden:
        if phrase.lower() in goal.lower():
            errors.append(f"goal contains runtime control-structure synthesis phrase: {phrase}")

    if errors:
        print("FAIL")
        print(f"NEXT: {suggest_next_action(errors)}")
        for e in errors:
            print(f"ERROR: {e}")
        return 2
    print("PASS")
    print("NEXT: CompileRuntimeGoal")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
