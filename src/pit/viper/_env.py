"""Load environment variables from a `.env` file."""
import os
from pathlib import Path
from typing import Any

_EQUALS = "="
_NEW_LINE = "\n"
_ENCLOSING_CHARS = f" \"'{_NEW_LINE}"

_env_prefix = ""
_env_enabled = False
_oldnew: dict[str, str] = {}


class UnsupportedFileFormatError(Exception):
    """Raised when the file format is not supported."""

    def __init__(self: "UnsupportedFileFormatError", path: Path) -> None:
        """Initialize the exception."""
        super().__init__(f"Unsupported file format: {path.suffix}")


def auto_env(
    *,
    path: Path | None = None,
    overwrite: bool = False,
) -> dict[str, str]:
    """Populate environment variables with variables from a `.env` file.

    The `.env` file is being read as text using the UTF-8 character
    encoding.

    Parameters
    ----------
    path : Path | None, optional
        Path to the `.env` file. If not set, `pit-viper` will try to
        find the file in the current working directory, by default None
    overwrite : bool, optional
        Whether or not to overwrite existing environment variables with
        the variables from the `.env` file, by default False

    Returns
    -------
    dict[str, str]
        Environment variables after populating.

    Raises
    ------
    UnsupportedFileFormatError
        Raised if the file format is not supported, i.e., if the
        specified path does not lead to a `.env` file.
    """
    if path is None:
        path = Path(".env")
    if path.exists():
        if ".env" in [path.name, path.suffix]:
            _populate_env(path=path, overwrite=overwrite)
        else:
            raise UnsupportedFileFormatError(path=path)

    global _env_enabled  # noqa: PLW0603
    _env_enabled = True

    return dict(os.environ)


def is_env_enabled() -> bool:
    """Check if environment variables are enabled.

    Environment variables are enabled if the `auto_env` function has
    been called.
    """
    return _env_enabled


def set_env_prefix(prefix: str) -> None:
    """Set a prefix for environment variables.

    The prefix will be added to the key used for accessing environment
    variables.

    Parameters
    ----------
    prefix : str
        Prefix to add to environment variables.
    """
    global _env_prefix  # noqa: PLW0603
    _env_prefix = prefix.upper()


def get_env_prefix() -> str:
    """Get the prefix for environment variables."""
    return f"{_env_prefix}_" if _env_prefix else ""


def set_env_key_replacer(oldnew: dict[str, str]) -> None:
    """Set replacer to replace keys and substrings of keys.

    Replacements are being performed when retrieving environment
    variables.

    Parameters
    ----------
    oldnew : dict[str, str]
       Maps keys and substrings of keys used to retrieve environment
       variables to new keys and substrings.
    """
    global _oldnew  # noqa: PLW0603w
    _oldnew = oldnew


def get_env(key: str) -> Any:
    """Get an environment variable by key."""
    if is_env_enabled():
        for old, new in _oldnew.items():
            key = key.replace(old, new)
        env_key = f"{get_env_prefix()}{key.upper()}"
        return os.environ.get(env_key)

    return None


def _populate_env(*, path: Path, overwrite: bool = False) -> None:
    """Populate environment variables."""
    with path.open(encoding="utf-8") as stream:
        for line in stream:
            if line == _NEW_LINE:
                continue

            k, v = line.split(_EQUALS)

            # Strip any combination of enclosing characters.
            k = k.strip(_ENCLOSING_CHARS)
            v = v.strip(_ENCLOSING_CHARS)

            _set_variable(key=k, value=v, overwrite=overwrite)


def _set_variable(key: str, value: str, *, overwrite: bool = False) -> None:
    """Set an environment variable."""
    if overwrite:
        os.environ[key] = value
    else:
        os.environ.setdefault(key, value)
