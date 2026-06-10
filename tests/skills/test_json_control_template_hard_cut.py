import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

OFFICIAL_MARKDOWN_TEMPLATE_PATHS = [
    ROOT / ".agents/skills/analyzing-cybernetic-requirements/assets/requirements-analysis-template.md",
    ROOT / ".agents/skills/designing-cybernetic-solutions/assets/solution-design-template.md",
    ROOT / ".agents/skills/writing-cybernetic-goals/assets/goal-contract-template.md",
    ROOT / ".agents/skills/writing-cybernetic-execution-policies/assets/execution-policy-template.md",
    ROOT / ".agents/skills/reviewing-cybernetic-control-structures/assets/control-review-template.md",
    ROOT / ".agents/skills/compiling-cybernetic-runtime-goals/assets/runtime-goal-template.txt",
]

REQUIRED_JSON_EXAMPLES = [
    ROOT / ".agents/skills/analyzing-cybernetic-requirements/assets/requirements.control.example.json",
    ROOT / ".agents/skills/designing-cybernetic-solutions/assets/design.control.example.json",
    ROOT / ".agents/skills/writing-cybernetic-goals/assets/goal.control.example.json",
    ROOT / ".agents/skills/writing-cybernetic-execution-policies/assets/plan.control.example.json",
    ROOT / ".agents/skills/reviewing-cybernetic-control-structures/assets/review.control.example.json",
    ROOT / ".agents/skills/compiling-cybernetic-runtime-goals/assets/runtime.control.example.json",
]

OFFICIAL_MARKDOWN_CONTROL_FILENAMES = (
    "requirements.md",
    "design.md",
    "goal.md",
    "plan.md",
    "review.md",
    "runtime-goal.md",
    "runtime.goal.md",
    ".goal.md",
)


class JsonControlTemplateHardCutTest(unittest.TestCase):
    def test_markdown_assets_are_deauthorized_as_control_fact_templates(self):
        for path in OFFICIAL_MARKDOWN_TEMPLATE_PATHS:
            with self.subTest(path=path.relative_to(ROOT)):
                text = path.read_text(encoding="utf-8")

                self.assertIn("not an official control fact template", text.casefold())
                self.assertIn("docs/cybernetics/runs/<slug>/", text)
                self.assertIn(".control.json", text)
                self.assertIn("progress.jsonl", text)
                self.assertIn("runtime-status.json", text)
                self.assertIn("final-report.json", text)
                self.assertNotRegex(text, r"^# (Requirements|Design|Goal|Execution Policy|Review|Runtime Goal)\b")
                for filename in OFFICIAL_MARKDOWN_CONTROL_FILENAMES:
                    self.assertNotIn(filename, text)

    def test_json_examples_exist_for_each_control_fact_stage(self):
        expected_artifact_types = {
            "requirements.control",
            "design.control",
            "goal.control",
            "plan.control",
            "review.control",
            "runtime.control",
        }
        observed_artifact_types = set()

        for path in REQUIRED_JSON_EXAMPLES:
            with self.subTest(path=path.relative_to(ROOT)):
                data = json.loads(path.read_text(encoding="utf-8"))
                observed_artifact_types.add(data["artifact_type"])
                serialized = json.dumps(data, sort_keys=True)
                expected_schema_version = "1.1.0" if data["artifact_type"] == "requirements.control" else "1"

                self.assertEqual(expected_schema_version, data["schema_version"])
                self.assertNotRegex(serialized, re.compile("|".join(re.escape(name) for name in OFFICIAL_MARKDOWN_CONTROL_FILENAMES)))

        self.assertEqual(expected_artifact_types, observed_artifact_types)

    def test_runtime_example_declares_json_only_writable_runtime_outputs(self):
        runtime = json.loads(
            (ROOT / ".agents/skills/compiling-cybernetic-runtime-goals/assets/runtime.control.example.json").read_text(
                encoding="utf-8"
            )
        )

        self.assertEqual(
            [
                "requirements.control.json",
                "design.control.json",
                "goal.control.json",
                "plan.control.json",
                "review.control.json",
                "runtime.control.json",
            ],
            runtime["runtime"]["readonly_files"],
        )
        self.assertEqual(
            ["progress.jsonl", "runtime-status.json", "final-report.json"],
            runtime["runtime"]["writable_files"],
        )
        self.assertTrue(runtime["progress"]["append_only"])
        self.assertTrue(runtime["verifier"]["required_before_goal_achieved"])


if __name__ == "__main__":
    unittest.main()
