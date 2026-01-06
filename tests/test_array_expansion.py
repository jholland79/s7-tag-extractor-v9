"""Tests for array detection and expansion."""

from s7_tag_extractor_v9.parser.arrays import expand_array


def test_expand_array_int_array_0_to_9_returns_10_tags_with_correct_addresses() -> None:
    """expand_array for Array[0..9] of INT returns 10 individual tags."""
    array_name = "Temperatures"
    array_type = "INT"
    start_index = 0
    end_index = 9
    base_address = 0  # Starting byte offset in the data block

    result = expand_array(
        name=array_name,
        element_type=array_type,
        start_index=start_index,
        end_index=end_index,
        base_address=base_address,
    )

    assert len(result) == 10
    assert result[0].name == "Temperatures[0]"
    assert result[0].address == 0
    assert result[0].data_type == "INT"
    assert result[9].name == "Temperatures[9]"
    assert result[9].address == 18  # INT is 2 bytes, so index 9 is at offset 18
