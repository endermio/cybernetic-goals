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

    def test_full_chain_skill_is_not_level2_bounded_runtime_protocol(self):
        text = combined_protocol_text()

        self.assertRegex(text, re.compile(r"not[^.\n]*Level 2 bounded", re.I))
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

    def test_amendment_proposal_documents_source_requirements_and_compatibility_split(self):
        text = combined_protocol_text()

        self.assertIn("affected_source_requirements", text)
        self.assertRegex(text, re.compile(r"v1\.0[^.\n]*compatibility", re.I))
        self.assertRegex(text, re.compile(r"runtime[^.\n]*policy[^.\n]*requires[^.\n]*affected_source_requirements", re.I))

    def test_goal_achieved_true_requires_verifier_permission(self):
        text = combined_protocol_text()

        self.assertIn("goal_achieved: true", text)
        self.assertRegex(text, re.compile(r"verifier[^.\n]*before[^.\n]*goal_achieved: true", re.I))
        self.assertRegex(text, re.compile(r"verifier[^.\n]*(allows|permits|approved)", re.I))

    def test_short_goal_adapter_stays_pointer_only(self):
        text = combined_protocol_text()

        self.assertIn("/goal", text)
        self.assertIn("short pointer", text)
        self.assertIn("runtime.control.json", text)
        self.assertIn("using-control-json", text)
        self.assertRegex(text, re.compile(r"/goal[^.\n]*not[^.\n]*control fact", re.I))


if __name__ == "__main__":
    unittest.main()
