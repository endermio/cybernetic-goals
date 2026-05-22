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
    ap.add_argument("--skip-guard", action="store_true")
    args = ap.parse_args()

    here = Path(__file__).resolve().parent
    guard = here / "control_chain_guard.py"
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
        "Execute serially according to the approved batch rhythm. "
        "Intermediate states inside a batch may be broken if the approved plan allows it, but each batch must end in the approved openable/verifiable state. "
        "Treat tests as sensors, not objectives; if a sensor conflicts with confirmed semantics, stop or follow the approved sensor-governance rule. "
        "If the clarification, goal, plan, or review conflict or become insufficient, stop and report the smallest required human decision."
    )

    if args.out:
        Path(args.out).write_text(command + "\n", encoding="utf-8")
    print(command)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
