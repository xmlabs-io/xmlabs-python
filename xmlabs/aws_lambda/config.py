from dynaconf import Dynaconf
from dynaconf.constants import DEFAULT_SETTINGS_FILES

LOADERS_FOR_DYNACONF = [
    'dynaconf.loaders.env_loader', #Inorder to configure AWS_SSM_PREFIX we need to load it from environment
    'xmlabs.dynaconf.aws_ssm_loader',
    'dynaconf.loaders.env_loader', #Good to load environment last so that it takes precedenceover other config
]

ENVIRONMENTS= ['prod','dev','stage']

settings = Dynaconf(
    #settings_files=['settings.toml', '.secrets.toml'],
    warn_dynaconf_global_settings = True,
    load_dotenv = True,
    default_settings_paths = DEFAULT_SETTINGS_FILES,
    loaders = LOADERS_FOR_DYNACONF,
    envvar_prefix=  "APP",
    env_switcher = "APP_ENV",
    env='dev',
    environments=ENVIRONMENTS,
    #environments=True,
)

