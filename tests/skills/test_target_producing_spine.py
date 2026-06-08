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
| Human purpose | produce a target state through an actor-centered path |
| Input role binding | fixture source material is approved background |
| Primary object | target-producing spine fixture |
| Requested transformation | approved target into spine-first execution policy |
| Non-goals | do not count component-only work as goal progress |
| Purpose Feedback Boundary | purpose feedback remains separately calibrated |
| Realization Surface Closure | RSC remains separately calibrated |
| Single target-achieved predicate | all required spine transitions are satisfied |
| Target-producing evidence required | spine transition evidence exists |
| Non-achieved terminal report handling | report goal achieved: no when spine transitions are unsatisfied |
| Target-producing path | S0 no durable state -> S1 durable state -> S2 observable target state |
| Execution horizon | target-producing spine fixture horizon |
| Runtime authority | local guard fixture checks |
| Forbidden live / irreversible actions | none |
| Required handling for unauthorized actions | none |
| Explicitly out-of-scope items | none |
| Output Contract | guard output |
| Workflow fit | full pre-goal guard fixture |
| Known assumptions | fixture-only assumptions |

Approval record:

- Approved by: `test fixture`
- Approval phrase or source: `approved target-producing spine`
"""


class TargetProducingSpineTest(unittest.TestCase):
    def read(self, path: str) -> str:
        return (ROOT / path).read_text(encoding="utf-8")

    def write_chain(
        self,
        tmp: Path,
        *,
        include_goal_spine: bool = True,
        include_plan_spine: bool = True,
        include_candidate_spine_nodes: bool = True,
        include_review_spine: bool = True,
        review_spine_independence: str = "yes",
    ) -> tuple[Path, Path, Path, Path]:
        requirements = tmp / "requirements.md"
        goal = tmp / "goal.md"
        plan = tmp / "plan.md"
        review = tmp / "review.md"

        requirements.write_text(
            f"# Requirements\n\n## Requirements Analysis Status\n\nStatus: `Complete`\n\n{HSA_APPROVED}\n",
            encoding="utf-8",
        )

        target_rows = [
            "| Single target-achieved predicate | all required spine transitions are satisfied |",
            "| Required target-producing evidence | spine transition evidence exists |",
            "| Allowed achieved claim | goal achieved: yes only when all required spine transitions are satisfied |",
        ]
        if include_goal_spine:
            target_rows.append("| Target-producing spine | S1 and S2 transitions in the execution policy Target-Producing Spine |")

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
                    "Codex may report `goal achieved: yes` only when the single target-achieved predicate is satisfied.",
                    "",
                    "## Purpose Feedback Contract",
                    "",
                    "| Element | Requirement |",
                    "|---|---|",
                    "| Beneficiary / observer | operator |",
                    "| Purpose-realizing outcome observed | operator observes the target-producing path completed |",
                    "| Supporting Evidence | internal checks support progress only |",
                    "| Sufficient evidence level | purpose-boundary |",
                    "| Purpose feedback unavailable handling | report pending and next observation |",
                    "| Allowed completion wording | achieved only when spine transitions are satisfied |",
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
                    "| Approved horizon | target-producing spine fixture horizon |",
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
            "| target-producing spine fixture | yes | execute | run guard / compiler fixture checks | yes if fixture passes |",
            "",
        ]
        if include_plan_spine:
            plan_parts.extend(
                [
                    "## Target-Producing Spine",
                    "",
                    "| Spine node | Required state transition | Required evidence |",
                    "|---|---|---|",
                    "| S1 | no durable state -> durable state exists | durable state id is recorded |",
                    "| S2 | durable state exists -> observable target state | target observation references durable state id |",
                    "",
                ]
            )
        plan_parts.extend(
            [
                "## Target-Producing Action Strategy",
                "",
                "Target-producing action required:",
                "",
                "- Satisfy S1 and S2 spine transitions before any achieved claim.",
                "",
                "Proof of impossibility, if any:",
                "",
                "- Record the condition proving a spine transition cannot be attempted.",
                "",
                "Non-achieved terminal report rule:",
                "",
                "- A non-achieved report may be produced only after the transition is attempted and fails, or impossibility is proven.",
                "",
                "## Realization Surface Closure Strategy",
                "",
                "- RSC status: `RSC not applicable with justification`",
                "- Why no target-state surface closure is required: this fixture only checks TPS structure.",
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
                "## Candidate Plan Tasks",
                "",
                "### Batch 1: satisfy spine fixture",
                "",
            ]
        )
        if include_candidate_spine_nodes:
            plan_parts.extend(
                [
                    "Spine node(s):",
                    "",
                    "- S1",
                    "- S2",
                    "",
                ]
            )
        plan_parts.extend(
            [
                "Goal:",
                "",
                "- Drive the fixture through the approved target-producing spine.",
                "",
                "Batch-end gate:",
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
            "- Human setpoint fidelity: `yes`",
            "- Goal contract: `yes`",
            "- Execution policy: `yes`",
            "- Context management / execution topology: `yes`",
            "- Purpose feedback adequacy: `yes`",
            "- Realization surface closure adequacy: `yes`",
            "- Target achievement predicate fidelity: `yes`",
            f"- Target-producing spine fidelity: `{review_spine_independence}`",
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
            "## Target Achievement Predicate Fidelity",
            "",
            "Findings:",
            "- The single target-achieved predicate is separated from non-achieved terminal reports.",
            "",
        ]
        if include_review_spine:
            review_parts.extend(
                [
                    "## Target-Producing Spine Fidelity",
                    "",
                    "Findings:",
                    "- Work packages are mapped to S1/S2 spine transitions and supporting-only work cannot satisfy goal progress by itself.",
                    "",
                ]
            )
        review_parts.extend(
            [
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

    def test_templates_include_target_producing_spine(self):
        requirements = self.read(".agents/skills/analyzing-cybernetic-requirements/assets/requirements-analysis-template.md")
        goal = self.read(".agents/skills/writing-cybernetic-goals/assets/goal-contract-template.md")
        plan = self.read(".agents/skills/writing-cybernetic-execution-policies/assets/execution-policy-template.md")
        review = self.read(".agents/skills/reviewing-cybernetic-control-structures/assets/control-review-template.md")

        self.assertIn("Target-producing path", requirements)
        self.assertIn("Target-producing spine", goal)
        self.assertIn("Target-Producing Spine", plan)
        self.assertIn("Spine node(s)", plan)
        self.assertIn("Target-Producing Spine Fidelity", review)
        self.assertIn("Target-producing spine fidelity", review)

    def test_guard_accepts_complete_target_producing_spine_chain(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            requirements, goal, plan, review = self.write_chain(Path(tmpdir))
            result = self.guard(requirements, goal, plan, review)

        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn("NEXT: CompileRuntimeGoal", result.stdout)

    def test_guard_rejects_goal_missing_target_producing_spine_reference(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            requirements, goal, plan, review = self.write_chain(Path(tmpdir), include_goal_spine=False)
            result = self.guard(requirements, goal, plan, review)

        output = result.stdout + result.stderr
        self.assertEqual(2, result.returncode, output)
        self.assertIn("NEXT: RunGoalWriting", output)
        self.assertIn("Target-producing spine", output)

    def test_guard_rejects_plan_missing_target_producing_spine(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            requirements, goal, plan, review = self.write_chain(Path(tmpdir), include_plan_spine=False)
            result = self.guard(requirements, goal, plan, review)

        output = result.stdout + result.stderr
        self.assertEqual(2, result.returncode, output)
        self.assertIn("NEXT: RunExecutionPolicy", output)
        self.assertIn("Target-Producing Spine", output)

    def test_guard_rejects_candidate_task_without_spine_nodes(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            requirements, goal, plan, review = self.write_chain(Path(tmpdir), include_candidate_spine_nodes=False)
            result = self.guard(requirements, goal, plan, review)

        output = result.stdout + result.stderr
        self.assertEqual(2, result.returncode, output)
        self.assertIn("NEXT: RunExecutionPolicy", output)
        self.assertIn("Spine node(s)", output)

    def test_guard_rejects_review_missing_spine_fidelity(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            requirements, goal, plan, review = self.write_chain(
                Path(tmpdir),
                include_review_spine=False,
                review_spine_independence="no",
            )
            result = self.guard(requirements, goal, plan, review)

        output = result.stdout + result.stderr
        self.assertEqual(2, result.returncode, output)
        self.assertIn("NEXT: RunReview", output)
        self.assertIn("Target-Producing Spine Fidelity", output)
        self.assertIn("Target-producing spine fidelity: yes", output)

    def test_runtime_contract_indexes_target_producing_spine(self):
        compiler = self.read(".agents/skills/compiling-cybernetic-runtime-goals/scripts/compile_runtime_goal.py")
        template = self.read(".agents/skills/compiling-cybernetic-runtime-goals/assets/runtime-goal-template.txt")
        skill = self.read(".agents/skills/compiling-cybernetic-runtime-goals/SKILL.md")

        for text in (compiler, template, skill):
            self.assertIn("Target-Producing Spine", text)
            self.assertIn("Target-Producing Spine Fidelity", text)

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
        self.assertIn("Target-Producing Spine", contract_text)
        self.assertIn("Target-Producing Spine Fidelity", contract_text)

    def test_progress_log_rules_track_spine_node_status(self):
        template = self.read(".agents/skills/writing-cybernetic-execution-policies/assets/execution-policy-template.md")
        progress_log = template.split("## Progress Log Rules", 1)[1]

        self.assertIn("target-producing spine node status", progress_log)
        self.assertIn("spine transitions satisfied", progress_log)
        self.assertIn("spine transitions failed / blocked / unobserved", progress_log)
        self.assertIn("supporting-only work completed", progress_log)
        self.assertIn("supporting-only work not counted as goal progress", progress_log)


if __name__ == "__main__":
    unittest.main()
