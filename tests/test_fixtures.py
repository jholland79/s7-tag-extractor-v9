"""Tests for Step 7 sample project fixtures.

These tests verify that the sample Step 7 project from snap7 repo
is available and contains the required DBF files for testing.
"""

from pathlib import Path

from s7_tag_extractor_v9 import __version__


def test_package_version_is_defined() -> None:
    """Package has a valid semantic version string."""
    assert __version__
    parts = __version__.split(".")
    assert len(parts) == 3, f"Expected semver format, got: {__version__}"


def test_sample_project_has_symlist_dbf(sample_project_path: Path) -> None:
    """Sample Step 7 project contains SYMLIST.DBF for symbol table testing."""
    # Find any SYMLIST.DBF file in the sample project (may be in subdirectory)
    symlist_files = list(sample_project_path.rglob("SYMLIST.DBF"))

    assert symlist_files, (
        f"Expected SYMLIST.DBF in {sample_project_path}, but none found. "
        "Download sample project from: "
        "https://github.com/SCADACS/snap7/tree/master/examples/Step%207/Snap7"
    )
