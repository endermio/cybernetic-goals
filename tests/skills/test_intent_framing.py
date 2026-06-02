import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


class IntentFramingSkillTest(unittest.TestCase):
    def read(self, path: str) -> str:
        return (ROOT / path).read_text(encoding="utf-8")

    def test_required_files_metadata_and_manifest_entries_exist(self):
        required_paths = (
            ".agents/skills/framing-cybernetic-intent/SKILL.md",
            ".agents/skills/framing-cybernetic-intent/agents/openai.yaml",
            ".agents/skills/framing-cybernetic-intent/assets/intent-frame-template.md",
            ".agents/skills/framing-cybernetic-intent/evals/evals.json",
            "tests/skills/test_intent_framing.py",
        )
        manifest = self.read("MANIFEST.txt")
        metadata = self.read(
            ".agents/skills/framing-cybernetic-intent/agents/openai.yaml"
        )

        for path in required_paths:
            self.assertTrue((ROOT / path).exists(), path)
            self.assertIn(path, manifest)
        self.assertIn("allow_implicit_invocation: false", metadata)

    def test_skill_contract_anchors_exist(self):
        skill = self.read(".agents/skills/framing-cybernetic-intent/SKILL.md")
        skill_text = skill.casefold()

        self.assertIn("name: framing-cybernetic-intent", skill)
        self.assertIn("Shared Intent Understanding", skill)
        for term in (
            "pre-task",
            "collaborative intent framing",
            "method",
            "purpose",
            "must not",
            "optional task",
        ):
            self.assertIn(term, skill_text)
        self.assertIn("routing-cybernetic-workflows", skill)

    def test_template_preserves_intent_frame_not_control_artifacts(self):
        template = self.read(
            ".agents/skills/framing-cybernetic-intent/assets/intent-frame-template.md"
        )

        for heading in (
            "## Human Situation",
            "## Method vs Purpose",
            "## Risk or Uncertainty to Reduce",
            "## What Not To Assume Yet",
            "## Shared Intent Understanding",
            "## Optional Task Formation",
        ):
            self.assertIn(heading, template)
        self.assertNotIn("Execution Policy", template)
        self.assertNotIn("Runtime /goal", template)

    def test_evals_cover_pre_task_failure_modes(self):
        evals = json.loads(
            self.read(".agents/skills/framing-cybernetic-intent/evals/evals.json")
        )
        ids = {item["id"] for item in evals["evals"]}

        self.assertIn("method-preference-is-not-purpose", ids)
        self.assertIn("dissatisfaction-is-not-execution-task", ids)
        self.assertIn("failure-experience-is-not-repair-goal", ids)
        self.assertIn("unstable-intent-asks-one-question", ids)
        self.assertIn("shared-understanding-before-task-candidate", ids)
        self.assertIn("chat-only-default-no-artifact", ids)
        self.assertIn("persistent-intent-brief-only-when-justified", ids)

    def test_integration_surfaces_reference_pre_task_handoff(self):
        readme = self.read("README.md")
        router = self.read(".agents/skills/routing-cybernetic-workflows/SKILL.md")
        requirements = self.read(
            ".agents/skills/analyzing-cybernetic-requirements/SKILL.md"
        )
        matrix = self.read("docs/cybernetic-framework/invariant-artifact-consumer-matrix.md")

        self.assertIn("human situation", readme)
        self.assertIn("framing-cybernetic-intent", readme)
        for text in (router, requirements):
            folded = text.casefold()
            self.assertIn("framing-cybernetic-intent", text)
            self.assertIn("pre-task", folded)
            self.assertIn("formed task", folded)
        self.assertIn("INV-INT-001", matrix)
        self.assertIn("framing-cybernetic-intent", matrix)


if __name__ == "__main__":
    unittest.main()
