#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from control_json_runtime import result_payload, validate_event


def main() -> int:
    parser = argparse.ArgumentParser(description="Append one validated JSON progress event to progress.jsonl.")
    parser.add_argument("run_dir", help="Directory that owns progress.jsonl.")
    parser.add_argument("--event-json", required=True, help="A single JSON object to append.")
    args = parser.parse_args()

    try:
        event = json.loads(args.event_json)
    except json.JSONDecodeError as exc:
        errors = [f"event-json is invalid JSON: {exc}"]
        print(json.dumps(result_payload(False, errors), indent=2))
        return 1
    if not isinstance(event, dict):
        errors = ["event-json must be a JSON object"]
        print(json.dumps(result_payload(False, errors), indent=2))
        return 1

    errors = validate_event(event)
    if errors:
        print(json.dumps(result_payload(False, errors), indent=2))
        return 1

    progress_path = Path(args.run_dir) / "progress.jsonl"
    with progress_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event, separators=(",", ":")) + "\n")

    print(json.dumps(result_payload(True, [], progress_path=str(progress_path)), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
