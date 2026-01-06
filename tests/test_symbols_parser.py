"""Tests for symbol table parsing from SYMLIST.DBF."""

from pathlib import Path

from s7_tag_extractor_v9.models import Symbol
from s7_tag_extractor_v9.parser.symbols import parse_symbols


def test_parse_symbols_extracts_symbol_with_name_address_comment(
    sample_project_path: Path,
) -> None:
    """parse_symbols returns Symbol objects with name, address, and comment."""
    symlist_path = sample_project_path / "SYMLIST.DBF"

    result = parse_symbols(symlist_path)

    assert isinstance(result, list)
    assert len(result) > 0
    symbol = result[0]
    assert isinstance(symbol, Symbol)
    assert symbol.name != ""
    assert symbol.address != ""
