import copy
import hashlib
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCHEMA_DIR = ROOT / "schemas/control-json"
ANSWER_METHOD_REGISTRY = ROOT / ".agents/skills/references/answer-method-registry.json"
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
            "required_outcomes": [
                {
                    "id": "outcome.schema-validation",
                    "statement": "JSON control artifacts validate only when required outcomes are preserved",
                    "blocks_goal_achieved_if_missing": True,
                    "required_evidence": [
                        {
                            "evidence_id": "evidence.schema-validation-tests",
                            "kind": "progress_event",
                            "description": "schema validation tests passed",
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
        "registry_bindings": {
            "answer_method_key": "implementation-spine",
            "forbidden_substitute_key": "component-inventory-completion",
        },
    },
    "design.control.schema.json": {
        "artifact_type": "design.control",
        "schema_version": "1.0.0",
        "status": "approved",
        "source_contracts": {
            "requirements": "requirements.control.json",
            "requirements_registry_sidecar": "requirements.control.json",
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
        "registry_bindings": {
            "answer_method_key": "implementation-spine",
            "forbidden_substitute_key": "component-inventory-completion",
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
        "registry_bindings": {
            "answer_method_key": "implementation-spine",
            "forbidden_substitute_key": "component-inventory-completion",
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
            "answer_method_key": "implementation-spine",
        },
        "required_steps": [
            {
                "step_id": "S1",
                "transition": "Markdown dependencies inventoried",
                "evidence": ["inventory and failing-input list"],
                "satisfies_outcomes": ["outcome.schema-validation"],
            }
        ],
        "work_packages": [
            {
                "work_package_id": "WP1",
                "required_steps": ["S1", "S2", "S3"],
                "allowed_write_paths": ["schemas/control-json", "tests/skills/test_control_json_schemas.py"],
                "forbidden_write_paths": ["guard scripts", "compiler scripts"],
                "required_tests": ["python3 -m unittest tests.skills.test_control_json_schemas"],
            }
        ],
        "runtime": {
            "readonly_files": ["requirements.control.json", "design.control.json", "goal.control.json", "plan.control.json", "review.control.json", "runtime.control.json"],
            "writable_files": ["progress.jsonl", "runtime-status.json", "final-report.json"],
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
            "answer_method_key": "implementation-spine",
            "selected_agent_workflow": "superpowers-dispatching-parallel-agents",
        },
        "review_checks": [
            review_check("design-answer-method", ["required answer path preserved"]),
            review_check("required-answer-path", ["runtime required steps are covered"]),
            review_check("intent-preservation", ["approved user intent is preserved across design, goal, and plan"]),
            review_check("obligation-preservation", ["required outcomes are not downgraded into permission, readiness, or future work"]),
            review_check("required-outcome-coverage", ["blocking required outcomes are mapped through required steps, work packages, and verifier"]),
            review_check("work-assignment", ["parallel workflow registry binding present"]),
            review_check("horizon-authority", ["covered work remains in this run"]),
            review_check("final-observer", ["approved JSON chain ready for runtime"]),
        ],
    },
    "runtime.control.schema.json": {
        "artifact_type": "runtime.control",
        "schema_version": "1.0.0",
        "status": "compiled",
        "control_chain": {
            "requirements": "requirements.control.json",
            "design": "design.control.json",
            "goal": "goal.control.json",
            "plan": "plan.control.json",
            "review": "review.control.json",
        },
        "registry_bindings": {
            "answer_method_key": "implementation-spine",
            "selected_agent_workflow": "superpowers-dispatching-parallel-agents",
        },
        "runtime": {
            "readonly_files": ["requirements.control.json", "design.control.json", "goal.control.json", "plan.control.json", "review.control.json", "runtime.control.json"],
            "writable_files": ["progress.jsonl", "runtime-status.json", "final-report.json"],
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
    "progress-event.schema.json": {
        "event_type": "step.completed",
        "schema_version": "1.0.0",
        "occurred_at": "2026-06-09T00:00:00Z",
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
        testcase.assertFalse(schema.get("additionalProperties"), f"{path} must reject unknown fields")
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
        for schema_name in (
            "requirements.control.schema.json",
            "design.control.schema.json",
            "goal.control.schema.json",
            "plan.control.schema.json",
            "review.control.schema.json",
            "runtime.control.schema.json",
        ):
            with self.subTest(schema=schema_name):
                schema = load_json(SCHEMA_DIR / schema_name)
                properties = schema["properties"]
                self.assertIn("registry_bindings", properties)
                if schema_name != "review.control.schema.json":
                    self.assertIn("approved_control", properties)

        plan = load_json(SCHEMA_DIR / "plan.control.schema.json")
        self.assertIn("work_packages", plan["properties"])
        self.assertIn("runtime", plan["properties"])
        self.assertIn("progress", plan["properties"])
        self.assertIn("verifier", plan["properties"])

        review = load_json(SCHEMA_DIR / "review.control.schema.json")
        self.assertIn("review_checks", review["properties"])

    def test_registry_binding_keys_exist_for_answer_method_and_delegation_workflow(self):
        answer_registry = load_json(ANSWER_METHOD_REGISTRY)
        delegation_registry = load_json(DELEGATION_WORKFLOW_REGISTRY)

        self.assertIn("implementation-spine", answer_registry)
        self.assertIn("mandatory_nodes", answer_registry["implementation-spine"])
        self.assertIn("forbidden_substitutions", answer_registry["implementation-spine"])
        self.assertIn("done_rule", answer_registry["implementation-spine"])
        self.assertTrue(answer_registry["implementation-spine"]["done_rule"]["all_mandatory_nodes_required"])

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
                "blocks_goal_achieved_if_missing",
                "required_evidence",
                "not_satisfied_by",
            ],
            outcome_schema["required"],
        )
        evidence_schema = outcome_schema["properties"]["required_evidence"]["items"]
        self.assertEqual(
            ["evidence_id", "kind", "description"],
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
        runtime = load_json(SCHEMA_DIR / "runtime.control.schema.json")
        for schema in (plan, runtime):
            verifier = schema["properties"]["verifier"]
            self.assertIn("required_outcomes", verifier["required"])
            self.assertIn("required_outcomes", verifier["properties"])

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
