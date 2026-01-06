"""PI Builder Excel export."""

from typing import BinaryIO

from openpyxl import Workbook

from s7_tag_extractor_v9.models import Symbol


def export_to_pi_builder(symbols: list[Symbol], output: BinaryIO) -> None:
    """Export symbols to PI Builder Excel format.

    Args:
        symbols: List of Symbol objects to export.
        output: Binary file object to write Excel data to.
    """
    workbook = Workbook()
    sheet = workbook.active

    # Write header row
    headers = [
        "Tag",
        "PointType",
        "PointSource",
        "Descriptor",
        "InstrumentTag",
        "Location2",
    ]
    sheet.append(headers)

    # Save to output
    workbook.save(output)
