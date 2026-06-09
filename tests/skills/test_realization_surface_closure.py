import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

USER_APPROVAL_FIXTURE = """## What the User Approved

Status: `Approved`

| Element | Commitment |
|---|---|
| Human purpose | keep realization place guard fixtures focused on result-placement behavior |
| Input role binding | test fixture source material is approved background |
| Primary object | realization place guard fixture |
| Requested transformation | approved control chain to result-placement guard checks |
| Non-goals | do not test What the User Approved behavior in this fixture |
| How We Know The User Purpose Was Met | covered by compact fixture |
| Where The Result Must Show Up | dedicated test target |
| What counts as done | evidence needed to call it done is observed |
| Evidence needed to call it done | evidence needed to call it done is observed |
| Non-achieved terminal report handling | report goal achieved: no |
| Required answer path | result-placement guard fixture required answer path |
| Work covered in this run | result-placement guard fixture horizon |
| What the agent may do | local guard fixture checks |
| Forbidden live / irreversible actions | none |
| Required handling for unauthorized actions | none |
| Explicitly out-of-scope items | none |
| Final Answer Format | guard output |
| Why this process is needed | full pre-goal guard fixture |
| Known assumptions | fixture-only assumptions |

Approval record:

- Approved by: `test fixture`
- Approval phrase or source: `approved fixture approved target`
"""


class RealizationPlaceCompletionTest(unittest.TestCase):
    def read(self, path: str) -> str:
        return (ROOT / path).read_text(encoding="utf-8")

    def write_guard_artifacts(
        self,
        tmp: Path,
        *,
        include_goal_rsc: bool = True,
        complete_goal_rsc_fields: bool = True,
        include_plan_rsc: bool = True,
        plan_rsc_not_applicable: bool = False,
        include_review_rsc: bool = True,
        review_independence_rsc: str = "yes",
    ) -> tuple[Path, Path, Path, Path]:
        requirements = tmp / "requirements.md"
        goal = tmp / "goal.md"
        plan = tmp / "plan.md"
        review = tmp / "review.md"

        requirements.write_text(
            f"# Requirements\n\n## Requirements Analysis Status\n\nStatus: `Complete`\n\n{USER_APPROVAL_FIXTURE}\n",
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
                    "- Evidence needed to call it done is present.",
                    "",
                    "## How We Know The User Purpose Was Met",
            "",
            "| Element | Requirement |",
            "|---|---|",
            "| Beneficiary / observer | operator |",
            "| Purpose-realizing outcome observed | operator can observe the intended result |",
            "| Supporting Evidence | internal checks support progress only |",
            "| Sufficient evidence level | purpose-limit |",
            "| If user-purpose evidence unavailable | report pending and next observation |",
            "| Allowed completion wording | pending until user-purpose evidence is observed |",
            "",
        ]
        if include_goal_rsc:
            rsc_rows = [
                "| Target state | target semantics are represented across realization places |",
                "| Required result places | place model, action classification, residual reconciliation |",
            ]
            if complete_goal_rsc_fields:
                rsc_rows.extend(
                    [
                        "| Place actions | act / inspect / preserve / exclude / discover |",
                        "| Residual reconciliation | account for old state, unknown places, exclusions, preserved places, and remaining mismatches |",
                        "| Result-placement wording | strongest result claim claim requires result-placement adequate |",
                        "| Partial/unavailable handling | report partial, missing, unavailable, or not applicable with justification |",
                        "| Distinction from user-purpose evidence | result-placement is distinct from How We Know The User Purpose Was Met |",
                    ]
                )
            goal_parts.extend(["## Where The Result Must Show Up", "", "| Element | Requirement |", "|---|---|", *rsc_rows, ""])
        goal_parts.extend(
            [
                "## What Counts As Done",
                "",
                "| Element | Requirement |",
                "|---|---|",
                "| What counts as done | evidence needed to call it done is observed |",
                    "| Evidence needed to call it done | evidence needed to call it done is observed |",
                "| Allowed achieved claim | only what counts as done supports goal achieved: yes |",
                "| Steps that make the result true | result-placement guard fixture required answer path |",
                "",
                "## Work Covered And Allowed Actions Contract",
                "",
                "| Element | Requirement |",
                "|---|---|",
                "| Work covered in this run | result-placement guard fixture horizon |",
                "| What the agent may do | local guard fixture checks |",
                "| Forbidden actions | none |",
                "| Prepare-only / observe-only actions | none |",
                "| Explicitly out-of-scope items | none |",
                "| Work coverage rule | every horizon item is accounted for in this fixture |",
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
            "## Work Coverage And Action Limits Matrix",
            "",
            "| Work item / place | In work covered in this run? | What the agent may do | Required runtime handling | Counts as achieved? |",
            "|---|---|---|---|---|",
            "| result-placement guard fixture | yes | execute | run guard / compiler fixture checks | yes if fixture passes |",
            "",
            "## Steps That Make The Result True",
            "",
            "| Required step | Required state transition | Required evidence |",
            "|---|---|---|",
            "| S1 | fixture input -> result-placement guard-ready chain | guard fixture files exist |",
            "",
            "## Action That Can Make It Done",
            "",
            "Action that can make it done:",
            "",
            "- Run or observe the action that can make it done before any achieved claim.",
            "",
            "Proof of impossibility, if any:",
            "",
            "- Record the condition proving the action cannot be attempted.",
            "",
            "Non-achieved terminal report rule:",
            "",
            "- If it is not done, the report may be produced only after the action is attempted and fails, or impossibility is proven.",
            "",
        ]
        if include_plan_rsc:
            if plan_rsc_not_applicable:
                plan_parts.extend(
                    [
                        "## Where The Result Must Show Up",
                        "",
                        "- Result placement status: `not applicable with justification`",
                        "- Why no intended-result result placement is required: this fixture only checks runtime chain structure.",
                        "- Why no place discovery / residual reconciliation is needed: no controlled-object intended result is changed.",
                        "- Allowed result claim wording: do not claim intended-result realization; report not applicable with justification.",
                        "",
                    ]
                )
            else:
                plan_parts.extend(
                    [
                        "## Where The Result Must Show Up",
                        "",
                        "### Places The Result Appears",
                        "",
                        "| Place | Role in target realization | Required action | Verification / reconciliation |",
                        "|---|---|---|---|",
                        "| controlled places | carry target semantics | act / inspect | reconcile residual old state |",
                        "",
                        "### Place Classes",
                        "",
                        "- Must act: controlled places that must change.",
                        "- Must inspect: supporting places that may retain old state.",
                        "- Must preserve: places intentionally unchanged.",
                        "- Explicitly out of scope: excluded places with reason.",
                        "- Unknown or requires discovery: places needing runtime discovery.",
                        "",
                        "### Residual Reconciliation",
                        "",
                        "- Reconcile old state, unknown places, exclusions, preserved places, and remaining mismatches.",
                        "",
                    ]
                )
        plan_parts.extend(
            [
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
                "### Batch 1: result-placement guard fixture",
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
                "- Keep the result-placement guard fixture structurally ready.",
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
            "- Goal file: `yes`",
            "- Execution policy: `yes`",
            "- Who does the work / context use: `yes`",
            "- User purpose evidence check: `yes`",
            f"- Result placement check: `{review_independence_rsc}`",
            "- What counts as done check: `yes`",
            "- answer path check: `yes`",
            "- Work covered in this run and authority check: `yes`",
            "",
            "## Who Does The Work / Context Use",
            "",
            "Findings:",
            "- Reviewed work assignment and no Blocking/Major findings.",
            "",
            "## User Purpose Evidence Check",
            "",
            "Classification:",
            "- Internally verified, user purpose evidence pending",
            "",
            "Findings:",
            "- Internal checks are progress evidence; purpose achievement claim waits for purpose-limit feedback.",
            "",
        ]
        if include_review_rsc:
            review_parts.extend(
                [
                    "## Result Placement Check",
                    "",
                    "Classification:",
                    "- result-placement adequate",
                    "",
                    "Findings:",
                    "- Place model, old behavior check, and result claim wording were reviewed.",
                    "",
                ]
            )
        review_parts.extend(
            [
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
                "## Work Covered And Allowed Actions Check",
                "",
                "Findings:",
                "- Work covered in this run and runtime authority are compact and fixture-bounded.",
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

    def test_requirements_define_realization_place_completion_limit(self):
        skill = self.read(".agents/skills/analyzing-cybernetic-requirements/SKILL.md")
        template = self.read(
            ".agents/skills/analyzing-cybernetic-requirements/assets/requirements-analysis-template.md"
        )

        for text in (skill, template):
            self.assertIn("Where The Result Must Show Up", text)
            self.assertIn("Intended result", text)
            self.assertIn("Required action", text)
            self.assertIn("Old behavior check", text)
            self.assertIn("Result placement status", text)
            self.assertIn("result-placement is distinct from How We Know The User Purpose Was Met", text)
        self.assertIn("Required result places", skill)
        self.assertIn("Places the result must appear", template)

        high_value_questions = skill.split("## Ask Only High-Value Human Questions", 1)[1].split(
            "## Final Answer Format Check", 1
        )[0]
        self.assertIn("where the result must show up", high_value_questions)
        self.assertIn("intended result", high_value_questions)
        self.assertIn("required result places", high_value_questions)
        self.assertIn("required action", high_value_questions)
        self.assertIn("old behavior check", high_value_questions)

    def test_goal_preserves_rsc_contract_and_completion_wording(self):
        skill = self.read(".agents/skills/writing-cybernetic-goals/SKILL.md")
        template = self.read(".agents/skills/writing-cybernetic-goals/assets/goal-contract-template.md")

        self.assertIn("always for compiled runtime goals", skill)
        self.assertIn("not applicable with justification", skill)
        for text in (skill, template):
            self.assertIn("Where The Result Must Show Up", text)
            self.assertIn("Intended result", text)
            self.assertIn("Required result places", text)
            self.assertIn("Result-placement wording", text)
            self.assertIn("strongest positive result claim requires result-placement adequate", text)
            self.assertIn("partial, missing, unavailable, or not applicable with justification", text)
            self.assertIn("result-placement is distinct from How We Know The User Purpose Was Met", text)

    def test_execution_policy_defines_rsc_strategy(self):
        skill = self.read(".agents/skills/writing-cybernetic-execution-policies/SKILL.md")
        template = self.read(
            ".agents/skills/writing-cybernetic-execution-policies/assets/execution-policy-template.md"
        )

        for text in (skill, template):
            self.assertIn("Where The Result Must Show Up", text)
            self.assertIn("always include", text)
            self.assertIn("not applicable with justification", text)
            self.assertIn("Places The Result Appears", text)
            self.assertIn("Place Classes", text)
            self.assertIn("Residual Reconciliation", text)
            self.assertIn("Must act", text)
            self.assertIn("Must inspect", text)
            self.assertIn("Must preserve", text)
            self.assertIn("Explicitly out of scope", text)
            self.assertIn("Unknown or requires discovery", text)

    def test_execution_policy_progress_log_records_rsc_status(self):
        template = self.read(
            ".agents/skills/writing-cybernetic-execution-policies/assets/execution-policy-template.md"
        )
        progress_log = template.split("## Progress Log Rules", 1)[1]

        for required in (
            "Result placement status",
            "places acted on or inspected",
            "residuals and reconciliation",
            "allowed result claim wording",
        ):
            self.assertIn(required, progress_log)

    def test_review_classifies_rsc_adequacy(self):
        skill = self.read(".agents/skills/reviewing-cybernetic-control-structures/SKILL.md")
        template = self.read(
            ".agents/skills/reviewing-cybernetic-control-structures/assets/control-review-template.md"
        )

        for text in (skill, template):
            self.assertIn("Result Placement Check", text)
            self.assertIn("result-placement adequate", text)
            self.assertIn("result-placement partial", text)
            self.assertIn("result-placement missing", text)
            self.assertIn("result-placement unavailable", text)
            self.assertIn("not applicable with justification", text)
            self.assertIn("local action is being treated as global intended-result realization", text)

    def test_runtime_compiler_calibrates_rsc_completion_claims(self):
        skill = self.read(".agents/skills/compiling-cybernetic-runtime-goals/SKILL.md")
        template = self.read(
            ".agents/skills/compiling-cybernetic-runtime-goals/assets/runtime-goal-template.txt"
        )
        compiler = self.read(
            ".agents/skills/compiling-cybernetic-runtime-goals/scripts/compile_runtime_goal.py"
        )

        for text in (skill, template, compiler):
            self.assertIn("Where The Result Must Show Up", text)
            self.assertIn("result places covered, actions completed or justified, old behavior checked", text)
        preconditions = skill.split("## Preconditions", 1)[1].split("## Runtime Goal", 1)[0]
        self.assertIn("goal includes a compact `How We Know The User Purpose Was Met`", preconditions)
        self.assertIn("review records `User purpose evidence check: yes`", preconditions)
        self.assertIn("goal includes a compact `Where The Result Must Show Up`", preconditions)
        self.assertIn("execution policy includes `Where The Result Must Show Up`", preconditions)
        self.assertIn("review records `Result placement check: yes`", preconditions)

        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            requirements, goal, plan, review = self.write_guard_artifacts(tmp)
            runtime_contract = tmp / "runtime.goal.md"
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
                    "--out",
                    str(runtime_contract),
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
            )
            contract_text = runtime_contract.read_text(encoding="utf-8")

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("Use this /goal:", result.stdout)
        self.assertNotIn("Where The Result Must Show Up", result.stdout)
        self.assertIn("Where The Result Must Show Up", contract_text)
        self.assertIn("Where The Result Must Show Up", contract_text)
        self.assertIn("Result Placement Check", contract_text)
        self.assertIn("result places covered, actions completed or justified, old behavior checked", contract_text)

    def test_control_chain_guard_rejects_goal_missing_rsc_contract(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            requirements, goal, plan, review = self.write_guard_artifacts(
                Path(tmpdir),
                include_goal_rsc=False,
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
        self.assertIn("Where The Result Must Show Up", output)

    def test_control_chain_guard_rejects_goal_rsc_contract_missing_required_fields(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            requirements, goal, plan, review = self.write_guard_artifacts(
                Path(tmpdir),
                complete_goal_rsc_fields=False,
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
        self.assertIn("goal Where The Result Must Show Up missing Place actions", output)
        self.assertIn("goal Where The Result Must Show Up missing Residual reconciliation", output)
        self.assertIn("goal Where The Result Must Show Up missing Distinction from user-purpose evidence", output)

    def test_control_chain_guard_rejects_plan_missing_rsc_strategy(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            requirements, goal, plan, review = self.write_guard_artifacts(
                Path(tmpdir),
                include_plan_rsc=False,
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
        self.assertIn("Where The Result Must Show Up", output)

    def test_control_chain_guard_accepts_rsc_not_applicable_plan_strategy(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            requirements, goal, plan, review = self.write_guard_artifacts(
                Path(tmpdir),
                plan_rsc_not_applicable=True,
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

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("PASS", result.stdout)

    def test_control_chain_guard_rejects_review_missing_rsc_adequacy(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            requirements, goal, plan, review = self.write_guard_artifacts(
                Path(tmpdir),
                include_review_rsc=False,
                review_independence_rsc="no",
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
        self.assertIn("Result Placement Check", output)
        self.assertIn("Result placement check: yes", output)

    def test_rsc_evals_cover_false_completion_and_not_applicable_justification(self):
        review_evals = json.loads(
            self.read(".agents/skills/reviewing-cybernetic-control-structures/evals/evals.json")
        )
        compiler_evals = json.loads(
            self.read(".agents/skills/compiling-cybernetic-runtime-goals/evals/evals.json")
        )

        review_ids = {item["id"] for item in review_evals["evals"]}
        compiler_ids = {item["id"] for item in compiler_evals["evals"]}

        self.assertIn("local-action-cannot-claim-result-without-placement", review_ids)
        self.assertIn("result-placement-not-applicable-requires-justification", review_ids)
        self.assertIn("runtime-calibrates-result-placement-claims", compiler_ids)

    def test_invariant_matrix_tracks_realization_place_completion(self):
        matrix = self.read("docs/cybernetic-framework/invariant-artifact-consumer-matrix.md")

        self.assertIn("INV-result-placement-001", matrix)
        self.assertIn("Where The Result Must Show Up", matrix)
        self.assertIn("Where The Result Must Show Up", matrix)
        self.assertIn("Result Placement Check", matrix)
        self.assertIn("execution policy result-placement strategy", matrix)
        self.assertIn("tests/skills/test_realization_surface_closure.py", matrix)


if __name__ == "__main__":
    unittest.main()
