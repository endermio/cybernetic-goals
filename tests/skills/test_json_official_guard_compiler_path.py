import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from tests.skills.test_control_json_schemas import SCHEMA_FIXTURES


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


def write_control_run(run_dir: Path, include_runtime: bool = True) -> None:
    fixture_by_file = {
        "requirements.control.json": SCHEMA_FIXTURES["requirements.control.schema.json"],
        "design.control.json": SCHEMA_FIXTURES["design.control.schema.json"],
        "goal.control.json": SCHEMA_FIXTURES["goal.control.schema.json"],
        "plan.control.json": SCHEMA_FIXTURES["plan.control.schema.json"],
        "review.control.json": SCHEMA_FIXTURES["review.control.schema.json"],
        "runtime.control.json": SCHEMA_FIXTURES["runtime.control.schema.json"],
    }
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
