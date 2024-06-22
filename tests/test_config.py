"""Test the config module."""

from pit import viper

from tests import config

CONFIG_NAME = "config"
CONFIG_TYPE = "toml"

EX_CONFIG = {
    "foo": "config-bar",
    "test.nested.a": 0,
    "test.nested.b": 1.1,
    "test.nested.c": True,
    "test.nested.d": "test-string",
}


def test_load_config() -> None:
    """Test loading a config file."""
    viper.set_config_path(config.TEST_CONFIG_DIR)
    viper.set_config_name(CONFIG_NAME)
    viper.set_config_type(CONFIG_TYPE)
    viper.load_config()

    for key, value in EX_CONFIG.items():
        assert viper.get(key) == value


def test_load_config_with_defaults() -> None:
    """Test loading a config file with defaults."""
    viper.set_config_path(config.TEST_CONFIG_DIR)
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


def test_config_env_hierarchy() -> None:
    """Test the hierarchy of config and environment variables."""
    viper.set_config_path(config.TEST_CONFIG_DIR)
    viper.set_config_name(CONFIG_NAME)
    viper.set_config_type(CONFIG_TYPE)

    viper.set("foo", "default bar")

    viper.auto_env(path=config.TEST_DOTENV_PATH, overwrite=True)
    viper.load_config()

    # Environment variables should overwrite config variables.
    # Therefore, we expect the value of `foo` to be `env-bar` which is
    # the value specified in the .env file.
    assert viper.get("foo") == "env-bar"


def test_env_prefix() -> None:
    """Test setting an environment variable prefix."""
    viper.set_env_prefix("test")
    viper.auto_env(path=config.TEST_DOTENV_PATH, overwrite=True)

    assert viper.get("foo") == "env-test-bar"
