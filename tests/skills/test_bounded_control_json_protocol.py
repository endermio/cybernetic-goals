import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from tests.skills.test_control_json_schemas import assert_all_object_schemas_are_strict, validate


ROOT = Path(__file__).resolve().parents[2]
WRITING_GOALS_SKILL = ROOT / ".agents/skills/writing-cybernetic-goals/SKILL.md"
ROUTING_SKILL = ROOT / ".agents/skills/routing-cybernetic-workflows/SKILL.md"
BOUNDED_SKILL = ROOT / ".agents/skills/using-bounded-control-json/SKILL.md"
BOUNDED_VALIDATE = ROOT / ".agents/skills/using-bounded-control-json/scripts/validate_bounded_runtime.py"
BOUNDED_VERIFY = ROOT / ".agents/skills/using-bounded-control-json/scripts/verify_bounded_runtime.py"
FULL_CHAIN_VALIDATE = ROOT / ".agents/skills/using-control-json/scripts/validate_control_chain.py"
BOUNDED_RUNTIME_SCHEMA = ROOT / "schemas/control-json/bounded-runtime.control.schema.json"


def bounded_goal() -> dict:
    return {
        "artifact_type": "goal.control",
        "schema_version": "1.0.0",
        "status": "approved",
        "human_purpose": "Repair one bounded local issue without expanding scope.",
        "objective": "Bounded repair produces the requested local state change.",
        "success_condition": "The bounded runtime required step is complete with evidence.",
        "source_of_truth": {"user_request": "approved bounded repair"},
    }


def bounded_runtime() -> dict:
    return {
        "artifact_type": "bounded-runtime.control",
        "schema_version": "1.0.0",
        "control_kind": "bounded_runtime",
        "status": "compiled",
        "approved_source": {
            "source_type": "user_request",
            "summary": "Approved bounded local repair with fixed meaning.",
        },
        "goal": "goal.control.json",
        "objective": "Repair one bounded local issue.",
        "scope": {
            "work_covered": "Only the bounded repair named in the goal.",
            "allowed_actions": ["edit local files", "run local tests"],
            "forbidden_actions": ["remote destructive actions", "scope expansion"],
        },
        "what_counts_as_done": "Required step S1 is completed with evidence evidence.s1.",
        "runtime": {
            "readonly_files": ["goal.control.json", "runtime.control.json"],
            "writable_files": ["progress.jsonl", "runtime-status.json", "final-report.json"],
        },
        "required_steps": [
            {
                "step_id": "S1",
                "description": "Complete the bounded repair.",
                "evidence_required": ["evidence.s1"],
                "done_when": "progress.jsonl has a passing mainline completion event for S1 with evidence.s1",
            }
        ],
        "progress": {
            "path": "progress.jsonl",
            "append_only": True,
        },
        "verifier": {
            "required_before_goal_achieved": True,
            "command": "python3 .agents/skills/using-bounded-control-json/scripts/verify_bounded_runtime.py",
            "output_schema": "schemas/control-json/final-report.schema.json",
        },
        "stop_conditions": ["runtime JSON is missing, invalid, or insufficient"],
        "final_report": {
            "path": "final-report.json",
        },
    }


def write_bounded_run(run_dir: Path, *, progress_evidence: list[str] | None = None, final_report: bool = True) -> None:
    (run_dir / "goal.control.json").write_text(json.dumps(bounded_goal(), indent=2), encoding="utf-8")
    (run_dir / "runtime.control.json").write_text(json.dumps(bounded_runtime(), indent=2), encoding="utf-8")
    if progress_evidence is not None:
        event = {
            "event_type": "step.completed",
            "schema_version": "1.0.0",
            "occurred_at": "2026-06-09T00:00:00Z",
            "work_package_id": "WP1",
            "required_step": "S1",
            "status": "pass",
            "progress_role": "mainline",
            "counts_as_goal_progress": True,
            "evidence": progress_evidence,
        }
        (run_dir / "progress.jsonl").write_text(json.dumps(event) + "\n", encoding="utf-8")
    if final_report:
        report = {
            "artifact_type": "final-report",
            "schema_version": "1.0.0",
            "goal_achieved": True,
            "what_counts_as_done_met": True,
            "evidence": ["evidence.s1"],
            "work_coverage": {
                "status": "explicitly_bounded",
                "executed": ["S1"],
                "prepared_only": [],
                "forbidden_not_executed": [],
                "out_of_scope": [],
            },
            "remaining_gaps": [],
        }
        (run_dir / "final-report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")


def run_script(script: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["python3", str(script), *args], text=True, capture_output=True)


class BoundedControlJsonProtocolTest(unittest.TestCase):
    def test_bounded_runtime_schema_accepts_minimal_runtime_and_rejects_unknown_fields(self):
        schema = json.loads(BOUNDED_RUNTIME_SCHEMA.read_text(encoding="utf-8"))
        runtime = bounded_runtime()

        assert_all_object_schemas_are_strict(self, schema)
        validate(runtime, schema)

        invalid = dict(runtime)
        invalid["unexpected_field"] = "must fail"
        with self.assertRaises(AssertionError):
            validate(invalid, schema)

    def test_bounded_goal_writer_points_to_bounded_runtime_skill_not_json_pregoal_skill(self):
        text = WRITING_GOALS_SKILL.read_text(encoding="utf-8")
        mode_b = text.split("### Mode B: Bounded File Goal / Audit Goal", 1)[1]

        self.assertIn("using-bounded-control-json", mode_b)
        self.assertNotIn("using-control-json", mode_b)
        self.assertIn("does not require requirements/design/plan/review", mode_b)
        self.assertNotIn("Level 2", mode_b)

    def test_entry_guidance_does_not_route_bounded_runtime_by_level(self):
        text = ROUTING_SKILL.read_text(encoding="utf-8")

        self.assertIn("bounded_runtime", text)
        self.assertIn("using-bounded-control-json", text)
        self.assertNotIn("### Level 2", text)
        self.assertNotIn("Routing decision: Level", text)

    def test_bounded_validator_accepts_goal_and_runtime_only(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            write_bounded_run(run_dir, final_report=False)

            result = run_script(BOUNDED_VALIDATE, str(run_dir))

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            payload = json.loads(result.stdout)
            self.assertTrue(payload["ok"])

    def test_json_pregoal_validator_still_rejects_bounded_goal_and_runtime_only(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            write_bounded_run(run_dir, final_report=False)

            result = run_script(FULL_CHAIN_VALIDATE, str(run_dir))

            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("missing run.control.json", result.stdout + result.stderr)

    def test_bounded_verifier_requires_named_step_evidence(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            write_bounded_run(run_dir, progress_evidence=["wrong.evidence"])

            result = run_script(BOUNDED_VERIFY, str(run_dir))

            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("missing required evidence for required steps: S1: evidence.s1", result.stdout + result.stderr)

    def test_bounded_verifier_permits_complete_bounded_runtime(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            write_bounded_run(run_dir, progress_evidence=["evidence.s1"])

            result = run_script(BOUNDED_VERIFY, str(run_dir))

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            payload = json.loads(result.stdout)
            self.assertTrue(payload["goal_achieved_permitted"])

    def test_bounded_verifier_does_not_require_final_report_to_predeclare_verifier_pass(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            write_bounded_run(run_dir, progress_evidence=["evidence.s1"])

            result = run_script(BOUNDED_VERIFY, str(run_dir))

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            payload = json.loads(result.stdout)
            self.assertTrue(payload["goal_achieved_permitted"])

    def test_bounded_skill_says_final_report_does_not_self_grant_verifier_permission(self):
        text = BOUNDED_SKILL.read_text(encoding="utf-8")

        self.assertIn("final-report.json", text)
        self.assertIn("does not grant verifier permission to itself", text)
        self.assertIn("verifier process output", text)


if __name__ == "__main__":
    unittest.main()
