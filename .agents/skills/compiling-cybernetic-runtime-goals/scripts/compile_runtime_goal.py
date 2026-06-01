#!/usr/bin/env python3
"""Compile a final runtime /goal command from approved control artifacts."""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path


HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$", re.MULTILINE)


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


def final_output_contract_clause(goal_path: str) -> str:
    goal = Path(goal_path).read_text(encoding="utf-8")
    body = section_body(goal, "Final Output Contract")
    if body is None:
        return ""
    if not body.strip():
        return ""

    return (
        f"Follow the Final Output Contract section in {goal_path}. "
        "Do not substitute a different audience, purpose, medium, structure, detail level, destination, or machine-readable shape. "
    )


def selected_execution_topology(plan_path: str) -> str | None:
    plan = Path(plan_path).read_text(encoding="utf-8")
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
    if "parallel" in lowered and "subagent" in lowered:
        return "Parallel subagent-driven"
    if "serial" in lowered and "subagent" in lowered:
        return "Serial subagent-driven"
    if "main-only" in lowered or "main only" in lowered:
        return "Main-only"
    return None


def topology_section(plan_path: str) -> str:
    plan = Path(plan_path).read_text(encoding="utf-8")
    return section_body(plan, "Context Management / Execution Topology") or ""


def selected_superpowers_subagent_workflow(plan_path: str) -> bool:
    for line in topology_section(plan_path).splitlines():
        lowered = line.casefold()
        if "subagent-driven-development" not in lowered:
            continue
        if "[" in line and "]" in line:
            continue
        if "do not" in lowered or "does not" in lowered or "not use" in lowered:
            continue
        return True
    return False


def conditional_subagent_workflow_clause(plan_path: str) -> str:
    if not selected_superpowers_subagent_workflow(plan_path):
        return ""
    return (
        "The approved plan explicitly selects `$superpowers:subagent-driven-development`; use it only when the approved plan's work packages match that workflow. "
    )


def execution_topology_clause(plan_path: str) -> str:
    topology = selected_execution_topology(plan_path)
    base = f"Use the approved execution topology defined in {plan_path}. "

    if topology == "Serial subagent-driven":
        return (
            base +
            "Because the approved topology is Serial subagent-driven, use the approved bounded subagent delegation protocol defined in the plan with only one execution subagent active at a time. "
            f"{conditional_subagent_workflow_clause(plan_path)}"
            "The main agent coordinates, integrates, maintains the progress log, and detects stop conditions; it must not personally absorb delegated bounded work packages. "
            "Subagents may execute only the bounded work packages, context packs, allowed actions, return formats, and integration gates defined in the approved plan. "
            "Subagent outputs are candidate results until the main agent integrates them against the approved control artifacts, progress log, evidence requirements, and stop conditions. "
        )

    if topology == "Parallel subagent-driven":
        return (
            base +
            "Because the approved topology is Parallel subagent-driven, use the approved bounded subagent delegation protocol defined in the plan and spawn subagents only for work packages explicitly marked independent by the dependency matrix and approved control review. "
            f"{conditional_subagent_workflow_clause(plan_path)}"
            "The main agent coordinates, integrates, maintains the progress log, and detects stop conditions; it must not personally absorb delegated bounded work packages. "
            "Subagents may execute only the bounded work packages, context packs, allowed actions, return formats, and integration gates defined in the approved plan. "
            "Subagent outputs are candidate results until the main agent integrates them against the approved control artifacts, progress log, evidence requirements, and stop conditions. "
        )

    if topology == "Main-only":
        return (
            base +
            "Because the approved topology is Main-only, do not dispatch target-work subagents unless the execution policy is revised and reviewed. "
        )

    return base


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--requirements", dest="requirements")
    ap.add_argument("--clarification", dest="requirements", help="Deprecated alias for --requirements")
    ap.add_argument("--design")
    ap.add_argument("--goal", required=True)
    ap.add_argument("--plan", required=True)
    ap.add_argument("--review", required=True)
    ap.add_argument("--out")
    ap.add_argument("--skip-guard", action="store_true", help="Internal validation only. Bypasses phase-gate checks and must not be used for official runtime goal compilation.")
    ap.add_argument("--i-understand-this-bypasses-phase-gates", action="store_true", help="Required with --skip-guard to make phase-gate bypass explicit.")
    args = ap.parse_args()
    if not args.requirements:
        ap.error("--requirements is required")

    here = Path(__file__).resolve().parent
    guard = here / "control_chain_guard.py"
    if args.skip_guard and not args.i_understand_this_bypasses_phase_gates:
        print("ERROR: --skip-guard is for internal validation only and requires --i-understand-this-bypasses-phase-gates", file=sys.stderr)
        return 2
    if not args.skip_guard:
        cmd = [sys.executable, str(guard), "--requirements", args.requirements, "--goal", args.goal, "--plan", args.plan, "--review", args.review]
        if args.design:
            cmd.extend(["--design", args.design])
        result = subprocess.run(cmd, text=True, capture_output=True)
        if result.returncode != 0:
            sys.stdout.write(result.stdout)
            sys.stderr.write(result.stderr)
            return result.returncode

    design_boundary = "rewrite the solution design, " if args.design else ""
    design_sensor_clause = " or solution-design invariants" if args.design else ""
    conflict_clause = "design, " if args.design else ""
    if args.design:
        context_clause = (
            f"under the control contract in {args.goal}, "
            f"the confirmed requirements in {args.requirements}, "
            f"and the solution design in {args.design}. "
        )
    else:
        context_clause = (
            f"under the control contract in {args.goal} "
            f"and the confirmed requirements in {args.requirements}. "
        )

    output_contract_clause = final_output_contract_clause(args.goal)
    topology_clause = execution_topology_clause(args.plan)

    command = (
        f"/goal Execute the approved execution policy in {args.plan} "
        f"{context_clause}"
        f"Use the approved control review in {args.review} as the phase-gate record. "
        f"{output_contract_clause}"
        f"Do not reinterpret requirements, {design_boundary}rewrite the control strategy, replace approved sensors, or start unreviewed work. "
        "Use `$superpowers:executing-plans` discipline against the approved plan. "
        "Use `$superpowers:systematic-debugging` for unclear or repeated failures. "
        "Use `$superpowers:verification-before-completion` before claiming completion. "
        "If runtime cannot load these skills, follow the equivalent discipline already written in the approved plan and control review. "
        f"{topology_clause}"
        "Follow the approved batch rhythm. "
        "Intermediate states inside a batch may be broken if the approved plan allows it, but each batch must end in the approved openable/verifiable state. "
        f"Treat approved sensors, checks, and evidence channels as sensors, not objectives; if an evidence channel conflicts with confirmed requirements{design_sensor_clause}, stop or follow the approved sensor-governance rule. "
        "If any referenced artifact is missing, not approved, or internally inconsistent, stop and report the smallest required human decision. "
        f"If the requirements analysis, {conflict_clause}goal, plan, or review conflict or become insufficient, stop and report the smallest required human decision."
    )

    if args.out:
        Path(args.out).write_text(command + "\n", encoding="utf-8")
    print(command)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
