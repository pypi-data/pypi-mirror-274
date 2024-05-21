# Pynenv

Richer featured environment variable grabber.

## Install

```bash
pip install pynenv
```

## Example Useage

```python
from pynenv.environment import get_environment_variable

my_env_var = get_environment_variable('SOME_VAR')
```

## Build

* Adjust version in ```pyproject.toml```
* Run ```poerty build```
* Run ```poetry publish```
