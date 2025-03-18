import requests
from http import HTTPStatus

from accounts.models import Account
from utils.currency import invalid_amount_string


base_url = None


CURRENCIES = list(Account.CURRENCIES.keys())

class ConversionAPIError(Exception):
    pass


def build_request(request, source: str, target: str, amount: str) -> str:
    url = None
    protocol = "https://"


    if base_url is not None:
        url = protocol + base_url
    else:
        url = request.get_host()
        protocol = protocol if request.is_secure() else "http://"
        url = protocol + url + "/conversion"


    if source not in CURRENCIES or target not in CURRENCIES:
        raise ValueError("Unsupported currency")

    if source == target:
        raise ValueError("Cannot convert to the same currency")


    if (invalid_amount_string(amount)):
        raise ValueError("Invalid value for amount")

    if (float(amount) == 0):
        raise ValueError("Invalid value for amount")


    return f"{url}/{source}/{target}/{amount}"



def call_conversion_api(request, source: str, target: str, amount: str):
    url = build_request(request, source, target, amount)
    response = requests.get(url, timeout=1)

    if response.status_code == 200:
        return response.json()["result"]


    if response.status_code == HTTPStatus.BAD_REQUEST:
        msg = response.content.decode()
        raise ValueError(msg)
    else:
        raise ConversionAPIError




