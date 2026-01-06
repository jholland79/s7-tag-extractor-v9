"""Tests for PI Builder Excel export."""

from io import BytesIO

from openpyxl import load_workbook
from s7_tag_extractor_v9.exporters.pi_builder import export_to_pi_builder

from s7_tag_extractor_v9.models import Symbol

PI_BUILDER_COLUMNS = [
    "Tag",
    "PointType",
    "PointSource",
    "Descriptor",
    "InstrumentTag",
    "Location2",
]


def test_export_creates_excel_with_pi_builder_columns() -> None:
    """Export creates Excel with correct PI Builder columns."""
    symbols = [
        Symbol(
            name="Motor1_Run",
            address="DB100.DBX4.0",
            data_type="BOOL",
            comment="Motor 1 Running",
        ),
    ]

    output = BytesIO()
    export_to_pi_builder(symbols, output)

    output.seek(0)
    workbook = load_workbook(output)
    sheet = workbook.active

    header_row = [cell.value for cell in sheet[1]]

    assert header_row == PI_BUILDER_COLUMNS
