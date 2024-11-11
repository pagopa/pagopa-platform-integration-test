import logging
import time
from tabnanny import check
from urllib.parse import parse_qs
from urllib.parse import urlparse

import src.bdd.steps.request_generator as requestgen
import src.bdd.steps.session as session
from allure_commons._allure import attach
from behave import *

from src.utility import constants
from src.utility import routes as router
from src.utility import utils


def check_status_code(context, actor, expected_status_code):
    actual_status_code = context.flow_data['action']['response']['status_code']
    assert int(expected_status_code) == actual_status_code, f'The status code is not {expected_status_code}. Current value: {actual_status_code}.'

# @when('the {actor} sends a {primitive} action')
def send_primitive(context, actor, primitive):
    # skipping this step if its execution is not required
    if session.skip_tests(context):
        logging.debug('Skipping send_primitive step')
        return

    # retrieve generated request from context in order to execute the API call
    request = context.flow_data['action']['request']['body']

    # initialize API call and get response
    url, subkey, content_type = router.get_primitive_url(context, primitive)
    headers = {}
    if content_type == constants.ResponseType.XML:
        headers = {'Content-Type': 'application/xml', 'SOAPAction': primitive,
                   constants.OCP_APIM_SUBSCRIPTION_KEY: subkey}
    elif content_type == constants.ResponseType.JSON:
        headers = {'Content-Type': 'application/json', constants.OCP_APIM_SUBSCRIPTION_KEY: subkey}
    req_description = constants.REQ_DESCRIPTION_EXECUTE_SOAP_CALL.format(step=context.running_step)

    status_code, body_response, _ = utils.execute_request(url, 'post', headers, request, content_type,
                                                          description=req_description)

    # update context setting all information about response
    context.flow_data['action']['response']['status_code'] = status_code
    context.flow_data['action']['response']['body'] = body_response
    context.flow_data['action']['response']['content_type'] = content_type

    logging.info(f'Response status code: {status_code}')
    logging.info(f'Response body: {body_response}')

# @then('the response contains the field {field_name} with value {field_value}')  # MODIFIED
def check_field(context, field_name, field_value):
    # skipping this step if its execution is not required
    if session.skip_tests(context):
        logging.debug('Skipping check_field step')
        return

    # retrieve response information related to executed request
    field_value = field_value.replace('\'', '')
    response = context.flow_data['action']['response']['body']

    content_type = context.flow_data['action']['response']['content_type']

    # executing assertions
    if content_type == constants.ResponseType.XML:
        field_value_in_object = response.find(f'.//{field_name}')

        utils.assert_show_message(field_value_in_object is not None, f'The field [{field_name}] does not exists.')
        field_value_in_object = field_value_in_object.text
    elif content_type == constants.ResponseType.JSON:
        field_value_in_object = utils.get_nested_field(response, field_name)
        utils.assert_show_message(field_value_in_object is not None, f'The field [{field_name}] does not exists.')
        utils.assert_show_message(field_value_in_object == field_value,
                                  f'The field [{field_name}] is not equals to {field_value}. Current value: {field_value_in_object}.')

# @then('the response contains the {url_type} URL')  # MODIFIED
def check_redirect_url(context, url_type):
    # retrieve information related to executed request
    response = context.flow_data['action']['response']['body']

    url = response.find('.//url')
    utils.assert_show_message(url is not None, f"The field 'redirect_url' in response doesn't exists.")
    extracted_url = url.text
    parsed_url = urlparse(extracted_url)
    query_params = parse_qs(parsed_url.query)
    id_session = query_params['idSession'][0] if len(query_params['idSession']) > 0 else None

    # executing assertions
    utils.assert_show_message(id_session is not None, f"The field 'idSession' in response is not correctly set.")
    if 'redirect' in url_type:
        utils.assert_show_message('wisp-converter' in extracted_url,
                                  f'The URL is not the one defined for WISP dismantling.')
    elif 'old WISP' in url_type:
        utils.assert_show_message('wallet' in extracted_url, f'The URL is not the one defined for old WISP.')
    elif 'fake WFESP' in url_type:
        utils.assert_show_message('wfesp' in extracted_url, f'The URL is not the one defined for WFESP dismantling.')

    # set session identifier in context in order to be better analyzed in the next steps
    context.flow_data['common']['session_id'] = id_session

#@given('a valid session identifier to be redirected to WISP dismantling')
def get_valid_sessionid(context):
    session.set_skip_tests(context, False)

    # retrieve session id previously generated in redirect call
    session_id = context.flow_data['common']['session_id']

    # executing assertions
    utils.assert_show_message(len(session_id) == 36,
                              f'The session ID must consist of a UUID only. Session ID: [{session_id}]')

# @when('the user continue the session in WISP dismantling')
def send_sessionid_to_wispdismantling(context):
    # initialize API call and get response
    url, _ = router.get_rest_url(context, 'redirect')
    headers = {'Content-Type': 'application/xml'}
    session_id = context.flow_data['common']['session_id']

    url += session_id
    req_description = constants.REQ_DESCRIPTION_EXECUTE_CALL_TO_WISPCONV.format(step=context.running_step,
                                                                                sessionId=session_id)
    status_code, response_body, response_headers = utils.execute_request(url, 'get', headers,
                                                                         type=constants.ResponseType.HTML,
                                                                         allow_redirect=False,
                                                                         description=req_description)

    # update context setting all information about response
    if 'Location' in response_headers:
        location_header = response_headers['Location']
        attach(location_header, name='Received response')

        context.flow_data['action']['response']['body'] = location_header

    else:
        attach(response_body, name='Received response')
        context.flow_data['action']['response']['body'] = response_body

    context.flow_data['action']['response']['status_code'] = status_code
    context.flow_data['action']['response']['content_type'] = constants.ResponseType.HTML

# @then('the user can be redirected to Checkout')
def check_checkout_url(context):
    # retrieve redirect URL extracted from executed request
    location_redirect_url = context.flow_data['action']['response']['body']

    # executing assertions
    utils.assert_show_message(location_redirect_url is not None, f"The header 'Location' does not exists.")
    utils.assert_show_message('ecommerce/checkout' in location_redirect_url,
                              f"The header 'Location' does not refers to Checkout service. {location_redirect_url}")

# @given('a waiting time of {time_in_seconds} second{notes}')
def wait_for_n_seconds(context, time_in_seconds, notes):
    session.set_skip_tests(context, False)
    logging.info(f'Waiting [{time_in_seconds}] second{notes}')
    time.sleep(int(time_in_seconds))
    logging.info(f'Wait time ended')

# @given('the {index} IUV code of the sent RPTs')  # MODIFIED
def get_iuv_from_session(context, index):
    session.set_skip_tests(context, False)

    # retrieve raw RPTs from context
    rpt_index = utils.get_index_from_cardinal(index)
    raw_rpts = context.flow_data['common']['rpts']

    # check if IUV at passed index exists
    if rpt_index + 1 > len(raw_rpts):
        session.set_skip_tests(context, True)
        return

    #  update IUV structure with the one retrieved from raw RPTs
    iuv = raw_rpts[rpt_index]['payment_data']['iuv']
    iuvs = context.flow_data['common']['iuvs']

    if iuvs is None:
        iuvs = [None, None, None, None, None]
    iuvs[rpt_index] = iuv

    # update context with IUVs to be sent
    context.flow_data['common']['iuvs'] = iuvs

# @when('the user searches for flow steps by IUVs')  # MODIFIED
def search_in_re_by_iuv(context):
    # skipping this step if its execution is not required
    if session.skip_tests(context):
        logging.debug('Skipping search_in_re_by_iuv step')
        return

    # retrieve and initialize information needed for next API execution
    iuvs = context.flow_data['common']['iuvs']

    creditor_institution = context.commondata['creditor_institution']

    today = utils.get_current_date()
    re_events = []

    # initialize API call main information
    base_url, subkey = router.get_rest_url(context, 'search_in_re_by_iuv')
    headers = {'Content-Type': 'application/json', constants.OCP_APIM_SUBSCRIPTION_KEY: subkey}

    # for each iuv it is required to retrieve events from RE

    for iuv in iuvs.values():
        if iuv is not None:
            # initialize API call and get response
            url = base_url.format(creditor_institution=creditor_institution, iuv=iuv, date_from=today, date_to=today)
            req_description = constants.REQ_DESCRIPTION_RETRIEVE_EVENTS_FROM_RE.format(step=context.running_step,
                                                                                       iuv=iuv)
            status_code, body_response, _ = utils.execute_request(url, 'get', headers, type=constants.ResponseType.JSON,
                                                                  description=req_description)

            # executing assertions
            utils.assert_show_message('data' in body_response, f'The response does not contains data.')
            utils.assert_show_message(len(body_response['data']) > 0, f'There are not event data in the response.')

            # add received event on the list of whole events
            re_events.extend(body_response['data'])

    # update context setting all information about response
    context.flow_data['action']['response']['status_code'] = status_code

    context.flow_data['action']['response']['body'] = re_events

# @then('all the related notice numbers can be retrieved')
def retrieve_payment_notice_from_re_event(context):
    # retrieve events elated to executed request
    re_events = context.flow_data['action']['response']['body']

    # executing assertions
    needed_events = [re_event for re_event in re_events if 'status' in re_event and re_event[
        'status'] == 'SAVED_RPT_IN_CART_RECEIVED_REDIRECT_URL_FROM_CHECKOUT']
    utils.assert_show_message(len(needed_events) > 0,
                              f'The redirect process is not ended successfully or there are missing events in RE')
    notices = set([(re_event['domainId'], re_event['iuv'], re_event['noticeNumber']) for re_event in needed_events])
    utils.assert_show_message(len(notices) > 0, f'Impossible to extract payment notices from events in RE')

    # set updated payment notices in context in order to be better analyzed in the next steps
    payment_notices = []
    for payment_notice in notices:
        payment_notices.append({
            'domain_id': payment_notice[0],
            'iuv': payment_notice[1],
            'notice_number': payment_notice[2],
            'payment_token': None
        })

    context.flow_data['common']['payment_notices'] = payment_notices

# @given('a valid checkPosition request')
def generate_checkposition(context):
    session.set_skip_tests(context, False)

    # generate checkPosition request from retrieved payment notices
    payment_notices = context.flow_data['common']['payment_notices']

    request = requestgen.generate_checkposition(payment_notices)

    # update context with request to be sent
    context.flow_data['action']['request']['body'] = request

# @then('the response contains the field {field_name} as not empty list')  # MODIFIED
def check_field_as_not_empty_list(context, field_name):
    # retrieve response information related to executed request

    response = context.flow_data['action']['response']['body']
    content_type = context.flow_data['action']['response']['content_type']

    # executing assertions
    if content_type == constants.ResponseType.XML:
        field_value_in_object = response.find(f'.//{field_name}')
    elif content_type == constants.ResponseType.JSON:
        field_value_in_object = utils.get_nested_field(response, field_name)

    utils.assert_show_message(field_value_in_object is not None, f'The field [{field_name}] does not exists.')
    utils.assert_show_message(len(field_value_in_object) > 0,
                              f'The field [{field_name}] is empty but is required to be not empty.')

# @given('a valid activatePaymentNoticeV2 request on {index} payment notice')  # MODIFIED
def generate_activatepaymentnotice(context, index):
    session.set_skip_tests(context, False)

    # retrieve test_data in order to generate flow_data session data
    test_data = context.commondata

    # retrieve session id previously generated in redirect call
    session_id = context.flow_data['common']['session_id']

    # retrieve payment notices in order to generate request
    payment_notice_index = index

    payment_notices = context.flow_data['common']['payment_notices']

    # check if payment notice at passed index exists
    if payment_notice_index + 1 > len(payment_notices):
        session.set_skip_tests(context, True)
        return

    # generate activatePaymentNoticeV2 request from retrieved payment notices
    rpts = context.flow_data['common']['rpts']

    request = requestgen.generate_activatepaymentnotice(test_data, payment_notices, rpts[payment_notice_index],
                                                        session_id, context.secrets.CHANNEL_CHECKOUT_PASSWORD)

    # update context with request to be sent
    context.flow_data['action']['request']['body'] = request

# @then('the response contains the field {field_name} with non-null value')  # MODIFIED
def check_field_with_non_null_value(context, field_name):
    # skipping this step if its execution is not required
    if session.skip_tests(context):
        logging.debug('Skipping check_field step')
        return

    # retrieve response information related to executed request
    response = context.flow_data['action']['response']['body']
    content_type = context.flow_data['action']['response']['content_type']

    # executing assertions
    if content_type == constants.ResponseType.XML:
        field_value_in_object = response.find(f'.//{field_name}')
    elif content_type == constants.ResponseType.JSON:
        field_value_in_object = utils.get_nested_field(response, field_name)
    utils.assert_show_message(field_value_in_object is not None, f'The field [{field_name}] does not exists.')

# @then('the payment token can be retrieved and associated to {index} RPT')  # MODIFIED
def retrieve_payment_token_from_activatepaymentnotice(context, index):
    # skipping this step if its execution is not required
    if session.skip_tests(context):
        logging.debug('Skipping retrieve_payment_token_from_activatepaymentnotice step')
        return

    # retrieve information related to executed request
    rpt_index = index
    response = context.flow_data['action']['response']['body']

    field_value_in_object = response.find('.//paymentToken')
    # executing assertions
    payment_notices = context.flow_data['common']['payment_notices']

    utils.assert_show_message(len(payment_notices) >= rpt_index + 1,
                              f'Not enough payment notices are defined in the session data for correctly point at index {rpt_index}.')
    payment_notice = payment_notices[rpt_index]
    utils.assert_show_message('iuv' in payment_notice, f'No valid payment is defined at index {rpt_index}.')
    payment_notice['payment_token'] = field_value_in_object.text

    context.flow_data['common']['payment_notices'] = payment_notices

# @then('there is a {business_process} event with field {field_name} with value {field_value}')  # MODIFIED
def check_event(context, business_process, field_name, field_value):
    # skipping this step if its execution is not required
    if session.skip_tests(context):
        logging.debug('Skipping check_event step')
        return

    # retrieve response information related to executed request
    re_events = context.flow_data['action']['response']['body']

    # executing assertions
    needed_process_events = [re_event for re_event in re_events if
                             'businessProcess' in re_event and re_event['businessProcess'] == business_process]
    utils.assert_show_message(len(needed_process_events) > 0,
                              f'There are not events with business process {business_process}.')
    needed_events = [re_event for re_event in needed_process_events if
                     field_name in re_event and re_event[field_name] == field_value]

    utils.assert_show_message(len(needed_events) > 0,
                              f'There are not events with business process {business_process} and field {field_name} with value [{field_value}].')

    # set needed events in context in order to be better analyzed in the next steps
    context.flow_data['common']['re']['last_analyzed_event'] = needed_events

# @then('these events are related to each payment token')  # MODIFIED
def check_event_token_relation(context):
    # retrieve events and payment notices related to executed request
    needed_events = context.flow_data['common']['re']['last_analyzed_event']

    payment_notices = context.flow_data['common']['payment_notices']

    # executing assertions
    payment_tokens = [payment_notice['payment_token'] for payment_notice in payment_notices]
    for payment_token in payment_tokens:
        utils.assert_show_message(any(event['paymentToken'] == payment_token for event in needed_events),
                                  f'The payment token {payment_token} is not correctly handled by the previous event.')

# @given('a valid closePaymentV2 request with outcome {outcome}')  # MODIFIED
def generate_closepayment(context, outcome):
    session.set_skip_tests(context, False)

    # retrieve test_data in order to generate flow_data session data
    test_data = context.commondata

    # generate request
    payment_notices = context.flow_data['common']['payment_notices']

    # generate closePaymentV2 request from retrieved raw RPTs and payment notices
    rpts = context.flow_data['common']['rpts']

    request = requestgen.generate_closepayment(test_data, payment_notices, rpts, outcome)

    # update context with request to be sent
    context.flow_data['action']['request']['body'] = request

# @given('all the IUV codes of the sent RPTs')  # MODIFIED
def get_iuvs_from_session(context):
    session.set_skip_tests(context, False)

    # retrieve raw RPTs from context
    raw_rpts = context.flow_data['common']['rpts']

    #  update IUV structure with all the ones retrieved from raw RPTs
    iuvs = context.flow_data['common']['iuvs']

    if iuvs is None:
        iuvs = [None, None, None, None, None]
    rpt_index = 0
    for raw_rpt in raw_rpts:
        iuv = raw_rpt['payment_data']['iuv']
        iuvs[rpt_index] = iuv
        rpt_index += 1

    # update context with IUVs to be sent
    context.flow_data['common']['iuvs'] = iuvs

# @then('these events are related to each notice number')  # MODIFIED
def check_event_notice_number_relation(context):
    # retrieve events and payment notices related to executed request
    needed_events = context.flow_data['common']['re']['last_analyzed_event']

    payment_notices = context.flow_data['common']['payment_notices']

    # executing assertions
    notice_numbers = [payment_notice['notice_number'] for payment_notice in payment_notices]
    for notice_number in notice_numbers:
        utils.assert_show_message(any(event['noticeNumber'] == notice_number for event in needed_events),
                                  f'The notice number {notice_number} is not correctly handled by the previous event.')

# @when('the user searches for payment position in GPD by {index} IUV')  # MODIFIED
def search_paymentposition_by_iuv(context, index):
    # retrieve payment notice from context in order to execute the API call
    rpt_index = index
    payment_notices = context.flow_data['common']['payment_notices']

    # skipping this step if its execution is not required
    if rpt_index + 1 > len(payment_notices):
        session.set_skip_tests(context, True)
        return

    # retrieve data required for API call
    payment_notice = payment_notices[rpt_index]
    iuv = payment_notice['iuv']

    # initialize API call and get response
    base_url, subkey = router.get_rest_url(context, 'get_paymentposition_by_iuv')
    url = base_url.format(creditor_institution=payment_notice['domain_id'], iuv=iuv)
    headers = {'Content-Type': 'application/json', constants.OCP_APIM_SUBSCRIPTION_KEY: subkey}
    req_description = constants.REQ_DESCRIPTION_RETRIEVE_PAYMENT_POSITION.format(step=context.running_step, iuv=iuv)
    status_code, body_response, _ = utils.execute_request(url, 'get', headers, type=constants.ResponseType.JSON,
                                                          description=req_description)

    # update context setting all information about response
    context.flow_data['action']['response'][status_code] = status_code

    context.flow_data['action']['response']['body'] = body_response

    context.flow_data['action']['response']['content_type'] = constants.ResponseType.JSON

# @then('the response contains a single payment option')  # MODIFIED
def check_single_paymentoption(context):
    # skipping this step if its execution is not required
    if session.skip_tests(context):
        logging.debug('Skipping check_single_paymentoption step')
        return

    # retrieve information related to executed request
    response = context.flow_data['action']['response']['body']

    # executing assertions
    utils.assert_show_message('paymentOption' in response,
                              f"No field 'paymentOption' is defined for the retrieved payment position.")
    payment_options = utils.get_nested_field(response, 'paymentOption')
    utils.assert_show_message(len(payment_options) == 1,
                              f'There is not only one payment option in the payment position. Found number {len(payment_options)}.')

    # sorting transfer by transfer ID in order to avoid strange comparations
    transfers = payment_options[0]['transfer']
    transfers = sorted(transfers, key=lambda transfer: transfer['idTransfer'])
    payment_options[0]['transfer'] = transfers
    response['paymentOption'] = payment_options

    context.flow_data['action']['response']['body'] = response

# @then('the response contains the payment option correctly generated from {index} RPT')  # MODIFIED
def check_paymentoption_amounts(context, index):
    # skipping this step if its execution is not required
    if session.skip_tests(context):
        logging.debug('Skipping check_paymentoption_amounts step')
        return

    # retrieve response information related to executed request
    response = context.flow_data['action']['response']['body']

    rpt_index = index
    payment_options = utils.get_nested_field(response, 'paymentOption')
    payment_option = payment_options[0]

    # retrieve payment notices and raw RPT in order to execute checks on data
    payment_notices = context.flow_data['common']['payment_notices']

    payment_notice = payment_notices[rpt_index]
    rpts = context.flow_data['common']['rpts']

    rpt = [rpt for rpt in rpts if rpt['payment_data']['iuv'] == payment_notice['iuv']][0]
    payment_data = rpt['payment_data']

    # executing assertions
    # utils.assert_show_message(response['pull'] == False, f'The payment option must be not defined for pull payments.')
    utils.assert_show_message(int(payment_option['amount']) == round(payment_data['total_amount'] * 100),
                              f"The total amount calculated for {index} RPT is not equals to the one defined in GPD payment position. GPD's: [{int(payment_option['amount'])}], RPT's: [{round(payment_data['total_amount'] * 100)}]")
    utils.assert_show_message(payment_option['notificationFee'] == 0,
                              f'The notification fee in the {index} payment position defined for GPD must be always 0.')
    utils.assert_show_message(payment_option['isPartialPayment'] == False,
                              f'The payment option must be not defined as partial payment.')

# @then('the response contains the status in {status} for the payment option')  # MODIFIED
def check_paymentposition_status(context, status):
    # skipping this step if its execution is not required
    if session.skip_tests(context):
        logging.debug('Skipping check_paymentposition_status step')
        return

    # retrieve response information related to executed request
    response = context.flow_data['action']['response']['body']

    payment_options = utils.get_nested_field(response, 'paymentOption')
    payment_option = payment_options[0]

    # executing assertions
    utils.assert_show_message(payment_option['status'] == status,
                              f"The payment option must be equals to [{status}]. Current status: [{payment_option['status']}]")

# @then('the response contains the transfers correctly generated from RPT')  # MODIFIED
def check_paymentposition_transfers(context):
    # skipping this step if its execution is not required
    if session.skip_tests(context):
        logging.debug('Skipping check_paymentposition_transfers step')
        return

    # retrieve response information related to executed request
    response = context.flow_data['action']['response']['body']

    payment_options = utils.get_nested_field(response, 'paymentOption')
    transfers_from_po = payment_options[0]['transfer']

    # retrieve payment notices and raw RPT in order to execute checks on data
    raw_rpts = context.flow_data['common']['rpts']

    rpt = [rpt for rpt in raw_rpts if rpt['payment_data']['iuv'] == payment_options[0]['iuv']][0]
    transfers_from_rpt = rpt['payment_data']['transfers']

    # executing assertions
    utils.assert_show_message(len(transfers_from_po) == len(transfers_from_rpt),
                              f"There are not the same amount of transfers. GPD's: [{len(transfers_from_po)}], RPT's: [{len(transfers_from_rpt)}]")
    for transfer_index in range(len(transfers_from_po)):
        transfer_from_po = transfers_from_po[transfer_index]
        transfer_from_rpt = transfers_from_rpt[transfer_index]
        utils.assert_show_message(transfer_from_po['status'] == 'T_UNREPORTED',
                                  f"The status of the transfer {transfer_index} must be equals to [T_UNREPORTED]. Current status: [{transfer_from_po['status']}]")
        utils.assert_show_message(int(transfer_from_po['amount']) == round(transfer_from_rpt['amount'] * 100),
                                  f"The amount of the transfer {transfer_index} must be equals to the same defined in the payment position. GPD's: [{int(transfer_from_po['amount'])}], RPT's: [{round(transfer_from_rpt['amount'])}]")
        utils.assert_show_message(
            'transferMetadata' in transfer_from_po and len(transfer_from_po['transferMetadata']) > 0,
            f'There are not transfer metadata in transfer {transfer_index} but at least one is required.')
        utils.assert_show_message('stamp' in transfer_from_po or 'iban' in transfer_from_po,
                                  f'There are either IBAN and stamp definition in transfer {transfer_index} but they cannot be defined together.')
        if transfer_from_rpt['is_mbd'] == True:
            utils.assert_show_message('stamp' in transfer_from_po,
                                      f'There is not stamp definition in transfer {transfer_index} but RPT transfer require it.')
            utils.assert_show_message('hashDocument' in transfer_from_po['stamp'],
                                      f'There is not a valid hash for stamp in transfer {transfer_index}.')
            utils.assert_show_message('stampType' in transfer_from_po['stamp'],
                                      f'There is not a valid type for stamp in transfer {transfer_index}.')
            utils.assert_show_message(transfer_from_po['stamp']['hashDocument'] == transfer_from_rpt['stamp_hash'],
                                      f"The hash defined for the stamp in payment position in transfer {transfer_index} is not equals to the one defined in RPT. GPD's: [{transfer_from_po['stamp']['hashDocument']}], RPT's: [{transfer_from_rpt['stamp_hash']}]")
            utils.assert_show_message(transfer_from_po['stamp']['stampType'] == transfer_from_rpt['stamp_type'],
                                      f"The type defined for the stamp in payment position in transfer {transfer_index} is not equals to the one defined in RPT. GPD's: [{transfer_from_po['stamp']['stampType']}], RPT's: [{transfer_from_rpt['stamp_type']}]")
        else:
            utils.assert_show_message('iban' in transfer_from_po,
                                      f'There is not IBAN definition in transfer {transfer_index} but RPT transfer require it.')
            utils.assert_show_message(transfer_from_po['iban'] == transfer_from_rpt['creditor_iban'],
                                      f"The IBAN defined in transfer {transfer_index} is not equals to the one defined in RPT. GPD's: [{transfer_from_po['iban']}], RPT's: [{transfer_from_rpt['creditor_iban']}]")

# @then('the {actor} receives an HTML page with an error')
def check_html_error_page(context, actor):
    # retrieve response body related to executed request
    response = context.flow_data['action']['response']['body']


    # executing assertions
    utils.assert_show_message('<!DOCTYPE html>' in response, f'The response is not an HTML page')
    utils.assert_show_message('Si &egrave; verificato un errore imprevisto' in response,
                              f'The HTML page does not contains an error message.')

# @given('a valid nodoInviaRPT request')
def generate_nodoinviarpt(context):
    session.set_skip_tests(context, False)

    # retrieve test_data in order to generate flow_data session data
    test_data = context.commondata
    # generate nodoInviaRPT request from raw RPT
    raw_rpts = context.flow_data['common']['rpts']
    request = requestgen.generate_nodoinviarpt(test_data, raw_rpts[0], context.secrets.STATION_PASSWORD)

    # update context with request and edit flow_data
    context.flow_data['action']['request']['body'] = request


######################################
def exec_nm1_to_nmu(context, actor):
    get_valid_sessionid(context)
    send_sessionid_to_wispdismantling(context)
    check_status_code(context, actor, '302')
    check_checkout_url(context)

def retrieve_related_notice_numbers_from_redirect(context):
    wait_for_n_seconds(context, '2', 'to wait for Nodo to write RE events')
    get_iuv_from_session(context, 'first')
    search_in_re_by_iuv(context)
    check_status_code(context, 'user', '200')
    retrieve_payment_notice_from_re_event(context)

def send_checkposition_request(context):
    generate_checkposition(context)
    send_primitive(context, 'creditor institution', 'checkPosition')
    check_status_code(context, 'creditor institution', '200')
    check_field(context, 'outcome', 'OK')
    check_field_as_not_empty_list(context, 'positionslist')

def send_index_activatePaymentNoticeV2_request(context, index):

    for i in range(index):
        generate_activatepaymentnotice(context, i)
        send_primitive(context, 'creditor istitution', 'activatePaymentNoticeV2')
        check_status_code(context, 'creditor istitution', '200')
        check_field(context, 'outcome', 'OK')
        check_field_with_non_null_value(context, 'paymentToken')
        retrieve_payment_token_from_activatepaymentnotice(context, i)


def check_wisp_session_timers(context):
    wait_for_n_seconds(context, '5', 'to wait for Nodo to write RE events')
    search_in_re_by_iuv(context)
    check_status_code(context, 'user', '200')
    check_event(context, 'timer-set', 'operationStatus', 'Success')
    check_event_token_relation(context)

def send_closePaymentV2_request(context):
    generate_closepayment(context, 'OK')
    send_primitive(context, 'creditor istitution','closePaymentV2')
    check_status_code(context, 'creditor istitution', '200')
    check_field(context, 'outcome', 'OK')

def check_wisp_session_timers_del_and_rts_were_sent(context):
    wait_for_n_seconds(context, '10', 'to wait for Nodo to write RE events')
    get_iuvs_from_session(context)
    search_in_re_by_iuv(context)
    check_status_code(context, 'user', '200')
    check_event(context, 'timer-delete', 'status', 'RECEIPT_TIMER_GENERATION_DELETED_SCHEDULED_SEND')
    check_event_token_relation(context)
    check_event(context, 'receipt-ok','status','RT_SEND_SUCCESS')
    check_event_notice_number_relation(context)

def check_index_paid_payment_positions(context, index):

    for i in range(index):
        search_paymentposition_by_iuv(context, i)
        check_status_code(context, 'user', '200')
        check_field(context, 'status', 'PAID')
        check_single_paymentoption(context)
        check_paymentoption_amounts(context, i)
        check_paymentposition_status(context, 'PO_PAID')
        check_paymentposition_transfers(context)


def check_existing_debt_position_usage(context):
    wait_for_n_seconds(context, '2', 'to wait for Nodo to write RE events')
    get_iuv_from_session(context, 'first')
    search_in_re_by_iuv(context)
    check_status_code(context, 'user', '200')
    check_event(context, 'redirect', 'status', 'UPDATED_EXISTING_PAYMENT_POSITION_IN_GPD')

def check_fail_nm1_to_nmu_conversion(context):
    get_valid_sessionid(context)
    send_sessionid_to_wispdismantling(context)
    check_status_code(context, 'user', '200')
    check_html_error_page(context, 'user')

def check_debt_position_invalid_and_sent_ko_receipt(context):
    wait_for_n_seconds(context, '2', 'to wait for Nodo to write RE events')
    get_iuv_from_session(context, 'first')
    search_in_re_by_iuv(context)
    check_status_code(context, 'user', '200')
    check_event(context, 'redirect', 'operationErrorCode', 'WIC-1205')
    check_event(context, 'redirect', 'status', 'RT_SEND_SUCCESS')











