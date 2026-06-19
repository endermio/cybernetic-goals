import copy
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from tests.skills.test_reviewed_replanning_control import (
    CONTROL_GUARD,
    COMPILER,
    LEGACY_FIXTURE,
    apply_hashes,
    approved_generation_review,
    canonical_json_hash,
    final_report,
    progress_event,
    requirements,
    run_control,
    runtime_control,
    write_strategy_run,
)


ROOT = Path(__file__).resolve().parents[2]
ORCHESTRATION_GUARD = ROOT / ".agents/skills/orchestrating-cybernetic-pregoal/scripts/orchestration_guard.py"
PREDICTOR = ROOT / ".agents/skills/analyzing-cybernetic-requirements/scripts/predict_pregoal_handoff.py"


def run_script(script: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["python3", str(script), *args], text=True, capture_output=True)


class JsonOfficialGuardCompilerPathTest(unittest.TestCase):
    def test_control_chain_guard_accepts_generation_run_directory(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            write_strategy_run(run_dir)

            result = run_script(CONTROL_GUARD, "--run-dir", str(run_dir))

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("PASS", result.stdout)
            self.assertIn("CompileRuntimeGoal", result.stdout)

    def test_official_guard_and_compiler_reject_root_chain_without_run_control(self):
        fixture = json.loads(LEGACY_FIXTURE.read_text(encoding="utf-8"))["valid"]
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            for filename, payload in fixture["control_files"].items():
                (run_dir / filename).write_text(json.dumps(payload, indent=2), encoding="utf-8")

            guard = run_script(CONTROL_GUARD, "--run-dir", str(run_dir))
            compiler = run_script(COMPILER, "--run-dir", str(run_dir))

            for result in (guard, compiler):
                self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertIn("missing run.control.json", result.stdout + result.stderr)

    def test_orchestration_guard_accepts_generation_run_before_runtime_compile(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            write_strategy_run(run_dir)

            result = run_script(
                ORCHESTRATION_GUARD,
                "--state",
                "before-runtime-compile",
                "--run-dir",
                str(run_dir),
                "--json",
            )

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            payload = json.loads(result.stdout)
            self.assertTrue(payload["ok"])
            self.assertEqual(payload["next_allowed_action"], "RunRuntimeCompile")

    def test_orchestration_guard_routes_current_generation_review_needs_revision(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            write_strategy_run(run_dir)
            review_path = run_dir / "gen-000/review.control.json"
            review = json.loads(review_path.read_text(encoding="utf-8"))
            review["status"] = "needs_revision"
            review["review_checks"] = [
                {
                    "check_id": "required-outcome-coverage",
                    "status": "needs_revision",
                    "verdict": "needs_revision",
                    "return_to_stage": "plan",
                    "evidence": ["plan downgraded required implementation to readiness"],
                    "findings": ["plan downgraded required implementation to readiness"],
                    "required_changes": ["regenerate strategy from approved required outcome"],
                    "checked_transformations": ["runtime->plan"],
                }
            ]
            review_path.write_text(json.dumps(review, indent=2), encoding="utf-8")

            result = run_script(
                ORCHESTRATION_GUARD,
                "--state",
                "before-runtime-compile",
                "--run-dir",
                str(run_dir),
                "--json",
            )

            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
            payload = json.loads(result.stdout)
            self.assertFalse(payload["ok"])
            self.assertEqual(payload["next_allowed_action"], "RunExecutionPolicy")
            self.assertIn("plan downgraded required implementation", "\n".join(payload["errors"]))

    def test_orchestration_guard_routes_missing_counterexample_gate_to_review(self):
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

            result = run_script(
                ORCHESTRATION_GUARD,
                "--state",
                "before-runtime-compile",
                "--run-dir",
                str(run_dir),
                "--json",
            )

            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
            payload = json.loads(result.stdout)
            self.assertFalse(payload["ok"])
            self.assertEqual(payload["next_allowed_action"], "RunReview")
            self.assertIn("counterexample-gate", "\n".join(payload["errors"]))

    def test_compile_runtime_goal_creates_current_generation_runtime_and_pointer(self):
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
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            (run_dir / "requirements.control.json").write_text(json.dumps(req, indent=2), encoding="utf-8")
            (run_dir / "run.control.json").write_text(json.dumps(run, indent=2), encoding="utf-8")

            result = run_script(COMPILER, "--run-dir", str(run_dir))

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            runtime_path = run_dir / "gen-000/runtime.control.json"
            self.assertTrue(runtime_path.exists())
            runtime = json.loads(runtime_path.read_text(encoding="utf-8"))
            self.assertEqual(runtime["generation"]["id"], "gen-000")
            self.assertEqual(runtime["strategy_policy"], "frozen_strategy")
            self.assertEqual(runtime["gate_mode"], "none")
            self.assertNotIn("control_mode", runtime)
            self.assertIn("/goal Execute the runtime control JSON at", result.stdout)
            self.assertIn("gen-000/runtime.control.json", result.stdout)
            self.assertNotIn(".goal.md", result.stdout)

    def test_compile_runtime_goal_does_not_write_runtime_when_counterexample_gate_missing(self):
        req = requirements()
        run = run_control(
            generations=[
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
                            "evidence": ["evidence.target-startup"],
                            "satisfies_outcomes": ["O-target-startup"],
                        }
                    ],
                }
            ]
        )
        run["semantic_base_ref"] = copy.deepcopy(req["approved_control"]["semantic_base"])
        review = approved_generation_review()
        review["review_checks"] = [
            check
            for check in review["review_checks"]
            if check["check_id"] != "counterexample-gate"
        ]
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            review_path = run_dir / "gen-000/review.control.json"
            review_path.parent.mkdir(parents=True, exist_ok=True)
            (run_dir / "requirements.control.json").write_text(json.dumps(req, indent=2), encoding="utf-8")
            (run_dir / "run.control.json").write_text(json.dumps(run, indent=2), encoding="utf-8")
            review_path.write_text(json.dumps(review, indent=2), encoding="utf-8")

            result = run_script(COMPILER, "--run-dir", str(run_dir))

            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("counterexample-gate", result.stdout + result.stderr)
            self.assertFalse((run_dir / "gen-000/runtime.control.json").exists())

    def test_json_mode_rejects_markdown_official_inputs_for_guard_and_compiler(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            for filename in ("requirements.md", "design.md", "goal.md", "plan.md", "review.md"):
                (run_dir / filename).write_text("# legacy markdown\n\nStatus: `Approved`\n", encoding="utf-8")

            guard = run_script(CONTROL_GUARD, "--run-dir", str(run_dir))
            compiler = run_script(COMPILER, "--run-dir", str(run_dir))

            self.assertNotEqual(guard.returncode, 0, guard.stdout + guard.stderr)
            self.assertNotEqual(compiler.returncode, 0, compiler.stdout + compiler.stderr)
            self.assertIn("Markdown control artifacts are not official JSON control input", guard.stdout + guard.stderr)
            self.assertIn("Markdown control artifacts are not official JSON control input", compiler.stdout + compiler.stderr)

    def test_generation_guard_rejects_required_outcome_coverage_gap(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            write_strategy_run(run_dir)
            req = json.loads((run_dir / "requirements.control.json").read_text(encoding="utf-8"))
            run = json.loads((run_dir / "run.control.json").read_text(encoding="utf-8"))
            review = json.loads((run_dir / "gen-000/review.control.json").read_text(encoding="utf-8"))
            runtime = json.loads((run_dir / "gen-000/runtime.control.json").read_text(encoding="utf-8"))
            runtime["required_steps"][0]["satisfies_outcomes"] = ["O-other"]
            apply_hashes(req, run, runtime, "gen-000/runtime.control.json", review, "gen-000/review.control.json")
            (run_dir / "gen-000/runtime.control.json").write_text(json.dumps(runtime, indent=2), encoding="utf-8")

            result = run_script(CONTROL_GUARD, "--run-dir", str(run_dir))

            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("required_steps do not satisfy blocking required outcomes", result.stdout + result.stderr)

    def test_generation_guard_rejects_required_evidence_outside_authorized_paths(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            write_strategy_run(run_dir)
            req = json.loads((run_dir / "requirements.control.json").read_text(encoding="utf-8"))
            run = json.loads((run_dir / "run.control.json").read_text(encoding="utf-8"))
            review = json.loads((run_dir / "gen-000/review.control.json").read_text(encoding="utf-8"))
            runtime = json.loads((run_dir / "gen-000/runtime.control.json").read_text(encoding="utf-8"))
            req["approved_control"]["required_outcomes"][0]["required_evidence"][0]["path"] = "evidence/mainline.json"
            approved = copy.deepcopy(req["approved_control"])
            approved.pop("semantic_base", None)
            req["approved_control"]["semantic_base"]["hash"] = canonical_json_hash(approved)
            runtime["runtime"]["writable_evidence_paths"] = ["results/"]
            apply_hashes(req, run, runtime, "gen-000/runtime.control.json", review, "gen-000/review.control.json")
            (run_dir / "requirements.control.json").write_text(json.dumps(req, indent=2), encoding="utf-8")
            (run_dir / "run.control.json").write_text(json.dumps(run, indent=2), encoding="utf-8")
            (run_dir / "gen-000/runtime.control.json").write_text(json.dumps(runtime, indent=2), encoding="utf-8")

            result = run_script(CONTROL_GUARD, "--run-dir", str(run_dir))

            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("required evidence path is not authorized", result.stdout + result.stderr)

    def test_pregoal_predictor_uses_current_generation_runtime(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            write_strategy_run(
                run_dir,
                progress_events=[progress_event("evidence.target-startup")],
                report=final_report("gen-000", "evidence.target-startup"),
            )

            result = run_script(PREDICTOR, "--run-dir", str(run_dir))

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn(str(run_dir / "gen-000/runtime.control.json"), result.stdout)
            self.assertIn("$orchestrating-cybernetic-pregoal 根据 JSON run directory", result.stdout)
            self.assertNotIn(".goal.md", result.stdout)


if __name__ == "__main__":
    unittest.main()
