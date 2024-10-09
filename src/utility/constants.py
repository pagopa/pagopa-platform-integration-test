from enum import Enum

NODOINVIARPT_STRUCTURE = """<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ppt="http://ws.pagamenti.telematici.gov/ppthead" xmlns:ws="http://ws.pagamenti.telematici.gov/">
    <soapenv:Header>
        <ppt:intestazionePPT>
            <identificativoIntermediarioPA>{creditor_institution_broker}</identificativoIntermediarioPA>
            <identificativoStazioneIntermediarioPA>{station}</identificativoStazioneIntermediarioPA>
            <identificativoDominio>{creditor_institution}</identificativoDominio>
            <identificativoUnivocoVersamento>{iuv}</identificativoUnivocoVersamento>
            <codiceContestoPagamento>{ccp}</codiceContestoPagamento>
        </ppt:intestazionePPT>
    </soapenv:Header>
    <soapenv:Body>
        <ws:nodoInviaRPT>
            <password>{password}</password>
            <identificativoPSP>{psp}</identificativoPSP>
            <identificativoIntermediarioPSP>{psp_broker}</identificativoIntermediarioPSP>
            <identificativoCanale>{channel}</identificativoCanale>
            <tipoFirma></tipoFirma>
            <rpt>{rpt}</rpt>
        </ws:nodoInviaRPT>
    </soapenv:Body>
</soapenv:Envelope>""";

NODOINVIACARRELLORPT_STRUCTURE = """<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <soapenv:Header>
    <ns1:intestazioneCarrelloPPT xmlns:ns1="http://ws.pagamenti.telematici.gov/ppthead">
      <identificativoIntermediarioPA>{creditor_institution_broker}</identificativoIntermediarioPA>
      <identificativoStazioneIntermediarioPA>{station}</identificativoStazioneIntermediarioPA>
      <identificativoCarrello>{cart_id}</identificativoCarrello>
    </ns1:intestazioneCarrelloPPT>
  </soapenv:Header>
  <soapenv:Body>
    <nodoInviaCarrelloRPT xmlns="http://ws.pagamenti.telematici.gov/">
      <password xmlns="">{password}</password>
      <identificativoPSP xmlns="">{psp}</identificativoPSP>
      <identificativoIntermediarioPSP xmlns="">{psp_broker}</identificativoIntermediarioPSP>
      <identificativoCanale xmlns="">{channel}</identificativoCanale>
      <listaRPT xmlns="">
        {rpt_list}
      </listaRPT>
      <multiBeneficiario xmlns="">{is_multibeneficiary}</multiBeneficiario>
    </nodoInviaCarrelloRPT>
  </soapenv:Body>
</soapenv:Envelope>""";

RPT_STRUCTURE = """<pay_i:RPT xmlns:pay_i="http://www.digitpa.gov.it/schemas/2011/Pagamenti/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.digitpa.gov.it/schemas/2011/Pagamenti/ PagInf_RPT_RT_6_2_0.xsd ">
    <pay_i:versioneOggetto>6.0</pay_i:versioneOggetto>
    <pay_i:dominio>
        <pay_i:identificativoDominio>{creditor_institution}</pay_i:identificativoDominio>
        <pay_i:identificativoStazioneRichiedente>{station}</pay_i:identificativoStazioneRichiedente>
    </pay_i:dominio>
    <pay_i:identificativoMessaggioRichiesta>integrationtestreq</pay_i:identificativoMessaggioRichiesta>
    <pay_i:dataOraMessaggioRichiesta>{current_date_time}</pay_i:dataOraMessaggioRichiesta>
    <pay_i:autenticazioneSoggetto>CNS</pay_i:autenticazioneSoggetto>
    {payer_delegate}
    {payer}
    {payee_institution}
    {payment}
</pay_i:RPT>""";

SINGLE_RPT_IN_CART = """<elementoListaRPT>
            <identificativoDominio>{creditor_institution}</identificativoDominio>
            <identificativoUnivocoVersamento>{iuv}</identificativoUnivocoVersamento>
            <codiceContestoPagamento>{ccp}</codiceContestoPagamento>
            <tipoFirma></tipoFirma>
            <rpt>{rpt}</rpt>
        </elementoListaRPT>
"""

# All injected data refers to 'payer' sublevel
RPT_PAYER_STRUCTURE = """<pay_i:soggettoPagatore>
        <pay_i:identificativoUnivocoPagatore>
            <pay_i:tipoIdentificativoUnivoco>{payer_type}</pay_i:tipoIdentificativoUnivoco>
            <pay_i:codiceIdentificativoUnivoco>{payer_fiscal_code}</pay_i:codiceIdentificativoUnivoco>
        </pay_i:identificativoUnivocoPagatore>
        <pay_i:anagraficaPagatore>{payer_name}</pay_i:anagraficaPagatore>
        <pay_i:indirizzoPagatore>{payer_address}</pay_i:indirizzoPagatore>
        <pay_i:civicoPagatore>{payer_address_number}</pay_i:civicoPagatore>
        <pay_i:capPagatore>{payer_address_zipcode}</pay_i:capPagatore>
        <pay_i:localitaPagatore>{payer_address_location}</pay_i:localitaPagatore>
        <pay_i:provinciaPagatore>{payer_address_province}</pay_i:provinciaPagatore>
        <pay_i:nazionePagatore>{payer_address_nation}</pay_i:nazionePagatore>
        <pay_i:e-mailPagatore>{payer_email}</pay_i:e-mailPagatore>
	</pay_i:soggettoPagatore>""";

# All injected data refers to 'payer_delegate' sublevel
RPT_PAYERDELEGATE_STRUCTURE = """<pay_i:soggettoVersante>
        <pay_i:identificativoUnivocoVersante>
            <pay_i:tipoIdentificativoUnivoco>{payer_delegate_type}</pay_i:tipoIdentificativoUnivoco>
            <pay_i:codiceIdentificativoUnivoco>{payer_delegate_fiscal_code}</pay_i:codiceIdentificativoUnivoco>
        </pay_i:identificativoUnivocoVersante>
        <pay_i:anagraficaVersante>{payer_delegate_name}</pay_i:anagraficaVersante>
        <pay_i:indirizzoVersante>{payer_delegate_address}</pay_i:indirizzoVersante>
        <pay_i:civicoVersante>{payer_delegate_address_number}</pay_i:civicoVersante>
        <pay_i:capVersante>{payer_delegate_address_zipcode}</pay_i:capVersante>
        <pay_i:localitaVersante>{payer_delegate_address_location}</pay_i:localitaVersante>
        <pay_i:provinciaVersante>{payer_delegate_address_province}</pay_i:provinciaVersante>
        <pay_i:nazioneVersante>{payer_delegate_address_nation}</pay_i:nazioneVersante>
        <pay_i:e-mailVersante>{payer_delegate_email}</pay_i:e-mailVersante>
    </pay_i:soggettoVersante>""";

# All injected data refers to 'payee_institution' sublevel
RPT_PAYEEINSTITUTION_STRUCTURE = """<pay_i:enteBeneficiario>
        <pay_i:identificativoUnivocoBeneficiario>
            <pay_i:tipoIdentificativoUnivoco>G</pay_i:tipoIdentificativoUnivoco>
            <pay_i:codiceIdentificativoUnivoco>{payee_institution_fiscal_code}</pay_i:codiceIdentificativoUnivoco>
        </pay_i:identificativoUnivocoBeneficiario>
        <pay_i:denominazioneBeneficiario>{payee_institution_name}</pay_i:denominazioneBeneficiario>
        <pay_i:codiceUnitOperBeneficiario>{payee_institution_operative_code}</pay_i:codiceUnitOperBeneficiario>
        <pay_i:denomUnitOperBeneficiario>{payee_institution_operative_denomination}</pay_i:denomUnitOperBeneficiario>
        <pay_i:indirizzoBeneficiario>{payee_institution_address}</pay_i:indirizzoBeneficiario>
        <pay_i:civicoBeneficiario>{payee_institution_address_number}</pay_i:civicoBeneficiario>
        <pay_i:capBeneficiario>{payee_institution_address_zipcode}</pay_i:capBeneficiario>
        <pay_i:localitaBeneficiario>{payee_institution_address_location}</pay_i:localitaBeneficiario>
        <pay_i:provinciaBeneficiario>{payee_institution_address_province}</pay_i:provinciaBeneficiario>
        <pay_i:nazioneBeneficiario>{payee_institution_address_nation}</pay_i:nazioneBeneficiario>
    </pay_i:enteBeneficiario>""";

RPT_TRANSFER_SET_STRUCTURE = """<pay_i:datiVersamento>
        <pay_i:dataEsecuzionePagamento>{payment_payment_date}</pay_i:dataEsecuzionePagamento>
        <pay_i:importoTotaleDaVersare>{payment_total_amount}</pay_i:importoTotaleDaVersare>
        <pay_i:tipoVersamento>{payment_payment_type}</pay_i:tipoVersamento>
        <pay_i:identificativoUnivocoVersamento>{payment_iuv}</pay_i:identificativoUnivocoVersamento>
        <pay_i:codiceContestoPagamento>{payment_ccp}</pay_i:codiceContestoPagamento>
        <pay_i:ibanAddebito>{payment_debtor_iban}</pay_i:ibanAddebito>
        <pay_i:bicAddebito>{payment_debtor_bic}</pay_i:bicAddebito>
        <pay_i:firmaRicevuta>0</pay_i:firmaRicevuta>
        {transfers}
    </pay_i:datiVersamento>"""

# All injected data refers to 'transfer' sublevel
RPT_SINGLE_TRANSFER_STRUCTURE = """<pay_i:datiSingoloVersamento>
        \t<pay_i:importoSingoloVersamento>{transfer_amount}</pay_i:importoSingoloVersamento>
        \t<pay_i:commissioneCaricoPA>{transfer_fee}</pay_i:commissioneCaricoPA>
        \t<pay_i:ibanAccredito>{transfer_creditor_iban}</pay_i:ibanAccredito>
        \t<pay_i:bicAccredito>{transfer_creditor_bic}</pay_i:bicAccredito>
        \t<pay_i:ibanAppoggio>{transfer_creditor_iban2}</pay_i:ibanAppoggio>
        \t<pay_i:bicAppoggio>{transfer_creditor_bic2}</pay_i:bicAppoggio>
        \t<pay_i:credenzialiPagatore>{transfer_payer_info}</pay_i:credenzialiPagatore>
        \t<pay_i:causaleVersamento>/RFB/{transfer_iuv}/{transfer_amount}/TXT/DEBITORE/{payer_fiscal_code}</pay_i:causaleVersamento>
        \t<pay_i:datiSpecificiRiscossione>{transfer_taxonomy}</pay_i:datiSpecificiRiscossione>
    \t</pay_i:datiSingoloVersamento>""";

# All injected data refers to 'transfer' sublevel
RPT_SINGLE_MBD_TRANSFER_STRUCTURE = """<pay_i:datiSingoloVersamento>
        \t<pay_i:importoSingoloVersamento>{transfer_amount}</pay_i:importoSingoloVersamento>
        \t<pay_i:causaleVersamento>/RFB/{transfer_iuv}/{transfer_amount}/TXT/DEBITORE/{payer_fiscal_code}</pay_i:causaleVersamento>
        \t<pay_i:datiSpecificiRiscossione>{transfer_taxonomy}</pay_i:datiSpecificiRiscossione>
        \t<pay_i:datiMarcaBolloDigitale>
            \t<pay_i:tipoBollo>{transfer_stamp_type}</pay_i:tipoBollo>
            \t<pay_i:hashDocumento>{transfer_stamp_hash}</pay_i:hashDocumento>
            \t<pay_i:provinciaResidenza>{transfer_stamp_province}</pay_i:provinciaResidenza>
        \t</pay_i:datiMarcaBolloDigitale>
    \t</pay_i:datiSingoloVersamento>""";

ACTIVATE_PAYMENT_NOTICE = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:nod="http://pagopa-api.pagopa.gov.it/node/nodeForPsp.xsd">
	<soapenv:Header />
	<soapenv:Body>
		<nod:activatePaymentNoticeV2Request>
			<idPSP>{psp}</idPSP>
			<idBrokerPSP>{psp_broker}</idBrokerPSP>
			<idChannel>{channel}</idChannel>
			<password>{password}</password>
			<idempotencyKey>{idempotency_key}</idempotencyKey>
			<qrCode>
				<fiscalCode>{fiscal_code}</fiscalCode>
				<noticeNumber>{notice_number}</noticeNumber>
			</qrCode>
			<expirationTime>900000</expirationTime>
			<amount>{amount}</amount>
			<paymentNote>{payment_note}</paymentNote>
		</nod:activatePaymentNoticeV2Request>
	</soapenv:Body>
</soapenv:Envelope>
"""

SESSION_DATA = 'session_data'
SESSION_DATA_TEST_DATA = 'test_data' #commondata.yaml
SKIP_TESTS = 'skip_tests'
PASSWORD_PLACEHOLDER = 'placeholder'

SESSION_DATA_REQ_BODY = 'flow_data.action.request.body'
SESSION_DATA_RES_BODY = 'flow_data.action.response.body'
SESSION_DATA_RES_CODE = 'flow_data.action.response.status_code'
SESSION_DATA_RES_CONTENTTYPE = 'flow_data.action.response.content_type'
SESSION_DATA_TRIGGER_PRIMITIVE = 'flow_data.action.trigger_primitive.name'

SESSION_DATA_SESSION_ID = 'flow_data.common.session_id'
SESSION_DATA_IUVS = 'flow_data.common.iuvs'
SESSION_DATA_CART_ID = 'flow_data.common.cart.id'
SESSION_DATA_CART_IS_MULTIBENEFICIARY = 'flow_data.common.cart.is_multibeneficiary'
SESSION_DATA_CART_MULTIBENEFICIARY_IUV = 'flow_data.common.cart.iuv_for_multibeneficiary'
SESSION_DATA_PAYMENT_NOTICES = 'flow_data.common.payment_notices'
SESSION_DATA_DEBT_POSITIONS = 'flow_data.common.debt_positions'
SESSION_DATA_RAW_RPTS = 'flow_data.common.rpts'
SESSION_DATA_LAST_ANALYZED_RE_EVENT = 'flow_data.common.re.last_analyzed_event'

PRIMITIVE_NODOINVIARPT = 'nodoInviaRPT'
PRIMITIVE_NODOINVIACARRELLORPT = 'nodoInviaCarrelloRPT'

OCP_APIM_SUBSCRIPTION_KEY = 'Ocp-Apim-Subscription-Key'

REQ_DESCRIPTION_EXECUTE_SOAP_CALL = 'Step: [{step}]'
REQ_DESCRIPTION_EXECUTE_CALL_TO_WISPCONV = 'Step: [{step}]: on sessionId: [{sessionId}]'
REQ_DESCRIPTION_RETRIEVE_EVENTS_FROM_RE = 'Step: [{step}]: on IUV: [{iuv}]'
REQ_DESCRIPTION_RETRIEVE_PAYMENT_POSITION = 'Step: [{step}] on IUV: [{iuv}]'
REQ_DESCRIPTION_CREATE_PAYMENT_POSITION = 'Step: [{step}]'


class ResponseType(Enum):
    XML = 1
    JSON = 2
    HTML = 3

empty_flow_data = {
    'action': {
        'request': {
            'body': {}
        },
        'response': {
            'body': {},
            'status_code': {},
            'content_type': {}
        },
        'trigger_primitive': {
            'name': {}
        }
    },
    'common': {
        'session_id': {},
        'iuvs': {},
        'cart': {
            'id': {},
            'is_multibeneficiary': {},
            'iuv_for_multibeneficiary': {}
        },
        'payment_notices': {},
        'debt_positions': {},
        'rpts': [],
        're': {
            'last_analyzed_event': {}
        }
    }
}
