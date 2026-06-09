#!/usr/bin/env python3
from __future__ import annotations

import argparse


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a short /goal pointer for a runtime control JSON file.")
    parser.add_argument("runtime_control_json", help="Path to runtime.control.json.")
    args = parser.parse_args()

    print(
        "/goal Execute the runtime control JSON at "
        f"{args.runtime_control_json} using .agents/skills/using-control-json. "
        "Read it first; if required JSON is missing, invalid, or inconsistent, stop and report the smallest required human decision."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
