"""DBF file format constants and utilities shared across parsers."""

import struct
from dataclasses import dataclass
from typing import BinaryIO

# DBF header structure offsets
DBF_HEADER_SIZE = 32
NUM_RECORDS_OFFSET = 4
HEADER_LENGTH_OFFSET = 8
RECORD_LENGTH_OFFSET = 10

# Delete marker
DELETED_RECORD_MARKER = ord("*")


@dataclass
class DBFHeader:
    """Parsed DBF file header information."""

    num_records: int
    header_length: int
    record_length: int


def parse_dbf_header(f: BinaryIO) -> DBFHeader:
    """Parse the header of a DBF file.

    Args:
        f: Open file handle positioned at the start of the file

    Returns:
        DBFHeader with parsed values
    """
    header = f.read(DBF_HEADER_SIZE)

    num_records_slice = header[NUM_RECORDS_OFFSET : NUM_RECORDS_OFFSET + 4]
    num_records = struct.unpack("<I", num_records_slice)[0]

    header_len_slice = header[HEADER_LENGTH_OFFSET : HEADER_LENGTH_OFFSET + 2]
    header_length = struct.unpack("<H", header_len_slice)[0]

    record_len_slice = header[RECORD_LENGTH_OFFSET : RECORD_LENGTH_OFFSET + 2]
    record_length = struct.unpack("<H", record_len_slice)[0]

    return DBFHeader(
        num_records=num_records,
        header_length=header_length,
        record_length=record_length,
    )
