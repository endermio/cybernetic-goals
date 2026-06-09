#!/usr/bin/env python3
"""Guard for compiling a runtime /goal from approved control artifacts.

This script checks phase-check conditions. It does not decide requirement semantics.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$", re.MULTILINE)
STATUS_LINE_RE = re.compile(r"(?im)^\s*Status\s*:\s*`?([^`\n]+?)`?\s*$")
YES_NO_LINE_RE = re.compile(r"(?im)^\s*-\s*{label}\s*:\s*`?([^`\n]+?)`?\s*$")
ENUM_STATUS_RE = re.compile(r"(?im)^\s*Status\s*:\s*`?([^`\n]*\s/\s[^`\n]*)`?\s*$")
PLACEHOLDER_RE = re.compile(r"\[[^\]\n]{3,}\](?!\()|YYYY-MM-DD(?:-slug|-<slug>)?")
DUPLICATE_PARAGRAPH_MIN_CHARS = 120

RESPONSE_ONLY_PROMPTS = (
    "$orchestrating-cybernetic-pregoal",
    "$writing-cybernetic-goals",
    "$designing-cybernetic-solutions",
    "/goal Execute",
    "Recommended next step:",
    "Response-only handoff:",
)

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


def design_check_required(*texts: str) -> bool:
    combined = "\n".join(texts)
    for line in combined.splitlines():
        lowered = line.casefold()
        if "design check" not in lowered:
            continue
        if re.search(r"not\s+required|not\s+applicable|satisfied", lowered):
            continue
        if "required" in lowered:
            return True
    return False


def output_contract_check_required(*texts: str) -> bool:
    combined = "\n".join(texts)
    for line in combined.splitlines():
        lowered = line.casefold()
        if "output contract check" not in lowered:
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


def line_number(text: str, index: int) -> int:
    return text.count("\n", 0, index) + 1


def normalize_paragraph(paragraph: str) -> str:
    return re.sub(r"\s+", " ", paragraph).strip()


def check_artifact_hygiene(label: str, text: str, errors: list[str]) -> None:
    for match in ENUM_STATUS_RE.finditer(text):
        errors.append(f"{label} artifact hygiene line {line_number(text, match.start())}: unresolved enum status")

    for match in PLACEHOLDER_RE.finditer(text):
        errors.append(f"{label} artifact hygiene line {line_number(text, match.start())}: unresolved placeholder")

    lowered = text.casefold()
    for prompt in RESPONSE_ONLY_PROMPTS:
        index = lowered.find(prompt.casefold())
        if index >= 0:
            errors.append(
                f"{label} artifact hygiene line {line_number(text, index)}: response-only prompt leaked into artifact: {prompt}"
            )

    seen_headings: set[str] = set()
    for match in HEADING_RE.finditer(text):
        heading = match.group(2).strip().rstrip("#").strip()
        normalized = f"{len(match.group(1))}:{heading.casefold()}"
        if normalized in seen_headings:
            errors.append(f"{label} artifact hygiene line {line_number(text, match.start())}: duplicate heading: {heading}")
        else:
            seen_headings.add(normalized)

    seen_paragraphs: set[str] = set()
    offset = 0
    for paragraph in re.split(r"\n\s*\n", text):
        normalized = normalize_paragraph(paragraph)
        paragraph_start = text.find(paragraph, offset)
        offset = paragraph_start + len(paragraph) if paragraph_start >= 0 else offset
        if len(normalized) < DUPLICATE_PARAGRAPH_MIN_CHARS:
            continue
        if normalized.startswith("#") or normalized.startswith("|"):
            continue
        if normalized in seen_paragraphs:
            errors.append(f"{label} artifact hygiene line {line_number(text, max(paragraph_start, 0))}: duplicate paragraph")
        else:
            seen_paragraphs.add(normalized)


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
        section_has_meaningful_content(requirements, "Final Answer Format")
        or section_has_meaningful_content(design, "Final Answer Format Design")
        or section_has_meaningful_content(goal, "Final Final Answer Format")
    )


def output_contract_required(*texts: str | None) -> bool:
    return output_contract_check_required(*(text or "" for text in texts)) or output_contract_present_upstream(
        requirements=texts[0] if len(texts) > 0 else None,
        design=texts[1] if len(texts) > 1 else None,
        goal=texts[2] if len(texts) > 2 else None,
    )


def selected_execution_work_assignment(plan: str | None) -> str | None:
    if not plan:
        return None
    body = section_body(plan, "Who Does The Work / Context Use")
    if body is None:
        return None
    m = re.search(r"(?im)^\s*Who does the work\s*:\s*`?([^`\n]+?)`?\s*$", body)
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
        errors.append("execution policy must define a selected Who Does The Work / Context Use")
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


def check_review_context_work_assignment(review: str, errors: list[str]) -> None:
    independence = section_body(review, "Review Independence")
    if independence is None:
        errors.append("review missing ## Review Independence for Who Does The Work / Context Use")
    else:
        work_assignment_reviewed = yes_no_value(independence, "Who does the work / context use")
        if work_assignment_reviewed != "yes":
            errors.append(
                "review did not record Who does the work / context use: yes in ## Review Independence"
            )

    body = section_body(review, "Who Does The Work / Context Use")
    if body is None:
        errors.append("review missing ## Who Does The Work / Context Use")
        return
    if not labeled_block_has_content(body, "Findings"):
        errors.append("review Who Does The Work / Context Use section has no meaningful findings")


def check_review_subagent_concurrency(plan: str, review: str, errors: list[str]) -> None:
    work_assignment = selected_execution_work_assignment(plan)
    if work_assignment not in {"Serial subagent-driven", "Parallel subagent-driven"}:
        return

    independence = section_body(review, "Review Independence")
    if independence is None:
        errors.append("review missing ## Review Independence for Parallel Agent Safety Check")
    else:
        reviewed = yes_no_value(independence, "Subagent concurrency check")
        if reviewed != "yes":
            errors.append("review did not record Subagent concurrency check: yes in ## Review Independence")

    body = section_body(review, "Parallel Agent Safety Check")
    if body is None:
        errors.append("review missing ## Parallel Agent Safety Check")
        return
    if not labeled_block_has_content(body, "Findings"):
        errors.append("review Parallel Agent Safety Check section has no meaningful findings")


def check_human_approved_target_approval(requirements: str, errors: list[str]) -> None:
    body = section_body(requirements, "What the User Approved")
    if body is None:
        errors.append("requirements missing ## What the User Approved")
        return

    status = section_status(requirements, "What the User Approved")
    if status != "Approved":
        errors.append(f"What the User Approved is not Approved: {status!r}")


def check_max_safe_parallel_preference(requirements: str, plan: str | None, errors: list[str]) -> None:
    hsa = section_body(requirements, "What the User Approved")
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


def check_delegation_workflow_preference(requirements: str, plan: str | None, errors: list[str]) -> None:
    hsa = section_body(requirements, "What the User Approved")
    if hsa is None:
        return

    raw_preference = field_value(hsa, "Agent workflow preference")
    workflow_preference = normalize_agent_workflow(raw_preference)
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


def requirements_control_path(requirements_path: str | None) -> Path | None:
    if not requirements_path:
        return None
    return Path(requirements_path).with_suffix(".control.json")


def read_requirements_control(requirements_path: str | None, errors: list[str]) -> dict[str, object] | None:
    control_path = requirements_control_path(requirements_path)
    if control_path is None:
        errors.append("requirements control sidecar path unavailable")
        return None
    try:
        value = json.loads(control_path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        errors.append(f"requirements control sidecar missing: {control_path}")
        return None
    except json.JSONDecodeError as exc:
        errors.append(f"requirements control sidecar invalid JSON: {control_path}: {exc}")
        return None
    if not isinstance(value, dict):
        errors.append(f"requirements control sidecar must be a JSON object: {control_path}")
        return None
    return value


def sidecar_string(control: dict[str, object] | None, key: str) -> str | None:
    if control is None:
        return None
    value = control.get(key)
    return value if isinstance(value, str) and value.strip() else None


def check_design_answer_path_check(requirements_path: str | None, requirements: str | None, design: str | None, errors: list[str]) -> None:
    hsa = section_body(requirements or "", "What the User Approved")
    if hsa is None or design is None:
        return

    answering_method = field_value(hsa, "How this should be answered")
    not_sufficient = field_value(hsa, "What is not enough")
    if not any((answering_method, not_sufficient)):
        return

    control = read_requirements_control(requirements_path, errors)
    answer_method_key = sidecar_string(control, "answer_method_key")
    forbidden_substitute_key = sidecar_string(control, "forbidden_substitute_key")
    if not answer_method_key:
        errors.append("requirements control sidecar missing answer_method_key")
    if not_sufficient and not forbidden_substitute_key:
        errors.append("requirements control sidecar missing forbidden_substitute_key")

    definition = answer_method_definition(answer_method_key or "")
    if answer_method_key and not definition:
        errors.append(f"requirements control sidecar uses unknown answer_method_key: {answer_method_key}")

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
    forbidden_terms = set(registry_string_list(definition, "forbidden_substitutions"))
    if forbidden_substitute_key:
        forbidden_terms.add(forbidden_substitute_key)
    if substitute:
        forbidden_terms.add(substitute)
    for term in sorted(term for term in forbidden_terms if term):
        if term.casefold() in instantiated:
            errors.append(f"design Answer Method Check substitutes what is not enough: {term}")
    if substitute and substitute in instantiated:
        errors.append(f"design Answer Method Check substitutes what is not enough: {not_sufficient}")
    if substitute and (avoided.startswith("no") or " no" in avoided[:12]):
        errors.append("design Answer Method Check records what is not enough was not avoided")
    if answering_method and not mandatory:
        errors.append("design Answer Method Check missing required steps coverage")
    for node in registry_string_list(definition, "mandatory_nodes"):
        if node.casefold() not in mandatory:
            errors.append(f"design Answer Method Check missing registry required step: {node}")


def hsa_requires_design_answer_path_review(requirements: str | None) -> bool:
    hsa = section_body(requirements or "", "What the User Approved")
    if hsa is None:
        return False
    return any(
        field_value(hsa, label)
        for label in (
            "How this should be answered",
            "What is not enough",
        )
    )


def check_review_design_answer_path(requirements: str, review: str, errors: list[str]) -> None:
    if not hsa_requires_design_answer_path_review(requirements):
        return

    independence = section_body(review, "Review Independence")
    if independence is None:
        errors.append("review missing ## Review Independence for Design Answer Method Check")
    else:
        reviewed = yes_no_value(independence, "Design answer method check")
        if reviewed != "yes":
            errors.append("review did not record Design answer method check: yes in ## Review Independence")

    body = section_body(review, "Design Answer Method Check")
    if body is None:
        errors.append("review missing ## Design Answer Method Check")
        return
    if not labeled_block_has_content(body, "Findings"):
        errors.append("review Design Answer Method Check section has no meaningful findings")


def check_goal_purpose_feedback(goal: str, errors: list[str]) -> None:
    body = section_body(goal, "How We Know The User Purpose Was Met")
    if body is None:
        errors.append("goal missing ## How We Know The User Purpose Was Met")
        return

    required_fields = [
        "Beneficiary / observer",
        "Purpose-realizing outcome observed",
        "Supporting Evidence",
        "Sufficient evidence level",
        "If user-purpose evidence unavailable",
        "Allowed completion wording",
    ]
    for field in required_fields:
        if not labeled_or_table_field_has_content(body, field):
            errors.append(f"goal How We Know The User Purpose Was Met missing {field}")


def check_review_purpose_feedback(review: str, errors: list[str]) -> None:
    independence = section_body(review, "Review Independence")
    if independence is None:
        errors.append("review missing ## Review Independence for User Purpose Evidence Check")
    else:
        reviewed = yes_no_value(independence, "User purpose evidence check")
        if reviewed != "yes":
            errors.append("review did not record User purpose evidence check: yes in ## Review Independence")

    body = section_body(review, "User Purpose Evidence Check")
    if body is None:
        errors.append("review missing ## User Purpose Evidence Check")
        return
    if not labeled_block_has_content(body, "Findings"):
        errors.append("review User Purpose Evidence Check section has no meaningful findings")


def check_goal_realization_place(goal: str, errors: list[str]) -> None:
    body = section_body(goal, "Where The Result Must Show Up")
    if body is None:
        errors.append("goal missing ## Where The Result Must Show Up")
        return

    required_fields = [
        "Target state",
        "Required result places",
        "Place actions",
        "Residual reconciliation",
        "Result-placement wording",
        "Partial/unavailable handling",
        "Distinction from user-purpose evidence",
    ]
    for field in required_fields:
        if not labeled_or_table_field_has_content(body, field):
            errors.append(f"goal Where The Result Must Show Up missing {field}")


NON_ACHIEVED_SUCCESS_TERMS = ("fallback", "partial", "diagnostic", "blocked", "invalid", "unavailable")
TARGET_CONTRACT_FORBIDDEN_TERMS = (
    "fallback report handling",
    "valid report-when-not-done statuses",
    "report-when-not-done statuses",
    "not done report",
    "report when not done status",
    "report when not done statuses",
    "reports when not done",
    "not done status",
    "not done statuses",
    "report-when-not-done status",
    "report-when-not-done statuses",
    "valid final status",
)


def is_prohibition_line(line: str) -> bool:
    lowered = re.sub(r"^[-*]\s*", "", line.strip()).casefold()
    return (
        lowered.startswith("no ")
        or " must not " in lowered
        or " cannot " in lowered
        or " may not " in lowered
        or "not target states" in lowered
    )


def check_goal_target_achievement(goal: str, errors: list[str]) -> None:
    body = section_body(goal, "What Counts As Done")
    if body is None:
        errors.append("goal missing ## What Counts As Done")
        return

    required_fields = [
        "What counts as done",
        "Evidence needed to call it done",
        "Allowed achieved claim",
        "Steps that make the result true",
    ]
    for field in required_fields:
        if not labeled_or_table_field_has_content(body, field):
            errors.append(f"goal What Counts As Done missing {field}")

    condition_count = target_achieved_condition_field_count(body)
    if condition_count != 1:
        errors.append("goal What Counts As Done must contain exactly one What counts as done field")

    for line in body.splitlines():
        lowered = line.casefold()
        if is_prohibition_line(line):
            continue
        for term in TARGET_CONTRACT_FORBIDDEN_TERMS:
            if term in lowered:
                errors.append(f"goal What Counts As Done contains not done or fallback term: {term}")

    success = section_body(goal, "Success Condition")
    if success is None:
        errors.append("goal missing ## Success Condition")
        return

    for line in success.splitlines():
        if is_prohibition_line(line):
            continue
        lowered = line.casefold()
        for term in NON_ACHIEVED_SUCCESS_TERMS:
            if re.search(rf"\b{re.escape(term)}\b", lowered):
                errors.append(f"goal Success Condition contains not done report term: {term}")


def check_goal_execution_horizon_authority(goal: str, errors: list[str]) -> None:
    body = section_body(goal, "Work Covered And Allowed Actions Contract")
    if body is None:
        errors.append("goal missing ## Work Covered And Allowed Actions Contract")
        return

    required_fields = [
        "Work covered in this run",
        "What the agent may do",
        "Forbidden actions",
        "Prepare-only / observe-only actions",
        "Explicitly out-of-scope items",
        "Work coverage rule",
    ]
    for field in required_fields:
        if not labeled_or_table_field_has_content(body, field):
            errors.append(f"goal Work Covered And Allowed Actions Contract missing {field}")


def target_achieved_condition_field_count(text: str) -> int:
    count = 0
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or is_prohibition_line(stripped):
            continue
        if "|" in stripped:
            cells = [cell.strip().casefold() for cell in stripped.strip("|").split("|")]
            if cells and "what counts as done" in cells[0]:
                count += 1
            continue
        label = stripped.split(":", 1)[0].strip("-* ").casefold()
        if "what counts as done" in label:
            count += 1
    return count


def check_plan_target_producing_strategy(plan: str, errors: list[str]) -> None:
    body = section_body(plan, "Action That Can Make It Done")
    if body is None:
        errors.append("execution policy missing ## Action That Can Make It Done")
        return

    required_fields = [
        "Action that can make it done",
        "Proof of impossibility, if any",
        "Non-achieved terminal report rule",
    ]
    for field in required_fields:
        if not labeled_or_table_field_has_content(body, field):
            errors.append(f"execution policy Action That Can Make It Done missing {field}")


def check_plan_target_producing_spine(plan: str, errors: list[str]) -> None:
    body = section_body(plan, "Steps That Make The Result True")
    if body is None:
        errors.append("execution policy missing ## Steps That Make The Result True")
        return

    lowered = body.casefold()
    required_columns = [
        "required step",
        "required state transition",
        "required evidence",
    ]
    for column in required_columns:
        if column not in lowered:
            errors.append(f"execution policy Steps That Make The Result True missing {column}")

    has_data_row = False
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
        if len(cells) >= len(required_columns) and all(meaningful_line(cell) for cell in cells[: len(required_columns)]):
            has_data_row = True

    if not has_data_row:
        errors.append("execution policy Steps That Make The Result True has no meaningful required step rows")


def check_candidate_plan_tasks_spine_nodes(plan: str, errors: list[str]) -> None:
    body = section_body(plan, "Candidate Plan Tasks")
    if body is None:
        errors.append("execution policy missing ## Candidate Plan Tasks")
        return

    task_matches = list(re.finditer(r"(?m)^###\s+(.+?)\s*$", body))
    if not task_matches:
        errors.append("execution policy Candidate Plan Tasks has no candidate tasks")
        return

    for index, match in enumerate(task_matches):
        start = match.end()
        end = task_matches[index + 1].start() if index + 1 < len(task_matches) else len(body)
        task_body = body[start:end]
        task_name = match.group(1).strip()
        required_fields = [
            "Required step(s)",
            "Role",
            "State transition advanced",
            "Transition evidence produced",
            "Integration check",
            "Counts as goal progress",
            "Why this is not merely component completion",
        ]
        for field in required_fields:
            if not labeled_or_table_field_has_content(task_body, field):
                errors.append(f"execution policy Candidate Plan Task missing {field}: {task_name}")


def check_plan_horizon_authority(plan: str, errors: list[str]) -> None:
    body = section_body(plan, "Work Coverage And Action Limits Matrix")
    if body is None:
        errors.append("execution policy missing ## Work Coverage And Action Limits Matrix")
        return

    lowered = body.casefold()
    required_columns = [
        "work item / place",
        "in work covered in this run?",
        "what the agent may do",
        "required runtime handling",
        "counts as achieved?",
    ]
    for column in required_columns:
        if column not in lowered:
            errors.append(f"execution policy Work Coverage And Action Limits Matrix missing {column}")

    has_data_row = False
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
        if len(cells) >= len(required_columns) and all(meaningful_line(cell) for cell in cells[: len(required_columns)]):
            has_data_row = True
        if "future roadmap" in row_lowered:
            errors.append("execution policy future roadmap cannot replace work covered in this run in ## Work Coverage And Action Limits Matrix")

    if not has_data_row:
        errors.append("execution policy Work Coverage And Action Limits Matrix has no meaningful coverage rows")


def check_plan_realization_place(plan: str, errors: list[str]) -> None:
    body = section_body(plan, "Where The Result Must Show Up")
    if body is None:
        errors.append("execution policy missing ## Where The Result Must Show Up")
        return

    if plan_realization_place_not_applicable(body):
        return

    required_sections = [
        "Places The Result Appears",
        "Place Classes",
        "Residual Reconciliation",
    ]
    for heading in required_sections:
        if not section_has_meaningful_content(body, heading):
            errors.append(f"execution policy Where The Result Must Show Up missing {heading}")


def plan_realization_place_not_applicable(body: str) -> bool:
    status = labeled_value(body, "Result placement status")
    if status is None or status.casefold() != "not applicable with justification":
        return False

    required_fields = [
        "Why no intended-result result placement is required",
        "Why no place discovery / residual reconciliation is needed",
        "Allowed result claim wording",
    ]
    return all(labeled_or_table_field_has_content(body, field) for field in required_fields)


def check_review_realization_place(review: str, errors: list[str]) -> None:
    independence = section_body(review, "Review Independence")
    if independence is None:
        errors.append("review missing ## Review Independence for Result Placement Check")
    else:
        reviewed = yes_no_value(independence, "Result placement check")
        if reviewed != "yes":
            errors.append("review did not record Result placement check: yes in ## Review Independence")

    body = section_body(review, "Result Placement Check")
    if body is None:
        errors.append("review missing ## Result Placement Check")
        return
    if not labeled_block_has_content(body, "Findings"):
        errors.append("review Result Placement Check section has no meaningful findings")


def check_review_target_achievement_condition(review: str, errors: list[str]) -> None:
    independence = section_body(review, "Review Independence")
    if independence is None:
        errors.append("review missing ## Review Independence for What Counts As Done Check")
    else:
        reviewed = yes_no_value(independence, "What counts as done check")
        if reviewed != "yes":
            errors.append("review did not record What counts as done check: yes in ## Review Independence")

    body = section_body(review, "What Counts As Done Check")
    if body is None:
        errors.append("review missing ## What Counts As Done Check")
        return
    if not labeled_block_has_content(body, "Findings"):
        errors.append("review What Counts As Done Check section has no meaningful findings")


def check_review_target_producing_spine(review: str, errors: list[str]) -> None:
    independence = section_body(review, "Review Independence")
    if independence is None:
        errors.append("review missing ## Review Independence for Answer Path Check")
    else:
        reviewed = yes_no_value(independence, "answer path check")
        if reviewed != "yes":
            errors.append("review did not record answer path check: yes in ## Review Independence")

    body = section_body(review, "Answer Path Check")
    if body is None:
        errors.append("review missing ## Answer Path Check")
        return
    if not labeled_block_has_content(body, "Findings"):
        errors.append("review Answer Path Check section has no meaningful findings")


def check_review_execution_horizon_authority(review: str, errors: list[str]) -> None:
    independence = section_body(review, "Review Independence")
    if independence is None:
        errors.append("review missing ## Review Independence for Work Covered And Allowed Actions Check")
    else:
        reviewed = yes_no_value(independence, "Work covered in this run and authority check")
        if reviewed != "yes":
            errors.append("review did not record Work covered in this run and authority check: yes in ## Review Independence")

    body = section_body(review, "Work Covered And Allowed Actions Check")
    if body is None:
        errors.append("review missing ## Work Covered And Allowed Actions Check")
        return
    if not labeled_block_has_content(body, "Findings"):
        errors.append("review Work Covered And Allowed Actions Check section has no meaningful findings")


def suggest_next_action(errors: list[str]) -> str:
    joined = "\n".join(errors).casefold()
    lowered_errors = [error.casefold() for error in errors]

    if (
        "requirements analysis status is not complete" in joined
        or "requirements missing ## what the user approved" in joined
        or "what the user approved is not approved" in joined
        or "requirements control sidecar" in joined
        or "records conflicting agent workflow preference" in joined
    ):
        return "ReturnToRequirementsAnalysis"
    if (
        "design check is required" in joined
        or "design status" in joined
        or "design does not reference" in joined
        or ("answer method check" in joined and "review" not in joined)
    ):
        return "RunDesign"
    if (
        "output contract" in joined
        or "goal lacks" in joined
        or "goal contains runtime control-structure" in joined
        or "goal artifact hygiene" in joined
        or "goal missing ## purpose feedback contract" in joined
        or "goal purpose feedback contract missing" in joined
        or "goal missing ## how we know the user purpose was met" in joined
        or "goal how we know the user purpose was met missing" in joined
        or "goal missing ## realization place contract" in joined
        or "goal realization place contract missing" in joined
        or "goal missing ## where the result must show up" in joined
        or "goal where the result must show up missing" in joined
        or "goal missing ## target achievement contract" in joined
        or "goal target achievement contract missing" in joined
        or "goal missing ## what counts as done" in joined
        or "goal what counts as done missing" in joined
        or "goal what counts as done must contain exactly one what counts as done field" in joined
        or "goal what counts as done contains not done or fallback term" in joined
        or "goal target achievement contract missing steps that make the result true" in joined
        or "goal missing ## work covered and allowed actions contract" in joined
        or "goal work covered in this run and authority contract missing" in joined
        or "goal target achievement contract must contain exactly one what counts as done field" in joined
        or "goal success condition contains not done report term" in joined
        or "goal target achievement contract contains not done or fallback term" in joined
    ):
        return "RunGoalWriting"
    if (
        "execution policy status" in joined
        or "plan artifact hygiene" in joined
        or "execution policy missing ## where the result must show up" in joined
        or "execution policy missing ## action that can make it done" in joined
        or "execution policy missing ## realization place completion strategy" in joined
        or "execution policy realization place completion strategy missing" in joined
        or "execution policy missing ## action that can make it done strategy" in joined
        or "execution policy action that can make it done strategy missing" in joined
        or "execution policy missing ## steps that make the result true" in joined
        or "execution policy steps that make the result true" in joined
        or "execution policy missing ## candidate plan tasks" in joined
        or "execution policy candidate plan task missing" in joined
        or "candidate plan tasks has no candidate tasks" in joined
        or "execution policy missing ## work coverage and action limits matrix" in joined
        or "execution policy work coverage and action limits matrix" in joined
        or "future roadmap cannot replace work covered in this run" in joined
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
        or any(
            error.startswith(
                (
                    "execution work assignment",
                    "subagent-driven work assignment",
                    "level 3/4 main-only",
                    "parallel execution work assignment",
                )
            )
            for error in lowered_errors
        )
    ):
        return "RunExecutionPolicy"
    if (
        "review status" in joined
        or "review artifact hygiene" in joined
        or "final observer" in joined
        or "post-review" in joined
        or "deterministic-only exception" in joined
        or "review does not reference" in joined
        or "review missing ## review independence" in joined
        or "review missing ## who does the work / context use" in joined
        or "review missing ## user purpose evidence check" in joined
        or "review missing ## result placement check" in joined
        or "review missing ## result placement check" in joined
        or "review missing ## what counts as done check" in joined
        or "review missing ## work covered and allowed actions check" in joined
        or "review missing ## subagent concurrency check" in joined
        or "review missing ## context management / execution work assignment" in joined
        or "review missing ## design answer method check" in joined
        or "review missing ## purpose feedback adequacy" in joined
        or "review missing ## realization place completion adequacy" in joined
        or "review missing ## target achievement condition check" in joined
        or "review missing ## answer path check" in joined
        or "review missing ## work covered in this run and authority check" in joined
        or "review missing ## subagent concurrency check" in joined
        or "design answer method check section has no meaningful findings" in joined
        or "purpose feedback adequacy section has no meaningful findings" in joined
        or "realization place completion adequacy section has no meaningful findings" in joined
        or "target achievement condition check section has no meaningful findings" in joined
        or "answer path check section has no meaningful findings" in joined
        or "work covered in this run and authority check section has no meaningful findings" in joined
        or "subagent concurrency check section has no meaningful findings" in joined
        or "did not record design answer method check" in joined
        or "did not record user purpose evidence check" in joined
        or "did not record result placement check" in joined
        or "did not record result placement check" in joined
        or "did not record what counts as done check" in joined
        or "did not record work covered in this run and authority check" in joined
        or "did not record subagent concurrency check" in joined
        or "did not record purpose feedback adequacy" in joined
        or "did not record realization place completion adequacy" in joined
        or "did not record target achievement condition check" in joined
        or "did not record answer path check" in joined
        or "did not record work covered in this run and authority check" in joined
        or "did not record subagent concurrency check" in joined
        or "context management / execution work assignment section has no meaningful findings" in joined
        or "did not record context management / execution work assignment" in joined
    ):
        return "RunReview"
    if "missing file" in joined:
        return "ProvideMissingArtifact"
    if "requirements artifact hygiene" in joined:
        return "ReturnToRequirementsAnalysis"
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
        check_artifact_hygiene("requirements", requirements, errors)
        requirements_status = first_section_status(requirements, "Requirements Analysis Status", "Clarification Status")
        if requirements_status != "Complete":
            errors.append(f"requirements analysis status is not Complete: {requirements_status!r}")
        check_human_approved_target_approval(requirements, errors)

    if design:
        check_artifact_hygiene("design", design, errors)
        design_status = section_status(design, "Design Status")
        if design_status not in {"Candidate", "Reviewed", "Approved"}:
            errors.append(f"design status under ## Design Status must be Candidate, Reviewed, or Approved: {design_status!r}")
        if args.requirements not in design:
            errors.append(f"design does not reference required requirements path: {args.requirements}")
        if output_contract_check_required(requirements, design) and not output_contract_present_upstream(requirements, design):
            errors.append("Final Answer Format Check is required but no upstream output contract is present")
        check_design_answer_path_check(args.requirements, requirements, design, errors)
    elif design_check_required(requirements, goal, plan, review):
        errors.append("Design Check is required but --design was not provided")

    if goal and output_contract_required(requirements, design or "", goal) and not section_has_meaningful_content(goal, "Final Final Answer Format"):
        errors.append("Output contract is required by check or upstream artifact, but goal lacks meaningful ## Final Final Answer Format")

    if goal:
        check_artifact_hygiene("goal", goal, errors)
        check_goal_purpose_feedback(goal, errors)
        check_goal_realization_place(goal, errors)
        check_goal_target_achievement(goal, errors)
        check_goal_execution_horizon_authority(goal, errors)

    if plan:
        check_artifact_hygiene("plan", plan, errors)
        plan_status = section_status(plan, "Execution Policy Status")
        if plan_status != "Candidate":
            errors.append(f"execution policy status under ## Execution Policy Status must be Candidate: {plan_status!r}")
        check_plan_realization_place(plan, errors)
        check_plan_target_producing_strategy(plan, errors)
        check_plan_target_producing_spine(plan, errors)
        check_candidate_plan_tasks_spine_nodes(plan, errors)
        check_plan_horizon_authority(plan, errors)
        check_execution_work_assignment(plan, errors)
        check_max_safe_parallel_preference(requirements, plan, errors)
        check_delegation_workflow_preference(requirements, plan, errors)

    if review:
        check_artifact_hygiene("review", review, errors)
        review_status = section_status(review, "Review Status")
        if review_status != "Approved":
            errors.append(f"review status under ## Review Status is not Approved: {review_status!r}")
        check_final_observer(review, errors)
        check_review_design_answer_path(requirements, review, errors)
        check_review_context_work_assignment(review, errors)
        if plan:
            check_review_subagent_concurrency(plan, review, errors)
        check_review_purpose_feedback(review, errors)
        check_review_realization_place(review, errors)
        check_review_target_achievement_condition(review, errors)
        check_review_target_producing_spine(review, errors)
        check_review_execution_horizon_authority(review, errors)

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
