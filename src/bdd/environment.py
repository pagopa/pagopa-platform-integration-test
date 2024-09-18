from src.config.configuration import settings
from src.config.configuration import secrets


def before_all(context):
    context.settings = settings
    context.secrets = secrets
