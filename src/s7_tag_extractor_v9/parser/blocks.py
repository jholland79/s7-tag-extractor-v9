"""Data block parsing from BAUSTEIN.DBF files."""

from pathlib import Path

from s7_tag_extractor_v9.models import DataBlock
from s7_tag_extractor_v9.parser.dbf_constants import _unpack_field, iter_dbf_records

# Block number field position (after delete marker)
BLOCK_NUMBER_FIELD_START = 1


def parse_blocks(baustein_path: Path) -> list[DataBlock]:
    """Parse data blocks from a BAUSTEIN.DBF file.

    Args:
        baustein_path: Path to the BAUSTEIN.DBF file

    Returns:
        List of DataBlock objects parsed from the DBF file
    """
    blocks = []

    with open(baustein_path, "rb") as f:
        for record_data in iter_dbf_records(f):
            block_number = _unpack_field(record_data, BLOCK_NUMBER_FIELD_START, "<H")

            block = DataBlock(number=block_number, elements=[])
            blocks.append(block)

    return blocks
