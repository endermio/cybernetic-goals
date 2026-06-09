import subprocess
import sys
import tempfile
import unittest
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = (
    ROOT
    / ".agents/skills/analyzing-cybernetic-requirements/scripts/predict_pregoal_handoff.py"
)


USER_APPROVAL_APPROVED = """## What the User Approved

Status: `Approved`

| Element | Commitment |
|---|---|
| Human purpose | compile a queue-friendly pre-goal handoff |
| Input role binding | requirements fixture is approved source material |
| Primary object | pre-goal handoff predictor |
| Requested transformation | requirements path to handoff commands |
| Non-goals | do not compile final runtime goal |
| How We Know The User Purpose Was Met | final approval remains downstream |
| Where The Result Must Show Up | not applicable to predictor fixture |
| Final Answer Format | response-only handoff text |
| Why this process is needed | full pre-goal orchestration |
| Known assumptions | fixture-only |
"""


USER_APPROVAL_WITH_ANSWER_METHOD = """## What the User Approved

Status: `Approved`

| Element | Commitment |
|---|---|
| Human purpose | measure the complete workflow ceiling |
| Input role binding | prior partial results are source material |
| Primary object | complete workflow ceiling answer |
| Requested transformation | workflow evidence into a ceiling answer |
| Non-goals | do not validate only one candidate run |
| How We Know The User Purpose Was Met | the full workflow ceiling question is answered |
| Where The Result Must Show Up | final evidence bundle |
| Required answer path | scope inventory -> source inventory -> coverage criterion -> matrix -> run -> interpretation |
| How this should be answered | list full workflow scope, identify major removable sources, define coverage, prove candidate coverage, run full workflow, and interpret against coverage |
| What is not enough | only running one full-workflow candidate |
| Final Answer Format | response-only handoff text |
| Why this process is needed | full pre-goal orchestration |
| Known assumptions | fixture-only |
"""


class PregoalHandoffPredictorTest(unittest.TestCase):
    def write_requirements(
        self,
        tmp: Path,
        *,
        status: str = "Complete",
        hsa: str = USER_APPROVAL_APPROVED,
        design_check: str = "required",
        name: str = "2026-06-06-predictor.md",
    ) -> Path:
        req_dir = tmp / "docs/cybernetics/requirements"
        req_dir.mkdir(parents=True)
        path = req_dir / name
        path.write_text(
            "\n".join(
                [
                    "# Requirements",
                    "",
                    "## Requirements Analysis Status",
                    "",
                    f"Status: `{status}`",
                    "",
                    hsa,
                    "",
                    "## Required Checks Before Moving On",
                    "",
                    "| Check | Status | Reason |",
                    "|---|---|---|",
                    f"| design check | `{design_check}` | fixture |",
                    "",
                ]
            ),
            encoding="utf-8",
        )
        return path

    def run_script(self, requirements: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), "--requirements", str(requirements)],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )

    def test_generates_queue_friendly_handoff_for_approved_target(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            requirements = self.write_requirements(Path(tmpdir))
            result = self.run_script(requirements)

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("$orchestrating-cybernetic-pregoal", result.stdout)
        self.assertIn(str(requirements), result.stdout)
        self.assertIn("Predicted runtime contract path:", result.stdout)
        self.assertIn("/goal Execute the runtime goal file at", result.stdout)
        self.assertNotIn("/goal Execute the approved execution policy", result.stdout)
        self.assertIn("docs/cybernetics/runtime-goals/2026-06-06-predictor.goal.md", result.stdout)
        self.assertIn("docs/cybernetics/goals/2026-06-06-predictor.md", result.stdout)
        self.assertIn("docs/cybernetics/plans/2026-06-06-predictor.md", result.stdout)
        self.assertIn("docs/cybernetics/control-reviews/2026-06-06-predictor.md", result.stdout)
        self.assertIn("docs/cybernetics/designs/2026-06-06-predictor.md", result.stdout)
        self.assertIn("If any referenced artifact is missing, not approved, or inconsistent", result.stdout)
        self.assertIn("compile_runtime_goal.py", result.stdout)
        self.assertIn("Predicted", result.stdout)

    def test_blocks_when_user_approval_is_not_approved(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            requirements = self.write_requirements(
                Path(tmpdir),
                hsa="## What the User Approved\n\nStatus: `Pending`\n",
            )
            result = self.run_script(requirements)

        output = result.stdout + result.stderr
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("What the User Approved is not Approved", output)
        self.assertIn("approve or revise the compact control commitment", output)
        self.assertNotIn("$orchestrating-cybernetic-pregoal", output)
        self.assertNotIn("/goal Execute", output)

    def test_blocks_when_requirements_path_cannot_define_slug(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            requirements = Path(tmpdir) / "requirements.md"
            requirements.write_text(
                "# Requirements\n\n## Requirements Analysis Status\n\nStatus: `Complete`\n\n"
                + USER_APPROVAL_APPROVED,
                encoding="utf-8",
            )
            result = self.run_script(requirements)

        output = result.stdout + result.stderr
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("requirements path must look like", output)
        self.assertNotIn("/goal Execute", output)

    def test_blocks_when_answer_method_sidecar_is_missing(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            requirements = self.write_requirements(
                Path(tmpdir),
                hsa=USER_APPROVAL_WITH_ANSWER_METHOD,
            )
            result = self.run_script(requirements)

        output = result.stdout + result.stderr
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("requirements control sidecar missing", output)
        self.assertNotIn("$orchestrating-cybernetic-pregoal", output)
        self.assertNotIn("/goal Execute", output)

    def test_skill_and_manifest_reference_predictor(self):
        skill = (ROOT / ".agents/skills/analyzing-cybernetic-requirements/SKILL.md").read_text(
            encoding="utf-8"
        )
        manifest = (ROOT / "MANIFEST.txt").read_text(encoding="utf-8")

        script_path = ".agents/skills/analyzing-cybernetic-requirements/scripts/predict_pregoal_handoff.py"
        test_path = "tests/skills/test_pregoal_handoff_predictor.py"

        self.assertIn(script_path, skill)
        self.assertIn("Use the script output instead of hand-writing predicted runtime commands", skill)
        self.assertIn(script_path, manifest)
        self.assertIn(test_path, manifest)

    def test_design_check_dispatch_note_does_not_replace_predicted_goal(self):
        skill = (ROOT / ".agents/skills/analyzing-cybernetic-requirements/SKILL.md").read_text(
            encoding="utf-8"
        )
        evals = json.loads(
            (ROOT / ".agents/skills/analyzing-cybernetic-requirements/evals/evals.json").read_text(
                encoding="utf-8"
            )
        )["evals"]
        complete_level_3 = {
            entry["id"]: entry for entry in evals
        }["complete-level-3-analysis-routes-to-orchestrator-not-manual-design"]

        self.assertIn(
            "design check dispatch note must not replace the predicted pointer-only `/goal`",
            skill,
        )
        self.assertIn("predicted runtime contract path", complete_level_3["expected_output"])
        self.assertTrue(
            any("pointer-only /goal" in assertion for assertion in complete_level_3["assertions"])
        )


if __name__ == "__main__":
    unittest.main()
