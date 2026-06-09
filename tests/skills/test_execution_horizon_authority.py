import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
GUARD = ROOT / ".agents/skills/compiling-cybernetic-runtime-goals/scripts/control_chain_guard.py"
COMPILER = ROOT / ".agents/skills/compiling-cybernetic-runtime-goals/scripts/compile_runtime_goal.py"


USER_APPROVAL_APPROVED = """## What the User Approved

Status: `Approved`

| Element | Commitment |
|---|---|
| Human purpose | complete the work covered in this run without shrinking it to the first safe segment |
| Input role binding | fixture source material is approved background |
| Primary object | horizon and authority check fixture |
| Requested transformation | approved full horizon into bounded runtime execution |
| Non-goals | do not execute forbidden live actions |
| How We Know The User Purpose Was Met | user-purpose evidence remains separately calibrated |
| Where The Result Must Show Up | result-placement remains separately calibrated |
| What counts as done | work covered in this run coverage is accounted for |
| Evidence needed to call it done | work coverage matrix and authorized execution evidence exist |
| Non-achieved terminal report handling | report goal achieved: no when work covered in this run is only partially covered |
| Required answer path | work coverage and action limits guard fixture required answer path |
| Work covered in this run | Batch 1 through Batch 8 are in the work covered in this run |
| What the agent may do | local code, local tests, local smoke, ledgers, runbooks, and evidence packages may be executed |
| Forbidden live / irreversible actions | remote deployment, production nginx cutover, service restart, and production artifact overwrite |
| Required handling for unauthorized actions | prepare runbook / rollback / evidence checklist and report not executed |
| Explicitly out-of-scope items | none |
| Final Answer Format | guard output |
| Why this process is needed | full pre-goal guard fixture |
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
            f"# Requirements\n\n## Requirements Analysis Status\n\nStatus: `Complete`\n\n{USER_APPROVAL_APPROVED}\n",
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
            "Codex may report `goal achieved: yes` only when the single what counts as done is satisfied.",
            "",
            "## How We Know The User Purpose Was Met",
            "",
            "| Element | Requirement |",
            "|---|---|",
            "| Beneficiary / observer | operator |",
            "| Purpose-realizing outcome observed | operator observes work covered in this run coverage |",
            "| Supporting Evidence | internal checks support progress only |",
            "| Sufficient evidence level | purpose-limit |",
            "| If user-purpose evidence unavailable | report pending and next observation |",
            "| Allowed completion wording | achieved only when work covered in this run coverage is accounted for |",
            "",
            "## Where The Result Must Show Up",
            "",
            "| Element | Requirement |",
            "|---|---|",
            "| Target state | guard fixture intended result |",
            "| Required result places | guard fixture place model |",
            "| Place actions | act / inspect / preserve / exclude / discover |",
            "| Residual reconciliation | account for old state, unknown places, exclusions, preserved places, and remaining mismatches |",
            "| Result-placement wording | strongest result claim claim requires result-placement adequate |",
            "| Partial/unavailable handling | report not done terminal status without result claim claim |",
            "| Distinction from user-purpose evidence | result-placement is distinct from How We Know The User Purpose Was Met |",
            "",
            "## What Counts As Done",
            "",
            "| Element | Requirement |",
            "|---|---|",
            "| What counts as done | work covered in this run coverage is accounted for |",
            "| Evidence needed to call it done | work coverage matrix and authorized execution evidence exist |",
            "| Allowed achieved claim | `goal achieved: yes` only when work covered in this run coverage is accounted for |",
            "| Steps that make the result true | work coverage and action limits guard fixture required answer path |",
            "",
        ]
        if include_goal_eha:
            goal_parts.extend(
                [
                    "## Work Covered And Allowed Actions Contract",
                    "",
                    "| Element | Requirement |",
                    "|---|---|",
                    "| Work covered in this run | Batch 1 through Batch 8 are in the work covered in this run |",
                    "| What the agent may do | local code, local tests, local smoke, ledgers, runbooks, and evidence packages |",
                    "| Forbidden actions | remote deployment, production nginx cutover, service restart, production artifact overwrite |",
                    "| Prepare-only / observe-only actions | forbidden live actions must produce runbook / rollback / evidence checklist only |",
                    "| Explicitly out-of-scope items | none |",
                    "| Work coverage rule | every work covered in this run item must be executed, prepared-only, forbidden-not-executed, or explicitly out of scope by What the User Approved |",
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
            f"- Goal file: `{goal}`",
            "",
        ]
        if include_plan_eha:
            plan_parts.extend(
                [
                    "## Work Coverage And Action Limits Matrix",
                    "",
                    "| Work item / place | In work covered in this run? | What the agent may do | Required runtime handling | Counts as achieved? |",
                    "|---|---|---|---|---|",
                    "| Batch 1 local route parity | yes | execute | modify and test locally | yes if evidence checks pass |",
                    "| Batch 6 remote deployment | yes | forbidden-not-executed | prepare runbook and rollback checklist | no live claim |",
                ]
            )
            if future_roadmap_in_plan:
                plan_parts.append("| Batch 7-8 remaining route families | yes | future roadmap | move to later handoff | no |")
            plan_parts.append("")
        plan_parts.extend(
            [
                "## Steps That Make The Result True",
                "",
                "| Required step | Required state transition | Required evidence |",
                "|---|---|---|",
                "| S1 | work covered in this run exists -> work coverage accounted | work coverage matrix has coverage rows |",
                "",
                "## Action That Can Make It Done",
                "",
                "Action that can make it done:",
                "",
                "- Account for every work covered in this run item by execution, prepare-only handling, forbidden-not-executed handling, or explicit What the User Approved out-of-scope classification.",
                "",
                "Proof of impossibility, if any:",
                "",
                "- Record the condition proving a action that can make it done cannot be attempted.",
                "",
                "Non-achieved terminal report rule:",
                "",
                "- If it is not done, the report may be produced only after work coverage is accounted for or impossibility is proven.",
                "",
                "## Where The Result Must Show Up",
                "",
                "- Result placement status: `not applicable with justification`",
                "- Why no intended-result result placement is required: this fixture only checks work coverage and action limits structure.",
                "- Why no place discovery / residual reconciliation is needed: no controlled-object intended result is changed.",
                "- Allowed result claim wording: do not claim intended-result realization.",
                "",
                "## Who Does The Work / Context Use",
                "",
                "Task level: `Level 2`",
                "",
                "Who does the work: `Main-only`",
                "",
                "Selected agent workflow: `none`",
                "",
                "Work Assignment rationale:",
                "",
                "- Bounded fixture fits main-only execution.",
                "",
                "Main agent owns:",
                "",
                "- approved control artifacts",
                "- progress log",
                "- stop-condition detection",
                "",
                "## Candidate Plan Tasks",
                "",
                "### Batch 1: work coverage and action limits guard fixture",
                "",
                "Required step(s):",
                "",
                "- S1",
                "",
                "Role: `mainline`",
                "",
                "State transition advanced:",
                "",
                "- S1 fixture transition is satisfied.",
                "",
                "Transition evidence produced:",
                "",
                "- Fixture evidence needed to call it done is recorded.",
                "",
                "Integration check:",
                "",
                "- Main agent accepts S1 evidence.",
                "",
                "Counts as goal progress: `yes`",
                "",
                "Why this is not merely component completion:",
                "",
                "- It records transition evidence for the fixture path.",
                "",
                "Goal:",
                "",
                "- Keep the work coverage and action limits guard fixture structurally ready.",
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
            "- Human approved target check: `yes`",
            "- Goal file: `yes`",
            "- Execution policy: `yes`",
            "- Who does the work / context use: `yes`",
            "- User purpose evidence check: `yes`",
            "- Result placement check: `yes`",
            "- What counts as done check: `yes`",
            "- answer path check: `yes`",
            f"- Work covered in this run and authority check: `{review_eha_independence}`",
            "",
            "## Who Does The Work / Context Use",
            "",
            "Findings:",
            "- Reviewed work assignment.",
            "",
            "## User Purpose Evidence Check",
            "",
            "Findings:",
            "- Purpose feedback waits for purpose-limit evidence.",
            "",
            "## Result Placement Check",
            "",
            "Findings:",
            "- not applicable is justified for this fixture.",
            "",
            "## What Counts As Done Check",
            "",
            "Findings:",
            "- The single what counts as done is separated from not done reports.",
            "",
            "## Answer Path Check",
            "",
            "Findings:",
            "- Work packages map to the fixture required step.",
            "",
        ]
        if include_review_eha:
            review_parts.extend(
                [
                    "## Work Covered And Allowed Actions Check",
                    "",
                    "Findings:",
                    "- Work covered in this run remains in scope while authority limits define execute / prepare-only / forbidden-not-executed handling.",
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
            "Work covered in this run",
            "What the agent may do",
            "Forbidden live / irreversible actions",
            "Required handling for unauthorized actions",
            "Explicitly out-of-scope items",
        ):
            self.assertIn(required, requirements)

        self.assertIn("Work Covered And Allowed Actions Contract", goal)
        self.assertIn("Work covered in this run", goal)
        self.assertIn("What the agent may do", goal)
        self.assertIn("Work coverage rule", goal)

        self.assertIn("Work Coverage And Action Limits Matrix", plan)
        self.assertIn("What the agent may do", plan)
        self.assertIn("Required runtime handling", plan)

        self.assertIn("Work Covered And Allowed Actions Check", review)
        self.assertIn("Work covered in this run and authority check", review)

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
        self.assertIn("Work Covered And Allowed Actions Contract", output)

    def test_guard_rejects_plan_missing_horizon_authority_matrix(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            requirements, goal, plan, review = self.write_chain(Path(tmpdir), include_plan_eha=False)
            result = self.guard(requirements, goal, plan, review)

        output = result.stdout + result.stderr
        self.assertEqual(2, result.returncode, output)
        self.assertIn("NEXT: RunExecutionPolicy", output)
        self.assertIn("Work Coverage And Action Limits Matrix", output)

    def test_guard_rejects_review_missing_horizon_authority_check(self):
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
        self.assertIn("Work Covered And Allowed Actions Check", output)
        self.assertIn("Work covered in this run and authority check: yes", output)

    def test_guard_rejects_future_roadmap_inside_approved_horizon_matrix(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            requirements, goal, plan, review = self.write_chain(Path(tmpdir), future_roadmap_in_plan=True)
            result = self.guard(requirements, goal, plan, review)

        output = result.stdout + result.stderr
        self.assertEqual(2, result.returncode, output)
        self.assertIn("NEXT: RunExecutionPolicy", output)
        self.assertIn("future roadmap cannot replace work covered in this run", output)

    def test_runtime_contract_requires_horizon_coverage_report_fields(self):
        compiler = self.read(".agents/skills/compiling-cybernetic-runtime-goals/scripts/compile_runtime_goal.py")
        template = self.read(".agents/skills/compiling-cybernetic-runtime-goals/assets/runtime-goal-template.txt")
        skill = self.read(".agents/skills/compiling-cybernetic-runtime-goals/SKILL.md")

        for text in (compiler, template, skill):
            self.assertIn("work coverage", text)
            self.assertIn("executed", text)
            self.assertIn("prepared-only", text)
            self.assertIn("forbidden-not-executed", text)
            self.assertIn("explicitly out-of-scope by what the user approved", text)

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
        self.assertIn("Work Coverage And Action Limits Matrix", contract_text)
        self.assertIn("Work Covered And Allowed Actions Check", contract_text)
        self.assertIn("work coverage", contract_text)
        self.assertNotIn("future roadmap", contract_text.casefold())


if __name__ == "__main__":
    unittest.main()
