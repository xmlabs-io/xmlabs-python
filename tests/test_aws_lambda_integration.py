
import pytest

from xmlabs import xmlabs_lambda_handler


@xmlabs_lambda_handler
def lambda_handler(event, context, config):
    assert(config)

def test_lambda_handler():
    lambda_handler({},{})
