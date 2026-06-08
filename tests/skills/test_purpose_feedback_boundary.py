import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

HSA_FIXTURE = """## What the User Approved

Status: `Approved`

| Element | Commitment |
|---|---|
| Human purpose | keep purpose feedback guard fixtures focused on PFB behavior |
| Input role binding | test fixture source material is approved background |
| Primary object | purpose feedback guard fixture |
| Requested transformation | approved control chain to PFB guard checks |
| Non-goals | do not test HSA behavior in this fixture |
| Purpose Feedback Boundary | dedicated test target |
| Realization Surface Closure | covered by compact fixture |
| What counts as done | purpose-boundary evidence is observed |
| Evidence needed to call it done | target-producing evidence is observed |
| Non-achieved terminal report handling | report goal achieved: no |
| Required answer path | PFB guard fixture spine |
| Work covered in this run | PFB guard fixture horizon |
| What the agent may do | local guard fixture checks |
| Forbidden live / irreversible actions | none |
| Required handling for unauthorized actions | none |
| Explicitly out-of-scope items | none |
| Output Contract | guard output |
| Workflow fit | full pre-goal guard fixture |
| Known assumptions | fixture-only assumptions |

Approval record:

- Approved by: `test fixture`
- Approval phrase or source: `approved fixture setpoint`
"""


class PurposeFeedbackBoundaryTest(unittest.TestCase):
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
            "## Success Condition",
            "",
            "Codex may report `goal achieved: yes` only when the single target-achieved predicate is satisfied.",
            "",
            "- Required target-producing evidence is present.",
            "",
        ]
        if include_goal_pfb:
            goal_parts.extend(
                [
                    "## Purpose Feedback Contract",
                    "",
                    "| Element | Requirement |",
                    "|---|---|",
                    "| Beneficiary / observer | operator |",
                    "| Purpose-realizing outcome observed | operator can observe the intended result |",
                    "| Supporting Evidence | internal checks support progress only |",
                    "| Sufficient evidence level | purpose-boundary |",
                    "| Purpose feedback unavailable handling | report pending and next observation |",
                    "| Allowed completion wording | pending until purpose feedback is observed |",
                    "",
                ]
            )
        goal_parts.extend(
            [
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
                "## Target Achievement Contract",
                "",
                "| Element | Requirement |",
                "|---|---|",
                "| What counts as done | purpose-boundary evidence is observed |",
                    "| Required target-producing evidence | target-producing evidence is observed |",
                "| Allowed achieved claim | only target-achieved predicate supports goal achieved: yes |",
                "| Steps that make the result true | PFB guard fixture spine |",
                "",
                "## Work Covered And Allowed Actions Contract",
                "",
                "| Element | Requirement |",
                "|---|---|",
                "| Approved horizon | PFB guard fixture horizon |",
                "| Runtime-authorized actions | local guard fixture checks |",
                "| Forbidden actions | none |",
                "| Prepare-only / observe-only actions | none |",
                "| Explicitly out-of-scope items | none |",
                "| Horizon completion rule | every horizon item is accounted for in this fixture |",
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
                    "## Work Coverage And Action Limits Matrix",
                    "",
                    "| Batch / surface | In approved horizon? | What the agent may do | Required runtime handling | Counts as achieved? |",
                    "|---|---|---|---|---|",
                    "| PFB guard fixture | yes | execute | run guard / compiler fixture checks | yes if fixture passes |",
                    "",
                    "## Steps That Make The Result True",
                    "",
                    "| Spine node | Required state transition | Required evidence |",
                    "|---|---|---|",
                    "| S1 | fixture input -> PFB guard-ready chain | guard fixture files exist |",
                    "",
                    "## Target-Producing Action Strategy",
                    "",
                    "Target-producing action required:",
                    "",
                    "- Run or observe the target-producing action before any achieved claim.",
                    "",
                    "Proof of impossibility, if any:",
                    "",
                    "- Record the condition proving the action cannot be attempted.",
                    "",
                    "Non-achieved terminal report rule:",
                    "",
                    "- A non-achieved report may be produced only after the action is attempted and fails, or impossibility is proven.",
                    "",
                    "## Realization Surface Closure Strategy",
                    "",
                    "### Surface Model",
                    "",
                    "| Surface | Role in target realization | Required action | Verification / reconciliation |",
                    "|---|---|---|---|",
                    "| guard fixture surface | carries fixture target state | inspect | reconcile residuals in fixture scope |",
                    "",
                    "### Surface Classes",
                    "",
                    "- Must act: none for PFB fixture.",
                    "- Must inspect: guard fixture surface.",
                    "- Must preserve: PFB semantics.",
                    "- Explicitly out of scope: target implementation.",
                    "- Unknown or requires discovery: none.",
                    "",
                    "### Residual Reconciliation",
                    "",
                    "- RSC fixture residuals are not the tested behavior in this file.",
                    "",
                    "## Context Management / Execution Topology",
                    "",
                    "Task level: `Level 2`",
                    "",
                    "Selected topology: `Main-only`",
                    "",
                    "Selected agent workflow: `none`",
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
                    "## Candidate Plan Tasks",
                    "",
                    "### Batch 1: PFB guard fixture",
                    "",
                    "Spine node(s):",
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
                    "- Fixture target-producing evidence is recorded.",
                    "",
                    "Integration gate:",
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
                    "- Keep the PFB guard fixture structurally ready.",
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
            "- Goal contract: `yes`",
            "- Execution policy: `yes`",
            "- Context management / execution topology: `yes`",
            f"- Purpose feedback adequacy: `{review_independence_pfb}`",
            "- Realization surface closure adequacy: `yes`",
            "- Target achievement predicate fidelity: `yes`",
            "- answer path check: `yes`",
            "- Work covered in this run and authority fidelity: `yes`",
            "",
            "## Context Management / Execution Topology",
            "",
            "Findings:",
            "- Reviewed selected topology and no Blocking/Major findings.",
            "",
        ]
        if include_review_pfb:
            review_parts.extend(
                [
                    "## Purpose Feedback Adequacy",
                    "",
                    "Classification:",
                    "",
                    "- Internally verified, purpose feedback pending",
                    "",
                    "Findings:",
                    "- Internal checks are progress evidence; purpose achievement claim waits for purpose-boundary feedback.",
                    "",
                ]
            )
        review_parts.extend(
            [
                "## Realization Surface Closure Adequacy",
                "",
                "Classification:",
                "- RSC adequate",
                "",
                "Findings:",
                "- Guard fixture includes RSC structure so PFB tests isolate purpose-feedback behavior.",
                "",
                "## Target Achievement Predicate Fidelity",
                "",
                "Findings:",
                "- Target-achieved status is separate from non-achieved report statuses.",
                "",
                "## Answer Path Check",
                "",
                "Findings:",
                "- Work packages map to the fixture spine node.",
                "",
                "## Work Covered And Allowed Actions Check",
                "",
                "Findings:",
                "- Approved horizon and runtime authority are compact and fixture-bounded.",
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

    def test_requirements_define_purpose_feedback_boundary(self):
        skill = self.read(".agents/skills/analyzing-cybernetic-requirements/SKILL.md")
        template = self.read(
            ".agents/skills/analyzing-cybernetic-requirements/assets/requirements-analysis-template.md"
        )

        for text in (skill, template):
            self.assertIn("Purpose Feedback Boundary", text)
            self.assertIn("Human purpose", text)
            self.assertIn("Beneficiary / observer", text)
            self.assertIn("Purpose-realizing outcome", text)
            self.assertIn("Feedback needed", text)
            self.assertIn("Internal sensors role", text)
            self.assertIn("Sufficient evidence level", text)
            self.assertIn("If feedback unavailable", text)
        self.assertIn("purpose feedback boundary", skill.casefold())
        self.assertIn("beneficiary/observer", skill)
        self.assertIn("sufficient evidence level", skill)
        self.assertIn("feedback-unavailable handling", skill)

    def test_goal_separates_purpose_achievement_from_supporting_sensors(self):
        skill = self.read(".agents/skills/writing-cybernetic-goals/SKILL.md")
        template = self.read(".agents/skills/writing-cybernetic-goals/assets/goal-contract-template.md")

        for text in (skill, template):
            self.assertIn("Purpose Feedback Contract", text)
            self.assertIn("Purpose-realizing outcome observed", text)
            self.assertIn("Supporting Evidence", text)
            self.assertIn(
                "Do not define success as internal sensor success unless the human purpose is internal-state correctness.",
                text,
            )

    def test_goal_final_report_uses_purpose_feedback_status(self):
        template = self.read(".agents/skills/writing-cybernetic-goals/assets/goal-contract-template.md")
        final_report = template.split("## Final Report Format", 1)[1]

        self.assertIn("- goal achieved: yes/no", final_report)
        for required in (
            "purpose feedback status",
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
            self.assertIn("Purpose Feedback Strategy", text)
            self.assertIn("Internal feedback", text)
            self.assertIn("Integration feedback", text)
            self.assertIn("Purpose-boundary feedback", text)
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
            "purpose feedback status",
            "highest purpose-relevant evidence observed",
            "purpose feedback not yet observed",
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
            self.assertIn("Purpose Feedback Adequacy", text)
            self.assertIn("Purpose feedback adequate", text)
            self.assertIn("Internally verified, purpose feedback pending", text)
            self.assertIn("Purpose partially observed", text)
            self.assertIn("Purpose feedback unavailable, honest handoff required", text)
            self.assertIn("Purpose-boundary evidence not required, justified", text)
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
            self.assertIn("Purpose Feedback", text)
            self.assertIn("purpose feedback status and highest purpose-relevant evidence observed", text)

        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            requirements = tmp / "requirements.md"
            goal = tmp / "goal.md"
            plan = tmp / "plan.md"
            review = tmp / "review.md"
            requirements.write_text(
                f"## Requirements Analysis Status\n\nStatus: `Complete`\n\n{HSA_FIXTURE}",
                encoding="utf-8",
            )
            goal.write_text("## Source Contracts\n\n- Requirements analysis: `requirements.md`\n", encoding="utf-8")
            plan.write_text("## Context Management / Execution Topology\n\nSelected topology: `Main-only`\n", encoding="utf-8")
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
                    "--i-understand-this-bypasses-phase-gates",
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
        self.assertIn("Execute the runtime goal contract at", result.stdout)
        self.assertNotIn("highest purpose-relevant evidence actually observed", result.stdout)
        self.assertIn("Purpose Feedback Contract", contract_text)
        self.assertIn("Purpose Feedback Adequacy", contract_text)
        self.assertIn("purpose feedback status and highest purpose-relevant evidence observed", contract_text)

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
        self.assertIn("Purpose Feedback Contract", output)

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
        self.assertIn("Purpose Feedback Adequacy", output)
        self.assertIn("Purpose feedback adequacy: yes", output)

    def test_purpose_feedback_evals_cover_false_completion_and_overcontrol(self):
        review_evals = json.loads(
            self.read(".agents/skills/reviewing-cybernetic-control-structures/evals/evals.json")
        )
        compiler_evals = json.loads(
            self.read(".agents/skills/compiling-cybernetic-runtime-goals/evals/evals.json")
        )

        review_ids = {item["id"] for item in review_evals["evals"]}
        compiler_ids = {item["id"] for item in compiler_evals["evals"]}

        self.assertIn("purpose-visible-outcome-cannot-be-claimed-from-internal-sensors-only", review_ids)
        self.assertIn("internal-purpose-can-use-internal-feedback", review_ids)
        self.assertIn("runtime-calibrates-purpose-feedback-claims", compiler_ids)

    def test_invariant_matrix_tracks_purpose_feedback_boundary(self):
        matrix = self.read("docs/cybernetic-framework/invariant-artifact-consumer-matrix.md")

        self.assertIn("INV-PFB-001", matrix)
        self.assertIn("Purpose Feedback Boundary", matrix)
        self.assertIn("Purpose Feedback Adequacy", matrix)
        self.assertIn("goal Purpose Feedback Contract", matrix)
        self.assertIn("review Purpose Feedback Adequacy section", matrix)
        self.assertIn("tests/skills/test_purpose_feedback_boundary.py", matrix)


if __name__ == "__main__":
    unittest.main()
