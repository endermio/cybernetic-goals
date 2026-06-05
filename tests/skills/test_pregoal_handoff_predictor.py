import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = (
    ROOT
    / ".agents/skills/analyzing-cybernetic-requirements/scripts/predict_pregoal_handoff.py"
)


HSA_APPROVED = """## Human Setpoint Approval

Status: `Approved`

| Element | Commitment |
|---|---|
| Human purpose | compile a queue-friendly pre-goal handoff |
| Input role binding | requirements fixture is approved source material |
| Primary object | pre-goal handoff predictor |
| Requested transformation | requirements path to handoff commands |
| Non-goals | do not compile final runtime goal |
| Purpose Feedback Boundary | final approval remains downstream |
| Realization Surface Closure | not applicable to predictor fixture |
| Output Contract | response-only handoff text |
| Workflow fit | full pre-goal orchestration |
| Known assumptions | fixture-only |
"""


class PregoalHandoffPredictorTest(unittest.TestCase):
    def write_requirements(
        self,
        tmp: Path,
        *,
        status: str = "Complete",
        hsa: str = HSA_APPROVED,
        design_gate: str = "required",
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
                    "## Required Gates",
                    "",
                    "| Gate | Status | Reason |",
                    "|---|---|---|",
                    f"| Design Gate | `{design_gate}` | fixture |",
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

    def test_generates_queue_friendly_handoff_for_approved_setpoint(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            requirements = self.write_requirements(Path(tmpdir))
            result = self.run_script(requirements)

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("$orchestrating-cybernetic-pregoal", result.stdout)
        self.assertIn(str(requirements), result.stdout)
        self.assertIn("/goal Execute the approved execution policy", result.stdout)
        self.assertIn("docs/cybernetics/goals/2026-06-06-predictor.md", result.stdout)
        self.assertIn("docs/cybernetics/plans/2026-06-06-predictor.md", result.stdout)
        self.assertIn("docs/cybernetics/control-reviews/2026-06-06-predictor.md", result.stdout)
        self.assertIn("docs/cybernetics/designs/2026-06-06-predictor.md", result.stdout)
        self.assertIn("If any referenced artifact is missing, not approved, or internally inconsistent", result.stdout)
        self.assertIn("Predicted", result.stdout)

    def test_blocks_when_human_setpoint_is_not_approved(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            requirements = self.write_requirements(
                Path(tmpdir),
                hsa="## Human Setpoint Approval\n\nStatus: `Pending`\n",
            )
            result = self.run_script(requirements)

        output = result.stdout + result.stderr
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Human Setpoint Approval is not Approved", output)
        self.assertIn("approve or revise the compact control commitment", output)
        self.assertNotIn("$orchestrating-cybernetic-pregoal", output)
        self.assertNotIn("/goal Execute", output)

    def test_blocks_when_requirements_path_cannot_define_slug(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            requirements = Path(tmpdir) / "requirements.md"
            requirements.write_text(
                "# Requirements\n\n## Requirements Analysis Status\n\nStatus: `Complete`\n\n"
                + HSA_APPROVED,
                encoding="utf-8",
            )
            result = self.run_script(requirements)

        output = result.stdout + result.stderr
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("requirements path must look like", output)
        self.assertNotIn("/goal Execute", output)

    def test_skill_and_manifest_reference_predictor(self):
        skill = (ROOT / ".agents/skills/analyzing-cybernetic-requirements/SKILL.md").read_text(
            encoding="utf-8"
        )
        manifest = (ROOT / "MANIFEST.txt").read_text(encoding="utf-8")

        script_path = ".agents/skills/analyzing-cybernetic-requirements/scripts/predict_pregoal_handoff.py"
        test_path = "tests/skills/test_pregoal_handoff_predictor.py"

        self.assertIn(script_path, skill)
        self.assertIn("Use the script output instead of hand-writing the predicted `/goal`", skill)
        self.assertIn(script_path, manifest)
        self.assertIn(test_path, manifest)


if __name__ == "__main__":
    unittest.main()
