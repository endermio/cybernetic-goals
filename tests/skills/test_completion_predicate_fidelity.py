import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

HSA_FIXTURE = """## Human Setpoint Approval

Status: `Approved`

| Element | Commitment |
|---|---|
| Human purpose | measure a target-achieving outcome rather than classify a report |
| Input role binding | fixture material is approved background |
| Primary object | completion predicate guard fixture |
| Requested transformation | approved control chain to CPF guard checks |
| Non-goals | do not treat fallback reports as achieved |
| Purpose Feedback Boundary | covered by compact fixture |
| Realization Surface Closure | covered by compact fixture |
| Completion Predicate | goal achieved only when target-producing evidence is observed |
| Non-achieved report statuses | partial, diagnostic, blocked, invalid |
| Fallback report handling | report honestly without claiming goal achieved |
| Output Contract | guard output |
| Workflow fit | full pre-goal guard fixture |
| Known assumptions | fixture-only assumptions |

Approval record:

- Approved by: `test fixture`
- Approval phrase or source: `approved fixture setpoint`
"""


class CompletionPredicateFidelityTest(unittest.TestCase):
    def read(self, path: str) -> str:
        return (ROOT / path).read_text(encoding="utf-8")

    def write_guard_artifacts(
        self,
        tmp: Path,
        *,
        include_goal_cpf: bool = True,
        include_review_cpf: bool = True,
        review_independence_cpf: str = "yes",
    ) -> tuple[Path, Path, Path, Path]:
        requirements = tmp / "requirements.md"
        goal = tmp / "goal.md"
        plan = tmp / "plan.md"
        review = tmp / "review.md"

        requirements.write_text(
            f"# Requirements\n\n## Requirements Analysis Status\n\nStatus: `Complete`\n\n{HSA_FIXTURE}\n",
            encoding="utf-8",
        )

        goal_parts = [
            "# Goal",
            "",
            "## Source Contracts",
            "",
            f"- Requirements analysis: `{requirements}`",
            "",
            "## Purpose Feedback Contract",
            "",
            "| Element | Requirement |",
            "|---|---|",
            "| Beneficiary / observer | operator |",
            "| Purpose-realizing outcome observed | operator can observe the target-achieving result |",
            "| Supporting Evidence | internal checks support progress only |",
            "| Sufficient evidence level | purpose-boundary |",
            "| Purpose feedback unavailable handling | report pending and next observation |",
            "| Allowed completion wording | pending until target-achieving evidence is observed |",
            "",
            "## Realization Surface Contract",
            "",
            "| Element | Requirement |",
            "|---|---|",
            "| Target state | guard fixture target state |",
            "| Required surfaces | guard fixture surface model |",
            "| Surface actions | act / inspect / preserve / exclude / discover |",
            "| Residual reconciliation | account for old state, unknown surfaces, exclusions, preserved surfaces, and remaining mismatches |",
            "| RSC status wording | strongest target-realization claim requires RSC adequate |",
            "| Partial/unavailable handling | report partial, missing, unavailable, or not applicable with justification |",
            "| RSC / PFB boundary | RSC calibrates target-state and surface-closure claims while PFB calibrates human-purpose realization claims |",
            "",
        ]
        if include_goal_cpf:
            goal_parts.extend(
                [
                    "## Completion Predicate Contract",
                    "",
                    "| Element | Requirement |",
                    "|---|---|",
                    "| Target-achieved predicate | target-producing evidence is observed |",
                    "| Valid non-achieved report statuses | partial, diagnostic, blocked, invalid |",
                    "| Fallback report handling | fallback reports are honest non-achieved reports |",
                    "| Allowed goal-achieved claim | only target-achieved predicate supports goal achieved: yes |",
                    "| CPF / PFB / RSC boundary | CPF calibrates completion claims; PFB calibrates purpose feedback; RSC calibrates target-state surface closure |",
                    "",
                ]
            )
        goal.write_text("\n".join(goal_parts), encoding="utf-8")

        plan.write_text(
            "\n".join(
                [
                    "# Plan",
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
                    "## Completion Predicate Strategy",
                    "",
                    "Target-achieving action:",
                    "",
                    "- Observe target-producing evidence before claiming achieved.",
                    "",
                    "Fallback report statuses:",
                    "",
                    "- partial",
                    "- diagnostic",
                    "- blocked",
                    "",
                    "Fallback cannot replace:",
                    "",
                    "- target-producing action or proof of impossibility.",
                    "",
                    "## Realization Surface Closure Strategy",
                    "",
                    "- RSC status: `RSC not applicable with justification`",
                    "- Why no target-state surface closure is required: this fixture only checks CPF structure.",
                    "- Why no surface discovery / residual reconciliation is needed: no controlled-object target state is changed.",
                    "- Allowed target-realization wording: do not claim target-state realization.",
                    "",
                    "## Context Management / Execution Topology",
                    "",
                    "Task level: `Level 2`",
                    "",
                    "Selected topology: `Main-only`",
                    "",
                    "Selected delegation substrate: `none`",
                    "",
                    "Topology rationale:",
                    "",
                    "- Bounded work fits main-only execution.",
                    "",
                    "Main agent owns:",
                    "",
                    "- approved control artifacts",
                    "- progress log",
                    "- stop-condition detection",
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
            "## Review Independence",
            "",
            "- Requirements analysis: `yes`",
            "- Human setpoint fidelity: `yes`",
            "- Goal contract: `yes`",
            "- Execution policy: `yes`",
            "- Context management / execution topology: `yes`",
            "- Purpose feedback adequacy: `yes`",
            "- Realization surface closure adequacy: `yes`",
            f"- Completion predicate fidelity: `{review_independence_cpf}`",
            "",
            "## Context Management / Execution Topology",
            "",
            "Findings:",
            "- Reviewed selected topology and no Blocking/Major findings.",
            "",
            "## Purpose Feedback Adequacy",
            "",
            "Findings:",
            "- Purpose feedback waits for purpose-boundary evidence.",
            "",
            "## Realization Surface Closure Adequacy",
            "",
            "Findings:",
            "- RSC not applicable is justified for this fixture.",
            "",
        ]
        if include_review_cpf:
            review_parts.extend(
                [
                    "## Completion Predicate Fidelity",
                    "",
                    "Findings:",
                    "- Target-achieved status is separated from partial, diagnostic, blocked, and invalid report statuses.",
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
                "",
            ]
        )
        review.write_text("\n".join(review_parts), encoding="utf-8")
        return requirements, goal, plan, review

    def test_requirements_hsa_records_completion_predicate_commitment(self):
        template = self.read(
            ".agents/skills/analyzing-cybernetic-requirements/assets/requirements-analysis-template.md"
        )
        hsa = template.split("## Human Setpoint Approval", 1)[1].split("## Human Purpose", 1)[0]

        self.assertIn("Completion Predicate", hsa)
        self.assertIn("Non-achieved report statuses", hsa)
        self.assertIn("Fallback report handling", hsa)

    def test_goal_defines_completion_predicate_contract(self):
        skill = self.read(".agents/skills/writing-cybernetic-goals/SKILL.md")
        template = self.read(".agents/skills/writing-cybernetic-goals/assets/goal-contract-template.md")

        for text in (skill, template):
            self.assertIn("Completion Predicate Contract", text)
            self.assertIn("Target-achieved predicate", text)
            self.assertIn("Valid non-achieved report statuses", text)
            self.assertIn("Fallback report handling", text)
            self.assertIn("Allowed goal-achieved claim", text)

    def test_execution_policy_defines_completion_predicate_strategy(self):
        skill = self.read(".agents/skills/writing-cybernetic-execution-policies/SKILL.md")
        template = self.read(
            ".agents/skills/writing-cybernetic-execution-policies/assets/execution-policy-template.md"
        )

        for text in (skill, template):
            self.assertIn("Completion Predicate Strategy", text)
            self.assertIn("Target-achieving action", text)
            self.assertIn("Fallback report statuses", text)
            self.assertIn("Fallback cannot replace", text)

    def test_review_checks_completion_predicate_fidelity(self):
        skill = self.read(".agents/skills/reviewing-cybernetic-control-structures/SKILL.md")
        template = self.read(
            ".agents/skills/reviewing-cybernetic-control-structures/assets/control-review-template.md"
        )

        for text in (skill, template):
            self.assertIn("Completion Predicate Fidelity", text)
            self.assertIn("fallback", text.casefold())
            self.assertIn("valid report status", text.casefold())
            self.assertIn("target-achieved", text)

    def test_control_chain_guard_rejects_goal_missing_completion_predicate_contract(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            requirements, goal, plan, review = self.write_guard_artifacts(
                Path(tmpdir),
                include_goal_cpf=False,
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
        self.assertIn("NEXT: RunGoalWriting", output)
        self.assertIn("Completion Predicate Contract", output)

    def test_control_chain_guard_rejects_review_missing_completion_predicate_fidelity(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            requirements, goal, plan, review = self.write_guard_artifacts(
                Path(tmpdir),
                include_review_cpf=False,
                review_independence_cpf="no",
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
        self.assertIn("Completion Predicate Fidelity", output)
        self.assertIn("Completion predicate fidelity: yes", output)

    def test_runtime_compiler_calibrates_fallback_report_statuses(self):
        skill = self.read(".agents/skills/compiling-cybernetic-runtime-goals/SKILL.md")
        template = self.read(".agents/skills/compiling-cybernetic-runtime-goals/assets/runtime-goal-template.txt")
        compiler = self.read(".agents/skills/compiling-cybernetic-runtime-goals/scripts/compile_runtime_goal.py")

        required = (
            "Do not treat fallback, partial, diagnostic, unavailable, invalid, or blocked report statuses as goal achieved",
            "goal achieved: yes/no",
            "target-achieved status",
            "report status",
            "target-producing evidence",
            "fallback reason",
            "smallest next target-producing attempt",
        )
        for text in (skill, template, compiler):
            for phrase in required:
                self.assertIn(phrase, text)

        with tempfile.TemporaryDirectory() as tmpdir:
            requirements, goal, plan, review = self.write_guard_artifacts(Path(tmpdir))
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
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
            )

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("fallback, partial, diagnostic, unavailable, invalid, or blocked", result.stdout)
        self.assertIn("goal achieved: yes/no", result.stdout)
        self.assertIn("smallest next target-producing attempt", result.stdout)

    def test_invariant_matrix_tracks_completion_predicate_fidelity(self):
        matrix = self.read("docs/cybernetic-framework/invariant-artifact-consumer-matrix.md")

        self.assertIn("INV-CPF-001", matrix)
        self.assertIn("Completion Predicate Fidelity", matrix)
        self.assertIn("Completion Predicate Contract", matrix)
        self.assertIn("control_chain_guard.py", matrix)
        self.assertIn("tests/skills/test_completion_predicate_fidelity.py", matrix)

    def test_completion_predicate_evals_cover_fallback_not_achieved(self):
        review_evals = json.loads(
            self.read(".agents/skills/reviewing-cybernetic-control-structures/evals/evals.json")
        )
        compiler_evals = json.loads(
            self.read(".agents/skills/compiling-cybernetic-runtime-goals/evals/evals.json")
        )
        review_ids = {item["id"] for item in review_evals["evals"]}
        compiler_ids = {item["id"] for item in compiler_evals["evals"]}

        self.assertIn("fallback-report-status-cannot-be-goal-achieved", review_ids)
        self.assertIn("classification-task-may-use-report-status-without-achieved-claim", review_ids)
        self.assertIn("runtime-calibrates-completion-predicate-claims", compiler_ids)


if __name__ == "__main__":
    unittest.main()
