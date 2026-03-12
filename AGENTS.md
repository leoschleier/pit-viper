# PROJECT KNOWLEDGE BASE

**Generated:** 2026-03-12
**Commit:** 093c941
**Branch:** main

## OVERVIEW

Python configuration library (Go Viper-inspired). Reads config from files (JSON/TOML/YAML) and `.env` environment variables. Singleton module-level state, no class instances. Published to PyPI as `pit-viper`, imported as `from pit import viper`.

## STRUCTURE

```
pit-viper/
├── src/pit/viper/       # Library source (namespace pkg `pit`)
│   ├── __init__.py      # Public API re-exports (get, set, load_config, auto_env, ...)
│   ├── _config.py       # Config file loading, get/set with dot-notation keys
│   ├── _env.py          # .env parsing, env var access, prefix/replacer
│   └── _io.py           # File readers: JSON, TOML, YAML
├── tests/               # pytest suite, one file per source module
│   ├── conftest.py      # Autouse fixtures: env cleanup + viper state reset
│   ├── config.py        # Shared test constants (paths to fixture data)
│   └── data/            # Static fixture files (.env, config.{json,toml,yaml})
├── scripts/             # Shell scripts (no extensions)
│   ├── validate         # Full pipeline: ruff format + ruff check + mypy + pyright + pytest
│   ├── setup            # Symlinks pre-commit hook into .git/hooks/
│   ├── publish          # poetry publish --build
│   └── hooks/pre-commit # Delegates to scripts/validate
└── docs/                # README.md, CHANGELOG.md (commitizen-managed)
```

## WHERE TO LOOK

| Task | Location | Notes |
|------|----------|-------|
| Public API | `src/pit/viper/__init__.py` | All exports; `get_conf` aliased as `get`, `set_conf` as `set` |
| Config file loading | `src/pit/viper/_config.py` | Dot-notation key access, recursive `_safe_set` for nested configs |
| Env var handling | `src/pit/viper/_env.py` | `auto_env()` loads `.env`; prefix + key replacer logic |
| File format support | `src/pit/viper/_io.py` | `read_config()` dispatches by extension via `match` |
| Value resolution | `_config.py:get_conf` | Env vars take precedence over config file values |
| Test fixtures | `tests/conftest.py` | Autouse: clears env vars + resets module globals |
| Test data paths | `tests/config.py` | `TEST_CONFIG_DIR`, `TEST_DOTENV_PATH` constants |
| Validation | `scripts/validate` | Run this to check everything locally |

## CODE MAP

| Symbol | Type | Location | Role |
|--------|------|----------|------|
| `get` (`get_conf`) | function | `_config.py:52` | Get value: env var precedence, then config dict with dot-path traversal |
| `set` (`set_conf`) | function | `_config.py:81` | Set value in config dict, creates nested dicts for dot-paths |
| `load_config` | function | `_config.py:101` | Read config file via `_io`, merge into state with `_safe_set` |
| `auto_env` | function | `_env.py:23` | Load `.env` file, enable env var lookups |
| `set_env_prefix` | function | `_env.py:76` | Prefix for env key lookup (uppercased) |
| `set_env_key_replacer` | function | `_env.py:96` | String replacements applied to keys before env lookup |
| `get_env` | function | `_env.py:112` | Internal: resolve key to env var with prefix + replacer |
| `read_config` | function | `_io.py:10` | Dispatch to format-specific reader by file extension |
| `UnsupportedFileFormatError` | exception | `_env.py:15` | Raised for non-`.env` files passed to `auto_env` |

## ARCHITECTURE

- **Singleton pattern**: All state is module-level globals (`_config`, `_config_path`, `_env_prefix`, etc.). No way to create isolated instances.
- **Value precedence**: `get()` checks env vars first, falls back to config dict.
- **Dot-notation keys**: `get("foo.bar")` traverses nested dicts. `set("foo.bar", v)` creates intermediate dicts.
- **`_safe_set`**: Recursive merge during `load_config` -- preserves manually `set()` defaults when loading from file.
- **Namespace package**: `src/pit/__init__.py` exists but is intended as a namespace root for potential sibling packages.

## CONVENTIONS

- **Line length**: 79 chars code, 72 chars docstrings
- **Linting**: `ruff select = ["ALL"]` -- every rule enabled; only `ANN401`, `COM812`, `ISC001` ignored
- **Formatting**: `ruff format` (not Black, despite vestigial `[tool.black]` config)
- **Type checking**: Both Pyright (strict) and Mypy run on every commit
- **Docstrings**: NumPy convention, required on every public function/module
- **Private modules**: Underscore prefix (`_config.py`, `_env.py`, `_io.py`); public API re-exported from `__init__.py`
- **Tests**: Plain functions (no classes), full type annotations, NumPy docstrings
- **Test naming**: `test_<module>.py` files, `test_<behavior>()` functions; private modules get `test__<name>.py` (double underscore)
- **Autouse fixtures**: Underscore-prefixed (`_prepare_env`, `_reset_viper`)
- **Commits**: Conventional Commits via Commitizen
- **Scripts**: Shell scripts without `.sh` extension, custom git hooks (not `pre-commit` framework)

## ANTI-PATTERNS

None found in source code (no TODO/FIXME/HACK/DEPRECATED markers). Clean codebase.

## COMMANDS

```bash
# Setup (first time)
poetry install
./scripts/setup          # symlinks pre-commit hook

# Full validation (format + lint + typecheck + test)
./scripts/validate

# Individual checks
ruff format . --check    # formatting
ruff check .             # linting
mypy .                   # type checking
pyright .                # strict type checking
pytest .                 # tests

# Publish
./scripts/publish        # poetry publish --build
```

## NOTES

- `scripts/validate` assumes `.venv` exists; run `poetry install` first
- No CI test/lint workflow on PRs -- validation is local pre-commit only
- `[tool.black]` in `pyproject.toml` is dead config (Ruff is the formatter)
- Python 3.11 only (`^3.11`) -- narrow support window for a library
- Version tracked in both `pyproject.toml` and `src/pit/viper/__version__.py` (Commitizen keeps them in sync)
