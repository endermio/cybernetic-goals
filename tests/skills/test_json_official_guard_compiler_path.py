import copy
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from tests.skills.test_control_json_schemas import SCHEMA_FIXTURES, apply_integrity_metadata


ROOT = Path(__file__).resolve().parents[2]
CONTROL_GUARD = ROOT / ".agents/skills/compiling-cybernetic-runtime-goals/scripts/control_chain_guard.py"
COMPILER = ROOT / ".agents/skills/compiling-cybernetic-runtime-goals/scripts/compile_runtime_goal.py"
ORCHESTRATION_GUARD = ROOT / ".agents/skills/orchestrating-cybernetic-pregoal/scripts/orchestration_guard.py"
PREDICTOR = ROOT / ".agents/skills/analyzing-cybernetic-requirements/scripts/predict_pregoal_handoff.py"

CONTROL_FILES = (
    "requirements.control.json",
    "design.control.json",
    "goal.control.json",
    "plan.control.json",
    "review.control.json",
)


def control_run_files() -> dict[str, dict]:
    return {
        "requirements.control.json": SCHEMA_FIXTURES["requirements.control.schema.json"],
        "design.control.json": SCHEMA_FIXTURES["design.control.schema.json"],
        "goal.control.json": SCHEMA_FIXTURES["goal.control.schema.json"],
        "plan.control.json": SCHEMA_FIXTURES["plan.control.schema.json"],
        "review.control.json": SCHEMA_FIXTURES["review.control.schema.json"],
        "runtime.control.json": SCHEMA_FIXTURES["runtime.control.schema.json"],
    }


def outcome_covered_control_run_files() -> dict[str, dict]:
    fixture_by_file = copy.deepcopy(control_run_files())
    outcome_id = "O-required-outcome-coverage"
    fixture_by_file["requirements.control.json"]["approved_control"]["required_outcomes"] = [
        {
            "id": outcome_id,
            "statement": "blocking required outcomes stay covered through runtime verification",
            "blocks_goal_achieved_if_missing": True,
            "required_evidence": [
                {
                    "evidence_id": "evidence.required-outcome-mainline",
                    "kind": "progress_event",
                    "description": "mainline completed progress event",
                }
            ],
            "not_satisfied_by": ["supporting-only progress"],
        },
        {
            "id": "O-nonblocking-support",
            "statement": "supporting work may be present but cannot replace the blocking outcome",
            "blocks_goal_achieved_if_missing": False,
            "required_evidence": [
                {
                    "evidence_id": "evidence.supporting-only",
                    "kind": "progress_event",
                    "description": "supporting evidence",
                }
            ],
            "not_satisfied_by": ["claiming support as the required outcome"],
        }
    ]
    for filename in ("design.control.json", "goal.control.json", "plan.control.json", "runtime.control.json"):
        fixture_by_file[filename]["required_steps"][0]["satisfies_outcomes"] = [outcome_id]
    fixture_by_file["runtime.control.json"]["verifier"]["required_outcomes"] = [outcome_id]
    apply_integrity_metadata(fixture_by_file)
    return fixture_by_file


def evidence_artifact_control_run_files() -> dict[str, dict]:
    fixture_by_file = outcome_covered_control_run_files()
    fixture_by_file["requirements.control.json"]["approved_control"]["required_outcomes"][0]["required_evidence"][0] = {
        "evidence_id": "evidence.required-outcome-mainline",
        "kind": "json_file",
        "description": "mainline evidence artifact",
        "path": "evidence/required-outcome-mainline.json",
    }
    fixture_by_file["plan.control.json"]["runtime"]["writable_evidence_paths"] = ["evidence/"]
    fixture_by_file["runtime.control.json"]["runtime"]["writable_evidence_paths"] = ["evidence/"]
    apply_integrity_metadata(fixture_by_file)
    return fixture_by_file


def candidate_design_plan_control_run_files() -> dict[str, dict]:
    fixture_by_file = copy.deepcopy(control_run_files())
    fixture_by_file["design.control.json"]["status"] = "candidate"
    fixture_by_file["plan.control.json"]["status"] = "candidate"
    apply_integrity_metadata(fixture_by_file)
    return fixture_by_file


def write_control_run(run_dir: Path, include_runtime: bool = True, fixture_by_file: dict[str, dict] | None = None) -> None:
    if fixture_by_file is None:
        fixture_by_file = control_run_files()
    for filename, value in fixture_by_file.items():
        if filename == "runtime.control.json" and not include_runtime:
            continue
        (run_dir / filename).write_text(json.dumps(value, indent=2), encoding="utf-8")


class JsonOfficialGuardCompilerPathTest(unittest.TestCase):
    def test_control_chain_guard_accepts_complete_json_run_directory(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            write_control_run(run_dir)

            result = subprocess.run(
                ["python3", str(CONTROL_GUARD), "--run-dir", str(run_dir)],
                text=True,
                capture_output=True,
            )

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("PASS", result.stdout)
            self.assertIn("CompileRuntimeGoal", result.stdout)

    def test_orchestration_guard_accepts_complete_json_run_directory_before_runtime_compile(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            write_control_run(run_dir)

            result = subprocess.run(
                [
                    "python3",
                    str(ORCHESTRATION_GUARD),
                    "--state",
                    "before-runtime-compile",
                    "--run-dir",
                    str(run_dir),
                    "--json",
                ],
                text=True,
                capture_output=True,
            )

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            payload = json.loads(result.stdout)
            self.assertTrue(payload["ok"])
            self.assertEqual(payload["next_allowed_action"], "RunRuntimeCompile")

    def test_orchestration_guard_routes_needs_revision_to_return_stage(self):
        fixture_by_file = outcome_covered_control_run_files()
        fixture_by_file["review.control.json"]["status"] = "needs_revision"
        fixture_by_file["review.control.json"]["review_checks"][0]["status"] = "needs_revision"
        fixture_by_file["review.control.json"]["review_checks"][0]["verdict"] = "needs_revision"
        fixture_by_file["review.control.json"]["review_checks"][0]["return_to_stage"] = "plan"
        fixture_by_file["review.control.json"]["review_checks"][0]["findings"] = [
            "plan downgraded required implementation to readiness"
        ]
        fixture_by_file["review.control.json"]["review_checks"][0]["required_changes"] = [
            "regenerate plan.control.json from approved required outcome"
        ]
        apply_integrity_metadata(fixture_by_file)
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            write_control_run(run_dir, fixture_by_file=fixture_by_file)

            result = subprocess.run(
                [
                    "python3",
                    str(ORCHESTRATION_GUARD),
                    "--state",
                    "before-runtime-compile",
                    "--run-dir",
                    str(run_dir),
                    "--json",
                ],
                text=True,
                capture_output=True,
            )

            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
            payload = json.loads(result.stdout)
            self.assertFalse(payload["ok"])
            self.assertEqual(payload["next_allowed_action"], "RunExecutionPolicy")
            self.assertIn("plan downgraded required implementation", "\n".join(payload["errors"]))

    def test_control_chain_guard_rejects_candidate_design_or_plan_before_runtime_compile(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            write_control_run(run_dir, fixture_by_file=candidate_design_plan_control_run_files())

            result = subprocess.run(
                ["python3", str(CONTROL_GUARD), "--run-dir", str(run_dir)],
                text=True,
                capture_output=True,
            )

            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("design.control.json status must be approved", result.stdout + result.stderr)
            self.assertIn("plan.control.json status must be approved", result.stdout + result.stderr)

    def test_compile_runtime_goal_rejects_candidate_design_or_plan_without_writing_runtime(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            write_control_run(
                run_dir,
                include_runtime=False,
                fixture_by_file=candidate_design_plan_control_run_files(),
            )

            result = subprocess.run(
                ["python3", str(COMPILER), "--run-dir", str(run_dir)],
                text=True,
                capture_output=True,
            )

            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("design.control.json status must be approved", result.stdout + result.stderr)
            self.assertIn("plan.control.json status must be approved", result.stdout + result.stderr)
            self.assertFalse((run_dir / "runtime.control.json").exists())

    def test_compile_runtime_goal_reads_json_run_dir_writes_runtime_control_and_prints_short_goal_pointer(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            write_control_run(run_dir, include_runtime=False)

            result = subprocess.run(
                ["python3", str(COMPILER), "--run-dir", str(run_dir)],
                text=True,
                capture_output=True,
            )

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            runtime_path = run_dir / "runtime.control.json"
            self.assertTrue(runtime_path.exists())
            runtime = json.loads(runtime_path.read_text(encoding="utf-8"))
            self.assertEqual(runtime["artifact_type"], "runtime.control")
            self.assertIn("/goal Execute the runtime control JSON at", result.stdout)
            self.assertIn("runtime.control.json", result.stdout)
            self.assertIn(".agents/skills/using-control-json", result.stdout)
            self.assertNotIn(".goal.md", result.stdout)
            self.assertFalse(any(path.name.endswith(".goal.md") for path in run_dir.iterdir()))

    def test_json_mode_rejects_markdown_official_inputs_for_guard_and_compiler(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            for filename in ("requirements.md", "design.md", "goal.md", "plan.md", "review.md"):
                (run_dir / filename).write_text("# legacy markdown\n\nStatus: `Approved`\n", encoding="utf-8")

            guard = subprocess.run(
                ["python3", str(CONTROL_GUARD), "--run-dir", str(run_dir)],
                text=True,
                capture_output=True,
            )
            compiler = subprocess.run(
                ["python3", str(COMPILER), "--run-dir", str(run_dir)],
                text=True,
                capture_output=True,
            )

            self.assertNotEqual(guard.returncode, 0, guard.stdout + guard.stderr)
            self.assertNotEqual(compiler.returncode, 0, compiler.stdout + compiler.stderr)
            self.assertIn("Markdown control artifacts are not official JSON control input", guard.stdout + guard.stderr)
            self.assertIn("Markdown control artifacts are not official JSON control input", compiler.stdout + compiler.stderr)

    def test_control_chain_guard_rejects_semantic_base_mismatch(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            write_control_run(run_dir)
            design_path = run_dir / "design.control.json"
            design = json.loads(design_path.read_text(encoding="utf-8"))
            design["semantic_base_ref"]["hash"] = "sha256:mismatched"
            design_path.write_text(json.dumps(design, indent=2), encoding="utf-8")

            result = subprocess.run(
                ["python3", str(CONTROL_GUARD), "--run-dir", str(run_dir)],
                text=True,
                capture_output=True,
            )

            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("semantic_base_ref must match requirements approved semantic_base", result.stdout + result.stderr)

    def test_control_chain_guard_rejects_approved_control_hash_mismatch(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            write_control_run(run_dir)
            runtime_path = run_dir / "runtime.control.json"
            runtime = json.loads(runtime_path.read_text(encoding="utf-8"))
            runtime["approved_control_hashes"]["goal.control.json"] = "sha256:mismatched"
            runtime_path.write_text(json.dumps(runtime, indent=2), encoding="utf-8")

            result = subprocess.run(
                ["python3", str(CONTROL_GUARD), "--run-dir", str(run_dir)],
                text=True,
                capture_output=True,
            )

            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("approved_control_hashes mismatch for goal.control.json", result.stdout + result.stderr)

    def test_control_chain_guard_accepts_required_outcome_covered_chain(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            write_control_run(run_dir, fixture_by_file=outcome_covered_control_run_files())

            result = subprocess.run(
                ["python3", str(CONTROL_GUARD), "--run-dir", str(run_dir)],
                text=True,
                capture_output=True,
            )

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("PASS", result.stdout)

    def test_control_chain_guard_accepts_required_evidence_artifact_when_authorized(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            write_control_run(run_dir, fixture_by_file=evidence_artifact_control_run_files())

            result = subprocess.run(
                ["python3", str(CONTROL_GUARD), "--run-dir", str(run_dir)],
                text=True,
                capture_output=True,
            )

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_control_chain_guard_rejects_required_evidence_artifact_outside_authorized_paths(self):
        fixture_by_file = evidence_artifact_control_run_files()
        fixture_by_file["plan.control.json"]["runtime"]["writable_evidence_paths"] = ["results/"]
        fixture_by_file["runtime.control.json"]["runtime"]["writable_evidence_paths"] = ["results/"]
        apply_integrity_metadata(fixture_by_file)
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            write_control_run(run_dir, fixture_by_file=fixture_by_file)

            result = subprocess.run(
                ["python3", str(CONTROL_GUARD), "--run-dir", str(run_dir)],
                text=True,
                capture_output=True,
            )

            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn(
                "requirements.control.json required evidence path is not authorized by runtime writable_evidence_paths: evidence/required-outcome-mainline.json",
                result.stdout + result.stderr,
            )

    def test_control_chain_guard_rejects_blocking_required_outcome_without_required_step_coverage(self):
        fixture_by_file = outcome_covered_control_run_files()
        fixture_by_file["runtime.control.json"]["required_steps"][0]["satisfies_outcomes"] = ["O-nonblocking-support"]
        apply_integrity_metadata(fixture_by_file)
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            write_control_run(run_dir, fixture_by_file=fixture_by_file)

            result = subprocess.run(
                ["python3", str(CONTROL_GUARD), "--run-dir", str(run_dir)],
                text=True,
                capture_output=True,
            )

            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn(
                "runtime.control.json required_steps do not satisfy blocking required outcomes: O-required-outcome-coverage",
                result.stdout + result.stderr,
            )

    def test_control_chain_guard_rejects_missing_runtime_verifier_required_outcome(self):
        fixture_by_file = outcome_covered_control_run_files()
        fixture_by_file["runtime.control.json"]["verifier"]["required_outcomes"] = ["O-nonblocking-support"]
        apply_integrity_metadata(fixture_by_file)
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            write_control_run(run_dir, fixture_by_file=fixture_by_file)

            result = subprocess.run(
                ["python3", str(CONTROL_GUARD), "--run-dir", str(run_dir)],
                text=True,
                capture_output=True,
            )

            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn(
                "runtime.control.json verifier.required_outcomes missing blocking required outcomes: O-required-outcome-coverage",
                result.stdout + result.stderr,
            )

    def test_control_chain_guard_rejects_work_packages_that_do_not_cover_blocking_outcomes(self):
        fixture_by_file = outcome_covered_control_run_files()
        fixture_by_file["plan.control.json"]["required_steps"][0]["satisfies_outcomes"] = ["O-nonblocking-support"]
        fixture_by_file["plan.control.json"]["required_steps"].append(
            {
                "step_id": "S2",
                "transition": "blocking outcome is documented but not assigned to a work package",
                "evidence": ["unassigned evidence"],
                "satisfies_outcomes": ["O-required-outcome-coverage"],
            }
        )
        fixture_by_file["plan.control.json"]["work_packages"][0]["required_steps"] = ["S1"]
        apply_integrity_metadata(fixture_by_file)
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            write_control_run(run_dir, fixture_by_file=fixture_by_file)

            result = subprocess.run(
                ["python3", str(CONTROL_GUARD), "--run-dir", str(run_dir)],
                text=True,
                capture_output=True,
            )

            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn(
                "plan.control.json work_packages do not cover blocking required outcomes: O-required-outcome-coverage",
                result.stdout + result.stderr,
            )

    def test_control_chain_guard_requires_intent_obligation_and_outcome_review_checks(self):
        fixture_by_file = outcome_covered_control_run_files()
        fixture_by_file["review.control.json"]["review_checks"] = [
            check
            for check in fixture_by_file["review.control.json"]["review_checks"]
            if check["check_id"]
            not in {
                "intent-preservation",
                "obligation-preservation",
                "required-outcome-coverage",
            }
        ]
        apply_integrity_metadata(fixture_by_file)
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            write_control_run(run_dir, fixture_by_file=fixture_by_file)

            result = subprocess.run(
                ["python3", str(CONTROL_GUARD), "--run-dir", str(run_dir)],
                text=True,
                capture_output=True,
            )

            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("intent-preservation", result.stdout + result.stderr)
            self.assertIn("obligation-preservation", result.stdout + result.stderr)
            self.assertIn("required-outcome-coverage", result.stdout + result.stderr)

    def test_control_chain_guard_rejects_review_check_with_non_approved_verdict(self):
        fixture_by_file = outcome_covered_control_run_files()
        fixture_by_file["review.control.json"]["review_checks"][0]["verdict"] = "needs_revision"
        fixture_by_file["review.control.json"]["review_checks"][0]["return_to_stage"] = "design"
        fixture_by_file["review.control.json"]["review_checks"][0]["required_changes"] = [
            "repair answer method drift"
        ]
        apply_integrity_metadata(fixture_by_file)
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            write_control_run(run_dir, fixture_by_file=fixture_by_file)

            result = subprocess.run(
                ["python3", str(CONTROL_GUARD), "--run-dir", str(run_dir)],
                text=True,
                capture_output=True,
            )

            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("required review checks did not pass", result.stdout + result.stderr)
            self.assertIn("design-answer-method", result.stdout + result.stderr)

    def test_legacy_markdown_cli_arguments_are_rejected_as_official_inputs(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            requirements = run_dir / "requirements.md"
            goal = run_dir / "goal.md"
            plan = run_dir / "plan.md"
            review = run_dir / "review.md"
            for path in (requirements, goal, plan, review):
                path.write_text("# legacy markdown\n\nStatus: `Approved`\n", encoding="utf-8")

            guard = subprocess.run(
                [
                    "python3",
                    str(CONTROL_GUARD),
                    "--requirements",
                    str(requirements),
                    "--goal",
                    str(goal),
                    "--plan",
                    str(plan),
                    "--review",
                    str(review),
                ],
                text=True,
                capture_output=True,
            )
            compiler = subprocess.run(
                [
                    "python3",
                    str(COMPILER),
                    "--requirements",
                    str(requirements),
                    "--goal",
                    str(goal),
                    "--plan",
                    str(plan),
                    "--review",
                    str(review),
                ],
                text=True,
                capture_output=True,
            )

            self.assertNotEqual(guard.returncode, 0, guard.stdout + guard.stderr)
            self.assertNotEqual(compiler.returncode, 0, compiler.stdout + compiler.stderr)
            self.assertIn("official control input is JSON-only", guard.stdout + guard.stderr)
            self.assertIn("official control input is JSON-only", compiler.stdout + compiler.stderr)

    def test_pregoal_predictor_points_json_requirements_to_runtime_control_json(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            write_control_run(run_dir)

            result = subprocess.run(
                ["python3", str(PREDICTOR), "--requirements", str(run_dir / "requirements.control.json")],
                text=True,
                capture_output=True,
            )

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn(str(run_dir / "runtime.control.json"), result.stdout)
            self.assertIn(".agents/skills/using-control-json", result.stdout)
            self.assertNotIn(".goal.md", result.stdout)

    def test_pregoal_predictor_accepts_json_run_directory(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            write_control_run(run_dir)

            result = subprocess.run(
                ["python3", str(PREDICTOR), "--run-dir", str(run_dir)],
                text=True,
                capture_output=True,
            )

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn(str(run_dir / "runtime.control.json"), result.stdout)
            self.assertIn("$orchestrating-cybernetic-pregoal 根据 JSON run directory", result.stdout)
            self.assertNotIn(".goal.md", result.stdout)


if __name__ == "__main__":
    unittest.main()
