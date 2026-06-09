"""Build paDemandPaymentNoticeRequest XML bodies for the CUP test suite.

Each build_* function returns a complete SOAP envelope as a UTF-8 string.
Optional fields (istatCode, catastalCode, debtorEmail, companyName) are
omitted from the XML when passed as None or empty string.
"""
from .constants import (
    DEMAND_PAYMENT_NOTICE_ENVELOPE,
    DEFAULT_ID_PA,
    DEFAULT_ID_BROKER_PA,
    DEFAULT_ID_STATION,
    DEFAULT_ID_SERVIZIO,
)


def _tag(name: str, value) -> str:
    """Return an XML tag line or empty string if value is falsy."""
    if value is None or str(value).strip() == '':
        return ''
    return f'          <{name}>{value}</{name}>'


def _build_envelope(
    id_pa: str,
    id_broker_pa: str,
    id_station: str,
    id_servizio: str,
    organization_fiscal_code,
    istat_code,
    catast_code,
    debtor_fiscal_code,
    debtor_full_name,
    debtor_email,
    company_name,
    amount,
) -> str:
    fields_lines = [
        _tag('organizationFiscalCode', organization_fiscal_code),
        _tag('istatCode', istat_code),
        _tag('catastalCode', catast_code),
        _tag('debtorFiscalCode', debtor_fiscal_code),
        _tag('debtorFullName', debtor_full_name),
        _tag('debtorEmail', debtor_email),
        _tag('companyName', company_name),
        _tag('amount', amount),
    ]
    cup_request_fields = '\n'.join(line for line in fields_lines if line)
    return DEMAND_PAYMENT_NOTICE_ENVELOPE.format(
        id_pa=id_pa,
        id_broker_pa=id_broker_pa,
        id_station=id_station,
        id_servizio=id_servizio,
        cup_request_fields=cup_request_fields,
    )


def build_happy_path(
    organization_fiscal_code: str = '01234567890',
    debtor_fiscal_code: str = '00588460050',
    debtor_full_name: str = 'TIM S.p.A.',
    debtor_email: str = 'amministrazione@tim.it',
    company_name: str = 'TIM',
    amount: str = '80.00',
    id_pa: str = DEFAULT_ID_PA,
    id_broker_pa: str = DEFAULT_ID_BROKER_PA,
    id_station: str = DEFAULT_ID_STATION,
) -> str:
    return _build_envelope(
        id_pa=id_pa, id_broker_pa=id_broker_pa, id_station=id_station,
        id_servizio=DEFAULT_ID_SERVIZIO,
        organization_fiscal_code=organization_fiscal_code,
        istat_code=None, catast_code=None,
        debtor_fiscal_code=debtor_fiscal_code,
        debtor_full_name=debtor_full_name,
        debtor_email=debtor_email, company_name=company_name, amount=amount,
    )


def build_multi_identificativo(
    organization_fiscal_code=None,
    istat_code=None,
    catast_code=None,
    debtor_fiscal_code: str = '00588460050',
    debtor_full_name: str = 'TIM S.p.A.',
    debtor_email: str = 'amministrazione@tim.it',
    company_name: str = 'TIM',
    amount: str = '80.00',
    id_pa: str = DEFAULT_ID_PA,
    id_broker_pa: str = DEFAULT_ID_BROKER_PA,
    id_station: str = DEFAULT_ID_STATION,
) -> str:
    return _build_envelope(
        id_pa=id_pa, id_broker_pa=id_broker_pa, id_station=id_station,
        id_servizio=DEFAULT_ID_SERVIZIO,
        organization_fiscal_code=organization_fiscal_code,
        istat_code=istat_code, catast_code=catast_code,
        debtor_fiscal_code=debtor_fiscal_code,
        debtor_full_name=debtor_full_name,
        debtor_email=debtor_email, company_name=company_name, amount=amount,
    )


def build_identificativo_formato_errato(
    organization_fiscal_code=None,
    istat_code=None,
    catast_code=None,
    debtor_fiscal_code: str = '00588460050',
    debtor_full_name: str = 'TIM S.p.A.',
    debtor_email: str = 'amministrazione@tim.it',
    company_name: str = 'TIM',
    amount: str = '80.00',
    id_pa: str = DEFAULT_ID_PA,
    id_broker_pa: str = DEFAULT_ID_BROKER_PA,
    id_station: str = DEFAULT_ID_STATION,
) -> str:
    return _build_envelope(
        id_pa=id_pa, id_broker_pa=id_broker_pa, id_station=id_station,
        id_servizio=DEFAULT_ID_SERVIZIO,
        organization_fiscal_code=organization_fiscal_code,
        istat_code=istat_code, catast_code=catast_code,
        debtor_fiscal_code=debtor_fiscal_code,
        debtor_full_name=debtor_full_name,
        debtor_email=debtor_email, company_name=company_name, amount=amount,
    )


def build_campi_obbligatori_mancanti(
    organization_fiscal_code: str = '01234567890',
    debtor_fiscal_code=None,
    debtor_full_name=None,
    debtor_email: str = 'amministrazione@tim.it',
    company_name: str = 'TIM',
    amount=None,
    id_pa: str = DEFAULT_ID_PA,
    id_broker_pa: str = DEFAULT_ID_BROKER_PA,
    id_station: str = DEFAULT_ID_STATION,
) -> str:
    return _build_envelope(
        id_pa=id_pa, id_broker_pa=id_broker_pa, id_station=id_station,
        id_servizio=DEFAULT_ID_SERVIZIO,
        organization_fiscal_code=organization_fiscal_code,
        istat_code=None, catast_code=None,
        debtor_fiscal_code=debtor_fiscal_code,
        debtor_full_name=debtor_full_name,
        debtor_email=debtor_email, company_name=company_name, amount=amount,
    )


def build_formato_campo_errato(
    organization_fiscal_code: str = '01234567890',
    debtor_fiscal_code=None,
    debtor_full_name: str = 'TIM S.p.A.',
    debtor_email: str = 'amministrazione@tim.it',
    company_name: str = 'TIM',
    amount=None,
    id_pa: str = DEFAULT_ID_PA,
    id_broker_pa: str = DEFAULT_ID_BROKER_PA,
    id_station: str = DEFAULT_ID_STATION,
) -> str:
    return _build_envelope(
        id_pa=id_pa, id_broker_pa=id_broker_pa, id_station=id_station,
        id_servizio=DEFAULT_ID_SERVIZIO,
        organization_fiscal_code=organization_fiscal_code,
        istat_code=None, catast_code=None,
        debtor_fiscal_code=debtor_fiscal_code,
        debtor_full_name=debtor_full_name,
        debtor_email=debtor_email, company_name=company_name, amount=amount,
    )


def build_non_in_cache(
    organization_fiscal_code=None,
    istat_code=None,
    catast_code=None,
    debtor_fiscal_code: str = '00588460050',
    debtor_full_name: str = 'TIM S.p.A.',
    debtor_email: str = 'amministrazione@tim.it',
    company_name: str = 'TIM',
    amount: str = '80.00',
    id_pa: str = DEFAULT_ID_PA,
    id_broker_pa: str = DEFAULT_ID_BROKER_PA,
    id_station: str = DEFAULT_ID_STATION,
) -> str:
    return _build_envelope(
        id_pa=id_pa, id_broker_pa=id_broker_pa, id_station=id_station,
        id_servizio=DEFAULT_ID_SERVIZIO,
        organization_fiscal_code=organization_fiscal_code,
        istat_code=istat_code, catast_code=catast_code,
        debtor_fiscal_code=debtor_fiscal_code,
        debtor_full_name=debtor_full_name,
        debtor_email=debtor_email, company_name=company_name, amount=amount,
    )
