#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from bounded_control_runtime import normalize_run_dir, result_payload, validate_bounded_runtime


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a bounded_runtime control JSON.")
    parser.add_argument("runtime_or_run_dir", help="Run directory or path to runtime.control.json.")
    args = parser.parse_args()

    run_dir = normalize_run_dir(Path(args.runtime_or_run_dir))
    _goal, _runtime, errors = validate_bounded_runtime(run_dir)
    ok = not errors
    print(json.dumps(result_payload(ok, errors, run_dir=str(run_dir)), indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
