import json
import re
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


class SkillRepositoryIntegrityTest(unittest.TestCase):
    def test_manifest_includes_release_surface_files(self):
        manifest_paths = set(
            line.strip()
            for line in (ROOT / "MANIFEST.txt").read_text(encoding="utf-8").splitlines()
            if line.strip()
        )
        tracked_paths = subprocess.check_output(
            [
                "git",
                "ls-files",
                ".agents/skills",
                "docs/cybernetic-framework",
                "observability",
                "scripts",
                "tests",
                "README.md",
                "MANIFEST.txt",
                ".github",
            ],
            cwd=ROOT,
            text=True,
        ).splitlines()
        required_paths = set(tracked_paths)
        required_paths.add("tests/skills/test_skill_repository_integrity.py")

        missing = sorted(required_paths - manifest_paths)

        self.assertEqual([], missing)

    def test_skill_evals_use_object_schema(self):
        for eval_path in sorted((ROOT / ".agents/skills").glob("*/evals/evals.json")):
            with self.subTest(path=eval_path.relative_to(ROOT)):
                data = json.loads(eval_path.read_text(encoding="utf-8"))
                skill_name = eval_path.parents[1].name

                self.assertIsInstance(data, dict)
                self.assertEqual(skill_name, data.get("skill_name"))
                self.assertIsInstance(data.get("evals"), list)
                self.assertGreater(len(data["evals"]), 0)

    def test_skill_descriptions_stay_trigger_focused(self):
        forbidden_process_summaries = (
            "Analyzes ",
            "Creates ",
            "Produces ",
            "Coordinates ",
            "Reviews ",
            "Defines ",
        )

        for skill_path in sorted((ROOT / ".agents/skills").glob("*/SKILL.md")):
            with self.subTest(path=skill_path.relative_to(ROOT)):
                text = skill_path.read_text(encoding="utf-8")
                match = re.search(r"description:\s*'([^']*)'", text)

                self.assertIsNotNone(match)
                description = match.group(1)
                self.assertLessEqual(len(description), 500)
                self.assertTrue(description.startswith("Use when "))
                for phrase in forbidden_process_summaries:
                    self.assertNotIn(phrase, description)


if __name__ == "__main__":
    unittest.main()
