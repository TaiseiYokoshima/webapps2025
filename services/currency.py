import requests
from http import HTTPStatus

from accounts.models import Account


from utils.currency import CurrencyAmount


# set this external api url string to use an external api to get the currency conversion
# if protocol is not specified it uses https
# to use internal api keep it None
external_api_url = None


CURRENCIES = list(Account.CURRENCIES.keys())

class ConversionAPIError(Exception):
    pass


def build_request(request, source: str, target: str, amount: str) -> str:
    url = None

    if external_api_url is not None:
        url = external_api_url

        if "https://" not in url and "http://" not in url:
            url = "https://" + url
    else:
        url = request.get_host().replace("https://", "").replace("http://", "")
        protocol = "https://" if request.is_secure() else "http://"
        url = protocol + url


    if source not in CURRENCIES or target not in CURRENCIES:
        raise ValueError("Unsupported currency")

    if source == target:
        raise ValueError("Cannot convert to the same currency")

    parsed = CurrencyAmount(amount)

    if (parsed == 0):
        raise ValueError("Cannot convert 0.00 " + source)

    return f"{url}/conversion/{source}/{target}/{amount}"



def call_conversion_api(request, source: str, target: str, amount: str):

    url = build_request(request, source, target, amount)
    response = requests.get(url, timeout=1)


    if response.status_code == 200:
        return response.json()["result"]


    if response.status_code == HTTPStatus.BAD_REQUEST:
        msg = response.content.decode()
        raise ValueError(msg)
    else:
        raise ConversionAPIError(f"code: {response.status_code}\nurl:\n{url}")




