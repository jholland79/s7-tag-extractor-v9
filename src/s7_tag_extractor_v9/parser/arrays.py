"""Array detection and expansion for S7 data blocks."""

from s7_tag_extractor_v9.models import Symbol

# Data type sizes in bytes
TYPE_SIZES = {
    "INT": 2,
    "REAL": 4,
}


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
    element_size = TYPE_SIZES[element_type]
    elements = []

    for i in range(start_index, end_index + 1):
        element_address = base_address + (i - start_index) * element_size
        element = Symbol(
            name=f"{name}[{i}]",
            address=element_address,
            data_type=element_type,
        )
        elements.append(element)

    return elements
