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
SHARED_SCRIPTS = REPO_ROOT / ".agents/skills/_shared"
sys.path.insert(0, str(COMPILE_SCRIPTS))
sys.path.insert(0, str(RUNTIME_SCRIPTS))
sys.path.insert(0, str(SHARED_SCRIPTS))

from compile_runtime_goal import compile_runtime_control  # noqa: E402
from control_json_runtime import generation_review_errors, read_progress_events, validate_control_chain  # noqa: E402
from transition_gate import transition_gate_payload  # noqa: E402


ANCHOR_FIELDS = ("semantic_base_change", "required_outcomes_changed", "authority_expanded")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def result_payload(ok: bool, **fields: Any) -> dict[str, Any]:
    next_action = str(fields.pop("next_allowed_action", fields.pop("next_action", "ContinueCurrentGeneration")))
    errors = fields.pop("errors", [])
    payload = transition_gate_payload(
        ok=ok,
        gate_id="amendment-orchestrator",
        next_action=next_action,
        errors=errors if isinstance(errors, list) else [str(errors)],
        legacy_next_allowed_action=True,
        **fields,
    )
    return payload


def string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, str) and item]


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


def safe_ref_path(run_dir: Path, ref: Any, label: str) -> tuple[Path | None, list[str]]:
    if not isinstance(ref, str) or not ref:
        return None, [f"{label} must be a non-empty relative path"]
    path = Path(ref)
    if path.is_absolute() or ".." in path.parts:
        return None, [f"{label} must stay inside the run directory"]
    return run_dir / path, []


def patch_validation_errors(patch: dict[str, Any], amendment: dict[str, Any], current_generation: str) -> list[str]:
    errors: list[str] = []
    amendment_id = amendment["amendment_id"]
    for forbidden in ("semantic_base_change", "required_outcomes_changed", "authority_expanded"):
        if forbidden in patch:
            errors.append(f"amendment patch must not contain approved-anchor field: {forbidden}")
    if patch.get("artifact_type") != "amendment.patch":
        errors.append("amendment patch artifact_type must be amendment.patch")
    if patch.get("amendment_id") != amendment_id:
        errors.append("amendment patch amendment_id must match proposal")
    if patch.get("parent_generation") != current_generation:
        errors.append("amendment patch parent_generation must match current_generation")
    if patch.get("strategy_kind") != "amendment":
        errors.append("amendment patch strategy_kind must be amendment")
    required_steps = patch.get("required_steps")
    if not isinstance(required_steps, list) or not required_steps:
        errors.append("amendment patch must include non-empty required_steps")
    else:
        for index, step in enumerate(required_steps):
            if not isinstance(step, dict):
                errors.append(f"amendment patch required_steps[{index}] must be an object")
                continue
            for field in ("step_id", "transition", "evidence", "satisfies_outcomes"):
                if field not in step:
                    errors.append(f"amendment patch required_steps[{index}] missing {field}")
            if step.get("synthetic") is True:
                errors.append("amendment patch required_steps must be reviewed non-synthetic steps")
    runtime_updates = patch.get("runtime_updates", {})
    if runtime_updates is None:
        runtime_updates = {}
    if not isinstance(runtime_updates, dict):
        errors.append("amendment patch runtime_updates must be an object when present")
    else:
        writable = runtime_updates.get("writable_evidence_paths")
        if writable is not None and not string_list(writable):
            errors.append("amendment patch runtime_updates.writable_evidence_paths must be a non-empty string list")
        verifier = runtime_updates.get("verifier")
        if verifier is not None:
            if not isinstance(verifier, dict):
                errors.append("amendment patch runtime_updates.verifier must be an object")
            else:
                for field in ("required_before_goal_achieved", "command", "required_outcomes", "output_schema"):
                    if field not in verifier:
                        errors.append(f"amendment patch runtime_updates.verifier missing {field}")
        for field in ("imported_evidence", "invalidated_evidence"):
            if field in runtime_updates and not isinstance(runtime_updates.get(field), list):
                errors.append(f"amendment patch runtime_updates.{field} must be a list")
    return errors


def generation_entry_from_patch(
    patch: dict[str, Any],
    amendment: dict[str, Any],
    new_generation: str,
    current_generation: str,
) -> dict[str, Any]:
    runtime_updates = patch.get("runtime_updates")
    if not isinstance(runtime_updates, dict):
        runtime_updates = {}
    entry: dict[str, Any] = {
        "id": new_generation,
        "strategy_kind": "amendment",
        "status": "active",
        "parent": current_generation,
        "runtime": f"{new_generation}/runtime.control.json",
        "review": f"amendments/{amendment['amendment_id']}.review.control.json",
        "amendment_source": f"progress.jsonl#{amendment['amendment_id']}",
        "patch_ref": amendment["patch_ref"],
        "required_steps": copy.deepcopy(patch["required_steps"]),
    }
    for field in ("writable_evidence_paths", "verifier", "imported_evidence", "invalidated_evidence"):
        if field in runtime_updates:
            entry[field] = copy.deepcopy(runtime_updates[field])
    return entry


def apply_amendment(run_dir: Path, requested_amendment_id: str | None = None) -> tuple[int, dict[str, Any]]:
    artifacts, chain_errors = validate_control_chain(run_dir)
    if artifacts is None or chain_errors:
        return 2, result_payload(False, next_allowed_action="FixJsonControlRun", errors=chain_errors)

    run_control = read_json(run_dir / "run.control.json")
    if run_control.get("strategy_policy") != "reviewed_replanning":
        return 2, result_payload(
            False,
            next_allowed_action="HumanApprovalRequired",
            errors=[
                "strategy_policy is "
                + str(run_control.get("strategy_policy"))
                + "; automatic amendment continuation requires reviewed_replanning"
            ],
        )
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

    patch_path, patch_ref_errors = safe_ref_path(run_dir, amendment.get("patch_ref"), "patch_ref")
    if patch_ref_errors:
        return 2, result_payload(False, next_allowed_action="FixAmendmentProposal", amendment_id=amendment_id, errors=patch_ref_errors)
    if patch_path is None or not patch_path.exists():
        return 2, result_payload(
            False,
            next_allowed_action="FixAmendmentPatch",
            amendment_id=amendment_id,
            errors=["amendment patch file is missing: " + str(amendment.get("patch_ref"))],
        )
    patch = read_json(patch_path)
    patch_errors = patch_validation_errors(patch, amendment, current_generation)
    if patch_errors:
        return 2, result_payload(False, next_allowed_action="FixAmendmentPatch", amendment_id=amendment_id, errors=patch_errors)
    new_generation = next_generation_id(run_control)
    new_generation_entry = generation_entry_from_patch(patch, amendment, new_generation, current_generation)
    review_ref = f"amendments/{amendment_id}.review.control.json"
    parent_run_ref = f"amendments/{amendment_id}.parent-run.control.json"
    parent_run_path = run_dir / parent_run_ref
    if not parent_run_path.exists():
        write_json(parent_run_path, run_control)
    review_path = run_dir / review_ref
    if not review_path.exists():
        candidate_path = run_dir / f"amendments/{amendment_id}.candidate-generation.json"
        write_json(candidate_path, new_generation_entry)
        return 2, result_payload(
            False,
            next_allowed_action="RunReview",
            amendment_id=amendment_id,
            candidate_generation=new_generation,
            candidate_generation_ref=str(candidate_path.relative_to(run_dir)),
            review_ref=review_ref,
            errors=["reviewed amendment patch requires approved review before generation switch"],
        )
    review = read_json(review_path)
    review_errors = generation_review_errors(
        review,
        context="amendment patch",
        requirements=artifacts["requirements"],
        run_dir=run_dir,
        run_control=run_control,
        runtime=artifacts["runtime"],
        runtime_rel=current.get("runtime") if isinstance(current.get("runtime"), str) else None,
        review_rel=review_ref,
    )
    if review.get("artifact_type") != "review.control" or review.get("status") != "approved":
        review_errors.append("amendment patch review must be an approved review.control artifact")
    if review_errors:
        return 2, result_payload(False, next_allowed_action="RunReview", amendment_id=amendment_id, errors=review_errors)

    updated_run = copy.deepcopy(run_control)
    for generation in updated_run["generations"]:
        if isinstance(generation, dict) and generation.get("id") == current_generation:
            generation["status"] = "superseded"
    updated_run["generations"].append(new_generation_entry)
    updated_run["current_generation"] = new_generation
    write_json(run_dir / "run.control.json", updated_run)

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
