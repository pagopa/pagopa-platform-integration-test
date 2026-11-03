import json
import re
import xml.etree.ElementTree as xmlutils

import requests
from allure import attachment_type
from allure_commons._allure import attach

from . import constants


NON_XML_BODY_MAX_CHARS = 500


def execute_request(url, method, headers, payload=None, type=constants.ResponseType.XML, allow_redirect=True,
                    description=None):
    """Execute an HTTP call, attach the exchange to the Allure report and return the parsed response.

    The received response is attached with its URL and HTTP status (an empty error body is attached as
    `<empty body>`). Returns `(status_code, parsed_body, headers)`; a body that does not match `type`
    (e.g. a JSON 500 for an XML call) raises an AssertionError carrying the status and a truncated body after the
    response was attached, so Allure reports a failed (not broken) step.
    """
    if description is None:
        description = url

    if payload is not None:
        attach(obfuscate_secrets('URL: ' + url + '\nRequest:\n' + payload), name=f'{description} - Sent request',
               attachment_type=attachment_type.TEXT)

    response = requests.request(method=method, url=url, headers=headers, data=payload, verify=False,
                                allow_redirects=allow_redirect)

    # The HTTP status is part of the attachment because a non-XML error body (e.g. an APIM 500) would otherwise
    # only surface as a parser exception, and the AI report analysis reads this header to tell the two apart.
    response_header = f'URL: {url}\nHTTP status: {response.status_code}\nResponse:\n'

    object_response = None
    if not url.endswith('/info') and response.text is not None and len(response.text) > 0:

        if type == constants.ResponseType.XML:
            formatted_response = remove_namespace(response.text)

            attach(obfuscate_secrets(response_header + formatted_response),
                   name=f'{description} - Received response', attachment_type=attachment_type.TEXT)
            if formatted_response is not None:
                try:
                    object_response = xmlutils.fromstring(formatted_response)
                except xmlutils.ParseError as error:
                    raise AssertionError(f'Response is not valid XML. HTTP status: {response.status_code}. '
                                         f'Body: {response.text[:NON_XML_BODY_MAX_CHARS]}') from error
        elif type == constants.ResponseType.JSON:
            object_response = response.json()
            attach(obfuscate_secrets(response_header + json.dumps(object_response, indent=2)),
                   name=f'{description} - Received response', attachment_type=attachment_type.TEXT)
        elif type == constants.ResponseType.HTML:
            object_response = response.text
            attach(obfuscate_secrets(response_header + object_response),
                   name=f'{description} - Received response', attachment_type=attachment_type.TEXT)
    elif not url.endswith('/info') and response.status_code >= 400:
        attach(response_header + '<empty body>',
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
