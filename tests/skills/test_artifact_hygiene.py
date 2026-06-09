import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HYGIENE_LINT = ROOT / "scripts/lint_cybernetic_artifact_hygiene.py"
CONTROL_GUARD = ROOT / ".agents/skills/compiling-cybernetic-runtime-goals/scripts/control_chain_guard.py"
JARGON_POLICY = ROOT / ".agents/skills/references/jargon-policy.yaml"


USER_APPROVAL_APPROVED = """## What the User Approved

Status: `Approved`

| Element | Commitment |
|---|---|
| Human purpose | keep generated control artifacts readable |
| Input role binding | fixture material is an approved control artifact |
| Primary object | artifact hygiene fixture |
| Requested transformation | approved chain to runtime guard check |
| Non-goals | do not test semantic adequacy |
| How We Know The User Purpose Was Met | user-purpose evidence remains separately calibrated |
| Where The Result Must Show Up | result placement remains separately calibrated |
| What counts as done | artifact hygiene evidence needed to call it done is observed |
| Evidence needed to call it done | evidence needed to call it done is observed |
| Non-achieved terminal report handling | report goal achieved: no |
| Required answer path | artifact hygiene guard fixture required answer path |
| Work covered in this run | artifact hygiene guard fixture horizon |
| What the agent may do | local guard fixture checks |
| Forbidden live / irreversible actions | none |
| Required handling for unauthorized actions | none |
| Explicitly out-of-scope items | none |
| Final Answer Format | guard output |
| Why this process is needed | full pre-goal guard fixture |
| Known assumptions | fixture-only assumptions |

Approval record:

- Approved by: `test fixture`
- Approval phrase or source: `approved approved target`
"""


class ArtifactHygieneTest(unittest.TestCase):
    def run_lint(self, *paths: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(HYGIENE_LINT), *[str(path) for path in paths]],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )

    def write_valid_chain(self, tmp: Path) -> tuple[Path, Path, Path, Path]:
        requirements = tmp / "requirements.md"
        goal = tmp / "goal.md"
        plan = tmp / "plan.md"
        review = tmp / "review.md"

        requirements.write_text(
            "\n".join(
                [
                    "# Requirements",
                    "",
                    "## Requirements Analysis Status",
                    "",
                    "Status: `Complete`",
                    "",
                    USER_APPROVAL_APPROVED,
                    "",
                    "## Confirmed Requirement Decisions",
                    "",
                    "- Fixture decisions are confirmed.",
                    "",
                ]
            ),
            encoding="utf-8",
        )

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
                    "- Evidence needed to call it done is present.",
                    "",
                    "## How We Know The User Purpose Was Met",
                    "",
                    "| Element | Requirement |",
                    "|---|---|",
                    "| Beneficiary / observer | operator |",
                    "| Purpose-realizing outcome observed | operator can observe the intended result |",
                    "| Supporting Evidence | internal checks support progress only |",
                    "| Sufficient evidence level | user-purpose |",
                    "| If user-purpose evidence unavailable | report pending and next observation |",
                    "| Allowed completion wording | pending until user-purpose evidence is observed |",
                    "",
                    "## Where The Result Must Show Up",
                    "",
                    "| Element | Requirement |",
                    "|---|---|",
                    "| Target state | target semantics are represented across result_places |",
                    "| Required result places | result_place model, action classification, residual reconciliation |",
                    "| Place actions | act, inspect, preserve, exclude, or discover result_places |",
                    "| Residual reconciliation | account for old state, unknown result_places, exclusions, preserved result_places, and remaining mismatches |",
                    "| Result-placement wording | strongest result claim claim requires result-placement adequate |",
                    "| Partial/unavailable handling | report partial, missing, unavailable, or not applicable with justification |",
                    "| Distinction from user-purpose evidence | result placement calibrates intended-result claims while user-purpose evidence calibrates human-purpose claims |",
                    "",
                    "## What Counts As Done",
                    "",
                    "| Element | Requirement |",
                    "|---|---|",
                    "| What counts as done | artifact hygiene evidence needed to call it done is observed |",
                    "| Evidence needed to call it done | evidence needed to call it done is observed |",
                    "| Allowed achieved claim | only what counts as done supports goal achieved: yes |",
                    "| Steps that make the result true | artifact hygiene guard fixture required answer path |",
                    "",
                    "## Work Covered And Allowed Actions Contract",
                    "",
                    "| Element | Requirement |",
                    "|---|---|",
                    "| work covered in this run | artifact hygiene guard fixture horizon |",
                    "| What the agent may do | local guard fixture checks |",
                    "| Forbidden actions | none |",
                    "| Prepare-only / observe-only actions | none |",
                    "| Explicitly out-of-scope items | none |",
                    "| Work coverage rule | every horizon item is accounted for in this fixture |",
                    "",
                    "## Final Final Answer Format",
                    "",
                    "| Element | Requirement |",
                    "|---|---|",
                    "| Audience | operator |",
                    "| Purpose | execution |",
                    "| Medium | chat |",
                    "| Required structure | concise report |",
                    "| Detail level | standard |",
                    "| Evidence references required | yes |",
                    "| Machine-readable required | no |",
                    "| Destination path | not required |",
                    "| Acceptance condition | report is usable |",
                    "",
                    "Recommended next step: $orchestrating-cybernetic-pregoal",
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
                    f"- Goal file: `{goal}`",
                    "",
                    "## Work Coverage And Action Limits Matrix",
                    "",
                    "| Work item / place | In work covered in this run? | What the agent may do | Required runtime handling | Counts as achieved? |",
                    "|---|---|---|---|---|",
                    "| artifact hygiene guard fixture | yes | execute | run guard / compiler fixture checks | yes if fixture passes |",
                    "",
                    "## Steps That Make The Result True",
                    "",
                    "| Required step | Required state transition | Required evidence |",
                    "|---|---|---|",
                    "| S1 | fixture input -> artifact hygiene guard-ready chain | guard fixture files exist |",
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
                    "- Result placement status: `not applicable with justification`",
                    "- Why no intended-result result placement is required: this fixture only checks artifact hygiene.",
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
                    "### Batch 1: artifact hygiene guard fixture",
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
                    "- Keep the artifact hygiene guard fixture structurally ready.",
                    "",
                ]
            ),
            encoding="utf-8",
        )

        review.write_text(
            "\n".join(
                [
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
                    "- Work covered in this run and authority check: `yes`",
                    "",
                    "## What The User Approved Check",
                    "",
                    "Findings:",
                    "- Downstream artifacts preserve the approved approved target.",
                    "",
                    "## Who Does The Work / Context Use",
                    "",
                    "Findings:",
                    "- Reviewed work assignment.",
                    "",
                    "## User Purpose Evidence Check",
                    "",
                    "Findings:",
                    "- Internal checks are progress evidence only.",
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
                    "## Work Covered And Allowed Actions Check",
                    "",
                    "Findings:",
                    "- work covered in this run and runtime authority are compact and fixture-bounded.",
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
            ),
            encoding="utf-8",
        )
        return requirements, goal, plan, review

    def test_hygiene_lint_fails_objective_generated_artifact_pollution(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            artifact = Path(tmpdir) / "requirements.md"
            repeated = (
                "This paragraph is intentionally long enough to be treated as a duplicate "
                "generated-artifact paragraph, and it should be reported when copied twice."
            )
            artifact.write_text(
                "\n".join(
                    [
                        "# Requirements",
                        "",
                        "## What the User Approved",
                        "",
                        "Status: `Pending / Approved / Rejected / Needs Revision / Not required`",
                        "",
                        "| Element | Commitment |",
                        "|---|---|",
                        "| Human purpose | [what the human wants to change or understand] |",
                        "",
                        "Recommended next step: $orchestrating-cybernetic-pregoal",
                        "",
                        "## Human Purpose",
                        "",
                        repeated,
                        "",
                        "## Human Purpose",
                        "",
                        repeated,
                        "",
                    ]
                ),
                encoding="utf-8",
            )

            result = self.run_lint(artifact)

            self.assertEqual(2, result.returncode, result.stdout + result.stderr)
            output = result.stdout + result.stderr
            self.assertIn("unresolved enum status", output)
            self.assertIn("unresolved placeholder", output)
            self.assertIn("response-only prompt", output)
            self.assertIn("duplicate heading", output)
            self.assertIn("duplicate paragraph", output)

    def test_hygiene_lint_warns_without_failing_on_defensive_density(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            artifact = Path(tmpdir) / "review.md"
            artifact.write_text(
                "\n".join(
                    [
                        "# Review",
                        "",
                        "## Review Status",
                        "",
                        "Status: `Approved`",
                        "",
                        "## Findings",
                        "",
                        *["- must not claim purpose achievement from internal evidence checks alone." for _ in range(12)],
                    ]
                ),
                encoding="utf-8",
            )

            result = self.run_lint(artifact)

            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            self.assertIn("WARN", result.stdout)
            self.assertIn("defensive clause density", result.stdout)

    def test_hygiene_lint_checks_skill_template_language_without_artifact_noise_checks(self):
        template = ROOT / ".agents/skills/analyzing-cybernetic-requirements/assets/requirements-analysis-template.md"

        result = self.run_lint(template)

        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertNotIn("SKIP", result.stdout)

    def test_jargon_policy_exists_for_user_visible_artifacts(self):
        policy = JARGON_POLICY.read_text(encoding="utf-8")

        self.assertIn("forbidden_in_user_artifacts", policy)
        self.assertIn("Task skeleton family", policy)
        self.assertIn("How this should be answered", policy)
        self.assertIn("target-achieved", policy)
        self.assertIn("What counts as done", policy)
        for term in (
            "Answer type",
            "Spine",
            "Predicate",
            "Fidelity",
            "Boundary",
            "Closure",
            "Surface",
            "Substrate",
            "Topology",
            "Setpoint",
            "Invariant",
            "Gate",
            "Sensor",
            "target-achieving",
            "target-producing",
        ):
            self.assertIn(f'term: "{term}"', policy)
        self.assertIn("allowed_internal_paths", policy)

    def test_hygiene_lint_rejects_user_visible_jargon(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            artifact = Path(tmpdir) / "requirements.md"
            artifact.write_text(
                "\n".join(
                    [
                        "# Requirements",
                        "",
                        "## What The User Approved",
                        "",
                        "| Element | Commitment |",
                        "|---|---|",
                        "| Task skeleton family | coverage-ceiling-measurement |",
                        "| Done condition | candidate report complete |",
                        "",
                    ]
                ),
                encoding="utf-8",
            )

            result = self.run_lint(artifact)

            self.assertEqual(2, result.returncode, result.stdout + result.stderr)
            self.assertIn("user-visible jargon", result.stdout)
            self.assertIn("Task skeleton family", result.stdout)
            self.assertIn("How this should be answered", result.stdout)

    def test_user_facing_templates_use_plain_answering_language(self):
        requirements_template = (
            ROOT / ".agents/skills/analyzing-cybernetic-requirements/assets/requirements-analysis-template.md"
        ).read_text(encoding="utf-8")
        design_template = (
            ROOT / ".agents/skills/designing-cybernetic-solutions/assets/solution-design-template.md"
        ).read_text(encoding="utf-8")

        self.assertIn("How this should be answered", requirements_template)
        self.assertIn("What is not enough", requirements_template)
        self.assertIn("Required answer path", requirements_template)
        self.assertNotIn("Answer type", requirements_template)
        self.assertNotIn("Task skeleton family", requirements_template)
        self.assertNotIn("Not-sufficient substitute", requirements_template)
        self.assertIn("Approved answer method", design_template)

    def test_user_facing_templates_do_not_expose_internal_control_jargon(self):
        template_paths = [
            ROOT / ".agents/skills/analyzing-cybernetic-requirements/assets/requirements-analysis-template.md",
            ROOT / ".agents/skills/designing-cybernetic-solutions/assets/solution-design-template.md",
            ROOT / ".agents/skills/writing-cybernetic-goals/assets/goal-contract-template.md",
            ROOT / ".agents/skills/writing-cybernetic-execution-policies/assets/execution-policy-template.md",
            ROOT / ".agents/skills/reviewing-cybernetic-control-structures/assets/control-review-template.md",
            ROOT / ".agents/skills/compiling-cybernetic-runtime-goals/assets/runtime-goal-template.txt",
        ]

        forbidden = (
            "Answer type",
            "Spine",
            "Predicate",
            "Fidelity",
            "Boundary",
            "Closure",
            "Surface",
            "Substrate",
            "Topology",
            "Setpoint",
            "Invariant",
            "Gate",
            "Sensor",
            "target-achieving",
            "target-producing",
        )
        for path in template_paths:
            text = path.read_text(encoding="utf-8")
            for term in forbidden:
                self.assertNotRegex(text, rf"\b{term}\b", f"{path} exposes {term}")

    def test_hygiene_lint_enforces_hard_size_budget_with_justification_escape(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            plan = Path(tmpdir) / "plan.md"
            long_body = "\n".join(f"- generated line {i}" for i in range(710))
            plan.write_text("# Plan\n\n## Execution Policy Status\n\nStatus: `Candidate`\n\n" + long_body, encoding="utf-8")

            result = self.run_lint(plan)

            self.assertEqual(2, result.returncode, result.stdout + result.stderr)
            self.assertIn("exceeds hard size budget", result.stdout)

            plan.write_text(
                "# Plan\n\n## Artifact Size Justification\n\n- Large fixture is justified for test coverage.\n\n" + long_body,
                encoding="utf-8",
            )
            result = self.run_lint(plan)

            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            self.assertIn("WARN", result.stdout)

    def test_requirements_template_uses_single_default_hsa_status(self):
        template = (ROOT / ".agents/skills/analyzing-cybernetic-requirements/assets/requirements-analysis-template.md").read_text(
            encoding="utf-8"
        )

        hsa_section = template.split("## What the User Approved", 1)[1].split("## Human Purpose", 1)[0]
        self.assertIn("Status: `Pending`", hsa_section)
        self.assertIn("Allowed values: `Pending / Approved / Rejected / Needs Revision / Not required`", hsa_section)
        self.assertNotIn("Status: `Pending / Approved", hsa_section)

    def test_invariant_matrix_records_artifact_hygiene(self):
        matrix = (ROOT / "docs/cybernetic-framework/invariant-artifact-consumer-matrix.md").read_text(encoding="utf-8")

        self.assertIn("INV-HYG-001", matrix)
        self.assertIn("lint_cybernetic_artifact_hygiene.py", matrix)
        self.assertIn("Artifact Hygiene / Signal-to-Noise", matrix)
        self.assertIn("INV-LANG-001", matrix)
        self.assertIn("jargon-policy.yaml", matrix)

    def test_control_chain_guard_rejects_goal_hygiene_pollution(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            requirements, goal, plan, review = self.write_valid_chain(Path(tmpdir))
            result = subprocess.run(
                [
                    sys.executable,
                    str(CONTROL_GUARD),
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

            self.assertEqual(2, result.returncode, result.stdout + result.stderr)
            self.assertIn("artifact hygiene", result.stdout)
            self.assertIn("response-only prompt", result.stdout)


if __name__ == "__main__":
    unittest.main()
