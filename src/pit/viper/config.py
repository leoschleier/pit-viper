"""Load config from file."""
from pathlib import Path
from typing import Any

from pit.viper import _io

_config_path: Path | None = None
_config_name: str = ""
_config_type: str = ""
_config: dict[str, Any] = {}


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


def set_config_type(type_: str) -> None:
    """Set the config type.

    Supported config formats: json, toml, yaml, yml.

    Parameters
    ----------
    type_ : str
        Config format.
    """
    global _config_type  # noqa: PLW0603
    _config_type = type_.lower()


def get_conf(key: str, default: Any = None) -> Any:
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
    keys = key.split(".")
    value = _config

    for k in keys:
        if isinstance(value, dict):
            value = value.get(k, default)

    return value


def set_conf(key: str, value: Any) -> None:
    """Set a value in the config.

    Parameters
    ----------
    key : str
        Key to set the value for.
    value : Any
        Value to set.
    """
    keys = key.split(".")
    config = _config

    for k in keys[:-1]:
        if isinstance(config, dict):
            config = config.setdefault(k, {})

    config[keys[-1]] = value


def load_config() -> None:
    """Load the config from the config file.

    Raises
    ------
    FileNotFoundError
        Raised if the config path is not set or the path does not exist.
    """
    if not _config_path:
        msg = "Config path not set."
        raise FileNotFoundError(msg)

    config_file = (
        f"{_config_name}.{_config_type}" if _config_type else _config_name
    )
    config_path = _config_path / config_file

    config = _io.read_config(config_path)
    for key, value in config.items():
        _safe_set(key, value)


def _safe_set(key: str, value: Any) -> None:
    """Set a value in the config without overwriting nested defaults.

    Parameters
    ----------
    key : str
        Key to set the value for.
    value : Any
        Value to set.
    """
    if isinstance(value, dict):
        for k, v in value.items():  # pyright: ignore [reportUnknownVariableType]
            _safe_set(f"{key}.{k}", v)
    else:
        set_conf(key, value)


