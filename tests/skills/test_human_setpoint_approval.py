import subprocess
import sys
import tempfile
import unittest
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


USER_APPROVAL_SECTION_APPROVED = """## What the User Approved

Status: `Approved`

Approval applies only to this compact control commitment.

| Element | Commitment |
|---|---|
| Human purpose | keep the control chain from executing an unapproved approved target |
| Input role binding | source material, current state, requested transformation, method preference |
| Primary object | human-approved approved target guard fixture |
| Requested transformation | requirements brief to approved pre-goal chain |
| Non-goals | do not reinterpret the approved target downstream |
| How We Know The User Purpose Was Met | user-purpose evidence remains separately calibrated |
| Where The Result Must Show Up | intended-result_places remain separately calibrated |
| What counts as done | approved What the User Approved guard target is observed |
| Evidence needed to call it done | target-producing evidence is observed |
| Non-achieved terminal report handling | report goal achieved: no |
| Required answer path | What the User Approved guard fixture required answer path |
| Work covered in this run | What the User Approved guard fixture horizon |
| What the agent may do | local guard fixture checks |
| Forbidden live / irreversible actions | none |
| Required handling for unauthorized actions | none |
| Explicitly out-of-scope items | none |
| Final Answer Format | final runtime command preserves approved artifacts |
| Why this process is needed | full pre-goal orchestration is required for this fixture |
| Known assumptions | test fixture assumptions only |

Approval record:

- Approved by: `human`
- Approval phrase or source: `批准这个 approved target，进入 orchestration`
- Approval time/context: `test`
"""


class HumanApprovalTest(unittest.TestCase):
    def read(self, path: str) -> str:
        return (ROOT / path).read_text(encoding="utf-8")

    def write_requirements(self, tmp: Path, *, hsa: str | None = USER_APPROVAL_SECTION_APPROVED) -> Path:
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

    def write_control_chain(self, tmp: Path, *, hsa: str | None = USER_APPROVAL_SECTION_APPROVED):
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
                    "## Where The Result Must Show Up",
                    "",
                    "| Element | Requirement |",
                    "|---|---|",
                    "| Target state | target semantics are represented across realization places |",
                    "| Required result places | place model, action classification, residual reconciliation |",
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
                    "| What counts as done | approved What the User Approved guard target is observed |",
                    "| Evidence needed to call it done | target-producing evidence is observed |",
                    "| Allowed achieved claim | only what counts as done supports goal achieved: yes |",
                    "| Steps that make the result true | What the User Approved guard fixture required answer path |",
                    "",
                    "## Work Covered And Allowed Actions Contract",
                    "",
                    "| Element | Requirement |",
                    "|---|---|",
                    "| Work covered in this run | What the User Approved guard fixture horizon |",
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
                    "| What the User Approved guard fixture | yes | execute | run guard / compiler fixture checks | yes if fixture passes |",
                    "",
                    "## Steps That Make The Result True",
                    "",
                    "| Required step | Required state transition | Required evidence |",
                    "|---|---|---|",
                    "| S1 | fixture input -> What the User Approved guard-ready chain | guard fixture files exist |",
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
                    "- Why no intended-result result placement is required: this fixture only checks What the User Approved structure.",
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
                    "### Batch 1: What the User Approved guard fixture",
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
                    "- Fixture target-producing evidence is recorded.",
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
                    "- Keep the What the User Approved guard fixture structurally ready.",
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
                    "## What the User Approved Check",
                    "",
                    "Findings:",
                    "- Downstream artifacts preserve the approved compact control commitment.",
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
                    "- Internal checks are progress evidence; purpose achievement waits for purpose-limit feedback.",
                    "",
                    "## Result Placement Check",
                    "",
                    "Classification:",
                    "- not applicable with justification",
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
                    "- Work covered in this run and runtime authority are compact and fixture-bounded.",
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

    def test_requirements_skill_and_template_define_user_approval(self):
        skill = self.read(".agents/skills/analyzing-cybernetic-requirements/SKILL.md")
        template = self.read(
            ".agents/skills/analyzing-cybernetic-requirements/assets/requirements-analysis-template.md"
        )

        for text in (skill, template):
            self.assertIn("What the User Approved", text)
            self.assertIn("Human purpose", text)
            self.assertIn("Input role binding", text)
            self.assertIn("Primary object", text)
            self.assertIn("Requested transformation", text)
            self.assertIn("Why this process is needed", text)

        self.assertIn("Human answers to clarification questions are inputs, not approval", skill)
        self.assertIn("do not output the orchestration command or predicted `/goal`", skill)

    def test_orchestration_guard_rejects_missing_user_approval_before_design(self):
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
        self.assertIn("What the User Approved", output)

    def test_control_chain_guard_rejects_missing_user_approval(self):
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
        self.assertIn("What the User Approved", output)

    def test_control_chain_guard_accepts_approved_user_approval(self):
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

    def test_downstream_skills_and_review_define_hsa_check(self):
        for path in (
            ".agents/skills/designing-cybernetic-solutions/SKILL.md",
            ".agents/skills/writing-cybernetic-goals/SKILL.md",
            ".agents/skills/writing-cybernetic-execution-policies/SKILL.md",
            ".agents/skills/reviewing-cybernetic-control-structures/SKILL.md",
            ".agents/skills/reviewing-cybernetic-control-structures/assets/control-review-template.md",
        ):
            text = self.read(path)
            self.assertIn("What the User Approved", text)

        review_skill = self.read(".agents/skills/reviewing-cybernetic-control-structures/SKILL.md")
        review_template = self.read(
            ".agents/skills/reviewing-cybernetic-control-structures/assets/control-review-template.md"
        )
        for text in (review_skill, review_template):
            self.assertIn("What The User Approved Check", text)
            self.assertIn("approved compact control commitment", text)

    def test_runtime_compiler_preserves_approved_target(self):
        skill = self.read(".agents/skills/compiling-cybernetic-runtime-goals/SKILL.md")
        compiler = self.read(".agents/skills/compiling-cybernetic-runtime-goals/scripts/compile_runtime_goal.py")
        template = self.read(
            ".agents/skills/compiling-cybernetic-runtime-goals/assets/runtime-goal-template.txt"
        )

        for text in (skill, compiler, template):
            self.assertIn("What the User Approved", text)
            self.assertIn("primary object", text)
            self.assertIn("requested transformation", text)
            self.assertIn("why this process is needed", text)

    def test_invariant_matrix_tracks_human_approved_target_approval(self):
        matrix = self.read("docs/cybernetic-framework/invariant-artifact-consumer-matrix.md")

        self.assertIn("INV-What the User Approved-001", matrix)
        self.assertIn("What the User Approved", matrix)
        self.assertIn("orchestration_guard.py", matrix)
        self.assertIn("control_chain_guard.py", matrix)
        self.assertIn("What the User Approved Check", matrix)
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
            "inserts-design-stage-when-design-check-required",
            "orchestrator-cannot-skip-required-design",
            "orchestrator-blocks-when-design-skill-unavailable",
            "existing-design-artifact-propagates-downstream",
            "orchestrator-cannot-compile-before-review",
            "orchestrator-propagates-execution-work-assignment-without-deciding-it",
        ]
        for eval_id in hsa_required_ids:
            self.assertIn(eval_id, eval_by_id)
            self.assertIn("What the User Approved: Approved", eval_by_id[eval_id]["prompt"])

    def test_orchestrator_candidate_mode_does_not_request_artifact_by_artifact_approval(self):
        skill = self.read(".agents/skills/orchestrating-cybernetic-pregoal/SKILL.md")

        self.assertNotIn("manually approve the artifacts", skill)
        self.assertNotIn("approves the artifacts", skill)
        self.assertIn("explicit control-review approval of the review findings", skill)
        self.assertIn("Do not ask for artifact-by-artifact review as a substitute for What the User Approved", skill)

    def test_current_message_approval_must_be_recorded_before_downstream_guards(self):
        required_phrase = (
            "update the requirements analysis `What the User Approved` section first"
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

        self.assertIn("goal file must be written", frontmatter)
        self.assertIn("Level 3/4 full pre-goal orchestration", frontmatter)
        self.assertIn("What the User Approved", frontmatter)


if __name__ == "__main__":
    unittest.main()
