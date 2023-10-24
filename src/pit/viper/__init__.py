"""Pit-viper offers configuration management capabilities.

This package currently provides one main function, `auto_env`,
which reads a `.env` file and sets the corresponding environment
variables in the current process. This can be useful for configuring
applications or scripts that rely on environment variables.

Usage:
    >>> from pit import viper
    >>> viper.auto_env()

For more information, see the documentation for the `auto_env`
function.
"""
from pit.viper.env import auto_env

__all__ = ["auto_env"]
