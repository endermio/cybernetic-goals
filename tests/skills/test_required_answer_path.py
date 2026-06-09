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
| Human purpose | produce a intended result through an actor-centered path |
| Input role binding | fixture source material is approved background |
| Primary object | required answer path fixture |
| Requested transformation | approved target into required answer path-first execution policy |
| Non-goals | do not count component-only work as goal progress |
| How We Know The User Purpose Was Met | user-purpose evidence remains separately calibrated |
| Where The Result Must Show Up | result placement remains separately calibrated |
| What counts as done | all required required steps are satisfied |
| Evidence needed to call it done | required step evidence exists |
| Non-achieved terminal report handling | report goal achieved: no when required steps are unsatisfied |
| Required answer path | S0 no durable state -> S1 durable state -> S2 observable intended result |
| Work covered in this run | required answer path fixture horizon |
| What the agent may do | local guard fixture checks |
| Forbidden live / irreversible actions | none |
| Required handling for unauthorized actions | none |
| Explicitly out-of-scope items | none |
| Final Answer Format | guard output |
| Why this process is needed | full pre-goal guard fixture |
| Known assumptions | fixture-only assumptions |

Approval record:

- Approved by: `test fixture`
- Approval phrase or source: `approved required answer path`
"""


class RequiredAnswerPathTest(unittest.TestCase):
    def read(self, path: str) -> str:
        return (ROOT / path).read_text(encoding="utf-8")

    def write_chain(
        self,
        tmp: Path,
        *,
        include_goal_required_answer_path: bool = True,
        include_plan_required_answer_path: bool = True,
        include_candidate_required_answer_path_nodes: bool = True,
        include_candidate_required_answer_path_transition_fields: bool = True,
        include_review_required_answer_path: bool = True,
        review_required_answer_path_independence: str = "yes",
    ) -> tuple[Path, Path, Path, Path]:
        requirements = tmp / "requirements.md"
        goal = tmp / "goal.md"
        plan = tmp / "plan.md"
        review = tmp / "review.md"

        requirements.write_text(
            f"# Requirements\n\n## Requirements Analysis Status\n\nStatus: `Complete`\n\n{USER_APPROVAL_APPROVED}\n",
            encoding="utf-8",
        )

        target_rows = [
            "| What counts as done | all required required steps are satisfied |",
            "| Evidence needed to call it done | required step evidence exists |",
            "| Allowed achieved claim | goal achieved: yes only when all required required steps are satisfied |",
        ]
        if include_goal_required_answer_path:
            target_rows.append("| Steps that make the result true | S1 and S2 transitions in the execution policy Steps That Make The Result True |")

        goal.write_text(
            "\n".join(
                [
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
                    "| Purpose-realizing outcome observed | operator observes the required answer path completed |",
                    "| Supporting Evidence | internal checks support progress only |",
                    "| Sufficient evidence level | purpose-limit |",
                    "| If user-purpose evidence unavailable | report pending and next observation |",
                    "| Allowed completion wording | achieved only when required steps are satisfied |",
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
                    *target_rows,
                    "",
                    "## Work Covered And Allowed Actions Contract",
                    "",
                    "| Element | Requirement |",
                    "|---|---|",
                    "| Work covered in this run | required answer path fixture horizon |",
                    "| What the agent may do | local guard fixture checks |",
                    "| Forbidden actions | none |",
                    "| Prepare-only / observe-only actions | none |",
                    "| Explicitly out-of-scope items | none |",
                    "| Work coverage rule | every horizon item is accounted for in this fixture |",
                    "",
                ]
            ),
            encoding="utf-8",
        )

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
            "## Work Coverage And Action Limits Matrix",
            "",
            "| Work item / place | In work covered in this run? | What the agent may do | Required runtime handling | Counts as achieved? |",
            "|---|---|---|---|---|",
            "| required answer path fixture | yes | execute | run guard / compiler fixture checks | yes if fixture passes |",
            "",
        ]
        if include_plan_required_answer_path:
            plan_parts.extend(
                [
                    "## Steps That Make The Result True",
                    "",
                    "| Required step | Required state transition | Required evidence |",
                    "|---|---|---|",
                    "| S1 | no durable state -> durable state exists | durable state id is recorded |",
                    "| S2 | durable state exists -> observable intended result | target observation references durable state id |",
                    "",
                ]
            )
        plan_parts.extend(
            [
                "## Action That Can Make It Done",
                "",
                "Action that can make it done:",
                "",
                "- Satisfy S1 and S2 required steps before any achieved claim.",
                "",
                "Proof of impossibility, if any:",
                "",
                "- Record the condition proving a required step cannot be attempted.",
                "",
                "If it is not done, what should be reported:",
                "",
                "- If it is not done, the report may be produced only after the transition is attempted and fails, or impossibility is proven.",
                "",
                    "## Where The Result Must Show Up",
                "",
                "- Result placement status: `not applicable with justification`",
                "- Why no intended-result result placement is required: this fixture only checks TPS structure.",
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
                "### Batch 1: satisfy answer path fixture",
                "",
            ]
        )
        if include_candidate_required_answer_path_nodes:
            plan_parts.extend(
                [
                    "Required step(s):",
                    "",
                    "- S1",
                    "- S2",
                    "",
                ]
            )
        if include_candidate_required_answer_path_transition_fields:
            plan_parts.extend(
                [
                    "Role: `mainline`",
                    "",
                    "State transition advanced:",
                    "",
                    "- S1 and S2 become satisfied for the actor-centered target path.",
                    "",
                    "Transition evidence produced:",
                    "",
                    "- Durable state and observable intended result evidence.",
                    "",
                    "Integration check:",
                    "",
                    "- Main agent accepts S1/S2 evidence into progress state.",
                    "",
                    "Counts as goal progress: `yes`",
                    "",
                    "Why this is not merely component completion:",
                    "",
                    "- The task satisfies actor-centered transitions rather than only creating a component.",
                    "",
                ]
            )
        plan_parts.extend(
            [
                "Goal:",
                "",
                "- Drive the fixture through the approved required answer path.",
                "",
                "Batch-end check:",
                "",
                "- S1 and S2 evidence recorded.",
                "",
                "Steps:",
                "",
                "- [ ] Record S1 evidence.",
                "- [ ] Record S2 evidence.",
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
            "- What the user approved check: `yes`",
            "- Goal file: `yes`",
            "- Execution policy: `yes`",
            "- Who does the work / context use: `yes`",
            "- User purpose evidence check: `yes`",
            "- Result placement check: `yes`",
            "- What counts as done check: `yes`",
            f"- answer path check: `{review_required_answer_path_independence}`",
            "- Work covered in this run and authority check: `yes`",
            "",
            "## Required Check Results",
            "",
            "- Design Answer Method Check: `Not applicable`",
            "- Steps That Make The Result True Check: `PASS`",
            "- Work Coverage / Action Limits Check: `PASS`",
            "- Done / Purpose / Result Placement Check: `PASS`",
            "- Work Assignment / Subagent Check: `PASS`",
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
        ]
        if include_review_required_answer_path:
            review_parts.extend(
                [
                    "## Answer Path Check",
                    "",
                    "Findings:",
                    "- Work packages are mapped to S1/S2 required steps and supporting-only work cannot satisfy goal progress by itself.",
                    "",
                ]
            )
        review_parts.extend(
            [
                "## Work Covered And Allowed Actions Check",
                "",
                "Findings:",
                "- Work covered in this run and runtime authority are compact and fixture-bounded.",
                "",
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

    def test_templates_include_required_answer_path(self):
        requirements = self.read(".agents/skills/analyzing-cybernetic-requirements/assets/requirements-analysis-template.md")
        goal = self.read(".agents/skills/writing-cybernetic-goals/assets/goal-contract-template.md")
        plan = self.read(".agents/skills/writing-cybernetic-execution-policies/assets/execution-policy-template.md")
        review = self.read(".agents/skills/reviewing-cybernetic-control-structures/assets/control-review-template.md")

        self.assertIn("Required answer path", requirements)
        self.assertIn("Steps that make the result true", goal)
        self.assertIn("Steps That Make The Result True", plan)
        self.assertIn("Required step(s)", plan)
        self.assertIn("Answer Path Check", review)
        self.assertIn("answer path check", review)

    def test_guard_accepts_complete_required_answer_path_chain(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            requirements, goal, plan, review = self.write_chain(Path(tmpdir))
            result = self.guard(requirements, goal, plan, review)

        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn("NEXT: CompileRuntimeGoal", result.stdout)

    def test_guard_rejects_goal_missing_required_answer_path_reference(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            requirements, goal, plan, review = self.write_chain(Path(tmpdir), include_goal_required_answer_path=False)
            result = self.guard(requirements, goal, plan, review)

        output = result.stdout + result.stderr
        self.assertEqual(2, result.returncode, output)
        self.assertIn("NEXT: RunGoalWriting", output)
        self.assertIn("Steps that make the result true", output)

    def test_guard_rejects_plan_missing_required_answer_path(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            requirements, goal, plan, review = self.write_chain(Path(tmpdir), include_plan_required_answer_path=False)
            result = self.guard(requirements, goal, plan, review)

        output = result.stdout + result.stderr
        self.assertEqual(2, result.returncode, output)
        self.assertIn("NEXT: RunExecutionPolicy", output)
        self.assertIn("Steps That Make The Result True", output)

    def test_guard_rejects_candidate_task_without_required_answer_path_nodes(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            requirements, goal, plan, review = self.write_chain(Path(tmpdir), include_candidate_required_answer_path_nodes=False)
            result = self.guard(requirements, goal, plan, review)

        output = result.stdout + result.stderr
        self.assertEqual(2, result.returncode, output)
        self.assertIn("NEXT: RunExecutionPolicy", output)
        self.assertIn("Required step(s)", output)

    def test_guard_rejects_candidate_task_with_only_required_answer_path_label(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            requirements, goal, plan, review = self.write_chain(
                Path(tmpdir),
                include_candidate_required_answer_path_transition_fields=False,
            )
            result = self.guard(requirements, goal, plan, review)

        output = result.stdout + result.stderr
        self.assertEqual(2, result.returncode, output)
        self.assertIn("NEXT: RunExecutionPolicy", output)
        self.assertIn("State transition advanced", output)
        self.assertIn("Transition evidence produced", output)
        self.assertIn("Counts as goal progress", output)

    def test_guard_rejects_review_missing_required_answer_path_check(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            requirements, goal, plan, review = self.write_chain(
                Path(tmpdir),
                include_review_required_answer_path=False,
                review_required_answer_path_independence="no",
            )
            result = self.guard(requirements, goal, plan, review)

        output = result.stdout + result.stderr
        self.assertEqual(2, result.returncode, output)
        self.assertIn("NEXT: RunReview", output)
        self.assertIn("Answer Path Check", output)
        self.assertIn("answer path check: yes", output)

    def test_runtime_contract_indexes_required_answer_path(self):
        compiler = self.read(".agents/skills/compiling-cybernetic-runtime-goals/scripts/compile_runtime_goal.py")
        template = self.read(".agents/skills/compiling-cybernetic-runtime-goals/assets/runtime-goal-template.txt")
        skill = self.read(".agents/skills/compiling-cybernetic-runtime-goals/SKILL.md")

        for text in (compiler, template, skill):
            self.assertIn("Steps That Make The Result True", text)
            self.assertIn("Answer Path Check", text)

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
        self.assertIn("Steps That Make The Result True", contract_text)
        self.assertIn("Answer Path Check", contract_text)

    def test_progress_log_rules_track_required_answer_path_node_status(self):
        template = self.read(".agents/skills/writing-cybernetic-execution-policies/assets/execution-policy-template.md")
        progress_log = template.split("## Progress Log Rules", 1)[1]

        self.assertIn("required answer path step status", progress_log)
        self.assertIn("required steps satisfied", progress_log)
        self.assertIn("required steps failed / blocked / unobserved", progress_log)
        self.assertIn("supporting-only work completed", progress_log)
        self.assertIn("supporting-only work not counted as goal progress", progress_log)


if __name__ == "__main__":
    unittest.main()
