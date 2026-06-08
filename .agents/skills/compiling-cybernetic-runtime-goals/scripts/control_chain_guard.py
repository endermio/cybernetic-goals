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


def selected_delegation_substrate(plan: str | None) -> str | None:
    body = section_body(plan or "", "Context Management / Execution Topology")
    if body is None:
        return None
    match = re.search(r"(?im)^\s*Selected delegation substrate\s*:\s*`?([^`\n]+?)`?\s*$", body)
    if not match:
        return None

    value = match.group(1).strip().strip("`").casefold()
    if "/" in value:
        return None
    if value in {"bounded-protocol", "bounded protocol"}:
        return "bounded-protocol"
    if value in {"superpowers-subagent-driven-development", "$superpowers:subagent-driven-development"}:
        return "superpowers-subagent-driven-development"
    if value in {"adapter-specific", "adapter specific"}:
        return "adapter-specific"
    if value == "none":
        return "none"
    return None


def task_level(plan: str | None) -> int | None:
    body = section_body(plan or "", "Context Management / Execution Topology")
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


CONTEXT_PACK_FIELDS = [
    "Relevant control excerpts",
    "Current batch objective",
    "Allowed artifacts/surfaces",
    "Forbidden changes",
    "Required sensors/evidence",
    "Stop conditions",
    "Expected return format",
]

CONTEXT_COMPRESSION_FIELDS = [
    "Active control summary",
    "Completed work packages",
    "Subagent outputs integrated",
    "Evidence produced",
    "Deferred sensors and reasons",
    "Unresolved blockers",
    "Deviations from policy",
    "Next allowed action",
]


def check_labeled_requirements(body: str, heading: str, labels: list[str], errors: list[str]) -> None:
    if heading.casefold() not in body.casefold():
        errors.append(f"execution topology missing {heading}: {', '.join(labels)}")
        return
    for label in labels:
        if not labeled_or_table_field_has_content(body, label):
            errors.append(f"execution topology {heading} missing {label}")


def check_execution_topology(plan: str | None, errors: list[str]) -> None:
    body = section_body(plan or "", "Context Management / Execution Topology")
    if body is None:
        errors.append("execution policy missing ## Context Management / Execution Topology")
        return

    topology = selected_execution_topology(plan)
    if topology is None:
        errors.append("execution policy must define a selected Context Management / Execution Topology")
        return

    if not labeled_block_has_content(body, "Topology rationale"):
        errors.append("execution topology missing Topology rationale")
    if not labeled_block_has_content(body, "Main agent owns"):
        errors.append("execution topology missing main-agent ownership")

    level = task_level(plan)
    if level is None:
        errors.append("execution topology missing Task level")
    if topology == "Main-only" and level in {3, 4} and not labeled_block_has_content(body, "Main-only context-load justification"):
        errors.append("Level 3/4 Main-only execution topology missing Main-only context-load justification")

    if topology in {"Serial subagent-driven", "Parallel subagent-driven"}:
        if not has_meaningful_delegation_matrix(body):
            errors.append("execution topology missing meaningful delegation matrix with Context pack, Allowed actions, Return format, and Integration gate")
        check_labeled_requirements(body, "Context Pack Requirements", CONTEXT_PACK_FIELDS, errors)
        substrate = selected_delegation_substrate(plan)
        if substrate is None:
            errors.append("subagent-driven topology missing valid Selected delegation substrate")
        elif substrate == "none":
            errors.append("subagent-driven topology cannot use Selected delegation substrate: none")
        if not labeled_block_has_content(body, "Subagent delegation substrate"):
            errors.append("subagent-driven topology missing approved bounded subagent delegation substrate")

    if topology in {"Serial subagent-driven", "Parallel subagent-driven"} or level in {3, 4}:
        check_labeled_requirements(body, "Context Compression Rule", CONTEXT_COMPRESSION_FIELDS, errors)

    if topology == "Parallel subagent-driven":
        for label in ("Human approval", "Dependency independence", "Control-review approval"):
            if not approval_value_is_yes(body, label):
                errors.append(f"parallel execution topology requires {label}: yes/approved")


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


def check_review_context_topology(review: str, errors: list[str]) -> None:
    independence = section_body(review, "Review Independence")
    if independence is None:
        errors.append("control review missing ## Review Independence for Context Management / Execution Topology")
    else:
        topology_reviewed = yes_no_value(independence, "Context management / execution topology")
        if topology_reviewed != "yes":
            errors.append(
                "control review did not record Context management / execution topology: yes in ## Review Independence"
            )

    body = section_body(review, "Context Management / Execution Topology")
    if body is None:
        errors.append("control review missing ## Context Management / Execution Topology")
        return
    if not labeled_block_has_content(body, "Findings"):
        errors.append("control review Context Management / Execution Topology section has no meaningful findings")


def check_human_setpoint_approval(requirements: str, errors: list[str]) -> None:
    body = section_body(requirements, "Human Setpoint Approval")
    if body is None:
        errors.append("requirements missing ## Human Setpoint Approval")
        return

    status = section_status(requirements, "Human Setpoint Approval")
    if status != "Approved":
        errors.append(f"Human Setpoint Approval is not Approved: {status!r}")


def check_goal_purpose_feedback(goal: str, errors: list[str]) -> None:
    body = section_body(goal, "Purpose Feedback Contract")
    if body is None:
        errors.append("goal missing ## Purpose Feedback Contract")
        return

    required_fields = [
        "Beneficiary / observer",
        "Purpose-realizing outcome observed",
        "Supporting Evidence",
        "Sufficient evidence level",
        "Purpose feedback unavailable handling",
        "Allowed completion wording",
    ]
    for field in required_fields:
        if not labeled_or_table_field_has_content(body, field):
            errors.append(f"goal Purpose Feedback Contract missing {field}")


def check_review_purpose_feedback(review: str, errors: list[str]) -> None:
    independence = section_body(review, "Review Independence")
    if independence is None:
        errors.append("control review missing ## Review Independence for Purpose Feedback Adequacy")
    else:
        reviewed = yes_no_value(independence, "Purpose feedback adequacy")
        if reviewed != "yes":
            errors.append("control review did not record Purpose feedback adequacy: yes in ## Review Independence")

    body = section_body(review, "Purpose Feedback Adequacy")
    if body is None:
        errors.append("control review missing ## Purpose Feedback Adequacy")
        return
    if not labeled_block_has_content(body, "Findings"):
        errors.append("control review Purpose Feedback Adequacy section has no meaningful findings")


def check_goal_realization_surface(goal: str, errors: list[str]) -> None:
    body = section_body(goal, "Realization Surface Contract")
    if body is None:
        errors.append("goal missing ## Realization Surface Contract")
        return

    required_fields = [
        "Target state",
        "Required surfaces",
        "Surface actions",
        "Residual reconciliation",
        "RSC status wording",
        "Partial/unavailable handling",
        "RSC / PFB boundary",
    ]
    for field in required_fields:
        if not labeled_or_table_field_has_content(body, field):
            errors.append(f"goal Realization Surface Contract missing {field}")


NON_ACHIEVED_SUCCESS_TERMS = ("fallback", "partial", "diagnostic", "blocked", "invalid", "unavailable")
TARGET_CONTRACT_FORBIDDEN_TERMS = (
    "fallback report handling",
    "valid non-achieved report statuses",
    "non-achieved report statuses",
    "non-achieved terminal report",
    "non-achieved terminal reports",
    "non-achieved terminal report status",
    "non-achieved terminal report statuses",
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
    body = section_body(goal, "Target Achievement Contract")
    if body is None:
        errors.append("goal missing ## Target Achievement Contract")
        return

    required_fields = [
        "Single target-achieved predicate",
        "Required target-producing evidence",
        "Allowed achieved claim",
        "Target-producing spine",
    ]
    for field in required_fields:
        if not labeled_or_table_field_has_content(body, field):
            errors.append(f"goal Target Achievement Contract missing {field}")

    predicate_count = target_achieved_predicate_field_count(body)
    if predicate_count != 1:
        errors.append("goal Target Achievement Contract must contain exactly one target-achieved predicate")

    for line in body.splitlines():
        lowered = line.casefold()
        if is_prohibition_line(line):
            continue
        for term in TARGET_CONTRACT_FORBIDDEN_TERMS:
            if term in lowered:
                errors.append(f"goal Target Achievement Contract contains non-achieved or fallback term: {term}")

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
                errors.append(f"goal Success Condition contains non-achieved terminal report term: {term}")


def check_goal_execution_horizon_authority(goal: str, errors: list[str]) -> None:
    body = section_body(goal, "Execution Horizon and Authority Contract")
    if body is None:
        errors.append("goal missing ## Execution Horizon and Authority Contract")
        return

    required_fields = [
        "Approved horizon",
        "Runtime-authorized actions",
        "Forbidden actions",
        "Prepare-only / observe-only actions",
        "Explicitly out-of-scope items",
        "Horizon completion rule",
    ]
    for field in required_fields:
        if not labeled_or_table_field_has_content(body, field):
            errors.append(f"goal Execution Horizon and Authority Contract missing {field}")


def target_achieved_predicate_field_count(text: str) -> int:
    count = 0
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or is_prohibition_line(stripped):
            continue
        if "|" in stripped:
            cells = [cell.strip().casefold() for cell in stripped.strip("|").split("|")]
            if cells and "target-achieved predicate" in cells[0]:
                count += 1
            continue
        label = stripped.split(":", 1)[0].strip("-* ").casefold()
        if "target-achieved predicate" in label:
            count += 1
    return count


def check_plan_target_producing_strategy(plan: str, errors: list[str]) -> None:
    body = section_body(plan, "Target-Producing Action Strategy")
    if body is None:
        errors.append("execution policy missing ## Target-Producing Action Strategy")
        return

    required_fields = [
        "Target-producing action required",
        "Proof of impossibility, if any",
        "Non-achieved terminal report rule",
    ]
    for field in required_fields:
        if not labeled_or_table_field_has_content(body, field):
            errors.append(f"execution policy Target-Producing Action Strategy missing {field}")


def check_plan_target_producing_spine(plan: str, errors: list[str]) -> None:
    body = section_body(plan, "Target-Producing Spine")
    if body is None:
        errors.append("execution policy missing ## Target-Producing Spine")
        return

    lowered = body.casefold()
    required_columns = [
        "spine node",
        "required state transition",
        "required evidence",
    ]
    for column in required_columns:
        if column not in lowered:
            errors.append(f"execution policy Target-Producing Spine missing {column}")

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
        errors.append("execution policy Target-Producing Spine has no meaningful spine transition rows")


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
        if not labeled_or_table_field_has_content(task_body, "Spine node(s)"):
            task_name = match.group(1).strip()
            errors.append(f"execution policy Candidate Plan Task missing Spine node(s): {task_name}")


def check_plan_horizon_authority(plan: str, errors: list[str]) -> None:
    body = section_body(plan, "Horizon and Authority Coverage Matrix")
    if body is None:
        errors.append("execution policy missing ## Horizon and Authority Coverage Matrix")
        return

    lowered = body.casefold()
    required_columns = [
        "batch / surface",
        "in approved horizon?",
        "runtime authority",
        "required runtime handling",
        "counts as achieved?",
    ]
    for column in required_columns:
        if column not in lowered:
            errors.append(f"execution policy Horizon and Authority Coverage Matrix missing {column}")

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
            errors.append("execution policy future roadmap cannot replace approved horizon in ## Horizon and Authority Coverage Matrix")

    if not has_data_row:
        errors.append("execution policy Horizon and Authority Coverage Matrix has no meaningful coverage rows")


def check_plan_realization_surface(plan: str, errors: list[str]) -> None:
    body = section_body(plan, "Realization Surface Closure Strategy")
    if body is None:
        errors.append("execution policy missing ## Realization Surface Closure Strategy")
        return

    if plan_realization_surface_not_applicable(body):
        return

    required_sections = [
        "Surface Model",
        "Surface Classes",
        "Residual Reconciliation",
    ]
    for heading in required_sections:
        if not section_has_meaningful_content(body, heading):
            errors.append(f"execution policy Realization Surface Closure Strategy missing {heading}")


def plan_realization_surface_not_applicable(body: str) -> bool:
    status = labeled_value(body, "RSC status")
    if status is None or status.casefold() != "rsc not applicable with justification":
        return False

    required_fields = [
        "Why no target-state surface closure is required",
        "Why no surface discovery / residual reconciliation is needed",
        "Allowed target-realization wording",
    ]
    return all(labeled_or_table_field_has_content(body, field) for field in required_fields)


def check_review_realization_surface(review: str, errors: list[str]) -> None:
    independence = section_body(review, "Review Independence")
    if independence is None:
        errors.append("control review missing ## Review Independence for Realization Surface Closure Adequacy")
    else:
        reviewed = yes_no_value(independence, "Realization surface closure adequacy")
        if reviewed != "yes":
            errors.append("control review did not record Realization surface closure adequacy: yes in ## Review Independence")

    body = section_body(review, "Realization Surface Closure Adequacy")
    if body is None:
        errors.append("control review missing ## Realization Surface Closure Adequacy")
        return
    if not labeled_block_has_content(body, "Findings"):
        errors.append("control review Realization Surface Closure Adequacy section has no meaningful findings")


def check_review_target_achievement_predicate(review: str, errors: list[str]) -> None:
    independence = section_body(review, "Review Independence")
    if independence is None:
        errors.append("control review missing ## Review Independence for Target Achievement Predicate Fidelity")
    else:
        reviewed = yes_no_value(independence, "Target achievement predicate fidelity")
        if reviewed != "yes":
            errors.append("control review did not record Target achievement predicate fidelity: yes in ## Review Independence")

    body = section_body(review, "Target Achievement Predicate Fidelity")
    if body is None:
        errors.append("control review missing ## Target Achievement Predicate Fidelity")
        return
    if not labeled_block_has_content(body, "Findings"):
        errors.append("control review Target Achievement Predicate Fidelity section has no meaningful findings")


def check_review_target_producing_spine(review: str, errors: list[str]) -> None:
    independence = section_body(review, "Review Independence")
    if independence is None:
        errors.append("control review missing ## Review Independence for Target-Producing Spine Fidelity")
    else:
        reviewed = yes_no_value(independence, "Target-producing spine fidelity")
        if reviewed != "yes":
            errors.append("control review did not record Target-producing spine fidelity: yes in ## Review Independence")

    body = section_body(review, "Target-Producing Spine Fidelity")
    if body is None:
        errors.append("control review missing ## Target-Producing Spine Fidelity")
        return
    if not labeled_block_has_content(body, "Findings"):
        errors.append("control review Target-Producing Spine Fidelity section has no meaningful findings")


def check_review_execution_horizon_authority(review: str, errors: list[str]) -> None:
    independence = section_body(review, "Review Independence")
    if independence is None:
        errors.append("control review missing ## Review Independence for Execution Horizon and Authority Fidelity")
    else:
        reviewed = yes_no_value(independence, "Execution horizon and authority fidelity")
        if reviewed != "yes":
            errors.append("control review did not record Execution horizon and authority fidelity: yes in ## Review Independence")

    body = section_body(review, "Execution Horizon and Authority Fidelity")
    if body is None:
        errors.append("control review missing ## Execution Horizon and Authority Fidelity")
        return
    if not labeled_block_has_content(body, "Findings"):
        errors.append("control review Execution Horizon and Authority Fidelity section has no meaningful findings")


def suggest_next_action(errors: list[str]) -> str:
    joined = "\n".join(errors).casefold()
    lowered_errors = [error.casefold() for error in errors]

    if "requirements analysis status is not complete" in joined or "human setpoint approval" in joined:
        return "ReturnToRequirementsAnalysis"
    if "design gate is required" in joined or "design status" in joined or "design does not reference" in joined:
        return "RunDesign"
    if (
        "output contract" in joined
        or "goal lacks" in joined
        or "goal contains runtime control-structure" in joined
        or "goal artifact hygiene" in joined
        or "goal missing ## purpose feedback contract" in joined
        or "goal purpose feedback contract missing" in joined
        or "goal missing ## realization surface contract" in joined
        or "goal realization surface contract missing" in joined
        or "goal missing ## target achievement contract" in joined
        or "goal target achievement contract missing" in joined
        or "goal target achievement contract missing target-producing spine" in joined
        or "goal missing ## execution horizon and authority contract" in joined
        or "goal execution horizon and authority contract missing" in joined
        or "goal target achievement contract must contain exactly one target-achieved predicate" in joined
        or "goal success condition contains non-achieved terminal report term" in joined
        or "goal target achievement contract contains non-achieved or fallback term" in joined
    ):
        return "RunGoalWriting"
    if (
        "execution policy status" in joined
        or "plan artifact hygiene" in joined
        or "execution policy missing ## realization surface closure strategy" in joined
        or "execution policy realization surface closure strategy missing" in joined
        or "execution policy missing ## target-producing action strategy" in joined
        or "execution policy target-producing action strategy missing" in joined
        or "execution policy missing ## target-producing spine" in joined
        or "execution policy target-producing spine" in joined
        or "execution policy missing ## candidate plan tasks" in joined
        or "execution policy candidate plan task missing spine node(s)" in joined
        or "candidate plan tasks has no candidate tasks" in joined
        or "execution policy missing ## horizon and authority coverage matrix" in joined
        or "execution policy horizon and authority coverage matrix" in joined
        or "future roadmap cannot replace approved horizon" in joined
        or "plan does not reference" in joined
        or any(
            error.startswith(
                (
                    "execution topology",
                    "subagent-driven topology",
                    "level 3/4 main-only",
                    "parallel execution topology",
                )
            )
            for error in lowered_errors
        )
    ):
        return "RunExecutionPolicy"
    if (
        "control review status" in joined
        or "review artifact hygiene" in joined
        or "final observer" in joined
        or "post-review" in joined
        or "deterministic-only exception" in joined
        or "review does not reference" in joined
        or "control review missing ## review independence" in joined
        or "control review missing ## context management / execution topology" in joined
        or "control review missing ## purpose feedback adequacy" in joined
        or "control review missing ## realization surface closure adequacy" in joined
        or "control review missing ## target achievement predicate fidelity" in joined
        or "control review missing ## target-producing spine fidelity" in joined
        or "control review missing ## execution horizon and authority fidelity" in joined
        or "purpose feedback adequacy section has no meaningful findings" in joined
        or "realization surface closure adequacy section has no meaningful findings" in joined
        or "target achievement predicate fidelity section has no meaningful findings" in joined
        or "target-producing spine fidelity section has no meaningful findings" in joined
        or "execution horizon and authority fidelity section has no meaningful findings" in joined
        or "did not record purpose feedback adequacy" in joined
        or "did not record realization surface closure adequacy" in joined
        or "did not record target achievement predicate fidelity" in joined
        or "did not record target-producing spine fidelity" in joined
        or "did not record execution horizon and authority fidelity" in joined
        or "context management / execution topology section has no meaningful findings" in joined
        or "did not record context management / execution topology" in joined
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
        check_human_setpoint_approval(requirements, errors)

    if design:
        check_artifact_hygiene("design", design, errors)
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

    if goal:
        check_artifact_hygiene("goal", goal, errors)
        check_goal_purpose_feedback(goal, errors)
        check_goal_realization_surface(goal, errors)
        check_goal_target_achievement(goal, errors)
        check_goal_execution_horizon_authority(goal, errors)

    if plan:
        check_artifact_hygiene("plan", plan, errors)
        plan_status = section_status(plan, "Execution Policy Status")
        if plan_status != "Candidate":
            errors.append(f"execution policy status under ## Execution Policy Status must be Candidate: {plan_status!r}")
        check_plan_realization_surface(plan, errors)
        check_plan_target_producing_strategy(plan, errors)
        check_plan_target_producing_spine(plan, errors)
        check_candidate_plan_tasks_spine_nodes(plan, errors)
        check_plan_horizon_authority(plan, errors)
        check_execution_topology(plan, errors)

    if review:
        check_artifact_hygiene("review", review, errors)
        review_status = section_status(review, "Review Status")
        if review_status != "Approved":
            errors.append(f"control review status under ## Review Status is not Approved: {review_status!r}")
        check_final_observer(review, errors)
        check_review_context_topology(review, errors)
        check_review_purpose_feedback(review, errors)
        check_review_realization_surface(review, errors)
        check_review_target_achievement_predicate(review, errors)
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
