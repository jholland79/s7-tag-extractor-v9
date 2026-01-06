"""Tests for Kepware CSV export."""

import csv
from io import StringIO

from s7_tag_extractor_v9.exporters.kepware import KEPWARE_COLUMNS, export_to_kepware
from s7_tag_extractor_v9.models import Symbol


def test_export_creates_csv_with_kepware_columns() -> None:
    """Export creates CSV with correct Kepware Siemens driver columns."""
    symbols = [
        Symbol(
            name="Motor1_Run",
            address="DB100.DBX4.0",
            data_type="BOOL",
            comment="Motor 1 Running",
        ),
    ]

    output = StringIO()
    export_to_kepware(symbols, output)

    output.seek(0)
    reader = csv.reader(output)
    header_row = next(reader)

    assert header_row == KEPWARE_COLUMNS
