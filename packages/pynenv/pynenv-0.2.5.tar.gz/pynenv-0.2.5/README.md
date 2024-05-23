# Pynenv

Richer featured environment variable grabber.

## Install

```bash
pip install pynenv
```

## Example Useage

```python
from pynenv.environment import get_environment_variable, json2dict, yaml2dict

my_env_var = get_environment_variable('HOME')
json_dict = json2dict('test_json.json')
yaml_dict = yaml2dict('test_yaml.yaml')
```

## Build

* Adjust version in ```pyproject.toml```
* Run ```poetry build```
* Run ```poetry publish```
