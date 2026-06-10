import copy
import hashlib
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from tests.skills.test_control_json_schemas import apply_integrity_metadata, validate


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


def outcome_covered_fixture() -> dict:
    fixture = load_fixture()
    control_files = fixture["control_files"]
    outcomes = [
        {
            "id": "O-runtime-progress",
            "statement": "runtime writes evidence-backed progress events",
            "blocks_goal_achieved_if_missing": True,
            "required_evidence": [
                {
                    "evidence_id": "evidence.runtime-progress",
                    "kind": "progress_event",
                    "description": "mainline progress event for S7",
                }
            ],
            "not_satisfied_by": ["supporting-only progress"],
        },
        {
            "id": "O-json-regressions",
            "statement": "old accident regressions are covered by JSON runtime verification",
            "blocks_goal_achieved_if_missing": True,
            "required_evidence": [
                {
                    "evidence_id": "evidence.json-regressions",
                    "kind": "progress_event",
                    "description": "mainline progress event for S9",
                }
            ],
            "not_satisfied_by": ["supporting-only progress"],
        },
    ]
    control_files["requirements.control.json"]["approved_control"]["required_outcomes"] = outcomes
    step_outcomes = {"S7": ["O-runtime-progress"], "S9": ["O-json-regressions"]}
    for filename in ("design.control.json", "goal.control.json", "plan.control.json", "runtime.control.json"):
        for step in control_files[filename]["required_steps"]:
            step["satisfies_outcomes"] = step_outcomes[step["step_id"]]
    control_files["runtime.control.json"]["verifier"]["required_outcomes"] = [
        "O-runtime-progress",
        "O-json-regressions",
    ]
    step_evidence = {
        "S7": ["evidence.runtime-progress"],
        "S9": ["evidence.json-regressions"],
    }
    for event in fixture.get("progress_events", []):
        if event.get("required_step") in step_evidence:
            event["evidence"] = step_evidence[event["required_step"]]
    apply_integrity_metadata(control_files)
    return fixture


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

    def test_validate_control_chain_rejects_required_outcome_coverage_gaps(self):
        missing_outcome_id = outcome_covered_fixture()
        del missing_outcome_id["control_files"]["requirements.control.json"]["approved_control"]["required_outcomes"][1]["id"]
        apply_integrity_metadata(missing_outcome_id["control_files"])

        missing_step_coverage = outcome_covered_fixture()
        missing_step_coverage["control_files"]["goal.control.json"]["required_steps"][1]["satisfies_outcomes"] = []
        apply_integrity_metadata(missing_step_coverage["control_files"])

        missing_verifier_outcome = outcome_covered_fixture()
        missing_verifier_outcome["control_files"]["runtime.control.json"]["verifier"]["required_outcomes"] = [
            "O-runtime-progress"
        ]
        apply_integrity_metadata(missing_verifier_outcome["control_files"])

        missing_work_package_coverage = outcome_covered_fixture()
        missing_work_package_coverage["control_files"]["plan.control.json"]["work_packages"][0]["required_steps"] = [
            "S7"
        ]
        apply_integrity_metadata(missing_work_package_coverage["control_files"])

        for fixture, expected in (
            (
                missing_outcome_id,
                "requirements.control.json required_outcomes[1].id must be a non-empty string",
            ),
            (
                missing_step_coverage,
                "goal.control.json required_steps do not satisfy blocking required outcomes: O-json-regressions",
            ),
            (
                missing_verifier_outcome,
                "runtime.control.json verifier.required_outcomes missing blocking required outcomes: O-json-regressions",
            ),
            (
                missing_work_package_coverage,
                "plan.control.json work_packages do not cover blocking required outcomes: O-json-regressions",
            ),
        ):
            with self.subTest(expected=expected), tempfile.TemporaryDirectory() as tmpdir:
                run_dir = Path(tmpdir)
                write_run(run_dir, fixture)

                result = run_script(VALIDATE, str(run_dir))

                self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertIn(expected, result.stdout + result.stderr)

    def test_validate_control_chain_rejects_plan_without_producing_action_alignment(self):
        supporting_package = outcome_covered_fixture()
        package = supporting_package["control_files"]["plan.control.json"]["work_packages"][0]
        package["role"] = "supporting-only"
        package["not_merely_verification"] = False
        package["counts_as_goal_progress"] = False
        apply_integrity_metadata(supporting_package["control_files"])

        missing_authority = outcome_covered_fixture()
        missing_authority["control_files"]["plan.control.json"]["step_action_alignment"][0]["allowed_authority_needed"]["write_paths"] = [
            "scripts/new-runner-mode.py"
        ]
        missing_authority["control_files"]["plan.control.json"]["work_packages"][0]["allowed_write_paths"] = [
            "evidence/"
        ]
        apply_integrity_metadata(missing_authority["control_files"])

        for fixture, expected in (
            (
                supporting_package,
                "plan.control.json mainline work package required for blocking outcomes must use a producing action",
            ),
            (
                missing_authority,
                "plan.control.json producing action write authority is not covered by work package allowed_write_paths",
            ),
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
            "runtime_generation": "legacy-full",
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

    def test_verify_runtime_progress_rejects_blocking_outcome_without_mainline_evidence(self):
        fixture = outcome_covered_fixture()
        fixture["progress_events"][1]["progress_role"] = "supporting_only"
        fixture["progress_events"][1]["counts_as_goal_progress"] = False
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            write_run(run_dir, fixture)

            result = run_script(VERIFY, str(run_dir))

            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn(
                "missing mainline evidence-backed progress for blocking required outcomes: O-json-regressions",
                result.stdout + result.stderr,
            )

    def test_verify_runtime_progress_rejects_missing_required_evidence_id(self):
        fixture = outcome_covered_fixture()
        fixture["progress_events"][1]["evidence"] = ["some-other-evidence"]
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            write_run(run_dir, fixture)

            result = run_script(VERIFY, str(run_dir))

            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn(
                "missing required evidence for blocking required outcomes: O-json-regressions: evidence.json-regressions",
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

    def test_verify_runtime_progress_permits_required_outcome_covered_progress(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            write_run(run_dir, outcome_covered_fixture())

            result = run_script(VERIFY, str(run_dir))

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual(["O-json-regressions", "O-runtime-progress"], payload["required_outcomes"])
            self.assertEqual(["O-json-regressions", "O-runtime-progress"], payload["completed_required_outcomes"])

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
