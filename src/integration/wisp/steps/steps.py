import session as session
from behave import *

import src.integration.utility.wisp.request_generator as requestgen
import src.integration.utility.wisp.steps_utils as steputils
from src.integration.utility.wisp import constants
from src.integration.utility.wisp import routes as router
from src.integration.utility.wisp import utils


@given(
    'una singola RPT di tipo {payment_type} con {number_of_transfers} versamenti di cui {number_of_stamps} sono marche da bollo')
@when('una singola RPT di tipo {payment_type} con {number_of_transfers} versamenti di cui {number_of_stamps} sono marche da bollo')
def generate_single_rpt(context, payment_type, number_of_transfers, number_of_stamps):
    session.set_skip_tests(context, False)
    if number_of_stamps == 'none':
        number_of_stamps = '0'

    context.payment_type = payment_type
    # forza la definizione dello IUV se la RPT fa parte di un carrello multibeneficiario
    iuv = None

    is_multibeneficiary_cart = context.flow_data['common']['cart']['is_multibeneficiary']

    if is_multibeneficiary_cart is not None and is_multibeneficiary_cart == True:
        iuv = context.flow_data['common']['cart']['iuv_for_multibeneficiary']

    # forza la definizione del CCP se la RPT fa parte di un carrello multibeneficiario
    ccp = None
    if is_multibeneficiary_cart:
        ccp = context.flow_data['common']['cart']['id']
    test_data = context.commondata

    domain_id = test_data['creditor_institution']

    payee_institution = test_data['payee_institutions_1']

    # imposta l'istituzione pagante corretta se deve essere creata una RPT non-prima del carrello multibeneficiario
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

    # genera la RPT grezza che sarà usata per costruire il contenuto XML
    rpt = requestgen.create_rpt(test_data, iuv, ccp, domain_id, payee_institution, payment_type,
                                int(number_of_transfers), int(number_of_stamps))

    # aggiorna la lista delle RPT grezze generate
    rpts.append(rpt)

    context.flow_data['common']['rpts'] = rpts


@then('the same cart is used for another try')
def update_old_nodoInviaCarrelloRPT_request(context):
    # modifica l'identificatore del carrello alterando l'ultimo carattere
    cart_id = context.flow_data['common']['cart']['id']

    # session.set_flow_data(context, constants.SESSION_DATA_CART_ID, utils.change_last_numeric_char(cart_id))
    context.flow_data['common']['cart']['id'] = utils.change_last_numeric_char(cart_id)

    # modifica il contenuto di tutti i CCP alterando l'ultimo carattere
    rpts = context.flow_data['common']['rpts']

    for rpt in rpts:
        ccp = rpt['payment_data']['ccp']
        rpt['payment_data']['ccp'] = utils.change_last_numeric_char(ccp)

    # aggiorna il contesto con la richiesta e modifica il flow_data
    context.flow_data['common']['rpts'] = rpts


@given(
    'una posizione debitoria esistente relativa alla {index} RPT con segregation code uguale a {segregation_code} e stato uguale a {payment_status}')
def generate_payment_position(context, index, segregation_code, payment_status):
    session.set_skip_tests(context, False)

    # recupera la RPT corretta dal contesto per generare una posizione debitoria a partire da essa
    raw_rpts = context.flow_data['common']['rpts']

    payment_notice_index = utils.get_index_from_cardinal(index)
    rpt = raw_rpts[payment_notice_index]

    # genera la posizione debitoria dalla RPT estratta
    payment_positions = requestgen.generate_gpd_paymentposition(context, rpt, segregation_code, payment_status)

    # se payment_status è VALID, l'URL recuperato conterrà il flag toPublish impostato a true
    if payment_status == 'VALID':
        base_url, subkey = router.get_rest_url(context, 'create_paymentposition_and_publish')

    # se payment_status non è VALID, l'URL recuperato conterrà il flag toPublish impostato a false
    else:
        base_url, subkey = router.get_rest_url(context, 'create_paymentposition')

    # inizializza la chiamata API e ottiene la risposta
    url = base_url.format(creditor_institution=rpt['domain']['id'])

    headers = {'Content-Type': 'application/json', constants.OCP_APIM_SUBSCRIPTION_KEY: subkey}

    req_description = constants.REQ_DESCRIPTION_CREATE_PAYMENT_POSITION.format(step=context.running_step)

    status_code, body, _ = utils.execute_request(url, 'post', headers, payment_positions,
                                                 type=constants.ResponseType.JSON,
                                                 description=req_description)
    # esecuzione delle asserzioni
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


@given('un carrello di RPT {note}')
def generate_empty_cart(context, note):
    """Generate an empty cart and set multibeneficiary flags based on step note."""
    # recupera i test_data per generare i dati di sessione flow_data
    test_data = context.commondata

    # imposta le informazioni sulla primitiva di trigger
    context.flow_data['action']['trigger_primitive']['name'] = constants.PRIMITIVE_NODOINVIACARRELLORPT

    normalized_note = ' '.join(note.lower().replace('-', ' ').split())
    is_multibeneficiary_note = normalized_note in (
        'for multibeneficiary',
        'multibeneficiary',
        'multi beneficiario',
    )

    # genera l'identificatore del carrello e definisce le info sul carrello multibeneficiario nel flow_data
    if is_multibeneficiary_note:
        iuv = utils.generate_iuv(in_18digit_format=True)

        context.flow_data['common']['cart']['id'] = utils.generate_cart_id(iuv, test_data['creditor_institution'])

        context.flow_data['common']['cart']['is_multibeneficiary'] = True

        context.flow_data['common']['cart']['iuv_for_multibeneficiary'] = iuv

    # genera l'identificatore del carrello e imposta le info multibeneficiario a False nel flow_data
    else:
        context.flow_data['common']['cart']['id'] = utils.generate_cart_id(None, test_data['creditor_institution'])

        context.flow_data['common']['cart']['is_multibeneficiary'] = False


@when("l'{actor} tenta di pagare la RPT sul sito dell'EC")
@given("l'{actor} tenta di pagare la RPT sul sito dell'EC")
def user_tries_to_pay_RPT(context, actor):
    steputils.generate_nodoinviarpt(context)
    steputils.send_primitive(context, actor, 'nodoInviaRPT')
    steputils.check_status_code(context, actor, '200')
    steputils.check_field(context, 'esito', 'OK')

    if context.payment_type == 'BBT':
        steputils.check_redirect_url(context, 'redirect')


@when("l'{actor} tenta di pagare la RPT sul sito dell'EC ma il pagamento fallisce")
def user_fail_to_pay_RPT(context, actor):
    steputils.generate_nodoinviarpt(context)
    steputils.send_primitive(context, actor, 'nodoInviaRPT')
    steputils.check_status_code(context, actor, '200')
    steputils.check_field(context, 'esito', 'KO')
    if context.payment_type == 'BBT':
        steputils.check_redirect_url(context, 'redirect')


@then(u"l'{actor} ha tentato di pagare la RPT sul sito dell'EC")
@when(u"l'{actor} ha tentato di pagare la RPT sul sito dell'EC")
@given(u"l'{actor} ha tentato di pagare la RPT sul sito dell'EC")
def user_tried_to_pay_RPT(context, actor):
    user_tries_to_pay_RPT(context, actor)
    nm1_to_nmu_succeeds(context)
    retrieve_notice_numbers_from_redirect(context)
    checkposition_request(context)


@then("l'{actor} viene reindirizzato su Checkout completando il pagamento")
def user_redirected_to_checkout(context, actor):
    steputils.exec_nm1_to_nmu(context, actor)
    steputils.retrieve_related_notice_numbers_from_redirect(context)
    steputils.send_checkposition_request(context)
    steputils.send_index_activatePaymentNoticeV2_request(context, 5)
    steputils.check_wisp_session_timers(context)
    steputils.send_closePaymentV2_request(context)
    steputils.check_wisp_session_timers_del_and_rts_were_sent(context)
    steputils.check_index_paid_payment_positions(context, 5)


@then("l'{actor} viene reindirizzato nuovamente su Checkout completando il pagamento")
def user_redirected_again_to_checkout(context, actor):
    steputils.exec_nm1_to_nmu(context, actor, expected_status='200')
    steputils.retrieve_related_notice_numbers_from_redirect(context)
    steputils.send_checkposition_request(context)
    steputils.send_index_activatePaymentNoticeV2_request(context, 5)
    steputils.check_wisp_session_timers(context)
    steputils.send_closePaymentV2_request(context)
    steputils.check_wisp_session_timers_del_and_rts_were_sent(context)
    steputils.check_index_paid_payment_positions(context, 5)


@then("l'{actor} viene reindirizzato su Checkout completando il pagamento multi-beneficiario")
@then("l'{actor} viene reindirizzato su Checkout completando il pagamento multibeneficiario")
def user_redirected_to_checkout(context, actor):
    steputils.exec_nm1_to_nmu(context, actor)
    steputils.retrieve_related_notice_numbers_from_redirect(context)
    steputils.send_checkposition_request(context)
    steputils.send_index_activatePaymentNoticeV2_request(context, 5)
    steputils.check_wisp_session_timers(context)
    steputils.send_closePaymentV2_request(context)
    steputils.check_wisp_session_timers_del_and_rts_were_sent(context)
    steputils.check_paid_payment_position_from_multibeneficiary_cart(context)


@then("l'{actor} viene reindirizzato su Checkout senza completare il pagamento multi-beneficiario")
@given("l'{actor} viene reindirizzato su Checkout senza completare il pagamento multi-beneficiario")
@then("l'{actor} viene reindirizzato su Checkout senza completare il pagamento multibeneficiario")
@given("l'{actor} viene reindirizzato su Checkout senza completare il pagamento multibeneficiario")
def user_redirected_to_checkout(context, actor):
    steputils.exec_nm1_to_nmu(context, actor)
    steputils.retrieve_related_notice_numbers_from_redirect(context)
    steputils.send_checkposition_request(context)
    steputils.send_index_activatePaymentNoticeV2_request(context, 5)
    steputils.check_wisp_session_timers(context)
    steputils.send_KO_closePaymentV2_request(context)
    steputils.check_wisp_session_timers_del_and_rts_were_sent_receipt_ko(context)


@then('la posizione debitoria è chiusa')
def payment_done_check(context):
    steputils.check_existing_debt_position_usage(context)


@then('la conversione al nuovo modello fallisce nel wisp-converter')
def nm1_to_nmu_fails(context):
    steputils.check_fail_nm1_to_nmu_conversion(context)


@then('la ricevuta KO è inviata')
def debt_position_invalid(context):
    steputils.check_debt_position_invalid_and_sent_ko_receipt(context)


@when("l'utente invia una richiesta nodoInviaRPT")
def check_successful_response_with_old_wisp_url(context):
    steputils.generate_nodoinviarpt(context)
    steputils.send_primitive(context, 'user', 'nodoInviaRPT')


@then("l'utente riceve una risposta con esito positivo")
def check_esito_response(context):
    steputils.check_status_code(context, 'user', '200')
    steputils.check_field(context, 'esito', 'OK')


@then('la risposta contiene il vecchio URL WISP')
def check_old_wisp_url(context):
    steputils.check_redirect_url(context, 'old WISP')


@then('la conversione al nuovo modello ha successo nel wisp-converter')
def nm1_to_nmu_succeeds(context):
    steputils.exec_nm1_to_nmu(context, 'user')


@then('the notice numbers are retrieved from redirect')
def retrieve_notice_numbers_from_redirect(context):
    steputils.retrieve_related_notice_numbers_from_redirect(context)


@then('the checkPosition request was successful')
def checkposition_request(context):
    steputils.send_checkposition_request(context)


@given(u'vengono inviate le richieste activatePaymentNoticeV2')
@when(u'vengono inviate le richieste activatePaymentNoticeV2')
def send_activatePaymentNoticeV2_request(context):
    steputils.send_index_activatePaymentNoticeV2_request(context, 5)


@then(u"il pagamento fallisce {error_notes} e viene restituito l'errore {error_value}")
def check_faultcode_with_notes(context, error_notes, error_value):
    steputils.check_field(context, 'faultCode', error_value)


@when(u"l'{actor} tenta di pagare il carrello di RPT sul sito dell'EC")
@given(u"l'{actor} tenta di pagare il carrello di RPT sul sito dell'EC")
def user_tried_to_pay_RPT_with_cart(context, actor):
    steputils.generate_nodoinviacarrellorpt(context, 'for WISP channel')
    steputils.send_primitive(context, actor, 'nodoInviaCarrelloRPT')
    steputils.check_status_code(context, actor, '200')
    steputils.check_field(context, 'esitoComplessivoOperazione', 'OK')
    steputils.check_redirect_url(context, 'redirect')


@when(u"l'{actor} tenta di pagare il carrello di RPT sul sito dell'EC senza verifica dell'URL di redirect")
def user_tried_to_pay_RPT_with_cart(context, actor):
    steputils.generate_nodoinviacarrellorpt(context, 'for WISP channel')
    steputils.send_primitive(context, actor, 'nodoInviaCarrelloRPT')
    steputils.check_status_code(context, actor, '200')
    steputils.check_field(context, 'esitoComplessivoOperazione', 'OK')


@when('il tentativo di pagamento fallisce')
def fails_trying_to_pay(context):
    steputils.check_field(context, 'esitoComplessivoOperazione', 'KO')


@then(u'la risposta contiene il campo {field_name} con valore {field_value}')
@when(u'la risposta contiene il campo {field_name} con valore {field_value}')
def check_field(context, field_name, field_value):
    steputils.check_field(context, field_name, field_value)


@then('the response contains the {url_type} URL')
def check_redirect_url(context, url_type):
    steputils.check_redirect_url(context, url_type)
