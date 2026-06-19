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


def body_word_count(text: str) -> int:
    body = text.split("---", 2)[-1] if text.startswith("---") else text
    return len(re.findall(r"[A-Za-z0-9_`/$.-]+|[\u4e00-\u9fff]", body))


class SkillHotPathCompressionTest(unittest.TestCase):
    def test_skill_main_files_stay_as_hot_path_indexes(self):
        max_lines = 260
        max_section_lines = 90
        max_words = 650
        for path in sorted((ROOT / ".agents/skills").glob("*/SKILL.md")):
            with self.subTest(path=path.relative_to(ROOT)):
                text = path.read_text(encoding="utf-8")
                self.assertLessEqual(len(text.splitlines()), max_lines)
                self.assertLessEqual(body_word_count(text), max_words)

                headings = list(re.finditer(r"^(#{2,3})\s+(.+?)\s*$", text, re.MULTILINE))
                for index, heading in enumerate(headings):
                    end = headings[index + 1].start() if index + 1 < len(headings) else len(text)
                    section_lines = text[heading.start() : end].splitlines()
                    self.assertLessEqual(
                        len(section_lines),
                        max_section_lines,
                        f"{path.relative_to(ROOT)} section {heading.group(2)!r}",
                    )

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

        self.assertLessEqual(len(skill.splitlines()), 260)
        self.assertLessEqual(skill.count("scripts/orchestration_guard.py"), 2)
        self.assertIn("references/output-and-final-checks.md", skill)
        self.assertIn("references/orchestration-protocol.md", skill)

    def test_entry_model_uses_controlled_run_not_levels(self):
        skill = read(".agents/skills/routing-cybernetic-workflows/SKILL.md")

        self.assertIn("controlled_run", skill)
        self.assertIn("strategy_policy", skill)
        self.assertIn("human_gate", skill)
        self.assertIn("live_gate", skill)
        self.assertIn("counterexample_gate", skill)
        self.assertNotIn("### Level", skill)
        self.assertNotIn("Routing decision: Level", skill)
        self.assertNotIn("Level 4", skill)

    def test_compiler_hot_path_is_generation_aware(self):
        skill = read(".agents/skills/compiling-cybernetic-runtime-goals/SKILL.md")

        self.assertLessEqual(body_word_count(skill), 650)
        self.assertIn("run.control.json", skill)
        self.assertIn("current_generation", skill)
        self.assertIn("strategy_policy", skill)
        self.assertNotIn("Inputs:\n\n- `requirements.control.json` with status Complete", skill)
        self.assertNotIn("approved control chain paths for requirements, design when present, goal, execution policy, and review", skill)

    def test_hot_paths_do_not_teach_old_long_runtime_goal_pattern(self):
        hot_paths = [
            ".agents/skills/orchestrating-cybernetic-pregoal/references/output-and-final-checks.md",
            ".agents/skills/analyzing-cybernetic-requirements/scripts/predict_pregoal_handoff.py",
            ".agents/skills/writing-cybernetic-goals/references/control-contract-rules.md",
        ]

        for path in hot_paths:
            text = read(path)
            self.assertNotIn(
                "/goal Execute the approved execution policy in",
                text,
                path,
            )
            self.assertNotIn(".goal.md", text, path)
            self.assertNotIn("runtime-goals/", text, path)

        orchestrator_checks = read(
            ".agents/skills/orchestrating-cybernetic-pregoal/references/output-and-final-checks.md"
        )
        self.assertIn("User-entered short `/goal` pointer", orchestrator_checks)
        self.assertIn("runtime.control.json", orchestrator_checks)
        self.assertIn("using-control-json", orchestrator_checks)

        control_rules = read(".agents/skills/writing-cybernetic-goals/references/control-contract-rules.md")
        self.assertIn("/goal Execute the runtime control JSON at", control_rules)
        self.assertIn("using-control-json", control_rules)

    def test_skill_descriptions_are_trigger_only_and_compact(self):
        for path in sorted((ROOT / ".agents/skills").glob("*/SKILL.md")):
            desc = frontmatter_description(path.read_text(encoding="utf-8"))
            self.assertLessEqual(len(desc), 300, str(path.relative_to(ROOT)))
            self.assertTrue(desc.startswith("Use when"), str(path.relative_to(ROOT)))


if __name__ == "__main__":
    unittest.main()
