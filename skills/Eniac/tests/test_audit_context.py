from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL_ROOT / "scripts"))

from audit_context import audit_context, budget_errors  # noqa: E402


class AuditContextTests(unittest.TestCase):
    def test_measures_entry_routes_and_ranked_references(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            skill = Path(directory) / "Eniac"
            references = skill / "references"
            references.mkdir(parents=True)
            (skill / "SKILL.md").write_text(
                "# Eniac\n\nUse references/a.md twice: references/a.md. ไทย\n",
                encoding="utf-8",
            )
            (references / "a.md").write_text("# A\nsmall\n", encoding="utf-8")
            (references / "b.md").write_text(
                "# B\nthis reference is larger\n",
                encoding="utf-8",
            )

            metrics = audit_context(skill, largest=2)

            self.assertEqual(metrics.entry.lines, 3)
            self.assertGreater(metrics.entry.utf8_bytes, metrics.entry.characters)
            self.assertEqual(metrics.reference_files, 2)
            self.assertEqual(metrics.direct_reference_routes, 1)
            self.assertEqual(
                [item.path for item in metrics.largest_references],
                ["references/b.md", "references/a.md"],
            )

    def test_entry_budget_is_optional_and_enforceable(self) -> None:
        metrics = audit_context(SKILL_ROOT, largest=0)

        self.assertEqual(budget_errors(metrics, None), [])
        self.assertEqual(budget_errors(metrics, metrics.entry.characters), [])
        self.assertTrue(
            any(
                "context budget exceeded" in error
                for error in budget_errors(metrics, metrics.entry.characters - 1)
            )
        )
        self.assertTrue(budget_errors(metrics, 0))


if __name__ == "__main__":
    unittest.main()
