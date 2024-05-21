import os
from loguru import logger


def get_environment_variable(env_var):
    environment_variable = os.getenv(env_var)
    if environment_variable:
        logger.success(f'environment variable {env_var} retrrived successfully')
    if not environment_variable:
        logger.error(f'environment variable {env_var} either not set or empty')
    assert environment_variable != None, f'environment variable {env_var} either not set or empty'
    return environment_variable

if __name__ == "__main__":
    get_environment_variable('HOME')
