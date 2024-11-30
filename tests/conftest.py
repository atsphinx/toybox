"""Configuration for pytest."""

from pathlib import Path

import pytest

pytest_plugins = "sphinx.testing.fixtures"


@pytest.fixture(scope="session")
def rootdir() -> Path:  # noqa: D103
    return Path(__file__).parent.resolve()
