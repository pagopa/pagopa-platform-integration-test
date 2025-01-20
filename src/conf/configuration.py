"""Parse configuration file to obtain current settings.
"""
import logging
import os

import urllib3
from dynaconf import Dynaconf

ENV_VAR_PREFIX = 'WISP_DISMANTLING'

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# `envvar_prefix` = export envvars with ENV_VAR_PREFIX as prefix.
# `settings_files` = Load settings files in the order.
settings = Dynaconf(
    envvar_prefix=ENV_VAR_PREFIX,
    settings_files=['config.yaml'],
)

if 'TARGET_ENV' not in os.environ:
    os.environ['TARGET_ENV'] = 'uat'

settings = settings[os.environ['TARGET_ENV']]

# Load the secrets for the specified environment
secrets = {}

try:
    all_secrets = Dynaconf(settings_files=settings.SECRET_PATH)
    if settings.TARGET_ENV in all_secrets:
        secrets = all_secrets[settings.TARGET_ENV]
except AttributeError as e:
    logging.error(e)
    exit()

commondata = Dynaconf(
    settings_files=['commondata.yaml'],
)

try:
    commondata = commondata['TEST_DATA'].to_dict()
except KeyError as e:
    logging.error(e)
    exit()
