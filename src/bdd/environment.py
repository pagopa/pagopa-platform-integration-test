import logging

from src.conf.configuration import settings, secrets


def before_all(context):
    # load settings and secrets into context
    context.settings = settings
    context.secrets = secrets

    # configure logging setup
    logging.basicConfig(level=logging.DEBUG)
