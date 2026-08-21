from __future__ import annotations

import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL_ROOT / "scripts"))

from finalize_plan import finalize  # noqa: E402


def run_finalize(plan: Path, retain: bool, workspace: Path, owner: str) -> int:
    with redirect_stdout(StringIO()), redirect_stderr(StringIO()):
        return finalize(plan, retain, workspace, owner)


def write_plan(
    root: Path,
    *,
    name: str = ".eniac-plan.md",
    status: str = "done",
    owner: str = "test-owner",
    retention: str = "delete-on-complete",
) -> Path:
    plan = root / name
    plan.write_text(
        "\n".join(
            (
                "# Test Plan",
                "",
                f"> Status: {status}",
                f"> Owner: {owner}",
                f"> Retention: {retention}",
                "",
            )
        ),
        encoding="utf-8",
    )
    return plan


class FinalizePlanTests(unittest.TestCase):
    def test_deletes_completed_owned_plan(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            plan = write_plan(root)

            result = run_finalize(plan, False, root, "test-owner")

            self.assertEqual(result, 0)
            self.assertFalse(plan.exists())

    def test_is_idempotent_when_plan_is_already_absent(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            plan = root / ".eniac-plan-2.md"

            result = run_finalize(plan, False, root, "test-owner")

            self.assertEqual(result, 0)

    def test_rejects_active_plan(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            plan = write_plan(root, status="active")

            result = run_finalize(plan, False, root, "test-owner")

            self.assertEqual(result, 1)
            self.assertTrue(plan.exists())

    def test_rejects_owner_mismatch(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            plan = write_plan(root)

            result = run_finalize(plan, False, root, "different-owner")

            self.assertEqual(result, 1)
            self.assertTrue(plan.exists())

    def test_retains_only_explicit_retention_plan(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            plan = write_plan(root, retention="retain-by-explicit-request")

            result = run_finalize(plan, True, root, "test-owner")

            self.assertEqual(result, 0)
            self.assertTrue(plan.exists())

    def test_rejects_retention_flag_without_plan_opt_in(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            plan = write_plan(root)

            result = run_finalize(plan, True, root, "test-owner")

            self.assertEqual(result, 1)
            self.assertTrue(plan.exists())

    def test_rejects_plan_outside_workspace(self) -> None:
        with tempfile.TemporaryDirectory() as workspace_directory:
            with tempfile.TemporaryDirectory() as outside_directory:
                workspace = Path(workspace_directory)
                plan = write_plan(Path(outside_directory))

                result = run_finalize(plan, False, workspace, "test-owner")

                self.assertEqual(result, 1)
                self.assertTrue(plan.exists())

    def test_rejects_non_eniac_filename(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            plan = write_plan(root, name="task-plan.md")

            result = run_finalize(plan, False, root, "test-owner")

            self.assertEqual(result, 1)
            self.assertTrue(plan.exists())


if __name__ == "__main__":
    unittest.main()
