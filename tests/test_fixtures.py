"""Tests for Step 7 sample project fixtures.

These tests verify that the sample Step 7 project from snap7 repo
is available and contains the required DBF files for testing.
"""

from pathlib import Path


def test_sample_project_has_symlist_dbf() -> None:
    """Sample Step 7 project contains SYMLIST.DBF for symbol table testing."""
    fixtures_dir = Path(__file__).parent / "fixtures" / "sample_project"

    # Find any SYMLIST.DBF file in the sample project (may be in subdirectory)
    symlist_files = list(fixtures_dir.rglob("SYMLIST.DBF"))

    assert len(symlist_files) > 0, (
        f"Expected SYMLIST.DBF in {fixtures_dir}, but none found. "
        "Download sample project from: "
        "https://github.com/SCADACS/snap7/tree/master/examples/Step%207/Snap7"
    )
