"""Test the config module."""
from pathlib import Path

from pit import viper

CONFIG_DIR = Path(__file__).parent / "data" / "config"
CONFIG_NAME = "config"
CONFIG_TYPE = "toml"

EX_CONFIG = {
    "foo": "bar",
    "test.nested.a": 0,
    "test.nested.b": 1.1,
    "test.nested.c": True,
    "test.nested.d": "test-string",
}


def test_load_config() -> None:
    """Test loading a config file."""
    viper.set_config_path(CONFIG_DIR)
    viper.set_config_name(CONFIG_NAME)
    viper.set_config_type(CONFIG_TYPE)
    viper.load_config()

    for key, value in EX_CONFIG.items():
        assert viper.get(key) == value


def test_load_config_with_defaults() -> None:
    """Test loading a config file with defaults."""
    viper.set_config_path(CONFIG_DIR)
    viper.set_config_name(CONFIG_NAME)
    viper.set_config_type(CONFIG_TYPE)

    # Parameters set before loading the config only serve as defaults
    # and can be overwritten on load.
    viper.set("foo", "default bar")
    viper.set("test.nested.e", "default-string")

    viper.load_config()

    # Parameters set after loading the config will overwrite the
    # respective values.
    viper.set("test.nested.d", "overwritten-string")

    for key, value in EX_CONFIG.items():
        if key != "test.nested.d":
            assert viper.get(key) == value

    assert viper.get("test.nested.d") == "overwritten-string"
    assert viper.get("test.nested.e") == "default-string"
