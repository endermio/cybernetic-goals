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


if __name__ == "__main__":
    unittest.main()
