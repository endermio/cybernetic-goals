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
            "docs/cybernetic-framework/invariant-artifact-consumer-matrix.md",
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
            "input role binding",
            "method",
            "purpose",
            "source material",
            "declared current state",
            "requested transformation",
            "primary object",
            "reference object",
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
            "## Input Role Binding",
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

        self.assertEqual("framing-cybernetic-intent", evals["skill_name"])
        self.assertIn("method-preference-is-not-purpose", ids)
        self.assertIn("dissatisfaction-is-not-execution-task", ids)
        self.assertIn("failure-experience-is-not-repair-goal", ids)
        self.assertIn("unstable-intent-asks-one-question", ids)
        self.assertIn("shared-understanding-before-task-candidate", ids)
        self.assertIn("chat-only-default-no-artifact", ids)
        self.assertIn("persistent-intent-brief-only-when-justified", ids)
        self.assertIn("completed-findings-become-repair-framing-not-audit", ids)
        self.assertIn("feasibility-inquiry-distinguishes-baseline-from-target", ids)

    def test_default_output_requires_input_role_binding(self):
        skill = self.read(".agents/skills/framing-cybernetic-intent/SKILL.md")

        self.assertIn("Input role binding:", skill)
        for field in (
            "- Source material:",
            "- Declared current state:",
            "- Requested transformation:",
            "- Primary object:",
            "- Reference object:",
            "- Method preference:",
            "- Non-goals:",
        ):
            self.assertIn(field, skill)

    def test_role_binding_prevents_source_material_from_becoming_task(self):
        skill = self.read(".agents/skills/framing-cybernetic-intent/SKILL.md")

        for rule in (
            "Do not turn source material into the task",
            "Do not turn a declared completed finding into a new investigation",
            "Do not treat current implementation as the primary object of a feasibility inquiry",
            "Ask one concise role-binding question",
        ):
            self.assertIn(rule, skill)

    def test_router_evals_cover_pre_task_method_preference_handoff(self):
        evals = json.loads(
            self.read(".agents/skills/routing-cybernetic-workflows/evals/evals.json")
        )
        ids = {item["id"] for item in evals["evals"]}
        target_id = "pre-task-method-preference-routes-to-intent-framing"

        self.assertIn(target_id, ids)
        target = next(
            item
            for item in evals["evals"]
            if item["id"] == target_id
        )
        target_text = json.dumps(target, ensure_ascii=False)

        self.assertEqual("routing-cybernetic-workflows", evals["skill_name"])
        self.assertIn("framing-cybernetic-intent", target_text)
        self.assertIn("method preference", target_text)
        self.assertIn("process distrust", target_text)
        self.assertIn("Does not classify as controlled_run", target_text)
        self.assertIn("Does not recommend orchestrating-cybernetic-pregoal yet", target_text)

    def test_integration_places_reference_pre_task_handoff(self):
        readme = self.read("README.md")
        router = self.read(".agents/skills/routing-cybernetic-workflows/SKILL.md")
        requirements = self.read(
            ".agents/skills/analyzing-cybernetic-requirements/SKILL.md"
        )
        matrix = self.read("docs/cybernetic-framework/invariant-artifact-consumer-matrix.md")

        self.assertIn("human situation", readme)
        self.assertIn("framing-cybernetic-intent", readme)
        self.assertIn("Turn a formed task or task candidate", requirements)
        for text in (router, requirements):
            folded = text.casefold()
            self.assertIn("framing-cybernetic-intent", text)
            self.assertIn("pre-task", folded)
            self.assertIn("formed task", folded)
        self.assertIn("INV-INT-001", matrix)
        self.assertIn("framing-cybernetic-intent", matrix)

    def test_orchestrator_requires_process_need_before_pregoal_artifacts(self):
        orchestrator = self.read(
            ".agents/skills/orchestrating-cybernetic-pregoal/SKILL.md"
        )
        folded = orchestrator.casefold()

        self.assertIn("Process Need Check", orchestrator)
        self.assertIn(
            "A user request to use a heavier or lighter process is not sufficient by itself.",
            orchestrator,
        )
        self.assertNotIn(
            "or the user explicitly chose a heavier process",
            orchestrator,
        )
        for term in (
            "pre-task intent",
            "ordinary direct work",
            "controlled run",
            "evidence/context/review budget",
        ):
            self.assertIn(term.casefold(), folded)
        self.assertIn("framing-cybernetic-intent", orchestrator)
        self.assertIn("routing-cybernetic-workflows", orchestrator)


if __name__ == "__main__":
    unittest.main()
