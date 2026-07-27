import os

from urllib.parse import unquote
from src.integration.fdr import common
from src.utility.rest.rest_auth_factory import build_api_key_auth_from_config
from src.utility.rest.rest_client_factory import build_rest_client
from src.integration.conf.configuration import commondata
from src.integration.conf.configuration import secrets
from src.integration.conf.configuration import settings


def before_all(context):
    context.settings = settings
    context.secrets = secrets
    context.commondata = commondata

    context.fdr.rest.auth = build_api_key_auth_from_config(context.config["fdr"]["api_key"])
    context.fdr.rest.client = build_rest_client(context.config["service"], context.fdr.rest.auth)

    context.psp.rest.auth = build_api_key_auth_from_config(context.config["psp"]["api_key"])
    context.psp.rest.client = build_rest_client(context.config["service"], context.psp.rest.auth)


def before_scenario(context, scenario):
    clear_context(context)
    for tag in scenario.tags:
        if tag.startswith("Crea_FdR"):
            # Extract parameters from the tag and create a FdR
            params_str = tag[tag.find("(") + 1:tag.find(")")].split(",")
            params = dict(item.split("=") for item in params_str.split(", "))
            context.fdr_id = unquote(params["id_fdr"])
            context.psp_id = unquote(params["id_psp"])
            common.create_fdr(context, context.fdr_id, context.psp_id)
        elif tag.startswith("Inserisci_Pagamenti"):
            # Extract parameters from the tag and insert payments
            params_str = tag[tag.find("(") + 1:tag.find(")")].split(",")
            params = dict(item.split("=") for item in params_str.split(", "))
            context.tot_payments = int(params["totPayments"])
            context.sum_payments = int(params["sumPayments"])
            common.insert_payments(context, context.tot_payments, context.sum_payments)
        elif tag.startswith("Pubblica_FdR"):
            # Publish the FdR
            common.publish_fdr(context)

    if hasattr(scenario, 'row') and scenario.row:
        # Check if the scenario has a "stato_esistente" column
        stato_esistente = scenario.row.get("stato_esistente")
        # If the "stato_esistente" column is present and its value is "INSERTED", insert payments
        if stato_esistente == "INSERTED":
            common.insert_payments(context, 3, 3000)
    
            

def after_scenario(context, scenario):
    clear_context(context)

def after_all(context):
    clear_context(context)
    context.fdr.rest.client.close()
    context.fdr = None
    context.psp.rest.client.close()
    context.psp = None


def clear_context(context):
    context.response = None
    context.get_fdr_response = None
    context.request_date = None
    context.fdr_id = None
    context.psp = None
    context.sender = None
    context.receiver = None
    context.bic_code_pouring_bank = None
    context.tot_payments = None
    context.sum_payments = None
    context.get_psp_response = None
