# pit-viper

Pit-Viper is a Python package that offers configuration management capabilities
like the Viper package in Golang.

## Table of Contents

1. [Installation](#installation)

2. [Usage](#usage)

3. [Development](#development)

## Installation

You can install `pit-viper` using `pip`:
 
```bash
pip install pit-viper
```

## Usage

### Environment Variables

The `pit-viper` package provides the `auto_env` function that loads environment
variables from a `.env` file. The function returns a `dict` of all existing
environment variables.

```python
from pit import viper

env = viper.auto_env()
```

We recommend accessing your environment variables via `viper.get`. 

```python
from pit import viper

viper.auto_env()
bar = viper.get("foo")
```

With this, you could also use`viper.set` to specify default parameters up
front.

**Note**: Changes to the environment following the first import of `pit-viper`
will not be reflected in the package's record of environment variables.

### Config Files

Config files are another config source for `pit-viper`. The package supports
loading, accessing, and setting defaults for a config. Supported file formats
are JSON, TOML, and YAML.

```python
from pathlib import Path
from pit import viper

MY_CONFIG_DIR = Path() / "config"

viper.set_config_path(MY_CONFIG_DIR)
viper.set_config_name("my_config")
viper.set_config_type("toml")

viper.set("foo", "default-value")

viper.load_config()

bar = viper.get("foo")
nested_parameter = viper.get("my.nested.parameter")
```

**Note**: After loading the environment varibles with `viper.auto_env`, every
call of `viper.get` will try to retrieve the parameter from the environment
variables before performing a lookup in the parameters of the config file.

## Development

We use [Poetry](https://github.com/python-poetry/poetry) for packaging and
dependency management.
We recommend creating your virtual environment in a directory named `.venv` in
the project's root directory. This ensures that all scripts and git hooks
relying on the Python environment will work properly. Therefore, after
installing Poetry, consider running the command below to configure Poetry for
the present project.

```bash
poetry config virtualenvs.in-project true --local 
```

Afterward, you can run the `install` command to install the dependencies
(including development requirements) specified in the `pyproject.toml` or
`poetry.lock` file.

```bash
poetry install
```

For a more comprehensive description of the Poetry setup and commands, see
their [documentation](https://python-poetry.org/docs).

The `pit-viper` package is intended to be
[PEP 561](https://peps.python.org/pep-0561/) compatible. For this reason, we
use a pre-commit hook that validates the code on every commit. The code
validation includes checks with Black, Ruff, Mypy, and Pyright.
