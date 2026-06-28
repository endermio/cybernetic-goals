import copy
import hashlib
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from tests.skills.test_control_json_schemas import validate
from tests.skills.test_reviewed_replanning_control import (
    apply_hashes,
    counterexample_review_event,
    final_report,
    progress_event,
    refresh_semantic_base,
    write_generation_review_evidence,
    write_information_sufficiency_review_evidence,
    write_strategy_run,
    write_updated_strategy_artifacts,
)


ROOT = Path(__file__).resolve().parents[2]
PROGRESS_EVENT_SCHEMA = ROOT / "schemas/control-json/progress-event.schema.json"
SCRIPTS = ROOT / ".agents/skills/using-control-json/scripts"
VALIDATE = SCRIPTS / "validate_control_chain.py"
APPEND = SCRIPTS / "append_progress_event.py"
VERIFY = SCRIPTS / "verify_runtime_progress.py"
BUILD_PROMPT = SCRIPTS / "build_runtime_prompt.py"


def run_script(script: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["python3", str(script), *args], text=True, capture_output=True)


def approved_hashes(run_dir: Path, runtime: dict) -> dict:
    return {
        filename: hashlib.sha256((run_dir / filename).read_bytes()).hexdigest()
        for filename in runtime["runtime"]["readonly_files"]
    }


class RuntimeJsonProgressVerifierTest(unittest.TestCase):
    def test_progress_event_schema_accepts_mainline_and_supporting_only_role_fields(self):
        schema = json.loads(PROGRESS_EVENT_SCHEMA.read_text(encoding="utf-8"))
        mainline = progress_event("evidence.target-startup")
        supporting = {
            **copy.deepcopy(mainline),
            "progress_role": "supporting_only",
            "counts_as_goal_progress": False,
        }

        validate(mainline, schema)
        validate(supporting, schema)

    def test_progress_event_schema_accepts_runtime_counterexample_review_event(self):
        schema = json.loads(PROGRESS_EVENT_SCHEMA.read_text(encoding="utf-8"))

        validate(counterexample_review_event(), schema)

    def test_validate_control_chain_accepts_complete_generation_run(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            write_strategy_run(run_dir)

            result = run_script(VALIDATE, str(run_dir))

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            payload = json.loads(result.stdout)
            self.assertTrue(payload["ok"])
            self.assertEqual(payload["run_dir"], str(run_dir))

    def test_validate_control_chain_rejects_api_v2_source_requirement_weakened_to_readiness(self):
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
            write_updated_strategy_artifacts(run_dir, req=req, run=run, runtime=runtime, review=review)

            result = run_script(VALIDATE, str(run_dir))

            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("source requirement appears weaker than source quote", result.stdout + result.stderr)

    def test_validate_control_chain_rejects_api_v2_routes_source_requirement_weakened_to_readiness(self):
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
            write_updated_strategy_artifacts(run_dir, req=req, run=run, runtime=runtime, review=review)

            result = run_script(VALIDATE, str(run_dir))

            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("source requirement appears weaker than source quote", result.stdout + result.stderr)

    def test_validate_control_chain_accepts_preserved_measurement_source_requirement_with_framework_words(self):
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
            write_updated_strategy_artifacts(run_dir, req=req, run=run, runtime=runtime, review=review)

            result = run_script(VALIDATE, str(run_dir))

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_validate_control_chain_accepts_api_v2_already_implemented_wording_as_preserved_behavior(self):
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
            write_updated_strategy_artifacts(run_dir, req=req, run=run, runtime=runtime, review=review)

            result = run_script(VALIDATE, str(run_dir))

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_validate_control_chain_accepts_legitimate_framework_source_requirement(self):
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
            write_updated_strategy_artifacts(run_dir, req=req, run=run, runtime=runtime, review=review)

            result = run_script(VALIDATE, str(run_dir))

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_validate_control_chain_rejects_measurement_source_requirement_weakened_to_framework(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            write_strategy_run(run_dir)
            req = json.loads((run_dir / "requirements.control.json").read_text(encoding="utf-8"))
            sr = req["approved_control"]["source_requirements"][0]
            sr["source"] = {"kind": "user_message", "quote": "measure scale curves for E and S"}
            sr["required_action"] = "define scan framework for E and S"
            sr["requirement_type"] = "define_framework_or_plan"
            sr["required_evidence_strength"] = "framework_document"
            sr["target_objects"] = ["E", "S"]
            sr["completion_checks"] = ["scan variables are listed"]
            outcome = req["approved_control"]["required_outcomes"][0]
            outcome["completion_claim"] = "Completes the request by defining scan variables."
            outcome["completed_target_objects"] = ["E", "S"]
            evidence = outcome["required_evidence"][0]
            evidence["evidence_strength"] = "framework_document"
            evidence["evidence_claim"] = "The document lists scan variables."
            evidence["completed_target_objects"] = ["E", "S"]
            run = json.loads((run_dir / "run.control.json").read_text(encoding="utf-8"))
            runtime = json.loads((run_dir / "gen-000/runtime.control.json").read_text(encoding="utf-8"))
            review = json.loads((run_dir / "gen-000/review.control.json").read_text(encoding="utf-8"))
            refresh_semantic_base(req)
            apply_hashes(req, run, runtime, "gen-000/runtime.control.json", review, "gen-000/review.control.json")
            write_updated_strategy_artifacts(run_dir, req=req, run=run, runtime=runtime, review=review)

            result = run_script(VALIDATE, str(run_dir))

            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("source requirement appears weaker than source quote", result.stdout + result.stderr)

    def test_append_progress_event_appends_jsonl_and_rejects_invalid_basics(self):
        event = progress_event("new evidence pointer")
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            write_strategy_run(run_dir)

            good = run_script(APPEND, str(run_dir), "--event-json", json.dumps(event))
            bad = run_script(APPEND, str(run_dir), "--event-json", json.dumps({**event, "evidence": []}))

            self.assertEqual(good.returncode, 0, good.stdout + good.stderr)
            self.assertNotEqual(bad.returncode, 0, bad.stdout + bad.stderr)
            events = [
                json.loads(line)
                for line in (run_dir / "progress.jsonl").read_text(encoding="utf-8").splitlines()
            ]
            self.assertEqual([event], events)
            self.assertIn("evidence must be a non-empty list", bad.stdout + bad.stderr)

    def test_append_progress_event_rejects_undefined_observation_correction_type(self):
        event = {
            "event_type": "observation.corrected",
            "schema_version": "1.1.0",
            "occurred_at": "2026-06-12T00:00:00Z",
            "runtime_generation": "gen-000",
            "evidence": ["evidence.corrected-observation"],
            "summary": "Corrects an earlier observation.",
        }
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            write_strategy_run(run_dir)
            progress_path = run_dir / "progress.jsonl"

            result = run_script(APPEND, str(run_dir), "--event-json", json.dumps(event))

            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("event_type is not recognized", result.stdout + result.stderr)
            self.assertFalse(progress_path.exists())

    def test_append_progress_event_rejects_invalid_observation_correction_metadata(self):
        event = {
            "event_type": "observation.recorded",
            "schema_version": "1.1.0",
            "occurred_at": "2026-06-12T00:00:00Z",
            "runtime_generation": "gen-000",
            "corrects_event_ref": 21,
            "summary": "Corrects an earlier observation.",
        }
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            write_strategy_run(run_dir)

            result = run_script(APPEND, str(run_dir), "--event-json", json.dumps(event))

            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("corrects_event_ref must be a non-empty string", result.stdout + result.stderr)

    def test_verify_runtime_progress_rejects_verifier_bypass_supporting_only_and_not_done_success(self):
        supporting_event = progress_event("evidence.target-startup")
        supporting_event["progress_role"] = "supporting_only"
        supporting_event["counts_as_goal_progress"] = False

        not_done_report = final_report("gen-000", "evidence.target-startup")
        not_done_report["goal_achieved"] = False
        not_done_report["what_counts_as_done_met"] = False
        not_done_report["work_coverage"]["status"] = "partial"
        not_done_report["remaining_gaps"] = ["guard integration still pending"]

        cases = (
            (
                [supporting_event],
                final_report("gen-000", "evidence.target-startup"),
                "missing mainline evidence-backed progress for required steps",
            ),
            (
                [progress_event("evidence.target-startup")],
                not_done_report,
                "not-done final report cannot be treated as success",
            ),
        )
        for events, report, expected in cases:
            with self.subTest(expected=expected), tempfile.TemporaryDirectory() as tmpdir:
                run_dir = Path(tmpdir)
                write_strategy_run(run_dir, progress_events=events, report=report)

                result = run_script(VERIFY, str(run_dir))

                self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertIn(expected, result.stdout + result.stderr)

    def test_verify_runtime_progress_does_not_require_final_report_to_predeclare_verifier_pass(self):
        report = final_report("gen-000", "evidence.target-startup")
        report.pop("verification", None)
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            write_strategy_run(
                run_dir,
                progress_events=[
                    progress_event("evidence.target-startup"),
                    counterexample_review_event(),
                ],
                report=report,
            )

            result = run_script(VERIFY, str(run_dir))

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            payload = json.loads(result.stdout)
            self.assertTrue(payload["goal_achieved_permitted"])

    def test_verify_runtime_progress_rejects_approved_json_mutation_boundary(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            write_strategy_run(
                run_dir,
                progress_events=[progress_event("evidence.target-startup")],
                report=final_report("gen-000", "evidence.target-startup"),
            )
            runtime = json.loads((run_dir / "gen-000/runtime.control.json").read_text(encoding="utf-8"))
            hashes = approved_hashes(run_dir, runtime)
            hash_file = run_dir / "approved-hashes.json"
            hash_file.write_text(json.dumps(hashes, indent=2), encoding="utf-8")

            run_control = json.loads((run_dir / "run.control.json").read_text(encoding="utf-8"))
            run_control["run_id"] = "mutated-during-runtime"
            (run_dir / "run.control.json").write_text(json.dumps(run_control, indent=2), encoding="utf-8")

            result = run_script(VERIFY, str(run_dir), "--approved-hashes", str(hash_file))

            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("approved control JSON changed after runtime start", result.stdout + result.stderr)

    def test_verify_runtime_progress_rejects_approved_json_mutation_from_embedded_hashes(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            write_strategy_run(
                run_dir,
                progress_events=[progress_event("evidence.target-startup")],
                report=final_report("gen-000", "evidence.target-startup"),
            )

            review = json.loads((run_dir / "gen-000/review.control.json").read_text(encoding="utf-8"))
            review["review_checks"][0]["evidence"] = ["mutated during runtime"]
            (run_dir / "gen-000/review.control.json").write_text(json.dumps(review, indent=2), encoding="utf-8")

            result = run_script(VERIFY, str(run_dir))

            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn(
                "runtime.control.json approved_control_hashes mismatch for gen-000/review.control.json",
                result.stdout + result.stderr,
            )

    def test_verify_runtime_progress_rejects_blocking_outcome_without_mainline_evidence(self):
        event = progress_event("evidence.target-startup")
        event["progress_role"] = "supporting_only"
        event["counts_as_goal_progress"] = False
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            write_strategy_run(run_dir, progress_events=[event], report=final_report("gen-000", "evidence.target-startup"))

            result = run_script(VERIFY, str(run_dir))

            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn(
                "missing mainline evidence-backed progress for blocking required outcomes: O-target-startup",
                result.stdout + result.stderr,
            )

    def test_verify_runtime_progress_rejects_missing_required_evidence_id(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            write_strategy_run(
                run_dir,
                progress_events=[progress_event("some-other-evidence")],
                report=final_report("gen-000", "some-other-evidence"),
            )

            result = run_script(VERIFY, str(run_dir))

            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn(
                "missing required evidence for blocking required outcomes: O-target-startup: evidence.target-startup",
                result.stdout + result.stderr,
            )

    def test_verify_runtime_progress_rejects_missing_completed_source_requirement_evidence(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            write_strategy_run(
                run_dir,
                progress_events=[progress_event("evidence.other")],
                report=final_report("gen-000", "evidence.other"),
            )

            result = run_script(VERIFY, str(run_dir))

            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
            payload = json.loads(result.stdout)
            self.assertIn(
                "missing completed evidence for blocking source requirements: SR-target-startup",
                result.stdout + result.stderr,
            )
            self.assertEqual([], payload["completed_source_requirements"])
            self.assertEqual(["SR-target-startup"], payload["source_requirements"])

    def test_verify_runtime_progress_permits_complete_mainline_verified_report(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            write_strategy_run(
                run_dir,
                progress_events=[
                    progress_event("evidence.target-startup"),
                    counterexample_review_event(),
                ],
                report=final_report("gen-000", "evidence.target-startup"),
            )

            result = run_script(VERIFY, str(run_dir))

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            payload = json.loads(result.stdout)
            self.assertTrue(payload["goal_achieved_permitted"])
            self.assertEqual(["O-target-startup"], payload["required_outcomes"])
            self.assertEqual(["O-target-startup"], payload["completed_required_outcomes"])
            self.assertEqual(["SR-target-startup"], payload["source_requirements"])
            self.assertEqual(["SR-target-startup"], payload["completed_source_requirements"])

    def test_verify_runtime_progress_rejects_goal_achieved_without_runtime_counterexample_review(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            write_strategy_run(
                run_dir,
                progress_events=[progress_event("evidence.target-startup")],
                report=final_report("gen-000", "evidence.target-startup"),
            )

            result = run_script(VERIFY, str(run_dir))

            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn(
                "missing runtime counterexample review for required steps: S1",
                result.stdout + result.stderr,
            )
            self.assertIn(
                "missing runtime counterexample review for blocking required outcomes: O-target-startup",
                result.stdout + result.stderr,
            )

    def test_verify_runtime_progress_rejects_counterexample_review_that_misses_stage_goal(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            write_strategy_run(
                run_dir,
                progress_events=[
                    progress_event("evidence.target-startup"),
                    counterexample_review_event(reviewed_steps=["S-other"]),
                ],
                report=final_report("gen-000", "evidence.target-startup"),
            )

            result = run_script(VERIFY, str(run_dir))

            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn(
                "missing runtime counterexample review for required steps: S1",
                result.stdout + result.stderr,
            )

    def test_verify_runtime_progress_rejects_placeholder_counterexample_review_evidence(self):
        review_event = counterexample_review_event(evidence_id="evidence/runtime_counterexample_review.json")
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            write_strategy_run(
                run_dir,
                progress_events=[
                    progress_event("evidence.target-startup"),
                    review_event,
                ],
                report=final_report("gen-000", "evidence.target-startup"),
            )
            (run_dir / "evidence").mkdir(exist_ok=True)
            (run_dir / "evidence/runtime_counterexample_review.json").write_text(
                json.dumps({"status": "pass", "verdict": "approved"}),
                encoding="utf-8",
            )

            result = run_script(VERIFY, str(run_dir))

            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("runtime counterexample review evidence", result.stdout + result.stderr)

    def test_verify_runtime_progress_rejects_counterexample_review_evidence_with_stale_hashes(self):
        review_event = counterexample_review_event(evidence_id="evidence/runtime_counterexample_review.json")
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            write_strategy_run(
                run_dir,
                progress_events=[
                    progress_event("evidence.target-startup"),
                    review_event,
                ],
                report=final_report("gen-000", "evidence.target-startup"),
            )
            reviewer = review_event["reviewer"]
            (run_dir / "evidence/runtime_counterexample_review.json").write_text(
                json.dumps(
                    {
                        "artifact_type": "runtime.counterexample_review.evidence",
                        "independent_review": True,
                        "status": review_event["status"],
                        "verdict": review_event["verdict"],
                        "reviewer": {"kind": reviewer["kind"], "id": reviewer["id"]},
                        "reviewed_steps": review_event["reviewed_steps"],
                        "reviewed_outcomes": review_event["reviewed_outcomes"],
                        "checked_transformations": review_event["checked_transformations"],
                        "evidence": review_event["evidence"],
                        "reviewed_artifact_hashes": {
                            "requirements.control.json": "sha256:stale",
                            "gen-000/runtime.control.json": "sha256:stale",
                        },
                    }
                ),
                encoding="utf-8",
            )

            result = run_script(VERIFY, str(run_dir))

            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("runtime counterexample review evidence", result.stdout + result.stderr)
            self.assertIn("hash", result.stdout + result.stderr)

    def test_verify_runtime_progress_rejects_shape_complete_counterexample_review_without_session(self):
        review_event = counterexample_review_event(evidence_id="evidence/runtime_counterexample_review.json")
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            write_strategy_run(
                run_dir,
                progress_events=[
                    progress_event("evidence.target-startup"),
                    review_event,
                ],
                report=final_report("gen-000", "evidence.target-startup"),
            )
            reviewer = review_event["reviewer"]
            generated = json.loads((run_dir / "evidence/runtime_counterexample_review.json").read_text(encoding="utf-8"))
            generated.pop("reviewer_session")
            generated.pop("review_request")
            generated.update(
                {
                    "status": review_event["status"],
                    "verdict": review_event["verdict"],
                    "reviewer": {"kind": reviewer["kind"], "id": reviewer["id"]},
                    "reviewed_steps": review_event["reviewed_steps"],
                    "reviewed_outcomes": review_event["reviewed_outcomes"],
                    "checked_transformations": review_event["checked_transformations"],
                    "evidence": review_event["evidence"],
                }
            )
            (run_dir / "evidence/runtime_counterexample_review.json").write_text(
                json.dumps(generated),
                encoding="utf-8",
            )

            result = run_script(VERIFY, str(run_dir))

            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("reviewer_session", result.stdout + result.stderr)

    def test_verify_runtime_progress_rejects_remote_counterexample_prompt_or_transcript(self):
        review_event = counterexample_review_event(evidence_id="evidence/runtime_counterexample_review.json")
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            write_strategy_run(
                run_dir,
                progress_events=[
                    progress_event("evidence.target-startup"),
                    review_event,
                ],
                report=final_report("gen-000", "evidence.target-startup"),
            )
            generated = json.loads((run_dir / "evidence/runtime_counterexample_review.json").read_text(encoding="utf-8"))
            generated["reviewer_session"]["transcript_ref"] = "https://example.invalid/runtime-transcript"
            generated["reviewer_session"]["transcript_hash"] = "sha256:" + hashlib.sha256(b"remote transcript").hexdigest()
            generated["review_request"]["prompt_ref"] = "https://example.invalid/runtime-prompt"
            generated["review_request"]["prompt_hash"] = "sha256:" + hashlib.sha256(b"remote prompt").hexdigest()
            (run_dir / "evidence/runtime_counterexample_review.json").write_text(
                json.dumps(generated),
                encoding="utf-8",
            )

            result = run_script(VERIFY, str(run_dir))

            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("ref must be a run-local relative file", result.stdout + result.stderr)

    def test_build_runtime_prompt_outputs_short_goal_pointer(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            write_strategy_run(run_dir)

            result = run_script(BUILD_PROMPT, str(run_dir / "gen-000/runtime.control.json"))

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("/goal Execute the runtime control JSON at", result.stdout)
            self.assertIn("gen-000/runtime.control.json", result.stdout)
            self.assertIn("using-control-json", result.stdout)
            self.assertIn("append_progress_event.py", result.stdout)
            self.assertNotIn("required_steps", result.stdout)
            self.assertLess(len(result.stdout.strip().splitlines()), 3)


if __name__ == "__main__":
    unittest.main()
