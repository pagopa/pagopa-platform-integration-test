import json
import re
import xml.etree.ElementTree as xmlutils

import requests
from allure import attachment_type
from allure_commons._allure import attach

from src.utility import constants


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
