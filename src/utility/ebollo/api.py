import requests


def post_mbd(url, api_key, mbd_payload):
    response = requests.post(
        url=url,
        headers={
            'Ocp-Apim-Subscription-Key': api_key,
            'Content-Type': 'application/json'
        },
        json=mbd_payload
    )
    return response
