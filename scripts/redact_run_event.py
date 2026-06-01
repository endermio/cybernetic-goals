#!/usr/bin/env python3
"""Redact cybernetic run events before export."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from validate_run_events import load_events, unsafe_metadata_key_reason, unsafe_metadata_value_reason, validate_event


REDACTED = object()


def redact_value(value: Any, redacted_fields: set[str], field_name: str | None = None) -> Any:
    if isinstance(value, dict):
        clean: dict[str, Any] = {}
        for key, child in value.items():
            if unsafe_metadata_key_reason(key):
                redacted_fields.add(key)
                continue
            clean_child = redact_value(child, redacted_fields, key)
            if clean_child is REDACTED:
                redacted_fields.add(key)
                continue
            clean[key] = clean_child
        return clean
    if isinstance(value, list):
        clean_items: list[Any] = []
        for item in value:
            clean_item = redact_value(item, redacted_fields, field_name)
            if clean_item is REDACTED:
                if field_name:
                    redacted_fields.add(field_name)
                continue
            clean_items.append(clean_item)
        return clean_items
    if unsafe_metadata_value_reason(value):
        return REDACTED
    return value


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("--mode", default="metadata_only", choices=["metadata_only", "redacted_content_opt_in"])
    parser.add_argument("--out")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    try:
        events = load_events(args.input)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}")
        return 2

    redacted_fields: set[str] = set()
    clean_events: list[dict[str, Any]] = []
    for event in events:
        clean = redact_value(event, redacted_fields)
        clean["privacy_mode"] = args.mode
        errors = validate_event(clean, set(), "event")
        if errors:
            for error in errors:
                print(f"ERROR: {error}")
            return 2
        clean_events.append(clean)

    payload = {
        "mode": args.mode,
        "event_count": len(clean_events),
        "redacted_fields": sorted(redacted_fields),
        "events": clean_events,
    }

    text = json.dumps(payload, indent=2, sort_keys=True)
    if args.out:
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.out).write_text(text + "\n", encoding="utf-8")
    if args.dry_run or not args.out:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
