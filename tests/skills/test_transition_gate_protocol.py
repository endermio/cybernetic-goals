import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from tests.skills.test_information_sufficiency_gate import (
    requirements_with_information_sufficiency,
    refresh_semantic_base,
)
from tests.skills.test_reviewed_replanning_control import write_strategy_run


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


def write_information_evidence(run_dir: Path) -> None:
    evidence_dir = run_dir / "evidence"
    evidence_dir.mkdir(parents=True, exist_ok=True)
    (evidence_dir / "client_minimal_example.json").write_text(
        json.dumps({"status": "pass", "observation": "client ok"}, indent=2),
        encoding="utf-8",
    )
    (evidence_dir / "information_sufficiency_counterexample.json").write_text(
        json.dumps({"status": "pass", "verdict": "approved"}, indent=2),
        encoding="utf-8",
    )


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
                    "command": ["python3", "-c", "print('client ok')"],
                    "working_dir": ".",
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

    def test_information_gate_missing_collection_actions_routes_to_repair_not_empty_action(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            req = requirements_with_information_sufficiency(status="needs_information_gathering")
            check = req["approved_control"]["information_sufficiency_check"]
            check["facts"][0]["current_status"] = "needs_information_gathering"
            check.pop("collection_actions", None)
            refresh_semantic_base(req)
            write_requirements(run_dir, req)

            result = run_script(INFO_LOOP, "--run-dir", str(run_dir), "--json")

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual("RepairRequirementsInformationState", payload["next_action"])
            self.assertFalse(payload["terminal"])
            self.assertTrue(payload["rerun_required"])
            self.assertFalse(payload["approval_allowed"])
            self.assertFalse(payload["handoff_allowed"])
            self.assertIn("collection_actions", "\n".join(payload["blocking_reasons"]))

    def test_information_gate_status_user_input_requires_user_action(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            req = requirements_with_information_sufficiency(status="needs_user_input")
            check = req["approved_control"]["information_sufficiency_check"]
            check["facts"][0]["current_status"] = "needs_user_input"
            check["collection_actions"] = [
                {
                    "action_id": "IA-read-only",
                    "fact_id": "F-client-minimal-example",
                    "action_type": "read_source",
                    "status": "planned",
                    "why_safe_or_needed": "This is safe but does not ask the user.",
                    "evidence_ref": "evidence/client_source_read.json",
                    "paths": ["client/"],
                }
            ]
            refresh_semantic_base(req)
            write_requirements(run_dir, req)

            result = run_script(INFO_LOOP, "--run-dir", str(run_dir), "--json")

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual("RepairRequirementsInformationState", payload["next_action"])
            self.assertFalse(payload["terminal"])
            self.assertEqual([], payload["user_actions"])
            self.assertIn("needs_user_input", "\n".join(payload["blocking_reasons"]))

    def test_information_gate_safe_probe_requires_executable_detail(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            req = requirements_with_information_sufficiency(status="needs_information_gathering")
            check = req["approved_control"]["information_sufficiency_check"]
            check["facts"][0]["current_status"] = "needs_information_gathering"
            check["collection_actions"] = [
                {
                    "action_id": "IA-empty-probe",
                    "fact_id": "F-client-minimal-example",
                    "action_type": "run_no_side_effect_probe",
                    "status": "planned",
                    "why_safe_or_needed": "A probe is needed, but no command was provided.",
                    "evidence_ref": "evidence/client_probe.json",
                }
            ]
            refresh_semantic_base(req)
            write_requirements(run_dir, req)

            result = run_script(INFO_LOOP, "--run-dir", str(run_dir), "--json")

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual("RepairRequirementsInformationState", payload["next_action"])
            self.assertFalse(payload["terminal"])
            self.assertEqual([], payload["automatic_actions"])
            self.assertIn("command", "\n".join(payload["blocking_reasons"]))

    def test_information_gate_satisfied_status_requires_passed_counterexample_review(self):
        for requirements_status, forbidden_next_action in (
            ("pending_approval", "ReadyForUserApproval"),
            ("approved", "ReadyForPreGoalHandoff"),
        ):
            with self.subTest(requirements_status=requirements_status):
                with tempfile.TemporaryDirectory() as tmpdir:
                    run_dir = Path(tmpdir)
                    req = requirements_with_information_sufficiency(status="satisfied")
                    req["status"] = requirements_status
                    req["approved_control"]["information_sufficiency_check"]["counterexample_review"] = {
                        "status": "fail",
                        "verdict": "needs_revision",
                        "reviewer": {
                            "kind": "subagent",
                            "id": "information-sufficiency-reviewer",
                            "evidence_ref": "evidence/information_sufficiency_counterexample.json",
                        },
                        "checked_facts": ["F-client-minimal-example"],
                        "checked_transformations": [
                            "source_requirements->information_sufficiency_facts",
                            "required_outcomes->information_sufficiency_facts",
                            "information_sufficiency_facts->design_plan_entry",
                        ],
                        "findings": ["The minimal client behavior fact is not actually evidenced."],
                    }
                    refresh_semantic_base(req)
                    write_requirements(run_dir, req)
                    write_information_evidence(run_dir)

                    result = run_script(INFO_LOOP, "--run-dir", str(run_dir), "--json")

                    self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                    payload = json.loads(result.stdout)
                    self.assertNotEqual(forbidden_next_action, payload["next_action"])
                    self.assertEqual("RunInformationCounterexampleReview", payload["next_action"])
                    self.assertFalse(payload["terminal"])
                    self.assertFalse(payload["approval_allowed"])
                    self.assertFalse(payload["handoff_allowed"])

    def test_information_gate_satisfied_status_requires_satisfied_blocking_facts(self):
        for requirements_status, forbidden_next_action in (
            ("pending_approval", "ReadyForUserApproval"),
            ("approved", "ReadyForPreGoalHandoff"),
        ):
            with self.subTest(requirements_status=requirements_status):
                with tempfile.TemporaryDirectory() as tmpdir:
                    run_dir = Path(tmpdir)
                    req = requirements_with_information_sufficiency(status="satisfied")
                    req["status"] = requirements_status
                    fact = req["approved_control"]["information_sufficiency_check"]["facts"][0]
                    fact["current_status"] = "missing"
                    refresh_semantic_base(req)
                    write_requirements(run_dir, req)
                    write_information_evidence(run_dir)

                    result = run_script(INFO_LOOP, "--run-dir", str(run_dir), "--json")

                    self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                    payload = json.loads(result.stdout)
                    self.assertNotEqual(forbidden_next_action, payload["next_action"])
                    self.assertEqual("RepairRequirementsInformationState", payload["next_action"])
                    self.assertFalse(payload["terminal"])
                    self.assertFalse(payload["approval_allowed"])
                    self.assertFalse(payload["handoff_allowed"])
                    self.assertIn("blocks handoff", "\n".join(payload["blocking_reasons"]))

    def test_information_gate_satisfied_status_requires_complete_fact_and_review_shape(self):
        mutations = [
            lambda req: req["approved_control"]["information_sufficiency_check"]["facts"][0].pop("acceptable_evidence"),
            lambda req: req["approved_control"]["information_sufficiency_check"]["facts"][0].pop("statement"),
            lambda req: req["approved_control"]["information_sufficiency_check"]["facts"][0].update(
                {"blocks_design_or_plan_if_missing": "yes"}
            ),
            lambda req: req["approved_control"]["information_sufficiency_check"]["counterexample_review"]["reviewer"].update(
                {"kind": "self"}
            ),
            lambda req: req["approved_control"]["information_sufficiency_check"]["counterexample_review"].pop("findings"),
        ]
        for mutate in mutations:
            with self.subTest(mutation=mutations.index(mutate)):
                with tempfile.TemporaryDirectory() as tmpdir:
                    run_dir = Path(tmpdir)
                    req = requirements_with_information_sufficiency(status="satisfied")
                    req["status"] = "approved"
                    mutate(req)
                    refresh_semantic_base(req)
                    write_requirements(run_dir, req)
                    write_information_evidence(run_dir)

                    result = run_script(INFO_LOOP, "--run-dir", str(run_dir), "--json")

                    self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                    payload = json.loads(result.stdout)
                    self.assertEqual("RepairRequirementsInformationState", payload["next_action"])
                    self.assertFalse(payload["terminal"])
                    self.assertFalse(payload["handoff_allowed"])

    def test_information_gate_ignores_non_planned_collection_actions_as_next_actions(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            req = requirements_with_information_sufficiency(status="needs_information_gathering")
            check = req["approved_control"]["information_sufficiency_check"]
            check["facts"][0]["current_status"] = "needs_information_gathering"
            check["collection_actions"] = [
                {
                    "action_id": "IA-completed-probe",
                    "fact_id": "F-client-minimal-example",
                    "action_type": "run_no_side_effect_probe",
                    "status": "completed",
                    "why_safe_or_needed": "This already ran and cannot be the next action.",
                    "evidence_ref": "evidence/client_minimal_example.json",
                    "command": ["python3", "-c", "print('client ok')"],
                    "working_dir": ".",
                    "allow_automatic_execution": True,
                }
            ]
            refresh_semantic_base(req)
            write_requirements(run_dir, req)

            result = run_script(INFO_LOOP, "--run-dir", str(run_dir), "--json")

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual("RepairRequirementsInformationState", payload["next_action"])
            self.assertFalse(payload["terminal"])
            self.assertEqual([], payload["automatic_actions"])
            self.assertIn("planned", "\n".join(payload["blocking_reasons"]))

    def test_information_gate_collection_action_must_target_current_unsatisfied_fact(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            req = requirements_with_information_sufficiency(status="needs_information_gathering")
            check = req["approved_control"]["information_sufficiency_check"]
            check["facts"].append(
                {
                    "fact_id": "F-satisfied-side-fact",
                    "statement": "An unrelated side fact is already satisfied.",
                    "derived_from": {
                        "source_requirements": ["SR-client-minimal-example"],
                        "required_outcomes": ["O-client-integration"],
                    },
                    "why_needed": "This side fact is not the current blocker.",
                    "acceptable_evidence": [
                        {"kind": "direct_observation", "description": "Already observed."}
                    ],
                    "current_status": "satisfied",
                    "evidence_ref": "evidence/client_minimal_example.json",
                    "blocks_design_or_plan_if_missing": True,
                }
            )
            check["facts"][0]["current_status"] = "needs_information_gathering"
            check["collection_actions"] = [
                {
                    "action_id": "IA-stale-side-fact",
                    "fact_id": "F-satisfied-side-fact",
                    "action_type": "run_no_side_effect_probe",
                    "status": "planned",
                    "why_safe_or_needed": "This action is stale and does not address the current blocker.",
                    "evidence_ref": "evidence/stale_side_fact.json",
                    "command": ["python3", "-c", "print('side ok')"],
                    "working_dir": ".",
                    "allow_automatic_execution": True,
                }
            ]
            refresh_semantic_base(req)
            write_requirements(run_dir, req)

            result = run_script(INFO_LOOP, "--run-dir", str(run_dir), "--json")

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual("RepairRequirementsInformationState", payload["next_action"])
            self.assertFalse(payload["terminal"])
            self.assertEqual([], payload["automatic_actions"])
            self.assertIn("current_status", "\n".join(payload["blocking_reasons"]))

    def test_information_gate_safe_probe_requires_explicit_automatic_authorization(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            req = requirements_with_information_sufficiency(status="needs_information_gathering")
            check = req["approved_control"]["information_sufficiency_check"]
            check["facts"][0]["current_status"] = "needs_information_gathering"
            check["collection_actions"] = [
                {
                    "action_id": "IA-no-auto-probe",
                    "fact_id": "F-client-minimal-example",
                    "action_type": "run_no_side_effect_probe",
                    "status": "planned",
                    "why_safe_or_needed": "The probe needs explicit authorization.",
                    "evidence_ref": "evidence/client_probe.json",
                    "command": ["python3", "-c", "print('client ok')"],
                    "working_dir": ".",
                    "allow_automatic_execution": False,
                }
            ]
            refresh_semantic_base(req)
            write_requirements(run_dir, req)

            result = run_script(INFO_LOOP, "--run-dir", str(run_dir), "--json")

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual("RepairRequirementsInformationState", payload["next_action"])
            self.assertFalse(payload["terminal"])
            self.assertEqual([], payload["automatic_actions"])
            self.assertIn("allow_automatic_execution", "\n".join(payload["blocking_reasons"]))

    def test_information_gate_collection_action_evidence_ref_must_stay_in_run_dir(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            req = requirements_with_information_sufficiency(status="needs_information_gathering")
            check = req["approved_control"]["information_sufficiency_check"]
            check["facts"][0]["current_status"] = "needs_information_gathering"
            check["collection_actions"] = [
                {
                    "action_id": "IA-outside-evidence",
                    "fact_id": "F-client-minimal-example",
                    "action_type": "run_no_side_effect_probe",
                    "status": "planned",
                    "why_safe_or_needed": "The probe evidence must be recorded in the run directory.",
                    "evidence_ref": "../outside.json",
                    "command": ["python3", "-c", "print('client ok')"],
                    "working_dir": ".",
                    "allow_automatic_execution": True,
                }
            ]
            refresh_semantic_base(req)
            write_requirements(run_dir, req)

            result = run_script(INFO_LOOP, "--run-dir", str(run_dir), "--json")

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual("RepairRequirementsInformationState", payload["next_action"])
            self.assertFalse(payload["terminal"])
            self.assertEqual([], payload["automatic_actions"])
            self.assertIn("evidence_ref", "\n".join(payload["blocking_reasons"]))

    def test_information_gate_ready_for_approval_is_terminal_for_requirements_analysis(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            req = requirements_with_information_sufficiency(status="satisfied")
            req["status"] = "pending_approval"
            refresh_semantic_base(req)
            write_requirements(run_dir, req)
            write_information_evidence(run_dir)

            result = run_script(INFO_LOOP, "--run-dir", str(run_dir), "--json")

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual("ReadyForUserApproval", payload["next_action"])
            self.assertTrue(payload["terminal"])
            self.assertFalse(payload["rerun_required"])
            self.assertTrue(payload["approval_allowed"])
            self.assertFalse(payload["handoff_allowed"])
            self.assertTrue(payload["may_ask_user"])

    def test_information_gate_ready_for_approval_requires_pending_approval_status(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            req = requirements_with_information_sufficiency(status="satisfied")
            req["status"] = "draft"
            refresh_semantic_base(req)
            write_requirements(run_dir, req)
            write_information_evidence(run_dir)

            result = run_script(INFO_LOOP, "--run-dir", str(run_dir), "--json")

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual("RepairRequirementsInformationState", payload["next_action"])
            self.assertFalse(payload["terminal"])
            self.assertFalse(payload["approval_allowed"])
            self.assertIn("pending_approval", "\n".join(payload["blocking_reasons"]))

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

    def test_amendment_orchestrator_missing_patch_routes_to_patch_repair_not_review(self):
        event = {
            "event_type": "control.amendment.proposed",
            "schema_version": "1.0.0",
            "occurred_at": "2026-06-10T00:00:00Z",
            "runtime_generation": "gen-000",
            "amendment_id": "A1",
            "reason": "current strategy cannot produce required evidence",
            "triggering_observation": "current strategy produced substitute evidence",
            "affected_stages": ["plan", "runtime"],
            "affected_source_requirements": ["SR-target-startup"],
            "semantic_base_change": False,
            "required_outcomes_changed": False,
            "authority_expanded": False,
            "proposed_changes": ["replace substitute evidence with producing strategy"],
            "review_required": ["intent-preservation", "required-outcome-coverage"],
            "patch_ref": "amendments/A1.patch.json",
        }
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            write_strategy_run(run_dir, progress_events=[event], strategy_policy="reviewed_replanning")

            result = run_script(AMENDMENT_ORCHESTRATOR, "--run-dir", str(run_dir))

            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual("FixAmendmentPatch", payload["next_action"])
            self.assertFalse(payload["terminal"])
            self.assertTrue(payload["rerun_required"])
            self.assertFalse(payload["requires_independent_review"])
            self.assertIn("patch file is missing", "\n".join(payload["errors"]))

    def test_amendment_orchestrator_no_proposal_is_terminal_wait_state(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)
            write_strategy_run(run_dir, progress_events=[], strategy_policy="reviewed_replanning")

            result = run_script(AMENDMENT_ORCHESTRATOR, "--run-dir", str(run_dir))

            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual("AwaitAmendmentProposal", payload["next_action"])
            self.assertTrue(payload["terminal"])
            self.assertFalse(payload["rerun_required"])
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
