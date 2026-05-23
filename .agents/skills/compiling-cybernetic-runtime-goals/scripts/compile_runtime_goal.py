#!/usr/bin/env python3
"""Compile a final runtime /goal command from approved control artifacts."""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--clarification", required=True)
    ap.add_argument("--goal", required=True)
    ap.add_argument("--plan", required=True)
    ap.add_argument("--review", required=True)
    ap.add_argument("--out")
    ap.add_argument("--skip-guard", action="store_true", help="Testing only. Bypasses phase-gate checks and must not be used for official runtime goal compilation.")
    ap.add_argument("--i-understand-this-bypasses-phase-gates", action="store_true", help="Required with --skip-guard to make phase-gate bypass explicit.")
    args = ap.parse_args()

    here = Path(__file__).resolve().parent
    guard = here / "control_chain_guard.py"
    if args.skip_guard and not args.i_understand_this_bypasses_phase_gates:
        print("ERROR: --skip-guard is for tests only and requires --i-understand-this-bypasses-phase-gates", file=sys.stderr)
        return 2
    if not args.skip_guard:
        cmd = [sys.executable, str(guard), "--clarification", args.clarification, "--goal", args.goal, "--plan", args.plan, "--review", args.review]
        result = subprocess.run(cmd, text=True, capture_output=True)
        if result.returncode != 0:
            sys.stdout.write(result.stdout)
            sys.stderr.write(result.stderr)
            return result.returncode

    command = (
        f"/goal Execute the approved execution policy in {args.plan} "
        f"under the control contract in {args.goal} "
        f"and the confirmed semantics in {args.clarification}. "
        f"Use the approved control review in {args.review} as the phase-gate record. "
        "Do not reinterpret requirements, rewrite the control strategy, replace approved sensors, or start unreviewed work. "
        "Use `$superpowers:executing-plans` discipline against the approved plan. "
        "Use `$superpowers:systematic-debugging` for unclear or repeated failures. "
        "Use `$superpowers:verification-before-completion` before claiming completion. "
        "If runtime cannot load these skills, follow the equivalent discipline already written in the approved plan and control review. "
        "Execute serially according to the approved batch rhythm. "
        "Intermediate states inside a batch may be broken if the approved plan allows it, but each batch must end in the approved openable/verifiable state. "
        "Treat tests as sensors, not objectives; if a sensor conflicts with confirmed semantics, stop or follow the approved sensor-governance rule. "
        "If any referenced artifact is missing, not approved, or internally inconsistent, stop and report the smallest required human decision. "
        "If the clarification, goal, plan, or review conflict or become insufficient, stop and report the smallest required human decision."
    )

    if args.out:
        Path(args.out).write_text(command + "\n", encoding="utf-8")
    print(command)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
