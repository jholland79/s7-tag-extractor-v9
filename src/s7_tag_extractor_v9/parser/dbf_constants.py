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


def _unpack_field(data: bytes, offset: int, fmt: str) -> int:
    """Unpack a single field from binary data at the given offset."""
    size = struct.calcsize(fmt)
    return struct.unpack(fmt, data[offset : offset + size])[0]


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

    num_records = _unpack_field(header, NUM_RECORDS_OFFSET, "<I")
    header_length = _unpack_field(header, HEADER_LENGTH_OFFSET, "<H")
    record_length = _unpack_field(header, RECORD_LENGTH_OFFSET, "<H")

    return DBFHeader(
        num_records=num_records,
        header_length=header_length,
        record_length=record_length,
    )


def iter_dbf_records(f: BinaryIO):
    """Iterate over non-deleted records in a DBF file.

    Args:
        f: Open file handle positioned at the start of the file

    Yields:
        bytes: Raw record data for each non-deleted record
    """
    dbf_header = parse_dbf_header(f)
    f.seek(dbf_header.header_length)

    for _ in range(dbf_header.num_records):
        record_data = f.read(dbf_header.record_length)
        if len(record_data) < dbf_header.record_length:
            break

        delete_marker = record_data[0]
        if delete_marker == DELETED_RECORD_MARKER:
            continue

        yield record_data
