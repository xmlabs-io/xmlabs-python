import boto3
import logging
import requests
from functools import lru_cache
from dynaconf.utils.parse_conf import parse_conf_data


logger = logging.getLogger()

IDENTIFIER = 'aws_ssm'


def load(obj, env=None, silent=True, key=None, filename=None):
    """
    Reads and loads in to "obj" a single key or all keys from source
    :param obj: the settings instance
    :param env: settings current env (upper case) default='DEVELOPMENT'
    :param silent: if errors should raise
    :param key: if defined load a single key, else load all from `env`
    :param filename: Custom filename to load (useful for tests)
    :return: None
    """
    # Load data from your custom data source (file, database, memory etc)
    # use `obj.set(key, value)` or `obj.update(dict)` to load data
    # use `obj.find_file('filename.ext')` to find the file in search tree
    # Return nothing
    prefix = ""
    if obj.get("AWS_SSM_PREFIX"):
        prefix = "/{}".format(obj.AWS_SSM_PREFIX)
    path = "{}/{}/".format(prefix, env.lower())
    if key:
        path =  "{}{}/".format(path, key)
    data = _read_aws_ssm_parameters(path)

    try:
        if data and key:
            value = parse_conf_data(
                data.get(key), tomlfy=True, box_settings=obj)
            if value:
                obj.set(key, value)
        elif data:
            obj.update(data, loader_identifier=IDENTIFIER, tomlfy=True)
    except Exception as e:
        if silent:
            return False
        raise


@lru_cache
def _read_aws_ssm_parameters(path):
    logger.debug(
        "Reading settings AWS SSM Parameter Store (Path = {}).".format(path)
    )
    print(
        "Reading settings AWS SSM Parameter Store (Path = {}).".format(path)
    )
    result = {}
    try:
        ssm = boto3.client("ssm")
        response = ssm.get_parameters_by_path(
            Path=path,
            Recursive=True,
            WithDecryption=True
        )
        while True:
            params = response["Parameters"]
            for param in params:
                name = param["Name"].replace(path, "").replace("/", "_")
                value = param["Value"]
                result[name] = value
            if "NextToken" in response:
                response = ssm.get_parameters_by_path(
                    Path=path,
                    Recursive=True,
                    WithDecryption=True,
                    NextToken=response["NextToken"],
                )
            else:
                break

    except Exception as ex:
        print(
            "ERROR: Trying to read aws ssm parameters (for {}): {}!".format(
                path, str(ex)
            )
        )
        result = {}

    logger.debug("Read {} parameters.".format(len(result)))
    return result
