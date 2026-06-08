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
| Human purpose | keep realization surface guard fixtures focused on RSC behavior |
| Input role binding | test fixture source material is approved background |
| Primary object | realization surface guard fixture |
| Requested transformation | approved control chain to RSC guard checks |
| Non-goals | do not test HSA behavior in this fixture |
| Purpose Feedback Boundary | covered by compact fixture |
| Realization Surface Closure | dedicated test target |
| Output Contract | guard output |
| Workflow fit | full pre-goal guard fixture |
| Known assumptions | fixture-only assumptions |

Approval record:

- Approved by: `test fixture`
- Approval phrase or source: `approved fixture setpoint`
"""


class RealizationSurfaceClosureTest(unittest.TestCase):
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
            "| Purpose-realizing outcome observed | operator can observe the intended result |",
            "| Supporting Evidence | internal checks support progress only |",
            "| Sufficient evidence level | purpose-boundary |",
            "| Purpose feedback unavailable handling | report pending and next observation |",
            "| Allowed completion wording | pending until purpose feedback is observed |",
            "",
        ]
        if include_goal_rsc:
            rsc_rows = [
                "| Target state | target semantics are represented across realization surfaces |",
                "| Required surfaces | surface model, action classification, residual reconciliation |",
            ]
            if complete_goal_rsc_fields:
                rsc_rows.extend(
                    [
                        "| Surface actions | act / inspect / preserve / exclude / discover |",
                        "| Residual reconciliation | account for old state, unknown surfaces, exclusions, preserved surfaces, and remaining mismatches |",
                        "| RSC status wording | strongest target-realization claim requires RSC adequate |",
                        "| Partial/unavailable handling | report partial, missing, unavailable, or not applicable with justification |",
                        "| RSC / PFB boundary | RSC calibrates target-state and surface-closure claims while PFB calibrates human-purpose realization claims |",
                    ]
                )
            goal_parts.extend(["## Realization Surface Contract", "", "| Element | Requirement |", "|---|---|", *rsc_rows, ""])
        goal_parts.extend(
            [
                "## Completion Predicate Contract",
                "",
                "| Element | Requirement |",
                "|---|---|",
                "| Target-achieved predicate | target-producing evidence is observed |",
                "| Valid non-achieved report statuses | partial, diagnostic, blocked, invalid |",
                "| Fallback report handling | report honestly without claiming achieved |",
                "| Allowed goal-achieved claim | only target-achieved predicate supports goal achieved: yes |",
                "| CPF / PFB / RSC boundary | CPF calibrates completion claims; PFB calibrates purpose feedback; RSC calibrates target-state surface closure |",
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
        if include_plan_rsc:
            if plan_rsc_not_applicable:
                plan_parts.extend(
                    [
                        "## Realization Surface Closure Strategy",
                        "",
                        "- RSC status: `RSC not applicable with justification`",
                        "- Why no target-state surface closure is required: this fixture only checks runtime chain structure.",
                        "- Why no surface discovery / residual reconciliation is needed: no controlled-object target state is changed.",
                        "- Allowed target-realization wording: do not claim target-state realization; report RSC not applicable with justification.",
                        "",
                    ]
                )
            else:
                plan_parts.extend(
                    [
                        "## Realization Surface Closure Strategy",
                        "",
                        "### Surface Model",
                        "",
                        "| Surface | Role in target realization | Required action | Verification / reconciliation |",
                        "|---|---|---|---|",
                        "| controlled surfaces | carry target semantics | act / inspect | reconcile residual old state |",
                        "",
                        "### Surface Classes",
                        "",
                        "- Must act: controlled surfaces that must change.",
                        "- Must inspect: supporting surfaces that may retain old state.",
                        "- Must preserve: surfaces intentionally unchanged.",
                        "- Explicitly out of scope: excluded surfaces with reason.",
                        "- Unknown or requires discovery: surfaces needing runtime discovery.",
                        "",
                        "### Residual Reconciliation",
                        "",
                        "- Reconcile old state, unknown surfaces, exclusions, preserved surfaces, and remaining mismatches.",
                        "",
                    ]
                )
        plan_parts.extend(
            [
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
            "- Goal contract: `yes`",
            "- Execution policy: `yes`",
            "- Context management / execution topology: `yes`",
            "- Purpose feedback adequacy: `yes`",
            f"- Realization surface closure adequacy: `{review_independence_rsc}`",
            "- Completion predicate fidelity: `yes`",
            "",
            "## Context Management / Execution Topology",
            "",
            "Findings:",
            "- Reviewed selected topology and no Blocking/Major findings.",
            "",
            "## Purpose Feedback Adequacy",
            "",
            "Classification:",
            "- Internally verified, purpose feedback pending",
            "",
            "Findings:",
            "- Internal checks are progress evidence; purpose achievement claim waits for purpose-boundary feedback.",
            "",
        ]
        if include_review_rsc:
            review_parts.extend(
                [
                    "## Realization Surface Closure Adequacy",
                    "",
                    "Classification:",
                    "- RSC adequate",
                    "",
                    "Findings:",
                    "- Surface model, residual reconciliation, and target-realization wording were reviewed.",
                    "",
                ]
            )
        review_parts.extend(
            [
                "## Completion Predicate Fidelity",
                "",
                "Findings:",
                "- Target-achieved status is separate from fallback report statuses.",
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

    def test_requirements_define_realization_surface_closure_boundary(self):
        skill = self.read(".agents/skills/analyzing-cybernetic-requirements/SKILL.md")
        template = self.read(
            ".agents/skills/analyzing-cybernetic-requirements/assets/requirements-analysis-template.md"
        )

        for text in (skill, template):
            self.assertIn("Realization Surface Closure", text)
            self.assertIn("Target state", text)
            self.assertIn("Realization surfaces", text)
            self.assertIn("Required surface action", text)
            self.assertIn("Residual reconciliation", text)
            self.assertIn("RSC status", text)
            self.assertIn("RSC is distinct from Purpose Feedback Boundary", text)

        high_value_questions = skill.split("## Ask Only High-Value Human Questions", 1)[1].split(
            "## Output Contract Gate", 1
        )[0]
        self.assertIn("realization surface closure", high_value_questions)
        self.assertIn("target state surface model", high_value_questions)
        self.assertIn("required surface action", high_value_questions)
        self.assertIn("residual reconciliation", high_value_questions)
        self.assertIn("preserved/excluded surfaces", high_value_questions)

    def test_goal_preserves_rsc_contract_and_completion_wording(self):
        skill = self.read(".agents/skills/writing-cybernetic-goals/SKILL.md")
        template = self.read(".agents/skills/writing-cybernetic-goals/assets/goal-contract-template.md")

        self.assertIn("always for compiled runtime goals", skill)
        self.assertIn("RSC not applicable with justification", skill)
        for text in (skill, template):
            self.assertIn("Realization Surface Contract", text)
            self.assertIn("Target state", text)
            self.assertIn("Required surfaces", text)
            self.assertIn("RSC status wording", text)
            self.assertIn("strongest positive target-realization claim requires RSC adequate", text)
            self.assertIn("partial, missing, unavailable, or not applicable with justification", text)
            self.assertIn("RSC is distinct from Purpose Feedback Boundary", text)

    def test_execution_policy_defines_rsc_strategy(self):
        skill = self.read(".agents/skills/writing-cybernetic-execution-policies/SKILL.md")
        template = self.read(
            ".agents/skills/writing-cybernetic-execution-policies/assets/execution-policy-template.md"
        )

        for text in (skill, template):
            self.assertIn("Realization Surface Closure Strategy", text)
            self.assertIn("always include", text)
            self.assertIn("RSC not applicable with justification", text)
            self.assertIn("Surface Model", text)
            self.assertIn("Surface Classes", text)
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
            "RSC status",
            "surfaces acted on or inspected",
            "residuals and reconciliation",
            "allowed target-realization wording",
        ):
            self.assertIn(required, progress_log)

    def test_review_classifies_rsc_adequacy(self):
        skill = self.read(".agents/skills/reviewing-cybernetic-control-structures/SKILL.md")
        template = self.read(
            ".agents/skills/reviewing-cybernetic-control-structures/assets/control-review-template.md"
        )

        for text in (skill, template):
            self.assertIn("Realization Surface Closure Adequacy", text)
            self.assertIn("RSC adequate", text)
            self.assertIn("RSC partial", text)
            self.assertIn("RSC missing", text)
            self.assertIn("RSC unavailable", text)
            self.assertIn("RSC not applicable with justification", text)
            self.assertIn("local action is being treated as global target-state realization", text)

    def test_runtime_compiler_calibrates_rsc_completion_claims(self):
        skill = self.read(".agents/skills/compiling-cybernetic-runtime-goals/SKILL.md")
        template = self.read(
            ".agents/skills/compiling-cybernetic-runtime-goals/assets/runtime-goal-template.txt"
        )
        compiler = self.read(
            ".agents/skills/compiling-cybernetic-runtime-goals/scripts/compile_runtime_goal.py"
        )

        for text in (skill, template, compiler):
            self.assertIn(
                "Do not claim target-state realization from local action alone when Realization Surface Closure is required.",
                text,
            )
            self.assertIn(
                "Strongest positive target-realization claims require RSC adequate.",
                text,
            )
            self.assertIn(
                "surfaces covered, required surface actions completed or justified, residuals reconciled, pending or unknown surfaces, and smallest next reconciliation",
                text,
            )
        preconditions = skill.split("## Preconditions", 1)[1].split("## Runtime Goal Contract", 1)[0]
        self.assertIn("goal includes a compact `Purpose Feedback Contract`", preconditions)
        self.assertIn("control review records `Purpose feedback adequacy: yes`", preconditions)
        self.assertIn("goal includes a compact `Realization Surface Contract`", preconditions)
        self.assertIn("execution policy includes `Realization Surface Closure Strategy`", preconditions)
        self.assertIn("control review records `Realization surface closure adequacy: yes`", preconditions)

        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            requirements, goal, plan, review = self.write_guard_artifacts(tmp)
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
        self.assertIn("target-state realization", result.stdout)
        self.assertIn("RSC adequate", result.stdout)
        self.assertIn("surfaces covered", result.stdout)
        self.assertIn("required surface actions completed or justified", result.stdout)
        self.assertIn("smallest next reconciliation", result.stdout)

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
        self.assertIn("Realization Surface Contract", output)

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
        self.assertIn("goal Realization Surface Contract missing Surface actions", output)
        self.assertIn("goal Realization Surface Contract missing Residual reconciliation", output)
        self.assertIn("goal Realization Surface Contract missing RSC / PFB boundary", output)

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
        self.assertIn("Realization Surface Closure Strategy", output)

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
        self.assertIn("Realization Surface Closure Adequacy", output)
        self.assertIn("Realization surface closure adequacy: yes", output)

    def test_rsc_evals_cover_false_completion_and_not_applicable_justification(self):
        review_evals = json.loads(
            self.read(".agents/skills/reviewing-cybernetic-control-structures/evals/evals.json")
        )
        compiler_evals = json.loads(
            self.read(".agents/skills/compiling-cybernetic-runtime-goals/evals/evals.json")
        )

        review_ids = {item["id"] for item in review_evals["evals"]}
        compiler_ids = {item["id"] for item in compiler_evals["evals"]}

        self.assertIn("local-action-cannot-claim-target-realization-without-rsc", review_ids)
        self.assertIn("rsc-not-applicable-requires-justification", review_ids)
        self.assertIn("runtime-calibrates-realization-surface-closure-claims", compiler_ids)

    def test_invariant_matrix_tracks_realization_surface_closure(self):
        matrix = self.read("docs/cybernetic-framework/invariant-artifact-consumer-matrix.md")

        self.assertIn("INV-RSC-001", matrix)
        self.assertIn("Realization Surface Closure", matrix)
        self.assertIn("Realization Surface Closure Strategy", matrix)
        self.assertIn("Realization Surface Closure Adequacy", matrix)
        self.assertIn("execution policy RSC strategy", matrix)
        self.assertIn("tests/skills/test_realization_surface_closure.py", matrix)


if __name__ == "__main__":
    unittest.main()
