#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from control_json_runtime import result_payload, validate_control_chain


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate an approved runtime control JSON chain.")
    parser.add_argument("run_dir", help="Directory containing runtime.control.json and its approved chain.")
    args = parser.parse_args()

    run_dir = Path(args.run_dir)
    artifacts, errors = validate_control_chain(run_dir)
    ok = artifacts is not None and not errors
    print(json.dumps(result_payload(ok, errors, run_dir=str(run_dir)), indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
