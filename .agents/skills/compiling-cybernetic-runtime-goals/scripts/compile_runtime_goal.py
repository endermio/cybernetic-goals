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


def selected_delegation_substrate(plan_path: str) -> str | None:
    body = topology_section(plan_path)
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


def derive_runtime_goal_path(requirements_path: str) -> Path:
    path = Path(requirements_path)
    stem = path.stem
    parts = list(path.parts)
    if "requirements" in parts:
        parts[parts.index("requirements")] = "runtime-goals"
        return Path(*parts).with_name(f"{stem}.goal.md")
    return path.with_name(f"{stem}.goal.md")


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
    topology = selected_execution_topology(plan) or "read from approved execution policy"
    substrate = selected_delegation_substrate(plan) or "read from approved execution policy"
    substrate_line = (
        "- If the selected delegation substrate is `superpowers-subagent-driven-development`, use `$superpowers:subagent-driven-development` only for approved matching work packages."
        if substrate == "superpowers-subagent-driven-development"
        else "- Use only the selected delegation substrate recorded in the approved execution policy."
    )

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
            "Execute the approved execution policy under the approved control chain. Do not reinterpret the approved setpoint, target-achieved predicate, output contract, topology, sensors, or control strategy.",
            "Treat the human-approved setpoint as the source for primary object, requested transformation, non-goals, execution horizon, runtime authority, forbidden actions, purpose feedback, realization surface closure, single target-achieved predicate, output contract, workflow fit, and known assumptions.",
            "",
            f"- Selected topology: `{topology}`",
            f"- Selected delegation substrate: `{substrate}`",
            "",
            "## Required Sections To Read",
            "",
            f"- Requirements `{requirements}`: `Human Setpoint Approval`, `Purpose Feedback Boundary`, `Realization Surface Closure`, `Output Contract`.",
            f"- Goal `{goal}`: `Success Condition`, `Target Achievement Contract`, `Execution Horizon and Authority Contract`, `Purpose Feedback Contract`, `Realization Surface Contract`, `Final Output Contract`.",
            f"- Execution policy `{plan}`: `Horizon and Authority Coverage Matrix`, `Target-Producing Action Strategy`, `Context Management / Execution Topology`, `Phase Gates`, `Progress Log Rules`, `Purpose Feedback Strategy`, `Realization Surface Closure Strategy`, `Sensor / Evidence Governance`.",
            f"- Control review `{review}`: `Execution Horizon and Authority Fidelity`, `Target Achievement Predicate Fidelity`, `Purpose Feedback Adequacy`, `Realization Surface Closure Adequacy`, `Context Management / Execution Topology`, `Final Observer Check`.",
            "",
            "## Runtime Discipline",
            "",
            "- Use `$superpowers:executing-plans` discipline against the approved execution policy.",
            "- Use `$superpowers:systematic-debugging` for unclear or repeated failures.",
            "- Use `$superpowers:verification-before-completion` before claiming completion.",
            "- Follow the approved execution topology and delegation substrate recorded in the execution policy.",
            substrate_line,
            "- Treat subagent work as governed by the execution policy's bounded delegation protocol and integration gates.",
            "- Treat approved sensors, checks, and evidence channels as sensors, not objectives.",
            "",
            "## Final Report Required Fields",
            "",
            "- goal achieved: yes/no",
            "- single target-achieved predicate met: yes/no",
            "- target-producing evidence",
            "- if no: non-achieved reason",
            "- if no: target-producing action attempted or proof of impossibility",
            "- if no: smallest next target-producing attempt",
            "- approved execution horizon",
            "- horizon coverage: complete / partial / unavailable / explicitly bounded by HSA",
            "- executed",
            "- prepared-only",
            "- forbidden-not-executed",
            "- explicitly out-of-scope by HSA",
            "- purpose feedback status and highest purpose-relevant evidence observed",
            "- realization surfaces covered, actions completed or justified, residuals reconciled, and pending or unknown surfaces when RSC applies",
            "",
            "## Stop Rule",
            "",
            "If any referenced artifact is missing, not approved, internally inconsistent, or insufficient for runtime execution, stop and report the smallest required human decision.",
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

    out_path = Path(args.out) if args.out else derive_runtime_goal_path(args.requirements)
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
