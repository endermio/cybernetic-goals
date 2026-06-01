import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


class ContextTopologySkillTest(unittest.TestCase):
    def test_execution_policy_requires_context_topology(self):
        skill = (
            ROOT
            / ".agents/skills/writing-cybernetic-execution-policies/SKILL.md"
        ).read_text(encoding="utf-8")
        template = (
            ROOT
            / ".agents/skills/writing-cybernetic-execution-policies/assets/execution-policy-template.md"
        ).read_text(encoding="utf-8")

        for text in (skill, template):
            self.assertIn("Context Management / Execution Topology", text)
            self.assertIn("Main-only", text)
            self.assertIn("Serial subagent-driven", text)
            self.assertIn("Parallel subagent-driven", text)
            self.assertIn("Context pack", text)
            self.assertIn("Return format", text)
            self.assertIn("Integration gate", text)

        self.assertIn("main agent owns", template.casefold())
        self.assertIn("subagent owns", template.casefold())

    def test_review_checks_context_topology(self):
        skill = (
            ROOT
            / ".agents/skills/reviewing-cybernetic-control-structures/SKILL.md"
        ).read_text(encoding="utf-8")
        template = (
            ROOT
            / ".agents/skills/reviewing-cybernetic-control-structures/assets/control-review-template.md"
        ).read_text(encoding="utf-8")

        for text in (skill, template):
            self.assertIn("Context Management / Execution Topology", text)
            self.assertIn("selected topology", text.casefold())
            self.assertIn("context pack", text.casefold())
            self.assertIn("return format", text.casefold())
            self.assertIn("integration gate", text.casefold())

        self.assertIn("Level 3/4", skill)
        self.assertIn("context overload", skill.casefold())

    def test_runtime_compiler_preserves_serial_subagent_topology(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            requirements = tmp / "requirements.md"
            goal = tmp / "goal.md"
            plan = tmp / "plan.md"
            review = tmp / "review.md"

            requirements.write_text(
                "# Requirements\n\n## Requirements Analysis Status\n\nStatus: `Complete`\n",
                encoding="utf-8",
            )
            goal.write_text(
                f"# Goal\n\n## Source Contracts\n\n- Requirements analysis: `{requirements}`\n",
                encoding="utf-8",
            )
            plan.write_text(
                "\n".join(
                    [
                        "# Execution Policy",
                        "",
                        "## Execution Policy Status",
                        "",
                        "Status: `Candidate`",
                        "",
                        "## Source Contracts",
                        "",
                        f"- Requirements analysis: `{requirements}`",
                        f"- Goal contract: `{goal}`",
                        "",
                        "## Context Management / Execution Topology",
                        "",
                        "Selected topology: `Serial subagent-driven`",
                    ]
                ),
                encoding="utf-8",
            )
            review.write_text(
                f"# Review\n\n## Review Status\n\nStatus: `Approved`\n\nReviewed `{requirements}`, `{goal}`, and `{plan}`.\n\n"
                "## Final Observer Check\n\n"
                "- Last independent review completed at: `test`\n"
                "- Substantive artifact changes after last independent review: `no`\n"
                "- If yes, final re-review performed: `no`\n"
                "- Final reviewers confirming no Blocking/Major findings:\n"
                "  - test reviewer\n"
                "- Deterministic-only exception used: `no`\n"
                "- Deterministic guard covering exception:\n"
                "  - not used\n"
                "- Approval allowed after final observer check: `yes`\n",
                encoding="utf-8",
            )

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
        self.assertIn("approved execution topology", result.stdout)
        self.assertIn("$superpowers:subagent-driven-development", result.stdout)
        self.assertIn("only one execution subagent active at a time", result.stdout)
        self.assertIn("main agent coordinates", result.stdout)
        self.assertNotIn("Execute serially according to the approved batch rhythm", result.stdout)
