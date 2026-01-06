"""Data block parsing from BAUSTEIN.DBF files."""

import struct
from pathlib import Path

from s7_tag_extractor_v9.models import DataBlock
from s7_tag_extractor_v9.parser.dbf_constants import (
    DELETED_RECORD_MARKER,
    parse_dbf_header,
)

# Block number field position (after delete marker)
BLOCK_NUMBER_FIELD_START = 1
BLOCK_NUMBER_FIELD_SIZE = 2


def parse_blocks(baustein_path: Path) -> list[DataBlock]:
    """Parse data blocks from a BAUSTEIN.DBF file.

    Args:
        baustein_path: Path to the BAUSTEIN.DBF file

    Returns:
        List of DataBlock objects parsed from the DBF file
    """
    blocks = []

    with open(baustein_path, "rb") as f:
        dbf_header = parse_dbf_header(f)
        f.seek(dbf_header.header_length)

        for _ in range(dbf_header.num_records):
            record_data = f.read(dbf_header.record_length)
            if len(record_data) < dbf_header.record_length:
                break

            delete_marker = record_data[0]
            if delete_marker == DELETED_RECORD_MARKER:
                continue

            block_number_end = BLOCK_NUMBER_FIELD_START + BLOCK_NUMBER_FIELD_SIZE
            block_number_bytes = record_data[BLOCK_NUMBER_FIELD_START:block_number_end]
            block_number = struct.unpack("<H", block_number_bytes)[0]

            block = DataBlock(number=block_number, elements=[])
            blocks.append(block)

    return blocks
