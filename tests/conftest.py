"""Shared pytest fixtures for all tests."""

from pathlib import Path

import pytest


@pytest.fixture
def sample_project_path() -> Path:
    """Path to the sample Step 7 project fixture."""
    return Path(__file__).parent / "fixtures" / "sample_project"
