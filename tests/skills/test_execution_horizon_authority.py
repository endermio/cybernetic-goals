import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
GUARD = ROOT / ".agents/skills/compiling-cybernetic-runtime-goals/scripts/control_chain_guard.py"
COMPILER = ROOT / ".agents/skills/compiling-cybernetic-runtime-goals/scripts/compile_runtime_goal.py"


HSA_APPROVED = """## Human Setpoint Approval

Status: `Approved`

| Element | Commitment |
|---|---|
| Human purpose | complete the approved execution horizon without shrinking it to the first safe segment |
| Input role binding | fixture source material is approved background |
| Primary object | horizon and authority fidelity fixture |
| Requested transformation | approved full horizon into bounded runtime execution |
| Non-goals | do not execute forbidden live actions |
| Purpose Feedback Boundary | purpose feedback remains separately calibrated |
| Realization Surface Closure | RSC remains separately calibrated |
| Single target-achieved predicate | approved horizon coverage is accounted for |
| Target-producing evidence required | horizon coverage matrix and authorized execution evidence exist |
| Non-achieved terminal report handling | report goal achieved: no when approved horizon is only partially covered |
| Execution horizon | Batch 1 through Batch 8 are in the approved horizon |
| Runtime authority | local code, local tests, local smoke, ledgers, runbooks, and evidence packages may be executed |
| Forbidden live / irreversible actions | remote deployment, production nginx cutover, service restart, and production artifact overwrite |
| Required handling for unauthorized actions | prepare runbook / rollback / evidence checklist and report not executed |
| Explicitly out-of-scope items | none |
| Output Contract | guard output |
| Workflow fit | full pre-goal guard fixture |
| Known assumptions | fixture-only assumptions |

Approval record:

- Approved by: `test fixture`
- Approval phrase or source: `approved full horizon`
"""


class ExecutionHorizonAuthorityTest(unittest.TestCase):
    def read(self, path: str) -> str:
        return (ROOT / path).read_text(encoding="utf-8")

    def write_chain(
        self,
        tmp: Path,
        *,
        include_goal_eha: bool = True,
        include_plan_eha: bool = True,
        include_review_eha: bool = True,
        review_eha_independence: str = "yes",
        future_roadmap_in_plan: bool = False,
    ) -> tuple[Path, Path, Path, Path]:
        requirements = tmp / "requirements.md"
        goal = tmp / "goal.md"
        plan = tmp / "plan.md"
        review = tmp / "review.md"

        requirements.write_text(
            f"# Requirements\n\n## Requirements Analysis Status\n\nStatus: `Complete`\n\n{HSA_APPROVED}\n",
            encoding="utf-8",
        )

        goal_parts = [
            "# Goal",
            "",
            "## Source Contracts",
            "",
            f"- Requirements analysis: `{requirements}`",
            "",
            "## Success Condition",
            "",
            "Codex may report `goal achieved: yes` only when the single target-achieved predicate is satisfied.",
            "",
            "## Purpose Feedback Contract",
            "",
            "| Element | Requirement |",
            "|---|---|",
            "| Beneficiary / observer | operator |",
            "| Purpose-realizing outcome observed | operator observes approved horizon coverage |",
            "| Supporting Evidence | internal checks support progress only |",
            "| Sufficient evidence level | purpose-boundary |",
            "| Purpose feedback unavailable handling | report pending and next observation |",
            "| Allowed completion wording | achieved only when approved horizon coverage is accounted for |",
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
            "| Partial/unavailable handling | report non-achieved terminal status without target-realization claim |",
            "| RSC / PFB boundary | RSC calibrates target-state and surface-closure claims while PFB calibrates human-purpose realization claims |",
            "",
            "## Target Achievement Contract",
            "",
            "| Element | Requirement |",
            "|---|---|",
            "| Single target-achieved predicate | approved horizon coverage is accounted for |",
            "| Required target-producing evidence | horizon coverage matrix and authorized execution evidence exist |",
            "| Allowed achieved claim | `goal achieved: yes` only when approved horizon coverage is accounted for |",
            "",
        ]
        if include_goal_eha:
            goal_parts.extend(
                [
                    "## Execution Horizon and Authority Contract",
                    "",
                    "| Element | Requirement |",
                    "|---|---|",
                    "| Approved horizon | Batch 1 through Batch 8 are in the approved horizon |",
                    "| Runtime-authorized actions | local code, local tests, local smoke, ledgers, runbooks, and evidence packages |",
                    "| Forbidden actions | remote deployment, production nginx cutover, service restart, production artifact overwrite |",
                    "| Prepare-only / observe-only actions | forbidden live actions must produce runbook / rollback / evidence checklist only |",
                    "| Explicitly out-of-scope items | none |",
                    "| Horizon completion rule | every approved horizon item must be executed, prepared-only, forbidden-not-executed, or explicitly out of scope by HSA |",
                    "",
                ]
            )
        goal.write_text("\n".join(goal_parts), encoding="utf-8")

        plan_parts = [
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
        ]
        if include_plan_eha:
            plan_parts.extend(
                [
                    "## Horizon and Authority Coverage Matrix",
                    "",
                    "| Batch / surface | In approved horizon? | Runtime authority | Required runtime handling | Counts as achieved? |",
                    "|---|---|---|---|---|",
                    "| Batch 1 local route parity | yes | execute | modify and test locally | yes if sensors pass |",
                    "| Batch 6 remote deployment | yes | forbidden-not-executed | prepare runbook and rollback checklist | no live claim |",
                ]
            )
            if future_roadmap_in_plan:
                plan_parts.append("| Batch 7-8 remaining route families | yes | future roadmap | move to later handoff | no |")
            plan_parts.append("")
        plan_parts.extend(
            [
                "## Target-Producing Action Strategy",
                "",
                "Target-producing action required:",
                "",
                "- Account for every approved horizon item by execution, prepare-only handling, forbidden-not-executed handling, or explicit HSA out-of-scope classification.",
                "",
                "Proof of impossibility, if any:",
                "",
                "- Record the condition proving a target-producing action cannot be attempted.",
                "",
                "Non-achieved terminal report rule:",
                "",
                "- A non-achieved terminal report may be produced only after horizon coverage is accounted for or impossibility is proven.",
                "",
                "## Realization Surface Closure Strategy",
                "",
                "- RSC status: `RSC not applicable with justification`",
                "- Why no target-state surface closure is required: this fixture only checks EHA structure.",
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
                "- Bounded fixture fits main-only execution.",
                "",
                "Main agent owns:",
                "",
                "- approved control artifacts",
                "- progress log",
                "- stop-condition detection",
                "",
            ]
        )
        plan.write_text("\n".join(plan_parts), encoding="utf-8")

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
            "- Target achievement predicate fidelity: `yes`",
            f"- Execution horizon and authority fidelity: `{review_eha_independence}`",
            "",
            "## Context Management / Execution Topology",
            "",
            "Findings:",
            "- Reviewed selected topology.",
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
            "## Target Achievement Predicate Fidelity",
            "",
            "Findings:",
            "- The single target-achieved predicate is separated from non-achieved terminal reports.",
            "",
        ]
        if include_review_eha:
            review_parts.extend(
                [
                    "## Execution Horizon and Authority Fidelity",
                    "",
                    "Findings:",
                    "- Approved horizon remains in scope while authority limits define execute / prepare-only / forbidden-not-executed handling.",
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

    def guard(self, requirements: Path, goal: Path, plan: Path, review: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                sys.executable,
                str(GUARD),
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

    def test_templates_include_execution_horizon_and_authority_fields(self):
        requirements = self.read(".agents/skills/analyzing-cybernetic-requirements/assets/requirements-analysis-template.md")
        goal = self.read(".agents/skills/writing-cybernetic-goals/assets/goal-contract-template.md")
        plan = self.read(".agents/skills/writing-cybernetic-execution-policies/assets/execution-policy-template.md")
        review = self.read(".agents/skills/reviewing-cybernetic-control-structures/assets/control-review-template.md")

        for required in (
            "Execution horizon",
            "Runtime authority",
            "Forbidden live / irreversible actions",
            "Required handling for unauthorized actions",
            "Explicitly out-of-scope items",
        ):
            self.assertIn(required, requirements)

        self.assertIn("Execution Horizon and Authority Contract", goal)
        self.assertIn("Approved horizon", goal)
        self.assertIn("Runtime-authorized actions", goal)
        self.assertIn("Horizon completion rule", goal)

        self.assertIn("Horizon and Authority Coverage Matrix", plan)
        self.assertIn("Runtime authority", plan)
        self.assertIn("Required runtime handling", plan)

        self.assertIn("Execution Horizon and Authority Fidelity", review)
        self.assertIn("Execution horizon and authority fidelity", review)

    def test_guard_accepts_complete_horizon_authority_chain(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            requirements, goal, plan, review = self.write_chain(Path(tmpdir))
            result = self.guard(requirements, goal, plan, review)

        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn("NEXT: CompileRuntimeGoal", result.stdout)

    def test_guard_rejects_goal_missing_horizon_authority_contract(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            requirements, goal, plan, review = self.write_chain(Path(tmpdir), include_goal_eha=False)
            result = self.guard(requirements, goal, plan, review)

        output = result.stdout + result.stderr
        self.assertEqual(2, result.returncode, output)
        self.assertIn("NEXT: RunGoalWriting", output)
        self.assertIn("Execution Horizon and Authority Contract", output)

    def test_guard_rejects_plan_missing_horizon_authority_matrix(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            requirements, goal, plan, review = self.write_chain(Path(tmpdir), include_plan_eha=False)
            result = self.guard(requirements, goal, plan, review)

        output = result.stdout + result.stderr
        self.assertEqual(2, result.returncode, output)
        self.assertIn("NEXT: RunExecutionPolicy", output)
        self.assertIn("Horizon and Authority Coverage Matrix", output)

    def test_guard_rejects_review_missing_horizon_authority_fidelity(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            requirements, goal, plan, review = self.write_chain(
                Path(tmpdir),
                include_review_eha=False,
                review_eha_independence="no",
            )
            result = self.guard(requirements, goal, plan, review)

        output = result.stdout + result.stderr
        self.assertEqual(2, result.returncode, output)
        self.assertIn("NEXT: RunReview", output)
        self.assertIn("Execution Horizon and Authority Fidelity", output)
        self.assertIn("Execution horizon and authority fidelity: yes", output)

    def test_guard_rejects_future_roadmap_inside_approved_horizon_matrix(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            requirements, goal, plan, review = self.write_chain(Path(tmpdir), future_roadmap_in_plan=True)
            result = self.guard(requirements, goal, plan, review)

        output = result.stdout + result.stderr
        self.assertEqual(2, result.returncode, output)
        self.assertIn("NEXT: RunExecutionPolicy", output)
        self.assertIn("future roadmap cannot replace approved horizon", output)

    def test_runtime_contract_requires_horizon_coverage_report_fields(self):
        compiler = self.read(".agents/skills/compiling-cybernetic-runtime-goals/scripts/compile_runtime_goal.py")
        template = self.read(".agents/skills/compiling-cybernetic-runtime-goals/assets/runtime-goal-template.txt")
        skill = self.read(".agents/skills/compiling-cybernetic-runtime-goals/SKILL.md")

        for text in (compiler, template, skill):
            self.assertIn("horizon coverage", text)
            self.assertIn("executed", text)
            self.assertIn("prepared-only", text)
            self.assertIn("forbidden-not-executed", text)
            self.assertIn("explicitly out-of-scope by HSA", text)

        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            requirements, goal, plan, review = self.write_chain(tmp)
            runtime_contract = tmp / "runtime.goal.md"
            result = subprocess.run(
                [
                    sys.executable,
                    str(COMPILER),
                    "--requirements",
                    str(requirements),
                    "--goal",
                    str(goal),
                    "--plan",
                    str(plan),
                    "--review",
                    str(review),
                    "--out",
                    str(runtime_contract),
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
            )
            contract_text = runtime_contract.read_text(encoding="utf-8") if runtime_contract.exists() else ""

        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn("Horizon and Authority Coverage Matrix", contract_text)
        self.assertIn("Execution Horizon and Authority Fidelity", contract_text)
        self.assertIn("horizon coverage", contract_text)
        self.assertNotIn("future roadmap", contract_text.casefold())


if __name__ == "__main__":
    unittest.main()
