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
        "id": "semantic-base:target-model-test",
        "hash": canonical_json_hash(approved),
    }


def requirements(outcome_id: str = "O-target-startup", evidence_id: str = "evidence.target-startup") -> dict:
    req = {
        "artifact_type": "requirements.control",
        "schema_version": "1.1.0",
        "status": "approved",
        "approved_control": {
            "human_purpose": "exercise target-model strategy control",
            "primary_object": "generation-aware control run",
            "requested_transformation": "run a target current generation",
            "non_goals": ["do not require expanded root artifacts for startup"],
            "how_we_know_purpose_was_met": "current generation verifier permits completion",
            "where_result_must_show_up": ["run.control.json", "gen-000/runtime.control.json"],
            "what_counts_as_done": "current generation has required evidence and no unresolved amendment",
            "source_requirements": [
                {
                    "id": "SR-target-startup",
                    "source": {"kind": "user_message", "quote": "run a target current generation"},
                    "required_action": "run a target current generation to completion",
                    "requirement_type": "implement_behavior",
                    "required_evidence_strength": "test_result",
                    "target_objects": ["target current generation"],
                    "completion_checks": ["current generation verifier permits completion"],
                    "blocks_goal_achieved_if_missing": True,
                }
            ],
            "required_outcomes": [
                {
                    "id": outcome_id,
                    "statement": f"{outcome_id} is implemented, not merely prepared",
                    "blocks_goal_achieved_if_missing": True,
                    "source_requirements": ["SR-target-startup"],
                    "completion_claim": "Completes the target current generation.",
                    "completed_target_objects": ["target current generation"],
                    "required_evidence": [
                        {
                            "evidence_id": evidence_id,
                            "kind": "progress_event",
                            "description": "mainline current-generation evidence",
                            "evidence_strength": "test_result",
                            "satisfies_source_requirements": ["SR-target-startup"],
                            "evidence_claim": "The current generation verifier permits completion.",
                            "completed_target_objects": ["target current generation"],
                        }
                    ],
                    "not_satisfied_by": ["readiness or partial candidate evidence"],
                }
            ],
            "counterexample_gate_contract": {
                "quality_standard": "Independent reverse review must try to disprove whether the current generation can claim complete or blocked without satisfying the approved source requirements.",
                "required_checked_transformations": [
                    "source_requirements->required_outcomes",
                    "required_outcomes->required_steps",
                    "required_steps->work_packages",
                    "required_steps->runtime_steps",
                    "pre_runtime_compile",
                    "blocked_or_goal_achieved",
                ],
                "minimum_reviewer": {
                    "allowed_kinds": ["subagent", "human", "external"],
                    "independence": "The reviewer must be independent from the execution agent's own completion claim.",
                    "evidence_ref_required": True,
                },
                "reject_if": [
                    "Readiness or partial candidate evidence is accepted as the completed target result.",
                    "A blocked or complete claim is not challenged against the approved source requirements.",
                ],
            },
            "final_answer_format": {
                "medium": "chat summary",
                "required_structure": ["verification"],
            },
        },
    }
    approved = copy.deepcopy(req["approved_control"])
    approved.pop("semantic_base", None)
    req["approved_control"]["semantic_base"] = {
        "id": "semantic-base:target-model-test",
        "hash": canonical_json_hash(approved),
    }
    return req


def default_target_model() -> dict:
    return {
        "result_orientation": ["state_change"],
        "result_content": "specified",
        "path": "known_enough",
        "result_placement": "multi_place",
        "impact_scope": "local_reversible",
    }


def run_control(
    current_generation: str = "gen-000",
    generations: list[dict] | None = None,
    *,
    strategy_policy: str = "frozen_strategy",
) -> dict:
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
                        "satisfies_outcomes": ["O-target-startup"],
                    }
                ],
            }
        ]
    return {
        "artifact_type": "run.control",
        "schema_version": "1.0.0",
        "status": "active",
        "run_id": "target-model-test-run",
        "control_level": 3,
        "target_model": default_target_model(),
        "strategy_policy": strategy_policy,
        "gate_mode": "none",
        "phase_structure": "single_phase",
        "current_generation": current_generation,
        "max_auto_amendment_rounds": 2,
        "semantic_base_ref": {"id": "semantic-base:target-model-test", "hash": "unset"},
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
        "control_level": run["control_level"],
        "target_model": copy.deepcopy(run["target_model"]),
        "strategy_policy": run["strategy_policy"],
        "gate_mode": run["gate_mode"],
        "phase_structure": run["phase_structure"],
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
        "counterexample-gate",
        "horizon-authority",
    ):
        checked_transformations = ["runtime->generation"]
        if check_id == "counterexample-gate":
            checked_transformations = [
                "source_requirements->required_outcomes",
                "required_outcomes->required_steps",
                "required_steps->work_packages",
                "required_steps->runtime_steps",
                "pre_runtime_compile",
                "blocked_or_goal_achieved",
            ]
        check = {
            "check_id": check_id,
            "status": "pass",
            "verdict": "approved",
            "return_to_stage": None,
            "evidence": [f"{check_id} passed for current generation"],
            "findings": [],
            "required_changes": [],
            "checked_transformations": checked_transformations,
        }
        if check_id == "counterexample-gate":
            check["reviewer"] = {
                "kind": "subagent",
                "id": "counterexample-reviewer",
                "evidence_ref": "gen-000/review.control.json#counterexample-gate",
                "summary": "Independent reverse review checked the required decomposition and completion gates.",
            }
        checks.append(check)
    return {
        "artifact_type": "review.control",
        "schema_version": "1.0.0",
        "status": "approved",
        "review_checks": checks,
    }


def amendment_patch(
    amendment_id: str = "A1",
    *,
    parent_generation: str = "gen-000",
    evidence_id: str = "evidence.target-startup.v2",
) -> dict:
    return {
        "artifact_type": "amendment.patch",
        "schema_version": "1.0.0",
        "amendment_id": amendment_id,
        "parent_generation": parent_generation,
        "strategy_kind": "amendment",
        "required_steps": [
            {
                "step_id": "S2",
                "transition": "reviewed amendment strategy produces required evidence",
                "evidence": [evidence_id],
                "satisfies_outcomes": ["O-target-startup"],
            }
        ],
        "runtime_updates": {
            "writable_evidence_paths": ["evidence/"],
            "verifier": {
                "required_before_goal_achieved": True,
                "command": "python3 .agents/skills/using-control-json/scripts/verify_runtime_progress.py",
                "required_outcomes": ["O-target-startup"],
                "output_schema": "final-report.schema.json",
            },
            "imported_evidence": [],
            "invalidated_evidence": ["evidence.target-startup"],
        },
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
        event["affected_source_requirements"] = ["SR-target-startup"]
        event["semantic_base_change"] = False
        event["required_outcomes_changed"] = False
        event["authority_expanded"] = False
        event["proposed_changes"] = ["replace substitute evidence with producing strategy"]
        event["review_required"] = ["intent-preservation", "required-outcome-coverage"]
        event["patch_ref"] = f"amendments/{amendment_id}.patch.json"
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


def write_strategy_run(
    run_dir: Path,
    *,
    outcome_id: str = "O-target-startup",
    required_evidence_id: str = "evidence.target-startup",
    progress_events: list[dict] | None = None,
    report: dict | None = None,
    current_generation: str = "gen-000",
    generations: list[dict] | None = None,
    strategy_policy: str = "frozen_strategy",
    runtime_edits=None,
) -> None:
    req = requirements(outcome_id, required_evidence_id)
    run = run_control(current_generation=current_generation, generations=generations, strategy_policy=strategy_policy)
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
    def test_official_runtime_entrypoints_reject_root_chain_without_run_control(self):
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

    def test_guard_and_runtime_validator_accept_generation_run_without_expanded_root_artifacts(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            write_strategy_run(run_dir)

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
            write_strategy_run(run_dir)
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

    def test_guard_rejects_generation_review_missing_counterexample_gate(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            write_strategy_run(run_dir)
            review_path = run_dir / "gen-000/review.control.json"
            review = json.loads(review_path.read_text(encoding="utf-8"))
            review["review_checks"] = [
                check
                for check in review["review_checks"]
                if check["check_id"] != "counterexample-gate"
            ]
            req = json.loads((run_dir / "requirements.control.json").read_text(encoding="utf-8"))
            run = json.loads((run_dir / "run.control.json").read_text(encoding="utf-8"))
            runtime = json.loads((run_dir / "gen-000/runtime.control.json").read_text(encoding="utf-8"))
            apply_hashes(req, run, runtime, "gen-000/runtime.control.json", review, "gen-000/review.control.json")
            review_path.write_text(json.dumps(review, indent=2), encoding="utf-8")
            (run_dir / "gen-000/runtime.control.json").write_text(json.dumps(runtime, indent=2), encoding="utf-8")

            result = run_script(CONTROL_GUARD, "--run-dir", str(run_dir))
            validate = run_script(VALIDATE, str(run_dir))

            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertNotEqual(validate.returncode, 0, validate.stdout + validate.stderr)
            self.assertIn("counterexample-gate", result.stdout + result.stderr)
            self.assertIn("counterexample-gate", validate.stdout + validate.stderr)

    def test_guard_rejects_counterexample_gate_without_independent_reviewer_provenance(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            write_strategy_run(run_dir)
            review_path = run_dir / "gen-000/review.control.json"
            review = json.loads(review_path.read_text(encoding="utf-8"))
            counterexample = next(check for check in review["review_checks"] if check["check_id"] == "counterexample-gate")
            counterexample.pop("reviewer", None)
            req = json.loads((run_dir / "requirements.control.json").read_text(encoding="utf-8"))
            run = json.loads((run_dir / "run.control.json").read_text(encoding="utf-8"))
            runtime = json.loads((run_dir / "gen-000/runtime.control.json").read_text(encoding="utf-8"))
            apply_hashes(req, run, runtime, "gen-000/runtime.control.json", review, "gen-000/review.control.json")
            review_path.write_text(json.dumps(review, indent=2), encoding="utf-8")
            (run_dir / "gen-000/runtime.control.json").write_text(json.dumps(runtime, indent=2), encoding="utf-8")

            result = run_script(CONTROL_GUARD, "--run-dir", str(run_dir))
            validate = run_script(VALIDATE, str(run_dir))

            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertNotEqual(validate.returncode, 0, validate.stdout + validate.stderr)
            for command_result in (result, validate):
                self.assertIn("counterexample-gate", command_result.stdout + command_result.stderr)
                self.assertIn("independent reviewer provenance", command_result.stdout + command_result.stderr)

    def test_guard_rejects_counterexample_gate_missing_goal_decomposition_edge(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            write_strategy_run(run_dir)
            review_path = run_dir / "gen-000/review.control.json"
            review = json.loads(review_path.read_text(encoding="utf-8"))
            counterexample = next(check for check in review["review_checks"] if check["check_id"] == "counterexample-gate")
            counterexample["checked_transformations"] = [
                transformation
                for transformation in counterexample["checked_transformations"]
                if transformation != "source_requirements->required_outcomes"
            ]
            req = json.loads((run_dir / "requirements.control.json").read_text(encoding="utf-8"))
            run = json.loads((run_dir / "run.control.json").read_text(encoding="utf-8"))
            runtime = json.loads((run_dir / "gen-000/runtime.control.json").read_text(encoding="utf-8"))
            apply_hashes(req, run, runtime, "gen-000/runtime.control.json", review, "gen-000/review.control.json")
            review_path.write_text(json.dumps(review, indent=2), encoding="utf-8")
            (run_dir / "gen-000/runtime.control.json").write_text(json.dumps(runtime, indent=2), encoding="utf-8")

            result = run_script(CONTROL_GUARD, "--run-dir", str(run_dir))
            validate = run_script(VALIDATE, str(run_dir))

            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertNotEqual(validate.returncode, 0, validate.stdout + validate.stderr)
            self.assertIn(
                "counterexample-gate missing required gate points: source_requirements->required_outcomes",
                result.stdout + result.stderr,
            )
            self.assertIn(
                "counterexample-gate missing required gate points: source_requirements->required_outcomes",
                validate.stdout + validate.stderr,
            )

    def test_guard_rejects_counterexample_gate_missing_work_package_decomposition_edge(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            write_strategy_run(run_dir)
            review_path = run_dir / "gen-000/review.control.json"
            review = json.loads(review_path.read_text(encoding="utf-8"))
            counterexample = next(check for check in review["review_checks"] if check["check_id"] == "counterexample-gate")
            counterexample["checked_transformations"] = [
                transformation
                for transformation in counterexample["checked_transformations"]
                if transformation != "required_steps->work_packages"
            ]
            req = json.loads((run_dir / "requirements.control.json").read_text(encoding="utf-8"))
            run = json.loads((run_dir / "run.control.json").read_text(encoding="utf-8"))
            runtime = json.loads((run_dir / "gen-000/runtime.control.json").read_text(encoding="utf-8"))
            apply_hashes(req, run, runtime, "gen-000/runtime.control.json", review, "gen-000/review.control.json")
            review_path.write_text(json.dumps(review, indent=2), encoding="utf-8")
            (run_dir / "gen-000/runtime.control.json").write_text(json.dumps(runtime, indent=2), encoding="utf-8")

            result = run_script(CONTROL_GUARD, "--run-dir", str(run_dir))
            validate = run_script(VALIDATE, str(run_dir))

            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertNotEqual(validate.returncode, 0, validate.stdout + validate.stderr)
            for command_result in (result, validate):
                self.assertIn(
                    "counterexample-gate missing required gate points: required_steps->work_packages",
                    command_result.stdout + command_result.stderr,
                )

    def test_guard_rejects_counterexample_gate_missing_requirements_contract_point(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            write_strategy_run(run_dir)
            req_path = run_dir / "requirements.control.json"
            review_path = run_dir / "gen-000/review.control.json"
            runtime_path = run_dir / "gen-000/runtime.control.json"
            req = json.loads(req_path.read_text(encoding="utf-8"))
            run = json.loads((run_dir / "run.control.json").read_text(encoding="utf-8"))
            review = json.loads(review_path.read_text(encoding="utf-8"))
            runtime = json.loads(runtime_path.read_text(encoding="utf-8"))

            req["approved_control"]["counterexample_gate_contract"]["required_checked_transformations"].append(
                "required_evidence->quality_standard"
            )
            refresh_semantic_base(req)
            apply_hashes(req, run, runtime, "gen-000/runtime.control.json", review, "gen-000/review.control.json")
            req_path.write_text(json.dumps(req, indent=2), encoding="utf-8")
            (run_dir / "run.control.json").write_text(json.dumps(run, indent=2), encoding="utf-8")
            runtime_path.write_text(json.dumps(runtime, indent=2), encoding="utf-8")

            result = run_script(CONTROL_GUARD, "--run-dir", str(run_dir))
            validate = run_script(VALIDATE, str(run_dir))

            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertNotEqual(validate.returncode, 0, validate.stdout + validate.stderr)
            for command_result in (result, validate):
                self.assertIn(
                    "counterexample-gate missing requirements-approved gate points: required_evidence->quality_standard",
                    command_result.stdout + command_result.stderr,
                )

    def test_runtime_validator_requires_runtime_generation_for_step_events(self):
        event = progress_event("evidence.target-startup")
        del event["runtime_generation"]
        events = [event]
        report = final_report("gen-000", "evidence.target-startup")
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            write_strategy_run(run_dir, progress_events=events, report=report)

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
            "affected_source_requirements": ["SR-target-startup"],
            "semantic_base_change": False,
            "required_outcomes_changed": False,
            "authority_expanded": False,
            "proposed_changes": ["replace substitute evidence with producing strategy"],
            "review_required": ["intent-preservation", "required-outcome-coverage"],
            "patch_ref": "amendments/A1.patch.json",
        }
        report = final_report("gen-000", "evidence.target-startup")
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            write_strategy_run(run_dir, progress_events=[event], report=report)

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
        events = [generation_event, progress_event("evidence.target-startup")]
        report = final_report("gen-000", "evidence.target-startup")
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            write_strategy_run(run_dir, progress_events=events, report=report)

            result = run_script(VERIFY, str(run_dir))

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertTrue(json.loads(result.stdout)["goal_achieved_permitted"])

    def test_amendment_orchestrator_requires_patch_review_before_switching_generation(self):
        event = {
            "event_type": "control.amendment.proposed",
            "schema_version": "1.0.0",
            "occurred_at": "2026-06-10T00:00:00Z",
            "runtime_generation": "gen-000",
            "amendment_id": "A1",
            "reason": "current strategy cannot produce required evidence",
            "triggering_observation": "current strategy cannot produce required evidence",
            "affected_stages": ["plan", "runtime"],
            "affected_source_requirements": ["SR-target-startup"],
            "semantic_base_change": False,
            "required_outcomes_changed": False,
            "authority_expanded": False,
            "proposed_changes": ["create reviewed amendment generation"],
            "review_required": ["intent-preservation", "required-outcome-coverage"],
            "patch_ref": "amendments/A1.patch.json",
        }
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            write_strategy_run(run_dir, progress_events=[event], strategy_policy="reviewed_replanning")
            patch_path = run_dir / "amendments/A1.patch.json"
            patch_path.parent.mkdir(parents=True, exist_ok=True)
            patch_path.write_text(json.dumps(amendment_patch(), indent=2), encoding="utf-8")

            result = run_script(AMENDMENT_ORCHESTRATOR, "--run-dir", str(run_dir))

            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual("RunReview", payload["next_allowed_action"])
            self.assertEqual("gen-001", payload["candidate_generation"])
            run = json.loads((run_dir / "run.control.json").read_text(encoding="utf-8"))
            self.assertEqual("gen-000", run["current_generation"])
            self.assertFalse((run_dir / "gen-001/runtime.control.json").exists())
            self.assertFalse((run_dir / "gen-001/review.control.json").exists())
            self.assertTrue((run_dir / "amendments/A1.candidate-generation.json").exists())
            progress = [
                json.loads(line)
                for line in (run_dir / "progress.jsonl").read_text(encoding="utf-8").splitlines()
                if line.strip()
            ]
            self.assertFalse(any(event.get("event_type") == "control.amendment.approved" for event in progress))

    def test_amendment_orchestrator_applies_reviewed_patch_after_review_exists(self):
        event = progress_event(
            "evidence.target-startup",
            event_type="control.amendment.proposed",
            amendment_id="A1",
        )
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            write_strategy_run(run_dir, progress_events=[event], strategy_policy="reviewed_replanning")
            patch_path = run_dir / "amendments/A1.patch.json"
            review_path = run_dir / "amendments/A1.review.control.json"
            patch_path.parent.mkdir(parents=True, exist_ok=True)
            patch_path.write_text(json.dumps(amendment_patch(), indent=2), encoding="utf-8")
            review = approved_generation_review()
            review["review_scope"] = "amendment"
            review["amendment_source"] = "progress.jsonl#A1"
            review["parent_generation"] = "gen-000"
            review_path.write_text(json.dumps(review, indent=2), encoding="utf-8")

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
            self.assertEqual("amendments/A1.patch.json", generations["gen-001"]["patch_ref"])
            self.assertEqual(["evidence.target-startup"], generations["gen-001"]["invalidated_evidence"])
            self.assertEqual(
                [{"step_id": "S2", "transition": "reviewed amendment strategy produces required evidence", "evidence": ["evidence.target-startup.v2"], "satisfies_outcomes": ["O-target-startup"]}],
                generations["gen-001"]["required_steps"],
            )
            self.assertTrue((run_dir / "gen-001/review.control.json").exists())
            self.assertTrue((run_dir / "gen-001/runtime.control.json").exists())
            runtime = json.loads((run_dir / "gen-001/runtime.control.json").read_text(encoding="utf-8"))
            self.assertEqual("S2", runtime["required_steps"][0]["step_id"])
            self.assertEqual(["evidence.target-startup"], runtime["invalidated_evidence"])
            copied_review = json.loads((run_dir / "gen-001/review.control.json").read_text(encoding="utf-8"))
            source_check = next(
                check
                for check in copied_review["review_checks"]
                if check["check_id"] == "source-requirement-preservation"
            )
            self.assertIn("source-requirement-preservation passed for current generation", "\n".join(source_check["evidence"]))
            self.assertEqual(0, run_script(CONTROL_GUARD, "--run-dir", str(run_dir)).returncode)
            progress = [
                json.loads(line)
                for line in (run_dir / "progress.jsonl").read_text(encoding="utf-8").splitlines()
                if line.strip()
            ]
            self.assertTrue(any(item.get("event_type") == "control.amendment.approved" for item in progress))

    def test_amendment_orchestrator_rejects_frozen_strategy_continuation(self):
        event = {
            "event_type": "control.amendment.proposed",
            "schema_version": "1.0.0",
            "occurred_at": "2026-06-10T00:00:00Z",
            "runtime_generation": "gen-000",
            "amendment_id": "A-frozen",
            "reason": "current strategy cannot produce required evidence",
            "triggering_observation": "current frozen strategy is insufficient",
            "affected_stages": ["plan", "runtime"],
            "affected_source_requirements": ["SR-target-startup"],
            "semantic_base_change": False,
            "required_outcomes_changed": False,
            "authority_expanded": False,
            "proposed_changes": ["create reviewed amendment generation"],
            "review_required": ["intent-preservation", "required-outcome-coverage"],
            "patch_ref": "amendments/A-frozen.patch.json",
        }
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            write_strategy_run(run_dir, progress_events=[event], strategy_policy="frozen_strategy")

            result = run_script(AMENDMENT_ORCHESTRATOR, "--run-dir", str(run_dir))

            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual("HumanApprovalRequired", payload["next_allowed_action"])
            self.assertIn("frozen_strategy", "\n".join(payload["errors"]))

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
            "affected_source_requirements": ["SR-target-startup"],
            "semantic_base_change": True,
            "required_outcomes_changed": False,
            "authority_expanded": False,
            "proposed_changes": ["change approved meaning"],
            "review_required": ["intent-preservation"],
            "patch_ref": "amendments/A-anchor.patch.json",
        }
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            write_strategy_run(run_dir, progress_events=[event])

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
                        "evidence": ["evidence.target-startup"],
                        "satisfies_outcomes": ["O-target-startup"],
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
            write_strategy_run(
                run_dir,
                generations=generations,
                current_generation="gen-001",
                strategy_policy="reviewed_replanning",
            )
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
            write_strategy_run(run_dir)
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
                    "source requirements not covered by required evidence: SR-target-startup",
                    result.stdout + result.stderr,
                )

    def test_guard_and_runtime_validator_reject_source_requirement_evidence_below_required_strength(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            write_strategy_run(run_dir)
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
                    "test_result for source requirement SR-target-startup",
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
                        "evidence": ["evidence.target-startup"],
                        "satisfies_outcomes": ["O-target-startup"],
                    }
                ],
            },
        ]
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            write_strategy_run(
                run_dir,
                generations=generations,
                current_generation="gen-001",
                strategy_policy="reviewed_replanning",
            )
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
            write_strategy_run(run_dir, progress_events=events, report=report)

            result = run_script(VERIFY, str(run_dir))

            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("control.amendment.proposed events must include triggering_observation", result.stdout + result.stderr)
            self.assertIn("control.amendment.proposed events must include affected_stages", result.stdout + result.stderr)
            self.assertIn("control.amendment.proposed events must include semantic_base_change", result.stdout + result.stderr)

    def test_runtime_validator_requires_patch_ref_on_amendment_proposal(self):
        event = progress_event(
            "evidence.target-startup",
            event_type="control.amendment.proposed",
            amendment_id="A1",
        )
        del event["patch_ref"]
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            write_strategy_run(
                run_dir,
                progress_events=[event],
                report=final_report("gen-000", "evidence.target-startup"),
            )

            result = run_script(VERIFY, str(run_dir))

            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn(
                "control.amendment.proposed events must include patch_ref",
                result.stdout + result.stderr,
            )

    def test_runtime_validator_requires_affected_source_requirements_on_amendment_proposal(self):
        event = progress_event(
            "evidence.target-startup",
            event_type="control.amendment.proposed",
            amendment_id="A1",
        )
        del event["affected_source_requirements"]
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            write_strategy_run(
                run_dir,
                progress_events=[event],
                report=final_report("gen-000", "evidence.target-startup"),
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
            progress_event("evidence.target-startup"),
            event,
            progress_event(
                "evidence.api-v2-readiness",
                event_type="control.amendment.blocked",
                amendment_id="A-api-v2-readiness",
            ),
        ]
        events[-1]["semantic_base_change"] = True
        report = final_report("gen-000", "evidence.target-startup")
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            write_strategy_run(run_dir, progress_events=events, report=report)

            result = run_script(VERIFY, str(run_dir))

            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("anchor-changing amendments require human decision", result.stdout + result.stderr)

    def test_guard_rejects_run_control_without_max_auto_amendment_rounds(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            write_strategy_run(run_dir)
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
            write_strategy_run(run_dir)
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
            write_strategy_run(run_dir)
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
            write_strategy_run(run_dir)
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
            write_strategy_run(run_dir)
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
            write_strategy_run(run_dir)
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
            write_strategy_run(run_dir)
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
            write_strategy_run(run_dir)
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
            write_strategy_run(run_dir)
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
            write_strategy_run(run_dir, generations=generations, current_generation="gen-003")

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
                        "satisfies_outcomes": ["O-target-startup"],
                    }
                ],
            }
        ]
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            write_strategy_run(run_dir, generations=generations)

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
                        "satisfies_outcomes": ["O-target-startup"],
                    }
                ],
            }
        ]
        events = [progress_event("evidence.target-startup")]
        report = final_report("gen-000", "evidence.target-startup")
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            write_strategy_run(run_dir, generations=generations, progress_events=events, report=report)

            result = run_script(VERIFY, str(run_dir))

            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("discovery generation cannot permit goal_achieved true", result.stdout + result.stderr)

    def test_compiler_creates_initial_generation_runtime_from_run_manifest(self):
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
            write_strategy_run(run_dir, generations=generations, current_generation="gen-001")

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
            write_strategy_run(
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
            write_strategy_run(
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
        events = [progress_event("evidence.target-startup", generation="gen-000")]
        report = final_report("gen-001", "evidence.target-startup")
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            write_strategy_run(
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
        events = [progress_event("evidence.target-startup", generation="gen-000")]
        report = final_report("gen-001", "evidence.target-startup")

        def import_old(runtime: dict) -> None:
            runtime["imported_evidence"] = ["evidence.target-startup"]

        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            write_strategy_run(
                run_dir,
                generations=generations,
                current_generation="gen-001",
                progress_events=events,
                report=report,
                runtime_edits=import_old,
                strategy_policy="reviewed_replanning",
            )

            result = run_script(VERIFY, str(run_dir))

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertTrue(json.loads(result.stdout)["goal_achieved_permitted"])


if __name__ == "__main__":
    unittest.main()
