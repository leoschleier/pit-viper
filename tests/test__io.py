"""Test the _io module."""
from pathlib import Path
from typing import Final

import pytest
from pit.viper import _io

CONFIG_DIR: Final = Path(__file__).parent / "data" / "config"
CONFIG_JSON: Final = CONFIG_DIR / "config.json"
CONFIG_TOML: Final = CONFIG_DIR / "config.toml"
CONFIG_YAML: Final = CONFIG_DIR / "config.yaml"

EX_CONFIG = {
    "foo": "config-bar",
    "test": {
        "nested": {
            "a": 0,
            "b": 1.1,
            "c": True,
            "d": "test-string",
        },
    },
}


@pytest.mark.parametrize(
    "config_path",
    [CONFIG_JSON, CONFIG_TOML, CONFIG_YAML],
)
def test_read_config(config_path: Path) -> None:
    """Test reading a config file.

    Parameters
    ----------
    config_path : Path
        Path to the config file.
    """
    config = _io.read_config(config_path)
    assert config == EX_CONFIG
