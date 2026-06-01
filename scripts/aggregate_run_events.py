#!/usr/bin/env python3
"""Aggregate redacted cybernetic run events into candidate outputs.

This script performs non-live aggregation only. It writes machine-readable
summary and eval-candidate artifacts and does not create GitHub issues.
"""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from validate_run_events import load_taxonomy, load_events, validate_event


DEFAULT_TAXONOMY = Path("observability/taxonomies/failure-taxonomy.yaml")
FAILURE_CANDIDATE_CATEGORIES = {
    "routing",
    "requirements",
    "design",
    "goal",
    "execution_policy",
    "review",
    "runtime",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_input(path: str) -> list[dict[str, Any]]:
    text = Path(path).read_text(encoding="utf-8")
    value = json.loads(text)
    if isinstance(value, dict) and "events" in value:
        events = value["events"]
        if not isinstance(events, list) or not all(isinstance(event, dict) for event in events):
            raise ValueError(f"{path}: package events must be an array of objects")
        return events
    return load_events(path)


def count_by(events: list[dict[str, Any]], field: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for event in events:
        value = str(event.get(field, "unknown"))
        counts[value] = counts.get(value, 0) + 1
    return dict(sorted(counts.items()))


def taxonomy_counts(events: list[dict[str, Any]]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for event in events:
        for code in event.get("taxonomy_codes", []) or []:
            counts[code] = counts.get(code, 0) + 1
    return dict(sorted(counts.items()))


def skill_pack_versions(events: list[dict[str, Any]]) -> list[str]:
    versions: set[str] = set()
    for event in events:
        skill_pack = event.get("skill_pack") or {}
        release = skill_pack.get("release")
        source_commit = skill_pack.get("source_commit")
        if release:
            versions.add(f"release:{release}")
        elif source_commit:
            versions.add(f"commit:{source_commit}")
        else:
            versions.add("unknown")
    return sorted(versions)


def candidate_id(code: str) -> str:
    safe = re.sub(r"[^a-z0-9]+", "-", code.casefold()).strip("-")
    return f"eval-candidate-{safe}"


def candidate_for_code(code: str, count: int) -> dict[str, Any]:
    return {
        "id": candidate_id(code),
        "taxonomy_code": code,
        "event_count": count,
        "prompt": f"Create a regression case for recurring cybernetic failure pattern `{code}`.",
        "expected_output": "The relevant cybernetic skill should preserve the approved control boundary and avoid this failure pattern.",
        "assertions": [
            f"Identifies `{code}` as the failure pattern under review.",
            "Preserves confirmed requirements and approved control artifacts.",
            "Does not turn candidate evidence into an accepted control-law change.",
            "Routes any rule change through review, eval evidence, and release gating."
        ],
        "status": "candidate",
    }


def build_eval_candidates(counts: dict[str, int]) -> list[dict[str, Any]]:
    candidates: list[dict[str, Any]] = []
    for code, count in counts.items():
        category = code.split(".", 1)[0]
        if category in FAILURE_CANDIDATE_CATEGORIES:
            candidates.append(candidate_for_code(code, count))
    return candidates


def write_json(path: str, payload: dict[str, Any]) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", action="append", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--eval-candidates-out", required=True)
    parser.add_argument("--taxonomy", default=str(DEFAULT_TAXONOMY))
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    taxonomy = load_taxonomy(args.taxonomy) if args.taxonomy else set()
    events: list[dict[str, Any]] = []
    try:
        for path in args.input:
            events.extend(load_input(path))
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}")
        return 2

    errors: list[str] = []
    for index, event in enumerate(events, start=1):
        errors.extend(validate_event(event, taxonomy, f"event:{index}"))
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 2

    tax_counts = taxonomy_counts(events)
    candidates = build_eval_candidates(tax_counts)
    generated_at = utc_now()

    summary = {
        "schema_version": "1.0.0",
        "generated_at": generated_at,
        "dry_run": bool(args.dry_run),
        "event_count": len(events),
        "event_type_counts": count_by(events, "event"),
        "status_counts": count_by(events, "status"),
        "skill_counts": count_by(events, "skill"),
        "taxonomy_counts": tax_counts,
        "skill_pack_versions": skill_pack_versions(events),
        "candidate_count": len(candidates),
    }
    eval_candidates = {
        "schema_version": "1.0.0",
        "generated_at": generated_at,
        "source_summary": args.out,
        "candidates": candidates,
    }

    write_json(args.out, summary)
    write_json(args.eval_candidates_out, eval_candidates)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
