import copy
import hashlib
import json
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CONTROL_GUARD = ROOT / ".agents/skills/compiling-cybernetic-runtime-goals/scripts/control_chain_guard.py"
ORCHESTRATION_GUARD = ROOT / ".agents/skills/orchestrating-cybernetic-pregoal/scripts/orchestration_guard.py"
VALIDATE = ROOT / ".agents/skills/using-control-json/scripts/validate_control_chain.py"
PREDICTOR = ROOT / ".agents/skills/analyzing-cybernetic-requirements/scripts/predict_pregoal_handoff.py"
INFO_LOOP = ROOT / ".agents/skills/analyzing-cybernetic-requirements/scripts/requirements_information_loop.py"


def canonical_json_hash(value: dict, omit_top_level: set[str] | None = None) -> str:
    canonical_value = copy.deepcopy(value)
    for key in omit_top_level or set():
        canonical_value.pop(key, None)
    encoded = json.dumps(canonical_value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return "sha256:" + hashlib.sha256(encoded).hexdigest()


def control_hash(filename: str, artifact: dict) -> str:
    omit = {"approved_control_hashes"} if filename.endswith("runtime.control.json") else set()
    return canonical_json_hash(artifact, omit)


def text_hash(text: str) -> str:
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


def file_hash(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def write_text_artifact(run_dir: Path, ref: str, text: str) -> str:
    path = run_dir / ref
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return file_hash(path)


def bound_refs_for_evidence(evidence_ref: str) -> tuple[str, str]:
    evidence_path = Path(evidence_ref.split("#", 1)[0])
    return (
        str(evidence_path.with_suffix(".prompt.txt")),
        str(evidence_path.with_suffix(".transcript.txt")),
    )


def run_script(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["python3", *map(str, args)],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )


def refresh_semantic_base(requirements: dict) -> None:
    approved = copy.deepcopy(requirements["approved_control"])
    approved.pop("semantic_base", None)
    requirements["approved_control"]["semantic_base"] = {
        "id": "semantic-base:information-sufficiency-test",
        "hash": canonical_json_hash(approved),
    }


def requirements_with_information_sufficiency(*, status: str = "satisfied") -> dict:
    req = {
        "artifact_type": "requirements.control",
        "schema_version": "1.2.0",
        "status": "approved",
        "approved_control": {
            "human_purpose": "integrate a client without guessing its behavior",
            "primary_object": "client integration control run",
            "requested_transformation": "integrate the client after observing its minimal working behavior",
            "non_goals": ["do not design from assumptions"],
            "how_we_know_purpose_was_met": "design starts only after minimal client behavior is observed",
            "where_result_must_show_up": ["requirements.control.json", "orchestration guard"],
            "what_counts_as_done": "minimal client behavior facts are derived, evidenced, and reviewed before design",
            "source_requirements": [
                {
                    "id": "SR-client-minimal-example",
                    "source": {"kind": "user_message", "quote": "integrate this client program"},
                    "required_action": "observe a minimal working client example before design",
                    "requirement_type": "implement_behavior",
                    "required_evidence_strength": "test_result",
                    "target_objects": ["client startup", "client input/output"],
                    "completion_checks": ["minimal client example was run before design"],
                    "blocks_goal_achieved_if_missing": True,
                }
            ],
            "information_sufficiency_check": {
                "status": status,
                "facts": [
                    {
                        "fact_id": "F-client-minimal-example",
                        "statement": "The client starts locally and its input/output boundary is observed.",
                        "derived_from": {
                            "source_requirements": ["SR-client-minimal-example"],
                            "required_outcomes": ["O-client-integration"],
                        },
                        "why_needed": "Without this fact, design can invent the wrong client boundary.",
                        "acceptable_evidence": [
                            {
                                "kind": "command_result",
                                "description": "A minimal client example command ran successfully.",
                            }
                        ],
                        "current_status": status,
                        "evidence_ref": "evidence/client_minimal_example.json",
                        "blocks_design_or_plan_if_missing": True,
                    }
                ],
                "counterexample_review": {
                    "status": "pass" if status == "satisfied" else "fail",
                    "verdict": "approved" if status == "satisfied" else "needs_revision",
                    "reviewer": {
                        "kind": "subagent",
                        "id": "information-sufficiency-reviewer",
                        "evidence_ref": "evidence/information_sufficiency_counterexample.json",
                    },
                    "checked_facts": ["F-client-minimal-example"],
                    "checked_transformations": [
                        "source_requirements->information_sufficiency_facts",
                        "required_outcomes->information_sufficiency_facts",
                        "information_sufficiency_facts->design_plan_entry",
                    ],
                    "findings": [] if status == "satisfied" else ["minimal example is missing"],
                },
            },
            "required_outcomes": [
                {
                    "id": "O-client-integration",
                    "statement": "Client integration is designed only after minimal client facts are known.",
                    "source_requirements": ["SR-client-minimal-example"],
                    "completion_claim": "Pre-design client facts are known and evidenced.",
                    "completed_target_objects": ["client startup", "client input/output"],
                    "blocks_goal_achieved_if_missing": True,
                    "required_evidence": [
                        {
                            "evidence_id": "E-client-minimal-example",
                            "kind": "progress_event",
                            "description": "minimal client example evidence exists",
                            "evidence_strength": "test_result",
                            "satisfies_source_requirements": ["SR-client-minimal-example"],
                            "evidence_claim": "The minimal client example was observed.",
                            "completed_target_objects": ["client startup", "client input/output"],
                        }
                    ],
                    "not_satisfied_by": ["agent-authored required_observations list"],
                    "counterexample_gate": {
                        "completion_standard": "Outcome is complete only when client facts are observed before design.",
                        "required_checked_transformations": [
                            "required_outcome:O-client-integration->completion_gate"
                        ],
                        "required_evidence_ids": ["E-client-minimal-example"],
                        "reject_if": ["The design starts from assumptions instead of the minimal client example."],
                    },
                }
            ],
            "counterexample_gate_contract": {
                "quality_standard": "Independent reviewer must search for missing client facts before design.",
                "required_checked_transformations": [
                    "source_requirements->required_outcomes",
                    "source_requirements->information_sufficiency_facts",
                    "required_outcomes->information_sufficiency_facts",
                    "information_sufficiency_facts->design_plan_entry",
                    "required_outcomes->required_steps",
                    "required_steps->work_packages",
                    "required_steps->runtime_steps",
                    "pre_runtime_compile",
                    "blocked_or_goal_achieved",
                ],
                "minimum_reviewer": {
                    "allowed_kinds": ["subagent", "human", "external"],
                    "independence": "reviewer is independent from the design-writing agent",
                    "evidence_ref_required": True,
                },
                "reject_if": ["A missing blocking fact does not prevent design."],
            },
            "final_answer_format": {"medium": "chat", "required_structure": ["summary"]},
        },
    }
    refresh_semantic_base(req)
    return req


def requirements_with_legacy_information_sufficiency_shape() -> dict:
    req = requirements_with_information_sufficiency()
    req["schema_version"] = "1.1.0"
    req["approved_control"]["information_sufficiency_check"] = {
        "facts": [
            {
                "fact_id": "F-client-minimal-example",
                "fact_statement": "The client starts locally and its input/output boundary is observed.",
                "why_needed": "Without this fact, design can invent the wrong client boundary.",
                "acceptable_evidence": ["minimal example command output"],
                "current_status": "preliminary_probe_only",
                "evidence_ref": "Prior probe evidence, not a run-local file",
                "blocks_design": True,
                "blocks_runtime_pass_if_unaddressed": True,
            }
        ],
        "counterexample_review": {
            "status": "required_before_orchestration_or_design_acceptance",
            "checked_transformations": [
                "source_requirements->information_sufficiency_facts",
                "required_outcomes->information_sufficiency_facts",
            ],
            "findings": ["Independent review must still run."],
        },
    }
    refresh_semantic_base(req)
    return req


def generation_review() -> dict:
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
                "source_requirements->information_sufficiency_facts",
                "required_outcomes->information_sufficiency_facts",
                "information_sufficiency_facts->design_plan_entry",
                "required_outcomes->required_steps",
                "required_steps->work_packages",
                "required_steps->runtime_steps",
                "pre_runtime_compile",
                "blocked_or_goal_achieved",
                "required_outcome:O-client-integration->completion_gate",
            ]
        check = {
            "check_id": check_id,
            "status": "pass",
            "verdict": "approved",
            "return_to_stage": None,
            "evidence": [f"{check_id} evidence"],
            "findings": [],
            "required_changes": [],
            "checked_transformations": checked_transformations,
        }
        if check_id == "counterexample-gate":
            check["reviewer"] = {
                "kind": "subagent",
                "id": "counterexample-reviewer",
                "evidence_ref": "gen-000/review.control.json#counterexample-gate",
            }
        checks.append(check)
    return {
        "artifact_type": "review.control",
        "schema_version": "1.0.0",
        "status": "approved",
        "review_checks": checks,
    }


def write_run(run_dir: Path, requirements: dict) -> None:
    run = {
        "artifact_type": "run.control",
        "schema_version": "1.0.0",
        "status": "active",
        "run_id": "information-sufficiency-test",
        "control_level": 3,
        "target_model": {
            "result_orientation": ["state_change"],
            "result_content": "specified",
            "path": "known_enough",
            "result_placement": "multi_place",
            "impact_scope": "persistent_internal",
        },
        "strategy_policy": "frozen_strategy",
        "gate_mode": "human_gate",
        "phase_structure": "staged",
        "current_generation": "gen-000",
        "max_auto_amendment_rounds": 0,
        "semantic_base_ref": requirements["approved_control"]["semantic_base"],
        "amendment_policy": {
            "may_change": ["implementation_sequence"],
            "must_not_change_without_human": ["semantic_base", "required_outcomes", "authority"],
        },
        "generations": [
            {
                "id": "gen-000",
                "strategy_kind": "execution",
                "status": "active",
                "runtime": "gen-000/runtime.control.json",
                "review": "gen-000/review.control.json",
                "required_steps": [
                    {
                        "step_id": "S1",
                        "transition": "client facts become known before design",
                        "evidence": ["E-client-minimal-example"],
                        "satisfies_outcomes": ["O-client-integration"],
                    }
                ],
            }
        ],
    }
    review = generation_review()
    runtime = {
        "artifact_type": "runtime.control",
        "schema_version": "1.0.0",
        "status": "compiled",
        "control_level": 3,
        "target_model": copy.deepcopy(run["target_model"]),
        "strategy_policy": run["strategy_policy"],
        "gate_mode": run["gate_mode"],
        "phase_structure": run["phase_structure"],
        "generation": {"id": "gen-000"},
        "semantic_base_ref": requirements["approved_control"]["semantic_base"],
        "approved_control": {
            "objective": requirements["approved_control"]["requested_transformation"],
            "what_counts_as_done": requirements["approved_control"]["what_counts_as_done"],
        },
        "approved_control_hashes": {},
        "runtime": {
            "readonly_files": [
                "requirements.control.json",
                "run.control.json",
                "gen-000/review.control.json",
                "gen-000/runtime.control.json",
            ],
            "writable_files": ["progress.jsonl", "runtime-status.json", "final-report.json"],
            "writable_evidence_paths": ["evidence/"],
        },
        "required_steps": copy.deepcopy(run["generations"][0]["required_steps"]),
        "progress": {"event_schema": "progress-event.schema.json", "append_only": True},
        "verifier": {
            "required_before_goal_achieved": True,
            "command": "python3 .agents/skills/using-control-json/scripts/verify_runtime_progress.py",
            "required_outcomes": ["O-client-integration"],
            "output_schema": "final-report.schema.json",
        },
        "imported_evidence": [],
        "invalidated_evidence": [],
    }
    runtime["approved_control_hashes"] = {
        "requirements.control.json": control_hash("requirements.control.json", requirements),
        "run.control.json": control_hash("run.control.json", run),
        "gen-000/review.control.json": control_hash("gen-000/review.control.json", review),
        "gen-000/runtime.control.json": control_hash("gen-000/runtime.control.json", runtime),
    }
    (run_dir / "gen-000").mkdir(parents=True, exist_ok=True)
    (run_dir / "evidence").mkdir(parents=True, exist_ok=True)
    (run_dir / "evidence/client_minimal_example.json").write_text(
        json.dumps({"status": "pass", "observed": ["startup", "input_output_boundary"]}),
        encoding="utf-8",
    )
    (run_dir / "requirements.control.json").write_text(json.dumps(requirements, indent=2), encoding="utf-8")
    info_check = requirements["approved_control"].get("information_sufficiency_check")
    review = info_check.get("counterexample_review") if isinstance(info_check, dict) else None
    reviewer = review.get("reviewer") if isinstance(review, dict) else None
    if isinstance(review, dict) and isinstance(reviewer, dict):
        reviewed_hashes = {
            "requirements.control.json": control_hash("requirements.control.json", requirements)
        }
        prompt_ref, transcript_ref = bound_refs_for_evidence(reviewer["evidence_ref"])
        prompt_hash = write_text_artifact(run_dir, prompt_ref, "information sufficiency counterexample review")
        transcript_hash = write_text_artifact(
            run_dir,
            transcript_ref,
            "independent information sufficiency reviewer transcript",
        )
        (run_dir / "evidence/information_sufficiency_counterexample.json").write_text(
            json.dumps(
                {
                    "artifact_type": "information_sufficiency.counterexample_review.evidence",
                    "independent_review": True,
                    "status": review.get("status"),
                    "verdict": review.get("verdict"),
                    "reviewer": {"kind": reviewer.get("kind"), "id": reviewer.get("id")},
                    "reviewer_session": {
                        "kind": reviewer.get("kind"),
                        "id": reviewer.get("id"),
                        "transcript_ref": transcript_ref,
                        "transcript_hash": transcript_hash,
                    },
                    "review_request": {
                        "prompt_ref": prompt_ref,
                        "prompt_hash": prompt_hash,
                        "reviewed_artifact_hashes": reviewed_hashes,
                    },
                    "checked_facts": review.get("checked_facts"),
                    "checked_transformations": review.get("checked_transformations"),
                    "findings": review.get("findings", []),
                    "reviewed_artifact_hashes": reviewed_hashes,
                },
                indent=2,
            ),
            encoding="utf-8",
        )
    (run_dir / "run.control.json").write_text(json.dumps(run, indent=2), encoding="utf-8")
    (run_dir / "gen-000/review.control.json").write_text(json.dumps(review, indent=2), encoding="utf-8")
    (run_dir / "gen-000/runtime.control.json").write_text(json.dumps(runtime, indent=2), encoding="utf-8")


class InformationSufficiencyGateTest(unittest.TestCase):
    def test_approved_v1_1_without_information_sufficiency_check_is_not_handoff_ready(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            req = requirements_with_information_sufficiency(status="satisfied")
            req["schema_version"] = "1.1.0"
            del req["approved_control"]["information_sufficiency_check"]
            refresh_semantic_base(req)
            write_run(run_dir, req)

            guard = run_script(CONTROL_GUARD, "--run-dir", str(run_dir))
            validate = run_script(VALIDATE, str(run_dir))
            predictor = run_script(PREDICTOR, "--run-dir", str(run_dir))
            orchestration = run_script(
                ORCHESTRATION_GUARD,
                "--state",
                "before-design",
                "--run-dir",
                str(run_dir),
                "--json",
            )

            for result in (guard, validate, predictor, orchestration):
                self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertIn("information_sufficiency_check", result.stdout + result.stderr)
            self.assertIn("is required", guard.stdout + guard.stderr)
            payload = json.loads(orchestration.stdout)
            self.assertEqual("RunInformationSufficiencyCheck", payload["next_allowed_action"])

    def test_guard_runtime_validator_and_predictor_reject_legacy_information_sufficiency_shape(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            req = requirements_with_legacy_information_sufficiency_shape()
            write_run(run_dir, req)

            guard = run_script(CONTROL_GUARD, "--run-dir", str(run_dir))
            validate = run_script(VALIDATE, str(run_dir))
            predictor = run_script(PREDICTOR, "--run-dir", str(run_dir))

            for result in (guard, validate, predictor):
                self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
                combined = result.stdout + result.stderr
                self.assertIn("information_sufficiency_check", combined)
                self.assertIn("statement must be non-empty", combined)
                self.assertIn("derived_from must be an object", combined)

    def test_predictor_rejects_unexecuted_information_counterexample_review(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            req = requirements_with_information_sufficiency()
            req["approved_control"]["information_sufficiency_check"]["counterexample_review"] = {
                "status": "required_before_orchestration_or_design_acceptance",
                "verdict": "needs_revision",
                "checked_facts": ["F-client-minimal-example"],
                "checked_transformations": [
                    "source_requirements->information_sufficiency_facts",
                    "required_outcomes->information_sufficiency_facts",
                    "information_sufficiency_facts->design_plan_entry",
                ],
                "findings": ["Independent review has not run."],
            }
            refresh_semantic_base(req)
            (run_dir / "requirements.control.json").write_text(json.dumps(req, indent=2), encoding="utf-8")

            result = run_script(PREDICTOR, "--run-dir", str(run_dir))

            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("counterexample_review", result.stdout + result.stderr)
            self.assertIn("pass with verdict approved", result.stdout + result.stderr)

    def test_predictor_rejects_information_gathering_before_handoff_even_if_top_level_is_approved(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            req = requirements_with_information_sufficiency(status="needs_information_gathering")
            fact = req["approved_control"]["information_sufficiency_check"]["facts"][0]
            fact["current_status"] = "needs_information_gathering"
            req["approved_control"]["information_sufficiency_check"]["collection_actions"] = [
                {
                    "action_id": "IA-client-minimal-example",
                    "fact_id": "F-client-minimal-example",
                    "action_type": "run_no_side_effect_probe",
                    "status": "planned",
                    "why_safe_or_needed": "A minimal local example is required before design can name the client boundary.",
                    "evidence_ref": "evidence/client_minimal_example.json",
                    "command": ["python3", "-c", "print('client ok')"],
                    "working_dir": ".",
                    "allow_automatic_execution": True,
                }
            ]
            refresh_semantic_base(req)
            (run_dir / "requirements.control.json").write_text(json.dumps(req, indent=2), encoding="utf-8")

            result = run_script(PREDICTOR, "--run-dir", str(run_dir))

            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("information_sufficiency_check status must be satisfied", result.stdout + result.stderr)

    def test_guard_rejects_missing_information_sufficiency_for_v1_2(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            req = requirements_with_information_sufficiency()
            del req["approved_control"]["information_sufficiency_check"]
            refresh_semantic_base(req)
            write_run(run_dir, req)

            result = run_script(CONTROL_GUARD, "--run-dir", str(run_dir))
            validate = run_script(VALIDATE, str(run_dir))

            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertNotEqual(validate.returncode, 0, validate.stdout + validate.stderr)
            self.assertIn("information_sufficiency_check", result.stdout + result.stderr)
            self.assertIn("information_sufficiency_check", validate.stdout + validate.stderr)

    def test_guard_rejects_unsatisfied_blocking_information_fact(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            req = requirements_with_information_sufficiency(status="missing")
            write_run(run_dir, req)

            result = run_script(CONTROL_GUARD, "--run-dir", str(run_dir))

            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("F-client-minimal-example", result.stdout + result.stderr)
            self.assertIn("not satisfied", result.stdout + result.stderr)

    def test_guard_and_runtime_validator_reject_satisfied_check_with_unfinished_nonblocking_fact(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            req = requirements_with_information_sufficiency(status="satisfied")
            fact = req["approved_control"]["information_sufficiency_check"]["facts"][0]
            fact["current_status"] = "needs_user_input"
            fact["blocks_design_or_plan_if_missing"] = False
            refresh_semantic_base(req)
            write_run(run_dir, req)

            result = run_script(CONTROL_GUARD, "--run-dir", str(run_dir))
            validate = run_script(VALIDATE, str(run_dir))

            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertNotEqual(validate.returncode, 0, validate.stdout + validate.stderr)
            self.assertIn("not terminal", result.stdout + result.stderr)
            self.assertIn("not terminal", validate.stdout + validate.stderr)

    def test_guard_rejects_fact_not_derived_from_source_or_outcome(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            req = requirements_with_information_sufficiency()
            fact = req["approved_control"]["information_sufficiency_check"]["facts"][0]
            fact["derived_from"] = {"source_requirements": [], "required_outcomes": []}
            refresh_semantic_base(req)
            write_run(run_dir, req)

            result = run_script(CONTROL_GUARD, "--run-dir", str(run_dir))

            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("derived_from", result.stdout + result.stderr)

    def test_guard_and_runtime_validator_reject_missing_information_evidence_ref(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            req = requirements_with_information_sufficiency()
            fact = req["approved_control"]["information_sufficiency_check"]["facts"][0]
            fact["evidence_ref"] = "evidence/does_not_exist.json"
            refresh_semantic_base(req)
            write_run(run_dir, req)

            result = run_script(CONTROL_GUARD, "--run-dir", str(run_dir))
            validate = run_script(VALIDATE, str(run_dir))

            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertNotEqual(validate.returncode, 0, validate.stdout + validate.stderr)
            self.assertIn("evidence_ref does not exist", result.stdout + result.stderr)
            self.assertIn("evidence_ref does not exist", validate.stdout + validate.stderr)

    def test_guard_rejects_required_observations_substitute_inside_sufficiency_check(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            req = requirements_with_information_sufficiency()
            req["approved_control"]["information_sufficiency_check"]["required_observations"] = [
                "client can start locally"
            ]
            refresh_semantic_base(req)
            write_run(run_dir, req)

            result = run_script(CONTROL_GUARD, "--run-dir", str(run_dir))

            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("unknown fields ['required_observations']", result.stdout + result.stderr)

    def test_guard_and_runtime_validator_reject_missing_information_counterexample_reviewer(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            req = requirements_with_information_sufficiency()
            req["approved_control"]["information_sufficiency_check"]["counterexample_review"].pop("reviewer")
            refresh_semantic_base(req)
            write_run(run_dir, req)

            result = run_script(CONTROL_GUARD, "--run-dir", str(run_dir))
            validate = run_script(VALIDATE, str(run_dir))

            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertNotEqual(validate.returncode, 0, validate.stdout + validate.stderr)
            self.assertIn("counterexample_review reviewer", result.stdout + result.stderr)
            self.assertIn("counterexample_review reviewer", validate.stdout + validate.stderr)

    def test_guard_and_runtime_validator_reject_placeholder_information_counterexample_evidence(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            req = requirements_with_information_sufficiency()
            write_run(run_dir, req)
            (run_dir / "evidence/information_sufficiency_counterexample.json").write_text(
                json.dumps({"status": "pass", "verdict": "approved"}),
                encoding="utf-8",
            )

            result = run_script(CONTROL_GUARD, "--run-dir", str(run_dir))
            validate = run_script(VALIDATE, str(run_dir))

            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertNotEqual(validate.returncode, 0, validate.stdout + validate.stderr)
            self.assertIn("counterexample_review evidence", result.stdout + result.stderr)
            self.assertIn("counterexample_review evidence", validate.stdout + validate.stderr)

    def test_guard_and_runtime_validator_reject_shape_complete_counterexample_without_provenance(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            req = requirements_with_information_sufficiency()
            write_run(run_dir, req)
            review = req["approved_control"]["information_sufficiency_check"]["counterexample_review"]
            reviewer = review["reviewer"]
            (run_dir / "evidence/information_sufficiency_counterexample.json").write_text(
                json.dumps(
                    {
                        "artifact_type": "information_sufficiency.counterexample_review.evidence",
                        "independent_review": True,
                        "status": review["status"],
                        "verdict": review["verdict"],
                        "reviewer": {"kind": reviewer["kind"], "id": reviewer["id"]},
                        "checked_facts": review["checked_facts"],
                        "checked_transformations": review["checked_transformations"],
                        "findings": [],
                        "reviewed_artifact_hashes": {
                            "requirements.control.json": control_hash("requirements.control.json", req)
                        },
                    },
                    indent=2,
                ),
                encoding="utf-8",
            )

            result = run_script(CONTROL_GUARD, "--run-dir", str(run_dir))
            validate = run_script(VALIDATE, str(run_dir))

            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertNotEqual(validate.returncode, 0, validate.stdout + validate.stderr)
            self.assertIn("reviewer_session", result.stdout + result.stderr)
            self.assertIn("reviewer_session", validate.stdout + validate.stderr)

    def test_guard_and_runtime_validator_reject_remote_information_counterexample_prompt_or_transcript(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            req = requirements_with_information_sufficiency()
            write_run(run_dir, req)
            evidence_path = run_dir / "evidence/information_sufficiency_counterexample.json"
            evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
            evidence["reviewer_session"]["transcript_ref"] = "https://example.invalid/reviewer-transcript"
            evidence["reviewer_session"]["transcript_hash"] = text_hash("remote transcript")
            evidence["review_request"]["prompt_ref"] = "https://example.invalid/review-prompt"
            evidence["review_request"]["prompt_hash"] = text_hash("remote prompt")
            evidence_path.write_text(json.dumps(evidence, indent=2), encoding="utf-8")

            result = run_script(CONTROL_GUARD, "--run-dir", str(run_dir))
            validate = run_script(VALIDATE, str(run_dir))

            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertNotEqual(validate.returncode, 0, validate.stdout + validate.stderr)
            for command_result in (result, validate):
                output = command_result.stdout + command_result.stderr
                self.assertIn("ref must be a run-local relative file", output)

    def test_orchestration_routes_all_pregoal_states_to_information_sufficiency_first(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            req = requirements_with_information_sufficiency(status="missing")
            (run_dir / "requirements.control.json").write_text(json.dumps(req, indent=2), encoding="utf-8")

            for state in ("before-design", "before-goal", "before-policy", "before-review", "before-runtime-compile"):
                with self.subTest(state=state):
                    result = run_script(
                        ORCHESTRATION_GUARD,
                        "--state",
                        state,
                        "--run-dir",
                        str(run_dir),
                        "--json",
                    )

                    self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
                    payload = json.loads(result.stdout)
                    self.assertEqual("RunInformationSufficiencyCheck", payload["next_allowed_action"])
                    self.assertIn("information_sufficiency_check", "\n".join(payload["errors"]))

    def test_orchestration_rejects_satisfied_check_with_unfinished_nonblocking_fact(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            req = requirements_with_information_sufficiency(status="satisfied")
            fact = req["approved_control"]["information_sufficiency_check"]["facts"][0]
            fact["current_status"] = "needs_user_input"
            fact["blocks_design_or_plan_if_missing"] = False
            refresh_semantic_base(req)
            (run_dir / "requirements.control.json").write_text(json.dumps(req, indent=2), encoding="utf-8")
            (run_dir / "evidence").mkdir(parents=True, exist_ok=True)
            (run_dir / "evidence/client_minimal_example.json").write_text(
                json.dumps({"status": "pass"}),
                encoding="utf-8",
            )
            (run_dir / "evidence/information_sufficiency_counterexample.json").write_text(
                json.dumps({"status": "pass", "verdict": "approved"}),
                encoding="utf-8",
            )

            result = run_script(
                ORCHESTRATION_GUARD,
                "--state",
                "before-design",
                "--run-dir",
                str(run_dir),
                "--json",
            )

            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual("RunInformationSufficiencyCheck", payload["next_allowed_action"])
            self.assertIn("not terminal", "\n".join(payload["errors"]))

    def test_orchestration_before_policy_routes_to_information_sufficiency_before_policy(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            req = requirements_with_information_sufficiency(status="missing")
            (run_dir / "requirements.control.json").write_text(json.dumps(req, indent=2), encoding="utf-8")

            result = run_script(
                ORCHESTRATION_GUARD,
                "--state",
                "before-policy",
                "--run-dir",
                str(run_dir),
                "--json",
            )

            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual("RunInformationSufficiencyCheck", payload["next_allowed_action"])
            self.assertIn("information_sufficiency_check", "\n".join(payload["errors"]))

    def test_information_loop_routes_counterexample_review_without_user_authorization(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            req = requirements_with_information_sufficiency(status="needs_counterexample_review")
            info_check = req["approved_control"]["information_sufficiency_check"]
            info_check["counterexample_review"] = {
                "status": "needs_revision",
                "verdict": "needs_revision",
                "reviewer": {
                    "kind": "subagent",
                    "id": "pending-information-sufficiency-reviewer",
                    "evidence_ref": "evidence/information_sufficiency_counterexample.json",
                },
                "checked_facts": [],
                "checked_transformations": [],
                "findings": ["review has not run yet"],
            }
            refresh_semantic_base(req)
            (run_dir / "requirements.control.json").write_text(json.dumps(req, indent=2), encoding="utf-8")

            result = run_script(INFO_LOOP, "--run-dir", str(run_dir), "--json")

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual("RunInformationCounterexampleReview", payload["next_action"])
            self.assertEqual("agent", payload["action_owner"])
            self.assertFalse(payload["requires_user_authorization"])
            self.assertFalse(payload["user_action_required"])
            self.assertTrue(payload["agent_must_continue"])
            self.assertIn("F-client-minimal-example", payload["review_prompt"])

    def test_information_loop_plain_output_marks_internal_review_as_agent_owned(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            req = requirements_with_information_sufficiency(status="needs_counterexample_review")
            info_check = req["approved_control"]["information_sufficiency_check"]
            info_check["counterexample_review"] = {
                "status": "needs_revision",
                "verdict": "needs_revision",
                "reviewer": {
                    "kind": "subagent",
                    "id": "pending-information-sufficiency-reviewer",
                    "evidence_ref": "evidence/information_sufficiency_counterexample.json",
                },
                "checked_facts": [],
                "checked_transformations": [],
                "findings": ["review has not run yet"],
            }
            refresh_semantic_base(req)
            (run_dir / "requirements.control.json").write_text(json.dumps(req, indent=2), encoding="utf-8")

            result = run_script(INFO_LOOP, "--run-dir", str(run_dir))

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("NEXT: RunInformationCounterexampleReview", result.stdout)
            self.assertIn("ACTION_OWNER: agent", result.stdout)
            self.assertIn("AGENT_MUST_CONTINUE: true", result.stdout)
            self.assertIn("USER_ACTION_REQUIRED: false", result.stdout)
            self.assertIn("DO_NOT_ASK_USER_AUTHORIZATION", result.stdout)

    def test_information_loop_exposes_safe_information_gathering_actions(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            req = requirements_with_information_sufficiency(status="needs_information_gathering")
            info_check = req["approved_control"]["information_sufficiency_check"]
            info_check["facts"][0]["current_status"] = "needs_information_gathering"
            info_check["collection_actions"] = [
                {
                    "action_id": "IA-client-minimal-example",
                    "fact_id": "F-client-minimal-example",
                    "action_type": "run_no_side_effect_probe",
                    "status": "planned",
                    "why_safe_or_needed": "A local minimal example is required before design can name the client boundary.",
                    "evidence_ref": "evidence/client_minimal_example.json",
                    "command": ["python3", "-c", "print('client ok')"],
                    "working_dir": ".",
                    "allow_automatic_execution": True,
                }
            ]
            refresh_semantic_base(req)
            (run_dir / "requirements.control.json").write_text(json.dumps(req, indent=2), encoding="utf-8")

            result = run_script(INFO_LOOP, "--run-dir", str(run_dir), "--json")

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual("RunInformationGathering", payload["next_action"])
            self.assertEqual(["IA-client-minimal-example"], [item["action_id"] for item in payload["automatic_actions"]])
            self.assertEqual([], payload["user_actions"])

    def test_information_loop_surfaces_user_input_before_approval(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            req = requirements_with_information_sufficiency(status="needs_user_input")
            info_check = req["approved_control"]["information_sufficiency_check"]
            info_check["facts"][0]["current_status"] = "needs_user_input"
            info_check["collection_actions"] = [
                {
                    "action_id": "IA-client-credential",
                    "fact_id": "F-client-minimal-example",
                    "action_type": "ask_user",
                    "status": "planned",
                    "why_safe_or_needed": "The client credential cannot be inferred from local files.",
                    "evidence_ref": "evidence/client_credential_decision.json",
                    "question": "Please provide the client credential or confirm that this integration should use a mock credential.",
                }
            ]
            refresh_semantic_base(req)
            (run_dir / "requirements.control.json").write_text(json.dumps(req, indent=2), encoding="utf-8")

            result = run_script(INFO_LOOP, "--run-dir", str(run_dir), "--json")

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual("AskUserForInformation", payload["next_action"])
            self.assertEqual([], payload["automatic_actions"])
            self.assertIn("client credential", payload["user_actions"][0]["question"])


if __name__ == "__main__":
    unittest.main()
