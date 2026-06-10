import copy
import hashlib
import json
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
LEGACY_FIXTURE = ROOT / "tests/fixtures/cybernetics/runtime_verifier/control_runs.json"
CONTROL_GUARD = ROOT / ".agents/skills/compiling-cybernetic-runtime-goals/scripts/control_chain_guard.py"
COMPILER = ROOT / ".agents/skills/compiling-cybernetic-runtime-goals/scripts/compile_runtime_goal.py"
VALIDATE = ROOT / ".agents/skills/using-control-json/scripts/validate_control_chain.py"
VERIFY = ROOT / ".agents/skills/using-control-json/scripts/verify_runtime_progress.py"
AMENDMENT_ORCHESTRATOR = ROOT / ".agents/skills/orchestrating-cybernetic-pregoal/scripts/amendment_orchestrator.py"


def canonical_json_hash(value: dict, omit_top_level: set[str] | None = None) -> str:
    canonical_value = copy.deepcopy(value)
    for key in omit_top_level or set():
        canonical_value.pop(key, None)
    encoded = json.dumps(canonical_value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return "sha256:" + hashlib.sha256(encoded).hexdigest()


def control_hash(filename: str, artifact: dict) -> str:
    omit = {"approved_control_hashes"} if filename.endswith("runtime.control.json") else set()
    return canonical_json_hash(artifact, omit)


def refresh_semantic_base(req: dict) -> None:
    approved = copy.deepcopy(req["approved_control"])
    approved.pop("semantic_base", None)
    req["approved_control"]["semantic_base"] = {
        "id": "semantic-base:lean-test",
        "hash": canonical_json_hash(approved),
    }


def requirements(outcome_id: str = "O-lean-startup", evidence_id: str = "evidence.lean-startup") -> dict:
    req = {
        "artifact_type": "requirements.control",
        "schema_version": "1.1.0",
        "status": "approved",
        "approved_control": {
            "human_purpose": "exercise lean pre-goal reviewed replanning",
            "primary_object": "generation-aware control run",
            "requested_transformation": "run a lean current generation",
            "non_goals": ["do not use full-chain artifacts as startup requirements"],
            "how_we_know_purpose_was_met": "current generation verifier permits completion",
            "where_result_must_show_up": ["run.control.json", "gen-000/runtime.control.json"],
            "what_counts_as_done": "current generation has required evidence and no unresolved amendment",
            "source_requirements": [
                {
                    "id": "SR-lean-startup",
                    "source": {"kind": "user_message", "quote": "run a lean current generation"},
                    "required_action": "run a lean current generation to completion",
                    "requirement_type": "implement_behavior",
                    "required_evidence_strength": "test_result",
                    "target_objects": ["lean current generation"],
                    "completion_checks": ["current generation verifier permits completion"],
                    "blocks_goal_achieved_if_missing": True,
                }
            ],
            "required_outcomes": [
                {
                    "id": outcome_id,
                    "statement": f"{outcome_id} is implemented, not merely prepared",
                    "blocks_goal_achieved_if_missing": True,
                    "source_requirements": ["SR-lean-startup"],
                    "completion_claim": "Completes the lean current generation.",
                    "completed_target_objects": ["lean current generation"],
                    "required_evidence": [
                        {
                            "evidence_id": evidence_id,
                            "kind": "progress_event",
                            "description": "mainline current-generation evidence",
                            "evidence_strength": "test_result",
                            "satisfies_source_requirements": ["SR-lean-startup"],
                            "evidence_claim": "The current generation verifier permits completion.",
                            "completed_target_objects": ["lean current generation"],
                        }
                    ],
                    "not_satisfied_by": ["readiness or partial candidate evidence"],
                }
            ],
            "final_answer_format": {
                "medium": "chat summary",
                "required_structure": ["verification"],
            },
        },
    }
    approved = copy.deepcopy(req["approved_control"])
    approved.pop("semantic_base", None)
    req["approved_control"]["semantic_base"] = {
        "id": "semantic-base:lean-test",
        "hash": canonical_json_hash(approved),
    }
    return req


def run_control(current_generation: str = "gen-000", generations: list[dict] | None = None) -> dict:
    if generations is None:
        generations = [
            {
                "id": "gen-000",
                "strategy_kind": "execution",
                "status": "active",
                "runtime": "gen-000/runtime.control.json",
                "review": "gen-000/review.control.json",
                "required_steps": [
                    {
                        "step_id": "S1",
                        "transition": "current generation produces required evidence",
                        "evidence": ["current generation evidence"],
                        "satisfies_outcomes": ["O-lean-startup"],
                    }
                ],
            }
        ]
    return {
        "artifact_type": "run.control",
        "schema_version": "1.0.0",
        "status": "active",
        "run_id": "lean-test-run",
        "control_mode": "lean",
        "current_generation": current_generation,
        "max_auto_amendment_rounds": 2,
        "semantic_base_ref": {"id": "semantic-base:lean-test", "hash": "unset"},
        "amendment_policy": {
            "may_change": ["design_strategy", "plan_strategy", "runtime_strategy", "verifier_config"],
            "must_not_change_without_human": [
                "semantic_base",
                "required_outcomes",
                "what_counts_as_done",
                "work_covered",
                "authority",
                "forbidden_actions",
            ],
        },
        "generations": generations,
    }


def runtime_control(req: dict, run: dict, generation_id: str, outcome_id: str, evidence_id: str) -> dict:
    generation = next(item for item in run["generations"] if item["id"] == generation_id)
    runtime = {
        "artifact_type": "runtime.control",
        "schema_version": "1.0.0",
        "status": "compiled",
        "control_mode": run["control_mode"],
        "generation": {"id": generation_id},
        "semantic_base_ref": req["approved_control"]["semantic_base"],
        "approved_control": {
            "objective": req["approved_control"]["requested_transformation"],
            "what_counts_as_done": req["approved_control"]["what_counts_as_done"],
        },
        "approved_control_hashes": {},
        "runtime": {
            "readonly_files": ["requirements.control.json", "run.control.json", generation["runtime"]],
            "writable_files": ["progress.jsonl", "runtime-status.json", "final-report.json"],
            "writable_evidence_paths": ["evidence/"],
        },
        "required_steps": [
            {
                "step_id": "S1",
                "transition": "current generation produces required evidence",
                "evidence": [evidence_id],
                "satisfies_outcomes": [outcome_id],
            }
        ],
        "progress": {"event_schema": "progress-event.schema.json", "append_only": True},
        "verifier": {
            "required_before_goal_achieved": True,
            "command": "python3 .agents/skills/using-control-json/scripts/verify_runtime_progress.py",
            "required_outcomes": [outcome_id],
            "output_schema": "final-report.schema.json",
        },
        "imported_evidence": [],
        "invalidated_evidence": [],
    }
    if generation.get("parent"):
        runtime["generation"]["parent"] = generation["parent"]
    if generation.get("amendment_source"):
        runtime["generation"]["amendment_source"] = generation["amendment_source"]
    if generation.get("review"):
        runtime["runtime"]["readonly_files"].insert(2, generation["review"])
    return runtime


def apply_hashes(req: dict, run: dict, runtime: dict, runtime_rel: str, review: dict | None = None, review_rel: str | None = None) -> None:
    run["semantic_base_ref"] = copy.deepcopy(req["approved_control"]["semantic_base"])
    runtime["semantic_base_ref"] = copy.deepcopy(req["approved_control"]["semantic_base"])
    runtime["approved_control_hashes"] = {
        "requirements.control.json": control_hash("requirements.control.json", req),
        "run.control.json": control_hash("run.control.json", run),
        runtime_rel: control_hash(runtime_rel, runtime),
    }
    if review is not None and review_rel is not None:
        runtime["approved_control_hashes"][review_rel] = control_hash(review_rel, review)


def approved_generation_review() -> dict:
    checks = []
    for check_id in (
        "intent-preservation",
        "obligation-preservation",
        "required-outcome-coverage",
        "source-requirement-preservation",
        "horizon-authority",
    ):
        checks.append(
            {
                "check_id": check_id,
                "status": "pass",
                "verdict": "approved",
                "return_to_stage": None,
                "evidence": [f"{check_id} passed for current generation"],
                "findings": [],
                "required_changes": [],
                "checked_transformations": ["runtime->generation"],
            }
        )
    return {
        "artifact_type": "review.control",
        "schema_version": "1.0.0",
        "status": "approved",
        "review_checks": checks,
    }


def progress_event(
    evidence_id: str,
    *,
    generation: str = "gen-000",
    event_type: str = "step.completed",
    amendment_id: str | None = None,
) -> dict:
    event = {
        "event_type": event_type,
        "schema_version": "1.0.0",
        "occurred_at": "2026-06-10T00:00:00Z",
        "work_package_id": "WP1",
        "required_step": "S1",
        "status": "pass" if event_type == "step.completed" else "partial",
        "progress_role": "mainline",
        "counts_as_goal_progress": event_type == "step.completed",
        "runtime_generation": generation,
        "evidence": [evidence_id],
    }
    if amendment_id:
        event["amendment_id"] = amendment_id
        event["reason"] = "current strategy cannot produce required evidence"
        event["triggering_observation"] = "current strategy produced substitute evidence"
        event["affected_stages"] = ["plan", "runtime"]
        event["affected_source_requirements"] = ["SR-lean-startup"]
        event["semantic_base_change"] = False
        event["required_outcomes_changed"] = False
        event["authority_expanded"] = False
        event["proposed_changes"] = ["replace substitute evidence with producing strategy"]
        event["review_required"] = ["intent-preservation", "required-outcome-coverage"]
    return event


def final_report(generation: str, evidence_id: str, unresolved: list[str] | None = None) -> dict:
    return {
        "artifact_type": "final-report",
        "schema_version": "1.0.0",
        "goal_achieved": True,
        "what_counts_as_done_met": True,
        "runtime_generation": generation,
        "superseded_generations": [],
        "unresolved_amendments": unresolved or [],
        "evidence": [evidence_id],
        "verification": {
            "verifier_result": "pass",
            "verifier_permits_goal_achieved": True,
        },
        "work_coverage": {
            "status": "complete",
            "executed": ["WP1"],
            "prepared_only": [],
            "forbidden_not_executed": [],
            "out_of_scope": [],
        },
        "remaining_gaps": [],
    }


def write_lean_run(
    run_dir: Path,
    *,
    outcome_id: str = "O-lean-startup",
    required_evidence_id: str = "evidence.lean-startup",
    progress_events: list[dict] | None = None,
    report: dict | None = None,
    current_generation: str = "gen-000",
    generations: list[dict] | None = None,
    runtime_edits=None,
) -> None:
    req = requirements(outcome_id, required_evidence_id)
    run = run_control(current_generation=current_generation, generations=generations)
    runtime_rel = next(item["runtime"] for item in run["generations"] if item["id"] == current_generation)
    runtime = runtime_control(req, run, current_generation, outcome_id, required_evidence_id)
    if runtime_edits:
        runtime_edits(runtime)
    review = None
    review_rel = next((item.get("review") for item in run["generations"] if item["id"] == current_generation), None)
    if review_rel:
        review = approved_generation_review()
    apply_hashes(req, run, runtime, runtime_rel, review, review_rel)
    (run_dir / "requirements.control.json").write_text(json.dumps(req, indent=2), encoding="utf-8")
    (run_dir / "run.control.json").write_text(json.dumps(run, indent=2), encoding="utf-8")
    runtime_path = run_dir / runtime_rel
    runtime_path.parent.mkdir(parents=True, exist_ok=True)
    runtime_path.write_text(json.dumps(runtime, indent=2), encoding="utf-8")
    if review_rel and review:
        review_path = run_dir / review_rel
        review_path.parent.mkdir(parents=True, exist_ok=True)
        review_path.write_text(json.dumps(review, indent=2), encoding="utf-8")
    if progress_events is not None:
        (run_dir / "progress.jsonl").write_text(
            "".join(json.dumps(event) + "\n" for event in progress_events),
            encoding="utf-8",
        )
    if report is not None:
        (run_dir / "final-report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")


def run_script(script: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["python3", str(script), *args], text=True, capture_output=True)


class ReviewedReplanningControlTest(unittest.TestCase):
    def test_official_runtime_entrypoints_reject_full_chain_without_run_control(self):
        fixture = json.loads(LEGACY_FIXTURE.read_text(encoding="utf-8"))["valid"]
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            for filename, payload in fixture["control_files"].items():
                (run_dir / filename).write_text(json.dumps(payload, indent=2), encoding="utf-8")

            compiler = run_script(COMPILER, "--run-dir", str(run_dir))
            guard = run_script(CONTROL_GUARD, "--run-dir", str(run_dir))
            validate = run_script(VALIDATE, str(run_dir))

            for result in (compiler, guard, validate):
                self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertIn("missing run.control.json", result.stdout + result.stderr)

    def test_guard_and_runtime_validator_accept_lean_run_without_full_chain_artifacts(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            write_lean_run(run_dir)

            guard = run_script(CONTROL_GUARD, "--run-dir", str(run_dir))
            validate = run_script(VALIDATE, str(run_dir))

            self.assertEqual(guard.returncode, 0, guard.stdout + guard.stderr)
            self.assertEqual(validate.returncode, 0, validate.stdout + validate.stderr)
            self.assertFalse((run_dir / "design.control.json").exists())
            self.assertIn("PASS", guard.stdout)
            self.assertTrue(json.loads(validate.stdout)["ok"])

    def test_guard_rejects_generation_review_missing_source_requirement_preservation(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            write_lean_run(run_dir)
            review_path = run_dir / "gen-000/review.control.json"
            review = json.loads(review_path.read_text(encoding="utf-8"))
            review["review_checks"] = [
                check
                for check in review["review_checks"]
                if check["check_id"] != "source-requirement-preservation"
            ]
            req = json.loads((run_dir / "requirements.control.json").read_text(encoding="utf-8"))
            run = json.loads((run_dir / "run.control.json").read_text(encoding="utf-8"))
            runtime = json.loads((run_dir / "gen-000/runtime.control.json").read_text(encoding="utf-8"))
            apply_hashes(req, run, runtime, "gen-000/runtime.control.json", review, "gen-000/review.control.json")
            review_path.write_text(json.dumps(review, indent=2), encoding="utf-8")
            (run_dir / "gen-000/runtime.control.json").write_text(json.dumps(runtime, indent=2), encoding="utf-8")

            result = run_script(CONTROL_GUARD, "--run-dir", str(run_dir))

            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("source-requirement-preservation", result.stdout + result.stderr)

    def test_runtime_validator_requires_runtime_generation_for_step_events(self):
        event = progress_event("evidence.lean-startup")
        del event["runtime_generation"]
        events = [event]
        report = final_report("gen-000", "evidence.lean-startup")
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            write_lean_run(run_dir, progress_events=events, report=report)

            result = run_script(VERIFY, str(run_dir))

            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("all progress events must include runtime_generation", result.stdout + result.stderr)

    def test_amendment_proposal_event_does_not_require_step_event_fields(self):
        event = {
            "event_type": "control.amendment.proposed",
            "schema_version": "1.0.0",
            "occurred_at": "2026-06-10T00:00:00Z",
            "runtime_generation": "gen-000",
            "amendment_id": "A1",
            "reason": "current strategy cannot produce required evidence",
            "triggering_observation": "current strategy produced substitute evidence",
            "affected_stages": ["plan", "runtime"],
            "affected_source_requirements": ["SR-lean-startup"],
            "semantic_base_change": False,
            "required_outcomes_changed": False,
            "authority_expanded": False,
            "proposed_changes": ["replace substitute evidence with producing strategy"],
            "review_required": ["intent-preservation", "required-outcome-coverage"],
        }
        report = final_report("gen-000", "evidence.lean-startup")
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            write_lean_run(run_dir, progress_events=[event], report=report)

            result = run_script(VERIFY, str(run_dir))
            payload = json.loads(result.stdout)
            combined = "\n".join(payload["errors"])

            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertNotIn("event missing required field: work_package_id", combined)
            self.assertNotIn("event missing required field: required_step", combined)
            self.assertNotIn("event missing required field: status", combined)
            self.assertNotIn("event missing required field: evidence", combined)
            self.assertIn("A1", payload["unresolved_amendments"])

    def test_generation_event_does_not_require_step_event_fields(self):
        generation_event = {
            "event_type": "runtime.generation.started",
            "schema_version": "1.0.0",
            "occurred_at": "2026-06-10T00:00:00Z",
            "runtime_generation": "gen-000",
            "reason": "initial generation started",
        }
        events = [generation_event, progress_event("evidence.lean-startup")]
        report = final_report("gen-000", "evidence.lean-startup")
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            write_lean_run(run_dir, progress_events=events, report=report)

            result = run_script(VERIFY, str(run_dir))

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertTrue(json.loads(result.stdout)["goal_achieved_permitted"])

    def test_amendment_orchestrator_creates_reviewed_next_generation_for_anchor_preserving_proposal(self):
        event = {
            "event_type": "control.amendment.proposed",
            "schema_version": "1.0.0",
            "occurred_at": "2026-06-10T00:00:00Z",
            "runtime_generation": "gen-000",
            "amendment_id": "A1",
            "reason": "current strategy cannot produce required evidence",
            "triggering_observation": "current strategy cannot produce required evidence",
            "affected_stages": ["plan", "runtime"],
            "affected_source_requirements": ["SR-lean-startup"],
            "semantic_base_change": False,
            "required_outcomes_changed": False,
            "authority_expanded": False,
            "proposed_changes": ["create reviewed amendment generation"],
            "review_required": ["intent-preservation", "required-outcome-coverage"],
        }
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            write_lean_run(run_dir, progress_events=[event])

            result = run_script(AMENDMENT_ORCHESTRATOR, "--run-dir", str(run_dir))

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual("gen-001", payload["new_generation"])
            run = json.loads((run_dir / "run.control.json").read_text(encoding="utf-8"))
            self.assertEqual("gen-001", run["current_generation"])
            generations = {generation["id"]: generation for generation in run["generations"]}
            self.assertEqual("superseded", generations["gen-000"]["status"])
            self.assertEqual("active", generations["gen-001"]["status"])
            self.assertEqual("amendment", generations["gen-001"]["strategy_kind"])
            self.assertEqual("gen-000", generations["gen-001"]["parent"])
            self.assertTrue((run_dir / "gen-001/review.control.json").exists())
            self.assertTrue((run_dir / "gen-001/runtime.control.json").exists())
            review = json.loads((run_dir / "gen-001/review.control.json").read_text(encoding="utf-8"))
            check_ids = {check["check_id"] for check in review["review_checks"]}
            self.assertGreaterEqual(
                check_ids,
                {
                    "intent-preservation",
                    "obligation-preservation",
                    "required-outcome-coverage",
                    "source-requirement-preservation",
                    "horizon-authority",
                },
            )
            source_check = next(
                check
                for check in review["review_checks"]
                if check["check_id"] == "source-requirement-preservation"
            )
            self.assertIn("SR-lean-startup", "\n".join(source_check["evidence"]))
            self.assertEqual(0, run_script(CONTROL_GUARD, "--run-dir", str(run_dir)).returncode)
            progress = [
                json.loads(line)
                for line in (run_dir / "progress.jsonl").read_text(encoding="utf-8").splitlines()
                if line.strip()
            ]
            self.assertTrue(any(event.get("event_type") == "control.amendment.approved" for event in progress))

    def test_amendment_orchestrator_blocks_anchor_changing_proposal(self):
        event = {
            "event_type": "control.amendment.proposed",
            "schema_version": "1.0.0",
            "occurred_at": "2026-06-10T00:00:00Z",
            "runtime_generation": "gen-000",
            "amendment_id": "A-anchor",
            "reason": "current strategy would require changing approved anchors",
            "triggering_observation": "required outcome must change",
            "affected_stages": ["plan", "runtime"],
            "affected_source_requirements": ["SR-lean-startup"],
            "semantic_base_change": True,
            "required_outcomes_changed": False,
            "authority_expanded": False,
            "proposed_changes": ["change approved meaning"],
            "review_required": ["intent-preservation"],
        }
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            write_lean_run(run_dir, progress_events=[event])

            result = run_script(AMENDMENT_ORCHESTRATOR, "--run-dir", str(run_dir))

            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual("HumanApprovalRequired", payload["next_allowed_action"])
            self.assertFalse((run_dir / "gen-001/runtime.control.json").exists())

    def test_guard_rejects_amendment_generation_with_shallow_review(self):
        generations = [
            {
                "id": "gen-000",
                "strategy_kind": "execution",
                "status": "superseded",
                "runtime": "gen-000/runtime.control.json",
                "review": "gen-000/review.control.json",
            },
            {
                "id": "gen-001",
                "strategy_kind": "amendment",
                "status": "active",
                "parent": "gen-000",
                "runtime": "gen-001/runtime.control.json",
                "review": "gen-001/review.control.json",
                "amendment_source": "progress.jsonl#A1",
                "required_steps": [
                    {
                        "step_id": "S1",
                        "transition": "current generation produces required evidence",
                        "evidence": ["evidence.lean-startup"],
                        "satisfies_outcomes": ["O-lean-startup"],
                    }
                ],
            },
        ]
        shallow = {
            "artifact_type": "review.control",
            "schema_version": "1.0.0",
            "status": "approved",
            "review_checks": [
                {
                    "check_id": "anchor-preservation",
                    "status": "pass",
                    "verdict": "approved",
                    "return_to_stage": None,
                    "evidence": ["anchors unchanged"],
                    "findings": [],
                    "required_changes": [],
                    "checked_transformations": ["runtime->amendment-generation"],
                }
            ],
        }
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            write_lean_run(run_dir, generations=generations, current_generation="gen-001")
            (run_dir / "gen-001/review.control.json").write_text(json.dumps(shallow, indent=2), encoding="utf-8")
            req = json.loads((run_dir / "requirements.control.json").read_text(encoding="utf-8"))
            run = json.loads((run_dir / "run.control.json").read_text(encoding="utf-8"))
            runtime = json.loads((run_dir / "gen-001/runtime.control.json").read_text(encoding="utf-8"))
            apply_hashes(req, run, runtime, "gen-001/runtime.control.json", shallow, "gen-001/review.control.json")
            (run_dir / "gen-001/runtime.control.json").write_text(json.dumps(runtime, indent=2), encoding="utf-8")

            result = run_script(CONTROL_GUARD, "--run-dir", str(run_dir))

            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("amendment generation review missing required review checks", result.stdout + result.stderr)

    def test_guard_and_runtime_validator_reject_missing_evidence_source_requirement_coverage(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            write_lean_run(run_dir)
            req = json.loads((run_dir / "requirements.control.json").read_text(encoding="utf-8"))
            req["approved_control"]["required_outcomes"][0]["required_evidence"][0][
                "satisfies_source_requirements"
            ] = []
            run = json.loads((run_dir / "run.control.json").read_text(encoding="utf-8"))
            runtime = json.loads((run_dir / "gen-000/runtime.control.json").read_text(encoding="utf-8"))
            review = json.loads((run_dir / "gen-000/review.control.json").read_text(encoding="utf-8"))
            refresh_semantic_base(req)
            apply_hashes(req, run, runtime, "gen-000/runtime.control.json", review, "gen-000/review.control.json")
            (run_dir / "requirements.control.json").write_text(json.dumps(req, indent=2), encoding="utf-8")
            (run_dir / "run.control.json").write_text(json.dumps(run, indent=2), encoding="utf-8")
            (run_dir / "gen-000/runtime.control.json").write_text(json.dumps(runtime, indent=2), encoding="utf-8")

            guard = run_script(CONTROL_GUARD, "--run-dir", str(run_dir))
            validate = run_script(VALIDATE, str(run_dir))

            for result in (guard, validate):
                self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertIn(
                    "source requirements not covered by required evidence: SR-lean-startup",
                    result.stdout + result.stderr,
                )

    def test_guard_and_runtime_validator_reject_source_requirement_evidence_below_required_strength(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            write_lean_run(run_dir)
            req = json.loads((run_dir / "requirements.control.json").read_text(encoding="utf-8"))
            evidence = req["approved_control"]["required_outcomes"][0]["required_evidence"][0]
            evidence["evidence_strength"] = "behavior_exists"
            run = json.loads((run_dir / "run.control.json").read_text(encoding="utf-8"))
            runtime = json.loads((run_dir / "gen-000/runtime.control.json").read_text(encoding="utf-8"))
            review = json.loads((run_dir / "gen-000/review.control.json").read_text(encoding="utf-8"))
            refresh_semantic_base(req)
            apply_hashes(req, run, runtime, "gen-000/runtime.control.json", review, "gen-000/review.control.json")
            (run_dir / "requirements.control.json").write_text(json.dumps(req, indent=2), encoding="utf-8")
            (run_dir / "run.control.json").write_text(json.dumps(run, indent=2), encoding="utf-8")
            (run_dir / "gen-000/runtime.control.json").write_text(json.dumps(runtime, indent=2), encoding="utf-8")

            guard = run_script(CONTROL_GUARD, "--run-dir", str(run_dir))
            validate = run_script(VALIDATE, str(run_dir))

            for result in (guard, validate):
                self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertIn(
                    "evidence strength behavior_exists does not meet required evidence strength "
                    "test_result for source requirement SR-lean-startup",
                    result.stdout + result.stderr,
                )

    def test_guard_and_runtime_validator_reject_amendment_review_missing_source_requirement_preservation(self):
        generations = [
            {
                "id": "gen-000",
                "strategy_kind": "execution",
                "status": "superseded",
                "runtime": "gen-000/runtime.control.json",
                "review": "gen-000/review.control.json",
            },
            {
                "id": "gen-001",
                "strategy_kind": "amendment",
                "status": "active",
                "parent": "gen-000",
                "runtime": "gen-001/runtime.control.json",
                "review": "gen-001/review.control.json",
                "amendment_source": "progress.jsonl#A1",
                "required_steps": [
                    {
                        "step_id": "S1",
                        "transition": "current generation produces required evidence",
                        "evidence": ["evidence.lean-startup"],
                        "satisfies_outcomes": ["O-lean-startup"],
                    }
                ],
            },
        ]
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            write_lean_run(run_dir, generations=generations, current_generation="gen-001")
            review = approved_generation_review()
            review["review_checks"] = [
                check
                for check in review["review_checks"]
                if check["check_id"] != "source-requirement-preservation"
            ]
            (run_dir / "gen-001/review.control.json").write_text(json.dumps(review, indent=2), encoding="utf-8")
            req = json.loads((run_dir / "requirements.control.json").read_text(encoding="utf-8"))
            run = json.loads((run_dir / "run.control.json").read_text(encoding="utf-8"))
            runtime = json.loads((run_dir / "gen-001/runtime.control.json").read_text(encoding="utf-8"))
            apply_hashes(req, run, runtime, "gen-001/runtime.control.json", review, "gen-001/review.control.json")
            (run_dir / "gen-001/runtime.control.json").write_text(json.dumps(runtime, indent=2), encoding="utf-8")

            guard = run_script(CONTROL_GUARD, "--run-dir", str(run_dir))
            validate = run_script(VALIDATE, str(run_dir))

            for result in (guard, validate):
                self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertIn(
                    "amendment generation review missing required review checks: source-requirement-preservation",
                    result.stdout + result.stderr,
                )

    def test_runtime_validator_rejects_incomplete_amendment_proposal_event(self):
        event = progress_event(
            "evidence.api-v2-readiness",
            event_type="control.amendment.proposed",
            amendment_id="A-api-v2-readiness",
        )
        del event["triggering_observation"]
        del event["affected_stages"]
        del event["semantic_base_change"]
        del event["required_outcomes_changed"]
        del event["authority_expanded"]
        events = [event]
        report = final_report("gen-000", "evidence.api-v2-readiness")
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            write_lean_run(run_dir, progress_events=events, report=report)

            result = run_script(VERIFY, str(run_dir))

            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("control.amendment.proposed events must include triggering_observation", result.stdout + result.stderr)
            self.assertIn("control.amendment.proposed events must include affected_stages", result.stdout + result.stderr)
            self.assertIn("control.amendment.proposed events must include semantic_base_change", result.stdout + result.stderr)

    def test_runtime_validator_requires_affected_source_requirements_on_amendment_proposal(self):
        event = progress_event(
            "evidence.lean-startup",
            event_type="control.amendment.proposed",
            amendment_id="A1",
        )
        del event["affected_source_requirements"]
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            write_lean_run(
                run_dir,
                progress_events=[event],
                report=final_report("gen-000", "evidence.lean-startup"),
            )

            result = run_script(VERIFY, str(run_dir))

            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn(
                "control.amendment.proposed events must include affected_source_requirements",
                result.stdout + result.stderr,
            )

    def test_verifier_rejects_anchor_changing_amendment_as_automatic_goal_completion(self):
        event = progress_event(
            "evidence.api-v2-readiness",
            event_type="control.amendment.proposed",
            amendment_id="A-api-v2-readiness",
        )
        event["semantic_base_change"] = True
        events = [
            progress_event("evidence.lean-startup"),
            event,
            progress_event(
                "evidence.api-v2-readiness",
                event_type="control.amendment.blocked",
                amendment_id="A-api-v2-readiness",
            ),
        ]
        events[-1]["semantic_base_change"] = True
        report = final_report("gen-000", "evidence.lean-startup")
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            write_lean_run(run_dir, progress_events=events, report=report)

            result = run_script(VERIFY, str(run_dir))

            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("anchor-changing amendments require human decision", result.stdout + result.stderr)

    def test_guard_rejects_run_control_without_max_auto_amendment_rounds(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            write_lean_run(run_dir)
            run = json.loads((run_dir / "run.control.json").read_text(encoding="utf-8"))
            del run["max_auto_amendment_rounds"]
            runtime = json.loads((run_dir / "gen-000/runtime.control.json").read_text(encoding="utf-8"))
            apply_hashes(
                json.loads((run_dir / "requirements.control.json").read_text(encoding="utf-8")),
                run,
                runtime,
                "gen-000/runtime.control.json",
                json.loads((run_dir / "gen-000/review.control.json").read_text(encoding="utf-8")),
                "gen-000/review.control.json",
            )
            (run_dir / "run.control.json").write_text(json.dumps(run, indent=2), encoding="utf-8")
            (run_dir / "gen-000/runtime.control.json").write_text(json.dumps(runtime, indent=2), encoding="utf-8")

            result = run_script(CONTROL_GUARD, "--run-dir", str(run_dir))

            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("max_auto_amendment_rounds", result.stdout + result.stderr)

    def test_guard_rejects_blocking_source_requirement_without_outcome_coverage(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            write_lean_run(run_dir)
            req = json.loads((run_dir / "requirements.control.json").read_text(encoding="utf-8"))
            req["approved_control"]["source_requirements"].append(
                {
                    "id": "SR-api-v2",
                    "source": {"kind": "user_message", "quote": "implement /api/v2 routes"},
                    "required_action": "implement /api/v2 routes",
                    "requirement_type": "implement_behavior",
                    "required_evidence_strength": "behavior_exists",
                    "target_objects": ["/api/v2 routes"],
                    "completion_checks": ["/api/v2 routes return non-404 behavior under tests"],
                    "blocks_goal_achieved_if_missing": True,
                }
            )
            run = json.loads((run_dir / "run.control.json").read_text(encoding="utf-8"))
            runtime = json.loads((run_dir / "gen-000/runtime.control.json").read_text(encoding="utf-8"))
            review = json.loads((run_dir / "gen-000/review.control.json").read_text(encoding="utf-8"))
            refresh_semantic_base(req)
            apply_hashes(req, run, runtime, "gen-000/runtime.control.json", review, "gen-000/review.control.json")
            (run_dir / "requirements.control.json").write_text(json.dumps(req, indent=2), encoding="utf-8")
            (run_dir / "run.control.json").write_text(json.dumps(run, indent=2), encoding="utf-8")
            (run_dir / "gen-000/runtime.control.json").write_text(json.dumps(runtime, indent=2), encoding="utf-8")

            result = run_script(CONTROL_GUARD, "--run-dir", str(run_dir))

            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn(
                "source requirements not covered by blocking required outcomes: SR-api-v2",
                result.stdout + result.stderr,
            )

    def test_guard_rejects_framework_evidence_for_measurement_source_requirement(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            write_lean_run(run_dir)
            req = json.loads((run_dir / "requirements.control.json").read_text(encoding="utf-8"))
            sr = req["approved_control"]["source_requirements"][0]
            sr["id"] = "SR-measure-curves"
            sr["source"] = {"kind": "user_message", "quote": "measure scale curves"}
            sr["required_action"] = "measure scale curves"
            sr["requirement_type"] = "produce_empirical_measurement"
            sr["required_evidence_strength"] = "measured_curve_data"
            sr["target_objects"] = ["E", "S"]
            sr["completion_checks"] = ["measured data exists for E", "measured data exists for S"]
            outcome = req["approved_control"]["required_outcomes"][0]
            outcome["source_requirements"] = ["SR-measure-curves"]
            outcome["completion_claim"] = "Defines a scan framework for E and S."
            outcome["completed_target_objects"] = ["E", "S"]
            evidence = outcome["required_evidence"][0]
            evidence["evidence_strength"] = "framework_document"
            evidence["satisfies_source_requirements"] = ["SR-measure-curves"]
            evidence["evidence_claim"] = "The file defines scan rules."
            evidence["completed_target_objects"] = ["E", "S"]
            run = json.loads((run_dir / "run.control.json").read_text(encoding="utf-8"))
            runtime = json.loads((run_dir / "gen-000/runtime.control.json").read_text(encoding="utf-8"))
            review = json.loads((run_dir / "gen-000/review.control.json").read_text(encoding="utf-8"))
            refresh_semantic_base(req)
            apply_hashes(req, run, runtime, "gen-000/runtime.control.json", review, "gen-000/review.control.json")
            (run_dir / "requirements.control.json").write_text(json.dumps(req, indent=2), encoding="utf-8")
            (run_dir / "run.control.json").write_text(json.dumps(run, indent=2), encoding="utf-8")
            (run_dir / "gen-000/runtime.control.json").write_text(json.dumps(runtime, indent=2), encoding="utf-8")

            result = run_script(CONTROL_GUARD, "--run-dir", str(run_dir))

            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn(
                "evidence strength framework_document is too weak for source requirement SR-measure-curves",
                result.stdout + result.stderr,
            )

    def test_guard_rejects_source_requirement_weakened_from_quote(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            write_lean_run(run_dir)
            req = json.loads((run_dir / "requirements.control.json").read_text(encoding="utf-8"))
            sr = req["approved_control"]["source_requirements"][0]
            sr["source"] = {"kind": "user_message", "quote": "measure scale curves for E and S"}
            sr["required_action"] = "define scan framework for E and S"
            sr["requirement_type"] = "define_framework_or_plan"
            sr["required_evidence_strength"] = "framework_document"
            sr["completion_checks"] = ["scan variables are listed"]
            outcome = req["approved_control"]["required_outcomes"][0]
            outcome["completion_claim"] = "Completes the request by defining scan variables."
            evidence = outcome["required_evidence"][0]
            evidence["evidence_strength"] = "framework_document"
            evidence["evidence_claim"] = "The document lists scan variables."
            run = json.loads((run_dir / "run.control.json").read_text(encoding="utf-8"))
            runtime = json.loads((run_dir / "gen-000/runtime.control.json").read_text(encoding="utf-8"))
            review = json.loads((run_dir / "gen-000/review.control.json").read_text(encoding="utf-8"))
            refresh_semantic_base(req)
            apply_hashes(req, run, runtime, "gen-000/runtime.control.json", review, "gen-000/review.control.json")
            (run_dir / "requirements.control.json").write_text(json.dumps(req, indent=2), encoding="utf-8")
            (run_dir / "run.control.json").write_text(json.dumps(run, indent=2), encoding="utf-8")
            (run_dir / "gen-000/runtime.control.json").write_text(json.dumps(runtime, indent=2), encoding="utf-8")

            result = run_script(CONTROL_GUARD, "--run-dir", str(run_dir))

            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("source requirement appears weaker than source quote", result.stdout + result.stderr)

    def test_guard_rejects_api_v2_source_requirement_weakened_to_readiness(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            write_lean_run(run_dir)
            req = json.loads((run_dir / "requirements.control.json").read_text(encoding="utf-8"))
            sr = req["approved_control"]["source_requirements"][0]
            sr["source"] = {
                "kind": "user_message",
                "quote": "implement /api/v2 download/extract/preview API family",
            }
            sr["required_action"] = "document future v2 compatibility readiness"
            sr["requirement_type"] = "define_framework_or_plan"
            sr["required_evidence_strength"] = "framework_document"
            sr["target_objects"] = ["/api/v2 download/extract/preview"]
            sr["completion_checks"] = ["future v2 exposure remains compatible"]
            outcome = req["approved_control"]["required_outcomes"][0]
            outcome["completion_claim"] = "Documents readiness for future v2 exposure."
            evidence = outcome["required_evidence"][0]
            evidence["evidence_strength"] = "framework_document"
            evidence["evidence_claim"] = "The framework document records compatibility readiness."
            run = json.loads((run_dir / "run.control.json").read_text(encoding="utf-8"))
            runtime = json.loads((run_dir / "gen-000/runtime.control.json").read_text(encoding="utf-8"))
            review = json.loads((run_dir / "gen-000/review.control.json").read_text(encoding="utf-8"))
            refresh_semantic_base(req)
            apply_hashes(req, run, runtime, "gen-000/runtime.control.json", review, "gen-000/review.control.json")
            (run_dir / "requirements.control.json").write_text(json.dumps(req, indent=2), encoding="utf-8")
            (run_dir / "run.control.json").write_text(json.dumps(run, indent=2), encoding="utf-8")
            (run_dir / "gen-000/runtime.control.json").write_text(json.dumps(runtime, indent=2), encoding="utf-8")

            result = run_script(CONTROL_GUARD, "--run-dir", str(run_dir))

            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("source requirement appears weaker than source quote", result.stdout + result.stderr)

    def test_guard_rejects_api_v2_routes_source_requirement_weakened_to_readiness(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            write_lean_run(run_dir)
            req = json.loads((run_dir / "requirements.control.json").read_text(encoding="utf-8"))
            sr = req["approved_control"]["source_requirements"][0]
            sr["source"] = {"kind": "user_message", "quote": "implement /api/v2 routes"}
            sr["required_action"] = "document future v2 compatibility readiness"
            sr["requirement_type"] = "define_framework_or_plan"
            sr["required_evidence_strength"] = "framework_document"
            sr["target_objects"] = ["/api/v2 routes"]
            sr["completion_checks"] = ["future v2 route exposure remains compatible"]
            outcome = req["approved_control"]["required_outcomes"][0]
            outcome["completion_claim"] = "Documents readiness for future v2 route exposure."
            outcome["completed_target_objects"] = ["/api/v2 routes"]
            evidence = outcome["required_evidence"][0]
            evidence["evidence_strength"] = "framework_document"
            evidence["evidence_claim"] = "The framework document records compatibility readiness."
            evidence["completed_target_objects"] = ["/api/v2 routes"]
            run = json.loads((run_dir / "run.control.json").read_text(encoding="utf-8"))
            runtime = json.loads((run_dir / "gen-000/runtime.control.json").read_text(encoding="utf-8"))
            review = json.loads((run_dir / "gen-000/review.control.json").read_text(encoding="utf-8"))
            refresh_semantic_base(req)
            apply_hashes(req, run, runtime, "gen-000/runtime.control.json", review, "gen-000/review.control.json")
            (run_dir / "requirements.control.json").write_text(json.dumps(req, indent=2), encoding="utf-8")
            (run_dir / "run.control.json").write_text(json.dumps(run, indent=2), encoding="utf-8")
            (run_dir / "gen-000/runtime.control.json").write_text(json.dumps(runtime, indent=2), encoding="utf-8")

            result = run_script(CONTROL_GUARD, "--run-dir", str(run_dir))

            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("source requirement appears weaker than source quote", result.stdout + result.stderr)

    def test_guard_accepts_preserved_measurement_source_requirement_with_framework_words(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            write_lean_run(run_dir)
            req = json.loads((run_dir / "requirements.control.json").read_text(encoding="utf-8"))
            sr = req["approved_control"]["source_requirements"][0]
            sr["source"] = {"kind": "user_message", "quote": "measure framework adoption growth curves"}
            sr["required_action"] = "measure framework adoption growth curves"
            sr["requirement_type"] = "produce_empirical_measurement"
            sr["required_evidence_strength"] = "measured_curve_data"
            sr["target_objects"] = ["framework adoption"]
            sr["completion_checks"] = ["measured curve data exists for framework adoption growth"]
            outcome = req["approved_control"]["required_outcomes"][0]
            outcome["completion_claim"] = "Produces measured framework adoption growth curves."
            outcome["completed_target_objects"] = ["framework adoption"]
            evidence = outcome["required_evidence"][0]
            evidence["evidence_strength"] = "measured_curve_data"
            evidence["evidence_claim"] = "The evidence contains measured curve data for framework adoption growth."
            evidence["completed_target_objects"] = ["framework adoption"]
            run = json.loads((run_dir / "run.control.json").read_text(encoding="utf-8"))
            runtime = json.loads((run_dir / "gen-000/runtime.control.json").read_text(encoding="utf-8"))
            review = json.loads((run_dir / "gen-000/review.control.json").read_text(encoding="utf-8"))
            refresh_semantic_base(req)
            apply_hashes(req, run, runtime, "gen-000/runtime.control.json", review, "gen-000/review.control.json")
            (run_dir / "requirements.control.json").write_text(json.dumps(req, indent=2), encoding="utf-8")
            (run_dir / "run.control.json").write_text(json.dumps(run, indent=2), encoding="utf-8")
            (run_dir / "gen-000/runtime.control.json").write_text(json.dumps(runtime, indent=2), encoding="utf-8")

            result = run_script(CONTROL_GUARD, "--run-dir", str(run_dir))

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_guard_accepts_api_v2_already_implemented_wording_as_preserved_behavior(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            write_lean_run(run_dir)
            req = json.loads((run_dir / "requirements.control.json").read_text(encoding="utf-8"))
            sr = req["approved_control"]["source_requirements"][0]
            sr["source"] = {"kind": "user_message", "quote": "implement /api/v2 routes"}
            sr["required_action"] = "verify /api/v2 already implemented behavior"
            sr["requirement_type"] = "implement_behavior"
            sr["required_evidence_strength"] = "behavior_exists"
            sr["target_objects"] = ["/api/v2 routes"]
            sr["completion_checks"] = ["/api/v2 already implemented behavior remains covered"]
            outcome = req["approved_control"]["required_outcomes"][0]
            outcome["completion_claim"] = "Verifies /api/v2 already implemented behavior."
            outcome["completed_target_objects"] = ["/api/v2 routes"]
            evidence = outcome["required_evidence"][0]
            evidence["evidence_strength"] = "behavior_exists"
            evidence["evidence_claim"] = "Behavior exists for the /api/v2 already implemented route."
            evidence["completed_target_objects"] = ["/api/v2 routes"]
            run = json.loads((run_dir / "run.control.json").read_text(encoding="utf-8"))
            runtime = json.loads((run_dir / "gen-000/runtime.control.json").read_text(encoding="utf-8"))
            review = json.loads((run_dir / "gen-000/review.control.json").read_text(encoding="utf-8"))
            refresh_semantic_base(req)
            apply_hashes(req, run, runtime, "gen-000/runtime.control.json", review, "gen-000/review.control.json")
            (run_dir / "requirements.control.json").write_text(json.dumps(req, indent=2), encoding="utf-8")
            (run_dir / "run.control.json").write_text(json.dumps(run, indent=2), encoding="utf-8")
            (run_dir / "gen-000/runtime.control.json").write_text(json.dumps(runtime, indent=2), encoding="utf-8")

            result = run_script(CONTROL_GUARD, "--run-dir", str(run_dir))

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_guard_accepts_legitimate_framework_source_requirement(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            write_lean_run(run_dir)
            req = json.loads((run_dir / "requirements.control.json").read_text(encoding="utf-8"))
            sr = req["approved_control"]["source_requirements"][0]
            sr["source"] = {
                "kind": "user_message",
                "quote": "implement a framework for measurement planning for E and S",
            }
            sr["required_action"] = "define a framework for measurement planning for E and S"
            sr["requirement_type"] = "define_framework_or_plan"
            sr["required_evidence_strength"] = "framework_document"
            sr["target_objects"] = ["E", "S"]
            sr["completion_checks"] = ["framework document covers measurement planning for E and S"]
            outcome = req["approved_control"]["required_outcomes"][0]
            outcome["completion_claim"] = "Defines the measurement planning framework for E and S."
            outcome["completed_target_objects"] = ["E", "S"]
            evidence = outcome["required_evidence"][0]
            evidence["evidence_strength"] = "framework_document"
            evidence["evidence_claim"] = "The framework document covers measurement planning for E and S."
            evidence["completed_target_objects"] = ["E", "S"]
            run = json.loads((run_dir / "run.control.json").read_text(encoding="utf-8"))
            runtime = json.loads((run_dir / "gen-000/runtime.control.json").read_text(encoding="utf-8"))
            review = json.loads((run_dir / "gen-000/review.control.json").read_text(encoding="utf-8"))
            refresh_semantic_base(req)
            apply_hashes(req, run, runtime, "gen-000/runtime.control.json", review, "gen-000/review.control.json")
            (run_dir / "requirements.control.json").write_text(json.dumps(req, indent=2), encoding="utf-8")
            (run_dir / "run.control.json").write_text(json.dumps(run, indent=2), encoding="utf-8")
            (run_dir / "gen-000/runtime.control.json").write_text(json.dumps(runtime, indent=2), encoding="utf-8")

            result = run_script(CONTROL_GUARD, "--run-dir", str(run_dir))

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_guard_rejects_generation_history_over_auto_amendment_limit(self):
        generations = [
            {"id": "gen-000", "strategy_kind": "discovery", "status": "superseded", "runtime": "gen-000/runtime.control.json"},
            {
                "id": "gen-001",
                "strategy_kind": "amendment",
                "status": "superseded",
                "parent": "gen-000",
                "runtime": "gen-001/runtime.control.json",
                "review": "gen-001/review.control.json",
                "amendment_source": "progress.jsonl#A1",
            },
            {
                "id": "gen-002",
                "strategy_kind": "amendment",
                "status": "superseded",
                "parent": "gen-001",
                "runtime": "gen-002/runtime.control.json",
                "review": "gen-002/review.control.json",
                "amendment_source": "progress.jsonl#A2",
            },
            {
                "id": "gen-003",
                "strategy_kind": "amendment",
                "status": "active",
                "parent": "gen-002",
                "runtime": "gen-003/runtime.control.json",
                "review": "gen-003/review.control.json",
                "amendment_source": "progress.jsonl#A3",
            },
        ]
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            write_lean_run(run_dir, generations=generations, current_generation="gen-003")

            result = run_script(CONTROL_GUARD, "--run-dir", str(run_dir))

            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("auto amendment rounds exceed max_auto_amendment_rounds", result.stdout + result.stderr)

    def test_guard_rejects_execution_generation_without_review(self):
        generations = [
            {
                "id": "gen-000",
                "strategy_kind": "execution",
                "status": "active",
                "runtime": "gen-000/runtime.control.json",
                "required_steps": [
                    {
                        "step_id": "S1",
                        "transition": "current generation produces required evidence",
                        "evidence": ["current generation evidence"],
                        "satisfies_outcomes": ["O-lean-startup"],
                    }
                ],
            }
        ]
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            write_lean_run(run_dir, generations=generations)

            result = run_script(CONTROL_GUARD, "--run-dir", str(run_dir))

            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("execution generations must declare review", result.stdout + result.stderr)

    def test_verifier_rejects_discovery_generation_goal_achieved(self):
        generations = [
            {
                "id": "gen-000",
                "strategy_kind": "discovery",
                "status": "active",
                "runtime": "gen-000/runtime.control.json",
                "required_steps": [
                    {
                        "step_id": "S1",
                        "transition": "current generation discovers required evidence path",
                        "evidence": ["current generation evidence"],
                        "satisfies_outcomes": ["O-lean-startup"],
                    }
                ],
            }
        ]
        events = [progress_event("evidence.lean-startup")]
        report = final_report("gen-000", "evidence.lean-startup")
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            write_lean_run(run_dir, generations=generations, progress_events=events, report=report)

            result = run_script(VERIFY, str(run_dir))

            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("discovery generation cannot permit goal_achieved true", result.stdout + result.stderr)

    def test_compiler_creates_initial_generation_runtime_from_lean_run_manifest(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            req = requirements()
            run = run_control(
                generations=[
                    {
                        "id": "gen-000",
                        "strategy_kind": "discovery",
                        "status": "active",
                        "runtime": "gen-000/runtime.control.json",
                    }
                ]
            )
            run["semantic_base_ref"] = copy.deepcopy(req["approved_control"]["semantic_base"])
            (run_dir / "requirements.control.json").write_text(json.dumps(req, indent=2), encoding="utf-8")
            (run_dir / "run.control.json").write_text(json.dumps(run, indent=2), encoding="utf-8")

            result = run_script(COMPILER, "--run-dir", str(run_dir))

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertTrue((run_dir / "gen-000/runtime.control.json").exists())
            self.assertIn("gen-000/runtime.control.json", result.stdout)

    def test_guard_rejects_stale_current_generation(self):
        generations = [
            {"id": "gen-000", "strategy_kind": "discovery", "status": "active", "runtime": "gen-000/runtime.control.json"},
            {"id": "gen-001", "strategy_kind": "discovery", "status": "active", "runtime": "gen-001/runtime.control.json"},
        ]
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            write_lean_run(run_dir, generations=generations, current_generation="gen-001")

            result = run_script(CONTROL_GUARD, "--run-dir", str(run_dir))

            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("exactly current_generation must be active", result.stdout + result.stderr)

    def test_verifier_rejects_api_v2_readiness_substitution_with_unresolved_amendment(self):
        events = [
            progress_event("evidence.api-v2-readiness"),
            progress_event(
                "evidence.api-v2-readiness",
                event_type="control.amendment.proposed",
                amendment_id="A-api-v2-readiness",
            ),
        ]
        report = final_report("gen-000", "evidence.api-v2-readiness")
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            write_lean_run(
                run_dir,
                outcome_id="O-api-v2-implementation",
                required_evidence_id="evidence.api-v2-implementation",
                progress_events=events,
                report=report,
            )

            result = run_script(VERIFY, str(run_dir))

            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("missing required evidence", result.stdout + result.stderr)
            self.assertIn("unresolved amendments block goal_achieved true", result.stdout + result.stderr)

    def test_verifier_rejects_checkpoint_only_full_ceiling_substitution(self):
        events = [
            progress_event("evidence.checkpoint-only"),
            progress_event(
                "evidence.checkpoint-only",
                event_type="control.amendment.proposed",
                amendment_id="A-checkpoint-only",
            ),
        ]
        report = final_report("gen-000", "evidence.checkpoint-only")
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            write_lean_run(
                run_dir,
                outcome_id="O-full-workflow-ceiling",
                required_evidence_id="evidence.full-workflow-ceiling",
                progress_events=events,
                report=report,
            )

            result = run_script(VERIFY, str(run_dir))

            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("missing required evidence", result.stdout + result.stderr)
            self.assertIn("unresolved amendments block goal_achieved true", result.stdout + result.stderr)

    def test_verifier_does_not_reuse_old_generation_evidence_without_explicit_import(self):
        generations = [
            {"id": "gen-000", "strategy_kind": "discovery", "status": "superseded", "runtime": "gen-000/runtime.control.json"},
            {
                "id": "gen-001",
                "strategy_kind": "amendment",
                "status": "active",
                "parent": "gen-000",
                "runtime": "gen-001/runtime.control.json",
                "review": "gen-001/review.control.json",
                "amendment_source": "progress.jsonl#A1",
            },
        ]
        events = [progress_event("evidence.lean-startup", generation="gen-000")]
        report = final_report("gen-001", "evidence.lean-startup")
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            write_lean_run(
                run_dir,
                generations=generations,
                current_generation="gen-001",
                progress_events=events,
                report=report,
            )

            result = run_script(VERIFY, str(run_dir))

            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("missing mainline evidence-backed progress", result.stdout + result.stderr)

    def test_verifier_accepts_explicitly_imported_old_generation_evidence(self):
        generations = [
            {"id": "gen-000", "strategy_kind": "discovery", "status": "superseded", "runtime": "gen-000/runtime.control.json"},
            {
                "id": "gen-001",
                "strategy_kind": "amendment",
                "status": "active",
                "parent": "gen-000",
                "runtime": "gen-001/runtime.control.json",
                "review": "gen-001/review.control.json",
                "amendment_source": "progress.jsonl#A1",
            },
        ]
        events = [progress_event("evidence.lean-startup", generation="gen-000")]
        report = final_report("gen-001", "evidence.lean-startup")

        def import_old(runtime: dict) -> None:
            runtime["imported_evidence"] = ["evidence.lean-startup"]

        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            write_lean_run(
                run_dir,
                generations=generations,
                current_generation="gen-001",
                progress_events=events,
                report=report,
                runtime_edits=import_old,
            )

            result = run_script(VERIFY, str(run_dir))

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertTrue(json.loads(result.stdout)["goal_achieved_permitted"])


if __name__ == "__main__":
    unittest.main()
