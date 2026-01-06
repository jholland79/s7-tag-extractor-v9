"""Array detection and expansion for S7 data blocks."""


def expand_array(
    name: str,
    element_type: str,
    start_index: int,
    end_index: int,
    base_address: int,
) -> list:
    """Expand an array declaration into individual element tags.

    Args:
        name: Base name of the array
        element_type: Data type of each element (e.g., INT, REAL)
        start_index: Starting array index
        end_index: Ending array index
        base_address: Byte offset where the array starts

    Returns:
        List of expanded element tags
    """
    raise NotImplementedError()
