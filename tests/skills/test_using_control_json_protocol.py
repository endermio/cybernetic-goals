import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SKILL = ROOT / ".agents/skills/using-control-json/SKILL.md"
PROTOCOL = ROOT / ".agents/skills/using-control-json/references/runtime-control-json-protocol.md"


def combined_protocol_text() -> str:
    return "\n".join(
        path.read_text(encoding="utf-8")
        for path in (SKILL, PROTOCOL)
    )


class UsingControlJsonProtocolTest(unittest.TestCase):
    def test_skill_and_protocol_files_exist(self):
        self.assertTrue(SKILL.exists(), SKILL)
        self.assertTrue(PROTOCOL.exists(), PROTOCOL)

    def test_approved_control_json_is_read_only(self):
        text = combined_protocol_text()

        self.assertIn("approved control JSON is read-only", text)
        for artifact in (
            "requirements.control.json",
            "design.control.json",
            "goal.control.json",
            "plan.control.json",
            "review.control.json",
            "runtime.control.json",
        ):
            self.assertIn(artifact, text)

        self.assertRegex(
            text,
            re.compile(r"stop[^.\n]*(missing|invalid|inconsistent)[^.\n]*JSON", re.I),
        )

    def test_json_pregoal_skill_is_not_bounded_runtime_protocol(self):
        text = combined_protocol_text()

        self.assertRegex(text, re.compile(r"not[^.\n]*bounded_runtime", re.I))
        self.assertIn("using-bounded-control-json", text)

    def test_runtime_writes_are_limited_to_three_files(self):
        text = combined_protocol_text()

        self.assertIn("runtime writes only", text)
        for writable in ("progress.jsonl", "runtime-status.json", "final-report.json"):
            self.assertIn(writable, text)

    def test_runtime_self_hash_excludes_approved_control_hashes(self):
        text = combined_protocol_text()

        self.assertIn("approved_control_hashes", text)
        self.assertIn("runtime.control.json", text)
        self.assertRegex(text, re.compile(r"runtime\.control\.json[^.\n]*exclude[^.\n]*approved_control_hashes", re.I))
        self.assertIn("self-reference", text)

    def test_progress_events_are_append_only_jsonl_observations(self):
        text = combined_protocol_text()

        self.assertRegex(text, re.compile(r"append[^.\n]*progress\.jsonl", re.I))
        self.assertIn("one JSON object per line", text)
        self.assertIn("observations", text)
        self.assertIn("do not mutate approved JSON", text)

    def test_progress_events_must_use_validated_append_helper(self):
        text = combined_protocol_text()

        self.assertIn("append_progress_event.py", text)
        self.assertRegex(text, re.compile(r"direct[^.\n]*writes?[^.\n]*progress\.jsonl[^.\n]*invalid", re.I))
        self.assertRegex(text, re.compile(r"must[^.\n]*append_progress_event\.py", re.I))

    def test_amendment_proposal_documents_source_requirements_and_compatibility_split(self):
        text = combined_protocol_text()

        self.assertIn("affected_source_requirements", text)
        self.assertRegex(text, re.compile(r"v1\.0[^.\n]*compatibility", re.I))
        self.assertRegex(text, re.compile(r"runtime[^.\n]*policy[^.\n]*requires[^.\n]*affected_source_requirements", re.I))

    def test_runtime_preserves_information_sufficiency_failures(self):
        text = combined_protocol_text()

        self.assertIn("information_sufficiency_check", text)
        self.assertRegex(text, re.compile(r"should have been known before design or\s+planning", re.I))
        self.assertRegex(text, re.compile(r"must\s+not[^.\n]*invent[^.\n]*sufficiency standard", re.I))
        self.assertIn("control.amendment.proposed", text)
        self.assertRegex(text, re.compile(r"reviewed amendment proposal", re.I))

    def test_requirements_skill_defines_information_collection_as_requirements_analysis_loop(self):
        main = (ROOT / ".agents/skills/analyzing-cybernetic-requirements/SKILL.md").read_text(encoding="utf-8")
        details = (
            ROOT / ".agents/skills/analyzing-cybernetic-requirements/references/requirements-analysis-detailed-rules.md"
        ).read_text(encoding="utf-8")
        text = main + "\n" + details

        self.assertIn("Information collection is part of requirements analysis", text)
        self.assertIn("needs_information_gathering", text)
        self.assertIn("needs_requirements_revision", text)
        self.assertIn("Do not ask for final requirements approval", text)

    def test_goal_achieved_true_requires_verifier_permission(self):
        text = combined_protocol_text()
        normalized = " ".join(text.split())

        self.assertIn("goal_achieved: true", text)
        self.assertRegex(text, re.compile(r"verifier[^.\n]*before[^.\n]*(accepting|reporting|acting on)", re.I))
        self.assertRegex(text, re.compile(r"final-report\.json[^.\n]*does not grant verifier permission to itself", re.I))
        self.assertIn("structural final-claim gate", normalized)
        self.assertIn("not a semantic quality gate", normalized)
        self.assertNotIn("verifier process output as the source of truth", normalized)
        self.assertNotRegex(text, re.compile(r"verifier[^.\n]*output[^.\n]*source of truth", re.I))

    def test_validators_are_structural_gates_not_quality_approval(self):
        text = combined_protocol_text()

        self.assertIn("Structural gates", text)
        self.assertIn("Quality gate", text)
        for structural in ("schema", "control_chain_guard", "validate_control_chain", "verify_runtime_progress"):
            self.assertIn(structural, text)
        self.assertIn("counterexample-gate", text)
        self.assertRegex(text, re.compile(r"structural[^.\n]*not[^.\n]*quality approval", re.I))
        self.assertRegex(text, re.compile(r"counterexample-gate[^.\n]*quality gate", re.I))

    def test_short_goal_adapter_stays_pointer_only(self):
        text = combined_protocol_text()

        self.assertIn("/goal", text)
        self.assertIn("short pointer", text)
        self.assertIn("runtime.control.json", text)
        self.assertIn("using-control-json", text)
        self.assertRegex(text, re.compile(r"/goal[^.\n]*not[^.\n]*control fact", re.I))


if __name__ == "__main__":
    unittest.main()
