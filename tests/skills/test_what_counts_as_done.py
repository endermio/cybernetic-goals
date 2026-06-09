import json
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
| Human purpose | produce done-making evidence, not an alternate report status |
| Input role binding | fixture source material is approved background |
| Primary object | target achievement condition fixture |
| Requested transformation | approved chain to what-counts-as-done guard checks |
| Non-goals | do not create alternate success states |
| How We Know The User Purpose Was Met | user-purpose evidence remains separately calibrated |
| Where The Result Must Show Up | result-placement remains separately calibrated |
| What counts as done | evidence needed to call it done is observed |
| Evidence needed to call it done | action that can make it done runs or observation exists |
| Non-achieved terminal report handling | report goal achieved: no without creating alternate goals |
| Required answer path | what-counts-as-done guard fixture required answer path |
| Work covered in this run | what-counts-as-done guard fixture horizon |
| What the agent may do | local guard fixture checks |
| Forbidden live / irreversible actions | none |
| Required handling for unauthorized actions | none |
| Explicitly out-of-scope items | none |
| Final Answer Format | guard output |
| Why this process is needed | full pre-goal guard fixture |
| Known assumptions | fixture-only assumptions |

Approval record:

- Approved by: `test fixture`
- Approval phrase or source: `approved target condition`
"""


class TargetAchievementConditionCheckTest(unittest.TestCase):
    def read(self, path: str) -> str:
        return (ROOT / path).read_text(encoding="utf-8")

    def write_chain(
        self,
        tmp: Path,
        *,
        success_condition: str | None = None,
        target_contract_extra: list[str] | None = None,
        include_plan_strategy: bool = True,
        include_review_tap: bool = True,
        review_tap_independence: str = "yes",
    ) -> tuple[Path, Path, Path, Path]:
        requirements = tmp / "requirements.md"
        goal = tmp / "goal.md"
        plan = tmp / "plan.md"
        review = tmp / "review.md"

        requirements.write_text(
            f"# Requirements\n\n## Requirements Analysis Status\n\nStatus: `Complete`\n\n{USER_APPROVAL_APPROVED}\n",
            encoding="utf-8",
        )

        success = success_condition or "\n".join(
            [
                "Codex may report `goal achieved: yes` only when:",
                "",
                "- What counts as done in `What Counts As Done` is satisfied.",
                "- Required evidence needed to call it done is present.",
            ]
        )
        target_rows = [
            "| What counts as done | evidence needed to call it done is observed |",
            "| Required evidence needed to call it done | action that can make it done runs or observation exists |",
            "| Allowed achieved claim | `goal achieved: yes` only when the single condition is met |",
            "| Steps that make the result true | what-counts-as-done guard fixture required answer path |",
        ]
        target_rows.extend(target_contract_extra or [])
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
                    success,
                    "",
                    "## How We Know The User Purpose Was Met",
                    "",
                    "| Element | Requirement |",
                    "|---|---|",
                    "| Beneficiary / observer | operator |",
                    "| Purpose-realizing outcome observed | operator observes the done-making result |",
                    "| Supporting Evidence | internal checks support progress only |",
                    "| Sufficient evidence level | purpose-limit |",
                    "| If user-purpose evidence unavailable | report pending and next observation |",
                    "| Allowed completion wording | achieved only with approved target evidence |",
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
                    "| Work covered in this run | what-counts-as-done guard fixture horizon |",
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
            "| what-counts-as-done guard fixture | yes | execute | run guard / compiler fixture checks | yes if fixture passes |",
            "",
            "## Steps That Make The Result True",
            "",
            "| Required step | Required state transition | Required evidence |",
            "|---|---|---|",
            "| S1 | fixture input -> what-counts-as-done guard-ready chain | guard fixture files exist |",
            "",
        ]
        if include_plan_strategy:
            plan_parts.extend(
                [
                    "## Action That Can Make It Done",
                    "",
                    "Action that can make it done:",
                    "",
                    "- Run or observe the action that can make it done before any achieved claim.",
                    "",
                    "Proof of impossibility, if any:",
                    "",
                    "- Record the environmental or dependency condition that proves the action cannot be attempted.",
                    "",
                    "If it is not done, what should be reported:",
                    "",
                    "- If it is not done, the report may be produced only after the action is attempted and fails, or impossibility is proven.",
                    "",
                ]
            )
        plan_parts.extend(
            [
                "## Where The Result Must Show Up",
                "",
                "- Result placement status: `not applicable with justification`",
                "- Why no intended-result result placement is required: this fixture only checks what-counts-as-done structure.",
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
                "- Bounded work fits main-only execution.",
                "",
                "Main agent owns:",
                "",
                "- approved control artifacts",
                "- progress log",
                "- stop-condition detection",
                "",
                "## Candidate Plan Tasks",
                "",
                "### Batch 1: what-counts-as-done guard fixture",
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
                "- Keep the what-counts-as-done guard fixture structurally ready.",
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
            f"- What counts as done check: `{review_tap_independence}`",
            "- answer path check: `yes`",
            "- Work covered in this run and authority check: `yes`",
            "",
            "## Required Check Results",
            "",
            "- Design Answer Method Check: `Not applicable`",
            "- Steps That Make The Result True Check: `PASS`",
            "- Work Coverage / Action Limits Check: `PASS`",
            f"- Done / Purpose / Result Placement Check: `{'PASS' if review_tap_independence == 'yes' else 'FAIL'}`",
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
        ]
        if include_review_tap:
            review_parts.extend(
                [
                    "## What Counts As Done Check",
                    "",
                    "Findings:",
                    "- The single what counts as done is separated from not done reports.",
                    "",
                ]
            )
        review_parts.extend(
            [
                "## Answer Path Check",
                "",
                "Findings:",
                "- Work packages map to the fixture required step.",
                "",
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

    def test_templates_use_target_achievement_names_and_no_fallback_target_fields(self):
        files = [
            ".agents/skills/analyzing-cybernetic-requirements/assets/requirements-analysis-template.md",
            ".agents/skills/writing-cybernetic-goals/assets/goal-contract-template.md",
            ".agents/skills/writing-cybernetic-execution-policies/assets/execution-policy-template.md",
            ".agents/skills/reviewing-cybernetic-control-structures/assets/control-review-template.md",
        ]
        combined = "\n".join(self.read(path) for path in files)

        for required in (
            "What counts as done",
            "Evidence needed to call it done",
            "What Counts As Done",
            "Action That Can Make It Done",
            "What Counts As Done Check",
        ):
            self.assertIn(required, combined)

        for removed in (
            "What Counts As Done Contract",
            "What Counts As Done Strategy",
            "Valid not done report statuses",
            "Fallback report handling",
            "Fallback report statuses",
            "fallback reason",
        ):
            self.assertNotIn(removed, combined)

        success_condition = self.read(
            ".agents/skills/writing-cybernetic-goals/assets/goal-contract-template.md"
        ).split("## Success Condition", 1)[1].split("## How We Know The User Purpose Was Met", 1)[0]
        self.assertNotIn("Supporting Evidence", success_condition)

    def test_guard_rejects_success_condition_with_non_achieved_status(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            requirements, goal, plan, review = self.write_chain(
                Path(tmpdir),
                success_condition=(
                    "Codex may stop successfully when one valid final status is reached, "
                    "including partial, diagnostic, blocked, invalid, or unavailable."
                ),
            )
            result = self.guard(requirements, goal, plan, review)

        output = result.stdout + result.stderr
        self.assertEqual(2, result.returncode, output)
        self.assertIn("NEXT: RunGoalWriting", output)
        self.assertIn("Success Condition", output)
        self.assertIn("not done report term", output)

    def test_guard_rejects_target_contract_with_fallback_or_valid_final_status(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            requirements, goal, plan, review = self.write_chain(
                Path(tmpdir),
                target_contract_extra=[
                    "| Valid final status | global_ready / partial / blocked |",
                    "| Fallback report handling | use partial report when target run is unavailable |",
                ],
            )
            result = self.guard(requirements, goal, plan, review)

        output = result.stdout + result.stderr
        self.assertEqual(2, result.returncode, output)
        self.assertIn("NEXT: RunGoalWriting", output)
        self.assertIn("What Counts As Done", output)
        self.assertIn("not done or fallback term", output)

    def test_guard_rejects_target_contract_with_non_achieved_terminal_report_statuses(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            requirements, goal, plan, review = self.write_chain(
                Path(tmpdir),
                target_contract_extra=[
                    "| Report when not done statuses | partial / blocked |",
                ],
            )
            result = self.guard(requirements, goal, plan, review)

        output = result.stdout + result.stderr
        self.assertEqual(2, result.returncode, output)
        self.assertIn("NEXT: RunGoalWriting", output)
        self.assertIn("What Counts As Done", output)
        self.assertIn("not done or fallback term", output)

    def test_guard_rejects_multiple_target_achieved_conditions(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            requirements, goal, plan, review = self.write_chain(
                Path(tmpdir),
                target_contract_extra=[
                    "| What counts as done | a lower-cost report exists |",
                ],
            )
            result = self.guard(requirements, goal, plan, review)

        output = result.stdout + result.stderr
        self.assertEqual(2, result.returncode, output)
        self.assertIn("NEXT: RunGoalWriting", output)
        self.assertIn("exactly one What counts as done field", output)

    def test_guard_rejects_plan_missing_target_producing_action_strategy(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            requirements, goal, plan, review = self.write_chain(Path(tmpdir), include_plan_strategy=False)
            result = self.guard(requirements, goal, plan, review)

        output = result.stdout + result.stderr
        self.assertEqual(2, result.returncode, output)
        self.assertIn("NEXT: RunExecutionPolicy", output)
        self.assertIn("Action That Can Make It Done", output)

    def test_guard_rejects_review_missing_target_achievement_condition_check(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            requirements, goal, plan, review = self.write_chain(
                Path(tmpdir),
                include_review_tap=False,
                review_tap_independence="no",
            )
            result = self.guard(requirements, goal, plan, review)

        output = result.stdout + result.stderr
        self.assertEqual(2, result.returncode, output)
        self.assertIn("NEXT: RunReview", output)
        self.assertIn("What Counts As Done Check", output)
        self.assertIn("What counts as done check: yes", output)

    def test_runtime_compiler_uses_non_achieved_reason_not_fallback_reason(self):
        compiler = self.read(".agents/skills/compiling-cybernetic-runtime-goals/scripts/compile_runtime_goal.py")
        template = self.read(".agents/skills/compiling-cybernetic-runtime-goals/assets/runtime-goal-template.txt")
        skill = self.read(".agents/skills/compiling-cybernetic-runtime-goals/SKILL.md")

        for text in (compiler, template, skill):
            self.assertIn("what counts as done met: yes/no", text)
            self.assertIn("not done reason", text)
            self.assertIn("action that can make it done attempted or proof of impossibility", text)
            self.assertNotIn("fallback reason", text)

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
            contract_text = runtime_contract.read_text(encoding="utf-8")

        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn("Use this /goal:", result.stdout)
        self.assertNotIn("what counts as done met: yes/no", result.stdout)
        self.assertIn("what counts as done met: yes/no", contract_text)
        self.assertIn("not done reason", contract_text)
        self.assertNotIn("fallback reason", result.stdout)

    def test_runtime_compiler_rejects_misleading_out_path_suffix(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            requirements, goal, plan, review = self.write_chain(tmp)
            misleading_out = tmp / "runtime-command.txt"
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
                    str(misleading_out),
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
            )

        self.assertEqual(2, result.returncode, result.stdout + result.stderr)
        self.assertIn(".goal.md", result.stderr)
        self.assertFalse(misleading_out.exists())

    def test_runtime_compiler_emits_short_pointer_to_runtime_contract(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            requirements, goal, plan, review = self.write_chain(tmp)
            runtime_contract = tmp / "docs/cybernetics/runtime-goals/fixture.goal.md"
            runtime_contract.parent.mkdir(parents=True, exist_ok=True)
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
        self.assertIn("Runtime goal file written:", result.stdout)
        self.assertIn("Use this /goal:", result.stdout)

        pointer = next(line for line in result.stdout.splitlines() if line.startswith("/goal "))
        self.assertLessEqual(len(pointer), 800, pointer)
        self.assertIn("Execute the runtime goal file at", pointer)
        self.assertIn("docs/cybernetics/runtime-goals/fixture.goal.md", pointer)
        self.assertNotIn("How We Know The User Purpose Was Met", pointer)
        self.assertNotIn("Where The Result Must Show Up", pointer)
        self.assertNotIn("what counts as done met", pointer)
        self.assertNotIn("subagent outputs are candidate results", pointer.casefold())

        self.assertIn("## Approved Control Chain", contract_text)
        self.assertIn(str(requirements), contract_text)
        self.assertIn(str(goal), contract_text)
        self.assertIn(str(plan), contract_text)
        self.assertIn(str(review), contract_text)
        self.assertIn("## Required Sections To Read", contract_text)
        self.assertIn("What the User Approved", contract_text)
        self.assertIn("What Counts As Done", contract_text)
        self.assertIn("How We Know The User Purpose Was Met", contract_text)
        self.assertIn("Where The Result Must Show Up", contract_text)
        self.assertIn("Action That Can Make It Done", contract_text)
        self.assertIn("Who Does The Work / Context Use", contract_text)
        self.assertIn("What Counts As Done Check", contract_text)
        self.assertIn("User Purpose Evidence Check", contract_text)
        self.assertIn("Result Placement Check", contract_text)
        self.assertIn("Final Observer Check", contract_text)
        self.assertIn("goal achieved: yes/no", contract_text)
        self.assertIn("what counts as done met: yes/no", contract_text)
        self.assertIn("smallest next action that can make it done", contract_text)

    def test_matrix_and_evals_track_tap_invariant(self):
        matrix = self.read("docs/cybernetic-framework/invariant-artifact-consumer-matrix.md")
        review_evals = json.loads(self.read(".agents/skills/reviewing-cybernetic-control-structures/evals/evals.json"))
        compiler_evals = json.loads(self.read(".agents/skills/compiling-cybernetic-runtime-goals/evals/evals.json"))

        self.assertIn("INV-what-counts-as-done-001", matrix)
        self.assertIn("What Counts As Done Check", matrix)
        self.assertIn("tests/skills/test_what_counts_as_done.py", matrix)
        self.assertNotIn("INV-CPF-001", matrix)

        review_ids = {item["id"] for item in review_evals["evals"]}
        compiler_ids = {item["id"] for item in compiler_evals["evals"]}
        self.assertIn("report-when-not-done-cannot-count-as-done", review_ids)
        self.assertIn("target-contract-cannot-contain-alternate-report-statuses", review_ids)
        self.assertIn("runtime-calibrates-what-counts-as-done-claims", compiler_ids)


if __name__ == "__main__":
    unittest.main()
