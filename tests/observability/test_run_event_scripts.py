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
