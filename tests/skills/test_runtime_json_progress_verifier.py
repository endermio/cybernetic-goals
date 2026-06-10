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
    final_report,
    progress_event,
    refresh_semantic_base,
    write_lean_run,
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
        mainline = progress_event("evidence.lean-startup")
        supporting = {
            **copy.deepcopy(mainline),
            "progress_role": "supporting_only",
            "counts_as_goal_progress": False,
        }

        validate(mainline, schema)
        validate(supporting, schema)

    def test_validate_control_chain_accepts_complete_generation_run(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            write_lean_run(run_dir)

            result = run_script(VALIDATE, str(run_dir))

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            payload = json.loads(result.stdout)
            self.assertTrue(payload["ok"])
            self.assertEqual(payload["run_dir"], str(run_dir))

    def test_validate_control_chain_rejects_api_v2_source_requirement_weakened_to_readiness(self):
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

            result = run_script(VALIDATE, str(run_dir))

            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("source requirement appears weaker than source quote", result.stdout + result.stderr)

    def test_validate_control_chain_accepts_legitimate_framework_source_requirement(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            write_lean_run(run_dir)
            req = json.loads((run_dir / "requirements.control.json").read_text(encoding="utf-8"))
            sr = req["approved_control"]["source_requirements"][0]
            sr["source"] = {"kind": "user_message", "quote": "implement a framework for measurement planning"}
            sr["required_action"] = "define a framework for measurement planning"
            sr["requirement_type"] = "define_framework_or_plan"
            sr["required_evidence_strength"] = "framework_document"
            sr["target_objects"] = ["measurement planning framework"]
            sr["completion_checks"] = ["framework document covers measurement planning"]
            outcome = req["approved_control"]["required_outcomes"][0]
            outcome["completion_claim"] = "Defines the measurement planning framework."
            outcome["completed_target_objects"] = ["measurement planning framework"]
            evidence = outcome["required_evidence"][0]
            evidence["evidence_strength"] = "framework_document"
            evidence["evidence_claim"] = "The framework document covers measurement planning."
            evidence["completed_target_objects"] = ["measurement planning framework"]
            run = json.loads((run_dir / "run.control.json").read_text(encoding="utf-8"))
            runtime = json.loads((run_dir / "gen-000/runtime.control.json").read_text(encoding="utf-8"))
            review = json.loads((run_dir / "gen-000/review.control.json").read_text(encoding="utf-8"))
            refresh_semantic_base(req)
            apply_hashes(req, run, runtime, "gen-000/runtime.control.json", review, "gen-000/review.control.json")
            (run_dir / "requirements.control.json").write_text(json.dumps(req, indent=2), encoding="utf-8")
            (run_dir / "run.control.json").write_text(json.dumps(run, indent=2), encoding="utf-8")
            (run_dir / "gen-000/runtime.control.json").write_text(json.dumps(runtime, indent=2), encoding="utf-8")

            result = run_script(VALIDATE, str(run_dir))

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_append_progress_event_appends_jsonl_and_rejects_invalid_basics(self):
        event = progress_event("new evidence pointer")
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            write_lean_run(run_dir)

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

    def test_verify_runtime_progress_rejects_verifier_bypass_supporting_only_and_not_done_success(self):
        bypass_report = final_report("gen-000", "evidence.lean-startup")
        bypass_report["verification"] = {
            "verifier_result": "not_run",
            "verifier_permits_goal_achieved": False,
        }

        supporting_event = progress_event("evidence.lean-startup")
        supporting_event["progress_role"] = "supporting_only"
        supporting_event["counts_as_goal_progress"] = False

        not_done_report = final_report("gen-000", "evidence.lean-startup")
        not_done_report["goal_achieved"] = False
        not_done_report["what_counts_as_done_met"] = False
        not_done_report["work_coverage"]["status"] = "partial"
        not_done_report["remaining_gaps"] = ["guard integration still pending"]

        cases = (
            (
                [progress_event("evidence.lean-startup")],
                bypass_report,
                "verifier does not permit goal_achieved true",
            ),
            (
                [supporting_event],
                final_report("gen-000", "evidence.lean-startup"),
                "missing mainline evidence-backed progress for required steps",
            ),
            (
                [progress_event("evidence.lean-startup")],
                not_done_report,
                "not-done final report cannot be treated as success",
            ),
        )
        for events, report, expected in cases:
            with self.subTest(expected=expected), tempfile.TemporaryDirectory() as tmpdir:
                run_dir = Path(tmpdir)
                write_lean_run(run_dir, progress_events=events, report=report)

                result = run_script(VERIFY, str(run_dir))

                self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertIn(expected, result.stdout + result.stderr)

    def test_verify_runtime_progress_rejects_approved_json_mutation_boundary(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            write_lean_run(
                run_dir,
                progress_events=[progress_event("evidence.lean-startup")],
                report=final_report("gen-000", "evidence.lean-startup"),
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
            write_lean_run(
                run_dir,
                progress_events=[progress_event("evidence.lean-startup")],
                report=final_report("gen-000", "evidence.lean-startup"),
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
        event = progress_event("evidence.lean-startup")
        event["progress_role"] = "supporting_only"
        event["counts_as_goal_progress"] = False
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            write_lean_run(run_dir, progress_events=[event], report=final_report("gen-000", "evidence.lean-startup"))

            result = run_script(VERIFY, str(run_dir))

            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn(
                "missing mainline evidence-backed progress for blocking required outcomes: O-lean-startup",
                result.stdout + result.stderr,
            )

    def test_verify_runtime_progress_rejects_missing_required_evidence_id(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            write_lean_run(
                run_dir,
                progress_events=[progress_event("some-other-evidence")],
                report=final_report("gen-000", "some-other-evidence"),
            )

            result = run_script(VERIFY, str(run_dir))

            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn(
                "missing required evidence for blocking required outcomes: O-lean-startup: evidence.lean-startup",
                result.stdout + result.stderr,
            )

    def test_verify_runtime_progress_rejects_missing_completed_source_requirement_evidence(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            write_lean_run(
                run_dir,
                progress_events=[progress_event("evidence.other")],
                report=final_report("gen-000", "evidence.other"),
            )

            result = run_script(VERIFY, str(run_dir))

            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
            payload = json.loads(result.stdout)
            self.assertIn(
                "missing completed evidence for blocking source requirements: SR-lean-startup",
                result.stdout + result.stderr,
            )
            self.assertEqual([], payload["completed_source_requirements"])
            self.assertEqual(["SR-lean-startup"], payload["source_requirements"])

    def test_verify_runtime_progress_permits_complete_mainline_verified_report(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            write_lean_run(
                run_dir,
                progress_events=[progress_event("evidence.lean-startup")],
                report=final_report("gen-000", "evidence.lean-startup"),
            )

            result = run_script(VERIFY, str(run_dir))

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            payload = json.loads(result.stdout)
            self.assertTrue(payload["goal_achieved_permitted"])
            self.assertEqual(["O-lean-startup"], payload["required_outcomes"])
            self.assertEqual(["O-lean-startup"], payload["completed_required_outcomes"])
            self.assertEqual(["SR-lean-startup"], payload["source_requirements"])
            self.assertEqual(["SR-lean-startup"], payload["completed_source_requirements"])

    def test_build_runtime_prompt_outputs_short_goal_pointer(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            write_lean_run(run_dir)

            result = run_script(BUILD_PROMPT, str(run_dir / "gen-000/runtime.control.json"))

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("/goal Execute the runtime control JSON at", result.stdout)
            self.assertIn("gen-000/runtime.control.json", result.stdout)
            self.assertIn("using-control-json", result.stdout)
            self.assertNotIn("required_steps", result.stdout)
            self.assertLess(len(result.stdout.strip().splitlines()), 3)


if __name__ == "__main__":
    unittest.main()
