"""Test the env module."""
import os
from pathlib import Path

import py  # pyright: ignore [reportMissingTypeStubs]
from pit import viper

from tests import config


def test_auto_env_without_overwrite() -> None:
    """Test the `auto_env` function without overwrite.

    We expect that the value of the already existing environment
    variable `FOO` is not being overwritten with the value from the
    .env file.
    """
    os.environ["FOO"] = "already-set"

    e = viper.auto_env(path=config.TEST_DOTENV_PATH)

    assert e["FOO"] == "already-set"
    assert e["TEST_VAR"] == "test_value"


def test_auto_env_with_overwrite() -> None:
    """Test the `auto_env` function with overwrite.

    We expect that the value of the already existing environment
    variable `FOO` is being overwritten with the value from the .env
    file.
    """
    os.environ["FOO"] = "already-set"

    e = viper.auto_env(path=config.TEST_DOTENV_PATH, overwrite=True)

    assert e["FOO"] == "bar"
    assert e["TEST_VAR"] == "test_value"


def test_auto_env_with_non_existing_path(tmpdir: py.path.LocalPath) -> None:
    """Test the `auto_env` function with a non-existing path.

    We expect that the function still returns a dictionary of
    environment variables. Consequently, the dictionary must be non-
    empty. Moreover, the dictionary must not contain the variables
    provided in the test .env file.

    Note that the `auto_env` function is supposed to not raise an error
    even though the path a wrong file extension is being used.
    """
    # Use a temporary directory to ensure that the path does not exist.
    non_existent_path = Path(tmpdir) / ".wrong"
    e = viper.auto_env(path=non_existent_path)

    assert e
    assert isinstance(e, dict)
    assert not e.get("FOO")
    assert not e.get("TEST_VAR")
