import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


class ValidateRunEventsTest(unittest.TestCase):
    def run_validator(self, *args):
        return subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "validate_run_events.py"), *args],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )

    def test_metadata_only_example_validates_against_taxonomy(self):
        result = self.run_validator(
            "--taxonomy",
            "observability/taxonomies/failure-taxonomy.yaml",
            "observability/examples/metadata-only-event.json",
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("validated 1 event", result.stdout)

    def test_metadata_only_rejects_content_summary_and_real_paths(self):
        unsafe = {
            "schema_version": "1.0.0",
            "event_id": "evt_unsafe",
            "event": "skill_invoked",
            "timestamp": "2026-06-01T00:00:00Z",
            "privacy_mode": "metadata_only",
            "machine_id": "anon-12345678",
            "skill_pack": {"source_commit": "abc1234"},
            "skill": "routing-cybernetic-workflows",
            "status": "success",
            "task_hash": "sha256:" + "a" * 64,
            "content_summary": "private customer task",
            "real_path": "/home/ender/customer/repo",
        }

        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as tmp:
            json.dump(unsafe, tmp)
            tmp_path = tmp.name

        try:
            result = self.run_validator(tmp_path)
        finally:
            Path(tmp_path).unlink(missing_ok=True)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("content_summary", result.stdout + result.stderr)
        self.assertIn("real_path", result.stdout + result.stderr)

    def test_metadata_only_rejects_normalized_unsafe_field_variants(self):
        unsafe = {
            "schema_version": "1.0.0",
            "event_id": "evt_unsafe_key_variants",
            "event": "skill_invoked",
            "timestamp": "2026-06-01T00:00:00Z",
            "privacy_mode": "metadata_only",
            "machine_id": "anon-12345678",
            "skill_pack": {"source_commit": "abc1234"},
            "skill": "routing-cybernetic-workflows",
            "status": "success",
            "task_hash": "sha256:" + "f" * 64,
            "Raw_Prompt": "private task prompt",
            "rawPrompt": "private task prompt",
            "contentSummary": "private summary",
            "Repository_Name": "customer/repo",
        }

        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as tmp:
            json.dump(unsafe, tmp)
            tmp_path = tmp.name

        try:
            result = self.run_validator(tmp_path)
        finally:
            Path(tmp_path).unlink(missing_ok=True)

        output = result.stdout + result.stderr
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Raw_Prompt", output)
        self.assertIn("rawPrompt", output)
        self.assertIn("contentSummary", output)
        self.assertIn("Repository_Name", output)

    def test_metadata_only_rejects_derivative_unsafe_field_variants(self):
        unsafe = {
            "schema_version": "1.0.0",
            "event_id": "evt_unsafe_derivative_key_variants",
            "event": "skill_invoked",
            "timestamp": "2026-06-01T00:00:00Z",
            "privacy_mode": "metadata_only",
            "machine_id": "anon-12345678",
            "skill_pack": {"source_commit": "abc1234"},
            "skill": "routing-cybernetic-workflows",
            "status": "success",
            "task_hash": "sha256:" + "9" * 64,
            "prompt_text": "private task prompt",
            "rawPromptText": "private raw task prompt",
            "contentSummaries": ["private summary"],
            "contentExcerptText": "private excerpt",
            "promptExamples": ["private prompt example"],
            "contentExamples": ["private content example"],
            "artifactExamples": ["private artifact example"],
            "codeSnippet": "private code",
            "logExcerptText": "private log",
            "artifactBodyText": "private artifact body",
            "apiToken": "private token",
            "token_value": "private token",
            "secretKey": "private secret",
            "customerDataText": "private customer data",
            "codeText": "private code",
            "logText": "private log",
        }

        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as tmp:
            json.dump(unsafe, tmp)
            tmp_path = tmp.name

        try:
            result = self.run_validator(tmp_path)
        finally:
            Path(tmp_path).unlink(missing_ok=True)

        output = result.stdout + result.stderr
        self.assertNotEqual(result.returncode, 0)
        for key in (
            "prompt_text",
            "rawPromptText",
            "contentSummaries",
            "contentExcerptText",
            "promptExamples",
            "contentExamples",
            "artifactExamples",
            "codeSnippet",
            "logExcerptText",
            "artifactBodyText",
            "apiToken",
            "token_value",
            "secretKey",
            "customerDataText",
            "codeText",
            "logText",
        ):
            self.assertIn(key, output)

    def test_metadata_only_accepts_safe_structured_keys_with_new_derivative_logic(self):
        safe = {
            "schema_version": "1.0.0",
            "event_id": "evt_safe_structured_keys",
            "event": "runtime_outcome",
            "timestamp": "2026-06-01T00:00:00Z",
            "privacy_mode": "metadata_only",
            "machine_id": "anon-12345678",
            "skill_pack": {"source_commit": "abc1234"},
            "status": "success",
            "task_hash": "sha256:" + "8" * 64,
            "failure_taxonomy": "sync.transport.timeout",
            "event_id_alias": "evt_alias",
            "skill_pack_alias": {"release": "v1.2.3"},
            "created_artifacts": [{"kind": "summary", "count": 1}],
            "artifact_count": 1,
            "blocked_reason": "waiting_for_review",
            "final_state": "recorded",
            "required_gates": ["compile", "unit"],
            "impromptu_status": "not a prompt",
            "task_hash_alias": "sha256:" + "7" * 64,
            "machine_id_alias": "anon-machine",
            "privacy_mode_alias": "metadata_only",
            "raw_event_count": 3,
            "raw_metric_name": "duration_ms",
        }

        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as tmp:
            json.dump(safe, tmp)
            tmp_path = tmp.name

        try:
            result = self.run_validator(tmp_path)
        finally:
            Path(tmp_path).unlink(missing_ok=True)

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_metadata_only_rejects_unsafe_values_under_neutral_keys(self):
        unsafe = {
            "schema_version": "1.0.0",
            "event_id": "evt_unsafe_value",
            "event": "skill_invoked",
            "timestamp": "2026-06-01T00:00:00Z",
            "privacy_mode": "metadata_only",
            "machine_id": "anon-12345678",
            "skill_pack": {"source_commit": "abc1234"},
            "skill": "routing-cybernetic-workflows",
            "status": "success",
            "task_hash": "sha256:" + "e" * 64,
            "details": "failed while reading /home/ender/customer/repo",
        }

        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as tmp:
            json.dump(unsafe, tmp)
            tmp_path = tmp.name

        try:
            result = self.run_validator(tmp_path)
        finally:
            Path(tmp_path).unlink(missing_ok=True)

        output = result.stdout + result.stderr
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("unsafe metadata-only value", output)

    def test_metadata_only_rejects_dynamic_key_that_is_real_path(self):
        unsafe = {
            "schema_version": "1.0.0",
            "event_id": "evt_unsafe_dynamic_path_key",
            "event": "skill_invoked",
            "timestamp": "2026-06-01T00:00:00Z",
            "privacy_mode": "metadata_only",
            "machine_id": "anon-12345678",
            "skill_pack": {"source_commit": "abc1234"},
            "skill": "routing-cybernetic-workflows",
            "status": "success",
            "task_hash": "sha256:" + "6" * 64,
            "artifacts": {
                "/home/ender/work/private-project/file.txt": {"kind": "summary", "count": 1},
            },
        }

        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as tmp:
            json.dump(unsafe, tmp)
            tmp_path = tmp.name

        try:
            result = self.run_validator(tmp_path)
        finally:
            Path(tmp_path).unlink(missing_ok=True)

        output = result.stdout + result.stderr
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("metadata_only", output)
        self.assertIn("/home/ender/work/private-project/file.txt", output)

    def test_redacted_content_opt_in_rejects_dynamic_key_that_is_hosted_repo_identifier(self):
        unsafe = {
            "schema_version": "1.0.0",
            "event_id": "evt_unsafe_dynamic_repo_key",
            "event": "runtime_outcome",
            "timestamp": "2026-06-01T00:00:00Z",
            "privacy_mode": "redacted_content_opt_in",
            "machine_id": "anon-12345678",
            "skill_pack": {"source_commit": "abc1234"},
            "status": "success",
            "task_hash": "sha256:" + "0" * 64,
            "repositories": {
                "github.com/acme/private-repo": {"status": "recorded"},
            },
        }

        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as tmp:
            json.dump(unsafe, tmp)
            tmp_path = tmp.name

        try:
            result = self.run_validator(tmp_path)
        finally:
            Path(tmp_path).unlink(missing_ok=True)

        output = result.stdout + result.stderr
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("redacted_content_opt_in", output)
        self.assertIn("github.com/acme/private-repo", output)

    def test_redacted_content_opt_in_rejects_raw_unsafe_fields(self):
        unsafe = {
            "schema_version": "1.0.0",
            "event_id": "evt_unsafe_redacted_opt_in",
            "event": "skill_invoked",
            "timestamp": "2026-06-01T00:00:00Z",
            "privacy_mode": "redacted_content_opt_in",
            "machine_id": "anon-12345678",
            "skill_pack": {"source_commit": "abc1234"},
            "skill": "routing-cybernetic-workflows",
            "status": "success",
            "task_hash": "sha256:" + "1" * 64,
            "raw_prompt": "private task prompt",
        }

        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as tmp:
            json.dump(unsafe, tmp)
            tmp_path = tmp.name

        try:
            result = self.run_validator(tmp_path)
        finally:
            Path(tmp_path).unlink(missing_ok=True)

        output = result.stdout + result.stderr
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("redacted_content_opt_in", output)
        self.assertIn("raw_prompt", output)

    def test_metadata_only_rejects_raw_response_field(self):
        unsafe = {
            "schema_version": "1.0.0",
            "event_id": "evt_unsafe_raw_response",
            "event": "skill_invoked",
            "timestamp": "2026-06-01T00:00:00Z",
            "privacy_mode": "metadata_only",
            "machine_id": "anon-12345678",
            "skill_pack": {"source_commit": "abc1234"},
            "skill": "routing-cybernetic-workflows",
            "status": "success",
            "task_hash": "sha256:" + "2" * 64,
            "raw_response": "private model response",
        }

        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as tmp:
            json.dump(unsafe, tmp)
            tmp_path = tmp.name

        try:
            result = self.run_validator(tmp_path)
        finally:
            Path(tmp_path).unlink(missing_ok=True)

        output = result.stdout + result.stderr
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("metadata_only", output)
        self.assertIn("raw_response", output)

    def test_redacted_content_opt_in_rejects_raw_response_field(self):
        unsafe = {
            "schema_version": "1.0.0",
            "event_id": "evt_unsafe_opt_in_raw_response",
            "event": "skill_invoked",
            "timestamp": "2026-06-01T00:00:00Z",
            "privacy_mode": "redacted_content_opt_in",
            "machine_id": "anon-12345678",
            "skill_pack": {"source_commit": "abc1234"},
            "skill": "routing-cybernetic-workflows",
            "status": "success",
            "task_hash": "sha256:" + "3" * 64,
            "raw_response": "private model response",
        }

        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as tmp:
            json.dump(unsafe, tmp)
            tmp_path = tmp.name

        try:
            result = self.run_validator(tmp_path)
        finally:
            Path(tmp_path).unlink(missing_ok=True)

        output = result.stdout + result.stderr
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("redacted_content_opt_in", output)
        self.assertIn("raw_response", output)

    def test_rejects_hostname_like_machine_id(self):
        unsafe = {
            "schema_version": "1.0.0",
            "event_id": "evt_hostname",
            "event": "skill_invoked",
            "timestamp": "2026-06-01T00:00:00Z",
            "privacy_mode": "metadata_only",
            "machine_id": "workstation.local",
            "skill_pack": {"source_commit": "abc1234"},
            "skill": "routing-cybernetic-workflows",
            "status": "success",
            "task_hash": "sha256:" + "b" * 64,
        }

        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as tmp:
            json.dump(unsafe, tmp)
            tmp_path = tmp.name

        try:
            result = self.run_validator(tmp_path)
        finally:
            Path(tmp_path).unlink(missing_ok=True)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("machine_id", result.stdout + result.stderr)

    def test_requires_status_and_real_version_identity(self):
        unsafe = {
            "schema_version": "1.0.0",
            "event_id": "evt_missing_status_unknown_version",
            "event": "skill_invoked",
            "timestamp": "2026-06-01T00:00:00Z",
            "privacy_mode": "metadata_only",
            "machine_id": "anon-12345678",
            "skill_pack": {"source_commit": "unknown"},
            "task_hash": "sha256:" + "c" * 64,
        }

        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as tmp:
            json.dump(unsafe, tmp)
            tmp_path = tmp.name

        try:
            result = self.run_validator(tmp_path)
        finally:
            Path(tmp_path).unlink(missing_ok=True)

        output = result.stdout + result.stderr
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("missing required field status", output)
        self.assertIn("must not be unknown", output)

    def test_rejects_null_skill_pack_release_even_with_valid_source_commit(self):
        unsafe = {
            "schema_version": "1.0.0",
            "event_id": "evt_null_release",
            "event": "skill_invoked",
            "timestamp": "2026-06-01T00:00:00Z",
            "privacy_mode": "metadata_only",
            "machine_id": "anon-12345678",
            "skill_pack": {"release": None, "source_commit": "abc1234"},
            "status": "success",
            "task_hash": "sha256:" + "4" * 64,
        }

        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as tmp:
            json.dump(unsafe, tmp)
            tmp_path = tmp.name

        try:
            result = self.run_validator(tmp_path)
        finally:
            Path(tmp_path).unlink(missing_ok=True)

        output = result.stdout + result.stderr
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("skill_pack release must be a non-empty string", output)

    def test_rejects_null_skill_pack_source_commit_even_with_valid_release(self):
        unsafe = {
            "schema_version": "1.0.0",
            "event_id": "evt_null_source_commit",
            "event": "skill_invoked",
            "timestamp": "2026-06-01T00:00:00Z",
            "privacy_mode": "metadata_only",
            "machine_id": "anon-12345678",
            "skill_pack": {"release": "v1.2.3", "source_commit": None},
            "status": "success",
            "task_hash": "sha256:" + "5" * 64,
        }

        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as tmp:
            json.dump(unsafe, tmp)
            tmp_path = tmp.name

        try:
            result = self.run_validator(tmp_path)
        finally:
            Path(tmp_path).unlink(missing_ok=True)

        output = result.stdout + result.stderr
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("skill_pack source_commit must be a non-empty string", output)

    def test_rejects_null_status(self):
        unsafe = {
            "schema_version": "1.0.0",
            "event_id": "evt_null_status",
            "event": "skill_invoked",
            "timestamp": "2026-06-01T00:00:00Z",
            "privacy_mode": "metadata_only",
            "machine_id": "anon-12345678",
            "skill_pack": {"source_commit": "abc1234"},
            "status": None,
            "task_hash": "sha256:" + "d" * 64,
        }

        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as tmp:
            json.dump(unsafe, tmp)
            tmp_path = tmp.name

        try:
            result = self.run_validator(tmp_path)
        finally:
            Path(tmp_path).unlink(missing_ok=True)

        output = result.stdout + result.stderr
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("status", output)


if __name__ == "__main__":
    unittest.main()
