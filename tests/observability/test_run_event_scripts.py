import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SAMPLE = ROOT / "observability" / "examples" / "metadata-only-event.json"


class RunEventScriptsTest(unittest.TestCase):
    def run_script(self, script, *args, env=None):
        merged_env = os.environ.copy()
        if env:
            merged_env.update(env)
        return subprocess.run(
            [sys.executable, str(ROOT / "scripts" / script), *args],
            cwd=ROOT,
            text=True,
            capture_output=True,
            env=merged_env,
        )

    def test_record_run_event_dry_run_outputs_valid_metadata_only_event(self):
        result = self.run_script(
            "record_run_event.py",
            "--event",
            "skill_invoked",
            "--skill",
            "routing-cybernetic-workflows",
            "--status",
            "success",
            "--machine-id",
            "anon-testmachine",
            "--task-hash",
            "sha256:" + "c" * 64,
            "--dry-run",
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        event = json.loads(result.stdout)
        self.assertEqual(event["privacy_mode"], "metadata_only")
        self.assertEqual(event["machine_id"], "anon-testmachine")
        self.assertTrue(event["event_id"].startswith("evt_"))
        self.assertNotIn("release", event["skill_pack"])
        self.assertNotIn("raw_prompt", event)
        self.assertNotIn("content_summary", event)

        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as tmp:
            json.dump(event, tmp)
            tmp_path = tmp.name
        try:
            validation = self.run_script("validate_run_events.py", tmp_path)
        finally:
            Path(tmp_path).unlink(missing_ok=True)
        self.assertEqual(validation.returncode, 0, validation.stdout + validation.stderr)

    def test_record_run_event_appends_jsonl_locally_without_network(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / "runs.jsonl"
            result = self.run_script(
                "record_run_event.py",
                "--event",
                "blocked",
                "--status",
                "blocked",
                "--reason-code",
                "sync_blocked_missing_config",
                "--machine-id",
                "anon-testmachine",
                "--task-hash",
                "sha256:" + "d" * 64,
                "--output",
                str(output),
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            lines = output.read_text(encoding="utf-8").splitlines()
            self.assertEqual(len(lines), 1)
            event = json.loads(lines[0])
            self.assertEqual(event["event"], "blocked")
            self.assertEqual(event["reason_code"], "sync_blocked_missing_config")

    def test_redactor_removes_unsafe_fields_in_metadata_only_mode(self):
        unsafe = json.loads(SAMPLE.read_text(encoding="utf-8"))
        unsafe["content_summary"] = "private summary"
        unsafe["real_path"] = "/home/ender/private/repo"
        unsafe["artifact_body"] = "secret artifact"

        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as tmp:
            json.dump(unsafe, tmp)
            tmp_path = tmp.name
        try:
            result = self.run_script(
                "redact_run_event.py",
                tmp_path,
                "--mode",
                "metadata_only",
                "--dry-run",
            )
        finally:
            Path(tmp_path).unlink(missing_ok=True)

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        payload = json.loads(result.stdout)
        redacted_event = payload["events"][0]
        self.assertNotIn("content_summary", redacted_event)
        self.assertNotIn("real_path", redacted_event)
        self.assertNotIn("artifact_body", redacted_event)
        self.assertEqual(set(payload["redacted_fields"]), {"artifact_body", "content_summary", "real_path"})

    def test_redactor_removes_normalized_unsafe_field_variants_in_metadata_only_mode(self):
        unsafe = json.loads(SAMPLE.read_text(encoding="utf-8"))
        unsafe["Raw_Prompt"] = "private task prompt"
        unsafe["rawPrompt"] = "private task prompt"
        unsafe["contentSummary"] = "private summary"
        unsafe["Repository_Name"] = "customer/repo"

        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as tmp:
            json.dump(unsafe, tmp)
            tmp_path = tmp.name
        try:
            result = self.run_script(
                "redact_run_event.py",
                tmp_path,
                "--mode",
                "metadata_only",
                "--dry-run",
            )
        finally:
            Path(tmp_path).unlink(missing_ok=True)

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        payload = json.loads(result.stdout)
        redacted_event = payload["events"][0]
        self.assertNotIn("Raw_Prompt", redacted_event)
        self.assertNotIn("rawPrompt", redacted_event)
        self.assertNotIn("contentSummary", redacted_event)
        self.assertNotIn("Repository_Name", redacted_event)
        self.assertEqual(
            set(payload["redacted_fields"]),
            {"Raw_Prompt", "rawPrompt", "contentSummary", "Repository_Name"},
        )

    def test_redactor_removes_derivative_unsafe_field_variants_in_metadata_only_mode(self):
        unsafe = json.loads(SAMPLE.read_text(encoding="utf-8"))
        unsafe["prompt_text"] = "private task prompt"
        unsafe["rawPromptText"] = "private raw task prompt"
        unsafe["contentSummaries"] = ["private summary"]
        unsafe["contentExcerptText"] = "private excerpt"
        unsafe["promptExamples"] = ["private prompt example"]
        unsafe["contentExamples"] = ["private content example"]
        unsafe["artifactExamples"] = ["private artifact example"]
        unsafe["codeSnippet"] = "private code"
        unsafe["logExcerptText"] = "private log"
        unsafe["artifactBodyText"] = "private artifact body"
        unsafe["apiToken"] = "private token"
        unsafe["token_value"] = "private token"
        unsafe["secretKey"] = "private secret"
        unsafe["customerDataText"] = "private customer data"
        unsafe["codeText"] = "private code"
        unsafe["logText"] = "private log"

        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as tmp:
            json.dump(unsafe, tmp)
            tmp_path = tmp.name
        try:
            result = self.run_script(
                "redact_run_event.py",
                tmp_path,
                "--mode",
                "metadata_only",
                "--dry-run",
            )
        finally:
            Path(tmp_path).unlink(missing_ok=True)

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        payload = json.loads(result.stdout)
        redacted_event = payload["events"][0]
        expected_fields = {
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
        }
        for key in expected_fields:
            self.assertNotIn(key, redacted_event)
        self.assertEqual(set(payload["redacted_fields"]), expected_fields)

    def test_redactor_removes_unsafe_values_under_neutral_keys(self):
        unsafe = json.loads(SAMPLE.read_text(encoding="utf-8"))
        unsafe["details"] = "failed while reading /home/ender/private/repo"

        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as tmp:
            json.dump(unsafe, tmp)
            tmp_path = tmp.name
        try:
            result = self.run_script(
                "redact_run_event.py",
                tmp_path,
                "--mode",
                "metadata_only",
                "--dry-run",
            )
        finally:
            Path(tmp_path).unlink(missing_ok=True)

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        payload = json.loads(result.stdout)
        redacted_event = payload["events"][0]
        self.assertNotIn("details", redacted_event)
        self.assertEqual(payload["redacted_fields"], ["details"])

    def test_redactor_removes_dynamic_keys_that_match_unsafe_string_patterns(self):
        unsafe = json.loads(SAMPLE.read_text(encoding="utf-8"))
        unsafe["artifacts"] = {
            "/home/ender/private/repo/file.txt": {"kind": "summary"},
            "safe_artifact_count": 1,
        }
        unsafe["repositories"] = {
            "github.com/acme/private-repo": {"status": "recorded"},
            "repository_count": 1,
        }

        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as tmp:
            json.dump(unsafe, tmp)
            tmp_path = tmp.name
        try:
            result = self.run_script(
                "redact_run_event.py",
                tmp_path,
                "--mode",
                "redacted_content_opt_in",
                "--dry-run",
            )
        finally:
            Path(tmp_path).unlink(missing_ok=True)

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        payload = json.loads(result.stdout)
        redacted_event = payload["events"][0]
        self.assertNotIn("/home/ender/private/repo/file.txt", redacted_event["artifacts"])
        self.assertEqual(redacted_event["artifacts"]["safe_artifact_count"], 1)
        self.assertNotIn("github.com/acme/private-repo", redacted_event["repositories"])
        self.assertEqual(redacted_event["repositories"]["repository_count"], 1)
        self.assertEqual(
            set(payload["redacted_fields"]),
            {"unsafe dynamic key (real_path)", "unsafe dynamic key (real_repo)"},
        )
        output = result.stdout + result.stderr
        self.assertNotIn("/home/ender/private/repo/file.txt", output)
        self.assertNotIn("github.com/acme/private-repo", output)
        self.assertNotIn("private-repo", output)

    def test_redactor_removes_dynamic_short_repo_keys(self):
        unsafe = json.loads(SAMPLE.read_text(encoding="utf-8"))
        unsafe["repositories"] = {
            "acme/private-repo": {"status": "recorded"},
            "primary": "acme/private-repo",
            "repository_count": 1,
        }

        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as tmp:
            json.dump(unsafe, tmp)
            tmp_path = tmp.name
        try:
            result = self.run_script(
                "redact_run_event.py",
                tmp_path,
                "--mode",
                "metadata_only",
                "--dry-run",
            )
        finally:
            Path(tmp_path).unlink(missing_ok=True)

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        payload = json.loads(result.stdout)
        redacted_event = payload["events"][0]
        self.assertNotIn("acme/private-repo", redacted_event["repositories"])
        self.assertNotIn("primary", redacted_event["repositories"])
        self.assertEqual(redacted_event["repositories"]["repository_count"], 1)
        self.assertEqual(set(payload["redacted_fields"]), {"primary", "unsafe dynamic key (real_repo)"})
        output = result.stdout + result.stderr
        self.assertNotIn("acme/private-repo", output)
        self.assertNotIn("private-repo", output)

    def test_redactor_removes_nested_dynamic_short_repo_keys(self):
        unsafe = json.loads(SAMPLE.read_text(encoding="utf-8"))
        unsafe["repositories"] = {
            "by_status": {
                "acme/private-repo": {"status": "recorded"},
                "repository_count": 1,
            },
        }

        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as tmp:
            json.dump(unsafe, tmp)
            tmp_path = tmp.name
        try:
            result = self.run_script(
                "redact_run_event.py",
                tmp_path,
                "--mode",
                "metadata_only",
                "--dry-run",
            )
        finally:
            Path(tmp_path).unlink(missing_ok=True)

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        payload = json.loads(result.stdout)
        redacted_event = payload["events"][0]
        self.assertNotIn("acme/private-repo", redacted_event["repositories"]["by_status"])
        self.assertEqual(redacted_event["repositories"]["by_status"]["repository_count"], 1)
        self.assertEqual(set(payload["redacted_fields"]), {"unsafe dynamic key (real_repo)"})
        output = result.stdout + result.stderr
        self.assertNotIn("acme/private-repo", output)
        self.assertNotIn("private-repo", output)

    def test_redactor_removes_raw_prompt_in_redacted_content_opt_in_mode(self):
        unsafe = json.loads(SAMPLE.read_text(encoding="utf-8"))
        unsafe["raw_prompt"] = "private task prompt"

        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as tmp:
            json.dump(unsafe, tmp)
            tmp_path = tmp.name
        try:
            result = self.run_script(
                "redact_run_event.py",
                tmp_path,
                "--mode",
                "redacted_content_opt_in",
                "--dry-run",
            )
        finally:
            Path(tmp_path).unlink(missing_ok=True)

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        payload = json.loads(result.stdout)
        redacted_event = payload["events"][0]
        self.assertEqual(redacted_event["privacy_mode"], "redacted_content_opt_in")
        self.assertNotIn("raw_prompt", redacted_event)
        self.assertEqual(payload["redacted_fields"], ["raw_prompt"])

    def test_redactor_removes_raw_response_in_metadata_only_mode(self):
        unsafe = json.loads(SAMPLE.read_text(encoding="utf-8"))
        unsafe["raw_response"] = "private model response"

        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as tmp:
            json.dump(unsafe, tmp)
            tmp_path = tmp.name
        try:
            result = self.run_script(
                "redact_run_event.py",
                tmp_path,
                "--mode",
                "metadata_only",
                "--dry-run",
            )
        finally:
            Path(tmp_path).unlink(missing_ok=True)

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        payload = json.loads(result.stdout)
        redacted_event = payload["events"][0]
        self.assertNotIn("raw_response", redacted_event)
        self.assertEqual(payload["redacted_fields"], ["raw_response"])

    def test_redactor_removes_raw_response_in_redacted_content_opt_in_mode(self):
        unsafe = json.loads(SAMPLE.read_text(encoding="utf-8"))
        unsafe["raw_response"] = "private model response"

        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as tmp:
            json.dump(unsafe, tmp)
            tmp_path = tmp.name
        try:
            result = self.run_script(
                "redact_run_event.py",
                tmp_path,
                "--mode",
                "redacted_content_opt_in",
                "--dry-run",
            )
        finally:
            Path(tmp_path).unlink(missing_ok=True)

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        payload = json.loads(result.stdout)
        redacted_event = payload["events"][0]
        self.assertEqual(redacted_event["privacy_mode"], "redacted_content_opt_in")
        self.assertNotIn("raw_response", redacted_event)
        self.assertEqual(payload["redacted_fields"], ["raw_response"])

    def test_sync_export_refuses_redacted_content_opt_in_with_raw_prompt(self):
        unsafe = json.loads(SAMPLE.read_text(encoding="utf-8"))
        unsafe["privacy_mode"] = "redacted_content_opt_in"
        unsafe["raw_prompt"] = "private task prompt"

        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as tmp:
            json.dump(unsafe, tmp)
            input_path = tmp.name
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as tmp:
            export_path = tmp.name
        Path(export_path).unlink(missing_ok=True)

        try:
            result = self.run_script(
                "sync_run_events_to_github.py",
                "--input",
                input_path,
                "--export-out",
                export_path,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("raw_prompt", result.stdout + result.stderr)
            self.assertFalse(Path(export_path).exists())
        finally:
            Path(input_path).unlink(missing_ok=True)
            Path(export_path).unlink(missing_ok=True)

    def test_sync_export_refuses_redacted_content_opt_in_with_raw_response(self):
        unsafe = json.loads(SAMPLE.read_text(encoding="utf-8"))
        unsafe["privacy_mode"] = "redacted_content_opt_in"
        unsafe["raw_response"] = "private model response"

        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as tmp:
            json.dump(unsafe, tmp)
            input_path = tmp.name
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as tmp:
            export_path = tmp.name
        Path(export_path).unlink(missing_ok=True)

        try:
            result = self.run_script(
                "sync_run_events_to_github.py",
                "--input",
                input_path,
                "--export-out",
                export_path,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("raw_response", result.stdout + result.stderr)
            self.assertFalse(Path(export_path).exists())
        finally:
            Path(input_path).unlink(missing_ok=True)
            Path(export_path).unlink(missing_ok=True)

    def test_sync_export_refuses_unredacted_event_with_dynamic_unsafe_key(self):
        unsafe = json.loads(SAMPLE.read_text(encoding="utf-8"))
        unsafe["privacy_mode"] = "metadata_only"
        unsafe["artifacts"] = {
            "/home/ender/private/repo/file.txt": {"kind": "summary"},
        }

        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as tmp:
            json.dump(unsafe, tmp)
            input_path = tmp.name
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as tmp:
            export_path = tmp.name
        Path(export_path).unlink(missing_ok=True)

        try:
            result = self.run_script(
                "sync_run_events_to_github.py",
                "--input",
                input_path,
                "--export-out",
                export_path,
            )
            self.assertNotEqual(result.returncode, 0)
            output = result.stdout + result.stderr
            self.assertIn("unsafe dynamic key (real_path)", output)
            self.assertNotIn("/home/ender/private/repo/file.txt", output)
            self.assertNotIn("private/repo", output)
            self.assertFalse(Path(export_path).exists())
        finally:
            Path(input_path).unlink(missing_ok=True)
            Path(export_path).unlink(missing_ok=True)

    def test_sync_export_refuses_unredacted_event_with_dynamic_short_repo_key(self):
        unsafe = json.loads(SAMPLE.read_text(encoding="utf-8"))
        unsafe["privacy_mode"] = "metadata_only"
        unsafe["repositories"] = {
            "acme/private-repo": {"status": "recorded"},
        }

        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as tmp:
            json.dump(unsafe, tmp)
            input_path = tmp.name
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as tmp:
            export_path = tmp.name
        Path(export_path).unlink(missing_ok=True)

        try:
            result = self.run_script(
                "sync_run_events_to_github.py",
                "--input",
                input_path,
                "--export-out",
                export_path,
            )
            self.assertNotEqual(result.returncode, 0)
            output = result.stdout + result.stderr
            self.assertIn("unsafe dynamic key (real_repo)", output)
            self.assertNotIn("acme/private-repo", output)
            self.assertNotIn("private-repo", output)
            self.assertFalse(Path(export_path).exists())
        finally:
            Path(input_path).unlink(missing_ok=True)
            Path(export_path).unlink(missing_ok=True)

    def test_sync_export_refuses_unredacted_event_with_nested_dynamic_short_repo_key(self):
        unsafe = json.loads(SAMPLE.read_text(encoding="utf-8"))
        unsafe["privacy_mode"] = "metadata_only"
        unsafe["repositories"] = {
            "by_status": {
                "acme/private-repo": {"status": "recorded"},
            },
        }

        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as tmp:
            json.dump(unsafe, tmp)
            input_path = tmp.name
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as tmp:
            export_path = tmp.name
        Path(export_path).unlink(missing_ok=True)

        try:
            result = self.run_script(
                "sync_run_events_to_github.py",
                "--input",
                input_path,
                "--export-out",
                export_path,
            )
            self.assertNotEqual(result.returncode, 0)
            output = result.stdout + result.stderr
            self.assertIn("unsafe dynamic key (real_repo)", output)
            self.assertNotIn("acme/private-repo", output)
            self.assertNotIn("private-repo", output)
            self.assertFalse(Path(export_path).exists())
        finally:
            Path(input_path).unlink(missing_ok=True)
            Path(export_path).unlink(missing_ok=True)

    def test_sync_dry_run_reports_counts_without_upload(self):
        result = self.run_script(
            "sync_run_events_to_github.py",
            "--dry-run",
            "--input",
            str(SAMPLE),
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["mode"], "dry_run")
        self.assertEqual(payload["event_count"], 1)
        self.assertFalse(payload["would_upload"])

    def test_sync_upload_requires_explicit_config(self):
        result = self.run_script(
            "sync_run_events_to_github.py",
            "--upload",
            "--input",
            str(SAMPLE),
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("explicit destination", result.stdout + result.stderr)

    def test_sync_simulated_upload_records_sent_and_refuses_duplicate(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            env = {"CYBERNETIC_SYNC_TOKEN": "dummy-token"}
            first = self.run_script(
                "sync_run_events_to_github.py",
                "--upload",
                "--simulate-upload",
                "--destination",
                "example/repo",
                "--token-env",
                "CYBERNETIC_SYNC_TOKEN",
                "--state-dir",
                tmpdir,
                "--input",
                str(SAMPLE),
                env=env,
            )
            self.assertEqual(first.returncode, 0, first.stdout + first.stderr)
            first_payload = json.loads(first.stdout)
            self.assertEqual(first_payload["status"], "sent")

            duplicate = self.run_script(
                "sync_run_events_to_github.py",
                "--upload",
                "--simulate-upload",
                "--destination",
                "example/repo",
                "--token-env",
                "CYBERNETIC_SYNC_TOKEN",
                "--state-dir",
                tmpdir,
                "--input",
                str(SAMPLE),
                env=env,
            )
            self.assertNotEqual(duplicate.returncode, 0)
            self.assertIn("duplicate send refused", duplicate.stdout + duplicate.stderr)


if __name__ == "__main__":
    unittest.main()
