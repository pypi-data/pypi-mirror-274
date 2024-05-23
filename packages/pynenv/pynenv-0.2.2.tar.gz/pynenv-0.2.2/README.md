# Pynenv

Richer featured environment variable grabber.

## Install

```bash
pip install pynenv
```

## Example Useage

```python
from pynenv.environment import get_environment_variable, json2file, yaml2file

my_env_var = get_environment_variable('SOME_VAR')
json_dict = json
```

## Build

* Adjust version in ```pyproject.toml```
* Run ```poetry build```
* Run ```poetry publish```
