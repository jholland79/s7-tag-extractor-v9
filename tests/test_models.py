"""Tests for data models (Tag, Symbol, DataBlock)."""

from s7_tag_extractor_v9.models import Symbol


def test_symbol_creation_with_required_fields() -> None:
    """Symbol dataclass can be created with name, address, and data type."""
    symbol = Symbol(
        name="Motor_Run",
        address="M0.0",
        data_type="BOOL",
    )

    assert symbol.name == "Motor_Run"
    assert symbol.address == "M0.0"
    assert symbol.data_type == "BOOL"
    assert symbol.comment is None  # Optional field defaults to None
