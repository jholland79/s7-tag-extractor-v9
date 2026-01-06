"""Data models for S7 tag extraction."""

from dataclasses import dataclass


@dataclass
class Symbol:
    """Symbol dataclass with name, address, and data type."""

    name: str
    address: str
    data_type: str
    comment: str | None = None


@dataclass
class DataBlock:
    """DataBlock dataclass with block number and elements."""

    number: int
    elements: list
