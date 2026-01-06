"""Tests for data block parsing from BAUSTEIN.DBF."""

from pathlib import Path

from s7_tag_extractor_v9.parser.blocks import parse_blocks

from s7_tag_extractor_v9.models import DataBlock


def test_parse_blocks_extracts_data_block_with_number_and_elements(
    sample_project_path: Path,
) -> None:
    """parse_blocks returns DataBlock objects with block number and elements."""
    baustein_path = sample_project_path / "BAUSTEIN.DBF"

    result = parse_blocks(baustein_path)

    assert isinstance(result, list)
    assert len(result) > 0
    block = result[0]
    assert isinstance(block, DataBlock)
    assert block.number > 0
    assert isinstance(block.elements, list)
