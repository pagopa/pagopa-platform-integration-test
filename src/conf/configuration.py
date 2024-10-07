"""Parse configuration file to obtain current settings.
"""
import logging

from dynaconf import Dynaconf

ENV_VAR_PREFIX = 'WISP_DISMANTLING'

# `envvar_prefix` = export envvars with ENV_VAR_PREFIX as prefix.
# `settings_files` = Load settings files in the order.
settings = Dynaconf(
    envvar_prefix=ENV_VAR_PREFIX,
    settings_files=['config.yaml'],
)

# Load the secrets for the specified environment
secrets = {}

try:
    all_secrets = Dynaconf(settings_files=settings.SECRET_PATH)
    if settings.TARGET_ENV in all_secrets:
        secrets = all_secrets[settings.TARGET_ENV]
except AttributeError as e:
    logging.warning(e)
    exit()


commondata = Dynaconf(
    settings_files=['commondata.yaml'],
)

try:
    if commondata is not None:
        print('commondata is populated')
except AttributeError as e:
    logging.warning(e)
    exit()
