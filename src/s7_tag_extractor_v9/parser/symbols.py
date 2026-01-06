"""Symbol table parsing from SYMLIST.DBF files."""

import struct
from pathlib import Path

from s7_tag_extractor_v9.models import Symbol

# DBF header structure offsets
DBF_HEADER_SIZE = 32
NUM_RECORDS_OFFSET = 4
HEADER_LENGTH_OFFSET = 8
RECORD_LENGTH_OFFSET = 10

# DBF record field positions and widths
NAME_FIELD_START = 1
NAME_FIELD_WIDTH = 20
ADDRESS_FIELD_START = 21
ADDRESS_FIELD_WIDTH = 20

# Delete marker
DELETED_RECORD_MARKER = ord("*")


def _extract_field(record_data: bytes, start: int, width: int) -> str:
    """Extract and decode a fixed-width field from a DBF record."""
    field_bytes = record_data[start : start + width]
    return field_bytes.decode("ascii", errors="ignore").strip()


def parse_symbols(symlist_path: Path) -> list[Symbol]:
    """Parse symbols from a SYMLIST.DBF file.

    Args:
        symlist_path: Path to the SYMLIST.DBF file

    Returns:
        List of Symbol objects parsed from the DBF file
    """
    symbols = []

    with open(symlist_path, "rb") as f:
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

            name = _extract_field(record_data, NAME_FIELD_START, NAME_FIELD_WIDTH)
            address = _extract_field(
                record_data, ADDRESS_FIELD_START, ADDRESS_FIELD_WIDTH
            )

            if name and address:
                symbol = Symbol(name=name, address=address, data_type="", comment=None)
                symbols.append(symbol)

    return symbols
