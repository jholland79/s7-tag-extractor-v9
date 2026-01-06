"""Symbol table parsing from SYMLIST.DBF files."""

from pathlib import Path

from s7_tag_extractor_v9.models import Symbol
from s7_tag_extractor_v9.parser.dbf_constants import iter_dbf_records

# DBF record field positions and widths
NAME_FIELD_START = 1
NAME_FIELD_WIDTH = 20
ADDRESS_FIELD_START = 21
ADDRESS_FIELD_WIDTH = 20


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
        for record_data in iter_dbf_records(f):
            name = _extract_field(record_data, NAME_FIELD_START, NAME_FIELD_WIDTH)
            address = _extract_field(
                record_data, ADDRESS_FIELD_START, ADDRESS_FIELD_WIDTH
            )

            if name and address:
                symbol = Symbol(name=name, address=address, data_type="", comment=None)
                symbols.append(symbol)

    return symbols
