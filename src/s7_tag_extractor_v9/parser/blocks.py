"""Data block parsing from BAUSTEIN.DBF files."""

import struct
from pathlib import Path

from s7_tag_extractor_v9.models import DataBlock

# DBF header structure offsets
DBF_HEADER_SIZE = 32
NUM_RECORDS_OFFSET = 4
HEADER_LENGTH_OFFSET = 8
RECORD_LENGTH_OFFSET = 10

# Delete marker
DELETED_RECORD_MARKER = ord("*")


def parse_blocks(baustein_path: Path) -> list[DataBlock]:
    """Parse data blocks from a BAUSTEIN.DBF file.

    Args:
        baustein_path: Path to the BAUSTEIN.DBF file

    Returns:
        List of DataBlock objects parsed from the DBF file
    """
    blocks = []

    with open(baustein_path, "rb") as f:
        header = f.read(DBF_HEADER_SIZE)

        num_records_slice = header[NUM_RECORDS_OFFSET : NUM_RECORDS_OFFSET + 4]
        num_records = struct.unpack("<I", num_records_slice)[0]

        header_len_slice = header[HEADER_LENGTH_OFFSET : HEADER_LENGTH_OFFSET + 2]
        header_length = struct.unpack("<H", header_len_slice)[0]

        record_len_slice = header[RECORD_LENGTH_OFFSET : RECORD_LENGTH_OFFSET + 2]
        record_length = struct.unpack("<H", record_len_slice)[0]

        f.seek(header_length)

        for _ in range(num_records):
            record_data = f.read(record_length)
            if len(record_data) < record_length:
                break

            delete_marker = record_data[0]
            if delete_marker == DELETED_RECORD_MARKER:
                continue

            # Extract block number from first field (2 bytes, little-endian)
            block_number = struct.unpack("<H", record_data[1:3])[0]

            block = DataBlock(number=block_number, elements=[])
            blocks.append(block)

    return blocks
