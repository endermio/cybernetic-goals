import copy
import hashlib
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from tests.skills.test_control_json_schemas import validate


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "tests/fixtures/cybernetics/runtime_verifier/control_runs.json"
PROGRESS_EVENT_SCHEMA = ROOT / "schemas/control-json/progress-event.schema.json"
SCRIPTS = ROOT / ".agents/skills/using-control-json/scripts"
VALIDATE = SCRIPTS / "validate_control_chain.py"
APPEND = SCRIPTS / "append_progress_event.py"
VERIFY = SCRIPTS / "verify_runtime_progress.py"
BUILD_PROMPT = SCRIPTS / "build_runtime_prompt.py"


def load_fixture() -> dict:
    return json.loads(FIXTURE.read_text(encoding="utf-8"))["valid"]


def write_run(run_dir: Path, fixture: dict) -> None:
    for filename, payload in fixture["control_files"].items():
        (run_dir / filename).write_text(json.dumps(payload, indent=2), encoding="utf-8")
    if "progress_events" in fixture:
        (run_dir / "progress.jsonl").write_text(
            "".join(json.dumps(event) + "\n" for event in fixture["progress_events"]),
            encoding="utf-8",
        )
    if "final_report" in fixture:
        (run_dir / "final-report.json").write_text(
            json.dumps(fixture["final_report"], indent=2),
            encoding="utf-8",
        )


def run_script(script: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["python3", str(script), *args],
        text=True,
        capture_output=True,
    )


def approved_hashes(run_dir: Path, runtime: dict) -> dict:
    return {
        filename: hashlib.sha256((run_dir / filename).read_bytes()).hexdigest()
        for filename in runtime["runtime"]["readonly_files"]
    }


class RuntimeJsonProgressVerifierTest(unittest.TestCase):
    def test_progress_event_schema_accepts_mainline_and_supporting_only_role_fields(self):
        schema = json.loads(PROGRESS_EVENT_SCHEMA.read_text(encoding="utf-8"))
        mainline = load_fixture()["progress_events"][0]
        supporting = {
            **copy.deepcopy(mainline),
            "progress_role": "supporting_only",
            "counts_as_goal_progress": False,
        }

        validate(mainline, schema)
        validate(supporting, schema)

    def test_validate_control_chain_accepts_complete_json_run(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            write_run(run_dir, load_fixture())

            result = run_script(VALIDATE, str(run_dir))

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            payload = json.loads(result.stdout)
            self.assertTrue(payload["ok"])
            self.assertEqual(payload["run_dir"], str(run_dir))

    def test_validate_control_chain_rejects_missing_review_checks(self):
        fixture = load_fixture()
        fixture["control_files"]["review.control.json"]["review_checks"] = [
            fixture["control_files"]["review.control.json"]["review_checks"][0]
        ]
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            write_run(run_dir, fixture)

            result = run_script(VALIDATE, str(run_dir))

            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("missing required review checks", result.stdout + result.stderr)

    def test_validate_control_chain_rejects_weaker_answer_method_and_missing_mandatory_nodes(self):
        weaker = load_fixture()
        for filename in ("requirements.control.json", "design.control.json", "goal.control.json"):
            weaker["control_files"][filename]["registry_bindings"]["answer_method_key"] = "component-inventory-completion"

        missing_node = load_fixture()
        missing_node["control_files"]["design.control.json"]["approved_control"]["required_answer_path"] = [
            "initial state",
            "observable target state",
        ]

        for fixture, expected in (
            (weaker, "forbidden or unknown answer method"),
            (missing_node, "missing mandatory answer path nodes"),
        ):
            with self.subTest(expected=expected), tempfile.TemporaryDirectory() as tmpdir:
                run_dir = Path(tmpdir)
                write_run(run_dir, fixture)

                result = run_script(VALIDATE, str(run_dir))

                self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertIn(expected, result.stdout + result.stderr)

    def test_append_progress_event_appends_jsonl_and_rejects_invalid_basics(self):
        event = {
            "event_type": "step.completed",
            "schema_version": "1.0.0",
            "occurred_at": "2026-06-09T00:02:00Z",
            "work_package_id": "WP5",
            "required_step": "S7",
            "status": "pass",
            "progress_role": "mainline",
            "counts_as_goal_progress": True,
            "evidence": ["new evidence pointer"],
        }
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            write_run(run_dir, {"control_files": load_fixture()["control_files"]})

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
        bypass = load_fixture()
        bypass["final_report"]["verification"] = {
            "verifier_result": "not_run",
            "verifier_permits_goal_achieved": False,
        }

        supporting_only = load_fixture()
        supporting_only["progress_events"] = [
            {
                **copy.deepcopy(event),
                "progress_role": "supporting_only",
                "counts_as_goal_progress": False,
                "evidence": ["supporting-only evidence"],
            }
            for event in supporting_only["progress_events"]
        ]

        not_done = load_fixture()
        not_done["final_report"]["goal_achieved"] = False
        not_done["final_report"]["what_counts_as_done_met"] = False
        not_done["final_report"]["work_coverage"]["status"] = "partial"
        not_done["final_report"]["remaining_gaps"] = ["guard integration still pending"]

        for fixture, expected in (
            (bypass, "verifier does not permit goal_achieved true"),
            (supporting_only, "missing mainline evidence-backed progress for required steps"),
            (not_done, "not-done final report cannot be treated as success"),
        ):
            with self.subTest(expected=expected), tempfile.TemporaryDirectory() as tmpdir:
                run_dir = Path(tmpdir)
                write_run(run_dir, fixture)

                result = run_script(VERIFY, str(run_dir))

                self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertIn(expected, result.stdout + result.stderr)

    def test_verify_runtime_progress_rejects_approved_json_mutation_boundary(self):
        fixture = load_fixture()
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            write_run(run_dir, fixture)
            runtime = fixture["control_files"]["runtime.control.json"]
            hashes = approved_hashes(run_dir, runtime)
            hash_file = run_dir / "approved-hashes.json"
            hash_file.write_text(json.dumps(hashes, indent=2), encoding="utf-8")

            goal = json.loads((run_dir / "goal.control.json").read_text(encoding="utf-8"))
            goal["approved_control"]["objective"] = "mutated during runtime"
            (run_dir / "goal.control.json").write_text(json.dumps(goal, indent=2), encoding="utf-8")

            result = run_script(VERIFY, str(run_dir), "--approved-hashes", str(hash_file))

            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("approved control JSON changed after runtime start", result.stdout + result.stderr)

    def test_verify_runtime_progress_rejects_approved_json_mutation_from_embedded_hashes(self):
        fixture = load_fixture()
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            write_run(run_dir, fixture)

            goal = json.loads((run_dir / "goal.control.json").read_text(encoding="utf-8"))
            goal["approved_control"]["objective"] = "mutated during runtime"
            (run_dir / "goal.control.json").write_text(json.dumps(goal, indent=2), encoding="utf-8")

            result = run_script(VERIFY, str(run_dir))

            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn(
                "runtime.control.json approved_control_hashes mismatch for goal.control.json",
                result.stdout + result.stderr,
            )

    def test_verify_runtime_progress_permits_complete_mainline_verified_report(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            write_run(run_dir, load_fixture())

            result = run_script(VERIFY, str(run_dir))

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            payload = json.loads(result.stdout)
            self.assertTrue(payload["goal_achieved_permitted"])

    def test_build_runtime_prompt_outputs_short_goal_pointer(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            write_run(run_dir, load_fixture())

            result = run_script(BUILD_PROMPT, str(run_dir / "runtime.control.json"))

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("/goal Execute the runtime control JSON at", result.stdout)
            self.assertIn("runtime.control.json", result.stdout)
            self.assertIn("using-control-json", result.stdout)
            self.assertNotIn("required_steps", result.stdout)
            self.assertLess(len(result.stdout.strip().splitlines()), 3)


if __name__ == "__main__":
    unittest.main()
