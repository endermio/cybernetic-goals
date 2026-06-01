import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


class ContextTopologySkillTest(unittest.TestCase):
    def complete_serial_topology(self) -> str:
        return "\n".join(
            [
                "Selected topology: `Serial subagent-driven`",
                "",
                "Topology rationale:",
                "",
                "- Level 3 context load needs bounded delegation.",
                "",
                "Main agent owns:",
                "",
                "- approved control artifacts",
                "- dispatch",
                "- integration",
                "- progress log",
                "- stop-condition detection",
                "",
                "Delegation matrix:",
                "",
                "| Work package | Executor | Context pack | Allowed actions | Return format | Integration gate |",
                "|---|---|---|---|---|---|",
                "| Package A | serial subagent | requirements, goal, plan | inspect files | findings and evidence | main integrates result |",
                "",
                "Subagent delegation substrate:",
                "",
                "- Runtime target-work delegation uses `$superpowers:subagent-driven-development` discipline.",
            ]
        )

    def write_artifact_chain(self, tmp: Path, topology_body: str) -> tuple[Path, Path, Path, Path]:
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
                    topology_body,
                    "",
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
        return requirements, goal, plan, review

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
            requirements, goal, plan, review = self.write_artifact_chain(
                tmp,
                self.complete_serial_topology(),
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

    def test_control_chain_guard_rejects_incomplete_subagent_topology(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            requirements, goal, plan, review = self.write_artifact_chain(
                Path(tmpdir),
                "Selected topology: `Serial subagent-driven`\n",
            )

            result = subprocess.run(
                [
                    sys.executable,
                    str(
                        ROOT
                        / ".agents/skills/compiling-cybernetic-runtime-goals/scripts/control_chain_guard.py"
                    ),
                    "--requirements",
                    str(requirements),
                    "--goal",
                    str(goal),
                    "--plan",
                    str(plan),
                    "--review",
                    str(review),
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
            )

        output = result.stdout + result.stderr
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("NEXT: RunExecutionPolicy", output)
        self.assertIn("Context pack", output)
        self.assertIn("Return format", output)
        self.assertIn("Integration gate", output)

    def test_orchestration_guard_rejects_incomplete_subagent_topology(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            requirements, goal, plan, _review = self.write_artifact_chain(
                Path(tmpdir),
                "Selected topology: `Serial subagent-driven`\n",
            )

            result = subprocess.run(
                [
                    sys.executable,
                    str(
                        ROOT
                        / ".agents/skills/orchestrating-cybernetic-pregoal/scripts/orchestration_guard.py"
                    ),
                    "--state",
                    "before-review",
                    "--requirements",
                    str(requirements),
                    "--goal",
                    str(goal),
                    "--plan",
                    str(plan),
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
            )

        output = result.stdout + result.stderr
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("NEXT: RunExecutionPolicy", output)
        self.assertIn("Context pack", output)
        self.assertIn("Return format", output)
        self.assertIn("Integration gate", output)

    def test_guards_accept_complete_subagent_topology_structure(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            requirements, goal, plan, review = self.write_artifact_chain(
                Path(tmpdir),
                self.complete_serial_topology(),
            )

            control_guard = subprocess.run(
                [
                    sys.executable,
                    str(
                        ROOT
                        / ".agents/skills/compiling-cybernetic-runtime-goals/scripts/control_chain_guard.py"
                    ),
                    "--requirements",
                    str(requirements),
                    "--goal",
                    str(goal),
                    "--plan",
                    str(plan),
                    "--review",
                    str(review),
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
            )
            orchestration_guard = subprocess.run(
                [
                    sys.executable,
                    str(
                        ROOT
                        / ".agents/skills/orchestrating-cybernetic-pregoal/scripts/orchestration_guard.py"
                    ),
                    "--state",
                    "before-review",
                    "--requirements",
                    str(requirements),
                    "--goal",
                    str(goal),
                    "--plan",
                    str(plan),
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
            )

        self.assertEqual(control_guard.returncode, 0, control_guard.stdout + control_guard.stderr)
        self.assertEqual(orchestration_guard.returncode, 0, orchestration_guard.stdout + orchestration_guard.stderr)
