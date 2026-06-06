import subprocess
import sys
import tempfile
import unittest
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


HSA_SECTION_APPROVED = """## Human Setpoint Approval

Status: `Approved`

Approval applies only to this compact control commitment.

| Element | Commitment |
|---|---|
| Human purpose | keep the control chain from executing an unapproved setpoint |
| Input role binding | source material, current state, requested transformation, method preference |
| Primary object | human-approved setpoint guard fixture |
| Requested transformation | requirements brief to approved pre-goal chain |
| Non-goals | do not reinterpret the setpoint downstream |
| Purpose Feedback Boundary | purpose feedback remains separately calibrated |
| Realization Surface Closure | target-state surfaces remain separately calibrated |
| Output Contract | final runtime command preserves approved artifacts |
| Workflow fit | full pre-goal orchestration is required for this fixture |
| Known assumptions | test fixture assumptions only |

Approval record:

- Approved by: `human`
- Approval phrase or source: `批准这个 setpoint，进入 orchestration`
- Approval time/context: `test`
"""


class HumanSetpointApprovalTest(unittest.TestCase):
    def read(self, path: str) -> str:
        return (ROOT / path).read_text(encoding="utf-8")

    def write_requirements(self, tmp: Path, *, hsa: str | None = HSA_SECTION_APPROVED) -> Path:
        requirements = tmp / "requirements.md"
        parts = [
            "# Requirements",
            "",
            "## Requirements Analysis Status",
            "",
            "Status: `Complete`",
            "",
            "## Confirmed Requirement Decisions",
            "",
            "- Fixture decisions are confirmed.",
            "",
        ]
        if hsa:
            parts.extend([hsa, ""])
        requirements.write_text("\n".join(parts), encoding="utf-8")
        return requirements

    def write_control_chain(self, tmp: Path, *, hsa: str | None = HSA_SECTION_APPROVED):
        requirements = self.write_requirements(tmp, hsa=hsa)
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
                    "| Surface actions | act / inspect / preserve / exclude / discover |",
                    "| Residual reconciliation | account for old state, unknown surfaces, exclusions, preserved surfaces, and remaining mismatches |",
                    "| RSC status wording | strongest target-realization claim requires RSC adequate |",
                    "| Partial/unavailable handling | report partial, missing, unavailable, or not applicable with justification |",
                    "| RSC / PFB boundary | RSC calibrates target-state and surface-closure claims while PFB calibrates human-purpose realization claims |",
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
                    "## Realization Surface Closure Strategy",
                    "",
                    "- RSC status: `RSC not applicable with justification`",
                    "- Why no target-state surface closure is required: this fixture only checks HSA structure.",
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
                    "",
                    "## Human Setpoint Fidelity",
                    "",
                    "Findings:",
                    "- Downstream artifacts preserve the approved compact control commitment.",
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
                    "- Internal checks are progress evidence; purpose achievement waits for purpose-boundary feedback.",
                    "",
                    "## Realization Surface Closure Adequacy",
                    "",
                    "Classification:",
                    "- RSC not applicable with justification",
                    "",
                    "Findings:",
                    "- RSC not applicable is justified for this fixture.",
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

    def test_requirements_skill_and_template_define_human_setpoint_approval(self):
        skill = self.read(".agents/skills/analyzing-cybernetic-requirements/SKILL.md")
        template = self.read(
            ".agents/skills/analyzing-cybernetic-requirements/assets/requirements-analysis-template.md"
        )

        for text in (skill, template):
            self.assertIn("Human Setpoint Approval", text)
            self.assertIn("Human purpose", text)
            self.assertIn("Input role binding", text)
            self.assertIn("Primary object", text)
            self.assertIn("Requested transformation", text)
            self.assertIn("Workflow fit", text)

        self.assertIn("Human answers to clarification questions are inputs, not approval", skill)
        self.assertIn("do not output the orchestration command or predicted `/goal`", skill)

    def test_orchestration_guard_rejects_missing_human_setpoint_approval_before_design(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            requirements = self.write_requirements(Path(tmpdir), hsa=None)
            result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / ".agents/skills/orchestrating-cybernetic-pregoal/scripts/orchestration_guard.py"),
                    "--state",
                    "before-design",
                    "--requirements",
                    str(requirements),
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
            )

        output = result.stdout + result.stderr
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("NEXT: ReturnToRequirementsAnalysis", output)
        self.assertIn("Human Setpoint Approval", output)

    def test_control_chain_guard_rejects_missing_human_setpoint_approval(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            requirements, goal, plan, review = self.write_control_chain(Path(tmpdir), hsa=None)
            result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / ".agents/skills/compiling-cybernetic-runtime-goals/scripts/control_chain_guard.py"),
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
        self.assertIn("NEXT: ReturnToRequirementsAnalysis", output)
        self.assertIn("Human Setpoint Approval", output)

    def test_control_chain_guard_accepts_approved_human_setpoint(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            requirements, goal, plan, review = self.write_control_chain(Path(tmpdir))
            result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / ".agents/skills/compiling-cybernetic-runtime-goals/scripts/control_chain_guard.py"),
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

    def test_downstream_skills_and_review_define_hsa_fidelity(self):
        for path in (
            ".agents/skills/designing-cybernetic-solutions/SKILL.md",
            ".agents/skills/writing-cybernetic-goals/SKILL.md",
            ".agents/skills/writing-cybernetic-execution-policies/SKILL.md",
            ".agents/skills/reviewing-cybernetic-control-structures/SKILL.md",
            ".agents/skills/reviewing-cybernetic-control-structures/assets/control-review-template.md",
        ):
            text = self.read(path)
            self.assertIn("Human Setpoint Approval", text)

        review_skill = self.read(".agents/skills/reviewing-cybernetic-control-structures/SKILL.md")
        review_template = self.read(
            ".agents/skills/reviewing-cybernetic-control-structures/assets/control-review-template.md"
        )
        for text in (review_skill, review_template):
            self.assertIn("Human Setpoint Fidelity", text)
            self.assertIn("approved compact control commitment", text)

    def test_runtime_compiler_preserves_approved_setpoint(self):
        skill = self.read(".agents/skills/compiling-cybernetic-runtime-goals/SKILL.md")
        compiler = self.read(".agents/skills/compiling-cybernetic-runtime-goals/scripts/compile_runtime_goal.py")
        template = self.read(
            ".agents/skills/compiling-cybernetic-runtime-goals/assets/runtime-goal-template.txt"
        )

        for text in (skill, compiler, template):
            self.assertIn("human-approved setpoint", text)
            self.assertIn("primary object", text)
            self.assertIn("requested transformation", text)
            self.assertIn("workflow fit", text)

    def test_invariant_matrix_tracks_human_setpoint_approval(self):
        matrix = self.read("docs/cybernetic-framework/invariant-artifact-consumer-matrix.md")

        self.assertIn("INV-HSA-001", matrix)
        self.assertIn("Human Setpoint Approval", matrix)
        self.assertIn("orchestration_guard.py", matrix)
        self.assertIn("control_chain_guard.py", matrix)
        self.assertIn("Human Setpoint Fidelity", matrix)
        self.assertIn("tests/skills/test_human_setpoint_approval.py", matrix)

    def test_orchestrator_evals_do_not_bypass_hsa(self):
        evals = json.loads(
            self.read(".agents/skills/orchestrating-cybernetic-pregoal/evals/evals.json")
        )["evals"]
        eval_by_id = {entry["id"]: entry for entry in evals}

        hsa_required_ids = [
            "orchestrates-complete-requirements-analysis-with-subagents",
            "no-subagents-candidate-only",
            "runtime-goal-does-not-write-plan",
            "uses-requirements-analysis-slug-for-artifacts",
            "review-nonconvergence-blocks",
            "no-independent-review-no-approval",
            "post-review-revision-requires-final-observer",
            "inserts-design-stage-when-design-gate-required",
            "orchestrator-cannot-skip-required-design",
            "orchestrator-blocks-when-design-skill-unavailable",
            "existing-design-artifact-propagates-downstream",
            "orchestrator-cannot-compile-before-review",
            "orchestrator-propagates-execution-topology-without-deciding-it",
        ]
        for eval_id in hsa_required_ids:
            self.assertIn(eval_id, eval_by_id)
            self.assertIn("Human Setpoint Approval: Approved", eval_by_id[eval_id]["prompt"])

    def test_orchestrator_candidate_mode_does_not_request_artifact_by_artifact_approval(self):
        skill = self.read(".agents/skills/orchestrating-cybernetic-pregoal/SKILL.md")

        self.assertNotIn("manually approve the artifacts", skill)
        self.assertNotIn("approves the artifacts", skill)
        self.assertIn("explicit control-review approval of the review findings", skill)
        self.assertIn("Do not ask for artifact-by-artifact review as a substitute for Human Setpoint Approval", skill)

    def test_current_message_approval_must_be_recorded_before_downstream_guards(self):
        required_phrase = (
            "update the requirements analysis `Human Setpoint Approval` section first"
        )
        for path in (
            ".agents/skills/analyzing-cybernetic-requirements/SKILL.md",
            ".agents/skills/orchestrating-cybernetic-pregoal/SKILL.md",
            ".agents/skills/designing-cybernetic-solutions/SKILL.md",
            ".agents/skills/writing-cybernetic-goals/SKILL.md",
            ".agents/skills/writing-cybernetic-execution-policies/SKILL.md",
        ):
            self.assertIn(required_phrase, self.read(path))

    def test_goal_skill_frontmatter_covers_complex_goal_contracts(self):
        skill = self.read(".agents/skills/writing-cybernetic-goals/SKILL.md")
        frontmatter = skill.split("---", 2)[1]

        self.assertIn("control contract must be written", frontmatter)
        self.assertIn("Level 3/4 full pre-goal orchestration", frontmatter)
        self.assertIn("Human Setpoint Approval", frontmatter)


if __name__ == "__main__":
    unittest.main()
