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

    def write_two_event_jsonl(self, path):
        first = json.loads(SAMPLE.read_text(encoding="utf-8"))
        second = dict(first)
        second["event_id"] = "evt_jsonl_second"
        second["event"] = "runtime_outcome"
        path.write_text(
            "\n".join(json.dumps(event) for event in (first, second)) + "\n",
            encoding="utf-8",
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

    def test_record_run_event_does_not_use_caller_repo_head_as_source_commit(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            caller_repo = Path(tmpdir) / "caller-repo"
            caller_repo.mkdir()
            subprocess.run(["git", "init"], cwd=caller_repo, check=True, text=True, capture_output=True)
            subprocess.run(["git", "config", "user.email", "test@example.invalid"], cwd=caller_repo, check=True)
            subprocess.run(["git", "config", "user.name", "Test User"], cwd=caller_repo, check=True)
            (caller_repo / "private.txt").write_text("private caller repo\n", encoding="utf-8")
            subprocess.run(["git", "add", "private.txt"], cwd=caller_repo, check=True)
            subprocess.run(["git", "commit", "-m", "private caller commit"], cwd=caller_repo, check=True, text=True, capture_output=True)
            private_head = subprocess.run(
                ["git", "rev-parse", "--short", "HEAD"],
                cwd=caller_repo,
                check=True,
                text=True,
                capture_output=True,
            ).stdout.strip()

            result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts" / "record_run_event.py"),
                    "--event",
                    "skill_invoked",
                    "--skill",
                    "routing-cybernetic-workflows",
                    "--status",
                    "success",
                    "--machine-id",
                    "anon-testmachine",
                    "--task-hash",
                    "sha256:" + "e" * 64,
                    "--dry-run",
                ],
                cwd=caller_repo,
                text=True,
                capture_output=True,
            )

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        event = json.loads(result.stdout)
        self.assertNotEqual(event["skill_pack"].get("source_commit"), private_head)

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

    def test_redactor_sanitizes_composite_unsafe_key_redacted_fields(self):
        unsafe = json.loads(SAMPLE.read_text(encoding="utf-8"))
        for key in ("repoName_acme/private-repo", "repositoryName_acme/private-repo", "rawResponse_acme/private-repo"):
            unsafe[key] = "private metadata"

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
        for key in ("repoName_acme/private-repo", "repositoryName_acme/private-repo", "rawResponse_acme/private-repo"):
            self.assertNotIn(key, redacted_event)
        output = result.stdout + result.stderr
        self.assertIn("repo_name", output)
        self.assertIn("repository_name", output)
        self.assertIn("raw_response", output)
        self.assertNotIn("acme/private-repo", output)
        self.assertNotIn("private-repo", output)

    def test_redactor_sanitizes_underscore_composite_unsafe_key_redacted_fields(self):
        unsafe = json.loads(SAMPLE.read_text(encoding="utf-8"))
        for key in ("repoName_acme_private_repo", "repositoryName_acme_private_repo", "rawResponse_acme_private_repo"):
            unsafe[key] = "private metadata"

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
        for key in ("repoName_acme_private_repo", "repositoryName_acme_private_repo", "rawResponse_acme_private_repo"):
            self.assertNotIn(key, redacted_event)
        self.assertEqual(set(payload["redacted_fields"]), {"unsafe key (repo_name)", "unsafe key (repository_name)", "unsafe key (raw_response)"})
        output = result.stdout + result.stderr
        self.assertNotIn("repoName_acme_private_repo", output)
        self.assertNotIn("repositoryName_acme_private_repo", output)
        self.assertNotIn("rawResponse_acme_private_repo", output)
        self.assertNotIn("acme_private_repo", output)

    def test_redactor_sanitizes_hyphen_and_camel_composite_unsafe_key_redacted_fields(self):
        unsafe = json.loads(SAMPLE.read_text(encoding="utf-8"))
        for key in (
            "repoName-acme-private-repo",
            "repositoryName-acme-private-repo",
            "rawResponse-acme-private-repo",
            "repoNameAcmePrivateRepo",
        ):
            unsafe[key] = {"details": "/home/ender/private/repo"}

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
        for key in (
            "repoName-acme-private-repo",
            "repositoryName-acme-private-repo",
            "rawResponse-acme-private-repo",
            "repoNameAcmePrivateRepo",
        ):
            self.assertNotIn(key, redacted_event)
        self.assertEqual(set(payload["redacted_fields"]), {"unsafe key (repo_name)", "unsafe key (repository_name)", "unsafe key (raw_response)"})
        output = result.stdout + result.stderr
        self.assertNotIn("repoName-acme-private-repo", output)
        self.assertNotIn("repositoryName-acme-private-repo", output)
        self.assertNotIn("rawResponse-acme-private-repo", output)
        self.assertNotIn("repoNameAcmePrivateRepo", output)
        self.assertNotIn("acme-private-repo", output)
        self.assertNotIn("AcmePrivateRepo", output)
        self.assertNotIn("/home", output)

    def test_redactor_sanitizes_repo_private_event_keys_without_parent_context(self):
        unsafe = json.loads(SAMPLE.read_text(encoding="utf-8"))
        for key in (
            "acme/private-repo",
            "acme_private_repo",
            "privateRepo",
            "repoAcmePrivateRepo",
            "repositoryAcmePrivateRepo",
        ):
            unsafe[key] = {"details": "/home/ender/private/repo"}

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
        for key in (
            "acme/private-repo",
            "acme_private_repo",
            "privateRepo",
            "repoAcmePrivateRepo",
            "repositoryAcmePrivateRepo",
        ):
            self.assertNotIn(key, redacted_event)
        self.assertEqual(payload["redacted_fields"], ["unsafe key (real_repo)"])
        output = result.stdout + result.stderr
        self.assertNotIn("acme/private-repo", output)
        self.assertNotIn("acme_private_repo", output)
        self.assertNotIn("privateRepo", output)
        self.assertNotIn("repoAcmePrivateRepo", output)
        self.assertNotIn("repositoryAcmePrivateRepo", output)
        self.assertNotIn("private-repo", output)
        self.assertNotIn("/home", output)

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

    def test_redactor_removes_general_short_repo_key_without_echoing_it(self):
        unsafe = json.loads(SAMPLE.read_text(encoding="utf-8"))
        unsafe["acme/service"] = {"status": "recorded"}

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
        self.assertNotIn("acme/service", redacted_event)
        self.assertEqual(payload["redacted_fields"], ["unsafe dynamic key (real_repo)"])
        output = result.stdout + result.stderr
        self.assertNotIn("acme/service", output)
        self.assertNotIn("service", output)

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

    def test_redactor_removes_nested_raw_response_without_echoing_value(self):
        unsafe = json.loads(SAMPLE.read_text(encoding="utf-8"))
        unsafe["raw"] = {
            "response": "private model response",
            "content": "private content",
            "message_count": 2,
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
        self.assertEqual(redacted_event["raw"], {"message_count": 2})
        self.assertEqual(set(payload["redacted_fields"]), {"raw_content", "raw_response"})
        output = result.stdout + result.stderr
        self.assertNotIn("private model response", output)
        self.assertNotIn("private content", output)

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

    def test_sync_export_refuses_unredacted_event_with_nested_raw_response(self):
        unsafe = json.loads(SAMPLE.read_text(encoding="utf-8"))
        unsafe["privacy_mode"] = "metadata_only"
        unsafe["raw"] = {"response": "private model response"}

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
            self.assertIn("raw_response", output)
            self.assertNotIn("private model response", output)
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

    def test_sync_export_refuses_composite_unsafe_keys_without_repo_fragment(self):
        unsafe = json.loads(SAMPLE.read_text(encoding="utf-8"))
        unsafe["privacy_mode"] = "metadata_only"
        for key in ("repoName_acme/private-repo", "repositoryName_acme/private-repo", "rawResponse_acme/private-repo"):
            unsafe[key] = "private metadata"

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
            self.assertIn("repo_name", output)
            self.assertIn("repository_name", output)
            self.assertIn("raw_response", output)
            self.assertNotIn("acme/private-repo", output)
            self.assertNotIn("private-repo", output)
            self.assertFalse(Path(export_path).exists())
        finally:
            Path(input_path).unlink(missing_ok=True)
            Path(export_path).unlink(missing_ok=True)

    def test_sync_export_sanitizes_underscore_composite_unsafe_keys(self):
        unsafe = json.loads(SAMPLE.read_text(encoding="utf-8"))
        unsafe["privacy_mode"] = "metadata_only"
        for key in ("repoName_acme_private_repo", "repositoryName_acme_private_repo", "rawResponse_acme_private_repo"):
            unsafe[key] = {"details": "/home/ender/private/repo"}

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
            self.assertIn("unsafe field unsafe key (repo_name)", output)
            self.assertIn("unsafe field unsafe key (repository_name)", output)
            self.assertIn("unsafe field unsafe key (raw_response)", output)
            self.assertIn("unsafe metadata-only value at $.<unsafe-key>.details", output)
            self.assertNotIn("repoName_acme_private_repo", output)
            self.assertNotIn("repositoryName_acme_private_repo", output)
            self.assertNotIn("rawResponse_acme_private_repo", output)
            self.assertNotIn("acme_private_repo", output)
            self.assertNotIn("/home", output)
            self.assertFalse(Path(export_path).exists())
        finally:
            Path(input_path).unlink(missing_ok=True)
            Path(export_path).unlink(missing_ok=True)

    def test_sync_export_sanitizes_composite_unsafe_key_in_value_path(self):
        unsafe = json.loads(SAMPLE.read_text(encoding="utf-8"))
        unsafe["privacy_mode"] = "metadata_only"
        unsafe["repoName_acme/private-repo"] = {"details": "/home/ender/private/repo"}

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
            self.assertIn("unsafe field unsafe key (repo_name)", output)
            self.assertIn("unsafe metadata-only value at $.<unsafe-key>.details", output)
            self.assertNotIn("repoName_acme/private-repo", output)
            self.assertNotIn("acme/private-repo", output)
            self.assertNotIn("private-repo", output)
            self.assertNotIn("/home", output)
            self.assertFalse(Path(export_path).exists())
        finally:
            Path(input_path).unlink(missing_ok=True)
            Path(export_path).unlink(missing_ok=True)

    def test_sync_export_sanitizes_hyphen_and_camel_composite_unsafe_keys(self):
        unsafe = json.loads(SAMPLE.read_text(encoding="utf-8"))
        unsafe["privacy_mode"] = "metadata_only"
        for key in (
            "repoName-acme-private-repo",
            "repositoryName-acme-private-repo",
            "rawResponse-acme-private-repo",
            "repoNameAcmePrivateRepo",
        ):
            unsafe[key] = {"details": "/home/ender/private/repo"}

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
            self.assertIn("unsafe field unsafe key (repo_name)", output)
            self.assertIn("unsafe field unsafe key (repository_name)", output)
            self.assertIn("unsafe field unsafe key (raw_response)", output)
            self.assertIn("unsafe metadata-only value at $.<unsafe-key>.details", output)
            self.assertNotIn("repoName-acme-private-repo", output)
            self.assertNotIn("repositoryName-acme-private-repo", output)
            self.assertNotIn("rawResponse-acme-private-repo", output)
            self.assertNotIn("repoNameAcmePrivateRepo", output)
            self.assertNotIn("acme-private-repo", output)
            self.assertNotIn("AcmePrivateRepo", output)
            self.assertNotIn("/home", output)
            self.assertFalse(Path(export_path).exists())
        finally:
            Path(input_path).unlink(missing_ok=True)
            Path(export_path).unlink(missing_ok=True)

    def test_sync_export_sanitizes_repo_private_event_keys_without_parent_context(self):
        unsafe = json.loads(SAMPLE.read_text(encoding="utf-8"))
        unsafe["privacy_mode"] = "metadata_only"
        for key in (
            "acme/private-repo",
            "acme_private_repo",
            "privateRepo",
            "repoAcmePrivateRepo",
            "repositoryAcmePrivateRepo",
        ):
            unsafe[key] = {"details": "/home/ender/private/repo"}

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
            self.assertIn("unsafe field unsafe key (real_repo)", output)
            self.assertIn("unsafe metadata-only value at $.<unsafe-key>.details", output)
            self.assertNotIn("acme/private-repo", output)
            self.assertNotIn("acme_private_repo", output)
            self.assertNotIn("privateRepo", output)
            self.assertNotIn("repoAcmePrivateRepo", output)
            self.assertNotIn("repositoryAcmePrivateRepo", output)
            self.assertNotIn("private-repo", output)
            self.assertNotIn("/home", output)
            self.assertFalse(Path(export_path).exists())
        finally:
            Path(input_path).unlink(missing_ok=True)
            Path(export_path).unlink(missing_ok=True)

    def test_sync_export_refuses_general_short_repo_key_without_echoing_it(self):
        unsafe = json.loads(SAMPLE.read_text(encoding="utf-8"))
        unsafe["privacy_mode"] = "metadata_only"
        unsafe["acme/service"] = {"details": "/home/ender/private/work"}

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
            self.assertIn("unsafe field unsafe dynamic key (real_repo)", output)
            self.assertIn("unsafe metadata-only value at $.<unsafe-key>.details", output)
            self.assertNotIn("acme/service", output)
            self.assertNotIn("service", output)
            self.assertNotIn("/home", output)
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

    def test_sync_dry_run_accepts_two_line_jsonl_without_upload(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = Path(tmpdir) / "events.jsonl"
            self.write_two_event_jsonl(input_path)

            result = self.run_script(
                "sync_run_events_to_github.py",
                "--dry-run",
                "--input",
                str(input_path),
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            payload = json.loads(result.stdout)

        self.assertEqual(payload["mode"], "dry_run")
        self.assertEqual(payload["event_count"], 2)
        self.assertFalse(payload["would_upload"])

    def test_sync_export_accepts_two_line_jsonl_without_upload(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = Path(tmpdir) / "events.jsonl"
            export_path = Path(tmpdir) / "export.json"
            self.write_two_event_jsonl(input_path)

            result = self.run_script(
                "sync_run_events_to_github.py",
                "--input",
                str(input_path),
                "--export-out",
                str(export_path),
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            stdout_payload = json.loads(result.stdout)
            export_payload = json.loads(export_path.read_text(encoding="utf-8"))

        self.assertEqual(stdout_payload["mode"], "export")
        self.assertEqual(stdout_payload["event_count"], 2)
        self.assertFalse(stdout_payload["would_upload"])
        self.assertEqual(export_payload["event_count"], 2)
        self.assertEqual(len(export_payload["events"]), 2)

    def test_sync_export_package_validates_then_aggregates(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = Path(tmpdir) / "events.jsonl"
            export_path = Path(tmpdir) / "export.json"
            summary_path = Path(tmpdir) / "summary.json"
            candidates_path = Path(tmpdir) / "candidates.json"
            self.write_two_event_jsonl(input_path)

            export = self.run_script(
                "sync_run_events_to_github.py",
                "--input",
                str(input_path),
                "--export-out",
                str(export_path),
            )
            self.assertEqual(export.returncode, 0, export.stdout + export.stderr)

            validation = self.run_script("validate_run_events.py", str(export_path))
            self.assertEqual(validation.returncode, 0, validation.stdout + validation.stderr)
            self.assertIn("validated 2 events", validation.stdout)

            aggregate = self.run_script(
                "aggregate_run_events.py",
                "--input",
                str(export_path),
                "--out",
                str(summary_path),
                "--eval-candidates-out",
                str(candidates_path),
                "--dry-run",
            )
            self.assertEqual(aggregate.returncode, 0, aggregate.stdout + aggregate.stderr)
            summary_payload = json.loads(summary_path.read_text(encoding="utf-8"))

        self.assertEqual(summary_payload["event_count"], 2)

    def test_sync_dry_run_rejects_unsafe_export_package_without_leaking_values(self):
        event = json.loads(SAMPLE.read_text(encoding="utf-8"))
        package = {
            "mode": "export",
            "event_count": 1,
            "event_ids": ["acme/private-repo"],
            "package_id": "pkg_acme/private-repo",
            "destination_hash": None,
            "taxonomy_counts": {"observability.metadata_only_recorded": 1},
            "would_upload": False,
            "events": [event],
        }

        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = Path(tmpdir) / "export.json"
            input_path.write_text(json.dumps(package), encoding="utf-8")

            result = self.run_script(
                "sync_run_events_to_github.py",
                "--dry-run",
                "--input",
                str(input_path),
            )

        output = result.stdout + result.stderr
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("package_id", output)
        self.assertIn("event_ids", output)
        self.assertNotIn("acme/private-repo", output)

    def test_sync_dry_run_dominates_simulated_upload_without_ledger_writes(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            env = {"CYBERNETIC_SYNC_TOKEN": "dummy-token"}
            result = self.run_script(
                "sync_run_events_to_github.py",
                "--dry-run",
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

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["mode"], "dry_run")
            self.assertFalse(payload["would_upload"])
            self.assertFalse((Path(tmpdir) / "pending.json").exists())
            self.assertFalse((Path(tmpdir) / "sent.json").exists())

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
