import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
INVENTORY = ROOT / "tests/fixtures/cybernetics/json_only_control_regression_inventory.json"


EXPECTED_FAILURE_MODES = {
    "markdown_official_input_accepted",
    "json_sidecar_accepted_while_markdown_authoritative",
    "approved_json_mutated_at_runtime",
    "goal_achieved_verifier_bypass",
    "required_outcome_coverage_gap",
    "supporting_only_counted_as_progress",
    "not_done_report_treated_as_success",
    "authority_shrink",
    "missing_review_checks",
}

EXPECTED_OLD_ACCIDENT_SURFACES = {
    "required_outcome_coverage",
    "work_assignment_context",
    "required_answer_path",
    "what_counts_as_done",
    "execution_horizon_authority",
    "artifact_hygiene",
}


class JsonControlRegressionInventoryTest(unittest.TestCase):
    def load_inventory(self) -> dict:
        self.assertTrue(INVENTORY.exists(), f"missing inventory fixture: {INVENTORY}")
        return json.loads(INVENTORY.read_text(encoding="utf-8"))

    def test_inventory_declares_json_regression_port_status(self):
        inventory = self.load_inventory()

        self.assertEqual("legacy_accident_inventory_for_json_regressions", inventory["inventory_status"])
        self.assertEqual("implemented_in_json_regression_tests", inventory["json_regression_port_status"])
        self.assertTrue(inventory["does_not_claim_full_goal_complete"])
        self.assertIn("retired_legacy_control_artifacts", inventory)
        self.assertNotIn("runtime_goal", inventory)
        self.assertNotIn("execution_policy", inventory)

    def test_inventory_covers_required_failure_classes(self):
        inventory = self.load_inventory()
        modes = {mode["id"]: mode for mode in inventory["failure_modes"]}

        self.assertEqual(EXPECTED_FAILURE_MODES, set(modes))
        for mode_id, mode in modes.items():
            with self.subTest(mode=mode_id):
                self.assertIn(mode["required_step"], {"S5", "S6", "S7", "S8", "S9"})
                self.assertTrue(mode["failure_class"])
                self.assertTrue(mode["json_regression_requirement"])
                self.assertGreaterEqual(len(mode["future_assertions"]), 1)
                self.assertTrue(
                    mode.get("legacy_sources") or mode.get("control_sources"),
                    "mode must cite existing regression tests or approved control sources",
                )

    def test_inventory_maps_old_accident_surfaces_to_json_regression_requirements(self):
        inventory = self.load_inventory()
        surfaces = {surface["id"]: surface for surface in inventory["old_accident_surfaces"]}

        self.assertEqual(EXPECTED_OLD_ACCIDENT_SURFACES, set(surfaces))
        for surface_id, surface in surfaces.items():
            with self.subTest(surface=surface_id):
                self.assertIn("retired_source_test_file", surface)
                self.assertTrue(surface["representative_tests"])
                self.assertTrue(surface["json_replacement_tests"])
                for replacement in surface["json_replacement_tests"]:
                    replacement_path = ROOT / replacement["file"]
                    self.assertTrue(replacement_path.exists(), f"missing JSON replacement test: {replacement_path}")
                    replacement_text = replacement_path.read_text(encoding="utf-8")
                    for test_name in replacement["tests"]:
                        self.assertIn(test_name, replacement_text)
                self.assertTrue(surface["json_port_groundwork"])


if __name__ == "__main__":
    unittest.main()
