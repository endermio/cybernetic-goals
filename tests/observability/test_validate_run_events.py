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
