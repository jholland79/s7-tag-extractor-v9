"""Command-line interface for s7-tag-extractor."""

from pathlib import Path

import click

from s7_tag_extractor_v9.exporters.pi_builder import export_to_pi_builder
from s7_tag_extractor_v9.parser.project import find_dbf_files
from s7_tag_extractor_v9.parser.symbols import parse_symbols

# Export format constants
FORMAT_PI_BUILDER = "pi-builder"


@click.group()
def cli() -> None:
    """S7 Tag Extractor CLI."""
    pass


@cli.command()
@click.argument("project", type=click.Path(exists=True))
@click.option(
    "--format", "export_format", default=FORMAT_PI_BUILDER, help="Export format"
)
@click.option("-o", "--output", required=True, help="Output file path")
def export(project: str, export_format: str, output: str) -> None:
    """Export symbols from a project."""
    project_path = Path(project)
    output_path = Path(output)

    # Find DBF files in the project
    dbf_files = find_dbf_files(project_path)

    # Parse symbols from all found files
    all_symbols = []
    for symlist_file in dbf_files.get("symlist", []):
        symbols = parse_symbols(symlist_file)
        all_symbols.extend(symbols)

    # Export based on format
    if export_format != FORMAT_PI_BUILDER:
        raise click.BadParameter(f"Unknown format: {export_format}")

    with open(output_path, "wb") as f:
        export_to_pi_builder(all_symbols, f)
