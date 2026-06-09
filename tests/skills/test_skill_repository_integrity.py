import json
import re
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


class SkillRepositoryIntegrityTest(unittest.TestCase):
    def test_manifest_includes_release_place_files(self):
        manifest_paths = set(
            line.strip()
            for line in (ROOT / "MANIFEST.txt").read_text(encoding="utf-8").splitlines()
            if line.strip()
        )
        tracked_paths = subprocess.check_output(
            [
                "git",
                "ls-files",
                "--cached",
                "--others",
                "--exclude-standard",
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
        required_paths = {
            path
            for path in tracked_paths
            if (ROOT / path).exists()
            and "__pycache__" not in path
            and not path.endswith(".pyc")
        }
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

    def test_skill_limits_are_positive_first(self):
        defensive_openers = (
            "This skill must not:",
            "It must not:",
        )
        contrastive_heading = re.compile(r"^## .*Do Not", re.MULTILINE)

        for skill_path in sorted((ROOT / ".agents/skills").glob("*/SKILL.md")):
            with self.subTest(path=skill_path.relative_to(ROOT)):
                text = skill_path.read_text(encoding="utf-8")
                for opener in defensive_openers:
                    self.assertNotIn(opener, text)
                self.assertIsNone(contrastive_heading.search(text))

    def test_skill_docs_limit_contrastive_idiom_density(self):
        contrastive = re.compile(
            r"\bnot\b.{0,140}\bbut\b|\brather than\b|\binstead of\b",
            re.IGNORECASE,
        )

        for skill_path in sorted((ROOT / ".agents/skills").glob("*/SKILL.md")):
            with self.subTest(path=skill_path.relative_to(ROOT)):
                text = skill_path.read_text(encoding="utf-8")
                matches = contrastive.findall(text)
                self.assertLessEqual(len(matches), 2, matches)


if __name__ == "__main__":
    unittest.main()
