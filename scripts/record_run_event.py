#!/usr/bin/env python3
"""Record a local cybernetic run event.

This script never uploads. It either prints a dry-run event or appends one JSON
object per line to a local JSONL store.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from validate_run_events import validate_event


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def default_state_dir() -> Path:
    return Path(os.environ.get("CYBERNETIC_STATE_DIR", Path.home() / ".cybernetic-goals"))


def load_or_create_machine_id(state_dir: Path, dry_run: bool) -> str:
    explicit = os.environ.get("CYBERNETIC_MACHINE_ID")
    if explicit:
        return explicit
    if dry_run:
        return f"anon-{uuid.uuid4().hex[:12]}"

    state_dir.mkdir(parents=True, exist_ok=True)
    machine_id_file = state_dir / "machine-id"
    if machine_id_file.exists():
        return machine_id_file.read_text(encoding="utf-8").strip()
    machine_id = f"anon-{uuid.uuid4().hex[:12]}"
    machine_id_file.write_text(machine_id + "\n", encoding="utf-8")
    return machine_id


LOCAL_UNVERSIONED_RELEASE = "local-unversioned"


def git_source_commit(repo_root: Path) -> str | None:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=repo_root,
            text=True,
            capture_output=True,
            check=False,
        )
    except OSError:
        return None
    if result.returncode == 0:
        return result.stdout.strip() or None
    return None


def default_skill_pack_identity(args: argparse.Namespace) -> dict[str, str]:
    if args.release:
        skill_pack = {"release": args.release}
        if args.source_commit:
            skill_pack["source_commit"] = args.source_commit
        return skill_pack
    if args.source_commit:
        return {"source_commit": args.source_commit}

    env_source_commit = os.environ.get("CYBERNETIC_SKILL_PACK_COMMIT")
    if env_source_commit:
        return {"source_commit": env_source_commit}

    repo_source_commit = git_source_commit(Path(__file__).resolve().parents[1])
    if repo_source_commit:
        return {"source_commit": repo_source_commit}
    return {"release": LOCAL_UNVERSIONED_RELEASE}


def default_task_hash(args: argparse.Namespace) -> str:
    payload = {
        "event": args.event,
        "skill": args.skill,
        "status": args.status,
        "reason_code": args.reason_code,
        "artifact_type": args.artifact_type,
    }
    digest = hashlib.sha256(json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()
    return f"sha256:{digest}"


def build_event(args: argparse.Namespace) -> dict[str, Any]:
    state_dir = Path(args.state_dir) if args.state_dir else default_state_dir()
    event: dict[str, Any] = {
        "schema_version": "1.0.0",
        "event_id": args.event_id or f"evt_{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}_{uuid.uuid4().hex[:8]}",
        "event": args.event,
        "timestamp": args.timestamp or utc_now(),
        "privacy_mode": "metadata_only",
        "machine_id": args.machine_id or load_or_create_machine_id(state_dir, args.dry_run),
        "skill_pack": default_skill_pack_identity(args),
        "task_hash": args.task_hash or default_task_hash(args),
    }
    if args.skill:
        event["skill"] = args.skill
    if args.status:
        event["status"] = args.status
    if args.reason_code:
        event["reason_code"] = args.reason_code
    if args.artifact_type:
        event["artifact_type"] = args.artifact_type
    if args.taxonomy_code:
        event["taxonomy_codes"] = args.taxonomy_code
    if args.explicit_user_invocation:
        event["explicit_user_invocation"] = True
    return event


def default_output_path(state_dir: Path) -> Path:
    day = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    return state_dir / "runs" / f"{day}.jsonl"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--event", required=True)
    parser.add_argument("--skill")
    parser.add_argument("--status")
    parser.add_argument("--reason-code")
    parser.add_argument("--artifact-type")
    parser.add_argument("--taxonomy-code", action="append")
    parser.add_argument("--event-id")
    parser.add_argument("--timestamp")
    parser.add_argument("--machine-id")
    parser.add_argument("--release")
    parser.add_argument("--source-commit")
    parser.add_argument("--task-hash")
    parser.add_argument("--state-dir")
    parser.add_argument("--output")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--explicit-user-invocation", action="store_true")
    args = parser.parse_args()

    event = build_event(args)
    errors = validate_event(event, set(), "event")
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 2

    if args.dry_run:
        print(json.dumps(event, indent=2, sort_keys=True))
        return 0

    state_dir = Path(args.state_dir) if args.state_dir else default_state_dir()
    output_path = Path(args.output) if args.output else default_output_path(state_dir)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event, sort_keys=True) + "\n")
    print(json.dumps({"status": "recorded", "path": str(output_path), "event_id": event["event_id"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
