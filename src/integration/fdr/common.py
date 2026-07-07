from datetime import date

def check_health(context):
    fdr_base_url = context.config.fdr_base_url
    fdr_health_endpoint = f"{fdr_base_url}/health"
    response = context.fdr.rest.client.get(fdr_health_endpoint)
    assert response.httpStatusCode == 200, f"Health check failed with status code {response.status_code} and response: {response.text}"

def build_create_fdr_request_payload(context):
    # Build the request payload for creating a new flow structure
    context.request_date = date.today().isoformat();
    return {
        "fdr": [
            f"{context.fdr_id}"
        ],
        "fdrDate": [
            f"{context.request_date}"
        ],
        "sender": {
            "type": f"{context.psp.type}",
            "id": [
            f"{context.sender.id}"
            ],
            "pspId": [
            f"{context.sender.psp_id}"
            ],
            "pspName": [
            f"{context.sender.name}"
            ],
            "pspBrokerId": [
            f"{context.sender.broker_id}"
            ],
            "channelId": [
            f"{context.sender.channel_id}"
            ]
        },
        "receiver": {
            "id": [
            f"{context.receiver.id}"
            ],
            "organizationId": [
            f"{context.receiver.organization_id}"
            ],
            "organizationName": [
            f"{context.receiver.organization_name}"
            ]
        },
        "regulation": [
            "SEPA - Bonifico X"
        ],
        "regulationDate": f"{context.request_date}",
        "bicCodePouringBank": [
            f"{context.bic_code_pouring_bank}"
        ],
        "totPayments": [
            f"{context.tot_payments}"
        ],
        "sumPayments": [
            f"{context.sum_payments}"
        ]
    }

def create_fdr(context, fdr_id, psp_id):
    pass

def insert_payments(context, tot_payments, sum_payments):
    pass

def publish_fdr(context):
    pass