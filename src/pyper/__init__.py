"""Pyper offers powerful configuration management capabilities.

This package currently provides one main function, `populate_env`,
which reads a `.env` file and sets the corresponding environment
variables in the current process. This can be useful for configuring
applications or scripts that rely on environment variables.

Usage:
    >>> from pyper import populate_env
    >>> populate_env()

For more information, see the documentation for the `populate_env`
function.
"""
from pyper.env import populate_env

__all__ = ["populate_env"]
