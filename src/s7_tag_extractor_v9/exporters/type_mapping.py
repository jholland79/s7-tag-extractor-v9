"""S7 to PI type mapping."""

from dataclasses import dataclass


@dataclass
class MappedType:
    """Mapped type with point_type and location2."""

    point_type: str
    location2: int


def map_s7_type_to_pi(s7_type: str) -> MappedType:
    """Map S7 type to PI type.

    Args:
        s7_type: The S7 data type name.

    Returns:
        MappedType with point_type and location2.
    """
    if s7_type == "BOOL":
        return MappedType(point_type="Int16", location2=2)

    raise ValueError(f"Unknown S7 type: {s7_type}")
