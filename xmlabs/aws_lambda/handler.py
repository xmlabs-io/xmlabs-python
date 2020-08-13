from .config import settings
from .env import get_environment
from functools import wraps


def lambda_handler(fn):
    @wraps(fn)
    def wrapped(*args, **kwargs):
        env, config = None , None
        try:
            env = get_environment(*args, **kwargs)
            if not env:
                raise Exception("No Environment detected")
        except Exception as ex:
            ## TODO: Improve Exception catching here
            ## TODO: Log to cloudwatch that Getting environment failed
            raise 

        try:
            config = settings.from_env(env)
            #config.setenv(env)
            if not config:
                raise Exception("No Configuration found")
        except Exception as ex:
            ## TODO: Improve Exception catching
            ## TODO: Log to cloudwatch that Retrieving Settings failed
            raise

        ## Standard Invoke logging for 
        #lambda_invoke_logger(*args, **kwargs)

        try:
            return fn(*args, **kwargs, config=config)
        except Exception as ex:
            # Make a standard error log to Cloudwatch for eas of capturing
            raise

    return wrapped
