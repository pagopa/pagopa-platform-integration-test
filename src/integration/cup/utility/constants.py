SOAP_ACTION_DEMAND_PAYMENT_NOTICE = "paDemandPaymentNotice"

NAMESPACE_SOAPENV = "http://schemas.xmlsoap.org/soap/envelope/"
NAMESPACE_PAFN = "http://pagopa-api.pagopa.gov.it/pa/paForNode.xsd"

DEFAULT_ID_PA = "01234567890"
DEFAULT_ID_BROKER_PA = "GPS_BROKER_ID"
DEFAULT_ID_STATION = "GPS_STATION_ID"
DEFAULT_ID_SERVIZIO = "CUP"

# XML template for paDemandPaymentNoticeRequest.
# Optional tags (istatCode, catastalCode, debtorEmail, companyName) are included only when their value is not None.
# Use build_* functions in request_builder.py instead of using this template directly.
DEMAND_PAYMENT_NOTICE_ENVELOPE = """\
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:pafn="http://pagopa-api.pagopa.gov.it/pa/paForNode.xsd">
  <soapenv:Body>
    <pafn:paDemandPaymentNoticeRequest>
      <idPA>{id_pa}</idPA>
      <idBrokerPA>{id_broker_pa}</idBrokerPA>
      <idStation>{id_station}</idStation>
      <idServizio>{id_servizio}</idServizio>
      <datiSpecificiServizioRequest>
        <cupRequest>
{cup_request_fields}
        </cupRequest>
      </datiSpecificiServizioRequest>
    </pafn:paDemandPaymentNoticeRequest>
  </soapenv:Body>
</soapenv:Envelope>"""
