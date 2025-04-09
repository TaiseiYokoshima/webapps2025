from typing import assert_type
from django.http import HttpResponseBadRequest, HttpResponseServerError

from django.http import JsonResponse
from django.views.decorators.http import require_GET


import re

from_gbp = { "EUR": 1.19, "USD": 1.29 }

from_eur = { "GBP": 0.84, "USD": 1.09 }

from_usd = { "GBP": 0.77, "EUR": 0.92 }


rates = {
        "GBP": from_gbp,
        "EUR": from_eur,
        "USD": from_usd
        }


from utils.currency import CurrencyAmount


@require_GET
def convert(request, source, target, amount):

    source = source.upper()
    target = target.upper()

    if source not in rates or target not in rates:
        return HttpResponseBadRequest("Unsupported currency")

    if source == target:
        return HttpResponseBadRequest("Cannot convert to the same currency")


    if not CurrencyAmount.parse_str_strict(amount):
        return HttpResponseBadRequest(CurrencyAmount.str_parse_error_msg)

    amount = CurrencyAmount(amount)

    if (amount == 0):
        return HttpResponseBadRequest("Cannot convert 0.00 " + source)


    assert_type(rates[source][target], float)

    rate: CurrencyAmount = CurrencyAmount(rates[source][target])
    result : CurrencyAmount = amount * rate
    result_str: str = str(result.into())
    rate_str: str = str(rate)


    return JsonResponse({'amount': result_str, "rate": rate_str})

    







