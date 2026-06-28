import hashlib
import json
import re
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".agents/skills/_shared"))

from information_sufficiency import canonical_json_hash, information_sufficiency_errors  # noqa: E402

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
                if data["artifact_type"] == "requirements.control":
                    self.assertIn("information_sufficiency_check", data["approved_control"])
                    self.assertIn(data["approved_control"]["information_sufficiency_check"]["status"], {"satisfied", "not_required"})
                self.assertNotRegex(serialized, re.compile("|".join(re.escape(name) for name in OFFICIAL_MARKDOWN_CONTROL_FILENAMES)))

        self.assertEqual(expected_artifact_types, observed_artifact_types)

    def test_requirements_example_information_sufficiency_gate_is_executable(self):
        requirements_path = ROOT / ".agents/skills/analyzing-cybernetic-requirements/assets/requirements.control.example.json"
        requirements = json.loads(requirements_path.read_text(encoding="utf-8"))
        review = requirements["approved_control"]["information_sufficiency_check"]["counterexample_review"]
        reviewer = review["reviewer"]
        reviewed_hashes = {
            "requirements.control.json": canonical_json_hash(requirements)
        }

        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            (run_dir / "evidence").mkdir()
            prompt_ref = "evidence/information_sufficiency_counterexample.prompt.txt"
            transcript_ref = "evidence/information_sufficiency_counterexample.transcript.txt"
            (run_dir / prompt_ref).write_text("information sufficiency counterexample review", encoding="utf-8")
            (run_dir / transcript_ref).write_text(
                "independent information sufficiency reviewer transcript",
                encoding="utf-8",
            )
            prompt_hash = "sha256:" + hashlib.sha256((run_dir / prompt_ref).read_bytes()).hexdigest()
            transcript_hash = "sha256:" + hashlib.sha256((run_dir / transcript_ref).read_bytes()).hexdigest()
            (run_dir / "requirements.control.json").write_text(
                json.dumps(requirements, indent=2),
                encoding="utf-8",
            )
            (run_dir / reviewer["evidence_ref"]).write_text(
                json.dumps(
                    {
                        "artifact_type": "information_sufficiency.counterexample_review.evidence",
                        "independent_review": True,
                        "status": review["status"],
                        "verdict": review["verdict"],
                        "reviewer": {"kind": reviewer["kind"], "id": reviewer["id"]},
                        "reviewer_session": {
                            "kind": reviewer["kind"],
                            "id": reviewer["id"],
                            "transcript_ref": transcript_ref,
                            "transcript_hash": transcript_hash,
                        },
                        "review_request": {
                            "prompt_ref": prompt_ref,
                            "prompt_hash": prompt_hash,
                            "reviewed_artifact_hashes": reviewed_hashes,
                        },
                        "checked_facts": review["checked_facts"],
                        "checked_transformations": review["checked_transformations"],
                        "findings": review["findings"],
                        "reviewed_artifact_hashes": reviewed_hashes,
                    },
                    indent=2,
                ),
                encoding="utf-8",
            )

            self.assertEqual([], information_sufficiency_errors(requirements, run_dir))

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
