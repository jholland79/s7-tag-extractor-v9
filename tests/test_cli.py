"""Tests for CLI interface."""

from pathlib import Path

from click.testing import CliRunner
from s7_tag_extractor_v9.cli import cli


def test_export_command_creates_excel_file(
    sample_project_path: Path, tmp_path: Path
) -> None:
    """Export command creates Excel file with pi-builder format."""
    output_file = tmp_path / "output.xlsx"

    runner = CliRunner()
    result = runner.invoke(
        cli,
        [
            "export",
            str(sample_project_path),
            "--format",
            "pi-builder",
            "-o",
            str(output_file),
        ],
    )

    assert result.exit_code == 0
    assert output_file.exists()
