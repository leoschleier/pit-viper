"""Fixtures for the tests."""

import os

import pytest


@pytest.fixture(autouse=True)
def _prepare_env() -> None:  # pyright: ignore [reportUnusedFunction]
    """Prepare the environment for testing."""
    os.environ.pop("FOO", None)
    os.environ.pop("TEST_VAR", None)
