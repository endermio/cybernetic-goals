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
                "Task level: `Level 3`",
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
                "Context Pack Requirements:",
                "",
                "| Field | Content |",
                "|---|---|",
                "| Relevant control excerpts | requirements success conditions, goal invariants, execution policy stop conditions |",
                "| Current batch objective | complete Package A bounded inspection |",
                "| Allowed artifacts/surfaces | target files listed in package scope |",
                "| Forbidden changes | control artifacts, scope, topology, unrelated files |",
                "| Required sensors/evidence | command output and evidence references |",
                "| Stop conditions | missing context, invariant conflict, unauthorized scope change |",
                "| Expected return format | summary, files inspected, evidence, blockers, next integration note |",
                "",
                "Subagent delegation substrate:",
                "",
                "- Runtime target-work delegation uses `$superpowers:subagent-driven-development` discipline.",
                "",
                "Context Compression Rule:",
                "",
                "- Active control summary: summarize current requirements, goal invariants, topology, and stop conditions.",
                "- Completed work packages: record packages integrated at the boundary.",
                "- Subagent outputs integrated: record candidate outputs accepted into main progress state.",
                "- Evidence produced: record evidence references and sensor interpretation.",
                "- Deferred sensors and reasons: preserve policy-approved deferrals.",
                "- Unresolved blockers: record blockers requiring revision or human input.",
                "- Deviations from policy: record deviations and whether execution must stop.",
                "- Next allowed action: record the next policy-approved action.",
            ]
        )

    def write_artifact_chain(
        self,
        tmp: Path,
        topology_body: str,
        *,
        include_review_topology: bool = True,
        review_topology_independence: str = "yes",
    ) -> tuple[Path, Path, Path, Path]:
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
        review_parts = [
            "# Review",
            "",
            "## Review Status",
            "",
            "Status: `Approved`",
            "",
            f"Reviewed `{requirements}`, `{goal}`, and `{plan}`.",
            "",
        ]
        if include_review_topology:
            review_parts.extend(
                [
                    "## Review Independence",
                    "",
                    "- Requirements analysis: `yes`",
                    "- Goal contract: `yes`",
                    "- Execution policy: `yes`",
                    f"- Context management / execution topology: `{review_topology_independence}`",
                    "",
                    "## Context Management / Execution Topology",
                    "",
                    "Findings:",
                    "- Reviewed selected topology, context pack requirements, delegation substrate, context compression, and integration gates; no Blocking/Major findings.",
                    "",
                ]
            )
        review_parts.extend(
            [
                "## Final Observer Check",
                "",
                "- Last independent review completed at: `test`",
                "- Substantive artifact changes after last independent review: `no`",
                "- If yes, final re-review performed: `no`",
                "- Final reviewers confirming no Blocking/Major findings:",
                "  - test reviewer",
                "- Deterministic-only exception used: `no`",
                "- Deterministic guard covering exception:",
                "  - not used",
                "- Approval allowed after final observer check: `yes`",
            ]
        )
        review.write_text("\n".join(review_parts) + "\n", encoding="utf-8")
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
            self.assertIn("Task level", text)
            self.assertIn("Context Pack Requirements", text)
            self.assertIn("Context Compression Rule", text)

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
        self.assertIn("Subagent outputs are candidate results until the main agent integrates them", result.stdout)
        self.assertNotIn("Execute serially according to the approved batch rhythm", result.stdout)

    def test_control_chain_guard_requires_review_of_context_topology(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            requirements, goal, plan, review = self.write_artifact_chain(
                Path(tmpdir),
                self.complete_serial_topology(),
                include_review_topology=False,
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
        self.assertIn("NEXT: RunReview", output)
        self.assertIn("Context Management / Execution Topology", output)

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

    def test_guards_reject_level_3_main_only_without_context_load_justification(self):
        topology_body = "\n".join(
            [
                "Selected topology: `Main-only`",
                "",
                "Task level: `Level 3`",
                "",
                "Topology rationale:",
                "",
                "- simpler",
                "",
                "Main agent owns:",
                "",
                "- approved control artifacts",
                "- dispatch",
                "- integration",
                "- progress log",
                "- stop-condition detection",
            ]
        )
        with tempfile.TemporaryDirectory() as tmpdir:
            requirements, goal, plan, review = self.write_artifact_chain(Path(tmpdir), topology_body)

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

        for result in (control_guard, orchestration_guard):
            output = result.stdout + result.stderr
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Main-only context-load justification", output)

    def test_guards_reject_weak_context_pack_requirements(self):
        weak_topology = "\n".join(
            [
                "Selected topology: `Serial subagent-driven`",
                "",
                "Task level: `Level 3`",
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
                "| Package A | serial subagent | requirements, goal, plan | inspect files | summary | review |",
                "",
                "Subagent delegation substrate:",
                "",
                "- Runtime target-work delegation uses `$superpowers:subagent-driven-development` discipline.",
                "",
                "Context Compression Rule:",
                "",
                "- Active control summary: present.",
                "- Completed work packages: present.",
                "- Subagent outputs integrated: present.",
                "- Evidence produced: present.",
                "- Deferred sensors and reasons: present.",
                "- Unresolved blockers: present.",
                "- Deviations from policy: present.",
                "- Next allowed action: present.",
            ]
        )
        with tempfile.TemporaryDirectory() as tmpdir:
            requirements, goal, plan, review = self.write_artifact_chain(Path(tmpdir), weak_topology)

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

        for result in (control_guard, orchestration_guard):
            output = result.stdout + result.stderr
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Context Pack Requirements", output)
            self.assertIn("Relevant control excerpts", output)

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
