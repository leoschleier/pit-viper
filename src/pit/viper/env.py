"""Load environment variables from a `.env` file."""
import os
from pathlib import Path
from typing import Self

_EQUALS = "="
_NEW_LINE = "\n"

_ENCLOSING_CHARS = f" \"'{_NEW_LINE}"


class UnsupportedFileFormatError(Exception):
    """Raised when the file format is not supported."""

    def __init__(self: Self, path: Path) -> None:
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

    return dict(os.environ)


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
