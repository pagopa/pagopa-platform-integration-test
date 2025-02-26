import datetime
import json
import logging
import random
import re
import string
import time
import xml.etree.ElementTree as xmlutils

import requests
from allure import attachment_type
from allure_commons._allure import attach

from src.utility.wisp import constants


def execute_request(url, method, headers, payload=None, type=constants.ResponseType.XML, allow_redirect=True,
                    description=None):
    if description is None:
        description = url

    if payload is not None:
        attach(obfuscate_secrets('URL: ' + url + '\nRequest:\n' + payload), name=f'{description} - Sent request',
               attachment_type=attachment_type.TEXT)

    response = requests.request(method=method, url=url, headers=headers, data=payload, verify=False,
                                allow_redirects=allow_redirect)

    object_response = None
    if not url.endswith('/info') and response.text is not None and len(response.text) > 0:

        if type == constants.ResponseType.XML:
            formatted_response = remove_namespace(response.text)

            attach(obfuscate_secrets('URL: ' + url + '\nResponse:\n' + formatted_response),
                   name=f'{description} - Received response', attachment_type=attachment_type.TEXT)
            if formatted_response is not None:
                object_response = xmlutils.fromstring(formatted_response)
        elif type == constants.ResponseType.JSON:
            object_response = response.json()
            attach(obfuscate_secrets('URL: ' + url + '\nResponse:\n' + json.dumps(object_response, indent=2)),
                   name=f'{description} - Received response', attachment_type=attachment_type.TEXT)
        elif type == constants.ResponseType.HTML:
            object_response = response.text
            attach(obfuscate_secrets('URL: ' + url + '\nResponse:\n' + object_response),
                   name=f'{description} - Received response', attachment_type=attachment_type.TEXT)

    return response.status_code, object_response, response.headers


def obfuscate_secrets(request):
    request_without_secrets = re.sub(r'<password>(.*)<\/password>', '<password>***</password>', request)
    request_without_secrets = re.sub(r'<password xmlns="">(.*)<\/password>', "<password xmlns=\"\">***</password>",
                                     request_without_secrets)
    request_without_secrets = re.sub(r'\"password\":\s{0,1}\"(.*)\"', "\"password\": \"***\"", request_without_secrets)
    request_without_secrets = re.sub(r'Ocp-Apim-Subscription-Key,(.*)\)', 'Ocp-Apim-Subscription-Key,***)',
                                     request_without_secrets)
    return request_without_secrets


def remove_namespace(content):
    content_without_ns = re.sub(r'(<\/?)(\w+:)', r'\1', content)
    content_without_ns = re.sub(r'\sxmlns[^"]+"[^"]+"', '', content_without_ns)
    content_without_ns = re.sub(r'\sxsi[^"]+"[^"]+"', '', content_without_ns)
    return content_without_ns


def generate_iuv(in_18digit_format=False):
    iuv = ''
    if in_18digit_format:
        iuv = '348' + get_random_digit_string(15)
    else:
        iuv = get_random_digit_string(15)
    return iuv;


def get_random_digit_string(length):
    return ''.join(random.choice(string.digits) for i in range(length))


def generate_random_monetary_amount(min, max):
    random_amount = random.uniform(min, max)
    return round(random_amount, 2)


def get_current_datetime():
    today = datetime.datetime.today().astimezone()
    return today.strftime('%Y-%m-%dT%H:%M:%S')


def generate_ccp():
    return get_random_digit_string(16)


def get_current_datetime():
    today = datetime.datetime.today().astimezone()
    return today.strftime('%Y-%m-%dT%H:%M:%S')


def get_current_date():
    today = datetime.datetime.today().astimezone()
    return today.strftime('%Y-%m-%d')


def get_index_from_cardinal(cardinal):
    index = -1
    match cardinal:
        case 'first':
            index = 0
        case 'second':
            index = 1
        case 'third':
            index = 2
        case 'fourth':
            index = 3
        case 'fifth':
            index = 4
    return index


def generate_nav(segregation_code):
    return f'3{segregation_code}{int(time.time() * 100000)}'


def get_tomorrow_datetime():
    today = datetime.datetime.today().astimezone()
    tomorrow = today + datetime.timedelta(days=1)
    return tomorrow.strftime('%Y-%m-%dT%H:%M:%S')


def assert_show_message(assertion_value, message):
    try:
        assert assertion_value, message
    except AssertionError as e:
        logging.error(f'[Assert Error] {e}')
        raise


def get_nested_field(object, field_name):
    try:
        nested_fields = field_name.split('.')
        analyzed_object = object
        for field in nested_fields:
            if field in analyzed_object:
                analyzed_object = analyzed_object[field]
            else:
                return None
        return analyzed_object
    except Exception as e:
        return None


def get_random_alphanumeric_string(length):
    return ''.join(random.choice(string.ascii_letters + string.digits) for i in range(length))

def generate_cart_id(iuv, creditor_institution):
    cart_id = ''
    if iuv is not None:
        cart_id = creditor_institution + iuv + '-' + get_random_digit_string(5)
    else:
        cart_id = get_random_digit_string(32)
    return cart_id

def change_last_numeric_char(value):
    last_char = value[-1]
    other_char = value[:-1]
    new_last_char = str((int(last_char) + 1) % 10)
    return other_char + new_last_char
