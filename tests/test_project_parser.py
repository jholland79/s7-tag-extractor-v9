"""Tests for project structure navigation."""

from pathlib import Path

from s7_tag_extractor_v9.parser.project import find_dbf_files


def test_find_dbf_files_locates_symlist_in_project() -> None:
    """Given a project path, find_dbf_files returns paths to SYMLIST.DBF files."""
    fixtures_dir = Path(__file__).parent / "fixtures" / "sample_project"

    result = find_dbf_files(fixtures_dir)

    assert "symlist" in result
    assert len(result["symlist"]) > 0
    assert all(p.name == "SYMLIST.DBF" for p in result["symlist"])
