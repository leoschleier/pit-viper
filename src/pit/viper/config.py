"""Load config from file."""
from pathlib import Path
from typing import Any

from pit.viper import _io

_config_path: Path | None = None
_config_name: str | None = None
_config: dict[str, Any] = {}


class ConfigError(Exception):
    """Raised when the is not loaded or its path has not been set."""


def set_config_name(name: str) -> None:
    """Set the config name.

    Parameters
    ----------
    name : str
        Name of the config file.
    """
    global _config_name  # noqa: PLW0603
    _config_name = name


def set_config_path(path: Path) -> None:
    """Set the config path.

    Parameters
    ----------
    path : Path
        Path to the config file or the directory containing the config
        file.
    """
    global _config_path  # noqa: PLW0603
    _config_path = path


def getconf(key: str, default: Any = None) -> Any:
    """Get a value from the config.

    Parameters
    ----------
    key : str
        Key to get the value for.
    default : Any, optional
        Default value to return if the key is not found, by default None

    Returns
    -------
    Any
        Value for the key.
    """
    if key not in _config:
        return default

    return _config[key]


def setconf(key: str, value: Any) -> None:
    """Set a value in the config.

    Parameters
    ----------
    key : str
        Key to set the value for.
    value : Any
        Value to set.
    """
    _config[key] = value


def load_config() -> dict[str, Any]:
    """Load the config from the config file.

    Returns
    -------
    dict[str, Any]
        Config.

    Raises
    ------
    ValueError
        Raised if the config path is not set.
    """
    if not _config_path:
        msg = "Config path not set."
        raise ConfigError(msg)

    config_path = _config_path

    if _config_name:
        config_path = config_path / _config_name

    if not config_path.exists():
        msg = f"Path {config_path.resolve()} does not exist."
        raise FileNotFoundError(msg)

    global _config  # noqa: PLW0603
    _config |= _io.read_config(config_path)
