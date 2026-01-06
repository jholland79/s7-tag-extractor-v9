"""Symbol table parsing from SYMLIST.DBF files."""

import struct
from pathlib import Path

from s7_tag_extractor_v9.models import Symbol


def parse_symbols(symlist_path: Path) -> list[Symbol]:
    """Parse symbols from a SYMLIST.DBF file.

    Args:
        symlist_path: Path to the SYMLIST.DBF file

    Returns:
        List of Symbol objects parsed from the DBF file
    """
    symbols = []

    with open(symlist_path, "rb") as f:
        # Read DBF header (32 bytes)
        header = f.read(32)

        # Get number of records (bytes 4-7, little-endian)
        num_records = struct.unpack("<I", header[4:8])[0]

        # Get header length (bytes 8-9, little-endian)
        header_length = struct.unpack("<H", header[8:10])[0]

        # Get record length (bytes 10-11, little-endian)
        record_length = struct.unpack("<H", header[10:12])[0]

        # Skip to data area (already read 32 bytes of header, need to read rest)
        f.seek(header_length)

        # Read each record
        for _ in range(num_records):
            record_data = f.read(record_length)
            if len(record_data) < record_length:
                break

            # First byte is delete marker (0x20 = not deleted)
            delete_marker = record_data[0]
            if delete_marker == ord("*"):  # Deleted record
                continue

            # Extract NAME field (second field, 20 chars)
            name = record_data[1:21].decode("ascii", errors="ignore").strip()

            # Extract ADDRESS field (third field, 20 chars)
            address = record_data[21:41].decode("ascii", errors="ignore").strip()

            if name and address:
                symbol = Symbol(name=name, address=address, data_type="", comment=None)
                symbols.append(symbol)

    return symbols
