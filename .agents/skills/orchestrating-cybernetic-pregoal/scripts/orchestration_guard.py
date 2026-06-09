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
    if (
        "requirements missing ## what the user approved" in joined
        or "what the user approved is not approved" in joined
        or "records conflicting agent workflow preference" in joined
    ):
        return "ReturnToRequirementsAnalysis"
    if "$designing-cybernetic-solutions is unavailable" in joined:
        return "Blocked"
    if "design artifact is missing" in joined:
        return "RunDesign"
    if (
        "design status" in joined
        or "design does not reference" in joined
        or "design has blocking" in joined
        or "answer method check" in joined
    ):
        return "RunDesign"
    if "output contract check" in joined and "design lacks" in joined:
        return "RunDesign"
    if "output contract check" in joined and "goal lacks" in joined:
        return "RunGoalWriting"
    if "output contract is required" in joined and "goal lacks" in joined:
        return "RunGoalWriting"
    if "goal file is required" in joined or "goal does not reference" in joined:
        return "RunGoalWriting"
    if (
        "execution policy is required" in joined
        or "execution policy status" in joined
        or "execution work assignment" in joined
        or "plan does not reference" in joined
        or "subagent execution mode" in joined
        or "max concurrent subagents" in joined
        or "ordered work package sequence" in joined
        or "integration check after each package" in joined
        or "parallel wave matrix" in joined
        or "conflict / lock model" in joined
        or "failure policy" in joined
        or "concurrency frontier rule" in joined
        or "safe frontier" in joined
        or "runtime delegation preference" in joined
        or "agent workflow preference" in joined
        or "main-agent integration rule" in joined
        or "execution policy missing ## action that can make it done strategy" in joined
        or "execution policy action that can make it done strategy missing" in joined
        or "execution policy missing ## steps that make the result true" in joined
        or "execution policy steps that make the result true" in joined
        or "execution policy missing ## candidate plan tasks" in joined
        or "execution policy candidate plan task missing" in joined
        or "candidate plan tasks has no candidate tasks" in joined
        or "execution policy missing ## work coverage and action limits matrix" in joined
        or "execution policy work coverage and action limits matrix" in joined
    ):
        return "RunExecutionPolicy"
    if (
        "review" in joined
        or "final observer" in joined
        or "review does not reference" in joined
        or "post-review" in joined
    ):
        return "RunReview"
    return "Blocked"


def ok_next_action(state: str, requirements: str | None, design_path: str | None) -> str:
    if state == "before-design":
        if design_check_required(requirements) and not design_path:
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


def design_check_required(*texts: str | None) -> bool:
    combined = "\n".join(text for text in texts if text)
    for line in combined.splitlines():
        lowered = line.casefold()
        if "design check" not in lowered:
            continue
        if re.search(r"not\s+required|not\s+applicable|satisfied", lowered):
            continue
        if "required" in lowered:
            return True
    return False


def output_contract_check_required(*texts: str | None) -> bool:
    combined = "\n".join(text for text in texts if text)
    for line in combined.splitlines():
        lowered = line.casefold()
        if "output contract check" not in lowered:
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
        section_has_meaningful_content(requirements, "Final Answer Format")
        or section_has_meaningful_content(design, "Final Answer Format Design")
        or section_has_meaningful_content(goal, "Final Final Answer Format")
    )


def output_contract_required(requirements: str | None, design: str | None, goal: str | None) -> bool:
    return output_contract_check_required(requirements, design, goal) or output_contract_present_upstream(requirements, design, goal)


def selected_execution_work_assignment(plan: str | None) -> str | None:
    if not plan:
        return None
    body = section_body(plan, "Who Does The Work / Context Use")
    if body is None:
        return None
    match = re.search(r"(?im)^\s*Who does the work\s*:\s*`?([^`\n]+?)`?\s*$", body)
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


def selected_agent_workflow(plan: str | None) -> str | None:
    body = section_body(plan or "", "Who Does The Work / Context Use")
    if body is None:
        return None
    match = re.search(r"(?im)^\s*Selected agent workflow\s*:\s*`?([^`\n]+?)`?\s*$", body)
    if not match:
        return None

    return normalize_agent_workflow(match.group(1))


def normalize_agent_workflow(value: str | None) -> str | None:
    if value is None:
        return None
    value = value.strip().strip("`").casefold()
    if "/" in value:
        return None
    if value in {"bounded-protocol", "bounded protocol"}:
        return "bounded-protocol"
    if value in {"superpowers-subagent-driven-development", "$superpowers:subagent-driven-development"}:
        return "superpowers-subagent-driven-development"
    if value in {"superpowers-dispatching-parallel-agents", "$superpowers:dispatching-parallel-agents"}:
        return "superpowers-dispatching-parallel-agents"
    if value in {"adapter-specific", "adapter specific"}:
        return "adapter-specific"
    if value == "none":
        return "none"
    if value in {"no preference", "not specified", "unspecified", "not applicable", "n/a"}:
        return "no preference"
    return None


DELEGATION_WORKFLOW_REGISTRY_PATH = Path(__file__).resolve().parents[2] / "references/delegation-workflow-registry.json"


def delegation_workflow_registry() -> dict[str, object]:
    try:
        return json.loads(DELEGATION_WORKFLOW_REGISTRY_PATH.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def delegation_workflow_definition(workflow: str | None) -> dict[str, object]:
    value = delegation_workflow_registry().get(workflow or "", {})
    return value if isinstance(value, dict) else {}


def registry_list_field(definition: dict[str, object], key: str) -> list[str]:
    value = definition.get(key, [])
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, str)]


def selected_subagent_execution_mode(plan: str | None) -> str | None:
    body = section_body(plan or "", "Who Does The Work / Context Use")
    if body is None:
        return None
    match = re.search(r"(?im)^\s*Subagent execution mode\s*:\s*`?([^`\n]+?)`?\s*$", body)
    if not match:
        return None

    value = match.group(1).strip().strip("`").casefold()
    if "/" in value:
        return None
    if value in {"none", "not applicable", "n/a"}:
        return "none"
    if value in {"serial-single-active", "serial single active"}:
        return "serial-single-active"
    if value in {"parallel-max-safe", "parallel max safe"}:
        return "parallel-max-safe"
    return None


def max_concurrent_subagents(plan: str | None) -> str | None:
    body = section_body(plan or "", "Who Does The Work / Context Use")
    if body is None:
        return None
    value = labeled_value(body, "Max concurrent subagents")
    if value is None:
        return None
    value = value.strip().strip("`")
    if "/" in value:
        return None
    return value


def task_level(plan: str | None) -> int | None:
    body = section_body(plan or "", "Who Does The Work / Context Use")
    if body is None:
        return None
    match = re.search(r"(?im)^\s*Task level\s*:\s*`?Level\s*([0-4])`?\s*$", body)
    if not match:
        return None
    return int(match.group(1))


APPROVAL_YES_VALUES = {"yes", "y", "true", "approved", "是", "已批准", "批准"}


def labeled_value(text: str, label: str) -> str | None:
    patterns = [
        rf"(?im)^\s*-\s*{re.escape(label)}\s*:\s*`?([^`\n]+?)`?\s*$",
        rf"(?im)^\s*{re.escape(label)}\s*:\s*`?([^`\n]+?)`?\s*$",
    ]
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(1).strip().strip("`")
    return None


def table_field_value(text: str, field: str) -> str | None:
    for line in text.splitlines():
        stripped = line.strip()
        if "|" not in stripped:
            continue
        if re.fullmatch(r"\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)+\|?", stripped):
            continue
        cells = [cell.strip().strip("`") for cell in stripped.strip("|").split("|")]
        if len(cells) < 2 or field.casefold() not in cells[0].casefold():
            continue
        for cell in cells[1:]:
            if meaningful_line(cell):
                return cell
    return None


def field_value(text: str, label: str) -> str | None:
    return labeled_value(text, label) or table_field_value(text, label)


def approval_value_is_yes(text: str, label: str) -> bool:
    value = labeled_value(text, label)
    return value is not None and value.casefold() in APPROVAL_YES_VALUES


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


def table_field_has_content(text: str, field: str) -> bool:
    for line in text.splitlines():
        stripped = line.strip()
        if "|" not in stripped:
            continue
        if re.fullmatch(r"\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)+\|?", stripped):
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if not cells or field.casefold() not in cells[0].casefold():
            continue
        return any(meaningful_line(cell) for cell in cells[1:])
    return False


def labeled_or_table_field_has_content(text: str, label: str) -> bool:
    return bullet_has_content(text, label) or labeled_block_has_content(text, label) or table_field_has_content(text, label)


def has_meaningful_delegation_matrix(body: str) -> bool:
    lowered = body.casefold()
    required_columns = [
        "work package",
        "executor",
        "context pack",
        "allowed actions",
        "return format",
        "integration check",
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


def has_table_with_data_row(body: str, required_columns: list[str]) -> bool:
    lowered = body.casefold()
    if not all(column.casefold() in lowered for column in required_columns):
        return False

    for line in body.splitlines():
        stripped = line.strip()
        if "|" not in stripped:
            continue
        if re.fullmatch(r"\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)+\|?", stripped):
            continue
        row_lowered = stripped.casefold()
        if all(column.casefold() in row_lowered for column in required_columns):
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if len(cells) >= len(required_columns) and all(meaningful_line(cell) for cell in cells[: len(required_columns)]):
            return True
    return False


CONTEXT_PACK_FIELDS = [
    "Relevant control excerpts",
    "Current batch objective",
    "Allowed artifacts/places",
    "Forbidden changes",
    "Required evidence checks/evidence",
    "Stop conditions",
    "Expected return format",
]

CONTEXT_COMPRESSION_FIELDS = [
    "Active control summary",
    "Completed work packages",
    "Subagent outputs integrated",
    "Evidence produced",
    "Deferred evidence checks and reasons",
    "Unresolved blockers",
    "Deviations from policy",
    "Next allowed action",
]


def check_labeled_requirements(body: str, heading: str, labels: list[str], errors: list[str]) -> None:
    if heading.casefold() not in body.casefold():
        errors.append(f"execution work assignment missing {heading}: {', '.join(labels)}")
        return
    for label in labels:
        if not labeled_or_table_field_has_content(body, label):
            errors.append(f"execution work assignment {heading} missing {label}")


def check_execution_work_assignment(plan: str | None, errors: list[str]) -> None:
    body = section_body(plan or "", "Who Does The Work / Context Use")
    if body is None:
        errors.append("execution policy missing ## Who Does The Work / Context Use")
        return

    work_assignment = selected_execution_work_assignment(plan)
    if work_assignment is None:
        errors.append("execution policy is required to define a selected Who Does The Work / Context Use")
        return

    if not labeled_block_has_content(body, "Work Assignment rationale"):
        errors.append("execution work assignment missing Work Assignment rationale")
    if not labeled_block_has_content(body, "Main agent owns"):
        errors.append("execution work assignment missing main-agent ownership")

    level = task_level(plan)
    if level is None:
        errors.append("execution work assignment missing Task level")
    if work_assignment == "Main-only" and level in {3, 4} and not labeled_block_has_content(body, "Main-only context-load justification"):
        errors.append("Level 3/4 Main-only execution work assignment missing Main-only context-load justification")

    if work_assignment in {"Serial subagent-driven", "Parallel subagent-driven"}:
        if not has_meaningful_delegation_matrix(body):
            errors.append("execution work assignment missing meaningful delegation matrix with Context pack, Allowed actions, Return format, and Integration check")
        check_labeled_requirements(body, "Context Pack Requirements", CONTEXT_PACK_FIELDS, errors)
        workflow = selected_agent_workflow(plan)
        if workflow is None:
            errors.append("subagent-driven work assignment missing valid Selected agent workflow")
        elif workflow == "none":
            errors.append("subagent-driven work assignment cannot use Selected agent workflow: none")
        if not labeled_block_has_content(body, "Subagent workflow"):
            errors.append("subagent-driven work assignment missing approved bounded subagent workflow")

        mode = selected_subagent_execution_mode(plan)
        max_concurrent = max_concurrent_subagents(plan)
        check_workflow_mode_compatibility(work_assignment, workflow, mode, max_concurrent, errors)
        if work_assignment == "Serial subagent-driven":
            if mode != "serial-single-active":
                errors.append("Serial subagent-driven work assignment requires Subagent execution mode: serial-single-active")
            if max_concurrent != "1":
                errors.append("Serial subagent-driven work assignment requires Max concurrent subagents: 1")
            if not labeled_block_has_content(body, "Ordered work package sequence"):
                errors.append("Serial subagent-driven work assignment missing Ordered work package sequence")
            if not labeled_block_has_content(body, "Integration check after each package"):
                errors.append("Serial subagent-driven work assignment missing Integration check after each package")
        elif work_assignment == "Parallel subagent-driven":
            if mode != "parallel-max-safe":
                errors.append("Parallel subagent-driven work assignment requires Subagent execution mode: parallel-max-safe")
            if max_concurrent is None or not (max_concurrent.casefold() == "auto" or re.fullmatch(r"[1-9][0-9]*", max_concurrent)):
                errors.append("Parallel subagent-driven work assignment requires Max concurrent subagents: auto or N")
            for label in (
                "Concurrency selection rationale",
                "Concurrency frontier rule",
                "Failure policy",
                "Main-agent integration rule",
            ):
                if not labeled_block_has_content(body, label):
                    errors.append(f"Parallel subagent-driven work assignment missing {label}")
            if not has_table_with_data_row(body, ["Artifact / state / shared place", "Lock owner", "Conflict rule"]):
                errors.append("Parallel subagent-driven work assignment missing meaningful Conflict / lock model")
            if not has_table_with_data_row(body, ["Wave", "Required-step frontier", "Work packages", "Independence proof", "Shared places / locks", "Integration barrier"]):
                errors.append("Parallel subagent-driven work assignment missing meaningful Parallel wave matrix with Required-step frontier")

    if work_assignment in {"Serial subagent-driven", "Parallel subagent-driven"} or level in {3, 4}:
        check_labeled_requirements(body, "Context Compression Rule", CONTEXT_COMPRESSION_FIELDS, errors)

    if work_assignment == "Parallel subagent-driven":
        for label in ("Human approval", "Dependency independence", "Control-review approval"):
            if not approval_value_is_yes(body, label):
                errors.append(f"parallel execution work assignment requires {label}: yes/approved")


def check_workflow_mode_compatibility(
    work_assignment: str,
    workflow: str | None,
    mode: str | None,
    max_concurrent: str | None,
    errors: list[str],
) -> None:
    definition = delegation_workflow_definition(workflow)
    if definition:
        allowed_work_assignment = registry_list_field(definition, "allowed_work_assignment")
        allowed_mode = registry_list_field(definition, "allowed_mode")
        max_rule = str(definition.get("max_concurrent", "")).strip()
        if allowed_work_assignment and work_assignment not in allowed_work_assignment:
            errors.append(f"Selected agent workflow {workflow} is not compatible with work assignment {work_assignment}")
        if allowed_mode and mode not in allowed_mode:
            errors.append(f"Selected agent workflow {workflow} is not compatible with Subagent execution mode: {mode}")
        if max_rule == "1" and max_concurrent != "1":
            errors.append(f"Selected agent workflow {workflow} requires Max concurrent subagents: 1")

    if workflow == "superpowers-subagent-driven-development":
        if work_assignment != "Serial subagent-driven" or mode != "serial-single-active" or max_concurrent != "1":
            errors.append(
                "Selected agent workflow superpowers-subagent-driven-development supports only Serial subagent-driven, Subagent execution mode: serial-single-active, Max concurrent subagents: 1; it cannot be used with parallel-max-safe"
            )
    if workflow == "superpowers-dispatching-parallel-agents":
        if work_assignment != "Parallel subagent-driven" or mode != "parallel-max-safe":
            errors.append(
                "Selected agent workflow superpowers-dispatching-parallel-agents supports only Parallel subagent-driven with Subagent execution mode: parallel-max-safe"
            )
    if mode == "parallel-max-safe" and workflow == "superpowers-subagent-driven-development":
        errors.append("parallel-max-safe cannot use Selected agent workflow: superpowers-subagent-driven-development")


def check_plan_target_producing_strategy(plan: str | None, errors: list[str]) -> None:
    body = section_body(plan or "", "Action That Can Make It Done")
    if body is None:
        errors.append("execution policy missing ## Action That Can Make It Done")
        return
    for label in (
        "Action that can make it done",
        "Proof of impossibility, if any",
        "Non-achieved terminal report rule",
    ):
        if not labeled_or_table_field_has_content(body, label):
            errors.append(f"execution policy Action That Can Make It Done missing {label}")


def check_plan_target_producing_spine(plan: str | None, errors: list[str]) -> None:
    body = section_body(plan or "", "Steps That Make The Result True")
    if body is None:
        errors.append("execution policy missing ## Steps That Make The Result True")
        return
    required_columns = ["Required step", "Required state transition", "Required evidence"]
    if not has_table_with_data_row(body, required_columns):
        errors.append("execution policy Steps That Make The Result True has no meaningful required step rows")


def check_candidate_plan_tasks_spine_nodes(plan: str | None, errors: list[str]) -> None:
    body = section_body(plan or "", "Candidate Plan Tasks")
    if body is None:
        errors.append("execution policy missing ## Candidate Plan Tasks")
        return

    task_matches = list(re.finditer(r"(?m)^###\s+(.+?)\s*$", body))
    if not task_matches:
        errors.append("execution policy Candidate Plan Tasks has no candidate tasks")
        return

    required_fields = [
        "Required step(s)",
        "Role",
        "State transition advanced",
        "Transition evidence produced",
        "Integration check",
        "Counts as goal progress",
        "Why this is not merely component completion",
    ]
    for index, match in enumerate(task_matches):
        start = match.end()
        end = task_matches[index + 1].start() if index + 1 < len(task_matches) else len(body)
        task_body = body[start:end]
        task_name = match.group(1).strip()
        for field in required_fields:
            if not labeled_or_table_field_has_content(task_body, field):
                errors.append(f"execution policy Candidate Plan Task missing {field}: {task_name}")


def check_plan_horizon_authority(plan: str | None, errors: list[str]) -> None:
    body = section_body(plan or "", "Work Coverage And Action Limits Matrix")
    if body is None:
        errors.append("execution policy missing ## Work Coverage And Action Limits Matrix")
        return
    required_columns = [
        "Work item / place",
        "In work covered in this run?",
        "What the agent may do",
        "Required runtime handling",
        "Counts as achieved?",
    ]
    if not has_table_with_data_row(body, required_columns):
        errors.append("execution policy Work Coverage And Action Limits Matrix has no meaningful coverage rows")


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
        errors.append("review missing ## Final Observer Check")
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
    hsa_body = section_body(requirements, "What the User Approved")
    if hsa_body is None:
        errors.append("requirements missing ## What the User Approved")
        return
    hsa_status = section_status(requirements, "What the User Approved")
    if hsa_status != "Approved":
        errors.append(f"What the User Approved is not Approved: {hsa_status!r}")


def check_max_safe_parallel_preference(requirements: str | None, plan: str | None, errors: list[str]) -> None:
    hsa = section_body(requirements or "", "What the User Approved")
    if hsa is None or plan is None:
        return

    preference = field_value(hsa, "Agent delegation preference")
    if preference is None or preference.casefold() != "max-safe-parallel":
        return

    work_assignment = selected_execution_work_assignment(plan)
    if work_assignment == "Parallel subagent-driven":
        return

    work_assignment_body = section_body(plan, "Who Does The Work / Context Use") or ""
    rationale = field_value(work_assignment_body, "Concurrency selection rationale")
    if rationale is None or "safe frontier" not in rationale.casefold():
        errors.append(
            "What the User Approved records Agent delegation preference as max-safe-parallel but execution policy is not Parallel subagent-driven; Concurrency selection rationale must mention safe frontier"
        )


def check_delegation_workflow_preference(requirements: str | None, plan: str | None, errors: list[str]) -> None:
    hsa = section_body(requirements or "", "What the User Approved")
    if hsa is None:
        return

    workflow_preference = normalize_agent_workflow(field_value(hsa, "Agent workflow preference"))
    if workflow_preference in {None, "no preference"}:
        return

    runtime_preference = (field_value(hsa, "Agent delegation preference") or "").casefold()
    if runtime_preference == "max-safe-parallel" and workflow_preference == "superpowers-subagent-driven-development":
        errors.append(
            "What the User Approved records conflicting Agent workflow preference and Agent delegation preference: max-safe-parallel; superpowers-subagent-driven-development is serial-single-active only"
        )
        return

    if plan is None:
        return

    selected = selected_agent_workflow(plan)
    if selected == workflow_preference:
        return

    work_assignment_body = section_body(plan, "Who Does The Work / Context Use") or ""
    rationale = (
        field_value(work_assignment_body, "Agent workflow compatibility rationale")
        or field_value(work_assignment_body, "Agent workflow compatibility rationale")
        or ""
    )
    lowered = rationale.casefold()
    if not any(term in lowered for term in ("incompatible", "not compatible", "capability limit", "unsupported")):
        errors.append(
            f"What the User Approved records Agent workflow preference as {workflow_preference}, but execution policy selected {selected}; record an agent workflow compatibility rationale before changing it"
        )


def check_design_ready(
    requirements_path: str,
    requirements: str | None,
    design_path: str | None,
    design: str | None,
    design_skill_path: str,
    errors: list[str],
) -> None:
    if not design_path or not design:
        if design_check_required(requirements):
            if not Path(design_skill_path).exists():
                errors.append(f"Design Check required but $designing-cybernetic-solutions is unavailable at {design_skill_path}")
            else:
                errors.append("Design Check required but design artifact is missing; next allowed action is RunDesign")
        return

    status = section_status(design, "Design Status")
    if status not in {"Candidate", "Reviewed", "Approved"}:
        errors.append(f"design status must be Candidate, Reviewed, or Approved: {status!r}")
    require_reference(design, requirements_path, "design", errors)
    if output_contract_check_required(requirements, design) and not output_contract_present_upstream(requirements, design):
        errors.append("Final Answer Format Check is required but no upstream output contract is present")
    check_design_answer_path_check(requirements, design, errors)
    if has_blocking_design_questions(design):
        errors.append("design has blocking open design questions")


ANSWER_METHOD_REGISTRY_PATH = Path(__file__).resolve().parents[2] / "references/answer-method-registry.json"


def answer_method_registry() -> dict[str, object]:
    try:
        return json.loads(ANSWER_METHOD_REGISTRY_PATH.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def answer_method_definition(family: str) -> dict[str, object]:
    value = answer_method_registry().get(family, {})
    return value if isinstance(value, dict) else {}


def registry_string_list(definition: dict[str, object], key: str) -> list[str]:
    value = definition.get(key, [])
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, str)]


def check_design_answer_path_check(requirements: str | None, design: str | None, errors: list[str]) -> None:
    hsa = section_body(requirements or "", "What the User Approved")
    if hsa is None or design is None:
        return

    answering_method = field_value(hsa, "How this should be answered")
    not_sufficient = field_value(hsa, "What is not enough")
    if not any((answering_method, not_sufficient)):
        return

    body = section_body(design, "Answer Method Check")
    if body is None:
        errors.append("design missing ## Answer Method Check for approved answer method")
        return

    for label in (
        "Approved answer method",
        "Required answer path",
        "Required steps covered",
        "What is not enough avoided",
    ):
        if not labeled_or_table_field_has_content(body, label):
            errors.append(f"design Answer Method Check missing {label}")

    instantiated = (field_value(body, "Required answer path") or "").casefold()
    mandatory = (field_value(body, "Required steps covered") or "").casefold()
    avoided = (field_value(body, "What is not enough avoided") or "").casefold()
    substitute = (not_sufficient or "").casefold()
    approved = (field_value(body, "Approved answer method") or "").casefold()
    if answering_method and answering_method.casefold() not in approved:
        errors.append("design Answer Method Check does not preserve approved answer method")
    if substitute and substitute in instantiated:
        errors.append(f"design Answer Method Check substitutes what is not enough: {not_sufficient}")
    if substitute and (avoided.startswith("no") or " no" in avoided[:12]):
        errors.append("design Answer Method Check records what is not enough was not avoided")
    if answering_method and not mandatory:
        errors.append("design Answer Method Check missing required steps coverage")


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
        errors.append("goal file is required")
        return
    require_reference(goal, requirements_path, "goal", errors)
    require_reference(goal, design_path, "goal", errors)
    if output_contract_required(requirements, design, goal) and not section_has_meaningful_content(goal, "Final Final Answer Format"):
        errors.append("Output contract is required by check or upstream artifact, but goal lacks meaningful ## Final Final Answer Format")


def check_plan_ready(
    requirements_path: str,
    requirements: str | None,
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
    check_execution_work_assignment(plan, errors)
    check_max_safe_parallel_preference(requirements, plan, errors)
    check_delegation_workflow_preference(requirements, plan, errors)
    check_plan_target_producing_strategy(plan, errors)
    check_plan_target_producing_spine(plan, errors)
    check_candidate_plan_tasks_spine_nodes(plan, errors)
    check_plan_horizon_authority(plan, errors)


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
        errors.append("review is required")
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
        if args.state == "before-design" and design_check_required(requirements) and not Path(args.design_skill_path).exists():
            errors.append(f"Design Check required but $designing-cybernetic-solutions is unavailable at {args.design_skill_path}")

    if args.state in {"before-goal", "before-policy", "before-review", "before-runtime-compile"}:
        check_design_ready(args.requirements, requirements, args.design, design, args.design_skill_path, errors)

    if args.state in {"before-policy", "before-review", "before-runtime-compile"}:
        check_goal_ready(args.requirements, requirements, design, args.design, args.goal, goal, errors)

    if args.state in {"before-review", "before-runtime-compile"}:
        check_plan_ready(args.requirements, requirements, args.design, args.goal, args.plan, plan, errors)

    if args.state == "before-runtime-compile":
        check_review_ready(args.requirements, args.design, args.goal, args.plan, args.review, review, errors)
        if review:
            status = section_status(review, "Review Status")
            if status != "Approved":
                errors.append(f"review status under ## Review Status is not Approved: {status!r}")
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
