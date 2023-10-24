"""Test the env module."""
import os
from pathlib import Path

import py
import pytest
from pit.viper import env

_TEST_DOTENV_PATH = Path(__file__).parent / "data" / ".env"


@pytest.fixture(autouse=True)
def _prepare_env() -> None:
    """Prepare the environment for testing."""
    os.environ.pop("FOO", None)
    os.environ.pop("TEST_VAR", None)


def test_auto_env_without_overwrite() -> None:
    """Test the `auto_env` function without overwrite.

    We expect that the value of the already existing environment
    variable `FOO` is not being overwritten with the value from the
    .env file.
    """
    os.environ["FOO"] = "already-set"

    e = env.auto_env(path=_TEST_DOTENV_PATH)

    assert e["FOO"] == "already-set"
    assert e["TEST_VAR"] == "test_value"


def test_auto_env_with_overwrite() -> None:
    """Test the `auto_env` function with overwrite.

    We expect that the value of the already existing environment
    variable `FOO` is being overwritten with the value from the .env
    file.
    """
    os.environ["FOO"] = "already-set"

    e = env.auto_env(path=_TEST_DOTENV_PATH, overwrite=True)

    assert e["FOO"] == "bar"
    assert e["TEST_VAR"] == "test_value"


def test_auto_env_with_non_existing_path(tmpdir: py.path.local) -> None:
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
    e = env.auto_env(path=non_existent_path)

    assert e
    assert isinstance(e, dict)
    assert not e.get("FOO")
    assert not e.get("TEST_VAR")
