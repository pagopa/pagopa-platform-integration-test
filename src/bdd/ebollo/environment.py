import logging

from src.conf.configuration import commondata
from src.conf.configuration import secrets
from src.conf.configuration import settings


def before_all(context):
    # load settings and secrets into context
    context.settings = settings
    context.secrets = secrets
    context.commondata = commondata

    # configure logging setup
    logging.basicConfig(level=logging.DEBUG)
