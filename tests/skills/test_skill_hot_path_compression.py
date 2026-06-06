import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def section_body(text: str, heading: str) -> str:
    pattern = re.compile(r"^(#{2,3})\s+(.+?)\s*$", re.MULTILINE)
    for match in pattern.finditer(text):
        title = match.group(2).strip().rstrip("#").strip()
        if title != heading:
            continue

        level = len(match.group(1))
        start = match.end()
        end = len(text)
        for next_match in pattern.finditer(text, start):
            if len(next_match.group(1)) <= level:
                end = next_match.start()
                break
        return text[start:end]
    raise AssertionError(f"missing section: {heading}")


def frontmatter_description(text: str) -> str:
    match = re.match(r"---\n(.*?)\n---", text, re.S)
    if not match:
        raise AssertionError("missing frontmatter")
    desc = re.search(r"^description:\s*['\"]?(.*?)['\"]?\s*$", match.group(1), re.M)
    if not desc:
        raise AssertionError("missing description")
    return desc.group(1)


class SkillHotPathCompressionTest(unittest.TestCase):
    def test_requirements_output_format_is_compact_and_script_owned(self):
        skill = read(".agents/skills/analyzing-cybernetic-requirements/SKILL.md")
        output_format = section_body(skill, "Output Format")

        self.assertLessEqual(len(output_format.splitlines()), 90)
        self.assertIn("predict_pregoal_handoff.py", output_format)
        self.assertNotIn(
            "/goal Execute the approved execution policy in docs/cybernetics/plans/YYYY-MM-DD-slug.md",
            output_format,
        )
        self.assertNotIn(
            "$writing-cybernetic-goals 使用 docs/cybernetics/requirements/YYYY-MM-DD-slug.md",
            output_format,
        )

    def test_orchestrator_hot_path_avoids_repeated_guard_commands(self):
        skill = read(".agents/skills/orchestrating-cybernetic-pregoal/SKILL.md")

        self.assertLessEqual(len(skill.splitlines()), 520)
        self.assertLessEqual(skill.count("scripts/orchestration_guard.py"), 2)
        self.assertIn("references/output-and-final-checks.md", skill)
        self.assertIn("references/orchestration-protocol.md", skill)

    def test_skill_descriptions_are_trigger_only_and_compact(self):
        for path in sorted((ROOT / ".agents/skills").glob("*/SKILL.md")):
            desc = frontmatter_description(path.read_text(encoding="utf-8"))
            self.assertLessEqual(len(desc), 300, str(path.relative_to(ROOT)))
            self.assertTrue(desc.startswith("Use when"), str(path.relative_to(ROOT)))


if __name__ == "__main__":
    unittest.main()
