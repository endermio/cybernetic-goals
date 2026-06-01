#!/usr/bin/env python3
"""Dry-run, export, or explicitly sync redacted cybernetic run events.

Network upload is disabled by default. The only non-dry-run path implemented in
this MVP is an explicit simulated upload, which records pending/sent ledger
state without contacting GitHub.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from validate_run_events import load_events, validate_event


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def default_state_dir() -> Path:
    return Path(os.environ.get("CYBERNETIC_STATE_DIR", Path.home() / ".cybernetic-goals" / "sync"))


def load_input(path: str) -> list[dict[str, Any]]:
    text = Path(path).read_text(encoding="utf-8")
    value = json.loads(text)
    if isinstance(value, dict) and "events" in value:
        events = value["events"]
        if not isinstance(events, list) or not all(isinstance(event, dict) for event in events):
            raise ValueError("package events must be an array of objects")
        return events
    return load_events(path)


def validate_events(events: list[dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    for index, event in enumerate(events, start=1):
        errors.extend(validate_event(event, set(), f"event:{index}"))
    return errors


def package_id(events: list[dict[str, Any]]) -> str:
    canonical = json.dumps(events, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return "pkg_" + hashlib.sha256(canonical).hexdigest()


def destination_hash(destination: str | None) -> str | None:
    if not destination:
        return None
    return "sha256:" + hashlib.sha256(destination.encode("utf-8")).hexdigest()


def read_ledger(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    return json.loads(path.read_text(encoding="utf-8"))


def write_ledger(path: Path, entries: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(entries, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def append_unique(path: Path, entry: dict[str, Any], keys: tuple[str, ...]) -> None:
    entries = read_ledger(path)
    for existing in entries:
        if all(existing.get(key) == entry.get(key) for key in keys):
            existing.update(entry)
            write_ledger(path, entries)
            return
    entries.append(entry)
    write_ledger(path, entries)


def already_sent(sent_path: Path, pkg_id: str, dest_hash: str) -> bool:
    return any(
        entry.get("package_id") == pkg_id and entry.get("destination_hash") == dest_hash
        for entry in read_ledger(sent_path)
    )


def summarize(mode: str, events: list[dict[str, Any]], pkg_id: str, dest_hash: str | None, would_upload: bool) -> dict[str, Any]:
    taxonomy_counts: dict[str, int] = {}
    for event in events:
        for code in event.get("taxonomy_codes", []) or []:
            taxonomy_counts[code] = taxonomy_counts.get(code, 0) + 1
    return {
        "mode": mode,
        "event_count": len(events),
        "event_ids": [event["event_id"] for event in events],
        "package_id": pkg_id,
        "destination_hash": dest_hash,
        "taxonomy_counts": taxonomy_counts,
        "would_upload": would_upload,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--upload", action="store_true")
    parser.add_argument("--simulate-upload", action="store_true")
    parser.add_argument("--destination")
    parser.add_argument("--token-env")
    parser.add_argument("--state-dir")
    parser.add_argument("--export-out")
    parser.add_argument("--force-resend", action="store_true")
    args = parser.parse_args()

    try:
        events = load_input(args.input)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}")
        return 2

    errors = validate_events(events)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 2

    pkg_id = package_id(events)
    dest_hash = destination_hash(args.destination)

    if args.upload:
        if not args.destination or not args.token_env or not os.environ.get(args.token_env):
            print("ERROR: upload requires explicit destination and token-env with a configured token")
            return 2
        if not args.simulate_upload:
            print("ERROR: live upload is not enabled in this MVP; use --dry-run, --export-out, or --simulate-upload")
            return 2

    if args.export_out:
        payload = summarize("export", events, pkg_id, dest_hash, would_upload=False)
        payload["events"] = events
        Path(args.export_out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.export_out).write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps({k: v for k, v in payload.items() if k != "events"}, indent=2, sort_keys=True))
        return 0

    if not args.upload:
        print(json.dumps(summarize("dry_run", events, pkg_id, dest_hash, would_upload=False), indent=2, sort_keys=True))
        return 0

    state_dir = Path(args.state_dir) if args.state_dir else default_state_dir()
    pending_path = state_dir / "pending.json"
    sent_path = state_dir / "sent.json"
    assert dest_hash is not None

    if already_sent(sent_path, pkg_id, dest_hash) and not args.force_resend:
        print(f"ERROR: duplicate send refused for package {pkg_id}")
        return 2

    pending_entry = {
        "package_id": pkg_id,
        "destination_hash": dest_hash,
        "event_ids": [event["event_id"] for event in events],
        "status": "pending",
        "updated_at": utc_now(),
    }
    append_unique(pending_path, pending_entry, ("package_id", "destination_hash"))

    sent_entry = dict(pending_entry)
    sent_entry["status"] = "sent"
    sent_entry["sent_at"] = utc_now()
    sent_entry["response_id"] = "simulated"
    append_unique(sent_path, sent_entry, ("package_id", "destination_hash"))

    payload = summarize("simulated_upload", events, pkg_id, dest_hash, would_upload=True)
    payload["status"] = "sent"
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
