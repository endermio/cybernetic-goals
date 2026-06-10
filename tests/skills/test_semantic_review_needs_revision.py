import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
ORCHESTRATION_SKILL = ROOT / ".agents/skills/orchestrating-cybernetic-pregoal/SKILL.md"
ORCHESTRATION_PROTOCOL = (
    ROOT / ".agents/skills/orchestrating-cybernetic-pregoal/references/orchestration-protocol.md"
)
SUBAGENT_ROLES = (
    ROOT / ".agents/skills/orchestrating-cybernetic-pregoal/references/subagent-review-roles.md"
)
REVIEW_SKILL = ROOT / ".agents/skills/reviewing-cybernetic-control-structures/SKILL.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class SemanticReviewNeedsRevisionTest(unittest.TestCase):
    def test_review_defines_intent_and_obligation_preservation_verdicts(self):
        review_text = read(REVIEW_SKILL)
        roles_text = read(SUBAGENT_ROLES)

        self.assertIn("Intent Preservation / Obligation Preservation Review", review_text)
        self.assertIn("Intent Preservation / Obligation Preservation Reviewer", roles_text)
        self.assertIn("`Approved` / `NeedsRevision` / `Blocked`", review_text)
        self.assertIn("not a simple fail", review_text)
        self.assertIn("runtime compilation is forbidden until the verdict is `Approved`", review_text)

        for downgrade in ("readiness", "future", "allowed", "compatibility-only"):
            with self.subTest(downgrade=downgrade):
                self.assertIn(downgrade, review_text)

    def test_needs_revision_routes_to_stage_where_drift_was_introduced(self):
        combined = "\n".join(
            [
                read(ORCHESTRATION_SKILL),
                read(ORCHESTRATION_PROTOCOL),
                read(REVIEW_SKILL),
            ]
        )

        for route in (
            "Requirements drift -> `ReturnToRequirementsAnalysis`",
            "Design drift -> `RunDesign`",
            "Goal drift -> `RunGoalWriting`",
            "Plan drift -> `RunExecutionPolicy`",
        ):
            with self.subTest(route=route):
                self.assertIn(route, combined)

        self.assertIn("NeedsRevision routes to the earliest artifact that introduced drift", combined)
        self.assertIn("do not compile `runtime.control.json`", combined)

    def test_api_v2_downgrade_accident_is_needs_revision_not_approval(self):
        review_text = read(REVIEW_SKILL)
        orchestration_text = read(ORCHESTRATION_SKILL)

        for text in (review_text, orchestration_text):
            with self.subTest(path=text[:30]):
                self.assertIn("required `/api/v2` implementation", text)
                self.assertIn("legacy Drogon compatibility readiness", text)
                self.assertIn("NeedsRevision", text)
                self.assertIn("must not be accepted", text)

    def test_source_requirement_extraction_cannot_weaken_measurement_to_framework(self):
        review_text = read(REVIEW_SKILL)

        self.assertIn("source-requirement-preservation", review_text)
        self.assertIn("measure E, S, A, M, Q, K, Se, Nout, Cckpt growth curves", review_text)
        self.assertIn("define scan framework and dominance rules", review_text)
        self.assertIn("NeedsRevision", review_text)
        self.assertIn("ReturnToRequirementsAnalysis", review_text)

    def test_source_requirement_extraction_cannot_weaken_api_v2_implementation_to_compatibility(self):
        review_text = read(REVIEW_SKILL)

        self.assertIn("source-requirement-preservation", review_text)
        self.assertIn("implement /api/v2 download/extract/preview API family", review_text)
        self.assertIn("compatible with future v2 exposure", review_text)
        self.assertIn("NeedsRevision", review_text)
        self.assertIn("ReturnToRequirementsAnalysis", review_text)

    def test_runtime_compile_requires_approved_control_statuses_and_runtime_validator(self):
        combined = "\n".join(
            [
                read(ORCHESTRATION_SKILL),
                read(ROOT / ".agents/skills/orchestrating-cybernetic-pregoal/references/output-and-final-checks.md"),
            ]
        )

        for phrase in (
            "design.control.json status == approved",
            "goal.control.json status == approved",
            "plan.control.json status == approved",
            "review.control.json status == approved",
            "runtime.control.json status == compiled",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, combined)

        self.assertIn(
            "python3 .agents/skills/using-control-json/scripts/validate_control_chain.py",
            combined,
        )
        self.assertIn("ok: true", combined)
        self.assertIn("Candidate", combined)
        self.assertIn("may not enter runtime compilation", combined)


if __name__ == "__main__":
    unittest.main()
