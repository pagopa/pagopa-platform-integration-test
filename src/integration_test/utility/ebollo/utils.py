import base64
import hashlib
import os
import random

from faker import Faker

fake = Faker('it_IT')


def generate_mbd_payload(first_name='', last_name='', fiscal_code='', amount=0, document_hash='',
                         email='example@example.com', province='RO', id_ci_service='00005',
                         success_url='https://success.com/', cancel_url='https://cancel.com/', error_url='https://error.com/'):
    if not first_name:
        first_name = fake.name().split(' ')[0]

    if not last_name:
        last_name = fake.name().split(' ')[1]

    if not fiscal_code:
        fiscal_code = fake.ssn()

    if not amount:
        amount = round(random.uniform(0, 99999), 2)

    if not document_hash:
        document_hash = generate_random_document_hash()

    payload = {
        'paymentNotices': [
            {
                'firstName': first_name,
                'lastName': last_name,
                'fiscalCode': fiscal_code,
                'email': email,
                'amount': amount,
                'province': province,
                'documentHash': document_hash
            }
        ],
        'idCIService': id_ci_service,
        'returnUrls': {
            'successUrl': success_url,
            'cancelUrl': cancel_url,
            'errorUrl': error_url
        }
    }
    return payload


def generate_random_document_hash():
    dummy_document_content = os.urandom(512)

    sha256_hash = hashlib.sha256(dummy_document_content).digest()

    base64_encoded_hash = base64.b64encode(sha256_hash)

    result = base64_encoded_hash.decode('utf-8').replace('\n', '')

    return result
