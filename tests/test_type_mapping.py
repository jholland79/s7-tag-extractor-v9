"""Tests for S7 to PI type mapping."""

from s7_tag_extractor_v9.exporters.type_mapping import map_s7_type_to_pi


def test_map_bool_returns_int16_with_location2() -> None:
    """BOOL maps to Int16 PointType with Location2=2."""
    result = map_s7_type_to_pi("BOOL")

    assert result.point_type == "Int16"
    assert result.location2 == 2
