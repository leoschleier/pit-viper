"""Pit-viper offers configuration management capabilities.

This package supports accessing parameters from environment variables,
and configuration files.

Usage:
    >>> from pit import viper
    >>> from pathlib import Path
    >>>
    >>> viper.auto_env()
    >>>
    >>> viper.set_config_path(Path() / "config")
    >>> viper.set_config_name("my_config")
    >>> viper.set_config_type("toml")
    >>> viper.set("foo", "default-value")
    >>>
    >>> viper.load_config()
    >>> foo = viper.get("foo")

For more information, see the https://github.com/leoschleier/pit-viper.
"""
from pit.viper.config import get_conf as get
from pit.viper.config import (
    load_config,
    set_config_name,
    set_config_path,
    set_config_type,
)
from pit.viper.config import set_conf as set  # noqa: A001
from pit.viper.env import auto_env

__all__ = [
    "auto_env",
    "get",
    "load_config",
    "set",
    "set_config_name",
    "set_config_path",
    "set_config_type",
]
