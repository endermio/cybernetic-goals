#!/usr/bin/env python3
"""Apply an anchor-preserving amendment proposal as the next reviewed generation."""
from __future__ import annotations

import argparse
import copy
import json
import re
import sys
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[4]
COMPILE_SCRIPTS = REPO_ROOT / ".agents/skills/compiling-cybernetic-runtime-goals/scripts"
RUNTIME_SCRIPTS = REPO_ROOT / ".agents/skills/using-control-json/scripts"
sys.path.insert(0, str(COMPILE_SCRIPTS))
sys.path.insert(0, str(RUNTIME_SCRIPTS))

from compile_runtime_goal import compile_runtime_control  # noqa: E402
from control_json_runtime import read_progress_events, validate_control_chain  # noqa: E402


ANCHOR_FIELDS = ("semantic_base_change", "required_outcomes_changed", "authority_expanded")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def result_payload(ok: bool, **fields: Any) -> dict[str, Any]:
    payload: dict[str, Any] = {"ok": ok}
    payload.update(fields)
    return payload


def active_generation(run_control: dict[str, Any]) -> dict[str, Any] | None:
    current = run_control.get("current_generation")
    generations = run_control.get("generations")
    if not isinstance(current, str) or not isinstance(generations, list):
        return None
    for generation in generations:
        if isinstance(generation, dict) and generation.get("id") == current:
            return generation
    return None


def amendment_generation_count(run_control: dict[str, Any]) -> int:
    generations = run_control.get("generations")
    if not isinstance(generations, list):
        return 0
    return sum(1 for generation in generations if isinstance(generation, dict) and generation.get("parent"))


def next_generation_id(run_control: dict[str, Any]) -> str:
    max_index = -1
    generations = run_control.get("generations")
    if isinstance(generations, list):
        for generation in generations:
            if not isinstance(generation, dict):
                continue
            generation_id = generation.get("id")
            match = re.fullmatch(r"gen-(\d+)", generation_id) if isinstance(generation_id, str) else None
            if match:
                max_index = max(max_index, int(match.group(1)))
    return f"gen-{max_index + 1:03d}"


def unresolved_proposals(events: list[dict[str, Any]], current_generation: str) -> list[dict[str, Any]]:
    proposed: dict[str, dict[str, Any]] = {}
    resolved: set[str] = set()
    for event in events:
        if event.get("runtime_generation") != current_generation:
            continue
        amendment_id = event.get("amendment_id")
        if not isinstance(amendment_id, str) or not amendment_id:
            continue
        event_type = event.get("event_type")
        if event_type == "control.amendment.proposed":
            proposed[amendment_id] = event
        elif event_type in {
            "control.amendment.approved",
            "control.amendment.rejected",
            "control.amendment.blocked",
        }:
            resolved.add(amendment_id)
    return [event for amendment_id, event in proposed.items() if amendment_id not in resolved]


def append_progress_event(run_dir: Path, event: dict[str, Any]) -> None:
    progress_path = run_dir / "progress.jsonl"
    with progress_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event, ensure_ascii=False, separators=(",", ":")) + "\n")


def approved_review(amendment: dict[str, Any], parent_generation: str) -> dict[str, Any]:
    amendment_id = amendment["amendment_id"]
    return {
        "artifact_type": "review.control",
        "schema_version": amendment.get("schema_version", "1.0.0"),
        "status": "approved",
        "review_scope": "amendment",
        "amendment_source": f"progress.jsonl#{amendment_id}",
        "parent_generation": parent_generation,
        "review_checks": [
            {
                "check_id": "anchor-preservation",
                "status": "pass",
                "verdict": "approved",
                "return_to_stage": None,
                "evidence": [f"amendment {amendment_id} does not change approved anchors"],
                "findings": [],
                "required_changes": [],
                "checked_transformations": ["runtime->amendment-generation"],
            }
        ],
    }


def apply_amendment(run_dir: Path, requested_amendment_id: str | None = None) -> tuple[int, dict[str, Any]]:
    artifacts, chain_errors = validate_control_chain(run_dir)
    if artifacts is None or chain_errors:
        return 2, result_payload(False, next_allowed_action="FixJsonControlRun", errors=chain_errors)

    run_control = read_json(run_dir / "run.control.json")
    current_generation = run_control.get("current_generation")
    current = active_generation(run_control)
    if not isinstance(current_generation, str) or current is None:
        return 2, result_payload(False, next_allowed_action="FixJsonControlRun", errors=["run.control.json current_generation is invalid"])

    events, event_errors = read_progress_events(run_dir / "progress.jsonl")
    if event_errors:
        return 2, result_payload(False, next_allowed_action="FixProgressEvents", errors=event_errors)
    proposals = unresolved_proposals(events, current_generation)
    if requested_amendment_id:
        proposals = [proposal for proposal in proposals if proposal.get("amendment_id") == requested_amendment_id]
    if not proposals:
        return 2, result_payload(False, next_allowed_action="AwaitAmendmentProposal", errors=["no unresolved amendment proposal for current_generation"])

    amendment = proposals[-1]
    amendment_id = amendment["amendment_id"]
    changed_anchors = [field for field in ANCHOR_FIELDS if amendment.get(field) is True]
    if changed_anchors:
        return 2, result_payload(
            False,
            next_allowed_action="HumanApprovalRequired",
            amendment_id=amendment_id,
            errors=["amendment changes approved anchors or authority: " + ", ".join(changed_anchors)],
        )

    max_rounds = run_control.get("max_auto_amendment_rounds")
    if not isinstance(max_rounds, int) or isinstance(max_rounds, bool) or amendment_generation_count(run_control) + 1 > max_rounds:
        return 2, result_payload(
            False,
            next_allowed_action="Blocked",
            amendment_id=amendment_id,
            errors=["auto amendment rounds exceed max_auto_amendment_rounds"],
        )

    runtime_rel = current.get("runtime")
    if not isinstance(runtime_rel, str):
        return 2, result_payload(False, next_allowed_action="FixJsonControlRun", errors=["current generation has no runtime"])
    current_runtime = read_json(run_dir / runtime_rel)
    required_steps = copy.deepcopy(current_runtime.get("required_steps"))
    if not isinstance(required_steps, list) or not required_steps:
        return 2, result_payload(False, next_allowed_action="RunReview", errors=["current runtime has no required_steps to refine"])
    for step in required_steps:
        if isinstance(step, dict) and step.get("synthetic") is True:
            return 2, result_payload(
                False,
                next_allowed_action="RunReview",
                amendment_id=amendment_id,
                errors=["synthetic discovery steps require reviewed non-synthetic refinement"],
            )

    new_generation = next_generation_id(run_control)
    new_generation_entry = {
        "id": new_generation,
        "strategy_kind": "amendment",
        "status": "active",
        "parent": current_generation,
        "runtime": f"{new_generation}/runtime.control.json",
        "review": f"{new_generation}/review.control.json",
        "amendment_source": f"progress.jsonl#{amendment_id}",
        "required_steps": required_steps,
    }

    updated_run = copy.deepcopy(run_control)
    for generation in updated_run["generations"]:
        if isinstance(generation, dict) and generation.get("id") == current_generation:
            generation["status"] = "superseded"
    updated_run["generations"].append(new_generation_entry)
    updated_run["current_generation"] = new_generation
    write_json(run_dir / "run.control.json", updated_run)
    write_json(run_dir / new_generation_entry["review"], approved_review(amendment, current_generation))

    runtime_path = compile_runtime_control(run_dir)
    append_progress_event(
        run_dir,
        {
            "event_type": "control.amendment.approved",
            "schema_version": amendment.get("schema_version", "1.0.0"),
            "occurred_at": amendment.get("occurred_at", "unknown"),
            "runtime_generation": current_generation,
            "amendment_id": amendment_id,
            "next_generation": new_generation,
        },
    )

    return 0, result_payload(
        True,
        next_allowed_action="ContinueCurrentGeneration",
        amendment_id=amendment_id,
        previous_generation=current_generation,
        new_generation=new_generation,
        runtime_control=str(runtime_path.relative_to(run_dir)),
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Create the next reviewed generation from an amendment proposal.")
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--amendment-id")
    args = parser.parse_args()

    code, payload = apply_amendment(Path(args.run_dir), args.amendment_id)
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
