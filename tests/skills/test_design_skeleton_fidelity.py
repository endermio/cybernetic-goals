import subprocess
import sys
import tempfile
import unittest
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
ORCHESTRATION_GUARD = ROOT / ".agents/skills/orchestrating-cybernetic-pregoal/scripts/orchestration_guard.py"
CONTROL_CHAIN_GUARD = ROOT / ".agents/skills/compiling-cybernetic-runtime-goals/scripts/control_chain_guard.py"
COMPILER = ROOT / ".agents/skills/compiling-cybernetic-runtime-goals/scripts/compile_runtime_goal.py"


USER_APPROVAL_WITH_COVERAGE_PATH = """## What the User Approved

Status: `Approved`

| Element | Commitment |
|---|---|
| Human purpose | measure the complete end-to-end workflow performance ceiling |
| Input role binding | prior partial results are source material, not the final answer |
| Primary object | full workflow ceiling measurement |
| Requested transformation | full workflow scope and bottleneck inventory into a ceiling measurement |
| Non-goals | do not validate only one full-workflow candidate path |
| How We Know The User Purpose Was Met | purpose is realized only when the full workflow ceiling is answered |
| Where The Result Must Show Up | measurement result_places must cover the workflow evidence bundle |
| What counts as done | full workflow ceiling coverage answer path is satisfied |
| Evidence needed to call it done | scope inventory, removable-source inventory, coverage criterion, coverage matrix, full workflow run, and interpretation against coverage |
| Non-achieved terminal report handling | report goal achieved: no when coverage answer path is unsatisfied |
| Required answer path | coverage inventory -> coverage criterion -> candidate coverage matrix -> same-workload run -> interpretation |
| How this should be answered | list full workflow scope, identify major removable sources, define ceiling coverage, prove candidate coverage, run full workflow, and interpret against coverage |
| What is not enough | only running one full-workflow candidate path and passing same-workload checks |
| Work covered in this run | full workflow ceiling measurement horizon |
| What the agent may do | local measurement and report generation |
| Forbidden live / irreversible actions | none |
| Required handling for unauthorized actions | none |
| Explicitly out-of-scope items | none |
| Agent delegation preference | no preference |
| Agent workflow preference | no preference |
| Parallel execution authority | not applicable |
| Maximum parallel agents | not specified |
| Final Answer Format | guard output |
| Why this process is needed | full pre-goal orchestration required |
| Known assumptions | fixture assumptions only |

Approval record:

- Approved by: `test fixture`
- Approval phrase or source: `approved coverage ceiling answering method`
"""


def write_requirements(
    tmp: Path,
    *,
    control_sidecar: bool = True,
    answer_method_key: str = "coverage-ceiling-measurement",
    forbidden_substitute_key: str = "full-workflow-run-validation",
) -> Path:
    requirements = tmp / "requirements.md"
    requirements.write_text(
        "\n".join(
            [
                "# Requirements",
                "",
                "## Requirements Analysis Status",
                "",
                "Status: `Complete`",
                "",
                "## Required Checks",
                "",
                "| Check | Status | Reason |",
                "|---|---|---|",
                "| required design | required | coverage answer path must be designed |",
                "",
                USER_APPROVAL_WITH_COVERAGE_PATH,
                "",
            ]
        ),
        encoding="utf-8",
    )
    if control_sidecar:
        (tmp / "requirements.control.json").write_text(
            json.dumps(
                {
                    "answer_method_key": answer_method_key,
                    "forbidden_substitute_key": forbidden_substitute_key,
                },
                indent=2,
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
        )
    return requirements


def write_design(tmp: Path, requirements: Path, *, answer_path: str, mandatory_nodes: list[str], substitution_avoided: str) -> Path:
    design = tmp / "design.md"
    design.write_text(
        "\n".join(
            [
                "# Design",
                "",
                "## Design Status",
                "",
                "Status: `Candidate`",
                "",
                "## Source Contracts",
                "",
                f"- Requirements analysis: `{requirements}`",
                "",
                "## Human Purpose",
                "",
                "Measure the complete workflow ceiling.",
                "",
                "## Confirmed Meaning",
                "",
                "Preserve the approved answering method.",
                "",
                "## Answer Method Check",
                "",
                "| Element | Design |",
                "|---|---|",
                "| Approved answer method | list full workflow scope, identify major removable sources, define ceiling coverage, prove candidate coverage, run full workflow, and interpret against coverage |",
                f"| Required answer path | {answer_path} |",
                f"| Required steps covered | {', '.join(mandatory_nodes)} |",
                f"| What is not enough avoided | {substitution_avoided} |",
                "",
                "## Required Answer Path",
                "",
                "| Required step | Required change or answer step | Required evidence | Completion condition |",
                "|---|---|---|---|",
                "| S1 | scope -> covered | evidence | complete |",
                "",
                "## What Supports Each Required Step",
                "",
                "| Required step | Required support object/component/mechanism | Why needed | Evidence produced |",
                "|---|---|---|---|",
                "| S1 | fixture mechanism | fixture reason | fixture evidence |",
                "",
                "## Design Details Tied To Required Steps",
                "",
                "### Components / Mechanisms",
                "",
                "| Component / Mechanism | Required answer step supported | Mainline or supporting-only | Responsibility | Inputs | Outputs | Evidence produced |",
                "|---|---|---|---|---|---|---|",
                "| fixture mechanism | S1 | mainline | fixture | input | output | evidence |",
                "",
                "## Open Design Questions",
                "",
                "- None",
                "",
            ]
        ),
        encoding="utf-8",
    )
    return design


def write_runtime_chain(
    tmp: Path,
    *,
    include_review_design_answer_path: bool = True,
    review_design_answer_path_independence: str = "yes",
) -> tuple[Path, Path, Path, Path, Path]:
    requirements = write_requirements(tmp)
    design = write_design(
        tmp,
        requirements,
        answer_path="scope inventory -> removable-source inventory -> coverage criterion -> candidate coverage matrix -> same-workload run -> interpretation",
        mandatory_nodes=[
            "full workflow scope inventory",
            "major removable source inventory",
            "ceiling coverage criterion",
            "candidate coverage matrix",
            "same-workload full workflow run",
            "interpretation against coverage matrix",
        ],
        substitution_avoided="yes, the insufficient one-candidate run-validation answer is not used",
    )
    goal = tmp / "goal.md"
    plan = tmp / "plan.md"
    review = tmp / "review.md"

    goal.write_text(
        "\n".join(
            [
                "# Goal",
                "",
                "## Source Contracts",
                "",
                f"- Requirements analysis: `{requirements}`",
                f"- Solution design: `{design}`",
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
                "| Purpose-realizing outcome observed | operator observes the full workflow ceiling answer |",
                "| Supporting Evidence | internal checks support progress only |",
                "| Sufficient evidence level | user-purpose |",
                "| If user-purpose evidence unavailable | report pending and next observation |",
                "| Allowed completion wording | achieved only when the coverage answer path is satisfied |",
                "",
                "## Where The Result Must Show Up",
                "",
                "| Element | Requirement |",
                "|---|---|",
                "| Target state | measurement answer state |",
                "| Required result places | scope inventory, source inventory, coverage criterion, coverage matrix, run, interpretation |",
                "| Place actions | act / inspect / preserve / exclude / discover |",
                "| Residual reconciliation | account for old state, unknown result_places, exclusions, preserved result_places, and remaining mismatches |",
                "| Result-placement wording | strongest result claim claim requires result-placement adequate |",
                "| Partial/unavailable handling | report goal achieved: no without result claim claim |",
                "| Distinction from user-purpose evidence | result placement calibrates answer-result_place completion while user-purpose evidence calibrates human-purpose realization |",
                "",
                "## What Counts As Done",
                "",
                "| Element | Requirement |",
                "|---|---|",
                "| What counts as done | the full workflow ceiling answer path is satisfied |",
                "| Evidence needed to call it done | scope inventory, source inventory, coverage criterion, coverage matrix, full workflow run, and interpretation evidence exist |",
                "| Allowed achieved claim | goal achieved: yes only when the full workflow ceiling answer path is satisfied |",
                "| Steps that make the result true | coverage inventory -> criterion -> matrix -> same-workload run -> interpretation |",
                "",
                "## Work Covered And Allowed Actions Contract",
                "",
                "| Element | Requirement |",
                "|---|---|",
                "| work covered in this run | full workflow ceiling measurement work |",
                "| What the agent may do | local measurement fixture actions |",
                "| Forbidden actions | none |",
                "| Prepare-only / observe-only actions | none |",
                "| Explicitly out-of-scope items | none |",
                "| Work coverage rule | every horizon item is accounted for in the fixture |",
                "",
            ]
        ),
        encoding="utf-8",
    )

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
                f"- Solution design: `{design}`",
                f"- Goal file: `{goal}`",
                "",
                "## Work Coverage And Action Limits Matrix",
                "",
                "| Work item / place | In work covered in this run? | What the agent may do | Required runtime handling | Counts as achieved? |",
                "|---|---|---|---|---|",
                "| full workflow ceiling fixture | yes | execute | run fixture checks | yes if required answer evidence exists |",
                "",
                "## Steps That Make The Result True",
                "",
                "| Required step | Required state transition | Required evidence |",
                "|---|---|---|",
                "| S1 | no scope inventory -> full workflow scope inventory exists | scope inventory evidence |",
                "| S2 | scope inventory -> removable source inventory exists | source inventory evidence |",
                "| S3 | source inventory -> coverage criterion exists | criterion evidence |",
                "| S4 | criterion -> candidate coverage matrix exists | matrix evidence |",
                "| S5 | matrix -> same-workload full workflow run completed | run evidence |",
                "| S6 | run -> interpretation against coverage matrix exists | interpretation evidence |",
                "",
                "## Action That Can Make It Done",
                "",
                "Action that can make it done:",
                "",
                "- Satisfy S1 through S6 before any achieved claim.",
                "",
                "Proof of impossibility, if any:",
                "",
                "- Record the condition proving a required step cannot be attempted.",
                "",
                "Non-achieved terminal report rule:",
                "",
                "- If it is not done, the report may be produced only after the transition is attempted and fails, or impossibility is proven.",
                "",
                "## Where The Result Must Show Up",
                "",
                "- Result placement status: `not applicable with justification`",
                "- Why no intended-result result placement is required: this fixture only checks required answer path structure.",
                "- Why no place discovery / residual reconciliation is needed: no target code state is changed.",
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
                "### Batch 1: satisfy full workflow ceiling answer path fixture",
                "",
                "Required step(s):",
                "",
                "- S1",
                "- S2",
                "- S3",
                "- S4",
                "- S5",
                "- S6",
                "",
                "Role: `mainline`",
                "",
                "State transition advanced:",
                "",
                "- S1 through S6 answer-path transitions are satisfied.",
                "",
                "Transition evidence produced:",
                "",
                "- Full workflow ceiling required answer evidence is recorded.",
                "",
                "Integration check:",
                "",
                "- Main agent accepts S1 through S6 evidence.",
                "",
                "Counts as goal progress: `yes`",
                "",
                "Why this is not merely component completion:",
                "",
                "- It records full workflow ceiling transition evidence for the approved answer path.",
                "",
                "Goal:",
                "",
                "- Drive the fixture through the approved full workflow ceiling answer path.",
                "",
                "Batch-end check:",
                "",
                "- S1 through S6 evidence recorded.",
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
        f"Reviewed `{requirements}`, `{design}`, `{goal}`, and `{plan}`.",
        "",
        "## Review Independence",
        "",
        "- Who does the work / context use: `yes`",
        f"- Design answer method check: `{review_design_answer_path_independence}`",
        "- User purpose evidence check: `yes`",
        "- Result placement check: `yes`",
        "- What counts as done check: `yes`",
        "- answer path check: `yes`",
        "- Work covered in this run and authority check: `yes`",
        "",
    ]
    if include_review_design_answer_path:
        review_parts.extend(
            [
                "## Design Answer Method Check",
                "",
                "Findings:",
                "- The design preserves the approved full workflow ceiling answering method and does not substitute a one-candidate run validation.",
                "",
            ]
        )
    review_parts.extend(
        [
            "## Who Does The Work / Context Use",
            "",
            "Findings:",
            "- Reviewed work assignment.",
            "",
            "## User Purpose Evidence Check",
            "",
            "Findings:",
            "- Purpose feedback waits for user-purpose evidence.",
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
            "- Work packages map to coverage-ceiling answer path transitions.",
            "",
            "## Work Covered And Allowed Actions Check",
            "",
            "Findings:",
            "- work covered in this run and runtime authority are fixture-bounded.",
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
    return requirements, design, goal, plan, review


class DesignAnswerPathCheckTest(unittest.TestCase):
    def test_templates_expose_answering_method_and_design_answer_path_check(self):
        requirements_template = (
            ROOT / ".agents/skills/analyzing-cybernetic-requirements/assets/requirements-analysis-template.md"
        ).read_text(encoding="utf-8")
        design_template = (
            ROOT / ".agents/skills/designing-cybernetic-solutions/assets/solution-design-template.md"
        ).read_text(encoding="utf-8")
        review_template = (
            ROOT / ".agents/skills/reviewing-cybernetic-control-structures/assets/control-review-template.md"
        ).read_text(encoding="utf-8")

        for expected in ("How this should be answered", "What is not enough", "Required answer path"):
            self.assertIn(expected, requirements_template)
        self.assertNotIn("Answer type", requirements_template)

        for expected in (
            "Answer Method Check",
            "Approved answer method",
            "Required answer path",
            "Required steps covered",
            "What is not enough avoided",
            "Required Answer Path",
            "What Supports Each Required Step",
            "Required answer step supported",
            "Mainline or supporting-only",
            "Evidence produced",
        ):
            self.assertIn(expected, design_template)
        for forbidden in ("Approved answer type", "Target Answer Path Instance", "Answer Path node", "Support Model Mapping"):
            self.assertNotIn(forbidden, design_template)

        self.assertIn("Design Answer Method Check", review_template)

    def test_design_template_is_answer_path_first_not_model_first(self):
        design_template_path = ROOT / ".agents/skills/designing-cybernetic-solutions/assets/solution-design-template.md"
        design_skill_path = ROOT / ".agents/skills/designing-cybernetic-solutions/SKILL.md"
        design_template = design_template_path.read_text(encoding="utf-8")
        design_skill = design_skill_path.read_text(encoding="utf-8")

        answer_path_index = design_template.index("## Answer Method Check")
        support_index = design_template.index("## What Supports Each Required Step")
        self.assertLess(answer_path_index, support_index)
        self.assertNotIn("## Conceptual Design", design_template)
        self.assertIn("Required step", design_template)
        self.assertIn("Required support object/component/mechanism", design_template)
        self.assertIn("required answer path first", design_skill)
        self.assertNotIn("solution model synthesis", design_skill.casefold())

    def test_answer_method_registry_drives_coverage_ceiling_guard(self):
        registry = ROOT / ".agents/skills/references/answer-method-registry.json"
        self.assertTrue(registry.exists())
        registry_text = registry.read_text(encoding="utf-8")
        orchestration_guard = ORCHESTRATION_GUARD.read_text(encoding="utf-8")
        control_guard = CONTROL_CHAIN_GUARD.read_text(encoding="utf-8")

        self.assertIn("coverage-ceiling-measurement", registry_text)
        self.assertIn("full-workflow-run-validation", registry_text)
        self.assertIn("answer-method-registry.json", orchestration_guard)
        self.assertIn("answer-method-registry.json", control_guard)
        self.assertNotIn("COVERAGE_CEILING_REQUIRED_NODES", orchestration_guard)
        self.assertNotIn("COVERAGE_CEILING_REQUIRED_NODES", control_guard)

    def test_orchestration_guard_requires_answer_method_sidecar_before_goal(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            requirements = write_requirements(tmp, control_sidecar=False)
            design = write_design(
                tmp,
                requirements,
                answer_path="coverage answer path",
                mandatory_nodes=[
                    "full workflow scope inventory",
                    "major removable source inventory",
                    "ceiling coverage criterion",
                    "candidate coverage matrix",
                    "same-workload full workflow run",
                    "interpretation against coverage matrix",
                ],
                substitution_avoided="yes, the insufficient one-candidate run-validation answer is not used",
            )

            result = subprocess.run(
                [
                    sys.executable,
                    str(ORCHESTRATION_GUARD),
                    "--state",
                    "before-goal",
                    "--requirements",
                    str(requirements),
                    "--design",
                    str(design),
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
            )

        output = result.stdout + result.stderr
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("NEXT: ReturnToRequirementsAnalysis", output)
        self.assertIn("requirements control sidecar missing", output)

    def test_orchestration_guard_rejects_missing_registry_mandatory_step(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            requirements = write_requirements(tmp)
            design = write_design(
                tmp,
                requirements,
                answer_path="coverage answer path",
                mandatory_nodes=[
                    "full workflow scope inventory",
                    "major removable source inventory",
                    "ceiling coverage criterion",
                    "same-workload full workflow run",
                    "interpretation against coverage matrix",
                ],
                substitution_avoided="yes, the insufficient one-candidate run-validation answer is not used",
            )

            result = subprocess.run(
                [
                    sys.executable,
                    str(ORCHESTRATION_GUARD),
                    "--state",
                    "before-goal",
                    "--requirements",
                    str(requirements),
                    "--design",
                    str(design),
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
            )

        output = result.stdout + result.stderr
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("NEXT: RunDesign", output)
        self.assertIn("candidate coverage matrix", output)

    def test_orchestration_guard_rejects_run_validation_substitution_before_goal(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            requirements = write_requirements(tmp)
            design = write_design(
                tmp,
                requirements,
                answer_path="full-workflow-run-validation",
                mandatory_nodes=["same-workload full workflow run"],
                substitution_avoided="no, this substitutes the forbidden run-validation answer",
            )

            result = subprocess.run(
                [
                    sys.executable,
                    str(ORCHESTRATION_GUARD),
                    "--state",
                    "before-goal",
                    "--requirements",
                    str(requirements),
                    "--design",
                    str(design),
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
            )

        output = result.stdout + result.stderr
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("NEXT: RunDesign", output)
        self.assertIn("Answer Method Check", output)
        self.assertIn("full-workflow-run-validation", output)

    def test_orchestration_guard_accepts_coverage_ceiling_answer_path_before_goal(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            requirements = write_requirements(tmp)
            design = write_design(
                tmp,
                requirements,
                answer_path="scope inventory -> removable-source inventory -> coverage criterion -> candidate coverage matrix -> same-workload run -> interpretation",
                mandatory_nodes=[
                    "full workflow scope inventory",
                    "major removable source inventory",
                    "ceiling coverage criterion",
                    "candidate coverage matrix",
                    "same-workload full workflow run",
                    "interpretation against coverage matrix",
                ],
                substitution_avoided="yes, the insufficient one-candidate run-validation answer is not used",
            )

            result = subprocess.run(
                [
                    sys.executable,
                    str(ORCHESTRATION_GUARD),
                    "--state",
                    "before-goal",
                    "--requirements",
                    str(requirements),
                    "--design",
                    str(design),
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
            )

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_control_chain_guard_requires_review_design_answer_path_check(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            requirements, design, goal, plan, review = write_runtime_chain(
                Path(tmpdir),
                include_review_design_answer_path=False,
                review_design_answer_path_independence="no",
            )
            result = subprocess.run(
                [
                    sys.executable,
                    str(CONTROL_CHAIN_GUARD),
                    "--requirements",
                    str(requirements),
                    "--design",
                    str(design),
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
        self.assertEqual(2, result.returncode, output)
        self.assertIn("NEXT: RunReview", output)
        self.assertIn("Design Answer Method Check", output)
        self.assertIn("Design answer method check: yes", output)

    def test_control_chain_guard_requires_answer_method_sidecar(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            requirements, design, goal, plan, review = write_runtime_chain(tmp)
            requirements.with_suffix(".control.json").unlink()
            result = subprocess.run(
                [
                    sys.executable,
                    str(CONTROL_CHAIN_GUARD),
                    "--requirements",
                    str(requirements),
                    "--design",
                    str(design),
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
        self.assertEqual(2, result.returncode, output)
        self.assertIn("NEXT: ReturnToRequirementsAnalysis", output)
        self.assertIn("requirements control sidecar missing", output)

    def test_runtime_contract_indexes_design_answer_path_check(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            requirements, design, goal, plan, review = write_runtime_chain(tmp)
            runtime_contract = tmp / "runtime.goal.md"
            result = subprocess.run(
                [
                    sys.executable,
                    str(COMPILER),
                    "--requirements",
                    str(requirements),
                    "--design",
                    str(design),
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
        self.assertIn("Use this /goal:", result.stdout)
        self.assertIn("Answer Method Check", contract_text)
        self.assertIn("Design Answer Method Check", contract_text)
        self.assertIn("answer method completion evidence", contract_text)
