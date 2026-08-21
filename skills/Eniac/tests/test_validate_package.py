from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT_CANDIDATE = Path(__file__).resolve().parents[3]
REPO_ROOT = (
    REPO_ROOT_CANDIDATE if (REPO_ROOT_CANDIDATE / "README.md").is_file() else None
)
sys.path.insert(0, str(SKILL_ROOT / "scripts"))

from validate_package import validate_package  # noqa: E402


class ValidatePackageTests(unittest.TestCase):
    def test_repository_package_passes(self) -> None:
        self.assertEqual(validate_package(SKILL_ROOT, REPO_ROOT), [])

    def test_detects_unrouted_reference(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            skill = Path(directory) / "Eniac"
            references = skill / "references"
            references.mkdir(parents=True)
            (skill / "SKILL.md").write_text(
                "\n".join(
                    (
                        "---",
                        "name: eniac",
                        'description: "Test Eniac skill."',
                        "---",
                        "",
                        "# Eniac",
                        "",
                        "Use [a](references/a.md).",
                        "",
                    )
                ),
                encoding="utf-8",
            )
            (references / "a.md").write_text("# A\n", encoding="utf-8")
            (references / "orphan.md").write_text(
                "# Orphan\n\nSelf: references/orphan.md\n",
                encoding="utf-8",
            )

            errors = validate_package(skill)

            self.assertTrue(
                any("reference is unreachable" in error for error in errors),
                errors,
            )

    def test_detects_missing_local_link(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            skill = Path(directory) / "Eniac"
            references = skill / "references"
            references.mkdir(parents=True)
            (skill / "SKILL.md").write_text(
                "\n".join(
                    (
                        "---",
                        "name: eniac",
                        'description: "Test Eniac skill."',
                        "---",
                        "",
                        "# Eniac",
                        "",
                        "Use [missing](references/missing.md).",
                        "",
                    )
                ),
                encoding="utf-8",
            )

            errors = validate_package(skill)

            self.assertTrue(
                any("missing reference" in error for error in errors),
                errors,
            )

    def test_detects_missing_local_anchor(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            skill = Path(directory) / "Eniac"
            references = skill / "references"
            references.mkdir(parents=True)
            (skill / "SKILL.md").write_text(
                "\n".join(
                    (
                        "---",
                        "name: eniac",
                        'description: "Test Eniac skill."',
                        "---",
                        "",
                        "# Eniac",
                        "",
                        "Use [a](references/a.md#missing-section).",
                        "",
                    )
                ),
                encoding="utf-8",
            )
            (references / "a.md").write_text("# A\n", encoding="utf-8")

            errors = validate_package(skill)

            self.assertTrue(
                any("missing local anchor" in error for error in errors),
                errors,
            )

    def test_ignores_example_links_inside_fenced_templates(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            skill = Path(directory) / "Eniac"
            references = skill / "references"
            references.mkdir(parents=True)
            (skill / "SKILL.md").write_text(
                "\n".join(
                    (
                        "---",
                        "name: eniac",
                        'description: "Test Eniac skill."',
                        "---",
                        "",
                        "# Eniac",
                        "",
                        "Use [template](references/template.md).",
                        "",
                    )
                ),
                encoding="utf-8",
            )
            (references / "template.md").write_text(
                "# Template\n\n```markdown\n[License](LICENSE)\n```\n",
                encoding="utf-8",
            )

            self.assertEqual(validate_package(skill), [])

    def test_routes_reference_graph_through_relative_markdown_link(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            skill = Path(directory) / "Eniac"
            references = skill / "references"
            nested = references / "nested"
            nested.mkdir(parents=True)
            (skill / "SKILL.md").write_text(
                "\n".join(
                    (
                        "---",
                        "name: eniac",
                        'description: "Test Eniac skill."',
                        "---",
                        "",
                        "# Eniac",
                        "",
                        "Use `references/router.md`.",
                        "",
                    )
                ),
                encoding="utf-8",
            )
            (references / "router.md").write_text(
                "# Router\n\nRead [child](nested/child.md).\n",
                encoding="utf-8",
            )
            (nested / "child.md").write_text("# Child\n", encoding="utf-8")

            self.assertEqual(validate_package(skill), [])

    def test_detects_stale_readme_reference_count(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            skill = repo / "skills" / "Eniac"
            references = skill / "references"
            references.mkdir(parents=True)
            (skill / "SKILL.md").write_text(
                "\n".join(
                    (
                        "---",
                        "name: eniac",
                        'description: "Test Eniac skill."',
                        "---",
                        "",
                        "# Eniac",
                        "",
                        "Use [a](references/a.md).",
                        "",
                    )
                ),
                encoding="utf-8",
            )
            (references / "a.md").write_text("# A\n", encoding="utf-8")
            (repo / "README.md").write_text(
                "Package has 2 reference files.\n",
                encoding="utf-8",
            )

            errors = validate_package(skill, repo)

            self.assertTrue(
                any("reference count is stale" in error for error in errors),
                errors,
            )

    def test_detects_invalid_evaluation_scenario(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            skill = Path(directory) / "Eniac"
            (skill / "references").mkdir(parents=True)
            evals = skill / "evals"
            evals.mkdir()
            (skill / "SKILL.md").write_text(
                "\n".join(
                    (
                        "---",
                        "name: eniac",
                        'description: "Test Eniac skill."',
                        "---",
                        "",
                        "# Eniac",
                        "",
                    )
                ),
                encoding="utf-8",
            )
            (evals / "scenarios.json").write_text(
                """
{
  "schema_version": 1,
  "scenarios": [
    {
      "id": "Bad Id",
      "kind": "unknown",
      "prompt": "",
      "expected": [],
      "anti_patterns": []
    }
  ]
}
""".strip(),
                encoding="utf-8",
            )

            errors = validate_package(skill)

            self.assertTrue(any("lower-kebab-case" in error for error in errors))
            self.assertTrue(any("kind must be one of" in error for error in errors))
            self.assertTrue(any("prompt must be" in error for error in errors))
            self.assertTrue(any("expected must be" in error for error in errors))

    def test_detects_duplicate_evaluation_ids(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            skill = Path(directory) / "Eniac"
            (skill / "references").mkdir(parents=True)
            evals = skill / "evals"
            evals.mkdir()
            (skill / "SKILL.md").write_text(
                "\n".join(
                    (
                        "---",
                        "name: eniac",
                        'description: "Test Eniac skill."',
                        "---",
                        "",
                        "# Eniac",
                        "",
                    )
                ),
                encoding="utf-8",
            )
            scenario = {
                "id": "same-id",
                "kind": "technique",
                "prompt": "Apply a method.",
                "expected": ["observable result"],
                "anti_patterns": ["unsupported claim"],
            }
            (evals / "scenarios.json").write_text(
                json.dumps(
                    {"schema_version": 1, "scenarios": [scenario, scenario]}
                ),
                encoding="utf-8",
            )

            errors = validate_package(skill)

            self.assertTrue(any("is duplicated" in error for error in errors), errors)


if __name__ == "__main__":
    unittest.main()
