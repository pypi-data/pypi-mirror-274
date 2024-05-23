import os
import json
import yaml
from loguru import logger


def get_environment_variable(env_var):
    environment_variable = os.getenv(env_var)
    if environment_variable:
        logger.success(f'environment variable {env_var} retrrived successfully')
    if not environment_variable:
        logger.error(f'environment variable {env_var} either not set or empty')
    assert environment_variable != None, f'environment variable {
        env_var} not set'
    assert environment_variable != '', f'environment variable {env_var} empty'
    return environment_variable


def json2dict(json_file):
    logger.info(f'loading json file {json_file}')
    with open(json_file) as file:
        json_data = json.load(file)
    return json_data


def yaml2dict(yaml_file):
    logger.info(f'loading yaml file {yaml_file}')
    with open(yaml_file) as file:
        yaml_data = yaml.safe_load(file)
    return yaml_data
