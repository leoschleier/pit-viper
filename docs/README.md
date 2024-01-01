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

## Development

We use [Poetry](https://github.com/python-poetry/poetry) for packaging and
dependency management.
After installing Poetry, consider running the command below to configure Poetry
to create virtual environments in a folder named `.venv` within the project's
root directory.

```bash
poetry config virtualenvs.in-project true
```

Afterward, you can run the `install` command to install the dependencies
(including development requirements) specified in the `pyproject.toml` or
`poetry.lock` file.

```bash
poetry install
```

For a more comprehensive description of the Poetry setup and commands, see
their [documentation](https://python-poetry.org/docs).
