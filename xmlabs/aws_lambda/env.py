import os
import logging

logger = logging.getLogger()


def get_environment(event, context=None):
    valid_envs = ["stage", "prod", "dev"]
    env = None
#    default_env = os.getenv("DEFAULT_ENV", "dev")
    default_env = os.getenv("APP_ENV", os.getenv("DEFAULT_ENV", "dev"))
    override_env = os.getenv("ENV")

    if override_env:
        logger.info("Overriding Environment with {}".format(override_env))
        return override_env

    ####################################
    ### X-Environment                ###
    ###   (override)                 ###
    ####################################
    if event.get('headers'):
        if event['headers'].get("X-Environment"):
            return event['headers']['X-Environment'].lower()


    ####################################
    ### if lambda function arn       ###
    ####################################
    split_arn = None
    try:
        split_arn = context.invoked_function_arn.split(':')
    except Exception as ex:
        split_arn = None
    if split_arn:

        ####################################
        ### lambda function arn alias    ###
        ###   (preferred)                ###
        ####################################
        e = split_arn[len(split_arn) - 1]
        if e in valid_envs:
            env = e
            return env.lower()


        #######################################
        ### Lambda Function Name Evaluation ###
        #######################################
        split_fn = split_arn[6].split("_")
        if split_fn[-1].lower() in valid_envs:
            return split_fn[-1].lower()


    ####################################
    ### Stage Variable Evaluation    ###
    ####################################
    apiStageVariable = None
    if event.get("stageVariables"):
        apiStageVariable = event["stageVariables"].get("env")
        env = apiStageVariable
    apiStage = None
    if event.get("requestContext"):
        apiStage = event["requestContext"].get("stage")
        if not env:
            env = apiStage
    if apiStage and apiStageVariable and apiStage != apiStageVariable:
        logger.warning("Tentrr: Using different api GW stagename and api Stage Variable is not recommended")
    if env:
        return env.lower()

    # If invoked without alias
    if (not split_arn or len(split_arn) == 7) and default_env:
        return default_env
    else:
        raise Exception("Environment could not be determined")
    return None
