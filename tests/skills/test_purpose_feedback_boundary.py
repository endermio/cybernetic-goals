import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


class PurposeFeedbackBoundaryTest(unittest.TestCase):
    def read(self, path: str) -> str:
        return (ROOT / path).read_text(encoding="utf-8")

    def test_requirements_define_purpose_feedback_boundary(self):
        skill = self.read(".agents/skills/analyzing-cybernetic-requirements/SKILL.md")
        template = self.read(
            ".agents/skills/analyzing-cybernetic-requirements/assets/requirements-analysis-template.md"
        )

        for text in (skill, template):
            self.assertIn("Purpose Feedback Boundary", text)
            self.assertIn("Human purpose", text)
            self.assertIn("Beneficiary / observer", text)
            self.assertIn("Purpose-realizing outcome", text)
            self.assertIn("Feedback needed", text)
            self.assertIn("Internal sensors role", text)
            self.assertIn("Sufficient evidence level", text)
            self.assertIn("If feedback unavailable", text)

    def test_goal_separates_purpose_achievement_from_supporting_sensors(self):
        skill = self.read(".agents/skills/writing-cybernetic-goals/SKILL.md")
        template = self.read(".agents/skills/writing-cybernetic-goals/assets/goal-contract-template.md")

        for text in (skill, template):
            self.assertIn("Purpose Feedback Contract", text)
            self.assertIn("Purpose-realizing outcome observed", text)
            self.assertIn("Supporting Evidence", text)
            self.assertIn(
                "Do not define success as internal sensor success unless the human purpose is internal-state correctness.",
                text,
            )

    def test_execution_policy_defines_purpose_feedback_strategy(self):
        skill = self.read(".agents/skills/writing-cybernetic-execution-policies/SKILL.md")
        template = self.read(
            ".agents/skills/writing-cybernetic-execution-policies/assets/execution-policy-template.md"
        )

        for text in (skill, template):
            self.assertIn("Purpose Feedback Strategy", text)
            self.assertIn("Internal feedback", text)
            self.assertIn("Integration feedback", text)
            self.assertIn("Purpose-boundary feedback", text)
            self.assertIn("Operational feedback", text)
            self.assertIn("Feedback cadence", text)
            self.assertIn("Evidence unavailable handling", text)
            self.assertIn("Allowed completion wording", text)

    def test_review_classifies_purpose_feedback_adequacy(self):
        skill = self.read(".agents/skills/reviewing-cybernetic-control-structures/SKILL.md")
        template = self.read(
            ".agents/skills/reviewing-cybernetic-control-structures/assets/control-review-template.md"
        )

        for text in (skill, template):
            self.assertIn("Purpose Feedback Adequacy", text)
            self.assertIn("Purpose feedback adequate", text)
            self.assertIn("Internally verified, purpose feedback pending", text)
            self.assertIn("Purpose partially observed", text)
            self.assertIn("Purpose feedback unavailable, honest handoff required", text)
            self.assertIn("Purpose-boundary evidence not required, justified", text)
            self.assertIn("Block false completion claims, not necessarily continued execution.", text)

    def test_runtime_compiler_calibrates_completion_claims_to_purpose_feedback(self):
        skill = self.read(".agents/skills/compiling-cybernetic-runtime-goals/SKILL.md")
        template = self.read(
            ".agents/skills/compiling-cybernetic-runtime-goals/assets/runtime-goal-template.txt"
        )
        compiler = self.read(
            ".agents/skills/compiling-cybernetic-runtime-goals/scripts/compile_runtime_goal.py"
        )

        for text in (skill, template, compiler):
            self.assertIn(
                "Report completion status according to the highest purpose-relevant evidence actually observed.",
                text,
            )
            self.assertIn(
                "Do not claim the human purpose is achieved from internal sensors alone",
                text,
            )
            self.assertIn("smallest next observation needed", text)

        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            requirements = tmp / "requirements.md"
            goal = tmp / "goal.md"
            plan = tmp / "plan.md"
            review = tmp / "review.md"
            requirements.write_text("## Requirements Analysis Status\n\nStatus: `Complete`\n", encoding="utf-8")
            goal.write_text("## Source Contracts\n\n- Requirements analysis: `requirements.md`\n", encoding="utf-8")
            plan.write_text("## Context Management / Execution Topology\n\nSelected topology: `Main-only`\n", encoding="utf-8")
            review.write_text("## Review Status\n\nStatus: `Approved`\n", encoding="utf-8")

            result = subprocess.run(
                [
                    sys.executable,
                    str(
                        ROOT
                        / ".agents/skills/compiling-cybernetic-runtime-goals/scripts/compile_runtime_goal.py"
                    ),
                    "--requirements",
                    str(requirements),
                    "--goal",
                    str(goal),
                    "--plan",
                    str(plan),
                    "--review",
                    str(review),
                    "--skip-guard",
                    "--i-understand-this-bypasses-phase-gates",
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
            )

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("highest purpose-relevant evidence actually observed", result.stdout)
        self.assertIn("smallest next observation needed", result.stdout)

    def test_purpose_feedback_evals_cover_false_completion_and_overcontrol(self):
        review_evals = json.loads(
            self.read(".agents/skills/reviewing-cybernetic-control-structures/evals/evals.json")
        )
        compiler_evals = json.loads(
            self.read(".agents/skills/compiling-cybernetic-runtime-goals/evals/evals.json")
        )

        review_ids = {item["id"] for item in review_evals["evals"]}
        compiler_ids = {item["id"] for item in compiler_evals["evals"]}

        self.assertIn("purpose-visible-outcome-cannot-be-claimed-from-internal-sensors-only", review_ids)
        self.assertIn("internal-purpose-can-use-internal-feedback", review_ids)
        self.assertIn("runtime-calibrates-purpose-feedback-claims", compiler_ids)

    def test_invariant_matrix_tracks_purpose_feedback_boundary(self):
        matrix = self.read("docs/cybernetic-framework/invariant-artifact-consumer-matrix.md")

        self.assertIn("INV-PFB-001", matrix)
        self.assertIn("Purpose Feedback Boundary", matrix)
        self.assertIn("Purpose Feedback Adequacy", matrix)
        self.assertIn("tests/skills/test_purpose_feedback_boundary.py", matrix)


if __name__ == "__main__":
    unittest.main()
