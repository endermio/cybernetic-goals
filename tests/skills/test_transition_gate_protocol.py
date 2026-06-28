import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from tests.skills.test_information_sufficiency_gate import (
    requirements_with_information_sufficiency,
    refresh_semantic_base,
)


ROOT = Path(__file__).resolve().parents[2]
INFO_LOOP = ROOT / ".agents/skills/analyzing-cybernetic-requirements/scripts/requirements_information_loop.py"
ORCHESTRATION_GUARD = ROOT / ".agents/skills/orchestrating-cybernetic-pregoal/scripts/orchestration_guard.py"
AMENDMENT_ORCHESTRATOR = ROOT / ".agents/skills/orchestrating-cybernetic-pregoal/scripts/amendment_orchestrator.py"


def run_script(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["python3", *map(str, args)],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )


def write_requirements(run_dir: Path, requirements: dict) -> None:
    (run_dir / "requirements.control.json").write_text(json.dumps(requirements, indent=2), encoding="utf-8")


class TransitionGateProtocolTest(unittest.TestCase):
    def test_information_gate_nonterminal_actions_prohibit_approval_and_require_rerun(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            req = requirements_with_information_sufficiency(status="needs_information_gathering")
            check = req["approved_control"]["information_sufficiency_check"]
            check["facts"][0]["current_status"] = "needs_information_gathering"
            check["collection_actions"] = [
                {
                    "action_id": "IA-client-minimal-example",
                    "fact_id": "F-client-minimal-example",
                    "action_type": "run_no_side_effect_probe",
                    "status": "planned",
                    "why_safe_or_needed": "A local probe is required before design.",
                    "evidence_ref": "evidence/client_minimal_example.json",
                    "allow_automatic_execution": True,
                }
            ]
            refresh_semantic_base(req)
            write_requirements(run_dir, req)

            result = run_script(INFO_LOOP, "--run-dir", str(run_dir), "--json")

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual("transition-gate/v1", payload["gate_protocol"])
            self.assertEqual("requirements-information-sufficiency", payload["gate_id"])
            self.assertEqual("RunInformationGathering", payload["next_action"])
            self.assertFalse(payload["terminal"])
            self.assertTrue(payload["rerun_required"])
            self.assertFalse(payload["approval_allowed"])
            self.assertFalse(payload["handoff_allowed"])
            self.assertFalse(payload["may_ask_user"])

    def test_information_gate_user_input_allows_question_but_not_approval(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            req = requirements_with_information_sufficiency(status="needs_user_input")
            check = req["approved_control"]["information_sufficiency_check"]
            check["facts"][0]["current_status"] = "needs_user_input"
            check["collection_actions"] = [
                {
                    "action_id": "IA-client-credential",
                    "fact_id": "F-client-minimal-example",
                    "action_type": "ask_user",
                    "status": "planned",
                    "why_safe_or_needed": "The credential is not available locally.",
                    "evidence_ref": "evidence/client_credential_decision.json",
                    "question": "Provide the client credential.",
                }
            ]
            refresh_semantic_base(req)
            write_requirements(run_dir, req)

            result = run_script(INFO_LOOP, "--run-dir", str(run_dir), "--json")

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual("AskUserForInformation", payload["next_action"])
            self.assertFalse(payload["terminal"])
            self.assertTrue(payload["rerun_required"])
            self.assertTrue(payload["may_ask_user"])
            self.assertFalse(payload["approval_allowed"])
            self.assertFalse(payload["handoff_allowed"])

    def test_information_gate_ready_for_approval_is_terminal_for_requirements_analysis(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            req = requirements_with_information_sufficiency(status="satisfied")
            req["status"] = "pending_approval"
            refresh_semantic_base(req)
            write_requirements(run_dir, req)

            result = run_script(INFO_LOOP, "--run-dir", str(run_dir), "--json")

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual("ReadyForUserApproval", payload["next_action"])
            self.assertTrue(payload["terminal"])
            self.assertFalse(payload["rerun_required"])
            self.assertTrue(payload["approval_allowed"])
            self.assertFalse(payload["handoff_allowed"])
            self.assertTrue(payload["may_ask_user"])

    def test_orchestration_guard_uses_transition_gate_fields_for_blocked_handoff(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            req = requirements_with_information_sufficiency(status="missing")
            write_requirements(run_dir, req)

            result = run_script(
                ORCHESTRATION_GUARD,
                "--state",
                "before-design",
                "--run-dir",
                str(run_dir),
                "--json",
            )

            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual("transition-gate/v1", payload["gate_protocol"])
            self.assertEqual("pregoal-orchestration", payload["gate_id"])
            self.assertEqual("RunInformationSufficiencyCheck", payload["next_action"])
            self.assertEqual("RunInformationSufficiencyCheck", payload["next_allowed_action"])
            self.assertFalse(payload["terminal"])
            self.assertTrue(payload["rerun_required"])
            self.assertFalse(payload["approval_allowed"])
            self.assertFalse(payload["handoff_allowed"])

    def test_amendment_orchestrator_uses_transition_gate_fields_even_on_invalid_run(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            result = run_script(AMENDMENT_ORCHESTRATOR, "--run-dir", tmpdir)

            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual("transition-gate/v1", payload["gate_protocol"])
            self.assertEqual("amendment-orchestrator", payload["gate_id"])
            self.assertEqual("FixJsonControlRun", payload["next_action"])
            self.assertEqual("FixJsonControlRun", payload["next_allowed_action"])
            self.assertFalse(payload["terminal"])
            self.assertTrue(payload["rerun_required"])
            self.assertFalse(payload["approval_allowed"])
            self.assertFalse(payload["handoff_allowed"])

    def test_hot_path_docs_reference_shared_transition_gate_protocol(self):
        paths = [
            ".agents/skills/analyzing-cybernetic-requirements/SKILL.md",
            ".agents/skills/orchestrating-cybernetic-pregoal/SKILL.md",
            ".agents/skills/reviewing-cybernetic-control-structures/SKILL.md",
            ".agents/skills/using-control-json/SKILL.md",
        ]
        for path in paths:
            with self.subTest(path=path):
                text = (ROOT / path).read_text(encoding="utf-8")
                self.assertIn("transition-gate-protocol.md", text)

        protocol = (ROOT / ".agents/skills/references/transition-gate-protocol.md").read_text(encoding="utf-8")
        for field in (
            "terminal",
            "rerun_required",
            "approval_allowed",
            "handoff_allowed",
            "may_ask_user",
            "requires_independent_review",
        ):
            self.assertIn(field, protocol)


if __name__ == "__main__":
    unittest.main()
