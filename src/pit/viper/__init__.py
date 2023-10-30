"""Pit-viper offers configuration management capabilities.

This package currently provides one main function, `auto_env`,
which reads a `.env` file and sets the corresponding environment
variables in the current process. This can be useful for configuring
applications or scripts that rely on environment variables.

Usage:
    >>> from pit import viper
    >>> from pathlib import Path
    >>>
    >>> viper.auto_env()
    >>> viper.set_config_path(Path() / "config")
    >>> viper.set_config_name("my_config.toml")
    >>> viper.load_config()
    >>> foo = viper.get("foo")

For more information, see the documentation for the `auto_env`
function.
"""
from pit.viper.config import getconf as get
from pit.viper.config import load_config, set_config_name, set_config_path
from pit.viper.config import setconf as set  # noqa: A001
from pit.viper.env import auto_env

__all__ = [
    "auto_env",
    "get",
    "load_config",
    "set",
    "set_config_name",
    "set_config_path",
]
