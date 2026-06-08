import json
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
| Human purpose | produce target-achieving evidence, not an alternate report status |
| Input role binding | fixture source material is approved background |
| Primary object | target achievement predicate fixture |
| Requested transformation | approved chain to TAP guard checks |
| Non-goals | do not create alternate success states |
| Purpose Feedback Boundary | purpose feedback remains separately calibrated |
| Realization Surface Closure | RSC remains separately calibrated |
| Single target-achieved predicate | target-producing evidence is observed |
| Target-producing evidence required | target-producing action runs or observation exists |
| Non-achieved terminal report handling | report goal achieved: no without creating alternate goals |
| Target-producing path | TAP guard fixture spine |
| Execution horizon | TAP guard fixture horizon |
| Runtime authority | local guard fixture checks |
| Forbidden live / irreversible actions | none |
| Required handling for unauthorized actions | none |
| Explicitly out-of-scope items | none |
| Output Contract | guard output |
| Workflow fit | full pre-goal guard fixture |
| Known assumptions | fixture-only assumptions |

Approval record:

- Approved by: `test fixture`
- Approval phrase or source: `approved target predicate`
"""


class TargetAchievementPredicateFidelityTest(unittest.TestCase):
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
            f"# Requirements\n\n## Requirements Analysis Status\n\nStatus: `Complete`\n\n{HSA_APPROVED}\n",
            encoding="utf-8",
        )

        success = success_condition or "\n".join(
            [
                "Codex may report `goal achieved: yes` only when:",
                "",
                "- Single target-achieved predicate in `Target Achievement Contract` is satisfied.",
                "- Required target-producing evidence is present.",
            ]
        )
        target_rows = [
            "| Single target-achieved predicate | target-producing evidence is observed |",
            "| Required target-producing evidence | target-producing action runs or observation exists |",
            "| Allowed achieved claim | `goal achieved: yes` only when the single predicate is met |",
            "| Target-producing spine | TAP guard fixture spine |",
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
                    "## Purpose Feedback Contract",
                    "",
                    "| Element | Requirement |",
                    "|---|---|",
                    "| Beneficiary / observer | operator |",
                    "| Purpose-realizing outcome observed | operator observes the target-achieving result |",
                    "| Supporting Evidence | internal checks support progress only |",
                    "| Sufficient evidence level | purpose-boundary |",
                    "| Purpose feedback unavailable handling | report pending and next observation |",
                    "| Allowed completion wording | achieved only with approved target evidence |",
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
                    *target_rows,
                    "",
                    "## Execution Horizon and Authority Contract",
                    "",
                    "| Element | Requirement |",
                    "|---|---|",
                    "| Approved horizon | TAP guard fixture horizon |",
                    "| Runtime-authorized actions | local guard fixture checks |",
                    "| Forbidden actions | none |",
                    "| Prepare-only / observe-only actions | none |",
                    "| Explicitly out-of-scope items | none |",
                    "| Horizon completion rule | every horizon item is accounted for in this fixture |",
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
            f"- Goal contract: `{goal}`",
            "",
            "## Horizon and Authority Coverage Matrix",
            "",
            "| Batch / surface | In approved horizon? | Runtime authority | Required runtime handling | Counts as achieved? |",
            "|---|---|---|---|---|",
            "| TAP guard fixture | yes | execute | run guard / compiler fixture checks | yes if fixture passes |",
            "",
            "## Target-Producing Spine",
            "",
            "| Spine node | Required state transition | Required evidence |",
            "|---|---|---|",
            "| S1 | fixture input -> TAP guard-ready chain | guard fixture files exist |",
            "",
        ]
        if include_plan_strategy:
            plan_parts.extend(
                [
                    "## Target-Producing Action Strategy",
                    "",
                    "Target-producing action required:",
                    "",
                    "- Run or observe the target-producing action before any achieved claim.",
                    "",
                    "Proof of impossibility, if any:",
                    "",
                    "- Record the environmental or dependency condition that proves the action cannot be attempted.",
                    "",
                    "Non-achieved terminal report rule:",
                    "",
                    "- A non-achieved terminal report may be produced only after the action is attempted and fails, or impossibility is proven.",
                    "",
                ]
            )
        plan_parts.extend(
            [
                "## Realization Surface Closure Strategy",
                "",
                "- RSC status: `RSC not applicable with justification`",
                "- Why no target-state surface closure is required: this fixture only checks TAP structure.",
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
                "## Candidate Plan Tasks",
                "",
                "### Batch 1: TAP guard fixture",
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
                "- Keep the TAP guard fixture structurally ready.",
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
            f"- Target achievement predicate fidelity: `{review_tap_independence}`",
            "- Target-producing spine fidelity: `yes`",
            "- Execution horizon and authority fidelity: `yes`",
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
        ]
        if include_review_tap:
            review_parts.extend(
                [
                    "## Target Achievement Predicate Fidelity",
                    "",
                    "Findings:",
                    "- The single target-achieved predicate is separated from non-achieved terminal reports.",
                    "",
                ]
            )
        review_parts.extend(
            [
                "## Target-Producing Spine Fidelity",
                "",
                "Findings:",
                "- Work packages map to the fixture spine node.",
                "",
                "## Execution Horizon and Authority Fidelity",
                "",
                "Findings:",
                "- Approved horizon and runtime authority are compact and fixture-bounded.",
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
            "Single target-achieved predicate",
            "Target-producing evidence required",
            "Target Achievement Contract",
            "Target-Producing Action Strategy",
            "Target Achievement Predicate Fidelity",
        ):
            self.assertIn(required, combined)

        for removed in (
            "Completion Predicate Contract",
            "Completion Predicate Strategy",
            "Completion Predicate Fidelity",
            "Valid non-achieved report statuses",
            "Fallback report handling",
            "Fallback report statuses",
            "fallback reason",
        ):
            self.assertNotIn(removed, combined)

        success_condition = self.read(
            ".agents/skills/writing-cybernetic-goals/assets/goal-contract-template.md"
        ).split("## Success Condition", 1)[1].split("## Purpose Feedback Contract", 1)[0]
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
        self.assertIn("non-achieved terminal report term", output)

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
        self.assertIn("Target Achievement Contract", output)
        self.assertIn("non-achieved or fallback term", output)

    def test_guard_rejects_target_contract_with_non_achieved_terminal_report_statuses(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            requirements, goal, plan, review = self.write_chain(
                Path(tmpdir),
                target_contract_extra=[
                    "| Non-achieved terminal report statuses | partial / blocked |",
                ],
            )
            result = self.guard(requirements, goal, plan, review)

        output = result.stdout + result.stderr
        self.assertEqual(2, result.returncode, output)
        self.assertIn("NEXT: RunGoalWriting", output)
        self.assertIn("Target Achievement Contract", output)
        self.assertIn("non-achieved or fallback term", output)

    def test_guard_rejects_multiple_target_achieved_predicates(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            requirements, goal, plan, review = self.write_chain(
                Path(tmpdir),
                target_contract_extra=[
                    "| Alternative target-achieved predicate | a lower-cost report exists |",
                ],
            )
            result = self.guard(requirements, goal, plan, review)

        output = result.stdout + result.stderr
        self.assertEqual(2, result.returncode, output)
        self.assertIn("NEXT: RunGoalWriting", output)
        self.assertIn("exactly one target-achieved predicate", output)

    def test_guard_rejects_plan_missing_target_producing_action_strategy(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            requirements, goal, plan, review = self.write_chain(Path(tmpdir), include_plan_strategy=False)
            result = self.guard(requirements, goal, plan, review)

        output = result.stdout + result.stderr
        self.assertEqual(2, result.returncode, output)
        self.assertIn("NEXT: RunExecutionPolicy", output)
        self.assertIn("Target-Producing Action Strategy", output)

    def test_guard_rejects_review_missing_target_achievement_predicate_fidelity(self):
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
        self.assertIn("Target Achievement Predicate Fidelity", output)
        self.assertIn("Target achievement predicate fidelity: yes", output)

    def test_runtime_compiler_uses_non_achieved_reason_not_fallback_reason(self):
        compiler = self.read(".agents/skills/compiling-cybernetic-runtime-goals/scripts/compile_runtime_goal.py")
        template = self.read(".agents/skills/compiling-cybernetic-runtime-goals/assets/runtime-goal-template.txt")
        skill = self.read(".agents/skills/compiling-cybernetic-runtime-goals/SKILL.md")

        for text in (compiler, template, skill):
            self.assertIn("single target-achieved predicate met: yes/no", text)
            self.assertIn("non-achieved reason", text)
            self.assertIn("target-producing action attempted or proof of impossibility", text)
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
        self.assertNotIn("single target-achieved predicate met: yes/no", result.stdout)
        self.assertIn("single target-achieved predicate met: yes/no", contract_text)
        self.assertIn("non-achieved reason", contract_text)
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
        self.assertIn("Runtime goal contract written:", result.stdout)
        self.assertIn("Use this /goal:", result.stdout)

        pointer = next(line for line in result.stdout.splitlines() if line.startswith("/goal "))
        self.assertLessEqual(len(pointer), 800, pointer)
        self.assertIn("Execute the runtime goal contract at", pointer)
        self.assertIn("docs/cybernetics/runtime-goals/fixture.goal.md", pointer)
        self.assertNotIn("Purpose Feedback Boundary", pointer)
        self.assertNotIn("Realization Surface Closure", pointer)
        self.assertNotIn("single target-achieved predicate met", pointer)
        self.assertNotIn("subagent outputs are candidate results", pointer.casefold())

        self.assertIn("## Approved Control Chain", contract_text)
        self.assertIn(str(requirements), contract_text)
        self.assertIn(str(goal), contract_text)
        self.assertIn(str(plan), contract_text)
        self.assertIn(str(review), contract_text)
        self.assertIn("## Required Sections To Read", contract_text)
        self.assertIn("Human Setpoint Approval", contract_text)
        self.assertIn("Target Achievement Contract", contract_text)
        self.assertIn("Purpose Feedback Contract", contract_text)
        self.assertIn("Realization Surface Contract", contract_text)
        self.assertIn("Target-Producing Action Strategy", contract_text)
        self.assertIn("Context Management / Execution Topology", contract_text)
        self.assertIn("Target Achievement Predicate Fidelity", contract_text)
        self.assertIn("Purpose Feedback Adequacy", contract_text)
        self.assertIn("Realization Surface Closure Adequacy", contract_text)
        self.assertIn("Final Observer Check", contract_text)
        self.assertIn("goal achieved: yes/no", contract_text)
        self.assertIn("single target-achieved predicate met: yes/no", contract_text)
        self.assertIn("smallest next target-producing attempt", contract_text)

    def test_matrix_and_evals_track_tap_invariant(self):
        matrix = self.read("docs/cybernetic-framework/invariant-artifact-consumer-matrix.md")
        review_evals = json.loads(self.read(".agents/skills/reviewing-cybernetic-control-structures/evals/evals.json"))
        compiler_evals = json.loads(self.read(".agents/skills/compiling-cybernetic-runtime-goals/evals/evals.json"))

        self.assertIn("INV-TAP-001", matrix)
        self.assertIn("Target Achievement Predicate Fidelity", matrix)
        self.assertIn("tests/skills/test_target_achievement_predicate_fidelity.py", matrix)
        self.assertNotIn("INV-CPF-001", matrix)

        review_ids = {item["id"] for item in review_evals["evals"]}
        compiler_ids = {item["id"] for item in compiler_evals["evals"]}
        self.assertIn("non-achieved-terminal-report-cannot-be-target-achieved", review_ids)
        self.assertIn("target-contract-cannot-contain-alternate-report-statuses", review_ids)
        self.assertIn("runtime-calibrates-target-achievement-predicate-claims", compiler_ids)


if __name__ == "__main__":
    unittest.main()
