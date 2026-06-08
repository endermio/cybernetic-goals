import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HYGIENE_LINT = ROOT / "scripts/lint_cybernetic_artifact_hygiene.py"
CONTROL_GUARD = ROOT / ".agents/skills/compiling-cybernetic-runtime-goals/scripts/control_chain_guard.py"


HSA_APPROVED = """## Human Setpoint Approval

Status: `Approved`

| Element | Commitment |
|---|---|
| Human purpose | keep generated control artifacts readable |
| Input role binding | fixture material is an approved control artifact |
| Primary object | artifact hygiene fixture |
| Requested transformation | approved chain to runtime guard check |
| Non-goals | do not test semantic adequacy |
| Purpose Feedback Boundary | purpose feedback remains separately calibrated |
| Realization Surface Closure | RSC remains separately calibrated |
| Single target-achieved predicate | artifact hygiene target-producing evidence is observed |
| Target-producing evidence required | target-producing evidence is observed |
| Non-achieved terminal report handling | report goal achieved: no |
| Execution horizon | artifact hygiene guard fixture horizon |
| Runtime authority | local guard fixture checks |
| Forbidden live / irreversible actions | none |
| Required handling for unauthorized actions | none |
| Explicitly out-of-scope items | none |
| Output Contract | guard output |
| Workflow fit | full pre-goal guard fixture |
| Known assumptions | fixture-only assumptions |

Approval record:

- Approved by: `test fixture`
- Approval phrase or source: `approved setpoint`
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
                    HSA_APPROVED,
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
                    "Codex may report `goal achieved: yes` only when the single target-achieved predicate is satisfied.",
                    "",
                    "- Required target-producing evidence is present.",
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
                    "## Realization Surface Contract",
                    "",
                    "| Element | Requirement |",
                    "|---|---|",
                    "| Target state | target semantics are represented across realization surfaces |",
                    "| Required surfaces | surface model, action classification, residual reconciliation |",
                    "| Surface actions | act, inspect, preserve, exclude, or discover surfaces |",
                    "| Residual reconciliation | account for old state, unknown surfaces, exclusions, preserved surfaces, and remaining mismatches |",
                    "| RSC status wording | strongest target-realization claim requires RSC adequate |",
                    "| Partial/unavailable handling | report partial, missing, unavailable, or not applicable with justification |",
                    "| RSC / PFB boundary | RSC calibrates target-state claims while PFB calibrates human-purpose claims |",
                    "",
                    "## Target Achievement Contract",
                    "",
                    "| Element | Requirement |",
                    "|---|---|",
                    "| Single target-achieved predicate | artifact hygiene target-producing evidence is observed |",
                    "| Required target-producing evidence | target-producing evidence is observed |",
                    "| Allowed achieved claim | only target-achieved predicate supports goal achieved: yes |",
                    "",
                    "## Execution Horizon and Authority Contract",
                    "",
                    "| Element | Requirement |",
                    "|---|---|",
                    "| Approved horizon | artifact hygiene guard fixture horizon |",
                    "| Runtime-authorized actions | local guard fixture checks |",
                    "| Forbidden actions | none |",
                    "| Prepare-only / observe-only actions | none |",
                    "| Explicitly out-of-scope items | none |",
                    "| Horizon completion rule | every horizon item is accounted for in this fixture |",
                    "",
                    "## Final Output Contract",
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
                    f"- Goal contract: `{goal}`",
                    "",
                    "## Horizon and Authority Coverage Matrix",
                    "",
                    "| Batch / surface | In approved horizon? | Runtime authority | Required runtime handling | Counts as achieved? |",
                    "|---|---|---|---|---|",
                    "| artifact hygiene guard fixture | yes | execute | run guard / compiler fixture checks | yes if fixture passes |",
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
                    "- RSC status: `RSC not applicable with justification`",
                    "- Why no target-state surface closure is required: this fixture only checks artifact hygiene.",
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
                    "- Human setpoint fidelity: `yes`",
                    "- Goal contract: `yes`",
                    "- Execution policy: `yes`",
                    "- Context management / execution topology: `yes`",
                    "- Purpose feedback adequacy: `yes`",
                    "- Realization surface closure adequacy: `yes`",
                    "- Target achievement predicate fidelity: `yes`",
                    "- Execution horizon and authority fidelity: `yes`",
                    "",
                    "## Human Setpoint Fidelity",
                    "",
                    "Findings:",
                    "- Downstream artifacts preserve the approved setpoint.",
                    "",
                    "## Context Management / Execution Topology",
                    "",
                    "Findings:",
                    "- Reviewed selected topology.",
                    "",
                    "## Purpose Feedback Adequacy",
                    "",
                    "Findings:",
                    "- Internal checks are progress evidence only.",
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
                        "## Human Setpoint Approval",
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
                        *["- must not claim purpose achievement from internal sensors alone." for _ in range(12)],
                    ]
                ),
                encoding="utf-8",
            )

            result = self.run_lint(artifact)

            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            self.assertIn("WARN", result.stdout)
            self.assertIn("defensive clause density", result.stdout)

    def test_hygiene_lint_skips_skill_templates(self):
        template = ROOT / ".agents/skills/analyzing-cybernetic-requirements/assets/requirements-analysis-template.md"

        result = self.run_lint(template)

        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn("SKIP", result.stdout)

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

        hsa_section = template.split("## Human Setpoint Approval", 1)[1].split("## Human Purpose", 1)[0]
        self.assertIn("Status: `Pending`", hsa_section)
        self.assertIn("Allowed values: `Pending / Approved / Rejected / Needs Revision / Not required`", hsa_section)
        self.assertNotIn("Status: `Pending / Approved", hsa_section)

    def test_invariant_matrix_records_artifact_hygiene(self):
        matrix = (ROOT / "docs/cybernetic-framework/invariant-artifact-consumer-matrix.md").read_text(encoding="utf-8")

        self.assertIn("INV-HYG-001", matrix)
        self.assertIn("lint_cybernetic_artifact_hygiene.py", matrix)
        self.assertIn("Artifact Hygiene / Signal-to-Noise", matrix)

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
