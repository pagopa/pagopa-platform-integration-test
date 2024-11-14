import logging
import time

import request_generator as requestgen
import session as session
from allure_commons._allure import attach
from behave import *

from src.utility import constants
from src.utility import routes as router
from src.utility import utils
import src.utility.steps_utils as steputils

@given('a single RPT of type {payment_type} with {number_of_transfers} transfers of which {number_of_stamps} are stamps')
@when('a single RPT of type {payment_type} with {number_of_transfers} transfers of which {number_of_stamps} are stamps')
def generate_single_rpt(context, payment_type, number_of_transfers, number_of_stamps):
    session.set_skip_tests(context, False)
    if number_of_stamps == 'none':
        number_of_stamps = '0'

    context.payment_type = payment_type
    # force IUV definition if the RPT is part of multibeneficiary cart
    iuv = None

    is_multibeneficiary_cart = context.flow_data['common']['cart']['is_multibeneficiary']

    if is_multibeneficiary_cart is not None and is_multibeneficiary_cart == True:
        iuv = context.flow_data['common']['cart']['iuv_for_multibeneficiary']

    # force CCP definition if the RPT is part of multibeneficiary cart
    ccp = None
    if is_multibeneficiary_cart:
        ccp = context.flow_data['common']['cart']['id']
    test_data = context.commondata

    domain_id = test_data['creditor_institution']

    payee_institution = test_data['payee_institutions_1']

    # set valid payee institution if non-first RPT of multibeneficiary cart must be created
    rpts = context.flow_data['common']['rpts']

    if is_multibeneficiary_cart:
        if len(rpts) == 1:
            other_payee_institution = test_data['payee_institutions_2']
            domain_id = other_payee_institution['fiscal_code']
            payee_institution = other_payee_institution
        elif len(rpts) == 2:
            other_payee_institution = test_data['payee_institutions_3']
            domain_id = other_payee_institution['fiscal_code']
            payee_institution = other_payee_institution

    # generate raw RPT that will be used for construct XML content
    rpt = requestgen.create_rpt(test_data, iuv, ccp, domain_id, payee_institution, payment_type,
                                int(number_of_transfers), int(number_of_stamps))

    # update the list of generated raw RPTs
    rpts.append(rpt)

    context.flow_data['common']['rpts'] = rpts

@given('the same nodoInviaCarrelloRPT for another try')
def update_old_nodoInviaCarrelloRPT_request(context):
    # change cart identifier editing last char value
    cart_id = context.flow_data['common']['cart']['id']

    # session.set_flow_data(context, constants.SESSION_DATA_CART_ID, utils.change_last_numeric_char(cart_id))
    context.flow_data['common']['cart']['id'] = utils.change_last_numeric_char(cart_id)


    # change all CCPs content editing last char value
    rpts = context.flow_data['common']['rpts']

    for rpt in rpts:
        ccp = rpt['payment_data']['ccp']
        rpt['payment_data']['ccp'] = utils.change_last_numeric_char(ccp)

    # update context with request and edit flow_data
    context.flow_data['common']['rpts'] = rpts

@given('an existing payment position related to {index} RPT with segregation code equals to {segregation_code} and state equals to {payment_status}')
def generate_payment_position(context, index, segregation_code, payment_status):
    session.set_skip_tests(context, False)

    # retrieve correct RPT from context in order to generate a payment position from it
    raw_rpts = context.flow_data['common']['rpts']

    payment_notice_index = utils.get_index_from_cardinal(index)
    rpt = raw_rpts[payment_notice_index]

    # generate payment position from extracted RPT
    payment_positions = requestgen.generate_gpd_paymentposition(context, rpt, segregation_code, payment_status)

    # if payment_status is VALID, the retrieved URL will contains toPublish flag set as true
    if payment_status == 'VALID':
        base_url, subkey = router.get_rest_url(context, 'create_paymentposition_and_publish')

    # if payment_status is not VALID, the retrieved URL will contains toPublish flag set as false
    else:
        base_url, subkey = router.get_rest_url(context, 'create_paymentposition')

    # initialize API call and get response
    url = base_url.format(creditor_institution=rpt['domain']['id'])

    headers = {'Content-Type': 'application/json', constants.OCP_APIM_SUBSCRIPTION_KEY: subkey}

    req_description = constants.REQ_DESCRIPTION_CREATE_PAYMENT_POSITION.format(step=context.running_step)

    status_code, body, _ = utils.execute_request(url, 'post', headers, payment_positions,
                                                 type=constants.ResponseType.JSON,
                                                 description=req_description)
    # executing assertions
    utils.assert_show_message(status_code == 201,
                              f'The debt position for RPT with index [{index}] was not created. Expected status code [201], Current status code [{status_code}]')


@step('the execution of "{scenario_name}" was successful')
def step_impl(context, scenario_name):
    all_scenarios = [scenario
                     for feature in context._runner.features
                     for scenario in feature.walk_scenarios()]

    phase = ([scenario for scenario in all_scenarios if scenario_name in scenario.name] or [None])[0]

    text_step = ''.join(
        [step.keyword + ' ' + step.name + "\n\"\"\"\n" + (step.text or '') + "\n\"\"\"\n" for step in phase.steps])
    context.execute_steps(text_step)

@given('a cart of RPTs {note}')
def generate_empty_cart(context, note):
    # retrieve test_data in order to generate flow_data session data
    test_data = context.commondata

    # set trigger primitive information
    context.flow_data['action']['trigger_primitive']['name'] = constants.PRIMITIVE_NODOINVIACARRELLORPT



    # generate cart identifier and defining info about multibeneficiary cart on flow_data
    if 'for multibeneficiary' in note:
        iuv = utils.generate_iuv(in_18digit_format=True)

        context.flow_data['common']['cart']['id'] = utils.generate_cart_id(iuv, test_data['creditor_institution'])


        context.flow_data['common']['cart']['is_multibeneficiary'] = True


        context.flow_data['common']['cart']['iuv_for_multibeneficiary'] = iuv

    # generate cart identifier and set multibeneficiary info to False on flow_data
    else:
        context.flow_data['common']['cart']['id'] = utils.generate_cart_id(None, test_data['creditor_institution'])


        context.flow_data['common']['cart']['is_multibeneficiary'] = False


@when('the {actor} tries to pay the RPT on EC website')
def user_tries_to_pay_RPT(context, actor):
    steputils.generate_nodoinviarpt(context)
    steputils.send_primitive(context, actor, 'nodoInviaRPT' )
    steputils.check_status_code(context, actor, '200')
    steputils.check_field(context, 'esito', 'OK')

    if context.payment_type == 'BBT':
        steputils.check_redirect_url(context, 'redirect')


@when('the {actor} tries to pay the RPT on EC website but fails')
def user_fail_to_pay_RPT(context, actor):
    steputils.generate_nodoinviarpt(context)
    steputils.send_primitive(context, actor, 'nodoInviaRPT')
    steputils.check_status_code(context, actor, '200')
    steputils.check_field(context, 'esito', 'KO')
    if context.payment_type == 'BBT':
        steputils.check_redirect_url(context, 'redirect')

@then(u'the {actor} tried to pay the RPT on EC website')
def user_tried_to_pay_RPT(context, actor):
    user_tries_to_pay_RPT(context, actor)
    nm1_to_nmu_succeeds(context)
    retrieve_notice_numbers_from_redirect(context)
    checkposition_request(context)

@then('the {actor} is redirected on Checkout completing the payment')
def user_redirected_to_checkout(context, actor):
    steputils.exec_nm1_to_nmu(context, actor)
    steputils.retrieve_related_notice_numbers_from_redirect(context)
    steputils.send_checkposition_request(context)
    steputils.send_index_activatePaymentNoticeV2_request(context, 5)
    steputils.check_wisp_session_timers(context)
    steputils.send_closePaymentV2_request(context)
    steputils.check_wisp_session_timers_del_and_rts_were_sent(context)
    steputils.check_index_paid_payment_positions(context, 5)

@then('the {actor} is redirected on Checkout completing the multibeneficiary payment')
def user_redirected_to_checkout(context, actor):
    steputils.exec_nm1_to_nmu(context, actor)
    steputils.retrieve_related_notice_numbers_from_redirect(context)
    steputils.send_checkposition_request(context)
    steputils.send_index_activatePaymentNoticeV2_request(context, 5)
    steputils.check_wisp_session_timers(context)
    steputils.send_closePaymentV2_request(context)
    steputils.check_wisp_session_timers_del_and_rts_were_sent(context)
    steputils.check_paid_payment_position_from_multibeneficiary_cart(context)

@then('the {actor} is redirected on Checkout not completing the multibeneficiary payment')
def user_redirected_to_checkout(context, actor):
    steputils.exec_nm1_to_nmu(context, actor)
    steputils.retrieve_related_notice_numbers_from_redirect(context)
    steputils.send_checkposition_request(context)
    steputils.send_index_activatePaymentNoticeV2_request(context, 5)
    steputils.check_wisp_session_timers(context)
    steputils.send_KO_closePaymentV2_request(context)
    steputils.check_wisp_session_timers_del_and_rts_were_sent_receipt_ko(context)

@then('the debt position was closed')
def payment_done_check(context):
    steputils.check_existing_debt_position_usage(context)

@then('conversion to new model fails in wisp-converter')
def nm1_to_nmu_fails(context):
    steputils.check_fail_nm1_to_nmu_conversion(context)

@then('the KO receipt was sent')
def debt_position_invalid(context):
    steputils.check_debt_position_invalid_and_sent_ko_receipt(context)

@when('the user sends a nodoInviaRPT request')
def check_successful_response_with_old_wisp_url(context):
    steputils.generate_nodoinviarpt(context)
    steputils.send_primitive(context, 'user', 'nodoInviaRPT')

@then('the user receives a successful response')
def check_esito_response(context):
    steputils.check_status_code(context, 'user','200')
    steputils.check_field(context, 'esito', 'OK')

@then('the response contains the old WISP URL')
def check_old_wisp_url(context):
    steputils.check_redirect_url(context, 'old WISP')

@then('the conversion to new model succeeds in wisp-converter')
def nm1_to_nmu_succeeds(context):
    steputils.exec_nm1_to_nmu(context, 'user')

@then('the notice numbers are retrieved from redirect')
def retrieve_notice_numbers_from_redirect(context):
    steputils.retrieve_related_notice_numbers_from_redirect(context)

@then('the checkPosition request was successful')
def checkposition_request(context):
    steputils.send_checkposition_request(context)

@given(u'send activatePaymentNoticeV2 requests')
def send_activatePaymentNoticeV2_request(context):
    steputils.send_index_activatePaymentNoticeV2_request(context, 5)

@then(u'the response contains the field faultCode with value PPT_SEMANTICA')
def check_faultcode_ppt_semantica(context):
    steputils.check_field(context, 'faultCode', 'PPT_SEMANTICA')

@when(u'the {actor} tries to pay a cart of RPTs on EC website')
def user_tried_to_pay_RPT_with_cart(context, actor):
    steputils.generate_nodoinviacarrellorpt(context, 'for WISP channel')
    steputils.send_primitive(context, actor, 'nodoInviaCarrelloRPT')
    steputils.check_status_code(context, actor, '200')
    steputils.check_field(context, 'esitoComplessivoOperazione', 'OK')
    steputils.check_redirect_url(context, 'redirect')

@when(u'the {actor} tries to pay a cart of RPTs on EC website but fails having the field value {field_value}')
@then(u'the {actor} tries to pay a cart of RPTs on EC website but fails having the field value {field_value}')
def user_tried_to_pay_RPT_with_cart(context, actor, field_value):
    steputils.generate_nodoinviacarrellorpt(context, 'for WISP channel')
    steputils.send_primitive(context, actor, 'nodoInviaCarrelloRPT')
    steputils.check_status_code(context, actor, '200')
    steputils.check_field(context, 'esitoComplessivoOperazione', 'KO')
    steputils.check_field(context, 'faultCode', field_value)


@then(u'the response contains the field {field_name} with value {field_value}')
def check_field(context, field_name, field_value):
   steputils.check_field(context, field_name, field_value)

@then('the response contains the {url_type} URL')
def check_redirect_url(context, url_type):
    steputils.check_redirect_url(context,url_type)
