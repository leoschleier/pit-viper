"""Fixtures for the tests."""

import os

import pytest
from pit import viper

# pyright: reportGeneralTypeIssues=false, reportUnknownMemberType=false


@pytest.fixture(autouse=True)
def _prepare_env() -> None:  # pyright: ignore [reportUnusedFunction]
    """Prepare the environment for testing."""
    os.environ.pop("FOO", None)
    os.environ.pop("TEST_FOO", None)
    os.environ.pop("TEST_VAR", None)


@pytest.fixture(autouse=True)
def _reset_viper() -> None:  # pyright: ignore [reportUnusedFunction]
    """Reset viper's state."""
    viper._config._config_path = None
    viper._config._config_name = ""
    viper._config._config_type = ""
    viper._config._config = {}

    viper._env._env_prefix = ""
    viper._env._env_enabled = False
    viper._env._oldnew = {}
