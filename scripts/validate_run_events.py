#!/usr/bin/env python3
"""Validate cybernetic run-event JSON/JSONL files.

The validator intentionally uses only the Python standard library. It enforces
the repository's metadata-only safety contract rather than attempting full JSON
Schema coverage.
"""

from __future__ import annotations

import argparse
import json
import re
import socket
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


EVENT_TYPES = {
    "skill_invoked",
    "route_decided",
    "artifact_created",
    "blocked",
    "human_feedback",
    "runtime_outcome",
}

REQUIRED_FIELDS = {
    "schema_version",
    "event_id",
    "event",
    "timestamp",
    "privacy_mode",
    "machine_id",
    "skill_pack",
    "task_hash",
}

UNSAFE_METADATA_ONLY_KEYS = {
    "artifact_body",
    "code",
    "code_excerpt",
    "content_excerpt",
    "content_summary",
    "credential",
    "credentials",
    "customer_data",
    "log",
    "log_excerpt",
    "path",
    "prompt",
    "raw_prompt",
    "real_path",
    "real_repo",
    "repo_name",
    "repository",
    "repository_name",
    "secret",
    "token",
}

TASK_HASH_RE = re.compile(r"^sha256:[a-f0-9]{64}$")
EVENT_ID_RE = re.compile(r"^evt_[A-Za-z0-9_.-]+$")
MACHINE_ID_RE = re.compile(r"^anon-[A-Za-z0-9_.-]+$")


def load_taxonomy(path: str | None) -> set[str]:
    if not path:
        return set()

    taxonomy: set[str] = set()
    current_category: str | None = None
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if not line.startswith(" ") and stripped.endswith(":"):
            current_category = stripped[:-1]
            continue
        if current_category and stripped.startswith("- "):
            taxonomy.add(f"{current_category}.{stripped[2:].strip()}")
    return taxonomy


def load_events(path: str) -> list[dict[str, Any]]:
    text = Path(path).read_text(encoding="utf-8")
    if not text.strip():
        return []
    if path.endswith(".jsonl"):
        events: list[dict[str, Any]] = []
        for index, line in enumerate(text.splitlines(), start=1):
            if not line.strip():
                continue
            value = json.loads(line)
            if not isinstance(value, dict):
                raise ValueError(f"{path}:{index}: event must be a JSON object")
            events.append(value)
        return events

    value = json.loads(text)
    if isinstance(value, list):
        if not all(isinstance(item, dict) for item in value):
            raise ValueError(f"{path}: all array items must be event objects")
        return value
    if isinstance(value, dict):
        return [value]
    raise ValueError(f"{path}: event file must contain an object or array")


def iter_keys(value: Any) -> list[str]:
    keys: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            keys.append(str(key))
            keys.extend(iter_keys(child))
    elif isinstance(value, list):
        for child in value:
            keys.extend(iter_keys(child))
    return keys


def validate_timestamp(value: Any, errors: list[str], prefix: str) -> None:
    if not isinstance(value, str):
        errors.append(f"{prefix}: timestamp must be a string")
        return
    candidate = value.replace("Z", "+00:00")
    try:
        datetime.fromisoformat(candidate)
    except ValueError:
        errors.append(f"{prefix}: timestamp is not ISO-8601 date-time")


def validate_skill_pack(value: Any, errors: list[str], prefix: str) -> None:
    if not isinstance(value, dict):
        errors.append(f"{prefix}: skill_pack must be an object")
        return
    release = value.get("release")
    source_commit = value.get("source_commit")
    if not release and not source_commit:
        errors.append(f"{prefix}: skill_pack requires release or source_commit")


def validate_machine_id(value: Any, errors: list[str], prefix: str) -> None:
    if not isinstance(value, str) or not MACHINE_ID_RE.match(value):
        errors.append(f"{prefix}: machine_id must be pseudonymous and start with anon-")
        return
    hostname = socket.gethostname()
    if hostname and value.casefold() == hostname.casefold():
        errors.append(f"{prefix}: machine_id must not be derived from hostname")


def validate_event(event: dict[str, Any], taxonomy: set[str], prefix: str) -> list[str]:
    errors: list[str] = []

    missing = sorted(REQUIRED_FIELDS - set(event))
    for field in missing:
        errors.append(f"{prefix}: missing required field {field}")

    if event.get("schema_version") != "1.0.0":
        errors.append(f"{prefix}: schema_version must be 1.0.0")
    if not isinstance(event.get("event_id"), str) or not EVENT_ID_RE.match(str(event.get("event_id"))):
        errors.append(f"{prefix}: event_id must match evt_*")
    if event.get("event") not in EVENT_TYPES:
        errors.append(f"{prefix}: event must be one of {sorted(EVENT_TYPES)}")
    validate_timestamp(event.get("timestamp"), errors, prefix)
    if event.get("privacy_mode") not in {"metadata_only", "redacted_content_opt_in"}:
        errors.append(f"{prefix}: privacy_mode must be metadata_only or redacted_content_opt_in")
    validate_machine_id(event.get("machine_id"), errors, prefix)
    validate_skill_pack(event.get("skill_pack"), errors, prefix)

    task_hash = event.get("task_hash")
    if not isinstance(task_hash, str) or not TASK_HASH_RE.match(task_hash):
        errors.append(f"{prefix}: task_hash must match sha256:<64 lowercase hex>")

    taxonomy_codes = event.get("taxonomy_codes", [])
    if taxonomy_codes is None:
        taxonomy_codes = []
    if not isinstance(taxonomy_codes, list) or not all(isinstance(code, str) for code in taxonomy_codes):
        errors.append(f"{prefix}: taxonomy_codes must be an array of strings")
    elif taxonomy:
        unknown = sorted(set(taxonomy_codes) - taxonomy)
        for code in unknown:
            errors.append(f"{prefix}: unknown taxonomy code {code}")

    if event.get("privacy_mode") == "metadata_only":
        unsafe = sorted(set(iter_keys(event)) & UNSAFE_METADATA_ONLY_KEYS)
        for key in unsafe:
            errors.append(f"{prefix}: metadata_only event contains unsafe field {key}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="+", help="JSON or JSONL event files")
    parser.add_argument("--taxonomy", help="Failure taxonomy YAML path")
    args = parser.parse_args()

    taxonomy = load_taxonomy(args.taxonomy)
    all_errors: list[str] = []
    total_events = 0

    for path in args.paths:
        try:
            events = load_events(path)
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            all_errors.append(f"{path}: {exc}")
            continue
        for index, event in enumerate(events, start=1):
            total_events += 1
            all_errors.extend(validate_event(event, taxonomy, f"{path}:{index}"))

    if all_errors:
        for error in all_errors:
            print(f"ERROR: {error}")
        return 2

    print(f"validated {total_events} event{'s' if total_events != 1 else ''}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
