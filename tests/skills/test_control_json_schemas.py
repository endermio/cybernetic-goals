import copy
import hashlib
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCHEMA_DIR = ROOT / "schemas/control-json"
DELEGATION_WORKFLOW_REGISTRY = ROOT / ".agents/skills/references/delegation-workflow-registry.json"


def review_check(check_id: str, evidence: list[str], checked_transformations: list[str] | None = None) -> dict:
    return {
        "check_id": check_id,
        "status": "pass",
        "verdict": "approved",
        "return_to_stage": None,
        "evidence": evidence,
        "findings": [],
        "required_changes": [],
        "checked_transformations": checked_transformations
        or ["requirements->design", "design->goal", "goal->plan", "plan->runtime"],
    }


SCHEMA_FIXTURES = {
    "requirements.control.schema.json": {
        "artifact_type": "requirements.control",
        "schema_version": "1.0.0",
        "status": "approved",
        "approved_control": {
            "human_purpose": "move official control facts to JSON",
            "primary_object": "cybernetic control chain",
            "requested_transformation": "replace Markdown authority with strict JSON control files",
            "non_goals": ["long-term Markdown compatibility"],
            "how_we_know_purpose_was_met": "JSON guard/compiler/runtime path operates without Markdown control inputs",
            "where_result_must_show_up": ["schemas", "registries", "guards"],
            "what_counts_as_done": "official JSON path passes and Markdown control input fails",
            "source_requirements": [
                {
                    "id": "SR-schema-validation",
                    "source": {
                        "kind": "user_message",
                        "quote": "replace Markdown authority with strict JSON control files",
                    },
                    "required_action": "replace Markdown authority with strict JSON control files",
                    "requirement_type": "implement_behavior",
                    "required_evidence_strength": "test_result",
                    "target_objects": ["JSON control files", "Markdown control inputs"],
                    "completion_checks": [
                        "JSON control files validate through schema tests.",
                        "Markdown control inputs are rejected by official guard/compiler/runtime paths.",
                    ],
                    "blocks_goal_achieved_if_missing": True,
                }
            ],
            "required_outcomes": [
                {
                    "id": "outcome.schema-validation",
                    "statement": "JSON control artifacts validate only when required outcomes are preserved",
                    "source_requirements": ["SR-schema-validation"],
                    "completion_claim": "Completes the request by making JSON control files pass and Markdown control inputs fail.",
                    "completed_target_objects": ["JSON control files", "Markdown control inputs"],
                    "blocks_goal_achieved_if_missing": True,
                    "required_evidence": [
                        {
                            "evidence_id": "evidence.schema-validation-tests",
                            "kind": "progress_event",
                            "description": "schema validation tests passed",
                            "evidence_strength": "test_result",
                            "satisfies_source_requirements": ["SR-schema-validation"],
                            "evidence_claim": "The schema validation tests prove JSON control files pass and Markdown control inputs fail.",
                            "completed_target_objects": ["JSON control files", "Markdown control inputs"],
                        }
                    ],
                    "not_satisfied_by": ["required step completion without outcome coverage"],
                }
            ],
            "final_answer_format": {
                "medium": "chat summary",
                "required_structure": ["changed files", "verification commands"],
            },
        },
    },
    "design.control.schema.json": {
        "artifact_type": "design.control",
        "schema_version": "1.0.0",
        "status": "approved",
        "source_contracts": {
            "requirements": "requirements.control.json",
        },
        "approved_control": {
            "confirmed_meaning": "JSON is the only official persistent control fact",
            "required_answer_path": [
                "initial state",
                "state transition that makes the result true",
                "observable target state",
            ],
            "what_is_not_enough_avoided": ["JSON sidecars with Markdown authority"],
        },
        "required_steps": [
            {
                "step_id": "S2",
                "transition": "strict JSON schema set exists",
                "evidence": ["schema validation tests"],
                "satisfies_outcomes": ["outcome.schema-validation"],
            }
        ],
    },
    "goal.control.schema.json": {
        "artifact_type": "goal.control",
        "schema_version": "1.0.0",
        "status": "approved",
        "source_contracts": {
            "requirements": "requirements.control.json",
            "design": "design.control.json",
        },
        "approved_control": {
            "objective": "migrate official cybernetic control facts to JSON",
            "success_condition": "JSON-only official path and verifier-gated completion are observed",
            "what_counts_as_done": "schemas, registries, guard/compiler/runtime, progress, verifier, and regressions pass",
            "rules_that_must_not_change": [
                "approved JSON is runtime read-only",
                "Markdown is not official control input",
            ],
        },
        "required_steps": [
            {
                "step_id": "S1",
                "transition": "Markdown dependencies inventoried",
                "evidence": ["inventory and failing-input list"],
                "satisfies_outcomes": ["outcome.schema-validation"],
            }
        ],
    },
    "plan.control.schema.json": {
        "artifact_type": "plan.control",
        "schema_version": "1.0.0",
        "status": "approved",
        "source_contracts": {
            "requirements": "requirements.control.json",
            "design": "design.control.json",
            "goal": "goal.control.json",
        },
        "registry_bindings": {
            "selected_agent_workflow": "superpowers-dispatching-parallel-agents",
            "allowed_work_assignment": "Parallel subagent-driven",
        },
        "required_steps": [
            {
                "step_id": "S1",
                "transition": "Markdown dependencies inventoried",
                "evidence": ["inventory and failing-input list"],
                "satisfies_outcomes": ["outcome.schema-validation"],
            }
        ],
        "step_action_alignment": [
            {
                "required_step_id": "S1",
                "what_would_make_it_true": "Markdown dependencies are inventoried and represented as JSON-only schema tests.",
                "current_state": "Markdown control artifacts may still be accepted by old paths.",
                "planned_producing_action": "Create schema coverage and tests that make Markdown official input fail.",
                "why_this_can_make_it_true": "The action changes the validation state instead of only checking existing artifacts.",
                "allowed_authority_needed": {
                    "write_paths": ["schemas/control-json", "tests/skills/test_control_json_schemas.py"],
                    "run_commands": ["python3 -m unittest tests.skills.test_control_json_schemas"],
                },
                "evidence_after_action": ["schema validation tests"],
                "if_not_producible": "return_to_design_or_requirements_with_reason",
            }
        ],
        "work_packages": [
            {
                "work_package_id": "WP1",
                "required_steps": ["S1"],
                "role": "mainline",
                "uses_step_action_alignment": ["S1"],
                "state_change_it_produces": "JSON schema validation state changes from permissive to strict.",
                "not_merely_verification": True,
                "counts_as_goal_progress": True,
                "allowed_write_paths": ["schemas/control-json", "tests/skills/test_control_json_schemas.py"],
                "forbidden_write_paths": ["guard scripts", "compiler scripts"],
                "required_tests": ["python3 -m unittest tests.skills.test_control_json_schemas"],
            }
        ],
        "runtime": {
            "readonly_files": ["requirements.control.json", "design.control.json", "goal.control.json", "plan.control.json", "review.control.json", "runtime.control.json"],
            "writable_files": ["progress.jsonl", "runtime-status.json", "final-report.json"],
            "writable_evidence_paths": ["evidence/"],
        },
        "progress": {
            "event_schema": "progress-event.schema.json",
            "append_only": True,
        },
        "verifier": {
            "required_before_goal_achieved": True,
            "required_outcomes": ["outcome.schema-validation"],
            "output_schema": "final-report.schema.json",
        },
    },
    "review.control.schema.json": {
        "artifact_type": "review.control",
        "schema_version": "1.0.0",
        "status": "approved",
        "source_contracts": {
            "requirements": "requirements.control.json",
            "design": "design.control.json",
            "goal": "goal.control.json",
            "plan": "plan.control.json",
        },
        "registry_bindings": {
            "selected_agent_workflow": "superpowers-dispatching-parallel-agents",
        },
        "review_checks": [
            review_check("required-answer-path", ["runtime required steps are covered"]),
            review_check("intent-preservation", ["approved user intent is preserved across design, goal, and plan"]),
            review_check("obligation-preservation", ["required outcomes are not downgraded into permission, readiness, or future work"]),
            review_check("required-outcome-coverage", ["blocking required outcomes are mapped through required steps, work packages, and verifier"]),
            review_check("producing-action-alignment", ["blocking required steps are mapped to producing actions and mainline work packages"]),
            review_check("work-assignment", ["parallel workflow registry binding present"]),
            review_check("horizon-authority", ["covered work remains in this run"]),
            review_check("final-observer", ["approved JSON chain ready for runtime"]),
        ],
    },
    "runtime.control.schema.json": {
        "artifact_type": "runtime.control",
        "schema_version": "1.0.0",
        "status": "compiled",
        "control_mode": "lean",
        "generation": {
            "id": "gen-000",
        },
        "control_chain": {
            "requirements": "requirements.control.json",
            "design": "design.control.json",
            "goal": "goal.control.json",
            "plan": "plan.control.json",
            "review": "review.control.json",
        },
        "registry_bindings": {
            "selected_agent_workflow": "superpowers-dispatching-parallel-agents",
        },
        "runtime": {
            "readonly_files": ["requirements.control.json", "design.control.json", "goal.control.json", "plan.control.json", "review.control.json", "runtime.control.json"],
            "writable_files": ["progress.jsonl", "runtime-status.json", "final-report.json"],
            "writable_evidence_paths": ["evidence/"],
        },
        "required_steps": [
            {
                "step_id": "S1",
                "transition": "Markdown dependencies inventoried",
                "evidence": ["inventory and failing-input list"],
                "satisfies_outcomes": ["outcome.schema-validation"],
            }
        ],
        "progress": {
            "event_schema": "progress-event.schema.json",
            "append_only": True,
        },
        "verifier": {
            "required_before_goal_achieved": True,
            "command": "verify-control-run",
            "required_outcomes": ["outcome.schema-validation"],
            "output_schema": "final-report.schema.json",
        },
    },
    "run.control.schema.json": {
        "artifact_type": "run.control",
        "schema_version": "1.0.0",
        "status": "active",
        "run_id": "2026-06-10-lean-fixture",
        "control_mode": "lean",
        "current_generation": "gen-000",
        "max_auto_amendment_rounds": 2,
        "semantic_base_ref": {
            "id": "semantic-base:test-fixture",
            "hash": "sha256:test-fixture",
        },
        "amendment_policy": {
            "may_change": [
                "design_strategy",
                "plan_strategy",
                "runtime_strategy",
                "required_step_refinement",
                "work_packages",
                "instrumentation",
                "verifier_config",
            ],
            "must_not_change_without_human": [
                "semantic_base",
                "required_outcomes",
                "what_counts_as_done",
                "work_covered",
                "authority",
                "forbidden_actions",
            ],
        },
        "generations": [
            {
                "id": "gen-000",
                "strategy_kind": "execution",
                "status": "active",
                "runtime": "gen-000/runtime.control.json",
                "review": "gen-000/review.control.json",
                "required_steps": [
                    {
                        "step_id": "S1",
                        "transition": "first lean horizon is executable",
                        "evidence": ["lean runtime evidence"],
                        "satisfies_outcomes": ["outcome.schema-validation"],
                    }
                ],
            }
        ],
    },
    "amendment-proposal.schema.json": {
        "artifact_type": "control.amendment.proposal",
        "schema_version": "1.0.0",
        "status": "proposed",
        "amendment_id": "A1",
        "runtime_generation": "gen-000",
        "reason": "Current strategy cannot produce required outcome evidence.",
        "triggering_observation": "The current evidence proves readiness, not implementation.",
        "affected_stages": ["design", "plan", "runtime"],
        "affected_source_requirements": ["SR-schema-validation"],
        "semantic_base_change": False,
        "required_outcomes_changed": False,
        "authority_expanded": False,
        "proposed_changes": ["replace readiness-only work package with implementation work"],
        "review_required": ["intent-preservation", "obligation-preservation"],
    },
    "progress-event.schema.json": {
        "event_type": "step.completed",
        "schema_version": "1.0.0",
        "occurred_at": "2026-06-09T00:00:00Z",
        "runtime_generation": "gen-000",
        "work_package_id": "WP1",
        "required_step": "S2",
        "status": "pass",
        "evidence": ["schema validation tests passed"],
    },
    "final-report.schema.json": {
        "artifact_type": "final-report",
        "schema_version": "1.0.0",
        "goal_achieved": False,
        "what_counts_as_done_met": False,
        "runtime_generation": "gen-000",
        "superseded_generations": [],
        "unresolved_amendments": [],
        "evidence": ["focused schema test"],
        "verification": {
            "verifier_result": "not_run",
            "verifier_permits_goal_achieved": False,
        },
        "work_coverage": {
            "status": "partial",
            "executed": ["WP1 schema foundation"],
            "prepared_only": [],
            "forbidden_not_executed": [],
            "out_of_scope": ["external production systems"],
        },
        "remaining_gaps": ["guard/compiler/runtime conversion pending"],
    },
}


READONLY_FILES = [
    "requirements.control.json",
    "design.control.json",
    "goal.control.json",
    "plan.control.json",
    "review.control.json",
    "runtime.control.json",
]
REVIEW_HASH_FILES = [
    "requirements.control.json",
    "design.control.json",
    "goal.control.json",
    "plan.control.json",
]


def canonical_json_hash(value: dict, omit_top_level: set[str] | None = None) -> str:
    canonical_value = copy.deepcopy(value)
    for key in omit_top_level or set():
        canonical_value.pop(key, None)
    encoded = json.dumps(canonical_value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return "sha256:" + hashlib.sha256(encoded).hexdigest()


def semantic_base_for_requirements(requirements: dict) -> dict:
    approved = copy.deepcopy(requirements["approved_control"])
    approved.pop("semantic_base", None)
    return {
        "id": "semantic-base:test-fixture",
        "hash": canonical_json_hash(approved),
    }


def control_hash(filename: str, artifact: dict) -> str:
    omit = {"approved_control_hashes"} if filename == "runtime.control.json" else set()
    return canonical_json_hash(artifact, omit)


def apply_integrity_metadata(control_files: dict[str, dict]) -> None:
    semantic_base = semantic_base_for_requirements(control_files["requirements.control.json"])
    control_files["requirements.control.json"]["approved_control"]["semantic_base"] = semantic_base
    for filename in (
        "design.control.json",
        "goal.control.json",
        "plan.control.json",
        "review.control.json",
        "runtime.control.json",
    ):
        control_files[filename]["semantic_base_ref"] = copy.deepcopy(semantic_base)

    control_files["review.control.json"]["approved_control_hashes"] = {
        filename: control_hash(filename, control_files[filename])
        for filename in REVIEW_HASH_FILES
    }
    control_files["runtime.control.json"]["approved_control_hashes"] = {
        filename: control_hash(filename, control_files[filename])
        for filename in READONLY_FILES
    }


apply_integrity_metadata(
    {
        "requirements.control.json": SCHEMA_FIXTURES["requirements.control.schema.json"],
        "design.control.json": SCHEMA_FIXTURES["design.control.schema.json"],
        "goal.control.json": SCHEMA_FIXTURES["goal.control.schema.json"],
        "plan.control.json": SCHEMA_FIXTURES["plan.control.schema.json"],
        "review.control.json": SCHEMA_FIXTURES["review.control.schema.json"],
        "runtime.control.json": SCHEMA_FIXTURES["runtime.control.schema.json"],
    }
)


class SchemaValidationError(AssertionError):
    pass


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def validate(instance, schema, path="$"):
    if "const" in schema and instance != schema["const"]:
        raise SchemaValidationError(f"{path}: expected const {schema['const']!r}, got {instance!r}")
    if "enum" in schema and instance not in schema["enum"]:
        raise SchemaValidationError(f"{path}: expected one of {schema['enum']!r}, got {instance!r}")

    expected_type = schema.get("type")
    if expected_type == "object":
        if not isinstance(instance, dict):
            raise SchemaValidationError(f"{path}: expected object")
        required = schema.get("required", [])
        for key in required:
            if key not in instance:
                raise SchemaValidationError(f"{path}: missing required key {key!r}")
        properties = schema.get("properties", {})
        if schema.get("additionalProperties") is False:
            extra = sorted(set(instance) - set(properties))
            if extra:
                raise SchemaValidationError(f"{path}: unknown keys {extra!r}")
        for key, subschema in properties.items():
            if key in instance:
                validate(instance[key], subschema, f"{path}.{key}")
    elif expected_type == "array":
        if not isinstance(instance, list):
            raise SchemaValidationError(f"{path}: expected array")
        if "minItems" in schema and len(instance) < schema["minItems"]:
            raise SchemaValidationError(f"{path}: expected at least {schema['minItems']} items")
        for index, item in enumerate(instance):
            validate(item, schema.get("items", {}), f"{path}[{index}]")
    elif expected_type == "string":
        if not isinstance(instance, str):
            raise SchemaValidationError(f"{path}: expected string")
        if schema.get("minLength", 0) and len(instance) < schema["minLength"]:
            raise SchemaValidationError(f"{path}: expected non-empty string")
    elif expected_type == "boolean":
        if not isinstance(instance, bool):
            raise SchemaValidationError(f"{path}: expected boolean")
    elif expected_type == "integer":
        if not isinstance(instance, int) or isinstance(instance, bool):
            raise SchemaValidationError(f"{path}: expected integer")
    elif expected_type == "number":
        if not isinstance(instance, (int, float)) or isinstance(instance, bool):
            raise SchemaValidationError(f"{path}: expected number")


def assert_all_object_schemas_are_strict(testcase: unittest.TestCase, schema: dict, path: str = "$"):
    if schema.get("type") == "object":
        additional = schema.get("additionalProperties")
        if isinstance(additional, dict):
            testcase.assertEqual("string", additional.get("type"), f"{path} dynamic keys must be string-valued")
        else:
            testcase.assertFalse(additional, f"{path} must reject unknown fields")
        for key, subschema in schema.get("properties", {}).items():
            assert_all_object_schemas_are_strict(testcase, subschema, f"{path}.{key}")
    elif schema.get("type") == "array":
        assert_all_object_schemas_are_strict(testcase, schema.get("items", {}), f"{path}[]")


class ControlJsonSchemaTest(unittest.TestCase):
    def test_every_schema_loads_and_accepts_minimal_fixture(self):
        for schema_name, fixture in SCHEMA_FIXTURES.items():
            with self.subTest(schema=schema_name):
                schema = load_json(SCHEMA_DIR / schema_name)
                assert_all_object_schemas_are_strict(self, schema)
                validate(fixture, schema)

    def test_schemas_reject_unknown_top_level_fields(self):
        for schema_name, fixture in SCHEMA_FIXTURES.items():
            with self.subTest(schema=schema_name):
                schema = load_json(SCHEMA_DIR / schema_name)
                invalid = copy.deepcopy(fixture)
                invalid["unexpected_field"] = "must be rejected"
                with self.assertRaises(SchemaValidationError):
                    validate(invalid, schema)

    def test_schema_set_represents_control_chain_foundations(self):
        for schema_name in ("plan.control.schema.json", "review.control.schema.json", "runtime.control.schema.json"):
            with self.subTest(schema=schema_name):
                schema = load_json(SCHEMA_DIR / schema_name)
                properties = schema["properties"]
                self.assertIn("registry_bindings", properties)
        for schema_name in ("requirements.control.schema.json", "design.control.schema.json", "goal.control.schema.json"):
            with self.subTest(schema=schema_name):
                schema = load_json(SCHEMA_DIR / schema_name)
                self.assertNotIn("registry_bindings", schema["properties"])
                self.assertIn("approved_control", schema["properties"])

        plan = load_json(SCHEMA_DIR / "plan.control.schema.json")
        self.assertIn("step_action_alignment", plan["properties"])
        self.assertIn("work_packages", plan["properties"])
        self.assertIn("runtime", plan["properties"])
        self.assertIn("progress", plan["properties"])
        self.assertIn("verifier", plan["properties"])

        review = load_json(SCHEMA_DIR / "review.control.schema.json")
        self.assertIn("review_checks", review["properties"])

    def test_no_predefined_answer_method_registry_or_keys_remain(self):
        self.assertFalse((ROOT / ".agents/skills/references/answer-method-registry.json").exists())
        for schema_name in (
            "requirements.control.schema.json",
            "design.control.schema.json",
            "goal.control.schema.json",
            "plan.control.schema.json",
            "review.control.schema.json",
            "runtime.control.schema.json",
        ):
            schema_text = (SCHEMA_DIR / schema_name).read_text(encoding="utf-8")
            self.assertNotIn("answer_method_key", schema_text)
            self.assertNotIn("forbidden_substitute_key", schema_text)

    def test_registry_binding_keys_exist_for_delegation_workflow_only(self):
        delegation_registry = load_json(DELEGATION_WORKFLOW_REGISTRY)

        self.assertIn("superpowers-dispatching-parallel-agents", delegation_registry)
        workflow = delegation_registry["superpowers-dispatching-parallel-agents"]
        self.assertIn("allowed_work_assignment", workflow)
        self.assertNotIn("allowed_work assignment", workflow)
        self.assertIn("Parallel subagent-driven", workflow["allowed_work_assignment"])
        self.assertIn("parallel-max-safe", workflow["allowed_mode"])

    def test_schemas_bind_semantic_base_and_approved_control_hashes(self):
        requirements = load_json(SCHEMA_DIR / "requirements.control.schema.json")
        design = load_json(SCHEMA_DIR / "design.control.schema.json")
        goal = load_json(SCHEMA_DIR / "goal.control.schema.json")
        plan = load_json(SCHEMA_DIR / "plan.control.schema.json")
        review = load_json(SCHEMA_DIR / "review.control.schema.json")
        runtime = load_json(SCHEMA_DIR / "runtime.control.schema.json")

        self.assertIn("semantic_base", requirements["properties"]["approved_control"]["properties"])
        for schema in (design, goal, plan, review, runtime):
            self.assertIn("semantic_base_ref", schema["required"])
            self.assertIn("semantic_base_ref", schema["properties"])
        for schema in (review, runtime):
            self.assertIn("approved_control_hashes", schema["required"])
            self.assertIn("approved_control_hashes", schema["properties"])

    def test_required_outcomes_are_first_class_across_control_chain(self):
        requirements = load_json(SCHEMA_DIR / "requirements.control.schema.json")
        approved_control = requirements["properties"]["approved_control"]
        self.assertIn("required_outcomes", approved_control["required"])
        outcome_schema = approved_control["properties"]["required_outcomes"]["items"]
        self.assertEqual(
            [
                "id",
                "statement",
                "source_requirements",
                "completion_claim",
                "blocks_goal_achieved_if_missing",
                "required_evidence",
                "not_satisfied_by",
            ],
            outcome_schema["required"],
        )
        evidence_schema = outcome_schema["properties"]["required_evidence"]["items"]
        self.assertEqual(
            [
                "evidence_id",
                "kind",
                "description",
                "evidence_strength",
                "satisfies_source_requirements",
                "evidence_claim",
            ],
            evidence_schema["required"],
        )
        self.assertIn("progress_event", evidence_schema["properties"]["kind"]["enum"])
        self.assertIn("file_exists", evidence_schema["properties"]["kind"]["enum"])
        self.assertIn("json_file", evidence_schema["properties"]["kind"]["enum"])
        self.assertIn("command_result", evidence_schema["properties"]["kind"]["enum"])

        for schema_name in (
            "design.control.schema.json",
            "goal.control.schema.json",
            "plan.control.schema.json",
            "runtime.control.schema.json",
        ):
            with self.subTest(schema=schema_name):
                schema = load_json(SCHEMA_DIR / schema_name)
                step_schema = schema["properties"]["required_steps"]["items"]
                self.assertIn("satisfies_outcomes", step_schema["required"])
                self.assertIn("satisfies_outcomes", step_schema["properties"])

        plan = load_json(SCHEMA_DIR / "plan.control.schema.json")
        self.assertIn("step_action_alignment", plan["required"])
        alignment_schema = plan["properties"]["step_action_alignment"]["items"]
        for field in (
            "required_step_id",
            "what_would_make_it_true",
            "current_state",
            "planned_producing_action",
            "why_this_can_make_it_true",
            "allowed_authority_needed",
            "evidence_after_action",
            "if_not_producible",
        ):
            with self.subTest(alignment_field=field):
                self.assertIn(field, alignment_schema["required"])
                self.assertIn(field, alignment_schema["properties"])
        work_package_schema = plan["properties"]["work_packages"]["items"]
        for field in (
            "role",
            "uses_step_action_alignment",
            "state_change_it_produces",
            "not_merely_verification",
            "counts_as_goal_progress",
        ):
            with self.subTest(work_package_field=field):
                self.assertIn(field, work_package_schema["required"])
                self.assertIn(field, work_package_schema["properties"])

        runtime = load_json(SCHEMA_DIR / "runtime.control.schema.json")
        for schema in (plan, runtime):
            verifier = schema["properties"]["verifier"]
            self.assertIn("required_outcomes", verifier["required"])
            self.assertIn("required_outcomes", verifier["properties"])
        self.assertIn("control_mode", runtime["required"])
        self.assertIn("generation", runtime["required"])

    def test_generation_and_amendment_schemas_are_first_class(self):
        run_schema = load_json(SCHEMA_DIR / "run.control.schema.json")
        amendment_schema = load_json(SCHEMA_DIR / "amendment-proposal.schema.json")
        progress_schema = load_json(SCHEMA_DIR / "progress-event.schema.json")
        final_report_schema = load_json(SCHEMA_DIR / "final-report.schema.json")

        self.assertIn("current_generation", run_schema["required"])
        self.assertIn("max_auto_amendment_rounds", run_schema["required"])
        self.assertEqual(["lean", "full"], run_schema["properties"]["control_mode"]["enum"])
        self.assertIn("must_not_change_without_human", run_schema["properties"]["amendment_policy"]["required"])
        self.assertIn("strategy_kind", run_schema["properties"]["generations"]["items"]["required"])
        self.assertIn("runtime", run_schema["properties"]["generations"]["items"]["required"])

        self.assertEqual("control.amendment.proposal", amendment_schema["properties"]["artifact_type"]["const"])
        self.assertIn("semantic_base_change", amendment_schema["required"])
        self.assertIn("authority_expanded", amendment_schema["required"])

        event_types = progress_schema["properties"]["event_type"]["enum"]
        self.assertIn("control.amendment.proposed", event_types)
        self.assertIn("runtime.generation.started", event_types)
        self.assertIn("runtime_generation", progress_schema["required"])
        self.assertNotIn("work_package_id", progress_schema["required"])
        self.assertNotIn("required_step", progress_schema["required"])
        self.assertNotIn("status", progress_schema["required"])
        self.assertIn("runtime_generation", progress_schema["properties"])
        self.assertIn("proposed_changes", progress_schema["properties"])
        self.assertIn("next_generation", progress_schema["properties"])
        self.assertIn("allOf", progress_schema)

        self.assertIn("runtime_generation", final_report_schema["properties"])
        self.assertIn("unresolved_amendments", final_report_schema["properties"])

    def test_requirements_schema_rejects_missing_source_requirement_fields_for_v1_1(self):
        schema = json.loads((SCHEMA_DIR / "requirements.control.schema.json").read_text(encoding="utf-8"))
        fixture = copy.deepcopy(SCHEMA_FIXTURES["requirements.control.schema.json"])
        fixture["schema_version"] = "1.1.0"
        del fixture["approved_control"]["source_requirements"][0]["completion_checks"]

        with self.assertRaises(AssertionError):
            validate(fixture, schema)

    def test_progress_event_schema_accepts_affected_source_requirements_on_amendment(self):
        schema = json.loads((SCHEMA_DIR / "progress-event.schema.json").read_text(encoding="utf-8"))
        event = {
            "event_type": "control.amendment.proposed",
            "schema_version": "1.1.0",
            "occurred_at": "2026-06-10T00:00:00Z",
            "runtime_generation": "gen-000",
            "amendment_id": "A1",
            "reason": "current strategy cannot complete source requirement",
            "triggering_observation": "only framework evidence exists for a measurement request",
            "affected_stages": ["plan", "runtime"],
            "affected_source_requirements": ["SR-measure-scale-curves"],
            "semantic_base_change": False,
            "required_outcomes_changed": False,
            "authority_expanded": False,
            "proposed_changes": ["add measured curve producing step"],
            "review_required": ["source-requirement-preservation", "obligation-preservation"],
        }

        validate(event, schema)

    def test_review_checks_are_structured_certificates(self):
        review = load_json(SCHEMA_DIR / "review.control.schema.json")
        check_schema = review["properties"]["review_checks"]["items"]

        for field in (
            "check_id",
            "status",
            "verdict",
            "return_to_stage",
            "evidence",
            "findings",
            "required_changes",
            "checked_transformations",
        ):
            with self.subTest(field=field):
                self.assertIn(field, check_schema["required"])
                self.assertIn(field, check_schema["properties"])

        self.assertIn("approved", check_schema["properties"]["verdict"]["enum"])
        self.assertIn("needs_revision", check_schema["properties"]["verdict"]["enum"])
        self.assertIn("blocked", check_schema["properties"]["verdict"]["enum"])


if __name__ == "__main__":
    unittest.main()
