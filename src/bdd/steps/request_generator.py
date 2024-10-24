import base64
import json
import uuid

import session as session

from src.utility import constants
from src.utility import utils


# ==============================================

def generate_nodoinviarpt(test_data, rpt, station_password=constants.PASSWORD_PLACEHOLDER):
    payer_from_rpt = rpt['payer']
    payee_from_rpt = rpt['payee_institution']
    delegate_from_rpt = rpt['payer_delegate']
    payment = rpt['payment_data']

    payer = constants.RPT_PAYER_STRUCTURE.format(
        payer_type=payer_from_rpt['type'],
        payer_fiscal_code=payer_from_rpt['fiscal_code'],
        payer_name=payer_from_rpt['name'],
        payer_address=payer_from_rpt['address'],
        payer_address_number=payer_from_rpt['address_number'],
        payer_address_zipcode=payer_from_rpt['address_zipcode'],
        payer_address_location=payer_from_rpt['address_location'],
        payer_address_province=payer_from_rpt['address_province'],
        payer_address_nation=payer_from_rpt['address_nation'],
        payer_email=payer_from_rpt['email'],
    )
    payer_delegate = constants.RPT_PAYERDELEGATE_STRUCTURE.format(
        payer_delegate_type=delegate_from_rpt['type'],
        payer_delegate_fiscal_code=delegate_from_rpt['fiscal_code'],
        payer_delegate_name=delegate_from_rpt['name'],
        payer_delegate_address=delegate_from_rpt['address'],
        payer_delegate_address_number=delegate_from_rpt['address_number'],
        payer_delegate_address_zipcode=delegate_from_rpt['address_zipcode'],
        payer_delegate_address_location=delegate_from_rpt['address_location'],
        payer_delegate_address_province=delegate_from_rpt['address_province'],
        payer_delegate_address_nation=delegate_from_rpt['address_nation'],
        payer_delegate_email=delegate_from_rpt['email'],
    )
    payee_institution = constants.RPT_PAYEEINSTITUTION_STRUCTURE.format(
        payee_institution_fiscal_code=payee_from_rpt['fiscal_code'],
        payee_institution_name=payee_from_rpt['name'],
        payee_institution_operative_code=payee_from_rpt['operative_code'],
        payee_institution_operative_denomination=payee_from_rpt['operative_denomination'],
        payee_institution_address=payee_from_rpt['address'],
        payee_institution_address_number=payee_from_rpt['address_number'],
        payee_institution_address_zipcode=payee_from_rpt['address_zipcode'],
        payee_institution_address_location=payee_from_rpt['address_location'],
        payee_institution_address_province=payee_from_rpt['address_province'],
        payee_institution_address_nation=payee_from_rpt['address_nation'],
    )
    rpt_content = constants.RPT_STRUCTURE.format(
        creditor_institution=rpt['domain']['id'],
        station=rpt['domain']['station'],
        current_date_time=rpt['date_time_request'],
        payer_delegate=payer_delegate,
        payer=payer,
        payee_institution=payee_institution,
        payment=generate_transfers(test_data, payment)
    )
    request = constants.NODOINVIARPT_STRUCTURE.format(
        creditor_institution_broker=test_data['creditor_institution_broker'],
        creditor_institution=test_data['creditor_institution'],
        station=test_data['station'],
        psp_broker=test_data['psp_broker_wisp'],
        psp=test_data['psp_wisp'],
        channel=test_data['channel_wisp'],
        password=station_password,
        iuv=payment['iuv'],
        ccp=payment['ccp'],
        rpt=base64.b64encode(rpt_content.encode('utf-8')).decode('utf-8')
    )
    return request


# ==============================================

def generate_nodoinviacarrellorpt(test_data, cart_id, rpts, psp, psp_broker, channel, password,
                                  is_multibeneficiary=False):
    rpt_list = ''
    for rpt in rpts:
        payer_from_rpt = rpt['payer']
        payee_from_rpt = rpt['payee_institution']
        delegate_from_rpt = rpt['payer_delegate']
        payment = rpt['payment_data']

        payer = constants.RPT_PAYER_STRUCTURE.format(
            payer_type=payer_from_rpt['type'],
            payer_fiscal_code=payer_from_rpt['fiscal_code'],
            payer_name=payer_from_rpt['name'],
            payer_address=payer_from_rpt['address'],
            payer_address_number=payer_from_rpt['address_number'],
            payer_address_zipcode=payer_from_rpt['address_zipcode'],
            payer_address_location=payer_from_rpt['address_location'],
            payer_address_province=payer_from_rpt['address_province'],
            payer_address_nation=payer_from_rpt['address_nation'],
            payer_email=payer_from_rpt['email'],
        )
        payer_delegate = constants.RPT_PAYERDELEGATE_STRUCTURE.format(
            payer_delegate_type=delegate_from_rpt['type'],
            payer_delegate_fiscal_code=delegate_from_rpt['fiscal_code'],
            payer_delegate_name=delegate_from_rpt['name'],
            payer_delegate_address=delegate_from_rpt['address'],
            payer_delegate_address_number=delegate_from_rpt['address_number'],
            payer_delegate_address_zipcode=delegate_from_rpt['address_zipcode'],
            payer_delegate_address_location=delegate_from_rpt['address_location'],
            payer_delegate_address_province=delegate_from_rpt['address_province'],
            payer_delegate_address_nation=delegate_from_rpt['address_nation'],
            payer_delegate_email=delegate_from_rpt['email'],
        )
        payee_institution = constants.RPT_PAYEEINSTITUTION_STRUCTURE.format(
            payee_institution_fiscal_code=payee_from_rpt['fiscal_code'],
            payee_institution_name=payee_from_rpt['name'],
            payee_institution_operative_code=payee_from_rpt['operative_code'],
            payee_institution_operative_denomination=payee_from_rpt['operative_denomination'],
            payee_institution_address=payee_from_rpt['address'],
            payee_institution_address_number=payee_from_rpt['address_number'],
            payee_institution_address_zipcode=payee_from_rpt['address_zipcode'],
            payee_institution_address_location=payee_from_rpt['address_location'],
            payee_institution_address_province=payee_from_rpt['address_province'],
            payee_institution_address_nation=payee_from_rpt['address_nation'],
        )
        rpt_content = constants.RPT_STRUCTURE.format(
            creditor_institution=rpt['domain']['id'],
            station=rpt['domain']['station'],
            current_date_time=rpt['date_time_request'],
            payer_delegate=payer_delegate,
            payer=payer,
            payee_institution=payee_institution,
            payment=generate_transfers(test_data, payment)
        )
        rpt_list += constants.SINGLE_RPT_IN_CART.format(
            creditor_institution=rpt['domain']['id'],
            iuv=rpt['payment_data']['iuv'],
            ccp=rpt['payment_data']['ccp'],
            rpt=base64.b64encode(rpt_content.encode('utf-8')).decode('utf-8')
        )

    request = constants.NODOINVIACARRELLORPT_STRUCTURE.format(
        creditor_institution_broker=test_data['creditor_institution_broker'],
        station=test_data['station'],
        cart_id=cart_id,
        psp_broker=psp_broker,
        psp=psp,
        channel=channel,
        password=password,
        is_multibeneficiary='true' if is_multibeneficiary else 'false',
        rpt_list=rpt_list
    )
    return request


# ==============================================

def generate_transfers(test_data, payment):
    transfers_content = ''
    for transfer in payment['transfers']:

        if not transfer['is_mbd']:
            transfer_content = constants.RPT_SINGLE_TRANSFER_STRUCTURE.format(
                payer_fiscal_code=test_data['payer']['fiscal_code'],
                transfer_iuv=transfer['iuv'],
                transfer_amount='{:.2f}'.format(transfer['amount']),
                transfer_fee='{:.2f}'.format(transfer['fee']),
                transfer_creditor_iban=transfer['creditor_iban'],
                transfer_creditor_bic=transfer['creditor_bic'],
                transfer_creditor_iban2=transfer['creditor_iban'],
                transfer_creditor_bic2=transfer['creditor_bic'],
                transfer_payer_info=transfer['payer_info'],
                transfer_taxonomy=transfer['taxonomy'],
            )
        else:
            transfer_content = constants.RPT_SINGLE_MBD_TRANSFER_STRUCTURE.format(
                payer_fiscal_code=test_data['payer']['fiscal_code'],
                transfer_iuv=transfer['iuv'],
                transfer_amount='{:.2f}'.format(transfer['amount']),
                transfer_fee='{:.2f}'.format(transfer['fee']),
                transfer_payer_info=transfer['payer_info'],
                transfer_taxonomy=transfer['taxonomy'],
                transfer_stamp_type=transfer['stamp_type'],
                transfer_stamp_hash=transfer['stamp_hash'],
                transfer_stamp_province=transfer['stamp_province']
            )
        transfers_content += transfer_content

    return constants.RPT_TRANSFER_SET_STRUCTURE.format(
        payment_payment_date=payment['payment_date'],
        payment_total_amount='{:.2f}'.format(payment['total_amount']),
        payment_payment_type=payment['payment_type'],
        payment_iuv=payment['iuv'],
        payment_ccp=payment['ccp'],
        payment_debtor_iban=test_data['payer_delegate']['iban'],
        payment_debtor_bic=test_data['payer_delegate']['bic'],
        transfers=transfers_content
    )


# ==============================================

def generate_checkposition(payment_notices):
    checkposition = {'positionslist': []}
    for payment_notice in payment_notices:
        checkposition['positionslist'].append({
            'fiscalCode': payment_notice['domain_id'],
            'noticeNumber': payment_notice['notice_number']
        })
    content = json.dumps(checkposition, separators=(',', ':'))
    return content


# ==============================================

def generate_activatepaymentnotice(test_data, payment_notices, rpt, session_id,
                                   channel_checkout_password=constants.PASSWORD_PLACEHOLDER):
    iuv = rpt['payment_data']['iuv']
    total_amount = rpt['payment_data']['total_amount']
    notice_number = None
    for payment_notice in payment_notices:
        if payment_notice['iuv'] == iuv:
            notice_number = payment_notice['notice_number']
    idempotency_key = notice_number + '_' + utils.get_random_digit_string(10)

    return constants.ACTIVATE_PAYMENT_NOTICE.format(
        psp=test_data['psp_wisp'],
        psp_broker=test_data['psp_broker_wisp'],
        channel=test_data['channel_checkout'],
        password=channel_checkout_password,
        idempotency_key=idempotency_key,
        fiscal_code=payment_notice['domain_id'],
        notice_number=notice_number,
        amount='{:.2f}'.format(total_amount),
        payment_note=session_id
    )


# ==============================================

def generate_closepayment(test_data, payment_notices, rpts, outcome):
    transactionId = utils.get_random_alphanumeric_string(32)
    amount = round(sum(rpt['payment_data']['total_amount'] for rpt in rpts), 2)
    fees = round(sum(rpt['payment_data']['total_fee'] for rpt in rpts), 2)
    grand_total = round((amount + fees) * 100, 2)
    auth_code = utils.get_random_digit_string(6)
    rrn = utils.get_random_digit_string(12)
    now = utils.get_current_datetime() + '.000Z'

    closepayment = {
        'paymentTokens': [payment_notice['payment_token'] for payment_notice in payment_notices],
        'outcome': outcome,
        'idPSP': 'BCITITMM',
        'idBrokerPSP': '00799960158',
        'idChannel': test_data['channel_payment'],
        'paymentMethod': 'CP',
        'transactionId': transactionId,
        'totalAmount': round(grand_total / 100, 2),
        'fee': fees,
        'timestampOperation': now,
        'transactionDetails': {
            'transaction': {
                'transactionId': transactionId,
                'transactionStatus': 'Confermato',
                'creationDate': now,
                'grandTotal': int(grand_total),
                'amount': int(amount * 100),
                'fee': int(fees * 100),
                'authorizationCode': auth_code,
                'rrn': rrn,
                'psp': {
                    'idPsp': test_data['psp_payment'],
                    'idChannel': test_data['channel_payment'],
                    'businessName': test_data['psp_name'],
                    'brokerName': test_data['psp_broker_payment'],
                    'pspOnUs': False
                },
                'timestampOperation': now,
                'paymentGateway': 'NPG'
            },
            'info': {
                'type': 'CP',
                'brandLogo': 'https://assets.cdn.platform.pagopa.it/creditcard/mastercard.png',
                'brand': 'MC',
                'paymentMethodName': 'CARDS',
                'clientId': 'CHECKOUT'
            },
            'user': {
                'type': 'GUEST'
            }
        },
        'additionalPaymentInformations': {
            'outcomePaymentGateway': outcome,
            'fee': '{:.2f}'.format(fees),
            'totalAmount': '{:.2f}'.format(grand_total / 100),
            'timestampOperation': now,
            'rrn': rrn,
            'authorizationCode': auth_code,
            'email': 'test@mail.it'
        }
    }

    content = json.dumps(closepayment, separators=(',', ':'))
    return content


# ==============================================

def create_rpt(test_data, iuv, ccp, domain_id, payee_institution, payment_type, number_of_transfers, number_of_mbd=0):
    payer_info = 'CP1.1'
    taxonomy_simple_transfer = '9/0301109AP'
    taxonomy_stamp_transfer = '9/0301116TS/9/24B0060000000017'
    payment_description = '/RFB/{iuv}/{amount:.2f}/TXT/DEBITORE/{fiscal_code}'
    iuv = utils.generate_iuv() if iuv is None else iuv
    payer_delegate = test_data['payer_delegate']
    transfers = []

    no_mbd_transfers = number_of_transfers - number_of_mbd
    for i in range(number_of_transfers):

        amount = utils.generate_random_monetary_amount(10.00, 599.99)
        transfer_note = payment_description.format(
            iuv=iuv,
            amount=amount,
            fiscal_code=test_data['payer']['fiscal_code']
        )

        # generating simple transfer
        if no_mbd_transfers > 0:
            transfers.append({
                'iuv': iuv,
                'amount': amount,
                'fee': utils.generate_random_monetary_amount(0.10, 2.50),
                'creditor_iban': payee_institution['iban'],
                'creditor_bic': payee_institution['bic'],
                'payer_info': f'{payer_info} - Transfer {i}',
                'taxonomy': taxonomy_simple_transfer,
                'transfer_note': transfer_note,
                'is_mbd': False
            })
            no_mbd_transfers -= 1

        # generating MBD transfer
        else:
            transfers.append({
                'iuv': iuv,
                'amount': 16.00,
                'fee': utils.generate_random_monetary_amount(0.10, 0.50),
                'stamp_hash': 'cXVlc3RhIMOoIHVuYSBtYXJjYSBkYSBib2xsbw==',
                'stamp_type': '01',
                'stamp_province': 'RM',
                'payer_info': f'{payer_info} - MBD for transfer {i}',
                'taxonomy': taxonomy_stamp_transfer,
                'transfer_note': transfer_note,
                'is_mbd': True
            })

    total_amount = round(sum(transfer['amount'] for transfer in transfers), 2)
    payment_note = payment_description.format(
        iuv=iuv,
        amount=total_amount,
        fiscal_code=test_data['payer']['fiscal_code']
    )

    rpt = {
        'domain': {
            'id': domain_id,
            'name': payee_institution['name'],
            'station': test_data['station']
        },
        'date_time_request': utils.get_current_datetime(),
        'payer': test_data['payer'],
        'payer_delegate': payer_delegate,
        'payee_institution': payee_institution,
        'payment_data': {
            'iuv': iuv,
            'ccp': utils.generate_ccp() if ccp is None else ccp,
            'payment_date': utils.get_current_date(),
            'total_amount': total_amount,
            'total_fee': round(sum(transfer['fee'] for transfer in transfers), 2),
            'payment_type': payment_type,
            'debtor_iban': payer_delegate['iban'],
            'debtor_bic': payer_delegate['bic'],
            'payment_note': payment_note,
            'transfers': transfers
        }
    }

    return rpt


# ==============================================

def generate_gpd_paymentposition(context, rpt, segregation_code, payment_status):
    payment_positions = session.get_flow_data(context, constants.SESSION_DATA_DEBT_POSITIONS)
    if payment_positions is None:
        payment_positions = []

    payment_data = rpt['payment_data']
    payer = rpt['payer']

    iuv = payment_data['iuv']
    total_amount = payment_data['total_amount']
    domain_id = rpt['domain']['id']
    fiscal_code = payer['fiscal_code']
    nav = utils.generate_nav(segregation_code)
    extracted_transfers = payment_data['transfers']

    transfers = []
    transfer_index = 1
    for extracted_transfer in extracted_transfers:
        iban = extracted_transfer['creditor_iban'] if 'creditor_iban' in extracted_transfer else None
        stamp = None if not extracted_transfer['is_mbd'] else {
            'stampType': extracted_transfer['stamp_type'],
            'hashDocument': extracted_transfer['stamp_hash'],
            'provincialResidence': extracted_transfer['stamp_province']
        }
        transfers.append({
            'idTransfer': transfer_index,
            'amount': round(extracted_transfer['amount'] * 100),
            'organizationFiscalCode': domain_id,
            'remittanceInformation': extracted_transfer['transfer_note'],
            'category': extracted_transfer['taxonomy'],
            'iban': iban,
            'postalIban': iban if iban is not None and iban[5:10] == '07601' else None,
            'stamp': stamp,
            'transferMetadata': [
                {
                    'key': 'DatiSpecificiRiscossione',
                    'value': extracted_transfer['taxonomy']
                }
            ]
        })
        transfer_index += 1

    payment_position = {
        'iupd': f'wisp_{domain_id}_{uuid.uuid4()}',
        'type': 'F',
        'payStandIn': False,
        'fiscalCode': fiscal_code,
        'fullName': payer['name'],
        'streetName': payer['address'],
        'civicNumber': payer['address_number'],
        'postalCode': payer['address_zipcode'],
        'city': payer['address_location'],
        'province': payer['address_province'],
        'region': None,
        'country': payer['address_nation'],
        'email': payer['email'],
        'phone': None,
        'switchToExpired': False,
        'companyName': rpt['domain']['name'],
        'officeName': None,
        'validityDate': None,
        'paymentDate': None,
        'pull': False,
        'status': f'{payment_status}',
        'paymentOption': [
            {
                'nav': nav,
                'iuv': iuv,
                'amount': round(total_amount * 100),
                'description': f'/RFB/{iuv}/{total_amount}/TXT/DEBITORE/{fiscal_code}',
                'isPartialPayment': False,
                'dueDate': f'{utils.get_tomorrow_datetime()}.000000000',
                'retentionDate': None,
                'fee': 0,
                'notificationFee': None,
                'transfer': transfers,
                'paymentOptionMetadata': None
            }
        ]
    }
    payment_positions.append(payment_position)
    content = json.dumps({'paymentPositions': payment_positions}, separators=(',', ':'))
    return content

# ==============================================
