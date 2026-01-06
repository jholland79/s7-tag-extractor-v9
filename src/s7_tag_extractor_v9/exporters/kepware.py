"""Kepware CSV export."""

import csv
from typing import TextIO

from s7_tag_extractor_v9.models import Symbol

# Kepware Siemens driver column headers
KEPWARE_COLUMNS = [
    "Tag Name",
    "Address",
    "Data Type",
    "Respect Data Type",
    "Client Access",
    "Scan Rate",
    "Description",
]


def export_to_kepware(symbols: list[Symbol], output: TextIO) -> None:
    """Export symbols to Kepware CSV format.

    Args:
        symbols: List of Symbol objects to export.
        output: Text file object to write CSV data to.
    """
    writer = csv.writer(output)
    writer.writerow(KEPWARE_COLUMNS)
