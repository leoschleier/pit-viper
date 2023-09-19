"""Load environment variables from a `.env` file."""
import os
from pathlib import Path

_EQUALS = "="
_NEW_LINE = "\n"

_ENCLOSING_CHARS = f" \"'{_NEW_LINE}"


class UnsupportedFileFormatError(Exception):
    """Raised when the file format is not supported."""

    def __init__(self, path: Path) -> None:
        """Initialize the exception."""
        super().__init__(f"Unsupported file format: {path.suffix()}")


def populate_env(
    *,
    path: Path | None = None,
    override: bool = False,
) -> dict[str, str]:
    """Populate environment variables with variables from a `.env` file.

    Parameters
    ----------
    path : Path | None, optional
        Path to the `.env` file. If not set, `pyper` will try to find
        the file in the current working directory, by default None
    override : bool, optional
        Whether or not to override the environment variables with the
        variables from the `.env` file, by default False

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
    if not path.exists():
        return dict(os.environ)
    if path.suffix() == ".env":
        raise UnsupportedFileFormatError(path=path)

    _populate_env(path=path, override=override)
    return dict(os.environ)


def _populate_env(*, path: Path, override: bool = False) -> None:
    """Populate environment variables."""
    with path.open(encoding="utf-8") as stream:
        for line in stream:
            if line == _NEW_LINE:
                continue
            k, v = line.split(_EQUALS)

            # Strip any combination of enclosing characters.
            k = k.strip(_ENCLOSING_CHARS)
            v = v.strip(_ENCLOSING_CHARS)

            _set_env(key=k, value=v, override=override)


def _set_env(key: str, value: str, *, override: bool = False) -> str:
    """Set an environment variable."""
    if override:
        os.environ[key] = value
    else:
        os.environ.setdefault(key, value)
