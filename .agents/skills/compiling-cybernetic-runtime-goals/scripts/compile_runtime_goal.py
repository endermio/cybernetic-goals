#!/usr/bin/env python3
"""Compile a pointer-only runtime /goal and a runtime goal contract artifact."""
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


def selected_execution_topology(plan_path: str) -> str | None:
    plan = Path(plan_path).read_text(encoding="utf-8")
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
    if "parallel" in lowered and "subagent" in lowered:
        return "Parallel subagent-driven"
    if "serial" in lowered and "subagent" in lowered:
        return "Serial subagent-driven"
    if "main-only" in lowered or "main only" in lowered:
        return "Main-only"
    return None


def topology_section(plan_path: str) -> str:
    plan = Path(plan_path).read_text(encoding="utf-8")
    return section_body(plan, "Who Does The Work / Context Use") or ""


def selected_delegation_workflow(plan_path: str) -> str | None:
    body = topology_section(plan_path)
    match = re.search(r"(?im)^\s*Selected agent workflow\s*:\s*`?([^`\n]+?)`?\s*$", body)
    if not match:
        return None

    value = match.group(1).strip().strip("`").casefold()
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
    return None


def selected_subagent_execution_mode(plan_path: str) -> str | None:
    body = topology_section(plan_path)
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


def max_concurrent_subagents(plan_path: str) -> str | None:
    body = topology_section(plan_path)
    match = re.search(r"(?im)^\s*Max concurrent subagents\s*:\s*`?([^`\n]+?)`?\s*$", body)
    if not match:
        return None
    value = match.group(1).strip().strip("`")
    if "/" in value:
        return None
    return value


def normalize_expected_topology(value: str) -> str | None:
    lowered = value.strip().strip("`").casefold()
    if lowered in {"main-only", "main only"}:
        return "Main-only"
    if lowered in {"serial-subagent-driven", "serial subagent-driven", "serial"}:
        return "Serial subagent-driven"
    if lowered in {"parallel-subagent-driven", "parallel subagent-driven", "parallel"}:
        return "Parallel subagent-driven"
    return None


def normalize_expected_subagent_mode(value: str) -> str | None:
    lowered = value.strip().strip("`").casefold()
    if lowered in {"none", "not applicable", "n/a"}:
        return "none"
    if lowered in {"serial-single-active", "serial single active", "serial"}:
        return "serial-single-active"
    if lowered in {"parallel-max-safe", "parallel max safe", "parallel"}:
        return "parallel-max-safe"
    return None


def derive_runtime_goal_path(requirements_path: str) -> Path:
    path = Path(requirements_path)
    stem = path.stem
    parts = list(path.parts)
    if "requirements" in parts:
        parts[parts.index("requirements")] = "runtime-goals"
        return Path(*parts).with_name(f"{stem}.goal.md")
    return path.with_name(f"{stem}.goal.md")


def validate_runtime_contract_path(path: Path) -> bool:
    return path.name.endswith(".goal.md")


def pointer_command(runtime_contract_path: Path) -> str:
    return (
        f"/goal Execute the runtime goal contract at {runtime_contract_path}. "
        "Read it first and follow it exactly. "
        "If any referenced artifact is missing, not approved, or inconsistent, "
        "stop and report the smallest required human decision."
    )


def runtime_goal_contract(
    *,
    requirements: str,
    design: str | None,
    goal: str,
    plan: str,
    review: str,
) -> str:
    design_line = f"- Design: `{design}`" if design else "- Design: `not required`"
    design_required_line = (
        f"- Design `{design}`: `Answer Method Check`, `Final Answer Format Design`, `Design-to-Goal Mapping`, `Design-to-Execution Mapping`."
        if design
        else "- Design: `not required`."
    )
    work_assignment = selected_execution_topology(plan) or "read from approved execution policy"
    workflow = selected_delegation_workflow(plan) or "read from approved execution policy"
    subagent_mode = selected_subagent_execution_mode(plan) or "read from approved execution policy"
    max_concurrent = max_concurrent_subagents(plan) or "read from approved execution policy"
    if workflow == "superpowers-subagent-driven-development":
        workflow_line = (
            "- Because the selected agent workflow is `superpowers-subagent-driven-development`, use `$superpowers:subagent-driven-development` only in `serial-single-active` mode for approved current-session implementation-plan work packages."
        )
    elif workflow == "superpowers-dispatching-parallel-agents":
        workflow_line = (
            "- Because the selected agent workflow is `superpowers-dispatching-parallel-agents`, use `$superpowers:dispatching-parallel-agents` only for the approved independent work packages in the current wave, under the plan's required-step frontier, lock, barrier, failure, and main-agent integration rules."
        )
    else:
        workflow_line = "- Use only the selected agent workflow recorded in the approved execution policy."

    return "\n".join(
        [
            "# Runtime Goal Contract",
            "",
            "## Approved Control Chain",
            "",
            f"- Requirements: `{requirements}`",
            design_line,
            f"- Goal: `{goal}`",
            f"- Execution policy: `{plan}`",
            f"- Control review: `{review}`",
            "",
            "## Runtime Execution Rule",
            "",
            "Execute the approved execution policy under the approved control chain. Do not reinterpret what the user approved, how this should be answered, what counts as done, final answer format, work assignment, checks, or control strategy.",
            "Treat What the User Approved as the source for primary object, requested transformation, non-goals, how this should be answered, what is not enough, work covered in this run, what the agent may do, forbidden actions, purpose feedback, where the result must show up, what counts as done, final answer format, workflow fit, and known assumptions.",
            "",
            f"- Who does the work: `{work_assignment}`",
            f"- Selected agent workflow: `{workflow}`",
            f"- Subagent execution mode: `{subagent_mode}`",
            f"- Max concurrent subagents: `{max_concurrent}`",
            "",
            "## Required Sections To Read",
            "",
            f"- Requirements `{requirements}`: `What the User Approved`, `How We Know The User Purpose Was Met`, `Where The Result Must Show Up`, `Final Answer Format`.",
            design_required_line,
            f"- Goal `{goal}`: `Success Condition`, `What Counts As Done`, `Work Covered And Allowed Actions Contract`, `How We Know The User Purpose Was Met`, `Where The Result Must Show Up`, `Final Answer Format`.",
            f"- Execution policy `{plan}`: `Work Coverage And Action Limits Matrix`, `Steps That Make The Result True`, `Action That Can Make It Done`, `Candidate Plan Tasks`, `Who Does The Work / Context Use`, `Subagent execution mode`, `Parallel wave matrix`, `Conflict / lock model`, `Failure policy`, `Phase Gates`, `Progress Log Rules`, `User Purpose Strategy`, `Where The Result Must Show Up`, `Check / Evidence Rules`.",
            f"- Control review `{review}`: `Design Answer Method Check`, `Work Covered And Allowed Actions Check`, `Subagent Concurrency Check`, `Answer Path Check`, `What Counts As Done Check`, `User Purpose Evidence Check`, `Result Placement Check`, `Who Does The Work / Context Use`, `Final Observer Check`.",
            "",
            "## Runtime Discipline",
            "",
            "- Use `$superpowers:executing-plans` discipline against the approved execution policy.",
            "- Use `$superpowers:systematic-debugging` for unclear or repeated failures.",
            "- Use `$superpowers:verification-before-completion` before claiming completion.",
            "- Follow the approved work assignment and agent workflow recorded in the execution policy.",
            workflow_line,
            "- If `Subagent execution mode` is `serial-single-active`, run exactly one execution subagent at a time and integrate before launching the next.",
            "- If `Subagent execution mode` is `parallel-max-safe`, launch only the current approved wave up to the approved cap, after dependencies are satisfied and conflict locks are disjoint; integrate at the approved barrier before launching the next wave.",
            "- Treat subagent work as governed by the execution policy's bounded delegation protocol and integration gates.",
            "- Treat approved sensors, checks, and evidence channels as sensors, not objectives.",
            "",
            "## Final Report Required Fields",
            "",
            "- goal achieved: yes/no",
            "- what counts as done met: yes/no",
            "- evidence needed to call it done",
            "- required answer path coverage and step evidence",
            "- answer method completion evidence when requirements/design define how this should be answered",
            "- if no: not done reason",
            "- if no: action that can make it done attempted or proof of impossibility",
            "- if no: smallest next action that can make it done",
            "- work covered in this run",
            "- work coverage: complete / partial / unavailable / explicitly bounded by what the user approved",
            "- executed",
            "- prepared-only",
            "- forbidden-not-executed",
            "- explicitly out-of-scope by what the user approved",
            "- user purpose evidence status and highest purpose-relevant evidence observed",
            "- result places covered, actions completed or justified, old behavior checked, and pending or unknown places when result-placement applies",
            "",
            "## Stop Rule",
            "",
            "If any referenced artifact is missing, not approved, inconsistent, or insufficient for runtime execution, stop and report the smallest required human decision.",
            "",
        ]
    )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--requirements", dest="requirements")
    ap.add_argument("--clarification", dest="requirements", help="Deprecated alias for --requirements")
    ap.add_argument("--design")
    ap.add_argument("--goal", required=True)
    ap.add_argument("--plan", required=True)
    ap.add_argument("--review", required=True)
    ap.add_argument("--out")
    ap.add_argument("--expect-topology", help="Optional compile-time assertion; validates the approved plan work assignment but does not override it.")
    ap.add_argument("--expect-subagent-mode", help="Optional compile-time assertion; validates the approved plan subagent execution mode but does not override it.")
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

    if args.expect_topology:
        expected = normalize_expected_topology(args.expect_topology)
        actual = selected_execution_topology(args.plan)
        if expected is None:
            print(f"ERROR: invalid expected topology: {args.expect_topology}", file=sys.stderr)
            return 2
        if actual != expected:
            print(f"ERROR: expected topology {expected}, got {actual}", file=sys.stderr)
            return 2

    if args.expect_subagent_mode:
        expected_mode = normalize_expected_subagent_mode(args.expect_subagent_mode)
        actual_mode = selected_subagent_execution_mode(args.plan)
        if expected_mode is None:
            print(f"ERROR: invalid expected subagent execution mode: {args.expect_subagent_mode}", file=sys.stderr)
            return 2
        if actual_mode != expected_mode:
            print(f"ERROR: expected subagent execution mode {expected_mode}, got {actual_mode}", file=sys.stderr)
            return 2

    out_path = Path(args.out) if args.out else derive_runtime_goal_path(args.requirements)
    if not validate_runtime_contract_path(out_path):
        print(
            f"Runtime goal contract output path must end with .goal.md: {out_path}",
            file=sys.stderr,
        )
        return 2
    contract = runtime_goal_contract(
        requirements=args.requirements,
        design=args.design,
        goal=args.goal,
        plan=args.plan,
        review=args.review,
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(contract, encoding="utf-8")

    command = pointer_command(out_path)
    print("Runtime goal contract written:")
    print(out_path)
    print()
    print("Use this /goal:")
    print(command)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
