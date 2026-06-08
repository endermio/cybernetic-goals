import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


class EvidenceLifecycleBudgetTest(unittest.TestCase):
    def read(self, path: str) -> str:
        return (ROOT / path).read_text(encoding="utf-8")

    def test_execution_policy_defines_evidence_lifecycle_budget(self):
        skill = self.read(".agents/skills/writing-cybernetic-execution-policies/SKILL.md")
        template = self.read(
            ".agents/skills/writing-cybernetic-execution-policies/assets/execution-policy-template.md"
        )

        for text in (skill, template):
            self.assertIn("Evidence Lifecycle / Evidence Budget", text)
            self.assertIn("Evidence channel", text)
            self.assertIn("Raw allowed?", text)
            self.assertIn("Baseline policy", text)
            self.assertIn("Per-batch retention", text)
            self.assertIn("Delta required?", text)
            self.assertIn("Summary required?", text)
            self.assertIn("Max tracked size", text)
            self.assertIn("Git policy", text)
            self.assertIn("Raw pointer", text)
            self.assertIn("one full baseline", text)
            self.assertIn("one final full scan", text)
            self.assertIn("summary + delta", text)

    def test_progress_log_records_evidence_budget_status(self):
        template = self.read(
            ".agents/skills/writing-cybernetic-execution-policies/assets/execution-policy-template.md"
        )

        for required in (
            "evidence budget status",
            "raw evidence generated",
            "delta/summary path",
            "raw pointer/hash",
            "reason for full snapshot",
            "tracked evidence size estimate",
        ):
            self.assertIn(required, template)

    def test_review_checks_evidence_lifecycle_budget(self):
        skill = self.read(".agents/skills/reviewing-cybernetic-control-structures/SKILL.md")
        template = self.read(
            ".agents/skills/reviewing-cybernetic-control-structures/assets/control-review-template.md"
        )

        for text in (skill, template):
            self.assertIn("Evidence Lifecycle / Evidence Budget", text)
            self.assertIn("repeated full raw evidence check outputs", text)
            self.assertIn("summary", text)
            self.assertIn("delta", text)
            self.assertIn("reviewable", text)
            self.assertIn("raw pointer", text)

    def test_lint_requires_evidence_lifecycle_sections(self):
        lint = self.read(
            ".agents/skills/reviewing-cybernetic-control-structures/scripts/control_artifact_lint.py"
        )

        self.assertIn("Evidence Lifecycle / Evidence Budget", lint)

    def test_evals_cover_evidence_explosion(self):
        policy_evals = json.loads(
            self.read(".agents/skills/writing-cybernetic-execution-policies/evals/evals.json")
        )
        review_evals = json.loads(
            self.read(".agents/skills/reviewing-cybernetic-control-structures/evals/evals.json")
        )

        self.assertIn(
            "execution-policy-prevents-repeated-full-raw-evidence",
            {item["id"] for item in policy_evals["evals"]},
        )
        self.assertIn(
            "review-flags-evidence-explosion",
            {item["id"] for item in review_evals["evals"]},
        )

    def test_invariant_matrix_tracks_evidence_lifecycle_budget(self):
        matrix = self.read("docs/cybernetic-framework/invariant-artifact-consumer-matrix.md")

        self.assertIn("INV-EVD-001", matrix)
        self.assertIn("Evidence Lifecycle / Evidence Budget", matrix)
        self.assertIn("repeated full raw evidence check outputs", matrix)


if __name__ == "__main__":
    unittest.main()
