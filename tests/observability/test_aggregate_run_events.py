import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SAMPLE = ROOT / "observability" / "examples" / "metadata-only-event.json"


class AggregateRunEventsTest(unittest.TestCase):
    def run_aggregate(self, *args):
        return subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "aggregate_run_events.py"), *args],
            cwd=ROOT,
            text=True,
            capture_output=True,
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

    def test_dry_run_writes_machine_readable_summary_and_eval_candidates(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            summary = Path(tmpdir) / "aggregation-summary.json"
            candidates = Path(tmpdir) / "eval-candidates.json"
            result = self.run_aggregate(
                "--input",
                str(SAMPLE),
                "--out",
                str(summary),
                "--eval-candidates-out",
                str(candidates),
                "--dry-run",
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

            summary_payload = json.loads(summary.read_text(encoding="utf-8"))
            candidates_payload = json.loads(candidates.read_text(encoding="utf-8"))

        self.assertEqual(summary_payload["event_count"], 1)
        self.assertEqual(summary_payload["taxonomy_counts"]["observability.metadata_only_recorded"], 1)
        self.assertIn("skill_pack_versions", summary_payload)
        self.assertEqual(candidates_payload["schema_version"], "1.0.0")
        self.assertIn("candidates", candidates_payload)

    def test_dry_run_accepts_two_line_jsonl(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = Path(tmpdir) / "events.jsonl"
            summary = Path(tmpdir) / "aggregation-summary.json"
            candidates = Path(tmpdir) / "eval-candidates.json"
            self.write_two_event_jsonl(input_path)

            result = self.run_aggregate(
                "--input",
                str(input_path),
                "--out",
                str(summary),
                "--eval-candidates-out",
                str(candidates),
                "--dry-run",
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            summary_payload = json.loads(summary.read_text(encoding="utf-8"))

        self.assertEqual(summary_payload["event_count"], 2)
        self.assertEqual(summary_payload["event_type_counts"]["runtime_outcome"], 1)
        self.assertEqual(summary_payload["event_type_counts"]["skill_invoked"], 1)

    def test_generated_at_can_be_set_for_deterministic_outputs(self):
        generated_at = "2026-01-02T03:04:05Z"
        with tempfile.TemporaryDirectory() as tmpdir:
            summary = Path(tmpdir) / "aggregation-summary.json"
            candidates = Path(tmpdir) / "eval-candidates.json"
            result = self.run_aggregate(
                "--input",
                str(SAMPLE),
                "--out",
                str(summary),
                "--eval-candidates-out",
                str(candidates),
                "--dry-run",
                "--generated-at",
                generated_at,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

            summary_payload = json.loads(summary.read_text(encoding="utf-8"))
            candidates_payload = json.loads(candidates.read_text(encoding="utf-8"))

        self.assertEqual(summary_payload["generated_at"], generated_at)
        self.assertEqual(candidates_payload["generated_at"], generated_at)

    def test_failure_taxonomy_code_generates_eval_candidate(self):
        event = json.loads(SAMPLE.read_text(encoding="utf-8"))
        event["event_id"] = "evt_failure_candidate"
        event["event"] = "blocked"
        event["status"] = "blocked"
        event["taxonomy_codes"] = ["routing.over_control"]

        with tempfile.TemporaryDirectory() as tmpdir:
            event_path = Path(tmpdir) / "event.json"
            summary = Path(tmpdir) / "aggregation-summary.json"
            candidates = Path(tmpdir) / "eval-candidates.json"
            event_path.write_text(json.dumps(event), encoding="utf-8")
            result = self.run_aggregate(
                "--input",
                str(event_path),
                "--out",
                str(summary),
                "--eval-candidates-out",
                str(candidates),
                "--dry-run",
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            candidates_payload = json.loads(candidates.read_text(encoding="utf-8"))

        self.assertEqual(len(candidates_payload["candidates"]), 1)
        self.assertEqual(candidates_payload["candidates"][0]["taxonomy_code"], "routing.over_control")
        self.assertIn("assertions", candidates_payload["candidates"][0])

    def test_dry_run_sanitizes_underscore_composite_unsafe_key_validation_output(self):
        event = json.loads(SAMPLE.read_text(encoding="utf-8"))
        event["repoName_acme_private_repo"] = {"details": "/home/ender/private/repo"}
        event["repositoryName_acme_private_repo"] = {"details": "/home/ender/private/repo"}
        event["rawResponse_acme_private_repo"] = {"details": "/home/ender/private/repo"}

        with tempfile.TemporaryDirectory() as tmpdir:
            event_path = Path(tmpdir) / "event.json"
            summary = Path(tmpdir) / "aggregation-summary.json"
            candidates = Path(tmpdir) / "eval-candidates.json"
            event_path.write_text(json.dumps(event), encoding="utf-8")
            result = self.run_aggregate(
                "--input",
                str(event_path),
                "--out",
                str(summary),
                "--eval-candidates-out",
                str(candidates),
                "--dry-run",
            )

        output = result.stdout + result.stderr
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("unsafe field unsafe key (repo_name)", output)
        self.assertIn("unsafe field unsafe key (repository_name)", output)
        self.assertIn("unsafe field unsafe key (raw_response)", output)
        self.assertIn("unsafe metadata-only value at $.<unsafe-key>.details", output)
        self.assertNotIn("repoName_acme_private_repo", output)
        self.assertNotIn("repositoryName_acme_private_repo", output)
        self.assertNotIn("rawResponse_acme_private_repo", output)
        self.assertNotIn("acme_private_repo", output)
        self.assertNotIn("/home", output)

    def test_dry_run_sanitizes_hyphen_and_camel_composite_unsafe_key_validation_output(self):
        event = json.loads(SAMPLE.read_text(encoding="utf-8"))
        event["repoName-acme-private-repo"] = {"details": "/home/ender/private/repo"}
        event["repositoryName-acme-private-repo"] = {"details": "/home/ender/private/repo"}
        event["rawResponse-acme-private-repo"] = {"details": "/home/ender/private/repo"}
        event["repoNameAcmePrivateRepo"] = {"details": "/home/ender/private/repo"}

        with tempfile.TemporaryDirectory() as tmpdir:
            event_path = Path(tmpdir) / "event.json"
            summary = Path(tmpdir) / "aggregation-summary.json"
            candidates = Path(tmpdir) / "eval-candidates.json"
            event_path.write_text(json.dumps(event), encoding="utf-8")
            result = self.run_aggregate(
                "--input",
                str(event_path),
                "--out",
                str(summary),
                "--eval-candidates-out",
                str(candidates),
                "--dry-run",
            )

        output = result.stdout + result.stderr
        self.assertNotEqual(result.returncode, 0)
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

    def test_dry_run_sanitizes_repo_private_event_keys_without_parent_context(self):
        event = json.loads(SAMPLE.read_text(encoding="utf-8"))
        for key in (
            "acme/private-repo",
            "acme_private_repo",
            "privateRepo",
            "repoAcmePrivateRepo",
            "repositoryAcmePrivateRepo",
        ):
            event[key] = {"details": "/home/ender/private/repo"}

        with tempfile.TemporaryDirectory() as tmpdir:
            event_path = Path(tmpdir) / "event.json"
            summary = Path(tmpdir) / "aggregation-summary.json"
            candidates = Path(tmpdir) / "eval-candidates.json"
            event_path.write_text(json.dumps(event), encoding="utf-8")
            result = self.run_aggregate(
                "--input",
                str(event_path),
                "--out",
                str(summary),
                "--eval-candidates-out",
                str(candidates),
                "--dry-run",
            )

        output = result.stdout + result.stderr
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("unsafe field unsafe key (real_repo)", output)
        self.assertIn("unsafe metadata-only value at $.<unsafe-key>.details", output)
        self.assertNotIn("acme/private-repo", output)
        self.assertNotIn("acme_private_repo", output)
        self.assertNotIn("privateRepo", output)
        self.assertNotIn("repoAcmePrivateRepo", output)
        self.assertNotIn("repositoryAcmePrivateRepo", output)
        self.assertNotIn("private-repo", output)
        self.assertNotIn("/home", output)


if __name__ == "__main__":
    unittest.main()
