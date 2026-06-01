import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MATRIX = ROOT / "docs/cybernetic-framework/invariant-artifact-consumer-matrix.md"


class InvariantConsumerMatrixTest(unittest.TestCase):
    def parse_matrix_rows(self):
        text = MATRIX.read_text(encoding="utf-8")
        lines = text.splitlines()
        header_index = next(
            index
            for index, line in enumerate(lines)
            if line.startswith("| ID | Invariant |")
        )
        headers = [cell.strip() for cell in lines[header_index].strip("|").split("|")]
        rows = []
        for line in lines[header_index + 2 :]:
            if not line.startswith("|"):
                break
            cells = [cell.strip() for cell in line.strip("|").split("|")]
            rows.append(dict(zip(headers, cells, strict=True)))
        return headers, rows

    def test_matrix_exists_with_required_consumer_columns(self):
        self.assertTrue(MATRIX.exists())
        headers, rows = self.parse_matrix_rows()

        self.assertEqual(
            headers,
            [
                "ID",
                "Invariant",
                "Source skill",
                "Artifact field/template",
                "Guard",
                "Review",
                "Compiler/downstream",
                "Regression coverage",
                "Status",
            ],
        )
        self.assertGreaterEqual(len(rows), 12)

    def test_matrix_rows_have_no_empty_or_placeholder_consumers(self):
        _headers, rows = self.parse_matrix_rows()
        checked_columns = [
            "Source skill",
            "Artifact field/template",
            "Guard",
            "Review",
            "Compiler/downstream",
            "Regression coverage",
            "Status",
        ]
        for row in rows:
            with self.subTest(row=row["ID"]):
                for column in checked_columns:
                    value = row[column]
                    self.assertTrue(value)
                    self.assertNotIn("TBD", value)
                    self.assertNotIn("TODO", value)
                self.assertEqual(row["Status"], "Active")

    def test_matrix_tracks_recent_guard_invariants(self):
        _headers, rows = self.parse_matrix_rows()
        ids = {row["ID"] for row in rows}

        self.assertIn("INV-TOP-001", ids)
        self.assertIn("INV-TOP-002", ids)
        self.assertIn("INV-TOP-003", ids)
        self.assertIn("INV-TOP-004", ids)
        self.assertIn("INV-TOP-005", ids)
        self.assertIn("INV-OBS-001", ids)

    def test_readme_links_to_matrix_for_framework_maintenance(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")

        self.assertIn(
            "docs/cybernetic-framework/invariant-artifact-consumer-matrix.md",
            readme,
        )


if __name__ == "__main__":
    unittest.main()
