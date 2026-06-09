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
| Human purpose | keep user-purpose evidence guard fixtures focused on user-purpose evidence behavior |
| Input role binding | test fixture source material is approved background |
| Primary object | user-purpose evidence guard fixture |
| Requested transformation | approved control chain to user-purpose evidence guard checks |
| Non-goals | do not test What the User Approved behavior in this fixture |
| How We Know The User Purpose Was Met | dedicated test target |
| Where The Result Must Show Up | covered by compact fixture |
| What counts as done | purpose-limit evidence is observed |
| Evidence needed to call it done | evidence needed to call it done is observed |
| Non-achieved terminal report handling | report goal achieved: no |
| Required answer path | user-purpose evidence guard fixture required answer path |
| Work covered in this run | user-purpose evidence guard fixture horizon |
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


class PurposeFeedbackLimitTest(unittest.TestCase):
    def read(self, path: str) -> str:
        return (ROOT / path).read_text(encoding="utf-8")

    def write_guard_artifacts(
        self,
        tmp: Path,
        *,
        include_goal_pfb: bool = True,
        include_review_pfb: bool = True,
        review_independence_pfb: str = "yes",
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
        ]
        if include_goal_pfb:
            goal_parts.extend(
                [
                    "## How We Know The User Purpose Was Met",
                    "",
                    "| Element | Requirement |",
                    "|---|---|",
                    "| Beneficiary / observer | operator |",
                    "| Purpose-realizing outcome observed | operator can observe the intended result |",
                    "| Supporting Evidence | internal checks support progress only |",
                    "| Sufficient evidence level | purpose-limit |",
                    "| If user-purpose evidence unavailable | report pending and next observation |",
                    "| Allowed completion wording | pending until user purpose evidence is observed |",
                    "",
                ]
            )
        goal_parts.extend(
            [
                "## Where The Result Must Show Up",
                "",
                "| Element | Requirement |",
                "|---|---|",
                "| Target state | guard fixture intended result |",
                "| Required result places | guard fixture place model |",
                "| Place actions | act / inspect / preserve / exclude / discover |",
                "| Residual reconciliation | account for old state, unknown places, exclusions, preserved places, and remaining mismatches |",
                "| Result-placement wording | strongest result claim claim requires result-placement adequate |",
                "| Partial/unavailable handling | report partial, missing, unavailable, or not applicable with justification |",
                "| Distinction from user-purpose evidence | result-placement is distinct from How We Know The User Purpose Was Met |",
                "",
                "## What Counts As Done",
                "",
                "| Element | Requirement |",
                "|---|---|",
                "| What counts as done | purpose-limit evidence is observed |",
                    "| Evidence needed to call it done | evidence needed to call it done is observed |",
                "| Allowed achieved claim | only what counts as done supports goal achieved: yes |",
                "| Steps that make the result true | user-purpose evidence guard fixture required answer path |",
                "",
                "## Work Covered And Allowed Actions Contract",
                "",
                "| Element | Requirement |",
                "|---|---|",
                "| Work covered in this run | user-purpose evidence guard fixture horizon |",
                "| What the agent may do | local guard fixture checks |",
                "| Forbidden actions | none |",
                "| Prepare-only / observe-only actions | none |",
                "| Explicitly out-of-scope items | none |",
                "| Work coverage rule | every horizon item is accounted for in this fixture |",
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
                    f"- Goal file: `{goal}`",
                    "",
                    "## Work Coverage And Action Limits Matrix",
                    "",
                    "| Work item / place | In work covered in this run? | What the agent may do | Required runtime handling | Counts as achieved? |",
                    "|---|---|---|---|---|",
                    "| user-purpose evidence guard fixture | yes | execute | run guard / compiler fixture checks | yes if fixture passes |",
                    "",
                    "## Steps That Make The Result True",
                    "",
                    "| Required step | Required state transition | Required evidence |",
                    "|---|---|---|",
                    "| S1 | fixture input -> user-purpose evidence guard-ready chain | guard fixture files exist |",
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
                    "## Where The Result Must Show Up",
                    "",
                    "### Places The Result Appears",
                    "",
                    "| Place | Role in target realization | Required action | Verification / reconciliation |",
                    "|---|---|---|---|",
                    "| guard fixture place | carries fixture intended result | inspect | reconcile residuals in fixture scope |",
                    "",
                    "### Place Classes",
                    "",
                    "- Must act: none for user-purpose evidence fixture.",
                    "- Must inspect: guard fixture place.",
                    "- Must preserve: user-purpose evidence semantics.",
                    "- Explicitly out of scope: target implementation.",
                    "- Unknown or requires discovery: none.",
                    "",
                    "### Residual Reconciliation",
                    "",
                    "- result-placement fixture residuals are not the tested behavior in this file.",
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
                    "### Batch 1: user-purpose evidence guard fixture",
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
                    "- Keep the user-purpose evidence guard fixture structurally ready.",
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
            "- Goal file: `yes`",
            "- Execution policy: `yes`",
            "- Who does the work / context use: `yes`",
            f"- User purpose evidence check: `{review_independence_pfb}`",
            "- Result placement check: `yes`",
            "- What counts as done check: `yes`",
            "- answer path check: `yes`",
            "- Work covered in this run and authority check: `yes`",
            "",
            "## Who Does The Work / Context Use",
            "",
            "Findings:",
            "- Reviewed work assignment and no Blocking/Major findings.",
            "",
        ]
        if include_review_pfb:
            review_parts.extend(
                [
                    "## User Purpose Evidence Check",
                    "",
                    "Classification:",
                    "",
                    "- Internally verified, user purpose evidence pending",
                    "",
                    "Findings:",
                    "- Internal checks are progress evidence; purpose achievement claim waits for purpose-limit feedback.",
                    "",
                ]
            )
        review_parts.extend(
            [
                "## Result Placement Check",
                "",
                "Classification:",
                "- result-placement adequate",
                "",
                "Findings:",
                "- Guard fixture includes result placement structure so user-purpose evidence tests isolate purpose-feedback behavior.",
                "",
                "## What Counts As Done Check",
                "",
                "Findings:",
                "- Done status is separate from not done report statuses.",
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

    def test_requirements_define_purpose_feedback_limit(self):
        skill = self.read(".agents/skills/analyzing-cybernetic-requirements/SKILL.md")
        template = self.read(
            ".agents/skills/analyzing-cybernetic-requirements/assets/requirements-analysis-template.md"
        )

        for text in (skill, template):
            self.assertIn("How We Know The User Purpose Was Met", text)
            self.assertIn("Human purpose", text)
            self.assertIn("Beneficiary / observer", text)
            self.assertIn("Purpose-realizing outcome", text)
            self.assertIn("Feedback needed", text)
            self.assertIn("Internal checks role", text)
            self.assertIn("Sufficient evidence level", text)
            self.assertIn("If feedback unavailable", text)
        self.assertNotIn("user-purpose evidence limit", skill.casefold())
        self.assertIn("beneficiary/observer", skill)
        self.assertIn("sufficient evidence level", skill)
        self.assertIn("If feedback unavailable", skill)

    def test_goal_separates_purpose_achievement_from_supporting_evidence_checks(self):
        skill = self.read(".agents/skills/writing-cybernetic-goals/SKILL.md")
        template = self.read(".agents/skills/writing-cybernetic-goals/assets/goal-contract-template.md")

        for text in (skill, template):
            self.assertIn("How We Know The User Purpose Was Met", text)
            self.assertIn("Purpose-realizing outcome observed", text)
            self.assertIn("Supporting Evidence", text)
            self.assertIn(
                "Do not define success as internal evidence check success unless the human purpose is internal-state correctness.",
                text,
            )

    def test_goal_final_report_uses_purpose_feedback_status(self):
        template = self.read(".agents/skills/writing-cybernetic-goals/assets/goal-contract-template.md")
        final_report = template.split("## Final Report Format", 1)[1]

        self.assertIn("- goal achieved: yes/no", final_report)
        for required in (
            "user purpose evidence status",
            "highest purpose-relevant evidence observed",
            "supporting internal/integration evidence",
            "not yet observed",
            "smallest next observation needed",
            "commands run",
            "files changed",
            "known residual risks",
        ):
            self.assertIn(required, final_report)

    def test_execution_policy_defines_purpose_feedback_strategy(self):
        skill = self.read(".agents/skills/writing-cybernetic-execution-policies/SKILL.md")
        template = self.read(
            ".agents/skills/writing-cybernetic-execution-policies/assets/execution-policy-template.md"
        )

        for text in (skill, template):
            self.assertIn("User Purpose Strategy", text)
            self.assertIn("Internal feedback", text)
            self.assertIn("Integration feedback", text)
            self.assertIn("User-purpose feedback", text)
            self.assertIn("Operational feedback", text)
            self.assertIn("Feedback cadence", text)
            self.assertIn("Evidence unavailable handling", text)
            self.assertIn("Allowed completion wording", text)

    def test_execution_policy_progress_log_records_purpose_feedback_status(self):
        template = self.read(
            ".agents/skills/writing-cybernetic-execution-policies/assets/execution-policy-template.md"
        )
        progress_log = template.split("## Progress Log Rules", 1)[1]

        for required in (
            "user purpose evidence status",
            "highest purpose-relevant evidence observed",
            "user purpose evidence not yet observed",
            "smallest next observation needed",
            "allowed completion wording",
        ):
            self.assertIn(required, progress_log)

    def test_review_classifies_purpose_feedback_adequacy(self):
        skill = self.read(".agents/skills/reviewing-cybernetic-control-structures/SKILL.md")
        template = self.read(
            ".agents/skills/reviewing-cybernetic-control-structures/assets/control-review-template.md"
        )

        for text in (skill, template):
            self.assertIn("User Purpose Evidence Check", text)
            self.assertIn("User purpose evidence adequate", text)
            self.assertIn("Internally verified, user purpose evidence pending", text)
            self.assertIn("Purpose partially observed", text)
            self.assertIn("User purpose evidence unavailable, honest handoff required", text)
            self.assertIn("Purpose-limit evidence not required, justified", text)
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
            self.assertIn("How We Know The User Purpose Was Met", text)
            self.assertIn("user purpose evidence status and highest purpose-relevant evidence observed", text)

        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            requirements = tmp / "requirements.md"
            goal = tmp / "goal.md"
            plan = tmp / "plan.md"
            review = tmp / "review.md"
            requirements.write_text(
                f"## Requirements Analysis Status\n\nStatus: `Complete`\n\n{USER_APPROVAL_FIXTURE}",
                encoding="utf-8",
            )
            goal.write_text("## Source Contracts\n\n- Requirements analysis: `requirements.md`\n", encoding="utf-8")
            plan.write_text("## Who Does The Work / Context Use\n\nWho does the work: `Main-only`\n", encoding="utf-8")
            review.write_text("## Review Status\n\nStatus: `Approved`\n", encoding="utf-8")
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
                    "--skip-guard",
                    "--i-understand-this-bypasses-phase-checks",
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
        self.assertIn("Execute the runtime goal file at", result.stdout)
        self.assertNotIn("highest purpose-relevant evidence actually observed", result.stdout)
        self.assertIn("How We Know The User Purpose Was Met", contract_text)
        self.assertIn("User Purpose Evidence Check", contract_text)
        self.assertIn("user purpose evidence status and highest purpose-relevant evidence observed", contract_text)

    def test_control_chain_guard_rejects_goal_missing_purpose_feedback_contract(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            requirements, goal, plan, review = self.write_guard_artifacts(
                Path(tmpdir),
                include_goal_pfb=False,
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
        self.assertIn("How We Know The User Purpose Was Met", output)

    def test_control_chain_guard_rejects_review_missing_purpose_feedback_adequacy(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            requirements, goal, plan, review = self.write_guard_artifacts(
                Path(tmpdir),
                include_review_pfb=False,
                review_independence_pfb="no",
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
        self.assertIn("User Purpose Evidence Check", output)
        self.assertIn("User purpose evidence check: yes", output)

    def test_purpose_feedback_evals_cover_false_completion_and_overcontrol(self):
        review_evals = json.loads(
            self.read(".agents/skills/reviewing-cybernetic-control-structures/evals/evals.json")
        )
        compiler_evals = json.loads(
            self.read(".agents/skills/compiling-cybernetic-runtime-goals/evals/evals.json")
        )

        review_ids = {item["id"] for item in review_evals["evals"]}
        compiler_ids = {item["id"] for item in compiler_evals["evals"]}

        self.assertIn("purpose-visible-outcome-cannot-be-claimed-from-internal-evidence-checks-only", review_ids)
        self.assertIn("internal-purpose-can-use-internal-feedback", review_ids)
        self.assertIn("runtime-calibrates-user-purpose-evidence-claims", compiler_ids)

    def test_invariant_matrix_tracks_purpose_feedback_limit(self):
        matrix = self.read("docs/cybernetic-framework/invariant-artifact-consumer-matrix.md")

        self.assertIn("INV-user-purpose evidence-001", matrix)
        self.assertIn("How We Know The User Purpose Was Met", matrix)
        self.assertIn("User Purpose Evidence Check", matrix)
        self.assertIn("goal How We Know The User Purpose Was Met", matrix)
        self.assertIn("review User Purpose Evidence Check section", matrix)
        self.assertIn("tests/skills/test_purpose_feedback_boundary.py", matrix)


if __name__ == "__main__":
    unittest.main()
